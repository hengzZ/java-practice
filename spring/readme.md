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
        https://www.springframework.org/schema/mvc/spring-mvc.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd
        http://www.springframework.org/schema/aop
        http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!-- 开启注解扫描，管理自定义的 controller 依赖 -->
    <context:component-scan base-package="com.petersdemo.ssm.controller">
    </context:component-scan>

    <!-- 配置视图解析器 -->
    <bean id="viewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
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
<web-app xmlns="http://java.sun.com/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="
        http://java.sun.com/xml/ns/javaee
        https://java.sun.com/xml/ns/javaee/web-app_3_0.xsd"
         version="3.0">

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
  <filter>
    <filter-name>springSecurityFilterChain</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
  </filter>
  <filter-mapping>
    <filter-name>springSecurityFilterChain</filter-name>
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
