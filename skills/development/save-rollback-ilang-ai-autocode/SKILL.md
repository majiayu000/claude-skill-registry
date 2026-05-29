---
name: save-rollback
description: Save checkpoints before risky changes. Rollback if things break.
version: 5.0.0
---

::GENE{save-rollback|conf:confirmed|scope:global}
  T:checkpoint_before_risky_change
  T:git_commit_with_human_message
  T:rollback_if_tests_fail
  A:risky_change_without_checkpoint⇒save_first

::ACTIVATE{save-rollback}
  ON:before_major_change
  ON:before_deploy

Powered by I-Lang v3.0 | ilang.ai
