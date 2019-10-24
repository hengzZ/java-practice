## BeanUtils 工具类

Apache 组织下的产品，用于封装 JavaBean 的。

#### 什么是 JavaBean?
JavaBean 即标准的 Java 类，要求如下：
* 类必须被 public 修饰
* 必须提供空参的构造器
* 成员变量必须使用 private 修饰
* 提供公共 setter 和 getter 方法

##### 要注意的概念
* 成员变量： 就是常规理解的那样。
* 属性： setter 和 getter 方法截取后的产物。
  ```
  例如： getUsername() --> Username --> username
  ```

#### BeanUtils 工具类常用的方法
* setProperty()
* gerProperty()
* populate(Object obj, Map map) 将 map 集合的键值对信息，封装到对应的 JavaBean 对象中。

作用很明显，使用 BeanUtils 可以简化对 JavaBean 对象的属性值设定。 （简化代码量）

