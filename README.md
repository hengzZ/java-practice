# java-practice

#### 学习目标
* JavaWeb 三大组件： Servlet、Filter 和 Listener。
* JavaWeb 三层架构： MyBatis、Spring 和 SpringMVC。
* HTTP 通信过程
    * http request 和 response 对象。
    * cookie 和 session。
* 集群（分布式）
    * Redis 缓存技术、 Nginx部署Tomcat集群。
    * 消息队列、连接池。
* 响应式布局 Bootstrap。
* 单页面应用 Ajax/Vue.js。

#### 内容
1. 开发工具与环境配置 [1-development-tools-and-configuration.md](1-development-tools-and-configuration.md)
2. Java 语法
    * 基础语法（基本数据类型、语句、函数定义、代码组织）
    * 面向对象和封装（对象）
    * 继承与多态（依赖倒转原则、合成复用原则）
    * 常用 API、常用内置数据结构 （标准库）
    * 异常与多线程编程
    * 文件/IO/网络编程
3. 项目 —— 工具/框架学习

#### 技术选型
1. Web 层
    * 前台用户页面
        - Servlet：前端控制器
        - html：视图
        - Filter：过滤器
        - BeanUtils：表单数据封装
        - Jackson：json 序列化工具
    * 后台管理页面
        - Servlet：前端控制器
        - JSP：视图
        - Filter：过滤器
2. Service 层
    * javamail：java 邮件发送工具
    * Redis：nosql 内存数据库
    * Jedis：java 的 redis 客户端
    * 消息队列
3. Dao 层
    * MySQL：数据库
    * Druid/c3p0：数据库连接池
    * jdbcTemplate：jdbc 的工具

注意，Web 层的选型需要区分用户和管理页面。``前台用户页面的访问并发，一定远远大于后台管理页面的访问。因此，前台页面考虑的是并发量，管理页面考虑的是文件上传的敏捷开发。``
