## MyBatis

##### 持久层技术解决方案
* JDBC 技术
    * Connection
    * PreparedStatement
    * ResultSet
* Spring 的 JDBC Template
    * Spring 对 JDBC 的简单封装
* Apache DBUtils
    * 与 Spring 的 JDBC Template 很像，也是对 JDBC 的简单封装

注意，以上这些，都不是框架。 （JDBC 是规范，另外两个是基于规范实现的工具类。）

##### MyBatis 概述
mybatis 是一个 java 持久层框架，内部封装了 jdbc。 为开发者省去了加载驱动、创建连接、创建 statement 等复杂过程。

mybatis 通过 xml 或者注解的方式将要执行的各种 statement 与 java 成员函数关联，通过 sql 的动态参数机制进行最终的语句执行。

采用 ORM 思想解决了 JavaBean Object 与 数据库 映射的问题。

#### 1 MyBatis 环境搭建
中文官网 http://www.mybatis.cn/ ，参考网站的入门教程。

##### MyBatis 需要依赖的 jar 包
* mybatis 自身 jar 包。
* 数据库驱动 jar 包，如 mysql-connector-java.jar。
* 日志 jar 包，例 log4j.jar。
* mybatis-spring jar。

##### MyBatis 中文文档
http://www.mybatis.cn/679.html （推荐）

http://mybatis.org/mybatis-3/zh/index.html

##### MyBatis-Spring 中文文档
http://mybatis.org/spring/zh/

##### 快速入门（QuickStart）
http://www.mybatis.cn/679.html （推荐）

http://mybatis.org/mybatis-3/zh/getting-started.html

#### 2 MyBatis 学习路线
了解 -> 会用 -> 入门 -> 熟悉 -> 拓展。

* 了解阶段： 查阅 http://mybatis.org/mybatis-3/zh/index.html
* 会用阶段： 实际项目 + 官方指导文档 + 百度求助。
* 入门阶段： 结合 JDBC 知识，理解 MyBatis 工作原理和核心类库。
* 熟悉阶段： 指熟悉 MyBatis 源码，掌握重点类的代码。
* 拓展阶段： 存在此阶段是因为 MyBatis 自身的东西还是不够的，以事务为例，MyBatis 的事务内容，就是一层封装而已，真正去理解事务知识的时候，还需要去扩展自己的阅读面，阅读数据库的学习手册。

reference http://www.mybatis.cn/679.html
