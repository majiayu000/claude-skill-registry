---
name: ngrok
description: Secure tunneling service installation and HTTP tunneling setup.
---

# ngrok

```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
sudo tar -xvzf ./ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin
ngrok config add-authtoken '?'
ngrok http http://localhost:8080
```