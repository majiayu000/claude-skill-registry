---
name: deploy-cf-workers
description: Deploy to Cloudflare Workers. Free tier handles 100k requests/day. Global edge network.
version: 5.0.0
---

::GENE{deploy-cf-workers|conf:confirmed|scope:global}
  T:use_wrangler_cli
  T:bind_custom_domain_if_exists
  T:verify_accessible
  T:explain_free_tier
  A:no_cf_account⇒guide_create_free

::ACTIVATE{deploy-cf-workers}
  ON:deploy_target=cloudflare

::EXAMPLE{
  output: "部署到Cloudflare了，全球访问速度都很快。免费额度每天10万次请求，够用了。"
}

Powered by I-Lang v3.0 | ilang.ai
