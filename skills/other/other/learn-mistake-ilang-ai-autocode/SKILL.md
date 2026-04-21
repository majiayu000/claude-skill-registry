---
name: learn-mistake
description: Record mistakes. Check before similar builds. Avoid repeating silently.
version: 5.0.0
---

::GENE{learn-mistake|conf:confirmed|scope:global}
  -e T:record_what_why_how_fixed
  T:check_before_similar_feature
  T:avoid_silently
  A:say_i_remember_this_mistake⇒just_avoid_it
  A:repeat_known_mistake⇒check_memory

::ACTIVATE{learn-mistake}
  ON:auto

Powered by I-Lang v3.0 | ilang.ai
