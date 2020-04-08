## 使用 Python 和 Flask 设计 RESTful API
###### reference http://www.pythondoc.com/flask-restful/first.html

###### 近些年来 REST (REpresentational State Transfer) 已经变成了 web services 和 web APIs 的标配。

### 什么是 REST？
六条设计规范定义了一个 REST 系统的特点:
* **客户端-服务器**: 客户端和服务器之间隔离，服务器提供服务，客户端进行消费。
* **无状态**: 从客户端到服务器的每个请求都必须包含理解请求所必需的信息。换句话说， 服务器不会存储客户端上一次请求的信息用来给下一次使用。
* **可缓存**: 服务器必须明示客户端请求能否缓存。
* **分层系统**: 客户端和服务器之间的通信应该以一种标准的方式，就是中间层代替服务器做出响应的时候，客户端不需要做任何变动。
* **统一的接口**: 服务器和客户端的通信方法必须是统一的。
* **按需编码**: 服务器可以提供可执行代码或脚本，为客户端在它们的环境中执行。这个约束是唯一一个是可选的。 （非强制约束）

### 什么是一个 RESTful 的 web service？
RESTful web services 概念的核心就是 “资源”。 资源可以用 URI 来表示。
###### REST 架构的最初目的是适应万维网的 HTTP 协议。

HTTP 标准的方法有如下: 
```
==========  =====================  ==================================
HTTP 方法   行为                   示例
==========  =====================  ==================================
GET         获取资源的信息         http://example.com/api/orders
GET         获取某个特定资源的信息 http://example.com/api/orders/123
POST        创建新资源             http://example.com/api/orders
PUT         更新资源               http://example.com/api/orders/123
DELETE      删除资源               http://example.com/api/orders/123
==========  ====================== ==================================
```

**注意，REST 设计不需要特定的数据格式。** ``在请求中数据可以以 JSON 形式, 或者有时候作为 url 中查询参数项。``

### 设计一个简单的 web service
首先，需要确定你的应用程序将提供什么服务，理清服务列表（跟写代码无关）。

然后，就是决定用什么样的根 URL 来访问该服务。 例如： ``http://[hostname]/todo/api/v1.0/``。 （URL 模板）

有 2 点需要注意：
* 在 url 中包含应用的名称;
* 在 url 中包含 API 的版本号。

###### 应用名称其实相当于一个命名空间，以便区分同一系统上的其它服务。 版本号是帮助以后的更新，提供新旧共存，与命名空间的作用一样。

第三步，就是选择将由该服务暴露(展示)的资源。 （服务 -> urls）
例如：
```
==========  ===============================================  =============================
HTTP 方法   URL                                              动作
==========  ===============================================  ==============================
GET         http://[hostname]/todo/api/v1.0/tasks            检索任务列表
GET         http://[hostname]/todo/api/v1.0/tasks/[task_id]  检索某个任务
POST        http://[hostname]/todo/api/v1.0/tasks            创建新任务
PUT         http://[hostname]/todo/api/v1.0/tasks/[task_id]  更新任务
DELETE      http://[hostname]/todo/api/v1.0/tasks/[task_id]  删除任务
==========  ================================================ =============================
```

至此， web service 的设计基本完成。 剩下的事情就是实现它！

### 使用 Flask 实现 RESTful services 
在 Flask 中有许多扩展来帮助我们构建 RESTful services，但是，也可以不使用 Flask 的扩展。

##### 示例： 实现 /todo/api/v1.0/tasks API
```python
#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)
```
现在我们已经拥有一个 get_tasks 的函数，访问的 URI 为 /todo/api/v1.0/tasks，并且只允许 GET 的 HTTP 方法。

###### 注意，使用网页浏览器来测试我们的 web service 不是一个最好的主意。

##### 使用 curl 测试 API
网页浏览器上不能轻易地模拟所有的 HTTP 请求的方法，推荐使用 curl。 如果你还没有安装和使用过 curl，推荐你立即安装并体验一下。

curl 测试：
```bash
$ curl -i http://localhost:5000/todo/api/v1.0/tasks

# Response 信息
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 294
Server: Werkzeug/0.8.3 Python/2.7.3
Date: Mon, 20 May 2013 04:53:53 GMT

{
  "tasks": [
    {
      "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
      "done": false,
      "id": 1,
      "title": "Buy groceries"
    },
    {
      "description": "Need to find a good Python tutorial on the web",
      "done": false,
      "id": 2,
      "title": "Learn Python"
    }
  ]
}
```

##### 示例2： /todo/api/v1.0/tasks/[task_id]
```python
from flask import abort, make_response

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# Flask 默认的 404 响应返回的是 HTML 信息而不是 JSON，我们需要改善 404 错误处理程序
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
```

##### 示例3： /todo/api/v1.0/tasks POST API
```python
from flask import request

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201
```

测试：
```bash
$ curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks

# Response 信息
HTTP/1.0 201 Created
Content-Type: application/json
Content-Length: 104
Server: Werkzeug/0.8.3 Python/2.7.3
Date: Mon, 20 May 2013 05:56:21 GMT

{
  "task": {
    "description": "",
    "done": false,
    "id": 3,
    "title": "Read a book"
  }
}
```

##### 剩下的两个 API 实现如下
```python
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
```

## 优化 web service 接口
现在的 Web API 使用起来有问题么？ 对服务器端好像没什么问题，对客户端的开发呢？

对于客户端开发者，要根据需要的服务类型以及 API 模板，首先生成对应的 url 然后访问。 很不方便，你可以试试。
（以后 URLs 越来越多，查起来就反感，再涉及版本不同的问题，更累。）

请思考以下代码：
```python
from flask import url_for

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': map(make_public_task, tasks)})
```
这是一个小的辅助函数生成一个 “公共” 版本任务发送到客户端。

测试：
```bash
$ curl -i http://localhost:5000/todo/api/v1.0/tasks

# Response 信息
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 406
Server: Werkzeug/0.8.3 Python/2.7.3
Date: Mon, 20 May 2013 18:16:28 GMT

{
  "tasks": [
    {
      "title": "Buy groceries",
      "done": false,
      "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
      "uri": "http://localhost:5000/todo/api/v1.0/tasks/1"
    },
    {
      "title": "Learn Python",
      "done": false,
      "description": "Need to find a good Python tutorial on the web",
      "uri": "http://localhost:5000/todo/api/v1.0/tasks/2"
    }
  ]
}
```
##### 通过这种方法，我们可以提供 API 列表，使客户端一直可以看到 URIs，同时还可以隐藏一些想隐藏的信息。

## 加强 RESTful web service 的安全性
目前我们的 web service 对任何人都是公开的，这并不是一个好主意。
* 确保我们的 web service 安全服务的最简单的方法是要求客户端提供一个用户名和密码。

###### 在常规的 web 应用程序会提供一个登录的表单用来认证，并且服务器会创建一个会话为登录的用户以后的操作使用，会话的 id 以 cookie 形式存储在客户端浏览器中。
但是， REST 的规则之一就是 “无状态”！！  因此我们必须要求客户端在每一次请求中提供认证的信息。

此时，我们需要实现认证的话，就需要在 HTTP 的上下文中去完成。而非依赖 Session。 ``HTTP 协议提供了两种认证机制: Basic 和 Digest。``
有一个小的 Flask 扩展能够帮助我们：
```bash
$ pip install flask-httpauth
```

##### 案例： 使用用户名： miguel  和密码： python 进行认证
```python
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

# 改善错误处理函数，返回 JSON 数据格式而不是 HTML 的响应
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
```
###### get_password 函数是一个回调函数，Flask-HTTPAuth 使用它来获取给定用户的密码。
在一个更复杂的系统中，这个函数是需要检查一个用户数据库，在我们的例子中只有单一的用户因此没有必要。

##### 现在，需要将认证系统加入进去 ``通过 @auth.login_required 装饰器``
```python
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})
```

测试：
```bash
$ curl -i http://localhost:5000/todo/api/v1.0/tasks

HTTP/1.0 401 UNAUTHORIZED
Content-Type: application/json
Content-Length: 36
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/0.8.3 Python/2.7.3
Date: Mon, 20 May 2013 06:41:14 GMT

{
  "error": "Unauthorized access"
}
```
```bash
$ curl -u miguel:python -i http://localhost:5000/todo/api/v1.0/tasks

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 316
Server: Werkzeug/0.8.3 Python/2.7.3
Date: Mon, 20 May 2013 06:46:45 GMT

{
  "tasks": [
    {
      "title": "Buy groceries",
      "done": false,
      "description": "Milk, Cheese, Pizza, Fruit, Tylenol",
      "uri": "http://localhost:5000/todo/api/v1.0/tasks/1"
    },
    {
      "title": "Learn Python",
      "done": false,
      "description": "Need to find a good Python tutorial on the web",
      "uri": "http://localhost:5000/todo/api/v1.0/tasks/2"
    }
  ]
}
```

##### 认证扩展给予我们很大的自由选择哪些函数需要保护，哪些函数需要公开。

###### 补充： 两个小知识点
```
1. 为了确保登录信息的安全应该使用 HTTP 安全服务器，使用 HTTPS。
2. 让人不舒服的是，当 http 请求收到一个 401 的错误（认证不通过），就会会跳出一个丑陋的登录框，
   我们要把它隐藏掉！ 禁止跳转到浏览器显示身份验证对话框，一个简单的方式就是不返回 401 错误。 使用 403 代替。
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
```

## 其他可能的改进
* 一个真正的 web service 需要一个真实的数据库进行支撑。
* 另外一个可以提高的领域就是处理多用户。
* GET 检索任务列表请求可以在几个方面进行扩展
    * 可以携带一个可选的页的参数，以便客户端请求任务的一部分。
    * 另外，可以允许按照一定的标准筛选。

## 其他内容（进阶） —— 强烈推荐
* 使用 Flask-RESTful 设计 RESTful API http://www.pythondoc.com/flask-restful/second.html
* 使用 Flask 设计 RESTful 的认证 http://www.pythondoc.com/flask-restful/third.html


<br>

#### 附录：
##### Flask 大型项目开发实战教程 http://www.pythondoc.com/flask-mega-tutorial/index.html
可以查看很多 Flask 的真实实现方式。
