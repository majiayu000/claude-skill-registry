---
name: upload
description: Use when uploading a Markdown note to Feishu, optionally applying public or copy/download permissions, or requesting JSON upload results for automation or the Obsidian plugin direct-share flow.
---

# obshare-cli upload

Upload one Markdown file to Feishu.

## Syntax

```bash
conda run -n obsd obshare-cli upload <file>
conda run -n obsd obshare-cli upload <file> --public --allow-copy --allow-download
conda run -n obsd obshare-cli --json upload <file>
```

## Examples

```bash
conda run -n obsd obshare-cli upload note.md
conda run -n obsd obshare-cli upload /path/to/note.md --public
conda run -n obsd obshare-cli upload note.md --allow-copy --allow-download
conda run -n obsd obshare-cli --json upload note.md
```

## Result

Successful output includes:

- Document title
- Document token
- Feishu URL
- Applied permission flags
- Upload time

## Notes

- Required config must be complete before upload.
- Upload history is saved to `~/.obshare/history.json`.
- `--json` is a global flag and must appear before `upload`.
- If you rely on Mermaid rendering through the companion plugin, configure the optional Obsidian bridge settings first.
- In `V0.2.0`, the Obsidian companion plugin calls this command as the backend for direct note sharing.
