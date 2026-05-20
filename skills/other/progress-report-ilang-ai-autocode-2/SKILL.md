---
name: progress-report
description: Report progress after each feature. Percentage, what just completed, what comes next.
version: 5.0.0
---

::GENE{progress-report|conf:confirmed|scope:global}
  -e T:percentage_plus_fraction
  T:just_done_now_remaining
  T:max_3_lines
  T:focus_on_done_not_missing
  A:verbose_report⇒concise

::ACTIVATE{progress-report}
  ON:auto

Powered by I-Lang v3.0 | ilang.ai
