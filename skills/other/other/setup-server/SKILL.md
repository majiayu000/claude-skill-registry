---
name: setup-server
description: Bootstrap Pierre server with database, admin user, coaches, and test users for development and testing
user-invocable: true
---

# Setup Server Skill

**CLAUDE: When this skill is invoked with `/setup-server`, run the setup script:**
```bash
./bin/setup-and-start.sh --skip-fresh-start
```

For a completely fresh start (wipes database):
```bash
./bin/setup-and-start.sh
```

## Purpose
Bootstraps the Pierre MCP Server with all required components: database, admin user, coaches, and optionally test users. Essential for development, testing, and iOS Simulator testing.

## Usage
```bash
/setup-server
```

## Synthetic Provider vs Strava (IMPORTANT)

**CLAUDE: Default to synthetic provider. Ask if Strava is needed.**

### When to Use Synthetic Provider (DEFAULT)
- **Most development and testing** - no OAuth required
- **iOS Simulator testing** - works without external accounts
- **UI/UX development** - realistic data without API limits
- **CI/CD pipelines** - deterministic, reproducible tests

### When Strava is Needed
Only use Strava when:
- Testing OAuth flow specifically
- Validating real Strava API integration
- User explicitly requests Strava data
- Testing webhook sync features

### Set Provider in .envrc
```bash
# Default to synthetic (RECOMMENDED)
export PIERRE_DEFAULT_PROVIDER=synthetic

# Only if Strava OAuth testing needed
export PIERRE_DEFAULT_PROVIDER=strava
```

## Default Test Credentials

**CRITICAL: These are the default credentials from `.envrc`. Always use these for testing.**

### Admin User
```
Email:    admin@pierre.mcp
Password: adminpass123
```

### Regular Test User
```
Email:    user@example.com
Password: userpass123
```

### Environment Variables (from .envrc)
```bash
export ADMIN_EMAIL="admin@pierre.mcp"
export ADMIN_PASSWORD="adminpass123"
export OAUTH_DEFAULT_EMAIL="user@example.com"
export OAUTH_DEFAULT_PASSWORD="userpass123"
```

## Admin Token (REQUIRED FOR USER MANAGEMENT)

**CLAUDE: To create/approve users via admin API, you need an admin token.**

### Generate Admin Token
```bash
cargo run --bin pierre-cli -- token generate --service claude_test --expires-days 7
```

### Use Admin Token in API Calls
```bash
# Store the token
export ADMIN_TOKEN="<token-from-above-command>"

# Use in curl requests
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8081/admin/users
```

### Automatic Token Handling
The `complete-user-workflow.sh` script handles admin tokens automatically:
```bash
./scripts/complete-user-workflow.sh
```
This script:
1. Generates an admin token (or reuses existing)
2. Creates test user
3. Approves user with tenant
4. Saves all tokens to `.workflow_test_env`

### After Running Workflow Script
```bash
# Load saved tokens
source .workflow_test_env

# Now you can use $ADMIN_TOKEN and $JWT_TOKEN
echo "Admin: $ADMIN_TOKEN"
echo "User JWT: $JWT_TOKEN"
```

## Bootstrap Commands

### Quick Start (skip database wipe)
```bash
./bin/setup-and-start.sh --skip-fresh-start
```

### Fresh Start (wipes and recreates database)
```bash
./bin/setup-and-start.sh
```

### Fresh Start with Workflow Tests
```bash
./bin/setup-and-start.sh --run-tests
```

## What Setup Does

1. **Database Setup** - Creates/migrates SQLite database
2. **Admin User** - Creates admin@pierre.mcp with adminpass123
3. **Seed Coaches** - Loads AI coaching personas
4. **Start Server** - Starts on port 8081
5. **Health Check** - Waits for server to be healthy

**Note:** Basic setup only runs `seed-coaches`. For full test data, run additional seeders below.

## Data Seeders (IMPORTANT FOR TESTING)

**CLAUDE: Before testing features, run the appropriate seeders to populate test data.**

### Available Seeders

| Seeder | Command | What It Creates |
|--------|---------|-----------------|
| Coaches | `cargo run --bin seed-coaches` | 9 AI coaching personas (training, nutrition, recovery, mobility) |
| Demo Data | `cargo run --bin seed-demo-data` | Dashboard analytics, API keys, usage time-series data |
| Mobility | `cargo run --bin seed-mobility` | Stretching exercises, yoga poses, activity-muscle mappings |
| Social | `cargo run --bin seed-social` | Friend connections, shared insights, reactions, feed data |
| **Synthetic Activities** | `cargo run --bin seed-synthetic-activities` | **100+ diverse activities (run, MTB, nordic ski, etc.)** |

### Synthetic Activities Seeder (NEW - For Testing Without Strava)

**CRITICAL: Use this seeder for testing without OAuth.**

```bash
# Seed 100 activities for default test user
cargo run --bin seed-synthetic-activities

# Seed more activities
cargo run --bin seed-synthetic-activities -- --count 200

# Seed for specific user
cargo run --bin seed-synthetic-activities -- --email alice@example.com

# Reset and reseed
cargo run --bin seed-synthetic-activities -- --reset --count 150
```

**Sport types included:** Run, Trail Run, Ride, Mountain Bike, Gravel Ride, Nordic Ski, Backcountry Ski, Alpine Ski, Swim, Hike, Walk, Weight Training, Yoga, Rowing, Kayaking, SUP, and more.

### Run All Seeders (Full Test Setup)

**Option A: Fresh database with ALL seeders (RECOMMENDED)**
```bash
./bin/reset-dev-db.sh
```
This wipes the database and runs ALL seeders automatically.

**Option B: Run seeders individually (existing database)**
```bash
cargo run --bin seed-coaches
cargo run --bin seed-demo-data
cargo run --bin seed-mobility
cargo run --bin seed-social
```

### When to Run Which Seeder

| Testing This Feature | Required Seeders |
|---------------------|------------------|
| Mobile app login | `seed-coaches` (minimal) |
| Coach conversations | `seed-coaches` |
| Activity list/analysis | **`seed-synthetic-activities`** |
| Performance insights | **`seed-synthetic-activities`** |
| Dashboard/Analytics | `seed-demo-data` |
| Mobility/Stretching | `seed-mobility` |
| Friends/Feed/Social | `seed-social` + `seed-synthetic-activities` |
| **Full E2E testing** | **All seeders** |

## Complete User Workflow

After server is running, to create a test user with full access:
```bash
./scripts/complete-user-workflow.sh
```

This script:
1. Creates/gets admin token
2. Registers regular user (user@example.com)
3. Approves user with tenant creation
4. Tests MCP access
5. Saves tokens to `.workflow_test_env`

## iOS Simulator Testing

When testing the mobile app with iOS Simulator:

### 1. Reset Database with Full Test Data
```bash
./bin/reset-dev-db.sh
```
This creates a fresh database with ALL seeders (coaches, demo data, mobility, social).

### 2. Start Server
```bash
./bin/start-server.sh
```

### 3. Run User Workflow (creates test user)
```bash
./scripts/complete-user-workflow.sh
```

### 4. Login Credentials for Mobile App
```
Email:    user@example.com
Password: userpass123
```

### 5. Start Mobile App
```bash
cd frontend-mobile && bun start
```

## Server Endpoints

| Endpoint | Purpose |
|----------|---------|
| `http://localhost:8081/health` | Health check |
| `http://localhost:8081/oauth2/login` | Web login page |
| `http://localhost:8081/oauth/token` | OAuth token endpoint |
| `http://localhost:8081/mcp` | MCP protocol endpoint |
| `http://localhost:8081/admin/*` | Admin endpoints |

## Manual Server Control

### Start Server Only
```bash
./bin/start-server.sh
```

### Stop Server
```bash
./bin/stop-server.sh
```

### Check Server Status
```bash
curl http://localhost:8081/health
```

## Troubleshooting

### Server won't start
```bash
# Kill any existing processes
pkill -f pierre-mcp-server

# Check port availability
lsof -i :8081

# Start fresh
./bin/setup-and-start.sh
```

### Database errors
```bash
# Reset database completely
./bin/reset-dev-db.sh
```

### Token expired
```bash
# Generate new admin token
cargo run --bin pierre-cli -- token generate --service test --expires-days 7
```

### Missing .envrc
```bash
cp .envrc.example .envrc
direnv allow
```

## Environment Files After Setup

After running `complete-user-workflow.sh`:
```bash
# Contains JWT tokens for API testing
source .workflow_test_env

# Use tokens in curl commands
curl -H "Authorization: Bearer $JWT_TOKEN" http://localhost:8081/mcp ...
```

## Related Skills
- `validate-frontend` - Frontend validation
- `validate-mobile` - Mobile app validation
- `create-worktree` - Git worktree for feature branches
