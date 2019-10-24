## HTTP 协议的 Request 和 Response 对象

HTTP 的历史版本
* 1.0
* 1.1

HTTP 是基于 TCP 协议的，就会涉及到一次 HTTP 请求之后 TCP 连接是否断开的问题。

1.0 版本每一次请求都会建立新的 TCP 连接。 1.1 版本则复用之前的未被超时断开的连接。（即默认支持长连接/保活alive）

#### HTTP 协议规定的数据格式

##### 请求消息数据格式
1. 请求行
   ```
   格式： 请求方式 请求url 请求协议/版本
   示例： GET /login.html HTTP/1.1
   ```
2. 请求头 （header）
   ```
   格式： 请求头名称： 请求头值
         ... 
         (很多个，依据实际情况而定)
   ```
3. 请求空行
   ```
   就是一个空行，是协议强制要求添加的。
   ```
4. 请求体
   ```
   POST 方法的时候才会用到，平时都是空的，用于存放提交的内容。
   ```
注意，HTTP 请求的时候，提交（发送）的内容是有两个存放区域的：提交头、请求体。
``一般的协议相关的，都是放在请求头中，协议无关的内容才是放在请求体，例如：文件。``

###### 常用的请求头
```
# 很多请求头可以用于 服务端判断客户端浏览器的信息，以针对性处理。
1. User-Agent: 浏览器版本信息。 （用于解决浏览器兼容）
2. Referer: 告诉服务器，我（当前的请求）从哪里来。 即从哪个网站跳转过来的。
            作用： 防盗链； 统计工作，统计流量入口的导流量。
```

##### Request 对象
首先，要清晰 request 对象和 response 对象的原理
```
当有用户通过 url 访问 Servlet 的时候，tomcat 服务器会创建两个对象 request 和 response。
# request 对象，封装请求消息。
# response 对象，用于封装响应消息。
tomcat 将 request 和 response 对象传递给 service 方法，同时调用 service 方法。
服务器给浏览器做出响应的时候，所有信息来自于 response 对象。
```

request 获取请求消息
* 即获取四部分中的（请求行、请求头、请求空行、请求体）自己感兴趣的内容。

Servlet 协议中的 request 继承体系
```
# 继承体系
  ServletRequest  -- 接口
     |
  HttpServletRequest  -- 接口
     | 实现
  org.apache.catalina.connector.RequestFacade  -- 类（由tomcat实现）

# API
  查看 tomcat 源码，可知道具体实现和 API。
  1. 获取请求消息：
       1. 获取请求行中的数据
            * 请求方式： getMethd()
            * 虚拟目录： getContextPath()
            * Servlet 路径： getServletPath()
            * get 方式的请求参数： getQueryString()
            * uri: getRequestURI() getRequestURL()
            * 协议和版本： getProtocol()
            * 客户的 IP: getRemoteAddr()
       2. 获取请求头中的数据
            * getHeader()
            * getHeaderNames()
       3. 获取请求体中的数据
            * 步骤：
                1. 先获取流对象； getReader() getInputStream()
                2. 再从流对象中拿数据。
  2. 其他功能： （重要）
       1. 获取请求参数（通用方式）
            * getParameter() 根据名称获取参数值
            * getParameterValues()
            * getparameterNames()
            * getParameterMap()
            * 中文乱码问题：
              * get 方式： tomcat 8 已经将 get 方法乱码问题解决。
              * post 方式： 会乱码。 获取参数前设置流的编码（字符集）：request.setCharactorEncoding("utf-8");
       2. 请求转发： 服务器内部的资源跳转方式
            * 步骤：
                1. 通过 request 对象获取请求转发器对象： request.getRequestDispatcher(String path);
                2. 使用这个对象进行转发，forward(ServletRequest request, ServletResponse response);
       3. 共享数据(域对象)
            * 域对象： 一个有作用范围的对象，可以在范围内共享数据。
            * request 域： 代表一次请求的范围，一般用于请求转发的多个资源中共享数据。
            * 方法：
                1. setAttribute() 存储想共享的数据
                2. getAttribute() 通过键获取值
                3. removeAttribute（）
       4. 获取 ServletContext 对象
            * getServletContext()
```

##### 响应消息数据格式
1. 响应行
   ```
   格式： 协议/版本 响应状态码 状态码描述
   示例： HTTP/1.1 200 OK
   响应状态码： 服务器去告诉客户端浏览器本次请求对应的响应的状态。
         1. 状态码都是 3 位数字
         2. 分类：
            1. 1xx - 服务器接收客户端消息，但没有接收完成，等待一段时间，发送 1xx 状态码。（询问）
            2. 2xx - 成功。 最常见的，最期望的。
            3. 3xx - 重定向。 （参考 OAuth2.0 的重定向过程。）；
                     304 代表访问缓存 （指向/重定向至浏览器本地的缓存）。
            4. 4xx - 失败。 客户端错误。 客户端请求时指定的资源有误，代表： 404 - 路径对应的资源不存在。
                     405 代表请求方式没有被服务器实现/支持。 例如： 不支持 GET 方式访问，非要使用，则返回 405。
            5. 5xx - 失败。 服务器端错误。 服务器内部出现异常，很常见，服务器端出现了 bug 的表现。
   ```
2. 响应头 （header）
   ```
   格式： 请求头名称： 请求头值
         ... 
         (很多个，依据实际情况而定)
   ```
3. 响应空行
   ```
   就是一个空行，是协议强制要求添加的。
   ```
4. 响应体
   ```
   真实的传输的数据。
   ```

###### 常见的响应头
```
1. Content-Type: 服务器告诉客户端本次响应体数据的格式以及编码格式。 （重要，解决中文乱码问题。）
2. Content-disposition: 告诉客户端以什么格式打开响应体数据。
    1. 默认值： in-line 在当前页面内打开。
    2. attachment： 以附件形式打开响应体。 文件下载使用，同时需要设置 filename-xxx 头。
```

##### Response 对象
功能： 设置响应消息的。 （响应行、响应头、响应体）

HttpServletResponse API
```
1. 设置响应行
    * 就是设置状态码： setStatus(int sc)
2. 设置响应头
    * 也就一个方法： setHeader(String name, String value)
3. 设置响应体
    * 步骤： （使用流的方式，与请求体访问一样）
        1. 先获取流对象，getWriter() getOutputStream()
        2. 使用输出流，将数据写入。
```
Response 对象的使用比 Request 对象简单的多。

###### 小案例
```
1. 重定向的案例 （重要案例） - 在客户端进行自动资源跳转
   1. 告诉浏览器重定向 --> 状态码 302
   2. 告诉浏览器重定向的路径 --> 设置响应头 location：重定向的url 
   注意，重定向使用太频繁，因此专门添加了一个重定向方法： response.sendRedirect()
   # 重定向（redirect）和转发（dispatcher.forward）的区别：
   #  * 重定向的地址栏发生变化，转发是直接在服务端内部跳转，浏览器地址栏不变；
   #  * 重定向可以访问其他站点（服务器）的资源，转发只能访问当前服务器下的其他资源；
   #  * 重定向是两次请求，转发是一次请求。
   #  * 转发可以使用 request 对象共享数据，重定向没有此好处。

2. 服务器输出字符数据到浏览器 - getWriter()
   1. 获取字符输出流 PrintWriter pw = response.getWriter();
   2. 输出数据 pw.write("<h1>hello response</h1>");
   # 中文乱码的问题： (重要内容)
   #  1. 在获取字符流之前，设置流的编码； response.setCharacterEncoding() !!!
   #  2. 在获取字符流之前，设置 response 响应头，指定一样的编码： 
   #     content-type: text/html;charset=utf-8
   注意，指定编码使用太频繁，因此有专门的1个函数来做： response.setContentType()
   ### 特别强调！！！ 设置编码（无论是字节流的还是ContentType的）都是在获取字节流对象前！
   # 一个好的习惯是，每次都调用 response.setContentType() 设置编码，无论是否使用中文。

3. 服务器输出字节数据到浏览器 - getOutputStream()
   1. 获取字节输出流 ServletOutputStream sos = response.getOutputStream();
   2. 输出数据 sos.write("hello".getBytes());
   # 同字符输出流，设置编码： response.setContentType("text/html;charset=utf-8");

4. 验证码（内存中的一张图片） 输出到浏览器
   本质： 图片
   目的： 防止恶意表单注册
   # 参考文件下载，将内存中的图片写入 response 对象即可。

5. 文件下载
   * 首先，超链接指向一个文件资源；
   * 其次，使用响应头设置资源的打开方式； content-disposition:attachment;filename=xxx
   客户端：
   # <a href="/day15/download?filename=1.jpg">图片</a>
   # <a href="/day15/download?filename=1.avi">视频</a>
   Servlet 端：
   # 获取文件名称：
     String filename = request.getParameter("filename");
   # 加载文件进内存（使用字节输入流加载文件进内存）：
     ServletContext servletContext = this.getServletContext();
     String realPath = servletContext.getRealPath("/img/" + filename);
     FileInputStream fis = new FileInputStream(realPath);
   # 指定 response 的响应头： content-disposition: attachment;filename=xxx
     String mimeType = servletContext.getMimeType(filename);
     response.setHeader("content-type",mimeType);
     response.setHeader("content-disposition","attachment;filename="+filename);
   # 将数据写出到 response 对象：
     ServletOutputStream sos = response.getOutputStream();
     byte[] buff = new byte[1024 * 8];
     int len = 0;
     while((len = fis.read(buff)) != -1) {
        sos.write(buff,0,len);
     }
     fis.close();

6. 文件下载 - 中文文件名的问题
   解决思路：
      1. 获取客户端使用的浏览器版本信息；
      2. 根据不同的版本信息，响应不同的数据； （指的是设置 filename 的编码方式）
      # 例如：
      # if (agent.contains("MSIE")) {
      #      // IE 浏览器
      #      filename = URLEncoder.encode(filename, "utf-8");
      #      filename = filename.replace("+", " ");
      #  } else if (agent.contains("Firefox")) {
      #      // 火狐浏览器
      #      BASE64Encoder base64Encoder = new BASE64Encoder();
      #      filename = "?utf-8?B?" + base64Encoder.encode(filename.getBytes("utf-8")) + "?=";
      #  } else {
      #      // 其它浏览器
      #      filename = URLEncoder。encode(filename, "utf-8");
      #  }
      #  // 此时，使用转码后的 String 对象 filename 设置响应头即可。
      #  response.setHeader("content-disposition","attachment;filename="+filename);

7. 关于文件断点续传的原理，自行百度查询学习。
```

#### 细说 ServletContext 对象
概念：代表整个 web 应用，可以和程序的容器（服务器）来通信。

##### 功能：
* 获取 MIME 类型： ``在互联网通信过程中，定义的一种文件数据类型。 格式： 大类型/小类型。 text/html image/jpeg``
* 域对象： 共享数据
* 获取文件的真实（服务器）路径

##### 获取 ServletContext 对象
* 方法1： response.getServletContext()
* 方法2： this.getServletContext()  // this 指的是自定义的 Servlet 类

两种方法获取的是同一个对象。

##### 功能介绍
* 获取 MIME 类型
  ```
  String getMimeType(String filename);
  ```
* 域对象特性
  ```
  1. setAttribute(String name, Object value);
  2. getAttribute(String name);
  3. removeAttribute(String name);
  # 注意，该 ServletContext 域的范围（有效空间）： 所有用户所有请求的数据。（所有用户所有请求之间共享。）
  # 请谨慎使用！！ （服务器创建时它被创建，服务器关闭时它才被销毁。）
  # 请对比 Session 的概念。
  ```
* 获取文件的真实（服务器）路径
  ```
  String getRealPath(String path);
  ```

#### HTTP 协议的调试工具 curl
官方 https://curl.haxx.se/
