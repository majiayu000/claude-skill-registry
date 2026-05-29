---
name: iiot-seed/core
description: IIoT database seeding CLI built with @gbg/ctl
---

# iiot-seed/core

CLI tool for seeding the IIoT database with mock data.

## When to Use

- Need to seed IIoT database with test data
- Need to check current data statistics
- Need to clear mock data

## Commands

### seed

Seed the database with mock data.

```bash
# Default (fast mode, all data)
bun run src/lib/iiot/seed/ctl/src/index.ts seed

# Validated mode (schema validation)
bun run src/lib/iiot/seed/ctl/src/index.ts seed --mode validated

# Assets only (skip readings/alarms)
bun run src/lib/iiot/seed/ctl/src/index.ts seed --assets-only

# Clear before seeding
bun run src/lib/iiot/seed/ctl/src/index.ts seed --clear --verbose
```

### stats

Show current data statistics.

```bash
bun run src/lib/iiot/seed/ctl/src/index.ts stats
```

### clear

Clear all mock data.

```bash
bun run src/lib/iiot/seed/ctl/src/index.ts clear
```

## Options

| Option | Alias | Description |
|--------|-------|-------------|
| `--mode` | `-m` | fast (generate_series) or validated (repo batch) |
| `--clear` | `-c` | Clear existing mock data before seeding |
| `--assets-only` | `-a` | Only seed assets (skip readings/alarms) |
| `--verbose` | `-v` | Show detailed output |

## Architecture

Uses tiered seeding approach:
- **Tier 1**: Assets/Alarms via repos (full validation)
- **Tier 2**: Readings via generate_series (performance)

## Layer Composition

```typescript
const FullSeedLayer = Layer.merge(
  SeedPgClientWithMigrations,  // PgClient + Migrator
  IIoTRepositoriesLive         // All repos
)
```

## Database

- Host: localhost:5433
- Database: iiot_mock
- User: iiot

Ensure database is running:
```bash
docker compose -f docker/docker-compose.iiot.yml up -d
```
