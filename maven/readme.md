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
