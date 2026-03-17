# local-finetune

> Local model fine-tuning pipeline using ACSets + DuckDB + MLX

**Trit**: 0 (Coordinator - orchestrates data flow)
**Bundle**: substrate
**Requires**: duckdb, mlx-lm, acsets skill

## Overview

Pipeline for embedding skills into local models via LoRA fine-tuning on Apple Silicon.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   ACSets    │───▶│   DuckDB    │───▶│   JSONL     │───▶│  mlx-lm     │
│   Schema    │    │   Corpus    │    │  Training   │    │  LoRA       │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Database Location

```
~/skill-substrate/skill_corpus.duckdb
```

## Schema (ACSet-inspired)

```sql
-- Objects: Skill, Example, Category
-- Morphisms: skill_of, category_of, trit_of

CREATE TABLE skills (
    id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE,
    description TEXT,
    location VARCHAR,
    fingerprint UBIGINT,
    color_hex VARCHAR,
    trit INTEGER CHECK (trit IN (-1, 0, 1))
);

CREATE TABLE examples (
    id INTEGER PRIMARY KEY,
    skill_id INTEGER REFERENCES skills(id),
    instruction TEXT NOT NULL,
    input TEXT,
    output TEXT,
    fingerprint UBIGINT,
    trit INTEGER
);

CREATE TABLE claude_history (
    id INTEGER,
    content TEXT,
    ts TIMESTAMP,
    project VARCHAR,
    sessionId VARCHAR,
    fingerprint UBIGINT,
    color_hex VARCHAR,
    trit INTEGER
);
```

## Ingest Claude History

```sql
CREATE TABLE claude_history AS
SELECT
    row_number() OVER () as id,
    display as content,
    to_timestamp(timestamp/1000) as ts,
    project,
    sessionId,
    hash(display || COALESCE(project,'')) as fingerprint,
    '#' || printf('%06x', ABS(hash(display)) % 16777216) as color_hex,
    CAST(ABS(hash(display)) % 3 AS INTEGER) - 1 as trit
FROM read_json('~/.claude/history.jsonl',
    format='newline_delimited',
    ignore_errors=true,
    columns={display: 'VARCHAR', timestamp: 'BIGINT', project: 'VARCHAR', sessionId: 'VARCHAR'}
)
WHERE display IS NOT NULL AND LENGTH(display) > 10;
```

## Ingest Skills from Filesystem

```sql
CREATE TABLE skill_files AS
SELECT
    row_number() OVER () as id,
    regexp_extract(file, '/([^/]+)/[^/]+\.md$', 1) as skill_name,
    file as path,
    hash(file) as fingerprint,
    CAST(ABS(hash(file)) % 3 AS INTEGER) - 1 as trit
FROM glob('~/.claude/skills/*/*.md');

INSERT INTO skills (id, name, location, fingerprint, trit)
SELECT MIN(id), skill_name, FIRST(path), FIRST(fingerprint), FIRST(trit)
FROM skill_files WHERE skill_name IS NOT NULL
GROUP BY skill_name;
```

## Generate Training Pairs from History

```sql
CREATE VIEW training_candidates AS
WITH consecutive AS (
    SELECT
        id, content, ts, project,
        LAG(content) OVER (PARTITION BY project ORDER BY ts) as prev_content,
        LAG(ts) OVER (PARTITION BY project ORDER BY ts) as prev_ts,
        trit, fingerprint
    FROM claude_history
    WHERE LENGTH(content) > 20
)
SELECT
    prev_content as instruction,
    content as output,
    project as category,
    trit, fingerprint, ts
FROM consecutive
WHERE prev_content IS NOT NULL
  AND LENGTH(prev_content) > 10
  AND LENGTH(content) > 50
  AND ts - prev_ts < INTERVAL '5 minutes';
```

## Export to JSONL (Chat Format)

```sql
COPY (
    SELECT json_object(
        'messages', json_array(
            json_object('role', 'user', 'content', instruction),
            json_object('role', 'assistant', 'content', output)
        )
    ) as json_line
    FROM training_candidates
    WHERE LENGTH(instruction) < 2000 AND LENGTH(output) < 4000
    ORDER BY RANDOM()
) TO 'skills_train.jsonl' (FORMAT CSV, QUOTE '', HEADER false);
```

## Generate Skill Knowledge Examples (Python)

```python
#!/usr/bin/env python3
"""Generate training data from skill markdown files."""
import json, os, re
from pathlib import Path

skills_dir = Path.home() / ".claude" / "skills"
output = []

for skill_dir in sorted(skills_dir.iterdir()):
    if not skill_dir.is_dir():
        continue

    skill_name = skill_dir.name
    readme = skill_dir / "README.md"

    if not readme.exists():
        mds = list(skill_dir.glob("*.md"))
        if mds:
            readme = mds[0]
        else:
            continue

    content = readme.read_text()[:8000]

    # Extract description
    desc_match = re.search(r'^#[^#].*?\n\n(.+?)(?:\n\n|\n#)', content, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else content[:500]

    # Q&A: "What is X skill?"
    output.append({
        "messages": [
            {"role": "user", "content": f"What is the {skill_name} skill?"},
            {"role": "assistant", "content": description[:1500]}
        ]
    })

    # Extract code blocks as examples
    code_blocks = re.findall(r'```(\w+)?\n(.+?)```', content, re.DOTALL)
    for lang, code in code_blocks[:3]:
        if 50 < len(code) < 2000:
            output.append({
                "messages": [
                    {"role": "user", "content": f"Show me an example of using {skill_name}" + (f" in {lang}" if lang else "")},
                    {"role": "assistant", "content": f"```{lang or ''}\n{code.strip()}\n```"}
                ]
            })

with open("skill_knowledge.jsonl", "w") as f:
    for item in output:
        f.write(json.dumps(item) + "\n")

print(f"Generated {len(output)} examples")
```

## Split Train/Valid/Test

```bash
cd ~/skill-substrate
cat skills_train.jsonl skill_knowledge.jsonl | \
  awk 'BEGIN{srand()}{print rand()"\t"$0}' | sort -n | cut -f2- > combined_train.jsonl

total=$(wc -l < combined_train.jsonl)
train_n=$((total * 80 / 100))
valid_n=$((total * 10 / 100))

mkdir -p train_data
head -n $train_n combined_train.jsonl > train_data/train.jsonl
tail -n +$((train_n + 1)) combined_train.jsonl | head -n $valid_n > train_data/valid.jsonl
tail -n $valid_n combined_train.jsonl > train_data/test.jsonl
```

## MLX LoRA Fine-Tuning

**IMPORTANT**: Must run from native arm64 shell (not Rosetta).

```bash
# Check architecture first
arch  # Should show 'arm64', not 'i386'

# If i386, wrap with:
arch -arm64 /bin/zsh

# Then run:
mlx_lm.lora \
  --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit \
  --train \
  --data train_data \
  --batch-size 2 \
  --iters 200 \
  --learning-rate 1e-5 \
  --num-layers 8 \
  --steps-per-report 10 \
  --adapter-path adapters/skill-substrate \
  --seed 1069
```

## Model Recommendations by RAM

| RAM | Model | Batch Size |
|-----|-------|------------|
| 16GB | Qwen2.5-0.5B-4bit | 4 |
| 24GB | Qwen2.5-Coder-7B-4bit | 2 |
| 32GB | Qwen2.5-14B-4bit | 1 |
| 64GB+ | Qwen2.5-32B-4bit | 1 |

## Inference with Adapter

```bash
mlx_lm.generate \
  --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit \
  --adapter-path adapters/skill-substrate \
  --prompt "What is the acsets skill?"
```

## Fuse Adapter into Model

```bash
mlx_lm.fuse \
  --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit \
  --adapter-path adapters/skill-substrate \
  --save-path models/skill-substrate-7B
```

## GF(3) Conservation Check

```sql
SELECT
    'skills' as source, COUNT(*) as n, SUM(trit) as gf3,
    CASE WHEN SUM(trit) % 3 = 0 THEN '✓' ELSE '⚠' END as status
FROM skills
UNION ALL
SELECT 'history', COUNT(*), SUM(trit),
    CASE WHEN SUM(trit) % 3 = 0 THEN '✓' ELSE '⚠' END
FROM claude_history;
```

## Troubleshooting

### MLX float16_t Error

**Symptom**: `error: no member named 'float16_t' in the global namespace`

**Cause**: Running under Rosetta (x86_64) instead of native arm64.

**Fix**:
```bash
# Check current arch
arch  # If 'i386', you're in Rosetta

# Option 1: Force arm64
arch -arm64 /bin/zsh -c "mlx_lm.lora ..."

# Option 2: Use native Terminal.app
# System Settings > Terminal > disable "Open using Rosetta"
```

### Out of Memory

Reduce batch-size or num-layers:
```bash
--batch-size 1 --num-layers 4
```

## CLI Quick Reference

```bash
# Status check
duckdb ~/skill-substrate/skill_corpus.duckdb -c \
  "SELECT source, COUNT(*), SUM(trit) FROM (
    SELECT 'skills' as source, trit FROM skills
    UNION ALL SELECT 'history', trit FROM claude_history
  ) GROUP BY source;"

# Regenerate training data
duckdb ~/skill-substrate/skill_corpus.duckdb -c \
  "COPY (SELECT * FROM training_candidates LIMIT 1000)
   TO 'new_train.jsonl' (FORMAT JSON);"

# Test model
mlx_lm.chat --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit \
  --adapter-path adapters/skill-substrate
```

## Files

```
~/skill-substrate/
├── skill_corpus.duckdb       # Main database
├── combined_train.jsonl      # All training examples
├── skill_knowledge.jsonl     # Skill-derived examples
├── skills_train.jsonl        # History-derived examples
├── generate_skill_data.py    # Skill extraction script
├── train_data/
│   ├── train.jsonl          # 80%
│   ├── valid.jsonl          # 10%
│   └── test.jsonl           # 10%
└── adapters/
    └── skill-substrate/     # LoRA weights
```

## Related Skills

- `acsets` - Schema design foundation
- `duckdb-ies` - Interactome analytics
- `gay-mcp` - Deterministic coloring
- `mlx-whisper` - Audio transcription (same MLX stack)

## GF(3) Triad

| Trit | Role | Skill |
|------|------|-------|
| -1 | Data source | duckdb-ies |
| 0 | Orchestrator | **local-finetune** |
| +1 | Model output | mlx-lm inference |

Conservation: (-1) + (0) + (+1) = 0 ✓
