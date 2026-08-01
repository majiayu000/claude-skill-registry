---
name: swoole-doc
description: int swooleprocess::kill($pid, $signo = SIGTERM);
---

## swoole_process::kill
向进程发送信号

~~~
int swoole_process::kill($pid, $signo = SIGTERM);
~~~
* 默认的信号为SIGTERM，表示终止进程
* $signo=0，可以检测进程是否存在，不会发送信号

此方法类似于posix_kill <http://php.net/manual/zh/function.posix-kill.php>

### 僵尸进程

子进程退出后，父进程务必要执行swoole_process::wait进行回收，否则这个子进程就会变为僵尸进程。会浪费操作系统的进程资源。

父进程可以设置监听SIGCHLD信号，收到信号后执行swoole_process::wait回收退出的子进程。

~~~
<?php
$process = new swoole_process('callback_function', true);
//子进程执行的逻辑
function callback_function(swoole_process $worker)
{
    swoole_timer_tick(2000,function(){
        echo time();
    })
}
$pid = $process->start();
//父进程执行的逻辑
//监听子进程退出信号
swoole_process::signal(SIGCHLD, function($sig) {
  //必须为false，非阻塞模式
  while($ret =  swoole_process::wait(false)) {
      //执行回收后的处理逻辑，比如拉起一个新的进程
  }
});
~~~