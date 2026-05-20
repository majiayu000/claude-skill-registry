---
name: one-way-door
description: Use this skill when creating new files that represent architectural decisions — data models, infrastructure configs, auth boundaries, API contracts, CI/CD pipelines, or event systems. Flags irreversible decisions and forces a discussion about trade-offs before committing.
---

# One-way door check

Some decisions are easy to reverse — you can change a UI component, rename a variable, or swap a utility function with no lasting consequences. These are **two-way doors**: walk through, and if it's wrong, walk back.

Other decisions create gravity. Once traffic, users, or other code depends on them, changing course gets expensive. A database schema migration after launch. An API contract that external consumers rely on. An auth boundary that shapes your entire permission model. These are **one-way doors**.

The most expensive mistakes in software aren't bugs. They're irreversible architectural decisions made too quickly.

## What gets flagged

### Data models and database schemas

Files matching: `schema.prisma`, `schema.graphql`, `*.sql`, `migration*`, `models.py`, `models.ts`, `entities.py`, `entities.ts`

Data models are the hardest decisions to reverse. Once your database has rows, every schema change requires a migration. Column renames break queries. Relationship changes cascade through your entire application.

**Questions to ask:**
- Have you mapped all the relationships between entities?
- Will this schema support the queries you need without N+1 problems?
- Are you normalizing appropriately for your read/write patterns?

### Infrastructure and deployment configs

Files matching: `docker-compose*`, `Dockerfile`, `*.tf`, `terraform*`, `pulumi*`, `cdk*`, `cloudformation*`, `k8s*`, `kubernetes*`, `helm*`

Infrastructure choices constrain everything built on top of them. Switching from ECS to Kubernetes, or from Lambda to containers, affects deployment pipelines, monitoring, scaling, and team knowledge.

**Questions to ask:**
- Is this the simplest infrastructure that meets your needs?
- What's your team's operational experience with this stack?
- What does failure recovery look like?

### Authentication and authorization

Files matching: `auth.ts`, `auth.js`, `auth.py`, `firestore.rules`, `storage.rules`, `*.rules`, `rbac*`, `permissions*`, `security*`

Auth boundaries are load-bearing walls. Session vs JWT, role-based vs attribute-based, single-tenant vs multi-tenant — each choice shapes your security model, user experience, and compliance posture.

**Questions to ask:**
- Does this cover all your user types and access patterns?
- How will you handle token refresh, session expiry, and revocation?
- Are you building for single-tenant or multi-tenant from the start?

### API contracts and service interfaces

Files matching: `openapi*`, `swagger*`, `*.proto`, `*.graphql`, `api-schema*`, `routes.ts`, `routes.js`, `routes.py`

Published APIs are promises to consumers. Breaking changes require versioning, deprecation periods, and migration guides. Internal APIs between services create coupling that's hard to unwind.

**Questions to ask:**
- Who will consume this API? Internal services, external developers, or both?
- How will you version breaking changes?
- Are you exposing implementation details that should stay private?

### Event systems and message buses

Files matching: `events.ts`, `eventbus.ts`, `eventemitter.py`, `eventhandler.py`, `pubsub*`, `queue*`, `kafka*`, `rabbit*`

Event schemas are contracts between producers and consumers. Once multiple services subscribe to an event, changing its shape requires coordinated deploys. Event ordering assumptions become architectural constraints.

**Questions to ask:**
- Have you defined the event schema, including required vs optional fields?
- What happens when a consumer fails to process an event?
- Do you need ordering guarantees?

### CI/CD pipelines

Files in: `.github/`, `.gitlab/`, `.circleci/`, or matching `Jenkinsfile`, `.travis.yml`, `cloudbuild*`

CI/CD pipelines become the backbone of your release process. Teams build muscle memory around deploy workflows. Changing pipeline structure means retraining, and broken deploys during the transition can block your entire team.

**Questions to ask:**
- Does this pipeline support your branching strategy?
- What's the rollback procedure if a deploy fails?
- Are secrets handled securely?

### Dependency and package configs

Files matching: `package.json`, `Cargo.toml`, `go.mod`, `requirements.txt`, `pyproject.toml`, `Gemfile`

Framework and dependency choices ripple through your entire codebase. Switching from React to Vue, or from Express to Fastify, means rewriting large portions of your application.

**Questions to ask:**
- Is this dependency actively maintained?
- Does it handle your scale requirements?
- What's the migration path if you need to switch?

### Cloud service configs

Files matching: `firebase.json`, `.firebaserc`, `firestore.indexes*`

Cloud service configs lock you into specific providers and architectures. Firestore indexes determine query performance. Firebase rules define your security boundary.

**Questions to ask:**
- Are you comfortable with this provider for the long term?
- Have you tested these indexes against your actual query patterns?
- What's the exit strategy if you need to migrate?

## Two-way doors (what passes through)

These file types are safe to decide quickly and change later:

- **UI components** — React/Vue/Svelte components, CSS, templates
- **Utility functions** — Helpers, formatters, validators
- **Test files** — Test infrastructure can be refactored freely
- **Documentation** — README, guides, comments
- **Logging and monitoring** — Log formats, metric names
- **Configuration files** — `.env`, feature flags, app config
- **Static assets** — Images, fonts, icons

## How to implement

### Option 1: CLAUDE.md rule

Add this to your project's `CLAUDE.md`:

```markdown
### One-way door check
Before creating new files that represent architectural decisions, ask: "Which of these decisions would be difficult to reverse?" One-way doors include data models, service communication patterns, auth boundaries, tenancy models, and infrastructure configs. These create gravity — once traffic, users, or other code depends on them, changing course gets expensive. If a decision is a one-way door, pause and discuss the trade-offs before committing. Two-way doors (UI components, utilities, styling) can be decided quickly and changed later.
```

### Option 2: PreToolUse hook (automated enforcement)

Add this to your Claude Code `settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/one-way-door-check.sh"
          }
        ]
      }
    ]
  }
}
```

### The hook script

```bash
#!/bin/sh
# One-way door check hook (PreToolUse:Write)
# Flags architectural decisions that are hard to reverse.

INPUT=$(cat)
[ -z "$INPUT" ] && exit 0

# Extract the file path from tool_input
FILE_PATH=$(echo "$INPUT" | grep -oP '"file_path"\s*:\s*"[^"]*"' | head -1 | sed 's/.*"file_path"\s*:\s*"//;s/"//')
[ -z "$FILE_PATH" ] && exit 0

FILENAME=$(basename "$FILE_PATH")
FILENAME_LOWER=$(echo "$FILENAME" | tr "[:upper:]" "[:lower:]")
DIR=$(dirname "$FILE_PATH")

ONE_WAY=0
REASON=""

# Database schemas and migrations
if echo "$FILENAME_LOWER" | grep -qE "schema\.(prisma|graphql|sql)|migration|\.sql$|models?\.(py|ts|js)$|entities?\.(py|ts|js)$"; then
    ONE_WAY=1
    REASON="data model / database schema"
fi

# Infrastructure and deployment configs
if echo "$FILENAME_LOWER" | grep -qE "^(docker-compose|dockerfile|terraform|pulumi|cdk)|\.tf$|cloudformation|k8s|kubernetes|helm"; then
    ONE_WAY=1
    REASON="infrastructure / deployment config"
fi

# Authentication and authorization
if echo "$FILENAME_LOWER" | grep -qE "auth\.(ts|js|py)|firestore\.rules|storage\.rules|security|\.rules$|rbac|permissions"; then
    ONE_WAY=1
    REASON="auth / security rules"
fi

# API contracts and service interfaces
if echo "$FILENAME_LOWER" | grep -qE "openapi|swagger|\.proto$|\.graphql$|api-schema|routes\.(ts|js|py)$"; then
    ONE_WAY=1
    REASON="API contract / service interface"
fi

# Event systems and message queues
if echo "$FILENAME_LOWER" | grep -qE "event(s|bus|emitter|handler)\.(ts|js|py)$|pubsub|queue|kafka|rabbit"; then
    ONE_WAY=1
    REASON="event system / message bus"
fi

# Package manager configs (dependency choices)
if echo "$FILENAME_LOWER" | grep -qE "^(package\.json|cargo\.toml|go\.mod|requirements\.txt|pyproject\.toml|gemfile)$"; then
    ONE_WAY=1
    REASON="dependency / package config"
fi

# Firebase and cloud service configs
if echo "$FILENAME_LOWER" | grep -qE "^firebase\.json$|^\.firebaserc$|firestore\.indexes"; then
    ONE_WAY=1
    REASON="cloud service config (Firebase)"
fi

# CI/CD pipelines
if echo "$DIR" | grep -qE "\.(github|gitlab|circleci)" || echo "$FILENAME_LOWER" | grep -qE "^(jenkinsfile|\.travis\.yml|cloudbuild)"; then
    ONE_WAY=1
    REASON="CI/CD pipeline"
fi

if [ "$ONE_WAY" = "1" ]; then
    cat >&2 <<HOOK_MSG
ONE_WAY_DOOR: You tried to create $FILENAME ($REASON). This write has been blocked because it is a one-way door -- a decision that becomes hard to reverse once other code, data, or users depend on it.

REQUIRED ACTION: You MUST use the AskUserQuestion tool before retrying this write. Present the user with:
1. What this file does and why it is a one-way door
2. At least 2 alternative approaches (if any exist) with their trade-offs
3. An option to proceed as planned

Frame the question around the specific architectural decision, not just "should I create this file?" The user needs to understand what they are committing to.

After the user responds, proceed according to their choice.
HOOK_MSG
    exit 2
fi

exit 0
```

**How it works:**

1. The hook intercepts every `Write` tool call (new file creation)
2. It extracts the file path and checks it against known one-way-door patterns
3. If the file matches, the hook exits with code 2 (block) and sends a message to stderr
4. Claude receives the block message and must use `AskUserQuestion` to discuss the decision with the user
5. Two-way door files pass through silently (exit 0)

**Exit codes:**
- `0` — Allow (two-way door, proceed normally)
- `2` — Block (one-way door, requires discussion)

## The three questions

Before committing to any one-way door, ask:

1. **What am I committing to?** — What does this decision constrain? What becomes harder to change?
2. **What are the alternatives?** — Is there a simpler approach? A more reversible one?
3. **What's the migration path?** — If this turns out to be wrong, how do we change course?

If you can't answer these questions clearly, you're not ready to walk through the door.
