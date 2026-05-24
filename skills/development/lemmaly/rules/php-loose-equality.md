---
id: php-loose-equality
title: == / != — loose equality has surprising coercions
severity: info
impact: MEDIUM
impactDescription: Suboptimal; flag when n is large or on a hot path
language: php
tags: php, info, invariant-guard
---

# == / != — loose equality has surprising coercions

PHP `==` does type coercion in surprising ways (`"0" == false` is `true`, `"abc" == 0` was `true` before PHP 8). `===` compares value AND type — no surprises.

## Fix

Use `===` / `!==` unless type-juggling is explicitly intended (with a comment).

## Incorrect

```php
<?php
if ($status == 0) { /* matches "", "0", false, null, 0, "abc" pre-PHP 8 */ }
```

## Correct

```php
<?php
if ($status === 0) { /* matches only int 0 */ }
```

## Escalate to

If this pattern is widespread in the codebase, load **invariant-guard** for the corrective workflow.
