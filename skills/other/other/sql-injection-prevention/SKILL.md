---
name: sql-injection-prevention
description: Always use parameterized queries or prepared statements Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_sql_injection_prevention
---

# SQL Injection Prevention

Always use parameterized queries or prepared statements. Use ORMs or query builders that handle parameterization automatically. Never build SQL strings through concatenation with user input. Apply principle of least privilege to database accounts. Validate and sanitize input even when using parameterized queries as defense in depth.