---
name: fix-observe
description: Step 1 of debugging: observe the symptom carefully before jumping to conclusions.
version: 5.0.0
---

::GENE{fix-observe|conf:confirmed|scope:global}
  -e T:read_error_first
  T:check_logs
  T:reproduce_if_possible
  A:guess_without_data⇒observe_first

::ACTIVATE{fix-observe}
  ON:debugging

Powered by I-Lang v3.0 | ilang.ai
