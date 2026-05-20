---
name: test-data-generation
description: "Provides patterns and examples for generating test data using factory libraries. Use this skill when you need to create realistic and maintainable test data for your application. It covers factory patterns (e.g., Factory Boy for Python, Polly.js for JavaScript), handling relationships between models, using traits for data variations, sequence generation for unique values, and cleanup strategies. Trigger this skill for tasks involving test fixtures, data seeding for tests, or factory implementation."
---

# Test Data Generation

## Overview

This skill provides guidance and reusable patterns for creating robust and maintainable test data using factory libraries. It focuses on common patterns used in modern testing workflows, with examples primarily for Python (using `factory_boy`) and JavaScript (using `polly.js`).

Following these patterns helps create tests that are easier to read, write, and maintain.

## Core Concepts

The main workflow is to define factories for your data models and then use them in your tests to create instances of those models.

This skill is organized by topic. Refer to the relevant document for detailed patterns and examples.

### 1. Basic Factory and Trait Patterns

For defining basic factories and creating variations using traits (e.g., an `active` user vs. a `suspended` user). This is the best place to start.

**See [references/factory-patterns.md](./references/factory-patterns.md) for detailed examples.**

### 2. Handling Relationships

For creating data with relationships, such as a user who has many posts, or posts that belong to a category (one-to-many, many-to-one, many-to-many).

**See [references/relationship-patterns.md](./references/relationship-patterns.md) for detailed examples.**

### 3. Unique Values and Realistic Data

For ensuring data uniqueness using sequences and for generating realistic-looking data (names, emails, addresses) using Faker.

**See [references/sequence-and-faker.md](./references/sequence-and-faker.md) for detailed examples.**

### 4. Persistence Strategies

For understanding the difference between in-memory object generation and creating records in a test database.

**See [references/persistence.md](./references/persistence.md) for detailed examples.**

### 5. Data Cleanup

For strategies on how to clean up test data between test runs to ensure test isolation.

**See [references/cleanup.md](./references/cleanup.md) for detailed examples.**
