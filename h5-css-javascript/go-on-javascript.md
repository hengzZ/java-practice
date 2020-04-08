## JavaScript 深入

当我们在使用 JavaScript 的时候，通常会想到以下内容
* 更新/验证网页内的信息 （DOM 元素操作）
* 网页跳转/刷新/导出 （BOM 元素操作）
* Javascript 代码的设计模式 （模块化编码）

其他
* Ainimation？？
* Multimedia？？

<br>

#### 1. 更新/验证网页的信息
* 事件（Events） <br>
—— 事件是 DOM Level 3 的一部分，每个 HTML 元素都有一组事件，可用于触发 JavaScript 编码的响应。
    * *onclick* 按键的 js trigger
    ```html
      <input type = "button" onclick = "sayHello()" value = "Say Hello" />
      function sayHello() {
          alert("Hello World")
      }
    ```
    * *onsubmit* Form 的 js trigger
    ```html
      <form method = "POST" action = "t.cgi" onsubmit = "return validate()">
      ...
      <input type = "submit" value = "Submit" />
      </form>
      function validation() {
          // todo
          return true
      }
    ```
    * *onmouseover* / *onmouseout* images 或 text 的 js trigger
    ```html
      <div onmouseover = "over()" onmouseout = "out()">
         <h2> This is inside the division </h2>
      </div>
      function over() {
          document.write ("Mouse Over");
      }
      function out() {
          document.write ("Mouse Out");
      } 
    ```
    * 其他 H5 标准事件（钩子），查看相关文档
* 案例
    * 页面重定向（Page Redirection）
    ```html
      <input type = "button" value = "Redirect Me" onclick = "setTimeout('Redirect()', 1000)" />
      function Redirect() {
          window.location = "https://www.tutorialspoint.com";
      }
    ```
    * 对话框（Dialog Box） <br>
    *alert* - *confirm* - *prompt*
    ```html
      <input type = "button" value = "Click Me" onclick = "Warn();" />
      function Warn() {
          alert ("This is a warning message!");
      }
    ```
    ```html
      <input type = "button" value = "Click Me" onclick = "getConfirmation();" />
      function getConfirmation() {
          var retVal = confirm("Yes or Not");
          if( retVal == true ) {
              return true;
          } else {
              return false;
          }
      }
    ```
    ```html
      <input type = "button" value = "Click Me" onclick = "getValue();" />
      function getValue() {
          var retVal = prompt("Enter your name : ", "your name here");
          document.write("You have entered : " + retVal);
      }
    ```

#### 2. 网页跳转/刷新/导出
* *window.location* 网页跳转
```html
<input type = "button" value = "Redirect Me" onclick = "setTimeout('Redirect()', 1000)" />
function Redirect() {
    window.location = "https://www.tutorialspoint.com";
}
```
* *window.print()* 网页打印（导出）
```html
<input type = "button" value = "Print" onclick = "window.print()" />
```

#### 3. Javascript 代码的设计模式 （模块化编码）
—— 从蛮荒时代（*function/Object()*） 到 *require/import, export* 的进化
* 蛮荒时代（*function/Object()*）
    * *function*
    ```html
      function func(param1, param2) {
          // todo
      }
      function customObjType(param1, param2) {
          this.prop1 = param1;
          this.prop2 = param2;
          this.func1 = func;
      }
    ```
    * *Object()*
    ```html
      var customObjInst = new Object({
          prop1: value1,   /* 字典(dict) {key1:value1, key2:value2, ...} */
          func1: function(){ // todo; },
          func2: function(){ // todo; }
      }); 
    ```
    * *(function(){})()* 立即执行函数返回一个对象实例
    ```html
      var customObjInst = (
          function(){
              var count = 0;
              var nestedFunc1 = function(){alert(count);};
              var nestedFunc2 = function(){alert(count+1);};
              return {func1:nestedFunc1, func2:nestedFunc2};
          }
      )();
    ```
* 新的语法关键词，模块化支持 （ES6以前）
    * *module.exports/export, require* <br>
    —— CommonJS 规范 （node.js 社区的 JavaScript 扩展实现）
    * *define, require* <br>
    —— AMD(Asynchronous Module Definition) 规范 （require.js 和 curl.js 社区的 JavaScript 扩展实现）
    * *define, require* <br>
    —— CMD(Common Module Definition) 规范 （SeaJS 社区的 JavaScript 扩展实现）
* 新的语法关键词，模块化支持 （ES6-至今）
    * *export， import* <br>
    —— ES6 标准 （ES 标准委员会的 JavaScript 语法规范）
    ```html
      /* 导出名字 */
      export { name1, name2, …, nameN };
      export { variable1 as name1, variable2 as name2, …, nameN };
      export let name1, name2, …, nameN;
      export let name1=…, name2=…, …, nameN;
      /* 匿名 */
      export default expression;
      export default function (…) { … };
      export default function name1(…) { … };
      export { name1 as default, … };
      /* 从其他已有模块导出指定对象/函数/变量 */
      export * from …;
      export { name1, name2, …, nameN } from …;
      export { import1 as name1, import2 as name2, …, nameN } from …;
      /* 导入名字 */
      import defaultMember from "module-name";
      import * as name from "module-name";
      import { member } from "module-name";
      import { member as alias } from "module-name";
      import { member1 , member2 } from "module-name";
      import { member1 , member2 as alias2 , [...] } from "module-name";
      import defaultMember, { member [ , [...] ] } from "module-name";
      import defaultMember, * as name from "module-name";
      import "module-name";      
    ```
    * *class(){}* 关键词

###### refer: https://www.cnblogs.com/libin-1/p/7127481.html

#### 4. Ainimation 和 Multimedia
* Animation <br>
—— 依旧是通过 HTML 的内容和CSS式样来达到幻灯片动画效果 （DOM）
```html
<img id="myImage" src="/images/html.gif" />
<input type="button" value="Click Me" onclick="moveRight();" />
var imgObj = null;
function init() {
   imgObj = document.getElementById('myImage');
   imgObj.style.position= 'relative';  /* 通过 style 成员获取 CSS 属性 */
   imgObj.style.left = '0px'; 
}
function moveRight() {
    imgObj.style.left = parseInt(imgObj.style.left) + 10 + 'px';
}
window.onload = init;  /* 页面加载钩子 */
```
* Multimedia <br>
—— 通过 BOM 使用 Plugin 实现多媒体 （BOM）
    * *navigator.plugins* 已安装插件 <br>
    插件的四个属性
        * *name*
        * *filename*
        * *description*
        * *mimeTypes*
    ```html
      for (i = 0; i<navigator.plugins.length; i++) {
          document.write(navigator.plugins[i].name);
          document.write(navigator.plugins[i].filename);
          document.write(navigator.plugins[i].description);
      }
    ```
    * 使用插件播放多媒体文件 <br>
    —— \<embed\> 标签是 HTML 5 中的新标签
    ```html
      <embed id = "demo"
             name = "demo"
             src = "http://www.amrood.com/games/kumite.swf"
             width = "318" height = "300" play = "false" loop = "false"
             pluginspage = "http://www.macromedia.com/go/getflashplayer"
             swliveconnect = "true"
      >
      <input type="button" value="Start" onclick="play();" />
      <input type="button" value="Stop" onclick="stop();" />
      <input type="button" value="Rewind" onclick="rewind();" />
      function play() {
          if (!document.demo.IsPlaying()) {
              document.demo.Play();
          }
      }
      function stop() {
          if (document.demo.IsPlaying()) {
              document.demo.StopPlay();
          }
      }
      function rewind() {
          if (document.demo.IsPlaying()) {
              document.demo.StopPlay();
          }
          document.demo.Rewind();
      }
    ```
