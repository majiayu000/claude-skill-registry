---
name: publish
description: "Prepare a completed article for publishing on Substack or Medium. Formats the draft, checks all image paths, and presents for manual approval. REQUIRES explicit user approval before any publishing action."
disable-model-invocation: true
allowed-tools: Read, Glob
---

# Publish Preparation Skill

## Input
$ARGUMENTS = topic name

## Process

### Step 1: Load the Draft
Read drafts/<topic-slug>.md
Verify it exists and is complete.

### Step 2: Format for Substack/Medium
- Verify all image paths point to existing .png files in figures/output/
- Convert relative image paths to the format needed for the platform
- Add a compelling subtitle/deck (1 sentence summary)
- Add a "Further Reading" section with links to key sources
- Add a call-to-action at the end:
  "If you found this helpful, consider subscribing for more deep dives
  into the architectures behind modern AI."

### Step 3: Quality Final Check
Verify one more time:
- No em dashes in the entire document
- All figures referenced and files exist
- Consistent formatting throughout
- No broken markdown
- Spelling and grammar pass

### Step 4: Present to User for Approval
Show the user:
```
Article Ready for Publishing
=============================
Title: <title>
Subtitle: <subtitle>
Word Count: <count>
Figure Count: <count>
Sections: <list of section titles>

Preview (first 3 paragraphs):
<preview text>

Draft location: drafts/<topic-slug>.md
Figures location: figures/output/

ACTION REQUIRED: Please review the full draft and confirm publishing.
```

### IMPORTANT
- NEVER auto-publish. Always wait for explicit user approval.
- This skill can ONLY be invoked manually (disable-model-invocation: true).
- After user approves, copy the final version to published/<topic-slug>.md
