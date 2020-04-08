## 微信授权登陆

#### 依赖环境
```bash
pip install requests
pip install xmltodict
```

#### 准备工作
微信登录基于 OAuth2.0 协议标准。 开发微信扫码登陆之前，需要登陆微信开放平台注册开发者帐号，并且，要拥有一个已审核通过的网站应用，经过微信审核后获得相应的 AppID 和 AppSecret。 （即：在微信开放平台注册备案）

#### 微信授权的意义是什么
微信 OAuth2.0 授权登录，是让第三方应用获取到用户的微信系统接口调用凭证（access_token），可以访问用户的微信信息。

OAuth2.0 的令牌颁发方式有四种：
* 授权码（authorization-code）
* 隐藏式（implicit）
* 密码式（password）
* 客户端凭证（client credentials）

**目前，微信支持 authorization_code 模式。**

#### 流程
###### reference https://developers.weixin.qq.com/doc/oplatform/Website_App/WeChat_Login/Wechat_Login.html

##### 1. 第三方发起微信授权登录请求，获取用来让用户扫描的二维码。

##### 方式一： wechat_redirect （授权后强制跳转的方式）
```
# 模板
https://open.weixin.qq.com/connect/qrconnect?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
url 参数说明：
    * appid —— 应用唯一标识，微信平台备案获得的 id。 （必填）
    * redirect_uri —— 授权完成后，将跳转到的 url。 （必须是备案的那个 url，它与 appid 是对应的，必填）
    * response_type —— 填写 code。 （就这一种填法，必填）
    * scope —— 应用授权作用域，可以填多个值，用 “,” 分隔。 网页应用目前仅仅填写 snsapi_login。 （必填）
    * state —— 非必须。 如果填的话，授权请求后原样带回给第三方。 该参数可用于防止 csrf 攻击（跨站请求伪造攻击）！！

# 示例
https://open.weixin.qq.com/connect/qrconnect?appid=wx2646c1044ed4504b&redirect_uri=http://www.info-connect.cn&response_type=code&scope=snsapi_login&state=1234
```
* 测试： <br>
  打开浏览器，复制粘贴 示例 url，并跳转。
* 特别说明： <br>
  若用户禁止授权，则重定向后不会带上 code 参数，仅会带上 state 参数。 重定向的步骤是依旧执行的。

授权之后的返回结果如下:
```
http://www.info-connect.cn/?code=001i8iKO0jO8p42seMLO0v45KO0i8iKA&state=1234
```

##### 方式二： 只授权不跳转。（交互更友好，并可嵌入到 app 中）
满足网站更定制化的需求，支持网站将微信登录二维码内嵌到自己页面中。
* 用途： <br>
  网站希望用户在网站内就能完成登录，无需跳转到微信域下登录后再返回，提升微信登录的流畅性与成功率。
* 特别说明： <br>
  需要使用微信提供的 js 工具来完成。

```
# 第一步： 在页面中先引入如下 JS 文件。（支持 https 和 http）
http://res.wx.qq.com/connect/zh_CN/htmledition/js/wxLogin.js
# 第二步： 在需要使用微信登录的地方实例以下 JS 对象。
var obj = new WxLogin({
 self_redirect:true,
 id:"login_container", 
 appid: "", 
 scope: "", 
 redirect_uri: "",
 state: "",
 style: "",
 href: ""
 });
参数说明：
    * self_redirect —— true：手机点击确认登录后可以在 iframe 内跳转到 redirect_uri，
                        false：手机点击确认登录后可以在 top window 跳转到 redirect_uri。 默认为 false。
    * id —— 第三方页面显示二维码的容器 id。
    * appid —— 同 wechat_redirect 方式的含义。
    * scope —— 同 wechat_redirect 方式的含义。
    * redirect_uri —— 同上。 （但是，需要进行 UrlEncode）
    * state —— 同 wechat_redirect 方式的含义。
    * style —— 提供 "black"、"white" 可选，默认为黑色文字。
    * href —— 自定义样式链接，第三方可根据实际需求覆盖默认样式。
```

##### 2. 通过 code 获取 access_token
```
# 模板
https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
url 参数说明：
    * appid —— 必填。
    * secret —— 应用密钥 AppSecret，备案后获得。 必填。
    * code —— 用户授权后的 code 码。 必填。
    * grant_type —— 填 authorization_code。 填写内容唯一，且必填。
# 示例：
https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx2646c1044ed4504b&secret=SECRET&code=001i8iKO0jO8p42seMLO0v45KO0i8iKA&grant_type=authorization_code
```

* 正确的返回:
```
{ 
"access_token":"ACCESS_TOKEN", 
"expires_in":7200, 
"refresh_token":"REFRESH_TOKEN",
"openid":"OPENID", 
"scope":"SCOPE",
"unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
}
参数说明：
    * access_token —— 接口调用凭证。
    * expires_in —— access_token 接口调用凭证超时时间，单位（秒）。
    * refresh_token —— 用户刷新 access_token。
    * openid —— 授权用户唯一标识。
    * scope —— 用户授权的作用域，使用逗号（,）分隔。
    * unionid —— 当且仅当该网站应用已获得该用户的 userinfo 授权时，才会出现该字段。
```

* 错误返回样例：
```
{"errcode":40029,"errmsg":"invalid code"}
```

###### 补充： 刷新 access_token 有效期
```
1. 若 access_token 已超时，那么进行 refresh_token 会获取一个新的 access_token，新的超时时间；
2. 若 access_token 未超时，那么进行 refresh_token 不会改变 access_token，但超时时间会刷新，相当于续期 access_token。
# refresh_token 拥有较长的有效期（30天），当 refresh_token 失效的后，需要用户重新授权。
```

##### 3. 刷新 access_token 有效期
```
# 模板
https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN
url 参数说明：
    * appid —— 必填。
    * grant_type —— 填 refresh_token，填写内容唯一，且必填。
    * refresh_token —— 填写通过 access_token 获取到的 refresh_token 参数。
```

* 正确的返回值：
```
{ 
"access_token":"ACCESS_TOKEN", 
"expires_in":7200, 
"refresh_token":"REFRESH_TOKEN", 
"openid":"OPENID", 
"scope":"SCOPE" 
}
```

* 错误返回样例：
```
{"errcode":40030,"errmsg":"invalid refresh_token"}
```

##### 4. 通过 access_token 调用微信开放的接口
对于接口作用域（scope），能调用的接口有以下：
* snsapi_base —— /sns/oauth2/access_token —— 通过 code 换取 access_token、refresh_token 和已授权 scope。
* snsapi_base —— /sns/oauth2/refresh_token —— 刷新或续期 access_token 使用。
* snsapi_base —— /sns/auth —— 检查 access_token 有效性。
* snsapi_userinfo —— /sns/userinfo —— 获取用户个人信息。

##### 接口调用方法可查阅 https://developers.weixin.qq.com/doc/oplatform/Website_App/WeChat_Login/Authorized_Interface_Calling_UnionID.html

<br>

## Part II —— 开发

<br>

#### 1. 不依赖第三方库

##### 1.1 http request 使用
###### reference:
* https://www.cnblogs.com/zhangxinqi/p/9201594.html blog
* https://realpython.com/python-requests/ tutorial
* https://pypi.org/project/requests/ official manual

#####  1.1.1 python requests 安装
  ```bash
  pip install requests
  ```
requests 是通过 urllib3 实现自动发送 HTTP/1.1 请求，它能轻松的实现 cookies，登陆验证，代理设置等操作。

##### 1.1.2 为什么选择 requests?
python 内置的 urllib 模块，也可用于访问网络资源，但是，用起来比较麻烦，而且缺少很多实用的高级功能。

##### 1.1.3 requests 实现的内容
* 保持活力和连接池
* 支持国际域名和网址
* 会话与 Cookie 持久性
* 浏览器式 SSL 验证
* 自动内容解码
* 基本/摘要式身份验证
* 自动解压缩
* Unicode响应body
* HTTP(s)代理支持
* 多部分文件上传
* 流媒体下载
* 连接超时
* 分块的请求
* .netrc 支持

##### 1.1.4 发送 requests 请求
所有请求的功能可通过这 7 种方法访问，它们都返回 response 对象的一个实例。
* request —— 构造并发送一个 request。
* head —— 发送 head 请求，url:网站 URL 地址。
* get —— 发送 GET 请求，params: 要在查询字符串中发送的字典或字节 request。
* post —— 发送 POST 请求，data: 字典数据也可以是元组列表，将被表单编码，以字节或文件对象在数据主体中发送；
  json: 在 json 数据中发送正文。
* put —— 发送 PUT 请求参数同 POST 一样。
* patch —— 发送 PATCH 请求。
* delete —— 发送 DELETE 请求。

##### 1.1.5 请求的响应信息
response.Response：该 Response 对象包含服务器对 HTTP 请求的响应信息。

发送请求后，会得到响应信息，我们可以使用 text 和 content 获取相应的内容，此外还有很多属性和方法来获取其他信息，如状态码，响应头，Cookies 等。

##### 1.1.6 requests 异常处理
* exception requests.RequestException(*args, **kwargs)： 发送一个模糊的异常。
* exception requests.ConnectionError(*args, **kwargs)： 发生连接错误时的异常。
* exception requests.HTTPError(*args, **kwargs)： 发生 HTTP 错误时的异常。
* exception requests.URLRequired(*args, **kwargs)： URL 错误时的异常。
* exception requests.TooManyRedirects(*args, **kwargs)： 太多的重定向。
* exception requests.ConnectTimeout(*args, **kwargs)： 连接服务器是请求超时。
* exception requests.ReadTimeout(*args, **kwargs)： 服务器没有在指定的时间内发送数据。
* exception requests.Timeout(*args, **kwargs)： 请求超时。

##### 1.1.7 cookies
略

##### 1.1.8 请求会话 (Session)
###### 在 requests 中，如果直接利用 get() 和 post() 方法的确可以做到模拟网页的请求，但这实际上是相当于不同的会话，即相当于使用了两个浏览器打开 ileal 不同的页面。

可以使用简单的方法，Session 来维持会话，利用它不需要设置 cookies，它能帮助我们自动处理。

* Session 的意义 <br>
  利用 session 可以做到模拟同一个会话，而不用担心 cookies 的问题，它常用于模拟登陆成功后再进行下一步操作，可以模拟在同一个浏览器中打开同一个站点的不同页面。

###### 补充： 什么是 HTTP 保活 以及 什么是连接池？
```
# http 连接的类型分为： 长连接、短连接、keepalive 连接。 （三种）
    ● 长连接 —— 建立连接后，该连接不再进行释放。 
           优点： 性能较高，不需要重复建立 tcp 连接或者关闭 tcp 连接。
           缺点： 一般需要一个连接池来维护长连接， 复杂度较高。
    ● 短连接 —— 每次请求均需要 tcp 三次握手建立连接，业务执行，tcp 四次挥手关闭连接。
           优点： 实现简单。
           缺点： 性能较差。 大部分都是 tcp 层面上的交互。
    ● keepalive 连接 —— 用于 http 协议。在 http 1.1 中，为了解决长连接提出的。
           优点： 用于维护长连接，提升性能。
           缺点： 需要在 header 中进行控制，需要交互控制，相对复杂。
# 疑问： 为什么 http 是无状态的，还会有长连接？？
    ▪ HTTP 的长连接和短连接本质上是 TCP 长连接和短连接。
    ▪ HTTP 协议是无状态的，是指，打开一个服务器上的网页和上一次打开这个服务器上的网页之间没有任何联系。
    ▪ HTTP 是一个无状态的面向连接的协议，无状态不代表 HTTP 不能保持 TCP 连接。。。
    ▪ Keep-Alive 不会永久保持连接，它有一个保持时间，可以在不同的服务器软件（如 Apache）中设定这个时间。
# HTTP 连接池
    HttpClient 中使用了连接池来管理持有的 TCP 连接。 其实 “池” 技术是一种通用的设计，其设计思想并不复杂：
    1. 当有连接第一次使用的时候建立连接；
    2. 结束时对应连接不关闭，归还到池中；
    3. 下次同个目的的连接可从池中获取一个可用连接；
    4. 定期清理过期连接。
```

##### 1.2 编写自己的 oauth 模块


<br>

#### 2. 依赖第三方工具
