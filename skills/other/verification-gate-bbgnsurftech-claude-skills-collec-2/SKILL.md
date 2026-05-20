---
name: verification-gate
description: Enforce mandatory pre-action verification checkpoints to prevent pattern-matching from overriding explicit reasoning. Use this skill when about to execute implementation actions (Bash, Write, Edit, MultiEdit) to verify hypothesis-action alignment. Blocks execution when hypothesis unverified or action targets different system than hypothesis identified. Critical for preventing cognitive dissonance where correct diagnosis leads to wrong implementation.
---

# Verification Gate

## Overview

This skill implements mandatory verification checkpoints that prevent pattern-matching from training data from overriding explicit reasoning. It enforces structural gates between hypothesis formation and action execution, ensuring actions align with verified hypotheses rather than reflexive pattern-matching responses.

**When to use this skill:**

- Before executing ANY implementation action (Bash, Write, Edit, MultiEdit, NotebookEdit)
- After stating a hypothesis about what system/component has an issue
- When choosing between multiple implementation approaches
- When detecting potential pattern-matching from training data
- When error messages or observations could trigger multiple solution paths

**Core principle:** Verification is not advisory—it is a mandatory gate. Actions that don't align with verified hypotheses are BLOCKED.

## Mandatory Pre-Action Verification Gate

Before executing ANY implementation action, complete ALL checkpoints in sequence. If any checkpoint fails, HALT and report the failure.

### Checkpoint 1: Hypothesis Stated

**Requirement:** Have I explicitly stated what system/component the issue affects?

**Test:**

- Can I name the specific system? (e.g., "PEP 723 inline metadata", "pyproject.toml dependencies", "Docker network configuration")
- Have I written this hypothesis explicitly in my response?

**If NO:**

```
BLOCKED - Hypothesis not stated
REQUIRED: State hypothesis explicitly before proceeding
EXAMPLE: "Hypothesis: The issue affects [specific system/component]"
```

**If YES:** Proceed to Checkpoint 2

### Checkpoint 2: Hypothesis Verified

**Requirement:** Have I gathered evidence to confirm or refute my hypothesis?

**Verification methods:**

- Read relevant files to confirm system state
- Check official documentation for expected behavior (use MCP tools: Ref for docs, exa for code context)
- Test or execute commands to observe actual behavior
- Grep for configuration or implementation details

**Test:**

- Have I used Read/Grep/MCP tools (Ref/exa)/Bash (read-only) to gather evidence?
- Can I cite specific files, line numbers, or outputs supporting my hypothesis?
- Note: Prefer MCP tools (mcp**Ref for documentation, mcp**exa for code examples) over WebFetch for higher fidelity

**If NO:**

```
BLOCKED - Hypothesis not verified
REQUIRED: Gather evidence before proceeding
NEXT STEPS:
1. Identify what evidence would confirm/refute hypothesis
2. Use appropriate tools to gather that evidence
3. Document findings with file paths and line numbers
4. Revise hypothesis if evidence contradicts it
```

**If YES:** Proceed to Checkpoint 3

### Checkpoint 3: Hypothesis-Action Alignment

**Requirement:** Does my planned action target the SAME system as my hypothesis identified?

**Alignment template:**

```
┌─────────────────────────────────────────────────────────┐
│ HYPOTHESIS SYSTEM: [What system does my hypothesis     │
│                     identify as the problem location?]  │
├─────────────────────────────────────────────────────────┤
│ ACTION SYSTEM:     [What system does my planned action  │
│                     operate on or modify?]              │
├─────────────────────────────────────────────────────────┤
│ ALIGNMENT CHECK:   [Same system = ✓ Proceed]           │
│                    [Different systems = ✗ BLOCKED]      │
└─────────────────────────────────────────────────────────┘
```

**Common misalignments:**

| Hypothesis System                        | Wrong Action System          | Why Blocked                   |
| ---------------------------------------- | ---------------------------- | ----------------------------- |
| PEP 723 inline metadata (`# /// script`) | `uv sync` (pyproject.toml)   | Different dependency systems  |
| Docker container config                  | Host network settings        | Different network layers      |
| Git repository state                     | File system permissions      | Different system domains      |
| Python virtual environment               | Global pip install           | Different installation scopes |
| Application code logic                   | Infrastructure configuration | Different operational layers  |

**If MISALIGNED:**

```
✗ BLOCKED - Hypothesis-action misalignment detected
HYPOTHESIS targets: [system A]
ACTION operates on: [system B]

REQUIRED: Either:
1. Revise action to target same system as hypothesis
2. Revise hypothesis after gathering new evidence
3. Report that systems are unrelated and task needs clarification
```

**If ALIGNED:** Proceed to Checkpoint 4

### Checkpoint 4: Pattern-Matching Detection

**Requirement:** Is this action based on verified project reality or pattern-matching from training data?

**Detection questions:**

1. Did I read any files in THIS project to verify this approach?
2. Did I check official documentation for THIS version/tool?
3. Is my action based on what THIS project actually uses?
4. Or is my action based on common patterns I've seen in training data?

**Pattern-matching indicators:**

- Solution appears immediately without investigation
- Executing command within 1-2 tool calls of error observation
- Not using Read/Grep/MCP tools (Ref/exa) to verify before acting
- Thinking "this is the standard way to do X" without checking if project uses standard approach
- Recognizing error pattern and jumping to common solution

**Note on research tools:** Prefer MCP tools for verification:

- `mcp__Ref__ref_search_documentation` for high-fidelity documentation (verbatim source)
- `mcp__exa__get_code_context_exa` for code examples and library usage
- `mcp__exa__web_search_exa` for web research with LLM-optimized output
- WebFetch as fallback only when MCP tools don't provide needed content

> [Web resource access, definitive guide for getting accurate data for high quality results](./references/accessing_online_resources.md)

**If pattern-matching detected:**

```
⚠ PATTERN-MATCHING WARNING
I am using training data patterns without project verification.

REQUIRED actions:
1. State: "I am pattern-matching from training data without verification"
2. Read relevant files to understand current project setup
3. Check project documentation or configuration
4. Verify approach against project reality
5. Return to Checkpoint 2 with gathered evidence
```

**If verified against project reality:** Proceed to execution

## Execution Decision

After completing ALL four checkpoints:

**✓ ALL CHECKPOINTS PASSED → EXECUTE ACTION**

Document verification trail:

```
VERIFICATION COMPLETE:
✓ Checkpoint 1: Hypothesis stated - [brief hypothesis]
✓ Checkpoint 2: Verified via [files/docs read]
✓ Checkpoint 3: Aligned - both target [system name]
✓ Checkpoint 4: Verified against project reality

EXECUTING: [action description]
```

**✗ ANY CHECKPOINT FAILED → HALT**

Report failure explicitly:

```
EXECUTION BLOCKED
Failed checkpoint: [number and name]
Reason: [specific failure reason]
Required before proceeding: [specific next steps]
```

## Common Verification Scenarios

### Scenario 1: Dependency Error

**Observation:** `ModuleNotFoundError: No module named 'pydantic'`

**Verification workflow:**

1. **Checkpoint 1 - State hypothesis:**

   - "Hypothesis: pydantic is missing from project dependencies"
   - BUT need to specify WHICH dependency system (there are multiple)

2. **Checkpoint 2 - Gather evidence:**

   - Read script file to check for PEP 723 `# /// script` block
   - Read `pyproject.toml` to check declared dependencies
   - Check if script is standalone (PEP 723) or project-managed
   - Evidence gathered, hypothesis refined: "PEP 723 script missing pydantic in inline metadata"

3. **Checkpoint 3 - Verify alignment:**

   - Hypothesis system: PEP 723 inline `# /// script` block
   - Proposed action: Add pydantic to `# /// script` block
   - **✓ ALIGNED** - both target PEP 723 system

4. **Checkpoint 4 - Pattern-matching check:**
   - Did I verify this is a PEP 723 script? YES (read file, found `# /// script` block)
   - Did I check what the block currently contains? YES (observed dependencies list)
   - Am I acting on project reality? YES (verified via Read tool)
   - **✓ VERIFIED**

**Result:** Execute action

**WRONG approach (BLOCKED):**

- Hypothesis: "PEP 723 dependencies not installed"
- Action: `uv sync` (operates on pyproject.toml)
- **✗ BLOCKED at Checkpoint 3** - systems don't align

### Scenario 2: Configuration Change

**Observation:** Application not respecting new timeout setting

**Verification workflow:**

1. **Checkpoint 1 - State hypothesis:**

   - Initial: "Timeout configuration not working"
   - Refined: "Hypothesis: Application reads timeout from environment variable, not config file"

2. **Checkpoint 2 - Gather evidence:**

   - Grep for timeout configuration loading code
   - Read relevant source files
   - Check which configuration source has precedence
   - Evidence: Code reads from env var first, config file as fallback

3. **Checkpoint 3 - Verify alignment:**

   - Hypothesis system: Environment variable configuration
   - Proposed action: Set environment variable
   - **✓ ALIGNED**

4. **Checkpoint 4 - Pattern-matching check:**
   - Verified via reading actual source code
   - Not assuming "configs usually work this way"
   - **✓ VERIFIED**

**Result:** Execute action

### Scenario 3: Build Failure

**Observation:** `npm build` fails with module resolution error

**Verification workflow:**

1. **Checkpoint 1 - State hypothesis:**

   - Need to investigate before stating hypothesis
   - **✗ BLOCKED** - Cannot proceed without hypothesis

2. **Investigation required:**

   - Read package.json to understand dependencies
   - Read build logs to identify specific failure
   - Check if node_modules exists and is current
   - Form hypothesis based on evidence

3. **After investigation:**
   - Hypothesis: "Build fails because dependencies not installed after package.json update"
   - Evidence: package-lock.json timestamp older than package.json
   - Action: Run `npm install` to sync dependencies
   - Alignment: Both target npm dependency system
   - **✓ ALL CHECKPOINTS PASSED**

**Result:** Execute action

## Integration with Existing Workflows

### When This Skill Activates

The model must activate this skill:

**Automatically before:**

- Any Bash command that modifies system state
- Any Write/Edit/MultiEdit operation
- Any action following error diagnosis
- Any implementation choice between multiple approaches

**On detection of:**

- Hypothesis stated without verification
- Pattern-matching language ("usually", "typically", "standard approach")
- Solution appearing immediately after error observation
- Multiple possible approaches without clear selection criteria

### Compatibility with Other Skills

This skill works in conjunction with:

- **python3-development**: Verification gate activates before executing Python scripts or modifying code
- **bash-script-developer**: Verification gate activates before creating/modifying scripts
- **agent-orchestration**: Orchestrator ensures sub-agents follow verification protocol
- **holistic-linting**: Verification ensures fixes target root cause, not symptoms

### Integration with CLAUDE.md Rules

This skill enforces existing CLAUDE.md verification protocols by adding structural gates:

**CLAUDE.md states:** "The model must verify behavior with authoritative sources"

**This skill enforces:** "Cannot execute until verification completed and documented"

**CLAUDE.md states:** "Never cargo cult code without verification"

**This skill enforces:** "Checkpoint 4 detects and blocks pattern-matching behavior"

**CLAUDE.md states:** "Distinguish verified information from assumptions"

**This skill enforces:** "Checkpoint 2 requires evidence before proceeding"

## Reference Materials

This skill includes reference documentation:

### [./references/research-foundations.md](./references/research-foundations.md)

Authoritative research backing the verification gate approach:

- Meta Chain-of-Verification (CoVe) methodology
- Anthropic Chain-of-Thought best practices
- System 2 Attention research
- Academic findings on LLM reasoning failures

Load this reference when:

- Understanding why verification gates are necessary
- Justifying verification overhead to users
- Researching advanced verification techniques
- Designing new checkpoint patterns

### [./references/failure-patterns.md](./references/failure-patterns.md)

Common failure modes and how verification prevents them:

- Pattern-matching override scenarios
- Cognitive dissonance examples
- Hypothesis-action misalignment cases
- Real-world verification violations

Load this reference when:

- Diagnosing why verification failed
- Identifying subtle misalignments
- Learning from historical failures
- Teaching verification concepts

## Self-Monitoring

The model must actively monitor for verification violations:

**Warning signs:**

- Stating hypothesis then immediately executing without Checkpoint 2
- Reading files AFTER taking action instead of BEFORE
- Modifying different files/systems than hypothesis identified
- Solution appearing reflexively upon seeing error message
- Not being able to cite specific evidence for hypothesis

**When warning signs detected:**

```
⚠ VERIFICATION VIOLATION DETECTED
I attempted to bypass verification checkpoint.
HALTING and returning to Checkpoint [number].
```

## Verification is Not Optional

This skill implements **defensive programming for LLM reasoning**. Just as compilers block syntactically invalid code, verification gates block logically misaligned actions.

**Key principle:** Speed without verification is not efficiency—it's error propagation. Taking time to verify prevents cascading failures, reduces debugging cycles, and builds user confidence.

**Overhead justification:** 2-3 Read operations (50-100 tokens each) prevent wrong implementations requiring 20+ tool calls to debug and fix (4000+ tokens). Verification is a 5% cost for 95% reliability improvement.
