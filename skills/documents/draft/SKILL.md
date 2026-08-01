---
name: draft
description: shift+home|end 从光标处选择至行首行尾
---

# IDE 使用技巧

工欲善其事必先利其器

## 文本编辑(通用)

* `shift+home|end` 从光标处选择至行首行尾
* `Ctrl+back|del` 删除前或后一个单词

## webStorm 重型武器

### 设置背景

### 运行
* `Ctrl+shift+F9|F10` 已Node引擎 debug或运行当前文件js
* `Alt+F2` 浏览器打开当前html文件

### 错误警告提醒
* 单词拼写
* 参数提醒 (顺序/文档)
* 正则 (多余的转义符号)
* eslint
* 无用的变量
* 不正确的方法引用(不存在的方法, 参数顺序/类型不对 参数注释文档)
* 编辑被保护的文件


### 快速定位
* warning/error F2
* 变量方法声明 ctrl+b
* 匹配{} ctrl+{}
* 文件某处结构 ctrl+f12
* 上次浏览编辑位置 Ctrl + Alt + ← →

### 快速修复
> Alt + Enter
>> eslint
>> fun doc
>> import

### 快速编辑
* 复制行 ctrl+d
* 剪切行 ctrl+x
* Ctrl + alt + l 格式化代码(细节可调 code style)

### live templates
* `div.item*3>a+p` zen coding 快速编写 html + css
* `rsc|rscp` 快速生成React组件模板
* 自定义

### 快捷查看
* Ctrl+Q 显示注释文档 (联网的)
* 参数提醒 Ctrl + P
* ctrl + shift + i : 显示当前CSS选择器或者JS函数的详细信息
* 最近更改的文件 Ctrl + E

