---
name: ck:preview
description: "View files/directories OR generate visual explanations, slides, diagrams."
argument-hint: "[path] OR --explain|--slides|--diagram|--ascii [topic]"
---

# Preview

Universal viewer + visual generator. View existing content OR generate new visual explanations.

## Default (No Arguments)

If invoked without arguments, use `AskUserQuestion` to present available preview operations:

| Operation | Description |
|-----------|-------------|
| `(view)` | View a file or directory |
| `--explain` | Generate visual explanation |
| `--slides` | Generate presentation slides |
| `--diagram` | Generate architecture diagram |
| `--ascii` | Terminal-friendly diagram |
| `--stop` | Stop preview server |

Present as options via `AskUserQuestion` with header "Preview Operation", question "What would you like to do?".

## Usage

### View Mode
- `/ck:preview <file.md>` - View markdown file in novel-reader UI
- `/ck:preview <directory/>` - Browse directory contents
- `/ck:preview --stop` - Stop running server

### Generation Mode
- `/ck:preview --explain <topic>` - Generate visual explanation (ASCII + Mermaid + prose)
- `/ck:preview --slides <topic>` - Generate presentation slides (one concept per slide)
- `/ck:preview --diagram <topic>` - Generate focused diagram (ASCII + Mermaid)
- `/ck:preview --ascii <topic>` - Generate ASCII-only diagram (terminal-friendly)

## Argument Resolution

When processing arguments, follow this priority order:

1. **`--stop`** → Stop server (exit)
2. **Generation flags** (`--explain`, `--slides`, `--diagram`, `--ascii`) → Generation mode. Load `references/generation-modes.md`
3. **Resolve path from argument:**
   - If argument is an explicit path → use directly
   - If argument is a contextual reference → resolve from recent conversation context
4. **Resolved path exists on filesystem** → View mode. Load `references/view-mode.md`
5. **Path doesn't exist or can't resolve** → Ask user to clarify

**Topic-to-slug conversion:**
- Lowercase the topic
- Replace spaces/special chars with hyphens
- Remove non-alphanumeric except hyphens
- Collapse multiple hyphens → single hyphen
- Trim leading/trailing hyphens
- **Max 80 chars** - truncate at word boundary if longer

**Multiple flags:** If multiple generation flags provided, use first one; remaining treated as topic.

**Placeholder `{topic}`:** Replaced with original user input in title case (not the slug).

## Error Handling

| Error | Action |
|-------|--------|
| Invalid topic (empty) | Ask user to provide a topic |
| Flag without topic | Ask user: "Please provide a topic: `/ck:preview --explain <topic>`" |
| Topic becomes empty after sanitization | Ask for topic with alphanumeric characters |
| File write failure | Report error, suggest checking permissions |
| Server startup failure | Check if port in use, try `/ck:preview --stop` first |
| No generation flag + unresolvable reference | Ask user to clarify which file they meant |
| Existing file at output path | Overwrite with new content (no prompt) |
| Server already running | Reuse existing server instance, just open new URL |
| Parent `plans/` dir missing | Create directories recursively before write |
