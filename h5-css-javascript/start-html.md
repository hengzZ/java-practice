## HTML 入门
—— W3C 推荐入门教程 https://www.w3.org/MarkUp/Guide/

##### HTML 的本质
* HTML 的实质也是纯文本，不同点在于内部包含很多标签注释，当被浏览器读取的时候会附加显示特效。 HTML 的起初目的是为了文本和图片的展示呈现。
* HTML 通常被称为 “Web Pages（网页）”，网页是浏览器渲染出来的画面，并不是 HTML。 并不是只有 HTML 可以被浏览器读取并渲染。

##### “请思考当你写文档的时候通常由哪些部分组成？”

##### 一个网页的基本展示内容
* 抬头（题目）
* 小标题/段落
* 突出显示（emphasis）
* 图片
* 跳转链接
* 图表
* span 标签 （非常重要的标签）

<br>

##### 1. 抬头（题目）
* \<title\>题目 — HTML 入门\</title\>

##### 2. 小标题/段落
* \<h1\>一级标题\</h1\>
* \<h2\>二级标题\</h2\>
* \<h3\>三级标题\</h3\>
* \<h4\>四级标题\</h4\>
* \<h5\>五级标题\</h5\>
* \<h6\>六级标题\</h6\>
* \<p\>段落\</p\>

示例：
* \<h3\>桃花源记\</h3\>
* \<p\>（第 1 段） 晋太元中，武陵人捕鱼为业。缘溪行，忘路之远近。忽逢桃花林，夹岸数百步，中无杂树，芳草鲜美，落英缤纷，渔人甚异之，复前行，欲穷其林。\</p\>
* \<p\>（第 2 段） 林尽水源，便得一山，山有小口，仿佛若有光。便舍船，从口入。初极狭，才通人。复行数十步，豁然开朗。土地平旷，屋舍俨然，有良田美池桑竹之属。阡陌交通，鸡犬相闻。其中往来种作，男女衣着，悉如外人。黄发垂髫，并怡然自乐。\</p\>
* \<p\>（第 3 段） 见渔人，乃大惊，问所从来。具答之。便要还家，设酒杀鸡作食。村中闻有此人，咸来问讯。自云先世避秦时乱，率妻子邑人来此绝境，不复出焉，遂与外人间隔。问今是何世，乃不知有汉，无论魏晋。此人一一为具言所闻，皆叹惋。余人各复延至其家，皆出酒食。停数日，辞去。此中人语云：“不足为外人道也。” 既出，得其船，便扶向路，处处志之。及郡下，诣太守，说如此。太守即遣人随其往，寻向所志，遂迷，不复得路。\</p\>
* \<p\>（第 4 段） 南阳刘子骥，高尚士也，闻之，欣然规往。未果，寻病终，后遂无问津者。\</p\>

##### 3. 突出显示（emphasis）
* 请\<em\>注意\</em\>以下规则公告: ...

##### 4. 图片
* \<img src="peter.jpg" width="45%" height="45%" alt="My friend Peter"\>
* 特别提醒，GIF 属于图片格式，因此可以用 img 标签来导入。

##### 5. 跳转链接
* 文字链接 <br>
\<a href="http://www.w3.org/"\>W3C\</a\>
* 图片链接 <br>
\<a href="/"\><img src="logo.gif" alt="home page"\>\</a\>

##### 6. 图表
* 不带序号的列表 （Unordered List） <br>
\<ul\> <br>
\<li\>第一项\</li\> <br>
\<li\>第二项\</li\> <br>
\<li\>第三项\</li\> <br>
\</ul\>
* 带序号的列表 （Ordered List） <br>
\<ol\> <br>
\<li\>第一项\</li\> <br>
\<li\>第二项\</li\> <br>
\<li\>第三项\</li\> <br>
\</ol\>
* 带定义字段的列表 （Definition List - Term / Definition） <br>
\<dl\> <br>
\<dt\>第一项\</dt\> <br>
\<dd\>第一项的定义字段\</dd\> <br>
\<dt\>第二项\</dt\> <br>
\<dd\>第二项的定义字段\</dd\> <br>
\<dt\>第三项\</dt\> <br>
\<dd\>第三项的定义字段\</dd\> <br>
\</dl\>

##### 7. span 标签 （非常重要的标签）
\<span\>\</span\> 标签普遍是用于修改普通文本中的一部分内容的样式控制。

例如： ``你好\<span\>Zhiheng\</span\>.`` 使我们可以只控制指定内容的式样，而不会影响文本的排版。

<br>

#### 特别注意
* 每个 HTML 文件由唯一的一个 \<html\>\</html\> 包裹。
* \<html\>\</html\> 内包含唯一的 \<head\>\</head\> 和 \<body\>\</body\>。
