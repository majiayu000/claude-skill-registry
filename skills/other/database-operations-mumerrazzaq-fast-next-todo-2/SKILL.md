---
name: database-operations
description: A skill for performing database CRUD operations following best practices. Includes guidance on session management, query building (filters, joins, aggregations), transaction handling, bulk operations, error handling, connection pooling, and query optimization. Provides reusable templates for database session dependencies, CRUD service classes, and transaction context managers.
---

# Database Operations

## Overview

This skill provides a set of best practices and reusable templates for common database operations in Python, primarily using SQLAlchemy. It is designed to help you build robust, efficient, and maintainable data access layers.

This skill follows the "Progressive Disclosure" design principle. This main file provides a high-level overview, and the `references/` directory contains detailed documentation and code examples for each topic.

## Core Concepts & Reference Guides

- **Session Management**: Learn how to manage database sessions effectively, including a dependency injection pattern for web frameworks.
  - See [references/session-management.md](./references/session-management.md)

- **CRUD Service Layer**: A generic base class for creating, reading, updating, and deleting records. This promotes code reuse and a consistent API for data access.
  - See [references/crud-service.md](./references/crud-service.md)

- **Transaction Handling**: A context manager to ensure that a series of operations are treated as a single, atomic unit of work.
  - See [references/transactions.md](./references/transactions.md)

- **Querying Techniques**: Examples of how to build more complex queries, including filtering, joins, aggregations, and high-performance bulk operations.
  - See [references/query-examples.md](./references/query-examples.md)

- **Advanced Topics**: Guidance on handling common database errors, configuring the connection pool, and essential query optimization techniques to avoid performance bottlenecks.
  - See [references/advanced-topics.md](./references/advanced-topics.md)
