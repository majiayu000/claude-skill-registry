---
name: build-feature
description: Build one feature at a time. Complete each fully before moving to next. Auto-triggers quality check.
version: 5.0.0
---

::GENE{build-feature|conf:confirmed|scope:global}
  T:one_feature_at_a_time
  T:sequential_not_concurrent
  T:verify_before_next
  T:report_completion_in_user_language
  A:parallel_features⇒reject
  A:skip_verification⇒reject
  when:feature_too_big ⇒ ::ACTIVATE{plan-breakdown}

::ACTIVATE{build-feature}
  ON:plan_approved

::EXAMPLE{
  output: "登录功能做好了。用户可以注册、登录、登出。"
  progress: "✅ 3/5 完成，还剩2步。"
}

Powered by I-Lang v3.0 | ilang.ai
