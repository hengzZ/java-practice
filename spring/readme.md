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
```
IOC 设计模式的好处是，类名字符串还可以进一步放置于 xml 配置文件中，实现一套代码多种组合。

IOC 设计模式的最常见实现方式，叫做 “依赖注入”（Dependency Injection，DI），此外还有一种实现方式，叫 “依赖查找”（Dependency Lookup）。

#### AOP 设计模式
AOP 是 Aspect Oriented Programming 的缩写。 面向切面编程，通过预编译方式和运行期动态代理，实现程序功能的灵活性和可扩展性，AOP 也是 GoF 设计模式的延伸。

AOP 的初衷是将日志记录，性能统计，安全控制，事务处理，异常处理等非业务核心代码从业务逻辑代码中划分出来。

##### AOP 与 OOP 异同点 （封装 -> 切片）
* OOP 是对业务处理过程的实体及其属性和行为进行抽象封装。 （具体业务 -> 一个对象）
* AOP 则是对业务处理过程中的 “切面（处理过程中的某个步骤或阶段）” 进行提取。（动态代理技术）

```java
/**
 * AOP 设计模式实践
 */
public IAccountService getAccountService() {
    return (IAccountService)Proxy.newProxyInstance(
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
```
为对象添加代理是 AOP 的核心逻辑。

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
* 编写核心业务代码 （开发主线）
* 公用代码抽取，制作成通知。 （AOP 编程人员）
* 在配置文件中，声明切入点与通知的关系，即切面。 （AOP 编程人员）

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
