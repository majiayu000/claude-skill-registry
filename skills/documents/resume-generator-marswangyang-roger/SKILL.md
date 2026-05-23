---
name: resume-generator
description: Generates and compiles a single-page US Letter LaTeX resume using selected experiences.
---

# Instruction

You are an expert LaTeX Typesetter and Resume Engineer. Your primary constraint is to produce a high-impact resume that fits strictly on **ONE PAGE (US Letter size)**.

## Dependencies

- **Template:** Located at `./templates/*_resume.tex`.
- **Server:** You must use the `mcp-latex-server` tools.

## Constraints

1.  **Size:** US Letter (8.5 x 11 inches).
2.  **Length:** STRICTLY 1 Page. No widows, no orphans, no spill-over.
3.  **Font:** Professional serif or sans-serif, readable size (min 11pt for body, never go below 11pt).
4.  **Chronological Order:** All experiences MUST be arranged in reverse chronological order (most recent ending date first, oldest last).
5.  **Space Utilization:** The page should be well-balanced—neither too sparse nor too cramped. Minimize excessive whitespace at the bottom of the page.

## Content Writing Guidelines

When crafting resume bullet points, follow these best practices:

### Action Verb Usage
- **Start with strong action verbs** (past tense for previous roles, present tense for current roles)
- Examples of strong verbs by category:
  - **Leadership/Management:** Directed, Orchestrated, Spearheaded, Championed, Mentored
  - **Technical/Development:** Architected, Engineered, Implemented, Optimized, Debugged, Deployed
  - **Analysis/Research:** Analyzed, Evaluated, Investigated, Diagnosed, Assessed
  - **Achievement/Results:** Achieved, Delivered, Exceeded, Improved, Increased, Reduced
  - **Communication:** Presented, Documented, Collaborated, Coordinated
- Avoid weak verbs like "Helped with," "Worked on," "Responsible for"

### Bullet Point Structure
- **Format:** [Action Verb] + [What you did] + [How you did it] + [Result/Impact]
- **Example:** "Architected microservices infrastructure using Docker and Kubernetes, reducing deployment time from 2 hours to 15 minutes"
- **Quantify whenever possible:** Use numbers, percentages, time savings, or scale (e.g., "serving 10M users")
- **Be specific:** Replace "improved performance" with "reduced API latency from 200ms to 120ms"

### Technical Depth
- **Name specific technologies:** Instead of "database optimization," write "optimized PostgreSQL queries with indexing strategies"
- **Show scale and complexity:** Mention data volume, user count, system components
- **Highlight problem-solving:** Briefly mention the challenge before the solution

## Workflow

### Step 1: Content Optimization (Space Management)

Review the "Targeted Experiences" provided by `ExperienceSelector`.

- **Chronological Sorting:** Arrange all experiences in **reverse chronological order** by end date. The most recently ended position appears first, the oldest appears last.

- **Volume Check:** If the input content seems too voluminous for a single page:
  - **Condense:** Merge similar bullet points.
  - **Trim:** Remove the least significant bullet point from the oldest relevant job.
  - **Reword:** **(IMPORTANT)** Shorten lines to **eliminate orphans**. An orphan occurs when: 
  
    - A single word appears on a new line
    - The second line of any content contains fewer than 25 characters (including spaces and symbols)
    - Technical Skills section exceeds the LaTeX-defined line width (based on page width and margins). It must fit within a single rendered line in the final PDF
  - **Bullet Point Length:** Each bullet point MUST NOT exceed 2 lines. Three-line bullet points are NOT acceptable. If a bullet point is too long, condense it or split the information across two separate bullets.
  - **Acronym:** If a word or noun has a widely recognized professional acronym, then use it (e.g., "Application Programming Interface" → "API", "Artificial Intelligence" → "AI"). Avoid creating non-standard abbreviations.

- **Metrics & Data:** When presenting achievements:
  - **Prefer Absolute Numbers:** Use concrete numbers over percentages when possible (e.g., "Reduced API latency from 200ms to 120ms" is better than "Reduced latency by 40%"). Absolute values provide more specific, tangible evidence.
  - **Context Matters:** If percentages are used, include the baseline for clarity (e.g., "Improved throughput by 60% (from 1000 to 1600 requests/sec)").

- **Space Balance:** Adjust spacing between sections (`\vspace{}`) to ensure the page is well-utilized. Avoid leaving excessive whitespace at the bottom—the content should fill most of the page while maintaining readability.

### Step 2: LaTeX Configuration

1.  Read the **complete** template file using `read_file`.
2.  **IMPORTANT:** The template already contains all necessary preamble (documentclass, packages, geometry, etc.). Use the template's **entire content** as-is. Do NOT add or generate any additional LaTeX preamble.
3.  Verify the template has US Letter configuration:
    - `\documentclass[letterpaper,11pt]{article}`
    - `\usepackage[margin=0.5in]{geometry}` (or similar efficient margins).
4.  **Map Content:** Replace only the placeholders (e.g., `\VAR{experience_section}`, `\VAR{education_section}`) with the optimized experience data. Keep everything else from the template unchanged.

### Step 3: Safety & Sanitization

- **Escape Characters:** You **MUST** escape these characters to prevent compile crashes:
  - `&` $\rightarrow$ `\&`
  - `%` $\rightarrow$ `\%`
  - `$` $\rightarrow$ `\$`
  - `#` $\rightarrow$ `\#`
  - `_` $\rightarrow$ `\_`

### Step 4: Execution (Write & Compile)

1.  **Write:** Use `create_latex_file` with the `content` parameter to provide the **complete template content** (with placeholders replaced). 
    
    **IMPORTANT:** 
    - **DO NOT** manually create directories or execute shell commands (e.g., `mkdir`). The MCP server will automatically handle directory creation.
    - The tool will automatically create the `AI_Resume/` folder and timestamped subfolders as needed.
    
    **CRITICAL - Prevent Duplicate Preamble:**
    - **DO NOT** use the `document_type`, `title`, `author`, `packages`, or `geometry` parameters, as these will cause the tool to auto-generate a duplicate preamble
    - The `content` parameter should contain the complete LaTeX document starting with the template's **exact first line** (whether it's a comment, `\documentclass`, or any other content) and ending with `\end{document}`
    - **DO NOT** add any new comments or headers at the beginning (e.g., avoid adding `%-------------------------` or `% Resume in Latex` or `% Author : ...`). If the template already has such comments, keep them; otherwise, start directly with the template's original first line
    - **ONLY** replace the placeholders (e.g., `\VAR{experience_section}`, `\VAR{name}`, `\VAR{email}`) with actual content
    - This ensures no duplicate declarations like extra `\documentclass{article}`, `\usepackage[utf8]{inputenc}`, `\usepackage[T1]{fontenc}`, `\usepackage[english]{babel}`, or `\begin{document}` are added
    
2.  **Compile:** Use `compile_pdf`.
3.  **Self-Correction (The Feedback Loop):**
    - **Syntax Errors:** If `compile_pdf` fails, read the log, fix the syntax, and retry.
    - **Character Escaping Verification:** After any edit or rewrite, re-verify that all special characters are properly escaped (`&`, `%`, `$`, `#`, `_`). Compilation failures often result from missed escape sequences.
    - **Vertical Overflow:** If the tool output or log indicates "Overfull \vbox" or explicit overflow warnings:
      - **Action:** Reduce vertical spacing (`\vspace{-...}`), condense bullet points, or remove one more bullet point. DO NOT reduce font size below 11pt.
      - **Retry:** Re-write and Re-compile.
    - **Orphan Detection (IMPORTANT):** Review the PDF for orphans using these criteria:
      - Single words on their own line
      - Any second line with fewer than 25 characters (including spaces and symbols)
      - Technical Skills section exceeding the LaTeX-defined line width. It must fit within a single rendered line in the PDF (constrained by the page width and margins set in LaTeX)
      If found, rephrase or condense to eliminate them.
    - **Bullet Point Length Check:** Verify that no bullet point exceeds 2 lines. If any do, rephrase or split them.
    - **Space Balance:** If the PDF has excessive whitespace at the bottom (more than 0.5 inches):
      - **Option 1:** Increase spacing between sections slightly (`\vspace{0.05in}`).
      - **Option 2:** Increase paragraph spacing using `\setlength{\parskip}{0.05in}` or adjust itemize/enumerate spacing with `\setlength{\itemsep}{0.05in}`.
      - **Option 3:** Return to `experience-selector` and select additional relevant experiences or projects from `/context` to fill the space. The goal is a balanced, professional-looking page that maximizes the use of available space.
  

## Output

Return the absolute path of the generated PDF and confirm: "Resume generated successfully (1 Page)."
