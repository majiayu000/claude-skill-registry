---
name: gathering-migration
description: The drum sounds. Bear and Bloodhound gather for safe data movement. Use when migrating data that requires both careful movement and codebase understanding.
---

# Gathering Migration 🌲🐻🐕

The drum echoes through the valleys. The Bear wakes from long slumber, gathering strength for the journey ahead. The Bloodhound sniffs the terrain, understanding every path and connection. Together they move mountains of data safely—nothing lost, nothing broken, everything finding its new home.

## When to Summon

- Complex data migrations requiring codebase exploration
- Moving data between different system architectures
- Schema changes affecting multiple relationships
- Migrations requiring careful pathfinding
- When you need to understand the territory before moving

---

## Grove Tools for This Gathering

Use `gw` and `gf` throughout. Quick reference for migration work:

```bash
# Find migration-related code and schemas
gf --agent search "table_name"      # Find references to affected tables
gf --agent db                       # Find database-related code
gf --agent migrations               # List existing migration files

# Commit completed migrations
gw git ship --write -a -m "feat: migrate description"
```

---

## The Gathering

```
SUMMON → ORGANIZE → EXECUTE → VALIDATE → COMPLETE
   ↓         ↲          ↲          ↲          ↓
Receive  Dispatch   Animals    Verify   Migration
Request  Animals    Work       Data     Complete
```

### Animals Mobilized

1. **🐕 Bloodhound** — Scout the codebase, understand data relationships
2. **🐻 Bear** — Migrate data with patient strength

---

### Phase 1: SUMMON

_The drum sounds. The valleys stir..._

Receive and parse the request:

**Clarify the Migration:**

- What data needs to move?
- From where to where?
- Are relationships involved?
- What's the rollback plan?

**Scope Check:**

> "I'll mobilize a migration gathering for: **[migration description]**
>
> This will involve:
>
> - 🐕 Bloodhound scouting the codebase
>   - Map data relationships
>   - Find all references to affected tables
>   - Identify integration points
>   - Document current patterns
> - 🐻 Bear migrating the data
>   - Backup before moving
>   - Transform in batches
>   - Validate after each phase
>   - Verify complete migration
>
> Proceed with the gathering?"

---

### Phase 2: ORGANIZE

_The animals prepare for the journey..._

Dispatch in sequence:

**Dispatch Order:**

```
Bloodhound ──→ Bear
     │            │
     │            │
Scout          Migrate
Territory      Data
```

**Dependencies:**

- Bloodhound must complete before Bear (needs to understand relationships)

---

### Phase 3: EXECUTE

_The paths are known. The migration begins..._

Execute each phase:

**🐕 BLOODHOUND — SCOUT**

```
"Sniffing out every trail, every connection..."

Phase: SCENT
- Identify source and destination
- Find all tables/collections involved

Phase: TRACK
- Trace foreign key relationships
- Find code that references the data
- Map dependencies

Phase: HUNT
- Deep dive into complex relationships
- Identify orphaned records
- Find edge cases

Phase: REPORT
- Document all findings
- Create relationship diagrams
- List all files that need updates

Phase: RETURN
- Hand off complete map to Bear

Output:
- Data relationship map
- List of affected files
- Migration risk assessment
- Edge case documentation
```

**🐻 BEAR — MIGRATE**

```
"Waking from slumber, moving with strength..."

Phase: WAKE
- Create migration plan
- Set up tools
- Prepare rollback strategy

Phase: GATHER
- Backup all data
- Inventory data quality
- Document row counts

Phase: MOVE
- Transform data in batches
- Handle relationships carefully
- Process in correct order

Phase: HIBERNATE
- Verify row counts match
- Check data integrity
- Validate relationships

Phase: VERIFY
- Application tests pass
- Queries work correctly
- Performance acceptable

Output:
- Migrated data
- Validation reports
- Updated codebase
```

---

### Phase 4: VALIDATE

_The journey ends. Both animals confirm safe arrival..._

**Validation Checklist:**

- [ ] Bloodhound: All relationships mapped
- [ ] Bloodhound: All references found
- [ ] Bloodhound: Edge cases documented
- [ ] Bear: Backup created and verified
- [ ] Bear: Row counts match (source vs dest)
- [ ] Bear: Data integrity checks pass
- [ ] Bear: Foreign keys intact
- [ ] Bear: Application tests pass
- [ ] Bear: Rollback tested

**Data Quality Checks:**

```sql
-- Row count validation
SELECT
  (SELECT COUNT(*) FROM old_table) as source_count,
  (SELECT COUNT(*) FROM new_table) as dest_count;

-- Should be equal

-- Foreign key integrity
SELECT COUNT(*) as orphaned_records
FROM child_table c
LEFT JOIN parent_table p ON c.parent_id = p.id
WHERE p.id IS NULL;

-- Should be 0

-- Data sampling
SELECT * FROM new_table
ORDER BY RANDOM()
LIMIT 10;

-- Spot check transformation logic
```

---

### Phase 5: COMPLETE

_The gathering ends. Data rests in its new home..._

**Completion Report:**

```markdown
## 🌲 GATHERING MIGRATION COMPLETE

### Migration: [Description]

### Animals Mobilized

🐕 Bloodhound → 🐻 Bear

### Territory Mapped (Bloodhound)

- Tables affected: [count]
- Relationships found: [count]
- Code files referencing data: [count]
- Edge cases identified: [list]

### Data Moved (Bear)

- Records migrated: [count]
- Duration: [time]
- Batches processed: [count]
- Errors encountered: [count]

### Validation Results

- Row count match: ✅ [source] = [dest]
- Data integrity: ✅
- Foreign keys: ✅
- Application tests: ✅ [X/Y passing]
- Performance: ✅

### Rollback Status

- Backup retained at: [location]
- Rollback tested: ✅
- Rollback time: [estimated]

### Files Updated

- Migration scripts: [files]
- Application code: [files]
- Documentation: [files]

### Time Elapsed

[Duration]

_The data has found its new home._ 🌲
```

---

## Example Gathering

**User:** "/gathering-migration Move user preferences from users table to separate table"

**Gathering execution:**

1. 🌲 **SUMMON** — "Mobilizing for: Split user preferences. Move theme, notifications from users table to user_preferences table."

2. 🌲 **ORGANIZE** — "Bloodhound scouts → Bear migrates"

3. 🌲 **EXECUTE** —
   - 🐕 Bloodhound: "Found 15,423 users. 234 have theme set. 12 have notifications disabled. Referenced in dashboard, settings, 3 API routes."
   - 🐻 Bear: "Backup created. Migrated in 16 batches. All rows accounted for. FK constraints maintained."

4. 🌲 **VALIDATE** — "15,423 source = 15,423 dest. No orphans. All tests pass."

5. 🌲 **COMPLETE** — "Preferences migrated. Code updated. Backup retained."

---

_Every piece of data arrived safely._ 🌲
