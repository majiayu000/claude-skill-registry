---
name: case-study-generator
description: This skill generates case study entries for intelligent textbook projects from GitHub repositories. Use this skill when adding a new case study to the case studies index page, when the user provides a GitHub repo URL and wants to create a case study card entry. The skill handles repo analysis, thumbnail generation/compression, and markdown entry formatting.
---

# Case Study Generator

## Overview

This skill automates the creation of case study entries for the intelligent textbooks case studies page. Given a GitHub repository URL, it extracts project information, generates or processes a thumbnail image compressed to ~70KB, and creates a properly formatted markdown entry for `docs/case-studies/index.md`.

## Workflow

### Step 1: Gather Repository Information

Extract the following from the GitHub repository:

1. **Repository URL** - The full GitHub URL provided by the user
2. **Repository name** - Extract from URL (e.g., `dmccreary/geometry-course`)
3. **GitHub Pages URL** - Derive from repo: `https://{username}.github.io/{repo-name}`
4. **Project title** - Check for a clear title in README.md or use repo name
5. **Description** - Extract from README.md (first paragraph or project description)
6. **Metrics** (if available):
   - File count: `find docs -type f -name "*.md" | wc -l`
   - Word count: `find docs -type f -name "*.md" -exec cat {} \; | wc -w`
   - MicroSim count: Count directories in `docs/sims/`
   - Glossary term count: Parse `docs/glossary.md` if exists

Use the `gh` CLI or direct GitHub API to fetch repository information:

```bash
# Get repo description
gh repo view {owner}/{repo} --json description

# Clone repo temporarily for analysis
gh repo clone {owner}/{repo} /tmp/{repo} -- --depth 1
```

### Step 2: Obtain or Generate Thumbnail Image

Check for existing thumbnail options in priority order:

1. **Existing social card image** - Check `docs/img/` for `social-card.png` or similar
2. **README banner image** - Parse README.md for header images
3. **Custom image provided by user** - User may specify an image path
4. **Generate with AI** - If no image exists, suggest generating one with an AI image tool

Place the source image in `docs/case-studies/img/` with a filename matching the repo name:
- Use kebab-case: `geometry-course.jpg`, `deep-learning-course.jpg`

### Step 3: Compress Thumbnail Image

Compress the thumbnail to approximately 70KB for fast page loading.

#### For Initial Compression

Run the thumbnail compression script:

```bash
python3 src/compress-thumbnails.py docs/case-studies/img 70
```

This script:
- Targets 70KB file size
- Maintains minimum 400px width
- Preserves aspect ratio
- Creates `.backup` files for safety

#### For PNG to JPEG Conversion (if needed)

If PNG compression cannot achieve 70KB target, convert to JPEG:

```bash
python3 src/convert-png-to-jpg.py docs/case-studies/img 70
```

This script:
- Converts PNG to JPEG format
- Fills transparent areas with white background
- Achieves better compression for photographic images
- Removes original PNG after successful conversion

#### Manual Single-Image Compression

For compressing a single new image without affecting others:

```python
from PIL import Image, ImageOps

def compress_single_image(input_path, output_path, target_kb=70, min_width=400):
    """Compress a single image to target size."""
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)

    # Convert to RGB for JPEG
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        if img.mode in ('RGBA', 'LA'):
            background.paste(img, mask=img.split()[-1])
            img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Calculate resize factor
    orig_w, orig_h = img.size
    min_factor = min_width / orig_w if orig_w > min_width else 1.0

    for factor in [0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15]:
        if factor < min_factor:
            continue
        new_w = int(orig_w * factor)
        new_h = int(orig_h * factor)
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        for quality in [85, 80, 75, 70, 65, 60]:
            resized.save(output_path, "JPEG", quality=quality, optimize=True)
            if os.path.getsize(output_path) / 1024 <= target_kb:
                return True
    return False
```

### Step 4: Update index.md Image References

After converting PNG to JPEG, update `docs/case-studies/index.md` to use the new `.jpg` extension:

```markdown
# Before
![Project Name](./img/project-name.png)

# After
![Project Name](./img/project-name.jpg)
```

### Step 5: Generate Case Study Entry

Create the markdown entry using the format in `references/entry-format.md`.

#### Entry Format

```markdown
- **[Project Title](https://username.github.io/repo-name)**

    ![Alt Text](./img/repo-name.jpg)

    Brief 1-2 sentence description of the project, its purpose, and target audience.

    [:octicons-mark-github-16: Repository](https://github.com/username/repo-name) · XX Files · XXK Words · X MicroSims
```

#### Entry Guidelines

1. **Title**: Use the full descriptive project title, not the repo name
2. **Image alt text**: Match the project title or use a descriptive phrase
3. **Description**:
   - Keep to 1-2 sentences
   - Mention target audience (high school, college, etc.)
   - Highlight key features (MicroSims, learning graph, etc.)
4. **Metrics line**: Include available metrics separated by ` · `
   - Repository link with GitHub icon
   - File count (if significant)
   - Word count (rounded to K)
   - Glossary term count
   - MicroSim count
   - Development stage (if early: "Early Stage", "Active Development")

### Step 6: Insert Entry in Alphabetical Order

Insert the new entry into `docs/case-studies/index.md` in alphabetical order by project title. The entries are inside a `<div class="grid cards grid-3-col" markdown>` block.

### Step 7: Verify and Clean Up

1. **Verify image displays correctly**: Run `mkdocs serve` and check the case studies page
2. **Check image file size**: Confirm thumbnail is under 70KB
3. **Remove backup files** (after verification):
   ```bash
   rm docs/case-studies/img/*.backup
   ```
4. **Clean up temporary clone** (if created):
   ```bash
   rm -rf /tmp/{repo-name}
   ```

## Example Usage

**User request**: "Add a case study for https://github.com/dmccreary/systems-thinking"

**Process**:
1. Clone repo, extract: title="Systems Thinking in the Age of AI", description from README
2. Find existing image or generate thumbnail
3. Compress to `docs/case-studies/img/systems-thinking.jpg` (~31KB)
4. Generate entry:

```markdown
- **[Systems Thinking in the Age of AI](https://dmccreary.github.io/systems-thinking)**

    ![Systems Thinking](./img/systems-thinking.jpg)

    Interactive resources for teaching systems thinking from high school to executive level. Multiple course descriptions.

    [:octicons-mark-github-16: Repository](https://github.com/dmccreary/systems-thinking) · MicroSims included
```

5. Insert alphabetically after "STEM Robots" entry
6. Verify with `mkdocs serve`

## Resources

### Compression Scripts

The following scripts are located in the project's `src/` directory:

- **`src/compress-thumbnails.py`** - Compresses images to target KB size with configurable minimum width
- **`src/convert-png-to-jpg.py`** - Converts PNG files to JPEG format for better compression

### Reference Files

- **`references/entry-format.md`** - Template and examples for case study entries
