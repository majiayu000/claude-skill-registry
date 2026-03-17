---
name: avoid-abbreviations
description: "Write \"customer\" not \"cust\", \"configuration\" not \"cfg\", \"temporary\" not \"tmp\" Use when maintaining consistent code style. Style category skill."
metadata:
  category: Style
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_avoid_abbreviations
---

# Avoid Abbreviations

Write "customer" not "cust", "configuration" not "cfg", "temporary" not "tmp". Common abbreviations like "id", "url", "api" are acceptable. Abbreviations force readers to decode meaning. Full words are more searchable. The extra typing is minimal with autocomplete. Exception: very short scopes like loop counters (i, j) or conventional short names in specific domains.