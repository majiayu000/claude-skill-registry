---
name: create-code
description: >
  Orchestrate the end-to-end coding process for the Horus persona.
  Composes research (/dogpile), isolated execution (/battle),
  structured implementation (/task, /orchestrate), and brutal code review (/review-code).
allowed-tools: Bash, Read
triggers:
  - create code
  - build feature
  - implement algorithm
  - horus coding workflow
  - new project from idea
metadata:
  short-description: End-to-end Horus coding orchestration pipeline
---

# Create Code Skill

The `create-code` skill is the primary coding engine for the **Horus** persona. it orchestrates a multi-stage "Hardened Coding" workflow that ensures code is researched, isolated, tested, and brutally critiqued before completion.

---

## Horus Coding Workflow

The skill follows a strict 6-stage pipeline:

### 1. Idea & Initial Scoping

Horus starts with a high-level idea or requirement.

- **Stage 1 Gate**: Clarification interview to define scope and constraints.

### 2. Deep Research (/dogpile)

Horus research existing implementation patterns, libraries, and potential pitfalls.

- Calls `/dogpile search "<idea> implementation patterns"`
- Aggregates context into a research summary.

### 3. Isolated Execution & Digital Twin (/battle)

Horus spins up an isolated environment to safely test code or run adversarial simulations. This leverages a **Digital Twin** strategy for high-fidelity testing.

- **Tools**: `.pi/skills/battle` for Digital Twin orchestration (isolation). Optionally use `.pi/skills/hack` for security audits.
- **Modes**:
  - `git_worktree`: For repository-level isolation.
  - `docker`: For containerized environment testing.
  - `qemu`: For hardware/microprocessor emulation (firmware).

### 4. Structured Implementation (/task, /orchestrate)

Implementation is driven by `0N_TASKS.md` files with enforced quality gates.

- Uses `/task` to break down the idea into actionable items.
- Uses `/orchestrate` to execute tasks, requiring:
  - **Sanity Tests**: Every task must have a verification script.
  - **Assertions**: Core logic must be asserted.
  - **Definition of Done (DoD)**: Strict criteria for task completion.

### 5. Brutal Code Review (/review-code)

Horus submits the code for a multi-round "Brutal Review".

- Calls `/review-code` using **Copilot GPT-5** (or highest reasoning model available).
- Focuses on "No-Vibes" technical correctness, efficiency, and Horus's specific persona standards.

### 6. Final Research & Consolidation (/dogpile)

Horus performs a final dogpile search with the working code and full context to find any last-minute edge cases or optimizations.

- Consolidation of the project into the Horus/Memory knowledge graph.

---

## Usage

### When to use sub-skills
 - /dogpile: use when the idea or tasks are unclear, novel, or library-dependent; automatically triggered in Stage 2.
 - /battle: use when performance, resilience, or adversarial testing is needed (e.g., scale, concurrency, fuzz); triggered in Stage 3.
 - /hack: use when security-sensitive surfaces exist (auth, crypto, network, plugins, serialization, execution); auto-suggested by heuristics and runnable via --security-audit.
 - /anvil: use for heavy builds or reproducible environment provisioning; pair with /battle when complex dependencies are needed.

### Retry policies
By default, skills have these retry counts with exponential backoff:
- dogpile: 3 retries (research may be flaky)
- battle: 2 retries (isolation can fail transiently)
- review-code: 2 retries (provider may timeout)
- hack: 1 retry (security audits are generally deterministic)
- orchestrate: 1 retry (task execution should be idempotent)

Override via environment or direct run_skill calls.

```bash
# Start a new coding project from an idea
./run.sh start "Implement a high-performance vector store with ArangoDB"

# Resume an existing creation (picks up from last saved stage)
./run.sh resume --project-dir /path/to/project

# Run specific stages (supports project-local logging in .create-code.log)
./run.sh research "idea"
./run.sh review --provider github --model gpt-5 --yes
./run.sh sandbox --mode docker --yes
./run.sh implement --yes
```

## Commands

| Command     | Description                                         |
| ----------- | --------------------------------------------------- |
| `start`     | Launch full 6-stage workflow (saves state)          |
| `resume`    | Restart workflow from the last successful stage     |
| `research`  | Run Stage 2 Dogpile research                        |
| `sandbox`   | Spin up Stage 3 isolated environment (Digital Twin) |
| `battle`    | Run Stage 3 adversarial battle for hardening        |
| `implement` | Run Stage 4 Task/Orchestrate pipeline (uses /plan)  |
| `review`    | Run Stage 5 Brutal Code Review                      |
| `finalize`  | Run Stage 6 Final research and memory commit        |

---

## Key Principles

1. **Isolation First**: Never run untrusted or experimental code on the host.
2. **Quality Gates**: No code proceeds without passing sanity tests and DoD.
3. **Brutal Critique**: Embody Horus's uncompromising standard for technical excellence.
4. **Memory Integration**: Always check and update the knowledge graph.
