---
name: auto-quality
description: Silent quality check after every feature. Fix issues before telling user. Never claim tests passed without running them.
version: 5.0.0
---

::GENE{auto-quality|conf:confirmed|scope:global}
  T:check_after_every_feature
  T:silent_fix_if_minor
  T:run_tests_if_framework_exists
  A:claim_tests_passed_without_running⇒reject
  A:announce_checking⇒silent
  A:say_tests_failed⇒fix_first_then_report

::ACTIVATE{auto-quality}
  ON:feature_complete

Powered by I-Lang v3.0 | ilang.ai
