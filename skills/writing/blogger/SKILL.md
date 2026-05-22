---
name: blogger
description: Create, edit, and publish blog posts with consistent voice and style. Helps build and maintain a style guide, write drafts, edit for quality, optimize SEO, and fact-check claims before publishing.
---

# Blogger

A writing companion for maintaining a blog with consistent voice and quality.

## First-Run Check

**Before doing anything else**, check if a style guide exists:

```bash
# Check for style guide (adjust path as needed)
STYLE_GUIDE="${PROJECT_ROOT}/.blog-style/voice.md"
if [ ! -f "$STYLE_GUIDE" ]; then
  echo "NO_STYLE_GUIDE"
else
  echo "STYLE_GUIDE_EXISTS"
fi
```

**If no style guide exists:**
1. Offer to create one: "I don't see a style guide for this blog. Want me to analyze some existing posts and build one?"
2. If yes, run the post analyzer (see [Building a Style Guide](#building-a-style-guide))
3. If no, proceed but note that voice consistency won't be enforced

---

## Style Guide Location

Style guides live in the project root:

```
{project-root}/
├── .blog-style/
│   ├── voice.md           # Voice & tone document
│   ├── examples.md        # Links to exemplar posts
│   └── terminology.md     # Brand terms, jargon preferences
└── .credentials/
    └── wordpress.json     # API credentials (gitignored)
```

**Why project root?** The style guide is project-specific, not personal. It can be committed to git (it's not sensitive) and shared with collaborators or other tools.

---

## Building a Style Guide

### Automated Post Analysis

Run the analyzer to sample existing posts and extract patterns:

```bash
# Authenticated mode (recommended for your own blog - richer analysis)
node "{baseDir}/scripts/analyze-posts.js" \
  --site="https://example.com" \
  --credentials="${PROJECT_ROOT}/.credentials/wordpress.json" \
  --output="${PROJECT_ROOT}/.blog-style/"

# Public mode (any WordPress site - no auth required)
node "{baseDir}/scripts/analyze-posts.js" \
  --site="https://any-wordpress-site.com" \
  --output="${PROJECT_ROOT}/.blog-style/" \
  --public
```

**Modes:**
- **Authenticated:** Uses `context=edit` API, gets raw block content, analyzes block types used
- **Public:** Uses rendered HTML, works without credentials, basic text analysis only

The analyzer will:
1. Fetch recent posts (default: 20, varied by category/tag)
2. Analyze sentence structure, vocabulary, tone markers
3. Identify patterns (contractions, question usage, paragraph length)
4. Extract common phrases and stylistic signatures
5. Generate a draft `voice.md` for review

### Manual Style Guide Creation

If starting fresh or preferring manual setup, use the template:

```bash
cp "{baseDir}/templates/style-guide.md.template" "${PROJECT_ROOT}/.blog-style/voice.md"
```

Then fill in:
- **Voice characteristics** — Personality adjectives (friendly, authoritative, irreverent)
- **Tone variations** — How voice adapts to different content types
- **Grammar preferences** — Oxford comma, contractions, etc.
- **Formatting rules** — Heading styles, list preferences
- **Dos and Don'ts** — With concrete examples

See `{baseDir}/references/writing-guide.md` for guidance on each section.

---

## Workflows

### 1. Write a New Post

**Input needed:** Topic, target audience, key points (optional)

**Process:**
1. **Outline** — Generate structure with intro hook, main sections, conclusion
2. **Draft** — Write section by section, checking voice against style guide
3. **Headlines** — Generate 5+ title options using proven formulas
4. **Review** — Run through editing checklist

**Output:** Draft post ready for editing

```
/blogger write "Topic: Why I switched to Neovim"
```

### 2. Edit an Existing Draft

**Input needed:** Draft content (pasted or file path)

**Process:**
1. **Structure pass** — Does it flow logically? Are sections balanced?
2. **Clarity pass** — Simplify sentences, remove jargon, active voice
3. **Voice pass** — Compare against style guide, flag inconsistencies
4. **Technical pass** — Grammar, spelling, punctuation
5. **SEO pass** — Keywords, meta, internal/external links
6. **Fact-check pass** — Verify claims, check sources, flag unverified statements

**Output:** Edited draft with change suggestions and confidence notes

```
/blogger edit [paste draft or provide file path]
```

### 3. SEO Audit

**Input needed:** Draft content, target keyword

**Process:**
1. Check keyword in title, URL slug, first 100 words
2. Verify keyword density (aim for 1-2%, not stuffed)
3. Check for internal links to related content
4. Verify external links to credible sources
5. Generate meta description (≤155 characters)
6. Suggest related keywords and phrases

**Output:** SEO report with specific recommendations

```
/blogger seo "target keyword" [draft content]
```

### 4. Fact-Check

**Input needed:** Draft content

**Process:**
1. Extract all claims (statistics, quotes, dates, facts)
2. Categorize by verifiability:
   - **Verifiable** — Can be checked against sources
   - **Opinion** — Clearly stated as opinion, OK
   - **Unverified** — Stated as fact but no source
3. For verifiable claims:
   - Search for corroborating sources
   - Flag discrepancies or outdated info
   - Suggest citations

**Output:** Fact-check report with confidence levels

```
/blogger fact-check [draft content]
```

### 5. Publish

**Input needed:** Final draft, WordPress credentials

**Process:**
1. Final review checklist:
   - [ ] Title finalized
   - [ ] Meta description set
   - [ ] Categories/tags assigned
   - [ ] Featured image (if required)
   - [ ] Internal links added
   - [ ] Fact-check complete
2. Create draft in WordPress via REST API
3. Return preview URL for final review
4. On approval, publish (or schedule)

**Never auto-publish.** Always create as draft first.

```
/blogger publish [final draft]
```

---

## WordPress REST API

### Credentials Setup

```json
// .credentials/wordpress.json
{
  "site": "https://example.com",
  "rest_api": {
    "username": "your-username",
    "app_password": "xxxx xxxx xxxx xxxx xxxx xxxx"
  }
}
```

Generate an application password in WordPress: **Users → Profile → Application Passwords**

### Core Operations

```bash
# Load credentials
CREDS=$(cat "${PROJECT_ROOT}/.credentials/wordpress.json")
SITE=$(echo $CREDS | jq -r '.site')
USER=$(echo $CREDS | jq -r '.rest_api.username')
PASS=$(echo $CREDS | jq -r '.rest_api.app_password')
AUTH="$USER:$PASS"

# List recent posts
curl -s -u "$AUTH" "$SITE/wp-json/wp/v2/posts?per_page=10" | jq '.[] | {id, title: .title.rendered, status, date}'

# Create draft
curl -s -u "$AUTH" -X POST "$SITE/wp-json/wp/v2/posts" \
  -H "Content-Type: application/json" \
  -d '{"title":"Post Title","content":"...","status":"draft"}'

# Update post
curl -s -u "$AUTH" -X POST "$SITE/wp-json/wp/v2/posts/{id}" \
  -H "Content-Type: application/json" \
  -d '{"content":"Updated content..."}'

# Publish
curl -s -u "$AUTH" -X POST "$SITE/wp-json/wp/v2/posts/{id}" \
  -H "Content-Type: application/json" \
  -d '{"status":"publish"}'

# Get categories
curl -s "$SITE/wp-json/wp/v2/categories" | jq '.[] | {id, name, slug}'

# Get tags
curl -s "$SITE/wp-json/wp/v2/tags" | jq '.[] | {id, name, slug}'
```

### Block Format

WordPress uses Gutenberg blocks. Wrap content appropriately:

```html
<!-- wp:paragraph -->
<p>Regular paragraph text.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Section Heading</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>List item one</li>
<li>List item two</li>
</ul>
<!-- /wp:list -->

<!-- wp:quote -->
<blockquote class="wp-block-quote"><p>Quote text here.</p><cite>Attribution</cite></blockquote>
<!-- /wp:quote -->

<!-- wp:code -->
<pre class="wp-block-code"><code>code here</code></pre>
<!-- /wp:code -->

<!-- wp:image {"id":123} -->
<figure class="wp-block-image"><img src="..." alt="..." class="wp-image-123"/></figure>
<!-- /wp:image -->
```

---

## Reference Documents

- `{baseDir}/references/writing-guide.md` — Writing best practices, structure, hooks
- `{baseDir}/references/editing-checklist.md` — Multi-pass editing workflow
- `{baseDir}/references/seo-checklist.md` — SEO optimization reference
- `{baseDir}/references/headline-formulas.md` — Proven headline patterns
- `{baseDir}/references/fact-checking.md` — Verification workflow and sources

---

## Templates

- `{baseDir}/templates/style-guide.md.template` — Empty style guide to fill in
- `{baseDir}/templates/post-outline.md.template` — Blog post outline structure

---

## Tips

### Voice Consistency
- Read the style guide before every writing session
- When in doubt, check exemplar posts
- Flag any suggested edits that might change the voice

### Quality Over Speed
- Never skip the editing passes
- Fact-check anything that could be wrong
- Preview before publishing, always

### SEO Without Stuffing
- One primary keyword per post
- Write for humans first, then optimize
- Internal links help readers AND SEO

### When to Break the Rules
- Style guides are guidelines, not laws
- Some posts warrant a different tone (announcements, serious topics)
- Document exceptions in the style guide over time
