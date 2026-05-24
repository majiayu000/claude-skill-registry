---
layout: wiki
title: R 语言积累
categories: R
description: R　语言常用方法
keywords: skill ,R
---

　　积累一些在使用 R 语言编程中常用到的一些方法:


# 批处理 R 脚本使用

```bash
$ R CMD BATCH script.R
```

# R 获取帮助

##　使用 help()　或 ?

```r
help(seq)
#或者
?seq
```

## example() 运行例子代码

```r
example(seq)
```

## 使用 help.search() 或 ??

```r
help.search(ggplot2)
#或
??ggplot2
```

## 批处理模式帮助

```r
R CMD BATCH --help
R CMD INSTALL --help
```

## google 中搜索 R 脚本技巧

可以使用google 的文件类型准测，例如搜索permutations类型的R 语言脚本可以这样搜索

```
filetype:R permutations -rebol
```

其中 '-rebol' 是去掉 REBOL 语言中的.R脚本

# 向量化的 ifelse() 函数

`ifelse(b,u,v)`判断b为真返回值为u若为假则返回值为v

```r
> x <- 1:5
> y <- ifelse(x%%2 == 0,'yes','no')
> y
[1] "no"  "yes" "no"  "yes" "no" 
```

# 测试向量相等　all() 和 identical()

* `all()`相等即可，而`identical()`要求完全相等

```r
> x <-1:2
> y <- c(1,2)
> all(x==y)
[1] TRUE
> identical(x,y)
[1] FALSE
> typeof(x)
[1] "integer"
> typeof(y)
[1] "double"
```

# source()将函数代码读入R中

```r

source("script.R")

```

# R 中匿名函数


~~inc <- function(x) return(x^2)~~

```r
function(x) return(x^2)
```

# ubuntu中安装 Rstudio

* 下载 Rstudio 安装包

```bash
wget "https://download1.rstudio.org/rstudio-xenial-1.0.153-amd64.deb"

```

* 手动安装

```bash
sudo dpkg -i rstudio-xenial-1.0.153-amd64.deb
```

* 可能会出现依赖关系错误，执行强制安装

```bash
sudo apt-get -f install
```

# 合并数据框

* 有时会连续读取很多文本，文本要以数据框形式合并便于使用 `ggplot2` 画图，可以使用`ls()` 和 `do.call()` 方法实现。

```R
# test data frame
test_data <- data.frame("K"= c('A','B','C'),"V" =c(1,2,3))
# list store 10 data frame 
ls <- list()
id <- 1:10
for (i in id) {
  ls[[i]] <- test_data 
}
# combine
all_data_frame <- do.call("rbind", ls)

```

# 循环体结构中保存ggplot绘图

* 使用`ggplot2`绘图单次保存PDF没问题，放入循环体中则所有保存的PDF都为空白。是`ggplot2`的问题，需要加个`print()`函数解决。

* 例如：单次保存PDF，没有问题

```R

p <- ggplot(all_data, aes(x = V1, y = V2))
base_dir <- "~/home/test/"
pdf(paste0(base_dir,"test.pdf"),height =7.08, width=10.43)
p
dev.off()

```
* 循环体中保存绘制图片p，必须加`print()`函数才能正常保存。

```R

for(i in 1:10){
  p <- ggplot(all_data, aes(x = V1, y = V2))
  base_dir <- "~/home/test/"
  pdf(paste0(base_dir,i,"test.pdf"),height =7.08, width=10.43)
  print(p)
  dev.off()
}

```
# ggplot2中去掉默认灰色背景
* 开头加入 `theme_set(theme_bw())` 即可

```R

library(ggplot2)
theme_set(theme_bw())

```

***

**2021-5-2更新**

***
