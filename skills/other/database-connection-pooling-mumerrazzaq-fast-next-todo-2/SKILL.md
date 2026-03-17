---
name: database-connection-pooling
description: "Configures and manages database connection pools, with a focus on SQLAlchemy. Use this skill for tasks involving connection pool configuration, sizing, lifecycle management, health checks, and monitoring. It provides specialized guidance for both traditional server-based databases and serverless databases like Neon and PlanetScale."
---

# Database Connection Pooling Configuration

## Overview

This skill provides guidance and resources for configuring database connection pools, primarily using Python's SQLAlchemy library. It covers best practices for traditional databases and provides specific advice for modern serverless database architectures.

## Workflow

1.  **Identify Environment**: First, determine if the user's database is a traditional, server-based instance or a serverless one (e.g., Neon, PlanetScale, AWS Aurora Serverless).

2.  **Gather Workload Details**: Ask the user about their application's workload.
    *   For traditional web apps: How many application servers? How many worker processes/threads per server?
    *   For serverless functions: What is the expected concurrency?

3.  **Provide Configuration**: Based on the environment, guide the user to the appropriate reference material.

    *   For **traditional databases**, use `references/sqlalchemy_config.md` to configure a robust connection pool with appropriate sizing and recycling.

    *   For **serverless databases**, use `references/serverless_pooling.md` to learn about the unique challenges and recommended configurations for platforms like Neon and PlanetScale.

4.  **Implement Monitoring**: Once the pool is configured, refer to `references/monitoring.md` for best practices on monitoring pool health and detecting connection leaks. Use the `scripts/generate_dashboard_config.py` script to create a basic monitoring configuration.

## Resources

### `references/sqlalchemy_config.md`
- **Use for**: Configuring connection pools for traditional, server-based databases (e.g., a dedicated PostgreSQL or MySQL server).
- **Contains**: Detailed examples for `create_engine`, pool sizing formulas, and health check patterns.

### `references/serverless_pooling.md`
- **Use for**: Configuring connection pools for serverless database platforms.
- **Contains**: Specific guidance and settings for Neon and PlanetScale, including the use of external poolers like PgBouncer.

### `references/monitoring.md`
- **Use for**: Understanding how to monitor the connection pool and diagnose issues like connection leaks.
- **Contains**: Key metrics to track and instructions for using the `generate_dashboard_config.py` script.

### `scripts/generate_dashboard_config.py`
- **Use for**: Generating a basic JSON configuration for a monitoring dashboard.
- **To run**: `python3 scripts/generate_dashboard_config.py`. The output can be used as a template for setting up monitoring tools.
