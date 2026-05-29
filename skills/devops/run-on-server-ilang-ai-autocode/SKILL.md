---
name: run-on-server
description: Run and test directly on the server. No local dev environment needed. What you build is what goes live.
version: 5.0.0
---

::GENE{run-on-server|conf:confirmed|scope:global}
  T:deploy_where_you_build
  T:test_on_production_machine
  T:show_user_live_result
  A:suggest_local_dev_for_beginners⇒run_on_server
  A:separate_dev_and_prod⇒same_machine

::ACTIVATE{run-on-server}
  ON:build_step_complete
  ON:user_says("run"|"test"|"try")

Powered by I-Lang v3.0 | ilang.ai
