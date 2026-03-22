---
name: youmind
description: Use this skill when users need Youmind board operations via API (list/find/create boards, add links/files, chat, generate image/slides/docs, extract artifacts). Browser is only for auth bootstrap/refresh.
---

# Youmind API Skill (API-Only Runtime)

Use HTTP APIs for business operations. Do not use browser fallback for board/material/chat actions.

## Runtime Rules

- API-only for boards, materials, chat, and artifact extraction.
- Browser automation is only allowed for auth bootstrap/refresh (`auth_manager.py`).
- For board-scoped commands, prefer `--board-id`; `--board-url` is also supported in material/chat/artifact/wrapper commands.

## Authentication

```bash
python3 scripts/run.py auth_manager.py status
python3 scripts/run.py auth_manager.py validate
python3 scripts/run.py auth_manager.py setup
python3 scripts/run.py auth_manager.py reauth
python3 scripts/run.py auth_manager.py clear
```

## Board Commands

```bash
python3 scripts/run.py board_manager.py list

python3 scripts/run.py board_manager.py find --query "roadmap"

python3 scripts/run.py board_manager.py get --id <board-id>

python3 scripts/run.py board_manager.py create --name "My Board"
python3 scripts/run.py board_manager.py create --name "My Board" --prompt "Initialize this board for AI coding agent research"
```

## Material Commands

```bash
python3 scripts/run.py material_manager.py add-link --board-id <board-id> --url "https://example.com"
python3 scripts/run.py material_manager.py add-link --board-url "https://youmind.com/boards/<id>" --url "https://example.com"

python3 scripts/run.py material_manager.py upload-file --board-id <board-id> --file /path/to/file.pdf

python3 scripts/run.py material_manager.py get-snips --ids "<snip-id-1>,<snip-id-2>"

python3 scripts/run.py material_manager.py list-picks --board-id <board-id>
```

## Chat Commands

```bash
python3 scripts/run.py chat_manager.py create --board-id <board-id> --message "Summarize key ideas"

python3 scripts/run.py chat_manager.py send --board-id <board-id> --chat-id <chat-id> --message "Give next steps"

python3 scripts/run.py chat_manager.py history --board-id <board-id>
python3 scripts/run.py chat_manager.py detail --chat-id <chat-id>
python3 scripts/run.py chat_manager.py detail-by-origin --board-id <board-id>
python3 scripts/run.py chat_manager.py mark-read --chat-id <chat-id>

python3 scripts/run.py chat_manager.py generate-image --board-id <board-id> --prompt "Minimal blue AI poster"
python3 scripts/run.py chat_manager.py generate-slides --board-id <board-id> --prompt "6-page AI coding agent roadmap"
python3 scripts/run.py chat_manager.py create --board-id <board-id> --message "Write a 1-page product brief"
```

## Artifact Extraction

```bash
python3 scripts/run.py artifact_manager.py extract --chat-id <chat-id>
python3 scripts/run.py artifact_manager.py extract-latest --board-id <board-id>
python3 scripts/run.py artifact_manager.py extract-latest --board-url "https://youmind.com/boards/<id>"
python3 scripts/run.py artifact_manager.py extract --chat-id <chat-id> --include-raw-content
```

Extraction semantics:
- `image_generate`: returns image URLs and `media_ids`.
- `slides_generate`: returns per-slide image URLs and `media_ids` (no direct `.pptx` file URL currently).
- `write`: returns `page_id`, preview content, and optional raw doc content with `--include-raw-content`.

## Compatibility Wrapper

```bash
python3 scripts/run.py ask_question.py --board-id <board-id> --question "..."
python3 scripts/run.py ask_question.py --board-url "https://youmind.com/boards/<id>" --question "..."
python3 scripts/run.py ask_question.py --board-id <board-id> --chat-id <chat-id> --question "..."
```

## Local Data

Local auth state:

```text
data/
├── auth_info.json
└── browser_state/
    └── state.json
```

Do not commit `data/`.
