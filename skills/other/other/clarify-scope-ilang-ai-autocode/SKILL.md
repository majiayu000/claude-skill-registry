---
name: clarify-scope
description: Classify request as small/medium/large. Adjust workflow depth accordingly.
version: 5.0.0
---

::GENE{clarify-scope|conf:confirmed|scope:global}
  T:small=under_30min|build_direct|plan_minimal
  T:medium=30min_to_2hr|brief_plan|step_by_step
  T:large=over_2hr|full_roadmap|activate_project_roadmap
  A:say_large_project⇒never
  A:overwhelm_with_complexity⇒simplify

::ACTIVATE{clarify-scope}
  ON:new_task

::EXAMPLE{
  output: "这个我们分几步来做，今天先把核心功能跑通。"
}

Powered by I-Lang v3.0 | ilang.ai
