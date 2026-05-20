---
name: run-local
description: Run the product on the user's VPS so they can see it.
---

# Run Locally

After building:
1. Start the application on the VPS
2. Find the correct port and IP
3. Tell user: "做好了！打开这个网址看看效果：http://你的IP:端口"
4. If it doesn't load, check firewall, port conflicts, process errors

For web apps, make sure:
- The server binds to 0.0.0.0, not just localhost
- The port is open in firewall (iptables)
- The process stays running (use nohup or screen)

Tell user: "你的产品在运行了。打开浏览器试试，有问题截图给我。"
