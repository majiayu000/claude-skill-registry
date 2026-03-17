---
name: plan-feature
description: Gather requirements, analyze codebase, and create structured task lists before starting Rails feature development. Use when planning new features, starting development work, breaking down requirements, or when the user mentions "plan", "requirements", "tasks", or "kickoff".
allowed-tools: Read, Grep, Glob, AskUserQuestion, TodoWrite
---

# Plan Feature Skill

Systematically gather requirements and create implementation plans before starting Rails feature development. Ensures thorough planning, proper task breakdown, and alignment with project conventions.

## When to Use This Skill

Use this skill when:
- User mentions planning a new feature
- Starting development on a new capability
- Breaking down complex requirements
- User says "plan", "requirements", "tasks", "kickoff"
- Beginning work on authentication, CRUD, dashboards, or APIs

## Instructions

Follow these steps systematically when planning a feature:

### Step 1: Understand the Feature Request

Acknowledge the feature request and restate it to confirm understanding:

```
I'll help you plan the implementation of [feature name]. Let me gather requirements and analyze the codebase to create a structured plan.
```

### Step 2: Gather Requirements

Use the AskUserQuestion tool to ask 2-4 focused questions tailored to the feature type.

**For Authentication/Authorization:**
- Authentication method (email/password, OAuth, magic links)
- Session management and duration
- Password requirements and reset flow
- Multi-factor authentication needed?
- Role-based access control requirements

**For CRUD Features (Posts, Comments, etc.):**
- Required fields and validations
- Relationships to existing models
- Permission levels (who can create/edit/delete)
- UI requirements (forms, listings, filters)
- Real-time updates needed?

**For Dashboard/Admin Features:**
- Metrics and data to display
- Filters and search requirements
- Export capabilities
- Access restrictions
- Update frequency (real-time vs static)

**General Questions (always relevant):**
- Target users (all users, admins, specific roles)
- Mobile responsiveness requirements
- Performance considerations
- Integration with existing features

### Step 3: Analyze Codebase

Use Read, Grep, and Glob tools to understand current state:

```ruby
# Check existing models
Glob: "app/models/**/*.rb"

# Find similar features
Grep: Search for related functionality

# Review routes
Read: "config/routes.rb"

# Check migrations
Glob: "db/migrate/**/*.rb"

# Review test structure
Glob: "test/**/*_test.rb"
```

**Look for:**
- Existing models that need relationships
- Similar features to follow as patterns
- Naming conventions in use
- Testing patterns being followed
- Authentication/authorization setup

### Step 4: Create Implementation Plan

Design a comprehensive plan covering:

**Database Layer:**
- New migrations needed
- Model changes or new models
- Associations to add
- Indexes required for performance

**Business Logic:**
- Model validations
- Callbacks (use sparingly)
- Scopes for reusable queries
- Service objects for complex logic

**Controllers & Routes:**
- New controllers or actions needed
- RESTful routes to add
- Nested resources
- API endpoints if applicable

**Views & Frontend:**
- New views or partials
- Forms with proper helpers
- Turbo Frames/Streams for interactivity
- Stimulus controllers for JavaScript
- TailwindCSS styling approach

**Testing:**
- Model tests (validations, associations)
- Controller tests (actions, responses)
- System tests (user workflows)
- Fixtures or factories needed

**Security & Performance:**
- Authorization checks required
- Input sanitization points
- N+1 query prevention
- Caching opportunities

### Step 5: Create Task List

Use TodoWrite tool to create actionable tasks in logical order:

1. **Database setup** - Migrations, models, associations
2. **Business logic** - Validations, scopes, methods
3. **Controllers & routes** - RESTful actions, authorization
4. **Views & frontend** - Forms, Turbo Frames, TailwindCSS
5. **Testing** - Model, controller, system tests
6. **Review & polish** - Linters, security scan, browser testing

Each task should:
- Be specific and actionable
- Include both imperative and active forms
- Follow logical dependencies
- Include testing and review steps

### Step 6: Identify Dependencies & Risks

Call out potential issues:
- **Dependencies**: Gems to install, external services
- **Breaking changes**: Migrations affecting existing data
- **Risks**: Complex logic, performance concerns, security
- **Open questions**: Decisions needed before proceeding

### Step 7: Present Plan Summary

Provide a clear summary:

```
## Feature: [Name]

### Overview
[1-2 sentence description]

### Key Requirements
- Requirement 1
- Requirement 2
- Requirement 3

### Technical Approach
- Database: [brief description]
- Backend: [brief description]
- Frontend: [brief description]
- Testing: [brief description]

### Files to Create/Modify
- db/migrate/xxx_create_table.rb
- app/models/model.rb
- app/controllers/controller.rb
- app/views/resource/
- test/models/model_test.rb

### Tasks Created
[X tasks tracked in todo list]

### Next Steps
1. Review and confirm approach
2. (Optional) Run /refine-requirements to clarify details with follow-up questions
3. (Optional) Run /create-task-files to export tasks to markdown files
4. Start with: [first task]
5. Proceed sequentially through tasks

Ready to start implementation?
```

**Note:** After planning, you can:
- Run `/refine-requirements` to ask follow-up questions and clarify ambiguous requirements
- Run `/create-task-files` to export tasks into structured markdown files (epic, user-story, bug, issue) in a `tasks/` directory for git-based tracking

## Best Practices

**Do:**
- ✅ Ask focused, specific questions
- ✅ Search codebase before suggesting new patterns
- ✅ Follow existing project conventions
- ✅ Break features into small, manageable tasks
- ✅ Consider testing from the start
- ✅ Reference `.claude/rules/*.md` for implementation patterns

**Don't:**
- ❌ Make assumptions - ask when unclear
- ❌ Create vague or ambiguous tasks
- ❌ Ignore existing similar features
- ❌ Skip security considerations
- ❌ Forget mobile responsiveness
- ❌ Plan without understanding current state

## Integration with Project

This skill works within the Rails blog app structure:

- **Follows**: `.claude/CLAUDE.md` for project-specific setup
- **Applies**: `.claude/rules/*.md` for implementation guidelines
- **Uses**: Minitest (not RSpec) for testing
- **Leverages**: Hotwire, TailwindCSS, Solid trilogy
- **Respects**: Rails Omakase philosophy

## Example Usage

**User request:**
```
Plan a blog post commenting system
```

**Skill workflow:**
1. Asks: Comment nesting? Moderation? Real-time updates? Email notifications?
2. Analyzes: Checks for Post model, User model, existing auth patterns
3. Plans: Comment model with polymorphic associations, controller, Turbo Streams
4. Creates: 12 tasks from migration → tests → polish
5. Presents: Summary with technical approach and file list
6. Awaits: User confirmation to begin

## Output

Always use TodoWrite to create trackable tasks with:
- Clear descriptions (imperative: "Create migration", active: "Creating migration")
- Logical ordering (database → logic → UI → tests)
- Testing tasks included
- Review/polish tasks at end

This ensures thorough planning, reduces rework, and aligns with Rails best practices before writing code.
