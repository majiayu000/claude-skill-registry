---
name: information-architecture
description: Structuring information and content for clarity and navigation
category: Domain Architecture
---

# Skill: information-architecture

## What I do

I help you organise and structure content so users can find what they need with minimal effort. I focus on creating logical hierarchies, clear labelling systems, and intuitive navigation paths. I ensure that the way information is presented matches how users think about the domain.

## When to use me

- When you're designing the navigation for a complex documentation site.
- When you're categorising large sets of files or data.
- When you're creating a search experience that needs to be more than just keyword matching.
- When you're deciding how to group features or settings in a user interface.

## Core principles

1. **Mental model alignment**, structure information according to how your users perceive the system, not how the database is built.
2. **Progressive disclosure**, show only what's necessary at any given moment to avoid overwhelming the user.
3. **Consistency and predictability**, use familiar terms and patterns so users can predict where to find information.
4. **Contextual wayfinding**, always let the user know where they are, where they can go, and how to get back.

## Patterns & examples

### Content hierarchy
Organise information from general to specific.
- **Global**, highest level categories (e.g., Guides, API Reference, Tutorials).
- **Local**, sub-sections within a category (e.g., Authentication, Data Fetching).
- **Contextual**, links to related topics based on the current page.

### Labelling systems
Use clear and descriptive labels that avoid internal jargon.
- **Good**, "User Settings", "Project Configuration".
- **Bad**, "Account Management Module", "Global Config Flags".

### Search vs Browse
Design for both discovery paths.
- **Search**, optimized for users who know exactly what they want.
- **Browse**, optimized for users who are exploring or don't know the exact term.

### Breadcrumb trails
Always provide a path back to the home page or parent category.
- **Example**, `Home > Documentation > API > Authentication`

## Anti-patterns to avoid

- ❌ **Deep nesting**, buried content is hard to find and frustrates users. Keep hierarchies shallow.
- ❌ **Ambiguous labels**, terms like "Misc" or "Other" become dumping grounds for unrelated content.
- ❌ **Inside-out design**, structuring the UI based on your internal team structure rather than user needs.
- ❌ **Hidden navigation**, hiding main menu items behind icons or sub-menus without a clear reason.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Domain-Architecture/Information Architecture.md`

## Related skills

- `ux-design`, for designing the interaction layer.
- `documentation-writing`, for the actual content creation.
- `domain-modeling`, for aligning technical structures with business logic.
- `systems-thinker`, for understanding complex interconnections.
