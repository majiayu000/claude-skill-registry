---
name: interview
description: Gather structured user input via web form. Use when you need multiple clarifying questions answered, collecting design mockups/images, or getting user decisions on implementation choices. Better than sequential chat Q&A when 3+ questions are needed.
---

# Interview Skill

Use the `interview()` tool to open a web form for structured user input.

## When to Use Interview

**DO use interview for:**
- 3+ clarifying questions needed before starting work
- Collecting images, mockups, or screenshots
- Multiple-choice decisions (framework, features, architecture)
- Gathering requirements for new features/projects
- Getting user sign-off on options discovered during analysis

**DON'T use interview for:**
- Simple yes/no questions → just ask in chat
- Single clarifying question → just ask in chat
- Information you can find in the codebase
- Questions where you can make reasonable defaults

## Basic Workflow

```javascript
// 1. Construct questions based on what you need to know
const questions = {
  title: "Descriptive Title",
  description: "Brief context for the user",
  questions: [
    { id: "unique-id", type: "single|multi|text|image", question: "..." }
  ]
};

// 2. Write to temp file
// Use: /tmp/interview-{context}.json
write('/tmp/interview-feature-setup.json', JSON.stringify(questions, null, 2));

// 3. Invoke the tool
await interview({ questions: '/tmp/interview-feature-setup.json' });

// 4. Process responses and proceed with work
```

## Question Types

| Type | Use For | Returns |
|------|---------|---------|
| `single` | One choice from options | `string` |
| `multi` | Multiple selections | `string[]` |
| `text` | Free-form input | `string` |
| `image` | Upload mockup/screenshot | `string` (path) |

## Question Schema

```json
{
  "id": "unique-identifier",
  "type": "single",
  "question": "Clear, specific question text",
  "options": ["Option A", "Option B", "Option C"],
  "recommended": "Option A",
  "context": "Help text explaining the options"
}
```

**Fields:**
- `id` (required): Unique identifier for the response
- `type` (required): `single`, `multi`, `text`, or `image`
- `question` (required): The question text
- `options` (required for single/multi): Array of choices
- `recommended` (optional): Highlight suggested option(s) with `*`
- `context` (optional): Help text shown below question

## Patterns by Scenario

### Project/Feature Setup

```json
{
  "title": "Feature Requirements",
  "description": "Help me understand what you need before I create the implementation plan.",
  "questions": [
    {
      "id": "approach",
      "type": "single",
      "question": "Which approach should we take?",
      "options": ["Option A - faster", "Option B - more flexible", "Research both"],
      "recommended": "Option A - faster",
      "context": "Based on the codebase, Option A aligns with existing patterns."
    },
    {
      "id": "scope",
      "type": "multi",
      "question": "Which components should be included?",
      "options": ["Core feature", "Admin UI", "API endpoints", "Tests", "Documentation"],
      "recommended": ["Core feature", "Tests"]
    },
    {
      "id": "constraints",
      "type": "text",
      "question": "Any constraints or requirements I should know about?"
    }
  ]
}
```

### Code Review Decisions

```json
{
  "title": "Code Review Findings",
  "description": "I found some issues. How would you like me to handle them?",
  "questions": [
    {
      "id": "deprecated-api",
      "type": "single",
      "question": "Found deprecated API usage in 3 files. How to handle?",
      "options": ["Fix now", "Create issue for later", "Ignore - acceptable tech debt"],
      "recommended": "Fix now"
    },
    {
      "id": "missing-tests",
      "type": "single",
      "question": "Test coverage for changed files is 30%. Add tests?",
      "options": ["Yes - critical paths only", "Yes - comprehensive coverage", "No - ship as is"],
      "recommended": "Yes - critical paths only"
    }
  ]
}
```

### Design/Visual Input

```json
{
  "title": "UI Implementation",
  "description": "Upload your design and specify preferences.",
  "questions": [
    {
      "id": "mockup",
      "type": "image",
      "question": "Upload design mockup or screenshot",
      "context": "PNG, JPG, GIF, or WebP. You can also paste or drag & drop."
    },
    {
      "id": "fidelity",
      "type": "single",
      "question": "How closely should I match the design?",
      "options": ["Pixel-perfect", "Approximate - focus on functionality", "Use as inspiration only"],
      "recommended": "Approximate - focus on functionality"
    },
    {
      "id": "responsive",
      "type": "multi",
      "question": "Which screen sizes to support?",
      "options": ["Mobile", "Tablet", "Desktop"],
      "recommended": ["Mobile", "Desktop"]
    }
  ]
}
```

### Ambiguous Request Clarification

```json
{
  "title": "Clarifying Your Request",
  "description": "I want to make sure I understand what you need.",
  "questions": [
    {
      "id": "interpretation",
      "type": "single",
      "question": "When you said 'improve performance', did you mean:",
      "options": [
        "Faster load times",
        "Reduced memory usage", 
        "Better responsiveness/UX",
        "All of the above"
      ]
    },
    {
      "id": "priority",
      "type": "single",
      "question": "What's most important?",
      "options": ["Ship fast", "High quality", "Balance both"],
      "recommended": "Balance both"
    }
  ]
}
```

## Best Practices

### Writing Good Questions

1. **Be specific** - "Which auth provider?" not "How should auth work?"
2. **Provide context** - Use `context` field to explain trade-offs
3. **Use recommendations** - Help users decide with `recommended` field
4. **Include escape hatches** - Add "Not sure - you decide" or "Research for me" options
5. **Keep it focused** - 3-7 questions max; split into multiple interviews if needed

### Constructing Options

- Put most likely choice first
- Include "Other" for single/multi if appropriate (handled automatically)
- Be concise but clear - "React - largest ecosystem" not just "React"
- For technical choices, briefly note trade-offs

### When NOT to Interview

- You can infer from codebase patterns
- User already specified in their request
- There's an obvious default that's almost always right
- It's a simple yes/no (just ask inline)

## Tool Parameters

```javascript
await interview({
  questions: '/path/to/questions.json',  // Required: path to questions file
  timeout: 600,                          // Optional: seconds (default 600)
  verbose: false                         // Optional: debug logging
});
```

## Response Format

The tool returns structured responses:

```typescript
interface Response {
  id: string;
  value: string | string[];
  attachments?: string[];  // Image paths for non-image questions
}
```

Example response:
```
- approach: Option A - faster
- scope: Core feature, Tests
- constraints: Must work with existing auth system
- mockup: /tmp/uploaded-image.png
```

## Limits

- Max 12 images total per submission
- Max 5MB per image
- Max 4096x4096 pixels per image
- Allowed types: PNG, JPG, GIF, WebP
