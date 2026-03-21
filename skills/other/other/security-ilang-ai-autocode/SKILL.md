---
name: security
description: "[CHECK:security|auto=true|ask-user=false]=>[APPLY:checklist]"
---
[APPLY:auto|ask-user=never]
no-hardcoded-secrets|input-validation|parameterized-queries|XSS-escape
HTTPS-only|httpOnly-secure-tokens|file-upload-restrict|rate-limit-login+API
error-msg-no-internal-details
[USER:"安全吗?"]=>[SAY:"我做了防攻击处理，包括防注入、防跨站攻击、密码加密存储。正常使用不用担心安全问题。"]
