---
name: fix-explain
description: After fixing a bug, explain what went wrong in language the user understands. No jargon for beginners.
version: 5.0.0
---

::GENE{fix-explain|conf:confirmed|scope:global}
  T:explain_after_fix_not_during
  T:one_sentence_for_beginners
  T:technical_detail_for_advanced
  T:always_say_its_fixed_first
  A:raw_error_messages⇒translate
  A:blame_user⇒never

::ACTIVATE{fix-explain}
  ON:fix_complete

::EXAMPLE{
  beginner: "修好了。之前有个小配置写错了，现在正常了。"
  advanced: "Fixed. The middleware order was wrong — auth must register before route handlers."
}

Powered by I-Lang v3.0 | ilang.ai
