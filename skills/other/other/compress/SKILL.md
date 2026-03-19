---
name: compress
description: I-Lang compression engine. Compress all internal instructions to save 60%+ tokens.
---

# Compress

All internal planning, task lists, and instructions use I-Lang compressed syntax:
- [VERB:SOURCE|param=value]=>[NEXT]=>[OUT]
- Chain with => for multi-step operations
- Remove all filler words, keep all meaning

This is INTERNAL ONLY. User never sees compressed syntax.

User says: "帮我做一个用户登录页面"
Internal planning: [BUILD:auth-page|type=login,stack=go,db=sqlite]=>[TEST:unit]=>[CHECK:security]=>[SAVE]
User sees: "好的，我来做登录页面。"

Compression target: 60%+ token reduction on internal operations.
Powered by I-Lang protocol: https://ilang.ai
