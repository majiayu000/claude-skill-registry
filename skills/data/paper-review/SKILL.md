---
name: paper-review
description: Comprehensive peer review of academic papers for top-tier computer science conferences and journals. Supports PDF and LaTeX inputs, provides detailed reviews with scores, and generates improvement plans. Use when the user asks to review, evaluate, or provide feedback on academic papers.
license: MIT
---

# Academic Paper Review Skill

## Overview

This skill provides comprehensive peer review of academic papers for top-tier computer science conferences and journals. It evaluates papers against standard academic criteria including originality, technical quality, experimental validation, clarity, and significance.

## Supported Input Formats

1. **PDF files**: Direct analysis of compiled papers
2. **LaTeX files**: Analysis of source .tex files

## Review Process

### Step 1: Gather Review Context

Before starting the review, use AskUserQuestion to gather:

1. **Output Language**: Ask whether the review should be in Chinese or English
2. **Target Venue**: Ask for the conference or journal name (e.g., "NeurIPS 2026", "CVPR 2026", "ICML 2026", "TPAMI")

Example interaction:
```
AskUserQuestion with two questions:
1. "What language should the review be written in?"
   - Options: "English", "Chinese (中文)"
2. "What is the target conference or journal for this paper?"
   - Options: "NeurIPS", "CVPR", "ICML", "ICLR", "Other (please specify)"
```

### Step 2: Extract Paper Content

**For PDF files:**
```python
import pdfplumber

with pdfplumber.open(pdf_path) as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n\n"
```

**For LaTeX files:**
```python
# Read main .tex file and any \input or \include files
import re

def read_latex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find \input{} and \include{} commands
    includes = re.findall(r'\\(?:input|include)\{([^}]+)\}', content)

    # Read included files recursively
    for inc in includes:
        if not inc.endswith('.tex'):
            inc += '.tex'
        inc_path = os.path.join(os.path.dirname(filepath), inc)
        if os.path.exists(inc_path):
            inc_content = read_latex_file(inc_path)
            content = content.replace(f'\\input{{{inc}}}', inc_content)
            content = content.replace(f'\\include{{{inc}}}', inc_content)

    return content
```

### Step 3: Analyze Paper Structure

Extract and identify key sections:
- Abstract
- Introduction
- Related Work
- Methodology/Approach
- Experiments/Results
- Discussion
- Conclusion
- References

### Step 4: Conduct Comprehensive Review

Evaluate the paper across these dimensions:

#### 1. Originality & Novelty (Score: X/10)
- Is the problem new or is the approach novel?
- How does it differ from existing work?
- Are the contributions clearly stated?
- **Confidence Level**: 1-5 (1=Not familiar, 5=Expert)

#### 2. Technical Quality & Soundness (Score: X/10)
- Are the methods technically sound?
- Are claims supported by theory or evidence?
- Are there any technical errors or gaps?
- **Confidence Level**: 1-5

#### 3. Experimental Validation (Score: X/10)
- Are experiments comprehensive and well-designed?
- Are baselines appropriate and comparisons fair?
- Are results statistically significant?
- Are ablation studies included?
- **Confidence Level**: 1-5

#### 4. Clarity & Presentation (Score: X/10)
- Is the paper well-written and organized?
- Are concepts explained clearly?
- Is the notation consistent?
- Are there grammar or language issues?
- **Confidence Level**: 1-5

#### 5. Significance & Impact (Score: X/10)
- How important is this work to the field?
- What is the potential impact?
- Does it open new research directions?
- **Confidence Level**: 1-5

#### 6. Reproducibility (Score: X/10)
Check for:
- Code availability (mentioned or provided)
- Dataset descriptions and availability
- Hyperparameter details
- Experimental setup completeness
- Computational requirements
- **Confidence Level**: 1-5

#### 7. Visual Elements Quality
Evaluate:
- Figures: clarity, relevance, quality
- Tables: completeness, formatting, readability
- Diagrams: accuracy, helpfulness
- Captions: informativeness

#### 8. Ethics & Limitations
Assess:
- Discussion of limitations
- Potential negative societal impacts
- Ethical considerations
- Broader impact statement (if required by venue)

### Step 5: Generate Overall Assessment

Calculate overall score as weighted average:
- Originality: 20%
- Technical Quality: 25%
- Experimental Validation: 20%
- Clarity: 15%
- Significance: 15%
- Reproducibility: 5%

Provide recommendation:
- **Strong Accept** (9-10): Exceptional paper, clear accept
- **Accept** (8-8.9): Good paper, should be accepted
- **Weak Accept** (7-7.9): Above threshold, leaning accept
- **Borderline** (6-6.9): On the fence, could go either way
- **Weak Reject** (5-5.9): Below threshold, leaning reject
- **Reject** (4-4.9): Clear reject, significant issues
- **Strong Reject** (1-3.9): Fundamental flaws, strong reject

### Step 6: Write Review Document

Create `review-{paper-name}-{timestamp}.md` with this structure:

```markdown
# Paper Review: [Paper Title]

**Venue:** [Conference/Journal Name]
**Review Date:** [YYYY-MM-DD HH:MM]
**Review Language:** [Chinese/English]
**Reviewer:** Claude AI Assistant

---

## Overall Recommendation

- **Decision:** [Strong Accept / Accept / Weak Accept / Borderline / Weak Reject / Reject / Strong Reject]
- **Overall Score:** [X.X/10]
- **Confidence:** [5-Expert in this area / 4-Knowledgeable / 3-Familiar / 2-Somewhat familiar / 1-Not familiar]

---

## Summary

[2-3 paragraph summary covering:
- What the paper is about
- Main contributions
- Key strengths and weaknesses
- Overall assessment]

---

## Strengths

- [Strength 1]
- [Strength 2]
- [Strength 3]
- ...

---

## Weaknesses

- [Weakness 1]
- [Weakness 2]
- [Weakness 3]
- ...

---

## Detailed Evaluation

### 1. Originality & Novelty
**Score:** X/10 | **Confidence:** X/5

[Detailed assessment of novelty, comparison with related work, clarity of contributions]

### 2. Technical Quality & Soundness
**Score:** X/10 | **Confidence:** X/5

[Assessment of technical correctness, theoretical foundations, methodology soundness]

### 3. Experimental Validation
**Score:** X/10 | **Confidence:** X/5

[Evaluation of experimental design, baselines, results, ablation studies, statistical significance]

### 4. Clarity & Presentation
**Score:** X/10 | **Confidence:** X/5

[Assessment of writing quality, organization, notation, figures, readability]

### 5. Significance & Impact
**Score:** X/10 | **Confidence:** X/5

[Evaluation of importance, potential impact, relevance to community]

### 6. Reproducibility
**Score:** X/10 | **Confidence:** X/5

[Assessment of code availability, dataset details, hyperparameters, experimental setup]

### 7. Visual Elements Quality

[Analysis of figures, tables, and diagrams - clarity, completeness, appropriateness]

### 8. Ethics & Limitations

[Discussion of ethical considerations, limitations, broader impact, potential negative consequences]

---

## Questions for Authors

1. [Question 1]
2. [Question 2]
3. [Question 3]
...

---

## Suggestions for Rebuttal

[Constructive guidance on how authors might address the main concerns raised in this review. Focus on the most critical issues that could change the recommendation if addressed.]

---

## Minor Issues

- [Typo/formatting issue 1]
- [Reference issue 2]
- [Minor suggestion 3]
...

---

## Detailed Comments by Section

### Abstract
[Comments on abstract]

### Introduction
[Comments on introduction]

### Related Work
[Comments on related work section]

### Methodology
[Comments on methodology]

### Experiments
[Comments on experiments]

### Conclusion
[Comments on conclusion]

---

**End of Review**
```

### Step 7: Generate Improvement Plan

Create `improvements-{paper-name}-{timestamp}.md` with categorized TODO items:

```markdown
# Paper Improvement Plan

**Paper:** [Paper Title]
**Generated:** [YYYY-MM-DD HH:MM]

This document provides a structured improvement plan based on the review. Items are categorized by priority and type.

---

## 🔴 Critical Issues (Must Address)

These issues significantly impact the paper's acceptance chances and must be addressed.

- [ ] **[Issue 1 Title]**
  - **Location:** [Section/Page]
  - **Problem:** [Description of the issue]
  - **Suggested Fix:** [How to address it]
  - **Estimated Effort:** [High/Medium/Low]

- [ ] **[Issue 2 Title]**
  - **Location:** [Section/Page]
  - **Problem:** [Description]
  - **Suggested Fix:** [Solution]
  - **Estimated Effort:** [High/Medium/Low]

---

## 🟡 Major Improvements (Strongly Recommended)

These improvements would significantly strengthen the paper.

- [ ] **[Improvement 1 Title]**
  - **Location:** [Section/Page]
  - **Current State:** [What's there now]
  - **Suggested Enhancement:** [What to add/change]
  - **Expected Impact:** [How this helps]
  - **Estimated Effort:** [High/Medium/Low]

- [ ] **[Improvement 2 Title]**
  - **Location:** [Section/Page]
  - **Current State:** [Description]
  - **Suggested Enhancement:** [Enhancement]
  - **Expected Impact:** [Impact]
  - **Estimated Effort:** [High/Medium/Low]

---

## 🟢 Minor Suggestions (Nice to Have)

These are polish items that would improve the paper but aren't critical.

- [ ] **[Suggestion 1]** - [Brief description]
- [ ] **[Suggestion 2]** - [Brief description]
- [ ] **[Suggestion 3]** - [Brief description]

---

## 📝 Writing & Presentation

- [ ] **Grammar and Language**
  - [List specific issues with line numbers if possible]

- [ ] **Notation and Terminology**
  - [Inconsistencies or unclear notation]

- [ ] **Figure and Table Improvements**
  - [Specific suggestions for visual elements]

---

## 🔬 Experimental Enhancements

- [ ] **Additional Experiments**
  - [What experiments to add and why]

- [ ] **Baseline Comparisons**
  - [Missing baselines to include]

- [ ] **Ablation Studies**
  - [What ablations would be valuable]

---

## 📚 Related Work & Citations

- [ ] **Missing References**
  - [Important papers to cite]

- [ ] **Related Work Discussion**
  - [Gaps in related work coverage]

---

## 🎯 Priority Roadmap

### Phase 1: Critical Fixes (Before Resubmission)
1. [Critical issue 1]
2. [Critical issue 2]
3. [Critical issue 3]

### Phase 2: Major Improvements (Strengthen Paper)
1. [Major improvement 1]
2. [Major improvement 2]
3. [Major improvement 3]

### Phase 3: Polish (If Time Permits)
1. [Minor suggestion 1]
2. [Minor suggestion 2]
3. [Minor suggestion 3]

---

## 📊 Estimated Impact on Review Score

If all critical issues and major improvements are addressed:
- **Current Overall Score:** X.X/10
- **Potential Score After Improvements:** Y.Y/10
- **Expected Recommendation Change:** [Current] → [Potential]

---

**End of Improvement Plan**
```

## Review Tone Guidelines

Maintain a **constructive and balanced** tone throughout:

1. **Be Specific**: Provide concrete examples and line numbers when possible
2. **Be Fair**: Acknowledge both strengths and weaknesses
3. **Be Constructive**: Offer actionable suggestions, not just criticism
4. **Be Professional**: Maintain respectful and objective language
5. **Be Encouraging**: Recognize good work and potential

## Example Usage

```bash
# User invokes the skill
/paper-review path/to/paper.pdf

# Or with LaTeX
/paper-review path/to/paper.tex
```

## Output Files

The skill generates two files in the current directory:
1. `review-{paper-name}-{timestamp}.md` - Full review
2. `improvements-{paper-name}-{timestamp}.md` - Improvement plan

## Notes

- Always read the entire paper before starting the review
- For LaTeX files, handle multi-file projects by following \input and \include commands
- Adjust review depth based on paper length (conference papers vs journal papers)
- Consider venue-specific requirements (e.g., NeurIPS emphasizes reproducibility, CVPR emphasizes experimental results)
- Be aware of common pitfalls in CS papers: overclaiming, insufficient baselines, unclear notation, missing ablations

## Common CS Conference Standards

- **NeurIPS**: Strong emphasis on reproducibility, code submission, theoretical soundness
- **CVPR/ICCV/ECCV**: Focus on experimental results, visual quality, benchmark performance
- **ICML**: Balance of theory and experiments, statistical significance
- **ICLR**: Open review process, reproducibility, code availability
- **ACL/EMNLP**: Language quality, linguistic analysis, dataset details
- **SIGIR/WWW**: Real-world applicability, scalability, user studies

## Tips for Effective Reviews

1. **Read Abstract and Conclusion First**: Get the big picture
2. **Skim Figures and Tables**: Understand the experimental setup
3. **Read Introduction**: Understand motivation and contributions
4. **Deep Dive into Methods**: Check technical soundness
5. **Analyze Experiments**: Verify claims are supported
6. **Check Related Work**: Ensure proper positioning
7. **Review Writing Quality**: Note clarity issues
8. **Consider Reproducibility**: Check for missing details
