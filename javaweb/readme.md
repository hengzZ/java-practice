## JavaWeb
使用 Java 进行 Web（HTML） 开发。

#### 软件架构
* C/S : Client/Server
* B/S : Browser/Server

此处说的 JavaWeb 即 B/S 架构软件。

#### Web 的 “资源” 概念
URL、URI 都涉及 Resource 的概念，那么什么是资源？
* 静态资源 : 可以认为就是浏览器获取到的内容。 （HTML、CSS、JavaScript 都属于静态资源。）
* 动态资源 : 根据用户和访问者不同，向浏览器发送不同内容。 （jsp/servlet、php、asp..）

注意，浏览器获取到的一定是静态资源，动态资源的概念是为了表达： 服务端程序根据用户和请求不同返回不同的内容。
###### 可以简单理解为，静态资源就是服务端发给浏览器的内容（HTML、CSS、JS），动态资源就是服务端程序，它执行完成后一定是返回一些静态资源，并发给浏览器。

#### 从 “资源” 的概念来定学习计划
由于浏览器显示的一定是静态资源，并且它们由动态资源执行后产生，并发送给浏览器。 首先学习的一定是静态资源相关内容。

##### 静态资源学习
* HTML : 用于搭建基础网页，展示页面的内容。
* CSS : 用于美化页面，布局页面。
* JavaScript : 用于控制页面的元素，使页面有一些动态效果。 （注意，动态效果不是动态资源的概念。）

HTML-CSS-JS 扫盲，请参考 https://github.com/hengzZ/peter/tree/master/h5-css-javascript。

框架/工具
* Bootstrap : 定义了很多的 css 式样和 js 插件，使开发人员可以直接使用这些式样和插件，得到丰富的页面效果。
    * Bootstrap CSS 式样查询 https://v3.bootcss.com/css/
    * Bootstrap js 插件查询 https://v3.bootcss.com/javascript/
    * Bootstrap 组件(复合HTML元素) 查询 https://v3.bootcss.com/components/
* JQuery : 一个单纯的 js 框架。 用于简化 js 开发（编码代码书写）。

###### 响应式布局是使用框架的一个重要原因。 响应式布局的概念是，写一套代码就可以适配不同的分辨率和设备。
响应式布局扫盲 https://github.com/hengzZ/peter/blob/master/h5-css-javascript/responsive-layout.md。

##### 动态资源学习
* 
* 
