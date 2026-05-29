---
title: Mathematica一些小技巧收集
tags:  Code Mathematica 
layout: article
license: true
toc: true
key: a20241215
pageview: true
cover: /assets/images/Mma/MMA-logo.png
header:
  theme: dark
  background: 'linear-gradient(to right, rgb(101, 78, 163), rgb(234, 175, 200))'
article_header:
  type: overlay
  theme: dark
  background_color: false
  background_image: 
    gradient: 'linear-gradient(to right, rgb(101, 78, 163), rgb(234, 175, 200))'
    image: false
aside:
    toc: true
sitemap: true
mathjax: true
author: YuXuan
show_author_profile: true
---


整理收集一下使用[Mathematica](https://www.wolfram.com/mathematica/)时候的一些小技巧
{:.info}
<!--more-->

# 快速获取等高线数据
利用Mathematica绘制费米面最简单高效的方式就是使用ContourPlot函数，通过快速获取这些等能线上的点就能直接得到费米点了，但是ContourPlot函数一般只是绘制图像，并没有直接给出数据，这里就整理一下怎么直接来获取其中的绘图数据

![png](/assets/images/Mma/skill-1.png)

![png](/assets/images/Mma/skill-2.png)

可以通过FullForm函数来查看ContourPlot函数的结果，发现其中具有大量的List[x,y]这样的结构，其中的[x,y]就是绘制动能项的点，这里选择方式就是通过Mathematica的模式匹配将其提取出来。







# 公众号
相关内容均会在公众号进行同步，若对该Blog感兴趣，欢迎关注微信公众号。
{:.info}

<table>
  <tr>
    <!-- 图片单元格 -->
    <td style="width: 300px; height: 300px; text-align: center; vertical-align: middle; border: 1px solid #ccc; border-radius: 8px;">
      <img src="/assets/images/qrcode.jpg" alt="QR Code" width="300px" height="300px" style="border-radius: 8px;">
    </td>
    <!-- 文字单元格 -->
    <td style="width: 300px; height: 300px; text-align: center; vertical-align: middle; padding-left: 20px; border: 1px solid #ccc; border-radius: 8px;">
      <div>
        <h4 style="margin: 0;">Email</h4>
        <p style="margin: 5px 0;">yxli406@gmail.com</p>
      </div>
    </td>
  </tr>
</table>

