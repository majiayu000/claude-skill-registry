---
name: terminal-agents
description: "High-Performance CLI AI Agents (Claude Code, Gemini CLI, Open Code)."
trigger: terminal OR cli OR agent OR claude code OR gemini cli OR open code OR headless
scope: global
---

# Terminal AI Agents - The "Headless" Powerhouses

> [!TIP]
> These tools allow running AI Agents directly in the terminal, bypassing browser limitations and enabling direct file system access.
> Source: "You've Been Using AI the Hard Way" (Transcript).

## 1. Claude Code (The Daily Driver)

**Role**: Premium Autonomous Developer.

- **Key Features**:
  - **Agents**: Spawn sub-agents (e.g., "Brutal Critic", "Researcher") to work in parallel.
  - **Context**: Maintains `claude.md` for persistent project context.
  - **Power**: Can authenticate via Claude Pro (no API keys needed).
  - **Workflow**: `claude` (interactive) or `claude -p "prompt"` (headless).
- **Use Case**: Complex coding tasks, deep research, and multi-agent orchestration.

## 2. Gemini CLI (The Free Powerhouse)

**Role**: Accessible & Fast Terminal AI.

- **Key Features**:
  - **Free Tier**: Very generous usage limits.
  - **Context**: Maintains `gemini.md`.
  - **System Access**: Can read/write files, execute scripts, and analyze projects.
- **Use Case**: Quick answers, file manipulation, and zero-cost automation.

## 3. Open Code (The Local & Open Alternative)

**Role**: Private & Flexible.

- **Key Features**:
  - **Local Models**: Run Llama 3.2, DeepSeek, etc., locally (via Ollama).
  - **Claude Auth**: Can "borrow" Claude Pro auth for cloud models.
  - **TUI**: Nice Terminal User Interface.
  - **Config**: managed via `config.jsonc`.
- **Use Case**: Privacy-focused tasks, offline work, or using un-censored local models.

## 4. Workflow Integration (The "Holy Trinity")

**Strategy**: Run them all in the same directory.

- **Unified Context**: Ensure `claude.md`, `gemini.md`, and `agents.md` (Codex) are synced or referenced.
- **Parallelism**:
  - Use **Claude** for architecture/coding.
  - Use **Gemini** for broad research/docs.
  - Use **Open Code** (or Codex) for critique/review.
- **Result**: 3 AI brains working on the same file system simultaneously without copy-pasting.
