---
name: baoyu-danger-x-to-markdown
description: Convert X (Twitter) tweet or article URL to markdown. Uses reverse-engineered X API (private). Requires user consent before use.
---

# X to Markdown

Converts X (Twitter) content to markdown format:
- Tweet threads → Markdown with YAML front matter
- X Articles → Full article content extraction

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | CLI entry point for URL conversion |

## ⚠️ Disclaimer (REQUIRED)

**Before using this skill**, the consent check MUST be performed.

### Consent Check Flow

**Step 1**: Check consent file

```bash
# macOS
cat ~/Library/Application\ Support/baoyu-skills/x-to-markdown/consent.json 2>/dev/null

# Linux
cat ~/.local/share/baoyu-skills/x-to-markdown/consent.json 2>/dev/null

# Windows (PowerShell)
Get-Content "$env:APPDATA\baoyu-skills\x-to-markdown\consent.json" 2>$null
```

**Step 2**: If consent exists and `accepted: true` with matching `disclaimerVersion: "1.0"`:

Print warning and proceed:
```
⚠️  Warning: Using reverse-engineered X API (not official). Accepted on: <acceptedAt date>
```

**Step 3**: If consent file doesn't exist or `disclaimerVersion` mismatch:

Display disclaimer and ask user:

```
⚠️  DISCLAIMER

This tool uses a reverse-engineered X (Twitter) API, NOT an official API.

Risks:
- May break without notice if X changes their API
- No official support or guarantees
- Account restrictions possible if API usage detected
- Use at your own risk

Do you accept these terms and wish to continue?
```

Use `AskUserQuestion` tool with options:
- **Yes, I accept** - Continue and save consent
- **No, I decline** - Exit immediately

**Step 4**: On acceptance, create consent file:

```bash
# macOS
mkdir -p ~/Library/Application\ Support/baoyu-skills/x-to-markdown
cat > ~/Library/Application\ Support/baoyu-skills/x-to-markdown/consent.json << 'EOF'
{
  "version": 1,
  "accepted": true,
  "acceptedAt": "<ISO timestamp>",
  "disclaimerVersion": "1.0"
}
EOF

# Linux
mkdir -p ~/.local/share/baoyu-skills/x-to-markdown
cat > ~/.local/share/baoyu-skills/x-to-markdown/consent.json << 'EOF'
{
  "version": 1,
  "accepted": true,
  "acceptedAt": "<ISO timestamp>",
  "disclaimerVersion": "1.0"
}
EOF
```

**Step 5**: On decline, output message and stop:
```
User declined the disclaimer. Exiting.
```

---

## Usage

```bash
# Convert tweet (outputs markdown path)
npx -y bun ${SKILL_DIR}/scripts/main.ts <url>

# Save to specific file
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> -o output.md

# JSON output
npx -y bun ${SKILL_DIR}/scripts/main.ts <url> --json
```

## Options

| Option | Description |
|--------|-------------|
| `<url>` | Tweet or article URL |
| `-o <path>` | Output path (file or dir) |
| `--json` | Output as JSON |
| `--login` | Refresh cookies only |

## File Structure

```
x-to-markdown/
└── {username}/
    └── {tweet-id}.md
```

## Supported URLs

- `https://x.com/<user>/status/<id>`
- `https://twitter.com/<user>/status/<id>`
- `https://x.com/i/article/<id>`

## Output Format

```markdown
---
url: https://x.com/username/status/123
author: "Display Name (@username)"
tweet_count: 3
---

Tweet content...

---

Thread continuation...
```

## Authentication

**Option 1**: Environment variables (recommended)
- `X_AUTH_TOKEN` - auth_token cookie
- `X_CT0` - ct0 cookie

**Option 2**: Chrome login (auto if env vars not set)
- First run opens Chrome for login
- Cookies cached locally

## Extension Support

Custom configurations via EXTEND.md.

**Check paths** (priority order):
1. `.baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md` (project)
2. `~/.baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md` (user)

If found, load before workflow. Extension content overrides defaults.
