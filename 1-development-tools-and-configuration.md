## 开发工具与环境配置

#### 1. Java 语言开发环境搭建

##### 1.1 Java 虚拟机 —— JVM
JVM（Java Virtual Machine） 是 java 程序实际运行的环境。

###### Java 语言具有跨平台特性，但是，JVM 不具备跨平台特性，不同的操作系统下是不同版本的 JVM。

##### 1.2 JRE 和 JDK
JRE（Java Runtime Environment） 是 java 程序的运行时环境，指 ``JVM + 运行时需要的核心类库``。

JDK（Java Development Kit） 是 java 程序开发工具包，包含 ``JRE + 开发人员需要的工具（编译器等）``。

###### 运行 java 程序时，仅仅需要 JRE，但是，开发程序时需要 JDK。

##### 1.3 JDK 下载和安装
* 版本选择 Java 9，因为 Java 10 的更新可忽略不计。 （Java 9 是最后一个大版本更新）
* Java 8 为稳定版，因为已有很多企业基于这个版本开发。

###### 例如： JavaSE 9.0.4： 打开 Oracle Java 下载页面，找到 Java Archive，点击右侧 Download 然后查找自己想要的版本。

* 安装说明
  ```
  安装时，路径中最好不要出现中文和空格符。
  安装时，不需要安装独立 JRE，仅勾选 开发工具 + 源代码。
  ```

##### 1.4 Hello World 测试
* 编写 java 源代码文件 MyFirstJavaProgram.java
  ```java
  public class MyFirstJavaProgram {
    
    public static void main (String[] args) {
        System.out.println("Hello World");
    }
  }
  ```
* 编译 MyFirstJavaProgram.java 文件
  ```bash
  javac MyFirstJavaProgram.java
  ```
* 运行 java 程序
  ```bash
  java MyFirstJavaProgram
  ```
* 控制台输出结果
  ```bash
  Hello World
  ```

#### 2. Java 开发 IDE 安装和测试

###### 为什么用 IDE? 因为可以提高开发效率（速度）。

##### 2.1 IDEA —— 开发用 IDE 安装
搜索 IntelliJ IDEA，下载 Ultimate 版本。 （JetBrains 公司的产品）
###### 需要激活

##### 2.2 IDEA 测试
* 打开 IDEA 软件， 直接选择跳过 IDE 的配置即可。
* 点击 Create New Project，创建一个项目。
* 新建一个 Module。
* 选择 JDK，点击右侧的 New，然后选择已安装的 Java 9 对应的目录 jdk-9.0.4。
* 点击文件，新建一个 File ``MyFirstJavaProgram.java``，并编辑。
  ```java
  public class MyFirstJavaProgram {
    
    public static void main (String[] args) {
        System.out.println("Hello World");
    }
  }
  ```
* 编译
  ```
  点击 IDE 上部菜单栏的 Build，编译项目。
  ```
* 运行
  ```
  # 运行一个应用程序时，都需要有一个配置，这个过程是基本的。
  # 点击 Run 菜单，选择 编辑配置（Edit Configuration），然后点击 "+" 符号。
  # 选择 Application，填写右侧需要填的配置信息。 （主要是 Class Name，以及 Application 的 Name）
  # 点击 OK 后，再次点击 Run 菜单，选择刚才添加的 Application 的名字并运行即可。
  ```
* IDEA 界面的下部，Run 栏内会显示输出结果
  ```
  Hello World
  ```
