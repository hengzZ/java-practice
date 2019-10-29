## Java DataBase Connectivity (JDBC)

#### 数据库设计的范式
目前，关系型数据库有六种范式：
* 第一范式 （1NF） —— 第一范式就是无重复的域。 ``“原子列”，所有创建出来的数据库都满足该范式。``
* 第二范式 （2NF） —— 属性完全依赖于主键。 ``“表拆分”，将尽可能多的可移除的域，拆出去成立单独的表。``
* 第三范式 （3NF） —— 任何非主属性不得传递依赖于主属性。 ``“消除传递依赖”，消除拆出去后新成立的表的传递依赖。``
* 巴斯-科德范式 （BCNF）
* 第四范式 （4NF）
* 第五范式 （5NF，又称完美范式。）

设计范式的意义在于提出了一些数据库设计的标准规范/要求，使最大可能的减少数据冗余。 ``前三种范式应用最普遍``

## JDBC

##### JDBC 的本质
定义了操作所有关系型数据库的规则（Java代码规范）。

注意：
* JBDC 只是定义了接口，需要程序员自己去实现类！
* 这些实现类已由各厂商去完成，称为 “数据库驱动”。
* 因此，使用 JDBC 的时候需要加载驱动。

##### 快速入门
1. 导入 jar 包。 如：MySQL --> ``mysql-connector-java``；
2. 注册驱动；
3. 获取数据库连接对象 ``Connection``； （实际开发一般从连接池对象获取。）
4. 定义 sql；
5. 获取执行 sql 语句的对象 ``Statement``；
6. 执行 sql，得到返回结果；
7. 处理结果。
```java
package com.petersdemo.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class JdbcDemo1 {
    public static void main(String[] args) throws Exception {
        //1.导入 jar 包 mysql-connector-java
        //2.注册驱动 （关键步骤！）
        Class.forName("com.mysql.jdbc.Driver");
        //3.获取数据库连接对象
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/db3","root","password");
        //4.定义 sql 语句
        String sql = "update account set balance = 500 where id = 1";
        //5.获取执行 sql 的对象
        Statement stmt = conn.createStatement();
        //6.执行 sql
        int count = stmt.executeUpdate(sql);
        //7.处理结果
        System.out.println(count);
        //8.释放资源
        stmt.close();
        conn.close();
    }
}
```

### 各个接口和类详解

##### 1. JDBC 的 5 大对象
* DriverManager： 驱动管理对象
* Connection： 数据库连接对象
* Statement： 执行 sql 的对象
* ResultSet： 结果集对象
* PreparedStatement： 执行 sql 的对象 （Statement的子类，更强大。 常用的对象）

##### 2. JDBC 事务
JDBC 使用 Connection 对象来管理事务
* 开启事务： setAutoCommit(boolean autoCommit) 调用该方法设置参数为 false，即开启事务。
* 提交事务： commit()
* 回滚事务： rollback()

##### 3. JDBC 连接池
当系统初始化好后，容器（集合）被创建，其中会申请一些连接对象。 当用户访问数据库时，从容器中获取连接对象，访问完之后，将连接对象归还给容器。

一般我们不去实现它（连接池），有数据库厂商来实现，常用的有：
* C3P0: 数据库连接池技术 （老技术）
* Druid: 数据库连接池技术 （新技术，由阿里巴巴提供的）
* 等等。

对于连接池技术，更多的是使用，了解其中一种的实现机制即可。

##### 4. JDBC Template
使用 Spring JDBC 模块的 JDBC Template，简化 JDBC 的编程。 ``Spring 框架对 JDBC 的简单封装。``

使用步骤：
1. 导入 jar 包。
2. 创建 JdbcTemplate 对象。 依赖于数据源（线程池） DataSource。
   ```
   * JdbcTemplate template = new JdbcTemplate();
   ```
3. 调用 JdbcTemplate 的方法来完成 CRUD 操作。
   ```
   1. update()： 执行 DML 语句。 增、删、改语句。
   2. queryForMap()： 查询结果将封装为 Map 集合。
       * 注意，这个方法查询的结果集长度只能是 1。
   3. queryForList()： 查询结果将封装为 List 集合。
       * 注意，将每一条记录封装为一个 Map 集合，再将 Map 集合装载到 List 集合。
   4. query(): 查询结果将封装为 JavaBean 对象。
       * 注意，该方法需要传入一个 RowMapper。
           * 一般使用 BeanPropertyRowMapper 实现类。 可以完成数据到 JavaBean 的自动封装。
           * new BeanPropertyRowMapper<Emp>(Emp.class); 
           * // Emp - 类型； Emp.class - 类型的字节码对象
   5. queryForObject()： 查询结果将封装为对象。 （一般用来执行聚合函数的查询）
   ```

JDBC Template 查询的结果直接以对象返回，省去了大量的赋值过程。

入门程序
```
public class JdbcTemplateDemo1 {
    public static void main(String[] args) {
        //1.导入 jar 包
        //2.创建 JDBCTemplate 对象 （获取线程池对象，传入 JdbcTemplate 构造方法）
        JdbcTemplate template = new JdbcTemplate(JDBCUtils.getDataSource());
        //3.调用方法
        String sql = "update account set balance = 5000 where id = ?";
        int count = template.update(sql, 3);
        System.out.println(count);
    }
}
```
