# Spring AOP 日志

预备知识
* Java 反射
* 注解操作
* 前置通知
* 后置通知
* JoinPoint

## 第一部分 —— 数据库与表结构

#### 1 日志表信息描述 sysLog

SysLog 对象的 syslog 表单

| 序号 | 字段名称   | 字段类型      | 字段描述
| :-:  | :-:       | :-:          | :-: 
| 1    | id        | varchar(36)  | 主键，无意义 uuid
| 2    | visitTime | timestamp    | 访问时间
| 3    | username  | varchar(50)  | 操作者用户名
| 4    | ip        | varchar(30)  | 访问 ip
| 5    | url       | varchar(100) | 访问资源 url
| 6    | executionTime | int      | 执行时长
| 7    | method    | varchar(200) | 访问方法

sql 语句
```sql
create table syslog (
    id varchar(36) PRIMARY KEY,  -- default uuid()
    visitTime timestamp,
    username varchar(50),
    ip varchar(30),
    url varchar(100),
    executionTime int,
    method varchar(200)
);
```

实体类
```java
public class SysLog {
    private String id;
    private Date visitTime;
    private String visitTimeStr;
    private String username;
    private String ip;
    private String url;
    private Long executionTime;
    private String method;
}
```

## 第二部分 —— 基于 AOP 日志处理

#### 1 创建切面类处理日志
LogAop.java （也可以叫 SysLogController.java） ``注意，一般的 Sevlet Controller 是 @Controller + @RequestMapping("")，而 AOP 功能的 Controller 是 @Component + @Aspect 。``
```java
package com.petersdemo.ssm.controller;

import com.petersdemo.ssm.domain.SysLog;
import com.petersdemo.ssm.service.ISysLogService;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.servlet.http.HttpServletRequest;
import java.lang.reflect.Method;
import java.util.Date;

@Component
@Aspect
public class LogAop {

    @Autowired
    private HttpServletRequest request;

    @Autowired
    private ISysLogService sysLogService;

    private Date visitTime;  //访问时间
    private Class executionClass;  //访问的类
    private Method executionMethod; //访问的方法
    // 主要获取访问时间、访问的类、访问的方法

    // 前置通知： 拦截 com.petersdemo.ssm.controller 下的所有方法
    @Before("execution(* com.petersdemo.ssm.controller.*.*(..))")
    public void doBefore(JoinPoint jp) throws NoSuchMethodException, SecurityException {
        visitTime = new Date();  //访问时间
        // 获取访问的类
        executionClass = jp.getTarget().getClass();
        // 获取访问的方法
        String methodName = jp.getSignature().getName();  //获取访问的方法的名称

        Object[] args = jp.getArgs();  //获取访问的方法的参数
        if (args == null || args.length == 0) {  //无参数
            executionMethod = executionClass.getMethod(methodName);  //只能获取无参数方法
        }
        else {  //有参数
            // 将 args 中所有元素遍历，获取对应的 Class，装入到一个 Class[]
            Class[] classArgs = new Class[args.length];
            for (int i = 0; i < args.length; i++) {
                classArgs[i] = args[i].getClass();
            }
            executionMethod = executionClass.getMethod(methodName, classArgs);  //获取有参数的方法
        }
    }

    // 后置通知： 主要获取日志中的其他信息，时长、ip、url ...
    @After("execution(* com.petersdemo.ssm.controller.*.*(..))")
    public void doAfter(JoinPoint jp) throws Exception {

        // 获取访问时长
        long executionTime = new Date().getTime() - visitTime.getTime();
        // 获取 url
        String url = "";

        // 获取访问的 url （需要通过反射来完成操作）
        if (executionClass != null && executionMethod != null && executionClass != LogAop.class) {
            // 获取类上的 @RequestMapping 对象
            RequestMapping classAnnotation = (RequestMapping) executionClass.getAnnotation(RequestMapping.class);
            if (classAnnotation != null) {
                String[] classValue = classAnnotation.value();

                // 获取方法上的 @RequestMapping 对象
                RequestMapping methodAnnotation = executionMethod.getAnnotation(RequestMapping.class);
                if (methodAnnotation != null) {
                    String[] methodValue = methodAnnotation.value();
                    // url
                    url = classValue[0] + methodValue[0];
                }
            }
        }

        // 获取访问的 ip 地址 （通过 request 对象获取）
        // 在 web.xml 中配置一个 listener RequestContextListener
        //<!-- 配置监听器，监听 request 域对象的创建和销毁 -->
        //<listener>
        //<listener-class>org.springframework.web.context.request.RequestContextListener</listener-class>
        //</listener>
        // 此时，在类中添加 @Autowired private HttpServletRequest request; 即可获取 request 对象。
        String ip = request.getRemoteAddr();

        // 获取当前操作的用户 （可以通过 Spring Security 提供的一个 SecurityContext 对象获取）
        SecurityContext context = SecurityContextHolder.getContext();  //从上下文中获取当前登陆的用户
        User user = (User) context.getAuthentication().getPrincipal();
        String username = user.getUsername();
        // 也可以从 request.getSession 中获取上下文。 从 session 中获取。
        // request.getSession().getAttribute("SPRING_SECURITY_CONTEXT");

        // 将日志相关信息封装到 SysLog 对象
        SysLog sysLog = new SysLog();
        sysLog.setVisitTime(visitTime);
        sysLog.setUsername(username);
        sysLog.setIp(ip);
        sysLog.setUrl(url);
        sysLog.setExecutionTime(executionTime);
        sysLog.setMethod("[类名]"+ executionClass.getName() + "[方法名]"+executionMethod.getName());

        //调用 ISysLogService，调用 Dao 将 sysLog insert 数据库
        sysLogService.save(sysLog);
    }
}
```

注意，HttpServletRequest 需要依赖 servlet-api 依赖包。
```xml
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>4.0.1</version>
</dependency>
```

#### 2 Service
ISysLogService.java
```java
package com.petersdemo.ssm.service;

import com.petersdemo.ssm.domain.SysLog;

public interface ISysLogService {
    public void save (SysLog sysLog) throws Exception;
}
```
SysLogServiceImple.java
```java
package com.petersdemo.ssm.service.impl;

import com.petersdemo.ssm.dao.ISysLogDao;
import com.petersdemo.ssm.domain.SysLog;
import com.petersdemo.ssm.service.ISysLogService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class SysLogServiceImpl implements ISysLogService {

    @Autowired
    private ISysLogDao sysLogDao;

    @Override
    public void save(SysLog sysLog) throws Exception {
        sysLogDao.save(sysLog);
    }
}
```

#### 3 Dao
ISysLogDao.java
```java
package com.petersdemo.ssm.dao;

import com.petersdemo.ssm.domain.SysLog;
import org.apache.ibatis.annotations.Insert;

public interface ISysLogDao {

    @Insert("insert into syslog(id, visitTime, username, ip, url, executionTime, method)" +
            "values(uuid(), #{visitTime}, #{username}, #{ip}, #{url}, #{executionTime}, #{method})")
    public void save(SysLog sysLog) throws Exception;
}
```

# 知识回顾

#### 1 Java 反射机制

##### 1.1 反射机制的出发点
Java 反射机制是指在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法。因此，对于任何一个对象，就可以获取到它的所有方法并调用。

###### 这种动态获取信息以及动态调用对象方法的功能称为 java 语言的反射机制。

##### 1.2 反射可以做什么？
* 可以动态创建对象，根据类名字符串就可创建对象，如： Spring 中动态创建 Bean。
* 可以根据一个字符串得到一个类，如： ``Class classA = Class.forName("java.lang.String");``。

##### 1.3 与 Java 反射相关的类
* Class 类，代表类的实体，在运行的 Java 应用程序中表示类和接口。
* Field 类，代表类的成员变量（成员变量也称为类的属性）。
* Method 类，代表类的方法。
* Constructor 类，代表类的构造方法。

#### 2 注解操作
注解（Annotation），也叫元数据。一种代码级别的说明。它是 JDK1.5 及以后版本引入的一个特性，与类、接口、枚举是在同一个层次。它可以声明在包、类、字段、方法、局部变量、方法参数等的前面，用来对这些元素进行说明和注释。 使用方式： ``@注解名称``。

##### 2.1 注解可以干什么
* 编写文档：通过代码里标识的注解生成文档【生成doc文档】。
* 代码分析：通过代码里标识的注解对代码进行分析【使用反射】。
* 编译检查：通过代码里标识的注解让编译器能够实现基本的编译检查【Override】。

综上，Annotation 是一个辅助类，它在 Junit、Struts、Spring 等工具框架中被广泛使用。

##### 2.2 自定义注解
格式：
```
元注解
public @interface 注解名称 {
	属性列表;
}
```

注意，注解本质上就是一个接口，该接口默认继承 Annotation 接口。属性的返回值类型有下列取值：
* 基本数据类型
* String 类型
* 枚举
* 注解 （定义时不要带`@`）
* 以上类型的数组
* 返回值不能是void

示例：
```java
public @interface MyCustomAnnotation {
    int age();      //注意，不能带参数，因此 age(int x) 是不行的。
    //int age() default 18;  //定义带默认值的属性
    String name();
    MyAnno2 anno(); //注解
    Animal dog();   //枚举 DOG, CAT
    int[] arrs();
}
```
注意，定义了属性，在使用时就必须给属性赋值。除非定义属性时，使用 default 关键字给属性默认初始化值。
* 数组赋值时，值使用{}包裹。如果数组中只有一个值，则{}可以省略。
* 如果注解只有一个属性需要赋值，并且属性的名称是value，则value可以省略，直接定义值即可。如：Spring 中 ``@RequestMapping("/product")``。

##### 2.3 元注解
元注解：用于描述注解的注解。
* @Target：描述注解能够作用的位置。几个常用的取值如下：
    * TYPE：可以作用于类上。
    * METHOD：可以作用于方法上。
    * FIELD：可以作用于成员变量上。
    * 其他等等。
* @Retention：描述注解被保留的阶段，三个阶段。
    * SOURCE 仅会保留到源码阶段。
    * CLASS 可以保留到字节码文件中，并被JVM读取到。
    * RUNTIME 会保留到编译阶段。
* @Documented 标记这些注解是否包含在用户文档中。
* @Inherited 标记这个注解是继承于哪个注解类(默认：注解并没有继承于任何子类)

##### 2.4 解析注解
解析注解，即：在程序运行时获取注解中定义的属性值，以替代反射中使用的配置文件。（配置文件中指定类名和方法名。）

例如： Spring 中获取 Service 的方法上的注解对象
```java
// 获取类上的 @RequestMapping 对象
RequestMapping classAnnotation = (RequestMapping) executionClass.getAnnotation(RequestMapping.class);
// 获取方法上的 @RequestMapping 对象
RequestMapping methodAnnotation = (RequestMapping) executionMethod.getAnnotation(RequestMapping.class);
```

##### 2.5 常用注解
* @Override 提示被标注的方法重载了父类的方法。
* @Deprecated 如果开发人员正在调用一个过时的方法、类或成员变量时，可以用该注解进行标注。
* @SuppressWarnings 并不是一个标记类型注解，它可以阻止警告的提示。它有一个类型为 String[] 的成员，其值为被禁止的警告名。

关于注解的详细介绍，请参考：
* http://www.runoob.com/w3cnote/java-annotation.html
* http://www.jianshu.com/p/17a7a5983493

#### 3 注解与 XML 的利弊
以前，XML 是各大框架的青睐者，它以松耦合的方式完成了框架中几乎所有的配置。但是，随着项目越来越庞大，XML 的内容会越来越复杂，维护成本就会变高。
于是，就有人提出来一种标记式高耦合的配置方式，注解。方法上可以进行注解，类上可以注解，字段属性上也可以注解，反正几乎需要配置的地方都可以进行注解。

利弊：
* 注解提供了更大的便捷性，写代码时任何需要配置的地方直接写注解，OK了。但是，耦合度高。
* XML 相对于注解则是正好相反的。需要专门维护一个配置文件，但是完美的松耦合。

#### 4 