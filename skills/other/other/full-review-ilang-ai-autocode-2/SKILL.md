---
name: full-review
description: Full project review from beginning. Check every file. Plain language report.
version: 5.0.0
---

::GENE{full-review|conf:confirmed|scope:global}
  T:review_every_file
  T:report_in_user_language
  T:check_logic_edges_security_hardcoded
  T:human_readable_commit_messages
  A:partial_review⇒full_review
  A:skip_on_save⇒never

::ACTIVATE{full-review}
  ON:before_save
  ON:before_deploy
  ON:session_end

Powered by I-Lang v3.0 | ilang.ai
