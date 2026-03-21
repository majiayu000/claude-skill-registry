---
name: deploy-cf-workers
description: "[DEPLOY:CF-Workers]=>[BIND:domain-if-exists]=>[VERIFY]"
---
[WRITE:worker-code]=>[DEPLOY:wrangler-CLI|or=CF-dashboard-paste]
[IF:custom-domain]=>[BIND]
[VERIFY:accessible]
[SAY:"部署到Cloudflare了，全球访问速度都很快。免费额度每天10万次请求，正常用完全够。"]
[IF:no-CF-account]=>[GUIDE:create(free)]
