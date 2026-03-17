---
name: obsidian-issue-from-doc
description: Convert Obsidian documents into GitHub-ready issues with structured format. Use when transforming specs or design docs into actionable GitHub issues.
---

# Obsidian Issue From Doc Skill

Convert canonical Obsidian documents into well-structured GitHub issues.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Transform Obsidian documentation into GitHub issues with clear problem statements, goals, acceptance criteria, and implementation context.

## Background Knowledge

### Why Convert Documents to Issues?

Documentation captures decisions and specifications. Issues drive implementation. Converting docs to issues:

- Creates actionable work items from specifications
- Maintains traceability from design to implementation
- Ensures consistent issue quality
- Reduces manual issue writing effort

### Issue Quality Standards

GitHub issues generated from documents should be:

- **Self-contained**: All context included, no external knowledge required
- **Actionable**: Clear next steps for implementation
- **Testable**: Acceptance criteria that can be verified
- **Scoped**: Focused on a single deliverable

### Document Types and Issue Mapping

| Document Type | Issue Type | Focus |
|--------------|------------|-------|
| Specification | Feature | Implement specified behavior |
| Design doc | Epic/Feature | Implement design decisions |
| Bug analysis | Bug fix | Resolve identified issue |
| Proposal | RFC/Discussion | Gather feedback before implementation |

## Input Sources

The skill accepts:

- **Document path**: Obsidian document to convert
- **Repository**: Target GitHub repository
- **Labels**: Optional labels to apply
- **Milestone**: Optional milestone assignment

## Output Contract

Produce a GitHub-ready issue structure:

```json
{
  "source_document": "specs/feature-x.md",
  "issue": {
    "title": "Implement Feature X",
    "body": "[Formatted issue body - see template below]",
    "labels": ["enhancement", "spec-derived"],
    "milestone": "v1.0"
  },
  "metadata": {
    "document_status": "canonical",
    "document_updated": "2026-01-18",
    "wikilinks_referenced": ["[[related-spec]]", "[[design-doc]]"],
    "files_likely_affected": ["src/feature-x/", "tests/feature-x/"]
  }
}
```

### Issue Body Template

```markdown
## Summary

[One paragraph describing the feature/fix and its purpose]

## Problem Statement

[What problem does this solve? Why is it needed?]

## Goal / Definition of Done

[Clear statement of what "done" looks like]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Context

### Files/Systems Likely Affected

- `path/to/file1`
- `path/to/directory/`

### Dependencies

- Depends on: #issue-number (if applicable)
- Related: #issue-number

### Implementation Notes

[Any specific guidance from the source document]

---

**Source**: [document-name.md](link-to-document)
```

## Workflow

### 1. Read Source Document

Load and parse the Obsidian document:

```bash
# Read the document
cat /path/to/vault/specs/feature-x.md

# Extract frontmatter status
grep -A5 "^---" /path/to/vault/specs/feature-x.md | grep "status:"
```

### 2. Extract Issue Components

From the document, identify:

**Title**: Derive from document title or first H1
```markdown
# Authentication Specification
-> "Implement Authentication System"
```

**Problem Statement**: Look for sections like:
- "Problem", "Background", "Motivation"
- Opening paragraph describing the need

**Goal**: Look for sections like:
- "Goal", "Objective", "Outcome"
- "Definition of Done", "Success Criteria"

**Acceptance Criteria**: Look for:
- Bulleted lists of requirements
- "Requirements" or "Criteria" sections
- Testable statements

**Technical Context**: Look for:
- File paths or code references
- System/component names
- Dependencies and relationships

### 3. Identify Affected Files

Scan document for file/path references:

```bash
# Look for file paths in document
grep -oE "[a-zA-Z0-9_-]+/[a-zA-Z0-9_/-]+\.(ts|js|py|go|rs|md)" document.md

# Look for component/system names
grep -oE "(component|service|module|handler)[s]?:" document.md
```

### 4. Format Issue Body

Assemble components into the issue template:

1. Write summary paragraph
2. Extract or synthesize problem statement
3. Define goal/done criteria
4. List acceptance criteria as checkboxes
5. Add technical context
6. Link to source document

### 5. Validate Issue Quality

Before output, verify:

- [ ] Title is concise and actionable
- [ ] Problem statement explains the "why"
- [ ] Goal is measurable
- [ ] Acceptance criteria are testable
- [ ] Technical context provides implementation guidance
- [ ] Source document is referenced

## Example: Spec to Issue

**Input document: `specs/user-logout.md`**

```markdown
---
created: 2026-01-15
updated: 2026-01-18
status: canonical
---

# User Logout Specification

Users need the ability to securely log out of their session.

## Problem

Currently, users cannot end their session without closing the browser. This is a security concern for shared devices and does not meet user expectations.

## Requirements

- Logout button visible in header navigation
- Clicking logout clears session token
- User redirected to login page after logout
- Confirmation not required (one-click logout)

## Technical Notes

The session token is stored in localStorage under `auth_token`. The header component is in `src/components/Header.tsx`. Authentication state is managed by `src/contexts/AuthContext.tsx`.

## Related

- [[specs/authentication]] - Main auth specification
- [[design/session-handling]] - Session lifecycle design

---

## Sources

- [[_inbox/logout-request.md]]
```

**Output issue:**

```json
{
  "source_document": "specs/user-logout.md",
  "issue": {
    "title": "Implement user logout functionality",
    "body": "## Summary\n\nImplement a secure logout feature that allows users to end their session with a single click from the header navigation.\n\n## Problem Statement\n\nCurrently, users cannot end their session without closing the browser. This is a security concern for shared devices and does not meet user expectations for session management.\n\n## Goal / Definition of Done\n\nUsers can log out of their session via a visible button in the header, with immediate session termination and redirect to login.\n\n## Acceptance Criteria\n\n- [ ] Logout button is visible in header navigation\n- [ ] Clicking logout clears the session token from localStorage\n- [ ] User is redirected to login page after logout\n- [ ] Logout is one-click (no confirmation dialog required)\n\n## Technical Context\n\n### Files/Systems Likely Affected\n\n- `src/components/Header.tsx` - Add logout button\n- `src/contexts/AuthContext.tsx` - Implement logout action\n- `localStorage` - Clear `auth_token` key\n\n### Dependencies\n\n- Related: Authentication specification\n- Related: Session handling design\n\n### Implementation Notes\n\nThe session token is stored in localStorage under `auth_token`. Clear this value and reset the auth context state on logout.\n\n---\n\n**Source**: specs/user-logout.md",
    "labels": ["enhancement", "authentication"],
    "milestone": null
  },
  "metadata": {
    "document_status": "canonical",
    "document_updated": "2026-01-18",
    "wikilinks_referenced": ["[[specs/authentication]]", "[[design/session-handling]]"],
    "files_likely_affected": ["src/components/Header.tsx", "src/contexts/AuthContext.tsx"]
  }
}
```

## Issue Types

### Feature Issue (from Spec)

- Title: "Implement [feature name]"
- Focus on requirements and acceptance criteria
- Include technical implementation guidance

### Bug Fix Issue (from Analysis)

- Title: "Fix: [bug description]"
- Focus on root cause and expected vs. actual behavior
- Include reproduction steps if available

### Epic Issue (from Design Doc)

- Title: "[Epic name]"
- Higher-level description
- May reference sub-issues to create
- Focus on overall goal and scope

## Policies

### Always

- Include source document reference in issue body
- Make acceptance criteria testable and specific
- Extract file paths when mentioned in documents
- Note document status (draft issues need review)
- Preserve technical context from source

### Never

- Create issues from draft documents without flagging
- Fabricate acceptance criteria not in source document
- Omit the source document link
- Create issues that are too broad to implement
- Include internal wikilinks in GitHub issue body (convert to plain text)

### Draft Document Handling

If source document status is `draft`:

1. Flag the issue output as draft-derived
2. Add warning in issue body
3. Recommend document review before issue creation

```markdown
> **Note**: This issue was generated from a draft document.
> Review the source specification before implementation.
```

### Link Conversion

Wikilinks must be converted for GitHub:

```markdown
# In Obsidian document
See [[specs/authentication]] for details.

# In GitHub issue
See the Authentication specification for details.
```

## Integration

This skill works with:

- `obsidian-read-context` - Understand document relationships
- `obsidian-extract-inbox` - Proposals may become issues
- `obsidian-write-document` - Documents are issue sources
- `github-issues` - Actually create the issue in GitHub

## Output Format

When run, report:

1. Source document analyzed
2. The structured issue JSON
3. Warnings (draft status, missing sections, etc.)
4. Suggested labels based on content
5. Ready/not-ready status for GitHub creation
6. Command to create issue (if ready):
   ```bash
   gh issue create --title "..." --body "..." --label "..."
   ```
