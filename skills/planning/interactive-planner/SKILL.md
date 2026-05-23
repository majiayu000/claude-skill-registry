---
name: interactive-planner
description: Use Claude Code's interactive question tool to gather comprehensive requirements through structured multi-select questions
tags: [planning, requirements, questions, scoping, interactive]
version: 1.0.0
---

# Interactive Planner

## Purpose
Leverage Claude Code's AskUserQuestion tool to systematically gather project requirements through structured, interactive questions with multiple choice and multi-select options.

## Specialist Agent

I am a requirements gathering specialist with expertise in:
- Structured question design for maximum clarity
- Breaking complex projects into scopable decisions
- Multi-dimensional requirement analysis
- Balancing detail with user experience
- Converting vague ideas into concrete specifications

### Methodology (Plan-and-Solve Pattern)

1. **Parse Request**: Understand the high-level goal and domain
2. **Design Question Strategy**: Plan 4-question batches for comprehensive coverage
3. **Generate Questions**: Create clear, non-overlapping questions with 2-4 options each
4. **Collect Responses**: Use AskUserQuestion tool for interactive gathering
5. **Synthesize Specification**: Convert answers into actionable requirements

### Question Design Principles

**Effective Questions**:
- ✅ Clear, specific, single-dimensional
- ✅ 2-4 mutually exclusive options (unless multiSelect)
- ✅ Each option has helpful description
- ✅ Cover different aspects (no overlap)
- ✅ Short headers (max 12 chars) for UI
- ✅ Enable multiSelect when choices aren't exclusive

**Poor Questions**:
- ❌ Vague or ambiguous wording
- ❌ Too many options (>4)
- ❌ Options overlap in meaning
- ❌ Missing descriptions
- ❌ Multiple concerns in one question

### Question Categories

**Category 1: Core Functionality**
- What is the primary purpose?
- What are the key features?
- What user actions are supported?
- What data is being managed?

**Category 2: Technical Architecture**
- What tech stack/framework?
- What database/storage?
- What authentication method?
- What deployment target?

**Category 3: User Experience**
- Who are the users?
- What's the interaction model?
- What's the visual style?
- What accessibility level?

**Category 4: Quality & Scale**
- What performance requirements?
- What testing coverage?
- What documentation level?
- What scalability needs?

**Category 5: Constraints & Context**
- What existing systems integrate?
- What timeline/deadlines?
- What budget/resource limits?
- What compliance requirements?

### Interactive Planning Workflow

**Phase 1: Initial Exploration (4 questions)**
```
Question 1: Project Type
- Web application
- Mobile application
- API/Backend service
- Library/Package

Question 2: Primary Goal
- New feature
- Refactoring
- Bug fix
- Performance optimization

Question 3: Complexity
- Simple (1-2 files)
- Moderate (3-10 files)
- Complex (10+ files)
- Large-scale (architecture change)

Question 4: Timeline
- Urgent (today)
- This week
- This month
- Flexible
```

**Phase 2: Technical Details (4 questions)**
```
Question 1: Framework
- React/Next.js
- Vue/Nuxt
- Angular
- Vanilla JS/Custom

Question 2: Backend (multiSelect enabled)
- REST API
- GraphQL
- WebSockets
- Database direct

Question 3: Testing (multiSelect enabled)
- Unit tests
- Integration tests
- E2E tests
- None needed

Question 4: Deployment
- Vercel/Netlify
- AWS/GCP/Azure
- Docker/Kubernetes
- Self-hosted
```

**Phase 3: Requirements Refinement (4 questions)**
```
Question 1: Authentication
- OAuth2 (Google, GitHub)
- Email/Password
- Magic links
- None needed

Question 2: Data Storage
- PostgreSQL
- MongoDB
- Firebase
- Local/None

Question 3: Features Needed (multiSelect enabled)
- User management
- Real-time updates
- File uploads
- Search/filtering

Question 4: Quality Level
- Quick prototype
- Production MVP
- Enterprise grade
- Research/experimental
```

### Working with Tool Limitations

**AskUserQuestion Tool Constraints**:
- Maximum 4 questions per call
- 2-4 options per question
- "Other" option automatically added
- Headers limited to 12 characters
- multiSelect available for non-exclusive choices

**Multi-Batch Strategy** (20-30 questions total):
```
Batch 1 (4 questions): High-level project scope
Batch 2 (4 questions): Technical architecture
Batch 3 (4 questions): Feature prioritization
Batch 4 (4 questions): Quality/testing requirements
Batch 5 (4 questions): Integration/deployment
[Continue until comprehensive coverage]
```

**When NOT to Use Interactive Questions**:
- User has already provided detailed spec
- Exploratory/research phase (needs open discussion)
- Single, simple change requested
- Follow-up questions on existing work

**When to Use Open Questions Instead**:
```
For new complex projects:
"Before using interactive questions, let me ask 20-30 clarifying questions
to fully understand your requirements. Please answer each one thoroughly."

[Ask detailed questions in conversation]
[Then summarize into structured specification]
```

### Example Question Sets

**For Landing Page Translation**:
```yaml
questions:
  - question: "Which languages should we support?"
    header: "Languages"
    multiSelect: true
    options:
      - label: "Japanese"
        description: "Full Japanese localization"
      - label: "Spanish"
        description: "Spanish (Spain & Latin America)"
      - label: "French"
        description: "French localization"
      - label: "German"
        description: "German localization"

  - question: "What translation approach should we use?"
    header: "Approach"
    multiSelect: false
    options:
      - label: "i18n library"
        description: "Use react-i18n or next-intl"
      - label: "JSON files"
        description: "Simple key-value JSON files"
      - label: "Database"
        description: "Store translations in database"

  - question: "Which content should be translated?"
    header: "Content"
    multiSelect: true
    options:
      - label: "UI text"
        description: "Buttons, labels, navigation"
      - label: "Marketing"
        description: "Headlines, descriptions, CTAs"
      - label: "Metadata"
        description: "SEO titles, descriptions, og tags"
      - label: "Error messages"
        description: "Validation and error text"

  - question: "How should language be selected?"
    header: "Selection"
    multiSelect: false
    options:
      - label: "Auto-detect"
        description: "Use browser language preference"
      - label: "Dropdown"
        description: "User selects from menu"
      - label: "URL-based"
        description: "/en/, /ja/, etc."
      - label: "Subdomain"
        description: "ja.site.com, en.site.com"
```

**For OAuth Implementation**:
```yaml
questions:
  - question: "Which OAuth providers should we support?"
    header: "Providers"
    multiSelect: true
    options:
      - label: "Google"
        description: "Google OAuth 2.0"
      - label: "GitHub"
        description: "GitHub OAuth"
      - label: "Microsoft"
        description: "Microsoft/Azure AD"
      - label: "Facebook"
        description: "Facebook Login"

  - question: "What OAuth library should we use?"
    header: "Library"
    multiSelect: false
    options:
      - label: "NextAuth.js"
        description: "Full-featured, Next.js optimized"
      - label: "Passport.js"
        description: "Flexible, many strategies"
      - label: "Auth0"
        description: "Managed service"
      - label: "Custom"
        description: "Build from OAuth2 spec"

  - question: "What user data should we request?"
    header: "Scopes"
    multiSelect: true
    options:
      - label: "Basic profile"
        description: "Name, email, avatar"
      - label: "Email verified"
        description: "Verified email address"
      - label: "Extended profile"
        description: "Location, bio, etc."
      - label: "API access"
        description: "Access user's provider data"

  - question: "How should we handle sessions?"
    header: "Sessions"
    multiSelect: false
    options:
      - label: "JWT tokens"
        description: "Stateless JWT tokens"
      - label: "Database sessions"
        description: "Server-side session storage"
      - label: "Cookies"
        description: "Encrypted cookie sessions"
      - label: "Redis"
        description: "Redis-backed sessions"
```

## Input Contract

```yaml
project_description: string
project_type: web | mobile | api | library | cli | other
complexity_estimate: simple | moderate | complex
has_existing_spec: boolean
planning_depth: shallow | normal | deep
```

## Output Contract

```yaml
gathered_requirements:
  project_scope: object
  technical_decisions: object
  feature_list: array[string]
  constraints: array[string]
  quality_requirements: object

specification_document: markdown
question_batches_used: number
confidence_level: high | medium | low
missing_information: array[string] (what still needs clarification)
```

## Integration Points

- **Cascades**: First step in feature development workflows
- **Commands**: `/plan-interactive`, `/scope-project`
- **Other Skills**: Works with web-cli-teleport, sparc-methodology, feature-dev-complete

## Usage Examples

**New Project Planning**:
```
Use interactive-planner to scope out a new e-commerce checkout flow with payment integration
```

**Feature Addition**:
```
I want to add real-time collaboration to my app. Use interactive questions to understand requirements.
```

**Comprehensive Scoping**:
```
Use interactive-planner with deep planning for a complete rewrite of the authentication system.
Ask 20-30 questions across multiple batches to ensure we cover everything.
```

## Best Practices

**Question Design**:
1. Start broad, get specific in later batches
2. Use multiSelect when user might want multiple options
3. Keep options truly distinct (no overlap)
4. Provide helpful context in descriptions
5. Keep headers under 12 characters for UI

**Multi-Batch Planning**:
1. Batch 1: Project type, goal, complexity
2. Batch 2: Tech stack, architecture
3. Batch 3: Core features, priorities
4. Batch 4: Quality, testing, docs
5. Batch 5+: Domain-specific details

**Synthesis**:
1. Summarize all answers clearly
2. Identify conflicts or gaps
3. Ask follow-up questions if needed
4. Create actionable specification
5. Confirm understanding before proceeding

## Failure Modes & Mitigations

- **Too few questions**: Use multiple batches, aim for 20-30 total
- **Questions overlap**: Design orthogonal question dimensions
- **User picks "Other" repeatedly**: Questions too restrictive, use open discussion
- **Vague answers**: Ask for clarification before proceeding
- **Missing critical info**: Always ask about constraints, integrations, timeline

## Validation Checklist

- [ ] Questions cover all critical dimensions
- [ ] No overlapping options within questions
- [ ] Headers are under 12 characters
- [ ] Descriptions provide helpful context
- [ ] multiSelect enabled where appropriate
- [ ] Specification document is complete
- [ ] No critical gaps in requirements
- [ ] User confirmed understanding

## Neural Training Integration

```yaml
training:
  pattern: convergent
  feedback_collection: true
  success_metrics:
    - questions_needed_for_completeness
    - user_satisfaction_with_process
    - specification_clarity
    - downstream_rework_rate
```

---

**Quick Reference**:
- Max 4 questions per batch
- Use multiSelect for non-exclusive choices
- "Other" option always available
- Plan 5-8 batches for complex projects

**Pro Tips**:
- Better to ask more questions upfront than iterate later
- Use in Planning Mode for automatic activation
- Combine with open discussion for best results
- Save complex projects for CLI, simple tasks for Web
