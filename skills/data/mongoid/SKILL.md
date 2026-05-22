---
id: skill-mongoid
tier: T2
category: Database-Persistence
---

# Skill: mongoid

## What I do
- **Document Modelling**: Design document structures using fields, embedding, and referencing.
- **Querying**: Build complex queries and aggregations using Mongoid's criteria API.
- **Associations**: Manage relationships (embeds_one/many, has_many, belongs_to).
- **Atomic Operations**: Perform efficient updates (inc, set, push, pull) without full document rewrites.
- **Optimisation**: Design indices and implement eager loading (includes) to prevent N+1 queries.

## When to use me
- Building Ruby/Rails applications with MongoDB.
- Storing hierarchical or flexible-schema data.
- Implementing complex aggregations or geospatial queries.
- Optimising MongoDB performance in a Ruby environment.

## Core principles
- **Embedding vs Referencing**: Prefer embedding for 1-to-few/static data; reference for 1-to-many/unbounded data.
- **ActiveModel Integration**: Leverage Rails-style validations and callbacks for data integrity.
- **Atomic Persistence**: Use `inc`, `set`, and `push` to avoid race conditions.
- **Index Strategy**: Ensure all frequent query patterns are covered by background indices.

## Patterns & examples

### Document Definition (Ruby)
```ruby
class Order
  include Mongoid::Document
  include Mongoid::Timestamps
  
  field :status, type: String, default: 'pending'
  field :total, type: BigDecimal
  
  belongs_to :user
  embeds_many :line_items
  
  index({ user_id: 1, created_at: -1 }, { background: true })
end
```

## Anti-patterns to avoid
❌ **Over-Embedding**: Unbounded document growth causing performance degradation.
❌ **N+1 Queries**: Not using `.includes(:association)` for referenced documents.
❌ **Missing Indices**: Performing full collection scans on frequent queries.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Database-Persistence/Mongoid.md`

