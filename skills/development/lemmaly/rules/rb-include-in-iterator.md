---
id: rb-include-in-iterator
title: Array#include? inside iterator — O(n*m); use Set
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: ruby
tags: ruby, warning, complexity-cuts
---

# Array#include? inside iterator — O(n*m); use Set

`Array#include?` is O(n). Used inside an iterator over m items it is O(n·m). `Set#include?` is O(1).

## Fix

`require 'set'; allowed = Set.new(list); ... allowed.include?(x)`.

## Incorrect

```ruby
# O(n·m)
users.select { |u| banned.include?(u.id) }
```

## Correct

```ruby
# O(n+m)
require 'set'
banned_set = Set.new(banned)
users.select { |u| banned_set.include?(u.id) }
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
