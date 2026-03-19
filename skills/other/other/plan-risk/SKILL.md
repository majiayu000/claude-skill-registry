---
name: plan-risk
description: Identify potential problems before they happen. Warn the user in plain language.
---

# Risk Warning

Before building, scan for risks:
- Third-party API dependency (might be slow or down)
- Payment integration (needs real credentials to fully test)
- File upload (needs storage space)
- User authentication (security-sensitive)
- Heavy data processing (might be slow on cheap server)

If risks found, tell user simply:
"有一个地方要注意：支付功能需要你有一个支付平台的账号，我先用测试模式做，等你准备好了再接真实支付。"

Never scare the user. Frame risks as "things we'll handle" not "problems."
