## Spring

##### Spring 的核心内容
* Spring IoC 配置 （Inversion of Control）
* Spring AOP （Aspect Oriented Programming）
* Spring JDBC Template （JDBC标准的实现类）
* Spring 事务控制

##### Spring 概述
spring 的定位是做一个 java 的 ``full-stack`` 轻量级开源框架，框架本身提供了视图层方案 Spring MVC，持久层方案 Spring JDBC，以及业务层方案-业务层TransactionManager。同时，它还支持对接开源世界的第三方框架和类库，如 Mybatis 等。 官方网站 http://spring.io/ 。

##### Spring 的优势
* 方便解耦，简化开发（IOC设计模式）
* AOP 编程
* 声明式事务控制
* 方便的测试模块开发

官方教程
* 项目搭建教程 http://spring.io/guides
* spring 产品家族 http://spring.io/projects

##### Spring 框架的体系结构
<div align="center">
<img src="figures/spring-overview.png" width="50%">
</div>

* 架构图来源 http://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/overview.html

Spring 的核心部分是 Core Container 部分，主要支持 IOC 设计模式的实现，因此才有 Spring 的 xml 配置这一个环境搭建的核心部分。 DataAccess、Web 提供了大量的 MySQL 访问、Servlet 过滤器和监听器的实现代码，数据库访问几乎都不需要写代码了。 AOP 则定义了 Spring 编写业务代码的范式，需要编码人员掌握牢记。

官方文档 http://docs.spring.io/spring/docs/

#### IOC 设计模式
Inversion of Control (IOC) 是一种框架设计理念，其初衷是实现程序的解耦，在程序编译时，不再会因为依赖库的缺失而导致编译的失败。（代码编译不依赖外部类文件。）

```java
/**
 * IOC 设计模式实践
 */
private IAccountDao accountDao = new AccountDaoImpl();  // 一般方式
private IAcountDao accountDao = (IAccountDao)BeanFactory.getBean("accountDao");  // IOC设计模式

/**
 * 工厂类
 */
public class BeanFactory {

    public static Object getBean(String className) {
        try {
            //通过类名生成实例对象并将其返回
            Class c = Class.forName(className);
            Object obj = c.newInstance();
            return obj;
        }
        catch(Exception e) {
            e.printStackTrace();
			return null;
        }
    }
}
```
IOC 设计模式的好处是，类名字符串还可以进一步放置于 xml 配置文件中，实现一套代码多种组合。

IOC 设计模式的最常见实现方式，叫做 “依赖注入”（Dependency Injection，DI），此外还有一种实现方式，叫 “依赖查找”（Dependency Lookup）。

##### 依赖注入的示例：
```java
package com.petersdemo.factory;

public class BeanFactory {

    private IAccountService accountService;

    private TransactionManager txManager;

    // 提供注入（DI）接口
    public void setAccountService(IAccountService accountService) {
        this.accountService = accountService;
    }

    // 提供注入（DI）接口
    public void setTxManager(TransactionManager txManager) {
        this.txManager = txManager;
    }

    /**
     * 获取 Service 代理对象
     * return IAccountService
     */
    public IAccountService getAccountService() {
        return (IAccountService) Proxy.newProxyInstance(
            accountService.getClass().getClassLoader(),
            accountService.getClass().getInterfaces(),
            new InvocationHandler() {
                /**
                * 添加事务的支持
                *
                * @param proxy
                * @param method
                * @param args
                * @return
                * @throws Throwable
                */
                @Override
                public Object invoke(Object proxy, Method method, Object[] args) throws Trowable {
                    if ("test".equals(method.getName())) {
                        return method.invoke(accountService, args);
                    }
                    Object rtValue = null;
                    try {
                        //1. 开启事务
                        txManager.beginTransaction();
                        //2. 执行操作
                        rtValue = method.invoke(accountService, args);
                        //3. 提交事务
                        txManager.commit();
                        //4. 返回结果
                        return rtValue;
                    } catch (Exception e) {
                        //5. 回滚操作
                        txManager.rollback();
                        throw new RuntimeException(e);
                    } finally {
                        //6. 释放连接
                        txManager.release();
                    }
                }
        }); // End of return
    }
}
```
```xml
<!-- 通过一个工厂类获取一个代理类的实例对象 -->
<bean id="proxyAccountService" factory-bean="beanFactory" factory-method="getAccountService"/>
<!-- 创建一个工厂类实例 beanFactory -->
<bean id="beanFactory", class="com.petersdemo.factory.BeanFactory">
    <!-- 注入 accountService，自动会调用 setAccountService 为其赋值。 -->
    <property name="accountService" ref="accountService"/>
    <!-- 注入 txManager，自动会调用 setTxManager 为其赋值。 -->
    <property name="txManager" ref="txManager"/>
</bean>
<!-- 注意，我们此时已假设 ref="accountService" 和 ref="txManager" 指向的对象已通过 <bean> 标签创建完成，否则，运行时报引用为空错误。 -->
```

#### AOP 设计模式
AOP 是 Aspect Oriented Programming 的缩写。 面向切面编程，通过预编译方式和运行期动态代理，实现程序功能的灵活性和可扩展性，AOP 也是 GoF 设计模式的延伸。

AOP 的初衷是将日志记录，性能统计，安全控制，事务处理，异常处理等非业务核心代码从业务逻辑代码中划分出来。

##### AOP 与 OOP 异同点 （封装 -> 切片）
* OOP 是对业务处理过程的实体及其属性和行为进行抽象封装。 （具体业务 -> 一个对象）
* AOP 则是对业务处理过程中的 “切面（处理过程中的某个步骤或阶段）” 进行提取，将它们单独封装在一起。（Java 动态代理技术 - 相当于 Python 的装饰器对被装饰函数的增强）

```java
/**
 * AOP 设计模式实践
 */
package com.petersdemo.factory;

import com.petersdemo.service.IAccountService;

/**
 * 用于创建 Service 的代理对象的工厂
 */
public class BeanFactory {

    private IAccountService accountService;

    private TransactionManager txManager;

    // 提供注入（DI）接口
    public void setAccountService(IAccountService accountService) {
        this.accountService = accountService;
    }

    // 提供注入（DI）接口
    public void setTxManager(TransactionManager txManager) {
        this.txManager = txManager;
    }

    /**
     * 获取 Service 代理对象，动态创建出一个代理对象。
     *（此时使用的是 Java 官方的动态代理技术，详细内容查阅 Proxy 类的介绍。）
     * return IAccountService
     */
    public IAccountService getAccountService() {
        return (IAccountService) Proxy.newProxyInstance(
            accountService.getClass().getClassLoader(),
            accountService.getClass().getInterfaces(),
            new InvocationHandler() {
                /**
                * 添加事务的支持
                *
                * @param proxy
                * @param method
                * @param args
                * @return
                * @throws Throwable
                */
                @Override
                public Object invoke(Object proxy, Method method, Object[] args) throws Trowable {
                    if ("test".equals(method.getName())) {
                        return method.invoke(accountService, args);
                    }
                    Object rtValue = null;
                    try {
                        //1. 开启事务
                        txManager.beginTransaction();
                        //2. 执行操作
                        rtValue = method.invoke(accountService, args);
                        //3. 提交事务
                        txManager.commit();
                        //4. 返回结果
                        return rtValue;
                    } catch (Exception e) {
                        //5. 回滚操作
                        txManager.rollback();
                        throw new RuntimeException(e);
                    } finally {
                        //6. 释放连接
                        txManager.release();
                    }
                }
        }); // End of return
    }
}
```
为对象动态添加代理以实现周边功能的增强，是 AOP 的核心逻辑。

##### AOP 相关术语
* Joinpoint （连接点）
* Pointcut （切入点）
* Advice （通知/增强）
* Introduction （引介）
* Target （目标对象）
* Weaving （织入）
* Proxy （代理）
* Aspect （切面）

#### Spring 代码开发的特点
* 编写核心业务代码。（开发主线：实现功能类。没有异常处理，没有任何周边操作。）
* 公用代码抽取，制作成通知。（AOP 编程核心：梳理所有周边操作，对它们进行通知类型划分，然后封装于一个代理类中。注意是一个代理类。）
* 在配置文件中，声明切入点与通知的关系，即面向切面。（AOP 配置核心：使用代理类替换到所有的直接功能类。注意，从此以后功能类永不直接使用。）

##### 整个开发阶段，核心和难点是有一双慧眼，去抽取公共代码。

#### Spring 框架的启动逻辑
后台不断监控切入点方法（Servlet）的执行。 一旦监测到切入点方法被执行，使用代理机制动态创建目标对象的代理对象，在代理对象的对应位置，将通知对应的功能织入，执行。

<br>

# Spring 的 Maven 环境搭建

#### 1 需要的配置文件
* applicationContext.xml **（Spring 核心配置文件，Spring 框架启动配置）**
    * 配置自定义的 dao 和 service 依赖
    * spring 整合 mybatis
    * 事务管理配置
* spring-mvc.xml **（SpringMVC 核心配置文件，Servlet 启动配置）**
    * 配置自定义的 controller 依赖
    * 配置视图解析器
    * 配置静态资源过滤要求
    * 开启 Spring MVC 注解功能
    * 开启 AOP 注解功能
* web.xml **（Maven webapp 核心配置文件，Tomcat 启动配置）**
    * 配置解决中文乱码的过滤器
    * 配置 welcome-file-list （首页）
    * 配置 filter 和 listener
    * 配置 servlet 和 url 映射关系
    * 其他配置： JSP、security 和 login auth 等。

注意，整个 Spring 的工程，最终的启动入口都是 web.xml 配置文件，也就是 webapp 项目。其他子工程最终会以 jar 包的形式存在于 webapp 中。
``因此，所有的 xml 配置文件在创建的时候，就应在 webapp 目录下创建。``

#### 2 创建配置文件
在 maven webapp 项目的 src/main 目录下，右键，new -> directory，创建一个名为 java 的目录。
* 在 java 目录上，右键，Mark Directory as -> Source Root。
* 在 src/main 目录下，创建一个与 java 同级的目录 resources。然后将它标记为 Resources Root。
* 在 resources 目录下，创建 applicationContext.xml 文件。
* 在 resources 目录下，创建 spring-mvc.xml 文件。
* web.xml 文件在 webapp 项目创建时已存在于 src/main/webapp/WEB-INF 目录下，不用再去创建了。

#### 3 spring 项目的 jar 包依赖
##### 1. 在父项目的 pom.xml 文件中添加 spring-context 依赖
在 http://mvnrepository.com/ ，搜索 spring-context，点击进入，选择 5.0.2 release，点击，内容如下所示。 添加至 pom.xml 的 \<dependencies> 标签内。
```xml
<dependencies>
  <dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-context</artifactId>
    <version>5.0.2.RELEASE</version>
  </dependency>
</dependencies>
```
注意，spring 的 context 依赖不是一个简单的依赖，导入之后，自动导入 beans、core、aop、expression、jcl 等核心组件。 （因此，添加这一个依赖就可以认为 spring 基础依赖已配置完成。）

#### 4 配置文件填写
##### 1. 配置文件的模板
打开 spring 文档，进入 spring-framework-reference 目录，查看 Core Section 部分内容。 http://docs.spring.io/spring/docs/5.0.10.RELEASE/spring-framework-reference/core.html ，Ctrl+F 搜索 “xmls”，查看各种配置模板。（需要注意的是，Core Section 部分并不包含所有的配置模板，数据库配置、事务配置、Servlet 配置，查看对应的 Section 内容。）

* 中文文档 http://www.docs4dev.com/docs/zh/spring-framework/5.1.3.RELEASE/reference

##### 2. applicatonContext.xml （配置 Spring 框架启动项）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:aop="http://www.springframework.org/schema/aop"
    xmlns:tx="http://www.springframework.org/schema/tx"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd
        http://www.springframework.org/schema/aop
        http://www.springframework.org/schema/aop/spring-aop.xsd
        http://www.springframework.org/schema/tx
        http://www.springframework.org/schema/tx/spring-tx.xsd">

    <!-- 开启注解扫描，管理自定义的 service 和 dao 依赖 -->
    <context:component-scan base-package="com.petersdemo.ssm.service">
    </context:component-scan>
    <context:component-scan base-package="com.petersdemo.ssm.dao">
    </context:component-scan>

    <!-- Spring 整合 MyBatis (MyBatis 学习内容) -->
    <context:property-placeholder location="classpath:db.properties"/>
    <bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
        <property name="driverClass" value="${jdbc.driver}"/>
        <property name="jdbcUrl" value="${jdbc.url}"/>
        <property name="user" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="dataSource" />
    </bean>

    <!-- 扫描 dao 接口 -->
    <bean id="mapperScanner" class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="basePackage" value="com.petersdemo.ssm.dao"/>
    </bean>

    <!-- Spring 的声明式事务管理 -->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"/>
    </bean>
    <tx:annotation-driven transaction-manager="transactionManager"/>

</beans>
```
以上 xml 语法约束包含三部分内容： context（即ioc配置规范）、aop 配置规范、tx（即事务transaction）配置规范。

``导入 spring-context 依赖的时候是不包含 spring-tx 的，请搜索并添加 tx 对应的 jar 包``，如下：
```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-tx</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```

MyBatis 整合到 Spring 中需要四个依赖： MySQL、MyBatis、MyBatis-Spring，以及一个线程池（dataSource）c3p0。 另外，还有一个 “声明式事务管理” 依赖 spring-jdbc。
```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.15</version>
</dependency>

<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis</artifactId>
    <version>3.5.0</version>
</dependency>

<dependency>
    <groupId>org.mybatis</groupId>
    <artifactId>mybatis-spring</artifactId>
    <version>2.0.3</version>
</dependency>

<dependency>
    <groupId>com.mchange</groupId>
    <artifactId>c3p0</artifactId>
    <version>0.9.5.2</version>
</dependency>

<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-jdbc</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```

特别注意，另外需要在 src/main/resources 目录下，创建一个 db.properties 文件，配置数据库访问的驱动、路径、用户名、密码。
```
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/ssm?useUnicode=true&characterEncoding=utf8
jdbc.username=root
jdbc.password=root
```

Spring 与 MyBatis 聚合，参考 http://mybatis.org/spring/zh/getting-started.html ，以及 Spring 的 Data Access 部分。

Spring 事务管理（Transaction），参考 Spring 文档的 Data Access 部分。

##### 3 spring-mvc.xml （通过 mvc 配置 Servlet 启动项）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:mvc="http://www.springframework.org/schema/mvc"
    xmlns:context="http://www.springframework.org/schema/context"
    xmlns:aop="http://www.springframework.org/schema/aop"
    xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/mvc
        http://www.springframework.org/schema/mvc/spring-mvc.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd
        http://www.springframework.org/schema/aop
        http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!-- 开启注解扫描，管理自定义的 controller 依赖 -->
    <context:component-scan base-package="com.petersdemo.ssm.controller">
    </context:component-scan>

    <!-- 配置视图解析器 -->
    <bean id="viewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <!-- 配置 JSTL 支持（参考 Spring MVC 文档 JSTL 内容），jstl 需要依赖相关 jar 包 -->
        <property name="viewClass" value="org.springframework.web.servlet.view.JstlView"/>
        <!-- JSP 文件所在目录 -->
        <property name="prefix" value="/pages/"/>
        <!-- 文件的后缀名 -->
        <property name="suffix" value=".jsp"/>
    </bean>

    <!-- 设置静态资源不过滤 -->
    <mvc:resources mapping="/css/**" location="/css/"/>
    <mvc:resources mapping="/img/**" location="/img/"/>
    <mvc:resources mapping="/js/**" location="/js/"/>
    <mvc:resources mapping="/plugins/**" location="/plugins/"/>

    <!-- 开启对 SpringMVC 注解的支持 -->
    <mvc:annotation-driven/>

    <!--
        支持 AOP 的注解技术，AOP 底层使用代理技术。
        JDK 动态代理，要求必须有接口。
        cglib 代理，生成子类对象，proxy-target-class="true" 默认使用 cglib 的方式。
    -->
    <aop:aspectj-autoproxy proxy-target-class="true"/>

</beans>
```
以上 xml 语法约束包含： context 配置约束、aop 配置约束、mvc 配置约束。

jstl 的 maven 依赖有两个，如下：
```xml
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>jstl</artifactId>
    <version>1.2</version>
</dependency>

<dependency>
    <groupId>taglibs</groupId>
    <artifactId>standard</artifactId>
    <version>1.1.2</version>
</dependency>
```

aop 的支持需要两个依赖 ``spring-aop`` 和 ``spring-aspects``。
```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aop</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>

<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-aspects</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```

##### Servlet 的启动配置不使用原生 servlet 框架，采用 Spring MVC 框架，详细介绍见 Spring 文档的 Web Servlet 部分。

Spring MVC 不包含在 Spring 的核心组件中，因此，需要添加依赖 ``spring-web`` 和 ``spring-webmvc``。
```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-web</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>

<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```

##### 4 web.xml （Tomcat 的 Servlet 启动配置）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1"
         metadata-complete="true">

  <!-- 配置加载类路径的配置文件 -->
  <context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath*:applicationContext.xml,classpath*:spring-security.xml</param-value>
  </context-param>

  <!-- 配置监听器 -->
  <listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
  </listener>
  <!-- 配置监听器，监听 request 域对象的创建和销毁 -->
  <listener>
    <listener-class>org.springframework.web.context.request.RequestContextListener</listener-class>
  </listener>

  <!-- 前端控制器，加载 classpath:spring-mvc.xml，服务器启动时创建 servlet -->
  <servlet>
    <servlet-name>dispatcherServlet</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <!-- 配置初始化参数，创建完 DispatcherServlet 对象，加载 spring-mvc.xml 配置文件 -->
    <init-param>
      <param-name>contextConfigLocation</param-name>
      <param-value>classpath:spring-mvc.xml</param-value>
    </init-param>
    <!-- 服务器启动的时候，让 DispatcherServlet 对象创建（即创建 Servlet 对象） -->
    <load-on-startup>1</load-on-startup>
  </servlet>

  <servlet-mapping>
    <servlet-name>dispatcherServlet</servlet-name>
    <url-pattern>*.do</url-pattern>
  </servlet-mapping>

  <!-- 解决中文乱码过滤器 -->
  <filter>
    <filter-name>characterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
      <param-name>encoding</param-name>
      <param-value>UTF-8</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>characterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>

  <!-- 委派过滤器 -->
  <!--<filter>
    <filter-name>springSecurityFilterChain</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>springSecurityFilterChain</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>-->

  <welcome-file-list>
    <welcome-file>index.html</welcome-file>
    <welcome-file>index.htm</welcome-file>
    <welcome-file>index.jsp</welcome-file>
    <welcome-file>default.html</welcome-file>
    <welcome-file>default.htm</welcome-file>
    <welcome-file>default.jsp</welcome-file>
  </welcome-file-list>

</web-app>
```
web.xml 配置的是 Servlet 启动项，由于使用 Spring MVC 替代原生 Servlet 框架，此时做配置，应参考 Spring 文档的 Web Servlet 部分。
``同时需要注意的是，Spring Boot 与 Spring MVC 遵循不同的初始化顺序，详细信息参阅 Spring Boot 文档。``

###### WEB 应用中的 classpath 是什么，classpath: 与 classpath*: 有何区别。
```
首先，JavaEE 中的 classpath 与系统环境变量中的 classpath 不同。 WEB 应用中的 classpath 专指 WEB-INF/classes 和 WEB-INF/lib。
▪ [classpath:] 告知 web 容器去 classpath（WEB-INF/classes和WEB-INF/lib） 中去加载指定名称的配置文件，若是有同名文件，则只会加载一个。
▪ [classpath*:] 告知 web 容器去 classpath（WEB-INF/classes和WEB-INF/lib） 中去加载指定名称的配置文件，若是有同名文件，则全部加载。
```

##### 注意，web.xml 是这个 webapp 启动的核心，不建议上来就进行复杂配置，因为稍有 bug 就会导致 404 错误。。 推荐以下的渐进式 web.xml + index.jsp 模板
web.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1"
         metadata-complete="true">

  <!-- 解决中文乱码过滤器 -->
  <filter>
    <filter-name>characterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
      <param-name>encoding</param-name>
      <param-value>UTF-8</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>characterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>

  <welcome-file-list>
    <welcome-file>index.html</welcome-file>
    <welcome-file>index.htm</welcome-file>
    <welcome-file>index.jsp</welcome-file>
    <welcome-file>default.html</welcome-file>
    <welcome-file>default.htm</welcome-file>
    <welcome-file>default.jsp</welcome-file>
  </welcome-file-list>

</web-app>
```
index.jsp
```html
<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<h2>Hello World!</h2>
<a href="#">跳转连接</a>
</body>
</html>
```
##### 推荐项目初始化后，将以上内容添加到 web.xml 和 index.jsp。

<br>

# 一个完整 Spring 项目的配置过程

#### 1 对 Servlet 的配置，web.xml
Spring MVC 也有一个核心的 Servlet，称作 “DispatcherServlet”。 这个 dispatcherServlet 和任何 Servlet 一样，在 web.xml 中声明和映射（mapping）。 当然，也可以使用注解方式，此时就不需要 web.xml 了。

参考 Spring 文档的 Web Servlet 部分，Spring Web MVC -> DispatcherServlet 的介绍进行 web.xml 的配置。

#### 2 基于 Context Hierarchy，配置 spring-mvc.xml
DispatcherServlet 是通过委托一些特殊的 Bean 对象来完成 request 对象处理，以及 response 的渲染。

参考 Spring 文档的 Web Servlet 部分，Spring Web MVC -> DispatcherServlet -> Context Hierarchy 以及 Special Bean Types 的介绍进行 spring-mvc.xml 的配置。

#### 3 applicationContext.xml 的配置

关于 Spring 的逻辑和 Spring MVC 入门，查看 [../springmvc](../springmvc)。

## Spring 的 log4j 日志配置
log4j 的依赖包 Apache Log4j （1.x版本）
```xml
<dependency>
    <groupId>log4j</groupId>
    <artifactId>log4j</artifactId>
    <version>1.2.17</version>
</dependency>
```
##### 配置
Spring 默认加载的是 classpath 目录下面的 log4j.properties 文件，如果你的配置文件不是这个名称，需要在 web.xml 中进行配置。
``此处虽然使用相同名字，但是也可以多此一举地再显示配置一次。``

web.xml （log4j 1.x版本）
```xml
<context-param>
    <param-name>log4jConfigLocation</param-name>
    <param-value>classpath:log4j.properties</param-value>
</context-param>

<!-- 设定刷新日志配置文件的时间间隔，这里设置为 10s -->
<context-param>
    <param-name>log4jRefreshInterval</param-name>
    <param-value>10000</param-value>
</context-param>

<!--需要配置在 ContextLoaderListener之前 （记录后端日志）-->
<listener>
    <listener-class>org.springframework.web.util.Log4jConfigListener</listener-class>
</listener>

<!-- 放置于 log4j 的 listener 元素之后，log4j2 日志过滤器(记录前端日志) -->
<filter>
    <filter-name>log4jServletFilter</filter-name>
    <filter-class>org.apache.logging.log4j.web.Log4jServletFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>log4jServletFilter</filter-name>
    <url-pattern>/*</url-pattern>
    <dispatcher>REQUEST</dispatcher>
    <dispatcher>FORWARD</dispatcher>
    <dispatcher>INCLUDE</dispatcher>
    <dispatcher>ERROR</dispatcher>
    <dispatcher>ASYNC</dispatcher>
</filter-mapping>
```

注意，org.springframework.web.util.Log4jConfigListener 这个类在 Spring 5.0 及以上版本已废除。新版本推荐使用 log4j2（2.x版本），``此时的配置文件是 log4j2.properties``，依赖包如下：
```xml
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-core</artifactId>
    <version>2.11.1</version>
</dependency>

<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-api</artifactId>
    <version>2.11.1</version>
</dependency>

<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-web</artifactId>
    <version>2.11.1</version>
</dependency>
```

web.xml （log4j 2.x版本）
```xml
<context-param>
  <param-name>log4jConfigLocation</param-name>
  <param-value>classpath:log4j2.xml</param-value>
</context-param>

<!-- 设定刷新日志配置文件的时间间隔，这里设置为 10s -->
<context-param>
  <param-name>log4jRefreshInterval</param-name>
  <param-value>10000</param-value>
</context-param>

<!--需要配置在 ContextLoaderListener之前 （记录后端日志） -->
<listener>
  <listener-class>org.apache.logging.log4j.web.Log4jServletContextListener</listener-class>
</listener>

<!-- 放置于 log4j 的 listener 元素之后，log4j2 日志过滤器(记录前端日志) -->
<filter>
    <filter-name>log4jServletFilter</filter-name>
    <filter-class>org.apache.logging.log4j.web.Log4jServletFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>log4jServletFilter</filter-name>
    <url-pattern>/*</url-pattern>
    <dispatcher>REQUEST</dispatcher>
    <dispatcher>FORWARD</dispatcher>
    <dispatcher>INCLUDE</dispatcher>
    <dispatcher>ERROR</dispatcher>
    <dispatcher>ASYNC</dispatcher>
</filter-mapping>
```

##### log4j 的配置文件内容
##### log4j 包含三个组件，分别是 Logger(记录器)、Appender(输出目的地)、Layout(日志布局)。

配置 Logger 记录器
```
log4j.rootLogger = [ level ] , appenderName, appenderName, ...
其中，
▫ level 表示日志记录的优先级，由高到低分别为 OFF、FATAL、ERROR、WARN、INFO、DEBUG、ALL或者你定义的级别。
▫ appenderName 就是指日志输出的目的。（可以灵活地定义日志输出，也可以同时指定多个输出目的地。）
```

配置 Appender 输出目的地
```
# 输出目的地的类型
org.apache.log4j.ConsoleAppender（控制台）
org.apache.log4j.FileAppender（文件）
org.apache.log4j.DailyRollingFileAppender（每天产生一个日志文件）
org.apache.log4j.RollingFileAppender（文件大小到达指定尺寸的时候产生一个新的文件）
org.apache.log4j.WriterAppender（将日志信息以流格式发送到任意指定的地方）
```

配置 layout 日志布局
```
org.apache.log4j.HTMLLayout（HTML表格形式）
org.apache.log4j.SimpleLayout（简单格式的日志，只包括日志信息的级别和指定的信息字符串 ，如:DEBUG - Hello）
org.apache.log4j.TTCCLayout（日志的格式包括日志产生的时间、线程、类别等等信息）
org.apache.log4j.PatternLayout（灵活地自定义日志格式）
# 使用 org.apache.log4j.PatternLayout 来自定义信息格式时，可以使用 ConversionPattern=%-d{yyyy-MM-dd HH:mm:ss} [%c {Num}] [%l] [ %t:%r ] - [ %p ]  %m%n 来格式化信息。
```

log4j.properties （1.x版本 - 对应 Spring 4 版本）
```
### set log levels （注意，此处的 D, E 是自定义级别） ###
log4j.rootLogger = INFO, D, E

log4j.appender.D = org.apache.log4j.RollingFileAppender
log4j.appender.D.File =${scheduleProject}WEB-INF/logs/schedule.log
log4j.appender.D.Append = true
log4j.appender.D.Threshold = DEBUG
log4j.appender.D.MaxFileSize = 50000KB
log4j.appender.D.layout = org.apache.log4j.PatternLayout
log4j.appender.D.layout.ConversionPattern = %-d{yyyy-MM-dd HH:mm:ss}  [ %t:%r ] - [ %p ]  %m%n

log4j.appender.E = org.apache.log4j.RollingFileAppender
log4j.appender.E.File = ${scheduleProject}WEB-INF/logs/schedule.log
log4j.appender.E.Append = true
log4j.appender.E.Threshold = ERROR
log4j.appender.E.MaxFileSize = 50000KB
log4j.appender.E.layout = org.apache.log4j.PatternLayout
log4j.appender.E.layout.ConversionPattern =%-d{yyyy-MM-dd HH\:mm\:ss}  [ %l\:%c\:%t\:%r ] - [ %p ]  %m%n
```

log4j2.xml （2.x版本 - 对应 Spring 5.0 及以上） ``注意，可以使用 properties 文件，但是 xml 的层次结构更好。``
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- 设置 status=debug 可以查看 log4j 的加载过程，显示的非常详细。
     如果不知道配置的文件存到了哪里，将 status 从 off 改为 debug 即可查看详细过程。-->
<configuration status="off">

  <!-- 指定文件路径 -->
  <properties>
    <!-- 设置日志在硬盘上输出的目录 ${log4j:configParentLocation}，
         使用此查找将日志文件放在相对于 log4j 配置文件的目录中 -->
    <property name="Log_Home">${web:rootDir}/logs</property>
  </properties>

  <!-- 先定义所有的 appender -->
  <appenders>
    <!-- 输出控制台的配置 -->
    <Console name="Console" target="SYSTEM_OUT">
      <!-- 输出日志的格式
           %L:：输出代码中的行号。
           %M：输出产生日志信息的方法名。-->
      <!-- "%highlight{%d{HH:mm:ss.SSS} %-5level %logger{36}.%M() @%L - %msg%n}{FATAL=Bright Red, ERROR=Bright Magenta, WARN=Bright Yellow, INFO=Bright Green, DEBUG=Bright Cyan, TRACE=Bright White}" -->
      <PatternLayout pattern="%d{HH:mm:ss.SSS} %-5level %class{36}.%M @%L :-> %msg%xEx%n"/>
    </Console>

    <!-- 这个会打印出所有的信息，每次大小超过 size，则这 size 大小的日志会自动存入按年份-月份建立的文件夹下面并进行压缩，作为存档 -->
    <RollingFile name="RollingFileInfo" fileName="${Log_Home}/info.${date:yyyy-MM-dd}.log" immediateFlush="true" filePattern="${Log_Home}/$${date:yyyy-MM}/info-%d{MM-dd-yyyy}-%i.log.gz">
      <PatternLayout pattern="%d{yyyy-MM-dd 'at' HH:mm:ss z} %-5level %class{36}.%M @%L :-> %msg%xEx%n"/>
      <!-- 控制台只输出 level 及以上级别的信息（onMatch），其他的直接拒绝（onMismatch）-->
      <filters>
        <ThresholdFilter level="error" onMatch="DENY" onMismatch="NEUTRAL"/>
        <ThresholdFilter level="info" onMatch="ACCEPT" onMismatch="DENY"/>
      </filters>
      <Policies>
        <TimeBasedTriggeringPolicy modulate="true" interval="1"/>
        <SizeBasedTriggeringPolicy size="10MB"/>
      </Policies>
    </RollingFile>

    <!-- 这个会打印出所有的信息，每次大小超过 size，则这 size 大小的日志会自动存入按年份-月份建立的文件夹下面并进行压缩，作为存档 -->
    <RollingFile name="RollingFileDebug" fileName="${Log_Home}/debug.${date:yyyy-MM-dd}.log" immediateFlush="true" filePattern="${Log_Home}/$${date:yyyy-MM}/debug-%d{MM-dd-yyyy}-%i.log.gz">
      <PatternLayout pattern="%d{yyyy-MM-dd 'at' HH:mm:ss z} %-5level %class{36}.%M @%L :-> %msg%xEx%n"/>
      <filters>
        <ThresholdFilter level="info" onMatch="DENY" onMismatch="NEUTRAL"/>
        <ThresholdFilter level="debug" onMatch="ACCEPT" onMismatch="NEUTRAL"/>
      </filters>
      <Policies>
        <TimeBasedTriggeringPolicy modulate="true" interval="1"/>
        <SizeBasedTriggeringPolicy size="10MB"/>
      </Policies>
    </RollingFile>

    <!-- 这个会打印出所有的信息，每次大小超过 size，则这 size 大小的日志会自动存入按年份-月份建立的文件夹下面并进行压缩，作为存档 -->
    <RollingFile name="RollingFileError" fileName="${Log_Home}/error.${date:yyyy-MM-dd}.log" immediateFlush="true" filePattern="${Log_Home}/$${date:yyyy-MM}/error-%d{MM-dd-yyyy}-%i.log.gz">
      <PatternLayout pattern="%d{yyyy-MM-dd 'at' HH:mm:ss z} %-5level %class{36}.%M @%L :-> %msg%xEx%n"/>
      <ThresholdFilter level="error" onMatch="ACCEPT" onMismatch="DENY"/>
      <Policies>
        <TimeBasedTriggeringPolicy modulate="true" interval="1"/>
        <SizeBasedTriggeringPolicy size="10MB"/>
      </Policies>
    </RollingFile>
  </appenders>

  <!-- 优先级提醒： trace < debug < info < warn < error < fatal -->

  <!-- 现在定义 logger，只有定义了 logger，并引入相应的 appender，appender 才会生效 -->
  <!-- 过滤掉 spring 和 mybatis 的一些无用的 DEBUG 信息 -->
  <!-- log4j 的 additivity 属性： additivity 是 “子Logger” 是否继承 “父Logger” 的输出源（appender）的标志位。
       具体说，默认情况下子Logger会继承父Logger的appender，也就是说子Logger会在父Logger的appender里输出。
       若是additivity设为false，则子Logger只会在自己的appender里输出，而不会在父Logger的appender里输出。！ -->
  <!-- <logger name="org" level="INFO" additivity="false" ></logger> -->
  <!-- <logger name="org.springframework" level="INFO" additivity="false"></logger> -->
  <!-- <logger name="org.mybatis" level="INFO" additivity="false"></logger> -->
  <loggers>
    <logger name="org.springframework.core" level="info"></logger>
    <logger name="org.springframework.beans" level="info"></logger>
    <logger name="org.springframework.context" level="info"></logger>
    <logger name="org.springframework.web" level="info"></logger>
    <!-- 建立一个默认的 root 的 logger -->
    <root level="info">
      <appender-ref ref="Console"/>
      <appender-ref ref="RollingFileInfo"/>
      <appender-ref ref="RollingFileDebug"/>
      <appender-ref ref="RollingFileError"/>
    </root>
  </loggers>
</configuration>
```

###### Log4j2 介绍
```
Log4j2 配置文件关键节点：
1. LoggerContext： 日志系统上下文。 （仅是一个抽象概念）
2. Configuration： 每一个 LoggerContext 仅有一个有效的 Configuration，是 xml 配置文件的根元素标签。
3. Logger： Logger 继承自 AbstractLogger，即日志对象。
4. LoggerConfig： 一组 Appender 的引用，对应 \<appenders> 标签。
5. Appender： 用于指定日志的输出目的地，一个 appender 就是一个输出目的地。 （\<appenders> 内的子元素）
6. Filter： 过滤消息事件。
7. Layout： 用于自定义日志格式。
8. StrSubstitutor 和 StrLookup： 用于对 Log4j2 的各项配置项进行动态变量赋值。（用于支持配置文件内变量定义。）
9. 日志级别。
```

Log4j 中文教程
* http://www.docs4dev.com/docs/zh/log4j2/2.x/all （log4j2）
* http://www.yiibai.com/log4j （log4j）

在尝试配置之前，应先了解 loggers 如何在 Log4j 中工作至关重要。试图在不理解这些概念的情况下配置 Log4j 会导致挫败感。
http://www.docs4dev.com/docs/zh/log4j2/2.x/all/manual-architecture.html

#### Spring 的日志体系

##### Spring 4 的日志技术实现
查看 spring-context-4.1.9.jar 包依赖，可以发现 spring4 底层依赖了 commons-logging.jar。
```
# spring-context 依赖关系
 > spring-aop
 > spring-beans
 > spring-core
   > commons-logging
 > spring-expression
```

##### Spring 5 的日志技术实现
```
# spring-context 依赖关系
 > spring-aop
 > spring-beans
 > spring-core
   > spring-jcl （Jakarta Commons Logging）
 > spring-expression
```
spring5 中默认是使用 jcl 的接口，它的日志体系更加强大了，通过循环优先机制，优先扫描 log4j2，还可以使用 “slf4j+绑定器” 的方式与市面上各种主流日志框架进行集成。 ``SLF4J 是众多日志系统的内核，提供统一的接口，不提供具体实现。``

## Spring MVC 表单提交 400 错误排查

当前台 form 表单中的参数和后台接受的参数类型不一致时，将出现异常，会返回 400 错误。但是。。``400 错误会被 springmvc 默认忽略，难以定位错误原因。`` spring mvc 的 400 错误定位追踪是一个很让人头疼的问题。

##### 为了方便 400 错误排查，请将 springmvc 的日志级别都调成 debug。
```xml
<loggers>
    <logger name="org.springframework.core" level="debug"></logger>
    <logger name="org.springframework.beans" level="debug"></logger>
    <logger name="org.springframework.context" level="debug"></logger>
    <logger name="org.springframework.web" level="debug"></logger>
    <!-- 建立一个默认的 root 的 logger -->
    <root level="debug">
        <appender-ref ref="Console"/>
        <appender-ref ref="RollingFileInfo"/>
        <appender-ref ref="RollingFileDebug"/>
        <appender-ref ref="RollingFileError"/>
   </root>
</loggers>
```
注意，本方法仅对开发环境的 debug，返回 400 错误本身就应该是避免出现的问题。``注意给前端添加类型一致验证提示功能。``

<br>

# 订单分页查询 PageHelper
PageHelper 是国内非常优秀的一款开源的 mybaits 分页插件，支持基本主流且常用的数据库，如 mysql、oracle、mariaDB、DB2、SQLite、Hsqldb 等。

* 项目的 GitHub 地址：http://github.com/pagehelper/Mybatis-PageHelper
* 项目的 GitOsc 地址：http://gitee.com/free/Mybatis_PageHelper (Gitee，又名 Git OS China。)

maven 依赖环境
```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper</artifactId>
    <version>5.1.2</version>
</dependency>
```

#### 使用步骤

##### 配置
特别注意，新版拦截器是 ``com.github.pagehelper.PageInterceptor``。 ``com.github.pagehelper.PageHelper`` 现在是一个特殊的 ``dialect`` 实现类，是分页插件的默认实现类，提供了和以前相同的用法。

在 Mybatis 配置 xml 中配置拦截器插件 （单独使用 Mybatis 时的用法）
```xml
<!--
    plugins 在配置文件中的位置必须符合要求，否则会报错，顺序如下：
    properties?, settings?,
    typeAliases?, typeHandlers?,
    objectFactory?, objectWrapperFactory?,
    plugins?,
    environments?, databaseIdProvider?, mappers?
 -->
<plugins>
    <!-- com.github.pagehelper 为 PageHelper 类所在包名 -->
    <plugin interceptor="com.github.pagehelper.PageInterceptor">
        <!-- 使用下面的方式配置参数，后面会有所有的参数介绍 -->
        <property name="param1" value="value1"/>
    </plugin>
</plugins>
```

在 Spring 配置文件中配置拦截器插件 （Spring 项目中的用法）
```xml
<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
    <!-- 注意其他配置 -->
    <property name="plugins">
        <array>
          <bean class="com.github.pagehelper.PageInterceptor">
            <property name="properties">
                <!-- 使用下面的方式配置参数，一行配置一个 -->
                <value>params=value1</value>
            </property>
          </bean>
        </array>
    </property>
</bean>
```

##### Spring 配置实例
```xml
<!-- spring 和 mybatis 整合 -->
<context:property-placeholder location="classpath:db.properties"/>
<bean id="dataSource" class="com.mchange.v2.c3p0.ComboPooledDataSource">
    <property name="driverClass" value="${jdbc.driver}"/>
    <property name="jdbcUrl" value="${jdbc.url}"/>
    <property name="user" value="${jdbc.username}"/>
    <property name="password" value="${jdbc.password}"/>
</bean>
<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
    <property name="dataSource" ref="dataSource" />
    <!-- 传入 PageHelper 的插件 -->
    <property name="plugins">
        <array>
            <!-- 传入插件的对象 -->
            <bean class="com.github.pagehelper.PageInterceptor">
                <property name="properties">
                    <props>
                        <prop key="helperDialect">mysql</prop>
                        <prop key="reasonable">true</prop>
                    </props>
                </property>
            </bean>
        </array>
    </property>
</bean>
```

##### 分页插件参数介绍
* helperDialect 指定 sql 语句使用的方言，即指定使用的数据库名称。
* offsetAsPageNum 默认值 ``false``。当设置为 ``true`` 时，将 ``RowBounds`` 中的 ``offset`` 参数当作 ``pageNum`` 使用。
* rowBoundsWithCount 默认值 ``false``。当设置为 ``true`` 时，使用 ``RowBounds`` 分页时会进行 count 查询。
* pageSizeZero 默认值 ``false``。当设置为 ``true`` 时，如果 ``pageSize=0`` 或 ``RowBounds.limit=0`` 就会查询出全部的结果。
* reasonable 分页合理化参数，默认值 ``false``。当设置为 ``true`` 时，``pageNum<=0`` 会查询第一页，``pageNum>pages`` 会查询最后一页。 推荐使用 true。
* params 用于从对象中根据属性名取值。 可以配置 ``pageNum, pageSize, count, pageSizeZero, resonable``，不配置映射的用默认值，默认值为 ``pageNum=pageNum; pageSize=pageSize; count=countSql; reasonable=reasonable; pageSizeZero=pageSizeZero``。

#### 使用示例

##### PageHelper.startPage 静态方法调用（重点）
```
//获取第1页，10条内容，默认查询总数count
PageHelper.startPage(1, 10);
//紧接着的第一个select方法会被分页
List<Country> list = countryMapper.selectIf(1);
```

##### 订单分页查询
**Dao**
```java
public interface IOrdersDao {
    @Select("select * from orders")
    @Results({
            @Result(id=true, property = "id", column = "id"),  //true代表主键
            @Result(property = "orderNum", column = "orderNum"),
            @Result(property = "orderTime", column = "orderTime"),
            @Result(property = "orderStatus", column = "orderStatus"),
            @Result(property = "payType", column = "payType"),
            @Result(property = "orderDesc", column = "orderDesc"),
            @Result(property = "peopleCount", column = "peopleCount"),
            @Result(property = "product", column = "productId", javaType = Product.class, one = @One(select = "com.petersdemo.ssm.dao.IProductDao.findById")),
            @Result(property = "member", column = "memberId", javaType = Member.class, one=@One(select = "com.petersdemo.ssm.dao.IMemberDao.findById"))
    })
    public List<Orders> findAll() throws Exception;
}
```
**Service**
```java
@Override
public List<Orders> findAllByPage(int page, int pageSize) throws Exception {
    PageHelper.startPage(page, pageSize);
    return ordersDao.findAll();
}
```
**Controller**
```java
@RequestMapping("/findAllByPage.do")
public ModelAndView findAllByPage(
        @RequestParam(name = "page", required = true, defaultValue = "1") int page,
        @RequestParam(name = "pageSize", required = true, defaultValue = "10") int pageSize
) throws Exception {
    ModelAndView mv = new ModelAndView();
    List<Orders> ordersList = ordersService.findAllByPage(page, pageSize);
    PageInfo pageInfo = new PageInfo(ordersList);  //PageInfo就是一个分页Bean，可以用它来访问/配置分页参数
    mv.addObject("pageInfo", pageInfo);
    mv.setViewName("orders-page-list");
    return mv;
}
```
**jsp**
```html
<%@ page language="java" contentType="text/html;charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
</head>
<body>

  <!-- 列表显示 -->
  <c:forEach items="${pageInfo.list}" var="order">
      <!-- 获取order的属性值 -->
      ${order.id}
      ${order.orderNum}
  </c:forEach>
  <!-- /列表显示 -->

  <!-- 分页后的页码 -->
  <ul>
      <c:forEach begin="1" end="${pageInfo.pages}" var="pageNum">
        <li><a href="#">${pageNum}</a></li>
      </c:forEach>
  </ul>
  <!-- /分页后的页码 -->

</body>
</html>
```

<br>

# Spring Security 进行登陆认证和密码加密
Spring Security 中文文档 http://www.docs4dev.com/docs/zh/spring-security/5.1.2.RELEASE/reference

#### Maven 环境配置
在没有 Spring Boot 的情况下使用 Spring Security 时，首选方法是利用 Spring Security 的 BOM 来确保整个项目中使用 Spring Security 的一致 version。
```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-bom</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```
最小的 Spring Security Maven 依赖项集通常如下所示：
```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-web</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-config</artifactId>
    <version>5.0.12.RELEASE</version>
</dependency>
```

#### Spring Security 进行登陆认证

##### 配置步骤
第1步，导入 Spring Security 的依赖。
* security-web
* security-config

第2步，在 web.xml 中创建 Filter。 （Filter 是 Servlet 请求拦截的核心。）
```xml
<!-- spring security 配置文件导入 -->
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath*:spring-security.xml</param-value>
</context-param>
<!-- 配置监听器 -->
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
<!-- Spring Security 配置 filter，使用该 filter 需要导入 spring security 依赖 -->
<filter>
    <!-- 注意，此处的 filter-name 不可以修改，这个名称是强制约束的。 -->
    <filter-name>springSecurityFilterChain</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
</filter>
<filter-mapping>
    <filter-name>springSecurityFilterChain</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

第3步， spring-security.xml 配置文件配置
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:security="http://www.springframework.org/schema/security"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/security
        http://www.springframework.org/schema/security/spring-security.xsd">

    <!-- 指定需要认证的 url 以及认证规则 -->
    <security:http auto-config="true" use-expressions="false">
        <!-- intercept-url 定义一个过滤规则，pattern 表示对哪些 url 进行权限控制，access 属性表示在请求对应的 url 时需要什么权限。
             默认配置时它应该是一个以逗号分隔的角色列表，请求的用户只需拥有其中的一个角色就能成功访问。 -->
        <security:intercept-url pattern="/**" access="ROLE_USER,ROLE_ADMIN" />
        <!-- auto-config 配置后，不需要再配置下面信息: <security:form-login /> 定义登陆表单信息，
             <security:http-basic /> 和 <security:logout /> -->
    </security:http>

    <security:authentication-manager>
        <security:authentication-provider>
            <security:user-service>
                <security:user name="user" password="{noop}user" authorities="ROLE_USER"/>
                <security:user name="admin" password="{noop}admin" authorities="ROLE_ADMIN"/>
            </security:user-service>
        </security:authentication-provider>
    </security:authentication-manager>

   </beans>
   ```
以上使用 Spring Security 拦截所有 url 并需要用户登陆才可访问，此时还没有添加密码加密功能，是最简单的 Spring Security 认证示例。
``两个账户： 用户名 user 密码 user 和 用户名 admin 密码 admin``

#### 使用 Spring Security 实现密码加密

maven 依赖如下，web.xml 的配置则和上面登陆认证的配置一样。
```xml
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-web</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-config</artifactId>
    <version>5.0.12.RELEASE</version>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-crypto</artifactId>
    <version>5.0.2.RELEASE</version>
</dependency>
```
spring-security.xml 配置文件
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:security="http://www.springframework.org/schema/security"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/security
        http://www.springframework.org/schema/security/spring-security.xsd">

    <!-- 指定需要认证的 url 以及认证规则 -->
    <security:http auto-config="true" use-expressions="false">
        <!-- intercept-url 定义一个过滤规则，pattern 表示对哪些 url 进行权限控制，access 属性表示在请求对应的 url 时需要什么权限。
             默认配置时它应该是一个以逗号分隔的角色列表，请求的用户只需拥有其中的一个角色就能成功访问。 -->
        <security:intercept-url pattern="/**" access="ROLE_USER,ROLE_ADMIN" />
        <!-- auto-config 配置后，不需要再配置下面信息: <security:form-login /> 定义登陆表单信息，
             <security:http-basic /> 和 <security:logout /> -->
    </security:http>

    <!-- 自定义的 UserDetailsService 实现类，是一个扩展了 UserDetailsService 接口的 IUserService 实现类 -->
    <bean id="userService" class="com.petersdemo.ssm.service.impl.UserServiceImpl"/>

    <!-- 此处切换成使用数据库中的用户名和密码来认证，此时，IUserService 需要 extends UserDetailsService -->
    <!-- 由于自定义类扩展了 UserDetailsService 接口，此时在认证时，就会调用实现类的 loadUserByUsername 函数，
         该函数必须返回一个 UserDetails 对象。 -->
    <security:authentication-manager>
        <security:authentication-provider user-service-ref="userService">
            <!-- 配置加密的方式 -->
            <security:password-encoder ref="passwordEncoder"/>
        </security:authentication-provider>
    </security:authentication-manager>

    <!-- 配置加密类 -->
    <bean id="passwordEncoder" class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder"/>

</beans>
```
IUserService
```java
package com.petersdemo.ssm.service;

import com.petersdemo.ssm.domain.UserInfo;
import org.springframework.security.core.userdetails.UserDetailsService;

import java.util.List;

/* 注意，IUserService 接口必须扩展自 UserDetailsService */
public interface IUserService extends UserDetailsService {

    public List<UserInfo> findAll() throws Exception;

    public void save(UserInfo userInfo) throws Exception;
}
```
UserServiceImpl
```java
package com.petersdemo.ssm.service.impl;

import com.petersdemo.ssm.dao.IUserInfoDao;
import com.petersdemo.ssm.domain.UserInfo;
import com.petersdemo.ssm.service.IUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

@Service()
@Transactional
public class UserServiceImpl implements IUserService {

    @Autowired
    private IUserInfoDao userInfoDao;
    @Autowired
    private BCryptPasswordEncoder bCryptPasswordEncoder;

    @Override
    public List<UserInfo> findAll() throws Exception {
        return userInfoDao.findAll();
    }

    @Override
    public void save(UserInfo userInfo) throws Exception {
        //对密码进行加密处理 （数据库保存的是加密后的密码）
        userInfo.setPassword(bCryptPasswordEncoder.encode(userInfo.getPassword()));
        userInfoDao.save(userInfo);
    }

    /* Spring Security 登陆认证的时候会使用这个 API 来从数据库查找用户，然后与填写的用户信息对比。 */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserInfo userInfo = null;
        try {
            userInfo = userInfoDao.findByUsername(username);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        //处理自己的用户对象，然后封装成 UserDetails，此处省略了角色权限的查询
        User user = new User(userInfo.getUsername(), userInfo.getPassword(), userInfo.getStatus() == 0 ? false : true, true, true, true, getAuthorities());
        return user;
    }

    // 作用是返回一个 List 集合，集合中装入的是角色描述。 （总之就是获取用户对应的角色名，一般从 user_role 中间表查询）
    // public List<SimpleGrantedAuthority> getAuthorities(List<Role> roles) {
    // }

    /**
     * 该方法是上面的 getAuthorities 方法的省事实现，仅为了 Spring Security 的配置和测试。
     * 获取用户的角色权限，为了降低实验的难度，这里去掉了根据用户名获取角色的步骤，就不从数据库中查了。
     * @param - NULL
     * @return - List<SimpleGrantedAuthority>
     */
    private List<SimpleGrantedAuthority> getAuthorities(){
        List<SimpleGrantedAuthority> authList = new ArrayList<SimpleGrantedAuthority>();
        authList.add(new SimpleGrantedAuthority("ROLE_USER"));
        authList.add(new SimpleGrantedAuthority("ROLE_ADMIN"));
        return authList;
    }
}
```

##### 如果单独使用 BCryptPasswordEncoder 对密码加密的话，如下所示：
```java
package com.petersdemo.ssm.utils;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

public class BCryptPasswordEncoderUtils {

    private static BCryptPasswordEncoder bCryptPasswordEncoder = new BCryptPasswordEncoder();

    public static String encodePassword(String password) {
        return bCryptPasswordEncoder.encode(password);
    }

    //测试用
    public static void main(String args[]) {
        String password = "123";
        String pwd = encodePassword(password);
        System.out.println(pwd);
    }
}
```

#### Spring Security 的用户认证逻辑

Spring Security 提供的认证策略
* 内存用户存储库，即显示的配置在spring配置文件中。
* 基于 jdbc 的用户存储库
* 基于 LDAP 的用户存储库
* OpenID 分散式用户身份识别系统
* 中心认证服务(CAS)
* X.509 证书
* 基于 JAAS 的提供者

下面主要介绍一下：基于内存用户存储库 和 基于jdbc的用户存储库 的方式。 其他方式，参阅 Spring Security 的认证章节。

##### 基于内存用户存储库的认证

首先，建立一个用户服务，配置所有的用户和它的权限信息。然后，交给认证管理器管理，认证管理器会将认证的任务交给一个或多个认证提供者。
``spring security 的依赖包导入和 web.xml 配置，参考前面的登陆认证如何配置。``

spring-security.xml 配置
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:security="http://www.springframework.org/schema/security"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/security
        http://www.springframework.org/schema/security/spring-security.xsd">

    <!-- 指定需要认证的 url 以及认证规则 -->
    <security:http auto-config="true" use-expressions="false">
        <!-- intercept-url 定义一个过滤规则，pattern 表示对哪些 url 进行权限控制，access 属性表示在请求对应的 url 时需要什么权限。
             默认配置时它应该是一个以逗号分隔的角色列表，请求的用户只需拥有其中的一个角色就能成功访问。 -->
        <security:intercept-url pattern="/**" access="user,admin" />
        <!-- auto-config 配置后，不需要再配置下面信息: <security:form-login /> 定义登陆表单信息，
             <security:http-basic /> 和 <security:logout /> -->
    </security:http>

    <!-- 基于 In-Memory 身份验证，注意，此时的密码分别是 root 和 peter 加密后的密码！ -->
    <security:user-service id="userService">
        <security:user name="root" password="$2a$10$MxlnDFAUb.ow5flfNZJ0uOOrEhySKXqDIr4VM7nVy5OKkTscbfSTu" authorities="admin"/>
        <security:user name="peter" password="$2a$10$s4ZDfRhICld6azP.3H9/0uzvX/zJUaVJXSEabHlxO9r7HK6JkI1ye" authorities="user"/>
    </security:user-service>

    <!-- 切换成 In-Memory 的用户名和密码 -->
    <security:authentication-manager>
        <security:authentication-provider user-service-ref="userService">
            <!-- 配置加密的方式 -->
            <security:password-encoder ref="passwordEncoder"/>
        </security:authentication-provider>
    </security:authentication-manager>

    <!-- 配置加密类 -->
    <bean id="passwordEncoder" class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder"/>

</beans>
```

##### 基于 JDBC 的身份验证

下面的 example 假定您已在 application 中定义了 DataSource。 此时，userService 的定义使用 ``<security:jdbc-user-service>``。
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:security="http://www.springframework.org/schema/security"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/security
        http://www.springframework.org/schema/security/spring-security.xsd">

    <!-- 指定需要认证的 url 以及认证规则 -->
    <security:http auto-config="true" use-expressions="false">
        <!-- intercept-url 定义一个过滤规则，pattern 表示对哪些 url 进行权限控制，access 属性表示在请求对应的 url 时需要什么权限。
             默认配置时它应该是一个以逗号分隔的角色列表，请求的用户只需拥有其中的一个角色就能成功访问。 -->
        <security:intercept-url pattern="/**" access="user,admin" />
        <!-- auto-config 配置后，不需要再配置下面信息: <security:form-login /> 定义登陆表单信息，
             <security:http-basic /> 和 <security:logout /> -->
    </security:http>

    <!-- 基于 JDBC 身份验证，通过指定的 sql 语句在认证时自动读取数据库，然后认证。 -->
    <security:jdbc-user-service id="userService" data-source-ref="dataSource"
                                users-by-username-query="select username,password,status from users where username=?"
                                authorities-by-username-query="select username, role from user_role where username=?"/>

    <!-- 切换成 JDBC 查询用户名和密码 -->
    <security:authentication-manager>
        <security:authentication-provider user-service-ref="userService">
            <!-- 配置加密的方式 -->
            <security:password-encoder ref="passwordEncoder"/>
        </security:authentication-provider>
    </security:authentication-manager>

    <!-- 配置加密类 -->
    <bean id="passwordEncoder" class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder"/>

</beans>
```

##### 基于 UserDetailsService 的认证 （实现 UserDetailService 接口，来自定义认证过程）

Spring Security 中进行身份验证的是 AuthenticationManager 接口，ProviderManager 是它的一个默认实现，但它并不用来处理身份认证，而是委托给配置好的 AuthenticationProvider，每个 AuthenticationProvider 会轮流检查身份认证。 检查后或者返回Authentication对象或者抛出异常。

所谓验证身份，核心就是得到一个 UserDetails 对象（从内存获取或读数据库获取），拿它和用户输入的账号、密码、权限等信息匹配。 此步骤由实现 AuthenticationProvider 的 DaoAuthenticationProvider（它利用 UserDetailsService 验证用户名、密码和授权）处理。

下面，我们自定义一个 UserDetailsService 的实现类，来自定义身份验证过程。下面的 example，将自定义身份验证，假设 IUserService 扩展自 UserDetailsService 接口。

spring-security.xml 配置
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:security="http://www.springframework.org/schema/security"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/security
        http://www.springframework.org/schema/security/spring-security.xsd">

    <!-- 指定需要认证的 url 以及认证规则 -->
    <security:http auto-config="true" use-expressions="false">
        <!-- intercept-url 定义一个过滤规则，pattern 表示对哪些 url 进行权限控制，access 属性表示在请求对应的 url 时需要什么权限。
             默认配置时它应该是一个以逗号分隔的角色列表，请求的用户只需拥有其中的一个角色就能成功访问。 -->
        <security:intercept-url pattern="/**" access="ROLE_USER,ROLE_ADMIN" />
        <!-- auto-config 配置后，不需要再配置下面信息: <security:form-login /> 定义登陆表单信息，
             <security:http-basic /> 和 <security:logout /> -->
    </security:http>

    <!-- 自定义的 UserDetailsService 实现类，是一个扩展了 UserDetailsService 接口的 IUserService 实现类 -->
    <bean id="userService" class="com.petersdemo.ssm.service.impl.UserServiceImpl"/>

    <!-- 由于自定义类扩展了 UserDetailsService 接口，此时在认证时，就会调用实现类的 loadUserByUsername 函数，
         该函数必须返回一个 UserDetails 对象。 -->
    <security:authentication-manager>
        <security:authentication-provider user-service-ref="userService">
            <!-- 配置加密的方式 -->
            <security:password-encoder ref="passwordEncoder"/>
        </security:authentication-provider>
    </security:authentication-manager>

    <!-- 配置加密类 -->
    <bean id="passwordEncoder" class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder"/>

</beans>
```
IUserService
```java
package com.petersdemo.ssm.service;

import com.petersdemo.ssm.domain.UserInfo;
import org.springframework.security.core.userdetails.UserDetailsService;

import java.util.List;

/* 注意，IUserService 接口必须扩展自 UserDetailsService */
public interface IUserService extends UserDetailsService {

    public List<UserInfo> findAll() throws Exception;

    public void save(UserInfo userInfo) throws Exception;
}
```
UserServiceImpl
```java
package com.petersdemo.ssm.service.impl;

import com.petersdemo.ssm.dao.IUserInfoDao;
import com.petersdemo.ssm.domain.UserInfo;
import com.petersdemo.ssm.service.IUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

@Service()
@Transactional
public class UserServiceImpl implements IUserService {

    @Autowired
    private IUserInfoDao userInfoDao;
    @Autowired
    private BCryptPasswordEncoder bCryptPasswordEncoder;

    @Override
    public List<UserInfo> findAll() throws Exception {
        return userInfoDao.findAll();
    }

    @Override
    public void save(UserInfo userInfo) throws Exception {
        //对密码进行加密处理
        userInfo.setPassword(bCryptPasswordEncoder.encode(userInfo.getPassword()));
        userInfoDao.save(userInfo);
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        UserInfo userInfo = null;
        try {
            userInfo = userInfoDao.findByUsername(username);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        //处理自己的用户对象，然后封装成 UserDetails，此处省略了角色权限的查询
        User user = new User(userInfo.getUsername(), userInfo.getPassword(), userInfo.getStatus() == 0 ? false : true, true,true,true, getAuthorities());
        return user;
    }

    // 作用是返回一个 List 集合，集合中装入的是角色描述。 （总之就是获取用户对应的角色名，一般从 user_role 中间表查询）
    // public List<SimpleGrantedAuthority> getAuthorities(List<Role> roles) {
    // }

    /**
     * 该方法是上面的 getAuthorities 方法的省事实现，仅为了 Spring Security 的配置和测试。
     * 获取用户的角色权限，为了降低实验的难度，这里去掉了根据用户名获取角色的步骤，就不从数据库中查了。
     * @param - NULL
     * @return - List<SimpleGrantedAuthority>
     */
    private List<SimpleGrantedAuthority> getAuthorities(){
        List<SimpleGrantedAuthority> authList = new ArrayList<SimpleGrantedAuthority>();
        authList.add(new SimpleGrantedAuthority("ROLE_USER"));
        authList.add(new SimpleGrantedAuthority("ROLE_ADMIN"));
        return authList;
    }
}
```
注意，强制要求自定义的 Service 接口扩展自 Spring Security 的 ``UserDetailsService`` 接口，是为了使用 ``loadUserByUsername`` API 来和框架的登陆认证系统对接，对接方式就是返回一个 UserDetails 对象，内部含有用户名、密码、状态和角色名称。

#### Spring Security 的所有项目模块
1. 核心 - spring-security-core.jar
   ```
   包含核心身份验证和 access-contol classes 和接口，远程支持和基本配置 API。
   任何使用 Spring Security 的 application 都需要。
   包含 top-level 包：
   * org.springframework.security.core
   * org.springframework.security.access
   * org.springframework.security.authentication
   * org.springframework.security.provisioning
   ```
2. Remoting - spring-security-remoting.jar
   ```
   提供与 Spring Remoting 的整合。
   除非您正在编写使用 Spring Remoting 的 remote client，否则您不需要这样做。
   ```
3. Web - spring-security-web.jar
   ```
   包含过滤器和相关的 web-security infrastructure code。任何具有 servlet API 依赖性的东西。
   如果您需要 Spring Security web 身份验证服务和 URL-based access-control，则需要它。
   ```
4. 配置 - spring-security-config.jar
   ```
   包含解析 code 和 Java configuration code 的安全名称空间。
   如果您使用 Spring Security XML 命名空间进行 configuration 或 Spring Security 的 Java Configuration 支持，则需要它。
   ```
5. LDAP - spring-security-ldap.jar
   ```
   LDAP 身份验证和配置 code。
   如果您需要使用 LDAP 身份验证或管理 LDAP 用户条目，则为必需。
   ```
6. OAuth 2.0 核心 - spring-security-oauth2-core.jar
   ```
   为 OAuth 2.0 Authorization Framework 和 OpenID Connect Core 1.0 提供支持。
   使用 OAuth 2.0 或 OpenID Connect Core 1.0 的 applications 需要它。
   ```
7. OAuth 2.0 Client - spring-security-oauth2-client.jar
   ```
   Spring Security 的 client 支持 OAuth 2.0 授权 Framework 和
   OpenID Connect Core 1.0. applications 利用 OAuth 2.0 登录 and/or OAuth Client 支持。
   ```
8. OAuth 2.0 JOSE - spring-security-oauth2-jose.jar
   ```
   包含 Spring Security 对 JOSE(Javascript Object 签名和加密)framework 的支持。
   它由一系列规范构建：
   * JSON Web 令牌(JWT)
   * JSON Web 签名(JWS)
   * JSON Web 加密(JWE)
   * JSON Web Key(JWK)
   ```
9. ACL - spring-security-acl.jar
   ```
   专门域 object ACL implementation。
   用于将安全性应用于 application 中的特定域 object 实例。
   ```
10. CAS - spring-security-cas.jar
    ```
    Spring Security 的 CAS client integration。
    如果要对 CAS 单 sign-on 服务器使用 Spring Security web 身份验证。
    ```
11. OpenID - spring-security-openid.jar
    ```
    OpenID web 身份验证支持。
    用于针对外部 OpenID 服务器对用户进行身份验证。
    ```
12. 测试 - spring-security-test.jar
    ```
    支持使用 Spring Security 进行测试。
    ```

#### 使用自定义的 login 页面完成 Spring Security 的登陆认证
1. 导入 Spring Security 的依赖，同上。
2. web.xml 中创建 Filter，同上。
3. spring-security.xml 配置文件配置
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <beans xmlns="http://www.springframework.org/schema/beans"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xmlns:security="http://www.springframework.org/schema/security"
          xsi:schemaLocation="http://www.springframework.org/schema/beans
           http://www.springframework.org/schema/beans/spring-beans.xsd
           http://www.springframework.org/schema/security
           http://www.springframework.org/schema/security/spring-security.xsd">

       <!-- 配置不过滤的资源 (静态资源及登陆相关) -->
       <security:http security="none" pattern="/pages/login.jsp" />
       <security:http security="none" pattern="/pages/failer.jsp"/>
       <security:http auto-config="true" use-expressions="false">
           <!-- 配置拦截的连接，表示任意路径都需要 ROLE_USER 权限
                配置时它应该是一个以逗号分隔的角色列表，请求的用户只需拥有其中的一个角色就能成功访问。 -->
           <security:intercept-url pattern="/**" access="ROLE_USER,ROLE_ADMIN" />
           <!-- 自定义登陆页面，login-page 自定义登陆页面 authentication-failure-url 用户权限验证失败后才会跳转到这个 url
                default-target-url 登陆成功后跳转的页面。 注意，登陆页面用户名 username， 密码 password， action:login -->
           <security:form-login login-page="/pages/login.jsp"
                                login-processing-url="/login" username-parameter="username" password-parameter="password"
                                authentication-failure-url="/pages/failer.jsp"
                                default-target-url="/pages/hello.jsp"
                                authentication-success-forward-url="/pages/hello.jsp"
           />
           <!-- 用户退出，invalidate-session 是否删除 session， logout-url 登出处理链接（即：指定触发退出事件的url）
                logout-success-url 登出成功页面。
                注意，登出操作只需要链接到 logout 即可登出当前用户，不需要创建 logout.jsp 页面的。 -->
           <security:logout invalidate-session="true" logout-url="/logout"
                            logout-success-url="/pages/login.jsp" />
           <!-- 关闭 CSRF，防止页面中没有配置 crsf 而报错。 -->
           <security:csrf disabled="true"/>
       </security:http>

       <!-- 自定义的 UserDetailsService 实现类，是一个扩展了 UserDetailsService 接口的 IUserService 实现类 -->
       <bean id="userService" class="com.petersdemo.ssm.service.impl.UserServiceImpl"/>

       <!-- 此处切换成使用数据库中的用户名和密码来认证，此时，IUserService 需要 extends UserDetailsService -->
       <!-- 由于自定义类扩展了 UserDetailsService 接口，此时在认证时，就会调用实现类的 loadUserByUsername 函数，
            该函数必须返回一个 UserDetails 对象。 -->
       <security:authentication-manager>
           <security:authentication-provider user-service-ref="userService">
               <!-- 配置加密的方式 -->
               <security:password-encoder ref="passwordEncoder"/>
           </security:authentication-provider>
       </security:authentication-manager>

       <!-- 配置加密类 -->
       <bean id="passwordEncoder" class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder"/>

   </beans>
   ```
4. 登陆页面 login.html/login.jsp。
   ###### 注意，``action`` 必须指定为 ``login``，另外 ``method 为 post，用户名和密码输入框的 name 属性分别为 username、password``。 这是框架约定好的，不可修改。
   ```html
   <%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8"%>
   <!DOCTYPE html>
   <html>
   <head>
     <title>登陆认证</title>
   </head>
   <body>

     <!-- 登陆表单 -->
     <form action="${pageContext.request.contextPath}/login" method="POST">
        <table>
            <tr>
                <td>用户名：</td>
                <td><input type="text" name="username"/></td>
            </tr>
            <tr>
                <td>密码：</td>
                <td><input type="password" name="password"/></td>
            </tr>
            <tr>
                <td colspan="2" align="center">
                    <input type="submit" value="登陆"/>
                    <input type="reset" value="重置"/>
                </td>
            </tr>
        </table>
     </form>
     <!-- /登陆表单 -->

   </body>
   </html>
   ```
5. 用户退出。 用户退出需要在 ``<security:http auto-config="true" use-expressions="false">`` 中添加如下配置：
* spring-security.xml 添加配置
   ```xml
   <!-- 用户退出，invalidate-session 是否删除 session， logout-url 登出处理链接（即：指定触发退出事件的url）
             logout-success-url 登出成功页面。
             注意，登出操作只需要链接到 logout 即可登出当前用户，不需要创建 logout.jsp 页面的。 -->
   <security:logout invalidate-session="true" logout-url="/logout"
                    logout-success-url="/pages/login.jsp" />
   ```
* 在页面中添加/触发退出事件
  ```html
  <a href="${pageContext.request.contextPath}/logout" class="btn btn-default btn-flat">注销</a>
  ```
