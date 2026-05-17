#!/usr/bin/env bash
set -euo pipefail

# init-vault.sh — Scaffold an agent-ready Obsidian vault in the current directory.
# Usage: bash init-vault.sh [--force]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SCAFFOLD_DIR="$SKILL_DIR/scaffold"
PLUGIN_ROOT="$(dirname "$(dirname "$SKILL_DIR")")"
VAULT_DIR="$(pwd)"

FORCE=false
[[ "${1:-}" == "--force" ]] && FORCE=true

# Pre-flight
if [[ -f CLAUDE.md ]] && [[ "$FORCE" != true ]]; then
  echo "ERROR: CLAUDE.md already exists. Use --force to overwrite." >&2
  exit 1
fi

if ! command -v npx &>/dev/null; then
  echo "ERROR: npx not found. Install Node.js first." >&2
  exit 1
fi

echo "Scaffolding vault in: $VAULT_DIR"

# 1. Directory structure
mkdir -p notes templates assets Spaces Clippings temp
echo "  [1/8] Created directories"

# 2. Copy templates
cp -r "$SCAFFOLD_DIR/templates/"* templates/
echo "  [2/8] Copied templates"

# 3. Copy CLAUDE.md
cp "$SCAFFOLD_DIR/CLAUDE.md" ./CLAUDE.md
echo "  [3/8] Wrote CLAUDE.md"

# 4. Write .mcp.json with vault path
cp "$SCAFFOLD_DIR/mcp.json" ./.mcp.json
if [[ "$(uname)" == "Darwin" ]]; then
  sed -i '' "s|__VAULT_PATH__|$VAULT_DIR|g" .mcp.json
else
  sed -i "s|__VAULT_PATH__|$VAULT_DIR|g" .mcp.json
fi
echo "  [4/8] Wrote .mcp.json"

# 5. Copy hooks and write settings.json
mkdir -p .claude/hooks
cp "$PLUGIN_ROOT/hooks/"*.sh .claude/hooks/
chmod +x .claude/hooks/*.sh

# Preserve existing enabledPlugins if settings.json exists
cat > .claude/settings.json << 'SETTINGS'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-templates.sh",
            "statusMessage": "Checking templates protection..."
          }
        ]
      },
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-obsidian.sh",
            "statusMessage": "Checking .obsidian protection..."
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-frontmatter.sh",
            "statusMessage": "Validating frontmatter..."
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/on-compact.sh",
            "statusMessage": "Re-injecting vault context..."
          }
        ]
      }
    ]
  }
}
SETTINGS
echo "  [5/8] Set up hooks"

# 6. Write .gitignore
cat > .gitignore << 'GITIGNORE'
temp/
.claude/sessions/
.claude/settings.local.json
.obsidian/workspace.json
.obsidian/workspace
.obsidian/*conflicted*
.DS_Store
__pycache__
*.pyc
*.epub
*.bin
GITIGNORE
echo "  [6/8] Wrote .gitignore"

# 7. Create example notes
mkdir -p notes/example

cat > "notes/example/(Term) Spaced Repetition.md" << 'NOTE1'
---
id: "20260101000001"
created_date: 2026-01-01
updated_date: 2026-01-01
type: term
processing_status: processed
---

[ ](#anki-card)

# Spaced Repetition

- **Review at increasing intervals to fight the forgetting curve** — the core idea is that memory decays predictably, so you schedule reviews right before you'd forget
- Each successful recall strengthens the memory trace and pushes the next review further out
- The spacing effect was first documented by Ebbinghaus (1885) — retention drops ~50% within a day without review, but spaced practice flattens the curve
- Leitner system: cards move to higher boxes on correct recall, drop back on failure — a physical implementation of the algorithm
- Digital tools (Anki, SuperMemo) use SM-2 or similar algorithms to compute optimal intervals per card
- **Why it works**: retrieval practice during review is itself a learning event (testing effect), not just a measurement
- Connected to [[(Term) Desirable Difficulties]] — spacing makes recall harder in the moment, which paradoxically strengthens long-term retention

🏷️Tags: #term #learning #all-anki #01-2026
NOTE1

cat > "notes/example/(Post) Example Source Note.md" << 'NOTE2'
---
id: "20260101000002"
created_date: 2026-01-01
updated_date: 2026-01-01
type: post
link: https://example.com/article
processing_status: inbox
---

# Example Source Note

> This is a placeholder source note. Replace it with a real article, blog post, or any content you want to process.

## Notes
- This note has `processing_status: inbox` — it's waiting to be processed
- Run `/process` on this note to see the thinking pipeline in action
- The agent will ask you questions, suggest term extractions, and help you build connections

## Questions
- What concepts in this article deserve their own Term notes?
- How does this connect to things I already know?

## Related links
- [[(Term) Spaced Repetition]]

🏷️Tags: #post #01-2026
NOTE2

cat > "notes/example/(Thought) Cross-Domain Transfer.md" << 'NOTE3'
---
id: "20260101000003"
created_date: 2026-01-01
updated_date: 2026-01-01
type: thought
processing_status: processed
---

[ ](#anki-card)

# Cross-Domain Transfer

- **The most valuable insights come from connecting ideas across unrelated fields** — spaced repetition (learning) shares the same core principle as compound interest (finance): small consistent investments yield exponential returns over time
- Both rely on the same mathematical structure: exponential growth/decay curves with periodic reinforcement
- This pattern appears again in habit formation (psychology), network effects (startups), and even evolution (biology) — repeated small advantages compound
- The vault itself is a cross-domain transfer engine: by linking [[(Term) Spaced Repetition]] to finance and biology, you create retrieval paths that wouldn't exist in a single-domain notebook
- Implication: when learning something new, always ask "where have I seen this pattern before in a different domain?"

🏷️Tags: #thought #learning #01-2026
NOTE3
echo "  [7/8] Created example notes"

# 8. Init git
if [[ ! -d .git ]]; then
  git init -q
fi
git add -A
git commit -q -m "Initial vault setup via obsidian-vault-agent /init"
echo "  [8/8] Initialized git"

echo ""
echo "Done! Vault initialized at: $VAULT_DIR"
echo ""
echo "Next steps:"
echo "  1. Open this folder in Obsidian"
echo "  2. Enable Templates core plugin → set template folder to 'templates'"
echo "  3. Try: /process, /recall, /youtube, /research"
