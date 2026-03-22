---
name: browser
description: Real browser automation — screenshot, scrape, full page content, PDF, form fill via Chromium
user-invocable: true
---

# Browser Skill — arifOS_bot

Triggers: "open browser", "screenshot", "take a screenshot", "scrape page", "get page content",
          "fill form", "navigate to", "render page", "save as pdf", "web automation",
          "click on", "browser automation", "full page", "visit"

Browser: **Browserless Chromium 145** at `http://headless_browser:3000`
Protocol: REST API (POST JSON) + OpenClaw native `browser` tool

---

## Method 1 — OpenClaw Native Browser Tool

Use for interactive navigation, clicking, form-filling.
OpenClaw's `browser` tool is wired to `BROWSERLESS_URL=http://headless_browser:3000`.

```
# In OpenClaw tool call:
browser: navigate to https://example.com
browser: click on "Submit" button
browser: fill input[name=email] with "arif@example.com"
browser: get page text
browser: take screenshot
```

---

## Method 2 — Direct Browserless REST API

Use for precise control, bulk operations, or when native tool isn't enough.

### Screenshot
```bash
# Full page screenshot → save PNG
curl -s -X POST http://headless_browser:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://YOURURL.com",
    "options": {
      "fullPage": true,
      "type": "png"
    }
  }' -o ~/.openclaw/workspace/logs/screenshot_$(date +%s).png

echo "Saved to workspace/logs/"
```

### Get Full Page Content (Markdown-friendly HTML)
```bash
curl -s -X POST http://headless_browser:3000/content \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://YOURURL.com",
    "rejectResourceTypes": ["image","font","stylesheet"],
    "waitForSelector": "body"
  }' | head -200
```

### Scrape Specific Elements
```bash
# Extract structured data from page
curl -s -X POST http://headless_browser:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://YOURURL.com",
    "elements": [
      {"selector": "h1"},
      {"selector": ".price"},
      {"selector": "table tr"},
      {"selector": "article p"}
    ]
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
for block in data['data']:
    print(f\"=== {block['selector']} ===\")
    for r in block['results'][:5]:
        print(r['text'])
"
```

### Save Page as PDF
```bash
curl -s -X POST http://headless_browser:3000/pdf \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://YOURURL.com",
    "options": {
      "printBackground": true,
      "format": "A4",
      "margin": {"top":"20px","bottom":"20px","left":"20px","right":"20px"}
    }
  }' -o ~/.openclaw/workspace/logs/page_$(date +%s).pdf
echo "PDF saved"
```

### Execute Custom JavaScript on Page
```bash
curl -s -X POST http://headless_browser:3000/function \
  -H "Content-Type: application/json" \
  -d '{
    "code": "module.exports = async ({ page }) => {
      await page.goto(\"https://YOURURL.com\");
      const title = await page.title();
      const links = await page.$$eval(\"a\", els => els.map(e => ({text: e.textContent.trim(), href: e.href})).filter(l => l.text).slice(0, 20));
      return { title, links };
    }"
  }' | python3 -m json.tool
```

---

## Common Use Cases

### Check if a site is up + get title
```bash
curl -s -X POST http://headless_browser:3000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://TARGET.com","elements":[{"selector":"title"},{"selector":"h1"}]}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); [print(b['selector'],':', b['results'][0]['text'] if b['results'] else 'empty') for b in d['data']]"
```

### Monitor your own VPS domains
```bash
for DOMAIN in arifosmcp.arif-fazil.com claw.arifosmcp.arif-fazil.com flow.arifosmcp.arif-fazil.com; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://${DOMAIN}" --max-time 5)
  echo "${DOMAIN}: HTTP ${STATUS}"
done
```

### Login form automation (use with F13 awareness)
```bash
# F11: Credential handling → state intent, get Arif confirmation
curl -s -X POST http://headless_browser:3000/function \
  -H "Content-Type: application/json" \
  -d '{
    "code": "module.exports = async ({ page }) => {
      await page.goto(\"https://app.example.com/login\");
      await page.type(\"input[name=email]\", process.env.LOGIN_EMAIL);
      await page.type(\"input[name=password]\", process.env.LOGIN_PASS);
      await page.click(\"button[type=submit]\");
      await page.waitForNavigation();
      return { url: page.url(), title: await page.title() };
    }"
  }'
```

### Screenshot your VPS services dashboard
```bash
curl -s -X POST http://headless_browser:3000/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url":"http://arifos_grafana:3000","options":{"fullPage":true}}' \
  -o ~/.openclaw/workspace/logs/grafana_$(date +%Y%m%d).png
```

---

## Notes

- No TOKEN required (internal Docker network only)
- `headless_browser:3000` is accessible from openclaw container via `arifos_trinity` network
- For public URLs: container has full internet access
- Output files: save to `~/.openclaw/workspace/logs/` for git tracking
- For large scrapes: use `rejectResourceTypes: ["image","font","media"]` to speed up

*arifOS_bot — Chromium 145, Browserless REST API*
