# Spring 的权限管理和控制

## 第一部分 —— 权限管理
所谓权限管理，就是完成数据表的关联，为角色添加权限，为用户添加角色。

#### 1 用户关联角色
* 先查询出这个用户没有的角色信息
* 关联用户与角色信息，主要就是向 user_role 表中插入数据

#### 2 角色关联权限
* 先查询出这个角色没有的权限信息
* 关联角色与权限信息，主要就是向 role_permission 表中插入数据

## 第二部分 —— 权限控制
所谓权限控制，就是定义各个页面、url、service的方法可以被什么样的角色/权限访问。在服务器端，是通过 Spring Security 提供的注解来对方法进行权限控制的。
Spring Security 在方法的权限控制上支持三种类型的注解： JSR-250 注解、@Secured 注解、SPEL 表达式形式的注解。

#### 1 方法级别的权限控制 （服务器端访问控制）
* 先开启，默认情况下都是关闭。 (spring-security.xml)
  ```xml
  <!-- 开启 jsr-250 注解 -->
  <security:global-method-security jsr250-annotations="enabled" />
  <!-- 开启 @Secured 注解 -->
  <security:global-method-security secured-annotations="enabled" />
  <!-- 开启 SPEL 表达式注解 -->
  <security:global-method-security pre-post-annotations="enabled" />
  <!-- 注意，注解开启的注解是 @EnableGlobalMethodSecurity，Spring Security 默认是禁用注解的，
       要想开启注解，需要在继承 WebSecurityConfigureAdapter 的类上加 @EnableGlobalMethodSecurity 注解，
       并在该类中将 AuthenticationManager 定义为 Bean。 -->
  ```
* 使用。 注意 JSR250 在使用时，需要导入依赖 ``jsr250-api``。
  ```java
  // 1. JSR 250 注解示例
  @RequestMapping("/findAll.do")
  @RoleAllowed("ADMIN")   //JSR250 方式，可以省略前面的 ``ROLE_``
  public ModelAndView findAll() throws Exception {
      ModelAndView mv = new ModelAndView();
      // ...
      return mv;
  }
  // 2. @Secured 注解示例
  @RequestMapping("/findAll.do")
  @Secured("ROLE_ADMIN")  // Secured 注解不支持任何的角色名称省略
  public ModelAndView findAll(
            @RequestParam(name="page", required=true, defaultValue="1") int page,
            @RequestParam(name="pageSize", required=true, defaultValue="6") int pageSize
    ) throws Exception {
      ModelAndView mv = new ModelAndView();
      // ...
      return mv;
  }
  // 3. SPEL 表达式注解示例
  //用户添加方法
  @RequestMapping("/save.do")
  @PreAuthorize("authentication.principal.username == 'root'")
  public String save(UserInfo userInfo) throws Exception {
      userService.save(userInfo);
      return "redirect:findAll.do";
  }
  @RequestMapping("/findAll.do")
  @PreAuthorize("hasRole('ROLE_ADMIN')")
  public ModelAndView findAll(
            @RequestParam(name="page", required=true, defaultValue="1") int page,
            @RequestParam(name="pageSize", required=true, defaultValue="6") int pageSize
    ) throws Exception {
        ModelAndView mv = new ModelAndView();
        List<UserInfo> userList = userService.findAll(page, pageSize);
        PageInfo pageInfo = new PageInfo(userList);
        mv.addObject(pageInfo, pageInfo);
        mv.setViewName("user-page-list");
        return mv;
  }
  ```

#### 2 页面端标签控制权限 （页面端显示控制）
* 导入。 （maven 依赖包 + jsp 语法依赖 ）
  ```xml
  <!-- maven 依赖包 -->
  <dependency>
      <groupId>org.springframework.security</groupId>
      <artifactId>spring-security-taglibs</artifactId>
      <version>5.0.2.RELEASE</version>
  </dependency>
  ```
  ```html
  <!-- 在 jsp 页面导入语法依赖 -->
  <%@ taglib prefix="security" uri="http://www.springframework.org/security/tags" %>
  ```

* 常用标签：``authentication``、``authorize`` 和 ``accesscontrollist``。

##### 2.1 authentication 在页面上获取当前操作用户
使用 authentication 可以获取当前正在操作的用户信息。 如：登陆后，页面上的用户名显示。
```html
<security:authentication property="" htmlEscape="" scope="" var="" />
<!-- 使用示例，获取用户名 -->
<!-- 注意，principle 对象是认证系统对当前操作对象信息的封装。 -->
<security:authentication property="“principle.username" >
```
* property 只允许指定 Authentication 所拥有的属性，可以进行属性的级联获取，如 “principle.username”，不允许直接通过方法进行调用。
* htmlEscape 表示是否需要将 html 进行转义。默认为 true。
* scope 与 var 属性一起使用，指定存放获取的结果的属性名的作用范围，默认为 pageContext。 jsp 中拥有的作用范围都可以进行指定。
* var 用于指定一个属性名，这样当获取到了 authentication 的相关信息后，会将其以 var 指定的属性名进行存放，默认是存放在 pageContext 中。

##### 2.2 authorize 在页面上控制信息展示
authorize 是用来判断普通权限的，通过判断用户是否具有对应的权限而控制其所包含内容的显示。 如：对于普通用户，在菜单栏中隐藏角色管理、资源权限管理等。
```html
<security:authorize access="" method="" url="" var="">
</security:authorize>
<!-- 使用示例，非 admin 权限隐藏用户管理菜单 -->
<security:authorize access="hasRole('ADMIN')">
  <a href="${pageContext.request.contextPath}/user/findAll.do">
    <i class="fa fa-circle-o"></i> 用户管理
  </a>
</security:authorize>
<!-- 注意，使用 authorize 控制页面显示的时候会使用到表达式，因此，需要将 spring-security.xml 配置文件中的
    <security:http auto-config="true" use-expressions="false"> 标签属性 useruse-expressions 设置为 true，
    即改为：<security:http auto-config="true" use-expressions="true">
    另外，<security:intercept-url pattern="/**" access="ROLE_USER,ROLE_ADMIN" /> 也要改为表达式形式
    例：<security:intercept-url pattern="/**" access="hasAnyRole('ROLE_USER','ROLE_ADMIN')" />
    如果不想如此麻烦的修改配置，可以使用简便配置，如下在 spring-security.xml 中配置一个 bean
    <bean id="webexpressionHandler" class="org.springframework.security.web.access.expression.DefaultWebSecurityExpressionHandler"/>
    推荐，不修改原始配置，通过添加一个 bean 的方式来支持，此时，禁止表达式支持的话再注掉即可。 -->
```
* access 需要使用表达式来判断权限，当表达式的返回结果为 true 时表示拥有对应的权限。
* method 配合 url 属性一起使用，表示用户应当具有指定 url 指定 method 访问的权限。 method 的默认值为 GET，可选值为 http 请求的 7 种方法。
* url 表示如果用户拥有访问指定 url 的权限，即表示可以显示 authorize 标签包含的内容。
* var 用于指定将权限鉴定的结果存放在 pageContext 的哪个属性中。

##### 2.3 accesscontrollist
accesscontrollist 标签是用于鉴定 ACL 权限的，其一共定义了三个属性：hasPermission、domainObject 和 var。 其中前两个是必须指定的。
```html
<security:accesscontrollist hasPermission="" domainObject="" var="">
</security:accesscontrollist>
```
* hasPermission 用于指定以逗号分隔的权限列表。
* domainObject 用于指定对应的域对象。
* var 则是用以将鉴定的结果以指定的属性名存入 pageContext 中，以供同一页面的其他地方使用。

## 第三部分 —— 自定义访问受限时的提示页面

#### 1 配置 （指定 403 错误码的页面）
web.xml
```xml
<!-- 访问受限时的报错页面 403 错误 -->
<error-page>
    <error-code>403</error-code>
    <location>/403.jsp</location>
</error-page>
```
#### 2 页面内容
根据配置信息在对应位置创建一个页面即可，然后添加你想显示的内容。
