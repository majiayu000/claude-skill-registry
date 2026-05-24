---
id: php-in-array-in-loop
title: in_array inside loop — O(n*m); use array_flip + isset
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: php
tags: php, warning, complexity-cuts
---

# in_array inside loop — O(n*m); use array_flip + isset

`in_array` is a linear scan. Used inside a loop over m items it is O(n·m). `array_flip + isset` is O(1) per check.

## Fix

`$set = array_flip($haystack); ... isset($set[$x])` is O(1) per check.

## Incorrect

```php
<?php
foreach ($users as $u) {
  if (in_array($u->id, $banned)) continue;
  ship($u);
}
```

## Correct

```php
<?php
$bannedSet = array_flip($banned); // O(n) once
foreach ($users as $u) {
  if (isset($bannedSet[$u->id])) continue; // O(1)
  ship($u);
}
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
