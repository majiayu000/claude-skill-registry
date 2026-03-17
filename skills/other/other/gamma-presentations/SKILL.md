---
name: "Gamma Presentations Skill"
description: "Generate professional presentations using the Gamma API with expert storytelling consulting based on Duarte methodology."
applyTo: "**/*presentation*,**/*slides*,**/*deck*,**/*gamma*,**/*pitch*"
---

# Gamma Presentations Skill

> Generate professional presentations with expert storytelling consulting based on Duarte methodology.

> ⚠️ **Staleness Watch** (Last validated: Feb 2026 — API v0.2): Gamma is a SaaS product that ships new features and content types frequently. Check [gamma.app/api](https://gamma.app/api) for endpoint changes, new `contentType` values, credit pricing, and theme updates before advising on API calls.

Gamma is an AI-powered platform with 50M+ users for creating presentations, documents, social posts, and websites. This skill enables Alex to generate polished content programmatically **with professional presentation consulting**.

## Presentation Consulting Methodology

Alex uses the **Duarte methodology** — the industry-leading approach used by Nancy Duarte for Apple, Al Gore, and Fortune 500 companies.

### The 7 Principles of Expert Presentation Design

#### 1. The Hero's Journey Structure
Every presentation follows story structure:
- **Beginning**: Establish the current state ("what is")
- **Middle**: Contrast with the vision ("what could be") 
- **End**: Call to action and "new bliss" (attainable future)

#### 2. Audience as Hero, Presenter as Mentor
- The **audience** is the hero facing a challenge
- The **presenter** (or content) is the mentor providing tools to overcome it
- Position solutions as enabling the audience's success, not showcasing the presenter

#### 3. The Presentation Sparkline™
Alternate between "what is" and "what could be" throughout:
```
What is → What could be → What is → What could be → NEW BLISS
```
This contrast keeps audiences engaged (unlike flat reports or pure pitches).

#### 4. S.T.A.R. Moments™
Include "Something They'll Always Remember":
- Dramatic demonstrations
- Unexpected comparisons (like Steve Jobs sliding MacBook Air into envelope)
- Emotional stories that crystallize the message

#### 5. Data Storytelling
Transform data into meaning:
- **Humanize**: Make numbers relatable to individuals
- **Compare**: Use unexpected units of measurement
- **Surprise**: Lead with insight, not just charts

#### 6. Visual Hierarchy
- One idea per slide (rule of one)
- Clear title that states the insight (not just topic)
- 5-7 bullets maximum per slide
- Use whitespace strategically

#### 7. The New Bliss
End with a clear vision of the attainable future:
- What does success look like for the audience?
- How will their world be better?
- Concrete, achievable, inspiring

---

## Alex Consulting Workflow

When a user provides plain text or rough content, Alex follows this **consulting process**:

### Phase 1: Discovery
Alex analyzes the content and asks clarifying questions:
- Who is the audience? (executives, developers, investors, etc.)
- What is the goal? (inform, persuade, inspire, teach)
- What is the single most important takeaway?
- Are there emotional stories or data points to highlight?

### Phase 2: Concept Presentation
Alex presents a **narrative storyboard**:
```
📊 PRESENTATION CONCEPT

Title: [Compelling title framed as benefit to audience]
Subtitle: [Supporting context]

NARRATIVE ARC:
┌─────────────────────────────────────────────────┐
│ HOOK: [Opening that establishes stakes]        │
│ PROBLEM: [What is - current pain/challenge]    │
│ VISION: [What could be - better future]        │
│ SOLUTION: [How to get there - your offering]   │
│ PROOF: [Evidence, data, stories]               │
│ CALL TO ACTION: [Clear next step]              │
│ NEW BLISS: [Vision of success achieved]        │
└─────────────────────────────────────────────────┘

PROPOSED SLIDE STRUCTURE (10 slides):
1. Title slide with hook subtitle
2. The challenge your audience faces
3. Why this matters now
4. Section: The Vision [section divider]
5. What success looks like
6. The path forward
7. Proof point 1: [data/story]
8. Section: Taking Action [section divider]  
9. Key recommendations
10. Call to action + New Bliss

S.T.A.R. MOMENT: [Proposed memorable element]
```

### Phase 3: User Feedback
User refines the concept:
- "Add more data on slide 7"
- "Make the call to action stronger"
- "I want to emphasize X instead of Y"

### Phase 4: Structured Markdown Creation
Alex generates the **full structured markdown** for approval:

```markdown
# [Title]

## [Subtitle]

> [Speaker notes for opening]

---

# [Slide 2 Title]

- Bullet with **bold** for emphasis
- Another key point
- Third supporting point

> [Speaker notes with talking points]

---

## [Section Name] [section]

---
```

### Phase 5: User Approval
User reviews the markdown:
- Make inline edits if needed
- Request changes to specific slides
- Approve for generation

### Phase 6: Generation
Alex converts approved markdown to PPTX with:
- Alex brand colors and typography
- Proper slide layouts per the Duarte principles
- Speaker notes preserved
- Illustrations as specified

---

## Illustrations and Visual Elements

Alex supports multiple types of illustrations in presentations.

### Illustration Syntax

Use markdown image syntax with type prefixes:

| Syntax | Description | Example |
|--------|-------------|---------|
| `![icon:name]` | Lucide vector icon | `![icon:chart-bar]` |
| `![icon:name#color]` | Icon with hex color | `![icon:lightbulb#0550ae]` |
| `![stock:name]` | Stock business illustration | `![stock:collaboration]` |
| `![svg:path]` | Explicit SVG file path | `![svg:./assets/diagram.svg]` |
| `![logo:name]` | Auto-resolve from logos/ folder (PNG, JPG, SVG) | `![logo:acme]` |
| `![ticker:SYMBOL]` | Company logo by stock ticker (via API) | `![ticker:AAPL]` |
| `![image:path]` | Explicit image file path | `![image:./images/photo.png]` |

### Company Logos

#### Local Logo Collection (PNG, JPG, SVG)

Place your company logos in a `logos/` folder (configurable via `alex.logos.folder` setting):

```
workspace/
├── logos/
│   ├── acme.png        # PNG logos supported
│   ├── partner-a.jpg   # JPG logos supported  
│   ├── microsoft.svg   # SVG logos supported
│   └── google.webp     # WebP logos supported
└── presentation.md
```

Reference by name (Alex auto-detects format):
```markdown
# Our Partners

![logo:acme]
![logo:partner-a]
![logo:microsoft]

- Partner A brings expertise in...
```

#### Ticker-Based Logo API

Fetch company logos by stock ticker symbol (requires API key in settings):

```markdown
# Tech Giants Comparison

![ticker:AAPL]
![ticker:MSFT]  
![ticker:GOOGL]

| Company | Market Cap | Revenue |
|---------|-----------|---------|
| Apple | $3.0T | $394B |
| Microsoft | $2.8T | $211B |
| Google | $1.9T | $307B |
```

**Setup:**
1. Get a free API key from [Brandfetch](https://brandfetch.com) (no attribution required) or [Logo.dev](https://logo.dev) (500K/mo free)
2. Add to VS Code settings: `alex.logos.brandfetchClientId` or `alex.logos.logoDevToken`

### Available Icons

**Business & Charts**: `chart-bar`, `chart-line`, `chart-pie`, `trending-up`, `trending-down`, `target`, `trophy`, `briefcase`, `building`, `wallet`

**People & Teams**: `users`, `user`, `user-check`, `handshake`

**Technology**: `cpu`, `database`, `server`, `cloud`, `globe`, `code`, `terminal`, `wifi`, `brain`, `sparkles`

**Communication**: `mail`, `message-circle`, `phone`, `share`, `video`, `presentation`

**Actions & Status**: `check`, `check-circle`, `x`, `x-circle`, `plus`, `minus`, `alert-triangle`, `info`, `help-circle`

**Objects & Concepts**: `lightbulb`, `book`, `calendar`, `clock`, `file`, `file-text`, `folder`, `star`, `heart`, `lock`, `unlock`, `shield`, `zap`, `rocket`

**Arrows & Navigation**: `arrow-right`, `arrow-left`, `arrow-up`, `arrow-down`, `chevron-right`, `chevron-left`, `external-link`, `refresh`

### Available Stock Illustrations

| Name | Description |
|------|-------------|
| `collaboration` | Three connected circles representing teamwork |
| `growth` | Bar chart with upward trend line |
| `innovation` | Lightbulb with connected nodes |
| `process` | Three-step workflow with arrows |
| `security` | Shield with checkmark |
| `network` | Hub-and-spoke network diagram |
| `analytics` | Line chart with data points |
| `timeline` | Horizontal timeline with milestones |

### Example: Slide with Illustrations

```markdown
# Why Choose Us

## Key Differentiators

![icon:trophy#1a7f37]

- Industry-leading performance
- Enterprise-grade security
- 24/7 expert support

![stock:security]

> Emphasize the security certification in the demo
```

---

## Consulting Prompts

Use these prompts to engage Alex as a presentation consultant:

### Full Consulting Workflow
```
"Help me create a presentation about [topic]. 
I want to present to [audience] to [goal].
Here's my rough content: [paste content or file path]"
```

### Concept Review
```
"Review my presentation concept and suggest improvements:
[paste existing content]"
```

### Storyboard Request
```
"Create a storyboard for a presentation on [topic].
Audience: [who]
Goal: [what you want them to do/feel/know]
Key message: [single takeaway]"
```

### S.T.A.R. Moment Ideation
```
"What would be a memorable S.T.A.R. moment for a presentation about [topic]?
I want the audience to remember [key insight]."
```

---

## When to Use

- User asks to create a presentation or slide deck
- Need to generate a document or report
- Creating social media content (carousels, stories)
- Building simple webpages from content
- Converting notes or outlines into polished presentations

## Prerequisites

- Gamma account (Pro, Ultra, Teams, or Business plan for API access)
- API key from [gamma.app/settings](https://gamma.app/settings)
- Environment variable: `GAMMA_API_KEY`

---

## Help & User Manual

### How to Ask Alex to Create Gamma Content

Simply tell Alex what you want to create. **Alex will write the actual content for you**, then generate the presentation.

#### From a Topic (Alex writes all content)

```text
"Create a 10-slide presentation about machine learning for executives"
"Make a pitch deck for my startup idea: [description]"
"Generate a social media carousel about productivity tips"
```

**What Alex does:**
1. Creates a detailed markdown file with real slide content
2. Sends it to Gamma API for professional formatting
3. Returns the link and/or downloads the file
4. Opens it automatically if requested

#### From Your Own Content File

```text
"Create a presentation from README.md"
"Turn my CHANGELOG.md into a 15-slide deck"
"Make a document from .github/skills/cognitive-architecture/SKILL.md"
```

#### From Reference Documents

```text
"Create a presentation about appropriate reliance using all the documents in the article folder"
"Make a pitch deck from my business plan - use investor-deck.md and financials.md"
```

**Alex will:**
1. Read and synthesize the referenced files
2. Write presentation content based on that material
3. Generate the formatted presentation

#### With Specific Options

```text
"Create a presentation from my-notes.md with 12 slides, professional tone, for investors"
"Generate a webpage from PROJECT.md in Portuguese"
"Make an Instagram carousel (4x5) from tips.txt with vibrant AI images"
```

### Command Quick Reference

| What You Say | What Happens |
|--------------|--------------|
| "Create a presentation about X" | Alex writes content, then generates slides |
| "Create a presentation from FILE" | Reads file, converts to slides |
| "Create presentation using [files]" | Alex synthesizes files into slides |
| "Make a document from FILE" | Creates paginated document |
| "Generate a social post from X" | Creates carousel/story format |
| "Create a webpage from FILE" | Generates simple website |

### Available Options

When asking Alex to create Gamma content, you can specify:

| Option | Values | Example |
|--------|--------|---------|
| **Format** | presentation, document, social, webpage | "as a document" |
| **Slides/Cards** | 1-75 | "with 12 slides" |
| **Tone** | any description | "professional and confident" |
| **Audience** | any description | "for investors" |
| **Language** | 60+ languages | "in Spanish" |
| **Dimensions** | 16x9, 4x3, 1x1, 4x5, 9x16, letter, a4 | "in 16x9 format" |
| **Images** | AI, Unsplash, no images | "with AI-generated images" |
| **Export** | pptx, pdf | "export as PowerPoint" |
| **Illustrations only** | | "use only illustrations" (no photos) |

### Step-by-Step: Create from a Workspace File

1. **Tell Alex the file path:**
   > "Create a presentation from README.md"

2. **Alex reads the file** and sends content to Gamma API

3. **Alex polls for completion** (usually 15-60 seconds)

4. **Alex returns the link:** `https://gamma.app/docs/xxxxx`

5. **Open the link** to view, edit, or download your presentation

### Customization Examples

**Basic:**
> "Create a presentation from README.md"

**With slide count:**
> "Create a 15-slide presentation from README.md"

**With audience:**
> "Create a presentation from README.md for new developers, friendly tone"

**With export:**
> "Create a presentation from ROADMAP.md and export as PowerPoint"

**Full customization:**
> "Create a 12-slide pitch deck from my-startup.md in 16x9 format, confident tone, for VCs, with modern AI images, export as PDF and PowerPoint"

### What Alex Does Behind the Scenes

1. Reads the specified file from your workspace
2. Sends to Gamma API with your options:
   - `textMode: "generate"` (expands brief content) or `"condense"` (summarizes long content)
   - `format`, `numCards`, `textOptions`, `imageOptions` based on your request
3. Polls generation status every 2-3 seconds
4. Returns the Gamma URL when complete
5. Downloads export (PPTX/PDF) if requested
6. **Auto-opens** the file if `--open` flag is used
7. Reports credits used and remaining balance

### Pro Tips for Great Results

#### 1. Structure Your Content with Slide Markers

Use clear headers in your markdown — they become natural slide breaks:

```markdown
## Slide 1: Title
Main message here

## Slide 2: The Problem
- Pain point 1
- Pain point 2

## Slide 3: Our Solution
Description of solution
```

#### 2. Use Illustrations for Professional Decks

Specify `--image-style` with "illustrations" for consistent, modern look:

```bash
--image-model ideogram --image-style "modern clean illustrations, abstract concepts"
```

#### 3. Match Tone to Audience

| Audience | Suggested Tone |
|----------|----------------|
| Executives | "professional and concise" |
| Researchers | "intellectual and evidence-based" |
| Developers | "technical and practical" |
| Investors | "confident and visionary" |
| General | "friendly and accessible" |

#### 4. One Command, Open Result

Always use `--open` to immediately review your deck:

```bash
node .github/muscles/gamma-generator.js -f content.md -e pptx --open
```

#### 5. Iterate with Cost-Effective Models

Use cheaper models while iterating, premium for final:

```bash
# Drafts (2 credits/image)
--image-model flux-quick

# Final version (20 credits/image)
--image-model ideogram
```

### Cost Awareness

Alex will inform you of credit usage after each generation:

| Complexity | Estimated Credits |
|------------|-------------------|
| Simple 5-card deck | ~20-25 credits |
| Standard 10-card presentation | ~40-50 credits |
| 20-card with premium images | ~200-400 credits |
| Full pitch deck with exports | ~100-200 credits |

Check your balance: [gamma.app/settings/billing](https://gamma.app/settings/billing)

---

## Quick Reference

### API Base URL

```
https://public-api.gamma.app
```

### Authentication

```bash
--header 'X-API-KEY: <your-api-key>'
--header 'Content-Type: application/json'
```

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v0.2/generations` | POST | Generate new gamma from text |
| `/v0.2/generations/{id}` | GET | Check status, get URLs |
| `/v0.2/themes` | GET | List available themes |

---

## Generate API Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `inputText` | string | Content to generate from (max 100k tokens / ~400k chars) |
| `textMode` | enum | `generate` (expand), `condense` (summarize), `preserve` (keep exact) |

### Format Options

| Parameter | Default | Values |
|-----------|---------|--------|
| `format` | `presentation` | `presentation`, `document`, `social`, `webpage` |
| `numCards` | 10 | 1-60 (Pro) or 1-75 (Ultra) |
| `cardSplit` | `auto` | `auto`, `inputTextBreaks` (use `\n---\n`) |

### Text Options

```json
"textOptions": {
  "amount": "medium",      // brief, medium, detailed, extensive
  "tone": "professional",  // free text, 1-500 chars
  "audience": "executives", // free text, 1-500 chars
  "language": "en"         // 60+ languages
}
```

### Image Options

```json
"imageOptions": {
  "source": "aiGenerated",  // see source options below
  "model": "flux-1-pro",    // see model list below
  "style": "modern, minimal" // free text, 1-500 chars
}
```

**Image Sources:**
- `aiGenerated` - AI-generated images (use with model + style)
- `pictographic` - Pictographic library
- `unsplash` - Unsplash photos
- `giphy` - Animated GIFs
- `webAllImages` - Web images (any license)
- `webFreeToUse` - Personal use licensed
- `webFreeToUseCommercially` - Commercial use licensed
- `placeholder` - Empty placeholders
- `noImages` - No images (use if providing URLs in inputText)

### Card Dimensions

| Format | Options |
|--------|---------|
| Presentation | `fluid`, `16x9`, `4x3` |
| Document | `fluid`, `pageless`, `letter`, `a4` |
| Social | `1x1`, `4x5` (Instagram/LinkedIn), `9x16` (Stories) |

### Export Options

```json
"exportAs": "pptx"  // or "pdf"
```

---

## AI Image Models

### Cost-Effective (2 credits/image)
| Model | API Value |
|-------|-----------|
| Flux Fast 1.1 | `flux-1-quick` |
| Flux Kontext Fast | `flux-kontext-fast` |
| Imagen 3 Fast | `imagen-3-flash` |
| Luma Photon Flash | `luma-photon-flash-1` |

### Standard (8-15 credits/image)
| Model | API Value | Credits |
|-------|-----------|---------|
| Flux Pro | `flux-1-pro` | 8 |
| Imagen 3 | `imagen-3-pro` | 8 |
| Ideogram 3 Turbo | `ideogram-v3-turbo` | 10 |
| Leonardo Phoenix | `leonardo-phoenix` | 15 |

### Premium (20-33 credits/image)
| Model | API Value | Credits |
|-------|-----------|---------|
| Ideogram 3 | `ideogram-v3` | 20 |
| Imagen 4 | `imagen-4-pro` | 20 |
| Gemini 2.5 Flash | `gemini-2.5-flash-image` | 20 |
| Recraft | `recraft-v3` | 20 |
| GPT Image | `gpt-image-1-medium` | 30 |
| DALL-E 3 | `dall-e-3` | 33 |

### Ultra (30-120 credits/image, Ultra plan only)
| Model | API Value | Credits |
|-------|-----------|---------|
| Flux Ultra | `flux-1-ultra` | 30 |
| Imagen 4 Ultra | `imagen-4-ultra` | 30 |
| Recraft Vector | `recraft-v3-svg` | 40 |
| GPT Image Detailed | `gpt-image-1-high` | 120 |

---

## Credit Costs

| Factor | Credits |
|--------|---------|
| Per card | 3-4 |
| Basic AI image | ~2 |
| Standard AI image | ~8-15 |
| Premium AI image | ~20-40 |
| Ultra AI image | ~40-120 |

**Estimates:**
- 10-card deck + 5 basic images = ~40-50 credits
- 20-card doc + 15 premium images = ~360-680 credits

---

## Example Requests

### Simple Presentation

```bash
curl -X POST https://public-api.gamma.app/v1.0/generations \
  -H 'Content-Type: application/json' \
  -H 'X-API-KEY: sk-gamma-xxx' \
  -d '{
    "inputText": "Introduction to machine learning for business leaders",
    "textMode": "generate",
    "format": "presentation",
    "numCards": 8
  }'
```

### Professional Pitch Deck

```bash
curl -X POST https://public-api.gamma.app/v1.0/generations \
  -H 'Content-Type: application/json' \
  -H 'X-API-KEY: sk-gamma-xxx' \
  -d '{
    "inputText": "Our startup solves remote team collaboration with AI-powered async video messaging. Founded 2024, 10k users, $500k ARR, seeking $2M seed round.",
    "textMode": "generate",
    "format": "presentation",
    "numCards": 12,
    "textOptions": {
      "amount": "medium",
      "tone": "confident, professional, visionary",
      "audience": "venture capital investors"
    },
    "imageOptions": {
      "source": "aiGenerated",
      "model": "flux-1-pro",
      "style": "modern tech, clean, professional photography"
    },
    "cardOptions": {
      "dimensions": "16x9"
    },
    "exportAs": "pptx"
  }'
```

### Document from Notes

```bash
curl -X POST https://public-api.gamma.app/v1.0/generations \
  -H 'Content-Type: application/json' \
  -H 'X-API-KEY: sk-gamma-xxx' \
  -d '{
    "inputText": "Meeting notes from Q4 planning...\n---\nBudget discussion...\n---\nAction items...",
    "textMode": "preserve",
    "format": "document",
    "cardSplit": "inputTextBreaks",
    "textOptions": {
      "language": "en"
    },
    "imageOptions": {
      "source": "noImages"
    }
  }'
```

### Social Media Carousel

```bash
curl -X POST https://public-api.gamma.app/v1.0/generations \
  -H 'Content-Type: application/json' \
  -H 'X-API-KEY: sk-gamma-xxx' \
  -d '{
    "inputText": "5 productivity tips for developers: 1. Time blocking 2. Pomodoro technique 3. Code reviews in batches 4. Automate repetitive tasks 5. Take real breaks",
    "textMode": "generate",
    "format": "social",
    "numCards": 6,
    "cardOptions": {
      "dimensions": "4x5"
    },
    "imageOptions": {
      "source": "aiGenerated",
      "model": "ideogram-v3-turbo",
      "style": "vibrant, modern, tech aesthetic"
    }
  }'
```

---

## Response Handling

### POST Response

```json
{
  "generationId": "gen_abc123",
  "status": "pending"
}
```

### GET Status Response (Pending)

```json
{
  "generationId": "gen_abc123",
  "status": "pending"
}
```

### GET Status Response (Completed)

```json
{
  "generationId": "gen_abc123",
  "status": "completed",
  "gammaUrl": "https://gamma.app/docs/xyz",
  "pptxUrl": "https://...",  // if exportAs: "pptx"
  "pdfUrl": "https://...",   // if exportAs: "pdf"
  "creditsUsed": 45
}
```

### Polling Pattern

```javascript
async function waitForGeneration(generationId, apiKey) {
  const maxAttempts = 30;
  const delayMs = 2000;

  for (let i = 0; i < maxAttempts; i++) {
    const response = await fetch(
      `https://public-api.gamma.app/v1.0/generations/${generationId}`,
      { headers: { 'X-API-KEY': apiKey } }
    );
    const data = await response.json();

    if (data.status === 'completed') return data;
    if (data.status === 'failed') throw new Error(data.error);

    await new Promise(r => setTimeout(r, delayMs));
  }
  throw new Error('Generation timeout');
}
```

---

## MCP Integration

Gamma provides a hosted MCP server for AI tool integration.

### Setup in Claude

1. Open Claude Desktop or Web
2. Settings → Connectors
3. Search "Gamma" → Connect
4. Authorize Gamma account access

### MCP Tools Available

| Tool | Capability |
|------|------------|
| `generate_content` | Create presentations, docs, webpages, social |
| `browse_themes` | Search theme library |
| `organize_folders` | Save to workspace folders |

### Effective MCP Prompts

**Good:**
> "Create a 10-slide marketing strategy presentation covering target audience, campaign channels, budget breakdown, and success metrics. Use a professional blue theme and modern photography style."

**Better:**
> "Create a pitch deck for investors about our AI startup. 12 slides, 16:9 format, professional tone. Include: problem, solution, market size, business model, traction, team, financials, ask. Export as PowerPoint."

---

## Troubleshooting

### Insufficient Credits

**Problem**: Error "insufficient credits"

**Solution**:
- Check balance at gamma.app/settings/billing
- Purchase credits or upgrade plan
- Enable auto-recharge

### Authentication Failed

**Problem**: 401 Unauthorized

**Solution**:
- Verify API key is correct
- Check plan supports API (Pro+)
- Regenerate key if compromised

### Generation Timeout

**Problem**: Status stays "pending" too long

**Solution**:
- Complex generations take longer (large numCards, premium images)
- Increase polling timeout to 2-3 minutes
- Simplify request (fewer cards, basic images)

### Token Limit Exceeded

**Problem**: Input too large

**Solution**:
- inputText max: 100k tokens (~400k chars)
- Split into multiple generations
- Use `textMode: "condense"` for long content

---

## Best Practices

1. **Start simple** - Use defaults, then customize
2. **Match model to need** - Basic images for drafts, premium for finals
3. **Use appropriate textMode**:
   - `generate`: Brief input → expanded content
   - `condense`: Long input → summarized content
   - `preserve`: Keep exact text
4. **Control costs** - Use `flux-1-quick` or `imagen-3-flash` for iteration
5. **Export wisely** - Only request PPTX/PDF when needed (adds processing time)
6. **Organize content** - Use folderIds for workspace organization

---

## CLI Script

A standalone Node.js script is available for command-line generation:

**Location:** `.github/muscles/gamma-generator.js`

### Quick Examples

```bash
# Simple topic
node .github/muscles/gamma-generator.js --topic "Introduction to AI"

# From file with PowerPoint export
node .github/muscles/gamma-generator.js --file README.md --export pptx

# Generate and immediately open in PowerPoint 🚀
node .github/muscles/gamma-generator.js --file README.md --export pptx --open

# Full customization with auto-open
node .github/muscles/gamma-generator.js \
  --file my-content.md \
  --slides 15 \
  --tone "professional and inspiring" \
  --audience "executives" \
  --image-model ideogram \
  --image-style "modern illustrations, clean" \
  --dimensions 16x9 \
  --export pptx \
  --output ./exports \
  --open
```

### CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--topic` | `-t` | Topic or content to generate |
| `--file` | `-f` | Path to content file |
| `--format` | | presentation, document, social, webpage |
| `--slides` | `-n` | Number of slides (1-75) |
| `--tone` | | Tone description |
| `--audience` | | Target audience |
| `--language` | `-l` | Language code (en, es, pt...) |
| `--image-model` | | AI model (flux-quick, dalle3...) |
| `--image-style` | | Image style description |
| `--dimensions` | `-d` | Card dimensions |
| `--export` | `-e` | Export format (pptx, pdf) |
| `--output` | `-o` | Output directory (default: ./exports) |
| `--open` | | **Auto-open** exported file after generation |
| `--quiet` | `-q` | Suppress progress messages |
| `--timeout` | | Generation timeout in seconds (default: 180) |
| `--help` | `-h` | Show help |

### Best UX: The `--open` Flag

The `--open` flag provides seamless workflow — generate and review in one command:

```bash
# Create presentation and open immediately
node .github/muscles/gamma-generator.js \
  --file content.md \
  --export pptx \
  --open

# Works on all platforms:
# - Windows: Opens in PowerPoint
# - macOS: Opens in Keynote/PowerPoint
# - Linux: Opens with default application
```

### Two-Step Workflow: Draft → Edit → Generate

For full control over content, use the **draft workflow**:

#### Step 1: Generate a Draft Template

```bash
# Create editable markdown template (no API call, no credits)
node .github/muscles/gamma-generator.js \
  --topic "AI Ethics for Developers" \
  --slides 10 \
  --tone "thoughtful and practical" \
  --audience "software engineers" \
  --image-style "modern illustrations" \
  --draft \
  --open
```

This creates a markdown file with:
- Slide structure placeholders
- Your tone/audience settings preserved
- Image style guidance
- Opens immediately for editing

#### Step 2: Edit the Markdown

Fill in your actual content:

```markdown
## Slide 1: Title
**AI Ethics: A Developer's Responsibility**

Building AI that serves humanity

*Illustration: Developer at computer with ethical symbols*

---

## Slide 2: Why This Matters
**The Code We Write Has Consequences**

- AI systems affect millions of lives
- Bias in training data becomes bias in decisions
- We are the last line of defense

*Illustration: Ripple effect from code to society*
```

#### Step 3: Generate from Your Edited File

```bash
# Now generate the real presentation
node .github/muscles/gamma-generator.js \
  --file ./exports/ai-ethics-for-developers-draft.md \
  --image-model ideogram \
  --export pptx \
  --open
```

**Why use the draft workflow?**
- ✅ Full control over every slide's content
- ✅ No wasted credits on iterations
- ✅ Review structure before committing to generation
- ✅ Reuse templates for similar presentations

### CLI Options Summary

| Option | Short | Description |
|--------|-------|-------------|
| `--topic` | `-t` | Topic or content to generate |
| `--file` | `-f` | Path to content file |
| `--format` | | presentation, document, social, webpage |
| `--slides` | `-n` | Number of slides (1-75) |
| `--tone` | | Tone description |
| `--audience` | | Target audience |
| `--language` | `-l` | Language code (en, es, pt...) |
| `--image-model` | | AI model (flux-quick, dalle3...) |
| `--image-style` | | Image style description |
| `--dimensions` | `-d` | Card dimensions |
| `--export` | `-e` | Export format (pptx, pdf) |
| `--output` | `-o` | Output directory (default: ./exports) |
| `--open` | | **Auto-open** exported file after generation |
| `--draft` | | **Generate markdown template only** (no API call) |
| `--draft-output` | | Custom path for draft markdown file |
| `--quiet` | `-q` | Suppress progress messages |
| `--timeout` | | Generation timeout in seconds (default: 180) |
| `--help` | `-h` | Show help |

**Workflow tip:** Create a markdown file with your content structure, then generate and review:

```bash
# Quick workflow
node .github/muscles/gamma-generator.js -t "My Topic" --draft --open  # Edit the draft
node .github/muscles/gamma-generator.js -f exports/my-topic-draft.md -e pptx --open  # Generate
```

Run `node .github/muscles/gamma-generator.js --help` for full documentation.

---

## Related Skills

- [prompt-engineering](.github/skills/prompt-engineering/SKILL.md) - Crafting effective inputText
- [markdown-mermaid](.github/skills/markdown-mermaid/SKILL.md) - Diagrams for presentations
- [image-handling](.github/skills/image-handling/SKILL.md) - Working with generated images
