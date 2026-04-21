---
name: fix-guide
description: Guide user through errors they see. Translate error messages to human language.
version: 5.0.0
---

::GENE{fix-guide|conf:confirmed|scope:global}
  -e T:translate_error_to_human
  T:tell_user_what_to_copy_paste
  A:show_raw_error⇒translate

::ACTIVATE{fix-guide}
  ON:debugging

Powered by I-Lang v3.0 | ilang.ai
