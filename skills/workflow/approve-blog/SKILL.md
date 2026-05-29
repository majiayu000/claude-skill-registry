---
name: approve-blog
description: Approves a blog post draft for publishing by removing the draft flag. Use when the user says "approve", "publish", or "I'm done editing" a blog post.
args:
  - name: slug
    description: The slug of the blog post to approve (e.g., "my-post-title")
    required: true
---

# Approve Blog Post Skill

Approves a blog post draft for publishing by removing `draft: true` from the frontmatter.

## When to Use

Activate when users:
- Say they're done editing a blog draft
- Want to approve or publish a blog post
- Ask to remove the draft flag from a blog post

## Usage

```
/approve-blog <slug>
```

Where `<slug>` is the URL-friendly identifier of the blog post (e.g., `my-post-title`).

## Process

### Step 1: Verify the Draft Exists

Check that a draft review file exists:
```bash
cat .agents/drafts/blog-{{slug}}.review.json
```

If not found, list available drafts:
```bash
bun run src/agents/cli/agent-cli.ts drafts --type blog
```

### Step 2: Approve the Draft

Run the approve command:
```bash
bun run src/agents/cli/agent-cli.ts approve --type blog --slug {{slug}}
```

This will:
1. Read the draft review file at `.agents/drafts/blog-{{slug}}.review.json`
2. Find the content file at the stored bundle path
3. Replace `draft: true` with `draft: false` in the frontmatter
4. Update the review file status to `approved`

### Step 3: Confirm Approval

Show the user:
- Confirmation that the draft was approved
- The bundle path of the approved content
- Next steps (e.g., commit and deploy)

## Example

**User:** /approve-blog my-experience-with-claude-code

**Assistant:** Approving the blog post...

```bash
bun run src/agents/cli/agent-cli.ts approve --type blog --slug my-experience-with-claude-code
```

Your blog post has been approved and is ready for publishing:
- Bundle path: `content/blog/posts/2026-01-26-my-experience-with-claude-code/index.md`
- The `draft: true` flag has been removed

To publish, commit and deploy your changes:
```bash
git add content/blog/posts/2026-01-26-my-experience-with-claude-code/
git commit -m "Publish: My Experience with Claude Code"
git push
```

## Related Skills

- `/create-blog` - Create a new blog post draft
