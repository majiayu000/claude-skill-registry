---
name: synnovator
description: >
  Manage Synnovator platform data: 7 content types (event, post, resource, rule, user, group, interaction)
  and 9 relationship types via a file-based YAML+Markdown engine. Data stored in PROJECT_DIR/.synnovator/.
  Use when performing CRUD operations on platform content, managing activities/competitions, teams,
  posts, user interactions (likes/comments/ratings), or testing user journeys.
  Trigger: any request involving Synnovator platform data, user journey simulation, or content management.
---

# Synnovator

File-based data engine for the Synnovator platform. All records are `.md` files with YAML frontmatter + Markdown body, stored under `PROJECT_DIR/.synnovator/`.

## Quick Start

```bash
# Initialize data directory
uv run python .claude/skills/synnovator/scripts/engine.py --init

# CRUD operations
uv run python .claude/skills/synnovator/scripts/engine.py [--user USER_ID] COMMAND TYPE [OPTIONS]
```

Commands: `create`, `read`, `update`, `delete`

## Data Model

**7 content types** stored as `.md` files in `.synnovator/<type>/`:
- `event` - Activities/competitions (YAML + Markdown body)
- `post` - User posts with tags (YAML + Markdown body)
- `resource` - File attachments (YAML frontmatter only)
- `rule` - Activity rules with scoring criteria (YAML + Markdown body)
- `user` - User accounts (YAML frontmatter only)
- `group` - Teams/groups (YAML frontmatter only)
- `interaction` - Likes, comments, ratings (YAML frontmatter only). Target info is stored in `target_interaction` relation, not on the interaction itself.

**9 relationship types** stored in `.synnovator/relations/<type>/`:
- `event_rule` - Activity-to-rule bindings
- `event_post` - Activity-to-post submissions
- `event_group` - Team activity registration
- `event_event` - Activity association (stage / track / prerequisite)
- `post_post` - Post references/embeds/replies
- `post_resource` - Post-to-attachment links
- `group_user` - Group membership (with approval workflow)
- `user_user` - User follow/block relationships
- `target_interaction` - Content-to-interaction bindings

See [references/schema.md](references/schema.md) for complete field definitions.

## Content CRUD

### Create
```bash
engine.py [--user UID] create <type> --data '<json>' [--body 'markdown content']
```
Auto-generates: `id`, `created_at`, `updated_at`, `deleted_at`. Sets `created_by` from `--user`.

### Read
```bash
engine.py read <type> --id <record_id>           # Single record
engine.py read <type> --filters '<json>'          # Filtered list
engine.py read <type> --include-deleted           # Include soft-deleted
```

### Update
```bash
engine.py update <type> --id <record_id> --data '<json>'
```
For tags: `"+tagname"` appends, `"-tagname"` removes. Body: `"_body": "new markdown"`.

### Delete
```bash
engine.py delete <type> --id <record_id>          # Soft delete (default)
engine.py delete <type> --id <record_id> --hard    # Hard delete
```
Cascades: deleting a post removes its relations and soft-deletes linked interactions.

## Relation CRUD

```bash
engine.py create <rel_type> --data '<json>'                        # Create
engine.py read <rel_type> --filters '<json>'                       # Read
engine.py update <rel_type> --filters '<json>' --data '<json>'     # Update
engine.py delete <rel_type> --filters '<json>'                     # Delete (hard)
```
Use `_` or `:` separator: `event_rule` or `event:rule`.

## Key Behaviors

- **Soft delete**: Sets `deleted_at`, record stays on disk. Default for content types.
- **Hard delete**: Removes file. Default for relations.
- **Cache stats**: `like_count`, `comment_count`, `average_rating` on posts are **read-only** — auto-recalculated when `target_interaction` relations are created/deleted. Manual updates to these fields are silently ignored.
- **Two-step interactions**: Creating an interaction requires: (1) `create interaction` for the record, (2) `create target_interaction` to link it to a target. Cache updates, duplicate-like checks, and target validation happen at step 2.
- **Group approval**: `require_approval=true` sets join status to `pending`; owner approves via `UPDATE group_user`.
- **Uniqueness**: Enforced for user `(username)`, `(email)`; like `(user, target)` at `target_interaction` creation; relation duplicates; user-per-event-per-group (a user can only belong to one group per event); `user_user` `(source_user_id, target_user_id, relation_type)`; `event_event` `(source_category_id, target_category_id)`.
- **Self-reference prevention**: `user_user` and `event_event` cannot reference the same entity as both source and target.
- **Block enforcement**: If user B blocks user A, A cannot follow B.
- **Circular dependency detection**: `event_event` with `stage` or `prerequisite` relation types prevents cycles (A→B→C→A).
- **Prerequisite enforcement**: Creating a `event_group` registration checks that all prerequisite events (via `event_event` prerequisite) are closed.
- **Cascades**: Deleting content cascades to relations and interactions per the schema spec. Notably:
  - Deleting a **group** cascades to both `group_user` and `event_group` relations.
  - Deleting a **user** cascades to `group_user` and `user_user` relations and soft-deletes all user interactions.
  - Deleting a **event** cascades to `event_rule`, `event_post`, `event_group`, and `event_event` relations and soft-deletes linked interactions.

## Rule Enforcement

Rules linked to a event via `event_rule` are **automatically enforced** via a hook system. Rules support two definition styles: **fixed fields** (backward-compatible shorthand) and **declarative checks** (extensible condition-action pairs). All rules must pass (AND logic); any single violation rejects the operation.

### Hook Points

| Operation | Phase | Validations |
|-----------|-------|-------------|
| `create event_post` | pre | Time window, max submissions, submission format, min team size, resource requirements, entry prerequisites |
| `create event_post` | post | Post-submission actions (notifications, etc.) |
| `create group_user` | pre | Max team size (checked against all events the group is registered for) |
| `create group_user` | post | Post-join actions |
| `create event_group` | pre | Prerequisite events closed, entry conditions (team/proposal existence) |
| `create event_group` | post | Post-registration actions |
| `update post.status` | pre | `allow_public` / `require_review` path enforcement |
| `update post.status` | post | Post-status-change actions |
| `update event.status` | pre | Pre-closure validation |
| `update event.status` | post | Closure actions: disqualification flagging, ranking computation, certificate awarding |

### Phases

- **pre**: Runs before the operation. `on_fail: deny` blocks the operation. `on_fail: warn` allows with warning. `on_fail: flag` marks but allows.
- **post**: Runs after a successful operation. Never blocks. Used for compute/award/notify actions.

### Validation Chain

```
event_post:   event → event_rule → rule.checks[trigger=create_relation(event_post)]
group_user:      group → event_group → event → event_rule → rule.checks[trigger=create_relation(group_user)]
event_group:  event → event_event(prerequisite) + event_rule → rule.checks[trigger=create_relation(event_group)]
post.status:     post → event_post → event → event_rule → rule.checks[trigger=update_content(post.status)]
event.status: event → event_rule → rule.checks[trigger=update_content(event.status)]
```

### Fixed Fields as Syntactic Sugar

Fixed fields on Rule (`max_submissions`, `min_team_size`, `submission_format`, etc.) are automatically expanded into equivalent `checks` entries by the engine. User-defined `checks` are appended after expanded entries.

| Fixed Field | Expands To |
|------------|-----------|
| `submission_start` / `submission_deadline` | `time_window` check on `create_relation(event_post)` pre |
| `max_submissions` | `count` check on `create_relation(event_post)` pre |
| `submission_format` | `resource_format` check on `create_relation(event_post)` pre |
| `min_team_size` | `count` check on `create_relation(event_post)` pre |
| `max_team_size` | `count` check on `create_relation(group_user)` pre |
| `allow_public` / `require_review` | `field_match` check on `update_content(post.status)` pre |

### Condition Types

| Type | Description |
|------|-------------|
| `time_window` | Current time within [start, end] |
| `count` | Entity/relation count satisfies op + value |
| `exists` | Entity/relation exists (or must not exist) |
| `field_match` | Entity field matches a predicate |
| `resource_format` | Post resources match allowed formats |
| `resource_required` | Post has minimum required resources |
| `unique_per_scope` | Uniqueness within a scope |
| `aggregate` | Aggregated value (count/sum/avg) meets threshold |

### Action Types (post phase only)

| Action | Description |
|--------|-------------|
| `flag_disqualified` | Mark entities that fail post-closure checks |
| `compute_ranking` | Calculate rankings from `average_rating` |
| `award_certificate` | Auto-create certificate resources and posts per rank range |
| `notify` | Send notifications (reserved, not yet implemented) |

### Behavior

- **No rules linked** → no constraints, operation proceeds normally.
- **Rule field absent** → that constraint is skipped (e.g., no `submission_deadline` means no time limit).
- **Violation (pre)** → operation rejected with error: `Rule '<name>': <reason>`.
- **Violation (post)** → action executes (flag/compute/award), does not rollback.
- Posts not linked to any event are unconstrained (rules only apply through `event_post`).

See `docs/rule-engine.md` for the full specification.

## File Format

Each record is a `.md` file:
```markdown
---
name: 2025 AI Hackathon
type: competition
status: published
id: cat_abc123
created_by: user_alice
created_at: '2025-01-01T00:00:00Z'
---

## Activity Description

Markdown content here.
```

## Testing

Tests are organized as modular files under `scripts/tests/`, one per test-case spec in `specs/testcases/`.

```bash
# Run all tests
uv run python .claude/skills/synnovator/scripts/tests/run_all.py

# Run specific test files by number
uv run python .claude/skills/synnovator/scripts/tests/run_all.py 3 4 11

# Run a single test file directly
uv run python .claude/skills/synnovator/scripts/tests/test_11_user_journeys.py
```

### Test File Map

| # | File | TC Prefix | Coverage |
|---|------|-----------|----------|
| 1 | `test_01_user.py` | TC-USER-* | User CRUD |
| 2 | `test_02_category.py` | TC-CAT-* | Event CRUD |
| 3 | `test_03_rule.py` | TC-RULE-* | Rule CRUD + enforcement |
| 4 | `test_04_group.py` | TC-GRP-* | Group CRUD + approval |
| 5 | `test_05_post.py` | TC-POST-* | Post CRUD + visibility |
| 6 | `test_06_resource.py` | TC-RES-* | Resource CRUD |
| 7 | `test_07_interaction.py` | TC-IACT-* | Interaction CRUD |
| 8 | `test_08_relations.py` | TC-REL-* | All 9 relation types |
| 9 | `test_09_cascade_delete.py` | TC-DEL-* | Cascade delete |
| 10 | `test_10_permissions.py` | TC-PERM-* | Access control |
| 11 | `test_11_user_journeys.py` | TC-JOUR-* | Integration (sequential) |
| 12 | `test_12_resource_transfer.py` | TC-TRANSFER-* | Resource transfer |
| 13 | `test_13_user_follow.py` | TC-FRIEND-* | Follow/block |
| 14 | `test_14_category_association.py` | TC-STAGE/TRACK/PREREQ/CATREL-* | Event associations |
| 15 | `test_15_entry_rules.py` | TC-ENTRY-* | Entry preconditions |
| 16 | `test_16_closure_rules.py` | TC-CLOSE-* | Closure rules |
| 17 | `test_17_rule_engine.py` | TC-ENGINE-* | Rule engine conditions/actions |

Each file uses isolated data directories for parallel-safe execution. Shared fixtures are in `scripts/tests/base.py`.

See [references/endpoints.md](references/endpoints.md) for detailed API examples.
See [references/schema.md](references/schema.md) for complete field and enum definitions.

## Documentation Sync

This skill's data model is the **implementation** of the canonical specs in `docs/` and `specs/`. When modifying the skill's schema, engine logic, or data model, **must** sync the following docs:

| Skill file | Canonical docs | Sync what |
|-----------|---------------|-----------|
| `references/schema.md` | `docs/data-types.md`, `docs/relationships.md` | Field definitions, enums, required fields, relation schemas |
| `scripts/engine.py` (CRUD logic) | `docs/crud-operations.md`, `specs/data-integrity.md` | CRUD operations, cascade strategies, uniqueness constraints |
| `scripts/engine.py` (cache) | `specs/cache-strategy.md` | Cache stats triggers, read-only enforcement |
| `scripts/tests/test_11_user_journeys.py` | `docs/user-journeys.md` | User journey steps, data operation sequences |
| `scripts/tests/test_*.py` | `specs/testcases/*.md` | Test cases aligned 1:1 with spec numbering |

**Checklist when updating the skill:**
1. Update skill code (`engine.py`) and tests (`scripts/tests/test_*.py`)
2. Update skill reference docs (`references/schema.md`, `references/endpoints.md`)
3. Update canonical docs (`docs/data-types.md`, `docs/relationships.md`, `docs/crud-operations.md`, `docs/user-journeys.md`)
4. Run `uv run python .claude/skills/synnovator/scripts/tests/run_all.py` to verify
