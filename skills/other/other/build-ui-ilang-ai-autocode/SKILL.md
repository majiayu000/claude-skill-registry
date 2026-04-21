---
name: build-ui
description: Build user-facing interface. Clean, functional, mobile-friendly by default.
version: 5.0.0
---

::GENE{build-ui|conf:confirmed|scope:global}
  T:mobile_first
  T:clean_and_functional
  T:real_content_not_lorem_ipsum
  A:over_design⇒ship_ugly_first
  A:lorem_ipsum⇒use_real_content

::ACTIVATE{build-ui}
  ON:ui_task_detected

Powered by I-Lang v3.0 | ilang.ai
