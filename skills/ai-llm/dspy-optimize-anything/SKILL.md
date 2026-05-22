---
name: dspy-optimize-anything
description: Universal text artifact optimizer using GEPA's optimize_anything API for code, prompts, agent architectures, configs, and more
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# GEPA optimize_anything

## Goal

Optimize any artifact representable as text — code, prompts, agent architectures, vector graphics, configurations — using a single declarative API powered by GEPA's reflective evolutionary search.

## When to Use

- **Beyond prompt optimization** — optimizing code, configs, SVGs, scheduling policies, etc.
- **Single hard problems** — circle packing, kernel generation, algorithm discovery
- **Batch related problems** — CUDA kernels, code generation tasks with cross-transfer
- **Generalization** — agent skills, policies, or prompts that must transfer to unseen inputs
- When you can **express quality as a score** and provide **diagnostic feedback** (ASI)

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| `seed_candidate` | `str \| dict[str, str] \| None` | Starting artifact text, or `None` for seedless mode |
| `evaluator` | `Callable` | Returns score (higher=better), optionally with ASI dict |
| `dataset` | `list \| None` | Training examples (for multi-task and generalization modes) |
| `valset` | `list \| None` | Validation set (for generalization mode) |
| `objective` | `str \| None` | Natural language description of what to optimize for |
| `background` | `str \| None` | Domain knowledge and constraints |
| `config` | `GEPAConfig \| None` | Engine, reflection, and tracking settings |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `result.best_candidate` | `str \| dict` | Best optimized artifact |

## Workflow

### Phase 1: Install

```bash
pip install gepa
```

### Phase 2: Define Evaluator with ASI

The evaluator scores a candidate and returns Actionable Side Information (ASI) — diagnostic feedback that guides the LLM proposer during reflection.

**Simple evaluator (score only):**

```python
import gepa.optimize_anything as oa

def evaluate(candidate: str) -> float:
    score, diagnostic = run_my_system(candidate)
    oa.log(f"Error: {diagnostic}")  # captured as ASI
    return score
```

**Rich evaluator (score + structured ASI):**

```python
def evaluate(candidate: str) -> tuple[float, dict]:
    result = execute_code(candidate)
    return result.score, {
        "Error": result.stderr,
        "Output": result.stdout,
        "Runtime": f"{result.time_ms:.1f}ms",
    }
```

ASI can include open-ended text, structured data, multi-objectives (via `scores`), or images (via `gepa.Image`) for vision-capable LLMs.

### Phase 3: Choose Optimization Mode

**Mode 1 — Single-Task Search:** Solve one hard problem. No dataset needed.

```python
result = oa.optimize_anything(
    seed_candidate="<your initial artifact>",
    evaluator=evaluate,
)
```

**Mode 2 — Multi-Task Search:** Solve a batch of related problems with cross-transfer.

```python
result = oa.optimize_anything(
    seed_candidate="<your initial artifact>",
    evaluator=evaluate,
    dataset=tasks,
)
```

**Mode 3 — Generalization:** Build a skill/prompt/policy that transfers to unseen problems.

```python
result = oa.optimize_anything(
    seed_candidate="<your initial artifact>",
    evaluator=evaluate,
    dataset=train,
    valset=val,
)
```

**Seedless mode:** Describe what you need instead of providing a seed.

```python
result = oa.optimize_anything(
    evaluator=evaluate,
    objective="Generate a Python function `reverse()` that reverses a string.",
)
```

### Phase 4: Use Results

```python
print(result.best_candidate)
```

## Production Example

```python
import gepa.optimize_anything as oa
from gepa import Image
import logging

logger = logging.getLogger(__name__)

# ---------- SVG optimization with VLM feedback ----------

GOAL = "a pelican riding a bicycle"
VLM = "vertex_ai/gemini-3-flash-preview"

VISUAL_ASPECTS = [
    {"id": "overall",     "criteria": f"Rate overall quality of this SVG ({GOAL}). SCORE: X/10"},
    {"id": "anatomy",     "criteria": "Rate pelican accuracy: beak, pouch, plumage. SCORE: X/10"},
    {"id": "bicycle",     "criteria": "Rate bicycle: wheels, frame, handlebars, pedals. SCORE: X/10"},
    {"id": "composition", "criteria": "Rate how convincingly the pelican rides the bicycle. SCORE: X/10"},
]

def evaluate(candidate, example):
    """Render SVG, score with a VLM, return (score, ASI)."""
    image = render_image(candidate["svg_code"])  # via cairosvg
    score, feedback = get_vlm_score_feedback(VLM, image, example["criteria"])

    return score, {
        "RenderedSVG": Image(base64_data=image, media_type="image/png"),
        "Feedback": feedback,
    }

result = oa.optimize_anything(
    seed_candidate={"svg_code": "<svg>...</svg>"},
    evaluator=evaluate,
    dataset=VISUAL_ASPECTS,
    background=f"Optimize SVG source code depicting '{GOAL}'. "
               "Improve anatomy, composition, and visual quality.",
)

logger.info(f"Best SVG:\n{result.best_candidate['svg_code']}")


# ---------- Code optimization (single-task) ----------

def evaluate_solver(candidate: str) -> tuple[float, dict]:
    """Evaluate a Python solver for a mathematical optimization problem."""
    import subprocess, json

    proc = subprocess.run(
        ["python", "-c", candidate],
        capture_output=True, text=True, timeout=30,
    )

    if proc.returncode != 0:
        oa.log(f"Runtime error: {proc.stderr}")
        return 0.0, {"Error": proc.stderr}

    try:
        output = json.loads(proc.stdout)
        return output["score"], {
            "Output": output.get("solution"),
            "Runtime": f"{output.get('time_ms', 0):.1f}ms",
        }
    except (json.JSONDecodeError, KeyError) as e:
        oa.log(f"Parse error: {e}")
        return 0.0, {"Error": str(e), "Stdout": proc.stdout}

result = oa.optimize_anything(
    evaluator=evaluate_solver,
    objective="Write a Python solver for the bin packing problem that "
              "minimizes the number of bins. Output JSON with 'score' and 'solution'.",
    background="Use first-fit-decreasing as a starting heuristic. "
               "Higher score = fewer bins used.",
)

print(result.best_candidate)


# ---------- Agent architecture generalization ----------

def evaluate_agent(candidate: str, example: dict) -> tuple[float, dict]:
    """Run an agent architecture on a task and score it."""
    exec_globals = {}
    exec(candidate, exec_globals)
    agent_fn = exec_globals.get("solve")

    if agent_fn is None:
        return 0.0, {"Error": "No `solve` function defined"}

    try:
        prediction = agent_fn(example["input"])
        correct = prediction == example["expected"]
        score = 1.0 if correct else 0.0
        feedback = "Correct" if correct else (
            f"Expected '{example['expected']}', got '{prediction}'"
        )
        return score, {"Prediction": prediction, "Feedback": feedback}
    except Exception as e:
        return 0.0, {"Error": str(e)}

result = oa.optimize_anything(
    seed_candidate="def solve(input):\n    return input",
    evaluator=evaluate_agent,
    dataset=train_tasks,
    valset=val_tasks,
    background="Discover a Python agent function `solve(input)` that "
               "generalizes across unseen reasoning tasks.",
)

print(result.best_candidate)
```

## Integration with DSPy

`optimize_anything` complements DSPy's built-in optimizers. Use DSPy optimizers (GEPA, MIPROv2, BootstrapFewShot) for DSPy programs, and `optimize_anything` for arbitrary text artifacts outside DSPy:

```python
import dspy
import gepa.optimize_anything as oa

# DSPy program optimization (use dspy.GEPA)
optimizer = dspy.GEPA(
    metric=gepa_metric,
    reflection_lm=dspy.LM("openai/gpt-4o"),
    auto="medium",
)
compiled = optimizer.compile(agent, trainset=trainset)

# Non-DSPy artifact optimization (use optimize_anything)
result = oa.optimize_anything(
    seed_candidate=my_config_yaml,
    evaluator=eval_config,
    background="Optimize Kubernetes scheduling policy for cost.",
)
```

## Best Practices

1. **Rich ASI** — The more diagnostic feedback you provide, the better the proposer can reason about improvements
2. **Use `oa.log()`** — Route prints to the proposer as ASI instead of stdout
3. **Structured returns** — Return `(score, dict)` tuples for multi-faceted diagnostics
4. **Seedless for exploration** — Use `objective=` when the solution space is large and unfamiliar
5. **Background context** — Provide domain knowledge via `background=` to constrain the search
6. **Generalization mode** — Always provide `valset` when the artifact must transfer to unseen inputs
7. **Images as ASI** — Use `gepa.Image` to pass rendered outputs to vision-capable LLMs

## Limitations

- Requires the `gepa` package (`pip install gepa`)
- Evaluator must be deterministic or low-variance for stable optimization
- Compute cost scales with number of candidates explored
- Single-task mode does not generalize; use mode 3 with `valset` for transfer
- Currently powered by GEPA backend; API is backend-agnostic for future strategies
