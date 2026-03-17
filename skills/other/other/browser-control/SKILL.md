---
name: browser-control
description: Control a dedicated browser in Claude Code using Playwright scripts. Use when the user asks to open web pages, inspect page structure, click/type/press actions, wait for UI state, or take screenshots in a reproducible automation flow.
---

# Browser Control (Claude Code)

Use bundled Playwright scripts for deterministic web automation.

## Prerequisites
- Python 3.10+
- `pip install playwright`
- `python -m playwright install chromium`

## Scripts
- `.claude/skills/browser-control/scripts/open_url.py`
- `.claude/skills/browser-control/scripts/snapshot_dom.py`
- `.claude/skills/browser-control/scripts/act_click_type.py`
- `.claude/skills/browser-control/scripts/wait_for.py`
- `.claude/skills/browser-control/scripts/screenshot.py`

## Recommended flow
1. Open target URL
2. Snapshot DOM candidates
3. Run click/type/press actions
4. Wait for selector/text state
5. Capture screenshot and report

## Commands

### Open URL
```bash
python3 .claude/skills/browser-control/scripts/open_url.py \
  --url "https://example.com" \
  --out outputs/browser/open.json
```

### Snapshot candidates
```bash
python3 .claude/skills/browser-control/scripts/snapshot_dom.py \
  --url "https://example.com" \
  --out outputs/browser/snapshot.json
```

### Actions (click/type/press)
```bash
python3 .claude/skills/browser-control/scripts/act_click_type.py \
  --url "https://example.com" \
  --actions '[{"type":"click","selector":"text=More information"}]' \
  --out outputs/browser/act.json
```

### Wait for UI state
```bash
python3 .claude/skills/browser-control/scripts/wait_for.py \
  --url "https://example.com" \
  --selector "h1" \
  --timeout-ms 10000 \
  --out outputs/browser/wait.json
```

### Screenshot
```bash
python3 .claude/skills/browser-control/scripts/screenshot.py \
  --url "https://example.com" \
  --image outputs/browser/page.png \
  --out outputs/browser/screenshot.json
```

## Token optimization tips

Each script call and its output consumes tokens. Minimize unnecessary steps:

1. **Skip DOM snapshot when URL pattern is known**
   - Search engines (Naver, Google) have predictable URL patterns. Build the URL directly instead of snapshotting + typing + pressing Enter.
   ```bash
   # BAD: 3 steps (snapshot → type/click/press → screenshot) = high token cost
   python3 .claude/skills/browser-control/scripts/snapshot_dom.py --url "https://www.naver.com" ...
   python3 .claude/skills/browser-control/scripts/act_click_type.py --url "https://www.naver.com" --actions '[...]' ...
   python3 .claude/skills/browser-control/scripts/screenshot.py --url "https://search.naver.com/..." ...

   # GOOD: 1 step = low token cost
   python3 .claude/skills/browser-control/scripts/screenshot.py \
     --url "https://search.naver.com/search.naver?query=%EC%98%A4%ED%94%88%ED%81%B4%EB%A1%9C" \
     --image outputs/browser/result.png \
     --out outputs/browser/screenshot.json
   ```

2. **Never Read the full snapshot JSON into context**
   - Snapshot JSON can be hundreds of lines. Filter with `jq` in Bash instead of using the Read tool.
   ```bash
   python3 .claude/skills/browser-control/scripts/snapshot_dom.py \
     --url "https://example.com" --out /dev/stdout \
     | jq '.items[] | select(.tag=="input")'
   ```

3. **Combine actions into a single call**
   - Use one `act_click_type.py` call with multiple actions array instead of calling the script multiple times.

4. **Screenshot only when needed**
   - If you only need text data (e.g. link URLs, page title), use `snapshot_dom.py` with `jq` filtering instead of a screenshot.

## Policy (read/write access control)

`browser-control/policy.yaml` controls domain access.

- `write_allowed_hosts`: only these hosts/subdomains are writable (deny by default for write)
- `read_blocked_hosts`: only these hosts/subdomains are blocked for read (all others readable)
- Conflict rule: deny wins
- Redirect rule: policy is checked for both requested URL and final redirected URL

Example `policy.yaml` (JSON-compatible YAML):
```json
{
  "write_allowed_hosts": ["docs.openclaw.ai", "github.com"],
  "read_blocked_hosts": ["facebook.com", "x.com"]
}
```

## Rules
- Prefer stable selectors (`data-testid`, explicit ids, role/text) over brittle nth-child selectors.
- Save every step output JSON for reproducibility.
- If an action fails, return the failing selector/action index clearly.
- Use `--headed` only for debugging; default headless for automation.
