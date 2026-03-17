---
name: transport-security
description: Use HTTPS for all endpoints, including internal services Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_transport_security
---

# Transport Security

Use HTTPS for all endpoints, including internal services. Implement HSTS headers to prevent downgrade attacks. Use TLS 1.2 or higher with secure cipher suites. Validate SSL certificates properly—don't disable verification in production. Set secure cookie flags. Consider certificate pinning for mobile apps. Use secure WebSocket (wss://) for real-time connections.