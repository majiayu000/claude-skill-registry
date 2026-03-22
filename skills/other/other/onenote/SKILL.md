---
name: onenote
description: >-
  Create, read, and manage OneNote notebooks, sections, and pages via Microsoft Graph API.
  Use when someone asks to "create OneNote pages", "read OneNote notes", "automate OneNote",
  "save to OneNote", "extract OneNote content", "organize OneNote notebooks", or "OneNote API".
  Covers notebooks, sections, pages (create with HTML), content extraction, and search.
license: Apache-2.0
compatibility: "Microsoft Graph API v1.0. Requires Microsoft 365 account with OneNote."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["onenote", "microsoft-365", "notes", "graph-api", "api"]
---

# OneNote

## Overview

This skill helps AI agents integrate with Microsoft OneNote via the Graph API. It covers creating and managing notebooks, sections, and pages, generating rich page content with HTML, extracting text and images, and searching across notes.

## Instructions

### Authentication

```typescript
// Same Azure AD app as other Microsoft 365 services
// Permissions needed:
//   Notes.ReadWrite — read/write user's notebooks
//   Notes.ReadWrite.All — access all notebooks (admin)
//   Notes.Create — create only

import { Client } from '@microsoft/microsoft-graph-client';
// ... same auth setup as other Graph API skills
```

### Notebooks & Sections

```typescript
// List notebooks
const notebooks = await graphClient.api(`/users/${userId}/onenote/notebooks`)
  .select('id,displayName,createdDateTime,lastModifiedDateTime')
  .get();

// Create notebook
const notebook = await graphClient.api(`/users/${userId}/onenote/notebooks`)
  .post({ displayName: 'Project Notes' });

// List sections in a notebook
const sections = await graphClient
  .api(`/users/${userId}/onenote/notebooks/${notebookId}/sections`)
  .select('id,displayName')
  .get();

// Create section
const section = await graphClient
  .api(`/users/${userId}/onenote/notebooks/${notebookId}/sections`)
  .post({ displayName: 'Meeting Notes' });

// Create section group (for organizing sections)
const group = await graphClient
  .api(`/users/${userId}/onenote/notebooks/${notebookId}/sectionGroups`)
  .post({ displayName: 'Q1 2026' });
```

### Create Pages

OneNote pages are created using HTML. The API accepts a subset of HTML with OneNote-specific data attributes.

```typescript
// Simple page
await graphClient.api(`/users/${userId}/onenote/sections/${sectionId}/pages`)
  .header('Content-Type', 'application/xhtml+xml')
  .post(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Sprint 14 Standup — March 1, 2026</title>
      <meta name="created" content="2026-03-01T09:30:00-05:00" />
    </head>
    <body>
      <h1>Sprint 14 Daily Standup</h1>
      <p>Date: March 1, 2026 | Attendees: Sarah, Mike, Dani</p>
      
      <h2>Sarah</h2>
      <ul>
        <li><b>Yesterday:</b> Completed payment retry logic PR #142</li>
        <li><b>Today:</b> Start integration tests for retry flow</li>
        <li><b>Blockers:</b> None</li>
      </ul>
      
      <h2>Mike</h2>
      <ul>
        <li><b>Yesterday:</b> Reviewed 3 PRs, fixed CI flakiness</li>
        <li><b>Today:</b> Dashboard performance optimization</li>
        <li><b>Blockers:</b> Need access to production Datadog</li>
      </ul>
      
      <h2>Action Items</h2>
      <ul>
        <li data-tag="to-do">Grant Mike Datadog access — Sarah</li>
        <li data-tag="to-do">Schedule sprint demo for Friday — Dani</li>
      </ul>
      
      <h2>Notes</h2>
      <p>Sprint velocity tracking at 38 points, capacity is 42. On track for all commitments.</p>
    </body>
    </html>
  `);

// Page with table
await graphClient.api(`/users/${userId}/onenote/sections/${sectionId}/pages`)
  .header('Content-Type', 'application/xhtml+xml')
  .post(`
    <!DOCTYPE html>
    <html>
    <head><title>Weekly Metrics</title></head>
    <body>
      <h1>Weekly Metrics — Feb 24-28, 2026</h1>
      <table border="1">
        <tr><th>Metric</th><th>Value</th><th>Target</th><th>Status</th></tr>
        <tr><td>Revenue</td><td>$98,200</td><td>$90,000</td><td>✅ Above</td></tr>
        <tr><td>Sign-ups</td><td>142</td><td>150</td><td>⚠️ Below</td></tr>
        <tr><td>Churn</td><td>0.4%</td><td>0.5%</td><td>✅ Below</td></tr>
        <tr><td>NPS</td><td>72</td><td>65</td><td>✅ Above</td></tr>
      </table>
    </body>
    </html>
  `);

// Page with image from URL
await graphClient.api(`/users/${userId}/onenote/sections/${sectionId}/pages`)
  .header('Content-Type', 'application/xhtml+xml')
  .post(`
    <!DOCTYPE html>
    <html>
    <head><title>Architecture Diagram</title></head>
    <body>
      <h1>System Architecture — v2</h1>
      <img src="https://example.com/architecture-diagram.png" alt="Architecture diagram" />
      <p>Updated March 2026. Changes: added Redis cache layer, split API gateway.</p>
    </body>
    </html>
  `);
```

#### OneNote HTML Tags Reference

Key `data-tag` values: `to-do`, `important`, `question`, `remember-for-later`, `definition`, `highlight`, `contact`, `idea`, `critical`, `project-a`, `project-b`. Use `<meta name="created" content="2026-03-01T09:00:00-05:00" />` for timestamps. Standard `<ul>` nesting creates indented outlines.

### Read Pages

```typescript
// List pages in a section
const pages = await graphClient
  .api(`/users/${userId}/onenote/sections/${sectionId}/pages`)
  .select('id,title,createdDateTime,lastModifiedDateTime')
  .orderby('lastModifiedDateTime DESC')
  .top(50)
  .get();

// Get page content (returns HTML)
const pageContent = await graphClient
  .api(`/users/${userId}/onenote/pages/${pageId}/content`)
  .get();
// Returns full HTML of the page

// Get page metadata
const pageMeta = await graphClient
  .api(`/users/${userId}/onenote/pages/${pageId}`)
  .select('id,title,createdDateTime,lastModifiedDateTime,contentUrl')
  .get();
```

### Update Pages

```typescript
// Append content to existing page
await graphClient.api(`/users/${userId}/onenote/pages/${pageId}/content`)
  .patch([
    {
      target: 'body',
      action: 'append',
      position: 'after',
      content: '<h2>Update — March 2</h2><p>Sprint demo completed successfully. All 3 features demoed.</p>',
    },
  ]);

// Replace specific element
await graphClient.api(`/users/${userId}/onenote/pages/${pageId}/content`)
  .patch([
    {
      target: '#status-section', // Element with data-id="status-section"
      action: 'replace',
      content: '<p data-id="status-section">Status: <b>Complete</b> ✅</p>',
    },
  ]);

// Prepend content
await graphClient.api(`/users/${userId}/onenote/pages/${pageId}/content`)
  .patch([
    {
      target: 'body',
      action: 'prepend',
      content: '<p style="color:red;"><b>⚠️ UPDATED: See new figures below</b></p>',
    },
  ]);
```

### Search

```typescript
// Search across all OneNote content
const results = await graphClient
  .api(`/users/${userId}/onenote/pages`)
  .filter("contains(title, 'standup')")
  .select('id,title,createdDateTime,parentSection')
  .expand('parentSection($select=displayName)')
  .orderby('lastModifiedDateTime DESC')
  .get();

// Full-text search via Microsoft Search API
const searchResults = await graphClient.api('/search/query')
  .post({
    requests: [{
      entityTypes: ['driveItem'],
      query: { queryString: 'filetype:one AND "sprint planning"' },
      size: 20,
    }],
  });
```

### Common Patterns

## Examples

### Example 1: Create structured meeting notes in OneNote
**User prompt:** "Create a OneNote page in my Engineering notebook's Sprint section for today's sprint retrospective. Attendees are Marcus, Jenna, and Priya. We discussed what went well with the payment migration and what to improve in CI pipeline times."

The agent will use the Graph API to first look up the notebook named "Engineering" via `GET /onenote/notebooks?$filter=displayName eq 'Engineering'`, find the "Sprint" section, then create a new page via `POST /onenote/sections/{sectionId}/pages` with XHTML content. The page HTML includes a `<title>Sprint 14 Retrospective — February 18, 2026</title>`, a `<meta name="created">` timestamp, an `<h1>` header, attendee list, an `<h2>What Went Well</h2>` section with bullet points about the payment migration completing 2 days ahead of schedule, an `<h2>What to Improve</h2>` section noting CI pipeline averaging 18 minutes (target: under 10), and an `<h2>Action Items</h2>` with `data-tag="to-do"` items like "Marcus: investigate parallel test execution to cut CI time" and "Priya: document payment migration rollback procedure."

### Example 2: Search OneNote and append updates to an existing page
**User prompt:** "Find my OneNote page titled 'Q1 OKR Tracker' and append a progress update for the 'reduce churn' objective — we hit 2.1% churn this month, down from 2.8% in January."

The agent will search for the page using `GET /onenote/pages?$filter=contains(title, 'Q1 OKR Tracker')&$select=id,title,parentSection`, retrieve the page ID, then call `PATCH /onenote/pages/{pageId}/content` with a JSON body targeting `body` with action `append` and position `after`. The appended HTML content is `<h2>Update — February 18, 2026</h2><p><b>Reduce Churn Objective:</b> Monthly churn dropped to 2.1%, down from 2.8% in January. On track to hit Q1 target of 1.8%.</p><p data-tag="important">Key driver: improved onboarding flow launched Feb 3 reduced 30-day churn by 25%.</p>`.

## Guidelines

- Pages are created with HTML — use valid XHTML (close all tags, quote attributes)
- OneNote API supports a subset of HTML — stick to basic tags (h1-h6, p, ul, ol, table, img, b, i)
- Use `data-tag` attributes for to-do items, important notes, etc. — renders as OneNote tags
- Set `<title>` in HTML head — it becomes the page title in OneNote
- Use `<meta name="created">` to set custom creation timestamps
- Page updates use PATCH with target/action arrays — not full HTML replacement
- Images can be inline (base64 in multipart request) or URL references
- Search works on page titles via `$filter`; for full-text, use Microsoft Search API
- Rate limits: same as other Graph API resources (10,000 per 10 min)
- OneNote pages are stored in OneDrive — large notebooks count against storage quota
