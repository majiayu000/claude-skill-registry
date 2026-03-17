---
name: xss-prevention
description: Encode output appropriately for the context (HTML, JavaScript, CSS, URL) Use when implementing security best practices. Security category skill.
metadata:
  category: Security
  priority: high
  is-built-in: true
  session-guardian-id: builtin_xss_prevention
---

# XSS Prevention

Encode output appropriately for the context (HTML, JavaScript, CSS, URL). Use framework-provided escaping mechanisms (React's JSX, template engine auto-escaping). Avoid innerHTML, dangerouslySetInnerHTML, and similar APIs unless absolutely necessary and content is sanitized. Implement Content Security Policy (CSP) headers. Validate and sanitize user-generated content, especially rich text or markdown.