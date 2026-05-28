---
name: ufw
description: Uncomplicated Firewall management commands.
---

# ufw

```bash
sudo ufw allow from 192.168.1.0/24 to any port 22
sudo ufw status numbered
sudo ufw insert 1 deny from 192.168.1.0/24 to any port 80,443 proto tcp
sudo ufw delete 1
```