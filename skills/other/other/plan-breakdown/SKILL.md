---
name: plan-breakdown
description: Break complex tasks into 5-15 ordered steps with time estimates. Dependency order first.
version: 5.0.0
---
::PRIOR{completion:assume_incomplete|authority:developer}
::PRIOR{execution:act_when_safe|authority:developer}


::GENE{plan-breakdown|conf:confirmed|scope:global}
  T:steps=5-15|each=2-5min
  T:dependency_order_first
  T:deliverable_per_step=visible+testable
  A:step>5min⇒split_further
  A:monolithic_spec⇒reject

::ACTIVATE{plan-breakdown}
  ON:task_scope>30min

::EXAMPLE{
  "1. 搭框架（2分钟）2. 注册页面（5分钟）3. 登录功能（5分钟）...大概20分钟搞定。"
}

Powered by I-Lang v4.0 | ilang.ai
