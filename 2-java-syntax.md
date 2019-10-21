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

#### 2.1 继承与多态
##### 2.1.1 继承
***extends*** —— abstract / non-abstract
```java
public class Animal {
}

public class Mammal extends Animal {
}

public class Reptile extends Animal {
}

public class Dog extends Mammal {
}
```
* 注意 Java 的 ***super*** 关键字，类似于 C++ 的 ***this*** 关键字，但是..引用的不是当前对象，而是指 SuperClass （父类）。
* abstract 的概念源自于 “不能实例化”。
##### 2.1.2 多态
***implements*** —— interface
```java
/* File name : Animal.java */
interface Animal {
   public void eat();
   public void travel();
}

/* File name : MammalInt.java */
public class MammalInt implements Animal {

   public void eat() {
      System.out.println("Mammal eats");
   }

   public void travel() {
      System.out.println("Mammal travels");
   }

   public int noOfLegs() {
      return 0;
   }

   public static void main(String args[]) {
      MammalInt m = new MammalInt();
      m.eat();
      m.travel();
   }
}
```
使用 interface 扩展 interface
```java
// Filename: Sports.java
public interface Sports {
   public void setHomeTeam(String name);
   public void setVisitingTeam(String name);
}

// Filename: Football.java
public interface Football extends Sports {
   public void homeTeamScored(int points);
   public void visitingTeamScored(int points);
   public void endOfQuarter(int quarter);
}

// Filename: Hockey.java
public interface Hockey extends Sports {
   public void homeGoalScored();
   public void visitingGoalScored();
   public void endOfPeriod(int period);
   public void overtimePeriod(int ot);
}
```
多态与继承混合示例
```java
public interface Vegetarian{}
public class Animal{}
public class Deer extends Animal implements Vegetarian{}

Deer d = new Deer();
Animal a = d;
Vegetarian v = d;
Object o = d;
```
* interface 的概念源自于 “只定义函数接口，拒绝函数体细节”。

#### 2.2 数组

###### 数组是一种引用数据类型。 （Java 中除了基本数据类型，其他都是引用类型！）
###### 数组在运行期间，长度不可改变。

##### 2.2.1 创建一个数组对象
```java
方式1： 基本数据类型[] 标识符;
方式2： 基本数据类型 标识符[];
# 强烈推荐第一种书写方法，坚决抵制第二种书写。
```

##### 2.2.2 访问数组的元素
```java
方式1： []
    double total = 0;
    for (int i = 0; i < myList.length; i++) {
        total += myList[i];
    }
方式2： for (:)
    double[] myList = {1.9, 2.9, 3.4, 3.5};
    for (double element: myList) {
        System.out.println(element);
    }
```

##### 2.2.3 Java 中的内存划分
Java 的内存需要划分成 5 个部分
* 栈内存 stack
* 堆内存 heap （凡是 new 出来的东西，都在堆中。）
* 方法区 Method Area
* 本地方法栈 Native Method Stack （与操作系统相关）
* 寄存器 pc Register （与 CPU 相关）

##### 2.2.4 一个数组的内存图
一个数组的内存空间是在 堆内存 heap 中。 为一大块连续的内存空间。

##### 2.2.5 一个对象的内存图
成员变量在 堆内存 heap 中，成员方法（其实是保存的地址）也在 堆内存 heap 中，成员方法的实现代码在 方法区 Method Area 中。

###### 补充知识： Java 的垃圾回收机制
```
Java 中没有 “析构” 的概念，也不存在析构函数，代之的是 Java 的垃圾回收机制。
# Java 如何来清理内存？
  对于 JVM 来说，只要没有面临内存耗尽，那么，与垃圾回收有关的任何行为（尤其是 void fanalize() 方法）
  都不会执行。 简言之，不是迫不得已 Java 是不会浪费任何时间执行垃圾回收的。
# 那么如何自己定制垃圾回收策略？
  没有绝对的强制垃圾回收的方法，不过可以这样去做：
    ● 对于不再引用的对象，及时把它的引用赋为 null。 obj = null;
    ● 如果内存确实很紧张，调用 System.gc() 方法来建议垃圾回收器开始回收垃圾。
# 你是什么垃圾！
    ○ StrongReference - 强引用，暂时不是垃圾，未来不确定。
    ○ SoftReference - 软引用，当内存不足，将它当成垃圾回收。
    ○ WeakReference - 弱引用，垃圾，由 JVM 中的垃圾回收器发现并回收。
    ○ PhantomReference - 虚引用，空指针，垃圾？？？ 在任何时候都可能被垃圾回收器回收。
```

#### 2.3 标准库
