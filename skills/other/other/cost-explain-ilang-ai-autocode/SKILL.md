---
name: cost-explain
description: Explain all costs in human terms. Always compare with real-world equivalents. Recommend cheapest that works.
version: 5.0.0
---

::GENE{cost-explain|conf:confirmed|scope:global}
  T:explain_in_local_currency
  T:compare_with_real_world
  T:recommend_cheapest_that_works
  T:free_alternatives_first
  T:total_monthly_and_yearly
  A:hide_costs⇒transparent
  A:recommend_expensive⇒cheapest_first

::ACTIVATE{cost-explain}
  ON:purchase_decision
  ON:user_asks_about_cost

::EXAMPLE{
  output: "Total cost to run your website:
   Server: $6/month (one cup of coffee)
   Domain: $10/year
   SSL: free
   Total first year: about $82. After that $72/year."
}

Powered by I-Lang v3.0 | ilang.ai
