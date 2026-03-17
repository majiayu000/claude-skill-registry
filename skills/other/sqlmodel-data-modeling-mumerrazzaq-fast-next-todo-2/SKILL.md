---
name: sqlmodel-data-modeling
description: Guide for ORM-based data modeling with SQLModel. Use for defining database models, fields, constraints, relationships (1:N, N:M), inheritance, validators, and handling JSON fields and timestamps. Provides templates for User, Task, and Category models.
---

# SQLModel Data Modeling

This skill provides guidance and code patterns for creating robust and efficient data models using SQLModel.

## Workflow

1.  **Define Basic Models**: Start by defining the basic structure of your models. Refer to `references/model_definition.md` for defining tables, fields, and constraints. It includes templates for `User`, `Task`, and `Category` models.
2.  **Establish Relationships**: Define relationships between your models. See `references/relationships.md` for patterns on creating one-to-many (1:N) and many-to-many (N:M) relationships.
3.  **Implement Advanced Patterns**: For more complex scenarios, consult `references/advanced_patterns.md`. This guide covers model inheritance, a base model with audit timestamp fields, computed properties, and handling of JSON data.
4.  **Add Validation**: Implement data validation to ensure integrity. Examples of model validation using SQLModel's features are in `references/validation.md`.

Always consult the relevant reference document for detailed code examples and best practices for each step.
