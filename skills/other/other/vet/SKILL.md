---
name: vet
description: Run vet immediately after ANY logical unit of code changes. Do not batch your changes, do not wait to be asked to run vet, make sure you are proactive.
---

# Vet

**Run vet immediately after ANY logical unit of code changes. Do not batch changes, do not wait to be asked to run vet, make sure you are proactive.**

Vet reviews git diffs and conversation history to find issues in code changes and conversation history. It is most effective when run frequently with conversation history, which helps it catch misunderstandings between what was requested and what was implemented. Despite this, vet is not a replacement for running tests.

## Installation

Install vet using pip or uv:

```bash
# Using pip
pip install verify-everything

# Using uv (recommended)
uv pip install verify-everything

# Verify installation:
vet --help
```

## Running Vet

### Standard Usage

**OpenCode:**
```bash
vet "goal" --history-loader "python ~/.agents/skills/vet/scripts/export_opencode_session.py --session-id <ses_ID>"
```

**Codex:**
```bash
vet "goal" --history-loader "python ~/.codex/skills/vet/scripts/export_codex_session.py --session-file <path-to-session.jsonl>"
```

**Claude Code:**
```bash
vet "goal" --history-loader "python ~/.claude/skills/vet/scripts/export_claude_code_session.py --session-file <path-to-session.jsonl>"
```

**Without Conversation History**
```bash
vet "goal"
```

### Finding Your Session

**OpenCode:** The `--session-id` argument requires a `ses_...` session ID. To find the current session ID, search for the first user message from this conversation in the part files:
1. Find the most unique sentence / question / string in the current conversation.
2. Run: `grep -rl "UNIQUE_MESSAGE" ~/.local/share/opencode/storage/part/` to find the matching part file.
    - IMPORTANT: Verify the conversation you found matches the current conversation and that it is not another conversation with the same search string. This happens frequently so it is paramount you verify this. Repeat steps 1 and 2 until you have verified the session you found is the current conversation.
3. Read the `sessionID` field from that part JSON file.
4. Pass that value as `--session-id`.

**Codex:** Session files are stored in `~/.codex/sessions/YYYY/MM/DD/`. Find the correct conversation using the approach described above for opencode that uses textual search.

**Claude Code:** Session files are stored in `~/.claude/projects/<encoded-path>/`. The encoded path replaces `/` with `-` (e.g. `/home/user/myproject` becomes `-home-user-myproject`). Find the correct conversation using the approach described above for opencode that uses textual search.

NOTE: The examples in the standard usage section assume the user installed the vet skill at the user level, not the project level. Prior to trying to run vet, check if it was installed at the project level which should take precedence over the user level. If it is installed at the project level, ensure the history-loader option points to the correct location.

## Interpreting Results

Vet analyzes the full git diff from the base commit. This may include changes from other agents or sessions working in the same repository. If vet reports issues that relate to changes you did not make in this session, disregard them, assuming they belong to another agent or the user.

## Common Options

- `--base-commit REF`: Git ref for diff base (default: HEAD)
- `--model MODEL`: LLM model to use (default: claude-opus-4-6)
- `--confidence-threshold N`: Minimum confidence 0.0-1.0 (default: 0.8)
- `--output-format FORMAT`: Output as `text`, `json`, or `github`
- `--quiet`: Suppress status messages and 'No issues found.'
- `--agentic`: Mode that routes analysis through the locally installed Claude Code or Codex CLI instead of calling the API directly. Try this if vet fails due to missing API keys. Slower (~3 min) so not recommended as the default.
- `--help`: Show comprehensive list of options
