## JQuery

JQuery 是一个 JavaScript 库，极大地简化了 JavaScript 编程。 ``Query-选择器。`` 

### JQuery 快速入门
1. 导入 JQuery 的 js 文件
   ```
   jquery-xxx.js 与 jquery-xxx.min.js 的区别：
       1. jquery-xxx.js： 开发版本。 给程序员看的，有良好的缩进和注释。 文件体积大一些。
       2. jquery-xxx.min.js： 生产版本。 程序中使用，没有缩进。 体积小一些，程序加载更快。
   ```
2. 使用
   ```
   var div1 = $("#div1");
   alert(div1.html());
   ```

#### JQuery 对象与 JS 对象的区别和转换
1. JQuery 对象在操作时，更方便。
2. JQuery 对象和 JS 对象方法不通用。
3. 两者互相转换：
   ```
   * jq --> js:  JQ对象[索引] 或者 JQ对象.get(索引)
   * js --> jq:  $(JS对象)
   ```

#### 选择器
1. 基本语法学习
   ```
   1. 事件绑定
      $("#b1").click(function(){
      
      });
   2. 入口函数  #牢记，所有的 js 代码写在这个函数里面！！
      $(function() {
      
      });
      // 不推荐使用 window.onload = function(){ }; 的方式
   3. 式样控制
      $(#div1).css("background-color","red");
      $(#div1).css("backgroundColor","pink");  //DOM写法
   ```
2. 分类
    1. 基本选择器
       ```
       1.标签选择器    $("html标签名")
       2.id选择器      $("#id的属性值")
       3.类选择器      $(".class的属性值")
       4.并集选择器    $("选择器1,选择器2,...")  获得多个选择器选中的所有元素
       ```
    2. 层级选择器
       ```
       1.后代选择器    $("A B")      A 元素内部的所有 B 元素 （子辈、孙子辈、曾孙辈..都被选中）
       2.子选择器      $("A > B")    A 元素内部的所有 B 子元素 （只选中属于子辈的元素）
       ```
    3. 属性选择器
       ```
       1.属性名称选择器   $("A[属性名]")             指定属性
       2.属性选择器       $("A[属性名='值']")        指定属性等于指定值
       3.复合属性选择器   $("A[属性名='值'][]...")    包含多个属性条件
       # 注意，除了 “=” 等号，还有很多符号： 不等于 “！=” 包含 “*=” 以某值开头 “^=” 等等运算符。
       ```
    4. 过滤选择器
       ```
       1.首元素选择器    :first
       2.尾元素选择器    :last
       3.非元素选择器    :not(selector)
       4.偶数选择器      :even
       5.奇数选择器      :odd
       6.等于索引选择器   :eq(index)
       7.大于索引选择器   :gt(index)
       8.小于索引选择器   :lt(index)
       9.标题选择器       :header  获取标题元素
       ```
    5. 表单过滤选择器
       ```
       1.可用元素选择器     :enabled
       2.不可用元素选择器   :disabled
       3.选中选择器         :checked    单选/复选框选中的元素
       4.选中选择器         :selected   下拉框选中的元素
       ```

#### DOM 操作
1. 内容操作
   ```
   1. html() : 获取/设置元素的标签体内容。 <a><font>内容</font></a>  -->  <font>内容</font>
   2. text() : 获取/设置元素的标签体纯文本内容。 <a><font>内容</font></a>  -->  内容
   3. val()  : 获取/设置元素的 value 属性值。
   ```
2. 属性操作
   ```
   1. 通用属性操作
       1. attr(): 获取/设置元素的属性
       2. removeAttr(): 删除属性
       3. prop(): 获取/设置元素的属性
       4. removeProp(): 删除属性
       * attr 和 prop 的区别？
           1. 如果操作的是元素的固有属性，建议使用prop；
           2. 如果操作的是元素自定义的属性，建议使用attr。
              var name = $("#bj").attr("name");  //获取
              $("#bj").attr("name","beijing");   //设置
   2. 对 class 属性操作
       1. addClass():    添加 class 属性
       2. removeClass(): 删除 class 属性
       3. toggleClass(): 切换 class 属性
           * toggleClass("one"):
             判断如果元素对象上存在 class="one"，则将属性值 one 删除掉；
             如果元素对象上不存在 class="one"，则添加。
   ```
3. CRUD操作
   ```
   1. append(): 父元素将子元素追加到末尾
   2. prepend():  父元素将子元素追加到开头
   3. appendTo()
   4. prependTo()
   
   5. after(): 添加元素到元素后边
   6. before(): 添加元素到元素前边
   7. insertAfter()
   8. insertBefore()
   
   9. remove(): 移除元素。  对象.remove();
   10. empty(): 清空元素的所有后代元素。 对象.remove(); //但保留当前对象以及其属性节点。
   ```

### JQuery 高级用法

#### JQuery 动画和遍历
1. 动画
   ```
   1. 三种方式显示和隐藏元素
       1. 默认显示和隐藏方式：
           1. show([speed,[easing],[fn]])
           2. hide([speed,[easing],[fn]])
           3. toggle([speed,[easing],[fn]])
       2. 滑动显示和隐藏方式：
           1. slideDown([speed,[easing],[fn]])
           2. slideUp([speed,[easing],[fn]])
           3. slideToggle([speed,[easing],[fn]])
       3. 淡入淡出显示和隐藏方式：
           1. fadeIn([speed,[easing],[fn]])
           2. fadeOut([speed,[easing],[fn]])
           3. fadeToggle([speed,[easing],[fn]])
       * 参数说明：
            1. speed: 动画速度。 slow、normal、fast 或者指定具体的毫秒数，如：1000
            2. easing: 切换效果。 swing、linear 两种可选。 默认为 swing。
            3. fn: 在动画完成时执行的函数，每个元素执行一次。 一次！！
         例： $("#showDiv").fadeOut("slow");
   ```
2. 遍历
   ```
   1. JS 的遍历方式
       * for(初始化值;循环结束条件；步长)
   2. JQ 的遍历方式
       1. jq对象.each(callback)
       2. $.each(object, [callback])
       3. for..of: jquery 3.0 版本之后才提供的方式。 （不推荐使用）
       * callback: 回调函数，function(){ }
       * 回调函数返回值：
           1. false: 如果当前 fn 返回为 false，则结束循环（break）。
           2. true: 如果当前 fn 返回为 true，则结束本次循环，继续下次循环（continue）。
      例1： citys.each(function() {
               alert(this.innerHTML);
          });
      例2： citys.each(function(index, element) {
               alert(index+":"+element.innerHTML);     // js对象
               // alert(index+":"+$(element).html());  // js转jq后，再使用
          });
      例3： $.each(citys, function(index, element) {
               alert(index+":"+$(element).html());
          });
   ```

#### JQuery 事件绑定和切换
1. jquery 标准的绑定方式
   ```
   jq对象.事件方法(回调函数);
   * 注： 如果调用事件方法，不传递回掉函数，则触发浏览器默认行为。
         如： 表达对象.submit();  //表单提交
   ```
2. on绑定事件/off解除绑定
   ```
   jq对象.on("事件名称", 回调函数);
   jq对象.off("事件名称");
   ```
3. 事件切换： toggle
   ```
   jq对象.toggle(fn1,fn2...);
   # 注意，jquery 1.9 版本后，该方法删除了。 请引入 migrate 插件来恢复该方法。
   ```

#### 插件： 增强 JQuery 的功能
1. 实现方式：
   ```
   1. $.fn.extend(object)
       * 增强通过 JQuery 获取的对象的功能。 $("#id")
   2. $.extend(object)
       * 增强 JQuery 对象自身的功能。 $/jQuery
   ```
