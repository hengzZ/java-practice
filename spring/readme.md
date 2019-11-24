## Spring

##### Spring 的核心内容
* Spring IoC 配置 （Inversion of Control）
* Spring AOP （Aspect Oriented Programming）
* Spring JDBC Template
* Spring 事务控制

##### Spring 概述
官方网站 http://spring.io/ ，Spring 的定位是做一个 java 的 ``full-stack`` 轻量级开源框架，同时提供了视图层方案 SpringMVC，持久层方案 Spring JDBC，以及业务层方案-业务层事务管理等。 另外，还支持开源世界的第三方框架和类库，如 Mybatis 等。

##### Spring 的优势
* 方便解耦，简化开发
* AOP 编程
* 声明式事务控制
* 方便的测试模块开发

各种官方教程 http://spring.io/guides

各种Spring工程方案 http://spring.io/projects

##### Spring 体系结构
http://docs.spring.io/spring/docs/4.2.x/spring-framework-reference/html/overview.html
<div align="center">
<img src="figures/spring-overview.png" width="50%">
</div>

* Core IoC (Inversion of Control)
* AOP
* DAO
* Web
* Test

doc 文档 http://docs.spring.io/spring/docs/

#### 1 IOC 详解
Inversion of Control 是一种编程/框架设计理念。 初衷是实现程序的解耦，程序编译时，不会由于依赖库的缺失而导致编译失败。（当然，运行是肯定会失败的。编码和编译却不会被影响。）
```java
// private IAccountDao accountDao = new AccountDaoImpl();
private IAcountDao accountDao = (IAccountDao)BeanFactory.getBean("accountDao");  // IoC 模式
```
因此 ，IoC 更应该被理解为 ``“IoC模式”``。

控制反转（Inversion of Control，缩写为IoC），是面向对象编程中的一种设计原则。 最常见的实现方式叫做依赖注入（Dependency Injection，简称DI），还有另一种实现方式，叫 “依赖查找”（Dependency Lookup）。

#### 2 AOP 概念
AOP 是 Aspect Oriented Programming 的缩写。 面向切面编程，通过预编译方式和运行期动态代理，实现程序功能的灵活性和可扩展性，AOP 实际是GoF 设计模式的延续。

AOP 的初衷是将日志记录，性能统计，安全控制，事务处理，异常处理等代码从业务逻辑代码中划分出来。

##### AOP 与 OOP 的比较
AOP 与 OOP 是两种不同关注点的设计思想。
* OOP 针对业务处理过程的实体及其属性和行为进行抽象封装。 （业务 -> 对象）
* AOP 针对业务处理过程中的 “切面（处理过程中的某个步骤或阶段）” 进行提取。 （切片 -> 对象）

AOP 是 OOP 的延续，终点都是对象，但是，将什么封装至对象是两者的重大差异。

##### AOP 的技术原理
动态代理技术

##### AOP 相关术语
* Joinpoint （连接点）
* Pointcut （切入点）
* Advice （通知/增强）
* Introduction （引介）
* Target （目标对象）
* Weaving （织入）
* Proxy （代理）
* Aspect （切面）

```java
/**
 * 获取 Service 代理对象
 * @return
 */
public IAccountService getAccountService() {
    return (IAccountService)Proxy.newProxyInstance(accountService.getClass().getClassLoader(),accountService.getClass().getInterfaces(),
    new InvocationHandler() {
        /**
         * 添加事务的支持
         *
         * @param proxy
         * @param method
         * @param args
         * @return
         * @throws Throwable
         */
        @Override
        public Object invoke(Object proxy, Method method, Object[] args) throws Trowable {
            if ("test".equals(method.getName())) {
                return method.invoke(accountService, args);
            }

            Object rtValue = null;
            try {
                //1. 开启事务
                txManager.beginTransaction();
                //2. 执行操作
                rtValue = method.invoke(accountService, args);
                //3. 提交事务
                txManager.commit();
                //4. 返回结果
                return rtValue;
            } catch (Exception e) {
                //5. 回滚操作
                txManager.rollback();
                throw new RuntimeException(e);
            } finally {
                //6. 释放连接
                txManager.release();
            }
        }
    });
}
```
仔细琢磨以上代码，感受业务代码和数据库事务代码的结合技巧。

#### 3 Spring AOP 开发的阶段
* 编写核心业务代码 （开发主线）
* 公用代码抽取，制作成通知。 （AOP 编程人员）
* 在配置文件中，声明切入点与通知的关系，即切面。 （AOP 编程人员）

##### 整个开发阶段，核心和难点是有一双慧眼，去抽取公共代码。

#### 4 Spring 的运行逻辑
Spring 框架监控切入点方法的执行。 一旦监测到切入点方法被执行，使用代理机制动态创建目标对象的代理对象，在代理对象的对应位置，将通知对应的功能织入，然后完成完整的代码逻辑运行。
