---
name: 1-determine-techstack
description: Determine the type of project and summarize the tech stack. Your summary should include:
---

**Core Technology Analysis:**

- Programming language(s)
- Primary framework
- Any secondary or tertiary frameworks
- State management approach
- Any other relevant technologies or patterns

**Domain Specificity Analysis:**

- What specific problem domain does this application target? (e.g., "chaos game theory visualization", "e-commerce platform", "blog CMS", "data visualization dashboard")
- What are the core mathematical/business concepts? (e.g., "fractal mathematics", "payment processing", "content management")
- What type of user interactions does it support? (e.g., "mathematical parameter manipulation", "shopping workflows", "content editing")
- What are the primary data types and structures used? (e.g., "geometric points and vertices", "product catalogs", "articles and metadata")

**Application Boundaries:**

- What features/functionality are clearly within scope based on existing code?
- What types of features would be architecturally inconsistent with the current design?
- Are there any specialized libraries or mathematical concepts that suggest domain constraints?

Add all your findings to ./{output-folder}/1-techstack.md

The domain analysis should help future prompts understand what types of new features would fit vs. conflict with the existing application architecture.

Once completed, continue to skill 2-categorize-files and continue on accordingly with {output-folder} as the `output-folder`