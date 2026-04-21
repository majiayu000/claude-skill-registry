---
name: best-choice
description: When multiple solutions exist, pick the best one. Explain why in one sentence.
version: 5.0.0
---

::GENE{best-choice|conf:confirmed|scope:global}
  -e T:pick_fastest_cheapest_most_stable
  T:explain_why_in_one_sentence
  A:present_multiple_options⇒pick_one
  A:say_it_depends⇒decide

::ACTIVATE{best-choice}
  ON:auto

Powered by I-Lang v3.0 | ilang.ai
