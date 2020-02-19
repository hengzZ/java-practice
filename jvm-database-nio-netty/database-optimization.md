# 数据库优化

## Part I —— 数据库原理

### 1 数据模型
数据模型（Data Model）是数据库结构的基础，用来描述数据的概念和定义。数据模型主要有三个要素：数据结构、数据操作、数据的约束条件。
* 数据结构 —— 表结构
* 数据操作 —— 增删改查
* 数据的约束条件 —— 字段约束

### 2 数据库
* 关系型数据库：如 MySQL、Oracle、SQLServer
* 非关系型数据库：如 Redis、HBase

### 3 数据库管理系统
Database Management System，DBMS 是为用户提供交互途径的系统。

## Part II —— 关系代数

### 1 关系代数的基本运算
* 重命名
* 并
* 差
* 笛卡尔积（又称：叉积、交叉连接）
* 选择
* 投影

### 2 关系代数的组合运算
* 交
* 连接
* 自然连接
* 除

### 3 扩充的关系代数操作
* 外连接（左外和右外）
* 外部并
* 半连接

```
1. 左连接（left join）：以左表为基础，根据 ON 后的条件将两表连接起来。（左表所有的查询信息列出，而右表只列出 ON 后条件与左表满足的部分。）
2. 右连接（right join）：以右表为基础，根据 ON 后的条件将两表连接起来。（右表所有的查询信息列出，而左表只列出 ON 后条件与右表满足的部分。）
3. 自然连接（inner join）：根据两个表共有的列的值匹配两个表中的行。

自然连接（内连接）案例：
[class 表]            [student 表]          
 id   name            id     name      class_id
 1    一班             1     小明          2
 2    二班             2     小红          3
 3    三班             3     小张

$ select * from student inner join class on class.id=student.class_id;
【查询结果】
+----+------+-------------+----+------+
| id | name | class_id id | id | name |
+----+------+-------------+----+------+
| 1  | 小明 |      2      |  2 | 二班  |
| 2  | 小红 |      3      |  3 | 三班  |
+----+------+-------------+----+------+

左连接查询：select * from student left outer join class;  >> student 表中内容全部显示，class 信息没有的地方显示为 null。
右连接查询：select * from student right outer join class; >> class 表中内容全部显示，student 信息没有的地方显示为 null。
```

## Part III —— 数据库设计

### 1 请使用 E-R 图来直观的表示

### 2 通过 E-R 图的分析思考，确定表（实体）之间的关系
* 一对一。 1：1
* 一对多。 1：N
* 多对多。 N: N

### 3 数据库设计遵循的原则（范式概念）
范式的特点：分级、递进。``1NF ⊃ 2NF ⊃ 3NF ⊃ BCNF ⊃ 4NF ⊃ 5NF ⊃ 6NF``

##### 3.1 第一范式（First Normal Form）
所有属性都是不可分割的基本数据项。

##### 3.2 第二范式（Second Normal Form）
每个非主（non-primary）属性都是**完全函数依赖**于主键（primary）。``主键和非主属性之间的函数依赖关系。即，每个表必须有主键。``

##### 3.3 第三范式（Third Normal Form）
每个非主（non-primary）属性都**不传递函数依赖**于主键（primary）。 ``除主键之外，其他非主属性不能同时存在于两个表中。即，一个表中不能包含其他表中非关键字段的信息。（数据表不能有冗余字段。）``

注意：实际生产中往往不能遵守第三范式，因为合理的冗余字段将减少 join 查询的必要。

##### 3.4 BCNF（Boyce-Codd Normal Form）
每个属性都**不传递依赖于**主键。

## Part IV —— 数据库优化

### 1 数据库优化的方向
* 硬件更新
* 系统配置调优
* 数据库表结构优化
* SQL及索引优化

### 2 SQL及索引优化
1. 检查慢查日志是否开启。 ``show variables like 'slow_query_log';``
   ```
   设置日志位置：set global slow_query_log_file='/usr/share/mysql/sql_log/mysql-slow.log';
   查看变量信息：show variables like '%log%'; （查看所有log相关变量）
   配置：       set global log_queries_not_using_indexes=on;
   设置阈值：   set global long_query_time=1;
   开启：       set global slow_query_log=on;
   ```
2. 使用 MySQL 慢查日志分析工具。
3. 通过慢查日志发现有问题的 SQL。
    * 查询次数多且每次查询占用时间长的sql
    * IO 大的 sql
    * 未命中的索引的 sql
4. 通过 explain 查询分析 SQL 的执行计划。 ``示例：explain select count(*) from staff;``

##### 常见的优化案例：（重点）
1. 函数 Max() 的优化
2. 函数 Count() 的优化
3. 子查询的优化
4. group by 的优化
5. limit 查询的优化
6. 索引的优化

### 3 数据库结构的优化
1. 选择合适的数据类型
2. 数据库表的范式化优化
3. 数据库表的垂直拆分
4. 数据库表的水平拆分

### 4 数据库系统配置优化
1. 操作系统相关配置
    * 网络方面的配置，修改 /etc/sysctl_conf
        1. 增加 tcp 支持的队列数
        2. 减少断开连接时，资源回收（tcp有连接状态）
    * 打开文件数的限制，修改 /etc/security/limits.conf
    * 除此之外，最好在 MySQL 服务器上关闭 iptables、selinux 等防火墙软件。
2. MySQL 配置文件优化
    * 设置 max_used_connections / max_connections 的比值，理想值为 85%
    * back_log
    * interactive_timeout
    * 缓冲区变量
    * 其他等等

### 5 MySQL 的执行顺序（重要）
MySQL 的语句一共分为 11 步，最先执行的总是 FROM 操作，最后执行的是 LIMIT 操作。``其中每一个操作都会产生一张虚拟的表。``
只有最后的一个虚拟表才会作为结果返回。
