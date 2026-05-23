---
name: acli
description: Atlassian CLI tool installation and authentication.
---

# acli

```bash
curl -LO "https://acli.atlassian.com/linux/latest/acli_linux_amd64/acli"
chmod +x ./acli
sudo install -o root -g root -m 0755 acli /usr/local/bin/acli
acli rovodev auth login
```