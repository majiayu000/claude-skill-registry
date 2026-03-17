---
name: fly-deploy
description: Complete Fly.io deployment management - deploy, scale, logs, secrets, database, and more
---

# Fly Deployment Manager

Comprehensive Fly.io deployment management through conversation.

## Core Principle

**Deployments should be simple and observable.**

Guide users through Fly.io operations with clear feedback, helpful context, and actionable next steps. Abstract away complexity while maintaining full control.

## Usage

```
/fly-deploy                      # Show deployment status
/fly-deploy status               # Detailed app and database status
/fly-deploy deploy               # Deploy the app
/fly-deploy logs                 # Stream recent logs
/fly-deploy secrets              # Manage environment secrets
/fly-deploy scale                # Scale machines and resources
/fly-deploy db                   # Database management
/fly-deploy ssh                  # SSH into a machine
/fly-deploy health               # Check health status
/fly-deploy restart              # Restart all machines
/fly-deploy destroy              # Destroy app (with confirmation)
```

## Commands

### /fly-deploy (default: status)

Shows current deployment status:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JFL PLATFORM - FLY.IO STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

App: jfl-platform
Region: sjc (San Jose)
URL: https://jfl-platform.fly.dev

MACHINES
  ✓ 78d40e1a - running (sjc)
  ✓ 90e3f7a4 - running (sjc)

DATABASE
  ✓ jfl-platform-db - running
  Postgres 15
  Primary: sjc

HEALTH
  ✓ All checks passing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/fly-deploy deploy    Deploy latest changes
/fly-deploy logs      View recent logs
/fly-deploy ssh       SSH into machine
```

**Implementation:**
```bash
flyctl status --json
flyctl info --json
flyctl machines list --json
```

### /fly-deploy deploy

Deploys the application:

**Steps:**
1. Check if there are uncommitted changes (warn if so)
2. Show what will be deployed (git commit hash/message)
3. Run deployment
4. Stream build/deploy logs
5. Show final status with URL
6. Suggest next action (view logs, test URL, etc.)

**Implementation:**
```bash
# Check for uncommitted changes
git status --porcelain

# Get current commit
git log -1 --oneline

# Deploy
flyctl deploy

# Check health after deploy
flyctl status --json
```

**Example output:**
```
Deploying jfl-platform...

Commit: a4a4dfd "auto: session save"
Branch: main

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Building...
✓ Docker build complete (2m 15s)

Deploying...
✓ Machines updated (45s)

Health checks...
✓ All checks passing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEPLOYED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

https://jfl-platform.fly.dev

Want me to:
- Open the URL in your browser?
- Stream logs?
- Check health?
```

### /fly-deploy logs [--follow] [--machine=ID]

Shows recent application logs:

**Options:**
- `--follow` / `-f` - Stream logs in real-time
- `--machine=ID` - Logs from specific machine
- `--lines=N` - Number of recent lines (default: 100)

**Implementation:**
```bash
# Recent logs
flyctl logs --lines 100

# Follow logs
flyctl logs --follow

# Specific machine
flyctl logs --machine 78d40e1a
```

**Example output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOGS - jfl-platform
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2026-01-19T18:45:23Z [info] ✓ Ready in 1204ms
2026-01-19T18:45:45Z [info] GET /api/auth/session 200 in 45ms
2026-01-19T18:46:12Z [info] POST /api/projects 201 in 123ms
2026-01-19T18:46:15Z [error] Database connection timeout

Last 4 lines. Use /fly-deploy logs --follow to stream.
```

### /fly-deploy secrets

Manage environment secrets:

**Subcommands:**
- `list` - Show all secret names (not values)
- `set <KEY>=<VALUE>` - Set/update a secret
- `unset <KEY>` - Remove a secret
- `sync` - Sync from local .env file

**Implementation:**
```bash
# List secrets
flyctl secrets list

# Set secret
flyctl secrets set KEY="value"

# Unset secret
flyctl secrets unset KEY

# Bulk set from .env (with confirmation)
flyctl secrets import < .env
```

**Example output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECRETS - jfl-platform
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH_SECRET                     Set 2d ago
DATABASE_URL                    Set 5d ago (from Fly Postgres)
GITHUB_CLIENT_ID                Set 5d ago
GITHUB_CLIENT_SECRET            Set 5d ago
NODE_ENV                        Set 5d ago

5 secrets total

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/fly-deploy secrets set KEY=value    Add/update secret
/fly-deploy secrets sync             Sync from .env
```

**For sync command, confirm with user:**
```
This will sync all secrets from your local .env file:

Will set/update:
  - AUTH_SECRET
  - GITHUB_CLIENT_ID
  - GITHUB_CLIENT_SECRET
  - STRIPE_SECRET_KEY

Continue? (yes/no)
```

### /fly-deploy scale

Scale machines and resources:

**Options:**
- `machines <count>` - Scale to N machines
- `memory <size>` - Change memory (256mb, 512mb, 1gb, 2gb)
- `cpu <count>` - Change CPU count (1, 2, 4, 8)
- `regions <list>` - Add/remove regions

**Implementation:**
```bash
# Scale machines
flyctl scale count 3

# Scale memory
flyctl scale memory 1gb

# Scale CPU
flyctl scale cpu 2

# Scale to regions
flyctl regions add lax iad
```

**Example output:**
```
Current scale:
  Machines: 2
  Memory: 256mb
  CPU: 1 shared
  Regions: sjc

What would you like to change?
1. Scale to 3 machines (faster, costs ~$15/mo more)
2. Increase memory to 512mb (better performance)
3. Add regions (lax, iad - lower latency)
4. Custom configuration
```

### /fly-deploy db

Database management:

**Subcommands:**
- `status` - Database status and connection info
- `connect` - Open psql connection
- `migrate` - Run Prisma migrations
- `backup` - Create manual backup
- `restore <snapshot>` - Restore from backup

**Implementation:**
```bash
# Database status
flyctl postgres db show jfl-platform-db

# Connect via psql
flyctl postgres connect -a jfl-platform-db

# List backups
flyctl volumes list -a jfl-platform-db
```

**For migrations, use the app context:**
```bash
# SSH into app machine and run migrations
flyctl ssh console -a jfl-platform -C "npx prisma migrate deploy"
```

**Example output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATABASE - jfl-platform-db
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type: Postgres 15
Region: sjc (primary)
Storage: 10GB (2.3GB used)

CONNECTION
  Internal: jfl-platform-db.flycast
  Port: 5432

BACKUPS
  Last backup: 2h ago (automatic)
  Retention: 7 days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/fly-deploy db connect     Open psql console
/fly-deploy db migrate     Run Prisma migrations
```

### /fly-deploy ssh [machine-id]

SSH into a machine:

**Options:**
- No args - Pick from list of running machines
- `machine-id` - Connect to specific machine

**Implementation:**
```bash
# Interactive select
flyctl ssh console

# Specific machine
flyctl ssh console --machine 78d40e1a

# Run command
flyctl ssh console -C "ls -la"
```

**Example:**
```
Available machines:
1. 78d40e1a (sjc) - primary
2. 90e3f7a4 (sjc) - secondary

Which machine? (1-2, or 'all' to run command on all)

> 1

Connecting to 78d40e1a...

You're now in the machine. Type 'exit' to disconnect.

Common commands:
  ls /app              # App directory
  cat /app/package.json
  ps aux               # Running processes
  df -h                # Disk usage
```

### /fly-deploy health

Check application health:

**Checks:**
- HTTP health endpoint
- All machines responsive
- Database connectivity
- Recent errors in logs

**Implementation:**
```bash
# Machine status
flyctl status --json

# Check health endpoint
curl https://jfl-platform.fly.dev/api/health

# Recent errors
flyctl logs --lines 100 | grep -i error
```

**Example output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HEALTH CHECK - jfl-platform
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ HTTP health endpoint    200 OK (45ms)
✓ All machines running    2/2 healthy
✓ Database connected      Latency 12ms
⚠ Recent errors          3 errors in last hour

Recent issues:
  - 3x "Database connection timeout" at /api/projects

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Want me to:
- Show full error logs?
- Check database connection pool settings?
```

### /fly-deploy restart

Restart all machines:

**Behavior:**
1. Show current machine status
2. Confirm restart action
3. Rolling restart (one at a time for zero downtime)
4. Show new machine status

**Implementation:**
```bash
# Rolling restart
flyctl machines restart --force

# Or restart specific machine
flyctl machines restart 78d40e1a
```

**Example:**
```
This will restart all machines in a rolling fashion.

Current uptime: 3d 14h 22m

Continue? (yes/no)

> yes

Restarting machines...
  ✓ 78d40e1a restarted (15s)
  ✓ 90e3f7a4 restarted (12s)

All machines restarted. Health checks passing.
```

### /fly-deploy destroy

Destroy the application and database:

**DANGER ZONE**

**Behavior:**
1. Explain what will be destroyed
2. Require explicit confirmation with app name
3. Optionally backup database first
4. Destroy resources
5. Update local files (remove fly.toml reference)

**Implementation:**
```bash
# List resources
flyctl apps list
flyctl postgres list

# Destroy app (requires confirmation)
flyctl apps destroy jfl-platform

# Destroy database (requires confirmation)
flyctl postgres destroy jfl-platform-db
```

**Example:**
```
⚠️  DANGER ZONE

This will permanently destroy:
  - App: jfl-platform (2 machines)
  - Database: jfl-platform-db (Postgres 15, 10GB)
  - All data (Users, Projects, Deployments, etc.)

This cannot be undone.

Create a database backup first? (yes/no)

> yes

Creating backup... ✓

To confirm, type the app name: jfl-platform

> jfl-platform

Destroying resources...
  ✓ App destroyed
  ✓ Database destroyed

Deployment removed from Fly.io.
```

## Error Handling

### Not Authenticated

If `flyctl auth token` fails:

```
You're not authenticated with Fly.io.

Run this to login:
  flyctl auth login

This will open your browser to authenticate.
```

### App Not Found

If app doesn't exist on Fly:

```
No Fly.io app found.

Options:
1. Deploy new app: /fly-deploy init
2. Link existing app: flyctl config show [app-name]
```

### Build Failures

If deployment build fails, parse logs and suggest fixes:

```
Build failed: Docker error

Error: "npm ERR! missing: typescript@^5.0.0"

Suggested fix:
  npm install --save-dev typescript@^5.0.0

Want me to:
- Install the missing dependency?
- Show full build logs?
- Cancel deployment?
```

## Configuration Detection

### Auto-detect from fly.toml

```toml
app = 'jfl-platform'
primary_region = 'sjc'
```

**Read this to:**
- Get app name
- Get primary region
- Get configuration

### Auto-detect Database

```bash
# Check for attached Postgres
flyctl postgres list
flyctl postgres db show -a jfl-platform-db
```

### Multi-App Detection

If multiple fly.toml files exist (monorepo):

```
Multiple Fly apps detected:

1. jfl-platform (./platform)
2. jfl-api (./api)
3. jfl-worker (./worker)

Which app? (1-3, or 'all')
```

## Dependencies

- `flyctl` CLI installed and authenticated
- `fly.toml` in project directory
- Docker (for local builds)
- `git` (for commit detection)

## Tips and Best Practices

### Always show context

Don't just execute commands. Show what's happening:

```
Deploying changes from commit a4a4dfd...
```

### Suggest next actions

After any operation, guide the user:

```
Deployed successfully!

Next steps:
- Test the deployment: https://jfl-platform.fly.dev
- Watch logs: /fly-deploy logs --follow
- Check health: /fly-deploy health
```

### Warn on destructive actions

```
⚠️  This will restart all machines (brief downtime possible)
```

### Parse errors helpfully

If something fails, explain what went wrong and how to fix it:

```
Deployment failed: Health check timeout

The app deployed but isn't responding to health checks.

Common causes:
1. Database connection issues (check DATABASE_URL secret)
2. Port mismatch (app listening on wrong port)
3. Startup errors (check logs)

Want me to:
- Check the logs?
- Verify database connection?
- Rollback to previous version?
```

### Show costs when scaling

```
Scaling to 3 machines:
  Current cost: ~$5/mo
  New cost: ~$15/mo (+$10/mo)

Continue? (yes/no)
```

## Integration with Other Skills

### Works with /hud

Add deployment status to HUD:

```
Deployment: ✓ Production running (2 machines)
Last deploy: 2h ago
```

### Works with project specs

Check `product/platform/fly.toml` for configuration.

### Works with git

Detect uncommitted changes before deploy.
Show commit info in deploy logs.

## Quick Reference

```
/fly-deploy               # Status dashboard
/fly-deploy deploy        # Deploy latest changes
/fly-deploy logs -f       # Stream logs
/fly-deploy secrets list  # List secrets
/fly-deploy scale         # Scale resources
/fly-deploy db status     # Database info
/fly-deploy ssh           # SSH into machine
/fly-deploy health        # Health check
/fly-deploy restart       # Restart machines
```

---

**Remember:** Keep it conversational. Guide users through operations with clear feedback and helpful suggestions. Make Fly.io deployments feel simple and observable.
