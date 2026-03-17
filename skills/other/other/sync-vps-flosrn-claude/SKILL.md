---
name: sync-vps
description: Sync repos between Mac and VPS (bidirectional via git). ALWAYS use when the user says "sync", "sync vps", "sync claude", "sync clawd", "sync gapila", "sync lasdelaroute", "push vps", "pull vps", or mentions syncing local and VPS code.
allowed-tools: Bash
---

<objective>
Sync repos between local Mac and VPS via git.
Push = commit local + push + pull on VPS. Pull = commit VPS + push + pull locally.
</objective>

<context>
| Repo | Local | VPS | Branch |
|------|-------|-----|--------|
| claude | ~/.claude/ | /root/.claude/ | main |
| clawd | ~/clawd/ | /root/.openclaw/workspace/ | master |
| gapila | ~/code/nextjs/gapila/ | /root/gapila/ | main |
| lasdelaroute | ~/code/nextjs/lasdelaroute/ | /root/lasdelaroute/ | main |
</context>

<quick_start>
Parse user intent, then run the matching command:

**All repos:**
- `~/.claude/scripts/sync-vps.sh` — push all
- `~/.claude/scripts/sync-vps.sh --pull` — pull all

**Single repo:**
- `~/.claude/scripts/sync-vps.sh claude` — push claude only
- `~/.claude/scripts/sync-vps.sh --pull clawd` — pull clawd only
- `~/.claude/scripts/sync-vps.sh gapila` — push gapila only
- `~/.claude/scripts/sync-vps.sh lasdelaroute` — push lasdelaroute only

**Multiple repos:**
- `~/.claude/scripts/sync-vps.sh claude clawd` — push claude + clawd

**Preview:**
- `~/.claude/scripts/sync-vps.sh --dry-run [--pull] [repo...]`

<intent_mapping>
- "sync" / "sync vps" / "sync all" → push all
- "sync claude" / "sync clawd" / "sync gapila" / "sync lasdelaroute" → push that repo
- "pull" / "pull vps" / "recupere" → `--pull`
- "push" / "envoie" → push (default)
- "dry run" / "preview" / "sans toucher" → `--dry-run`
</intent_mapping>
</quick_start>

<success_criteria>
- Script completes with "Sync complete!" message
- Each targeted repo shows committed/pushed/pulled status
</success_criteria>
