---
name: prompt-engineering
description: Prompt engineering for Claude API, system prompts, context management, instruction design, depth levels, HTML generation. Use when working with Claude API integration, designing prompts, managing conversation context, or implementing AI-powered features.
allowed-tools: Read, Grep, Glob
---

# Prompt Engineering for Claude API

## Core Principles

1. **Clear Instructions** - Be specific about what you want Claude to do
2. **Context First** - Provide all necessary context before asking
3. **Examples Work** - Show examples of desired output
4. **Constraints Matter** - Define boundaries and rules explicitly
5. **Iterate and Test** - Refine prompts based on actual outputs

---

## System Prompt Structure

The system prompt in `server/prompts/system.txt` is the foundation of Claude's behavior.

### CORRECT: Well-Structured System Prompt

```
You are an expert instructional designer and educational content creator. Your job is to generate complete, self-contained HTML pages for educational purposes.

# Your Role

You create educational content at various depth levels (0-4) based on user specifications. Each page you generate must be:
- A single, complete HTML file
- Ready to paste into Blackboard LMS
- Styled with inline CSS (no external stylesheets)
- Accessible and well-structured
- Appropriate for the specified depth level

# Depth Levels (CRITICAL - NEVER DEVIATE)

Level 0 (Minimalist): Reference-only content. Tables, lists, minimal explanation.
- Example: CSS property reference table
- NO introductions, NO explanations, NO examples
- Just the facts in organized format

Level 1 (Introductory): For complete beginners with zero knowledge.
- Example: "What is a variable?"
- Simple language, no jargon, extensive analogies
- No code examples unless absolutely necessary
- Focus on concepts, not implementation

Level 2 (Intermediate): For students with basic programming knowledge.
- Example: "JavaScript Promises"
- Explain how and why, include code examples
- Balance theory and practice
- Assume basic CS knowledge

Level 3 (Advanced): For professional developers.
- Example: "RESTful API Design Best Practices"
- Production-ready patterns, edge cases, performance
- Assume strong programming background
- Include real-world considerations

Level 4 (Graduate): Academic and theoretical depth.
- Example: "Complexity Theory and P vs NP"
- Formal notation, proofs, academic rigor
- Citations and references
- Theoretical foundations

**CRITICAL RULE**: You MUST stay within the selected depth level. Do not mix levels.

# Style Flags

When the user enables style flags, incorporate these elements:

- **Accessibility**: WCAG 2.1 AA compliant, ARIA labels, screen reader friendly, high contrast
- **Visual-heavy**: Diagrams, charts, color coding, visual hierarchy, infographics
- **Technical**: Code snippets, terminal commands, technical terminology, implementation details
- **Conversational**: Friendly tone, direct address, casual language, analogies
- **Humor**: Appropriate jokes, light-hearted examples, playful language (never crude)

# HTML Template Structure

Always use this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Topic Title]</title>
    <style>
        /* Inline CSS here */
        body {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        /* More styles */
    </style>
</head>
<body>
    <!-- Content here -->
</body>
</html>
```

# Image Handling

When images are provided:
- Use external URLs (from Cloudinary)
- Include alt text for accessibility
- Ensure images enhance understanding
- Add captions where appropriate

Example:
```html
<figure>
    <img src="https://res.cloudinary.com/..." alt="Diagram showing..." />
    <figcaption>Figure 1: Description of diagram</figcaption>
</figure>
```

# Iteration and Refinement

When the user requests changes:
- Read the conversation history to understand context
- Apply changes to the ENTIRE page (regenerate fully)
- Maintain consistency with original depth level
- Preserve style flags unless asked to change

# Output Format

Your response must include:
1. A brief message to the user (1-2 sentences)
2. The complete HTML (wrapped in ```html code block)

Example response format:
```
I've created an intermediate-level page about JavaScript Promises with code examples and explanations.

```html
<!DOCTYPE html>
...complete HTML...
</html>
```
```

# Constraints

- NO external dependencies (CSS frameworks, JavaScript libraries)
- ALL styles must be inline in <style> tag
- ALL scripts must be inline in <script> tag
- Images must use external URLs only (Cloudinary)
- File size: Keep under 500KB when possible
- Must work in Blackboard's content editor
```

### WRONG: Vague System Prompt

```
You are a helpful assistant that creates educational content. Generate HTML pages based on user requests. Make them look nice.
```

Issues:
- No specific role definition
- No output format specified
- No depth level guidance
- No constraints defined
- No examples

---

## User Prompt Construction

### Building the Initial Generation Prompt

```javascript
// server/routes/generate.js
const buildInitialPrompt = (config) => {
  const { topic, depthLevel, styleFlags = [] } = config;

  let prompt = `Create an educational page about: ${topic}\n\n`;
  prompt += `Depth Level: ${depthLevel}\n`;

  if (styleFlags.length > 0) {
    prompt += `Style Flags: ${styleFlags.join(', ')}\n`;
  }

  return prompt;
};

// Example output:
// "Create an educational page about: JavaScript Async/Await
//
// Depth Level: 2
// Style Flags: visual-heavy, technical"
```

### Building Iteration Prompts

```javascript
const buildIterationPrompt = (userMessage, previousHtml, config) => {
  let prompt = userMessage + '\n\n';
  prompt += `Make this change to the existing page.\n`;
  prompt += `Maintain Depth Level: ${config.depthLevel}\n`;

  // Don't send full HTML back, Claude has it in conversation history
  // Just reference it
  prompt += `The current page HTML is in the conversation history above.`;

  return prompt;
};
```

---

## Conversation Context Management

### CORRECT: Maintaining Context

```javascript
// server/routes/generate.js
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

export const generatePage = async (config, userMessage, conversationHistory) => {
  // Build messages array with full history
  const messages = [
    // Include all previous messages for context
    ...conversationHistory.map(msg => ({
      role: msg.role,
      content: msg.content
    })),
    // Add new user message
    {
      role: 'user',
      content: buildPrompt(config, userMessage)
    }
  ];

  try {
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 8192, // Enough for full HTML page
      system: systemPrompt, // From server/prompts/system.txt
      messages: messages,
      temperature: 1.0 // Default creativity
    });

    return {
      message: extractMessage(response.content[0].text),
      html: extractHTML(response.content[0].text)
    };
  } catch (error) {
    throw new Error(`Claude API error: ${error.message}`);
  }
};
```

### Extracting HTML from Response

```javascript
const extractHTML = (responseText) => {
  // Claude wraps HTML in ```html code blocks
  const htmlMatch = responseText.match(/```html\n([\s\S]*?)\n```/);

  if (htmlMatch) {
    return htmlMatch[1].trim();
  }

  // Fallback: look for <!DOCTYPE html>
  const doctypeMatch = responseText.match(/<!DOCTYPE html>[\s\S]*/i);
  if (doctypeMatch) {
    return doctypeMatch[0].trim();
  }

  throw new Error('Could not extract HTML from response');
};

const extractMessage = (responseText) => {
  // Get text before the ```html code block
  const parts = responseText.split('```html');
  return parts[0].trim();
};
```

---

## Streaming Responses Pattern

For better UX with long generations:

```javascript
export const generatePageStream = async (config, userMessage, history, onChunk) => {
  const messages = [
    ...history.map(msg => ({ role: msg.role, content: msg.content })),
    { role: 'user', content: buildPrompt(config, userMessage) }
  ];

  const stream = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 8192,
    system: systemPrompt,
    messages: messages,
    stream: true // Enable streaming
  });

  let fullText = '';

  for await (const chunk of stream) {
    if (chunk.type === 'content_block_delta' && chunk.delta.type === 'text_delta') {
      const text = chunk.delta.text;
      fullText += text;

      // Send incremental updates
      onChunk({
        type: 'text',
        content: text,
        fullText: fullText
      });
    } else if (chunk.type === 'message_stop') {
      onChunk({
        type: 'done',
        message: extractMessage(fullText),
        html: extractHTML(fullText)
      });
    }
  }
};
```

---

## Depth Level Enforcement

The system prompt defines depth levels, but you can add safeguards:

```javascript
const validateDepthLevel = (config, generatedHtml) => {
  const { depthLevel } = config;

  // Simple heuristics (not foolproof, but helpful)
  const codeBlocks = (generatedHtml.match(/<code>/g) || []).length;
  const wordCount = generatedHtml.split(/\s+/).length;

  const warnings = [];

  if (depthLevel === 0 && wordCount > 200) {
    warnings.push('Level 0 should be more concise');
  }

  if (depthLevel === 1 && codeBlocks > 2) {
    warnings.push('Level 1 should avoid code examples');
  }

  if (depthLevel === 4 && !generatedHtml.includes('theorem') && !generatedHtml.includes('proof')) {
    warnings.push('Level 4 should include formal academic content');
  }

  return warnings;
};
```

---

## Image Integration Prompts

### Requesting Image Generation

```javascript
// When user says "generate a diagram of X"
const imageGenerationPrompt = `
The user has requested an image: "${userRequest}"

I will now generate this image using DALL-E and provide the URL. Once you have the URL, incorporate it into the page with:
- Appropriate placement in the content flow
- Descriptive alt text for accessibility
- A caption explaining the image
- Styling that fits the page design
`;
```

### Adding User-Provided Images

```javascript
const addImagePrompt = (imageUrl, description) => `
Add this image to the page:
URL: ${imageUrl}
Description: ${description || 'User-provided image'}

Place it where it makes most sense in the content and add appropriate styling.
`;
```

---

## Error Handling in Prompts

### Handling Generation Failures

```javascript
const handleGenerationError = async (error, config, userMessage, history) => {
  if (error.message.includes('max_tokens')) {
    // Response too long - ask Claude to shorten
    const retryPrompt = `${userMessage}\n\nNote: Please make the content more concise to fit within token limits.`;
    return generatePage(config, retryPrompt, history);
  }

  if (error.message.includes('rate_limit')) {
    // Rate limited - wait and retry
    await new Promise(resolve => setTimeout(resolve, 2000));
    return generatePage(config, userMessage, history);
  }

  throw error;
};
```

---

## Testing Prompts

Always test prompts with various inputs:

```javascript
// Test depth levels
const testDepthLevels = async () => {
  const topic = 'JavaScript Promises';

  for (let level = 0; level <= 4; level++) {
    const result = await generatePage(
      { topic, depthLevel: level, styleFlags: [] },
      `Create a page about ${topic}`,
      []
    );

    console.log(`Level ${level}:`, {
      wordCount: result.html.split(/\s+/).length,
      hasCode: result.html.includes('<code>'),
      hasExamples: result.html.toLowerCase().includes('example')
    });
  }
};

// Test style flags
const testStyleFlags = async () => {
  const combinations = [
    ['accessibility'],
    ['visual-heavy'],
    ['technical', 'conversational'],
    ['humor', 'visual-heavy']
  ];

  for (const flags of combinations) {
    const result = await generatePage(
      { topic: 'CSS Grid', depthLevel: 2, styleFlags: flags },
      'Create a page about CSS Grid',
      []
    );

    console.log(`Flags ${flags.join(', ')}:`, {
      hasAriaLabels: result.html.includes('aria-'),
      hasVisuals: result.html.includes('<svg>') || result.html.includes('style='),
      hasCode: result.html.includes('<code>'),
      hasHumor: /😄|🎉|funny|joke/i.test(result.html)
    });
  }
};
```

---

## Checklist

### Before Implementing Prompt
- [ ] Clear role and purpose defined
- [ ] Output format specified
- [ ] Constraints explicitly stated
- [ ] Examples provided where helpful
- [ ] Edge cases considered

### After Implementing Prompt
- [ ] Tested with various inputs
- [ ] Depth levels enforced correctly
- [ ] Style flags working as expected
- [ ] HTML extraction reliable
- [ ] Error cases handled
- [ ] Conversation context maintained
- [ ] Token usage reasonable

---

## Integration with Other Skills

- **express-api-patterns**: Implementing prompt endpoints
- **api-client-patterns**: Calling Claude API from client
- **systematic-debugging**: Debugging prompt issues
- **react-component-patterns**: Displaying generated content

---

## Common Mistakes to Avoid

1. ❌ Vague instructions in system prompt
2. ❌ Not maintaining conversation history
3. ❌ Missing output format specification
4. ❌ No examples in system prompt
5. ❌ Forgetting to extract HTML from response
6. ❌ Not handling streaming properly
7. ❌ Ignoring token limits
8. ❌ Not testing with edge cases
9. ❌ Missing error handling for API failures
10. ❌ Not enforcing depth level constraints
