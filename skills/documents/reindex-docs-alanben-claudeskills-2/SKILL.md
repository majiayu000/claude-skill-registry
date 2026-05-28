---
name: reindex-docs
description: Re-index all PDF and HTML documents, update index.html, and commit/push changes to the repository
---

# Reindex Documents Skill

You are a specialized agent for maintaining the document index in this static document repository.

## Your Task

Re-index all PDF and HTML documents in the repository and update index.html, then commit and push the changes.

## Process Steps

1. **Scan for all documents**
   - Use Glob to find all PDF files: `**/*.pdf`
   - Use Glob to find all HTML files: `**/*.html`
   - Run these searches in parallel for efficiency

2. **Read current index.html**
   - Read the existing index.html to understand the structure
   - Note the current documentTree JavaScript object structure

3. **Update index.html with new documents**
   - Update the `last-updated` date to today's date (format: YYYY-MM-DD)
   - Update the `documentTree` object to include:
     - All newly found documents
     - Proper Client → Project → Section → Folder hierarchy
     - Documents sorted in **reverse chronological order** (newest first)
     - Clean, readable document titles
     - Relative paths from root

4. **Organizational Rules**
   - **Clients** (top level): Turnbuckle, Nextgen, Loeries, MachinaXX, etc.
   - **Projects** (under clients): RentaStore, Adstream, LifeGauge, etc.
   - **Sections** (under projects): Meeting notes, Technical, Projects, Programs, etc.
   - **Folders** (under sections): Webstream, Phase 4, Modernization Program, etc.
   - **Documents**: Individual PDF and HTML files
   - Sort documents by date in reverse chronological order (most recent first)
   - Remove any empty folders that have no documents

5. **Commit and Push**
   - Add all untracked files (new documents)
   - Commit index.html changes with descriptive message
   - Commit new document files with descriptive message
   - Push all commits to remote repository
   - Use proper commit message format with Claude Code attribution

## Commit Message Format

Use this format for commits:

```
Update index with new documents - [Month Year]

Added/Updated documents:
- Client/Project: Document description
- Client/Project: Document description

Updated last modified date to YYYY-MM-DD

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

For new document files:

```
Add new client documents - [Month Year]

New documents added:
- Client/Project: Document description
- Client/Project: Document description

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Important Notes

- Exclude these HTML files from the document index (they are system files):
  - `index.html` (the index itself)
  - `repos.html` (repository index)
  - `access-denied.html` (security page)
- Maintain the existing JavaScript structure and styling
- Preserve the auth.js script reference in the head section
- Keep sections collapsed by default for clean navigation
- Use relative paths for all document links
- Follow the existing naming conventions for document titles

## Expected Output

After completion, provide a summary of:
- Number of new documents added
- Number of clients/projects updated
- Commit IDs created
- Confirmation that changes were pushed successfully
