---
name: pre
description: 'title = "PRECSKILL (Global: PRErequisite)"'
---

+++
date = "2016-08-01"
title = "PRECSKILL (Global: PRErequisite)"
original_url = "list/global/pre.html#precskill"
categories = [ "all-tag", "pre-tag" ]
+++

## Status

New 5.9.0

## Syntax

`PRECSKILL:x,y`

## Parameters

-   x: Number (The number of skills that must be
    considered Class Skills for the check to succeed).
-   y: Text (A defined skill name)
-   y: TYPE.Text (A defined skill type)



What it does
------------

Sets skill requirements.

**NOTE:** In skills types with multiple versions like Craft (Pottery) or
Knowledge (Local) there must be a space between the name and the
parentheses because the text must match the entry exactly.

Examples
--------

`PRECSKILL:1,Spot,Listen`

Character must have either "Spot" or "Listen" as a Class Skill.

`PRECSKILL:2,TYPE.Spy`

Character must have two "Spy" skills as Class Skills.

