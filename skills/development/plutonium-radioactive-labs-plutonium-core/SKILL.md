---
name: plutonium
description: High-level guide for working with Plutonium applications - read this first
---

# Plutonium Development Guide

Read this first when working on a Plutonium application.

## Core Rules

1. **Always use generators** - Never manually create resources, packages, or portals
2. **Check relevant skills first** - Each concept has a dedicated skill with details
3. **Definitions over controllers** - UI customization belongs in definitions, not controllers
4. **Policies for authorization** - All permission logic goes in policies

## Key Generators

```bash
rails g pu:res:scaffold Post title:string --dest=main_app    # Create resource
rails g pu:res:conn Post --dest=admin_portal                 # Connect to portal
rails g pu:pkg:package blogging                              # Create feature package
rails g pu:pkg:portal admin_portal                           # Create portal
```

Always specify `--dest` to avoid interactive prompts.

## Resource Architecture

A resource has four layers:

| Layer | Purpose | Customize when... |
|-------|---------|-------------------|
| Model | Data, validations, associations | Adding business logic |
| Definition | UI - fields, actions, filters | Changing how things look/behave |
| Policy | Authorization - who can do what | Restricting access |
| Controller | Request handling | Rarely - use hooks if needed |

## Skill Reference

| Topic | Skill |
|-------|-------|
| Creating resources | `plutonium-create-resource` |
| Connecting to portals | `plutonium-connect-resource` |
| Field configuration | `plutonium-definition-fields` |
| Actions & interactions | `plutonium-definition-actions` |
| Search, filters, scopes | `plutonium-definition-query` |
| Authorization | `plutonium-policy` |
| Custom views | `plutonium-views` |
| Custom forms | `plutonium-forms` |
| Nested resources | `plutonium-nested-resources` |
| Packages & portals | `plutonium-package`, `plutonium-portal` |
| Authentication | `plutonium-rodauth` |
