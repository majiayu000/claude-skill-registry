---
name: blog
description: '[wget][wget] 是一个命令行的下载工具。对于我们这些 Linux 用户来说，几乎每天都在使用它。下面为大家介绍几个有用的 wget
  小技巧，可以让你更加高效而灵活的使用 wget。'
---

#wget 使用常用技巧


[wget][wget] 是一个命令行的下载工具。对于我们这些 Linux 用户来说，几乎每天都在使用它。下面为大家介绍几个有用的 wget 小技巧，可以让你更加高效而灵活的使用 wget。

>$ wget -r -np -nd http://example.com/packages/

这条命令可以下载 http://example.com 网站上 packages 目录中的所有文件。其中，-np 的作用是不遍历父目录，-nd 表示不在本机重新创建目录结构。

>$ wget -r -np -nd --accept=iso http://example.com/centos-5/i386/

与上一条命令相似，但多加了一个 --accept=iso 选项，这指示 wget 仅下载 i386 目录中所有扩展名为 iso 的文件。你也可以指定多个扩展名，只需用逗号分隔即可。

>$ wget -i filename.txt

此命令常用于批量下载的情形，把所有需要下载文件的地址放到 filename.txt 中，然后 wget 就会自动为你下载所有文件了。

>$ wget -c http://example.com/really-big-file.iso

这里所指定的 -c 选项的作用为断点续传。

>$ wget -m -k (-H) http://www.example.com/

该命令可用来镜像一个网站，wget 将对链接进行转换。如果网站中的图像是放在另外的站点，那么可以使用 -H 选项。

[wget]:http://www.gnu.org/software/wget/
