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

#### 4 动态代理技术
Java 中的动态代理技术是面向切面编程的一种思想。（aop）

##### 4.1 动态代理技术的思想模型及出发点
```
A接口：doSomething()
  | 实现类
B类（A的实现类）：doSomething()
  | Proxy类
B的Proxy类（简单说，就是当需要调B.doSomething()的时候，不要直接使用B，而是调Proxy.doSomething()。）
```
注意 Proxy.doSomething() 的实现：
```java
public void doSomething() {
    try {
        doOtherthingA();   //B.doSomething 执行前
        B.doSomething();   //执行 B.doSomething() 【不管怎么说，执行B.doSomething()才是函数被invoke的主要原因】
        doOtherthingB();   //B.doSomething 执行后
    }
    catch(Exception e) {
        doOtherthingC();   //执行发生任何异常时
    }
    finally {
        doOtherthingD();   //finally中一定要执行的
    }
    //当然，还可以在这个代理函数里加很多很多 doOtherthing。。。
}
```

##### 4.2 动态代理可以做什么？
* 在操作数据库之前，我们需要开启事物，当操作完毕之后还要提交事物，发生异常事务回滚。
    * 现在，请在每个已有的数据库操作前后都添上事务支持。。呵呵哒。
    * 使用动态代理，就可以只写一份代理类代码就 OK 了。

* 动态代理在 Java 开发中有着广泛的应用，如：
    * Spring AOP
    * Hibernate 数据查询
    * 测试框架的后端 mock
    * RPC 远程调用
    * Java 注解对象获取
    * 日志
    * 用户鉴权
    * 全局性异常处理
    * 性能监控
    * 事务处理等

综上，可以看出 Java 的动态代理技术和 Python 的装饰器的功能作用一样。 ``需要注意的是，Java动态代理与Java反射机制关系紧密。``

##### 4.3 为什么称为动态代理？
注意，你在定义的时候，是分别定义接口实现类和代理类，而代理类实现的都是doOtherthing的代码，是不可能把实现类的函数实现拿进来的。

基于以上特点，Java 虚拟机将 Proxy 类和普通类区别对待。 Proxy 类与普通类的唯一区别就是其字节码是由 JVM 在运行时动态生成的而非预存在于任何一个 .class 文件中。

##### 4.4 补充：静态代理的缺点 （即：GoF代理模式的缺点）
静态代理实现之后，代码编译的时候会生成代理类的字节码。 但核心的缺陷是：
* 由于代理类要实现与目标对象一致的接口，如果被代理对象很多，接口又不同，那么就需要写很多代理类。
* 此时的方案有两种：``只维护一个代理类，但这个代理类实现多个接口`` 或 ``新建多个代理类，每个目标对象都对应一个代理类``。

另外，注意：当被代理对象的接口需要增加、删除、修改的时候。。静态的代理类要同步修改。。改到怀疑人生。

##### 4.5 应用示例
查看文档后面的 “[银行转账案例](#银行转账案例)”。

#### 5 Spring AOP
AOP：全称是 Aspect Oriented Programming 即：面向切面编程。 简单的说，它就是把我们程序重复的代码抽取出来，在需要执行的时候，使用动态代理的技术，在不修改源码的情况下，对我们的已有方法进行增强（附加新功能，就像Python的装饰器对被装饰方法的增强一样）。

* Spring 基于 XML 的 AOP。
* Spring 基于注解的 AOP。
* 在实际使用中应注意：切入点表达式的写法，常用通知类型，环绕通知。

#### 6 AOP 相关术语

##### JoinPoint （连接点）
所谓连接点是指那些被拦截到的点。在 Spring 中，这些点指的都是方法，因为 Spring 只支持方法类型的连接点。
##### Pointcut （切入点）
所谓切入点是指我们要对哪些 JoinPoint 进行拦截的定义。
##### Advice （通知/增强）
所谓通知是指拦截到 JoinPoint 之后所要做的事情就是通知。

通知的类型有如下：
* 前置通知 - doBefore
* 后置通知 - doAfter
* 异常通知 - catch 中执行的
* 最终通知 - finally 中执行的
* 环绕通知 - 被代理对象的方法在执行的过程中执行的
##### Introduction （引介）
引介是一种特殊的通知，在不修改类代码的前提下，Introduction 可以在运行期为类动态地添加一些方法或 Field。
##### Target （目标对象）
代理地目标对象。
##### Weaving （织入）
是指把增强应用到目标对象来创建新的代理对象的过程。 Spring 采用动态代理织入，而 Aspect 采用编译期织入和类装载期织入。
##### Proxy （代理）
一个类被 AOP 织入增强后，就产生一个结果代理类。
##### Aspect （切面）
是切入点和通知（引介）的结合。

# 银行转账案例

## 1 转账案例的纯业务代码 （纯净版本）

### 1.1 表对象和表结构

Account 对象的表结构

| 序号 | 字段名称 | 字段类型     | 字段描述
| :-:  | :-:     | :-:         | :-:
| 1    | id      | varchar(36) | 无意义，主键 uuid
| 2    | name    | varchar(50) | 账户名，唯一，不为空
| 3    | money   | float       | 账户余额，不为空

initdb.sql
```sql
-- 设置会话的字符集编码
set names utf8;

-- 删除用户 drop user 'peter'@'%';
-- 创建用户 peter
create user 'peter'@'%' identified by 'peter@root';

-- 删除数据库 drop database account;
-- 创建数据库 account
create database if not exists account default charset utf8 COLLATE utf8_general_ci;

-- 授权 （格式： 数据库.数据表）
grant all on account.* to 'peter'@'%';
-- 权限更新
flush privileges;

-- 使用数据库 account
use account;

-- 创建表单前，先删除
drop table if exists account;

create table account (
    id varchar(36) PRIMARY KEY,
    name varchar(50) NOT NULL UNIQUE,
    money float NOT NULL
);

-- 插入 mock 数据
insert into account(id, name, money) values(UUID(), 'aaa', 1000);
insert into account(id, name, money) values(UUID(), 'bbb', 1000);

-- 查看表结构
desc account;
-- 查看表内容
select * from account;
```

Account.java
```java
package com.petersdemo.account.domain;

public class Account {
    private String id;
    private String name;
    private Double money;
}
```

### 1.2 Dao 接口和实现类
IAccountDao.java
```java
package com.petersdemo.account.dao;

import com.petersdemo.account.domain.Account;

import java.util.List;

/**
 * 账户的持久层接口
 */
public interface IAccountDao {

    /**
     * 查询所有
     */
    public List<Account> findAllAccount();

    /**
     * 查询一个
     */
    public Account findAccountById(String id);

    /**
     * 根据名称查询账户
     * @param accountName
     * @return 如果有唯一的一个结果就返回，如果没有结果就返回 null
     *         如果结果集超过一个就抛异常。
     */
    public Account findAccountByName(String accountName);

    /**
     * 保存
     */
    public void saveAccount(Account account);

    /**
     * 更新
     */
    public void updateAccount(Account account);

    /**
     * 删除
     */
    public void deleteAccountById(String id);
    public void deleteAccountByName(String accountName);
}
```
AccountDaoImpl.java
```java
package com.petersdemo.account.dao.impl;

import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;
import org.apache.commons.dbutils.handlers.BeanListHandler;

import java.util.List;

/**
 * 账户的持久层实现类
 */
public class AccountDaoImpl implements IAccountDao {

    private QueryRunner runner;

    // 添加依赖注入(DI)接口
    public void setRunner(QueryRunner runner) {
        this.runner = runner;
    }

    @Override
    public List<Account> findAllAccount() {
        try {
            return runner.query("select * from account", new BeanListHandler<Account>(Account.class));
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Account findAccountById(String id) {
        try {
            return runner.query("select * from account where id = ?", new BeanHandler<Account>(Account.class), id);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Account findAccountByName(String accountName) {
        try {
            List<Account> accounts = runner.query("select * from account where name = ?", new BeanListHandler<Account>(Account.class), accountName);
            if (accounts == null || accounts.size() == 0) {
                return null;
            }
            else if (accounts.size() > 1) {
                throw new RuntimeException("结果集不唯一，数据有问题");
            }
            return accounts.get(0);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void saveAccount(Account account) {
        try {
            runner.update("insert into account(id, name, money) values(uuid(), ?, ?)", account.getName(), account.getMoney());
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void updateAccount(Account account) {
        try {
            runner.update("update account set name = ?, money = ? where name = ?", account.getName(), account.getMoney(), account.getName());
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void deleteAccountById(String id) {
        try {
            runner.update("delete from account where id = ?", id);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void deleteAccountByName(String accountName) {
        try {
            runner.update("delete from account where name = ?", accountName);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
```
注意，DAO 的实现需要借助于 JDBC 的实现类，此处使用 Apache DBUtils。
```xml
<dependency>
    <groupId>commons-dbutils</groupId>
    <artifactId>commons-dbutils</artifactId>
    <version>1.7</version>
</dependency>
```

### 1.3 Service 接口和实现类
IAccountService.java
```java
package com.petersdemo.account.service;

import com.petersdemo.account.domain.Account;

import java.util.List;

/**
 * 账户的业务层接口
 */
public interface IAccountService {

    /**
     * 查询所有
     */
    public List<Account> findAllAccount();

    /**
     * 查询一个
     */
    public Account findAccountById(String accountId);

    public Account findAccountByName(String accountName);

    /**
     * 保存
     */
    public void saveAccount(Account account);

    /**
     * 更新
     */
    public void updateAccount(Account account);

    /**
     * 删除
     */
    public void deleteAccountByName(String accountName);

    /**
     * 转账
     * @param sourceName
     * @param targetName
     * @param money
     */
    public void transfer(String sourceName, String targetName, Double money);
}
```
AccountServiceImpl.java
```java
package com.petersdemo.account.service.impl;

import com.petersdemo.account.dao.IAccountDao;
import com.petersdemo.account.domain.Account;
import com.petersdemo.account.service.IAccountService;

import java.util.List;

/**
 * 账户的业务层实现类
 * 注意：事务控制应该都是在业务层
 */
public class AccountServiceImpl implements IAccountService {

    private IAccountDao accountDao;

    //DI接口
    public void setAccountDao(IAccountDao accountDao) {
        this.accountDao = accountDao;
    }

    @Override
    public List<Account> findAllAccount() {
        return accountDao.findAllAccount();
    }

    @Override
    public Account findAccountById(String accountId) {
        return accountDao.findAccountById(accountId);
    }

    @Override
    public Account findAccountByName(String accountName) {
        return accountDao.findAccountByName(accountName);
    }

    @Override
    public void saveAccount(Account account) {
        accountDao.saveAccount(account);
    }

    @Override
    public void updateAccount(Account account) {
        accountDao.updateAccount(account);
    }

    @Override
    public void deleteAccountByName(String accountName) {
        accountDao.deleteAccountByName(accountName);
    }

    @Override
    public void transfer(String sourceName, String targetName, Double money) {
        //1.根据名称查询转出账户
        Account source = accountDao.findAccountByName(sourceName);
        //2.根据名称查询转入账户
        Account target = accountDao.findAccountByName(targetName);
        //3.转出账户减钱
        source.setMoney(source.getMoney()-money);
        //4.转入账户加钱
        target.setMoney(target.getMoney()+money);
        //5.更新转出账户
        accountDao.updateAccount(source);
        //6.更新转入账户
        accountDao.updateAccount(target);
    }
}
```
#### 以上，就是最纯净版本的业务代码。

### 1.4 单元测试

首先，在父工程的 pom.xml 文件添加如下配置（编译环境）：
```xml
<!-- 指定源文件编码方式 -->
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
<!-- 指定编译插件版本以及java版本 -->
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.1</version>
            <configuration>
                <source>9</source>
                <target>9</target>
            </configuration>
        </plugin>
    </plugins>
</build>
```

然后，在父工程的 pom.xml 文件添加如下配置（Junit4测试环境）：
```xml
<!-- Spring-Junit 测试环境 -->
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>

<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <version>4.12</version>
</dependency>

<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-test</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```

### 测试环境搭建（Spring 整合 Junit4 单元测试）

#### 1 在 Service 子项目的 src/test/java 目录下，创建 package 形如 ``com.petersdemo.account.service_test``，然后创建测试类。
AccountServiceTest.java
```java
package com.petersdemo.account.service_test;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:bean.xml"})  //Spring 的 ApplicationContext 配置文件 （可以为空，但必须要有。）
public class AccountServiceTest {

    @Test
    public void testInit(){  //自定义了一个测试单元testInit
        System.out.println("Test environment init success.");
    }
}
```

#### 2 在 Service 子项目的 src/test/resources 目录下，创建 bean.xml 作为 Spring 的 ApplicationContext 配置文件。
bean.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd">

    <!-- 这是一个空的 Spring ApplicationContext 配置 -->

</beans>
```
注意，src/java/resources 目录下的文件编译后将拷贝至 target/classes 目录，src/test/resources 目录下的则拷贝至 target/test-classes 目录。

#### 3 测试环境运行
在 IDEA 的右侧， Maven 控制面板中，执行父项目的 Lifecycle ``test``，如没有报错并运行成功表示测试环境搭建成功。示例：
```
Results :

Tests run: 1, Failures: 0, Errors: 0, Skipped: 0

[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO]
[INFO] account 1.0-SNAPSHOT ............................... SUCCESS [  0.006 s]
[INFO] domain ............................................. SUCCESS [  1.624 s]
[INFO] dao ................................................ SUCCESS [  0.082 s]
[INFO] service 1.0-SNAPSHOT ............................... SUCCESS [  1.654 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 3.601 s
[INFO] Finished at: 2019-12-05T13:29:16+08:00
[INFO] ------------------------------------------------------------------------
```

#### 4 开始测试
##### bean.xml 配置 Spring 的依赖注入 （Service -> Dao -> 数据库访问配置）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd">

    <!-- 注入 accountService 依赖 -->
    <bean id="accountService" class="com.petersdemo.account.service.impl.AccountServiceImpl">
        <!-- 注入 accountDao 依赖 -->
        <property name="accountDao" ref="accountDao"/>
    </bean>

    <!-- 创建 accountDao -->
    <bean id="accountDao" class="com.petersdemo.account.dao.impl.AccountDaoImpl">
        <!-- 注入 QueryRunner runner -->
        <property name="runner" ref="runner"/>
    </bean>

    <!-- 创建 QueryRunner runner -->
    <bean id="runner" class="org.apache.commons.dbutils.QueryRunner" scope="prototype">
        <!-- 指定数据源， QueryRunner 的源码定义的构造方法的参数是 ds -->
        <!-- 注意 property 与 constructor-arg 的用途差别 ！！ -->
        <constructor-arg name="ds" ref="dataSource"/>
    </bean>

    <!-- 创建 dataSource -->
    <bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
        <!-- 连接数据库的必备信息 -->
        <property name="driverClass" value="com.mysql.jdbc.Driver"/>
        <property name="jdbcUrl" value="jdbc:mysql://localhost:3306/account?useUnicode=true&amp;characterEncoding=utf8"/>
        <property name="user" value="peter"/>
        <property name="password" value="peter@root"/>
    </bean>

</beans>
```

###### 知识扩充： Spring Bean 的 scope 作用域
```
# 在 Spring2.0 之前 bean 只有 2 种作用域：singleton（单例）、non-singleton（也称 prototype）。
# 在 Spring2.0 以后，增加了 "session"、"request"、"global session" 三种专用于 Web 应用程序上下文的作用域。
# 如今，Spring 已支持的作用域共 5 种，但用户可以根据自己的需要自定义地添加作用域。
▫ 默认是单例模式，即 scope="singleton" 。
  此种配置下 Spring IOC 容器中只会存在一个共享的 bean 实例，所有对 bean 的请求，只要 id 与该 bean 的定义相匹配，则只会返回 bean 的同一实例。
▫ prototype，每一次请求都会产生一个新的 bean 实例。
  此种配置下 Spring 不负责 bean 实例的回收，回收 prototype bean 所持有的资源是客户端代码的职责。
▫ request 表示针对每一次 HTTP 请求都会产生一个新的 bean，同时该 bean 仅在当前 HTTP request 内有效。
▫ session 表示针对每一次 HTTP 请求都会产生一个新的 bean，同时该 bean 仅在当前 HTTP session 内有效。
▫ global session 类似于标准的 HTTP Session 作用域，只不过它仅仅在基于 portlet 的 web 应用中才有意义。
```

##### 注意，Setter 注入和 Constructor 注入使用的配置参数是不同的： ``setter 注入 <property name="" ref=""> ``，``构造函数 Constructor 注入 <constructor-arg name="" ref="">``。

maven 环境依赖
```xml
<dependency>
    <groupId>commons-dbutils</groupId>
    <artifactId>commons-dbutils</artifactId>
    <version>1.7</version>
</dependency>

<dependency>
    <groupId>com.mchange</groupId>
    <artifactId>c3p0</artifactId>
    <version>0.9.5.4</version>
</dependency>

<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.15</version>
</dependency>
```

#### 编写测试单元
AccountServiceTest.java
```java
package com.petersdemo.account.service_test;

import com.petersdemo.account.domain.Account;
import com.petersdemo.account.service.IAccountService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.List;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:bean.xml"})
public class AccountServiceTest {

    @Autowired
    private IAccountService accountService;

    @Test
    public void testInit(){
        System.out.println("Test environment init success.");
    }

    @Test
    public void testFindAll() {
        List<Account> accounts = accountService.findAllAccount();
        for (Account account : accounts) {
            System.out.println(account);
        }
    }

    @Test
    public void testSave() {
        Account account = new Account();
        account.setName("mock");
        account.setMoney(1234d);
        accountService.saveAccount(account);
    }

    @Test
    public void testUpdate() {
        Account account = accountService.findAccountByName("mock");
        account.setMoney(1000d);
        accountService.updateAccount(account);
    }

    @Test
    public void testDelete() {
        accountService.deleteAccountByName("mock");
    }

    @Test
    public void testTransfer() {
        accountService.transfer("aaa", "bbb", 100d);
    }
}
```

## 2 传统的事务控制案例 （为业务代码添加事务管理）

所谓事务控制，针对的对象是：内部包含有数据库访问或操作的 Service 的方法。

###### 基于的假设是： 如果服务中发生任何异常，都应该回到服务还没开始时的状态。

### 2.1 为了功能增强而必须引入的对象：

1. 连接工具类 ConnectionUtils。
2. 事务管理相关的工具类 TransactionManager。

ConnectionUtils.java （事务管理的一致性首先要从连接的一致性控制开始：“一个线程中使用的 sql 会话保证是同一个实例”。）
```java
package com.petersdemo.account.utils;

import javax.sql.DataSource;
import java.sql.Connection;

/**
 * 连接的工具类，它用于从数据源中获取一个连接，并且实现和线程的绑定
 */
public class ConnectionUtils {

    private ThreadLocal<Connection> tl = new ThreadLocal<Connection>();

    private DataSource dataSource;

    //DI接口
    public void setDataSource(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    /**
     * 获取当前线程上的连接
     */
    public Connection getThreadConnection() {
        try {
            // 1.从 ThreadLocal 上获取
            Connection conn = tl.get();
            // 2.判断是否为空
            if (conn == null) {
                // 为空，从线程池获取，并存入 ThreadLocal
                conn = dataSource.getConnection();
                tl.set(conn);
            }
            // 3.返回当前线程上的连接
            return conn;
        }
        catch(Exception e) {
            throw new RuntimeException(e);
        }
    }

    /**
     * 连接和线程解绑 （从线程上移除连接）
     */
    public void removeConnection() {
        tl.remove();
    }
}
```

TransactionManager.java （事务管理的执行工具类：开启、提交、回滚、释放连接）
```java
package com.petersdemo.account.utils;

/**
 * 事务管理相关的工具类，内部包含了： 开启事务、提交事务、回滚事务和释放连接。
 */
public class TransactionManager {

    private ConnectionUtils connectionUtils;

    //DI注入
    public void setConnectionUtils(ConnectionUtils connectionUtils) {
        this.connectionUtils = connectionUtils;
    }

    /**
     * 开启事务
     */
    public void beginTransaction() {
        try {
            connectionUtils.getThreadConnection().setAutoCommit(false);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 提交事务
     */
    public void commit() {
        try {
            connectionUtils.getThreadConnection().commit();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 回滚事务
     */
    public void rollback() {
        try {
            connectionUtils.getThreadConnection().rollback();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 释放连接
     */
    public void release() {
        try {
            connectionUtils.getThreadConnection().close(); //还回连接池中
            connectionUtils.removeConnection(); //连接和线程解绑
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

##### 将 “连接一致性” 约束织入 Dao 中
AccountDaoImpl.java
```java
package com.petersdemo.account.dao.impl;

import com.petersdemo.account.utils.ConnectionUtils;
import com.petersdemo.account.dao.IAccountDao;
import com.petersdemo.account.domain.Account;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;
import org.apache.commons.dbutils.handlers.BeanListHandler;

import java.util.List;

public class AccountDaoImpl implements IAccountDao {

    private QueryRunner runner;

    private ConnectionUtils connectionUtils;

    // 添加依赖注入(DI)接口
    public void setRunner(QueryRunner runner) {
        this.runner = runner;
    }

    //DI接口
    public void setConnectionUtils(ConnectionUtils connectionUtils) {
        this.connectionUtils = connectionUtils;
    }

    @Override
    public List<Account> findAllAccount() {
        try {
            return runner.query(connectionUtils.getThreadConnection(), "select * from account", new BeanListHandler<Account>(Account.class));
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Account findAccountById(String id) {
        try {
            return runner.query(connectionUtils.getThreadConnection(), "select * from account where id = ?", new BeanHandler<Account>(Account.class), id);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Account findAccountByName(String accountName) {
        try {
            List<Account> accounts = runner.query(connectionUtils.getThreadConnection(), "select * from account where name = ?", new BeanListHandler<Account>(Account.class), accountName);
            if (accounts == null || accounts.size() == 0) {
                return null;
            }
            else if (accounts.size() > 1) {
                throw new RuntimeException("结果集不唯一，数据有问题");
            }
            return accounts.get(0);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void saveAccount(Account account) {
        try {
            runner.update(connectionUtils.getThreadConnection(), "insert into account(id, name, money) values(uuid(), ?, ?)", account.getName(), account.getMoney());
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void updateAccount(Account account) {
        try {
            runner.update(connectionUtils.getThreadConnection(), "update account set name = ?, money = ? where name = ?", account.getName(), account.getMoney(), account.getName());
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void deleteAccountById(String id) {
        try {
            runner.update(connectionUtils.getThreadConnection(), "delete from account where id = ?", id);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void deleteAccountByName(String accountName) {
        try {
            runner.update(connectionUtils.getThreadConnection(), "delete from account where name = ?", accountName);
        }
        catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
```

### 2.2 使用最原始的方式，将事务控制代码织入

AccountServiceWithTxImpl.java
```java
package com.petersdemo.account.service.impl;

import com.petersdemo.account.dao.IAccountDao;
import com.petersdemo.account.domain.Account;
import com.petersdemo.account.service.IAccountService;
import com.petersdemo.account.utils.TransactionManager;

import java.util.List;

/**
 * 最原始的事务功能织入方式
 */
public class AccoutServiceWithTxImpl implements IAccountService {

    private IAccountDao accountDao;

    private TransactionManager txManager;

    //DI接口
    public void setAccountDao(IAccountDao accountDao) {
        this.accountDao = accountDao;
    }

    //DI接口
    public void setTxManager(TransactionManager txManager) {
        this.txManager = txManager;
    }

    @Override
    public List<Account> findAllAccount() {
        try {
            //1.开启事务
            txManager.beginTransaction();
            //2.执行操作
            List<Account> accounts = accountDao.findAllAccount();
            //3.提交事务
            txManager.commit();
            //4.返回结果
            return  accounts;
        } catch (Exception e) {
            //5.回滚事务
            txManager.rollback();
            throw new RuntimeException(e);
        } finally {
            //6.释放连接
            txManager.release();
        }
    }

    @Override
    public Account findAccountById(String accountId) {
        return accountDao.findAccountById(accountId);
    }

    @Override
    public Account findAccountByName(String accountName) {
        return accountDao.findAccountByName(accountName);
    }

    @Override
    public void saveAccount(Account account) {
        accountDao.saveAccount(account);
    }

    @Override
    public void updateAccount(Account account) {
        accountDao.updateAccount(account);
    }

    @Override
    public void deleteAccountByName(String accountName) {
        accountDao.deleteAccountByName(accountName);
    }

    @Override
    public void transfer(String sourceName, String targetName, Double money) {
        try {
            txManager.beginTransaction();
            //1.根据名称查询转出账户
            Account source = accountDao.findAccountByName(sourceName);
            //2.根据名称查询转入账户
            Account target = accountDao.findAccountByName(targetName);
            //3.转出账户减钱
            source.setMoney(source.getMoney()-money);
            //4.转入账户加钱
            target.setMoney(target.getMoney()+money);
            //5.更新转出账户
            accountDao.updateAccount(source);
            //6.更新转入账户
            accountDao.updateAccount(target);
            txManager.commit();
        } catch (Exception e) {
            txManager.rollback();
        } finally {
            txManager.release();
        }
    }
}
```

bean.xml 配置 Spring Bean 实例注入
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd">

    <!-- 注入 accountService 依赖 -->
    <bean id="accountService" class="com.petersdemo.test.service.impl.AccountServiceImpl">
        <!-- 注入 accountDao 依赖 -->
        <property name="accountDao" ref="accountDao"/>
    </bean>

    <!-- 创建 accountDao -->
    <bean id="accountDao" class="com.petersdemo.test.dao.impl.AccountDaoImpl">
        <!-- 注入 QueryRunner runner -->
        <property name="runner" ref="runner"/>
        <!-- 注入 connectionUtils -->
        <property name="connectionUtils" ref="connectionUtils"/>
    </bean>

    <!-- 创建 QueryRunner runner -->
    <bean id="runner" class="org.apache.commons.dbutils.QueryRunner" scope="prototype">
        <!-- 指定数据源， QueryRunner 的源码定义的构造方法的参数是 ds -->
        <constructor-arg name="ds" ref="dataSource"/>
    </bean>

    <!-- 创建 dataSource -->
    <bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
        <!-- 连接数据库的必备信息 -->
        <property name="driverClass" value="com.mysql.jdbc.Driver"/>
        <property name="jdbcUrl" value="jdbc:mysql://localhost:3306/account?useUnicode=true&amp;characterEncoding=utf8"/>
        <property name="user" value="peter"/>
        <property name="password" value="peter@root"/>
    </bean>

    <!-- 创建带事务控制的 accountService Bean -->
    <bean id="accountServiceWithTx" class="com.petersdemo.test.service.impl.AccoutServiceWithTxImpl">
        <!-- 注入 accountDao -->
        <property name="accountDao" ref="accountDao"/>
        <!-- 注入 txManager -->
        <property name="txManager" ref="txManager"/>
    </bean>

    <!-- 创建 txManager -->
    <bean id="txManager" class="com.petersdemo.test.utils.TransactionManager">
        <!-- 注入 connectionUtils -->
        <property name="connectionUtils" ref="connectionUtils"/>
    </bean>

    <!-- 创建 connectionUtils -->
    <bean id="connectionUtils" class="com.petersdemo.test.utils.ConnectionUtils">
        <!-- 注入 dataSource -->
        <property name="dataSource" ref="dataSource"/>
    </bean>

</beans>
```

测试代码
```java
package com.petersdemo.account.service_test;

import com.petersdemo.account.domain.Account;
import com.petersdemo.account.service.IAccountService;
import org.junit.test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.List;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:bean.xml"})
public class AccountServiceTest {

    @Autowired
    @Qualifier("accountServiceWithTx")  //存在多个 Bean 实例时，需要使用 Qualifier 指定注入哪个
    private IAccountService accountService;

    @Test
    public void testInit(){
        System.out.println("Test environment init success.");
    }

    @Test
    public void testFindAll() {
        List<Account> accounts = accountService.findAllAccount();
        for (Account account : accounts) {
            System.out.println(account);
        }
    }

    @Test
    public void testSave() {
        Account account = new Account();
        account.setName("mock");
        account.setMoney(1234d);
        accountService.saveAccount(account);
    }

    @Test
    public void testUpdate() {
        Account account = accountService.findAccountByName("mock");
        account.setMoney(1000d);
        accountService.updateAccount(account);
    }

    @Test
    public void testDelete() {
        accountService.deleteAccountByName("mock");
    }

    @Test
    public void testTransfer() {
        accountService.transfer("aaa", "bbb", 100d);
    }
}
```

#### 知识补充：
##### 1 Java 的 ThreadLocal 类
早在 JDK 1.2 版本就提供了 ``java.lang.ThreadLocal``，它的引入为解决多线程程序的并发问题提供了一种新的思路。

ThreadLocal 和 Synchronized 都是为了解决多线程中相同变量的访问冲突问题，其中：
* Synchronized 是通过线程等待（锁），牺牲时间来解决访问冲突。
* ThreadLocal 是通过每个线程单独一份存储空间（副本），牺牲空间来解决冲突。

ThreadLocal 具有线程隔离效果，当某些数据以线程为作用域，希望不同线程具有不同的数据副本时，就应该考虑采用 ThreadLocal。

##### 2 ThreadLocal 类的工作原理
涉及的 Java 类
* Thread
* ThreadLocalMap
* ThreadLocal
* Object

几者的耦合关系
1. Thread 类中有一个成员变量 ``ThreadLocal.ThreadLocalMap inheritableThreadLocals = null;``，一个 ThreadLocalMap 类的对象。
2. ThreadLocalMap 类其实是一个 Map，它的 key 是 ThreadLocal 实例对象，value 是 Object 类对象（数据对象的基类）。
    * 简单说，ThreadLocalMap 就是一个 ThreadLocal 和 Object 的关联表。 （类似于数据库的中间表）
3. ThreadLocal 又如何与 Thread 联系起来？
    * 注意，``Thread t = Thread.currentThread();`` 可以获取到当前线程对象。
    * 因此，ThreadLocal 就可以通过 ``ThreadLocalMap map = t.threadLocals;`` 获取到当前线程对象和映射表。
    * 然后，就可以访问当前线程的数据副本了（增删改查）。

ThreadLocal 的作用是提供线程内的局部变量，这种变量在线程的生命周期内起作用。每一个线程都可以随意修改自己的变量副本，而不会对其他线程产生影响。

## 3 AOP 模式实现事务控制 （运用 Java 的代理技术进行 AOP 编程）

### 3.1 为了功能增强而必须引入的对象
* BeanFactory 工厂类。（生成代理对象，完成方法增强功能织入。）

#### 工厂方法模式

IAccountServiceFactory.java
```java
package com.petersdemo.account.factory;

import com.petersdemo.account.service.IAccountService;

/**
 * AccountService 类的工厂方法模式接口
 */
public interface IAccountServiceFactory {
    public IAccountService getAccountService();
}
```

ProxyAccountServiceFactory.java
```java
package com.petersdemo.account.factory.impl;

import com.petersdemo.account.factory.IAccountServiceFactory;
import com.petersdemo.account.service.IAccountService;
import com.petersdemo.account.utils.TransactionManager;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

/**
 * 工厂方法模式：创建 AccountService 的代理对象
 */
public class ProxyAccountServiceFactory implements IAccountServiceFactory {

    private IAccountService accountService;  //被增强实例

    private TransactionManager txManager;    //提供增强操作的实例

    //DI接口
    public void setAccountService(IAccountService accountService) {
        this.accountService = accountService;
    }

    //DI接口
    public void setTxManager(TransactionManager txManager) {
        this.txManager = txManager;
    }

    /**
     * 工厂方法，获取 AccountService 代理对象
     * @return
     */
    @Override
    public IAccountService getAccountService() {
        return (IAccountService) Proxy.newProxyInstance(accountService.getClass().getClassLoader(),
                accountService.getClass().getInterfaces(),
                new InvocationHandler() {
                    /**
                     * 添加事务的支持
                     * @param proxy
                     * @param method
                     * @param args
                     * @return
                     * @throws Throwable
                     */
                    @Override
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        Object rtValue = null;
                        try {
                            //1.开启事务
                            txManager.beginTransaction();
                            //2.执行操作
                            rtValue = method.invoke(accountService, args);
                            //3.提交事务
                            txManager.commit();
                            //4.返回结果
                            return rtValue;
                        } catch (Exception e) {
                            //5.回滚事务
                            txManager.rollback();
                            throw new RuntimeException(e);
                        } finally {
                            //6.释放连接
                            txManager.release();
                        }
                    }
                });
    }
}
```
##### 注意，生成代理对象需要三大核心类：``被增强类``、``提供增强操作的类``、``返回代理对象的工厂类``。

#### Spring IOC 配置，实现从工厂类创建代理对象的 Bean 并注入
bean.xml
```xml
<!-- 创建工厂类实例 -->
<bean id="proxyAccountServiceFactory" class="com.petersdemo.account.service.impl.ProxyAccountServiceFactoryImpl">
    <!-- 注入被被代理类的实例 -->
    <property name="accountService" ref="accountService"/>
    <!-- 注入提供增强操作的类实例 -->
    <property name="txManager" ref="txManager"/>
</bean>
<!-- 使用工厂，创建代理类 proxyAccountService -->
<bean id="proxyAccountService" factory-bean="proxyAccountServiceFactory" factory-method="getAccountService"/>

<!-- 创建 accountService -->
<bean id="accountService" class="com.petersdemo.account.service.impl.AccountServiceImpl">
    <!-- 注入 accountDao 依赖 -->
    <property name="accountDao" ref="accountDao"/>
</bean>

<!-- 创建 accountDao -->
<bean id="accountDao" class="com.petersdemo.account.dao.impl.AccountDaoImpl">
    <!-- 注入 QueryRunner runner -->
    <property name="runner" ref="runner"/>
    <!-- 注入 connectionUtils （连接一致性控制） -->
    <property name="connectionUtils" ref="connectionUtils"/>
</bean>

<!-- 创建 QueryRunner runner -->
<bean id="runner" class="org.apache.commons.dbutils.QueryRunner" scope="prototype">
    <!-- 指定数据源， QueryRunner 的源码定义的构造方法的参数是 ds -->
    <constructor-arg name="ds" ref="dataSource"/>
</bean>

<!-- 创建 dataSource -->
<bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
    <!-- 连接数据库的必备信息 -->
    <property name="driverClass" value="com.mysql.jdbc.Driver"/>
    <property name="jdbcUrl" value="jdbc:mysql://localhost:3306/account?useUnicode=true&amp;characterEncoding=utf8"/>
    <property name="user" value="peter"/>
    <property name="password" value="peter@root"/>
</bean>

<!-- 创建 connectionUtils （连接一致性控制类） -->
<bean id="connectionUtils" class="com.petersdemo.account.utils.ConnectionUtils">
    <!-- 注入 dataSource -->
    <property name="dataSource" ref="dataSource"/>
</bean>

<!-- 创建 txManager （提供 “事务控制” 增强操作的类） -->
<bean id="txManager" class="com.petersdemo.account.utils.TransactionManager">
    <!-- 注入 connectionUtils -->
    <property name="connectionUtils" ref="connectionUtils"/>
</bean>
```

##### 注解 @ComponentScan
注意，对于类似上例的编码习惯，将 BeanFactory 工厂类专门放置于一个模块的情况，需要在配置 bean.xml 的时候添加依赖扫描（防止Spring容器找不到类的字节码）。 ``注解 @ComponentScan 的作用就是根据指定的扫描路径，把符合扫描规则的类装载到 Spring 容器中。``
```
默认情况下，<context:component-scan> 查找所有被构造型注解（stereotype）所标注的类，将被注解的类加入到 Spring 容器中。
# 常用的 stereotype 注解：
  1. @Controller   控制器  （用于标注业务层组件，注入服务）
  2. @Service      服务    （用于标注控制层组件，注入dao）
  3. @Repository   dao    （用于标注数据访问组件，表明是dao的实现类）
  4. @Component    pojo    （把普通pojo实例化到spring容器中）
综上，四种注解在语义上分别对应于：一般Java实现类（POJO）、控制器实现类、服务实现类、Dao实现类。
```

##### Spring 项目 Junit 测试报错 ClassNotFoundException 的问题
问题出现的原因：在 maven 项目中运行 Junit，仅 Maven 的 Dependencies 依赖树中的 package 会被编译和加载，使用未在 Dependencies 依赖树中的类，会报 ClassNotFoundException 错误，因为它的字节码确实没有被加载（Junit 对字节码的加载是按 Dependencies 依赖树的）。

解决方法：
* 在 Junit 单元测试类所在项目的 pom.xml 文件中添加 dependency 依赖配置。
* 检查下 dependency 的 scope 配置，如果是 provided 的话，一般极有可能引发 ClassNotFoundError。
```
# scope 的分类
1. compile  - 默认就是 compile，什么都不配置也意味着 compile。表示被依赖项目需要参与当前项目的编译。
2. test     - 表示被依赖项目仅仅参与测试相关的工作，仅参与测试代码的编译执行，如：junit。
3. runtime  - 表示被依赖项目无需参与项目的编译，不过后续的测试和运行周期需要其参与。（与 compile 相比，跳过编译而已。）
4. provided - 意味着打包的时候可以不用包进去。
5. system   - 从参与度来说，与 provided 相同。不过被依赖项不会从 maven 仓库抓，而是从本地文件系统拿，因此需要配合 systemPath 属性使用。
```

综上，Junit 测试的配置过程为：pom.xml 中添加 dependency 依赖，推荐 compile scope 配置，编写测试代码如下：
```java
import org.junit.runner.RunWith;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

//单元测试类。 命名规则： 被测试Java类的名称 + Test
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:bean.xml"})
public ClassNameTest {

    //单元测试函数。 命名规则： test + 被测函数的名称
    @Test
    public void testMethodName() {
        // ...
    }
}
```
如果依赖项有问题（可通过 maven 的 dependencies 依赖树查看是否有异常），一定出现 ClassNotFoundException。 例如：
```
上例中，将 Junit 单元测试代码放置于 service 所在项目，创建的 factory 项目依赖于 service 项目，
那么，现在在 service 项目中添加对 factory 的依赖，用于 Junit 单元测试。。结果肯定是依赖关系有问题，循环依赖。。
解决方法：
1. 将 factory 的代码放置于 service 项目，以消除循环依赖。
2. 或者将 Junit 单元测试代码移出 service 项目，单独放置于一个独立项目，以消除循环依赖。
```

### 3.2 AOP 形式的事务管理代码织入
动态代理：
* 特点：字节码随用随创建，随用随加载。
* 作用：不修改源码的基础上对方法增强（织入新操作）。

分类：
* 基于接口的动态代理
* 基于子类的动态代理

#### 1 基于接口的动态代理
* 涉及的类： ***Proxy***
* 提供者： Java 官方

##### 创建代理对象的要求
被代理类最少要实现一个接口，如果没有达标则不能使用。

##### 使用方法
```java
/**
 * 假设 Producer 是被代理的类，为它织入新操作。
 */
IProducer producer = new ProducerImpl();  //创建一个被增强类的实例
IEnhancer enhancer = new EnhancerImpl();  //创建一个提供增强操作的类实例，以织入前置通知/后置通知/环绕通知/异常通知/最终通知。

IProducer proxyProducer = (IProducer) Proxy.newProxyInstance(producer.getClass().getClassLoader(),
                producer.getClass().getInterfaces(),
                new InvocationHandler() {
                    /**
                     * 为 Producer 织入新操作
                     * @param proxy   代理对象的引用
                     * @param method  当前执行的方法
                     * @param args    当前执行方法所需的参数
                     * @return        和被代理对象方法有相同的返回值
                     * @throws Throwable
                     */
                    @Override
                    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                        Object rtValue = null;
                        try {
                            //1.前置通知
                            //2.执行操作
                            rtValue = method.invoke(producer, args);
                            //3.后置通知
                            //4.返回结果
                            return rtValue;
                        } catch (Exception e) {
                            //5.异常通知
                            //6.抛出异常
                            throw new RuntimeException(e);
                        } finally {
                            //7.最终通知
                        }
                    }
                });
```

##### Proxy.newProxyInstance 方法的参数
* ClassLoader：类加载器
  ```
  它用于代理对象字节码的加载。要求和被代理对象使用相同的类加载器，因此写法固定。
  ```
* Class[]：字节码数组
  ```
  它用于让代理对象和被代理对象有相同方法，因此传入被代理对象的接口数组。写法固定。
  ```
* InvocationHandler：用于提供增强的代码
  ```
  一般都是写一个 InvocationHandler 接口的实现类，通常情况下都是匿名内部类，但不是必须的。
  此接口的实现类都是谁用谁写。 AOP 编程的核心所在。
  ```

#### 2 基于子类的动态代理
* 涉及的类： ***Enhancer***
* 提供者： 第三方 cglib 库

```xml
<dependency>
    <groupId>cglib</groupId>
    <artifactId>cglib</artifactId>
    <version>3.3.0</version>
</dependency>
```

##### 创建代理对象的要求
被代理类不能是最终类。

##### 使用方法
```java
/**
 * 假设 Producer 是被代理的类，为它织入新操作。
 */
IProducer producer = new ProducerImpl();  //创建一个被增强类的实例
IEnhancer enhancer = new EnhancerImpl();  //创建一个提供增强操作的类实例，以织入前置通知/后置通知/环绕通知/异常通知/最终通知。

IProducer proxyProducer = (IProducer) Enhancer.create(producer.getClass(),
                new MethodInterceptor() {
                    /**
                     * 为 Producer 织入新操作
                     * @param proxy       代理对象的引用
                     * @param method      当前执行的方法
                     * @param args        当前执行方法所需的参数
                     * @param methodProxy 当前执行方法的代理对象
                     * @return            和被代理对象方法有相同的返回值
                     * @throws Throwable
                     */
                    @Override
                    public Object intercept(Object proxy, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
                        Object rtValue = null;
                        try {
                            //1.前置通知
                            //2.执行操作
                            rtValue = method.invoke(producer, args);
                            //3.后置通知
                            //4.返回结果
                            return rtValue;
                        } catch (Exception e) {
                            //5.异常通知
                            //6.抛出异常
                            throw new RuntimeException(e);
                        } finally {
                            //7.最终通知
                        }
                    }
                });
```

##### Ehancer.create 方法的参数
* Class：字节码
  ```
  指定被代理对象的字节码。
  ```
* Callback：用于提供增强的代码
  ```
  一般都是写一个 Interceptor 接口的实现类，通常情况下都是匿名内部类，但不是必须的。
  此接口的实现类都是谁用谁写。 AOP 编程的核心所在。
  注意： 此处一般写的都是 Interceptor 接口的子接口类 MethodInterceptor 的实现类。
  ```
