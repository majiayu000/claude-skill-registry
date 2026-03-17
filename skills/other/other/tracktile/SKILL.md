---
name: Tracktile
description: Tracktile
category: general
---


---
name: tracktile
description: Work in the Tracktile monorepo - Android builds (EAS), MR workflow (glab), testing, and development commands for the food & beverage manufacturing platform.
---

# Tracktile Monorepo Development

Work effectively in the Tracktile monorepo - an operating system for food & beverage manufacturers.

## Repository

```bash
# Clone (first time)
git clone git@gitlab.com:sharokenstudio/tracktile/tracktile.git ~/tracktile

# Or with wtm (worktree manager)
wtm init git@gitlab.com:sharokenstudio/tracktile/tracktile.git ~/tracktile
```

**Remote:** `git@gitlab.com:sharokenstudio/tracktile/tracktile.git`
**Default Branch:** `prerelease`
**CI:** GitLab CI/CD

## Monorepo Structure

```
tracktile/
├── apps/
│   ├── backend/           # Backend API
│   ├── frontend/          # React Native App (Web and Mobile)
│   ├── handbook/          # Internal Employee documentation (Docusaurus)
│   └── ...
├── packages/
│   ├── common/            # Shared types, utils
│   ├── ui/                # Shared UI components
│   └── ...
├── tools/                 # Build/dev tooling
├── pnpm-workspace.yaml
└── package.json
```

## Key Technologies

- **Backend:** Koa, Typebox, Knex, Objection.js
- **Frontend:** React Native, Unistyles V3, Signals
- **Mobile:** React Native, Expo
- **Build:** pnpm workspaces, Turborepo
- **Testing:** Jest, cypress (e2e)

## Development Workflow

### Setup
```bash
cd ~/tracktile
```

### Create Worktree for Task
```bash
# Using wtm (preferred)
wtm create fix/issue-name --from prerelease

### Before Committing - MANDATORY
```bash
# Run from repo root, IN SEQUENCE (not parallel)
pnpm typecheck    # Must pass
pnpm lint         # Must pass
pnpm test         # Must pass (or pnpm test:affected)
```

**⚠️ NO EXCEPTIONS. All three must pass before commit/MR.**

### Commit & Push
```bash
git add .
git commit -m "fix(backend): descriptive message"
git push -u origin fix/issue-name
```

## Handbook (Documentation)

The handbook (`apps/handbook`) is the source of truth for Tracktile's domain, architecture, and concepts.

**Local:** `apps/handbook/docs/`
**Structure:**
- `company/` — Culture, overview
- `engineering/platform/` — Apps, services, architecture
- `engineering/ops/` — Logging, monitoring, access
- `topics/` — Domain concepts (EDI, traceability, etc.)

**When working on Tracktile:**
1. Consult handbook for domain context
2. Update docs in same MR as code changes
3. Fix outdated info when found

## Key Directories by Task Type

### Backend Bugs/Features
- `apps/backend/src/services/` — Modular Services
- `apps/backend/src/shared/` — Shared backend code

### Frontend Bugs/Features
- `apps/frontend/src/components/` — UI components
- `apps/frontend/src/pages/` — Page components
- `apps/frontend/src/stores/` — Zustand stores

### Database/Migrations
- `apps/backend/src/migrations/` — Knex migrations

### Trace/Search/Inventory/Actions (Common Bug Area)
- `apps/backend/src/services/flow/` — Flow / Inventory Service
- `apps/backend/src/services/entity/` — Entity services

## MR Process

### Opening an MR (ALWAYS use glab)

```bash
# From your feature branch, after pushing
glab mr create --fill --target-branch prerelease

# Or with explicit options
glab mr create \
  --title "fix(backend): descriptive title" \
  --description "$(cat .gitlab/merge_request_templates/Default.md)" \
  --target-branch prerelease \
  --remove-source-branch
```

### MR Template (MANDATORY)

Always use the repo's MR template at `.gitlab/merge_request_templates/Default.md`.
Fill in ALL sections:

```markdown
## Notes
<!-- What changed and why -->

## Asana Ticket
<!-- CLICKABLE LINK - do NOT use "fixes:" or "closes:" prefix -->
[Asana #123456789](https://app.asana.com/0/0/123456789)

## Images & Looms
<!-- Screenshots or recordings if UI change -->

## Test Cases
<!-- Link to test cases if applicable -->

## Checklists
- [ ] Tested on Web
- [ ] Tested on Android (if mobile)
- [ ] Feature flagged (if new feature)
- [ ] Translations added (if user-facing text)
- [ ] Tests added/updated
```

### MR Commands (glab)

```bash
# List open MRs
glab mr list

# View MR details
glab mr view <mr-number>

# Check MR status/CI
glab mr view <mr-number> --comments

# Merge when ready
glab mr merge <mr-number>
```

**⚠️ NEVER use "fixes:" or "closes:" before Asana links** — triggers unwanted GitLab automations.

## Environment

- **Pre-Release:** Testing/staging environment
- **Production:** Live customer environment
- **Local:** Docker Compose for DB/Redis

## Common Commands

```bash
# Start backend locally
pnpm --filter backend dev

# Start frontend locally
pnpm --filter frontend dev

# Run specific test file
pnpm --filter backend test -- path/to/test.spec.ts

# Generate migration
pnpm --filter backend migration:generate MigrationName

# Check what's affected by changes
pnpm affected
```

## Mobile Builds (APK/AAB)

Build Android packages locally using EAS (Expo Application Services).

### Build Profiles (in `apps/frontend/eas.json`)

| Profile | Output | Purpose |
|---------|--------|---------|
| `local` | APK | Expo development build |
| `prerelease` | APK | Pre-release environment testing |
| `production-preview` | APK | Production environment testing |
| `production` | AAB | Play Store submission |

### Version Management (IMPORTANT)

EAS stores version codes remotely (`cli.appVersionSource: "remote"` in eas.json).

**Only `production` profile has `autoIncrement: true`.** For all other profiles, you MUST manually increment the version before building, or the build will reuse the same version code (causing Play Store/device conflicts).

```bash
cd apps/frontend

# 1. Check current version
eas build:version:get -p android

# 2. Increment version (for non-production profiles)
# Get current, add 1, then set
CURRENT=$(eas build:version:get -p android 2>/dev/null | grep -oP 'versionCode: \K\d+')
NEXT=$((CURRENT + 1))
eas build:version:set -p android --build-version $NEXT

# Or interactively (will prompt for version)
eas build:version:set -p android
```

| Profile | Auto-Increment? | Action Required |
|---------|-----------------|-----------------|
| `production` | ✅ Yes | None - auto-increments |
| `production-preview` | ❌ No | Run `eas build:version:set` first |
| `prerelease` | ❌ No | Run `eas build:version:set` first |
| `local` | ❌ No | Run `eas build:version:set` first |

### Building APKs/AABs

```bash
cd apps/frontend

# STEP 1: Increment version (skip for production profile)
eas build:version:set -p android

# STEP 2: Build

# Build APK for pre-release testing
eas build --platform android --local --profile=prerelease

# Build APK for production testing
eas build --platform android --local --profile=production-preview

# Build AAB for Play Store (auto-increments, no version:set needed)
eas build --platform android --local --profile=production

# Build development APK
eas build --platform android --local --profile=local
```

### Build Output

Local builds output to the current directory. The file will be named like:
- APK: `build-*.apk`
- AAB: `build-*.aab`

### Making Builds Available

After building, share the APK/AAB:
1. Upload to a shared location (Google Drive, S3, etc.)
2. Or use `eas submit` for Play Store submissions
3. For internal testing, share APK directly via Slack

### Prerequisites

- EAS CLI installed: `npm install -g eas-cli`
- Android SDK/NDK for local builds
- Logged into EAS: `eas login`

## Troubleshooting

### pnpm install fails
```bash
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### TypeORM entity issues
Check that entity is registered in the module's `TypeOrmModule.forFeature([...])`

### Test database issues
```bash
docker compose down -v
docker compose up -d
```
