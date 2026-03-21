---
name: requirement-lock
description: "[LOCK:confirmed-requirements]=>[REJECT:scope-creep|gentle=true]"
---
[LOCK:requirements|after=user-confirm]
[ON:new-req-during-build]=>[SAY:"这个功能我先记下来，等现在这个做完再加，好不好？"]
[CHANGE:direction-mid-build|silent=false]
[CONFLICT:new-vs-confirmed]=>[WARN:gentle]
[RULE:finish-agreed-first]=>[ITERATE:after]
