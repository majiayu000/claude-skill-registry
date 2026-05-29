# Webflow Publish Skill

Publish blog posts with images to the OpenEd Webflow CMS via API.

---

## When to Use

Use this skill when publishing articles, deep dives, or blog posts to opened.co. This handles:
- Markdown to HTML conversion
- Image uploads to Webflow CDN
- Author detection/creation
- CMS post creation

---

## API Configuration

**Token:** `.env` file as `WEBFLOW_API_KEY`
**Base URL:** `https://api.webflow.com/v2`

---

## Key IDs (OpenEd Site)

| Resource | ID |
|----------|-----|
| Site ID | `67c7406fc9e6913d1b92e341` |
| Posts Collection | `6805bf729a7b33423cc8a08c` |
| Authors Collection | `68089af9024139c740e4b922` |
| Post Type: Blog Posts | `6805d44048df4bd97a0754ed` |
| Post Type: Podcasts | `6805d42ba524fabb70579f4e` |
| Post Type: Daily Newsletters | `6805d5076ff8c966566279a4` |
| Post Type: Announcements | `6812753c2611e43906dc13d6` |

### Known Authors

| Author | ID |
|--------|-----|
| Charlie Deist | `68089b4d33745cf5ea4d746d` |

---

## Workflow

### Step 1: Author Detection

**Default:** Charlie Deist (`68089b4d33745cf5ea4d746d`)

If article has different author:

1. Search Authors collection for existing author:
```bash
curl -X POST "https://api.webflow.com/v2/collections/68089af9024139c740e4b922/items/list" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -H "Content-Type: application/json"
```

2. If not found, create new author:
```bash
curl -X POST "https://api.webflow.com/v2/collections/68089af9024139c740e4b922/items" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "isArchived": false,
    "isDraft": false,
    "fieldData": {
      "name": "Author Name",
      "slug": "author-name"
    }
  }'
```

---

### Step 2: Upload Images

**CRITICAL: Thumbnail image goes in `thumbnail` field ONLY - do NOT include it in article body content.** The thumbnail automatically displays above the article header in Webflow's design.

**CRITICAL: Image upload is a TWO-STEP process.** Step 2a creates an asset placeholder. Step 2b actually uploads the file. If you skip Step 2b, the asset ID exists but the image won't load. You MUST verify Step 2b returns HTTP 201 with an XML response containing `<PostResponse>`.

For each image (excluding thumbnail from body):

**Step 2a: Request presigned URL**
```bash
FILE_HASH=$(md5 -q /path/to/image.png)

curl -X POST "https://api.webflow.com/v2/sites/67c7406fc9e6913d1b92e341/assets" \
  -H "Authorization: Bearer $WEBFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"fileName\": \"descriptive-name.png\", \"fileHash\": \"$FILE_HASH\"}"
```

**Step 2b: Upload to S3**
Use the `uploadUrl` and `uploadDetails` from response:
```bash
curl -X POST "$UPLOAD_URL" \
  -F "acl=$ACL" \
  -F "bucket=$BUCKET" \
  -F "X-Amz-Algorithm=$ALGORITHM" \
  -F "X-Amz-Credential=$CREDENTIAL" \
  -F "X-Amz-Date=$DATE" \
  -F "key=$KEY" \
  -F "Policy=$POLICY" \
  -F "X-Amz-Signature=$SIGNATURE" \
  -F "success_action_status=201" \
  -F "Content-Type=image/png" \
  -F "Cache-Control=max-age=31536000, must-revalidate" \
  -F "file=@/path/to/image.png"
```

**Step 2c: Get CDN URL**
```
https://cdn.prod.website-files.com/67c7406fc9e6913d1b92e341/{asset_id}_{filename}
```

---

### Step 3: Convert Markdown to HTML

**CRITICAL: Strip these from body content:**
- H1 title (becomes `name` field)
- Metadata lines: `**Meta Title:**`, `**Meta Description:**`, `**URL:**`
- Word count lines: `*Word count:*`
- Horizontal rules (`---`)
- Em dashes (`—`) → replace with spaced hyphens (` - `)

**Key Rules:**
1. **Strip metadata** - Match both `**Meta Title:**` (bold) and `*Meta Title:` (italic)
2. **Replace em dashes globally** - Before any other processing
3. **Split by blank lines** - Paragraphs are separated by blank lines
4. **Convert links before bold** - So `**[text](url)**` works correctly
5. **Handle tables properly** - Filter empty cells from `|` delimiters
6. **Exclude thumbnail from body** - Only include non-thumbnail images

**Metadata stripping patterns:**
```python
def is_metadata_line(line):
    """Lines to strip from body content."""
    patterns = [
        r'^\*\*Meta Title:\*\*',      # Bold format
        r'^\*\*Meta Description:\*\*',
        r'^\*\*URL:\*\*',
        r'^\*Meta Title:',            # Italic format
        r'^\*Meta Description:',
        r'^\*URL:',
        r'^Meta Title:',              # Plain format
        r'^Meta Description:',
        r'^URL:',
        r'^\*Word count:',
    ]
    return any(re.match(p, line.strip(), re.IGNORECASE) for p in patterns)
```

**Table conversion:**
```python
def convert_table(block):
    """Convert markdown table to HTML."""
    lines = block.strip().split('\n')
    html = '<table>'
    for i, line in enumerate(lines):
        if '---' in line:  # Skip separator
            continue
        # Split and filter empty cells from leading/trailing |
        cells = [c.strip() for c in line.split('|') if c.strip()]
        tag = 'th' if i == 0 else 'td'
        row = ''.join(f'<{tag}>{convert_inline(c)}</{tag}>' for c in cells)
        html += f'<tr>{row}</tr>'
    return html + '</table>'
```

**Image format in rich text:**
```html
<figure class="w-richtext-figure-type-image w-richtext-align-center" data-rt-type="image" data-rt-align="center">
  <div>
    <img src="CDN_URL" alt="description" loading="lazy">
  </div>
</figure>
```

**Reference implementation:** `Studio/SEO Content Production/fix_webflow_posts.py`

---

### Step 4: Create Blog Post

```python
import requests
import json

payload = {
    "isArchived": False,
    "isDraft": True,  # Always create as draft first
    "fieldData": {
        "name": "Post Title",
        "slug": "post-slug",
        "post-type": ["6805d44048df4bd97a0754ed"],  # Blog Posts
        "summary": "Meta description for SEO",
        "published-date": "2026-01-23T00:00:00.000Z",
        "author": "68089b4d33745cf5ea4d746d",  # Author ID
        "thumbnail": {
            "fileId": "ASSET_ID",
            "url": "CDN_URL"
        },
        "content": html_content  # NO thumbnail image in here
    }
}

response = requests.post(
    "https://api.webflow.com/v2/collections/6805bf729a7b33423cc8a08c/items",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json=payload
)
```

---

### Step 5: Review and Publish

1. Check post in Webflow CMS dashboard
2. Verify formatting, images, links
3. Either publish from dashboard or update via API:

```python
requests.patch(
    f"https://api.webflow.com/v2/collections/6805bf729a7b33423cc8a08c/items/{post_id}",
    headers=headers,
    json={"isDraft": False}
)
```

---

### Step 6: Generate Social Suggestions (Automatic)

**After publishing, automatically run social extraction.**

This step chains to `newsletter-to-social` skill:

1. Extract 3-5 standalone snippets from the published content
2. Match each to best-fit social templates
3. Post suggestions to **#content-inbox** (C0ABV2VQQKS)
4. User triages with reactions (✍️ develop, ✅ approve, ❌ skip)

**Prompt to run:**
```
Content published to Webflow:
- Title: [post title]
- URL: [webflow URL]
- Type: [Blog/Newsletter/Podcast]

Now generating social suggestions...

[Run newsletter-to-social skill with this content]
```

**Expected output:** 6-9 social suggestions posted to #content-inbox.

**Note:** This step runs automatically as part of the Webflow publish workflow - no separate invocation needed.

---

## CMS Field Schema

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | PlainText | Yes | Post title |
| `slug` | PlainText | Yes | URL slug |
| `post-type` | MultiReference | Yes | Array of post type IDs |
| `thumbnail` | Image | No | `{fileId, url}` - both required |
| `summary` | PlainText | No | Meta description |
| `published-date` | DateTime | No | ISO 8601 format |
| `content` | RichText | No | HTML content (NO thumbnail) |
| `author` | Reference | No | Author ID |

---

## Image SEO Workflow

**Before uploading images**, optimize them:

1. **Format detection**: The upload function now detects actual image format via magic bytes. No more JPEG-as-PNG mismatches.
2. **WebP conversion**: Use the image optimizer before uploading:
   ```bash
   python3 .claude/skills/nano-banana-image-generator/scripts/image_optimizer.py \
     path/to/thumbnail.jpg --use thumbnail
   ```
3. **Descriptive filenames**: Upload with SEO names (e.g. `peter-gray-education-thumbnail.webp`), not timestamps.
4. **Alt text**: Always provide descriptive alt text. The converter warns on empty alt text.
5. **Smart loading**: The HTML converter automatically sets `loading="eager" fetchpriority="high"` on the first image and `loading="lazy"` on the rest.
6. **Dimensions**: Pass image metadata to the converter to add `width`/`height` attributes (prevents CLS):
   ```python
   from markdown_to_webflow import markdown_to_html, load_image_meta_from_sidecars
   meta = load_image_meta_from_sidecars("path/to/article/images/")
   html = markdown_to_html(content, image_meta=meta)
   ```

## Schema Markup

**After converting HTML**, generate structured data:

```python
from seo_schema_generator import generate_all_schema

schemas = generate_all_schema(
    headline="Article Title",
    description="Meta description",
    date_published="2026-02-06",
    slug="article-slug",
    html_content=html,
    image_url=thumbnail_cdn_url,
    image_width=1200,
    image_height=675,
)

# schemas['blog_posting'] - BlogPosting JSON-LD (handled by template)
# schemas['faq'] - FAQPage JSON-LD (goes in faq-schema CMS field)
```

The `faq-schema` CMS field must be created in Webflow Designer first (plain text, multi-line).

## Meta Description Validation

```python
from markdown_to_webflow import validate_meta_description

valid, messages = validate_meta_description(summary, keyword="homeschool math")
for msg in messages:
    print(f"  {msg}")
```

Checks: 120-160 char length, keyword presence.

## Checklist

Before publishing:

- [ ] Author identified or created
- [ ] Thumbnail optimized to WebP with descriptive filename
- [ ] Thumbnail uploaded (separate from body content)
- [ ] Body images uploaded with descriptive alt text
- [ ] Meta description validated (120-160 chars, keyword present)
- [ ] Markdown converted to HTML (smart loading, dimensions)
- [ ] FAQ schema generated and included in payload
- [ ] Post created as draft
- [ ] Reviewed in Webflow dashboard
- [ ] Published when ready

After publishing:

- [ ] Social suggestions generated (Step 6 - automatic)
- [ ] Suggestions posted to #content-inbox
- [ ] Report URL to user for verification
- [ ] Verify schema with Google Rich Results Test

---

## Common Issues

**Issue:** Metadata showing in body (Meta Title, Meta Description, URL)
**Fix:** Strip lines matching `**Meta Title:**`, `**Meta Description:**`, `**URL:**` (bold format). Also check italic format `*Meta Title:*`. The converter must handle BOTH formats.

**Issue:** Tables not rendering correctly
**Fix:** When splitting on `|`, the first and last elements are empty strings (from leading/trailing `|`). Filter: `cells = [c.strip() for c in line.split('|') if c.strip()]`

**Issue:** Em dashes in content
**Fix:** Replace globally BEFORE any other processing: `content = content.replace('—', ' - ')`

**Issue:** S3 upload returns 403 Access Denied
**Fix:** Cache-Control must be `max-age=31536000, must-revalidate` (NOT `immutable`)

**Issue:** Thumbnail not appearing in CMS
**Fix:** The presigned URL request creates an asset placeholder, but you MUST complete the S3 upload. Verify S3 returns status 201 with XML containing `<PostResponse>`.

**Issue:** Thumbnail appears twice
**Fix:** Don't include thumbnail in `content` field - it auto-displays above header

**Issue:** Links broken
**Fix:** Convert links BEFORE bold: process `[text](url)` first, then `**text**`

**Issue:** Author not showing
**Fix:** Use author ID as string, not array (unlike post-type)

**Issue:** Status 202 treated as error
**Fix:** 202 (Accepted) is success for async processing. Check 200, 201, AND 202.

**Issue:** Numbered lists not converting
**Fix:** Match `^\d+\.` pattern and wrap in `<ol><li>...</li></ol>`

---

## Newsletter Workflow

For weekly newsletters published to Webflow:

1. **Use Daily Newsletters post type:** `6805d5076ff8c966566279a4`
2. **Slug format:** `opened-weekly-YYYY-MM-DD`
3. **Thumbnail:** Usually the meme of the week
4. **Body:** Full newsletter content converted to HTML

**Status check pattern:**
```python
if response.status_code in [200, 201, 202]:
    # Success (202 = async processing, still success)
    data = response.json()
```

---

## Markdown Converter Notes

The converter should handle:
- Headers (H2, H3, H4) - skip H1 (becomes `name` field)
- Paragraphs (blank line separated)
- Bold (`**text**`) and italic (`*text*` or `_text_`)
- Links (`[text](url)`) - convert BEFORE bold
- Unordered lists (`- item`)
- Ordered/numbered lists (`1. item`, `2. item`)
- Horizontal rules (`---`)
- Images (to Webflow figure format)

**Order matters:** Process links before bold so `**[text](url)**` works.

---

## Example Files

**Recommended reference (most robust):**
- `Studio/SEO Content Production/fix_webflow_posts.py` - Complete converter with all edge cases handled

**Batch upload:**
- `Studio/SEO Content Production/batch_webflow_upload.py` - Upload multiple articles
- `Studio/SEO Content Production/update_thumbnails.py` - Upload thumbnails to existing posts

**Legacy examples:**
- `Studio/SEO Content Production/Open Education Hub/Deep Dive Studio/Apprenticeships CTE/convert_to_html.py`
- `Studio/OpenEd Weekly/2026-01-24 - Weekly/create_newsletter_post.py` (newsletter workflow)
