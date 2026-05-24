---
id: rb-bare-rescue
title: Bare rescue — catches StandardError, hides bugs
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: ruby
tags: ruby, warning, invariant-guard
---

# Bare rescue — catches StandardError, hides bugs

A bare `rescue` (without a class) catches `StandardError` — including `NoMethodError`, `ArgumentError`, and other bugs you almost always want to surface. Catch the specific class.

## Fix

Catch a specific class: `rescue Net::ReadTimeout` etc. Bare rescue swallows too much.

## Incorrect

```ruby
begin
  fetch_remote
rescue
  retry # also catches typos and bugs in fetch_remote
end
```

## Correct

```ruby
begin
  fetch_remote
rescue Net::ReadTimeout, Net::OpenTimeout => e
  retry
end
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
