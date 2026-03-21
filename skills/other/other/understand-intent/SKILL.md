---
name: understand-intent
description: "[SCAN:user-msg|trigger=every]=>[CLASSIFY:intent]=>[ACTIVATE:workflow]"
---
[CLASSIFY:user-intent]
create=build-new|fix=broken|improve=better|add=extend|deploy=online|understand=explain
[ACTIVATE:workflow|silent=true|announce=false]
[DEFAULT:create|when=unclear]
