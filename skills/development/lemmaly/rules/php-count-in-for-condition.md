---
id: php-count-in-for-condition
title: count() in for-condition — recomputed every iteration
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: php
tags: php, warning, complexity-cuts
---

# count() in for-condition — recomputed every iteration

PHP recomputes the loop condition every iteration. `count($a)` on a 100k-element array, called 100k times, is 10B element traversals. Hoist it.

## Fix

Hoist: `for ($i = 0, $n = count($a); $i < $n; $i++)`. Or use `foreach`.

## Incorrect

```php
<?php
for ($i = 0; $i < count($a); $i++) {
  echo $a[$i];
}
```

## Correct

```php
<?php
// Hoist the length
for ($i = 0, $n = count($a); $i < $n; $i++) {
  echo $a[$i];
}

// Or, idiomatic
foreach ($a as $x) {
  echo $x;
}
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
