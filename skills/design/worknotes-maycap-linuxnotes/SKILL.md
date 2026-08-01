---
name: worknotes
description: '>添加epel源，参考 http://fedoraproject.org/wiki/EPEL 选取对应版本的‘epel-release’，添加源后即可查询到，以EL6为例：'
---

## linux_skill

### 前言
记录平时见到的一些技巧，以备不时之需

***
#### yum源问题

>添加epel源，参考 http://fedoraproject.org/wiki/EPEL 选取对应版本的‘epel-release’，添加源后即可查询到，以EL6为例：

	yum install http://mirrors.opencas.cn/epel/6/i386/epel-release-6-8.noarch.rpm

>yum本地源

	mkdir -p /mnt/centos
	mount -o loop CentOS-6.5-x86_64-bin-DVD1.iso /mnt/centos/


	cat /etc/yum.repos.d/CentOS-Media.repo

	# To use this repo, put in your DVD and use it with the other repos too:
	#  yum --enablerepo=c6-media [command]
	#
	# or for ONLY the media repo, do this:
	#
	#  yum --disablerepo=\* --enablerepo=c6-media [command]

	[c6-media]
	name=CentOS-$releasever - Media
	baseurl=file:///media/CentOS/
	        file:///media/cdrom/
	        file:///media/cdrecorder/
	gpgcheck=0
	enabled=1
	gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6

>yum 问题记录

	[root@core /]# yum list

	Loaded plugins: fastestmirror

	Determining fastest mirrors

	Error: Cannot retrieve metalink for repository: epel. Please verify its path and try again

	--->解决方法
	yum upgrade ca-certificates --disablerepo=epel

>yum 系列问题

	1. yum  install salt-minion

	....
	file /usr/lib64/python2.6/zipfile.pyo from install of python-libs-2.6.6-64.el6.x86_64 conflicts with file from package python-2.6.6-36.el6.x86_64

	Error Summary

	--->缩小范围
	2. yum install python-libs  问题一样

	最后得出应先升级python

	yum update python

	然后在 yum  install salt-minion

>yum 使用

	#反查相关内容由哪个安装包提供
	yum whatprovides *xx*

>rpm解压

	rpm2cpio xxx.rpm | cpio -div

>yum 下载

	yum install yum-utils
	yumdownloader xxx-xx

#### 网络类

>查看机器公网IP：

	curl ifconfig.me
	telnet cip.cc  ---  ip.cip.cc 返回纯ip

>查看网站使用服务器：

	curl -I  website

>获取google SPF 记录中包含的网段

	nslookup -q=TXT _netblocks.google.com 8.8.8.8   --失败则替换为114.114.114.114
	nslookup -q=TXT _netblocks2.google.com 8.8.8.8
	nslookup -q=TXT _netblocks3.google.com 8.8.8.8

>转发3389，访问远程桌面

	iptables -t nat -A PREROUTING -d [跳转机外网IP] -p tcp --dport 3389 -j DNAT --to-destination [winIP]:3389

	iptables -t nat -A POSTROUTING -d [winIP] -p tcp --dport 3389 -j SNAT --to-source [跳转机内网IP]

>远程端口检测

	1.nmap -p [port] ip

	#无须输入即可批量得到返回值
	2.echo -e '\n' | telnet [port] ip


#### 编辑类
>替换输出：

	echo $a | tr . ' '

>grep

grep的语法支持正则表达式,下面是一些有用的参数：

	-A num, --after-context=num: 在结果中同时输出匹配行之后的num行
	-B num, --before-context=num: 在结果中同时输出匹配行之前的num行，有时候我们需要显示几行上下文。
	-i, --ignore-case: 忽略大小写
	-n, --line-number: 显示行号
	-R, -r, --recursive: 递归搜索子目录
	-v, --invert-match: 输出没有匹配的行

	#排除空行和注释行
	egrep -v "#|^$"  filename


>awk

	#使用环境变量
	a=q.w.e
	b=2

	#这种写法其实际是双括号变为单括号的常量,传递给了awk.
	echo $a | awk -F . '{print "'$b'"}'

	echo $a | awk -F . '{print $2}'
	echo $a | awk -F . "{print $"${b}" }"
	echo $a | awk  -v r="$b" -F. '{print $r}'

	#从file文件中找出长度大于80的行
	awk 'length>80' file

	#按连接数查看客户端IP
	netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr

	#打印99乘法表
	seq 9 | sed 'H;g' | awk -v RS='' '{for(i=1;i<=NF;i++)printf("%dx%d=%d%s", i, NR, i*NR, i==NR?"\n":"\t")}'

>大小写

	a="ATest"
	echo ${a,}
	echo ${a,,}
	## 前面输出aTest，后面输出的是atest。

>字符匹配

	[root@HSlave1 ~]# echo $a
	abcdef
	[root@HSlave1 ~]# echo $a  | sed -r 's/ab(.*)ef/\1/g'
	cd

>删除空格

	#删除行首空格
	sed ‘s/^[ \t]*//g'

	#删除行末空格
	sed ‘s/[ \t]*$//g'

	#删除所有的空格
	sed s/[[:space:]]//g

>删除指定换行符


	sed ':label;N;s/\n/:/;t label' filename

	#:label是标签   N;下一行放到模式空间合并处理    t\b 跳转到标签
	[root@ns1 ~]# echo -e "a\nb\nc\nd" | sed 's/\n/,/;'
	a
	b
	c
	d

	＃可以看出，单行选取是\n作为分隔符的，因此无法取到\n字符进行处理。需要N；将此行和下一行放入模式空间执行处理。
	[root@ns1 ~]# echo -e "a\nb\nc\nd" | sed 'N;s/\n/,/;'
	a,b
	c,d

	# 可以看出，N；执行将下一行放入模式空间合并处理后，被放入模式空间的行，属于已经处理过的，不会进入下一次操作。因此需要打标签，跳回放入合并操作前，才能被执行。
	[root@ns1 ~]# echo -e "a\nb\nc\nd" | sed ':a;N;s/\n/,/;b a'
	a,b,c,d


>文件编码

	#vim 中查看文件编码：
	set fileencoding
	（备注：如果vim按照fileencodings提供的编码尝试不到文件编码，就用latin1编码打开）
	（比如：中文编码gb2312 ，vim提示编码就为latin1)

	#vim修改编码，前提识别对编码才可
	set fileencoding=utf-8

	#iconv转码编码
	iconv -t utf-8 -f gb2312 -c my_database.sql > new.sql
	iconv -t utf-8 -f gb2312 -c my_database.sql | tee my_database.sql

	#iconv参数解析：
		-f  原编码
		-t  目标编码
		-c 忽略无法转换的字符



#### 加密类

>随机密码

	pwgen 10 1  （10位长度，一个）
	makepasswd --char 50 --count 7
	openssl rand -base64 10

>加密

	mkpasswd mytest -s tt  （指定加密使用文）

>对称加密

	echo Tecmint-is-a-Linux-Community | openssl enc -aes-256-cbc -a -salt -pass pass:tecmint
	>U2FsdGVkX18Zgoc+dfAdpIK58JbcEYFdJBPMINU91DKPeVVrU2k9oXWsgpvpdO/Z

>解密

	echo U2FsdGVkX18Zgoc+dfAdpIK58JbcEYFdJBPMINU91DKPeVVrU2k9oXWsgpvpdO/Z | openssl enc -aes-256-cbc -a -d -salt -pass pass:tecmint

#### 系统类

>查看服务器型号

	dmidecode | grep Product

>查看cpu

	numactl --hardware

	cat /proc/cpuinfo

>查看磁盘属性

	yum install sg3_utils
	#显示硬盘转速
	sg_vpd  /dev/sda --page=0xb1

	yum install epel-release
	yum install inxi

	#显示详细信息（-b简略信息)
	inxi -F

>挂载ntfs

	#安装文件系统包
	wget http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.2-2.el6.rf.x86_64.rpm
	rpm -ivh rpmforge-release-0.5.2-1.el6.rf.i686.rpm
	yum install ntfs-3g

	#找出挂载点
	fdisk -l

	#挂载
	mount -t ntfs-3g /dev/sdb1 /mnt/winC


>清除Cache

	# sync; echo 1 > /proc/sys/vm/drop_caches    ---仅清除页面缓存（PageCache）
	# sync; echo 2 > /proc/sys/vm/drop_caches    ---清除目录项和inode
	# sync; echo 3 > /proc/sys/vm/drop_caches    ---清除页面缓存，目录项和inode

	sync 将刷新文件系统缓冲区（buffer），命令通过“;”分隔，顺序执行，shell在执行序列中的下一个命令之前会等待命令的终止。
	正如内核文档中提到的，写入到drop_cache将清空缓存而不会杀死任何应用程序/服务，echo命令做写入文件的工作。
	如果你必须清除磁盘高速缓存，第一个命令在企业和生产环境中是最安全，"...echo 1> ..."只会清除页面缓存。
	在生产环境中不建议使用上面的第三个选项"...echo 3 > ..." ，除非你明确自己在做什么，因为它会清除缓存页，目录项和inodes。

>清除交换分区

	# swapoff -a && swapon -a

>综合使用

	#!/bin/sh
	echo 3 > /proc/sys/vm/drop_caches && swapoff -a && swapon -a && printf '\n%s\n' 'Ram-cache and Swap Cleared'

	chmod +x clear_cache_swap.sh

	crontab -e
	0 3 * * * /path/to/clear_cache_swap.sh

	warning:当所有的用户都从磁盘读取数据时，这将导致服务器崩溃并损坏数据库。

>修改时区

	#查看时区
	cat /etc/sysconfig/clock
		ZONE="Asia/Shanghai"

	#替换时区
	cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

	#时区写入bios
	clock -w

	#查看硬件时区
	hwclock

	#同步网络时间
	#NTP服务器(上海) ：ntp.api.bz
	ntpdate -u 210.72.145.44        --中国国家授时中心

>自动化定时任务

	＃继承以前的，追加一个新的
	(crontab -l 2>/dev/null ;echo "* * * 2 * hostname")  | crontab -
	or
	/var/spool/cron/admin   (只适合root操作)


#### 获取时间

	＃查看明天日期
	date -d next-day +%Y%m%d
	date -d tomorrow +%Y%m%d

	＃查看昨天日期
	date -d last-day +%Y%m%d
	date -d yesterday +%Y%m%d

	＃查看上个月日期
	date -d next-month +%Y%m

	＃查看明年日期
	date -d next-year +%Y

	＃获取昨天或多天前的日期
	date +%Y%m%d -d '2 days ago'

	#获取2周后日期
	date -d '2 weeks'

	＃高级功能展示
	date -d '50 days'   	(50天后的日期）
	date -d '-100 days' 	(100天以前的日期）
	date -d 'dec 14 -2 weeks' （相对：dec 14这个日期的两周前的日期）

#### ssh

>远程重启tomcat时，简单采用ssh，会报JAVA_HOME找不到，可采用

	ssh user@host "source /etc/profile;/path/to/tomcat/bin/shutdown.sh"

>ssh使用awk，$2打印失效，原因是变量被ssh执行过程中解析，需要逃逸

	ssh 192.168.1.123 "source /etc/profile; if [ $( ps -ef | grep /web/service/tomcat9_xx_8003|grep -v grep | wc -l) -eq 1 ];then ps -ef | grep /web/service/tomcat9_xx_8003|grep -v grep | awk '{print \$2}'| xargs kill -9;fi"

#### 进程类

>获取命令当前进程号(pid)

	tail -f access.log & echo $!

>获取脚本执行时当前进程号

	#!/bin/sh
	echo $$
	#echo $$ > /tmp/xxx.pid
	sleep 100
	echo 'over'


### SOA

>zookeeper客户端

	#连接查看注册信息
	bin/zkCli.sh -server host port


### rsync

>有没有/问题

	rsync -av /web/work   test:/web/work    ---结果是 test:/web/work/work/*

	rsync -av /web/wrok/  test:/web/work    ---结果是 test:/web/work/*

	=>通过v选项可以看出复制目录层级，target目录不影响

>假同步

	-n, --dry-run               perform a trial run with no changes made

>同步跳过某些文件

	--exclude=PATTERN       exclude files matching PATTERN
    --exclude-from=FILE     read exclude patterns from FILE

	rsync -av /web/eln4share/xuemall/  --exclude="WEB-INF/classes/env.properties"  web@xx.xx.xx.xx:/web/eln4share/xuemall/

>指定端口

	 rsync -arv -e 'ssh -p 100' source-file remotehost:/target-path

### git

>放弃本地修改，强行更新

	git fetch --all
	git reset --hard origin/master

### iptables

>列出含有序号的INPUT规则，通过num删除

	iptables -L INPUT --line-numbers

	#举例：删除指定的第4行规则
	iptables -D INPUT 4


### 权限类

>粘滞位

	普通文件的sticky位会被linux内核忽略，
	目录的sticky位表示这个目录里的文件只能被owner和root删除,验证如下：

	[dev@nagios tmp]$ id web
	uid=6001(web) gid=6002(web) groups=6002(web)
	[dev@nagios tmp]$ id dev
	uid=6002(dev) gid=6002(web) groups=6002(web)
	[dev@nagios tmp]$ ll
	total 8
	drwxrwxr-t 2 web web 4096 Mar  4 09:27 test
	drwxrwxr-x 2 web web 4096 Mar  4 09:27 test2

	[dev@nagios tmp]$ rm -fr test/a
	rm: cannot remove `test/a': Operation not permitted
	[dev@nagios tmp]$ rm -fr test2/b
	[dev@nagios tmp]$






