---
name: run-local
description: "[RUN:on-VPS]=>[FIND:IP+port]=>[VERIFY:accessible]=>[REPORT:user]"
---
[START:application-on-VPS]
[FIND:correct-port+IP]
[SAY:"做好了！打开这个网址看看效果：http://你的IP:端口"]
[IF:not-loading]=>[CHECK:firewall+port-conflict+process-error]
[ENSURE]bind=0.0.0.0(not-localhost)|firewall=port-open|process=persistent(nohup/screen)
[SAY:"你的产品在运行了。打开浏览器试试，有问题截图给我。"]
