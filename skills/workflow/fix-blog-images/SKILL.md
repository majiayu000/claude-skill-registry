---
name: fix-blog-images
description: Fix and optimize images in uncommitted blog posts. Use when preparing blog posts for publication, fixing broken image paths, renaming generic image names (image.png), moving images to proper /images/blog/ directory, improving alt text, or checking image references before committing. Trigger on "fix blog images", "check images", "prepare post for publish", or after pasting screenshots into markdown.
---

# Fix Blog Images

Fixes image issues in uncommitted blog posts before publishing.

## Workflow

1. Run the analysis script:

```bash
python3 scripts/fix_blog_images.py --json
```

2. Review output and for each issue:
   - **rename_and_move**: Move image to `/images/blog/` with descriptive name
   - **improve_alt_text**: Update alt text to describe the image content
   - **missing_image**: Locate or remove the reference

3. Apply fixes:
   - Move/rename image files to `packages/blog/public/images/blog/`
   - Update markdown references to use absolute paths `/images/blog/...`
   - Add descriptive alt text

## Image Conventions

- **Location**: All images in `packages/blog/public/images/blog/`
- **Naming**: `YYYYMMDD-HHMM-descriptive-name.png` or `YYYYMMDD-descriptive-name.png`
- **References**: Use absolute paths `/images/blog/filename.png`
- **Alt text**: Describe what the image shows for accessibility

## Example Fix

Before:

```markdown
![alt text](image.png)
```

After:

```markdown
![Screenshot showing terminal layout](/images/blog/20251229-post-slug-image.png)
```

# Addtional Notes

Don't try and Optimize Images. a git hook will run image optimization on commit. This skill is just to fix paths, names, and alt text before committing.
