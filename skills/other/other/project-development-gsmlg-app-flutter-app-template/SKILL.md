---
name: project-development
description: Development workflow guide for choosing the right skill based on your task - screens, widgets, BLoC, APIs, forms, storage, and more (project)
---

# Project Development Skill Guide

This skill guides you to the appropriate skill for your development task. Use this as a decision tree when starting new work on the project.

## When to Use

Trigger this skill when:
- Starting a new feature and unsure which skill applies
- Need guidance on the project's development workflow
- Creating a new project skill or updating existing skills
- User asks "how do I...", "which skill...", "where should I...", or "help me build..."
- User asks to "add a skill", "create a skill", "update skills", or "document a workflow"

## Quick Reference: Skill Selection

| Task | Skill | Command |
|------|-------|---------|
| Create a new screen/page | `/project-screen` | `mason make screen` |
| Create a reusable widget | `/project-widget` | `mason make widget` |
| Add state management | `/project-bloc` | `mason make simple_bloc` or `list_bloc` |
| Create a form with validation | `/project-form` | Manual setup |
| Integrate REST API | `/project-api` | `mason make api_client` |
| Add localized text | `/project-locale` | Edit ARB + `melos run gen-l10n` |
| Store data persistently | `/project-database` | Drift tables |
| Store secrets/tokens | `/project-secure-storage` | VaultRepository |
| Show user feedback | `/project-feedback` | Toasts, dialogs, snackbars |
| Create native plugin | `/project-plugin` | `mason make native_plugin` |
| Update app metadata | `/project-metadata` | Manual edits |
| Create/modify Mason brick | `/template-mason-brick` | Brick + test + workflow |
| **Add/update project skill** | `/project-development` | See "Creating New Project Skills" |

## Decision Tree: What Are You Building?

### 1. User Interface

```
Creating UI?
├── New page/route? → /project-screen
├── Reusable component? → /project-widget
├── Form with validation? → /project-form
└── Feedback (toast/dialog/snackbar)? → /project-feedback
```

### 2. Business Logic & State

```
Managing state?
├── Simple state (theme, settings)? → /project-bloc (simple_bloc)
├── List with CRUD? → /project-bloc (list_bloc)
└── Form state with validation? → /project-form
```

### 3. Data Layer

```
Working with data?
├── External REST API? → /project-api
├── Local persistent data? → /project-database
├── Sensitive data (tokens, keys)? → /project-secure-storage
└── User-facing text? → /project-locale
```

### 4. Platform Integration

```
Platform-specific code?
├── Native functionality? → /project-plugin
└── App identity (name, icons)? → /project-metadata
```

### 5. Project Tooling

```
Development tooling?
├── Code generation templates? → /template-mason-brick
└── Add/update project skills? → /project-development (this skill)
```

## Feature Development Workflow

When building a complete feature, follow this order:

### Step 1: Plan the Data Layer

1. **External API needed?** → `/project-api`
   - Create API client package with OpenAPI spec
   - Generate models and clients

2. **Local storage needed?** → `/project-database` or `/project-secure-storage`
   - Use `/project-database` for structured data (settings, cache, lists)
   - Use `/project-secure-storage` for secrets (tokens, API keys, credentials)

### Step 2: Create Business Logic

3. **State management** → `/project-bloc`
   - Create BLoC package for feature state
   - Use `simple_bloc` for basic state
   - Use `list_bloc` for list management

4. **Form handling** → `/project-form`
   - Create FormBloc for forms with validation

### Step 3: Build the UI

5. **Screen creation** → `/project-screen`
   - Create screen with routing conventions
   - Use `AppAdaptiveScaffold` for responsive layout

6. **Reusable widgets** → `/project-widget`
   - Extract shared components

7. **User feedback** → `/project-feedback`
   - Add toasts, dialogs, snackbars

### Step 4: Polish

8. **Localization** → `/project-locale`
   - Add all user-facing text to ARB files

9. **Testing** → Run `melos run test`

## Common Feature Patterns

### Authentication Feature

```
1. /project-api          → Auth API client (login, register, refresh)
2. /project-secure-storage → Token storage
3. /project-bloc         → AuthBloc (login state, session management)
4. /project-form         → LoginFormBloc, RegisterFormBloc
5. /project-screen       → LoginScreen, RegisterScreen
6. /project-feedback     → Error toasts, success messages
7. /project-locale       → Auth-related text
```

### Settings Feature

```
1. /project-database     → Settings storage (theme, preferences)
2. /project-bloc         → SettingsBloc (or use ThemeBloc)
3. /project-screen       → SettingsScreen, subpages
4. /project-locale       → Settings labels
```

### Data Listing Feature

```
1. /project-api          → Data API client
2. /project-database     → Optional caching
3. /project-bloc         → ListBloc (list_bloc template)
4. /project-screen       → List screen with detail navigation
5. /project-widget       → List item widget, empty state
6. /project-feedback     → Loading states, error handling
7. /project-locale       → List-related text
```

### Form Submission Feature

```
1. /project-api          → Submission endpoint
2. /project-form         → FormBloc with validation
3. /project-screen       → Form screen
4. /project-feedback     → Validation errors, success toast
5. /project-locale       → Form labels, errors
```

### Third-Party Integration (e.g., OpenAI, Stripe)

```
1. /project-api          → API client for third-party service
2. /project-secure-storage → API key storage (REQUIRED for secrets!)
3. /project-bloc         → Integration state management
4. /project-screen       → Settings screen for API key input
5. /project-feedback     → Integration status feedback
```

## Package Organization

```
Root Project
├── lib/                      # Main app (screens, router, providers)
├── app_api/                  # API clients (/project-api)
├── app_bloc/                 # BLoC packages (/project-bloc)
├── app_form/                 # Form modules (/project-form)
├── app_widget/               # Reusable widgets (/project-widget)
├── app_plugin/               # Native plugins (/project-plugin)
├── app_lib/                  # Core utilities
│   ├── database/             # /project-database
│   ├── locale/               # /project-locale
│   ├── secure_storage/       # /project-secure-storage
│   ├── theme/                # Theme management
│   ├── provider/             # App providers
│   └── logging/              # Logging utilities
├── bricks/                   # Mason templates (/template-mason-brick)
└── third_party/              # Modified third-party packages
```

## Storage Decision Guide

| Data Type | Solution | Skill |
|-----------|----------|-------|
| API tokens, passwords | Secure storage | `/project-secure-storage` |
| Third-party API keys | Secure storage | `/project-secure-storage` |
| Theme preference | SharedPreferences or DB | `/project-database` |
| User settings (complex) | Database | `/project-database` |
| Cached API responses | Database | `/project-database` |
| Offline data | Database | `/project-database` |
| Feature flags | SharedPreferences | (built-in) |

## Mason Brick Quick Reference

| Brick | Command | Purpose |
|-------|---------|---------|
| `screen` | `mason make screen --name Name` | Screen with routing |
| `widget` | `mason make widget --name Name` | Reusable widget |
| `simple_bloc` | `mason make simple_bloc --name=name -o app_bloc/name` | Basic BLoC |
| `list_bloc` | `mason make list_bloc --name=name -o app_bloc/name` | List BLoC |
| `repository` | `mason make repository --name=name -o app_lib/name` | Data repository |
| `api_client` | `mason make api_client --package_name=name -o app_api/name` | API client |
| `native_plugin` | `mason make native_plugin --name=name -o app_plugin` | Native plugin |

## Development Commands

```bash
# Initial setup
melos bootstrap && melos run prepare

# After code changes
melos run analyze          # Check for issues
melos run format           # Format code
melos run test             # Run all tests

# After ARB changes
melos run gen-l10n         # Generate localizations

# After model/database changes
melos run build-runner     # Generate code

# Run app
flutter run -d <device>
```

## Checklist: Before Committing

- [ ] All user-facing text localized (`/project-locale`)
- [ ] Sensitive data in secure storage (`/project-secure-storage`)
- [ ] Error handling with user feedback (`/project-feedback`)
- [ ] Tests written for new code
- [ ] `melos run analyze` passes
- [ ] `melos run format-check` passes

---

## Creating New Project Skills

When the project needs a new skill (e.g., new package type, new workflow, new integration pattern), follow this process.

### Step 1: Create Skill Directory

```bash
mkdir -p .claude/skills/project-<skill-name>
```

### Step 2: Create skill.md

Create `.claude/skills/project-<skill-name>/skill.md` with this structure:

```markdown
---
name: project-<skill-name>
description: Brief description of what this skill does (project)
---

# Flutter <Skill Name> Skill

Description of what this skill guides.

## When to Use

Trigger this skill when:
- Condition 1
- Condition 2
- User asks to "...", "...", or "..."

## [Main Content Sections]

- Package location and structure
- Step-by-step guide
- Code examples
- Best practices
- Common errors and solutions

## Quick Reference

Summary table or commands for easy lookup.
```

### Step 3: Update CLAUDE.md

Add the new skill to the Custom Skills list in `CLAUDE.md`:

```markdown
- `/project-<skill-name>` - Brief description
```

Keep the list alphabetized (except `/project-development` stays first).

### Step 4: Update This Skill (project-development)

Update this file to include the new skill:

1. **Quick Reference table** - Add row with task, skill, and command
2. **Decision Tree** - Add to appropriate category
3. **Common Feature Patterns** - Add if relevant to common workflows
4. **Package Organization** - Add if it introduces new package location

### Skill Naming Conventions

| Prefix | Use For |
|--------|---------|
| `project-` | Project-specific development workflows |
| `template-` | Mason brick and code generation |

### Skill Content Guidelines

1. **"When to Use" section is required** - Helps Claude trigger the skill appropriately
2. **Include concrete examples** - Code snippets, file structures, commands
3. **Reference existing packages** - Show where to find reference implementations
4. **Add troubleshooting** - Common errors and solutions
5. **Keep focused** - One skill per concern (don't combine unrelated topics)

---

## Updating This Skill (Self-Maintenance)

This skill (`/project-development`) should be updated when:

### When to Update

| Trigger | Action |
|---------|--------|
| New skill added | Add to Quick Reference, Decision Tree, relevant patterns |
| Skill removed | Remove all references |
| Skill renamed | Update all references |
| New feature pattern emerges | Add to Common Feature Patterns |
| New package location added | Update Package Organization |
| New Mason brick added | Add to Mason Brick Quick Reference |
| Workflow changes | Update Development Commands or Checklist |

### Update Checklist

When adding a new skill, update these sections:

- [ ] **Quick Reference: Skill Selection** - Add table row
- [ ] **Decision Tree** - Add to appropriate category (UI/State/Data/Platform/Tooling)
- [ ] **Common Feature Patterns** - Add to relevant patterns if applicable
- [ ] **Package Organization** - Add if new package location
- [ ] **Storage Decision Guide** - Add if storage-related
- [ ] **Mason Brick Quick Reference** - Add if includes Mason brick
- [ ] **CLAUDE.md** - Add to Custom Skills list

### Example: Adding a New Skill

If adding `/project-notifications` for push notifications:

1. Create `.claude/skills/project-notifications/skill.md`

2. Update Quick Reference table:
```markdown
| Push notifications | `/project-notifications` | Platform setup |
```

3. Update Decision Tree under Platform Integration:
```
Platform-specific code?
├── Native functionality? → /project-plugin
├── Push notifications? → /project-notifications  ← NEW
└── App identity (name, icons)? → /project-metadata
```

4. Add to Common Feature Patterns if needed:
```
### Push Notification Feature

1. /project-notifications → Platform setup (FCM, APNs)
2. /project-bloc         → NotificationBloc
3. /project-screen       → Notification settings screen
...
```

5. Update CLAUDE.md:
```markdown
- `/project-notifications` - Configure push notifications with FCM and APNs
```

---

## Getting Help

- **Unsure which skill?** → Ask: "Which skill should I use to [task]?"
- **Need more detail?** → Invoke the specific skill: `/project-<skill-name>`
- **Project conventions?** → Read `CLAUDE.md` at project root
- **Add new skill?** → Follow "Creating New Project Skills" section above
