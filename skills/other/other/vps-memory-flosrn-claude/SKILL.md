---
name: vps-memory
description: Access Flo's long-term memory on the VPS (OpenClaw). ALWAYS use when the user says "memory", "memories", "remember", "souviens-toi", "rappelle-toi", "save memory", "search memory", "VPS memory", "OpenClaw", or mentions saving/searching past sessions or knowledge.
allowed-tools: Bash
---

<objective>
Search or save memories on the VPS via OpenClaw's memory system.
</objective>

<context>
Flo's long-term memory lives on the VPS at `~/.openclaw/workspace/`.

**NEVER edit MEMORY.md** — it's curated by OpenClaw. Always create new files in `memory/`.

### Key paths on VPS
- MEMORY.md (curated, READ-ONLY): `/root/.openclaw/workspace/MEMORY.md`
- Session memories (CREATE HERE): `/root/.openclaw/workspace/memory/`
- SQLite index: `/root/.openclaw/memory/main.sqlite`
</context>

<quick_start>
Parse user intent, then run the matching command:

**Search memories:**
```bash
ssh vps 'cd /root/openclaw && docker compose exec openclaw-gateway node dist/index.js memory search "QUERY"'
```

**Save a new memory:**
```bash
ssh vps 'cat > /root/.openclaw/workspace/memory/YYYY-MM-DD-topic.md << '\''EOF'\''
# Session: YYYY-MM-DD (via Claude Code local)
## Topic
Content here

**Tags:** relevant, tags, here
EOF'
```
Then reindex:
```bash
ssh vps 'cd /root/openclaw && docker compose exec openclaw-gateway node dist/index.js memory index'
```

<intent_mapping>
- "search memory" / "cherche dans ma mémoire" / "tu te souviens" → search
- "save memory" / "retiens ça" / "souviens-toi" / "note ça" → save + reindex
- "show memories" / "list memories" → search with broad query
</intent_mapping>
</quick_start>

<success_criteria>
- Search: returns relevant memory results
- Save: file created on VPS + reindex completed successfully
</success_criteria>
