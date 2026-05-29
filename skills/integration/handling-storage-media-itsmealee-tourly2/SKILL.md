---
name: handling-storage-media
description: Manages Appwrite Storage for buckets, permissions, and image previews. Use when handling file uploads or displaying gallery images.
---

# Storage and Media Handling

## When to use this skill
- Managing tour images.
- Implementing user profile avatars.
- Generating thumbnails/previews.

## Workflow
- [ ] Create buckets in Appwrite (e.g., `tours`, `avatars`).
- [ ] Set permissions (e.g., Public Read for tours).
- [ ] Use `storage.getFileView()` or `storage.getFilePreview()` for URLs.

## Rules
- **Max Size**: 5MB for images.
- **Allowed Types**: jpg, png, webp.
- **Optimization**: Use Appwrite's built-in preview parameters (width, quality) to save bandwidth.

## Instructions
- **Placeholders**: Show a skeleton or generic travel image if the image fails to load.
