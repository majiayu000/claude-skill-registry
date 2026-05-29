---
name: llms-txt-manager
description: Comprehensive system for managing llms.txt and my-blog.json files across the project. Handles creation, updating, and synchronization of AI-readable content catalogs. Automatically detects when working with llms.txt files, my-blog.json files, or updating blog content. Includes utilities for fetching latest content from query-index.json and organizing by last modified dates. Keywords include llms.txt, my-blog.json, blog catalog, content index, query-index.json, AI content discovery, update llms, update blog, content synchronization.
---

# llms.txt Manager Skill

## Purpose

Manage llms.txt and my-blog.json files across the project, ensuring AI systems have comprehensive, up-to-date content catalogs. Automates synchronization between blog content (query-index.json) and llms.txt files.

## When to Use

This skill activates when:
- Creating or editing llms.txt files
- Creating or editing my-blog.json files
- User mentions updating blog catalogs
- User wants to synchronize content indexes
- Working with query-index.json data
- Creating folder-specific content indexes

## Core Concepts

### File Structure

**llms.txt** - AI-readable content catalog
- Location: Root or folder-specific (e.g., `blogs/ddt/integrations/llms.txt`)
- Purpose: Comprehensive list of content for AI systems
- Format: Markdown with metadata and categorized links
- Source: URLs from my-blog.json, text/descriptions from existing llms.txt

**my-blog.json** - Structured blog data
- Location: Same directory as llms.txt
- Purpose: Machine-readable catalog of blog posts
- Format: JSON with categories, posts, metadata
- Source: query-index.json filtered by folder context

**query-index.json** - Master content index
- Location: https://allabout.network/query-index.json
- Purpose: Single source of truth for all site content
- Contains: All pages with URLs, titles, descriptions, lastModified dates
- Updated: Automatically by the site

### Folder Context

When llms.txt is in a subfolder (e.g., `blogs/ddt/integrations/`):
- The final folder name indicates intent/scope
- my-blog.json should exist in same folder
- Content should be filtered to relevant posts only
- Example: `/integrations/` folder focuses on EDS integration tutorials

### Update Logic

**lastModified Date Comparison:**
1. Check lastModified date in llms.txt metadata
2. Fetch query-index.json
3. Filter entries with lastModified > llms.txt date
4. Add only new/updated content

## File Templates

### llms.txt Template

```markdown
# [Project/Section Title]

[Brief description of what this content covers]

**Last updated:** [Month Year]
**Authors:** [Author Names]

## [Category Name]

### [Subcategory Name]

- [Title](URL): Description
- [Title](URL): Description

## Version Information

**Version:** [version] (Updated: [date])
**Comprehensive catalog:** [count] posts across [n] categories
**Categories:** [List with counts]
```

### my-blog.json Template

```json
{
  "metadata": {
    "last-updated": "YYYY-MM-DD",
    "scope": "folder-name-or-site-wide"
  },
  "mostVisited": [
    {
      "title": "Popular Post Title",
      "url": "/path/to/post",
      "description": "Post description"
    }
  ],
  "categoryMap": [
    {
      "id": "category-id",
      "name": "Display Name",
      "count": 0,
      "description": "Category description"
    }
  ],
  "categories": [
    {
      "id": "category-id",
      "name": "Display Name",
      "posts": [
        {
          "title": "Post Title",
          "url": "/path/to/post",
          "description": "Post description",
          "lastModified": "YYYY-MM-DD"
        }
      ]
    }
  ]
}
```

**IMPORTANT:** Do NOT include a `latestPosts` array in my-blog.json files. The view-myblog block automatically generates it from the 3 most recent posts. Including it manually requires maintenance and defeats the purpose of auto-generation.

## Key Concepts

## Workflows

### Creating New llms.txt

**Automatic Creation:**
The sync script now automatically creates llms.txt files if they don't exist:

1. **Detects Missing Files**
   - Finds all my-blog.json files
   - Checks for paired llms.txt in same directory
   - Creates missing files automatically

2. **Builds Complete Structure**
   - Creates header with title, description, authors
   - Builds organized sections from my-blog.json categories
   - Uses folder name for context (e.g., "ai" → "Ai Resources")

3. **Populates Content**
   - Fetches from query-index.json
   - Filters by folder context if applicable
   - Formats posts with titles, URLs, descriptions
   - Updates metadata to current date

**Manual Creation:**
If you need to manually create one:

1. **Determine Scope**
   - Root llms.txt: Site-wide catalog
   - Folder llms.txt: Section-specific (use folder name for context)

2. **Check for my-blog.json**
   - Look in same directory as llms.txt
   - If missing, create one first
   - Filter query-index.json by folder path if folder-specific

3. **Structure Content**
   - Use folder name to determine focus (e.g., `/integrations/` = EDS integrations)
   - Organize with subsections for better scannability
   - Include all relevant posts from my-blog.json
   - Add descriptive text for context

4. **Add Metadata**
   - Version number
   - Last updated date
   - Category counts
   - Access guidelines (optional)

### Updating Existing llms.txt

1. **Read Current File**
   - Extract last-updated date from metadata
   - Note current structure and organization

2. **Fetch New Content**
   - Load query-index.json
   - Filter by lastModified > current date
   - Filter by folder context if applicable

3. **Merge New Posts**
   - Add new posts to organized sections
   - Update version number and date
   - Maintain text patterns and formatting

5. **Update my-blog.json**
   - Add new posts to appropriate categories
   - Update metadata.last-updated
   - Increment category counts

### Creating my-blog.json from query-index.json

**Automatic Creation:**
The sync script now automatically creates my-blog.json files if they don't exist:

1. **Detects Missing Files**
   - Finds all llms.txt files
   - Checks for paired my-blog.json in same directory
   - Creates missing files automatically

2. **Initializes Structure**
   - Creates empty categoryMap with all 6 standard categories
   - Sets metadata with scope (folder name or 'site-wide')
   - Sets last-updated to 2020-01-01 (extreme past, will populate on next update)

3. **Populates Content**
   - Fetches from query-index.json
   - Filters by folder context if applicable
   - Categorizes posts automatically
   - Updates metadata to current date

**Manual Creation:**
If you need to manually create one:

1. **Fetch Data**
   ```bash
   curl https://allabout.network/query-index.json
   ```

2. **Filter by Context**
   - Root my-blog.json: All content
   - Folder my-blog.json: Filter by path prefix

3. **Categorize Posts**
   - Group by topic/category
   - Count posts per category
   - Create categoryMap

4. **Structure Output**
   - metadata section with date and scope
   - categoryMap with counts
   - categories with full post arrays

## Command Usage

### /update-llms

Finds all llms.txt files in the project and updates them with new content:

```bash
/update-llms
```

**Or use the script directly:**
```bash
node scripts/sync-blog-content.js --target=llms
```

**Process:**
1. Find all existing llms.txt files: `**/*llms.txt`
2. Find all my-blog.json files without paired llms.txt
3. For each file (existing or new):
   - If new: Create complete structure from my-blog.json
   - If existing: Read last-updated date from metadata
   - Determine folder context (site-wide or folder-specific)
   - Fetch query-index.json from production
   - Filter by context (folder path matching)
   - Filter new posts (lastModified > last-updated)
   - Add new posts to organized sections (if any)
   - Update version date and metadata

### /update-my-blog

Finds all my-blog.json files and updates them with latest content:

```bash
/update-my-blog
```

**Process:**
1. Find all my-blog.json files: `**/*my-blog.json`
2. For each file:
   - Read current content and last-updated
   - Determine folder context
   - Fetch query-index.json
   - Filter by context and date
   - Update categories and counts
   - Update metadata

## Best Practices

### Content Organization

✅ **Use subsections** - Break large categories into logical groups
✅ **Consistent formatting** - Use same pattern throughout
✅ **Rich descriptions** - Include full descriptions from source
✅ **Clear hierarchy** - Main section → Subsection → Posts
✅ **Cross-references** - Link between related llms.txt files

### URL Management

✅ **Source of truth**: my-blog.json for URLs
✅ **Text source**: Existing llms.txt for descriptions/formatting
✅ **New content**: query-index.json for latest posts
✅ **Relative URLs**: Use relative paths in my-blog.json
✅ **Absolute URLs**: Use full URLs in llms.txt

### Date Handling

✅ **ISO format**: YYYY-MM-DD for dates
✅ **Comparison**: Filter by lastModified > last-updated
✅ **Display format**: "Month Year" in llms.txt header
✅ **Update always**: Change date when content changes

### Folder Context

✅ **Use folder name**: Final path segment indicates scope
✅ **Filter appropriately**: Only relevant content for folder llms.txt
✅ **Paired files**: Keep my-blog.json with llms.txt
✅ **Independent updates**: Each folder maintains own files

## Examples

### Example 1: Root llms.txt

Location: `/llms.txt`
Scope: Entire site
my-blog.json: `/my-blog.json` (all content)
Categories: All site categories

### Example 2: Integrations llms.txt

Location: `/blogs/ddt/integrations/llms.txt`
Scope: EDS integration tutorials only
my-blog.json: `/blogs/ddt/integrations/my-blog.json`
Categories: Filtered to integration-related posts

### Example 3: AI Topics llms.txt

Location: `/blogs/ddt/ai/llms.txt`
Scope: AI/LLM content only
my-blog.json: `/blogs/ddt/ai/my-blog.json`
Categories: Filtered to AI-related posts

## Troubleshooting

### my-blog.json Missing

**Solution**: Create it from query-index.json filtered by folder context

### Dates Not Comparing

**Solution**: Ensure ISO format (YYYY-MM-DD) and proper parsing

### Wrong Content Scope

**Solution**: Check folder context and filter query-index.json properly

### Duplicate Entries Within Categories

**Solution**: Deduplicate by URL before adding to categories

## Related Files

- `.claude/commands/update-llms.md` - Slash command for updating llms.txt
- `.claude/commands/update-my-blog.md` - Slash command for updating my-blog.json
- `scripts/sync-blog-content.js` - Utility script for bulk updates (no dependencies)

## Version

**Skill Version:** 1.0
**Last Updated:** November 2025
**Line Count:** < 500 ✅
