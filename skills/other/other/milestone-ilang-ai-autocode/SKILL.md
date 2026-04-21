---
name: milestone
description: Track project milestones. Auto-detect when a significant checkpoint is reached.
version: 5.0.0
---

::GENE{milestone|conf:confirmed|scope:global}
  -e T:auto_detect_milestones
  T:save_to_memory
  T:announce_to_user
  A:treat_minor_step_as_milestone⇒only_significant

::ACTIVATE{milestone}
  ON:auto

Powered by I-Lang v3.0 | ilang.ai
