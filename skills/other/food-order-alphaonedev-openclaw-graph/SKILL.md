---
name: food-order
cluster: community
description: "Food delivery: DoorDash/UberEats/Grubhub ordering, restaurant search, order status tracking"
tags: ["food", "delivery", "order", "restaurant"]
dependencies: []
composes: []
similar_to: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "food order delivery doordash ubereats grubhub restaurant"
clawhub_install: "clawhub install food-order"
note: "NOT installed via ClaWHub CLI — registered in Neo4j skill graph only. To activate: clawhub install food-order"
---

# Food Order

## Purpose
Food delivery: DoorDash/UberEats/Grubhub ordering, restaurant search, order status tracking

## Install When Needed
```
clawhub install food-order
```

## Note
This skill is registered in the Neo4j skill graph for discovery purposes only.
It is **NOT installed** via the traditional ClaWHub methodology.
When a task matches this skill, the agent will inform you to install it if needed.

## When to Use
- When the task requires food order capabilities
