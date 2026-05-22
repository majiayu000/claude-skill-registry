---
name: database-design-patterns
description: Database schema design patterns and optimization strategies for relational and NoSQL databases. Use when designing database schemas, optimizing query performance, or implementing data persistence layers at scale.
---

# Database Design Patterns

Expert guidance for designing scalable database schemas, optimizing query performance, and implementing robust data persistence layers across relational and NoSQL databases.

## When to Use This Skill

- Designing database schemas for new applications
- Optimizing slow queries and database performance
- Choosing between normalization and denormalization strategies
- Implementing partitioning, sharding, or replication strategies
- Migrating between database technologies (SQL to NoSQL or vice versa)
- Designing for high availability and disaster recovery
- Implementing caching strategies and read replicas
- Scaling databases horizontally or vertically
- Ensuring data consistency in distributed systems

## Core Concepts

### Data Modeling
Design schemas that reflect business domain, access patterns, and consistency requirements. Balance normalization (data integrity) with denormalization (read performance) based on workload characteristics.

### ACID vs. BASE
- **ACID** (Relational): Atomicity, Consistency, Isolation, Durability - strong guarantees
- **BASE** (NoSQL): Basically Available, Soft state, Eventually consistent - flexibility

### CAP Theorem
Distributed systems choose two of three: Consistency, Availability, Partition Tolerance.

### Polyglot Persistence
Use the right database for each use case: PostgreSQL for transactions, MongoDB for documents, Redis for caching, Elasticsearch for search, Cassandra for time-series, Neo4j for graphs.

## Quick Reference

| Task | Load reference |
| --- | --- |
| Core database principles (ACID, BASE, CAP) | `skills/database-design-patterns/references/core-principles.md` |
| Schema patterns (normalization, star schema, documents) | `skills/database-design-patterns/references/schema-design-patterns.md` |
| Index types and strategies (B-tree, hash, covering) | `skills/database-design-patterns/references/indexing-strategies.md` |
| Partitioning and sharding approaches | `skills/database-design-patterns/references/partitioning-patterns.md` |
| Replication modes (primary-replica, multi-leader) | `skills/database-design-patterns/references/replication-patterns.md` |
| Query optimization and caching | `skills/database-design-patterns/references/query-optimization.md` |

## Workflow

### Phase 1: Requirements Analysis
1. Identify access patterns (read-heavy vs. write-heavy)
2. Determine consistency requirements (strong vs. eventual)
3. Estimate data volume and growth rate
4. Define SLA requirements (latency, availability)

### Phase 2: Schema Design
1. Model entities and relationships
2. Choose normalization level based on workload
3. Design for query patterns, not just storage
4. Consider data distribution strategy (partitioning/sharding)

### Phase 3: Performance Optimization
1. Analyze query execution plans (`EXPLAIN ANALYZE`)
2. Add indexes for frequent queries
3. Implement caching where appropriate
4. Configure connection pooling
5. Monitor and iterate

### Phase 4: Scaling Strategy
1. Implement read replicas for read scaling
2. Consider partitioning for large tables (>100M rows)
3. Plan sharding strategy for horizontal scaling
4. Design for high availability with replication

## Common Mistakes

**Over-normalization**: Too many joins slow down reads. Denormalize for read-heavy workloads.

**Missing indexes**: Analyze query patterns and add indexes for frequent WHERE/JOIN columns.

**Wrong index type**: Use composite indexes with correct column order (equality first, then range).

**Ignoring replication lag**: Handle eventual consistency with read-your-writes pattern.

**Poor partitioning key**: Choose keys that distribute data evenly and align with query patterns.

**N+1 queries**: Use JOINs or batch loading instead of querying in loops.

**Inefficient pagination**: Use keyset pagination instead of OFFSET for large datasets.

**Connection exhaustion**: Implement connection pooling sized for your workload.

## Best Practices

1. **Model for access patterns** - Design schemas around how data will be queried
2. **Index strategically** - Index frequently queried columns, avoid over-indexing
3. **Partition large tables** - Use for tables >100M rows or time-series data
4. **Replicate for reads** - Primary-replica for read scaling, multi-leader for geo-distribution
5. **Optimize queries** - Analyze execution plans, avoid N+1, use proper pagination
6. **Cache hot data** - Application-level caching with appropriate TTLs
7. **Pool connections** - Size connection pools based on workload
8. **Monitor continuously** - Track query performance, index usage, replication lag
9. **Plan for growth** - Design for 3x current load
10. **Choose consistency wisely** - Match consistency level to business requirements

## Resources

**Books**:
- "Designing Data-Intensive Applications" (Kleppmann)
- "High Performance MySQL" (Schwartz)

**Sites**:
- use-the-index-luke.com
- PostgreSQL documentation
- MongoDB documentation

**Tools**:
- EXPLAIN ANALYZE
- pg_stat_statements
- Percona Toolkit
- pt-query-digest
