## Cookie 和 Session

会话（Session）跟踪是 Web 程序中常用的技术，用来跟踪用户的整个会话。
###### 为什么会有 Session 的概念？
```
你可以查询了解下 RESTful API，其中一条重要的原则就是：
无状态。 每个请求都必须包含理解该请求所需的所有信息，不能利用服务器上任何存储的上下文。
（这表示你应该尽可能的避免使用 session。。 此处就是学习 session，可以先不考虑这么高级）

RESTful API 代表着分布式服务的架构风格。 当然也有其他的 API 定义规范，即其他的风格。
```
虽然无状态是我们在进行 API 定义时的准则，但是..不表示一次软件服务可以没有上下文，可以不考虑任何的前后状态。
``客户端和服务器分别还是要自己去标识和跟踪会话状态（上下文状态）的。``

总之，Cookie 和 Session 就是这样的一种机制。它可以弥补 HTTP 协议无状态的不足。


#### 1. 什么是 Cookie
Cookie 是服务器发给客户端的特殊信息。 ``请注意，是服务器发给客户端的特殊信息，客户端收到后将其保存到内存或磁盘。``

另外，客户端每次向服务器发送请求的时候都会带上这些特殊的信息。（浏览器会自动附带的，附在 Request Header 内。）

使用案例：
```
通常，我们可以从很多网站的登录界面中看到 “请记住我” 这样的选项，如果你勾选了它之后再登录，
下一次访问该网站的时候就不需要进行重复而繁琐的登录动作了，这个功能就是通过 Cookie 实现的。
```

##### 特别说明
如果你把 Cookie 看成为 http 协议的一个扩展的话，理解起来就容易的多了。 （基于 HTTP 实现的一个状态跟踪，并且每次交互都附带上的功能。）
```
有两个 http 头部是专门用于 Cookie 功能的，分别是 Set-Cookie 和 Cookie。
当服务器返回给客户端一个 http 响应信息时，如果 Response Header 内有 Set-Cookie，
意思就是指示客户端要建立一个 cookie，并且后续的 http 请求中自动发送这个 cookie 到服务器端。
直到这个 cookie 过期。
```

##### 1.1 服务器端访问 Cookie （以 Flask 框架为例，其他请查阅对应文档）
* 设置 Cookie，即告诉客户端保存某 Cookie 值，然后在下次收到 request 的时候读取。 ``模板： 首先使用 make_response() 接管 response 对象，然后调用该对象的 set_cookie() 设置 cookie。``
  ``查看 request 的 cookie 比较简单，request.cookies.get() 即可访问。``
  ```python
  from flask import Flask, render_template, request, make_response

  app = Flask(__name__)


  @app.route('/')
  def index():
      return render_template('index.html')

  @app.route('/setcookie', methods = ['POST', 'GET'])
  def setcookie():
      if request.method == 'POST':
          user = request.form['nm']
   
      resp = make_response(render_template('readcookie.html'))
      resp.set_cookie('userID', user)
   
      return resp

  @app.route('/getcookie')
  def getcookie():
      name = request.cookies.get('userID')
      return '<h1>Welcome: '+name+'</h1>'


  if __name__ == '__main__':
      app.run()
  ```
  ```html
  <!-- index.html -->
  <html>
   <body>
      <form action = "/setcookie" method = "POST">
         <p><h3>Enter userID</h3></p>
         <p><input type = 'text' name = 'nm'/></p>
         <p><input type = 'submit' value = 'Login'/></p>
      </form>
   </body>
  </html>
  ```
  ```html
  <!-- readcookie.html -->
  <html>
    <body>
      Cookie 'usrID' is set <br>
      <a href="/getcookie">Click here to read cookie</a>
    </body>
  </html>
  ```

* Cookie 的到期时间以及删除，用到时请查看框架文档查询。

###### 此处要注意： 在 python 脚本的同级目录下，创建一个 templates 目录，并将 index.html 文件置于其中。 只有这种目录结构才可以运行成功，这是 flask 的强制约定。

##### 1.2 浏览器端访问 Cookie
* 保存 Cookie （客户端自己创建新的 Cookie 并保存） ``模板： document.cookie = "key1 = value1;key2 = value2;expires = date";``
  ```html
  <html>
   <head>   
      <script type = "text/javascript">
         <!--
            function WriteCookie() {
               if( document.myform.customer.value == "" ) {
                  alert("Enter some value!");
                  return;
               }
               cookievalue = escape(document.myform.customer.value) + ";";
               document.cookie = "name=" + cookievalue;
               document.write ("Setting Cookies : " + "name=" + cookievalue );
            }
         //-->
      </script>      
   </head>
   
   <body>      
      <form name = "myform" action = "">
         Enter name: <input type = "text" name = "customer"/>
         <input type = "button" value = "Set Cookie" onclick = "WriteCookie();"/>
      </form>   
   </body>
  </html>
  ```

* 读 Cookie ``模板： document.cookie``
  ```html
  <html>
   <head>   
      <script type = "text/javascript">
         <!--
            function ReadCookie() {
               var allcookies = document.cookie;
               document.write ("All Cookies : " + allcookies );
               
               // Get all the cookies pairs in an array
               cookiearray = allcookies.split(';');
               
               // Now take key value pair out of this array
               for(var i=0; i<cookiearray.length; i++) {
                  name = cookiearray[i].split('=')[0];
                  value = cookiearray[i].split('=')[1];
                  document.write ("Key is : " + name + " and Value is : " + value);
               }
            }
         //-->
      </script>      
   </head>
   
   <body>     
      <form name = "myform" action = "">
         <p> click the following button and see the result:</p>
         <input type = "button" value = "Get Cookie" onclick = "ReadCookie()"/>
      </form>      
   </body>
  </html>
  ```

* 设置 Cookie 的到期时间以及删除 Cookie。
  ```
  用到时，去查 Javascript 教程。
  ```

##### 1.3 Cookie 在浏览器中保存多长时间的问题
* 默认情况下，当浏览器关闭后，Cookie 数据被销毁。
* Cookie 的持久化存储：
    * 正数: 只要指定存活时间即表示持久化。 到期后文件自动被删除。
    * 负值: 默认值。 不指定存活时间的话，系统默认给它个负值（默认值），表示不持久化。
    * 零: 删除 Cookie 信息。 也会删除持久化文件。

##### 1.4 在 Cookie 中保存中文
* 需要将中文数据转码 --- 一般采用 URL 编码（如：%E3） 用于显示的时候再转回来。

##### 1.5 Cookie 的共享问题
* 一个远端 Web 服务器中，部署了多个 Web 项目，这些项目间共享 Cookie 么？
  ```
  默认情况下，多个 Web 项目间 Cookie 不能共享。
  * setPath(String path): 可以设置 cookie 的获取/存放路径。
  默认情况下，每个 Web 项目是以它的虚拟路径作为这个 path 参数的。 因此不共享，因为路径不同。
  如果要共享，则可以将 path 设置为 “/”。
  ```
* 不同的 tomcat 服务器间 Cookie 共享问题
  ```
  * setDomain(String path): 如果设置一级域名相同，那么多个服务器之间 cookie 就可以共享了。
  # 什么是一级域名？
  # 1. 域名是看第一个 “/” 符号左边的 url 信息。
  # 2. 第一个 “/” 左边的信息，不是从左往右去理解，而是从右往左理解。
  #    如： www.github.com/hengzZ 首先是看 com 然后是 github（一级域名） 最后是 www
  # 示例： setDomain(".baidu.com") 则 tieba.baidu.com 和 news.baidu.com 共享 cookie。
  ```

##### 1.6 Cookie 的特点和作用
* cookie 数据是存储在用户的浏览器上，安全性、不被修改性低。
* 浏览器对单个 cookie 大小有限制，对同一个域名下的总 cookie 数量也有限制（20个）。
```
# 因此， cookie 的作用是：
  1. cookie 一般存放少量的不太敏感的数据。 注意，首先一定是少量！
  2. cookie 的主要用途（几乎是全部用途）：
     在不登陆的情况下，完成服务器对客户端的身份识别。 （例如：保存一些用户的配置选项）
  案例： 记住上一次访问时间。
       1. 首次访问：提示 你好，欢迎您访问。
       2. 如果不是第一次访问，提示 欢迎回来，您上次的访问时间为：xxxx。
```


#### 2. 什么是 Session
Session 是一个概念，对应的是现实的一套方案，起源于解决用户名和密码存储不能放在 cookie 中的问题（因为 cookie 可以在本地查看）。

示例：
```python
from flask import Flask, session
import os
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

@app.route('/')
def index():
    if "user" not in session:
        print('user is not in session.')
    session['username'] = 'zhiliao'
    session['user_id'] = '123'
    # permanent：持久化
    session.permanent = True
    print(type(session))
    return 'Hello World!'

@app.route('/get_session/')
def get_session():
    username = session.get('username')
    user_id = session.get('user_id')
    print(user_id)
    return username or '没有session'

@app.route('/delete_session/')
def delete_session():
    # session.pop('username')
    session.clear()
    return '删除成功'


if __name__ == '__main__':
    app.run(debug=True)
```

##### 2.1 Session 的特点
* 同一用户的不同页面共享 Session。 通俗讲，就是浏览器的不同窗口共享 Session 信息。
* Session 的默认存在时间是 30 min，但是，超时时间可调。

###### 为什么一打开一个新页面，服务端就知道是哪个 session，而不会和网络中的其他用户串数据？
```
# Session 的跟踪机制
Servlet API 规范中定义了一个 HttpSession 接口，它可以管理和操作会话状态。
每一个客户端在 WEB 服务器端对应一个各自的 HttpSession 对象。（因为每个客户端在访问时的 IP 都不同，不会串数据）
WEB 服务器为 每个 HttpSession 对象分配一个独一无二的会话标识号，在响应消息中将这个会话标识号传递给客户端。
客户端需要记住会话标识号，后续的每次访问请求中都把这个会话标识号传送给 WEB 服务器！！！
（当然，这是底层细节，在开发的时候已被实现在开发框架中，不需要纠结了。）
```

##### 2.2 Session 的超时管理
WEB 服务器是无法判断当前的客户端浏览器是否还会继续访问的。 因此，WEB 服务器仅仅依靠自己约定的时间，再一定时间后自动释放在内存中保存的 Session 数据。

如果某个客户端在一定的时间之内（距离上次请求记录）没有发出后续请求，WEB 服务器则认为客户端已经停止了活动，清除 Session 数据。

会话的超时间隔可以在 web.xml 文件中设置，其默认值由 Servlet 容器定义。

###### 此处引出一个话题： 服务器端的配置
```
我们在做 Web 开发的时候，是基于 Web 服务器和“公共网关接口”(Common Gateway Interface)的，
因此，比如 Session 超时，持久化等等功能已被实现在这些基础工具（软件）中，配置是必须的。
请回想 Flask 的配置信息，现在应该更理解为什么会有 app.config['配置项'] = 配置内容。
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
```

##### 2.3 服务器如何确保在一次会话范围内，多次获取的 Session 对象是同一个？
* 第一次获取 Session 对象时，会在内存中创建一个新的 Session 对象，同时设置 cookie 保存 SessionID。
* 此后的多次交互过程，cookie 信息决定着 Session 对象的获取是否为同一个。

##### 2.4 使用 Session 要注意的细节
1. 当客户端关闭后，服务器不关闭，两次获取的 session 是否为同一个？
   ```
   默认情况下，不是。 (因为 cookie 被销毁了，SessionID 丢失。)
   1. 创建一个 cookie，如： Cookie c = new Cookie("JSESSIONID", session.getID());
   2. c.setMaxAge(60*60); // 持久化存储 1 小时
   3. response.addCookie(c);
   ```
2. 客户端不关闭，服务器关闭后，两次获取的 session 是否为同一个？
   ```
   默认情况下，不是。 因此，这种情况要考虑的就是：如何确保 session 数据不丢失。
   # session 的钝化： 在服务器正常关闭之前，将 session 对象序列化到硬盘上。
   # session 的活化： 在服务器启动后，将 session 文件转化为内存中的 session 对象。
   该任务，tomcat 服务器已帮我们开发者自动完成！！ 其他服务器，请咨询厂商。
   ```
3. session 的失效时间？
   ```
   1. 服务器关闭；
   2. session 对象调用 invalidate()，自己主动销毁；
   3. session 默认失效时间 30 分钟。 可以去服务器配置文件配置。
   ```

##### 2.5 Session 的特点和作用
* session 存储在服务器端。
* session 可以存储任意类型，任意大小的数据。
```
# 因此， session 的作用是： 就是因为存放在 cookie 中不合适。
```


#### 3. 什么时候用 Cookie，什么时候又用 Session?
###### 首先注意，默认情况下，WEB 服务器的 Session 功能是依赖 Cookie 功能的。 （使用 Cookie 保存 SessionID，为开发者省事）

Cookie 和 Session 选哪个，决定了存储压力在客户端还是服务器。 另外就是基于安全性的考虑。

##### Cookie 的缺点
* Cookie 的数据可在客户端被修改，也可被人为清除，作为开发者你自己决定是否敢用。

##### Session 的优点
* Session 里面的东西对 Client 是不可见的，用户不可修改。

##### Session 的缺点
* 存那么多数据，服务器存储压力能不大？！

综上，还是优先考虑使用 Cookie。


#### 4. 使用 Flask 进行 Cookie 和 Session 实战

任务： 同时使用 Cookie 和 Session 保存 UserID，退出时清除 Cookie 和 Session 数据。

* Flask 后台
```python
from flask import Flask, render_template, request, make_response, session, redirect, url_for
from functools import wraps

app = Flask(__name__)
app.config["SECRET_KEY"] = "111111"  # A secret key is required to use CSRF.


# 登陆装饰器!!
def user_login_req(f):
    @wraps(f)
    def login_req(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return login_req


# 首页
@app.route('/')
def index():
    return render_template('index.html')


# 登陆页
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        session["user"] = user  # session
        resp = make_response(render_template('login.html'))
        resp.set_cookie('userID', user)
    elif request.method == 'GET':
        resp = make_response(render_template('login.html'))

    return resp


# 退出
@app.route('/logout/')
@user_login_req  # 没有指定 session 信息就跳转到 login
def logout():
    name = request.cookies.get('userID')
    print("userID", name)
    # 清除 Cookie 和 Session 数据
    # session.pop('userID') # 删除
    session.clear()  # 清空
    resp = make_response(render_template('logout.html'))
    resp.delete_cookie('userID')  # 删除
    return resp


if __name__ == '__main__':
    app.run()
```

* 主页
```html
<!-- index.html -->
<html>
   <body>
      <div align="center"><h3>Home Page</h6></div>
      <div align="center"><p id="welcome-slogan">Welcome: UserID</p></div>
      <a href="/login/">Login</a> <br>
      <a href="/logout/">Logout</a>
   </body>
</html>

<script type="text/javascript" src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
<script src="https://cdn.staticfile.org/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
<script type="text/javascript">

   var welcome = "Please login."

   //$.cookie("userID", "HengzZ")
   //$.removeCookie("userID")
   var user = $.cookie("userID")

   if (user == undefined) {
      welcome = "userID is undefined. Please Login."
   }
   else if (user == "") {
      welcome = "userID is empty. Please Login."
   }
   else if (user == null) {
      welcome = "userID is null. Please Login."
   }
   else {
      welcome = "Welcome: " + user
   }


   $(document).ready(function(){
      $("#welcome-slogan").text(welcome)
   })

</script>
```

* 登陆页
```html
<!-- login.html -->
<html>
   <body>
      <form action = "/login/" method = "POST">
         <p><h3>Enter userID</h3></p>
         <p><input type = 'text' name = 'nm'/></p>
         <p><input type = 'submit' value = 'Login'/></p>
      </form>
      <a href="/">Home</a> <br>
      <a href="/logout/">Logout</a>
   </body>
</html>
```

* 退出页
```html
<!-- logout.html -->
<html>
   <body>
      You have logged out. Please go to <a href="/">Home Page</a> for checking. <br>
      If you want to check wether the session is cleared, please refresh. It'll redirect to login page if cleared.
   </body>
</html>
```

##### 学习内容
1. 请注意此处用的登陆装饰器。 虽然使用的业务逻辑不太好，装饰器的代码是很规范的。
2. 此处用到 JQuery，它是一个 JS 库，可以提升开发者效率。 （使 DOM 的内容选择和操作更舒服。）
3. 另外一个需要了解的工具是 BootStrap 框架，包含了很多式样和 html 组件，可以提升 UI 开发速度。 （不要自己在那反复调式样或者自定义一个复杂的 html 元素了）


#### 5. 高级话题： 浏览器禁用 Cookie 后的 Session 处理
例如网站要实现购物车功能，可以基于 Cookie，也可以基于 Session，若服务器性能较差，可以考虑基于 Cookie 实现购物车。

###### Cookie 不能用了，Session 如何继续使用？
```
方案： URL 重写。 简单讲，即每个访问链接(url)后都跟上用户的 sessionid。
此时， 有 SessionID，Session 功能就可以继续用。
```

##### 那么，Cookie 禁用了，Session 还能用么？
在默认的 JSP、PHP 配置中，SessionID 是需要存储在 Cookie 中的，默认 Cookie 名为：
* JSESSIONID
* PHPSESSIONID

因此，当客户端禁用了 Cookie，客户端还不去对 SessionID 主动地保存记忆的话，将丢失。 就无法使用 Session 功能，没有 ID，服务端有 HttpSession 对象也没用。

##### 此时，就引出了浏览器禁用 Cookie 后的 Session 处理 —— URL 重写。

#### 最后的一些说明
##### 1. 为什么 Cookie 和 Session 我们用起来的时候没有一直去考虑底层细节？
它们都是为 CGI 编程设计的，因此在 CGI 的功能中，以实现通信细节。

##### 2. Web 开发有两大重量级工具（app）在被使用，分别是 HTTP Server 和 CGI。
这两样东西普遍都被包含在 Web 开发的框架中，如：Flask 中，使用的时候以配置为主。 面试的时候问底层细节，实际上开发者不会去造这两个工具。
