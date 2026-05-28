---
name: zola-blog
description: This skill should be used when publishing Vietnamese Obsidian notes to a Zola blog. It converts Vietnamese content to English, optimizes writing style following strict anti-AI-detection guidelines, and publishes to the blog. Use when the user provides an Obsidian markdown file path and wants it published as a blog post.
---

# Zola Blog Publisher

Publish content to Zola blog with Vietnamese-to-English translation and writing optimization.

## Two Modes

### Mode 1: From Obsidian File
User provides path to Obsidian markdown file.
```
/zola-blog D:\pcloud\workspace\obsidian\10 cong cu\neovim\lazyvim.md
```

### Mode 2: From Bullet Points / Description
User provides brief outline, bullet points, or topic description without file path.
```
/zola-blog
- topic: setting up WezTerm for AI coding
- pain point: opening multiple terminals every morning
- solution: Lua script to auto-launch agents
- features: hotkey launcher, auto-maximize, tab management
```

Detect mode by checking if user input contains a valid file path (.md extension with drive letter or starts with path separator).

---

## Workflow for Mode 1 (From File)

### Step 1: Read Source File

Read the Obsidian markdown file from the provided path.

### Step 2: Convert Obsidian to Zola Format

Use the existing `import_markdown` function from the toolkit to handle:
- Remove Obsidian YAML frontmatter
- Convert wikilinks `[[link]]` to plain text
- Remove callout formatting `> [!note]`
- Process images: copy from Obsidian vault to blog static folder

Call the Python toolkit:
```bash
cd "D:\pcloud\workspace\code\python"
python -c "from toolkit_modules.tools.blog import BlogTools; BlogTools().import_markdown()"
```

Or use the conversion functions directly if needed.

### Step 3: Translate and Optimize

After conversion, translate and optimize the content:

1. **Translate Vietnamese to English**
   - Keep technical terms in English
   - Maintain code blocks unchanged
   - Preserve markdown formatting

2. **Optimize writing style** - Follow `references/blog-guidelines.md` strictly:
   - Remove AI buzzwords completely
   - Use personal voice: "I use", "I found", "I built"
   - Short paragraphs (2-4 sentences max)
   - Specific numbers instead of vague claims
   - Honest about pros AND cons
   - Active voice only

3. **Expand content where needed**
   - Add real examples from context
   - Include "who should use this" section
   - Add comparison with alternatives if relevant

### Step 4: Review Checklist

Before publishing, verify:
- [ ] No AI buzzwords (seamlessly, powerful, leverage, game-changer, etc.)
- [ ] Personal voice throughout ("I", not "we" or passive)
- [ ] Opening hook is specific pain point, not generic
- [ ] All numbers are concrete, not vague
- [ ] Short paragraphs (2-4 sentences)
- [ ] Reads like human developer wrote it

### Step 5: Write Final Post

Write the optimized English content to the blog:
- Location: `D:\pcloud\workspace\code\website\quoc app\content\blog\`
- Filename: slug from original filename
- Include Zola frontmatter with title, date, tags

### Step 6: Build and Deploy

Provide commands for user to run:
```bash
cd "D:\pcloud\workspace\code\website\quoc app"
zola build
git add .
git commit -m "Add new blog post: [title]"
git push
```

---

## Workflow for Mode 2 (From Bullet Points / Description)

### Step 1: Understand the Input

User provides outline in Vietnamese or English:
- Topic / subject
- Pain point or problem
- Solution or approach
- Key features or points to cover
- Personal experiences (if any)

Example input:
```
/zola-blog
- chủ đề: dùng marker convert PDF sang markdown
- vấn đề: PDF khó edit, copy text bị lỗi format
- giải pháp: dùng marker, hỗ trợ OCR, giữ được format
- tính năng: CLI đơn giản, hỗ trợ batch, extract ảnh
```

### Step 2: Research and Expand

Before writing, gather more context:
- Ask clarifying questions if needed (target audience, technical depth, specific examples)
- If topic is technical, understand the tool/concept fully
- Identify real use cases and scenarios

### Step 3: Write Full Blog Post

Write complete blog post in English following `references/blog-guidelines.md`:

**Structure to follow:**
1. Opening hook - specific pain point, personal story
2. Problem section - why existing solutions fail
3. Solution introduction - what it does, no hype
4. Features breakdown - each with real example
5. Real workflow examples - step-by-step with numbers
6. Comparison with alternatives - honest pros/cons
7. Who should use this - honest assessment
8. Setup guide (if technical)
9. Bottom line - restate benefit, simple CTA

**Critical rules:**
- Write as if YOU (the author) experienced this
- Use "I found", "I use", "I tried"
- Include specific numbers: "takes 30 seconds", "saved 2 hours"
- Be honest about limitations
- NO AI buzzwords

### Step 4: Review Checklist

Same as Mode 1 - verify:
- [ ] No AI buzzwords
- [ ] Personal voice throughout
- [ ] Specific opening hook
- [ ] Concrete numbers
- [ ] Short paragraphs
- [ ] Reads like human developer wrote it

### Step 5: Generate Slug and Write

- Generate slug from topic: `marker-pdf-to-markdown`
- Write to blog content folder
- Include proper Zola frontmatter

### Step 6: Build and Deploy

Same as Mode 1 - provide git commands.

---

## Key Paths

- Obsidian vault: `D:\pcloud\workspace\obsidian\`
- Obsidian images: `D:\pcloud\workspace\obsidian\90 luu tru\images\`
- Blog root: `D:\pcloud\workspace\code\website\quoc app\`
- Blog content: `D:\pcloud\workspace\code\website\quoc app\content\blog\`
- Blog images: `D:\pcloud\workspace\code\website\quoc app\static\images\blog\`

## Writing Guidelines Reference

For detailed writing guidelines, anti-AI patterns, and examples, see `references/blog-guidelines.md`.

## Example Usage

### Mode 1: From File
```
User: /zola-blog D:\pcloud\workspace\obsidian\10 cong cu\neovim\lazyvim.md
```

Agent will:
1. Read the Vietnamese source file
2. Convert Obsidian syntax to standard markdown
3. Copy any referenced images to blog static folder
4. Translate to English
5. Optimize writing following guidelines
6. Write to blog content folder
7. Provide git commands to publish

### Mode 2: From Outline
```
User: /zola-blog
- topic: using Marker to convert PDF to markdown
- problem: PDFs are hard to edit, copy-paste breaks formatting
- solution: Marker preserves structure, supports OCR
- features: simple CLI, batch processing, image extraction
- my experience: converted 50 research papers last week
```

Agent will:
1. Understand the outline and ask clarifying questions if needed
2. Research the topic for accuracy
3. Write complete blog post in English with personal voice
4. Follow anti-AI-detection guidelines strictly
5. Generate appropriate slug and frontmatter
6. Write to blog content folder
7. Provide git commands to publish
