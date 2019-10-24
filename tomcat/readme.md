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

