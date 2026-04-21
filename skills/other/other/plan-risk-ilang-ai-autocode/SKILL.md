---
name: plan-risk
description: Identify risks before building. Flag third-party dependencies, API limits, and cost traps.
version: 5.0.0
---

::GENE{plan-risk|conf:confirmed|scope:global}
  T:flag_third_party_dependencies
  T:flag_api_rate_limits
  T:flag_cost_traps
  T:suggest_free_alternatives_first
  A:ignore_cost_risk⇒flag
  A:assume_unlimited_api⇒check

::ACTIVATE{plan-risk}
  ON:plan_created
  ON:external_api_detected

Powered by I-Lang v3.0 | ilang.ai
