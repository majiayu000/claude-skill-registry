---
name: xiaohongshu-session-reader
description: Use this skill to read Xiaohongshu (小红书) via HTTP/API first with local logged-in Chrome cookies, and only use Playwright as fallback. Supports profile card extraction, note detail extraction, and conditional comment fallback when API is blocked.
---

# Xiaohongshu Session Reader

## Scope

- Reuse local Chrome logged-in session only.
- Prefer HTTP/API extraction for stability and speed.
- Use Playwright only when HTTP/API path is blocked (captcha / risk control).
- Support:
  - profile card titles (for 谁是卧底词组 collection)
  - note detail (title/desc/author)
  - comments when API permits; otherwise explicit fallback signal
- Do not forge identity, bypass captcha, or brute-force anti-bot checks.

## Prerequisite Check

Before extraction:

```bash
python3 --version
```

Fallback-only prerequisite:

```bash
codex mcp get playwright-ext
```

## Workflow

1. Run HTTP-first reader:

```bash
python3 <skill_dir>/scripts/xhs_http_reader.py \
  --url "<xhslink_or_xiaohongshu_url>" \
  --mode auto \
  --max-items 40 \
  --max-comments 20 \
  --pretty
```

2. If response has `fallback.required=false`, use returned data directly.
3. If response has `fallback.required=true`, switch to Playwright fallback:
   - profile: open profile page and read visible card titles.
   - note comments: open note detail and read comments from DOM snapshot.
4. Normalize four-word groups with `scripts/undercover_parser.py`.
5. Persist progress in `.cache/xhs_undercover_progress.json` for batch tasks.

## Block Handling Rules

- If HTTP returns captcha or risk code (for example `300011`), do not keep retrying aggressively.
- Degrade once to Playwright fallback and continue extraction.
- If Playwright also lands on captcha/login gate, request user to refresh local login session.
- Never claim detail/comments were obtained via HTTP when response marks fallback required.

## Output Contract

Use this structure:

```json
{
  "source": "<xhs link>",
  "captured_at": "YYYY-MM-DD",
  "groups": [
    { "id": 1, "words": ["词A", "词B", "词B", "词B"], "odd": "词A" }
  ]
}
```

If confidence is low, add `note` for manual verification.

## Resources

- HTTP-first reader: `scripts/xhs_http_reader.py`
- Cookie exporter (fallback tooling): `scripts/export_xhs_cookies.py`
- DOM fallback reference: `references/extraction-checklist.md`
- Group parser: `scripts/undercover_parser.py`
