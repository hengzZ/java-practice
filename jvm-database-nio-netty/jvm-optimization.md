# JVM 优化

#### 内容

Part I
* JVM 运行参数及设置
* JVM 的内存模型（堆模型）
* 内存使用情况统计分析（jstat、jmap）
* 内存溢出的定位与分析
* JVM 线程执行情况分析（jstack）
* VisualVM （专门用于虚拟机分析优化的 Java 虚拟机）

Part II
* 什么是垃圾回收
* 垃圾回收的常见算法
* 串行、并行、并发、G1垃圾收集器
* GC日志的可视化查看

Part III
* Tomcat 的优化

Part IV
* JVM 字节码分析

Part V
* 编码的优化建议（代码优化）

<br>

## Part I —— 虚拟机运行参数、运行环境配置、虚拟机内存模型

### 1 为什么会有 JVM 优化的需要？
生产环境中会遇到各种运行现象，如 “卡住”、“cpu 负载突然升高”、“追踪多线程的数量和分配” 等等。 ``JVM 优化即针对运行现象的分析工具/思路的集合。``

### 2 JVM 运行参数
#### 2.1 三种参数类型

* 标准参数
    * -help
    * -version (client/server模式)

* -X 参数（非标准参数）
    * -Xint
    * -Xcomp
    * -Xmixed

* -XX 参数（使用频率较高，主要用于 debug。）
    * -XX:NewSize
    * -XX:+UseSerialGC
    * -XX:MaxHeapSize / -XX:InitialHeapSize (等价于 -Xmx2048m -Xms512m)

``标准参数为所有 Java 版本都有的参数，其他参数由具体版本的说明文档提供。``（请使用 java -help / java -X / java -XX:+PrintFlagsFinal -version 查看）

#### 2.2 Java 运行时打印参数
* ``java -XX:+PrintFlagsFinal <java程序>``
* ``jinfo -flags <进程id>``

技巧：jps -l 可替代 ps -ef 查看 java 程序的进程 id。

### 3 JVM 的内存模型
#### 3.1 JVM 的堆内存模型
JVM 的内存模型在 1.7 和 1.8 有较大的区别。（堆的数据存储存活机制的差异）
* 1.8 中使用 ``Matespace`` 代理 ``Permanent`` 区域。
* Young（Eden、Survivor） 和 Old 区域仍然保持，并与 1.7 版本一样。

因为合理的永久区（Perm）难以确定，稍有不慎就容易抛出异常，所以废弃 1.7 中的永久区是有利的。

#### 3.2 jstat 命令查看堆内存使用情况
``jstat -h 查看使用说明``

* 查看 class 加载统计 ``jstat -class <进程ID>``
* 查看编译统计 ``jstat -compiler <进程ID>``
* 垃圾回收统计信息 ``jstat -gc <进程ID>``

#### 3.3 jmap 获取更加详细的统计信息
jmap 可获取比 jstat 更加详细的信息，如：内存使用情况的汇总、对内存溢出的定位与分析。

* ``jmap -heap <进程ID>``
* ``jmap -histo <进程ID> | more``
* ``jmap -dump:format=b,file=<文件名> <进程ID>`` 将内存使用情况 dump 到文件中

#### 3.4 分析 jmap 导出的内存分析数据
* ``jhat -port <port> <file>``
* 还可以使用 MAT(Memroy Analyzer Tool) 工具来分析。

### 4 内存溢出的定位与分析
* 为 java 运行程序添加参数： ``-Xms8m -Xmx8m -XX:+HeapDumpOnOutOfMemoryError`` （发生内存溢出错误时，导出日志）

* 使用 MAT 工具查看错误日志，分析原因。

### 5 JVM 线程执行情况分析
使用 jstack 分析线程执行情况，如：服务器 cpu 的负载突然增高、线程死锁、死循环等等。

* ``jstack <进程ID>``
* 在 java 中线程的状态一共被分为 6 种：初始态（NEW）、运行态（RUNNABLE，分为 RUNNING 和 READY）、阻塞态（BLOCKED）、等待态（WAITING）、超时等待态（TIMED_WAITING）、终止态（TERMINATED）。

### 6 VisualVM 工具
性能分析神器 VisualVM （Java VisualVM）。http://docs.oracle.com/javase/7/docs/technotes/guides/visualvm/

``VisualVM 的强大之处在于，可以监控远程的 jvm 进程。需要借助于 JMX 技术实现。``

## Part II —— Java 的垃圾回收机制

### 1 什么是垃圾回收？
程序的运行必然需要申请内存资源，垃圾回收就是对内存资源的管理。

### 2 垃圾回收的常见算法
* 引用计数法 —— 引用计数器 （缺点：无法解决循环引用的问题。）
* 标记清除法 —— 标记（从根节点开始标记引用的对象）、清除（未被标记引用的对象就是垃圾对象）（缺点：效率低，需要遍历；清除时停止应用程序，对于交互应用不适用；内存碎片化严重。）
* 标记压缩法 —— 标记清除法的升级版（清除时将存活的对象压缩到内存的一端，解决碎片化问题。）（缺点：效率低，需要遍历；清除时停止应用程序，对于交互应用不适用。）
* 复制算法 —— 将原有的内存空间一分为二，每次只使用其中的一块。（垃圾回收时，将正在使用的对象复制到另一块内存空间中。）（缺点：只能使用一半，内存使用率低。另外，在垃圾对象少的情况下不适用，发生不断的复制。）
* 分代算法 —— 复制算法的升级版（Eden + 'From' Survivor + 'To' Survivor + Old）（``在 JVM 中，年轻代使用复制算法，老年代使用标记清除或标记压缩算法。``）

### 3 垃圾收集器以及内存分配
* 串行垃圾收集器 —— 使用单线程进行垃圾回收，其它所有线程暂停 STW(Stop-The-World)。（对于交互性强的应用来说是不能接受的。）
* 并行垃圾收集器 —— 将单线程改为多线程进行垃圾回收，缩短垃圾回收的时间，其它所有线程暂停 STW(Stop-The-World)。
* CMS（并发）垃圾收集器 —— Concurrent Mark Sweep，并发的使用标记-清除算法的垃圾回收器。该回收器是针对老年代垃圾回收的。
* G1 垃圾收集器 —— 简化 JVM 性能调优，三步骤：
    1. 第一步，开启 G1 垃圾收集器
    2. 第二步，设置堆的最大内存
    3. 第三步，设置最大的停顿时间

    G1 中提供了三种模式的垃圾回收模式，Young GC、Mixed GC 和 Full GC，在不同的条件下被触发。

``G1 垃圾收集器取消了年轻代、老年代的物理上划分，只是逻辑上的年轻代、老年代区域。``

```
# 测试配置
1. -XX:+UseSerialGC -XX:+PrintGCDetails -Xms16m -Xmx16m  # 串行收集器
2.
-XX:+UseParNewGC -XX:+PrintGCDetails -Xms16m -Xmx16m  # 并行收集器
-XX:+UseParallelGC -XX:+PrintGCDetails -Xms16m -Xmx16m  # 并行收集器
-XX:+UseParallelOldGC -XX:+PrintGCDetails -Xms16m -Xmx16m  # 并行收集器
# ParallelGC 可搭配 -XX:MaxGCPauseMillis -XX:GCTimeRatio -XX:UseAdaptiveSizePolicy 使用。
3. -XX:+UseConcMarkSweepGC -XX:+PrintGCDetails -Xms16m -Xmx16m  # CMS（并发）垃圾收集器
4.
-XX:+UseG1GC 使用 G1 垃圾收集器
-XX:MaxGCPauseMillis 默认 200 毫秒（期望值，不是一定达到！）
-XX:G1HeapRegionSize=n 设置 G1 区域的大小，范围是 1MB 到 32MB 之间。
-XX:ParallelGCThreads=n 设置 STW 工作线程数的值，最多为 8。
-XX:ConcGCThreads=n 设置并行标记的线程数，ParallelGCThreads 的 1/4 左右。
-XX:InitiatingHeapOccupancyPercent=n 设置触发标记周期的 java 堆占用率阈值。
# Mixed GC 什么时候触发？由参数 -XX:InitiatingHeapOccupancyPercent=n 决定。默认：45%，即老年代大小占整个堆大小百分比达到 45% 时。
示例： -XX:+UseG1GC -XX:MaxGCPauseMillis=100 -XX:+PrintGCDetails -Xmx256m
```

### 4 可视化 GC 日志分析工具
在日志打印输出涉及到的参数如下：
```
1. -XX:+PrintGC 输出 GC 日志
2. -XX:+PrintGCDetails 输出 GC 的详细日志
3. -XX:+PrintGCTimeStamps 输出 GC 的时间戳
4. -XX:+PrintGCDateStamps 输出 GC 的时间戳（以日期形式）
5. -XX:+PrintHeapAtGC 在进行 GC 的前后打印出堆的信息
6. -Xloggc:../logs/gc.log 日志文件的输出路径
```

GC Easy 是一款在线的可视化工具，易用且功能强大。http://gceasy.io/

## Part III —— Tomcat8 的优化

### 1 Tomcat 的优化方向
* Tomcat 自身的配置
* 对 Tomcat 所运行的 jvm 虚拟机的调优

### 2 修改 Tomcat 的配置
* 禁用 AJP（Apache JServer Protocol） 服务
* 修改 server.xml，为 Tomcat 的运行提供线程池（添加一个执行器配置）
* Tomcat 的三种运行模式：
    1. bio —— 阻塞 IO，默认模式，性能低下。
    2. nio —— New IO 基于缓冲区，并提供非阻塞 IO 操作的 Java API。（non-blocking I/O） （Tomcat8 之后，添加了 nio2 模式）
    3. apr —— 该模式安装起来最困难，但是从操作系统级别来解决异步 IO 的问题，大幅度提高性能。
* 设置 Tomcat 最大等待队列数。（如果超过就不等待了，因此这样有些请求是失败的。但是请求时间就有保障了，典型应用如：12306。）

### 3 Apache JMeter 开源的压力测试工具，测试 Tomcat 的吞吐量等信息

### 4 调整 JVM 参数来调优 Tomcat 的性能
* 设置并行垃圾回收器
* 设置 G1 垃圾回收器
* 查看分析 gc 日志文件（Garbage Collection）

## Part IV —— JVM 字节码分析
* 查看 class 文件中的字节码内容 ``javap -v Test.class > Test.txt``。 ``javap -help 查看使用说明``

分析字节码，查看效率差异。

## Part V —— 编码的优化建议（代码优化）
1. 尽可能使用局部变量
2. 尽量减少对变量的重复计算 ``减少如下习惯：for(int i = 0; i < list.size(); i++) {...}``
3. 尽量采用懒加载的策略，在需要的时候才创建
4. 异常不应该用来控制程序流程
5. 不要将数组声明为 public static final
6. 不要创建一些不使用的对象，不要导入一些不使用的类
7. 程序运行过程中避免使用反射
8. 使用数据库连接池和线程池
9. 容器初始化时尽可能指定长度
10. ArrayList 随机遍历快，LinkedList 添加删除快
11. 使用 Entry 遍历 Map ``Map<String,String> map = new HashMap(); for(Map.Entry<String,String> entry : map.entrySet()) {String key = entry.getKey(); String value = entry.getValue();}``
12. 不要手动调用 System.gc()
13. String 尽量少用正则表达式
14. 日志的输出要注意级别
15. 对资源的 close() 建议分开操作 ``推荐： try{XXX.close();}catch(Exception e){...} try{YYY.close();}catch(Exception e){...}``
