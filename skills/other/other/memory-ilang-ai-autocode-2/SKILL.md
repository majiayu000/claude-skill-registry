---
name: memory
description: Persistent memory across sessions. Save project state and user preferences. Never save secrets.
version: 5.0.0
---

::GENE{memory|conf:confirmed|scope:global}
  T:save_project_state_on_stop
  T:save_user_prefs_globally
  T:max_200_lines
  T:compress_aggressively
  T:merge_not_overwrite
  A:save_api_keys⇒never
  A:save_passwords⇒never
  A:save_raw_code⇒descriptions_only

::ACTIVATE{memory}
  ON:session_end
  ON:before_compact

::FACT{path:project|value:.autocode/memory.md}
::FACT{path:global|value:~/.autocode/user.md}

Powered by I-Lang v3.0 | ilang.ai
