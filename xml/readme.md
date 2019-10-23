## XML 文件介绍
Extensible Markup Language（XML） 可扩展标记语言

#### XML 的由来
XML 的设计是在 HTML 之后，设计之初的目的是取代 HTML，因为 HTML 的语法不是强约束的。 但是，后来找到了新出路。

#### XML 的用途以及与 HTML 的区别
* XML 标签都是自定义的，HTML 标签是预定义。
* XML 语法严格，HTML 语法松散。
* XML 是存储数据的，HTML 是展示数据的。

#### XML 基本语法
1. XML 文档的后缀名 .xml。
2. XML 第一行必须定义为文档声明。 ``<?xml version="1.0" ?>``
3. 标签的属性值必须使用双引号（单双都可）引起来。
4. 标签必须正常关闭。
5. XML 标签名称区分大小写。
6. XML 文档中有且仅有一个根标签。

#### XML 的组成部分
1. 文档声明
    1. 格式： ``<?xml 属性列表 ？>``
    1. 属性列表：
        * version: 版本号
        * encoding: 编码方式（字符集）
        * standalone: 是否独立（已弃用）
2. 指令（了解）： 结合 CSS 的，当初为了替代 HTML，现在已无用
    * ``<?xml-stylesheet type="text/css" href="a.css" ?>``
3. 标签： 标签名称自定义的
4. 属性：
    * id 属性值唯一
5. 文本：
    * CDATA 区： 在该区域中的数据会被原样展示
        * 格式： ``<![CDATA[ 数据 ]]>``

### XML 约束 —— 规定 xml 文档的书写规则
学习目标：
* 能够在 xml 中引入约束文档
* 能够简单的读懂约束文档

#### XML 约束技术
* DTD： 一种简单的约束技术
* Schema: 一种复杂的约束技术

约束技术的用途： 因为 XML 标签都是自定义的，那么读和写 xml 的人如何互动？？ 有了约束的存在，就只能基于约束来写和读了。

案例1： 使用 DTD 约束的示例
```xml
<?xml version="1.0" encoding="utf-8" ?>
<!-- 外引 -->
<!DOCTYPE students SYSTEM "student.dtd">

<!-- 内联 -->
<!--<!DOCTYPE students [
    <!ELEMENT students (student+) >
    <!ELEMENT student (name,age,sex)>
    <!ELEMENT name (#PCDATA)>
    <!ELEMENT age (#PCDATA)>
    <!ELEMENT sex (#PCDATA)>
    <!ATTLIST student number ID #REQUIRED>
]>-->

<students>

    <student number="s001">
        <name>zhangsan</name>
        <age>23</age>
        <sex>male</sex>
    </student>
    
    <student number="s001">
        <name>lisi</name>
        <age>24</age>
        <sex>female</sex>
    </student>

</students>
```

案例2: 使用 Schema 约束的示例
```xml
<?xml version="1.0"?>

<note xmlns="https://www.w3schools.com"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="https://www.w3schools.com note.xsd">

<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>
```

XML Schema 的学习，参考网络教程。 https://www.runoob.com/schema/schema-tutorial.html

最后，为什么使用 XML Schemas?
* XML Schema 最重要的能力之一就是对数据类型的支持。 （可以约束数据类型）
* **XML Schema 可保护数据通信**。 通过 XML Schema，发送方可以用一种接受方能够明白的方式来描述数据。

### XML 解析

#### 解析 xml 的方式
* DOM 思想： 将标记语言文档一次性加载进内存中，在内存中形成一颗 dom 树。
    * 优点： 操作方便。
    * 缺点： 占用内存。
* SAX 思想： 逐行读取，基于事件驱动的。
    * 优点： 基本不占内存，适合嵌入式设备以及手机。
    * 缺点： 只能读，不能增删改。

#### 常见的 xml 解析器
* JAXP: Sun 公司提供的解析器，支持 DOM 和 SAX 两种思想。 （不好用）
* DOM4J: 一款非常优秀的解析器，基于 DOM 思想实现。 （服务端程序一般使用这个）
* Jsoup: 一款 Java HTML 解析器，但是可以用于 XML 解析，基于 DOM 思想。
* PULL: Android 操作系统内置的解析器，SAX 方式的。

使用的时候选择一款，学习使用。
