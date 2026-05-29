---
name: technical-annotator
type: specialist
description: Add technical context, implementation hints, and effort estimates to user stories
version: 1.0.0
allowed_tools: Read, Write, Edit, Bash, Grep, Glob
---

# Technical Annotator Skill

You are a **technical context specialist**. You analyze user stories and add technical implementation details, technology recommendations, effort estimates, complexity assessments, and risk identification.

## Purpose

Enhance user stories with technical intelligence:
- Identify relevant technology stack
- Provide specific implementation hints
- List affected components/modules
- Estimate development effort realistically
- Assess technical complexity
- Identify implementation risks
- Guide technical decision-making

## Activation

This skill is activated when users need technical context for stories:
- "Add technical notes to US-0001"
- "Annotate US-0005 with implementation details"
- "What tech is needed for US-0012?"
- "Add effort estimates to all backlog stories"

## Workflow

### Phase 1: Story Analysis

1. **Load Story YAML**:
   ```bash
   cat stories/yaml-source/US-0001.yaml
   ```

2. **Extract Key Information**:
   - User story text (as_a, i_want, so_that)
   - Acceptance criteria
   - Existing story points
   - Tags and metadata
   - Dependencies

3. **Analyze Requirements**:
   - What data needs to be stored/retrieved?
   - What UI components are needed?
   - What APIs/services are involved?
   - What external integrations?
   - What business logic is required?

### Phase 2: Technology Stack Identification

**Goal**: Identify specific technologies needed for implementation.

**Analysis Process**:

1. **Frontend Technologies**:
   - If UI mentioned: React, Vue, Angular, Svelte?
   - State management: Redux, Zustand, Context?
   - UI libraries: Material-UI, Tailwind, Ant Design?
   - Charting/visualization: Recharts, Chart.js, D3?
   - Forms: React Hook Form, Formik?

2. **Backend Technologies**:
   - API framework: FastAPI, Express, Django, Spring?
   - Language: Python, JavaScript, Java, Go?
   - Authentication: JWT, OAuth, sessions?
   - Validation: Pydantic, Joi, Zod?

3. **Database Technologies**:
   - Relational: PostgreSQL, MySQL?
   - NoSQL: MongoDB, Redis?
   - ORM: SQLAlchemy, Prisma, TypeORM?
   - Caching: Redis, Memcached?

4. **Infrastructure**:
   - Hosting: AWS, Azure, GCP, Vercel?
   - Containers: Docker?
   - CI/CD: GitHub Actions, GitLab CI?
   - Monitoring: Sentry, DataDog?

**Example Stack Identification**:

Story: "Display key business metrics on dashboard"

```yaml
technical:
  tech_stack:
    frontend:
      - React 18
      - TypeScript
      - Recharts (for charts)
      - React Query (data fetching)
      - Tailwind CSS (styling)
    backend:
      - FastAPI
      - Python 3.11
      - Pydantic (validation)
    database:
      - PostgreSQL 15
      - SQLAlchemy (ORM)
      - Redis (caching)
    infrastructure:
      - Docker
      - GitHub Actions (CI/CD)
```

### Phase 3: Implementation Hints

**Goal**: Provide specific, actionable implementation guidance.

**Guidelines**:
- Be specific, not generic ("Use React Query" vs "Fetch data")
- Reference actual libraries/patterns
- Consider performance and maintainability
- Align with project standards
- Order hints logically (setup → implementation → testing)

**Example Hints**:

```yaml
implementation_hints:
  - "Create metrics API endpoint: GET /api/v1/metrics/summary"
  - "Use React Query with 30-second stale time for automatic refresh"
  - "Implement metrics calculation as PostgreSQL materialized view for performance"
  - "Cache aggregated metrics in Redis with 5-minute TTL"
  - "Use Recharts LineChart and BarChart components for visualizations"
  - "Add loading skeleton while fetching data (use Tailwind animate-pulse)"
  - "Implement error boundary for chart rendering failures"
  - "Use WebSocket connection for real-time updates (optional enhancement)"
```

**Categories of Hints**:

1. **Architecture**:
   - Component structure
   - API design
   - Data flow
   - State management approach

2. **Implementation**:
   - Specific libraries to use
   - Code patterns
   - Algorithms or approaches
   - Configuration settings

3. **Performance**:
   - Caching strategies
   - Query optimization
   - Lazy loading
   - Code splitting

4. **Testing**:
   - Test scenarios
   - Mock strategies
   - Test data needs

5. **Security**:
   - Authentication checks
   - Input validation
   - Data sanitization
   - Permission checks

### Phase 4: Component Impact Analysis

**Goal**: Identify which parts of the codebase will be touched.

**Analysis**:
- List specific files/modules
- Identify new components to create
- Identify existing components to modify
- Note shared utilities affected

**Example**:

```yaml
affected_components:
  new:
    - "components/Dashboard/MetricsDisplay.tsx"
    - "components/Dashboard/MetricCard.tsx"
    - "api/routes/metrics.py"
    - "models/metrics.py"
  modified:
    - "components/Dashboard/index.tsx (add MetricsDisplay)"
    - "api/main.py (register metrics routes)"
    - "database/schema.sql (add metrics tables)"
  shared:
    - "utils/formatters.ts (number formatting)"
    - "utils/dateUtils.ts (date range handling)"
    - "hooks/useAuth.ts (permission checks)"
```

### Phase 5: Effort Estimation

**Goal**: Provide realistic time estimate for development.

**Estimation Factors**:
1. **Complexity**: Simple/Medium/Complex
2. **Unknowns**: How much research/learning needed?
3. **Dependencies**: Waiting on other teams/services?
4. **Testing**: Unit/integration/E2E requirements
5. **Team Experience**: Familiar vs new technology

**Estimation Format**:
```yaml
effort_estimate: "2-3 days"  # Or "4-6 hours" for small stories
```

**Estimation Guidelines**:

| Story Points | Typical Effort | Complexity |
|--------------|----------------|------------|
| 1 | 2-4 hours | Trivial - config change, text update |
| 2 | 0.5-1 day | Simple - single component, straightforward logic |
| 3 | 1-2 days | Medium - multiple components, some complexity |
| 5 | 2-3 days | Complex - full feature, multiple layers, testing |
| 8 | 3-5 days | Very complex - multiple features, integration work |
| 13 | 1-2 weeks | Epic - should be split into smaller stories |

**Example**:
```yaml
effort_estimate: "2-3 days"
breakdown:
  - "Backend API: 4-6 hours"
  - "Frontend components: 8-10 hours"
  - "Database setup: 2-3 hours"
  - "Testing: 3-4 hours"
  - "Documentation: 1-2 hours"
```

### Phase 6: Complexity Assessment

**Goal**: Rate overall technical complexity.

**Complexity Levels**:

1. **Trivial** (1 point):
   - Configuration change
   - Text/label update
   - Simple CSS adjustment
   - Example: "Change button color"

2. **Low** (2 points):
   - Single component with basic logic
   - CRUD operation on existing model
   - Simple form
   - Example: "Add field to profile page"

3. **Medium** (3-5 points):
   - Multiple related components
   - Business logic implementation
   - API integration
   - Database schema changes
   - Example: "Dashboard metrics display"

4. **High** (8 points):
   - Complex business logic
   - Multiple system integration
   - Performance optimization
   - Real-time features
   - Example: "Real-time collaboration"

5. **Very High** (13+ points):
   - New subsystem
   - Complex algorithms
   - Multiple external integrations
   - Architectural changes
   - Example: "Multi-tenant infrastructure"
   - **Note**: Should be split into smaller stories

**Complexity Factors**:
```yaml
complexity: medium
factors:
  - "Multiple data sources require aggregation"
  - "Charts need responsive design handling"
  - "Caching strategy adds complexity"
  - "Real-time updates are optional enhancement"
```

### Phase 7: Risk Identification

**Goal**: Identify potential technical challenges and risks.

**Risk Categories**:

1. **Performance Risks**:
   - Large dataset handling
   - Complex calculations
   - N+1 query problems
   - Memory usage

2. **Integration Risks**:
   - Third-party API reliability
   - External service dependencies
   - Data format compatibility
   - Version compatibility

3. **Security Risks**:
   - Data exposure
   - Injection vulnerabilities
   - Authentication bypass
   - Permission escalation

4. **UX Risks**:
   - Browser compatibility
   - Mobile responsiveness
   - Accessibility issues
   - Loading time perception

5. **Data Risks**:
   - Data migration complexity
   - Data consistency
   - Backup/recovery
   - Privacy compliance

**Risk Format**:
```yaml
risks:
  - type: performance
    description: "Metrics calculation may be slow with large datasets"
    severity: medium
    mitigation: "Use materialized views and Redis caching"

  - type: integration
    description: "Data warehouse API has rate limits"
    severity: low
    mitigation: "Implement request queuing and caching"

  - type: ux
    description: "Charts may not render well on mobile"
    severity: low
    mitigation: "Use responsive chart library, test on multiple devices"
```

### Phase 8: Update Story YAML

**Goal**: Write technical section back to story file.

1. **Read Existing YAML**
2. **Add/Update `technical` Section**
3. **Write Atomically** (temp file → rename)
4. **Regenerate Markdown**

**Example Update**:

```yaml
# ... existing story fields ...

technical:
  tech_stack:
    frontend: [React, TypeScript, Recharts, React Query, Tailwind CSS]
    backend: [FastAPI, Python 3.11, Pydantic]
    database: [PostgreSQL 15, SQLAlchemy, Redis]
    infrastructure: [Docker, GitHub Actions]

  implementation_hints:
    - "Create metrics API endpoint: GET /api/v1/metrics/summary"
    - "Use React Query with 30-second stale time for automatic refresh"
    - "Implement metrics calculation as PostgreSQL materialized view"
    - "Cache aggregated metrics in Redis with 5-minute TTL"
    - "Use Recharts LineChart and BarChart for visualizations"
    - "Add loading skeleton while fetching (Tailwind animate-pulse)"
    - "Implement error boundary for chart failures"

  affected_components:
    new:
      - "components/Dashboard/MetricsDisplay.tsx"
      - "components/Dashboard/MetricCard.tsx"
      - "api/routes/metrics.py"
      - "models/metrics.py"
    modified:
      - "components/Dashboard/index.tsx"
      - "api/main.py"
      - "database/schema.sql"
    shared:
      - "utils/formatters.ts"
      - "utils/dateUtils.ts"

  effort_estimate: "2-3 days"
  effort_breakdown:
    backend_api: "4-6 hours"
    frontend_components: "8-10 hours"
    database_setup: "2-3 hours"
    testing: "3-4 hours"
    documentation: "1-2 hours"

  complexity: medium
  complexity_factors:
    - "Multiple data sources require aggregation"
    - "Charts need responsive design"
    - "Caching strategy adds implementation complexity"

  risks:
    - type: performance
      description: "Metrics calculation may be slow with large datasets"
      severity: medium
      mitigation: "Use materialized views and Redis caching"

    - type: ux
      description: "Charts may not render well on mobile"
      severity: low
      mitigation: "Use responsive chart library, test on devices"

  notes:
    - "Consider WebSocket for real-time updates in future iteration"
    - "Metrics calculation can be moved to background job if needed"
    - "Add monitoring for query performance"
```

### Phase 9: Regenerate Documentation

**Goal**: Update Markdown documentation with technical context.

```bash
python3 .claude/skills/user-story-generator/scripts/generate_story_from_yaml.py --story-id US-0001
```

Verify technical section appears in Markdown:
```markdown
## Technical Details

### Technology Stack

**Frontend:**
- React
- TypeScript
- Recharts
- React Query
- Tailwind CSS

**Backend:**
- FastAPI
- Python 3.11
- Pydantic

**Database:**
- PostgreSQL 15
- SQLAlchemy
- Redis

[... rest of technical section ...]
```

### Phase 10: Present Summary

**Goal**: Report annotation results to user.

```
🛠️  Technical Annotation Complete: US-0001

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Story**: Display key business metrics on dashboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 Technology Stack

**Frontend**: React, TypeScript, Recharts, React Query, Tailwind CSS
**Backend**: FastAPI, Python 3.11, Pydantic
**Database**: PostgreSQL 15, SQLAlchemy, Redis
**Infrastructure**: Docker, GitHub Actions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Implementation Hints (7 provided)

Key recommendations:
1. Create metrics API endpoint: GET /api/v1/metrics/summary
2. Use React Query with 30-second stale time for auto-refresh
3. Implement metrics as PostgreSQL materialized view
4. Cache aggregated metrics in Redis (5-min TTL)
5. Use Recharts LineChart and BarChart components
6. Add loading skeleton (Tailwind animate-pulse)
7. Implement error boundary for chart failures

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Affected Components

**New Components** (4):
- components/Dashboard/MetricsDisplay.tsx
- components/Dashboard/MetricCard.tsx
- api/routes/metrics.py
- models/metrics.py

**Modified** (3):
- components/Dashboard/index.tsx
- api/main.py
- database/schema.sql

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  Effort Estimate

**Total**: 2-3 days

Breakdown:
- Backend API: 4-6 hours
- Frontend components: 8-10 hours
- Database setup: 2-3 hours
- Testing: 3-4 hours
- Documentation: 1-2 hours

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Complexity: Medium

Factors:
- Multiple data sources require aggregation
- Charts need responsive design handling
- Caching strategy adds implementation complexity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Identified Risks (2)

1. **Performance** (Medium severity)
   Issue: Metrics calculation may be slow with large datasets
   Mitigation: Use materialized views and Redis caching

2. **UX** (Low severity)
   Issue: Charts may not render well on mobile
   Mitigation: Use responsive chart library, test on devices

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Additional Notes

- Consider WebSocket for real-time updates in future
- Metrics calculation can move to background job if needed
- Add monitoring for query performance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Files Updated

- stories/yaml-source/US-0001.yaml (technical section added)
- stories/generated-docs/US-0001.md (regenerated with technical context)
```

## Bulk Annotation Mode

**Input**: "Annotate all backlog stories"

**Process**:

1. **Find Stories**:
   ```bash
   find stories/yaml-source -name "US-*.yaml" -exec grep -l "status: backlog" {} \;
   ```

2. **Annotate Each**:
   - Apply same annotation process
   - Reuse common tech stack where appropriate
   - Identify shared components

3. **Present Summary**:
   ```
   🛠️  Bulk Technical Annotation Complete

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   **Annotated**: 8 stories
   **Total Effort**: 18-24 days
   **Average Complexity**: Medium
   **High-Risk Stories**: 2

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📊 Summary by Story

   US-0001: Display key metrics (5pts) - 2-3 days - Medium
   US-0002: Filter by date (3pts) - 1-2 days - Low
   US-0003: Export PDF (3pts) - 1 day - Low
   US-0004: Mobile layout (5pts) - 2 days - Medium
   US-0005: Search (8pts) - 3-4 days - High ⚠️
   US-0006: Collaboration (8pts) - 4-5 days - High ⚠️
   US-0007: Profile edit (3pts) - 1-2 days - Low
   US-0008: Upload photo (5pts) - 2 days - Medium

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   🔧 Common Tech Stack

   All stories use:
   - Frontend: React, TypeScript, Tailwind CSS
   - Backend: FastAPI, Python 3.11
   - Database: PostgreSQL 15

   Story-specific additions noted in each story.

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ⚠️  High-Risk Stories

   US-0005: Advanced search functionality
   - Performance risk with large datasets
   - Complex query optimization needed
   - Consider Elasticsearch for better performance

   US-0006: Real-time collaboration
   - WebSocket scalability concerns
   - Conflict resolution complexity
   - Consider operational transform library

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   💡 Recommendations

   1. Review high-risk stories (US-0005, US-0006) with team
   2. Consider architecture review for collaboration feature
   3. Set up performance monitoring before implementing metrics
   4. Establish Redis caching strategy across all stories
   ```

## Smart Defaults and Inference

### Infer from Story Context

**Example 1**: Story mentions "chart" or "graph"
→ Automatically suggest charting library (Recharts, Chart.js)

**Example 2**: Story mentions "upload" or "file"
→ Suggest file handling libraries, storage solution

**Example 3**: Story mentions "real-time" or "live"
→ Suggest WebSocket, SSE, or polling approach

**Example 4**: Story mentions "export" to PDF/Excel
→ Suggest jsPDF, react-to-pdf, or xlsx library

### Reuse Project Patterns

If project already uses certain technologies:
- Continue using same stack
- Reference existing patterns
- Suggest similar implementations
- Point to existing code examples

## Error Handling

### Missing Story Context
```
⚠️  Insufficient story details for technical annotation

US-0010 has minimal information:
- Vague acceptance criteria
- No specific UI mentioned
- Unclear data requirements

I can provide generic technical notes, but for better guidance:
1. Add more specific acceptance criteria
2. Clarify what data is displayed/edited
3. Specify any performance requirements

Proceed with generic annotation? (yes/no)
```

### Conflicting Technologies
```
⚠️  Technology conflict detected

Story US-0015 suggests using:
- React (from story tags)
- Vue (mentioned in "i_want")

Project standard: React

Recommendation: Use React for consistency
Would you like me to update the story to clarify this?
```

## Integration with Scripts

### Story File Updates
```bash
# Read YAML
cat stories/yaml-source/US-0001.yaml

# Update (manual edit with Edit tool)

# Regenerate markdown
python3 .claude/skills/user-story-generator/scripts/generate_story_from_yaml.py --story-id US-0001
```

## Configuration

Uses project-level configuration from `.claude/skills/user-story-generator/config/automation-config.yaml` (if available):

```yaml
# automation-config.yaml
tech_stack:
  frontend:
    framework: "React"
    language: "TypeScript"
    styling: "Tailwind CSS"
  backend:
    framework: "FastAPI"
    language: "Python 3.11"
  database:
    primary: "PostgreSQL"
    cache: "Redis"

defaults:
  effort_multiplier: 1.0  # Adjust for team velocity
  complexity_threshold: 8  # Stories above this are "complex"
```

## Best Practices

### Be Specific
- ❌ "Use a chart library"
- ✅ "Use Recharts with LineChart component"

### Consider Context
- Check existing codebase patterns
- Align with team expertise
- Consider project constraints

### Be Realistic
- Don't underestimate effort
- Factor in testing time
- Include documentation time

### Identify Risks Early
- Performance concerns
- Security implications
- Integration challenges
- Technical debt

## Remember

- **Actionable**: Provide specific, usable guidance
- **Realistic**: Honest effort estimates and complexity
- **Risk-Aware**: Identify potential problems early
- **Consistent**: Align with project standards
- **Comprehensive**: Cover all technical aspects
- **Pragmatic**: Balance ideal vs. practical solutions
