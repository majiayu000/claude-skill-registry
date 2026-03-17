---
name: comments-explain-why
description: "Good comments explain: business rules (\"Tax is calculated differently for EU customers due to VAT... Use when documenting code and APIs. Documentation category skill."
metadata:
  category: Documentation
  priority: high
  is-built-in: true
  session-guardian-id: builtin_comments_explain_why
---

# Comments Explain Why

Good comments explain: business rules ("Tax is calculated differently for EU customers due to VAT regulations"), workarounds ("Using setTimeout because the library has a race condition - see issue #123"), non-obvious decisions ("We use insertion sort here because n is always small and it's faster for nearly-sorted data"). Don't comment what is obvious from the code itself.