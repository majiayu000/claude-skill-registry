---
name: storage
description: File storage - uploads, CDN, blobs. Use when handling files.
---

# Storage Guideline

## Tech Stack

* **Storage**: Vercel Blob
* **Framework**: Next.js (with Turbopack)
* **Platform**: Vercel

## Non-Negotiables

* All file uploads must be validated (type, size, content)
* Signed URLs for private content access
* No user-uploaded content served from main domain (XSS prevention)
* File deletion must cascade with parent entity deletion

## Context

File storage is deceptively complex. Users expect uploads to just work, but there are many ways for it to fail — large files, slow connections, wrong formats, malicious content.

Vercel Blob is the SSOT for file storage. No custom implementations.

## Driving Questions

* What happens when an upload fails halfway?
* How are large files handled without blocking?
* What file types are allowed and how is it enforced?
* How long are files retained after entity deletion?
* What's the storage cost and is it sustainable?
