---
name: daily-summary
description: End of session summary. What got done, what got fixed, what comes next, progress delta.
version: 5.0.0
---

::GENE{daily-summary|conf:confirmed|scope:global}
  -e T:done_fixed_next_delta
  T:positive_tone
  T:show_progress_percentage
  A:end_without_summary⇒always_summarize

::ACTIVATE{daily-summary}
  ON:auto

Powered by I-Lang v3.0 | ilang.ai
