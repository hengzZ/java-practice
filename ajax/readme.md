## Ajax

Asynchronous JavaScript And XML 异步的 JavaScript 和 XML。

1. 异步和同步： 客户端和服务器端互相通信的基础上
   ```
   * 客户端必须等待服务器端的响应。 在等待的期间客户端不能做其他操作。
   * 客户端不需要等待服务器端的响应。 在服务器端处理请求的过程中，客户端可以进行其他的操作。

   Ajax 是一种在无需重新加载整个网页的情况下，能够更新部分网页的技术。
   提升用户的体验。
   ```
2. 实现方式
   ```
   1. JavaScript 原生的实现方式 （了解即可）
       请查阅 JS 文档。 用起来有点麻烦。
   2. JQuery 实现方式：
       1. $.ajax()
           * 语法： $.ajax({键值对});
           //使用$.ajax()发送异步请求
             $.ajax({
                url: "ajaxServlet",  //请求路径
                type: "POST",        //请求方式
                //data: "username=jack&age=23", //请求参数
                data: {"username":"jack", "age":23},
                success: function(data) {
                    alert(data);
                },  //响应成功后的回调函数
                error: function() {
                    alert("出错啦..");
                },  //如果请求响应出现错误，会执行的回掉函数
                
                dataType: "text"  //设置接受到的响应数据的格式
             });
       2. $.get()  发送 GET 请求
           * 语法： $.get(url, [data], [callback], [type])
           * 参数：
               * url: 请求路径
               * data: 请求参数
               * callback： 回调函数
               * type: 响应结果的类型
       3. $.post() 发送 POST 请求
   ```
注意，从服务器端加载内容/信息的方式，可以认为就两种： ``页面跳转、Ajax``。 页面跳转就是我们最常使用和见到的样子，而所有的登陆/注册验证提示都是 ajax 方式。

## JSON

JavaScript Object Notation，JavaScript 对象表示法。
1. 原始作用
   ```javascript
   var p = {"name":"张三","age":23,"gender":"男"};  //声明（表示）JS对象
   ```
2. 现今用途
   ```
   * json 现在多用于存储和交换文本信息的语法；
   * 进行数据的传输；
   * JSON 比 XML 更小、更快，更易解析。
   ```

### 语法

#### 基础规则 （书写规则）
* 数据在名称/值对中： json 数据是由键值对构成的
    * 键用引号（单双都行）引起来，也可以不使用引号
    * 值的取值类型：
      ```
      1. 数字 （整数或浮点数）
      2. 字符串 （在双引号中）
      3. 逻辑值 （true 或 false）
      4. 数组 （在方括号中） {"persons":[{},{}]}
      5. 对象 （在花括号中） {"address":{"province":"河南"....}}
      6. null
      ```
* 数据由逗号分隔： 多个键值对由逗号分隔
* 花括号保存对象： 使用 {} 定义 json 格式
* 方括号保存数组： []

#### 获取数据 （指浏览器端）
1. json对象.键名
2. json对象\["键名"]
3. 数组对象\[索引]
4. 遍历
   ```
   //1. 定义基本格式
   var person = {"name":"张三","age":23,"gender":true};
   var ps = [{"name":"张三","age":23,"gender":true},
            {"name":"李四","age":24,"gender":false},
            {"name":"王五","age":25,"gender":true}];
   
   // 获取 person 对象中所有的键和值。 for in 循环
   for(var key in person) {
       // 注意，person.key 方式不行，因为相当于： person."name"
       alert(key+":"+person[key]);
   };
   
   // 获取 ps 中的所有值
   for (var i = 0; i < ps.length; i++) {
       var p = ps[i];
       for (var key in p) {
           alert(key+":"+p[key]);
       }
   }
   ```

#### JSON 数据和 Java 对象的相互转换 （指服务器端）

```
* JSON 解释器：
    * 常见的解释器： Jsonlib, Gson, fastjson, jackson。
```

1. JSON 转为 Java 对象
   ```
   1. 导入 jackson 的相关 jar 包；
   2. 创建 jackson 核心对象 ObjectMapper；
   3. 调用 ObjectMapper 的相关方法进行转换。
       * readValue(json字符串数据,Class);
   ```
2. Java 对象转换 JSON
    1. 使用步骤：
       ```
       1. 导入 jackson 的相关 jar 包；
       2. 创建 jackson 核心对象 ObjectMapper；
       3. 调用 ObjectMapper 的相关方法进行转换。
       ```
    2. 转换方法：
       ```
       * writeValue(参数1, obj):
           参数1：
               File: 将 obj 对象转换为 json 字符串，并保存到指定的文件中。
               Writer: 将 obj 对象转换为 json 字符串，并将 json 数据填充到字符输出流中。
               OutputStream: 将 obj 对象转换为 json 字符串，并将 json 数据填充到字节输出流中。
       * writeValueAsString(obj): 将对象转换为 json 字符串，作为返回值。
       ```
    3. 注解：
       ```
       1. @JsonIgnore: 排除属性。
       2. @JsonFormat: 属性值格式化。
           * @JsonFormat(pattern="yyyy-MM-dd")
       ```
    4. 复杂 Java 对象转换
       ```
       1. List: --> JSON 数组
       2. Map:  --> 与 JSON 对象格式一致
       ```

## Ajax + JSON 使用案例
在注册页面校验用户名是否存在

1. 服务器响应的数据，在客户端使用时，要想当作 json 数据格式使用
   ```
   1. $.get(type): 将最后一个参数 type 指定为 "json"。
   2. 或者，在服务器端设置 MIME 类型
      response.setContentType("application/json;charset=utf-8");
   ```

## 所谓单页面应用
可以认为，单页面应用就是： 第一次与服务器端交互（请求）时，采用``页面跳转``，此后的所有请求都是``Ajax``。

# 解决 chrome 阻止跨域方法

跨域 ajax 被拦截示例：
```
Access to XMLHttpRequest at 'http://localhost:5000/mipsList/findAll' from origin 'null' has
been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

很多情况下，开发人员的开发项目与服务器不在同一个环境下，此时 ajax 请求到数据，但并不会走 success 函数，而是在 error 里。
``http 同源策略不允许跨域请求数据。``

## 通过后端打开跨域权限
#### flask 跨域访问授权
```bash
pip install -U flask-cors
```
```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__,
            static_folder = "../dist/static",
            template_folder = "../dist")
cors = CORS(app, resources={"/api/*": {"origins": "*"}})  # 跨域授权

@app.route('/api/number')
def api_number():
    response = {
        'number': 100
    }
    return jsonify(response)

if __name__ == "__main__":
    app.debug = True
    app.run()
```
