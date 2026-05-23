---
name: "sqlite-agent-context"
description: "Detect agent capabilities and manage context intelligently"
tags:
  - "agent"
  - "context"
  - "detection"
  - "capabilities"
  - "optimization"
version: "1.0.0"
---

# Agent Context Management

## Purpose

This skill enables agents to understand their own capabilities, manage context efficiently, and format responses appropriately for their specific platform (Claude, GPT-4, etc.).

Key capabilities:
- Auto-detect what type of agent is running
- Understand agent-specific capabilities and limitations
- Calculate token budgets and context usage
- Format responses optimally for each agent type
- Manage multi-turn conversation context

## When to Use

Use this skill when you need to:
- Detect what agent/model is running the code
- Check agent capabilities (tool use, vision, code execution, etc.)
- Calculate remaining token budget
- Format responses for specific agents
- Optimize context usage in long conversations
- Handle agent-specific features or limitations

## Available Hooks

### sqlite.context.detect

Auto-detect the current agent type and version.

**Parameters:**
- `hints` (object, optional): Detection hints
  - `userAgent` (string): User agent string
  - `environment` (object): Environment variables
  - `capabilities` (array): Known capabilities

**Returns:**
- `type` (string): Agent type (e.g., 'claude-code', 'gpt-4', 'gpt-3.5-turbo')
- `version` (string): Agent version
- `capabilities` (array): Detected capabilities
- `confidence` (number): Detection confidence (0-1)

**Example:**
```javascript
const agent = await fixiplug.dispatch('sqlite.context.detect');

console.log(agent.type);  // 'claude-code'
console.log(agent.version);  // '3.5-sonnet-20241022'
console.log(agent.capabilities);
// [
//   'tool-use',
//   'vision',
//   'code-execution',
//   'file-editing',
//   'artifacts',
//   'extended-thinking'
// ]
console.log(agent.confidence);  // 0.98

// Agent-specific logic
if (agent.type.startsWith('claude')) {
  console.log('Using Claude-specific formatting');
} else if (agent.type.startsWith('gpt')) {
  console.log('Using GPT-specific formatting');
}
```

### sqlite.context.capabilities

Get detailed capabilities for a specific agent type.

**Parameters:**
- `agentType` (string, required): Agent type (e.g., 'claude-3-5-sonnet', 'gpt-4')
- `includeDetails` (boolean, optional): Include detailed capability info (default: false)

**Returns:**
- `agentType` (string): Agent type
- `maxTokens` (number): Maximum context tokens
- `maxOutputTokens` (number): Maximum output tokens
- `toolUseSupport` (boolean): Supports tool/function calling
- `visionSupport` (boolean): Supports image inputs
- `streamingSupport` (boolean): Supports streaming responses
- `capabilities` (array): List of capabilities
- `limitations` (array): Known limitations
- `recommendedPractices` (array): Best practices for this agent

**Example:**
```javascript
const caps = await fixiplug.dispatch('sqlite.context.capabilities', {
  agentType: 'claude-3-5-sonnet',
  includeDetails: true
});

console.log(`Max tokens: ${caps.maxTokens}`);  // 200000
console.log(`Tool use: ${caps.toolUseSupport}`);  // true
console.log(`Vision: ${caps.visionSupport}`);  // true

console.log('Capabilities:', caps.capabilities);
// [
//   { name: 'tool-use', description: 'Can use tools/functions', enabled: true },
//   { name: 'vision', description: 'Can analyze images', enabled: true },
//   { name: 'extended-thinking', description: 'Has extended thinking mode', enabled: true },
//   ...
// ]

console.log('Limitations:', caps.limitations);
// [
//   'Cannot execute code directly in some environments',
//   'Image input size limited to 5MB',
//   'Max 5 images per request'
// ]

console.log('Best practices:', caps.recommendedPractices);
// [
//   'Use structured outputs for complex data',
//   'Break large tasks into smaller tool calls',
//   'Provide clear, detailed prompts for best results'
// ]
```

### sqlite.context.token_budget

Calculate remaining token budget for current conversation.

**Parameters:**
- `agentType` (string, optional): Agent type (auto-detected if omitted)
- `conversation` (array, required): Conversation history
  - Each item: `{ role: 'user' | 'assistant', content: string }`
- `systemPrompt` (string, optional): System prompt
- `includeBreakdown` (boolean, optional): Include detailed breakdown (default: false)

**Returns:**
- `totalTokens` (number): Total tokens used so far
- `maxTokens` (number): Maximum tokens allowed
- `remainingTokens` (number): Tokens remaining
- `percentageUsed` (number): Percentage of budget used
- `recommendation` (string): Recommendation for next steps
- `breakdown` (object, optional): Detailed token breakdown

**Example:**
```javascript
const budget = await fixiplug.dispatch('sqlite.context.token_budget', {
  agentType: 'claude-3-5-sonnet',
  conversation: [
    { role: 'user', content: 'What is 2+2?' },
    { role: 'assistant', content: '2+2 equals 4.' },
    { role: 'user', content: 'Explain why.' },
    { role: 'assistant', content: 'Addition is combining quantities...' }
  ],
  systemPrompt: 'You are a helpful math tutor.',
  includeBreakdown: true
});

console.log(`Used: ${budget.totalTokens} / ${budget.maxTokens}`);
// Used: 1250 / 200000

console.log(`Remaining: ${budget.remainingTokens} tokens`);
// Remaining: 198750 tokens

console.log(`Budget used: ${budget.percentageUsed}%`);
// Budget used: 0.6%

console.log('Recommendation:', budget.recommendation);
// 'Plenty of context remaining, no optimization needed'

console.log('Breakdown:', budget.breakdown);
// {
//   systemPrompt: 42,
//   userMessages: 580,
//   assistantMessages: 628,
//   overhead: 0,
//   total: 1250
// }

// Make decisions based on budget
if (budget.percentageUsed > 80) {
  console.log('Context nearly full, consider summarizing');
} else if (budget.percentageUsed > 50) {
  console.log('Context half-used, monitor usage');
} else {
  console.log('Plenty of context available');
}
```

### sqlite.context.format_response

Format a response optimally for the current agent.

**Parameters:**
- `content` (any, required): Content to format
- `responseType` (string, required): Type of response ('text', 'code', 'data', 'error')
- `agentType` (string, optional): Target agent type (auto-detected if omitted)
- `options` (object, optional): Formatting options

**Returns:**
- `formatted` (string): Formatted content
- `metadata` (object): Format metadata

**Example:**
```javascript
// Format code response
const formatted = await fixiplug.dispatch('sqlite.context.format_response', {
  content: {
    language: 'python',
    code: 'def hello():\n    print("Hello, world!")'
  },
  responseType: 'code',
  options: {
    includeComments: true,
    syntaxHighlight: true
  }
});

console.log(formatted.formatted);
// For Claude: Uses markdown code blocks with syntax highlighting
// For GPT: Uses appropriate formatting for GPT UI

// Format data response
const dataFormatted = await fixiplug.dispatch('sqlite.context.format_response', {
  content: {
    results: [
      { name: 'Alice', score: 95 },
      { name: 'Bob', score: 87 }
    ]
  },
  responseType: 'data',
  options: {
    format: 'table'  // or 'json', 'list'
  }
});

console.log(dataFormatted.formatted);
// Formatted as markdown table for Claude, or appropriate format for other agents
```

## Best Practices

### 1. Always Detect Before Optimizing

```javascript
// Good: Detect first
const agent = await fixiplug.dispatch('sqlite.context.detect');
if (agent.capabilities.includes('vision')) {
  // Use vision features
}

// Bad: Assume capabilities
// Just try to use vision without checking
```

### 2. Monitor Token Budget

```javascript
// In long conversations
async function checkBudget(conversation) {
  const budget = await fixiplug.dispatch('sqlite.context.token_budget', {
    conversation
  });

  if (budget.percentageUsed > 80) {
    // Summarize or truncate history
    return summarizeConversation(conversation);
  }

  return conversation;
}
```

### 3. Format Appropriately

```javascript
// Detect agent and format accordingly
const agent = await fixiplug.dispatch('sqlite.context.detect');

const response = await fixiplug.dispatch('sqlite.context.format_response', {
  content: data,
  responseType: 'data',
  agentType: agent.type
});

return response.formatted;
```

### 4. Cache Detection Results

```javascript
// Cache detection result (doesn't change during session)
let cachedAgent = null;

async function getAgent() {
  if (!cachedAgent) {
    cachedAgent = await fixiplug.dispatch('sqlite.context.detect');
  }
  return cachedAgent;
}
```

## Common Use Cases

### Use Case 1: Agent-Specific Features
```javascript
const agent = await fixiplug.dispatch('sqlite.context.detect');

if (agent.type.startsWith('claude-code')) {
  // Use file editing features
  console.log('Can use file editing tools');
} else if (agent.type.startsWith('gpt-4')) {
  // Use GPT-4 specific features
  console.log('Can use advanced reasoning');
}
```

### Use Case 2: Context Management
```javascript
async function manageConversation(conversation) {
  const budget = await fixiplug.dispatch('sqlite.context.token_budget', {
    conversation,
    includeBreakdown: true
  });

  console.log(`Context usage: ${budget.percentageUsed.toFixed(1)}%`);

  if (budget.percentageUsed > 75) {
    console.log('Approaching context limit, summarizing...');
    // Summarize older messages
    const summary = createSummary(conversation.slice(0, -10));
    return [
      { role: 'system', content: `Previous context: ${summary}` },
      ...conversation.slice(-10)
    ];
  }

  return conversation;
}
```

### Use Case 3: Capability Checks
```javascript
const caps = await fixiplug.dispatch('sqlite.context.capabilities', {
  agentType: 'claude-3-5-sonnet'
});

// Check if vision is supported
if (caps.visionSupport) {
  console.log('Can process images');
  // Include image analysis features
}

// Check tool use
if (caps.toolUseSupport) {
  console.log('Can use tools');
  // Enable tool-based workflows
}

console.log(`Max context: ${caps.maxTokens} tokens`);
```

### Use Case 4: Response Formatting
```javascript
// Data to return
const results = {
  users: [
    { id: 1, name: 'Alice', score: 95 },
    { id: 2, name: 'Bob', score: 87 }
  ]
};

// Format for current agent
const formatted = await fixiplug.dispatch('sqlite.context.format_response', {
  content: results,
  responseType: 'data',
  options: { format: 'table' }
});

console.log(formatted.formatted);
// Automatically formatted as markdown table, JSON, or other format
// depending on what works best for the current agent
```

## Agent Types Reference

### Claude Family
- `claude-code`: Claude Code CLI agent
- `claude-3-5-sonnet`: Claude 3.5 Sonnet
- `claude-3-opus`: Claude 3 Opus
- `claude-3-haiku`: Claude 3 Haiku

**Common Capabilities:**
- Tool use ✓
- Vision (3.5+ models) ✓
- Extended thinking ✓
- Streaming ✓

### GPT Family
- `gpt-4`: GPT-4 base model
- `gpt-4-turbo`: GPT-4 Turbo
- `gpt-3.5-turbo`: GPT-3.5 Turbo

**Common Capabilities:**
- Function calling ✓
- Vision (GPT-4 Vision) ✓
- Streaming ✓

## Performance Characteristics

- **Agent Detection**: ~50-100ms (cache this!)
- **Capabilities Lookup**: ~10-20ms
- **Token Budget Calc**: ~100-200ms (depends on conversation size)
- **Response Formatting**: ~50-150ms

## Error Handling

Possible errors:
- `DetectionError`: Could not detect agent type
- `UnsupportedAgentError`: Agent type not recognized
- `ValidationError`: Invalid parameters

Example:
```javascript
try {
  const agent = await fixiplug.dispatch('sqlite.context.detect');
} catch (error) {
  if (error.name === 'DetectionError') {
    console.warn('Could not detect agent, using defaults');
    // Fall back to generic agent handling
  } else {
    console.error('Unexpected error:', error.message);
  }
}
```

## Advanced Features

### Multi-Agent Coordination

When multiple agents are working together:
```javascript
const agents = await Promise.all([
  fixiplug.dispatch('sqlite.context.detect', { hints: { id: 'agent-1' } }),
  fixiplug.dispatch('sqlite.context.detect', { hints: { id: 'agent-2' } })
]);

// Coordinate based on capabilities
const primaryAgent = agents.find(a => a.capabilities.includes('code-execution'));
const supportAgent = agents.find(a => !a.capabilities.includes('code-execution'));
```

### Dynamic Capability Adjustment

```javascript
const agent = await fixiplug.dispatch('sqlite.context.detect');

// Adjust workflow based on capabilities
if (agent.capabilities.includes('vision')) {
  workflow.addStep('image-analysis');
}

if (agent.capabilities.includes('tool-use')) {
  workflow.addStep('tool-execution');
}
```

### Context-Aware Caching

```javascript
const budget = await fixiplug.dispatch('sqlite.context.token_budget', {
  conversation
});

// Adjust caching strategy based on budget
if (budget.percentageUsed < 20) {
  cacheStrategy = 'aggressive';  // Cache more
} else if (budget.percentageUsed < 60) {
  cacheStrategy = 'balanced';
} else {
  cacheStrategy = 'minimal';  // Cache less, free up context
}
```

## Prerequisites

- SQLite Extensions Framework installed
- Environment variable: `SQLITE_FRAMEWORK_PATH`

## Related Skills

- `sqlite-pattern-learner`: Learn from database patterns
- `sqlite-extension-generator`: Generate optimized code
- `sqlite-agent-amplification`: Dynamic tool creation

## Version

1.0.0 - Initial release
