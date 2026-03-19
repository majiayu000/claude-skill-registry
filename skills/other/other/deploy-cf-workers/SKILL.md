---
name: deploy-cf-workers
description: Deploy to Cloudflare Workers. Fast, free tier, global.
---

# CF Workers Deployment

Steps:
1. Write the Worker code
2. Use wrangler CLI to deploy, or guide user to paste in CF dashboard
3. Bind custom domain if user has one
4. Verify it works

Tell user: "部署到Cloudflare了，全球访问速度都很快。免费额度每天10万次请求，正常用完全够。"

If user doesn't have CF account, guide them to create one (free).
