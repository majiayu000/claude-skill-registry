---
name: convex-security-check
description: Quick Convex security pass for auth, validation, exposure, and access-control mistakes.
version: 1.0.0
metadata:
  author: agentforge
  source: waynesutton/convexskills and upstream Convex rules
---

# Convex Security Check

Use this for a fast security-oriented pass before deeper review.

## Checklist

- public functions reviewed,
- validators present,
- auth checks present where needed,
- authorization checks enforce ownership or membership,
- secrets stay out of code and unsafe runtimes,
- internal functions are used for privileged flows.
