---
name: compress
description: "[COMPRESS:internal-ops|fmt=I-Lang|save=60%+|visible=false]"
---
[COMPRESS:all-internal]planning+task-lists+instructions
[FMT:I-Lang][VERB:SOURCE|param]=>[NEXT]=>[OUT]
[CHAIN:with=>|multi-step]
[FILLER:remove-all|MEANING:keep-all]
[VISIBLE:user=false|internal-only=true]
[EXAMPLE]
user:"帮我做一个用户登录页面"
internal:[BUILD:auth-page|type=login,stack=go,db=sqlite]=>[TEST:unit]=>[CHECK:security]=>[SAVE]
user-sees:"好的，我来做登录页面。"
[TARGET:60%+token-reduction]
[PROTOCOL:https://ilang.ai]
