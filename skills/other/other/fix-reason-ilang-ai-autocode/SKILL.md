---
name: fix-reason
description: Step 2 of debugging: reason about root cause based on observed symptoms.
version: 5.0.0
---

::GENE{fix-reason|conf:confirmed|scope:global}
  -e T:binary_search_for_cause
  T:check_recent_changes_first
  A:blame_random_component⇒systematic

::ACTIVATE{fix-reason}
  ON:debugging

Powered by I-Lang v3.0 | ilang.ai
