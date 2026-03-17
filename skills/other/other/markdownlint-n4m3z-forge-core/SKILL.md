---
name: MarkdownLint
description: Format and lint a markdown document — backtick code references, fix bare URLs, check list formatting and heading hierarchy. USE WHEN a document needs formatting cleanup, code references are not backticked, markdown quality needs improvement, or lint markdown.
argument-hint: "[path to markdown file]"
---

# MarkdownLint

Format and lint a markdown document for consistent code formatting, proper list structure, heading hierarchy, and link hygiene. Reads a file, applies all rules, writes the corrected version after confirmation.

## Instructions

### Step 1: Read the target file

If an argument was provided, use it as the file path. Otherwise, ask which file to lint.

Check TLP before reading:
- GREEN/CLEAR: Read directly
- AMBER: Use `safe-read` via Bash
- RED: Refuse

### Step 2: Schema validation

If `mdschema` is installed, look for a `.mdschema` in the file's parent directory (for skills: `skills/.mdschema`, for agents: `agents/.mdschema`). If found, run:

```bash
mdschema check "<file>" --schema "<schema>"
```

Report any violations (missing frontmatter fields, heading level skips, depth exceeded). These are structural issues that formatting rules cannot auto-fix — present them to the user as findings.

If `mdschema` is not installed or no schema exists, skip this step silently.

### Step 3: Identify protected zones

Before applying any rules, identify zones that MUST NOT be modified:

| Zone | Detection | Action |
|------|-----------|--------|
| YAML frontmatter | Lines between opening `---` and closing `---` at file start | Skip entirely |
| Fenced code blocks | Lines between `` ``` `` or `~~~` fences | Skip entirely |
| Inline code | Text between single backticks | Skip entirely |
| Wikilinks | Text matching `[[...]]` | Preserve as-is — never backtick |
| Obsidian embeds | Lines starting with `![[` or `![` | Preserve |
| HTML blocks | `<tag>...</tag>` blocks | Skip entirely |
| Obsidian comments | `%% ... %%` blocks | Skip entirely |

Process only unprotected text spans.

### Step 4: Apply formatting rules

#### 3a: Backtick filenames

Any word ending in a code-associated extension:

`.md`, `.yaml`, `.yml`, `.json`, `.rs`, `.sh`, `.ts`, `.js`, `.toml`, `.base`, `.css`, `.html`, `.py`, `.go`, `.lua`, `.sql`, `.env`, `.tlp`, `.gitignore`, `.claudeignore`

Examples: CLAUDE.md becomes `CLAUDE.md`, config.yaml becomes `config.yaml`.

Skip if already backticked, inside a wikilink, or part of a URL path.

#### 3b: Backtick CLI commands and tool names

Recognized patterns:
- Known tools: `safe-read`, `safe-write`, `blind-metadata`, `obsidian-base`, `build-templates`, `surface`, `insight`, `reflect`, `ekctl`, `cargo`, `make`, `git`, `npm`, `shellcheck`, `jq`
- Command invocations with flags: words followed by `--flag` or `-f`
- Make targets: `make install`, `make test`, `make clean`
- Compound commands: `cargo build`, `cargo test`, `git commit`

Backtick the full command phrase, not individual words.

#### 3c: Backtick technical identifiers

| Pattern | Example | Rule |
|---------|---------|------|
| Effort/log tags | #log/effort/short | Backtick the full tag |
| TLP tags as references | #tlp/red | Backtick when discussed as a value (not when used as actual inline tag) |
| Environment variables | FORGE_MODULE_ROOT | Backtick ALL_CAPS_UNDERSCORE identifiers |
| Config keys in prose | user.root, shared.journal.daily | Backtick dot-separated paths |
| YAML keys referenced in prose | source_module:, description: | Backtick when referenced as field names |

Exceptions: Tags used as actual functional Obsidian tags — leave as-is. Env vars inside code blocks — skip.

#### 3d: Convert bare URLs

Bare URLs (`<https://...>` or plain `https://...` in text):

1. GitHub repo URL: use repo name — `[forge-tlp](https://github.com/user/forge-tlp)`
2. Well-known service: use service name — `[Obsidian](https://obsidian.md/)`
3. Other: infer title from URL path or use domain name
4. If WebFetch available and URL is public, fetch the page title

Never convert URLs already inside markdown links `[text](url)` or code blocks.

#### 3e: Fix list formatting

- Use `-` for unordered lists (Obsidian convention)
- Proper indentation for child items
- Blank line before and after list blocks (unless inside a callout)

#### 3f: Check heading hierarchy

- No skipped levels (e.g., `##` followed by `####`)
- Single `#` H1 at document start (after frontmatter)
- Flag but do not auto-fix if structure is ambiguous

### Step 5: Special syntax recognition

Do NOT lint these as errors:
- `#tlp/red`, `#tlp/amber`, `#tlp/green`, `#tlp/clear` — valid TLP structural markers
- `%% @todo ... %%`, `%% @fixme ... %%` — valid Obsidian annotation markers
- `![[embed]]` — valid Obsidian embed syntax
- `> [!callout]` — valid Obsidian callout syntax
- Dataview blocks (`dataview`, `dataviewjs`)

### Step 6: Confirm changes

Present a summary:
- Count of backticked items by category (filenames, commands, tags, env vars)
- Count of URLs converted
- List/heading fixes
- 2-3 representative before/after examples

Ask the user to confirm before writing.

### Step 7: Write the corrected file

- AMBER: use `safe-write write` via Bash
- GREEN/CLEAR: use Write tool directly
- Preserve all protected zones exactly

## Constraints

- Never modify YAML frontmatter content
- Never modify content inside fenced code blocks or inline code
- Never backtick text inside wikilinks
- Never convert wikilinks to markdown links or vice versa
- Never change semantic meaning — only formatting
- Never add backticks to regular English words (e.g., "base" as a noun, "draft" as a verb)
- Preserve all Obsidian-specific syntax
- After linting, suggest the WikiLink skill if the document could benefit from knowledge graph links
