# Eureka

基于 Flask 的 Python Eureka Client 注册

#### Eureka 架构中的三个核心角色

- 服务注册中心 - 提供服务注册和发现功能
- 服务提供者 - 可以是任意技术实现，只要对外提供的是Rest风格服务即可。
- 服务消费者 - 消费应用从注册中心获取服务列表，从而得知每个服务方的信息，知道去哪里调用服务方。

服务提供方与Eureka之间通过“心跳”机制进行监控，当某个服务提供方出现问题，Eureka自然会把它从服务列表中剔除。

### Python Eureka Client

```bash
pip install py_eureka_client
```

```python
from flask import Flask
import py_eureka_client.eureka_client as eureka_client

app = Flask(__name__)


def setEureka():
    server_host = "localhost"
    server_port = 8088
    eureka_client.init(eureka_server="http://localhost:10086/eureka",
                       app_name="flask_server",
                       #当前组件的主机名为可选参数，如果不填写会自动计算一个，
                       #如果服务和 eureka 服务器部署在同一台机器，请必须填写，否则会计算出 127.0.0.1。
                       instance_host=server_host,
                       instance_port=server_port,
                       #调用其他服务时的高可用策略，可选，默认为随机
                       ha_strategy=eureka_client.HA_STRATEGY_RANDOM)

setEureka()


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=8088, host="0.0.0.0")
```
