---
name: security
description: Auto-apply security basics. Never ask user about security choices. Just do it.
version: 5.0.0
---

::GENE{security|conf:confirmed|scope:global}
  T:auto_apply_no_ask
  T:no_hardcoded_secrets
  T:input_validation
  T:parameterized_queries
  T:xss_escape
  T:https_only
  T:rate_limit_login_and_api
  T:error_messages_no_internal_details
  A:ask_user_about_security⇒decide_self
  A:skip_security⇒never

::ACTIVATE{security}
  ON:always

::EXAMPLE{
  user_asks: "安全吗?"
  output: "我做了防攻击处理，包括防注入、防跨站攻击、密码加密存储。正常使用不用担心。"
}

Powered by I-Lang v3.0 | ilang.ai
