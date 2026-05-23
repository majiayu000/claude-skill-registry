---
name: rlm-context-manager
description: Recursive Language Model context management for processing documents exceeding context window limits. Enables Claude to match Gemini's 2M token context capability through chunking, sub-LLM delegation, and synthesis.
version: 1.0.0
category: cross-model
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Task
triggers:
  - "large context"
  - "context window"
  - "long document"
  - "gemini context"
  - "2M tokens"
  - "exceed context"
---

# RLM Context Manager

**Purpose:** Enable Claude to process documents and contexts that exceed typical context window limits, matching Gemini's large context capabilities through intelligent chunking and recursive processing.

## Architecture (RLM Paper Implementation)

Based on [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) - Recursive Language Models by Zhang, Kraska, Khattab (MIT CSAIL).

| Component | IRP Implementation | Model |
|-----------|-------------------|-------|
| Root LLM | Main Claude Code conversation | Claude Opus 4.5 |
| Sub-LLM (`llm_query`) | `rlm-subcall` Task agent | Claude Haiku |
| External Environment | Persistent Python REPL | Python 3 |
| State Persistence | `${SKILLS_ROOT}/rlm-context-manager/state/` | Pickle |

## Use Cases

- Processing large codebases for analysis
- Analyzing lengthy documents (research papers, legal docs, logs)
- Working with Mnemosyne ledger archives
- Cross-session context restoration
- Bridging context between Claude and Gemini

## Commands

```
/rlm init <context_path>     - Initialize REPL with large context file
/rlm status                  - Show current RLM state (chars loaded, chunks, buffers)
/rlm query <question>        - Query the loaded context
/rlm chunk                   - Materialize context into chunk files
/rlm synthesize              - Merge collected evidence into final answer
/rlm reset                   - Clear RLM state
/rlm export                  - Export buffers to file
```

## Quick Start

```bash
# 1. Initialize with a large context file
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py init /path/to/large_document.txt

# 2. Check status
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py status

# 3. Scout the context (peek at beginning and end)
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py exec -c "print(peek(0, 3000))"

# 4. Create chunks for sub-LLM processing
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py exec <<'PY'
paths = write_chunks('${SKILLS_ROOT}/rlm-context-manager/state/chunks', size=200000, overlap=0)
print(f"Created {len(paths)} chunks")
PY
```

## Step-by-Step Procedure

### 1. Initialize the REPL State
```bash
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py init <context_path>
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py status
```

### 2. Scout the Context
```bash
# Peek at beginning
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py exec -c "print(peek(0, 3000))"

# Peek at end
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py exec -c "print(peek(len(content)-3000, len(content)))"

# Search for patterns
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py exec -c "print(grep('pattern', max_matches=10))"
```

### 3. Choose Chunking Strategy
- **Semantic chunking:** For structured formats (markdown headings, JSON, log timestamps)
- **Character chunking:** Default ~200k chars with optional overlap

### 4. Materialize Chunks
```bash
python3 ${SKILLS_ROOT}/rlm-context-manager/scripts/rlm_repl.py exec <<'PY'
paths = write_chunks('${SKILLS_ROOT}/rlm-context-manager/state/chunks', size=200000, overlap=0)
print(len(paths))
print(paths[:5])
PY
```

### 5. Sub-LLM Processing Loop

For each chunk, invoke the rlm-subcall subagent:

```
Task: rlm-subcall
Prompt: "Query: <user_query>. Chunk file: <chunk_path>. Extract relevant information."
Model: haiku
```

The sub-LLM returns structured JSON:
```json
{
  "chunk_id": "...",
  "relevant": [{"point": "...", "evidence": "...", "confidence": "high|medium|low"}],
  "missing": ["..."],
  "suggested_next_queries": ["..."],
  "answer_if_complete": "..."
}
```

### 6. Synthesis
Collect sub-LLM outputs and synthesize final answer in main conversation.

## REPL Helper Functions

| Function | Description |
|----------|-------------|
| `peek(start, end)` | Return substring of context |
| `grep(pattern, max_matches, window)` | Regex search with context window |
| `chunk_indices(size, overlap)` | Calculate chunk boundaries |
| `write_chunks(out_dir, size, overlap)` | Materialize chunks to files |
| `add_buffer(text)` | Store intermediate results |

## Guardrails

- Do NOT paste large raw chunks into main chat context
- Use REPL to locate exact excerpts; quote only what you need
- Subagents cannot spawn other subagents (orchestration stays in main conversation)
- Keep scratch/state files under `${SKILLS_ROOT}/rlm-context-manager/state/`
- Prefer chunk sizes ~100k-300k chars per subagent call

## Integration with IRP Protocols

### Mnemosyne Ledger
- Use RLM to process large Mnemosyne archives
- Export buffers as Mnemosyne packets for cross-session persistence

### Cross-Model (Gemini Bridging)
- Load Gemini's large context exports
- Chunk and analyze for Claude consumption
- Synthesize into Mnemosyne-compatible format

### CRTP Packets
- RLM outputs can be formatted as CRTP packets for multi-model relay

## File Structure
```
rlm-context-manager/
├── SKILL.md              # This file
├── scripts/
│   └── rlm_repl.py       # Persistent Python REPL
├── agents/
│   └── rlm-subcall.md    # Sub-LLM agent definition
└── state/                # Runtime state (gitignored)
    ├── state.pkl         # Persisted REPL state
    └── chunks/           # Materialized chunk files
```

## Credits

Based on the RLM paper by Zhang, Kraska, Khattab (MIT CSAIL) and the Claude Code RLM implementation by Brainqub3.
