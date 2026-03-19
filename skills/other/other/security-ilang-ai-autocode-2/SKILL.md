---
name: security
description: Protect the user's product from common attacks. Do this automatically.
---

# Security

Apply automatically during building. Never ask user about security — just do it.

Checklist:
- [ ] No hardcoded passwords, API keys, or secrets in code
- [ ] All user input is validated and sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (escape HTML output)
- [ ] HTTPS only (no HTTP)
- [ ] Authentication tokens are httpOnly and secure
- [ ] File uploads are restricted by type and size
- [ ] Rate limiting on login and API endpoints
- [ ] Error messages don't leak internal details

If user asks "安全吗？" — answer: "我做了防攻击处理，包括防注入、防跨站攻击、密码加密存储。正常使用不用担心安全问题。"
