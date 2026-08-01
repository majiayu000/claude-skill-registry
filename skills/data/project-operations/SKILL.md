---
name: project-operations
description: Provides intelligent project setup and management with agent-based architecture
  to minimize token usage. Auto-activates when user mentions project setup, "add project",
  "configure project", "monorepo"
---

---
name: project-operations
description: Provides intelligent project setup and management with agent-based architecture to minimize token usage. Auto-activates when user mentions project setup, "add project", "configure project", "monorepo", "subdirectories", "switch project", or "project info". Uses three specialized agents internally: project-detector (detect active), project-config-loader (load settings with validation), project-context-manager (manage active project). Guides through four workflows: Add New Project (setup + templates), Configure Monorepo (pattern matching + subdirectories), Switch Between Projects (auto or manual), View Project Information. Provides templates for common architectures (fullstack-with-jira, fullstack-linear-only, mobile-app, monorepo). Validates configuration and suggests fixes for errors. Handles context-aware error handling with specific fix suggestions.
---

# Project Operations Skill

This skill handles all project-related operations in CCPM, including setup, configuration, detection, and multi-project management. It automatically invokes specialized agents to optimize performance and reduce token usage.

## Instructions

### Automatic Activation

This skill activates when user mentions:
- Project setup or configuration
- Adding/updating/deleting projects
- Multi-project management
- Monorepo or subdirectory configuration
- Project switching or detection
- Active project context

### Core Principles

1. **Agent-First Approach**: Always use specialized agents for project operations
2. **Minimal Token Usage**: Agents handle heavy logic, skills provide guidance
3. **Context-Aware**: Detect project context before operations
4. **User-Friendly**: Clear errors and actionable suggestions

### Agent Usage Patterns

#### Pattern 1: Detect Project Context

**When**: Command needs to know active project

**Implementation**:
```javascript
// Always start with detection
const detection = Task(project-detector): `
Detect active project for current environment

Current directory: ${cwd}
Git remote: ${gitRemote}
`

// Then load full config
const context = Task(project-context-manager): `
Get full context for detected project
Project ID: ${detection.project_id}
Subproject: ${detection.subproject}
Include config: true
Format: standard
`

// Use context for operations
console.log(`📋 Project: ${context.display.title}`)
```

**Benefits**:
- Consistent detection logic
- Reduces token usage (agent handles logic)
- Structured output ready for use

#### Pattern 2: Load Project Configuration

**When**: Command needs project settings (Linear, Jira, tech stack)

**Implementation**:
```javascript
const config = Task(project-config-loader): `
Load configuration for project: ${projectId}
Include subproject: ${subprojectName}
Validate: true
`

if (!config.validation.valid) {
  console.error("Configuration errors:", config.validation.errors)
  return
}

// Use config
const linearTeam = config.linear.team
const techStack = config.tech_stack.languages
```

**Benefits**:
- Validation built-in
- Structured, type-safe output
- Errors with actionable messages

#### Pattern 3: Manage Project Context

**When**: Setting active project, enabling auto-detection

**Implementation**:
```javascript
// Set active project
const result = Task(project-context-manager): `
Set active project: ${projectId}
Mode: manual
Disable auto-detection: false
`

console.log(`✅ ${result.message}`)

// Or enable auto-detection
const result = Task(project-context-manager): `
Enable auto-detection
`

console.log(`✅ Auto-detection enabled`)
console.log(`Methods: ${result.methods.join(', ')}`)
```

### Project Setup Workflows

#### Workflow 1: Add New Project

**Trigger phrases**:
- "add a new project"
- "configure new project"
- "set up project"

**Command**: `/ccpm:project:add <project-id> [--template TEMPLATE]`

**Guidance**:
```
Let's set up your new project!

Quick templates available:
1. fullstack-with-jira - Full-stack app with Jira integration
2. fullstack-linear-only - Full-stack app, Linear-only
3. mobile-app - React Native / Expo mobile app
4. monorepo - Multi-project repository with subdirectories

Or create custom configuration interactively.

Example:
/ccpm:project:add my-app --template fullstack-with-jira
```

#### Workflow 2: Configure Monorepo with Subdirectories

**Trigger phrases**:
- "monorepo setup"
- "subdirectories"
- "multiple projects in one repo"

**Guidance**:
```
For monorepos with subdirectories (like Nx, Turborepo):

1. Add the project:
   /ccpm:project:add my-monorepo

2. Configure subdirectory detection:
   Edit ~/.claude/ccpm-config.yaml:

   ```yaml
   my-monorepo:
     repository:
       local_path: /Users/dev/monorepo

     context:
       detection:
         subdirectories:
           - subproject: frontend
             match_pattern: "*/apps/frontend/*"
             priority: 10
           - subproject: backend
             match_pattern: "*/apps/backend/*"
             priority: 10

     code_repository:
       subprojects:
         - name: frontend
           path: apps/frontend
           tech_stack:
             languages: [typescript]
             frameworks:
               frontend: [react, nextjs]
   ```

3. Enable auto-detection:
   /ccpm:project:set auto

4. Test detection:
   cd /Users/dev/monorepo/apps/frontend
   /ccpm:project:list  # Should show "frontend" subproject active
```

#### Workflow 3: Switch Between Projects

**Trigger phrases**:
- "switch project"
- "change active project"
- "work on different project"

**Commands**:
- `/ccpm:project:set <project-id>` - Set specific project
- `/ccpm:project:set auto` - Enable auto-detection
- `/ccpm:project:list` - See all projects with active marker

**Agent usage**:
```javascript
// Commands internally use:
Task(project-context-manager): `
Set active project: ${projectId}
Mode: manual
`

// Then display with:
Task(project-context-manager): `
Get context
Format: standard
`
```

#### Workflow 4: View Project Information

**Trigger phrases**:
- "show project details"
- "what's my current project"
- "project info"

**Commands**:
- `/ccpm:project:show <project-id>` - Detailed project info
- `/ccpm:project:list` - List all projects
- `/ccpm:work <issue-id>` - Task with project context

**Agent usage**:
```javascript
Task(project-context-manager): `
Get context for project: ${projectId}
Format: detailed
Include all sections: true
`

// Returns full display-ready output
```

### Monorepo Support

CCPM provides first-class monorepo support with automatic subdirectory detection, pattern-based matching, and intelligent context switching.

#### What is Monorepo Support?

Monorepos contain multiple projects/packages in a single repository (e.g., Nx, Turborepo, Lerna). CCPM automatically detects which subproject you're working in and applies the correct configuration.

**Key Features**:
- Auto-detection based on working directory
- Pattern-based matching with glob patterns
- Priority weighting for conflict resolution
- Per-subproject tech stack and configuration
- Seamless context switching on `cd`
- Performance: <100ms auto-detect, 0ms manual mode

#### How Subdirectory Detection Works

**Priority-Based Resolution** (highest to lowest):
1. **Manual Setting**: User explicitly set project with `/ccpm:project:set`
2. **Git Remote Match**: Matches repository URL to project config
3. **Subdirectory Pattern Match**: Matches current directory against glob patterns
4. **Local Path Match**: Falls back to project root directory match
5. **Custom Patterns**: User-defined patterns with priority weighting

**Detection Flow Example**:
```
Working in: /Users/dev/repeat/jarvis/src

Detection flow:
1. Check manual override → None set
2. Check git remote → matches "repeat" project ✓
3. Check subdirectory patterns:
   - "*/xygaming_symfony/*" (priority: 10) → ❌
   - "*/jarvis/*" (priority: 10) → ✅ Match!
4. Return: project="repeat", subproject="jarvis"

Result:
📋 Project: Repeat › jarvis
🛠️ Tech Stack: TypeScript, Next.js, NestJS
```

**Performance**:
- Auto-detection: <100ms (cached for session)
- Manual mode: 0ms (no detection overhead)
- Session cache: Detection runs once per command

#### Subdirectory Configuration Commands

Use these commands to manage subdirectories in monorepos:

##### Add Subdirectory
```bash
/ccpm:project:subdir:add <project-id> <subproject-name> <path> [--pattern <pattern>] [--priority <priority>]
```

**Example**:
```bash
# Add frontend subproject
/ccpm:project:subdir:add my-monorepo frontend apps/frontend \
  --pattern "*/apps/frontend/*" \
  --priority 10

# Add backend with higher priority
/ccpm:project:subdir:add my-monorepo backend apps/backend \
  --pattern "*/apps/backend/*" \
  --priority 15
```

##### List Subdirectories
```bash
/ccpm:project:subdir:list <project-id>
```

Shows all configured subdirectories with patterns and priorities.

##### Update Subdirectory
```bash
/ccpm:project:subdir:update <project-id> <subproject-name> [--field <field>]
```

**Examples**:
```bash
# Update pattern
/ccpm:project:subdir:update my-monorepo frontend --field pattern="*/web/*"

# Update priority
/ccpm:project:subdir:update my-monorepo backend --field priority=20

# Update tech stack
/ccpm:project:subdir:update my-monorepo mobile --field tech_stack.languages=["typescript", "swift"]
```

##### Remove Subdirectory
```bash
/ccpm:project:subdir:remove <project-id> <subproject-name>
```

#### Pattern-Based Detection

**Glob Pattern Syntax**:
- `*` - Matches any characters within a directory level
- `**` - Matches any number of directory levels
- `?` - Matches single character
- `[abc]` - Matches any character in set

**Pattern Examples**:
```yaml
# Exact subdirectory match
match_pattern: "*/apps/frontend/*"
# Matches: /any/path/apps/frontend/src/file.ts

# Multi-level wildcard
match_pattern: "**/packages/ui/**"
# Matches: /any/path/packages/ui/src/components/Button.tsx

# Multiple alternatives (use separate rules)
# For apps/web or web/
- match_pattern: "*/apps/web/*"
  priority: 10
- match_pattern: "*/web/*"
  priority: 5  # Lower priority (less specific)
```

**Priority Weighting**:
- Higher number = higher priority
- Use priorities to resolve conflicts
- Recommended: 10 for standard, 15-20 for specific, 5 for fallback

**Conflict Resolution Example**:
```yaml
subdirectories:
  # Specific match wins
  - subproject: admin-frontend
    match_pattern: "*/apps/admin/*"
    priority: 15

  # General match (fallback)
  - subproject: frontend
    match_pattern: "*/apps/*"
    priority: 5

# Working in: /apps/admin/src
# Result: admin-frontend (priority 15 > 5)
```

#### Project Context Switching

**Auto-Detection Mode** (recommended for monorepos):
```bash
# Enable auto-detection
/ccpm:project:set auto

# Now just cd to switch context
cd /Users/dev/monorepo/apps/frontend
# → Auto-detects: my-monorepo › frontend

cd /Users/dev/monorepo/apps/backend
# → Auto-detects: my-monorepo › backend
```

**Manual Mode** (stable across sessions):
```bash
# Set specific project
/ccpm:project:set my-monorepo

# Context stays stable even if you cd
cd /Users/dev/other-repo
# → Still: my-monorepo (no auto-detection)
```

**When to Use Each**:
- **Auto-detection**: Daily development, switching between subprojects frequently
- **Manual mode**: Working on one subproject for extended period, avoiding auto-switch

#### Monorepo Configuration Format

```yaml
projects:
  my-monorepo:
    repository:
      local_path: /Users/dev/monorepo
      git_remote: github.com/org/monorepo

    # Subdirectory detection rules
    context:
      detection:
        subdirectories:
          - subproject: frontend
            match_pattern: "*/apps/frontend/*"
            priority: 10

          - subproject: backend
            match_pattern: "*/apps/backend/*"
            priority: 10

          - subproject: mobile
            match_pattern: "*/apps/mobile/*"
            priority: 10

    # Subproject metadata (optional but recommended)
    code_repository:
      subprojects:
        - name: frontend
          path: apps/frontend
          description: Next.js web application
          tech_stack:
            languages: [typescript]
            frameworks:
              frontend: [react, nextjs, tailwindcss]

        - name: backend
          path: apps/backend
          description: NestJS API server
          tech_stack:
            languages: [typescript]
            frameworks:
              backend: [nestjs, prisma]

        - name: mobile
          path: apps/mobile
          description: React Native mobile app
          tech_stack:
            languages: [typescript]
            frameworks:
              mobile: [react-native, expo]
```

#### Monorepo Examples

##### Example 1: Simple Frontend/Backend Monorepo

```yaml
# Project structure:
# monorepo/
#   apps/
#     web/       - Next.js
#     api/       - Express
#   packages/
#     shared/    - Shared utilities

my-monorepo:
  repository:
    local_path: /Users/dev/monorepo

  context:
    detection:
      subdirectories:
        - subproject: web
          match_pattern: "*/apps/web/*"
          priority: 10

        - subproject: api
          match_pattern: "*/apps/api/*"
          priority: 10

        - subproject: shared
          match_pattern: "*/packages/shared/*"
          priority: 5  # Lower priority (fallback)

  code_repository:
    subprojects:
      - name: web
        path: apps/web
        tech_stack:
          languages: [typescript]
          frameworks:
            frontend: [react, nextjs]

      - name: api
        path: apps/api
        tech_stack:
          languages: [typescript]
          frameworks:
            backend: [express, prisma]
```

##### Example 2: Complex Package-Based Monorepo

```yaml
# Project structure:
# monorepo/
#   packages/
#     ui/           - Component library
#     api-client/   - API SDK
#     utils/        - Utilities
#     config/       - Shared config

my-packages:
  repository:
    local_path: /Users/dev/packages

  context:
    detection:
      subdirectories:
        # Use wildcard for all packages
        - subproject: ui
          match_pattern: "**/packages/ui/**"
          priority: 10

        - subproject: api-client
          match_pattern: "**/packages/api-client/**"
          priority: 10

        - subproject: utils
          match_pattern: "**/packages/utils/**"
          priority: 8

        # Fallback for other packages
        - subproject: core
          match_pattern: "**/packages/**"
          priority: 3

  code_repository:
    subprojects:
      - name: ui
        path: packages/ui
        tech_stack:
          languages: [typescript]
          frameworks:
            frontend: [react, tailwindcss]

      - name: api-client
        path: packages/api-client
        tech_stack:
          languages: [typescript]
```

##### Example 3: Multi-Team Enterprise Monorepo

```yaml
# Project structure:
# enterprise/
#   teams/
#     commerce/     - E-commerce team
#       web/
#       api/
#     marketing/    - Marketing team
#       landing/
#       cms/

enterprise:
  repository:
    local_path: /Users/dev/enterprise

  context:
    detection:
      subdirectories:
        # Commerce team
        - subproject: commerce-web
          match_pattern: "*/teams/commerce/web/*"
          priority: 15

        - subproject: commerce-api
          match_pattern: "*/teams/commerce/api/*"
          priority: 15

        # Marketing team
        - subproject: marketing-landing
          match_pattern: "*/teams/marketing/landing/*"
          priority: 15

        - subproject: marketing-cms
          match_pattern: "*/teams/marketing/cms/*"
          priority: 15

        # Fallback by team
        - subproject: commerce
          match_pattern: "*/teams/commerce/*"
          priority: 8

        - subproject: marketing
          match_pattern: "*/teams/marketing/*"
          priority: 8

  code_repository:
    subprojects:
      - name: commerce-web
        path: teams/commerce/web
        tech_stack:
          languages: [typescript]
          frameworks:
            frontend: [react, nextjs]

      - name: commerce-api
        path: teams/commerce/api
        tech_stack:
          languages: [typescript]
          frameworks:
            backend: [nestjs, graphql]
```

#### Monorepo Best Practices

##### 1. Pattern Design

**DO**:
- Use specific patterns with high priority for primary subprojects
- Add fallback patterns with lower priority for misc directories
- Test patterns match expected directories
- Document pattern logic in config comments

**DON'T**:
- Use overly broad patterns (e.g., `*/*`)
- Set all patterns to same priority (ambiguous)
- Forget to update patterns when restructuring

##### 2. Priority Assignment

**Recommended Priority Scheme**:
- **20-25**: Very specific (exact team/product match)
- **10-15**: Standard subprojects (apps, packages)
- **5-9**: Fallback patterns (general matches)
- **1-4**: Catch-all (rarely used)

**Example**:
```yaml
- match_pattern: "*/apps/admin/dashboard/*"  # Very specific
  priority: 20

- match_pattern: "*/apps/admin/*"            # Specific
  priority: 15

- match_pattern: "*/apps/*"                  # General
  priority: 5
```

##### 3. Organization Conventions

**Naming**:
- Use kebab-case for subproject names: `commerce-web`, `marketing-api`
- Match subproject name to directory when possible
- Use team prefixes for multi-team repos: `team-commerce`, `team-marketing`

**Structure**:
- Group related subprojects in config
- Order by priority (highest first) for readability
- Add comments explaining complex patterns

##### 4. Performance Optimization

**Cache Friendly**:
- Enable auto-detection mode (detection cached per session)
- Avoid excessive pattern matching (max ~10 patterns per project)
- Use manual mode for long-running sessions on one subproject

**Detection Speed**:
```yaml
# Good: 3 patterns, clear priorities
subdirectories:
  - subproject: frontend
    match_pattern: "*/apps/web/*"
    priority: 10
  - subproject: backend
    match_pattern: "*/apps/api/*"
    priority: 10
  - subproject: shared
    match_pattern: "*/packages/*"
    priority: 5

# Avoid: Too many overlapping patterns
subdirectories:
  - subproject: web
    match_pattern: "*/apps/web/*"
    priority: 10
  - subproject: web
    match_pattern: "*/web/*"
    priority: 9
  - subproject: web
    match_pattern: "**/web/**"
    priority: 8
  # ... (redundant patterns slow detection)
```

##### 5. Tech Stack Configuration

**Per-Subproject Stacks**:
```yaml
subprojects:
  - name: web
    tech_stack:
      languages: [typescript]
      frameworks:
        frontend: [react, nextjs]
      tools: [tailwindcss, vitest]

  - name: api
    tech_stack:
      languages: [typescript]
      frameworks:
        backend: [nestjs, prisma]
      tools: [jest, swagger]
```

**Benefits**:
- Agent selection uses subproject stack
- Commands show relevant tech context
- Better tool recommendations

##### 6. Testing Configuration

**Verify Detection**:
```bash
# Test each subproject
cd /path/to/monorepo/apps/frontend
/ccpm:project:list  # Should show correct subproject

cd /path/to/monorepo/apps/backend
/ccpm:project:list  # Should switch automatically
```

**Test Pattern Conflicts**:
```bash
# Create conflicting patterns intentionally
# Verify highest priority wins

cd /path/to/ambiguous/directory
/ccpm:project:list  # Should match highest priority pattern
```

##### 7. Migration from Single Project

**Steps**:
1. Start with existing single project config
2. Add subdirectory detection rules
3. Define subproject metadata
4. Test auto-detection in each directory
5. Enable auto-detection mode
6. Update team documentation

**Before** (single project):
```yaml
my-app:
  repository:
    local_path: /Users/dev/my-app
```

**After** (monorepo):
```yaml
my-app:
  repository:
    local_path: /Users/dev/my-app

  context:
    detection:
      subdirectories:
        - subproject: web
          match_pattern: "*/apps/web/*"
          priority: 10
        - subproject: api
          match_pattern: "*/apps/api/*"
          priority: 10

  code_repository:
    subprojects:
      - name: web
        path: apps/web
      - name: api
        path: apps/api
```

### Error Handling

#### No Project Detected

**Error**:
```
❌ Could not detect active project

Suggestions:
- Set active project: /ccpm:project:set <project-id>
- Enable auto-detection: /ccpm:project:set auto
- Check you're in a configured project directory
```

**Solution with agents**:
```javascript
const detection = Task(project-detector): "Detect active project"

if (detection.error) {
  console.log(detection.error.message)
  console.log("\nSuggestions:")
  detection.error.suggestions.forEach(s => console.log(`- ${s}`))
}
```

#### Configuration Error

**Error**:
```
❌ Project configuration invalid

Project 'my-app' missing required field: linear.team

Fix with: /ccpm:project:update my-app --field linear.team
```

**Solution with agents**:
```javascript
const config = Task(project-config-loader): `
Load project: ${projectId}
Validate: true
`

if (!config.validation.valid) {
  config.validation.errors.forEach(err => {
    console.error(`❌ ${err.message}`)
    err.actions?.forEach(action => console.log(`   Fix: ${action}`))
  })
}
```

### Best Practices

1. **Always Detect First**: Start commands with project detection
2. **Use Agents for Logic**: Don't reimplement detection/loading
3. **Cache Context**: Detect once, use throughout command
4. **Display Context**: Show users which project is active
5. **Handle Errors Gracefully**: Provide actionable error messages
6. **Support Auto-Detection**: Let users work naturally

### Command Integration Examples

#### Example 1: Planning Command with Project Context

```markdown
# In /ccpm:plan

Task(project-context-manager): `
Get active project context
Include: detection + config
Format: compact
`

# Display: 📋 Project: My Monorepo › frontend

# Use context for Linear:
linear_create_issue({
  team: context.config.linear.team,
  project: context.config.linear.project,
  labels: context.display.labels
})
```

#### Example 2: Implementation Command with Subproject Info

```markdown
# In /ccpm:work

const context = Task(project-context-manager): "Get context"

console.log(`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 Starting Implementation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project:     ${context.config.project_name}
Subproject:  ${context.config.subproject?.name || 'N/A'}
Tech Stack:  ${context.display.subtitle}
Location:    ${context.display.location}
`)

# Agent selection uses tech stack:
const agents = selectAgents(context.config.subproject?.tech_stack || context.config.tech_stack)
```

### Performance Optimizations

1. **Agent Caching**: Agents handle caching internally
2. **Lazy Loading**: Only load config when needed
3. **Parallel Ops**: Detect and load in parallel when possible
4. **Session State**: Cache detection result for command duration

### Testing

Test with these scenarios:

1. **Simple Project**: Single repo, no subdirectories
2. **Monorepo**: Multiple subdirectories with patterns
3. **Manual Override**: User sets specific project
4. **Auto-Detection**: Switch directories, auto-detect
5. **No Config**: Fresh install, guide user to setup
6. **Invalid Config**: Missing fields, show validation errors

### Related Commands

**Project Management**:
- `/ccpm:project:add` - Add new project
- `/ccpm:project:list` - List all projects
- `/ccpm:project:show` - Show project details
- `/ccpm:project:set` - Set active project
- `/ccpm:project:update` - Update project config
- `/ccpm:project:delete` - Delete project

**Monorepo Subdirectories**:
- `/ccpm:project:subdir:add` - Add subdirectory to project
- `/ccpm:project:subdir:list` - List project subdirectories
- `/ccpm:project:subdir:update` - Update subdirectory config
- `/ccpm:project:subdir:remove` - Remove subdirectory

### Maintenance

**When to update this skill**:
- New project config fields added
- New detection methods implemented
- Agent interfaces change
- New project templates added

**Update locations**:
- This skill (guidance and examples)
- Project agents (implementation)
- Command files (integration)
- Documentation (user-facing guides)
