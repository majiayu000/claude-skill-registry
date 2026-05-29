---
name: presentation-outline
description: Transform a Google Doc explaining a key topic into a structured presentation outline. Takes a source document and generates a slide-by-slide breakdown with titles, subtitles, and supporting bullet points, limited to a maximum of 10 slides. Displays the outline in the chat for review and editing.
---

# Presentation Outline

Generate a structured presentation outline from a Google Doc to quickly transform topic documentation into a presentation-ready format.

## How It Works

This skill takes a Google Doc containing information about a topic and transforms it into a presentation outline with the following structure per slide:

- **Slide Title** - The main topic or concept
- **Slide Subtitle** - Context or focus area (can be optional)
- **Bullet Points** - Supporting details (one subject per slide, 3-5 bullets)

The output is limited to a maximum of 10 slides for an optimal presentation length.

## Process

- **Provide a Google Doc** - Share the URL or ID of a Google Doc containing the topic information
- **Outline Generation** - Claude extracts key concepts and organizes them into distinct slides
- **Chat Display** - The outline is displayed in the chat window for you to review and edit
- **Refinement** - Adjust titles, subtitles, or bullets as needed

## Guidelines for Best Results

For detailed best practices on what makes an effective presentation outline, see `references/guide.md`. Key principles include:

- **One topic per slide** - Each slide focuses on a single main concept
- **Concise titles** - 3-8 words that clearly identify the slide topic
- **Supporting bullets** - 3-5 bullet points per slide that support the main topic
- **Optimal length** - 8-10 slides provides balanced pacing for a 20-30 minute presentation
- **Logical flow** - Clear progression from opening to conclusion

## Output Format

The outline is displayed in markdown format in the chat with clear delineation between slides:

```
# Slide 1: [Title]
**Subtitle**: [Subtitle if applicable]
- Bullet point 1
- Bullet point 2
- Bullet point 3

# Slide 2: [Title]
**Subtitle**: [Subtitle if applicable]
- Bullet point 1
- Bullet point 2
- Bullet point 3
```

## Tips

- Longer, more detailed source documents produce better outlines
- Ensure your Google Doc clearly separates different topics and concepts
- Review the generated outline and edit slide titles/bullets for your specific audience
- If the outline exceeds 10 slides, consider combining related slides or removing less critical content