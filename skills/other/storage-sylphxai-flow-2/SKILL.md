---
name: storage
description: File storage - uploads, CDN, blobs. Use when handling files.
---

# Storage Guideline

## Tech Stack

* **Storage**: Vercel Blob
* **Platform**: Vercel

## Non-Negotiables

* Uploads must be intent-based and server-verified (no direct client uploads to permanent storage)
* Server must validate blob ownership before attaching to resources
* Abandoned uploads must be cleanable

## Context

File uploads are a common attack vector. Users upload things you don't expect. Files live longer than you plan. Storage costs accumulate quietly. A well-designed upload system is secure, efficient, and maintainable.

Consider: what could a malicious user upload? What happens to files when the referencing entity is deleted? How does storage cost scale with usage?

## Driving Questions

* What could a malicious user do through the upload flow?
* What happens to orphaned files when entities are deleted?
* How much are we spending on storage, and is it efficient?
* What file types do we accept, and should we?
* How do we handle upload failures gracefully?
* What content validation exists (type, size, safety)?
