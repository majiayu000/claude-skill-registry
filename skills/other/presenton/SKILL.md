---
name: presenton
description: "Generate AI-powered presentations locally using Presenton. Use when: (1) User asks to create a presentation or slideshow, (2) User wants to convert a document or prompt into slides, (3) User needs PPTX/PDF export with AI-generated content."
---

# Presenton — AI Presentation Generator

Presenton is an open-source, locally-run AI presentation generator. It creates professional slideshows from text prompts or uploaded documents, exports to PPTX and PDF, and exposes a built-in MCP server so agents can generate presentations programmatically.

## When to use

- Use case 1: When the user asks to generate a presentation or slideshow on any topic
- Use case 2: When you need to convert a document, report, or prompt into structured slides
- Use case 3: When the user wants to export a presentation as PPTX or PDF
- Use case 4: When building agent workflows that produce presentation outputs via MCP
- Use case 5: When the user wants AI-generated presentations that run entirely on their own device

## Required tools / APIs

- Docker (recommended) or Node.js LTS + Python 3.11 + uv for local dev
- One of: OpenAI API key, Google Gemini API key, Anthropic API key, or a local Ollama instance
- Optional image providers: DALL-E 3, Gemini Flash, Pexels, Pixabay, or ComfyUI

Install options:

```bash
# Docker (Linux/macOS) — recommended
docker run -it --name presenton \
  -p 5000:80 \
  -v "./app_data:/app_data" \
  ghcr.io/presenton/presenton:latest

# Docker (Windows PowerShell)
docker run -it --name presenton `
  -p 5000:80 `
  -v "${PWD}\app_data:/app_data" `
  ghcr.io/presenton/presenton:latest

# With OpenAI + DALL-E 3 (no UI key entry needed)
docker run -it --name presenton \
  -p 5000:80 \
  -e LLM="openai" \
  -e OPENAI_API_KEY="<your-key>" \
  -e IMAGE_PROVIDER="dall-e-3" \
  -e CAN_CHANGE_KEYS="false" \
  -v "./app_data:/app_data" \
  ghcr.io/presenton/presenton:latest
```

## Skills

### generate_presentation_via_api

Generate a presentation by sending a prompt to the Presenton REST API.

```bash
# Start Presenton first (see install above), then call the API
curl -fsS --max-time 60 \
  -X POST "http://localhost:5000/api/v1/ppt/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Introduction to Quantum Computing", "n_slides": 8}'

# The response includes a presentation ID; download PPTX with:
PPTX_PATH=$(curl -s "http://localhost:5000/api/v1/ppt/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Introduction to Quantum Computing", "n_slides": 8}' \
  | jq -r '.pptx_url')
curl -s "http://localhost:5000${PPTX_PATH}" -o presentation.pptx
```

**Node.js:**

```javascript
async function generatePresentation(prompt, nSlides = 8, baseUrl = 'http://localhost:5000') {
  const res = await fetch(`${baseUrl}/api/v1/ppt/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, n_slides: nSlides }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return await res.json(); // contains pptx_url and pdf_url
}

// Usage
// generatePresentation('Introduction to Quantum Computing', 10).then(console.log);
```

### generate_with_mcp

Use Presenton's built-in MCP server to generate presentations from an AI agent.

```bash
# Add Presenton MCP server to your agent config (e.g. Claude Desktop, Cursor)
# mcp.json entry:
cat <<'EOF'
{
  "mcpServers": {
    "presenton": {
      "url": "http://localhost:5000/mcp"
    }
  }
}
EOF
```

**Node.js:**

```javascript
// The MCP server exposes a generate_presentation tool.
// Call it via your MCP client library:
const result = await mcpClient.callTool('presenton', 'generate_presentation', {
  prompt: 'Climate Change: Causes and Solutions',
  n_slides: 10,
});
console.log(result); // { pptx_url, pdf_url }
```

### generate_with_custom_template

Upload an existing PPTX to create an on-brand template, then generate from it.

```bash
# Upload a template PPTX to extract theme/design
curl -fsS --max-time 30 \
  -X POST "http://localhost:5000/api/v1/ppt/upload-template" \
  -F "file=@my_template.pptx"

# Generate a new presentation using that template
curl -fsS --max-time 60 \
  -X POST "http://localhost:5000/api/v1/ppt/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Q3 Sales Report", "n_slides": 6, "template": "my_template"}'
```

**Node.js:**

```javascript
const { readFileSync } = require('fs');

async function uploadTemplate(filePath, baseUrl = 'http://localhost:5000') {
  const form = new FormData();
  form.append('file', new Blob([readFileSync(filePath)]), 'template.pptx');
  const res = await fetch(`${baseUrl}/api/v1/ppt/upload-template`, {
    method: 'POST',
    body: form,
  });
  if (!res.ok) throw new Error(`Upload failed: HTTP ${res.status}`);
  return await res.json();
}

// Usage
// uploadTemplate('./branding.pptx').then(console.log);
```

## Output format

- `pptx_url`: Path to download the generated PPTX file (string)
- `pdf_url`: Path to download the generated PDF file (string)
- Error shape: `{ detail: "<message>" }` — check Presenton logs for root cause

## Rate limits / Best practices

- Generation takes 15–60 seconds depending on the model and number of slides; use async handling
- Cache generated presentations by prompt hash to avoid redundant API calls
- Use `DISABLE_IMAGE_GENERATION=true` for faster, text-only output during development
- Prefer Pexels or Pixabay as image providers to avoid per-image AI costs
- Set `CAN_CHANGE_KEYS=false` in production to lock down credentials

## Agent prompt

```text
You have Presenton capability. When a user asks to create a presentation:

1. Confirm the topic and desired number of slides (default: 8)
2. Call POST http://localhost:5000/api/v1/ppt/generate with {"prompt": "<topic>", "n_slides": <n>}
3. Wait for the response (up to 60 seconds) and extract pptx_url and pdf_url
4. Offer the user download links for both PPTX and PDF
5. If a custom template is requested, upload it first via /api/v1/ppt/upload-template and include the template name in the generate request

Always check that Presenton is running at http://localhost:5000 before calling the API.
Report any HTTP errors with the status code and response body so the user can diagnose the issue.
```

## Troubleshooting

**Presenton container not starting:**
- Symptom: `docker run` exits immediately or port 5000 is unreachable
- Solution: Check `docker logs presenton` for errors; ensure port 5000 is free (`lsof -i :5000`)

**Generation times out:**
- Symptom: API call hangs beyond 60 seconds
- Solution: Verify the LLM API key is valid and the model is reachable; reduce `n_slides`; check container logs

**No images in slides:**
- Symptom: Slides are generated but contain no images
- Solution: Set `IMAGE_PROVIDER` and the matching API key environment variable; or set `DISABLE_IMAGE_GENERATION=true` to skip images

**MCP server not responding:**
- Symptom: Agent cannot connect to `http://localhost:5000/mcp`
- Solution: Confirm Presenton is running and the MCP endpoint is accessible; check firewall rules

## See also

- [../browser-automation-agent/SKILL.md](../browser-automation-agent/SKILL.md) — Automate the Presenton web UI when API access is not available
- [../pdf-manipulation/SKILL.md](../pdf-manipulation/SKILL.md) — Post-process exported PDFs
- [../static-assets-hosting/SKILL.md](../static-assets-hosting/SKILL.md) — Host generated presentations for sharing

---

## Notes

- Source: https://github.com/presenton/presenton
- License: Apache 2.0
- Skill file path: `skills/presenton/SKILL.md`
