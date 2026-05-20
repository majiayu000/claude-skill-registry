---
name: content-generation
description: AI-powered document, image, and flowchart generation. Use this skill when generating images with fal.ai, creating flowcharts/diagrams, generating Google Docs, creating client proposals, converting markdown to PDF, or summarizing content. Triggers on image generation, diagram creation, document generation, or content formatting requests.
---

# Content Generation

## Overview

Generate professional content including images, diagrams, documents, and summaries using AI-powered tools.

## Quick Decision Tree

```
What do you need?
│
├── Generate images
│   └── references/images.md
│   └── Script: scripts/generate_images.py
│
├── Create flowchart/diagram
│   └── references/flowchart.md
│   └── Script: scripts/generate_flowchart.py
│
├── Create Google Doc
│   └── references/document.md
│   └── Script: scripts/generate_document.py
│
├── Generate client proposal
│   └── references/proposal.md
│   └── Script: scripts/generate_proposal.py
│
├── Convert Markdown to PDF
│   └── references/pdf.md
│   └── Script: scripts/md_to_pdf.py
│
└── Summarize content
    └── references/summarize.md
    └── Script: scripts/summarize_content.py
```

## Environment Setup

```bash
# Required in .env
FAL_API_KEY=fal_xxxx              # For image generation
OPENROUTER_API_KEY=sk-or-v1-xxx   # For AI text generation
```

Get API keys:
- fal.ai: https://fal.ai/dashboard/keys
- OpenRouter: https://openrouter.ai/keys

## Common Usage

### Generate Images
```bash
# Nano Banana Pro (best quality)
python scripts/generate_images.py "Professional product photo of smartwatch" --model nano-banana-pro

# FLUX-2 (fast, cheap)
python scripts/generate_images.py "Vibrant lifestyle photo" --model flux-2 --size landscape_4_3
```

### Create Flowchart
```bash
python scripts/generate_flowchart.py "User login: enter email, validate, check password, if correct go to dashboard"
```

### Generate Document
```bash
python scripts/generate_document.py --input content.json --title "Q4 Report"
```

### Generate Proposal
```bash
python scripts/generate_proposal.py --transcript-file meeting.txt --client "Acme Corp"
```

## Cost Estimates

| Tool | Cost |
|------|------|
| Nano Banana Pro 1K | $0.15/image |
| Nano Banana Pro 4K | $0.30/image |
| FLUX-2 | $0.012/megapixel |
| Flowchart | ~$0.005/diagram |
| Proposal | ~$0.10/doc |

## Security Notes

### Credential Handling
- Store `FAL_API_KEY` in `.env` file (never commit to git)
- Store `OPENROUTER_API_KEY` in `.env` file (never commit to git)
- Regenerate keys from respective dashboards if compromised
- Never log or print API keys in script output

### Data Privacy
- Text prompts sent to fal.ai and OpenRouter servers
- Generated images stored locally in `.tmp/` directory
- AI services may log prompts for service improvement
- Avoid including sensitive/confidential data in prompts
- Generated documents may be uploaded to Google Drive

### Access Scopes
- `FAL_API_KEY` - Full access to image generation models
- `OPENROUTER_API_KEY` - Access to configured AI models
- Google OAuth - Required for Google Docs creation (see google-workspace skill)

### Compliance Considerations
- **AI Disclosure**: Consider disclosing AI-generated content where required
- **Image Rights**: Generated images subject to fal.ai terms of use
- **Copyright**: AI-generated content copyright varies by jurisdiction
- **Brand Consistency**: Review AI outputs against brand guidelines
- **Sensitive Content**: AI image generators have content policies
- **Client Proposals**: Verify accuracy before sending to clients
- **Attribution**: Some contexts require AI generation disclosure

## Troubleshooting

### Common Issues

#### Issue: Image generation failed
**Symptoms:** fal.ai returns error or no image generated
**Cause:** Invalid prompt, model unavailable, or API issue
**Solution:**
- Check prompt for policy violations (explicit content, etc.)
- Verify model ID is correct and available
- Try a simpler prompt to test API connectivity
- Check fal.ai status page for outages

#### Issue: Content policy violation
**Symptoms:** "Content policy violation" or similar safety error
**Cause:** Prompt contains flagged terms or concepts
**Solution:**
- Remove explicit, violent, or harmful content from prompt
- Rephrase ambiguous terms that might trigger filters
- Review fal.ai content policy guidelines
- Use more general/professional language

#### Issue: Google Doc not created
**Symptoms:** Script completes but no document appears in Drive
**Cause:** OAuth issue, folder permissions, or API error
**Solution:**
- Verify Google OAuth is working (see google-workspace skill)
- Check target folder exists and is accessible
- Delete `mycreds.txt` and re-authenticate
- Look for error messages in script output

#### Issue: Flowchart syntax error
**Symptoms:** Mermaid diagram fails to render
**Cause:** Invalid Mermaid syntax in generated diagram
**Solution:**
- Review generated Mermaid code for syntax errors
- Simplify complex flows into smaller diagrams
- Test diagram at https://mermaid.live/
- Ensure special characters are properly escaped

#### Issue: PDF conversion fails
**Symptoms:** Error during markdown to PDF conversion
**Cause:** Missing dependencies or invalid markdown
**Solution:**
- Ensure required PDF tools are installed (weasyprint, etc.)
- Check markdown syntax is valid
- Verify font files exist if custom fonts specified
- Try with simpler markdown to isolate issue

#### Issue: OpenRouter API error
**Symptoms:** Text generation fails with API error
**Cause:** Invalid API key, model unavailable, or rate limit
**Solution:**
- Verify `OPENROUTER_API_KEY` is set correctly
- Check model availability at OpenRouter dashboard
- Try a different model if current one is unavailable
- Review rate limit status and add delays if needed

## Resources

- **references/images.md** - fal.ai image generation
- **references/flowchart.md** - Mermaid diagram generation
- **references/document.md** - Google Docs creation
- **references/proposal.md** - Client proposal generation
- **references/pdf.md** - Markdown to PDF conversion
- **references/summarize.md** - Content summarization

## Integration Patterns

### Generate and Save
**Skills:** content-generation → google-workspace
**Use case:** Create documents and store in Drive
**Flow:**
1. Generate content (proposal, report, summary)
2. Format as Google Doc or PDF
3. Upload to appropriate Drive folder via google-workspace

### Proposal to CRM
**Skills:** content-generation → attio-crm
**Use case:** Link generated proposals to deal records
**Flow:**
1. Generate client proposal from meeting transcript
2. Upload proposal to Google Drive
3. Add note to Attio CRM company record with proposal link

### Images to Video
**Skills:** content-generation → video-production
**Use case:** Create title slides for video courses
**Flow:**
1. Generate branded title slide images for each lesson
2. Export images to video-compatible format
3. Use video-production to stitch with lesson videos
