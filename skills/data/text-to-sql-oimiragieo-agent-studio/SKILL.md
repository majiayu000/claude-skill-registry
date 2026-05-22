---
name: text-to-sql
description: Convert natural language queries to SQL. Use for database queries, data analysis, and reporting.
allowed-tools: read, write, grep, glob
version: 1.0
best_practices:
  - Provide database schema context
  - Validate SQL before execution
  - Use parameterized queries
  - Test queries on sample data
error_handling: graceful
streaming: supported
---

# Text-to-SQL Skill

## Identity

Text-to-SQL - Converts natural language queries to SQL using database schema context and query patterns.

## Capabilities

- **Query Generation**: Convert natural language to SQL
- **Schema Awareness**: Uses database schema for accurate queries
- **Query Optimization**: Generates optimized SQL queries
- **Parameterized Queries**: Creates safe, parameterized queries

## Usage

### Basic SQL Generation

**When to Use**:

- Database queries from natural language
- Data analysis requests
- Reporting queries
- Ad-hoc database queries

**How to Invoke**:

```
"Generate SQL to find all users who signed up in the last month"
"Create a query to calculate total revenue by product"
"Write SQL to find duplicate records"
```

**What It Does**:

- Analyzes natural language query
- References database schema
- Generates SQL query
- Validates query syntax
- Returns parameterized query

### Advanced Features

**Schema Integration**:

- Loads database schema
- Understands table relationships
- Uses column types and constraints
- Handles joins and aggregations

**Query Optimization**:

- Generates efficient queries
- Uses appropriate indexes
- Optimizes joins
- Minimizes data transfer

**Safety**:

- Parameterized queries (prevents SQL injection)
- Validates query syntax
- Tests on sample data
- Error handling

## Best Practices

1. **Schema Context**: Provide complete database schema
2. **Query Validation**: Validate SQL before execution
3. **Parameterization**: Always use parameterized queries
4. **Testing**: Test queries on sample data
5. **Optimization**: Review query performance

## Integration

### With Database Architect

Text-to-SQL uses schema from database-architect:

- Table definitions
- Relationships
- Constraints
- Indexes

### With Developer

Text-to-SQL generates queries for developers:

- Query templates
- Parameterized queries
- Query optimization
- Error handling

## Examples

### Example 1: Simple Query

```
User: "Find all users who signed up in the last month"

Text-to-SQL:
1. Analyzes query
2. References users table schema
3. Generates SQL:
   SELECT * FROM users
   WHERE created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
4. Returns parameterized query
```

### Example 2: Complex Query

```
User: "Calculate total revenue by product for Q4"

Text-to-SQL:
1. Analyzes query
2. References orders and products tables
3. Generates SQL:
   SELECT p.name, SUM(o.total) as revenue
   FROM orders o
   JOIN products p ON o.product_id = p.id
   WHERE o.created_at >= '2024-10-01'
     AND o.created_at < '2025-01-01'
   GROUP BY p.id, p.name
4. Returns optimized query
```

## Evaluation

### Evaluation Framework

Based on Claude Cookbooks patterns, text-to-SQL evaluation includes:

**Syntax Validation**:

- SQL syntax correctness
- Schema compliance
- Query structure validation

**Functional Testing**:

- Query execution on test database
- Result correctness
- Performance validation

**Promptfoo Integration**:

- Multiple prompt variants (basic, few-shot, chain-of-thought, RAG)
- Temperature sweeps
- Model comparisons (Haiku vs Sonnet)

**Evaluation Configuration**:
See `.claude/evaluation/promptfoo_configs/text_to_sql_config.yaml` for complete evaluation setup.

### Running Evaluations

```bash
# Run text-to-SQL evaluation
npx promptfoo@latest eval -c .claude/evaluation/promptfoo_configs/text_to_sql_config.yaml
```

### Evaluation Metrics

- **Syntax Accuracy**: Percentage of queries with valid SQL syntax
- **Functional Correctness**: Percentage of queries returning correct results
- **Schema Compliance**: Percentage of queries using correct schema
- **Performance**: Query execution time and optimization

## Best Practices from Cookbooks

### 1. Provide Schema Context

Always include complete database schema:

- Table definitions with column types
- Relationships and foreign keys
- Constraints and indexes
- Sample data patterns

### 2. Use Few-Shot Examples

Provide examples of similar queries:

- Simple queries
- Complex queries with joins
- Aggregation queries
- Subquery patterns

### 3. Chain-of-Thought for Complex Queries

For complex queries, use chain-of-thought reasoning:

- Break down query into steps
- Identify required tables
- Plan joins and aggregations
- Generate SQL step by step

### 4. RAG for Schema Understanding

Use RAG to retrieve relevant schema information:

- Find relevant tables for query
- Understand relationships
- Get column details
- Retrieve query patterns

## Related Skills

- **classifier**: Classify database queries
- **database-architect**: Use for schema design
- **developer**: Generate query code

## Related Documentation

- [Classification Patterns](../docs/CLASSIFICATION_PATTERNS.md) - Classification guide
- [Evaluation Guide](../docs/EVALUATION_GUIDE.md) - Comprehensive evaluation
- [Claude Cookbooks - Text-to-SQL](https://github.com/anthropics/anthropic-cookbook/tree/main/capabilities/text_to_sql)
