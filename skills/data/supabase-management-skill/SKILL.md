---
name: supabase-management-skill
description: 'CRITICAL ENFORCEMENT: This skill prevents direct Supabase CLI operations.
  ALL database operations MUST go through the storage-based sync system using storage/scripts/.sh
  scripts.'
---

---
name: Supabase Management
description: Manage Supabase database using Orchestrator AI's storage-based sync system. Use when working with Supabase, database snapshots, migrations, agent exports, N8N workflow exports, backups, or storage scripts. CRITICAL: Prevents direct Supabase operations - all operations MUST use storage/scripts/*.sh
allowed-tools: SlashCommand, Bash, Read, Write, Edit, Glob, Grep
---

# Supabase Management Skill

**CRITICAL ENFORCEMENT**: This skill prevents direct Supabase CLI operations. ALL database operations MUST go through the storage-based sync system using `storage/scripts/*.sh` scripts.

## When to Use This Skill

Use this skill when the user wants to:
- **Export or apply database snapshots** (for intern distribution)
- **Manage agents** (export/import individual or all agents)
- **Manage N8N workflows** (export/import individual or all workflows)
- **Create or apply migrations** (intern proposal workflow)
- **Backup or restore databases** (daily backup system)
- **Sync agents/workflows** between storage and database

**DO NOT use this skill when:**
- User wants to use Supabase CLI directly (REDIRECT to storage scripts)
- User wants to bypass the storage system (BLOCK and explain why)
- Task is unrelated to database management

## Orchestrator AI Storage System Architecture

### Core Principle: Storage-Based Sync
**NEVER use Supabase CLI directly.** All operations must use `storage/scripts/*.sh` to maintain synchronization across team members and production.

### Directory Structure
```
storage/
├── backups/                          # Daily compressed backups
│   ├── golfergeek_supabase_backup_*.sql.gz
│   └── golfergeek_n8n_backup_*.sql.gz
├── snapshots/
│   ├── agents/                       # Individual agent JSON files (SOURCE OF TRUTH)
│   │   ├── demo_supabase_agent.json
│   │   └── ...
│   ├── n8n/                          # Individual N8N workflow JSON files (SOURCE OF TRUTH)
│   │   ├── helper-llm-task.json
│   │   ├── marketing-swarm-flexible-llm.json
│   │   └── ...
│   ├── latest/                       # Latest full snapshot (symlink/copy)
│   │   ├── schema.sql
│   │   ├── seed.sql
│   │   └── metadata.json
│   └── <timestamp>/                  # Timestamped snapshots
│       ├── schema.sql
│       ├── seed.sql
│       └── metadata.json
├── migrations/
│   ├── proposed/                     # Intern-proposed migrations
│   └── applied/                      # Approved migrations
└── scripts/                          # ALL management scripts (USE THESE ONLY)
    ├── export-snapshot.sh
    ├── apply-snapshot.sh
    ├── export-agent.sh
    ├── import-agent.sh
    ├── export-all-agents.sh
    ├── import-all-agents.sh
    ├── sync-agents-to-db.sh
    ├── export-n8n-workflow.sh
    ├── import-n8n-workflow.sh
    ├── export-all-n8n-workflows.sh
    ├── import-all-n8n-workflows.sh
    ├── sync-n8n-to-db.sh
    ├── backup-all-daily.sh
    ├── backup-supabase-daily.sh
    ├── backup-n8n-daily.sh
    ├── restore-from-backup.sh
    └── apply-proposed-migration.sh
```

### Database Schemas
Orchestrator AI uses **4 schemas**:
- `public` - Main application schema (agents, providers, models, conversations, tasks, etc.)
- `n8n` - N8N workflow storage schema
- `company` - Organization/tenant data
- `observability` - Metrics and monitoring data

### Database Connection Details
- **Host**: `127.0.0.1` (or `localhost`)
- **Port**: `7012` (Supabase), `7013` (N8N)
- **User**: `postgres`
- **Database**: `postgres`
- **Container**: `supabase_db_api-dev`
- **Password**: `postgres` (via `PGPASSWORD` environment variable)

## Core Operations

### 1. Database Snapshots (Full Schema + Seed Data)

**Purpose**: Export/apply complete database state for intern distribution

**Export Snapshot:**
```bash
npm run db:export-snapshot
# OR
bash storage/scripts/export-snapshot.sh
```

**What gets exported:**
- All 4 schemas: `public`, `n8n`, `company`, `observability`
- Schema structure only (no data except seed data)
- Seed data: `public.agents`, `public.providers`, `public.models`
- Timestamped directory: `storage/snapshots/<timestamp>/`
- Latest symlink: `storage/snapshots/latest/`

**Apply Snapshot:**
```bash
npm run db:apply-snapshot
# OR
bash storage/scripts/apply-snapshot.sh storage/snapshots/latest/
```

**WARNING**: Applying a snapshot will DELETE all data in the 4 schemas and replace with snapshot data.

### 2. Agent Management

**Source of Truth**: `storage/snapshots/agents/*.json` (individual JSON files)

**Export Single Agent:**
```bash
npm run db:export-agent <agent-name>
# Example: npm run db:export-agent demo_supabase_agent
```

**Import Single Agent:**
```bash
npm run db:import-agent <path-to-json>
# Example: npm run db:import-agent storage/snapshots/agents/demo_supabase_agent.json
```

**Export ALL Agents:**
```bash
npm run db:export-all-agents
# Exports all agents to storage/snapshots/agents/*.json
```

**Import ALL Agents:**
```bash
npm run db:import-all-agents
# Imports all agents from storage/snapshots/agents/
```

**Sync Agents (Delete Missing, Upsert Existing):**
```bash
npm run db:sync-agents
# OR
bash storage/scripts/sync-agents-to-db.sh
```

### 3. N8N Workflow Management

**Source of Truth**: `storage/snapshots/n8n/*.json` (individual JSON files)

**Export Single Workflow:**
```bash
npm run db:export-n8n "<workflow-name>"
# Example: npm run db:export-n8n "Helper: LLM Task"
```

**Import Single Workflow:**
```bash
npm run db:import-n8n <path-to-json>
# Example: npm run db:import-n8n storage/snapshots/n8n/helper-llm-task.json
```

**Export ALL Workflows:**
```bash
npm run db:export-all-n8n
# Exports all workflows to storage/snapshots/n8n/*.json
```

**Import ALL Workflows:**
```bash
npm run db:import-all-n8n
# Imports all workflows from storage/snapshots/n8n/
```

**Sync Workflows (Delete Missing, Upsert Existing):**
```bash
npm run db:sync-n8n
# OR
bash storage/scripts/sync-n8n-to-db.sh
```

### 4. Migrations (Intern Proposal Workflow)

**Proposed Migrations**: `storage/migrations/proposed/`
**Applied Migrations**: `storage/migrations/applied/`

**For Interns (Proposing Changes):**
1. Create migration file: `storage/migrations/proposed/YYYYMMDD-HHMM-description.sql`
2. Write SQL migration
3. Share with lead developer for review

**For Lead Developer (Reviewing & Applying):**
1. Review proposed migration: `cat storage/migrations/proposed/<file>.sql`
2. Test locally (optional)
3. If approved, move to applied: `mv storage/migrations/proposed/<file>.sql storage/migrations/applied/`
4. Apply migration: `bash storage/scripts/apply-proposed-migration.sh storage/migrations/applied/<file>.sql`
5. Export new snapshot: `npm run db:export-snapshot`
6. Share updated snapshot with team

### 5. Backups (Daily Backup System)

**Backup Both Databases:**
```bash
./storage/scripts/backup-all-daily.sh
```

**Backup Individually:**
```bash
./storage/scripts/backup-supabase-daily.sh
./storage/scripts/backup-n8n-daily.sh
```

**Restore from Backup:**
```bash
./storage/scripts/restore-from-backup.sh supabase <backup-file.sql.gz>
./storage/scripts/restore-from-backup.sh n8n <backup-file.sql.gz>
```

**Backup Features:**
- Timestamped backups: `golfergeek_supabase_backup_YYYYMMDD_HHMMSS.sql.gz`
- Automatic compression (gzip)
- Automatic cleanup (keeps last 7 days)
- Safe restoration (confirmation prompts)

## Enforcement: Preventing Direct Supabase Operations

**CRITICAL**: If user attempts direct Supabase CLI operations, you MUST:

1. **STOP** the operation immediately
2. **EXPLAIN** why direct operations are forbidden:
   - Breaks storage-based sync system
   - Causes database synchronization issues across team
   - Bypasses source of truth (storage/snapshots/)
   - Can cause production database drift
3. **REDIRECT** to appropriate storage script:
   - Direct schema changes → Use migration proposal workflow
   - Direct data changes → Use snapshot export/apply
   - Direct agent changes → Use agent export/import scripts
   - Direct N8N changes → Use N8N export/import scripts

**Example Error Response:**
```
❌ ERROR: Direct Supabase operations are forbidden in Orchestrator AI.

All database operations MUST use the storage-based sync system to maintain
synchronization across team members and production.

Instead of: supabase db reset
Use: npm run db:apply-snapshot

Instead of: supabase db push
Use: storage/migrations/proposed/ workflow

See storage/scripts/README.md for all available operations.
```

## Common Workflows

### Lead Developer: After Making Database Changes
```bash
# 1. Export full snapshot
npm run db:export-snapshot

# 2. Export all agents
npm run db:export-all-agents

# 3. Export all N8N workflows
npm run db:export-all-n8n

# 4. Share storage/snapshots/ directory with interns
```

### Intern: Getting Latest Database State
```bash
# 1. Receive storage/snapshots/ directory from lead
# 2. Apply full snapshot
npm run db:apply-snapshot

# 3. Verify with: npm run dev
```

### Intern: Updating Specific Agent
```bash
# 1. Receive single agent JSON file
# 2. Import agent
npm run db:import-agent <file>
```

### Intern: Updating Specific N8N Workflow
```bash
# 1. Receive single workflow JSON file
# 2. Import workflow
npm run db:import-n8n <file>
```

### Daily Operations: Manual Backup Before Major Changes
```bash
# Create backup
./storage/scripts/backup-all-daily.sh

# Emergency restore
LATEST=$(ls -t storage/backups/golfergeek_supabase_backup_*.sql.gz | head -1)
./storage/scripts/restore-from-backup.sh supabase "$LATEST"
```

## Related Documentation

- **Storage Scripts README**: [storage/scripts/README.md](../../storage/scripts/README.md)
- **Backup Documentation**: [storage/scripts/README-backups.md](../../storage/scripts/README-backups.md)
- **Migration Workflow**: [storage/migrations/README.md](../../storage/migrations/README.md)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

