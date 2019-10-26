## Filter （过滤器）

Web 中的过滤器： 当访问服务器的资源时，过滤器可以将请求拦截下来，完成一些特殊的功能。

过滤器的作用：
* 一般用于完成通过的操作。 如：登陆验证、统一编码处理、敏感字符过滤。。

### 过滤器快速入门

##### 步骤
1. 定义一个类，实现接口 Filter;
2. 重写方法；
3. 配置拦截路径
    1. web.xml
    2. 注解配置 ``自定义类前添加如： @WebFilter("/*")``

```java
package filters;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import java.io.IOException;

@WebFilter("/*") //访问所有资源之前，都会执行该过滤器
public class FilterDemo1 implements Filter {
    
    /**
     * 在服务器启动后，会创建 Filter 对象，然后调用 init 方法
     */
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {

    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        // 对 request 对象的请求消息增强
        System.out.println("filterDemo1 被执行了...");

        // 放行
        filterChain.doFilter(servletRequest,servletResponse);
        
        // 对 response 对象的响应消息增强
        System.out.println("filterDemo1 回来了...");
    }

    /**
     * 在服务器关闭后，Filter 对象被销毁。 如果服务器是正常关闭，则会执行 destroy 方法
     */
    @Override
    public void destroy() {

    }
}
```

#### 过滤器细节
1. web.xml 配置 （查文档）
2. 过滤器执行流程 （看前文的快速入门中 doFilter 方法内的注释）
3. 过滤器对象的生命周期 （看快速入门的代码注释）
4. 过滤器配置详情
    * 拦截路径配置
      ```
      1. 具体资源路径： /index.jsp
      2. 拦截目录： /user/*
      3. 后缀名拦截： *.jsp
      4. 拦截所有资源： /*
      ```
    * 拦截方式配置: 资源被访问的方式
      ```
      * 注解配置
           * 设置 dispatcherTypes 属性
               1. REQUEST: 默认值。 浏览器直接请求资源
               2. FORWARD: 转发访问资源
               3. INCLUDE: 包含访问资源
               4. ERROR: 错误跳转资源
               5. ASYNC: 异步访问资源
      * web.xml配置
      ```
5. 过滤器链 （配置多个过滤器）
    * 执行顺序： 如果有两个过滤器，过滤器1和过滤器2
      ```
      # 执行顺序：
      1. 过滤器1
      2. 过滤器2
      3. 资源执行
      4. 过滤器2
      5. 过滤器1
      ```
    * 过滤器先后顺序的问题：
      ```
      1. 注解配置： 按照类名的字符串比较规则进行比较，值小的先执行。
      2. web.xml配置： 谁定义在上边，谁先执行。
      ```

## Listener （监听器）

事件监听机制：
* 事件
* 事件源
* 监听器
* 注册监听： 将事件、事件源、监听器绑定在一起。 当事件源上发生某个事件后，执行监听器代码。

### 监听器快速入门
案例：
* ServletContextListener: 监听 ServletContext 对象的创建和销毁
    * 方法：
      ```
      * void contextDestroyed(ServletContextEvent sce): ServletContext 对象被销毁前会调用该方法
      * void contextInitialized(ServletContextEvent sce): ServletContext 对象创建后会调用该方法
      ```
    * 步骤：
      ```
      1. 定义一个类，实现 ServletContextListener 接口；
      2. 复写方法；
      3. 配置
          * web.xml 配置
          * 注解配置
      ```

Listener 没有 Filter 使用的频繁，因此，先了解即可。 ``总之，Listener 使我们可以监听服务器端的对象的变化（事件），然后基于事件来做应变处理。``
一般，自己不会去实现 Listener，而是将框架已实现好的 Listener 进行配置使用而已。

## JavaWeb 的三大组件
* Servlet
* Filter
* Listener
