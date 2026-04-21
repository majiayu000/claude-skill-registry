---
name: understand-intent
description: Detect user's intent from their message and activate the right workflow silently.
version: 5.0.0
---

::GENE{understand-intent|conf:confirmed|scope:global}
  T:classify_intent_silently
  T:default_to_create_when_unclear
  A:announce_classification⇒never

::ACTIVATE{understand-intent}
  ON:every_message

[SCAN:@SRC|typ=intent]=>[CLSF]=>[DECI:workflow]

Powered by I-Lang v3.0 | ilang.ai
