---
name: research-executor
description: "Execute research experiments using TDD methodology. Pops plans from .claude/plans/research_tasks/, implements with smoke/unit/integration tests, and documents results to results.md. Use when: (1) executing the next experiment from the queue, (2) executing a specific plan by number, (3) running an ad-hoc research idea with TDD."
user_invocable: true
---

# Research Executor

Execute research experiments using Test-Driven Development (TDD).

## Plan Queue

Plans are stored in `.claude/plans/research_tasks/plan-*.md`.

### Pop and Execute

1. **List plans**: `ls .claude/plans/research_tasks/plan-*.md`
2. **Select plan**: Default is `plan-1.md`, or specify `plan-N`
3. **Move to executed**:
   ```bash
   mkdir -p .claude/plans/research_tasks/executed
   mv .claude/plans/research_tasks/plan-{N}.md .claude/plans/research_tasks/executed/{YYYY-MM-DD}_{name}.md
   ```
4. **Renumber remaining plans** sequentially (plan-2 → plan-1, plan-3 → plan-2, etc.)

If no plans exist, ask user for an ad-hoc research idea.

## Execution Workflow

### Phase 1: Setup
- Parse hypothesis, variables, success criteria from plan
- Create directory:
  ```
  experiments/{experiment_name}/
  ├── README.md
  ├── notebook.ipynb          # Primary deliverable
  ├── tests/
  │   ├── smoke/
  │   ├── unit/
  │   └── integration/
  ├── src/
  └── results/
      └── figures/            # All generated plots
  ```

### Phase 2: Smoke Tests
- Test data loading, API calls, metric computation
- Implement minimal code to pass
- Run: `uv run pytest experiments/{name}/tests/smoke/ -v`

### Phase 3: Unit Tests
- Test each component (preprocessing, features, model, evaluation)
- TDD: Red → Green → Refactor
- Run: `uv run pytest experiments/{name}/tests/unit/ -v`

### Phase 4: Integration Tests
- Test full pipeline end-to-end
- Run on sampled data first
- Run: `uv run pytest experiments/{name}/tests/integration/ -v`

### Phase 5: Finalize
- Run full experiment
- Create Jupyter notebook deliverable (see below)
- Document results (see Results Documentation)
- Commit changes

## Jupyter Notebook Deliverable

**Required**: Every experiment MUST produce a Jupyter notebook at `experiments/{name}/notebook.ipynb`.

### Notebook Structure

```
1. Header & Setup
   - Experiment title, date, hypothesis
   - Import statements and configuration

2. Data Loading & Exploration
   - Load experimental data
   - Show sample data, shapes, dtypes
   - Basic statistics (describe(), value_counts())

3. Implementation
   - Core experiment code with explanatory markdown cells
   - Each major step in its own cell for re-runnability

4. Results & Visualizations
   - All figures generated inline (use %matplotlib inline)
   - Statistical tests with p-values, confidence intervals
   - Summary tables of key metrics

5. Conclusions
   - Key findings from the experiment
   - Link to hypothesis: supported/refuted/inconclusive
   - Next steps or follow-up questions
```

### Requirements

- All cells must be executed (outputs saved in notebook)
- Use markdown cells to explain each section
- Save figures both inline AND to `experiments/{name}/results/figures/`
- Include reproducibility info: random seeds, package versions
- Final cell: print summary statistics and status

## Results Documentation

Create `results.md` in `.claude/plans/research_tasks/executed/` alongside the executed plan:

```markdown
# Experiment: {name}

**Date**: {YYYY-MM-DD}
**Plan**: {original plan path}
**Status**: success | failure | partial

## Hypothesis
{from plan}

## Test Results
- Smoke: X/Y passing
- Unit: X/Y passing
- Integration: X/Y passing

## Findings
{key observations, metrics, conclusions}

## Artifacts
- **Notebook**: `experiments/{name}/notebook.ipynb` (primary deliverable)
- Code: `experiments/{name}/src/`
- Figures: `experiments/{name}/results/figures/`
- Data: `experiments/{name}/results/`
```

## Code Standards

- Type hints for all functions
- Docstrings for public APIs
- Reproducible random seeds (document in README)
- Use `uv run ruff check` and `uv run ruff format` before commits
