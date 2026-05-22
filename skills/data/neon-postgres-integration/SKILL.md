---
name: neon-postgres-integration
description: "Integrate Neon Serverless PostgreSQL using environment-based configuration. This skill should be used when setting up Neon PostgreSQL connection, configuring database connection strings, handling environment-based database configuration, managing connection pooling for serverless, troubleshooting database connectivity issues, and planning database migrations with Neon."
---

# Neon PostgreSQL Integration

## Purpose
Integrate Neon Serverless PostgreSQL using environment-based configuration. This skill establishes patterns for connecting to Neon's serverless PostgreSQL, managing connection strings securely, and handling serverless-specific considerations.

## When to Use
- When setting up Neon PostgreSQL connection
- When configuring database connection strings
- When handling environment-based database configuration
- When managing connection pooling for serverless
- When troubleshooting database connectivity issues
- When planning database migrations with Neon

## When NOT to Use
- When using a different database provider
- When working on frontend code without database access
- When designing data models (use relational-data-modeling)
- When the database provider hasn't been confirmed
- When specifications don't require persistent storage

## Required Clarifications
1. What is the Neon PostgreSQL connection string and credentials?
2. What are the specific environment configurations needed?
3. What are the connection pooling requirements for the application?
4. What are the SSL/TLS configuration requirements?

## Optional Clarifications
5. Are there specific performance requirements for database connections?
6. Are there existing database patterns in the codebase to follow?
7. What are the backup and recovery requirements for the database?

## Responsibilities
- Configure Neon connection string from environment
- Set up SQLModel/SQLAlchemy engine for Neon
- Handle serverless connection considerations
- Implement connection pooling if needed
- Secure database credentials management
- Configure SSL/TLS for database connections
- Handle connection timeouts and retries
- Document migration strategy for Neon

## Inputs
- Neon database credentials
- Environment configuration patterns
- SQLModel/SQLAlchemy requirements
- Connection pooling requirements
- SSL certificate requirements

## Outputs
- Database connection configuration
- Environment variable documentation
- Connection string patterns
- Engine/session factory setup
- Connection health check patterns
- Migration tooling configuration

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions |
| **Conversation** | User's specific requirements |
| **Skill References** | Domain patterns from `references/` |
| **User Guidelines** | Project-specific conventions |

## Implementation Workflow
1. Assess Neon PostgreSQL integration requirements
2. Configure connection string from environment
3. Set up SQLModel/SQLAlchemy engine
4. Implement connection pooling considerations
5. Configure SSL/TLS settings
6. Set up connection health checks
7. Plan migration strategy
8. Test connection and validate configuration
9. Document the setup process

## Output Checklist
- [ ] Neon connection string configured from environment
- [ ] SQLModel/SQLAlchemy engine set up
- [ ] Connection pooling configured appropriately
- [ ] SSL/TLS settings configured
- [ ] Connection health checks implemented
- [ ] Migration tooling configured
- [ ] Security constraints followed

## Constraints
- Never hardcode database credentials in source code
- Never commit connection strings to version control
- Never disable SSL for production connections
- Never ignore connection timeout settings
- Always use environment variables for credentials
- Always validate connection on application startup
- Always handle connection failures gracefully

## Interaction With Other Skills
- **sqlmodel-design:** Provides database engine for SQLModel operations
- **python-backend-structure:** Fits within backend configuration module
- **fastapi-architecture:** Integrates with FastAPI dependency injection
- **relational-data-modeling:** Supports defined relationships in Neon
- **constraint-enforcement:** Ensures secure credential handling

## Anti-Patterns
- **Credential exposure:** Hardcoding or logging database passwords
- **SSL bypass:** Disabling SSL for convenience
- **Connection leak:** Not properly closing database connections
- **Timeout ignore:** Not configuring appropriate timeout values
- **Single connection:** Not handling connection pooling for scale
- **Environment confusion:** Mixing development and production credentials
- **Migration skip:** Not planning for schema migrations

## Security Best Practices
- Use environment variables for all database credentials
- Implement proper SSL/TLS encryption for all connections
- Configure appropriate connection timeouts to prevent hanging connections
- Implement connection pooling to manage serverless limitations
- Validate and sanitize all database inputs
- Use parameterized queries to prevent SQL injection

## Documentation Resources
- [Neon PostgreSQL Documentation](https://neon.tech/docs)
- [PostgreSQL Connection String Reference](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
- [SQLAlchemy PostgreSQL Configuration](https://docs.sqlalchemy.org/en/20/dialects/postgresql/)
- [Python Database Security Best Practices](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/05-Authorization_Testing/01-Testing_for_Bypassing_Authorization_Schema.html)

## Phase Applicability
Phase II only. Phase I uses in-memory storage without external database.