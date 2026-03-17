---
name: site-slides
description: Generate presentation slides from images or PDF files. Use when user wants to create slides, generate presentations, or convert PDF to slides for the training camp website. Triggers on keywords like "slides", "presentation", "幻灯片", "演示文稿".
---

# Site Slides Generator

Generate presentation slides for the AI training camp website from a directory of images or a PDF file.

## Usage

User provides a directory name (e.g., `test1`), and this skill will:
1. Look for the directory in `./site/public/slides/<directory-name>`
2. If not found, report an error
3. If found, process the contents to generate slides

## Workflow

### Step 1: Validate Directory

Check if the directory exists:
```bash
ls ./site/public/slides/<directory-name>
```

If directory doesn't exist, inform the user and stop.

### Step 2: Analyze Contents

Check what's in the directory:
- If there's exactly ONE `.pdf` file and no image files → Go to Step 3 (PDF conversion)
- If there are image files (`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`) → Go to Step 4 (Generate slides)

### Step 3: PDF to Images Conversion

If directory contains only a PDF file:

1. Check if `pdf2jpg` command exists:
   ```bash
   which pdf2jpg
   ```

2. If not found, install swiss-knife:
   ```bash
   cargo install swiss-knife
   ```

3. Convert PDF to JPG images:
   ```bash
   cd ./site/public/slides/<directory-name> && pdf2jpg <filename>.pdf
   ```

   This generates `001.jpg`, `002.jpg`, etc. in the current directory.

4. Delete the original PDF file after successful conversion (if it still exists).
   Since we're still in the slides directory, use the filename directly:
   ```bash
   rm -f <filename>.pdf
   ```
   Note: Use `-f` flag in case `pdf2jpg` already deleted the file.

5. Proceed to Step 4.

### Step 4: Generate Slides MDX File

1. List all image files in sorted order:
   ```bash
   ls -1 ./site/public/slides/<directory-name>/*.{jpg,jpeg,png,gif,webp} 2>/dev/null | sort
   ```

2. Read each image to understand its content and generate appropriate captions.

3. Ask the user for:
   - **Title**: The presentation title (e.g., "Werner Vogels - The Renaissance Developer")
   - **Description**: Brief description of the presentation
   - **Category**: Category for the presentation (e.g., "技术分享", "课程介绍")

4. Create MDX file at `./site/src/pages/presentations/<directory-name>.mdx` following this template:

```mdx
---
layout: ../../layouts/PresentationLayout.astro
title: <TITLE>
description: <DESCRIPTION>
category: <CATEGORY>
---

import PresentationCarousel from '../../components/presentations/PresentationCarousel';
import { getUrl } from '../../utils/url';

# <TITLE>

<BRIEF_INTRO>

<PresentationCarousel
  client:load
  title="<TITLE>"
  slides={[
    {
      image: "/slides/<directory-name>/<image-filename>",
      alt: "<alt-text>",
      caption: "<caption>"
    },
    // ... more slides
  ]}
/>

## 核心要点

<KEY_POINTS_BASED_ON_CONTENT>

## 延伸阅读

- [查看课程大纲](/curriculum) - 了解 AI 编程训练营完整内容
- [探索工具生态](/tools) - 学习 AI 编程工具的使用
- [浏览学习资料](/materials) - 获取更多技术学习资源
```

### Step 5: Update index.astro

1. Read `./site/src/pages/presentations/index.astro`

2. Add a new entry to the `presentations` array:
   ```javascript
   {
     title: "<TITLE>",
     description: "<DESCRIPTION>",
     href: getUrl("presentations/<directory-name>"),
     thumbnail: getUrl("slides/<directory-name>/<first-image>"),
     slideCount: <NUMBER_OF_SLIDES>,
     date: "<YYYY-MM-DD>",  // Today's date
     category: "<CATEGORY>",
   },
   ```

3. Use the first image as the thumbnail (or ask the user to pick one).

## Example

User: "Create slides from the `vogels-keynote` directory"

1. Check `./site/public/slides/vogels-keynote` exists ✓
2. Find 32 JPG images
3. Ask user for title, description, category
4. Read images to understand content
5. Generate `./site/src/pages/presentations/vogels-keynote.mdx`
6. Update `./site/src/pages/presentations/index.astro`

## Notes

- Always read a sample of images (first, middle, last) to understand the presentation content
- Generate meaningful alt text and captions based on image content
- Use today's date for the `date` field in index.astro
- Image paths in the MDX should be absolute paths starting with `/slides/`

## Important: Avoiding MDX Syntax Errors

When generating captions and alt text, **NEVER use Chinese quotation marks** (`"` and `"`) inside JSX string attributes. These characters cause MDX parsing errors.

**Bad example:**
```jsx
caption: "真正的问题不是"AI会取代我吗？"而是..."
```

**Good example (use 「」 instead):**
```jsx
caption: "真正的问题不是「AI会取代我吗？」而是..."
```

Also avoid:
- Unescaped special characters in strings
- Line breaks within caption strings
- Using backticks or other quote characters that might conflict with JSX syntax
