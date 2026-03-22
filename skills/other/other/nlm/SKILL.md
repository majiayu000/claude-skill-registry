---
name: nlm
description: This skill should be used when the user asks to "create a notebook", "add source to notebook", "generate audio overview", "create podcast", "manage NotebookLM", "nlm", "add PDF to notebook", "list notebooks", "summarize sources", "generate study guide", "create FAQ", "briefing document", "chat with notebook", "generate outline", "research a topic", "deep research", or needs to interact with Google NotebookLM via the nlm CLI tool.
version: 0.2.0
user-invocable: false
---

# NotebookLM CLI (nlm)

Manage Google NotebookLM notebooks, sources, notes, and audio overviews via the `nlm` command-line tool.

**Requires:** `nlm` on PATH (`~/.local/bin/nlm` → `~/projects/nlm/nlm`)

**Check:** `command -v nlm || echo "MISSING: nlm CLI not installed"`

## Authentication

Before first use, authenticate with Google:

```bash
nlm auth login -all
```

This connects to Chrome via CDP (Chrome DevTools Protocol) to extract cookies from an active NotebookLM session. Credentials are stored in `~/.nlm/env`.

### Troubleshooting Authentication

If `nlm auth` fails with "no valid profiles found" or "SESSION_COOKIE_INVALID":

1. **Verify Chrome is running with remote debugging**:
   ```bash
   ps aux | grep -E "chrome.*remote-debugging-port=9400"
   ```

   If not running, Chrome needs to be started with `--remote-debugging-port=9400` flag.

2. **Test CDP connection**:
   ```bash
   curl http://localhost:9400/json/version
   ```

   Should return JSON with Chrome version info.

3. **Re-authenticate**:
   ```bash
   nlm auth login -debug -all
   ```

   This will show which profiles are checked and why authentication succeeds or fails.

4. **Verify authentication works**:
   ```bash
   nlm list
   ```

   Should list notebooks without errors.

**If authentication still fails**, you may need to:
- Log into notebooklm.google.com in Chrome manually
- Ensure Chrome profile has an active NotebookLM session
- Check `~/.nlm/env` file permissions

## Core Commands

### Notebook Management

```bash
# List all notebooks
nlm list

# Create a new notebook
nlm create “Research Notes”

# Delete a notebook
nlm rm <notebook-id>

# Get notebook analytics
nlm analytics <notebook-id>
```

### Source Management

Add sources from URLs, files, or stdin:

```bash
# Add URL source
nlm add <notebook-id> https://example.com/article

# Add PDF file
nlm add <notebook-id> document.pdf

# Add from stdin
echo “Some text content” | nlm add <notebook-id> -

# Add with specific MIME type
cat data.json | nlm add <notebook-id> - -mime=”application/json”

# Add YouTube video
nlm add <notebook-id> https://www.youtube.com/watch?v=VIDEO_ID

# List sources in notebook
nlm sources <notebook-id>

# Rename a source
nlm rename-source <source-id> “New Title”

# Remove a source
nlm rm-source <notebook-id> <source-id>

# Refresh source content
nlm refresh-source <source-id>
```

### Note Management

```bash
# List notes in notebook
nlm notes <notebook-id>

# Create new note
nlm new-note <notebook-id> “Note Title”

# Update note content
nlm update-note <notebook-id> <note-id> “New content” “New Title”

# Remove note
nlm rm-note <note-id>
```

### Audio Overviews

Generate AI podcast-style audio summaries:

```bash
# Create audio overview with instructions
nlm audio-create <notebook-id> “Focus on key themes and provide a professional summary”

# List audio overviews
nlm audio-list <notebook-id>

# Get audio overview status/content
nlm audio-get <notebook-id>

# Download audio file (requires --direct-rpc)
nlm audio-download <notebook-id> output.mp3 --direct-rpc

# Share audio (private)
nlm audio-share <notebook-id>

# Share audio (public)
nlm audio-share <notebook-id> --public

# Delete audio
nlm audio-rm <notebook-id>
```

### Video Overviews

| Command | Purpose |
|---------|---------|
| `video-create` | Create video overview |
| `video-list` | List video overviews |
| `video-download` | Download video (requires `--direct-rpc`) |

See `references/commands.md` for full syntax.

### Generation Commands

```bash
# Generate notebook guide (short summary)
nlm generate-guide <notebook-id>

# Generate comprehensive content outline
nlm generate-outline <notebook-id>

# Generate new content section
nlm generate-section <notebook-id>

# Free-form chat generation
nlm generate-chat <notebook-id> "What are the main themes?"

# Interactive chat session
nlm chat <notebook-id>

# Generate magic view synthesis from specific sources
nlm generate-magic <notebook-id> <source-id-1> <source-id-2>
```

### Content Transformation Commands

Transform sources into different formats. All commands take `<notebook-id> <source-id> [source-id...]`:

| Command | Purpose |
|---------|---------|
| `summarize` | Summarize content |
| `study-guide` | Key concepts + review questions |
| `faq` | Generate FAQ |
| `briefing-doc` | Professional briefing |
| `rephrase` / `expand` | Reword or elaborate |
| `critique` / `verify` | Critique or fact-check |
| `brainstorm` / `explain` | Ideate or simplify |
| `outline` / `toc` | Structured outline or TOC |
| `mindmap` / `timeline` | Visual mindmap or timeline |

See `references/commands.md` for full syntax and examples.

### Research Commands

Research topics and automatically import sources into a notebook:

```bash
# Research a topic and import sources to a notebook
nlm research "quantum computing advances" --notebook <notebook-id>

# Deep research mode for comprehensive investigation
nlm research "climate policy impacts" --notebook <notebook-id> --deep
```

The research command:
- Searches for relevant sources on the topic
- Automatically imports found sources into the specified notebook
- `--deep` mode performs more comprehensive research

### Batch Operations

Execute multiple commands in a single request: `nlm batch "cmd1" "cmd2" "cmd3"`

See `references/commands.md` for full syntax.

## Workflows

For detailed workflow recipes (research, study materials, content analysis, executive briefing, Readwise→NLM import), read `references/workflows.md`.

Quick start — automated research:

```bash
id=$(nlm create "Topic Research" | grep -o 'notebook [^ ]*' | cut -d' ' -f2)
nlm research "your topic" --notebook $id
nlm generate-chat $id "What are the key findings?"
```

## Troubleshooting

- **Auth errors**: Run `nlm auth` to re-authenticate
- **Debug mode**: Add `-debug` flag for detailed API interactions
- **Browser profile**: Use `--profile “Profile Name”` to specify browser profile

## Environment Variables

- `NLM_AUTH_TOKEN`: Authentication token (managed by auth command)
- `NLM_COOKIES`: Authentication cookies (managed by auth command)
- `NLM_BROWSER_PROFILE`: Chrome/Brave profile to use (default: “Default”)
