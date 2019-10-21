## Java 语法

### Part 1 —— 基础语法
* 核心概念
* 基本数据类型
* 语句
* 函数定义
* 代码组织

#### 1.1 提到 Java 源码时要牢记的概念
1. 大小写敏感
1. 类名 ClassName
1. 方法名 methodName
1. 源代码文件名 ClassName.java
1. 程序入口函数 public static void main(String[] args) {}

#### 1.2 修饰符
##### 1.2.1 访问权限修饰符
* default
* public
* protected
* private
##### 1.2.2 非访问相关的修饰符 （其他用途）
* static
* final
* abstract
* synchronized
* volatile

#### 1.3 变量作用域
* 局部变量 （函数内）
* 类变量 （静态成员变量）
* 实例的成员变量 （非静态的成员变量）

#### 1.4 基本数据类型
##### 1.4.1 Primitive （基本数据类型）
* 整数
  ```
  byte - 8 位，有符号
  short - 16 位，有符号
  int - 32 位，有符号
  long - 64 位，有符号
  ```
* 十进制数 （浮点数）
  ```
  float - 32 位
  double - 64 位
  ```
* 布尔数
  ```
  true or false
  ```
* 字符
  ```
  char - 16 位 unicode 编码
  ```
###### 特别说明： 如何选基本数据类型？
```
# 字符/字符串的存储
  选择字符类型或者 String 类型，没有什么可疑虑。
# 十进制数的存储
  对于常规的数值的存储，是需要特别讲究的：
  ● 首先要有并区分 integar / floating / decimal / precise 的概念。
  ● integar - 对应整数基本类型 （4种选择）
  ● floating - 对应 float 类型，例如 AI 的参数 （1种选择）
  ● decimal - 对应一些比较简单的 10 进制算术，选 double 类型 （1种选择）
  ● precise - 对应的是账户金额、余额、交易额的概念，注意！ 是不能使用基本数据类型来表示的！！ 请使用 string 来标识并操作。
```
##### 1.4.2 Reference/Object （引用/对象类型）
创建一个对象实例的三步骤：
* Declaration 声明变量 - 作为实例的标识符
* Instantiation 实例化 - 创建一个实例
* Initialization 初始化 - 调用对象的构造函数
```java
public class Puppy {
    // 构造函数定义
    public Puppy (String name) {
        System.out.println ("Passed Name is :" + name);
    }
    
    public static void main (String[] args) {
        Puppy myPuppy = new Puppy ("tommy");   // 变量声明(Puppy myPuppy) - 实例化（new） - 初始化（Puppy（“tommy”））
    }
}
```
对象的作用域：
* Class-Local Inner Class
* Method-Local Inner Class
* Anonymous(匿名) Inner Class
* Static nested classes （一定是 Class-Local）

#### 1.5 语句
* while
* for
* do..while
* if..else if
* switch
* ? :

#### 1.6 函数定义
编写 Java 函数，一定时刻牢记： 函数是一个类的函数！

#### 1.7 Java 代码编写请注意
##### 1.7.1 源代码编写注意
* 一个 java 源代码文件内，可以有多个 class 的定义，但是.. 只能有一个是 public 访问权限。
* java 源代码文件的名称，必须和内部的 public class 的名字一模一样！
##### 1.7.2 package 编写注意
* 如果使用 package 的概念来组织源代码的话，每一个 java 源码的文件格式一定是这样的：
  ```
  // 该源码属于哪个 package
  package animals;
  // 该源代码依赖哪个 package
  import java.io.File;
  import java.io.FileReader;
  import java.io.IOException;
  // 编写类的源码
  public class MammalInt {
  
  }
  ```

### Part 2 —— 面向对象 
* 继承与多态
* 标准库
* 异常编程和多线程编程
* 文件/IO/网络编程
