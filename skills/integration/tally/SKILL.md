---
name: tally
description: Use when submitting to Tally forms or discovering form field structure. Handles field discovery via WebFetch and guides manual submission (no API for external form submission).
---

# Tally Forms

Form builder platform. Two operations: **discover** form fields, **submit** to forms.

> **No submission API:** Tally's API is for form *owners*. Submitting to external forms requires manual paste. See [reference/api-research.md](./reference/api-research.md).

## Operations

### Discover Form Fields

Find the field structure for any Tally form.

**Input:** Form URL (e.g., `https://tally.so/r/nrvBY2`)

**Step 1: Fetch the form**

```
WebFetch:
  url: https://tally.so/r/<formId>
  prompt: "Extract the form structure: form ID, field names, field IDs (UUIDs),
           field types, required status, placeholders, and any hidden fields"
```

**Step 2: Parse the response**

Look for:
- `formId` and `workspaceId` in the page data
- Field blocks with UUIDs (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
- Field types: `textarea`, `email`, `text`, `number`, `dropdown`, etc.
- Required indicators
- Placeholder text (helps identify field purpose)

**Step 3: Output the structure**

```
Form: <form name>
URL: https://tally.so/r/<formId>

| Field | Type | Required | Placeholder |
|-------|------|----------|-------------|
| <label> | textarea | Yes | "Enter URLs..." |
| <label> | email | No | "john@example.com" |
```

**Example** (Ref's doc request form):

```
Form: Add docs to Ref
URL: https://tally.so/r/nrvBY2

| Field | Type | Required | Placeholder |
|-------|------|----------|-------------|
| What docs would you like indexed? | textarea | Yes | "https://react.dev, ..." |
| Email | email | No | "john.smith@acme.com" |
```

---

### Submit to Form

Guide user through manual submission to a Tally form.

**Input:**
- `formId`: From URL (e.g., `nrvBY2`)
- `fields`: Array of `{ name, value }` pairs

**Step 1: Display submission details**

Output in copy-friendly format (no side borders):

```
═══════════════════════════════════════════════
📋 TALLY FORM SUBMISSION
═══════════════════════════════════════════════

Form: https://tally.so/r/<formId>

── Field: <field1.name> ──

<field1.value>

── Field: <field2.name> ──

<field2.value>

═══════════════════════════════════════════════
```

**Step 2: Direct user**

1. Open the form URL
2. Copy each field value from above
3. Paste into corresponding form field
4. Submit

---

## URL Prefill (Limited)

Tally supports URL parameter prefill **only if the form owner configured hidden fields**.

Format: `https://tally.so/r/<formId>?field1=value1&field2=value2`

**Requirements:**
- Form owner must add hidden field blocks
- Hidden field names must match URL params exactly (case-sensitive)
- Hidden fields must be linked to visible fields via "default answer"

**If not configured:** URL params are ignored. Manual paste is the only option.

---

## Key URLs

| URL | Purpose |
|-----|---------|
| https://tally.so | Tally homepage |
| https://tally.so/r/{formId} | Form submission URL |
| https://developers.tally.so | API docs (for form owners) |
| https://tally.so/help/hidden-fields | Hidden fields guide |
| https://tally.so/help/pre-populate-form-fields | Prefill guide |

---

## When to Use This Skill

| Scenario | Operation |
|----------|-----------|
| Need to submit to a Tally form | Submit to Form |
| Need to find field names/IDs for a form | Discover Form Fields |
| Building a skill that uses a Tally form | Discover first, then document in your skill |
| Checking if URL prefill is possible | Discover fields, look for hidden field config |

## Reference

- [API Research](./reference/api-research.md) — What Tally's API can/can't do
