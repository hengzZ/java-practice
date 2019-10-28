## nginx

Nginx (engine x) 是一款轻量级的 Web 服务器/反向代理服务器及电子邮件（IMAP/POP3）代理服务器。

#### 什么是代理和反向代理
* 代理，即正向代理（forward proxy）： 客户端无法直接访问到目标服务器。 此时，客户端向代理服务器发送一个请求并指定目标，然后代理服务器向目标服务器转交请求，并将获得的内容返回给客户端。
* 反向代理（reverse proxy）： 指以代理服务器来接受internet上的连接请求，然后将请求转发给内部网络上的服务器。

##### 1. 正向代理的用途
* 突破访问限制： 访问国外网站，教育网等。
* 提高访问速度： 通常代理服务器都有缓存机制，当再次访问相同的信息时，直接由缓冲区中取出信息。
* 隐藏客户端真实IP： 隐藏自己的IP，免受攻击。 （但是！ 中介知道了，可能骚扰更多。）

##### 2. 反向代理的用途
* 隐藏服务器真实IP
* 负载均衡
* 提高访问速度 （因为缓存机制）
* 提供安全保障：
    1. 反向代理服务器可以作为应用层防火墙，为网站提供对基于 Web 的攻击行为（例如DoS/DDoS）的防护。
    2. 更容易排查恶意软件等。
    3. 可以为后端服务器统一提供加密和SSL加速（如SSL终端代理），提供HTTP访问认证等。

#### 为什么使用 Nginx?
对于一台服务器，无论如何去调优，它的并发量都是有上限的。 如果一台最好的服务器也无法满足并发量的需求，如何去满足？ Nginx 反向代理。
###### 用单机 tomcat 搭建的网站，在比较理想的情况下，能承受的并发访问量在 150 到 200 左右。
```
按照并发访问量占总用户数量占比为 5% 到 10% 考虑，单点 tomcat 可服务的用户数量为 1500 到 4000 之间。
```

### 在 Windows 上完成 Nginx + 多个 Tomcat 的环境搭建

#### 1. 安装 2 个 Tomcat
* 下载 Tomcat 安装包
* 安装： 注意，Tomcat 虽然解压压缩包即可使用，但是安装两个 Tomcat 的时候，需要去配置两个的环境变量，使它们不冲突。 （多台机器就没有这么麻烦了）
    1. 修改端口配置 （server.xml）
       ```
       1. shutdown 端口
       2. 启动端口 connector HTTP
       3. 启动端口 connector AJP
       # 搜索所有 port 字符串，阅读修改即可。 端口号都 +1 即可。
       ```
    2. 其他的环境配置 （除了 JRE_HOME，其它不要再添加至用户环境中。）
       ```
       JRE_HOME: 不需要修改。 （Java 运行环境）
       JAVA_HOME: tomcat 目录位置。 
       CATALINA_HOME: tomcat 目录位置。
       # 在 shutdown.bat 和 startup.bat 脚本中，设置以上两个环境变量。
       # 如： set "JAVA_HOME=<路径>/tomcat2"
       #     set "CATALINA_HOME=<路径>/tomcat2"
       ```
* 测试两个 tomcat 都正常启动。 localhost:8080 和 localhost:8081

#### 2. 安装 Nginx
* 下载： http://nginx.org/en/download.html
* 安装： 下载稳定版。 也是解压缩即用。
  ```
  注意，双击 nginx.exe，控制台闪现一下就结束了是正常现象。
       真实的启动情况，请在任务管理器中查看。
  ```
* 查看 nginx 运行是否成功，访问 localhost:80 地址。

#### 3. 地址映射 （配置 nginx）
参考文档： http://www.nginx.cn/doc/ ，查看负载均衡配置案例。

* 修改 nginx/conf/nginx.conf 文件
  ```
  示例：
  http {
       upstream myproject {
           server localhost:8080 weight=3;
           server localhost:8081;
       }

       server {
           listen 80;
           server_name localhost;
           location / {
               proxy_pass http://myproject;
           }
       }
  }
  # 1. 添加一个 upstream myproject；
  # 2. 将 server 的 location 配置注释掉，改为示例中的配置。
  ```
* nginx 的 upstream 目前支持 5 种方式的分配，上例使用的是权重赋值的方式。
* 重启 nginx 服务器： 命令行： ``nginx -s reload``
  ```
    # Nginx 命令行命令：
      -?,-h         : this help
      -v            : show version and exit
      -V            : show version and configure options then exit
      -t            : test configuration and exit
      -T            : test configuration, dump it and exit
      -q            : suppress non-error messages during configuration testing
      -s signal     : send signal to a master process: stop, quit, reopen, reload
      -p prefix     : set prefix path (default: NONE)
      -c filename   : set configuration file (default: conf/nginx.conf)
      -g directives : set global directives out of configuration file
  ```
* 注意，一定要使用 http://localhost:80 访问，如果是 https 的话，显示的还是 nginx 界面。

## Session 共享
tomcat 集群环境下，每次访问的后台服务器端其实一直在变动。 Session 是一个 tomcat 对象下的 HttpSession 对象，那么，两个不同的 tomcat 对象的 session 对象一定是不同的！

##### 解决方法
1. 设置 nginx 负载均衡配置为 ip_hash 模式。 （不推荐）
2. 使用 tomcat 的广播机制。 （强烈不推荐）
3. 基于 redis 服务器来共享 session 信息。 （缓存技术，强烈推荐！）

### 基于 redis 服务器的 session 共享

为什么使用 redis 服务器来做？
* NoSQL 的高性能特性；
* redis 的键值对结构与 session 本身的数据结构一致；
* redis 的定时删除机制与 session 的时效特点一致。

#### 案例
\<待完成>
