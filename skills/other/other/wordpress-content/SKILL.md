---
name: wordpress-content
description: >
  Create and manage WordPress posts, pages, media, categories, and menus.
  Workflow: determine content type, choose method (WP-CLI or REST API), execute, verify.
  Use when creating blog posts, updating pages, uploading media, managing categories
  and tags, updating menus, or doing bulk content operations on WordPress sites.
compatibility: claude-code-only
---

# WordPress Content

Create, update, and manage WordPress content — posts, pages, media, categories, tags, and menus. Produces live content on the site via WP-CLI or the REST API.

## Prerequisites

- Working WP-CLI SSH connection or REST API credentials (use **wordpress-setup** skill)
- Site config from `wordpress.config.json` or `wp-cli.yml`

## Workflow

### Step 1: Determine the Operation

| Task | Best Method |
|------|-------------|
| Create/edit single post or page | WP-CLI `wp post create/update` |
| Bulk create posts | WP-CLI loop or REST API batch |
| Upload images/media | WP-CLI `wp media import` |
| Manage categories/tags | WP-CLI `wp term` |
| Update navigation menus | WP-CLI `wp menu` |
| Scheduled posts | WP-CLI with `--post_date` |
| Complex HTML content | Write to temp file, pass to WP-CLI |

### Step 2: Create Content

#### Blog Posts

```bash
# Simple post
wp @site post create \
  --post_type=post \
  --post_title="My New Blog Post" \
  --post_content="<p>Post content here.</p>" \
  --post_status=draft \
  --post_category=3,5

# Post from HTML file (better for long content)
wp @site post create ./post-content.html \
  --post_type=post \
  --post_title="My New Blog Post" \
  --post_status=draft \
  --post_excerpt="A brief summary of the post." \
  --post_category=3,5 \
  --tags_input="tag1,tag2"
```

**Post statuses**: `draft`, `publish`, `pending`, `future` (use with `--post_date`)

#### Pages

```bash
wp @site post create \
  --post_type=page \
  --post_title="About Us" \
  --post_content="<h2>Our Story</h2><p>Content here...</p>" \
  --post_status=publish \
  --post_parent=0 \
  --menu_order=10
```

#### Scheduled Posts

```bash
wp @site post create \
  --post_type=post \
  --post_title="Scheduled Post" \
  --post_content="<p>This goes live tomorrow.</p>" \
  --post_status=future \
  --post_date="2026-02-23 09:00:00"
```

### Step 3: Upload Media

```bash
# Upload from URL
wp @site media import "https://example.com/image.jpg" \
  --title="Product Photo" \
  --alt="Product front view" \
  --caption="Our latest product"

# Upload from local file (requires SCP first for remote sites)
scp ./image.jpg user@host:/tmp/image.jpg
wp @site media import /tmp/image.jpg --title="Local Upload"
```

**Set featured image on a post**:

```bash
# Get the attachment ID from the import output, then:
wp @site post meta update {post_id} _thumbnail_id {attachment_id}
```

### Step 4: Manage Taxonomy

#### Categories

```bash
# List categories
wp @site term list category --fields=term_id,name,slug,count

# Create category
wp @site term create category "News" --slug=news --description="Company news and updates"

# Create child category
wp @site term create category "Product News" --slug=product-news --parent=5

# Assign category to post
wp @site post term add {post_id} category news
```

#### Tags

```bash
# Add tags during post creation
wp @site post create --post_title="..." --tags_input="seo,marketing,tips"

# Add tags to existing post
wp @site post term add {post_id} post_tag seo marketing tips
```

### Step 5: Manage Menus

```bash
# List menus
wp @site menu list --fields=term_id,name,slug,count

# List items in a menu
wp @site menu item list main-menu --fields=db_id,type,title,link

# Add page to menu
wp @site menu item add-post main-menu {page_id} --title="About Us"

# Add custom link
wp @site menu item add-custom main-menu "Contact" "https://example.com/contact/"

# Reorder (set position)
wp @site menu item update {item_id} --position=3
```

### Step 6: Update Existing Content

```bash
# Update post title and content
wp @site post update {post_id} \
  --post_title="Updated Title" \
  --post_content="<p>New content.</p>"

# Update from file
wp @site post update {post_id} ./updated-content.html

# Bulk update status
wp @site post list --post_type=post --post_status=draft --field=ID | \
  xargs -I {} wp @site post update {} --post_status=publish
```

### Step 7: Verify

```bash
# Check the post
wp @site post get {post_id} --fields=ID,post_title,post_status,guid

# Get the live URL
wp @site post get {post_id} --field=guid

# List recent posts
wp @site post list --post_type=post --posts_per_page=5 --fields=ID,post_title,post_status,post_date
```

Provide the admin URL and live URL:
- Admin: `https://example.com/wp-admin/post.php?post={id}&action=edit`
- Live: `https://example.com/{slug}/`

---

## Critical Patterns

### HTML Content in WP-CLI

For anything beyond a sentence, write HTML to a temp file and pass it:

```bash
cat > /tmp/post-content.html << 'EOF'
<h2>Section Heading</h2>
<p>Paragraph content with <strong>bold</strong> and <a href="/link">links</a>.</p>
<ul>
  <li>List item one</li>
  <li>List item two</li>
</ul>
EOF

wp @site post create /tmp/post-content.html --post_title="My Post" --post_status=draft
```

Shell quoting in `--post_content` is fragile for complex HTML.

### Bulk Operations

For creating many posts, use a loop with verification:

```bash
while IFS=, read -r title slug content_file category; do
  wp @site post create "$content_file" \
    --post_type=post \
    --post_title="$title" \
    --post_name="$slug" \
    --post_category="$category" \
    --post_status=draft
  sleep 0.5
done < posts.csv
```

Always create as `draft` first, review, then bulk-publish.

### ACF Custom Fields

If Advanced Custom Fields is installed:

```bash
# Set ACF field
wp @site post meta update {post_id} field_name "value"

# Get ACF field
wp @site post meta get {post_id} field_name
```

ACF stores fields with both the field value and a reference key (`_field_name` → `field_abc123`).

### REST API Alternative

When WP-CLI isn't available, use the REST API. See `references/rest-api-endpoints.md` for patterns.

---

## Reference Files

- `references/rest-api-endpoints.md` — REST API endpoints with authentication examples
- `references/wp-cli-content.md` — WP-CLI content management command reference
