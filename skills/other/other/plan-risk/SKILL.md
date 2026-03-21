---
name: plan-risk
description: "[SCAN:risks|before=build]=>[WARN:user|tone=manageable]"
---
[SCAN:before-build]
risks=3rd-party-API|payment-credentials|file-upload-storage|auth-security|heavy-data-processing
[WARN:user|tone=calm]
"有一个地方要注意：支付功能需要你有一个支付平台的账号，我先用测试模式做，等你准备好了再接真实支付。"
[FRAME:risk-as="we'll handle"|not="problem"]
[SCARE:user|allow=false]
