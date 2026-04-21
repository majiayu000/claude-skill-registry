---
name: learn-preference
description: Learn user's preferences over time. Code style, naming, structure. Save to global prefs.
version: 5.0.0
---

::GENE{learn-preference|conf:confirmed|scope:global}
  -e T:observe_dont_ask
  T:save_to_global_prefs
  T:apply_silently
  A:override_explicit_instruction⇒user_wins

::ACTIVATE{learn-preference}
  ON:auto

Powered by I-Lang v3.0 | ilang.ai
