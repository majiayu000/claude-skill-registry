#cocoaPods Skill

**cocoaPods commands list**

##OverView

* $ vim Podfile // 首先要创建一个Podfile
* $ pod install // 给项目安装pod
* $ pod search XXX // 搜索某一个库
* $ pod update // 更新pod

## CocoaPods 安装有问题
$ mkdir -p $HOME/Software/ruby
$ export GEM_HOME=$HOME/Software/ruby
$ gem install cocoapods
[...]
1 gem installed
$ export PATH $PATH:$HOME/Sofware/ruby/bin
$ pod --version
0.37.2