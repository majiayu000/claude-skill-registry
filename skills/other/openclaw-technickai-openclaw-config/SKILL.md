---
name: openclaw
version: 0.2.2
description: Install, configure, and update openclaw-config
triggers:
  - openclaw
  - openclaw-config
  - set up openclaw
  - update openclaw
metadata:
  openclaw:
    emoji: "🐾"
---

# OpenClaw Config Skill 🐾

Manages your openclaw-config installation.

**Users say things like:**

- "Set up openclaw-config"
- "Update my openclaw config"
- "Force update openclaw" (overwrites their changes)
- "Check if openclaw has updates"

---

# Setup

Do these steps in order:

1. **Clone repo** to `~/.openclaw-config`

2. **Copy templates** to workspace root (don't overwrite existing): AGENTS.md, SOUL.md,
   USER.md, TOOLS.md, HEARTBEAT.md, IDENTITY.md

3. **Create memory folders:** `memory/people`, `memory/projects`, `memory/topics`,
   `memory/decisions`

4. **Copy skills** to `skills/`

5. **Optional: Add workflows** — Ask if they want any workflows:
   - "Do you want the email steward workflow?" → Manages inbox automatically

   If yes:
   - Copy `AGENT.md` from `~/.openclaw-config/workflows/email-steward/` to
     `workflows/email-steward/`
   - Create `workflows/email-steward/logs/` directory
   - The workflow will interview them on first run to create `rules.md`

6. **Configure memory search** — Required for semantic search to work. Ask: LM Studio
   (local, free, recommended) or OpenAI?
   - **LM Studio:** Server on port 1234, model
     `lmstudio-community/embedding-gemma-300m-qat`, configure gateway
     memorySearch.remote.baseUrl to `http://127.0.0.1:1234/v1`
   - **OpenAI:** Get their API key, configure gateway memorySearch.remote.baseUrl to
     `https://api.openai.com/v1`, model `text-embedding-3-small`
   - **Verify it works:** Create test file in memory/, index it, search for it, confirm
     it returns results, clean up

7. **Personalization** — Ask and replace in templates: `{{USER_NAME}}`,
   `{{ASSISTANT_NAME}}`, `{{TIMEZONE}}`, `{{PRIORITY_1}}`, `{{PRIORITY_2}}`

8. **Optional skills** — These are optional. Ask about each one individually, only
   configure if they say yes:
   - "Do you have a Limitless Pendant?" → If yes, get API key from app.limitless.ai →
     Settings → Developer
   - "Do you use Fireflies.ai for meeting transcripts?" → If yes, get API key from
     app.fireflies.ai → Integrations → Fireflies API
   - "Do you use Quo for business phone?" → If yes, get API key from my.quo.com →
     Settings → API
   - "Do you want Parallel.ai for web search? (better results than built-in)" → If yes,
     get API key from platform.parallel.ai

   Skip any they don't use. Don't assume they want all of them.

9. **Health check setup** — Ask: "Do you want automated health monitoring? It runs
   hourly via cron (Claude Code + Sonnet) to check your gateway and services, fix minor
   issues, and notify you of problems."

   If yes:
   - Ask: "Who should be notified if there's a problem?" → `mkdir -p ~/.openclaw` then
     write their answer to `~/.openclaw/health-check-admin` (just the name, one line)
   - Resolve the claude CLI path with `which claude` — use the full path in the cron job
   - Install the cron job (substitute CLAUDE_PATH with the resolved path):
     ```
     0 0,7-23 * * * test -f "$HOME/.openclaw-config/devops/health-check.md" && flock -n "$HOME/.openclaw/health-check.lock" CLAUDE_PATH -p "Run health check" --model sonnet --append-system-prompt-file "$HOME/.openclaw-config/devops/health-check.md" --dangerously-skip-permissions --max-budget-usd 5.00 >> "$HOME/.openclaw/health-check.log" 2>&1
     ```
   - Verify: `crontab -l | grep health-check`
   - Do a test run: execute the claude command once and verify it produces output
   - Tell them: runs hourly 7 AM–midnight, logs at `~/.openclaw/health-check.log`

10. **Track version** in `.openclaw/installed-version`

11. **Summary** — Tell them what's configured

---

# Update

Compare `.openclaw/installed-version` with `~/.openclaw-config/VERSION`.

If newer: pull, update skills (safe to overwrite), update templates only if user hasn't
modified them, update version file, report changes.

If user wants to force/overwrite: backup to `.openclaw/backup/` first.

**Workflows:** Only update AGENT.md (the algorithm). Never touch rules.md,
agent_notes.md, or logs/ — those belong to the user.

---

# Status

Show installed version and skill versions. Fetch remote VERSION, report if updates
available.
