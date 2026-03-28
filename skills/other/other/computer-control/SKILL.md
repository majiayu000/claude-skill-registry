---
name: computer-control
description: 'Guide Claude through computer use API integration - screenshot capture,
  mouse/keyboard control, agent loops, and sandboxed desktop automation. Use when:
  computer use, computer control, desktop automation, screenshot capture, mouse control,
  keyboard control, agent loop, GUI automation, display toolkit, phantom.'
version: 1.0.0
alwaysApply: false
---
# Computer Control Skill

Use Claude's Computer Use API to see and control desktop
environments through screenshots and mouse/keyboard actions.

## When To Use

- Automating GUI-based workflows that lack CLI alternatives
- Testing web applications through visual interaction
- Filling forms, navigating menus, or interacting with desktop apps
- Building automation pipelines that need visual verification

## When NOT To Use

- Tasks achievable through CLI or API (no GUI needed)
- Browser automation better served by Playwright or CDP

## Architecture

The computer use system has three layers:

1. **Display Toolkit** (`phantom.display`) - executes OS-level
   actions via xdotool/scrot on the real or virtual display
2. **Agent Loop** (`phantom.loop`) - manages the conversation
   cycle between Claude API and the display toolkit
3. **CLI** (`phantom.cli`) - command-line interface for running
   tasks or checking environment readiness

```
User Task
    |
    v
Agent Loop  <---->  Claude API (beta)
    |                   |
    v                   v
Display Toolkit    tool_use responses
    |              (click, type, screenshot)
    v
OS Commands (xdotool, scrot)
    |
    v
Display (X11 / Xvfb / WSLg)
```

## Quick Start

### Check environment

```bash
cd plugins/phantom
uv run python -m phantom.cli --check
```

### Run a task

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
uv run python -m phantom.cli "Open Firefox and search for Claude AI"
```

### Use in Python

```python
from phantom.display import DisplayConfig, DisplayToolkit
from phantom.loop import LoopConfig, run_loop

result = run_loop(
    task="Take a screenshot of the desktop",
    api_key="sk-ant-...",
    loop_config=LoopConfig(
        model="claude-sonnet-4-6",
        max_iterations=10,
    ),
    display_config=DisplayConfig(width=1920, height=1080),
)

print(f"Done in {result.iterations} iterations")
print(result.final_text)
```

## API Versions

| Model | Tool Version | Beta Flag |
|-------|-------------|-----------|
| Opus 4.6, Sonnet 4.6, Opus 4.5 | `computer_20251124` | `computer-use-2025-11-24` |
| Sonnet 4.5, Haiku 4.5, older | `computer_20250124` | `computer-use-2025-01-24` |

The `resolve_tool_version()` function handles this mapping
automatically based on the model name.

## Available Actions

**All versions:**
- `screenshot` - capture display
- `left_click` - click at `[x, y]`
- `type` - type text string
- `key` - press key combo (e.g., `ctrl+s`)
- `mouse_move` - move cursor

**Enhanced (20250124+):**
- `scroll` - scroll with direction and amount
- `left_click_drag` - drag between coordinates
- `right_click`, `middle_click`, `double_click`, `triple_click`
- `hold_key` - hold key for duration
- `wait` - pause between actions

**Latest (20251124):**
- `zoom` - inspect screen region at full resolution

## Safety

Computer use carries risks. Follow these guidelines:

1. **Use a sandbox**: Run in Docker or a VM, not your main OS
2. **Limit access**: Do not provide login credentials unless
   necessary, and never for banking or sensitive services
3. **Set iteration caps**: Always use `max_iterations` to
   prevent runaway API costs
4. **Human approval**: For actions with real-world consequences,
   add confirmation callbacks via `on_action`
5. **Close sensitive apps**: Claude sees the full screen via
   screenshots; close anything private before starting

## Environment Requirements

**Linux (native or WSL2 with WSLg):**

```bash
sudo apt install xdotool scrot xclip
```

**Headless (Docker/CI):**

```bash
# Install Xvfb for virtual display
sudo apt install xvfb xdotool scrot xclip
Xvfb :1 -screen 0 1920x1080x24 &
export DISPLAY=:1
```

## Prompting Tips

1. Be specific about each step of the task
2. Add "After each step, take a screenshot and verify" to
   catch mistakes early
3. Use keyboard shortcuts when UI elements are hard to click
4. Provide example screenshots for repeatable workflows
5. Set a system prompt with domain-specific instructions
