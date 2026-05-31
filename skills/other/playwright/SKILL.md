---
name: playwright
description: "Navigate websites and query page content using Playwright CLI. Use this skill when the user asks to open a URL, extract data from a page, or check UI state."
allowed-tools: Bash(npx playwright*), Bash(node -e*)
---

Download the rendered HTML instead of PDF or screenshots. Use the Playwright CLI:

```bash
npx playwright open --save-har=/tmp/page.har --save-har-glob="**" <url> --headless
```

Or more directly, dump the fully rendered DOM:

```bash
node -e "const{chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto(process.argv[1],{waitUntil:'networkidle'});console.log(await p.content());await b.close()})();" <url> > /tmp/page.html
```

Then read `/tmp/page.html` to analyze the page content.
