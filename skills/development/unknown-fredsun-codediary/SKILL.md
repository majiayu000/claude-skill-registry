---
name: unknown
description: 1. imageloader 的话自己怎么设计这个功能
---

1. imageloader 的话自己怎么设计这个功能
2. 算法 链表翻转 异或取数组中的不同数
3. 大 json 的传输
  * 解决:
      * Gson提供了数据，不要用String()就行
        ```
        Gson gson = new Gson();
        Reader reader = new FileReader("/path/to/file");
        YourBean bean = gson.fromJson(reader,YourBean.class);
        ```
      * 或使用 Fastjson [链接](https://github.com/alibaba/fastjson)
      * 不推荐,application添加```largeheap="true"```，能缓解部分机型
* 网络提交数据时网络不好的情况怎么处理
5. 即时系统什么鬼
6. 设计模式的几种大的分类
7. 微信，支付宝支付需要准备的参数
8. 锁屏和锁屏30秒发生了什么
9. gzip炸弹
10. imageview包含context的回掉
11. [单例实战](https://github.com/guolindev/booksource/issues/5)
12. leak canavy
13. 主语从句 状语从句

15. 微博全景图PanoramaImageDetailView, 图片只是ImageView
16. DialogFragment + 动画方向 = 弹出页面带阴影
17. builder模式
```
public class MyBuilder{
    private int id;
    private String num;
    public MyData build(){
        MyData d=new MyData();
        d.setId(id);
        d.setNum(num);
        return t;
    }
    public MyBuilder setId(int id){
        this.id=id;
        return this;
    }
    public MyBuilder setNum(String num){
        this.num=num;
        return this;
    }

}

public class Test{
    public static void  main(String[] args){
        MyData d=new MyBuilder().setId(10).setNum("hc").build();
    }

}
```

阿里
https://www.nowcoder.com/discuss/30553?type=2&order=3&pos=9&page=1

https://www.nowcoder.com/discuss/29609?type=2&order=3&pos=10&page=1

https://www.nowcoder.com/discuss/30334?type=2&order=3&pos=8&page=1

17. 上下文究竟是什么, 为什么可以在onAttach中强转成implements过的 Listener
18. ActivityOptionsCompat
20. service
21. Robolectric
22. new SpannableString(" " + position);
23. DialogFragment和popupwindows，以及遮罩
24. 一天一题day3搞定
  * 第 1 天
  * 第 2 天
  * ~~第 3 天 Activity生命周期~~
  * ~~第 4 天 如何判断Activity是否在运行~~
  * 第 5 天
  * 第 6 天
  * ~~第 7 天 Java的值传递和引用传递~~
  * 第 8 天
  * ~~第 9 天 Parcelable和Serializable~~
  * ~~第 10 天 context~~
  * 第 11 天
  * 第 12 天
  * 第 13 天
  * 第 14 天
  * 第 15 天
  * 第 16 天
  * 第 17 天
  * 第 18 天
  * 第 19 天
  * 第 20 天
  * 第 21 天
  * 第 22 天
  * 第 23 天
  * 第 24 天
  * 第 25 天
  * 第 26 天
  * 第 27 天
  * 第 28 天
  * 第 29 天
  * 第 30 天
  * 第 31 天
  * 第 32 天
  * 第 33 天
  * 第 34 天
  * 第 35 天
  * 第 36 天
  * 第 37 天
  * 第 38 天
  * 第 39 天
  * 第 40 天
  * 第 41 天
  * 第 42 天
  * 第 43 天
  * 第 44 天
  * 第 45 天

* IntentService
26. 监听home键
27. 锁屏查看专车进度
28. 前端广告不错的例子[adblock下不一样的效果](http://www.nowamagic.net/academy/detail/50161533)\
29. 微信朋友圈清掉了exif信息,
30. 微博通知打开的界面, 任务列表看不见 MainTabActivity
* android:excludeFromRecents="true" 让后台的activity看不见
* 但是微博在activity在嵌套的时候按任务列表键也看不见, 为什么
31. 插件开发
32. 浏览器打开app
33. singleton
34. 反射会拿到单例的private方法
35. android现在是5层不是4层
36. remote view
37. 白屏时间 firstPaint = 开始解析dom的耗时, domReadyTime 用户可操作时间
38. getMetrics
39. broadcast 跨进程?
40. Toast没焦点
41. IBinder可以传递哪些类型
42. post runnanble 到主线程, 通常post 一个 handler , 如果有view可以view.post
43. TouchDelegate 扩大点击面积[http://blog.csdn.net/fishle123/article/details/50809872]
44. ```Expected BEGIN_ARRAY but was BEGIN_OBJECT at line 1 column 2 path```期待的数组，结果返回的是Object
45. 圆角
46. 多点触控
如果 3 个指头同时向下滑动，3 个指头的速度如果有偏差该怎么办，用什么办法来确定这个监听事件
47. String 为什么要设计成不可变的？
* oracle 想造出一个常量
* 确保线程安全, 可变的自有StringBuilder.即使 private final [] 也只是不可变地址, 元素还是可变的. final 只是防止被创建出子类后被重写方法
* 字符串池可以防止重复创建

48. Activity 上有 Dialog 的时候按 home 键时的生命周期
49. fragment 各种情况下的生命周期
50. 横竖屏切换的时候，Activity 各种情况下的生命周期
51. Application 和 Activity 的 context 对象的区别
52. 链表逆序
53. 求二叉树两个节点最短路径
54. 序列化的作用，以及 Android 两种序列化的区别
55. List 和 Map 的实现方式以及存储方式

57. 线程如何关闭，以及如何防止线程的内存泄漏
58. Linux 的一些常用指令
59. ANR
60. SurfaceView
61. OpenGL
62. OkHttp
63. HttpURLConnection
64. Android 系统的启动过程
65. RxJava 如何管理生命周期
66. 图片缓存策略
67. Okio 源码
68. OkHttp 中和 WebView 中 Cookie 是怎么处理的
69. Android 上 Socket 的使用
70. 注解
71. Android 上的进程通信、共享内存问题
72. Webp 格式
73. 内存泄漏的根本原因
* static 还拿着对象的引用, 无法被释放如 view.post时用的是静态线程池
74. 举出几种 HashMap 的迭代方式
75. 数据库 SQLite 的一些操作。
76. 抽象类和接口(abstract 和 interface 区别)
  * 抽象类是对根源的抽象, 接口是对方法的抽象
  * 抽象类是像xxx一样, 接口是能xxx.
  * 接口可以写方法, default 或 static 标识一下
76. 闭包
  * 对象是带方法的数据, 闭包是带(外部)数据的方法
  * final 修饰过的局部变量会被复制一份, 即使本身跟对象销毁了, 内部类还是能用到复制品, 因为final修饰过的变量数值不会变, 所以就好像原局部变量的生命周期被延长一样, 这就是java的闭包
76. 静态内部类和内部类的区别
* 静态内部类不持有外部类的引用, 所以无法调用外部类的非 static 的变量和方法
* 匿名内部类, 没"=", 直接 new XXX(){}, 完成了java的闭包
* 降低类的深度，方便类的使用，
77. 堆内存和栈内存的区别
78. 弱引用软引用区别
79. Serializable 和 Parcelable 的区别
80. ListView 的实现原理
81. Java 中同步方法
82. 非主线程更新 UI 的可能性
83. Freeline 插件提升编译速度
84. Overview 查看任务列表 ，标题怎么修改
85. ids是 [from](http://seniorzhai.github.io/2014/07/17/%E9%9D%9E%E5%B8%B8%E8%A7%81Android%E9%A1%B9%E7%9B%AE%E6%96%87%E4%BB%B6/#arrays-xml)
    自定义的xml文件, android 需要对view设置唯一的标志ID来区分, 自定义空间的命名
    ```‘css’
    <?xml version="1.0" encoding="utf-8"?>
    <resources>
        <item name="card_layout" type="id"/>
        <item name="card_actionarea" type="id"/>
        <item name="card_contentarea" type="id"/>
        <item name="card_title" type="id"/>
        <item name="card_content" type="id"/>
        <item name="card_overlay" type="id"/>
    </resources>
    ```

87. Listview 和 ScrillView冲突
88. StringBuilder的优势(为止长度的字符串才考虑sb).java9使用 makeconcatwithconstants
  * StringBuilder.subString 是 copy 后新建 String 对象
  * String.subString 是在原对象上修改 offset
89. 字面量
90. 知乎上了的三方CameraKit, FloatingActionButton
91. -10<x<10和Math.abs(x)<10
92. animator is Running?
93. androidstudio set up jdk
    解决方案: Invalidate Caches and Restart
94. activity的finish()方法并不会立即执行, 即使最简单的activity都会执行完oncreate后才z执行

95. .nomedia(https://zmywly8866.github.io/2016/05/05/android-disable-mediascanner-folders.html)
96. ScrollView撑满全屏: fillViewport
97. switch和多重if的区别
98. persistentHead Drawer
99. 珊瑚虫修改pe结构,注入器加载[github](https://github.com/JuncoJet/unlimited-landeng-for-win)
100. equals, ==,hashCode.
== 比较对象时看引用地址.
equals()是交给开发者去覆写的, String.equals() 覆写了 object 的 equals()
所以.字符串和对象比较用equals(), 但要 **注意equals()前的变量是否为空**
101. TextUtils.isEmpty
TextUtils.isEmpty(): if (str == null || str.length() == 0)
String.isEmpty(): return count == 0

102. try catch finally[参考](https://jun6.net/java-try-catch-finally/)
1. 先执行try中的return 后的表达式, 并隐性返回(如返回String的地址, 类的地址, 但若return 套了 return 先不执行后一个return),
2. 再执行 finally
3. 最后把 try 的 return 显性执行(),(执行完之前的 return 里的 return)

103. DecorView 的布局
104. windowIsTranslucent 设置true, ActivityA 跳到 ActivityB, A的onStop会不走
105. String indexOf 从第0位开始算
106. substring(start, end), 左闭右开
107. path 绘制 Rect 时无法设置起点, 只能用 line 拼接
108. bitmap 和 drawable
    * public abstract class Drawable
    * public final class Bitmap implements Parcelable
    * public class BitmapDrawable extends Drawable
    * bitmap 存储像素信息, Drawable 存储的是 canvas 的一系列操作, BitmapDrawable 是把 bitmap 渲染到 Drawable 上.
    * 前者重数据, 后者重行为
    * BitmapDrawable(Resources res, Bitmap bimap), 传入的res 用于获取屏幕密度, 非必须

109. 屏幕适配
    * 屏幕尺寸: 屏幕的对角线, 单位:英寸inch, 如5
    * px: 屏幕上横向和纵向的像素, 400X800, 宽高的单位,  px = density * dp
    * density = dpi/160, DisplayMetrics.density
    * px = dp * dpi/160
    * dpi: dots per inch, 像素密度, 每英寸像素点数 = DisplayMetrics.densityDpi = 根号下(宽平方+高平方) /屏幕尺寸
    * dp/dip: 设备独立像素, dpi=160的屏幕上, 1dp = 1px. -> dip = (dpi/160) * px

110. Recyclerview 不走 onCreateViewHolder/onBindViewHolder
  * getItemCount <= 0
  * 没设置LayoutManager
  * 被 ScrollView 嵌套(<25版本可能出现)
111. 数组转List: Arrays.asList(a[]);
112. get 和 post
  * http 协议并未限制 get/post 请求长度, 是浏览器限制的, 而且限制的不是请求参数, 而是 uri 整体长度, 若超出服务器会截断或者 414.
    * 浏览器
      * IE和Safari 俗称2K+53, 2083字符
      * Chrome 俗称8K, 8182Byte
    * 服务器
      * Apache 8192Byte
      * IIS 16384Byte
      * Perl HTTP::Daemon 8000Byte
      * ngnix 1k 或者4k/8k
113. Activity 和 Fragment 区别
  * 引入时间: 3.0 才引入Fragment
  * 创建: xml
  * 打开: Intent/加入FragmentManager
  * 父类: ContextThemeWrapper/Object
  * 管理: ActivityManager/FragmentManager
  * 共同: 都响应 callback,
  * 区域: window 和 contentView
114. 集合(Collection) 和数组(Array)的区别
  * 1. 集合长度可变, 数组是静态的,长度固定
  * 2. 集合只能存对象, 数组还可存储基本数据类型
  * 3. 集合可以存多种类型数据(Object的子类们), 数组只能存一种.
  * 相同: 存的都是地址
115. 集合
  * 数组 Array: 因为存储在连续的内存, 可直接通过下标访问, 且访问速度非常快
  * Iterable 接口
    * AbstractCollection 接口
    * AbstractList 抽象类
    * Collection 接口
      * List 接口, 可重复. (为解决ArrayList类型不安全和装箱而定, 推出了泛型,并在创建时固定类型)
        * ArrayList, 底层是数组结构, 内存地址连续 -> 查询快, 插入删除慢(为解决数组固定大小和插入类型相同而生, 但把所有插入类型都当作Object处理导致的自动装箱拆箱, 产生新的引用对象, 会有时间损耗)
        * LinkedList, 底层是链表结构, 内存地址任意 -> 增删容易. 移动指针 -> 查询慢, 必须从头节点开始一个个遍历 . (上一个元素指向下一个元素, 所以内存地址可能不连续)
        * Vector, 底层是数组结构, 线程安全, 单线程慢, 被 ArrayList 替代
      * Set, 不可重复, 必须定义 equals, 查询慢, 增删快, 增删不会引起元素位置改变. 存放根据hash值
        * TreeSet, 底层是二叉树, 有序
        * HashSet, 无序
  * Map, <key, value>的映射关系, key 不重复
    * HashTable, 底层是哈希表, 不可存 null, 线程安全, 单线程慢, 已被 ConcurrentHashMap 替代
    * HashMap, 底层是哈希表, 可存 null(hashCode设为0而已), 为了快速查找而设计的.
      * LinkedHashMap, 通过维持一个双向链表, 保证插入排序[参考TODO](https://blog.csdn.net/justloveyou_/article/details/71713781)
    * TreeMap, 底层是二叉树, 自动排序, 为了排序而设计
  * Queue, 先进先出, FIFO[参考](https://blog.csdn.net/qiaoquan3/article/details/51380992)
  * Stack, 后进先出, LIFO

116. 哈希
* hash: 就是把任意长度的输入(又叫做预映射pre-image), 通过 **散列算法**, 变成固定长度的输出(int), 该输出就是散列值.
    这种转换是有一种压缩映射, 也就是说, 散列值的空间远小于输入值. 所以容易出现重复散列值(碰撞)
    * 应用 - 哈希表:数据结构中, 数组 - 寻址容易, 插入删除困难. 链表 - 寻址困难, 插入删除容易. 那么有没有寻址容易, 插入删除也容易的数据结构? 哈希表
  * 哈希表: 实现方法很多, 最常用的"链表法" -> 存储链表的数组(就是HashMap).根据元素特征计算元素的数组下标的方法就是 **散列法**
* hashCode Object 类针对不同的对象返回不同的整数(对象的内存地址转换成整数)
* java 中 Collection 分三类:List, Queue, Set. 前两个元素有序, 可重复. 最后一个元素 **无序**, 不可重复. 保证元素不重复用到的判断 Object.equals.
  * 不可重复的集合存入数据的步骤:
  * 1. 计算传进来的元素的hashCode, 找到数组里的位置, 位置上没数据, 直接存
  * 2. 位置上有数据, 调用 equals() 比较, 相同就跳过, 不同就存(Java中HashSet, HashMap, HashTable的实现是放在表头)
* hashCode, 系统用来 **快速** 检测两个对象是否一致[参考](https://blog.csdn.net/justloveyou_/article/details/52464440)
来自于 public native int hashCode();
同一个类没被回收时, hashCode 保持一致
同一个类被再次创建(如 DialogFragment 再次打开), 即使此刻app活着, hashCode 依然改变
* 散列法
  * 容量, 哈希表中桶的大小(table数组的大小), 为2的n次方.
  * 负载因子, 用于衡量散列表的空间的使用程度(使用到了多少%开始扩容), 默认0.75
  * 哈希表扩容时, 阈值 = 容量 * 负载因子
  * 对于拉链法的哈希表, 查找一个元素的平均时间时间 O(1+a), a 是链表长度.
    * 特别的, 若负载因子越大, 那么, 对空间利用越充分, 查找效率也越低
    * 若负载因子越小, 那么, 对空间造成的浪费越严重. 所以默认的0.75是这种, 不需要去改
* 发生碰撞:
  * open hashing, 单独链表法, 将散列到同一个存储位置的所有元素保存在一个链表.
    实现时一种策略是散列表同一位置的冲突都放进一个栈, 新元素放在前端还是后端取决于怎么方便
  * close hashing = opened address, 开地址法, 继续找, 找到空的位置
*
* HashMap, 在计算出hash值后
  * put时,数据尽量均匀分布以便于查找, 于是想到取模, 但是取模消耗太大, 于是
  ```
  static int indexFor(int h, int length) {
        return h & (length-1);
  }
  ```
  这样做的好处是相当于取模且效率高于取模.
  同时容量为2的n次方的原因也是这个.
  当 length = 15时, length - 1 = 14
  h | length-1 | h&lengeh-1 |result
  --|--|--|--
  0|14|0000 & 1110 = 0000|0
  0|14|0001 & 1110 = 0000|0
  0|14|0010 & 1110 = 0010|2
  0|14|0011 & 1110 = 0010|2
  0|14|0100 & 1110 = 0100|4
  0|14|0101 & 1110 = 0100|4
  0|14|0110 & 1110 = 0110|6
  0|14|0111 & 1110 = 0110|6
  0|14|1000 & 1110 = 1000|8
  0|14|1001 & 1110 = 1000|8
  0|14|1010 & 1110 = 1010|10
  0|14|1011 & 1110 = 1010|10
  0|14|1100 & 1110 = 1100|12
  0|14|1101 & 1110 = 1100|12
  0|14|1110 & 1110 = 1110|14
  0|14|1111 & 1110 = 1110|14
  共发生了 8 次碰撞, 空间的浪费也是一半, 而选择 2 的 n 次方作为 length 时, 不容易发生碰撞
  * HashMap 数据唯一, 因为 put 迭代时 key 相同则覆盖.

117. 时间复杂度(链接)[https://www.zhihu.com/question/37381035]
* 有序列表
  * 查找 O(N)
  * 插入 O(1)
* 有序数组
  * 查找 O(1)
  * 插入 O(N)
118. 反射, 运行时获取一个类的全部方法和属性[参考](http://www.cnblogs.com/sunxlfree1206/p/4735453.html)
  * 获取类
    * 类名.class
    * 对象.getClass
    * Class.forName("包名.类名");
  * 获取构造函数
    * class.getConstructor后con.newInstance(...);
  * 获取成员变量
  ```
  Field[] fields = obj.getClass().getFields();
  for(Field field :fields){
     if(field.getType()==AAA.class){
       AAA oldValue = (AAA)field.get(obj);
     }

  }
  ```
  * 获取方法
    * Method method = class.getMethod("name", Class);
    * method.invoke(isStatic, ...);
119. 瘦身
* 没用到的资源检查
* 图片png(tinypng压缩)->jpg(可能失真)->Webp
* 删arm-v7包的so
* 微信的AndResGuard
* proguard深度混淆
* proguard去符号表
* 图片在线拉
* 去重复库
* 使用更小的库
* 删掉x86包

120. 排序
* 选择排序, 最大的和最右边的交换, O(n^2)
* 冒泡排序, 相邻的大的交换(优点：若本身排好序，直接遍历完不交换就结束了), O(n^2)
* 快速排序, O(nlgn)

121. Material Design
* 动作真实, 默认Animator的先加速后减速
* 响应式交互
  * 触控涟漪, android:colorControlHighlight, android:colorButtonNormal, ?android:attr/selectableItemBackground(有界涟漪), ?android:attr/selectableItemBackgroundBorderless(无界涟漪), 或者自定义<ripple>
* 揭露动画, ViewAnimationUtils.createCircularReveal()
* 曲线运动, 动画的插值器可自定义速度, 贝塞尔曲线
* 动画集


122. 算法
* 完数
* 斐波那契


123. 定位
* 定位权限组织的是,gps/蜂窝数据对定位的获取, 关闭定位权限后获取位置,wifiInfo().getBSSID();
* TODO 蓝牙, 磁场, 室内定位

123. Gradle
* 生命周期
  * 初始化阶段: 读取setting.gradle 中 include 信息, 决定有哪些工程加入构建
    include 'app', 'moduleA'
  * 配置阶段: 执行所有工程的 build.gradle 脚本. 配置 project 对象(即配置task).
    task hello{
      println "hello"
    }
  * 运行阶段: 根据传递来的 task 名称, 执行相关 task
    task hello{
      doLast{
        println "dolast"
      }
    }
* 抽出脚本后 apply from 'other.gradle'即可

124. Http, tcp/ip, socket
* Http
  * 应用层, 基于TCP/IP通信协议来传递数据
  * 简单快速, 请求时只传送请求方法和路径
  * 灵活, HTTP允许传输任意类型数据
  * 无连接
  * 无状态
  * 明文传输
  * 支持B/S, C/S.
  * URL:http://www.baidu.com:80/news/info/list/index.jsp?ID=111&name=222
    * "http:" 协议部分
    * "www.baidu.com" 域名部分
    * ":80" 端口部分, 省略则默认, 8080 用来代理, 1080 是socks
    * "/news/info/list/" 虚拟目录部分, 域名中的第一个 "/" 到最后一个 "/",
    * "index.jsp" 文件名部分, 最后一个 "/" 到 "?"/"#", 如果都没有, 则到路径最后
    * "#xxx" 锚部分.
    * "?ID=111&name=222" 参数部分, 从 "?" 到 "#".
  * ip是大马路, tcp是客车, http是乘客, 一个承载在另一个基础之上
  * 寄快递例子:[Ref:知乎](https://www.zhihu.com/question/38648948)
    * http客户端寄信两个物品给http服务端, tcp快递公司保证数据按序送达和丢失重传, ip负责查出地址和目的地的导航

125. ContentProvider 和 sql 区别
* ContentProvider 对数据共享不同app间访问
* ContentProvider 可操作包括sql,sp,file.
* ContentProvider 对外界隐藏了数据库的结构
* ContentProvider 结构
  * ContentProvider 关联CRUD
  * ContentResolver 用于获取另一个 app的数据
  * ContentObserver 另一个 app 监听数据变化

126. 静态锁和非静态锁
  * 静态锁锁类, 非静态锁锁对象, 每个对象都有一个锁
  * 所以调用同一个类是静态锁互斥, 同一个对象的非静态锁互斥, 但非静态

127. 多线程
  * 继承 Thread 或者实现 Runnable, 或实现Callable(可用Future接收)
  * 线程阻塞
    * sleep, 可被 interrupt
    * wait, 可被 interrupt
    * io
    * synchronized
  * 线程同步
    * synchronized
    * volatile
    * 并发包里的 ReentrantLock 重入锁
    * ThreadLocal
    * 阻塞队列
    * 原子变量
  * 死锁
    * 条件
      * 互斥
      * 不可抢占
      * 请求和保持
      * 循环等待
127. 线程 sleep() 和 wait(), yield()
  * Java的多线程是一种抢占机制, 而不是分时机制, 抢占式的机制是有多个线程处于可运行状态, 但是只有一个线程在运行.
  * 相同:
    * 都可以被 Thread.interrupt() 打断, 如线程A希望终止线程B.但必须B处于wait()/sleep()/join()状态, 并立刻抛出 InterruptedException. 如果B并不在这些状态, 则只是B的标识位被修改, 线程继续执行
  * 任何位置都能 sleep, wait 只能在 synchrinized
  * synchronized 代码段被线程执行时需要运行权限, 一个synchronized 只有一个钥匙.如果被其他线程拿走了, 只能等(线程阻塞)
  * sleep() Thread 里的静态方法, 不能改变对象的机锁. 当 synchronized 调用了 sleep(), 线程进入了休眠, 其他线程无法访问这个对象, 以及对象的锁. 但是依然保持监管状态
  * wait() Object 类里的方法(final 修饰的 native 方法). 当一个线程执行到 wait() 方法时, 就会进入到一个等待池, 同时释放对象的机锁, 使得其他线程能够访问, 可以通过 notify, notifyAll 方法来唤醒等待的线程.
  * yield() 让当前线程暂时放弃CPU, 但不会进入状态. 各厂商做法不同

128. ThreadLocal
  * synchronized 时间换空间, 为了共享数据, ThreadLocal 空间换时间, 为了保护数据
  * Looper 就是通过ThreadLocal<Looper> 实现每个线程只有一个Looper.
  * 存入 ThreadLocal 里的变量存入了线程的 ThreadLocalMap, 不过 ThreadLocalMap 还是属于线程的实例所有, 所以还是存在了堆内存, 只是一些技巧改成了线程可见.
  * 并不会内存泄漏, 因为 ThreadLocalMap 里存的是弱饮用

128. 抽象工厂模式
```
public interface A{

}
public interface B{

}
public interface C{
  public A a();
  public B b();
}
```
实现C的类们

129. 子线程更新UI
* Actvity.runOnUiThread();(通过线程合并join()实现)
* Handler();
* view.post[参考](https://blog.csdn.net/scnuxisan225/article/details/49815269)
  * 原理: attachToWindow 后直接 UI 线程的 handler 发送 Runnable.
        如果没 attach上 , 则塞进 ViewRootImpl 的 RunQueue 等到下一次 performTraversals
        如果下次 performTraversals 时仍未 attach 上, 则 Runnable 里的内容不会被执行(bug)
  * 内存泄漏: 当view在子线程里post一个runnable, 恰好还没执行 attachToWindow, 此时RunQueue被当前线程暂时持有, 而当前线程又是一个静态线程(常规线程池都是), 而调用的又是一直在线程池的核心线程, 此时调用 post 方法又不是 application.context 而是 new View(Mainactivity.this).post, 会变成一直存在的线程持有Activity的上下文而内存泄漏.
  * 版本: 4.4-5.2 执行子线程更新 ui 时会出现. 6.0 修复

130. 布局优化
  * <include>
  * <merge>
  * viewstub(此时不能merge)

131. Android 签名
  * 开发者身份确认, 确保升级
  * 对包中每个文件处理, 确保不被替换
  * 相同签名证书 app 数据共享.

132. ANR 时间（ActivityManagerService.java 中定义）
  * BroadcastReceiver.onReceive()超过 10S
  * 按键 5S
  * Service前后台 20/200
  * 调用线程的锁导致主线程一直等待

133. 向上转型, 向下转型
  * 向上转型
  ```
  Animal a = new Bird();
  a.eat();
  ```
  或一个接口的参数要求父类, 也可以穿进去子类
  * 向下转型
  ```
  Animal a = new Bird();
  Bird b = (Bird)a;
  b.fly();
  ```
  * 向下转型的类型不安全 -> 泛型
134. XML 解析
  * PULL Android内置, 类似SAX, 但是SAX靠回调, PULL 靠自身出发
  * SAX 事件驱动的流式解析,
  * DOM 来自html, 全部加载后逐句解析, 随机访问

135. Exception 和 Error
  * Eoor JVM 无法预期的错误, 属于 JVM 层次
  * Exception 分为运行时和检查时, 编译通过运行出问题和必须 try...catch
  * 都是 Throwable 子类

136. GC
  * 常规 GC 算法
    * 标记回收 Mark ans Sweep GC
    * 复制 Copying, 快, 空间换时间, 空间分一半, 再移动
    * 标记-压缩算法 Mark-Compact
  * 分代 年轻代用复制, 老年代用标记压缩
  * Dalvik 
    GC 算法是 Mark-Sweep.
    * 过程
      * 遍历堆地址空间,此时是第一次 STW
      * Mark: 从根据对象开始标记引用对象, STW 两次
      * Sweep: 回收没有被标记的对象占的内存.
    * Mark 用到的数据结构是 heap bitmap. 分为两种
      * live bitmap
        标记上一次没被回收的对象
      * mark bitmap.
        标记当前GC有被引用的对象
      因此需要被回收的对象就是live bitmap 为1, 而 mark bitmap 为0的.
    * mark 阶段再分为两个
      * 标记根集对象阶段
        此时必触发 STW, mark全局变量, 栈变量, 寄存器等引用的对象
      * 标记根集对象的引用对象阶段

     GC阶段必须stw一次, 防止刚还有引用的对象突然又没了引用. 为了减少stw, 引入了并行的垃圾回收算法 Concurrent GC. ART还并行处理GC

137. 内存泄漏和内存溢出以及OOM
  * 内存泄漏 Resources Leak
    内存申请后使用完没有释放导致一直持有
  * 内存溢出=内存越界 overflow
    一次性申请过大内存导致内存不够,
  * 优化
    * SparseArray 代替 HashMap, HashMap<Integer, Object>, 一个排序好的数组, 默认大小10, 折半查找,


138. String
  * String a = "aaa"; //字面量创建, 编译期就被确定了, 存入常量池
  * String b = "a"+"a"+"a"; //编译器就被解析为a一样的字面量
  * String c = new String("aaa"); // 通过 new 关键字按照一般对象创建, 不会放入常量池.
  * String d = "a" + new String("aa"); //编译期无法创建new String, 所以还是一般对象
  * String s2 = String.intern(); //在运行时去常量池找是否有相同 Unicode 的字面量常量,没有就把str复制后放进常量池. 1.7不复制, 放进对中str对象的引用

  * intern()在 jdk 1.6 和 1.7 的改变
    * 1.6
      把首次遇到时复制字符串对象进字符串池, 并返回引用
      因为字符串池在PermGen, 内存大小需在虚拟机启动前固定
    * 1.7
    * 字符串池中没该str的unicode, 把堆中str的引用返回
      把首次遇到的字符串对象的引用添加进字符串池, 并返回此引用
      如果字符串池中已经, 则返回字符串池中的引用
      字符串池在堆
    * "abc" //直接在字符串池建, 池中有或者有引用(intern进来的)都直接返回
    * new String("a")+new String("bc"); //在堆内存建, 然后返回引用
    * str.intern();//Java7下, 先看常量池里有这个字符串不, 没有, 把堆里这个串的引用丢进常量池. 有, 就返回这个串的引用.
    * 所以之后相同内容的字符串再 str.intern() 时, 返回的就是第一次 intern 进去的地址.也就是说 str2.intern() == str1
    * TODO 如果是str1 = new String("abc"), 或者str1 = new StringBuilder("a").append("bc"); 结果会相反

     数值 | constant pool
     a| a
  * “abc”; constant pool 里有
  * new String("abc"); constant pool 里有
  * new StringBuilder; 单纯的, constant pool 里有, 如果多了append(), constant pool 里就没有.
  * new String("a")+new String("bc"); constant pool里没有!(new String + new String 会被翻译成 new StringBuilder)
  * str.intern == str //当且仅当之前没有""和 new String("")相同内容时

  * intern 移入的不是 constant pool


139. TCP 拥塞机制和流量控制[参考](https://blog.csdn.net/chenchaofuck1/article/details/51995590)
  * 流量控制
    发送方速度不要太快, 滑动窗口实现,
    * 窗口 缓冲区, 窗口是数据段范围, 缓冲一定范围内的数据段
      * 接收端窗口 rwnd
      * 拥塞窗口 cwnd(congestion window)
      * 发送窗口 swnd
      * 最大报文段长度 MSS
  * 拥塞避免
    防止网络拥塞时数据大量丢失
    * 慢开始
      * swnd = 1, cwnd 从 MSS 开始, 每收到一个ACK后最大增多一个MSS报文段, 指数增长
      * 当 cwnd 达到 ssthresh 时, 开始拥塞避免算法, swnd 线性增长
      * 当发生拥塞,  ssthresh = swnd/2 (这是乘法减小算法)
      * swnd = 1 从头开始
    * 快重传, 快恢复
      * 快重传, 一连收到3个ACK, 确认报文丢失, 立刻重传丢失报文段
      * 快恢复, 一连收到3个ACK, 设置慢开始门限ssthresh.
        swnd = ssthresh + 3 * MSS
        cwnd = ssthresh + n * MSS
        若允许发送报文段则继续拥塞避免算法发送,
        若收到新报文段的 ACK, 将 swnd 缩小到 ssthresh

140. CoordinatorLayout
  * 把 RecyclerView, SwipeRefreshLayout, NestedScrollView 的 onTouchEvent 里的事件通过 NestedScrollingChildHelper 传递给 behavior, ViewParentCompat 或接口 NestedScrollingParent.
  * CoordinatorLayout 实现了接口 NestedScrollingParent
  * ViewParentCompat
    * 22, 5.1 加入
    * 提供 onNestXXX()
141. settext 勿set进int, 会去资源文件里找
142. JDK
  * Android Studio 2.2 开始自带 OpenJDK
143. ART[参考](https://github.com/ZhaoKaiQiang/AndroidDifficultAnalysis/blob/master/10.ART%E3%80%81JIT%E3%80%81AOT%E3%80%81Dalvik%E4%B9%8B%E9%97%B4%E6%9C%89%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB%EF%BC%9F.md)
  * Kitkat4.4 引入, 可切换, 5.0 设为默认特性, 主要特征是 ART 解释器.
  * ART(Android Run Time) 是一种 AOT 编译器, 在运行前就把中间代码编译成本地代码. 安装慢, 占用空间, 但是执行时省电, 而老版本的 JIT 是运行时动态编译,
    * 区别
      * JIT(Just In Time Compiler) 2.2提出, 即时编译技术, 运行时编译, 运行慢
      * AOT(Ahead Of Time) 安装时不做编译, 而是解释字节码, 变成本地机器码, 所以运行快. 但是消耗的空间会更多, 最多不超过应用代码包的20%.
      * 字节码, java代码被编译成字节码, 在JVM运行, JVM 再传给机器
      * 机器码, c代码被编译成机器码, 直接操作CPU

  * android打包流程:
    Java 编译器将所有 Java 文件编译为 class 文件
    dx工具将 class 文件转为 dex 字节码, 即 dex 文件
    之后签名, 对齐, 变为 APK(APK中包含dex文件)
    Dalvik 可以看作 JVM, 负责将dex文件解释为机器码, 如果不做处理, 每次都需要将 dex 代码编译成微处理器指令, 效率不高.
    于是2.2加入了 JIT, 当 App 运行时, 每当遇到一个新类, JIT 会对这个类进行编译, 编译后的代码会被优化为相当精简的原生型指令码, 这样下次执行相同逻辑时会更快
    当然编译也是花时间的, 如果执行次数很少, 编译花的时间可能还比执行多, 所以谷歌没对所有代码编译, 只编译执行次数较多的代码为本地机器码, 但是弊端仍然是 dex 编译为机器码需要耗费时间
    同样, JIT 编译发生在 app 运行时, 所以每次打开 app 时, 都需要 JIT 编译
    5.0 开始默认的 AOT, 第一次安装时dex字节码就全部编译成机器码存在了本地, 每次运行时也不需要编译, 直接读取本地机器码,
  * Android 4.x(Interpreter + JIT)[参考](https://www.zhihu.com/question/55652975)
    * 原理: 平时代码走解释器, 但热点 trace 会执行JIT进行及时编译
    * 优点: 占用内存少
    * 缺点: 耗电(下次打开还得编译), 卡顿(JIT编译时)
  * Android 5.0/5.1/6.0(Interpreter + AOT)
    * 原理: 安装时完成所有的编译(字节码->机器码)
    * 优点: 性能好, 运行时快
    * 缺点: APP安装时间长, 内存占用多.
  * Android 7.0/7.1 Hybrid(Interpreter + JIT + AOT)
    * 原理:
      * 安装时不编译, 安装速度快.
      * 运行时先走解释器, 热点trace被识别, 并被 JIT 编译, 存储在 jit code cache, 并产生 profile 文件
      * 等手机进入 charging 和 idle 状态, 系统每隔一段时间扫描 profile 文件, 并执行AOT编译(官方称之为 profile-guided compilation)
      * 不管是 JIT 还是 AOT 编译的 binary code, 最后都是 optimizing compiler 编译, 差别不大
      * 所以前几次执行会比较慢, 但是越用越快.
      * 也可以称之为 All Of the Time compilation
144. 为何 Intent 传递数据是 Bundle 而不是 HashMap[参考](https://github.com/ZhaoKaiQiang/AndroidDifficultAnalysis/blob/master/02.Android%E4%B8%BA%E4%BB%80%E4%B9%88%E8%A6%81%E8%AE%BE%E8%AE%A1%E5%87%BABundle%E8%80%8C%E4%B8%8D%E6%98%AF%E7%9B%B4%E6%8E%A5%E4%BD%BF%E7%94%A8HashMap%E6%9D%A5%E8%BF%9B%E8%A1%8C%E6%95%B0%E6%8D%AE%E4%BC%A0%E9%80%92.md)
  * Intent 传递的数据量一般不会很多.
  * Bundle内部是ArrayMap里的两个数组, 一个数据对应的下标, 一个存key,value. 内部使用二分法对 key 排序.所以CRUD也是二分法查找, 适合小数据量, 而大数据量时性能将退化. HashMap时数组+链表, 而数据量少时, HashMap 的 Entry Array 将占用更多的内存.
  * 且 HashMap 使用了 Serializable 序列化, 而 Bundle 是 Parcelable, 默认情况下开销更小.

145. Application
   * 一个Application 对应一个 Dalvik, 而一个App可能有多个 Dalvik (多进程模式)
   * Application 里可以存数据, 但是低内存时的 crash 会导致数据丢失, 所以需做判空
   * Application 生命周期和 Dalvik 一致, 所以单例/静态变量初始化需要 context 时, 使用 application的

146. 窗口变暗
```
/**
    * 调整窗口的透明度
    * @param from>=0&&from<=1.0f
    * @param to>=0&&to<=1.0f
    *
    * */
   private void dimBackground(final float from, final float to) {
       final Window window = getWindow();
       ValueAnimator valueAnimator = ValueAnimator.ofFloat(from, to);
       valueAnimator.setDuration(500);
       valueAnimator.addUpdateListener(new AnimatorUpdateListener() {
           @Override
           public void onAnimationUpdate(ValueAnimator animation) {
               WindowManager.LayoutParams params = window.getAttributes();
               params.alpha = (Float) animation.getAnimatedValue();
               window.setAttributes(params);
           }
       });

       valueAnimator.start();
   }
```

调用
```
/** 窗口背景变暗*/
   dimBackground(1.0f,0.5f);


   /** 窗口背景变亮*/
   dimBackground(0.5f,1.0f);
```

147. 数据库优化
  * 索引 加快 SELECT/WHERE, 但是占内存和减慢UPDATE/INSERT 语句时的数据输入
  * 事务 原子操作, 用于执行大量插入时, 避免频繁Cursor. Room @Insert 标签自带事务


149. get/post
  * 效果: get 获取资源, post 可改变服务器里的资源
  * 传输数据大小: 协议上都没限制, 但是各浏览器限制URL长度, 服务器限制数据大小
  * 安全: 明文的历史记录可查到, 且易被 Cross-site request forgery(跨站请求伪造攻击)
  * 接收方式: Request.QueryString 和 Request.From 获取变量的值

150. https
  * http和 tcp/ip 之间添加了 SSL

151. NIO/IO
  * NIO
    多连接, 少数量, 多了 Buffer 和 Selectors
    非阻塞, 通过 channel 调用, 再 Selector 管理 channel, 所以可以同时读多个流
  * IO
    少连接, 数据多, IO
    阻塞, 一旦线程调用 read(), write, 就阻塞了.

152. 视频播放
  * 监听 VideoView 的 prepared. handler 延时 3000 毫秒后给 DecorView 修改 SystemUiVisibility
  * VideoView 继承 SurfaceView, 内含 MediaPlayer 和 Vector 包含的
    * 缺点: 进入后台再出来, 不会恢复播放状态, 需自己在 onSaveInstanceState 保存,
153. 图片展示
  * ViewPager + Fragment.
  * 图片下载需申请权限, 下载使用 DownloadManager, 获取 SystemService 的 DOWNLOAD_SERVICE, DownloadManager.Request 设置保存路径
154. 图片上传
  * 拍照,
  * 相册
    * 判断权限
    * 开 ACTION_GET_CONTENT 的 intent,
      * 4.4 前 Intent 需 setType("image/\* video/\*");
      * 4.4 后 Intent 的 setType("\*/\* "), 但是 putExtra(Intent.EXTRA_MIME_TYPES, mimeTypes); mimeTypes是image/\*, video/\* 数组.
    * 根据回传的 intent
155. JVM
  * HotSpot 是 JVM 规范的一种实现, 全名 HotSpot VM, Oracle/Sun 用的都是它,
156. adb
  * 不同版本studio打开时会互相抢adb, 建议只开一个版本的
157. RecyclerView分割线/间距
  * ItemDecoration
158. DialogFragment.
  * 无法展示可能因其内部RecyclerView 涉及到 window 封装
159. SparseArray
  * 用于替代 HashMap
160. fresco 用了c代码作为核心, 不占用app内存, 即使自身崩溃, 也不影响
161. handler与线程
162. 500x500的图在drawable-xhdpi下占用多少内存
163. DialogFragment 需设置背景
```
window.setBackgroundDrawableResource(android.R.color.transparent);
```
才能让xml按照设定的UI展示,

164. 字符串轻量保存(SharedPreferences 存 Gson 转完的 String).
```
//存
Gson gson = new Gson();
String s = gson.toJson(markedMemberList);
SharePrefUtil.setStr("markMemberList", s);
```

```
//取
Gson gson = new Gson();
List<String> markedMemberList = gson.fromJson(markMemberList, new TypeToken<List<String>>(){}.getType());
```

165. 防爬虫
* 客户端ssl pinning, 判断服务证书是否合法，非法则不发送请求, (cycript 改属性破)
* 客户端插暗桩收集信息, 服务端根据账号和IP收集请求次数，时间段内切换IP次数

166. Fragment 需要接受Activity 传来的Listener时, Bundle不好传listener, 在Attach里强转context;
167. mkdir 和 mkdirs, 后者可在父路径不存在情况下创建
168. DialogFragment 蒙层透明度

```
@Override
   public void onStart() {
       super.onStart();
       WindowManager.LayoutParams attributes = getDialog().getWindow().getAttributes();
       float dimAmount = attributes.dimAmount;
       attributes.dimAmount = 0.4f;//此处设置透明度
       LogUtil.i("dimAmount", dimAmount+"");
       getDialog().getWindow().setAttributes(attributes);
       getDialog().getWindow().addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);
   }
```

169. textview 需要多个空格, ```" "```无效, 使用 ```&#160;``` , 但是需注意, ```replace(" ","")```无效, 需```replaceAll("\\s*", "")```.
170. textview 添加多个 String, 不能直接```%s```, 而需要 ```%1$s``` 和 ```%2$s```

171. studio 报错 Error:Failed to complete Gradle execution. Cause: Write access is allowed from event dispatch thread only
* File -> Project Structure -> SDK Location, 勾选Use embedded JDK
* ![参考](https://www.jianshu.com/p/d01acb816c0e)

172. drawPath
drawPath 画线时须设置为Stroke.

172. 自定义view画虚线.
* paint 设置 DashPathEffect
  * drawLine 需要提前关闭硬件加速
  * drawPath 直接用

172. studio 改回工具栏和编辑栏
* View-Toolbar

173. PathMeasure, 需要在path画完后在setPath

174. LinearGradient 的变色构造方法, x,y 的正负会影响变色的顺序.

175. canvas.translate 会影响
176. miui8及以上, 裁剪照片bug.[参考](https://blog.csdn.net/eclothy/article/details/42719217 )
裁剪后的图片通过Intent的putExtra("return-data",true)方法进行传递，miui系统问题就出在这里，return-data的方式只适用于小图，miui系统默认的裁剪图片可能裁剪得过大，或对return-data分配的资源不足，造成return-data失败。

解决思路是：裁剪后，intent保存图片的资源路径Uri，在onActivityResult()方法中，再提取对应的Uri图片资源转换为Bitmap使用。

  ```
  /**
   * 裁剪图片
   */
  private void startPhotoZoom(Uri uri, int size) {
      Intent intent = new Intent("com.android.camera.action.CROP");
      intent.setDataAndType(uri, "image/*");
      // crop为true是设置在开启的intent中设置显示的view可以剪裁
      intent.putExtra("crop", "true");

      // aspectX aspectY 是宽高的比例
      intent.putExtra("aspectX", 1);
      intent.putExtra("aspectY", 1);

      // outputX,outputY 是剪裁图片的宽高
      intent.putExtra("outputX", size);
      intent.putExtra("outputY", size);

      /**
       * 此方法返回的图片只能是小图片（sumsang测试为高宽160px的图片）
       * 故只保存图片Uri，调用时将Uri转换为Bitmap，此方法还可解决miui系统不能return data的问题
       */
      //intent.putExtra("return-data", true);

      //裁剪后的图片Uri路径，uritempFile为Uri类变量
      uritempFile = Uri.parse("file://" + "/" + Environment.getExternalStorageDirectory().getPath() + "/" + "small.jpg");
      intent.putExtra(MediaStore.EXTRA_OUTPUT, uritempFile);
      intent.putExtra("outputFormat", Bitmap.CompressFormat.JPEG.toString());

      startActivityForResult(intent, PHOTO_REQUEST_CUT);
  }

  ```
  ```
  /**
   * 处理返回结果
   */
  @Override
  protected void onActivityResult(int requestCode, int resultCode, Intent data) {
      // TODO Auto-generated method stub
      case PHOTO_REQUEST_CUT:
          //将Uri图片转换为Bitmap
          Bitmap bitmap = BitmapFactory.decodeStream(getContentResolver().openInputStream(uritempFile));
    //TODO，将裁剪的bitmap显示在imageview控件上
          break;
      }
      super.onActivityResult(requestCode, resultCode, data);
  }

  ```

177. database bug
```
java.sql.SQLException: queryForLong from database failed: SELECT COUNT(*) FROM `uploadmissionbean` WHERE `id` = ?
```
表未创建/更新

178. 多个 notification
NotificationManager.notify(id, builder.build()); 不同 id 创建不同通知栏

179. Service
Service Intent must be explicit 5.0 开始 service 的intent 需要显示调用

180. Service 弹 Toast, 需要切换到主线程(Toast需要加进Looper)
181. Looper.loop(); 是个死循环, 其后的代码无法运行
182. 2018-11-12T07:41:25Z 格林尼治时间线
183. 数据库的设计: 所有字段都是不可分解的原子值, 每一列都和主键相关,
184. 热点下gradle 速度慢, 梯子
185. Animation 在 RecyclerView 下会被打断, 替换为 ValueAnimator
186. 边缘阴影
187. Service 的 onStartCommand 中, 传入的 intent 可能为null, 因为是系统杀掉的, 再次打开的时候没intent, 所以补充判断, 并且return START_REDELIVER_INTENT;
188. UpdateManager
189. x.compareTo(y)
  * 正, x>y
  * 负, x<y
  * 0, x=y
190. A isAssignableFrom  B, A是否和B是一个类或者父类
191. glide 冲突(support包版本与项目不一致)
192. 蓝牙的读写需要控制状态, 只有不busy时才成功, writeCharacteristic/readCharacteristic 时置忙, onWriteCharacteristic, onReadCharacteristic 时置忙
193. gatt.close 在结束到 gattcallback 接收完后再执行.
194. aapt 问题, 先看一下报错xml
195. Glide图片压缩 resize()
196. jpg,jpeg 只是dos win95等早期系统限制了扩展名字数3
197. git新提交的库没有被忽略, 更新一下ignore
```
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```
198. layoutAnimation
http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2017/0807/8348.html

199. MAT, GIMP 查看heap
200. FinalizerReference 内存泄漏
201. daemon
202. singleTop 和 startActivityForResult 冲突
203. 依赖查询
204. 所有请求放入service 地址: https://github.com/taoliuh/v2ex/blob/master/v2ex/src/main/java/com/sonaive/v2ex/provider/V2exProvider.java
205. Service 替换 WorkManager
206. GlideApp, 需要创建在 Application 同级别下的注解 class
207. module 引入 jar, gradle 添加
```
sourceSets {
        main() {
            jniLibs.srcDirs = ['libs']
        }
    }
```

208. implementation 只针对当前包可用, module 引入 jar, 需使用 compile, 这样别的引用了这个 module 的 app 才可以用里面的 jar

209. 共享元素的finish(),    替换为     supportFinishAfterTransition();
201. 蓝牙scanMode 使用 SCAN_MODE_LOW_POWER, SCAN_MODE_LOW_LATENCY 会导致结束的时候多扫出一个设备 https://codeday.me/bug/20180714/195217.html
202. ConcurrentModificationException, 增强for/remove 导致
https://juejin.im/post/5a992a0d6fb9a028e46e17ef
203. Timer already cancelled, timerTask只可被schedule 1 次
204. Android Studio 获取SHA1
* 默认
```
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```
* 指定
```
keytool -list -v -keystore /Users/fred/Documents/GitHub/lanbuff-coach-app-android/lanbufflite.jks -alias key0 -storepass lan123 -keypass lan123
```
205. 运行时设置 textSize 为 dimen
```
tvLessonTime.setTextSize(TypedValue.COMPLEX_UNIT_PX, itemView.getResources().getDimension(R.dimen.dp_24));
```

206. RecyclerView 干掉 notifyXXXX时的闪烁
* https://www.jianshu.com/p/654dac931667
* 1
```
((SimpleItemAnimator)recyclerView.getItemAnimator()).setSupportsChangeAnimations(false);
```
* 2
```
recyclerView.getItemAnimator().setChangeDuration(0);
```


207. INSTALL FAILED CONFLICTING PROVIDER
* 有<provider> 占用了想用的包名
* 解决: <provider> 使用软编码
```
<provider
    android:name="android.support.v4.content.FileProvider"
    android:authorities="${applicationId}.fileprovider"
    android:grantUriPermissions="true"
    android:exported="false">
    <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>
```
* [参考](https://blog.csdn.net/fengyuzhengfan/article/details/52769480s)

208. 提取pdf图片
* ps打开
* 选择图片

209. RecyclerView 嵌套 ScrollView 无法滑动
```
public boolean canScrollVertically() {
               return false;
           }
```

210. Glide 无法适应 options
211. 拍照+水印
```
https://blog.csdn.net/dawanganban/article/details/51148070
https://www.jianshu.com/p/27530fbbe5a3
```

212. 7.0拍照
https://blog.csdn.net/u010356768/article/details/70808162

213. setResult
不能放在onDestroy
嵌套activity, 每个都要onActivityResult

214. %s, 单独的时候直接, 2个及以上是%1$s, %2$s, 序号和$必不可少
215. NestedScrollView
216. simplePagerTitleView.setTextSize(TypedValue.COMPLEX_UNIT_PX, getResources().getDimensionPixelSize(R.dimen.dp_32)); 设置textSize.

217. 使用tint修改颜色
218. ViewRootImpl: jank_removeInvalidNode jank list is null 华为9.0P20pro折线图 bug
219. retrofit, compose()里设置为DESTROY, 否则PAUSE时会被权限请求打断请求
艺术开发探索25页
220. super构造方法, 须super在前, 其他不必须
221. 旋转屏幕, activity 调用 onSaveInstance, 此时的 FragmentManager 的 commit 会导致运行时异常.
222. onRestoreInstance, 需在 activity 被销毁后才调用, 非必须和 onSaveInstance 同时出现
223. No static method/NoSuchMethodError, 可能导入了一个包的不同版本.
224. elevation, 必须是background, image 设置 src无效
225. Edittext 在投屏状态下无法展示
226. gradiant, 设置的angle 需要是45的倍数
227. json  optString(); 获取不存在的字段时不会报异常
228. LOCATION_HARDWARE 为隐私级权限, 三方app无法获取
229. 设置+app 两个界面切换, 设置打开权限, app 正常 onPause->onResume; 设置关闭权限, app 重启 onCreate
230. 华为8.0.0 权限问题, 说明[地址](https://github.com/yanzhenjie/AndPermission/issues/338), [地址2](https://github.com/SachinVin/citra_android/issues/144)
SplashActivity, 在acitvity 刚打开时弹出dialog会报activity的setcontentView为空
报错内容:
```
unable to start activity ComponentInfo
android.content.res.Resources$NotFoundException: Resource ID #0x0
DeadObjectException
```
231. onbackPress无法被调用, onKeyDown 拦截
232. webview 加载失败
233. transparent 是否缩小布局层数
* 是否加了http,
* 是否在一个局域网

234. OnFragmentInteractionListener
235. uri/url/intent
236. gson 相同子字段时解析奇怪gsonformat
237. 补间动画, translate/scale 分开调试
238. webview 加载 https, 图片不显示
* https 不能引用 http 资源, 默认混合模式关闭
* 设置
```
webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
```

239. Program type already present: android.support.v4.media.MediaBrowserCompat$ConnectionCallback$ConnectionCallbackInternal
240. HttpURLConnection.getContentLength(); 获取的size跟下载下来的不一致.[from](https://www.cnblogs.com/renkangke/p/3501506.html)
2.2 以上 HttpURLConnection 与服务器默认采用gzip压缩, 需设置
```
urlConnection.setRequestProperty("Accept-Encoding", "identity");
```
关闭压缩

241. vim
```
//打开vim, 如果没有则新建 touch .bash_prifile
vim .bash_profile
//进入编辑, 底部变成 --INSERT--
按 i
//输入内容
//退出编辑模式, 隐藏 --INSERT--
按 esc
//保存
:wq!
//生效配置
source .bash_profile
```

242. GCC, LLVM, Clang. Fortran
[参考1](https://www.cnblogs.com/qoakzmxncb/archive/2013/04/18/3029105.html)
[知乎](https://www.zhihu.com/question/20235742)
* GCC: GNU开发的编译器, GPLv3证书, 不支持模块化, 基于c, 不需要c++编译器
  * LLVM: 编译器的支持库BSD证书, 出错提示便捷,
* Clang: 基于LLVM, 运行时架在OpenGL, GPU可分担, 快, 内存占用小,
* Fortran: 一种规范严谨复杂的语言, 定位于科学计算

243. ./gradlew app:dependencies
244. gradle 编译错
```
Error:Execution failed for task ':app:compileDebugKotlin'. > Compilation error. See log for more details
```
解决：点开右侧Gradle, 选择"project名称"->":app"->"Tasks"->"build"->"assembleDebug"或者"assembleMyFlavor"[参考](https://stackoverflow.com/questions/43848845/errorexecution-failed-for-task-appcompiledebugkotlin-compilation-error/49717363#49717363)
调度算法
245. 向下兼容 = 向后兼容 back compatibility（后：落后，对过去的兼容负责）
246. ARM,X86(参考)[https://zhuanlan.zhihu.com/p/21266987]
* ARMv7
* ARMv8
  * AArch32 与ARMv7差不多，多了一些vfp指令
  * AArch64 指令编码还是32位，寄存器64位，两者可以无缝切换
* 苹果开放ARM64 LLVM
* 别的厂商竞争作出 AArch64
* 14年5月合并
* Intel和ARM区别
  * Intel 使用CISC(复杂指令集), 高效
  * ARM 使用RISC(精简指令集), 低功耗
  * 纳米数越小，能量使用效率越高
  * Intel 并没研发64位版本的x86指令集, x86_64实际是AMD研发的, 所以Intel做了IA64的64位处理器
  * ARM做出64位寻址和64位寄存器，就是AMD64
  * 11年ARM推出ARMv8 64位架构
  * 功耗:
    * Intel 自己厂商制造, 比ARM的代工厂台积电等快一代
    * 设计
      * 前端设计
        * CISC
        * RISC
        * ARM乱序执行能力不如x86, x86增强了单核的多线程能力，代价是无法高效关闭子模块，且时钟保持切换，功耗高。ARM次序进行，且多核，保持子模块和时钟信号的关闭，更省电
      * 后端设计（耗电）
        * 电压
        * 时钟
        * 耗电原因（都会使所控制的模块无法工作，但是门控时钟恢复速度快，但是上电顺序（需要按照模块供电顺序上电）也导致恢复的时间可能会很长）
          * 动态功耗，晶体管输入电压切换的时候产生的耗电
            * 门控时钟(Clock Gating)
          * 漏电功耗，关闭某个模块来省电
            * (Power Gating)
247. gnustl_static
* ndk 已经不在支持 ```gnustl_static```, ```c++_static``` 或 ```c++_shared``` 二选一

248. linux 配置环境变量[参考](https://blog.csdn.net/huanbia/article/details/50569774)
```
sudo gedit .bashrc
```
~/.bashrc : 该文件包含专用于你的bash shell的bash信息,当登录时以及每次打开新的shell时,该该文件被读取。
~/.profile :  在登录时用到的第三个文件 是.profile文件,每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该文件仅仅执行一次!默认情况下,他设置一些环境变量,执行用户的.bashrc文件。
/etc/bashrc : 为每一个运行bash shell的用户执行此文件.当bash shell被打开时,该文件被读取.
/etc/profile : 在登录时,操作系统定制用户环境时使用的第一个文件 ,此文件为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行。

249. CMake
* ninja: error: loading 'build.ninja': No such file or directory[参考](https://blog.csdn.net/kidults/article/details/80599923)
  * gradle关联原生库可能会未配置ndk
* CMake Error: CMake can not determine linker language for target: native-lib
  * add_library 中 native-lib 的路径可能不只是"src/main/cpp/native-lib.cpp", 而是需要找到native-lib, 右键 Copy Relative Path, 来获取

250. Error:Execution failed for task ':app:processDebugManifest'. >
Manifest的报错也是在gradle时爆出
251. Failed to download samples index, please check your connection and try again
Preferences -> Appearance&behavior -> System Settings -> HTTP Proxy -> Auto-detect proxy settings
252. mac传输文件给linux, linux设置ssh
```
sudo vi /Library/Preferences/VMware\ Fusion/vmnet8/nat.conf
```
找到[incomingtcp]部分，配置
```
[incomingtcp]

# Use these with care - anyone can enter into your VM through these...
# The format and example are as follows:
#<external port number> = <VM's IP address>:<VM's port number>
#8080 = 172.16.3.128:80
你MAC的端口 ＝ VM的IP:VM的端口
```
重启服务
```
sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --stop
sudo /Applications/VMware\ Fusion.app/Contents/Library/vmnet-cli --start
```
permission 报错
```
Permission denied, please try again.
```
打开 ssh 的 root 权限

```
E325: ATTENTION
```
rm -rf 删除xxx.swap文件

253. AndroidStudio 一debug就app打开后关闭
* 关闭开发者选项重新打开
* 删掉所有端点
* 打开“仅usb充电也可调试

254. RecyclerView 套RecyclerView，子RecyclerView出错时'android.view.View android.support.v7.widget.RecyclerView$ViewHolder.itemView' on a null object reference 不会显示具体的错误
255. Intent无法传递超过40K的文件(如bitmap)[CSDN](https://blog.csdn.net/shakdy/article/details/76283711)
* 转成数组传递
```
ByteArrayOutputStream output = new ByteArrayOutputStream();//初始化一个流对象
qrBitmap.compress(Bitmap.CompressFormat.PNG, 100, output);//把bitmap100%高质量压缩 到 output对象里
byte[] result;  //将bitmap转化的byte数组
result = output.toByteArray();//转换成功了  result就是一个bit的资源数组

Intent intent = new Intent(getActivity(), ShareActivity.class);
intent.putExtra("qrbitmap", result);
startActivity(intent);
```
接收
```
byte[] qrbitmapByte = getIntent().getByteArrayExtra("qrbitmap");
mQrBitmap = getPicFromBytes(qrbitmapByte,null);

//下面的这个方法是将byte数组转化为Bitmap对象的一个方法
public static Bitmap getPicFromBytes(byte[] bytes, BitmapFactory.Options opts) {

    if (bytes != null)
        if (opts != null)
            return BitmapFactory.decodeByteArray(bytes, 0, bytes.length,  opts);
        else
            return BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
    return null;

}
```


256. Unexpected token o in JSON at position 18[Ref:CSDN](https://blog.csdn.net/wxl1555/article/details/79184076)
* 直接看第18个字符，可能是不可见的字符

### 257. 代理
#### http代理
##### 普通代理(HTTP Proxy)[Ref:天天给 App 抓包，还不懂 HTTP 代理吗？](https://mp.weixin.qq.com/s/H5H0LixgRY6CoRunBaLBAw)
* 代理服务器作为中间人, 可以隐藏自己的存在, 但是通过X-Forwarded-IP这个自定义的Header, 可以告诉服务端真正的客户端IP, Request-URI必须使用绝对路径
* **HTTPS是普通代理的克星**，中间人拿不到证书和密钥，无法知道传输内容。只要两端严格验证证书，中间人就无法完成TLS握手（Charles抓HTTPS数据就需要安装证书，走回普通代理），不安装证书时的请求就是隧道代理
##### 隧道代理(HTTP tunnel, HTTP/1.1中加入)[Ref:什么是HTTP隧道，怎么理解HTTP隧道呢](https://www.zhihu.com/question/21955083)
* 常规请求，请求头结束的CRLF+CRLF后，之后的内容是请求体。
* CONNET方法请求，不包含请求体，请求头的两个CRLF后的内容是转发的内容
  * 请求：本地通过 CONNECT 方法, 创建一条 TCP 链接, 成功后服务器无脑盲转发 Head 后两个 CRLF 后的内容 **这些内容并非请求体**
  * 返回：服务器在 TCP 链接成功时，返回```HTTP/1.1 200 Connection Established```), 这个 HEAD 结束后的内容均为远程服务器返回的内容，直到TCP通道关闭
* 但是相比Socks5, RFC(请求注释文档)多，以及兼容历史等各种问题

### 258. CRLF[Ref:CSDN](https://seacatcry.pixnet.net/blog/post/13732061-%E3%80%90%E8%BD%89%E8%B2%BC%E3%80%91%5Cr%5Cn%E5%92%8C%5Cn%E7%9A%84%E5%B7%AE%E7%95%B0)
* \r, return (carriage return) 回车, 对应原始打印机把打印头定位在左边界
* \n, newline(line feed) 换行, 对应原始打印机把纸下移一行
* unix每行结尾只有\n，
* windows每行结尾是\n\r
* mac每行结尾只有\r

### 259. HTTP请求
一个完整的请求至少包含请求行，请求头，CRLF这三部分[Ref:RFC2016的第五章Request](https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html)
##### 1. 请求行(Request-Line, 位于首行, 除了间隔和末尾，请求行不允许其他位置使用CRLF)
  * 请求方法 空格 请求地址 空格 协议 \r\n
  * 即 Method-URL-Protocol
  * 其中, HTTP1.1中请求方法分为8种, **实际上服务器往往不会支持所有协议**
    * 1.HEAD
    * 2.TRACE
    * 3.CONNECT 用于代理
    * 4.OPTIONS
####### 后四个是RESTful API
    * 5.GET, 最常用
    * 6.POST, 最常用
    * 7.PUT
    * 8.DELETE

##### 2. 请求头(Generial-header, Request-header, entity-header)
  * head1:value1\r\n
  * head2:value2\r\n
  * headn:valuen\r\n
##### 3. 空行\r\n
##### 4. 请求体(Entity Body)[Ref:理解HTTP之ContentType](https://segmentfault.com/a/1190000003002851)
根据Content-Type的内容, 分为
* 1.text/html 默认
* 2.text/plain
* 3.text/css
* 4.text/javascript
* 5.text/xml 微信的数据传递方式
###### 后四个是post发包的形式[Ref:HTTP请求头与请求体](https://segmentfault.com/a/1190000006689767)
* 6.application/x-www-form-urlencoded, 常用表单提交
* 7.**multipart/form-data**, 用于发送文件的post包, 须配合Content-Disposition包含文件名, 分割文件为多个boundary
![multipart/form-data结构图](https://raw.githubusercontent.com/fredsun/RES/master/multipart%3Aform-data.png)
* 8. application/octet-stream, 传递二进制流, 生成的文件扩展名 .tif(图片格式的一种)
* 9.application/json, 常用json上传, HTTP并不存在json, 是将 String 转换成json
* 10.application/xml,
...
其中lanbuff上传图片就是拼接 RequestBody 为 MultipartBody 的 FORM 类型
```
RequestBody requestBody = new MultipartBody.Builder()
        .setType(MultipartBody.FORM)
        .addFormDataPart("userId", SharedPreferencesUtils.getStringData(this, Constant.sp_user_id, ""))
        .addFormDataPart("version", Utility.getVerName(LanbuffApp.getInstance()))
        .addFormDataPart("device", Utility.getDeviceId())
        .addFormDataPart("phone", uploadMissionBean.getPhone())
        .addFormDataPart("studentIds", uploadMissionBean.getStudentIds())
        .addFormDataPart("coachId", uploadMissionBean.getCoachId())
        .addFormDataPart("footprintTime", DateStrUtil.dateToStrSS(new Date()))
        .addFormDataPart("content", uploadMissionBean.getContent())
        .addFormDataPart("images", imageFile.getName(), RequestBody.create(MediaType.parse("image/*"), imageFile))
        .build();
uploadApi.sync2FootprintUrl(requestBody)
        .subscribeOn(Schedulers.io())
        .observeOn(AndroidSchedulers.mainThread())
        .subscribe(new Subscriber<BaseResponseBean>() {

以及请求api中:
@POST(Constant.url_sync_2_footprint)
Observable<BaseResponseBean> sync2FootprintUrl(@Body RequestBody body);
```

##### 请求实例:
```
POST /servlet/default.jsp HTTP/1.1
Accept: text/plain; text/html
Accept-Language: en-gb
Connection: Keep-Alive
Host: localhost
Referer: http://localhost/ch8/SendDetails.htm
User-Agent: Mozilla/4.0 (compatible; MSIE 4.01; Windows 98)
Content-Length: 33
Content-Type: application/x-www-form-urlencoded
Accept-Encoding: gzip, deflate

LastName=Franks&FirstName=Michael
```

### 260. HTTP响应[Ref:CSDN](https://blog.csdn.net/tycoon1988/article/details/39991211)
##### 1. 响应行
* 协议 空格 状态 空格 状态描述\r\n
##### 2. 响应头
* head1:value1\r\n
* head2:value2\r\n
* headn:valuen\r\n
##### 3. 空行\r\n
##### 4. 响应体

##### 响应实例:
```
HTTP/1.1 200 OK
Server: Microsoft-IIS/4.0
Date: Mon, 3 Jan 1998 13:13:33 GMT
Content-Type: text/html
Last-Modified: Mon, 11 Jan 1998 13:23:42 GMT
Content-Length: 112

< html>
< head>
< title>HTTP Response Example</title></head><body>
Welcome to Brainy Software
< /body>
< /html>
```

### 261. 一张500x500的图在drawable-xdpi下占多少空间.
* 图片大小: 500x500, 则图片大小是250000pixel(像素)
* 色彩模式: 每个像素能展示多大范围的颜色
  * 色彩模式如果是 RGB, 则是 250000 x 3 = 750000bytes


### 262.gradient
270度时会失效，反向用45加颜色对调替代

### 打包报错 app:lintVitalRelease
Module:app中添加
```
lintOptions {
        checkReleaseBuilds false
        abortOnError false
    }
```
### 263. TabLayout
* 取消下划线, 设置 app:tabIndicatorHeight="0dp"
* 文字和图片间距，自定义Tab
```
tabLayoutMultiMain.getTabAt(0).setCustomView(getTabView("工作台",R.drawable.icon_workbench_notselect));
tabLayoutMultiMain.getTabAt(1).setCustomView(getTabView("我",R.drawable.icon_workbench_notselect));
public View getTabView(String title, int image_src) {
    View v = LayoutInflater.from(getApplicationContext()).inflate(R.layout.tab_multi_main, null);
    TextView textView = v.findViewById(R.id.tv_item_multi_main_name);
    textView.setText(title);
    ImageView imageView =v.findViewById(R.id.iv_item_multi_main_icon);
    imageView.setImageResource(image_src);
    v.setTag(title);//因为我用tag去区分点击的item，如果你用的tab.getPosition可以不设置这个值
    return v;
}
```

### 264.sp存list
泛型在编译期类型被擦除导致

### 265. 报错 app:compileDebugJavaWithJavac
* 解决:
1. 是否支持了java8
2. 查看报错位置
```
gradlew compileDebugSources --stacktrace -info
```
3. ButterKnife 是否对 OnClick 注解的方法加了限制符 public/private
4. 一般是编译时的问题，回头看一下自己新增加了什么包或者改了什么类

### 266. org.gradle.api.internal.tasks.compile.CompilationFailedException: Compilation failed
* 解决:
* 1.gradle 需要将 compile 替换为 implementation
* 2. invalidate cache
### 267. statusbar 配合 fragment 切换.
### 268. 让 EditText 失去焦点, 外部设置
```
android:focusable="true"
android:focusableInTouchMode="true"
```
* activity 透明, fragment 补充不同颜色view

### 269. AGPBI: {"kind":"error","text":"Program type already present: android.support.v4.os.ResultReceiver$MyResultReceiver","sources":[{}],"tool":"D8"} :app:transformDexArchiveWithExternalLibsDexMergerForDebug FAILED
* 解决
* 1. 确保android.useAndroidX=true, android.enableJetifier=true
* 2. ButterKnife 可能和v4包存在冲突


### 270. Could not find common.jar (android.arch.lifecycle:common:1.1.0)
* 解决
* 1. project 的 gralde 补充, 切记顺序, google()排在 allprojects 的最上面
```
allprojects {
    repositories {
        google()
        jcenter()
        maven { url "https://maven.google.com" }
        maven { url "http://dl.bintray.com/laobie/maven" }
    }
}
```

### 270. java.lang.ClassCastException: java.util.ArrayList$SubList cannot be cast to java.util.ArrayList[Ref:知乎](https://zhuanlan.zhihu.com/p/25426466)

* 错误操作：list.subList()后的结果强转ArrayList失败
* 原理: subList 不可以强转成 List 的全部实现类(Vector, LinkedList) subList 的实现是返回了其内部类 SubList 的实例， 是原始链表的一个视图，只可查看，不可增删，增删需另建相应对象


### 271. dialog背景模糊:
* 截图Activity， 改变截图透明度，弹出窗口
[Ref:
安卓AlertDialog对话框背景模糊的简单实现](https://blog.csdn.net/qq_32718875/article/details/83513342)

### 272. int无法存储null

### 273. protected
private 只可自己用
默认多一个同包里的类
protected子类也可以
public 跨包

###274. 嵌套RecyclerView
第二个RecyclerView的高度不能是0dp

### 275.color has not declaration
剪切下错误的部分再贴回去

### 276. Glide 切换图片闪烁
placeholder 设置为当前图片的Drawable
placeholder(imaveView.getDrawable())

### 277. javax.net.ssl.SSLHandshakeException: Handshake failed
### 278. java.net.UnknownServiceException: CLEARTEXT communication to 182.61.31.87 not permitted by network s
### 279.  @Body parameters cannot be used with form or multi-part encoding. (parameter #1)

### 280 Bean, parcel嵌套多个list, 每一级都需要写
in.readTypedList(orderList, OrderListBean.CREATOR);
和  dest.writeTypedList(orderList);

### 281. RecyclerView 二级嵌套，父Holder里拦截子RecyclerView的touch时，注意itemView是否真的是父itemview
### 集合塞进去的是数组还是
