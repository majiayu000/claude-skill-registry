---
name: documentation-writing
description: Audience-first documentation guidance for READMEs, API docs, architecture docs, and tutorials. Ensures clarity, completeness, and maintainability.
---

# Documentation Writing Skill

## Core Principle

**Write for the reader's context, not the author's understanding.**

Documentation exists to transfer knowledge efficiently. Good documentation anticipates questions, provides context, and guides readers to success. The best documentation makes the next user (or future you) productive without requiring tribal knowledge or guesswork.

**Effective documentation:**
- Meets readers where they are (assumes appropriate background)
- Answers "why" not just "what" and "how"
- Provides working examples
- Stays current with code changes
- Guides readers to success, not just describes features

---

## Documentation Types

Different documentation serves different purposes. Choose the right type for your audience and goal.

### README.md (Project Overview)

**Purpose:** First impression and quick-start guide for new users/contributors

**Audience:**
- New users evaluating the project
- Developers wanting to contribute
- Stakeholders assessing project status

**Must include:**
- What the project does (1-2 sentences)
- Why it exists (problem being solved)
- Quick start (minimal steps to see it working)
- Installation/setup instructions
- Basic usage examples
- Link to fuller documentation
- How to contribute (if open source)
- License information

**Template:**
```markdown
# Project Name

Brief description (1-2 sentences) of what this project does.

## Why This Exists

[Problem statement - what pain point does this solve?]

## Quick Start

```bash
# Minimal steps to get running
npm install
npm start
# Now visit http://localhost:3000
```

## Installation

[Detailed setup instructions]

## Usage

[Basic examples with expected output]

## Documentation

- [API Reference](docs/api.md)
- [Architecture Guide](docs/architecture.md)
- [Contributing Guide](CONTRIBUTING.md)

## License

[License type and link]
```

### API Documentation (Reference)

**Purpose:** Technical reference for developers using the API/library

**Audience:** Developers integrating with your code

**Must include:**
- Function/method signatures
- Parameter types and constraints
- Return types and possible values
- Error conditions and exceptions
- Working code examples
- Performance characteristics (if relevant)

**Template:**
```markdown
## functionName(param1, param2, options)

Brief description of what this function does.

**Parameters:**
- `param1` (string, required): Description of parameter
- `param2` (number, optional, default: 0): Description
- `options` (object, optional): Configuration options
  - `option1` (boolean, default: false): Description
  - `option2` (string, default: 'value'): Description

**Returns:**
- (Promise<Result>): Description of return value

**Throws:**
- `ValidationError`: When param1 is empty
- `NotFoundError`: When resource doesn't exist

**Example:**
```javascript
const result = await functionName('input', 42, {
  option1: true
});
console.log(result); // { status: 'success', data: ... }
```

**Performance:**
- Time complexity: O(n)
- Caches results for 5 minutes
```

### Architecture Documentation (Design)

**Purpose:** Explain system design, patterns, and decisions

**Audience:**
- New team members ramping up
- Developers making changes
- Technical stakeholders reviewing design

**Must include:**
- System overview (components and interactions)
- Key design decisions and rationale
- Data flow diagrams
- Technology choices and tradeoffs
- Scaling considerations
- Security model
- Known limitations

**Template:**
```markdown
# System Architecture

## Overview

[High-level description of system components]

```
[ASCII diagram or mermaid diagram showing components]
User → API Gateway → Service Layer → Database
                   ↓
                Cache Layer
```

## Components

### Component Name
**Purpose:** What this component does
**Technology:** What it's built with
**Interactions:** What it talks to and how
**Scalability:** How it scales

## Design Decisions

### Decision: Why We Chose Technology X

**Context:** What problem we were solving
**Options Considered:** A, B, C
**Decision:** We chose B
**Rationale:** Why B was better than A and C
**Consequences:** Tradeoffs we accepted

## Data Flow

[Description of how data moves through the system]

## Security Model

[Authentication, authorization, encryption, etc.]

## Known Limitations

[Current constraints and future improvements]
```

### Tutorial (Learning)

**Purpose:** Teach users how to accomplish specific goals

**Audience:** Users learning to use the system

**Must include:**
- Clear learning objective
- Prerequisites (assumed knowledge)
- Step-by-step instructions
- Expected output at each step
- Explanations of what's happening
- Common mistakes and troubleshooting
- Next steps for further learning

**Template:**
```markdown
# Tutorial: [Learning Objective]

In this tutorial, you'll learn how to [specific goal]. By the end, you'll be
able to [concrete outcome].

## Prerequisites

Before starting, you should:
- Have [software] installed
- Understand [concepts]
- Have completed [prior tutorial]

## Step 1: [First Action]

[Detailed instruction]

```bash
command to run
```

**What's happening:** [Explanation of what this step does and why]

**Expected output:**
```
output you should see
```

**Troubleshooting:**
- If you see error X, do Y
- If Z doesn't work, check A

## Step 2: [Next Action]

[Continue pattern...]

## What You Learned

- Concept 1
- Concept 2
- How to do X

## Next Steps

- Try [related tutorial]
- Read [reference docs]
- Build [practice project]
```

### Reference Documentation (Lookup)

**Purpose:** Quick lookup for specific information

**Audience:** Users who know what they're looking for

**Must include:**
- Organized by category
- Searchable/indexable structure
- Concise descriptions
- Links to related information
- Version-specific information

**Template:**
```markdown
# Configuration Reference

## Environment Variables

### DATABASE_URL
- **Type:** String (connection string)
- **Required:** Yes
- **Default:** None
- **Example:** `postgresql://user:pass@localhost:5432/dbname`
- **Description:** Database connection string for PostgreSQL

### LOG_LEVEL
- **Type:** String (debug|info|warn|error)
- **Required:** No
- **Default:** `info`
- **Example:** `LOG_LEVEL=debug`
- **Description:** Logging verbosity level

## Configuration File

[Similar structure for config file options]

## See Also

- [Deployment Guide](deployment.md)
- [Troubleshooting](troubleshooting.md)
```

---

## Writing Style Guide

### Clarity Principles

**Use active voice:**
- ✅ "The function returns a promise"
- ❌ "A promise is returned by the function"

**Be specific:**
- ✅ "Install Node.js 18.x or later"
- ❌ "Install a recent version of Node.js"

**Use consistent terminology:**
- Choose one term and stick with it (user/customer, config/configuration)
- Don't switch between synonyms
- Define domain-specific terms

**Keep sentences short:**
- One idea per sentence
- Break complex sentences into multiple simple ones
- Use bullets for lists

### Example-Driven Writing

**Always provide examples:**

Bad (no example):
```markdown
The API accepts JSON payloads with user data.
```

Good (with example):
```markdown
The API accepts JSON payloads with user data:

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "admin"
}
```
```

**Show both success and failure cases:**

```markdown
**Success response:**
```json
{ "status": "ok", "userId": 123 }
```

**Error response:**
```json
{ "status": "error", "message": "Invalid email format" }
```
```

### Audience Awareness

**Adjust complexity to audience:**

For beginners:
```markdown
Run `npm install` to download the project dependencies. Dependencies are
external code libraries that your project needs to function.
```

For experienced developers:
```markdown
Run `npm install` to install dependencies.
```

**Don't condescend:**
- ❌ "Obviously, you should..."
- ❌ "Simply just..."
- ❌ "As everyone knows..."
- ✅ "First, configure the database connection..."

### Consistency Standards

**Use consistent formatting:**
- Code: `backticks`
- Commands: ```bash code blocks```
- File paths: `path/to/file.md`
- Variables: `VARIABLE_NAME`
- UI elements: **Bold**

**Use consistent structure:**
- Same heading levels for similar content
- Same example format throughout
- Same terminology across documents

**Maintain consistent voice:**
- Choose second person ("you") or third person and stick with it
- Maintain same level of formality throughout
- Use same tense (usually present for docs)

---

## Code Integration

Good documentation lives close to the code it describes.

### Docstrings (Function/Class Documentation)

**Python example:**
```python
def calculate_tax(amount: float, rate: float, region: str = 'US') -> float:
    """Calculate tax amount based on rate and region.

    Args:
        amount: The pre-tax amount in dollars
        rate: Tax rate as decimal (0.1 for 10%)
        region: Tax region code (default: 'US')

    Returns:
        Tax amount in dollars, rounded to 2 decimal places

    Raises:
        ValueError: If amount is negative or rate is outside 0-1 range

    Example:
        >>> calculate_tax(100.0, 0.1)
        10.0
        >>> calculate_tax(100.0, 0.2, region='EU')
        20.0
    """
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if not 0 <= rate <= 1:
        raise ValueError("Rate must be between 0 and 1")

    return round(amount * rate, 2)
```

**JavaScript/TypeScript example:**
```typescript
/**
 * Calculate tax amount based on rate and region.
 *
 * @param amount - The pre-tax amount in dollars
 * @param rate - Tax rate as decimal (0.1 for 10%)
 * @param region - Tax region code (default: 'US')
 * @returns Tax amount in dollars, rounded to 2 decimal places
 * @throws {Error} If amount is negative or rate is outside 0-1 range
 *
 * @example
 * ```typescript
 * calculateTax(100.0, 0.1) // returns 10.0
 * calculateTax(100.0, 0.2, 'EU') // returns 20.0
 * ```
 */
function calculateTax(
  amount: number,
  rate: number,
  region: string = 'US'
): number {
  if (amount < 0) {
    throw new Error('Amount cannot be negative');
  }
  if (rate < 0 || rate > 1) {
    throw new Error('Rate must be between 0 and 1');
  }

  return Math.round(amount * rate * 100) / 100;
}
```

### Inline Comments

**When to comment:**
- Complex algorithms (explain the approach)
- Non-obvious workarounds (explain why it's necessary)
- Business logic (explain the domain rule)
- Performance optimizations (explain the tradeoff)

**When NOT to comment:**
- Obvious code (the code is self-documenting)
- Repeating function/variable names
- Commented-out code (delete it, git remembers)

**Good comments:**
```python
# Use binary search since data is sorted (O(log n) vs O(n))
index = binary_search(sorted_data, target)

# Retry with exponential backoff per API rate limit docs
for attempt in range(max_retries):
    try:
        result = api_call()
        break
    except RateLimitError:
        time.sleep(2 ** attempt)
```

**Bad comments:**
```python
# Increment counter
counter = counter + 1

# Loop through items
for item in items:
    # Process item
    process(item)
```

### Type Hints/Annotations

Type hints serve as inline documentation:

**Python:**
```python
from typing import List, Dict, Optional

def find_users(
    filters: Dict[str, str],
    limit: int = 10,
    offset: int = 0
) -> List[User]:
    """Find users matching filters.

    Types document the contract:
    - filters: field name -> filter value
    - limit/offset: pagination parameters
    - returns: list of User objects (never None)
    """
    pass

def get_user(user_id: str) -> Optional[User]:
    """Get user by ID, or None if not found."""
    pass
```

**TypeScript:**
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

interface SearchFilters {
  [field: string]: string;
}

function findUsers(
  filters: SearchFilters,
  limit: number = 10,
  offset: number = 0
): User[] {
  // Implementation
}

function getUser(userId: string): User | null {
  // Implementation
}
```

---

## Maintenance Strategy

Documentation rots quickly if not maintained. Build maintenance into your workflow.

### Documentation Lives with Code

**Principle:** Documentation should be version-controlled alongside the code it describes.

**Structure:**
```
project/
├── README.md              # Project overview (always at root)
├── docs/
│   ├── api/               # API reference docs
│   ├── guides/            # Tutorials and guides
│   ├── architecture.md    # System design
│   └── contributing.md    # Contribution guidelines
├── src/
│   ├── module/
│   │   ├── index.ts      # Code
│   │   └── README.md     # Module-specific docs
│   └── ...
└── CHANGELOG.md          # Version history
```

**Why this matters:**
- Docs change with code in same PR
- Reviewers verify doc updates
- Git history shows doc evolution
- No stale documentation on separate wiki

### Documentation as Code Review Item

**Include in PR checklist:**
- [ ] Public APIs have docstrings
- [ ] README updated if behavior changed
- [ ] Examples updated if API changed
- [ ] Architecture docs updated if design changed
- [ ] CHANGELOG updated with user-facing changes

**Treat missing docs like missing tests:**
- Block merge if public API lacks documentation
- Request clarification for complex logic without comments
- Ask for examples in API documentation

### Deprecation Documentation

**When deprecating features:**

```markdown
## functionName() (DEPRECATED)

**Deprecated:** This function is deprecated as of v2.0.0 and will be removed
in v3.0.0. Use `newFunctionName()` instead.

**Migration guide:**

```javascript
// Old (deprecated):
const result = functionName(param1, param2);

// New (recommended):
const result = newFunctionName({ param1, param2 });
```

**Rationale:** The new function provides better error handling and supports
async operations.
```

### Versioning Documentation

**For libraries/APIs:**

- Version docs alongside code releases
- Maintain docs for supported versions
- Link to version-specific docs
- Document breaking changes prominently

**Example structure:**
```
docs/
├── latest/           # Symlink to current version
├── v2.1/
├── v2.0/
└── v1.0/            # Legacy, supported for 6 months
```

**In documentation:**
```markdown
# API Reference (v2.1)

This documentation is for version 2.1.x.

- [View v2.0 docs](../v2.0/api.md)
- [View v1.0 docs](../v1.0/api.md) (deprecated, supported until 2026-06-01)
```

---

## Quality Checklist

**Before considering documentation complete:**

### Completeness
- [ ] All public functions/classes documented
- [ ] All parameters and return types described
- [ ] Error conditions documented
- [ ] Examples provided for main use cases
- [ ] Prerequisites and setup instructions included

### Accuracy
- [ ] Examples actually work (copy-paste and test)
- [ ] API signatures match current code
- [ ] Version numbers are correct
- [ ] Links to other docs are valid
- [ ] Screenshots/diagrams reflect current state

### Clarity
- [ ] Technical terms defined or linked
- [ ] Sentences are concise and clear
- [ ] Active voice used consistently
- [ ] Examples progress from simple to complex
- [ ] Headings create logical structure

### Usability
- [ ] Table of contents for long documents
- [ ] Searchable (good heading structure)
- [ ] Links to related documentation
- [ ] Clear next steps or related reading
- [ ] Contact info for questions/issues

### Maintainability
- [ ] Documentation lives with code
- [ ] Version information included
- [ ] Last updated date visible
- [ ] Ownership/contact documented
- [ ] Contributing guidelines clear

---

## Common Mistakes

### What NOT to Do

**Don't assume knowledge:**
❌ "Configure the usual settings"
✅ "Configure the database connection string in DATABASE_URL"

**Don't use jargon without definition:**
❌ "The service uses eventual consistency with CRDTs"
✅ "The service uses eventual consistency (data may be briefly out of sync) with CRDTs (Conflict-free Replicated Data Types, a data structure that allows safe concurrent updates)"

**Don't skip error cases:**
❌ Document only happy path
✅ Document error responses, edge cases, and failure modes

**Don't write documentation that duplicates code:**
❌ "This function adds two numbers together" (obvious from code)
✅ "Calculates the total with tax included, rounded to 2 decimal places per accounting standards"

**Don't let docs drift:**
❌ Write docs once, never update
✅ Update docs in same PR as code changes

**Don't over-document:**
❌ Document every private helper function
✅ Document public API and complex/non-obvious logic

**Don't use vague language:**
❌ "This might sometimes cause issues"
✅ "This raises a TimeoutError after 30 seconds if the database doesn't respond"

### Documentation Smells

**Warning signs of poor documentation:**

- README is empty or just project name
- API docs missing parameter types
- Examples don't actually run
- Last updated > 6 months ago
- No error/exception documentation
- Broken links to other docs
- Comments in code contradict behavior
- No CHANGELOG or version history
- Installation instructions assume specific OS
- No troubleshooting section

---

## Integration with Task Management

**Documentation integrates with development workflow:**

### During Task Planning
- Include documentation requirements in acceptance criteria
- Example: "API endpoints documented with parameter types and examples"

### During Task Execution
- Write docs alongside code (not after)
- Include doc updates in same commit as code changes
- Use docstrings for inline documentation

### During Code Review
- Review documentation quality (see code-review skill)
- Verify examples actually work
- Check for completeness against checklist

### Task Completion
- Documentation is part of "done"
- Can't mark task complete without documentation
- Link documentation in task notes

**Example acceptance criteria:**

```
Task: Add user search API endpoint

Acceptance Criteria:
- [ ] Endpoint implemented at POST /api/users/search
- [ ] Handles pagination (limit, offset params)
- [ ] Returns 400 for invalid filters
- [ ] Tests cover success and error cases
- [ ] API documentation includes:
  - [ ] Request/response examples
  - [ ] Parameter types and constraints
  - [ ] Error response codes
  - [ ] Performance characteristics (< 500ms)
- [ ] CHANGELOG updated with new endpoint
```

---

## Examples: Good vs Bad Documentation

### Example 1: README

**Bad README:**
```markdown
# My Project

This is a cool project.

## Install
npm install

## Usage
Run it.
```

**Good README:**
```markdown
# Task Automation Service

Automated task scheduling and execution platform for background jobs.

## What This Does

Schedule and run recurring tasks (data syncs, cleanup jobs, reports) without managing infrastructure. Supports cron-style scheduling, retry logic, and monitoring.

## Quick Start

```bash
# Install dependencies
npm install

# Configure database (PostgreSQL required)
export DATABASE_URL="postgresql://localhost:5432/tasks"

# Run migrations
npm run migrate

# Start service
npm start

# Service now running on http://localhost:3000
```

## Create Your First Task

```javascript
const client = require('./client');

await client.createTask({
  name: 'daily-cleanup',
  schedule: '0 0 * * *',  // Daily at midnight
  action: 'cleanup_old_data',
  params: { retention_days: 30 }
});
```

## Documentation

- [API Reference](docs/api.md)
- [Task Configuration Guide](docs/tasks.md)
- [Deployment Guide](docs/deployment.md)

## Requirements

- Node.js 18+
- PostgreSQL 14+
- Redis 6+ (for task queue)

## License

MIT - see [LICENSE](LICENSE)
```

### Example 2: API Documentation

**Bad API docs:**
```markdown
## getUser

Gets a user.

```javascript
getUser(id)
```
```

**Good API docs:**
```markdown
## getUser(userId)

Retrieve a user by their unique identifier.

**Parameters:**
- `userId` (string, required): The user's UUID

**Returns:**
- `Promise<User>`: User object with fields:
  - `id` (string): User's UUID
  - `name` (string): Full name
  - `email` (string): Email address
  - `role` (string): One of 'admin', 'user', 'guest'
  - `createdAt` (Date): Account creation timestamp

**Throws:**
- `NotFoundError`: User with given ID doesn't exist
- `ValidationError`: Invalid UUID format

**Example:**

```javascript
const user = await getUser('550e8400-e29b-41d4-a716-446655440000');
console.log(user);
// {
//   id: '550e8400-e29b-41d4-a716-446655440000',
//   name: 'Jane Doe',
//   email: 'jane@example.com',
//   role: 'admin',
//   createdAt: 2024-01-15T10:30:00.000Z
// }
```

**Error handling:**

```javascript
try {
  const user = await getUser('invalid-id');
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log('User not found');
  } else if (error instanceof ValidationError) {
    console.log('Invalid user ID format');
  }
}
```

**Performance:**
- Average response time: < 50ms
- Results cached for 5 minutes
- Database indexed on user ID
```

### Example 3: Architecture Documentation

**Bad architecture docs:**
```markdown
# Architecture

We use microservices.
```

**Good architecture docs:**
```markdown
# System Architecture

## Overview

Event-driven microservices architecture for real-time order processing.
Components communicate via message queue with async event processing.

```
Customer → API Gateway → Order Service → Message Queue
                             ↓
                        Payment Service
                             ↓
                        Fulfillment Service
                             ↓
                        Notification Service
```

## Components

### API Gateway
- **Technology:** Node.js + Express
- **Purpose:** Request routing, authentication, rate limiting
- **Scale:** 3 instances behind load balancer
- **SLA:** 99.9% uptime, < 100ms latency

### Order Service
- **Technology:** Python + FastAPI
- **Purpose:** Order validation and creation
- **Database:** PostgreSQL (orders table)
- **Events Published:** `order.created`, `order.updated`
- **Scale:** Horizontally scalable, currently 5 instances

### Message Queue
- **Technology:** RabbitMQ
- **Purpose:** Async event distribution to downstream services
- **Durability:** Messages persisted to disk
- **Retry:** Exponential backoff, max 3 retries

## Design Decisions

### Decision: Event-Driven vs Synchronous API Calls

**Context:** Order creation triggers multiple downstream actions (payment, fulfillment, notifications)

**Options Considered:**
1. Synchronous API calls (Order Service calls Payment Service directly)
2. Event-driven architecture (Order Service publishes events, services subscribe)

**Decision:** Event-driven architecture (#2)

**Rationale:**
- Decouples services (Payment Service can be down without blocking orders)
- Enables parallelization (payment and fulfillment start simultaneously)
- Supports future features (analytics can subscribe to order events)
- Improves resilience (message queue handles retries)

**Consequences:**
- Added complexity (message queue infrastructure)
- Eventual consistency (order created before payment processed)
- Debugging harder (distributed tracing required)

## Data Flow

1. Customer submits order via API Gateway
2. API Gateway authenticates, forwards to Order Service
3. Order Service validates order, saves to database
4. Order Service publishes `order.created` event to queue
5. Payment Service receives event, processes payment
6. Fulfillment Service receives event, creates shipment
7. Notification Service receives event, sends confirmation email
8. Each service publishes completion events (`payment.completed`, etc.)

## Security Model

- **Authentication:** JWT tokens (15 min expiry, refresh tokens 7 days)
- **Authorization:** Role-based access control (RBAC)
- **Encryption:** TLS 1.3 for all external communication
- **Secrets:** Stored in AWS Secrets Manager, rotated every 90 days
- **Audit:** All mutations logged to audit trail

## Known Limitations

- **Eventual consistency:** Order status may be briefly out of sync
- **Message ordering:** Events from different instances may arrive out of order
- **Scalability ceiling:** Current queue handles 10K orders/min (need Kafka for higher throughput)
- **Single point of failure:** Message queue not currently HA (roadmap item for Q2)

## Future Improvements

- Add distributed tracing (OpenTelemetry)
- Implement circuit breakers for service calls
- Add caching layer (Redis) for frequently accessed data
- Migrate to Kafka for higher throughput
```

---

**Remember:** Documentation is a gift to your future self and teammates. Write docs that you'd want to find when joining a new project. Be specific, provide examples, and keep documentation current with code changes.
