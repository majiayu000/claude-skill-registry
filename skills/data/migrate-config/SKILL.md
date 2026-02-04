---
name: migrate-config
description: Migrate .env-only configuration to split secrets/config format
---

Migrate your project from the old .env-only format to the new split format where secrets stay in `.env` (gitignored) and configuration moves to `.specweave/config.json` (committed to git).

**What this command does:**

1. ✅ Analyzes your `.env` file
2. ✅ Classifies variables as "secrets" or "config"
3. ✅ Backs up original `.env` file
4. ✅ Updates `.env` (keeps only secrets)
5. ✅ Creates/updates `.specweave/config.json` (adds config)
6. ✅ Generates `.env.example` for team onboarding

**When to use:**

- You're upgrading from SpecWeave v0.23.x or earlier
- Your `.env` contains both secrets AND configuration (domain, strategy, etc.)
- You want to share configuration with your team via git

**Command:**

```bash
node -e "require('./dist/src/cli/commands/migrate-config.js').migrateConfig()"
```

**Options:**

- `--dry-run`: Preview migration without making changes
- `--yes`: Skip confirmation prompt
- `--force`: Force migration even if not needed

**Example output:**

```
🔄 SpecWeave Configuration Migration

📋 Migration Preview

Classification Results:
  Secrets: 3 variables
  Config:  5 variables

📊 Detailed Breakdown:

  Secrets (will stay in .env):
    JIRA_API_TOKEN=xyzabc***456
    └─ Contains keyword: token

    JIRA_EMAIL=user@example.com
    └─ Email address (used for authentication)

  Configuration (will move to config.json):
    JIRA_DOMAIN=company.atlassian.net
    └─ Non-sensitive configuration data

    JIRA_STRATEGY=project-per-team
    └─ Non-sensitive configuration data

✅ Migration Successful!

Summary:
  ✓ 3 secrets kept in .env
  ✓ 5 config items moved to config.json
  ✓ Backup created: .env.backup.1234567890
  ✓ .env.example generated

📝 Next Steps:

  1. Review .specweave/config.json (commit to git)
  2. Share .env.example with team (commit to git)
  3. Team members: cp .env.example .env (fill in tokens)
```

**Benefits:**

- ✅ Team shares configuration via git
- ✅ Secrets stay local (never committed)
- ✅ Type-safe configuration with validation
- ✅ Easy onboarding for new team members

**Classification logic:**

Variables classified as **secrets** (stay in .env):
- Contains keywords: `token`, `api_token`, `pat`, `secret`, `key`, `password`, `credential`, `auth`
- Email addresses (used for authentication)

Variables classified as **config** (move to config.json):
- Everything else: domains, strategies, project keys, organizations, etc.

**Safety:**

- 🔒 Always creates backup before modifying `.env`
- 🔒 Atomic operation (either completes fully or rolls back)
- 🔒 Idempotent (can run multiple times safely)
- 🔒 Dry-run mode available for preview

**See also:**

- ADR-0050: Secrets vs Configuration Separation
- `/sw:validate` - Validate configuration after migration
- Documentation: `CLAUDE.md` → Configuration Management section
