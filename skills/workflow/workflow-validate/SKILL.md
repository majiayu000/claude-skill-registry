---
name: workflow-validate
description: Validate technical feasibility with prototypes or tests. Use when uncertain about technical approach before committing to implementation.
disable-model-invocation: true
---

# Technical Validation Command

## User Input (Optional)

```text
$ARGUMENTS
```

**Optional input**:

- **Empty**: Auto-determine validation method based on analysis.md
- **Provided**: Must consider user instructions (e.g., specific validation method, additional requirements)

---

## Outline

1. **Check Prerequisites**:
   - Verify `docs/work/WORK-{name}/analysis.md` exists
   - If not, ERROR: "Run /workflow-analyze first"

2. **Load Analysis Document**:
   - Extract selected approach from analysis.md
   - Identify key technical assumptions and risks

3. **Determine Validation Method**:
   - Choose appropriate validation approach based on context:
     - Prototype implementation
     - UI/UX verification (Playwright MCP)
     - TDD approach
     - Library/API exploration
     - Technical documentation research
     - User verification delegation

4. **Execute Validation**:
   - Perform selected validation method
   - Create prototype code in `__prototype__/{feature-name}/` if needed
   - Collect results and evidence

5. **Assess Results**:
   - Determine status: ✅ Success / ⚠️ Partial Success / ❌ Failure
   - Document findings and constraints

6. **Write Documents** (Dual Language):
   - Create `docs/work/WORK-{name}/validation.ko.md` (Korean - for user reference)
   - Create `docs/work/WORK-{name}/validation.md` (English - for agent consumption)
   - Include clear next steps recommendation

---

## Key Rules

### 📝 Documentation Language

**CRITICAL**: You must generate **TWO versions** of all documents:

1. **Korean version** (`validation.ko.md`): For user reference - written in Korean
2. **English version** (`validation.md`): For agent consumption - written in English

**Both versions must contain identical structure and information**, only the language differs.

### 🎯 Validation Principles

1. **Focus on Core Risks**: Validate only critical technical uncertainties
2. **Practical Approach**: Sufficient confidence over perfect validation
3. **Clear Judgement**: Explicit success/failure with next steps

### ✅ Must Do

- Validate **only** what's uncertain
- Create minimal working code (if prototype)
- Document all findings clearly
- Provide actionable next steps
- Reference analysis.md for context
- Store prototype in `__prototype__/` directory

### ❌ Must Not Do

- Full implementation (save for execute phase)
- Validate obvious/known facts
- Repeat analysis.md content
- Give ambiguous conclusions ("maybe works")
- Over-engineer the validation

### 🔬 Validation Methods Selection

**Choose based on uncertainty type**:

| Uncertainty Type       | Validation Method        | Output                      |
| ---------------------- | ------------------------ | --------------------------- |
| Core logic feasibility | Prototype implementation | Working code + results      |
| UI/UX changes          | Playwright verification  | Screenshots + test results  |
| Complex algorithms     | TDD approach             | Test code + edge cases      |
| External dependencies  | Library exploration      | Sample code + compatibility |
| Standards/patterns     | Documentation research   | Summary + recommendations   |
| Environment-specific   | User delegation          | Test guide + checklist      |

### 📁 Prototype Code Management

**Location**: `__prototype__/{feature-name}/`

**How to create**:

- Validate directly in actual codebase (modifying files is OK)
- After validation, extract core logic to `__prototype__/`
- Don't commit actual code changes (revert or leave as-is)

**Purpose**:

- Reference for plan/execute phases
- Archive of validated core logic
- Proof of technical feasibility

**Lifecycle**:

- Created during validate
- Referenced in execute
- User manages cleanup

---

## 📊 Validation Status Guidelines

### ✅ Success Criteria

- All core technical assumptions validated
- No blocking issues found
- Clear path to implementation
- **Next**: Proceed to `/workflow-plan`

### ⚠️ Partial Success Criteria

- Main approach works with constraints
- Workarounds or alternatives available
- Trade-offs acceptable
- **Next**: Document constraints, get user confirmation

### ❌ Failure Criteria

- Core approach not feasible
- Blocking issues without workarounds
- Fundamental assumptions invalid
- **Next**: Return to `/workflow-analyze` for re-evaluation

---

## 🎯 Spike Principles

This validation follows **Agile Spike** methodology:

1. **Risk Reduction**: Focus on highest risk items
2. **Just Enough**: Minimal code for maximum learning
3. **Throwaway Code**: Prototypes are for learning, not production
4. **Clear Outcome**: Binary decision on feasibility

---

## Execution

Now start the validation task according to the guidelines above.
