---
name: secure-dependencies
description: Regularly audit dependencies for known vulnerabilities (npm audit, Snyk, Dependabot) Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_secure_dependencies
---

# Secure Dependencies

Regularly audit dependencies for known vulnerabilities (npm audit, Snyk, Dependabot). Keep dependencies updated, especially security patches. Pin dependency versions for reproducible builds. Review new dependencies before adding—consider maintenance status, known issues, and necessity. Minimize the number of dependencies. Use lock files to prevent supply chain attacks.