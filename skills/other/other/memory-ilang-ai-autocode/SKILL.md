---
name: memory
description: "[MEM:persistent|path=.autocode/memory.md|load=start|save=stop|merge=cross-session]"
---
[STORE:.autocode/memory.md]
[FMT:sections]
## Project=[name|stack|key-files]
## Decisions=[DECISION]desc—date
## State=[DONE|WORKS|BROKEN]
## Next=[-[ ]-immediate-task]
## User=[PREFERS|BUILDS|MISTAKE]
[RULES]
max=200-lines|compress=aggressive|merge=dont-overwrite|dedup=keep-newest
date=everything|secrets=never(no-API-keys/passwords/tokens)|code=never(descriptions-only)
