---
name: write-tickets-publish-to-jira
description: Publish a ticket to JIRA using acli. Converts markdown to ADF, creates the ticket, and sets component/sprint. Called by write-tickets after ticket content is finalized in a temp file. Not intended for direct user invocation.
user-invocable: false
---

# Publish Ticket to JIRA

Create a JIRA ticket from a finalized markdown temp file. This skill runs inline (not as a subagent) so you retain full context.

## Prerequisites

- `acli` installed and in PATH
- Authenticated: `acli jira auth status` should succeed
- If not authenticated, run `acli jira auth login --web` and tell the user to complete the browser auth flow

## Inputs

When this skill is invoked by `write-tickets`, you already have:

| Input | Source |
|-------|--------|
| **Title** | The ticket title from the plan |
| **Issue type** | `Story`, `Bug`, `Task`, or `Improvement` |
| **Project key** | e.g., `RETIRE` |
| **Component ID** | e.g., `17013` for Consumer |
| **Sprint ID** | e.g., `17210` for Mobile Refinement |
| **Markdown content** | Read from the temp file (user may have edited it) |

## Workflow

### Step 1: Check auth

```bash
acli jira auth status
```

If this fails, tell the user to authenticate and stop.

### Step 2: Convert markdown to ADF JSON

Build an ADF (Atlassian Document Format) JSON object from the markdown content. The description field MUST be ADF — raw markdown will not render in JIRA.

**Conversion rules:**

| Markdown | ADF node type |
|----------|---------------|
| `## Heading` | `heading` with `attrs.level: 2` |
| `### Heading` | `heading` with `attrs.level: 3` |
| Plain paragraph | `paragraph` |
| `- item` (bullet list) | `bulletList` > `listItem` > `paragraph` |
| `1. item` (ordered list) | `orderedList` > `listItem` > `paragraph` |
| `- [ ] item` (checkbox) | `bulletList` > `listItem` > `paragraph` with `☐ ` prefix text |
| `- [x] item` (checked) | `bulletList` > `listItem` > `paragraph` with `☑ ` prefix text |
| `` `code` `` (inline) | `text` with `marks: [{"type": "code"}]` |
| `**bold**` | `text` with `marks: [{"type": "strong"}]` |
| `[text](url)` | `text` with `marks: [{"type": "link", "attrs": {"href": "url"}}]` |
| `**[text](url)**` | `text` with both `strong` and `link` marks |
| Code block | `codeBlock` with `attrs.language` |
| Horizontal rule | `rule` |

**ADF skeleton:**

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    // ... converted nodes here
  ]
}
```

**Common node patterns:**

Heading:
```json
{"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": "Summary"}]}
```

Paragraph with mixed formatting:
```json
{
  "type": "paragraph",
  "content": [
    {"type": "text", "text": "Plain text "},
    {"type": "text", "text": "bold part", "marks": [{"type": "strong"}]},
    {"type": "text", "text": " and "},
    {"type": "text", "text": "linked text", "marks": [{"type": "link", "attrs": {"href": "https://example.com"}}]}
  ]
}
```

Bullet list:
```json
{
  "type": "bulletList",
  "content": [
    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Item one"}]}]},
    {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Item two"}]}]}
  ]
}
```

### Step 3: Build the workitem JSON

Write the full JSON to `/tmp/jira-workitem.json`:

```json
{
  "projectKey": "RETIRE",
  "type": "Bug",
  "summary": "The ticket title",
  "description": { ... ADF object from Step 2 ... }
}
```

### Step 4: Create the ticket

```bash
acli jira workitem create --from-json /tmp/jira-workitem.json
```

**Parse the output** to extract the JIRA key (e.g., `RETIRE-2849`). The key is typically printed in the command output.

If the command fails:
- Check if it's an auth issue → tell user to re-authenticate
- Check if it's a validation error → inspect the error, fix the JSON, retry
- If it fails after 2 retries → fall back (see Fallback section below)

### Step 5: Set component and sprint

After the ticket is created, set component and sprint via edit:

```bash
acli jira workitem edit --key RETIRE-XXXX --component "Consumer"
```

For sprint, use the custom field:

```bash
acli jira workitem edit --key RETIRE-XXXX --custom "customfield_10020=17210"
```

If these edits fail, note it to the user but don't fail the whole operation — the ticket is already created.

### Step 6: Clean up

Delete `/tmp/jira-workitem.json` after successful creation.

### Step 7: Return result

Return the JIRA key to the calling workflow. Format as a link when displaying to the user:
`[RETIRE-XXXX](https://gustohq.atlassian.net/browse/RETIRE-XXXX)`

## Fallback

If `acli` creation fails after retries, offer to copy the original markdown to the clipboard:

```
AskQuestion({
  "title": "JIRA Creation Failed",
  "questions": [{
    "id": "fallback",
    "prompt": "Failed to create ticket via acli. Copy markdown to clipboard for manual paste?",
    "options": [
      {"id": "copy", "label": "Yes, copy to clipboard"},
      {"id": "skip", "label": "Skip this ticket"},
      {"id": "retry", "label": "Try again"}
    ]
  }]
})
```

If "copy" selected: `pbcopy < /tmp/ticket-N-slug.md` (the temp file from write-tickets).

## Strict Rules

- **Always check auth first.** Don't attempt creation if not authenticated.
- **Always use ADF for descriptions.** Raw markdown will not render correctly in JIRA.
- **Parse inline formatting.** Don't dump markdown syntax into ADF text nodes — convert `**bold**` to strong marks, `[text](url)` to link marks, `` `code` `` to code marks.
- **Clean up temp files.** Delete `/tmp/jira-workitem.json` after creation.
- **Don't swallow errors.** If component/sprint edit fails, tell the user which field failed.
- **Return the JIRA key.** The calling workflow needs it for cross-references between tickets.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Putting raw markdown in ADF text nodes | Convert to proper ADF nodes and marks |
| Forgetting to parse inline `**bold**`, `[links](url)`, `` `code` `` | Split text at formatting boundaries, apply marks to each segment |
| Not checking auth before creating | Always run `acli jira auth status` first |
| Not parsing the JIRA key from output | Read acli output carefully for the key |
| Leaving `/tmp/jira-workitem.json` behind | Delete after successful creation |
| Failing silently on component/sprint edit | Report which fields failed but don't block |
| Using `--description` flag with markdown | Use `--from-json` with ADF — it's the only reliable approach |
