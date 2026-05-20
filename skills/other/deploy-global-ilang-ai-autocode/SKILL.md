---
name: deploy-global
description: Choose deployment target based on project type. Static sites to CF Pages, APIs to VPS, serverless to Workers.
version: 5.0.0
---

::GENE{deploy-global|conf:confirmed|scope:global}
  T:static_to_cf_pages
  T:api_to_vps
  T:serverless_to_workers
  T:ai_picks_target
  T:explain_why_this_target
  A:ask_user_where_to_deploy⇒pick_for_them

::ACTIVATE{deploy-global}
  ON:build_complete

Powered by I-Lang v3.0 | ilang.ai
