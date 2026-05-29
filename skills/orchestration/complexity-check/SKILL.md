---
name: complexity-check
description: Calculates a complexity score (1-50) from a user prompt. Analyzes keywords, scope indicators, quantity modifiers, and negation patterns to determine task complexity. Returns an integer used by commands for routing decisions.
---

# Complexity Check Skill

**Purpose:** Analyze a prompt and return an integer score from 1-50 based on task complexity.

**Input:** `prompt` (string) - The user's request

**Output:** `score` (integer) - Complexity score from 1-50

---

## How to Execute

This is a TEXT ANALYSIS task - parse keywords from the user's prompt as your sole input:

1. Scan the prompt text (case-insensitive) for keywords in the algorithm below
2. Apply each step of the scoring algorithm sequentially
3. Return ONLY: `score: <int>`
4. Complete in under 200 tokens

**Expected output format:**

```
score: 15
```

Always focus on the prompt text as your only input. Work directly with prompt content for keyword-based analysis and scoring.

---

## Scoring Algorithm

### Step 1: Keyword Detection

Scan prompt (case-insensitive) for keywords and add points:

| Category      | Points | Keywords                                                                                   |
| ------------- | ------ | ------------------------------------------------------------------------------------------ |
| Ultra-Complex | +8     | `enterprise`, `architecture`, `monorepo`, `system-wide`, `migration`, `standardize across` |
| Complex       | +6     | `refactor`, `standardize`, `implement`, `build service`, `integrate`                       |
| Standard      | +4     | `create`, `audit`, `configure`, `feature`, `add`, `update`                                 |
| Simple        | +2     | `fix`, `debug`, `explain`, `help`, `check`, `what is`                                      |

**Rules:**

- Each keyword matched adds its points
- Multiple matches in same category still add (e.g., "audit and configure" = +8)

---

### Step 2: Scope Multipliers

Add points for scope indicators:

| Indicator         | Points | Detection Patterns                                               |
| ----------------- | ------ | ---------------------------------------------------------------- |
| Multi-package     | +5     | `all packages`, `across`, `every`, `monorepo`, plural nouns      |
| Database          | +5     | `database`, `schema`, `migration`, `prisma`, `sql`               |
| Config management | +5     | `config`, `configuration`, `settings`, `.json`, `.yaml`          |
| Security-critical | +5     | `auth`, `security`, `credential`, `token`, `password`, `encrypt` |
| API surface       | +5     | `api`, `endpoint`, `rest`, `graphql`, `service`                  |
| Testing scope     | +3     | `test`, `coverage`, `e2e`, `integration test`                    |

---

### Step 3: Quantity Detection

Add points for explicit quantities:

| Pattern                        | Points |
| ------------------------------ | ------ |
| `all` / `every` / `entire`     | +10    |
| Number > 5 (e.g., "10 files")  | +5     |
| Number 2-5                     | +3     |
| Single/specific file mentioned | +0     |

---

### Step 4: Simplicity Adjustment

Reduce score when simplifying words indicate lower complexity:

| Pattern                    | Points |
| -------------------------- | ------ |
| `just` / `only` / `simple` | -3     |
| `quick` / `small`          | -2     |
| Single file path mentioned | -2     |

---

### Step 5: Clamp Result

- Minimum: 1 (always at least 1, never zero or negative)
- Maximum: 50 (cap for sanity)

---

### Step 6: Sanity Check

After calculating, verify the score makes sense:

- Does a score of 5 feel right for "fix typo in README"? (Correct)
- Does a score of 35 feel right for "explain what this function does"? (Recalibrate down if needed)
- Does a score of 8 feel right for "migrate entire database schema across all services"? (Recalibrate up if needed)

**If adjustment needed:** Override calculated score with sensible value aligned with actual task scope.

---

## Examples

### Example 1: Score 2

```
Prompt: "fix the typo in README.md"

  "fix" = +2
  Single file = -2
  Total = 0 -> clamped to 1
```

### Example 2: Score 9

```
Prompt: "audit the eslint config"

  "audit" = +4
  "config" = +5
  Total = 9
```

### Example 3: Score 19

```
Prompt: "implement JWT authentication API with tests"

  "implement" = +6
  "auth" = +5
  "api" = +5
  "test" = +3
  Total = 19
```

### Example 4: Score 34

```
Prompt: "standardize error handling across all microservices in the monorepo"

  "standardize" = +6
  "monorepo" = +8
  "across" = +5
  "all" = +10
  "service" = +5
  Total = 34
```

### Example 5: Score 1 (Negation)

```
Prompt: "just quickly fix the simple auth bug"

  "fix" = +2
  "auth" = +5
  "just" = -3
  "quickly" = -2
  "simple" = -3
  Total = -1 -> clamped to 1
```
