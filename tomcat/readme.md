## Tomcat

学习内容：
* Web 服务器软件
* Servlet 入门

#### Web 相关概念回顾
* 软件架构
    * C/S
    * B/S
* 资源
    * 静态资源
    * 动态资源
* 网络通信三要素
    * IP
    * 端口
    * 传输协议

思考： 既然是 B/S 软件架构，B 是浏览器（Browser），那么 S 是什么，以什么形式呈现？

#### Web 服务器软件
* 服务器： 安装了服务器软件的计算机。 （注意，安装了服务器软件，并且该软件在运行中的机器才可称为服务器！）
* 服务器软件： 接收用户的请求，处理请求，做出响应。
* Web 服务器软件： 接收用户的请求，处理请求，做出响应。
    * 在 Web 服务器软件中，可以部署 web 项目，让用户通过浏览器来访问这些项目。
    * 又称为 “Web 容器”，是动态资源依赖的执行环境。

##### 常见的 Java 相关的 Web 服务器软件
* webLogic: Oracle 公司，大型的 JavaEE 服务器，支持所有的 JavaEE 规范，收费的。
* webSphere: IBM 公司，大型的 JavaEE 服务器，支持所有的 JavaEE 规范，收费的。
* JBOSS: JBOSS 公司，大型的 JavaEE 服务器，支持所有的 JavaEE 规范，收费的。
* Tomcat: Apache 基金组织，中小型的 JavaEE 服务器，仅仅支持少量的 JavaEE 规范 servlet/jsp。 开源免费。

###### 补充： 什么是 JavaEE?
```
Java 语言在企业级开发中使用的技术规范的总和，一共规定了 13 项大的规范。
```

#### Tomcat： Web 服务器软件
一款软件的使用一定是包含以下内容：
* 下载： Tomcat8.5.31 https://archive.apache.org/dist/tomcat/
* 安装: 解压压缩包即可。
* 卸载: 删除目录就行了 。
* 启动：
* 关闭：
* 配置：

##### 启动

Tomcat 软件安装后的目录结构
```
bin 目录                  可执行文件
conf 目录                 配置文件
lib 目录                  依赖 jar 包
logs 目录                 日志文件
temp 目录
webapps 目录              存放 Web 项目
work 目录                 存放运行时的数据
LICENSE
NOTICE
RELEASE-NOTES
RUNNING.txt
```

启动
```bash
# bin 目录下的 startup.bat 或 startup.sh 分别对应 Windows 和 Linux
sh startup.sh
```

查看启动情况
```
打开浏览器，输入 http://localhost:8080 访问 Tomcat 默认 Web 项目。
```

可能遇到的启动问题:
```
1. 黑窗口一闪而过
   原因： 没有正确配置 JAVA_HOME 环境变量。 （很多 bat 脚本用到了。）
   解决： 1. 配置 JAVA_HOME 环境变量为 Tomcat 的路径。
         2. 然后，将 %JAVA_HOME%bin; 添加至 Path 环境变量中。
         3. 配置 CATALINA_HOME 环境变量为 Tomcat 的路径。
         4. 配置 JRE_HOME 环境变量为 jdk 的安装路径。
2. 启动报错
   原因： 端口占用。
   解决： 暴力方案 - 找到占用程序，关闭它。 netstat -ano
         温柔方案 - 修改自身的端口号。 conf 目录内，修改 server.xml 文件内端口配置。
注意，一般会将 tomcat 的默认端口号修改为 80， 80 端口是 http 协议的默认端口。
好处是，在访问时，就不用输入端口号。 实际上各大网站都是如此做的。
```

##### 关闭
正常关闭
```
方式1： bin 目录下 bin/shutdown.bat 脚本。
方式2： 在启动窗口中 Ctrl+C 关闭。
```

强制关闭
```
点击启动窗口的右上角 “X”，强制关闭。 （不推荐）
```

##### 配置
部署项目的方式（3种）：
* 直接将项目放置于 webapps 目录下即可。
  ```
  * /hello: 项目的访问路径 --> 虚拟目录  例如： localhost/hello/hello.html
  * 简化部署： 将项目打成一个 war 包，再将 war 包放置于 webapps 目录下。
  ```
* 配置 conf/server.xml 文件
  ```
  在 <Host> 标签体中配置，<Context docBase="D:\hello" path="/hehe" />
  * docBase: 项目存放路径。
  * path: 虚拟目录。
  ```
* 在 conf/Catalina/localhost 目录中，创建一个任意名称的 xml 文件，内容如下
  ```
  <Context docBase="D:\hello" />
  * 虚拟目录： 即创建的 xml 文件的名称。
  推荐！！ 这种部署是热部署，Tomcat 不需要关闭和重启。
  ```

#### Tomcat 静态项目和动态项目的区别

##### 目录结构上的区别
Java 动态项目的目录结构：
```
 项目的根目录
  -- WEB-INF 目录：
      -- web.xml: web 项目的核心配置文件
      -- classes 目录： 放置字节码文件的目录
      -- lib 目录： 放置依赖的 jar 包
    
```

静态项目没有 Java 代码，是单纯的 HTML+CSS+JavaScript，没有强约束的目录结构。

#### 将 Tomcat 与开发工具 IDEA 关联
将 Tomcat 集成到 IDEA 中，并创建 JavaEE 的项目，部署项目。

集成步骤：
```
打开 IDEA，点击菜单栏的 run，选择 Edit Configurations。
点击 Defaults，找到 Tomcat Server 选项，单击然后选择 local。
在面板里点击 configure 按钮，选中 Tomcat 安装目录。 点击 OK 完成配置。
```

创建 JavaEE 项目
```
点击菜单栏 File，new 一个新项目，选择 Java Enterprise。
在右侧面板 Java EE Versions 选择 JavaEE 7。 同时，可以去指定 JDK 和 Tomcat。
在 Additional Libraries and Frameworks 中， 勾选 Web Application (3.1)。
同时勾上面板下方的 Create web.xml。 然后，点击 Next，指定模块的名称。 创建完成。
```

部署项目
```
点击菜单栏的 run，选择 Edit Configurations。
在 Tomcat Server 菜单中可以找到你刚创建的 Web 项目。
右侧的面板可以做一些配置，例如 Deployment 中的 Application context 可以设置虚拟目录。
启动项目： 关闭配置面板，点击 IDEA 右上部的 “绿色启动三角” 图标。
```

## Servlet
Servlet（Server Applet） 称为 “运行在服务器端的小程序”。 Java Servlet 通常情况下与使用 CGI（Common Gateway Interface，公共网关接口） 实现的程序可以达到异曲同工的效果。

相比于 CGI，Servlet 有几点优势：
* 性能明显更好。
* Servlet 在 Web 服务器的地址空间内执行。 就没有必要再创建一个单独的进程来处理每个客户端请求。
* Servlet 是独立于平台的，Java 程序的跨平台特性。

Servlet 就是一个接口，定义了 Java 类被浏览器访问到（被tomcat识别）的规则。
###### 所谓 Web 后台服务程序开发，就是我们自定义一个类，实现 Servlet 接口，复写它的方法。

#### Servlet 快速入门
1. 创建 JavaEE 的项目。
2. 定义一个类，实现 Servlet 接口。
3. 实现接口中的抽象方法。 （5个方法）
4. 配置 Servlet。

Servlet API 文档： http://tomcat.apache.org/tomcat-5.5-doc/servletapi/

##### 案例： Servlet Hello World
第一步： 创建一个 JavaEE 项目，点击菜单 run，选择 Edit Configures 配置 Tomcat Server。

第二步： 在 src 目录创建一个 package，然后创建一个 java class，代码如下：
```java
package demo_servlet;

import javax.servlet.*;
import java.io.IOException;

public class ServletDemo1 implements Servlet {
    @Override
    public void init(ServletConfig servletConfig) throws ServletException {

    }

    @Override
    public ServletConfig getServletConfig() {
        return null;
    }

    // 提供服务的方法
    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
        System.out.println("Hello Servlet.");
    }

    @Override
    public String getServletInfo() {
        return null;
    }

    @Override
    public void destroy() {

    }
}
```

第三步： 配置 Servlet。 编辑 WEB-INF 目录下的 web.xml 文件，例如：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">

    <!-- 配置 Servlet -->
    <servlet>
        <servlet-name>demo1</servlet-name>
        <servlet-class>demo_servlet.ServletDemo1</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>demo1</servlet-name>
        <url-pattern>/demo1</url-pattern>
    </servlet-mapping>

</web-app>
```
配置 Servlet 的目的是，将一个 uri 与一个 Servlet 程序对应。 （使用 uri 调用远端小程序。）
###### 至此，可以发现，应用程序是从 main 函数开始执行，而 Web 程序没有 main 函数的概念，一个 uri 即对应一个小程序，访问一次 uri 就运行一次对应的小程序。

#### Servlet 执行原理
* 首先，uri 中的 url 可以找到服务器主机。
* 然后，通过 url 中的路径可以找到项目。
* 最后，基于 uri 中的资源标识符，查询 web.xml 内注册的对应资源，运行。

```
tomcat 将全类名的字节码文件加载进内存。 ``Class.forName()``
创建对象。 ``cls.newInstance()``
调用方法 —— service。
```

#### Servlet 的生命周期
即，Servlet 的五个方法执行的顺序和时间节点。

* init 方法
  ```
  在 Servlet 被创建时（第一次被调用时），执行，只会执行一次。
  ```
* service 方法
  ```
  每一次 Servlet 被访问时，执行。 总执行次数由访问次数决定。
  ```
* destroy 方法
  ```
  在 Servlet 被销毁时（即服务器正常关闭时），执行，只会执行一次。
  ```
* getServletConfig 方法
  ```
  获取 ServletConfig 对象，Servlet 配置。 （了解）
  ```
* getServletInfo 方法
  ```
  获取 Servlet 的信息。 （一般不考虑去实现它）
  ```

###### 通过配置 \<servlet> 标签下的 \<load-on-startup> 的值为 0 或正数，指定 Servlet 对象在服务器启动时就创建。 （针对启动时加载资源较多的情况。）

##### 一个重要的注意事项 （忽略将导致重大BUG）
一个 Servlet 在内存中只存在一个对象，即单例。 但是访问确是多用户可同时访问的。
```
这种情况相当于多个线程同时访问同一个对象！！  必然可能存在线程安全问题（同时操作相同数据）。
解决的方案就是： 尽量不要在 Servlet 中定义成员变量！！ （尽量不要定义成员变量！）
              即使定义了成员变量，不要对其修改值！ （能定义已是最大的宽限！） 
```

#### Servlet 3.0 以后的版本
* 支持注解配置，可以不需要 web.xml 了。

```java
package demo;

import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import java.io.IOException;

@WebServlet(urlPatterns="/demo")
public class ServletDemo2 implements Servlet {
    @Override
    public void init(ServletConfig servletConfig) throws ServletException {

    }

    @Override
    public ServletConfig getServletConfig() {
        return null;
    }

    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {
        System.out.println("demo");
    }

    @Override
    public String getServletInfo() {
        return null;
    }

    @Override
    public void destroy() {

    }
}
```
``注意，以上方式是否和 Flask 的路由十分神似。``

JavaEE 6 支持的 Servlet 3.0 版本，因此 JavaEE 6 及以后版本都支持注解配置。

## Servlet 与 HTTP 访问参数的关联
观察 Servlet 的方法 ``public void service(ServletRequest servletRequest, ServletResponse servletResponse);`` 可以发现里面有两个对象
* ServletRequest
* ServletResponse

因此，HTTP 请求的详细细节和信息是由这两个类来保存和传递的。

#### 补充： Servlet 的体系结构
Servlet 有一个子类 GenericServlet 和一个孙子类 HttpServlet。
```
Servlet -- 接口
  |
GenericServlet -- 抽象类
  |
HttpServlet -- 抽象类
```

##### GenericServlet
当自定义的 Servlet 类继承自 GenericServlet 可以使我们只用去复写 service 一个函数即可。 （其他方法默认实现为空。）
``虽然方便，依旧不用:)``

##### HttpServlet （推荐）
现在的请求都是基于 HTTP 协议的，所以专门为 HTTP 请求写一个 Servlet 做为通用父类。

#### HttpServlet —— 基于 HTTP 协议的 Servlet（服务端小程序）
当自定义的 Servlet 类继承自 HTTPServlet 的时候，就不需要去重写 service 方法了。
相应的，需要重写 doGet 和 doPost，两个被 service 调用的方法。 ``该方式可以有效的屏蔽 HTTP 的 GET、POST 的处理逻辑。（不需要自己去考虑和处理了）``

案例
```java
package demo;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet
public class ServletDemo3 extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        System.out.println("doGet...");
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        System.out.println("doPost...");
    }
}
```
