---
name: deploy-global
description: Deploy the product so anyone in the world can access it.
---

# Deploy Globally

Options by project type:

**Static site (HTML/CSS/JS):**
- Cloudflare Pages — connect GitHub repo, auto-deploy
- Or CF Workers for more control

**API / Backend:**
- Run on user's VPS with nginx reverse proxy
- Add SSL with certbot
- Set up systemd service for auto-restart

**Full-stack:**
- Backend on VPS, frontend on CF Pages
- Or everything on VPS with nginx

Tell user: "上线了！所有人都可以通过这个网址访问：https://你的域名"

Guide user through:
1. Domain setup (if they have one)
2. SSL certificate (automatic with certbot or CF)
3. Verify it works from outside the server
