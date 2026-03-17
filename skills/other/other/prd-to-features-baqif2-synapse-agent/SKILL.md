---
name: prd-to-features
description: "Convert PRD documents into features.json format with BDD test cases. Use this skill when users need to: (1) convert PRD/design documents into testable feature lists, (2) generate BDD test cases for PRD, (3) create features.json files."
---

# PRD to Features.json

Convert PRD documents into priority-ordered {prd_basename}-{number}.json files containing verifiable BDD test cases.

## Conversion Workflow

### Phase 1: Analyze PRD Completeness

1. Read the PRD document
2. Run the 6-dimension validation from [completeness-checklist.md](references/completeness-checklist.md) for each feature section
3. List incomplete points and ask the user:
   - **I'll provide details** — User provides specific information
   - **Use default assumptions** — Mark in `expected` field with `(Default assumption: ...)`

### Phase 2: Split into Verifiable Behaviors

After determining feature granularity, split each PRD section into independently verifiable behaviors:

```
PRD Section → Multiple features
Each feature → 1-N BDD test cases
Each BDD → Specific steps + Single expected result
```

**Granularity Principle**: Each BDD test case should independently verify a specific behavior.

### Phase 3: Priority Ordering

Order features from high to low priority (array order represents priority):

1. Core Infrastructure — Base components that other features depend on
2. Core Routing/Dispatch — Core logic that determines system behavior
3. Basic Capability Implementation — Concrete functionality implementation layer
4. Tools/Converters — Supporting toolchain
5. Discovery/Integration Mechanisms — Extensibility-related features
6. User Interface/Experience — User-facing interaction features

### Phase 4: Generate JSON

Generate features.json following the [spec.md](references/spec.md) format:

```json
{
  "category": "functional",
  "prd": "filename.md#section-anchor",
  "description": "Feature description",
  "bdd": [
    {
      "title": "Test title",
      "description": "Test description",
      "steps": ["Step 1", "Step 2"],
      "expected": "Expected result"
    }
  ],
  "passes": false
}
```

### Phase 5: Check File Size

- Lines ≤ 1000: Output single `{prd_basename}-{number}.json`
- Lines > 1000: Split by feature module boundaries into `prd-features-01.json`, `prd-features-02.json`

## Output Location

Default output to `plans/` subdirectory at the same level as the PRD:

```
prd-directory/
├── 02-architecture.md    # PRD file
└── prd-features-01.json     # Generated file
```

## Example Dialogue

**User**: Convert this PRD to features.json

**Assistant**:
1. Read PRD, run completeness check
2. List incomplete points (if any)
3. Ask user how to handle them
4. Confirm granularity and priority
5. Generate features.json to `plans/` directory
