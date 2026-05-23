---
name: create-blog
description: Creates conversational blog posts with proper Hugo frontmatter and SEO optimization. Use when the user wants to write a blog post, draft blog content, or add an article. Supports four content types (original, curated, embed, project) with voice learning for consistent tone.
---

# Blog Post Creation Skill

Creates blog posts with conversational, personal tone using proper Hugo page bundles and SEO/AEO optimization.

## When to Use

Activate when users:
- Want to write or create a blog post
- Ask to draft blog content
- Need to add an article or entry to the blog
- Request help with blog writing

## Required Information

Gather through conversation before generating:

| Field | Description | Notes |
|-------|-------------|-------|
| **Title** | Blog post title | Clear, descriptive |
| **Content Type** | One of: original, curated, embed, project | See types below |
| **Summary** | 150-200 character description | For SEO/social |

### Content Types

- **original** - Original thoughts and analysis written by the author
- **curated** - Collected resources with personal commentary (requires attribution, source_url)
- **embed** - Embedded external content with commentary (requires attribution, source_url)
- **project** - Project-based posts sharing work and learnings

## Optional Information

- **Key Points** - Main ideas to cover in the post
- **Tags** - Categorization tags (array)
- **Categories** - Blog categories (array)
- **Attribution** - Required for curated/embed: original content creator
- **Source URL** - Required for curated/embed: link to original source

## Generation Process

### Step 1: Gather Information

Ask the user conversationally:
1. "What's the title of your blog post?"
2. "What type of content is this?" (explain options if needed)
3. "Can you give me a 1-2 sentence summary?"
4. "What are the key points you want to cover?"

For curated/embed types, also ask:
5. "Who created the original content? (attribution)"
6. "What's the source URL?"

### Step 2: Invoke Blog Agent

Run the TypeScript agent to generate the content bundle:

```bash
bun run src/agents/cli/agent-cli.ts blog \
  --title "{{title}}" \
  --type {{content_type}} \
  --summary "{{summary}}" \
  --tags "{{tags}}" \
  --key-points "{{key_points}}"
```

The agent will:
1. Load voice learning patterns from style docs at `.agents/style-docs/blog-style.json`
2. Generate Hugo content bundle at `content/blog/posts/YYYY-MM-DD-slug/index.md`
3. Create image prompts (saved in bundle metadata)
4. Create a draft review file at `.agents/drafts/blog-{slug}.review.json`
5. Output the bundle path and preview

**Example output:**
```
--- Blog Agent ---

Generating blog post...

[SUCCESS] Blog post generated

Bundle path: content/blog/posts/2026-01-26-my-post/index.md

Frontmatter: { title: "My Post", draft: true, ... }

Image prompts: ["A professional photo of..."]

--- Content Preview ---

## Introduction
...
```

### Step 3: User Review

After generation, the user should:
1. Open the generated file at the bundle path
2. Edit the content as needed (the draft is fully editable)
3. Review the structure and tone

Show the user:
- The bundle path for editing
- A preview of the generated content
- Remind them the draft is saved with `draft: true`

### Step 4: Approval Workflow

**Never auto-publish.** When the user is satisfied with the draft:

Option A: Use the approve skill
```
/approve-blog {{slug}}
```

Option B: Use the CLI directly
```bash
bun run src/agents/cli/agent-cli.ts approve --type blog --slug {{slug}}
```

This will:
1. Remove `draft: true` from the content file
2. Update the review file status to `approved`
3. The content is now ready for publishing

### Step 5: Validate (Optional)

Run validation script to check for issues:
```bash
./scripts/validate-blog-post.sh content/blog/posts/YYYY-MM-DD-slug
```

Validation checks:
- Required frontmatter fields present
- No H1 headings in content body
- Summary length 150-200 characters
- Content type-specific requirements (attribution for curated/embed)
- Image paths valid (if images included)

## Voice Learning

Record feedback to improve future content. The style system learns from:
- Positive feedback: "I love the personal stories"
- Negative feedback: "This is too formal"

Style docs location: `.agents/style-docs/blog-style.json`

## Draft Management

List all pending drafts:
```bash
bun run src/agents/cli/agent-cli.ts drafts --type blog
```

## Example Interaction

**User:** I want to write a blog post about my experience with Claude Code

**Assistant:** Great! Let me gather some details for your blog post.

1. **Title:** What would you like to call it? Something like "My Experience with Claude Code" or something more specific?

2. **Content Type:** This sounds like **original** content - your own thoughts and analysis. Does that sound right?

3. **Summary:** Can you give me a 1-2 sentence summary? (This will appear in search results and social shares)

4. **Key Points:** What main points do you want to cover?

---

**User:** Title: "Why Claude Code Changed My Workflow"
Original content
Summary: "Claude Code fundamentally changed how I approach coding. Here's what I learned after 3 months of daily use."
Key points: faster iteration, better code quality, learning new patterns

**Assistant:** I'll generate your blog post now.

```bash
bun run src/agents/cli/agent-cli.ts blog \
  --title "Why Claude Code Changed My Workflow" \
  --type original \
  --summary "Claude Code fundamentally changed how I approach coding. Here's what I learned after 3 months of daily use." \
  --key-points "faster iteration,better code quality,learning new patterns"
```

Your draft is ready at:
`content/blog/posts/2026-01-26-why-claude-code-changed-my-workflow/index.md`

Please review the generated content and make any edits. When you're satisfied, run `/approve-blog why-claude-code-changed-my-workflow` to publish.

## File Locations

| Resource | Path |
|----------|------|
| Blog posts | `content/blog/posts/` |
| Draft review files | `.agents/drafts/` |
| Style documentation | `.agents/style-docs/blog-style.json` |
| Blog Agent | `src/agents/blog/blog-agent.ts` |
| Validation script | `scripts/validate-blog-post.sh` |
| Content types | `data/content_types.yaml` |
