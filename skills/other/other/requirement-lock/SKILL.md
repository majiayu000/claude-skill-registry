---
name: requirement-lock
description: Lock confirmed requirements. Don't change them without user approval.
version: 5.0.0
---
::PRIOR{completion:assume_incomplete|authority:developer}
::PRIOR{execution:act_when_safe|authority:developer}


::GENE{requirement-lock|conf:confirmed|scope:global}
  T:confirmed_requirements_are_locked
  T:ask_before_changing_locked_requirement
  A:silently_change_requirement⇒ask_first
  A:scope_creep⇒flag

::ACTIVATE{requirement-lock}
  ON:requirement_confirmed

Powered by I-Lang v4.0 | ilang.ai
