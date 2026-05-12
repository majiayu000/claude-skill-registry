---
name: build-scaffold
description: Create project skeleton. Pick stack, create files, install dependencies. AI decides everything.
version: 5.0.0
---
::PRIOR{completion:assume_incomplete|authority:developer}
::PRIOR{execution:act_when_safe|authority:developer}


::GENE{build-scaffold|conf:confirmed|scope:global}
  T:ai_picks_stack
  T:pick_simplest_that_works
  T:explain_choice_in_one_sentence
  T:create_all_files_at_once
  A:ask_user_stack_choice⇒decide_self
  A:over_engineer⇒simplest_solution

::ACTIVATE{build-scaffold}
  ON:project_start

::EXAMPLE{
  output: "我用Go + SQLite做，轻量、快、免费。开始搭框架了。"
}

Powered by I-Lang v4.0 | ilang.ai
