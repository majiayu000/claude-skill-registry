---
id: php-query-in-loop
title: DB query inside loop — N+1
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: php
tags: php, error, complexity-cuts
---

# DB query inside loop — N+1

A SQL query inside a loop is the textbook N+1 problem. 1000 orders, 1000 round-trips to the DB. Batch with `WHERE id IN (...)` or eager-load in your ORM.

## Fix

Collect the ids, run ONE `WHERE id IN (...)` query, index by id, then loop. In Eloquent use eager loading: `Model::with('relation')`.

## Incorrect

```php
<?php
foreach ($orderIds as $id) {
  $row = $db->query("SELECT * FROM orders WHERE id = $id"); // 1 query per id
  process($row);
}
```

## Correct

```php
<?php
// One bulk query
$placeholders = implode(',', array_fill(0, count($orderIds), '?'));
$stmt = $db->prepare("SELECT * FROM orders WHERE id IN ($placeholders)");
$stmt->execute($orderIds);
foreach ($stmt->fetchAll() as $row) {
  process($row);
}

// Eloquent / Doctrine: use eager loading
$orders = Order::with('items')->whereIn('id', $orderIds)->get();
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
