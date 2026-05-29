---
name: seed-designer
description: "Derive seed data requirements from test cases. Reads specs/testcases/*.md, extracts implicit data preconditions from each test scenario, deduplicates and organizes by entity type, then produces a seed data requirements document and annotated seed script. Use when test cases are created/updated and seed data needs to stay in sync. Triggers: 'design seed data', 'seed data from testcases', 'update seed requirements', 'what data do tests need', or when specs/testcases/ files change."
---

# Seed Designer

Derive seed data requirements from test case preconditions. Ensures every piece of seed data is traceable to a specific test case, and every test case has its data preconditions covered.

> **Core Principle:** Seed data is not invented — it is systematically extracted from test case scenarios. If a test case says "user submits a post to a published event", then the seed data must include a user, a published event, and the associated rules.

## When to Use

- **After writing test cases:** Run this after `tests-kit Insert` adds new test cases
- **After modifying test cases:** Re-derive requirements when scenarios change
- **Before updating seed script:** Ensure the script matches current test needs
- **New project setup:** After the first batch of test cases is written

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `specs/testcases/*.md` | **Yes** | Test case files with scenario descriptions |
| `docs/data-types.md` | **Yes** | Entity definitions (to validate field values) |
| `docs/relationships.md` | Optional | Relationship definitions (to identify needed relations) |

## Outputs

| Output | Purpose |
|--------|---------|
| `specs/seed-data-requirements.md` | Seed data requirements organized by entity type, each row mapped to test cases |
| Seed script annotations | Comments in `scripts/seed_dev_data.py` linking each seed function to test cases |

## Workflow

### Step 1: Scan Test Cases

Read all files in `specs/testcases/` and build a list of test case IDs with their scenario text.

```
For each file in specs/testcases/*.md:
  For each test case (TC-PREFIX-NNN):
    Extract: ID, title, scenario text
    Store in working list
```

### Step 2: Extract Data Preconditions

For each test case, identify what data must exist **before** the scenario can execute.

**Extraction heuristics:**

| Scenario Pattern | Implied Precondition |
|-----------------|---------------------|
| "用户在...页面" | A user exists (what role?) |
| "已发布的活动" | A event with status=published exists |
| "团队 owner 在..." | A group exists with at least one owner member |
| "用户点击帖子删除按钮" | A post exists, owned by the user |
| "评委给参赛内容打分" | An organizer user exists, a submission post exists |
| "未登录用户访问..." | No user precondition (negative test) |

**Output per test case:**

```
TC-XXX-NNN: [title]
  Preconditions:
    - user: [role] (identifier suggestion)
    - event: [status] (identifier suggestion)
    - post: [type, status, owner] (identifier suggestion)
    - relationship: [type, between which entities]
```

### Step 3: Deduplicate and Merge

Many test cases share the same preconditions. Merge identical data requirements.

**Rules:**
- If TC-A needs "a participant user" and TC-B needs "a participant user", they can share the same seed user
- If TC-A needs "a published event" and TC-B needs "a draft event", these are different seed records
- Group by entity type, then by distinguishing attributes (role, status, type, visibility)

**Assign stable identifiers:**

```
Pattern: {entity}_{distinguishing_attribute}_{number}

Examples:
  user_participant_1    (first participant user)
  user_organizer_1      (first organizer user)
  cat_published_1       (first published event)
  cat_draft_1           (first draft event)
  post_daily_1          (first daily post)
  group_public_1        (first public group)
```

### Step 4: Map Relationships

For preconditions that involve relationships between entities, define the required relationship records.

```
Example:
  TC-ENTRY-001 needs: user enrolled in a published event
  → Requires:
    - user_participant_1
    - cat_published_1 (with associated rule)
    - rule_entry_1
    - event_rule: cat_published_1 → rule_entry_1
    - event_group: cat_published_1 → group_public_1 (team enrollment)
    - group_user: group_public_1 → user_participant_1 (owner)
```

### Step 5: Generate Requirements Document

Write `specs/seed-data-requirements.md` with the following structure:

```markdown
# 种子数据需求清单

## [Entity Type] 数据

| 标识 | [Key Attributes] | 用途 | 关联测试用例 |
|------|------------------|------|-------------|
| identifier | attr values | purpose description | TC-XXX-NNN, TC-YYY-MMM |
```

**Requirements for each row:**
- `标识` must be a stable identifier (used in seed script)
- `关联测试用例` must list every TC that depends on this data
- No row should have an empty `关联测试用例` column (orphan seed data)

### Step 6: Annotate Seed Script

Update `scripts/seed_dev_data.py` with comments that link each seed function and data record to the requirements doc:

```python
def seed_users():
    """
    用户种子数据
    数据来源: specs/seed-data-requirements.md > 用户数据
    """
    users = [
        # user_participant_1: TC-POST-001~076, TC-ENTRY-001~010
        {"id": "user_participant_1", "username": "alice", "role": "participant"},
        # user_organizer_1: TC-CAT-001~020, TC-RULE-001~020
        {"id": "user_organizer_1", "username": "organizer", "role": "organizer"},
    ]
```

### Step 7: Verify Coverage

Cross-check that every test case has its preconditions covered.

**Verification checklist:**
- [ ] Every TC ID in `specs/testcases/` appears in at least one `关联测试用例` cell
- [ ] No seed data row has an empty `关联测试用例` (no orphan data)
- [ ] `scripts/seed_dev_data.py` has matching seed functions for every entity table in the requirements doc
- [ ] Seed data respects entity constraints defined in `docs/data-types.md` (valid enum values, required fields)

```bash
# Quick verification: count TCs in testcases vs TCs referenced in seed requirements
grep -oP 'TC-[A-Z]+-\d+' specs/testcases/*.md | sort -u | wc -l
grep -oP 'TC-[A-Z]+-\d+' specs/seed-data-requirements.md | sort -u | wc -l
```

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| **tests-kit** | Upstream — produces the test cases this skill reads |
| **domain-modeler** | Upstream — defines entity schemas that seed data must conform to |
| **api-builder** | Downstream — seed script calls the API endpoints that api-builder generates |

```
tests-kit (Insert) → specs/testcases/*.md
                          ↓
                    seed-designer ← docs/data-types.md (domain-modeler)
                          ↓
                    specs/seed-data-requirements.md
                          ↓
                    scripts/seed_dev_data.py
                          ↓
                    make seed (api-builder endpoints)
```

## Adapting for Different Projects

This skill is project-agnostic:

1. **Replace test case paths** — Adjust `specs/testcases/` to your project's test case location
2. **Replace entity types** — Use your project's entity names instead of user/event/post/etc.
3. **Replace seed script path** — Point to your project's seed data script
4. **Adjust extraction heuristics** — The scenario patterns in Step 2 are examples; adapt to your domain's language
