---
name: project-indexer
description: Generate and use project index for quick codebase understanding in new Claude Code sessions. Scans project structure, extracts code symbols, and creates a navigable feature map.
metadata: {"version": "1.0.0", "tags": ["productivity", "codebase", "indexing", "navigation"]}
license: MIT
---

# Project Indexer

Generate a structured index of any codebase to help Claude Code quickly understand project structure in new sessions with minimal context usage.

## When to Use This Skill

Use this skill when:
- Starting work on a new or unfamiliar project
- Beginning a new Claude Code session and need project context
- User says: "explore the project", "understand the codebase", "project structure"
- User says: "了解项目", "探索项目", "项目结构", "索引项目"
- User says: "generate index", "create project map", "生成索引"
- User explicitly calls `/project-indexer`
- User wants to regenerate/update the index: "regenerate index", "更新索引"

## Core Principle

The index serves as a **navigation map**, not a code copy. It provides just enough information for Claude to:
1. Understand the project globally (type, tech stack, architecture)
2. Navigate to specific areas on demand (feature map, file index)
3. Know what functions/classes exist without reading all files (symbol index)

## Workflow

### Step 1: Check for Existing Index

First, check if `.claude-index/index.md` exists in the project root.

```
IF .claude-index/index.md exists:
    → Go to "Using Existing Index" section
ELSE:
    → Go to "First-Time Generation" section
```

---

## Using Existing Index

When `.claude-index/index.md` already exists:

1. **Read the index file**
   ```
   Read .claude-index/index.md
   ```

2. **Read CLAUDE.md if exists** (independent file for project conventions)
   ```
   Read CLAUDE.md (if present)
   ```

3. **Inform the user**
   ```
   "I've loaded the project index. I now have an overview of:
   - Project structure and tech stack
   - Feature areas and their locations
   - Key functions and classes

   Ready to help with development. What would you like to work on?"
   ```

4. **Use the index for navigation**
   - When user asks about a feature, use the Feature Map to locate relevant files
   - When user needs a specific function, use the File Index to find it
   - Read actual source files only when needed for detailed work

---

## First-Time Generation

When no index exists, guide the user through configuration and generate the index.

### Step 1: Gather Configuration

Ask the user these questions (provide defaults):

**Question 1: Directories to Exclude**
```
"Which directories should I exclude from indexing?

Default exclusions: node_modules, .git, dist, build, __pycache__, .venv, vendor, coverage, .next, .nuxt, .cache, target, bin, obj

Would you like to:
A) Use defaults
B) Add more exclusions
C) Customize the list"
```

**Question 2: Priority Directories**
```
"Which directories are most important to index in detail?

Options:
A) Let me auto-detect based on project structure (Recommended)
B) Specify priority directories (e.g., src/, lib/, core/)
C) Index everything equally"
```

**Question 3: Tech Stack (Optional)**
```
"I'll auto-detect the tech stack, but you can specify if needed:
- Press Enter to auto-detect
- Or tell me: e.g., 'Next.js + FastAPI' or 'Vue + Django'"
```

### Step 2: Scan and Analyze Project

Perform these analysis steps:

1. **Traverse file structure** with exclusion rules
2. **Detect project type**: frontend / backend / fullstack / library / CLI / monorepo
3. **Identify primary languages** and their percentages
4. **Detect frameworks** (React, Vue, Next.js, Express, FastAPI, Django, etc.)
5. **Find entry points**: main.ts, index.js, app.py, main.go, etc.
6. **Group files by feature/domain**: auth/, api/, components/, utils/, etc.
7. **Extract exported symbols**: public classes, functions, constants with signatures
8. **Generate descriptions**: one-line AI-generated description for each file/module
9. **Analyze dependencies**: module-level dependency relationships

### Step 3: Apply Adaptive Sizing

Adjust detail level based on project size:

| Project Size | Files | Strategy |
|--------------|-------|----------|
| Small | <50 | Detailed index - include all files with full symbol extraction |
| Medium | 50-200 | Standard index - full coverage with concise descriptions |
| Large | 200+ | Focused index - prioritize core code, summarize peripheral areas |

For large projects:
- Focus detailed indexing on priority directories
- Provide summary-level coverage for other areas
- Group similar utility files together

### Step 4: Generate Index Files

Create two files in `.claude-index/`:

**1. config.md** - Stores configuration for future regeneration
```markdown
# Index Configuration

## Excluded Directories
- node_modules
- .git
- [other exclusions...]

## Priority Directories
- src/
- [other priorities...]

## Tech Stack
- Frontend: [detected/specified]
- Backend: [detected/specified]
- Language: [primary language]

## Index Settings
- Generated: [timestamp]
- Project Root: [path]
- Index Version: 1.0
```

**2. index.md** - Main index file (see format below)

### Step 5: Update CLAUDE.md

After generating the index files, update the project's `CLAUDE.md` to inform future Claude Code sessions about the index:

**If `CLAUDE.md` exists:**
1. Read the existing content
2. Look for `## Project Index` section
3. If found: Replace that entire section with updated content
4. If not found: Append the section at the end of the file

**If `CLAUDE.md` does not exist:**
1. Create a new `CLAUDE.md` file with the Project Index section
2. Inform user they can add more project-specific instructions to this file

**Content to add/update:**
```markdown
## Project Index

This project has a pre-generated index for quick codebase understanding.

- **Location:** `.claude-index/index.md`
- **Last Updated:** {YYYY-MM-DD}
- **Contents:** Project overview, feature map, file index, exported symbols, module dependencies

**Usage:** Read `.claude-index/index.md` to quickly understand the project structure before making changes. The index provides a navigation map of the codebase without needing to explore every file.

**Regenerate:** Say "regenerate index" or "更新索引" to update the index after major changes.
```

### Step 6: Inform User

```
"Project index generated successfully!

Created:
- .claude-index/index.md (main index)
- .claude-index/config.md (configuration)
- Updated CLAUDE.md with index information

The index includes:
- Project overview and tech stack
- Feature map with [N] areas identified
- [N] files indexed with [N] exported symbols
- Module dependency graph

Future Claude Code sessions will automatically know about this index from CLAUDE.md.

I'm now ready to help with development. What would you like to work on?"
```

---

## Regeneration Flow

When user requests index regeneration ("regenerate index", "更新索引", "refresh index"):

1. **Read existing config**
   ```
   Read .claude-index/config.md to preserve:
   - Exclusion rules
   - Priority directories
   - Tech stack settings
   ```

2. **Confirm with user**
   ```
   "I'll regenerate the index using your existing configuration:
   - Excluded: [list]
   - Priority: [list]

   Proceed? (Or would you like to update the configuration?)"
   ```

3. **Re-scan and regenerate**
   - Follow Steps 2-6 from First-Time Generation
   - Preserve config.md, regenerate index.md
   - Update the timestamp in CLAUDE.md's Project Index section

---

## Index File Format

The `index.md` should follow this structure:

```markdown
# Project Index: {project-name}

> Auto-generated by project-indexer | Last updated: {YYYY-MM-DD}

## Project Overview

- **Type:** {Frontend | Backend | Fullstack | Library | CLI | Monorepo}
- **Languages:** {TypeScript (70%), Python (30%)}
- **Frameworks:** {Next.js, FastAPI}
- **Entry Points:** `{src/app/page.tsx}`, `{api/main.py}`

## Feature Map

### {Feature Name} (`{path}/`)
Entry: `{entry-file}`
- {One-line description of this feature area}
- **Key exports:**
  - `{functionName}({params}): {returnType}` - {description}
  - `{ClassName}` - {description}

### Authentication (`src/auth/`)
Entry: `src/auth/index.ts`
- User authentication, session management, and authorization
- **Key exports:**
  - `login(credentials: LoginInput): Promise<User>` - Authenticate user
  - `logout(): void` - Clear session and tokens
  - `useAuth(): AuthContext` - React hook for auth state
  - `withAuth(Component)` - HOC for protected routes

### API Layer (`src/api/`)
Entry: `src/api/client.ts`
- REST API client with error handling and request interceptors
- **Key exports:**
  - `apiClient` - Configured axios instance
  - `useQuery<T>(endpoint): SWRResponse<T>` - Data fetching hook
  - `useMutation<T>(endpoint): MutationResult<T>` - Data mutation hook

[Continue for each feature area...]

## Module Dependencies

- `auth` → `api` (uses apiClient for authentication requests)
- `pages` → `auth`, `components` (imports hooks and UI components)
- `api` → (standalone, no internal dependencies)
- `components` → `utils` (uses helper functions)

## File Index

### src/auth/
| File | Description |
|------|-------------|
| index.ts | Auth module entry point, re-exports public API |
| login.ts | Login logic, credential validation, token handling |
| session.ts | Session storage, refresh token management |
| hooks.ts | React hooks: useAuth, useUser, usePermissions |
| types.ts | TypeScript types for auth entities |

### src/api/
| File | Description |
|------|-------------|
| client.ts | Axios instance with interceptors and base config |
| endpoints.ts | API endpoint path constants |
| types.ts | Request/response type definitions |
| errors.ts | Custom error classes and error handling |

### src/components/
| File | Description |
|------|-------------|
| Button.tsx | Reusable button with variants (primary, secondary, ghost) |
| Modal.tsx | Dialog component with portal and focus trap |
| Form/index.tsx | Form wrapper with validation context |
| Form/Input.tsx | Text input with label and error display |
| Form/Select.tsx | Dropdown select component |

[Continue for each directory...]
```

---

## Language Support

### Priority Support (Full Symbol Extraction)
- **JavaScript / TypeScript** (.js, .jsx, .ts, .tsx, .mjs)
- **Python** (.py)

### Best-Effort Support
- Java (.java)
- Kotlin (.kt)
- Go (.go)
- Rust (.rs)
- C/C++ (.c, .cpp, .h, .hpp)
- C# (.cs)
- Ruby (.rb)
- PHP (.php)

### Fallback Behavior
For unsupported or unknown file types:
- Include in file listing
- Provide basic file info (size, type)
- Skip detailed symbol extraction
- Generate description based on filename and location

---

## Best Practices

1. **Keep index focused** - Don't try to document everything; focus on navigation value
2. **Update when structure changes** - Regenerate after major refactoring
3. **Use with CLAUDE.md** - Index provides structure; CLAUDE.md provides conventions
4. **Trust the map** - Use index to navigate, read actual files for implementation details

## Troubleshooting

**Index too large?**
- Add more directories to exclusions
- Reduce priority directories
- The adaptive sizing should handle this automatically

**Missing important files?**
- Check exclusion rules in config.md
- Ensure priority directories are set correctly
- Regenerate with updated configuration

**Outdated information?**
- Run regeneration: "regenerate index" or "更新索引"
- Index is a snapshot; regenerate after significant changes
