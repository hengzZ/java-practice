## Cascading Style Sheets 3 (CSS3)
—— 指定网页的样式和布局

基本的布局设置/绘图/动画请查看
* [start-css.md](start-css.md)
* [go-on-css.md](go-on-css.md)

一般的页面布局与式样：
* 行间距
* 页边距
* 首行缩进
* 背景
* 字体
* 边界框

高级的页面布局与式样：
* 图标/绘图
* 2D/3D 幻灯片动画

<br>

#### CSS3 的语法组成
* 选择器、属性和值： selector {property: value}
* HTML 内包含 CSS 内容时，使用 \<style type="text/css"\>\</style\> 标签包裹。
* 外连 CSS 文件时，使用 \<link rel = "stylesheet" type = "text/css" href = "stylefile.css"\> 标签。

<br>

#### HTML 元素的式样可以通过两种方式来控制
* *id* attribute <br>
```html
// id="para1"
#para1
{
text-align:center;
color:red;
}
```
注意，ID 属性只能在每个 HTML 文档中出现一次。
* *class* attribute
```html
// class="center"
.center {text-align:center;}
```

<br>

#### CSS3 的功能划分
CSS3 被拆分为 "模块"，一些最重要的 CSS3 模块如下：
* 选择器
* 盒子模型
* 背景和边框
* 文字特效
* 2D/3D转换
* 动画
* 多列布局
* 用户界面

###### reference： https://www.tutorialspoint.com/css/index.htm
