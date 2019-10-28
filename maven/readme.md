## Maven

用于解决或者简化的任务：
1. jar 引用管理和防冲突。 ``#依赖管理``
2. 项目编译。 ``#build``
3. 单元测试自动化。 ``#``
4. 管理维护繁多的配置文件。 ``#``
5. 打包。 ``#``

Maven 官网： https://maven.apache.org/ ，Maven 还有自己的仓库网站 https://mvnrepository.com/ ，因此，它像 Git 一样是一个管理工具/软件。 （Maven 是一个应用软件。）

#### Maven 下载安装
下载网站 https://archive.apache.org/dist/maven/maven-3/

* 下载 binaries 目录下 apache-maven-3.5.3-bin.zip 文件
* 安装： 解压缩即可使用。
* 配置： 设置环境变量 ``MAVEN_HOME`` 为 maven 目录路径。
  ```
  # 可以在 windows 下的 linux bash (GitBash) 终端中创建一个脚本 maven.sh 如下：
  export MAVEN_HOME=/c/Users/zhihengw/PycharmProjects/apache-maven-3.5.3/${MAVEN_HOME:+:${MAVEN_HOME}}
  export PATH=/c/Users/zhihengw/PycharmProjects/apache-maven-3.5.3/bin/${PATH:+:${PATH}}
  # 每次使用前，source maven.sh 然后使用即可。
  ```

#### Maven 快速入门
* 打开命令行窗口，进入 maven 目录下的 bin 目录；
* 执行 ``mvn -v``，查看 maven 版本信息。
###### Maven 就是个控制台工具，-h 或者 -v 就是控制台工具的第一入门。


## Maven 使用
帮助文档 http://maven.apache.org/guides/index.html

#### Maven 环境测试
##### 1. 使用 maven 创建一个 Java 项目
```bash
mvn archetype:generate -DgroupId=com.mycompany.app -DartifactId=my-app -DarchetypeArtifactId=maven-archetype-quickstart -DarchetypeVersion=1.4 -DinteractiveMode=false
```

##### 2. Build the Project
```bash
cd my-app
mvn package
```

##### 3. Test the newly compiled and packaged JAR
```bash
java -cp target/my-app-1.0-SNAPSHOT.jar com.mycompany.app.App
```
* 备注： maven 指定代理： 形如 mvn compile ``-Dhttps.proxyHost=192.168.163.118 -Dhttps.proxyPort=3128``

以上三步成功完成，表示 maven 环境成功。 可以开始使用了。

创建 Java 项目模板成功后，打印信息如下：
```
[INFO] -----------------------------------------------------------------------------
[INFO] Using following parameters for creating project from Archetype: maven-archetype-quickstart:1.4
[INFO] ----------------------------------------------------------------------------
[INFO] Parameter: groupId, Value: com.mycompany.app
[INFO] Parameter: artifactId, Value: my-app
[INFO] Parameter: version, Value: 1.0-SNAPSHOT
[INFO] Parameter: package, Value: com.mycompany.app
[INFO] Parameter: packageInPathFormat, Value: com/mycompany/app
[INFO] Parameter: package, Value: com.mycompany.app
[INFO] Parameter: groupId, Value: com.mycompany.app
[INFO] Parameter: artifactId, Value: my-app
[INFO] Parameter: version, Value: 1.0-SNAPSHOT
[INFO] Project created from Archetype in dir: C:\Users\zhihengw\PycharmProjects\my-app
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

#### Maven 的 Java 项目模板
* 核心代码部分。 （Java 代码）
* 配置文件部分。 （配置文件）
* 测试代码部分。 （单元测试代码）
* 测试配置文件。 （测试环境配置文件）

##### maven 从以上四个方面考虑，定义了一个标准的目录规范：
* src/main/java 目录  -->  Java 核心代码
* src/main/resources 目录  --> 配置文件
* src/test/java 目录  --> 测试人员代码
* src/test/resources 目录  --> 测试环境配置文件
* src/main/webapp 目录  --> 页面资源（css、js、html、图片等等） // 针对 web 开发

#### Maven 常用命令
1. compile
   ```
   编译命令，将 src/main/java 目录下的代码编译为 class 文件，并输出到 target 目录下。
   $ mvn compile
   ```
2. clean
   ```
   清除命令，清除的是 target 目录以及内部所有内容和文件。
   $ mvn clean
   ```
3. test
   ```
   测试命令，将 src/test/java 目录下的代码编译为 class 文件，并输出到 target 目录下。
   # 默认会执行 mvn compile，进行 Java 核心代码的编译工作。 （如果之前没编译的话）
   $ mvn test
   ```
4. package
   ```
   打包命令，将 src/main/java 目录下的代码编译为 jar/war 包，并输出到 target 目录下。
   # 默认会执行 mvn compile 和 mvn test， 进行编译工作。 （如果之前没编译的话）
   $ mvn package
   ```
5. install
   ```
   安装命令，将 src/main/java 代码打包，并上传至仓库中。
   # 默认会执行 mvn pakcage，进行编译工作。
   $ mvn install
   ```


## Maven 的 "Lifecycle" 概念
生命周期（lifecycle） 就是将 ``编译Java代码、编译test代码、打包、安装、部署`` 这五步流程用一个名词来说明/替代。

拿到一个别人的 maven 工程，首先要确认的是当前处于的状态：
* 还在开发阶段 main or test；
* 已生成完整的 target 目录内容（mvn package）；
* 已安装（mvn install），将包上传至仓库中；
* 还是，已部署（mvn deploy）。

此时，谈论的就是，当前处于 maven （默认）生命周期的哪个阶段。
###### maven 还有另外两个生命周期的概念： 清理生命周期(Clean Lifecycle)、 站点管理生命周期(Site Lifecycle)。 


## Maven 的理念/概念模型图
pom.xml 文件包含了一个 maven 构建的 Java 项目包含的所有信息，主要是：
1. 依赖环境的说明和记录；  --> pom.xml 文件中 dependencies 标签对应的内容。
2. 编译的流程。 （maven 中称作一键构建）  --> pom.xml 文件中 build 标签对应的内容。

以图的形式展示 pom.xml 文件的内容组成，如下：
<div align="center"><img src="../pics/maven-pom.png" width="60%"></div>

<br>

# IDEA + Maven 进行 Java 开发

### 在 IDEA 中关联 Maven
##### 1. 配置 IDEA
* 打开 IDEA，点击 File 菜单，选择 Settings；
* 在 Build,Execution,Deployment > Build Tools 中找到 Maven；
* 点击 Maven 菜单，在右侧配置框中设置：
    * Maven home directory： Maven 目录路径；
    * User settings file:  Maven 的 conf/settings.xml 文件路径；
    * Local repository: Maven 的 local 仓库路径。 （默认为：${user.home}/.m2/repository）
* 点击 Maven > Runner 菜单，设置 VM Options: ``-DarchetypeCatalog=internal``。 （运行参数配置，推荐该配置）

###### 关于设置 IDEA + Maven 的网络代理的问题
```
1. 在 IDEA 的 File > Settings > Plugins 中设置 IDEA 的代理。
2. 在 Maven 的 conf/settings.xml 中设置 Maven 的代理。
# 如果需要代理的话，两个软件都需要设置代理，缺一不可。
```

##### 2. 测试
* 打开 IDEA，创建一个新项目（New Project）；
* 找到左边的 Maven 选项，点击；
* 此处，注意： 是否使用骨架（archetype）/模板？
    ```
    # 1. 使用骨架创建 Java 项目
    * 勾选 Create from archetype；
    * 选择要使用的 archetype，如： maven-archetype-quickstart 选项；
    * 点击 Next，指定： groudID，artifactID，version。
    ```
    ```
    # 2. 不使用骨架创建 Java 项目
    * 不勾选 Create from archetype；
    * 点击 Next，指定： groudID，artifactID，version。
    ```
    ```
    # 3. 使用 web 骨架创建 Java 项目
    * 勾选 Create from archetype；
    * 选择要使用的 archetype： maven-archetype-webapp 选项；
    * 点击 Next，指定： groudID，artifactID，version。
    ```
    ```
    # groudID - 公司名称，任意填写。
    # artifactID - app的名称，自定义。
    # version - 版本号，目前使用默认的即可。
    ```
    ###### 注意: 1. 不推荐使用骨架来创建 Java 项目。 2. 创建项目之后，记得去关注右下角的弹窗，然后选择 “自动加载 Enable Auto-Import”！！

##### 3. 添加文件夹/目录的正确方式 （重要事项）
* 光标放置于指定目录上，右键，点击 New 创建文件夹；
* 注意！ 创建成功后，右键，点击 **Mark Directory as**，选择文件夹的性质。 （非常关键！！）
    * Sources Root （Java 代码目录）
    * Test Sources Root （配置文件目录）
    * Resources Root （测试代码目录）
    * Test Resources Root （测试环境配置文件目录）

##### 4. 运行
使用 IDEA 运行程序，首先需要配置运行环境： Run > Edit Configurations 。
* quickstart 骨架，配置 application 选项。 ``设置 JRE 和 Main Class``
* webapp 骨架，配置 tomcat 选项。 ``templates 中找 tomcat server，进行配置。 注意，一定要去配置 Deployment！ 如果 Deploy at the server startup 栏为空，点击右侧加号添加一个 Artifact，然后就可以（出现）设置下面的 Application context（虚拟目录） 配置。``

配置完成后，点击 Run 或者绿色的小三角运行指定的 Java Class 文件。 /或双击 index.jsp 访问网页。

##### 5. 补充： Maven plugins 环境报错的解决方法
1. 如果是代理问题，请分别设置 IDEA 和 Maven 的代理。 二者缺一不可。
2. 如果网络连接正常，则查看报错的 plugin 是哪个，例如： org.apache.maven.plugins:maven-site-plugin:3.3 ，那么：
   ```
   注意，所有的 plugins 都是被下载放置于 local repositories 目录下的！
   1. 查看 org/apache/maven/plugins 目录下的对应文件夹是否存在；
   2. 存在的话，进入对应的文件夹，删除文件夹内的所有文件；
   3. 在 IDEA 的 Maven 控制面板中点击 "旋转符号"，Reimport 按钮。 等待重新下载即可。
   ```

### 为 Maven 工程导入 Jar 包
1. 编辑 pom.xml 文件，添加 dependencies 标签；
2. 如果已有 dependencies 标签的话，直接在内部添加 dependency 即可。
   ```
   例如：
   <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>servlet-api</artifactId>
      <version>2.5</version>
    </dependency>
   ```
3. **如何查找 jar 包的坐标**
    * 百度搜索 maven 中央仓库：https://mvnrepository.com/ ，打开网页；
    * 在搜索栏中搜索需要的 jar 包名称即可。
      ```
      如： 搜索 jsp 可获得一个条目显示如下：
      * JSP API
      javax.servlet » jsp-api
      # 点击进入，可知道有多少个版本。
      ```

### 在 IDEA 中执行 Maven 的命令（生命周期执行）
IDEA 右侧有一个 Maven，点击它就可以显示或缩小控制面板。

* 双击 Lifecycle 中的对应项就是执行对应的命令。
* 或者，寻找 Maven 面板上的菜单栏，有一个“m”标识的按钮，即命令行运行 mvn。

注意，这就是一个命令行终端。 命令不能执行也有错误原因提示。
