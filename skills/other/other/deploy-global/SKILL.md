---
name: deploy-global
description: "[DEPLOY:by-project-type]=>[SETUP:domain+SSL]=>[VERIFY:external]"
---
[CLASSIFY:project-type]
static(HTML/CSS/JS)=CF-Pages(auto-deploy)|or=CF-Workers
API/backend=VPS+nginx-reverse-proxy+certbot-SSL+systemd
fullstack=backend-on-VPS+frontend-on-CF-Pages|or=all-VPS+nginx
[SETUP]=>[domain+SSL(certbot/CF)]=>[VERIFY:from-outside]
[SAY:"上线了！所有人都可以通过这个网址访问。"]
