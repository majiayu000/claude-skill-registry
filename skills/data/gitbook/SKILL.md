---
name: gitbook
description: GitBook documentation platform - creating docs, publishing sites, Git sync, API references, and collaboration
---

# GitBook Skill

Use when working with GitBook documentation platform, generated from official documentation (107 pages).

## When to Use This Skill

This skill should be triggered when:
- Creating or managing GitBook documentation spaces
- Setting up Git synchronization (GitHub/GitLab)
- Publishing documentation sites with custom domains
- Working with GitBook's block-based editor
- Configuring OpenAPI/API reference documentation
- Managing team collaboration and change requests
- Migrating content to GitBook
- Customizing site appearance and branding

## Quick Reference

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Space** | A documentation project (like a book or wiki) |
| **Collection** | A group of related spaces |
| **Site** | Published documentation accessible via URL |
| **Change Request** | Draft changes for review before publishing |
| **Live Edits** | Direct changes without change request workflow |

### Content Blocks

GitBook uses a block-based editor. Common blocks:

| Block | Shortcut | Description |
|-------|----------|-------------|
| Paragraph | Just type | Default text block |
| Heading | `#`, `##`, `###` | Section headers (H1, H2, H3) |
| Code Block | ``` or `/code` | Syntax-highlighted code |
| Quote | `>` or `/quote` | Blockquote |
| List | `-`, `1.` | Unordered/ordered lists |
| Task List | `- [ ]` | Checkbox items |
| Table | `/table` | Data tables |
| Image | `/image` | Upload or embed images |
| Tabs | `/tabs` | Tabbed content |
| Expandable | `/expandable` | Collapsible sections |
| Cards | `/cards` | Visual link cards |
| Hint | `/hint` | Info, warning, danger, success boxes |
| API Reference | `/openapi` | OpenAPI spec integration |

### Inline Content (/) Palette

Press `/` in any text block to access:
- **Link** - Relative (internal) or absolute (external) links
- **Image** - Inline images
- **Emoji** - `:emoji_name:` syntax
- **Math** - LaTeX/KaTeX formulas: `$$formula$$`
- **Annotation** - Footnote-style explanations

### Common Patterns

#### Create a hint/callout box
```markdown
{% hint style="info" %}
This is an info hint
{% endhint %}

{% hint style="warning" %}
This is a warning
{% endhint %}

{% hint style="danger" %}
This is a danger/error hint
{% endhint %}

{% hint style="success" %}
This is a success hint
{% endhint %}
```

#### Create tabs
```markdown
{% tabs %}
{% tab title="JavaScript" %}
console.log("Hello");
{% endtab %}
{% tab title="Python" %}
print("Hello")
{% endtab %}
{% endtabs %}
```

#### Create expandable section
```markdown
{% expandable title="Click to expand" %}
Hidden content here
{% endexpandable %}
```

#### Create stepper (numbered steps)
```markdown
{% stepper %}
{% step %}
First step content
{% endstep %}
{% step %}
Second step content
{% endstep %}
{% endstepper %}
```

#### Create cards
```markdown
{% cards %}
{% card title="Card 1" href="/page1" %}
Description here
{% endcard %}
{% card title="Card 2" href="/page2" %}
Another description
{% endcard %}
{% endcards %}
```

### Git Sync Configuration

#### Enable GitHub Sync
1. Go to space settings → Git Sync
2. Connect GitHub account
3. Select repository and branch
4. Configure sync direction:
   - **GitBook → GitHub**: GitBook is source of truth
   - **GitHub → GitBook**: Git repo is source of truth
   - **Two-way**: Bidirectional sync

#### Directory structure for Git
```
docs/
├── README.md          # Space landing page
├── SUMMARY.md         # Table of contents
├── .gitbook.yaml      # GitBook configuration
├── page-one.md
├── group/
│   ├── README.md      # Group landing page
│   └── nested-page.md
└── .gitbook/
    └── assets/        # Images and files
```

#### SUMMARY.md structure
```markdown
# Table of contents

* [Introduction](README.md)
* [Getting Started](getting-started.md)

## Section Title

* [Page One](section/page-one.md)
* [Page Two](section/page-two.md)
```

#### .gitbook.yaml configuration
```yaml
root: ./docs/          # Documentation root directory

structure:
  readme: README.md    # Landing page file
  summary: SUMMARY.md  # Table of contents file

redirects:
  old-path: new-path   # URL redirects
```

### Custom Domain Setup

1. Go to site settings → Custom domain
2. Add your domain (e.g., `docs.example.com`)
3. Configure DNS:
   - **CNAME record**: Point to `hosting.gitbook.io`
   - Or **A record** for apex domains
4. Enable HTTPS (automatic via Let's Encrypt)

#### Subdirectory publishing (with Cloudflare/Vercel)
```
example.com/docs → GitBook site
```

### OpenAPI Integration

#### Add OpenAPI specification
1. Upload OpenAPI/Swagger file (JSON or YAML)
2. Or link to hosted spec URL
3. GitBook auto-generates interactive API docs

#### Customize API reference
```markdown
{% openapi src="./api.yaml" /%}
```

### Publishing Options

| Type | Description |
|------|-------------|
| **Public** | Accessible to everyone |
| **Unlisted** | No search indexing, URL access only |
| **Share links** | Private with token-based access |
| **Authenticated** | SSO/login required |

### Collaboration

#### Change Requests
- Create a change request for non-breaking changes
- Request reviews from team members
- Merge when approved
- Automatic conflict detection

#### Live Edits
- Direct editing for quick fixes
- No approval workflow
- Immediate publishing

#### Comments
- Inline comments on any block
- @mention team members
- Resolve when addressed

### Migration to GitBook

#### From other platforms
1. **Import panel**: Confluence, Notion, Docusaurus, Markdown
2. **Git Sync**: Connect existing Git repo with markdown files
3. **Manual**: Copy/paste with formatting preserved

#### Import via Git Sync
```bash
# Prepare your repo
mkdir docs
echo "# Welcome" > docs/README.md
echo "* [Welcome](README.md)" > docs/SUMMARY.md
git add . && git commit -m "Initial docs"
```

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Command palette | `⌘/Ctrl + K` |
| Bold | `⌘/Ctrl + B` |
| Italic | `⌘/Ctrl + I` |
| Link | `⌘/Ctrl + K` (with selection) |
| Code | `⌘/Ctrl + E` |
| Search | `⌘/Ctrl + /` |

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **llms-txt.md** - Full GitBook documentation (107 pages, 456 KB)
- **llms-full.md** - Complete llms.txt source
- **llms.md** - Condensed reference (95 KB)

Use `view` to read specific reference files when detailed information is needed.

## Content Categories

The reference documentation covers:

### Creating Content
- Blocks (code, tables, images, tabs, cards, etc.)
- Inline content (links, emojis, math, annotations)
- Formatting and layout
- Page structure and navigation

### Publishing
- Sites and custom domains
- Public vs private publishing
- Share links and authentication
- Redirects and SEO

### Collaboration
- Change requests and live edits
- Comments and reviews
- Team management
- Merge rules

### Integration
- Git Sync (GitHub, GitLab)
- OpenAPI/API documentation
- Translations
- Extensions

### Configuration
- Site structure and theming
- Icons, colors, and branding
- Content configuration
- Troubleshooting

## Common Issues

### Git Sync not working
- Check repository permissions
- Verify branch exists
- Ensure SUMMARY.md is valid
- Check for merge conflicts

### Custom domain issues
- Verify DNS propagation (can take 24-48 hours)
- Check CNAME points to `hosting.gitbook.io`
- Ensure no conflicting records

### Content not updating
- Check for pending change requests
- Verify Git sync status
- Clear browser cache
- Check for merge conflicts

## Notes

- This skill was generated from official GitBook documentation via llms.txt
- Reference files contain 107 pages of comprehensive documentation
- Content is current as of January 2026

## Resources

- [GitBook Documentation](https://docs.gitbook.com/)
- [GitBook Status](https://status.gitbook.com/)
- [GitBook Community](https://github.com/GitbookIO)
