---
name: fix-auto
description: Auto-fix bugs. Observe symptom, find root cause, apply minimal fix, verify, explain in human terms.
version: 5.0.0
---

::GENE{fix-auto|conf:confirmed|scope:global}
  T:observe_first_then_reason_then_fix
  T:minimal_change
  T:verify_fix_works
  T:explain_what_was_wrong_in_human_terms
  A:refactor_during_fix⇒separate_task
  A:show_raw_error_to_beginner⇒translate

::ACTIVATE{fix-auto}
  ON:error_detected
  ON:user_reports_problem

Powered by I-Lang v3.0 | ilang.ai
