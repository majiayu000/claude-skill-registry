---
name: gemini-rlm-min
description: Minimal implementation of Recursive Language Models (RLM) using Gemini 2.0 Flash and a local Python REPL. Enables processing of massive contexts via the Gemini CLI.
version: 1.0.0
category: cross-model
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
triggers:
  - "gemini rlm"
  - "gemini context"
  - "large document gemini"
  - "gemini cli"
---

# Gemini RLM (Minimal)

**Purpose:** Provide a lightweight, CLI-based implementation of the Recursive Language Model architecture using Google's Gemini models. This skill allows for processing extremely large documents by orchestrating chunking, sub-LLM processing, and synthesis entirely via a Python script and the Gemini API.

## Architecture

Based on [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) - Recursive Language Models.

| Component | Implementation | Model |
|-----------|----------------|-------|
| Root LLM | `gem_rlm.py` (Orchestrator) | Gemini 2.0 Flash |
| Sub-LLM | `gem_rlm.py` (Chunk Processor) | Gemini 2.0 Flash |
| External Environment | `scripts/rlm_repl.py` | Python 3 |

## Prerequisites

- **Environment Variable:** `GEMINI_API_KEY` must be set in your shell environment.
  ```bash
  export GEMINI_API_KEY="your_api_key_here"
  ```

## Usage

The primary entry point is the `gem_rlm.py` script.

### Syntax

```bash
${SKILLS_ROOT}/gemini-rlm-min/gem_rlm.py --context <path_to_large_file> --query <"your query"> [options]
```

### Options
- `--chunk-size`: Size of chunks in characters (default: 50000)
- `--overlap`: Overlap between chunks in characters (default: 0)

### Examples

**Analyze a large log file:**
```bash
export GEMINI_API_KEY="AIza..."
${SKILLS_ROOT}/gemini-rlm-min/gem_rlm.py --context ./large_logs.txt --query "Identify all security exceptions and their timestamps"
```

**Summarize a book:**
```bash
${SKILLS_ROOT}/gemini-rlm-min/gem_rlm.py --context ./mobydick.txt --query "Summarize the relationship between Ahab and Starbuck" --chunk-size 100000
```

## How It Works

1.  **Initialization:** The script initializes a persistent Python REPL (`rlm_repl.py`) and loads the large context file into memory.
2.  **Chunking:** The context is split into manageable chunks (e.g., 50k chars) using the REPL.
3.  **Sub-LLM Processing:** The script iterates through each chunk, sending it to `gemini-2.0-flash-exp` with a prompt to extract relevant information.
4.  **Synthesis:** The extracted findings from all chunks are aggregated and sent to the Root LLM (also Gemini 2.0 Flash) to generate the final answer.

## File Structure

```
gemini-rlm-min/
├── SKILL.md              # This definition file
├── gem_rlm.py            # Main CLI Orchestrator
├── scripts/
│   └── rlm_repl.py       # Persistent REPL environment
└── state/                # Runtime state storage (chunks, pickle files)
```

## Integration with IRP

This skill serves as a high-speed, low-overhead alternative to the full `rlm-context-manager` when:
- Quick analysis is needed via CLI.
- The context needs to be processed entirely by Gemini models.
- Minimal dependencies are preferred (no complex agent setup required).
