# JVM 优化

#### 内容
* JVM 运行参数及设置
* JVM 的内存模型（堆模型）
* 内存使用情况统计分析（jstat、jmap）
* 内存溢出的定位与分析
* JVM 线程执行情况分析（jstack）
* VisualVM （专门用于虚拟机分析优化的 Java 虚拟机）

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
