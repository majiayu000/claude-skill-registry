---
name: skill
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Answer Collector Skill

**Purpose:** Incrementally collect and validate product assessment responses in structured JSON format.

---

## When to Use

- Evaluating new product ideas with rigorous criteria
- Conducting go/no-go assessments before committing resources
- Building a decision audit trail for product decisions
- Gathering structured input from teams or stakeholders
- Progressive refinement of product hypotheses

---

## How It Works

### 1. Reading Questions

Questions are organized in 4 sections (`questions.md`):
- **WHY** (4 Q's): Problem, strategy, resources, timing
- **WHO** (4 Q's): User, access, economics, scale
- **WHAT** (5 Q's): Outcome, monetization, success metrics, fit, risk
- **GO/NO-GO** (4 criteria): Checklist for final decision

Each question is numbered 1-17.

### 2. Writing JSON Incrementally

Start with a template and add answers one at a time:

```json
{
  "metadata": {
    "product_name": "Your Product Name",
    "created_at": "2025-11-03T00:00:00Z",
    "status": "in_progress"
  },
  "answers": {
    "why_section": {
      "q1_problem_evidence": "Answer here..."
    }
  }
}
```

**Build incrementally:**
- Add one answer per interaction
- Preserve all previous answers
- Update `last_updated` timestamp
- Track `completion_percentage` in metadata

### 3. Validation Logic

**Auto-calculate:**
- `answered_questions`: Count non-empty answers
- `completion_percentage`: (answered_questions / 17) × 100
- `go_no_go_result`: "go" if all 4 checklist items true, else "no_go" or "pending"

**Validation rules:**
- All text answers must be non-empty and substantive
- Checklist items (q14-q17) must be boolean (true/false)
- Metadata fields (product_name) required to start
- All timestamps in ISO 8601 format

---

## Quick Reference

| Section | Questions | Type |
|---------|-----------|------|
| WHY | 1-4 | Text |
| WHO | 5-8 | Text |
| WHAT | 9-13 | Text |
| GO/NO-GO | 14-17 | Boolean |

---

## Usage Pattern

1. **Initialize:** Create JSON with metadata and product_name
2. **Collect:** Answer one question, validate, save
3. **Review:** Check completion_percentage and go_no_go_result
4. **Decide:** When all answers complete, review go_no_go_result

---

## File Structure

```
~/.claude/skills/answer-collector/
├── SKILL.md           # This file
├── questions.md       # The 17 assessment questions
├── schema.json        # JSON validation schema
└── assessments/       # (optional) Stored assessment JSONs
    └── product-name.json
```
