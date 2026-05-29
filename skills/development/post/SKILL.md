---


---

**首先说明,这只是一些常见的使用技巧或者方法,你完全可以使用别的方式实现.**

#### 1.遵循PEP 8风格

PEPE 8是针对Python代码格式而编写的风格指南.目的是让每个开发人员遵循同一种风格来编写代码，这样书写可以使代码更加易懂、易读;方便自己,也方便他人. PEP8 的指南在其官网地址为:[链接](https://www.python.org/dev/peps/pep-0008/),这里列出几条绝对要准许的规则。
<!--more-->
**空白**

* 和语法相关,Python中每个缩进都应该是4个空格,而不是一个tab(制表符)
* 同一个类中,每个方法之间应该用一个空行隔开
* 变量赋值时,等号左右应该各写一个空格,而且只写一个
* 同一文件中,函数和类用两个空行隔开
* 每行的字符数不应该超过80,多出来的应该换行书写

**命名**

* 函数、变量名、属性应该采用小写加下划线的方式
* 内部属性应该以单下划线开头,例如：_name
* 私有属性应该以双下划线开头,例如: __name
* 自定义的异常或者类应该使用驼峰法来命名,例如: PreRequest
* 模块级别的常量应该采用大写字符加下划线的方式,例如:DEFAULT_PORTS

**表达式和语句**

* 检测列表长度是否为0时,不要使用`if len(list) == 0`方式,而是直接采用空值检测`if not list`
* import 导入模块时,首先是标准库、第三方库、自用库
* 否定形式应该在表达式内部,而不是再次取反 如: `if a is not b `而不是`if not a is b`
* 包导入时应该使用绝对路径,而不是使用相对路径

#### 2.列表推导式代替函数

对于数据较少的列表来说,我们需要改变列表中每个元素的内容,这时应该使用列表推导式而不是map, filter或自定义函数。

```
In [1]: a = [1,2,3,4,5,6]
In [2]: [x * 2 for x in a ]
Out[2]: [2, 4, 6, 8, 10, 12]
```

对于列表推导式来说,这样的方法类似于采用`for`循环,当然列表推导式也支持多层循环,但实际中不推荐这样使用。

#### 3.生成器替代大列表推导式

对于读取文件，Socket等大数据量特别大的操作时,应该使用迭代器来生成每个数据,而不能使用列表推导式一次把数据全部读到内存.

```
In [6]: a = (print(x) for x in open('/etc/passwd'))
```

#### 4.for while循环后面不要写else.

Python为for和while两种循环都添加了else语法,但实际使用起来并不是很好用,由于对`if else`的理解,我们很容易理解为如果循环没有正常执行,那么就执行else块。 但实际却刚好相反。

```
In [9]: for i in [1,2,3]:
   ...:     print(i)
   ...:     if i ==2:
   ...:         break
   ...: else:
   ...:     print('else break')
1
2
```

```
In [10]: for i in [1,2,3]:
    ...:     print(i)
    ...: else:
    ...:     print('else break')
    ...:
1
2
3
else break
```

对于这种写法,有过其他语言基础的编程者会感到很不能理解,所以最好的方式就是不在循环后面添加else.

#### 5. if多分枝嵌套

我们经常可以看到对于一个新手写的代码中有大量的分支嵌套语句,也就是这样`if{ if { if { }}}`.但对于Python来说这样的做法更糟糕,因为缩进的原因,这很容易超出每行数字的限制.

我们以一段伪代码来看:

```
if 商店开门:
    if 有苹果:
        if 钱足够:
            do_buy_apple();
        else:
            print('钱不够')
    else:
        print('没有苹果')
else:
    print('商店没开门')
```

这样的代码可读性和维护性都比较差,我们完全可以使用*提前结束*来优化代码:

```
if not 商店开门:
	print('商店没开门')
if not 有苹果:
	print('没有苹果')
if not 钱足够:
    print('钱不够')
```

#### 6.函数应该返回同一种类型

Python的函数可以返回多个元素,也可以返回不同类型，这看起来是一件好事；我们可以使用同一个函数通过返回不同结果来实现多种功能。但个人认为，Python中的函数应该遵循单一职责原则,每个函数应该做好自己的事情提供稳定的返回值。

```
def get_users(user_id=None):
    if user_id is None:
        return User.get(user_id)
    else:
        return User.filter(is_active=True)
```

以上例子,应该讲这个函数功能拆分为`get_user_by_id`和`get_active_user.`

#### 7. 函数中*args, **kwargs减少参数数量

Python中的函数接受参数可以分为位置参数，关键字参数,一般来说我们可以无限制的在Python的形参位置上传递参数,但是这样看起来相当臃肿.*args、**kwargs可以帮助我们解决这个问题。

* *args 接受任意的位置参数,会将其参数当做一个元组
* **kwargs 接受任意的关键字参数, 其参数会被当做一个字典

```
def do_alarm(alerm_type,alarm_subject_template,expMessage,alarm_message_template,sms_message,user_phone,user_email,dingding_address):
    pass
```

```
def do_alarm(alerm_type, *args, **kwargs):
    pass
```

#### 8. 上下文管理器读取文件

Python中读取文件使用的是`Open`函数,但是这样有一个非常大的缺点,我们总是在读取完文件后忘记关闭文件描述符,所以我们通常采用`with`语句来管理读取的文件对象,这样在`with`语句结束后会自行帮我们关闭文件描述符.

```
In [11]: with open('/etc/passwd') as file:
    ...:     print(file.read())
```

这里我们只解决文件描述符关闭的问题,但对于大文件读取我们任然需要注意。 `file.read()`是将文件中的内容一次性的全部读取完毕，如果是一个10G那么仅仅一个文件读操作就消耗了所有的内存。

通常，我们有两种做法来解决这个问题。

1. 分片读取,每次读取一定量的数据字节,这和`readline()`或`readlines()`是同一个道理。
2. *生成器解耦*,这是生成器的强项.

```
def file_read(fd,chunk=512):
    while True:
        read_data = fd.read(chunk)
        if not read_data:
            break
        yield read_data
```

#### 9. 循环替代递归

递归是函数自身调用自己的一种形式,但是Python对于递归的支持并不是很好,而且在递归的层数上还有很大的限制,最多是999层.

所以我建议：**尽量少写递归**。如果你想用递归解决问题，先想想它是不是能方便的用循环来替代。如果答案是肯定的，那么就用循环来改写吧。

#### 10.类的设计思想

参考：[连接](https://www.zlovezl.cn/articles/write-solid-python-codes-part-1/)

其主要思想来自于SOLID设计原则。

S: 单一职责原则

O: 开放封闭原则

---

实用技巧

#### 11. 原地交换数字

```
x, y = 10, 20
x, y = y,x
```

#### 12. 列表去重

```
In [24]: l = [1,2,2,3,3,3]
In [26]: {}.fromkeys(l).keys()
Out[26]: dict_keys([1, 2, 3])

In [27]: list(set(l))
Out[27]: [1, 2, 3]
```

上述提供了两种去重的方法，但是对于大列表而言他们的性能又有很多差异。

```
In [29]: l = [ random.randint(1,50) for i in range(100000)]
In [33]: %time {}.fromkeys(l).keys()                                                     CPU times: user 1.91 ms, sys: 0 ns, total: 1.91 ms
Wall time: 1.91 ms

In [34]: %time list(set(l))                                                               CPU times: user 952 µs, sys: 0 ns, total: 952 µs
Wall time: 954 µs
```

可以看到第二种方法效率更高。

#### 13.\_\_slots__ 大量属性时减少内存占用

```
>>> class User(object):
...     __slots__ = ("name", "age")
...     def __init__(self, name, age):
...         self.name = name
...         self.age = age
...
>>> u = User("Dong", 28)
>>> hasattr(u, "__dict__")
False
>>> u.title = "xxx"
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'User' object has no attribute 'title
```

#### 14. 多用collections模块

**Count 统计频率**

```
In [44]: a = collections.Counter(l)
In [45]: a.most_common()                                                                  Out[45]: [(6, 5), (1, 3), (5, 3), (9, 2), (3, 2), (2, 2), (10, 1), (8, 1), (7, 1)]
```

**deque优化的列表**

```
In [47]: collections.deque?
Init signature: collections.deque(self, /, *args, **kwargs)
Docstring:
deque([iterable[, maxlen]]) --> deque object
A list-like sequence optimized for data accesses near its endpoints.
File:           /usr/local/miniconda3/envs/py3.6/lib/python3.6/collections/__init__.py
Type:           type
Subclasses:     Deque
In [48]: Q = collections.deque()
In [49]: Q.append(1)
```

**OrderedDict 有序字典**

**defaultdict 默认字典**

#### 15. pathlib 模块操作目录

这里写一个简单的路径拼接的方法:

```
In [67]: import os
In [68]: os.path.join('/tmp', 'foo.txt')
Out[68]: '/tmp/foo.txt'
```

```
In [70]: Path('/tmp') / 'foo.txt'                                                         Out[70]: PosixPath('/tmp/foo.txt')
```
