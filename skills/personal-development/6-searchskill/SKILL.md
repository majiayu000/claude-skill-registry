---
title: "那些值得了解的搜索技巧，你都知道吗？ "
date: 2019-11-17
draft: false
tags: [search]
categories: [🔑 奇妙技巧]
---

日常开发中，总免不了遇到一些技术问题，查阅资料是必然的。那么为了节约时间，掌握一些游览器的查询技巧就是必不可少的。<!-- more -->

# 游览器搜索技巧：

搜索技巧总的来说分为两种格式：

1. **搜索词 特定语法词：限定词**

   其中特定语法词包括：intitle、site、inurl、filetype

1. **特定符号 + 搜索词**

   特定符号包括；英文双引号""，书名《》，加号 +，减号 —，星号 \*

## 详细解读：

### intitle 搜索范围限定在标题中包含限定词的网页

例如：网络定位 intitle：andriod

### site 搜索范围限定在特定的网点

例如：Vue 教程 site：bilibili.com

### inurl 搜索范围限定在 url 包含限定词的网页中

例如：js 入门 inurl：js

### filetype 搜索范围限定在制定的文档格式中

例如：Vue 入门 filetype：pdf

### 使用 "" 进行完全匹配

例如："android 网络定位"

### 使用 \* 进行模糊匹配

当记不住查询内容的全部内容时，使用 _ 进行模糊匹配
例如：你好，_

### 使用 《》 查书

例如：《活着》

### 使用 - 排除关键字

例如：android 网络定位 -gps

### 使用 + 添加关键字

例如：android 网络定位 +gps

最后，百度也有一个[高级搜索](https://www.baidu.com/gaoji/advanced.html)功能，能提供更详细的搜索

# github 搜索技巧

点击查看[官方说明文档](https://help.github.com/en/github/searching-for-information-on-github/about-searching-on-github)

**格式：in:对象名 限定词 量化词:>数量**

对象名包括：name、description、language、readme 等

量化词包括：stars、pushed 等

举个例子就能明白了～

`in:name blog language:JavaScript stars:>1000 `

意思是：搜索项目名称里面带有 blog 字段的、开发语言是 JavaScript 的、且 stars 数量大于一千的项目
