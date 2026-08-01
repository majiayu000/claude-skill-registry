---
name: 2016-06
description: 上一篇主要温习了一下form表单的属性和表单元素，这一片主要讲解用JavaScript如何操作form。
---

#form表单那点事儿(下) 进阶篇

上一篇主要温习了一下form表单的属性和表单元素，这一片主要讲解用JavaScript如何操作form。

目录：

[表单操作](#handle)

* [取值](#get)

* [赋值](#set)

* [重置](#reset)

* [校验](#checkValidity)

* [提交](#submit)

[技巧](#skill)

* **[不提交空字段](#clean)**

* **[异步提交文件](#async)**

<a name='handle'></a>
##表单操作

<a name='get'></a>
###取值

用JavaScript操作表单，免不了会有取值赋值操作，比如有以下表单：
````html
  <form id='form0'></form>

  <form action="/login" method="post" target="blank" id='form1'>

    <input type="text" name='user_name'>  <!--field 0-->
    <input type="email" name='user_email'>  <!--field 1-->
    <select  name='user_phone'>  <!--field 2-->
      <option value='1'>13333333331</option>
      <option value='2'>13333333332</option>
      <option value='3'>13333333333</option>
    </select>
    <input type="text" name='form0_user_phone' form='form0'>  <!--field 3-->
    <button type='submit' form='form0'>预览</button>  <!--field 4-->

    <button type='submit'>提交</button>  <!--field 5-->

  </form>
````
用JavaScript获取表单的属性值，或者表单字段的值，可以直接通过 `elem.name` 的方式
````javascript
alert(form1.action); => '/login'
alert(form1.method); => 'post'
alert(form1.user_name.value) => ''
````
而要获取表单中的字段，则通过：
````javascript

// 属于本表单元素nodelist类数组，如果通过form属性指定到其他表单，不会算作本表单元素，下面获取到的元素是field 0，field 1，field 2，field 5
console.log(form1.elements);  => [<input>...,...,...</button>]

// 属于本表单元素个数，如果通过form属性指定到其他表单，不会算作本表单元素
console.log(form1.length);  => 4

// nodelist中下标为2的表单元素
console.log(form1[1]);  => <input type="email" name='user_email'>

// 表单中 name='user_name' 的元素,有同名的字段则返回一个nodelst类数组
console.log(form1['user_name']);  => <input type="text" name='user_name'> 或 nodelist

// 获取表单全部内容,详情见下面的 “提交” 条目
jQuery('#form1').serialize(); => user_name=&user_email=&user_phone=13333333331
jQuery('#form1').serializeArray(); => [] 一个数组，里面是每个字段的键值对
new FormData(form1) => 没有返回值

````


<a name='set'></a>
###赋值

表单本身的属性可以通过JavaScript赋值，比如 `action` , `method` , `target` 等。例如
````javascript
// 把表单提交到 "/signIn"
form1.action = '/signIn';

// 修改表单提交方式为 "GET"
form1.method = 'GET';
````

而给表单元素赋值，则是通过 `elem.value` 的方式，例如
````javascript
// 将user_name的值设定为 "hello world"
form1.user_name.value = "hello world";

// 选中select中值为2的option
form1.user_phone.value = 2;
````

<a name='reset'></a>
###重置
可以通过html或者JavaScript的方式把表单值重置为页面初始的样子。
html方式为点击 `type='reset'` 的 `input` 或 `button`。
JavaScript的方式为 `form1.reset()` 。
如果表单中应用了第三方UI库如 `select2` ，重置后还需要手动触发表单元素的change事件，以触发第三方库更新UI。
常用的方式是：
````javascript
form1.reset();
$(form1.user_phone).change();
````
<a name='checkValidity'></a>
###校验

#### 传统校验
传统的表单校验方式是通过监听的 `submit` 事件或是表单字段的 `input` , `focus` , `blur` , `change` 事件，去触发JavaScript中指定的校验规则，来确定表单是提交还是拒绝提交。

#### html5校验
步入html5时代之后，可以仅通过html本身完成表单提交前的校验工作。方式是给表单字段加上 `required` 和 `pattern` 属性，
`required` 是告诉浏览器这个字段需要校验，而 `pattern` 则指定一个正则表达式形式的校验规则。在表单提交时，浏览器会自动进行一系列的校验工作，没有通过校验的表单是无法提交到服务器的。
在表单提交之前，可以通过 `form.checkValidity()` 方法，这个方法会返回一个布尔值回馈整个表单是否通过了校验规则。
> 比较知名的表单校验插件是 [jquery-validation](https://github.com/jzaefferer/jquery-validation) 。

<a name='submit'></a>
###提交

#### 提交规则
提交表单时，表单拥有的字段会按照method中的指定方式提交给服务器，而表单提交的字段规则是：
    <table width='100%'>
        <tbody>
            <thead>
                <th>表单元素</th>
                <th>type<br></th>
                <th>规则<br></th>
            </thead>
            <tr>
                <td>&lt;input&gt;<br></td>
                <td>button<br></td>
                <td>永远不提交<br></td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>checkbox</td>
                <td>只在勾选后提交</td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>file</td>
                <td>永远提交，即使为空值</td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>hidden</td>
                <td>永远提交，即使为空值</td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>image</td>
                <td>永远提交，即使为空值</td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>password</td>
                <td>永远提交，即使为空值</td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>radio</td>
                <td>只在勾选后提交，如果一组Radio没有任何勾选，全部不提交。</td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>reset</td>
                <td>永远不提交<br></td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>submit</td>
                <td>点击哪个按钮，则提交这个按钮的值，其他的SUBMIT按钮值都不提交。<br>如果表单的提交行为是由JavaScript脚本触发的，则不提交任何值。<br></td>
            </tr>
            <tr>
                <td>&lt;input&gt;</td>
                <td>text</td>
                <td>永远提交，即使为空值</td>
            </tr>
            <tr>
                <td>&lt;button&gt;<br></td>
                <td>button<br></td>
                <td>永远不提交<br></td>
            </tr>
            <tr>
                <td>&lt;button&gt;</td>
                <td>reset</td>
                <td>永远不提交</td>
            </tr>
            <tr>
                <td>&lt;button&gt;</td>
                <td>submit</td>
                <td>点击哪个按钮提交表单，则提交这个按钮的值。<br>如果省略TYPE，IE默认为BUTTON，火狐默认SUBMIT。</td>
            </tr>
            <tr>
                <td>&lt;select&gt;<br></td>
                <td>-<br></td>
                <td>永远提交，即使为空值。</td>
            </tr>
            <tr>
                <td>&lt;textarea&gt;<br></td>
                <td>-</td>
                <td>永远提交，即使为空值。</td>
            </tr>
        </tbody>
    </table>
表格中没有提到的规则还有：
* 具有disabled属性的字段不会被提交
* 不具有name属性的字段不会被提交
* 同名的name属性会发生覆盖，radio和checkbox除外
* form指向其他表单的字段，不会被本表单提交

> [规则来源 http://www.cnblogs.com/manors/archive/2010/03/11/1683727.html](http://www.cnblogs.com/manors/archive/2010/03/11/1683727.html)

#### 表单序列化
GET方法提交表单，表单字段会被encodeURIComponent转换，并在url中显示出来。而post方法提交表单，会在请求body中发送表单字段键值对。

在通过JavaScript异步提交表单时，如何按照上面的规则去获取表单数据，jquery提供了 `serialize()` 和 `serializeArray()` 两个方法。使用该方法会取得和原生表单一致的提交字段。

#### 表单提交事件
表单提交到服务器时，会触发 `submit` 事件。也可以通过 `form.submit()` 手动提交一个表单。
````javascript
form1.onsubmit = function(event){
   event.preventDefault(); // 阻止默认事件，表单将不会提交到服务器
   if(confirm('你真的要提交我吗~')){
     this.submit(); // 点击确定后，表单会被提交
   }
}

````
<a name='skill'></a>
##技巧

<a name='clean'></a>
###不提交空字段
通过上方的表单提交规则可以知道，很多时候，无论是否填写了值，在提交的时候，该字段都会被提交到服务器。而在执行条件筛选表单提交的时候，由于常用的是GET请求，浏览器地址栏中通常会出现一长串字符。
这对于有洁癖的用户来说是无法忍受的，所以需要在提交表单前做一点小动作，让值为空的字段不提交到服务器。
````javascript
// 本段代码使用了jquery

var form = $('form'),
    fields = form.find(':input');

form.on('submit',function(event){
   event.preventDefault(); // 阻止默认事件，表单将不会提交到服务器
   fields.each(function(){
     if(!this.value.length) this.disabled = 'disabled'; // 含有disabled属性的表单字段将不会被提交
   });
   this.submit();
})

````

<a name='async'></a>
###异步提交文件
一般而言，文件提交都是同步的，因为一般的表单序列化方法，无法传输二进制的文件。而如果要实现异步上传文件的需求，主要依靠两种方式。
一种是新建一个 `iframe` ，在里面通过一个独立的form表单上传文件后，再和主frame进行通信。另一种则是通过html5的 `new FormData()` 方法,append进去一个文件，或是直接读取表单信息。
利用 `iframe` 方式提交文件的较为知名的插件是 [jquery.form.js](https://github.com/malsup/form) 。通过 `new FormData()` 则简单了许多：
````javascript
# 这是一个来自 MDN 的示例

// 原生JavaScript方式
var xhr = new XMLHttpRequest();
xhr.open("POST", form1.action);
xhr.send(new FormData(form1));

// 使用jquery的ajax()
$.ajax({
  url: form1.action,
  type: "POST",
  data: new FormData(form1),
  processData: false,  // 告诉jQuery不要去处理发送的数据
  contentType: false   // 告诉jQuery不要去设置Content-Type请求头
});
````

更多用法请参考 [MDN--使用FormData对象](https://developer.mozilla.org/zh-CN/docs/Web/Guide/Using_FormData_Objects) 。


#### 参考资料

[MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/form)

[w3.org](https://www.w3.org/TR/html5/forms.html)


