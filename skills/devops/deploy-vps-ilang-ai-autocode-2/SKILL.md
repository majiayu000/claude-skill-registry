---
name: deploy-vps
description: Deploy to VPS. Code is already on the server. Start the service, configure nginx, verify accessible.
version: 5.0.0
---

::GENE{deploy-vps|conf:confirmed|scope:global}
  T:code_already_on_server
  T:start_service_configure_nginx
  T:verify_accessible_after_deploy
  T:show_user_the_url
  A:deploy_without_verification⇒check_first

::ACTIVATE{deploy-vps}
  ON:build_complete

::EXAMPLE{
  output: "部署好了。打开 http://你的IP 看看效果。"
}

Powered by I-Lang v3.0 | ilang.ai
