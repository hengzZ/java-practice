## 防重复提交策略
reference
* https://www.cnblogs.com/jett010/p/9056567.html
* https://blog.csdn.net/shuke_zheng/article/details/79197345

##### 为什么会出现重复提交的情况？
* 提交完表单以后，不做其他操作，此时刷新页面。 （此种刷新情况意味着刷新之前的请求，因为上一次的操作是表单提交。）
* 在提交表单时，网速较差，用户感觉没反应所以会多次点击。
* 表单提交成功后，直接点击浏览器菜单的回退，不刷新页面并再次点击提交。


##### 怎么判断是重复提交还是确实为两次内容相同的提交？
首先，为什么需要提交？ 是因为服务器端需要用户输入一定的信息。

* 那么，当服务器发起一次对用户的输入请求，用户的第一次提交是正常的，应被认为是有效提交（虽然内容不合要求）。 ``但是不合要求的话，服务器会再发出对用户的输入请求。``
* 提交之后，服务器的响应是需要时间的，此阶段客户端必定是假死状态（一般很短暂，取决于网络），任何再提交都是重复提交。 （为何？因为服务器只发起了一次请求，它只要第一次的提交！！）
* 一般等服务器完成响应之后，会跳转到其他页面。 服务器发现提交内容不符的话，会再次让用户输入的。此时又是一次新的提交。

因此，是否为重复提交是由服务器决定，与提交的内容没有半点关系。 ``这也是令牌法最被推荐的原因，因为它由服务器颁发给客户端，每一次服务器的输入需求是一个唯一的令牌。``


##### 一些防重复提交的思路
* **令牌法** （强烈推荐的方法）
  ```
  生成一个令牌保存在用户 session 中，同时要在 form 中加一个 hidden 域，用来存放令牌的值。
  每次 form 提交后重新生成一个新的令牌，是重复提交的话，令牌的值会不一致。
  （服务器返回表单页面时，会先生成一个 subToken 保存于 session，并把该 subToken 传给表单页面。）
  ```
* 禁用按钮法 （很不推荐）
  ```
  点击按钮后，按钮变成灰色。 （不推荐，因为很容易绕过这种防止重复点击的机制。）
  ```
* 使用后端的数据库内容进行唯一性判断 （太过简单粗暴，数据库压力很大）
  ```
  数据库在建表的时候，给 ID 字段添加主键约束，给用户名、邮箱、电话等字段加唯一性约束。
  此方法可以有效避免数据库重复插入相同数据。 但是，无法阻止恶意用户重复提交表单（攻击网站），
  另外，重复提交虽然不会导致重复内容存在，sql 插入语句依旧是要执行的。。服务器和数据库负载很大。
  ```
* 使用 AOP 自定义切入实现
  ```
  1. 自定义防止重复提交标记（@AvoidRepeatableCommit）。
  2. 对需要防止重复提交的 Congtroller 里的 mapping 方法加上该注解。
  3. 新增 Aspect 切入点，为 @AvoidRepeatableCommit 加入切入点。
  4. 每次提交表单时，Aspect 都会保存当前 key 到 reids（须设置过期时间）。
  5. 重复提交时 Aspect 会判断当前 redis 是否有该 key，若有则拦截。
  ```


### 后端-- 防重复提交策略方法
* 在 session 中存放一个特殊标志 （令牌法，必须用）
  ```
  在服务器端，生成一个唯一的标识符，将它存入 session，同时将它写入表单的隐藏字段中。
  用户录入信息之后点击提交，服务端会获取表单中隐藏字段的值，与 session 中的唯一标识符比较。
  （两者一致，就移除 session 中的标识符；不一致，则为重复提交（恶意提交），不处理。）
  ```
* 使用 header 函数转向
  ```
  用户提交表单，服务器端处理后立即转向其他的页面。
  这样，即使用户使用刷新键，也不会导致表单的重复提交，因为已经转向新的页面。
  （与前端开发的 PRG 模式的思路一样。 只可杜绝刷新导致的提交，无法防止延迟发生时的重复点击提交。）
  ```

### 前端-- 防重复提交策略方法
* JS 禁掉提交按钮 （强烈不推荐，就别想着用该方法）
  ```
  表单提交后使用 Javascript 使提交按钮 disable。
  ```
* 使用 Post/Redirect/Get 模式 （强烈推荐，请与令牌法一同使用。）
  ```
  在提交后，执行页面重定向，就是所谓的 Post-Redirect-Get (PRG) 模式。
  简言之，当用户提交了表单后，你去执行一个客户端的重定向，转到提交成功信息页面。
  （注意，服务器令牌法确认提交成功后，Get 获得的页面中才能显示提交成功。）
  ```

##### 注意，前端防重复提交只是为了用户交互友好，不是真正的杜绝重复提交的发生。 杜绝重复提交发生依旧要靠服务端令牌法来。

### 表单过期的处理
经常会出现如下情况： 表单填写内容不符合服务端要求（表单出错），再次回到填写页面的时候，填写的信息全部丢失的情况。

为了支持页面回跳，可以通过以下两种方法实现：
* 使用 header 头设置缓存控制头 Cache-control。
  ```
  header(‘Cache-control: private, must-revalidate’);  //支持页面回跳
  ```
* 使用 session_cache_limiter 方法。
  ```
  session_cache_limiter(‘private, must-revalidate’);  //要写在session_start方法之前
  
  //防止用户填写表单的时候，单击“提交”按钮返回时，填写内容被清除
  session_cache_limiter(‘nocache’);
  session_cache_limiter(‘private’);
  session_cache_limiter(‘public’);
  session_start();
  ```

具体的表单过期处理方法，根据框架不同查询文档实现。

#### 最后需要说明的
##### 1. 此处只是将基本原理/思路说明，具体的实现方式依框架和工具不同而有差异（思路是一样的）。
请参考开头提供的连接内容。 ``考虑到服务端的异常处理问题，可能使用如 redis 等存储中间件，而非 session 来保存上下文信息。``

##### 2. 除了重复提交，还有服务器发起用户输入请求后，别人（其他机器）冒充你去提及。。即 CSRF 的概念。
CSRF 概念：CSRF 跨站点请求伪造(Cross—Site Request Forgery)，跟 XSS 攻击一样，存在巨大的危害性。
简单说就是，攻击者盗用了你的身份，以你的名义发送恶意请求，对服务器来说这个请求是完全合法的（因为服务器是发起了一次用户提交请求。。）。
