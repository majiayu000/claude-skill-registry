---
name: brainstorm-prompt-optimizer
description: >
  Optimizes raw idea descriptions into structured prompts ready for the brainstorming workflow.
  TRIGGER when: user says "optimize for brainstorm", "prepare idea for brainstorm", "enhance this idea",
  "make this ready for brainstorming", "imposta per brainstorm", or wants to improve a feature idea 
  before using /specs.brainstorm.
  DO NOT TRIGGER for code optimization, refactoring, or general prompt engineering tasks.
allowed-tools: Read, Bash
model: inherit
---

# Brainstorm Prompt Optimizer

Transform a raw idea into an optimized prompt ready for the brainstorming workflow (`/specs.brainstorm`).

This skill prepares ideas so that when passed to `/specs.brainstorm`, they produce better functional specifications
following EARS syntax, proper acceptance criteria taxonomy, and complete Non-Goals/Negative Requirements sections.

## When to Use

- User wants to optimize an idea before running `/specs.brainstorm`
- User says "prepare this idea for brainstorming", "enhance for brainstorm"
- User provides a simple idea and wants it structured for better brainstorming results
- User asks "make this ready for brainstorm"
- User says "imposta per brainstorm", "prepara idea per brainstorm"

### Do Not Use When

- User wants code or performance optimization (use appropriate skills)
- User wants general prompt engineering (use prompt-engineering skill)
- User wants analysis of an existing prompt
- User is asking to execute a task directly
- User wants to fix a bug or modify existing behavior → route to `specs.change-spec`

## How It Works

**Output ONLY the optimized prompt** — no analysis, no reports, no recommendations.

The workflow transforms a raw idea into a structured prompt that will produce better functional specifications when
used with `/specs.brainstorm`.

### Workflow

#### Phase 1: Detect Project Context

Check for project files to understand the environment:
- `CLAUDE.md` → project conventions
- `docs/specs/architecture.md` → existing architecture constraints
- `docs/specs/ontology.md` → existing domain terms

Tech stack detection:
- `package.json` → Node.js/TypeScript/React
- `pom.xml` / `build.gradle` → Java/Spring Boot
- `requirements.txt` / `pyproject.toml` → Python

#### Phase 2: Analyze the Idea

Parse the raw idea to identify:
1. **Core action**: What needs to be built/created (e.g., "add authentication", "create search")
2. **Target domain**: What part of the system is affected
3. **Implicit scope**: What's naturally included vs. excluded
4. **User perspective**: Who benefits from this feature
5. **Business value**: Why this feature matters

#### Phase 3: Identify Scope Size

Estimate complexity to help `/specs.brainstorm`:
- **Small**: Single user story, 1-3 entities, simple flow → 3-8 tasks
- **Medium**: 2-4 user stories, 4-8 entities → 8-15 tasks
- **Large**: 5+ user stories, 9+ entities → may need split (warn user)

#### Phase 4: Structure the Optimized Prompt

Build a structured prompt with these components (aligned with `/specs.brainstorm` template):

```
# [Core Action] — [Target Domain]

## Problem Statement
[What problem does this solve? Who has it?]

## Core Feature
[What should the system do? Focus on behavior, not implementation]

## Target Users
[Who will use this? What's their goal?]

## User Flows
1. [Primary flow from user perspective]
2. [Alternative flows if applicable]

## Data Requirements
- [What data the feature needs to work with]
- [Any data relationships]

## Success Criteria
- [IMP] [Testable criterion that requires code/implementation]
- [SEF] [Side-effect criterion - automatic consequence]
- [EXT] [External verification criterion]

## Non-Goals
- **Feature X**: [Brief explanation why excluded]
- **Feature Y**: [Brief explanation why excluded]

## Negative Requirements
- REQ-NR001: The system SHALL NOT [security/data integrity constraint]

## [NEEDS CLARIFICATION] (max 3)
- [Specific question that significantly impacts scope]
```

#### Phase 5: Output the Optimized Prompt

Present the complete optimized prompt in a fenced code block with the label `optimized-prompt`:

```markdown
```optimized-prompt
[Full optimized prompt content]
```
```

---

## EARS Syntax Reference

Use EARS (Easy Approach to Requirements Syntax) for requirements:

| Form | Pattern | Example |
|------|---------|---------|
| **Event-driven** | `WHEN <event> THEN the system SHALL <action>` | `WHEN the user clicks "Submit" THEN the system SHALL validate the form data` |
| **State-driven** | `WHEN <system state> THEN the system SHALL <action>` | `WHEN the session expires THEN the system SHALL clear user data` |
| **Generic** | `The system SHALL <action>` | `The system SHALL encrypt all stored passwords with bcrypt` |
| **Feature** | `IF <feature> THEN the system SHALL <action>` | `IF multi-factor auth is enabled THEN the system SHALL require second factor` |
| **Negative** | `IF <unwanted condition> THEN the system SHALL NOT <action>` | `IF SQL input detected THEN the system SHALL reject with 400` |

Mandatory keywords: **SHALL**, **WILL**, **MAY**
Forbidden words: "robust", "intuitive", "fast", "scalable", "efficient", "user-friendly"

---

## Acceptance Criteria Taxonomy

Every success criterion MUST be tagged:

| Tag | Meaning | Generates Tasks? |
|-----|---------|------------------|
| `[IMP]` | Requires new code, configuration, or explicit behavior | **YES** |
| `[SEF]` | Natural automatic consequence of an `[IMP]` criterion | NO (verify in e2e) |
| `[EXT]` | Verified by external tools or user observation | NO (e2e checkpoint) |

**60% Rule**: At least 60% of criteria should be `[IMP]`.

---

## Prompt Templates by Category

### Authentication & User Management

```optimized-prompt
# Add [Feature] — User Management

## Problem Statement
[Describe the problem users face without this feature]

## Core Feature
The system SHALL [describe what the feature does, focus on behavior]

## Target Users
- **Primary**: [main user type]
- **Secondary**: [other affected users]

## User Flows
1. **Primary Flow**: [Step by step from user perspective]
2. **Alternative Flow**: [If applicable]

## Data Requirements
- User entity: [fields]
- [Other entities involved]

## Success Criteria
- [IMP] [Criterion 1 — testable outcome requiring code]
- [IMP] [Criterion 2]
- [SEF] [Criterion 3 — automatic consequence]
- [EXT] [Criterion 4 — verified externally]

## Non-Goals
- **Social Login**: No OAuth providers (Google, GitHub, etc.)
- **Password Reset**: Not included in this specification
- **Two-Factor Auth**: Not included in this specification

## Negative Requirements
- REQ-NR001: The system SHALL NOT store passwords in plain text; it SHALL use bcrypt with cost factor ≥12
- REQ-NR002: The system SHALL NOT expose user existence through login error messages
```

### API & Backend Features

```optimized-prompt
# [Feature Name] — API Layer

## Problem Statement
[What integration need or capability gap exists]

## Core Feature
The system SHALL provide [describe the API behavior]

## Target Users
- **Primary**: [API consumers]
- **Secondary**: [administrators]

## User Flows
1. **Happy Path**: [Request → Validation → Response]
2. **Error Path**: [Invalid input → Error response]

## API Contract
- Endpoint: [path and method]
- Input: [what the API receives]
- Output: [what the API returns]
- Error cases: [failure modes with codes]

## Data Model
- [Entities involved]
- [Relationships]

## Success Criteria
- [IMP] [Criterion 1]
- [IMP] [Criterion 2]
- [SEF] [Criterion 3]

## Non-Goals
- **GraphQL**: REST only
- **Async Processing**: Synchronous only
- **Caching**: Not included

## Negative Requirements
- REQ-NR001: IF user input is used in SQL query THEN the system SHALL NOT concatenate directly
- REQ-NR002: The system SHALL NOT expose internal error details to clients
```

### UI & Frontend Features

```optimized-prompt
# [Feature Name] — User Interface

## Problem Statement
[What user experience gap exists]

## Core Feature
The user SHALL be able to [describe user action and system response]

## Target Users
- **Primary**: [end users]
- **Secondary**: [admin users if applicable]

## User Flows
1. **Entry**: [How user accesses this feature]
2. **Interaction**: [Primary user action]
3. **Outcome**: [Result user sees]
4. **Error**: [Error handling for invalid input]

## UI Requirements
- Layout: [description]
- Components: [key UI elements]
- Feedback: [success/error/loading states]

## Responsive Behavior
- Desktop: [behavior]
- Mobile: [behavior]

## Success Criteria
- [IMP] [Criterion 1 — visible behavior]
- [IMP] [Criterion 2]
- [IMP] [Criterion 3]
- [SEF] [Criterion 4 — automatic]

## Non-Goals
- **Real-time Updates**: No WebSocket or SSE
- **Offline Mode**: Not included
- **Accessibility Features**: [specific exclusions]

## Negative Requirements
- REQ-NR001: The system SHALL NOT display raw error messages to users
- REQ-NR002: The system SHALL NOT allow XSS through user input fields
```

### Data & Processing Features

```optimized-prompt
# [Feature Name] — Data Processing

## Problem Statement
[What data challenge exists]

## Core Feature
The system SHALL [describe data transformation/processing behavior]

## Target Users
- **Primary**: [who benefits]
- **Secondary**: [who monitors]

## User Flows
1. **Data Input**: [Source and format]
2. **Processing**: [Transformation steps]
3. **Output**: [Result destination and format]

## Data Quality
- Validation: [rules]
- Error handling: [for bad data]

## Performance Constraints
- Volume: [expected data size]
- Latency: [expected processing time]

## Success Criteria
- [IMP] [Criterion 1]
- [IMP] [Criterion 2]
- [EXT] [Criterion 3 — external verification]

## Non-Goals
- **Real-time Processing**: Batch only
- **Data Export**: Not included
- **Backup/Restore**: Not included

## Negative Requirements
- REQ-NR001: The system SHALL NOT lose data on processing failure
- REQ-NR002: The system SHALL NOT process unbounded data without pagination
```

---

## Examples

### Example 1: Simple Idea → Optimized

**Input:**
```
Add user authentication
```

**Output:**
```optimized-prompt
# Add User Authentication — Authentication Layer

## Problem Statement
Users cannot securely access the system. They need a way to prove their identity and access their personalized content.

## Core Feature
The system SHALL provide email/password authentication that allows users to:
- Register with a valid email address and secure password
- Log in with registered credentials
- Maintain an authenticated session across requests
- Log out to terminate their session

## Target Users
- **Primary**: End users who need to access personalized features
- **Secondary**: Administrators who manage user accounts

## User Flows
1. **Registration**: User enters email → receives confirmation → sets password → account created
2. **Login**: User enters credentials → validated → session established → redirected to dashboard
3. **Logout**: User clicks logout → session terminated → redirected to login page

## Data Requirements
- User entity: email, hashed_password, created_at, updated_at
- Session entity: user_id, token, expiration

## Success Criteria
- [IMP] Users can register with email/password
- [IMP] Users can log in with valid credentials
- [IMP] Invalid credentials show generic error message
- [IMP] Users can log out
- [IMP] Session persists across page navigation
- [IMP] Expired sessions require re-login

## Non-Goals
- **Social Login**: No OAuth providers (Google, GitHub, etc.)
- **Password Reset**: Not included in this specification
- **Two-Factor Authentication**: Not included in this specification

## Negative Requirements
- REQ-NR001: The system SHALL NOT store passwords in plain text; it SHALL use bcrypt with cost factor ≥12
- REQ-NR002: The system SHALL NOT expose user existence through login error messages; it SHALL use generic "invalid credentials" for both cases
- REQ-NR003: The system SHALL NOT allow weak passwords (minimum 8 characters, mixed case, number)
```

### Example 2: Vague Idea → Structured

**Input:**
```
Better search for products
```

**Output:**
```optimized-prompt
# Improve Product Search — Product Discovery

## Problem Statement
Users cannot find products they are looking for using the current search. Results are not relevant, don't match user intent, and sorting is not useful.

## Core Feature
The system SHALL provide enhanced product search that allows users to:
- Search products by name, description, and category
- Receive results ranked by relevance to search terms
- Filter results by category, price range, and availability
- Sort results by relevance, price, or newest

## Target Users
- **Primary**: Shoppers looking for specific products
- **Secondary**: Browsers exploring product catalog

## User Flows
1. **Direct Search**: User enters search terms → results displayed → user selects product
2. **Filtered Search**: User enters terms → applies filters → refined results → user selects product
3. **Empty Results**: User enters terms → no results → suggestion displayed

## Search Behavior
- Minimum 2 characters to trigger search
- Partial word matching for product names
- Search across: product name, description, category name, tags
- Results limited to 50 per page with pagination

## Filtering Options
- Category: single or multiple selection
- Price range: min/max with validation
- Availability: in-stock only toggle

## Sorting Options
- Relevance (default): based on search term match score
- Price: low-to-high or high-to-low
- Newest: by creation date descending

## Success Criteria
- [IMP] Search returns products matching the query terms
- [IMP] Search supports partial word matching
- [IMP] Category filter limits results to selected category
- [IMP] Price range filter shows products within min/max bounds
- [IMP] Results can be sorted by relevance, price, or date
- [IMP] Pagination allows navigation through large result sets
- [IMP] Empty search shows appropriate message with suggestions

## Non-Goals
- **Autocomplete**: Not included in this specification
- **Search Analytics**: Not included in this specification
- **Personalized Results**: Results are the same for all users
- **Image Search**: Not included in this specification

## Negative Requirements
- REQ-NR001: The system SHALL NOT expose product inventory details in search results unless explicitly needed
- REQ-NR002: The system SHALL NOT allow SQL injection through search terms; it SHALL sanitize all input
- REQ-NR003: The system SHALL NOT return results beyond configured pagination limits per request
```

### Example 3: Technical Idea → Functional

**Input:**
```
Implement Redis caching for API responses
```

**Output:**
```optimized-prompt
# Implement API Response Caching — Performance Optimization

## Problem Statement
The API is slow for frequently requested data. Repeated requests for the same resources consume unnecessary server resources and increase response times for users.

## Core Feature
The system SHALL cache frequently accessed API responses to reduce response times and server load:
- Cache GET requests for defined intervals
- Return cached responses when data hasn't changed
- Invalidate cache when underlying data changes
- Provide cache statistics for monitoring

## Target Users
- **Primary**: API consumers (frontend applications, mobile apps)
- **Secondary**: System administrators monitoring performance

## Cache Behavior
- Cache key based on request URL and parameters
- Default TTL: 5 minutes (configurable per endpoint)
- Cache stores: response body, status code, headers
- Cache miss: fetch from source, store, return

## Invalidation Rules
- Cache invalidated when source data is modified via POST/PUT/PATCH/DELETE
- Manual invalidation available via admin endpoint
- Bulk invalidation by cache key pattern

## Success Criteria
- [IMP] Cached requests return within 50ms
- [IMP] Cache hit rate visible in metrics
- [IMP] Manual cache invalidation works
- [IMP] Automatic invalidation on data changes
- [IMP] Cache can be disabled per request via header
- [SEF] Cache reduces database load for repeated requests
- [EXT] Response time improvement measurable via APM

## Non-Goals
- **Distributed Cache**: Single Redis instance only
- **Cache Warming**: Not included
- **Cache Partitioning**: Not included
- **Multi-Tenant Isolation**: Not included in this specification

## Negative Requirements
- REQ-NR001: The system SHALL NOT cache responses containing user-specific data
- REQ-NR002: The system SHALL NOT serve stale cache beyond configured TTL
- REQ-NR003: The system SHALL NOT expose cache internals in API responses
- REQ-NR004: IF cache connection fails THEN the system SHALL fall back to direct database access without error
```

---

## Integration with Brainstorming

The optimized prompt should be used directly with `/specs.brainstorm`:

```bash
# Copy the optimized prompt and use it with brainstorm
/specs.brainstorm [paste optimized prompt here]
```

### Workflow

```
Raw Idea → brainstorm-prompt-optimizer → Optimized Prompt → /specs.brainstorm → Functional Spec → /specs.spec-to-tasks → Tasks
```

## Constraints

- Output ONLY the optimized prompt — no analysis, no recommendations
- If the input is a bug fix or modification request, do NOT optimize → route to `specs.change-spec`
- If the input is too vague to optimize meaningfully, ask ONE clarifying question
- Keep the output focused on WHAT (behavior), not HOW (implementation)
- Include explicit Non-Goals section (minimum 3 items) to prevent scope creep
- Include Negative Requirements (minimum 2 items) for security/integrity constraints
- Use EARS syntax (SHALL/WILL/MAY) for requirements
- Tag every acceptance criterion with `[IMP]`, `[SEF]`, or `[EXT]`
- Maximum 3 `[NEEDS CLARIFICATION]` markers

## Related Commands & Skills

| Component | When to Use |
|-----------|-------------|
| `/specs.brainstorm` | After optimization, run brainstorm to create specification |
| `/specs.spec-to-tasks` | Convert specification to executable tasks |
| `specs-change-spec` | For bug fixes or delta changes (not new features) |
| `specs-brainstorm` | Reference for functional specification template |