---
id: rb-n-plus-one-activerecord
title: ActiveRecord iteration touching an association — N+1 without includes
severity: error
impact: CRITICAL
impactDescription: Will break or scale-fail in production
language: ruby
tags: ruby, error, complexity-cuts
---

# ActiveRecord iteration touching an association — N+1 without includes

Iterating an ActiveRecord scope and touching an association fires one extra query per row. `includes` (preload or eager_load) fetches everything in a constant number of queries.

## Fix

Use `Model.includes(:assoc)` or `:preload` / `:eager_load` before iterating.

## Incorrect

```ruby
# N+1 queries
Post.all.each do |p|
  puts p.author.name # 1 extra query per post
end
```

## Correct

```ruby
# 2 queries total (or 1 with eager_load)
Post.includes(:author).each do |p|
  puts p.author.name
end
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
