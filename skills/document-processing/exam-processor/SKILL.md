---
name: exam-processor
description: Process exam/test paper documents from DOCX format into structured markdown. Use when Claude needs to: (1) Extract exam content from Word documents (.docx), (2) Analyze images in exam papers using vision tools, (3) Convert questions to structured markdown with proper image references, (4) Understand question context to match images with appropriate questions, (5) Create organized exam output with YAML frontmatter and sections
---

# Exam Processor

Process Word documents containing exam/test papers into structured markdown with proper image analysis and organization.

## Workflow

### 1. Use doc Skill for Document Extraction

First, invoke the `doc` skill to extract content from the DOCX file:

```
Use doc skill to extract all content including text, images, and formatting from [file.docx]
```

The doc skill will:
- Extract all text content with structure preserved
- Extract embedded images
- Preserve document formatting information

### 2. Extract and Save Images

After doc extraction, save all extracted images to an `images/` subdirectory:

- Create an output folder named after the input filename (e.g., for `math-exam-2024.docx`, create `math-exam-2024/` directory)
- Create `images/` subdirectory inside the output folder
- Save images with descriptive names based on context (e.g., `question-1-diagram.png`, `figure-2-a.png`)
- Use sequential numbering if context is unclear (e.g., `image-001.png`, `image-002.png`)

### 3. Analyze Images with Vision Tools

Use `mcp__zai-mcp-server__analyze_image` to understand each image:

```
Analyze the image at images/question-1-diagram.png with prompt: "Describe this image in detail, including any text, diagrams, mathematical expressions, or visual elements. Identify what type of exam question this image supports (multiple choice, calculation, diagram labeling, etc.)."
```

Extract from analysis:
- Image content description
- Text/expressions visible
- Question type context
- Any labels, numbers, or annotations

### 4. Match Images to Questions

Correlate each image with its associated question:

1. **Read image content** - Look for question numbers, text, or labels in the image
2. **Check surrounding text** - Match image position with question flow
3. **Verify context** - Use vision analysis to confirm the image relates to the specific question

For ambiguous cases, use vision tool with:
```
Analyze the image and determine which question number it belongs to based on any visible text, labels, or context clues.
```

### 5. Generate Structured Markdown

Create markdown output with:

**YAML Frontmatter:**
```yaml
---
title: [Exam Title]
subject: [Subject Name]
date: [Exam Date or source document date]
total_questions: [count]
sections: [list of sections if applicable]
---
```

**Question Structure:**
```markdown
## Question 1

[Question text]

{Optional image reference}
![Question 1 diagram](images/question-1-diagram.png)
*Image description: [brief description from vision analysis]*

{For multiple choice}
a) [Option A]
b) [Option B]
c) [Option C]
d) [Option D]
```

**Section Organization:**
- Group questions by sections if the original document has them
- Use heading hierarchy: `#` for title, `##` for sections, `###` for questions
- Preserve numbering from original document

### 6. Verify and Validate

After generating markdown:

1. **Check all images are referenced** - Every saved image should be linked in the markdown
2. **Verify image-question alignment** - Confirm each image matches its question context
3. **Validate structure** - Ensure YAML frontmatter is complete and valid
4. **Check text completeness** - No questions or options should be missing

## Output File Structure

The output folder is named based on the input filename (without extension).

For example, if the input file is `math-exam-2024.docx`:

```
math-exam-2024/
├── exam-paper.md
└── images/
    ├── question-1-diagram.png
    ├── question-3-figure.png
    └── ...
```

If the input file is `physics-final.docx`:

```
physics-final/
├── exam-paper.md
└── images/
    ├── question-1-diagram.png
    ├── question-3-figure.png
    └── ...
```

## Tips

- When an image contains only the question text itself (e.g., screenshot of text), still include the image and transcribe the text
- For math expressions in images, use LaTeX notation in markdown: `$E = mc^2$`
- If image analysis is uncertain about context, note this in the image description
- Preserve original question numbering even if gaps exist
