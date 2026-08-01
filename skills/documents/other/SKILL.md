---
name: other
description: 表示搜索结果局限于某个具体网站或者网站频道，如 “edu.sina.com.cn”、“www.seoanyi.com”，或者是某个域名，如
  “com.cn”、“com”等等。
---

# 谷歌语法


1.site

表示搜索结果局限于某个具体网站或者网站频道，如 `“edu.sina.com.cn”`、`“www.seoanyi.com”`，或者是某个域名，如 `“com.cn”`、`“com”`等等。

如果是要排除某网站或者域名范围内的页面，只需用 `“-网站/域名”`。如：
```
seo site:www.seoanyi.com
```


2.link

语法返回所有链接到某个URL地址的网页。

示例:搜索所有含指向健康论坛 `“www.renliubbs.com”` 链接的网页。

搜索: `“link:www.renliubbs.com”`



3.inurl

搜索网址中包含的指定字符串。它更精确的用法是：allinurl。语法返回的网页链接中包含第一个关键字，后面的关键字则出现在链接中或者网页文档中。

有很多网站把某一类具有相同属性的资源名称显示在目录名称或者网页名称中，比如“MP3”、“GALLARY”等，于是，就可以用INURL语法找到这些相关资源链接，然后，用第二个关键词确定是否有某项具体资料。

INURL语法和基本搜索语法的最大区别在于，前者通常能提供非常精确的专题资料。

如：搜索: `“inurl:pdf seo”`



4.allinurl

语法返回的网页的链接中包含所有查询关键字。这个查询的对象只集中于网页的链接字符串。示例:查找可能具有PHF安全漏洞的公司网站。通常这些网站的CGI-BIN目录中含有PHF脚本程序(这个脚本是不安全的)，表现在链接中就是“域名/cgi-bin/phf”。

语法: `“allinurl:”cgi-bin” phf +com”`



5.related

用来搜索结构内容方面相似的网页。例:搜索所有与中文新浪网主页相似的页面(如网易首页，搜狐首页，中华网首页等)，“related:www.sina.com.cn/index.shtml”。

【注意事项】related只适用于Google



6.cache

用来搜索GOOGLE服务器上某页面的缓存，这个功能同“网页快照”，通常用于查找某些已经被删除的死链接网页，相当于使用普通搜索结果页面中的“网页快照”功能。



7.info

用来显示与某链接相关的一系列搜索，提供cache、link、related和完全包含该链接的网页的功能。



8.or

当我们要同时搜索Google和baidu的最新情况时，我们用“Google OR baidu”【注意事项】中间的OR要大写



9.引号“”的用法

加上双引号后的搜索结果是完全匹配，不加引号的则是可以把搜索的词拆分了模糊匹配。



另附上【Google hack之精简部分】

1.查看基本情况

info:xx.com   返回一些基本信息

site:xx.com   返回所有与该有关的url

link:xx.com   返回所有与该站做了链接的站

site:xx.com filetype:txt   查找txt文件



2.查找后台

site:xx.com intext:管理

site:xx.com inurl:login

site:xx.com intitile:后台



3.查看服务器使用的程序

site:xx.com filetype:asp

site:xx.com filetype:php

site:xx.com filetype:jsp

site:xx.com filetype:aspx



4.查看上传漏洞

site:xx.com inurl:file

site:xx.com inurl:load



5.查找注射点

site:xx.com filetype:asp


