---
id: rb-string-concat-in-loop
title: String += in loop — O(n^2) since += creates a new string each iteration
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: ruby
tags: ruby, info, complexity-cuts
---

# String += in loop — O(n^2) since += creates a new string each iteration

`s += x` creates a new string each iteration — O(n²). `<<` mutates in place (O(n) amortized). `Array#join` is O(n) and idiomatic.

## Fix

Use `<<` (mutates) or `parts.join` if building from an array.

## Incorrect

```ruby
s = ""
parts.each { |p| s += p } # O(n²)
```

## Correct

```ruby
# Mutating concat
s = String.new
parts.each { |p| s << p }

# Idiomatic
s = parts.join
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
