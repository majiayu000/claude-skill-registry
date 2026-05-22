---
name: convex-file-storage
description: Use Convex file storage correctly for uploads, references, and retrieval. Use when implementing file or attachment flows.
version: 1.0.0
metadata:
  author: agentforge
  source: waynesutton/convexskills and repo docs
---

# Convex File Storage

Use this skill when a task touches uploads, stored files, attachment metadata, or file lifecycle.

## Rules

- Use real Convex storage APIs such as upload URL generation.
- Store metadata and references explicitly in tables.
- Do not fake upload state with placeholder URLs.
- Consider pagination and cleanup for large file collections.
