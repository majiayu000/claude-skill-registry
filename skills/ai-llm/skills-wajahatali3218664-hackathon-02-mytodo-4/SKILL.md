---
name: groq-inference-skill
description: Use Groq for fast LLM inference with OpenAI-compatible client
when-to-use: AI agent logic, natural language processing
---
# Groq Inference Skill

## Instructions

This skill provides guidance for using Groq's fast LLM inference with an OpenAI-compatible client for AI agent logic and natural language processing.

### Project Structure
```
src/lib/
├── groq.ts                    # Groq client configuration
├── agents/
│   ├── task-agent.ts          # Task management agent
│   ├── planner-agent.ts       # Task planning agent
│   └── base-agent.ts          # Base agent class
└── prompts/
    ├── system-prompts.ts      # System prompt templates
    └── few-shot-examples.ts   # Example conversations
```

### Groq Client Setup

```tsx
// src/lib/groq.ts
import OpenAI from 'openai'

// Groq uses OpenAI-compatible API
export const groqClient = new OpenAI({
  apiKey: process.env.GROQ_API_KEY,
  baseURL: 'https://api.groq.com/openai/v1',
})

// Available Groq models (fast inference)
export const GROQ_MODELS = {
  LLAMA3_8B: 'llama3-8b-8192',
  LLAMA3_70B: 'llama3-70b-8192',
  MIXTRAL: 'mixtral-8x7b-32768',
  GEMMA: 'gemma-7b-it',
} as const

export type GroqModel = (typeof GROQ_MODELS)[keyof typeof GROQ_MODELS]

export interface GroqCompletionOptions {
  model?: GroqModel
  temperature?: number
  max_tokens?: number
  top_p?: number
  stream?: boolean
  stop?: string[]
}
```

### Basic Inference

```tsx
// src/lib/groq.ts (continued)
export async function createGroqCompletion(
  messages: { role: 'system' | 'user' | 'assistant'; content: string }[],
  options: GroqCompletionOptions = {}
) {
  const response = await groqClient.chat.completions.create({
    model: options.model || GROQ_MODELS.LLAMA3_70B,
    messages,
    temperature: options.temperature ?? 0.6,
    max_tokens: options.max_tokens ?? 1024,
    top_p: options.top_p ?? 0.9,
    stream: options.stream ?? false,
    stop: options.stop,
  })

  return response
}

export async function createGroqCompletionSimple(
  prompt: string,
  systemPrompt?: string
) {
  const messages: { role: 'system' | 'user'; content: string }[] = []

  if (systemPrompt) {
    messages.push({ role: 'system', content: systemPrompt })
  }

  messages.push({ role: 'user', content: prompt })

  const response = await createGroqCompletion(messages)
  return response.choices[0]?.message?.content || ''
}
```

### Task Management Agent

```tsx
// src/lib/agents/task-agent.ts
import { createGroqCompletion } from '../groq'
import { GROQ_MODELS } from '../groq'
import type { Task } from '@/types'

// System prompt for task agent
const TASK_AGENT_SYSTEM_PROMPT = `You are a helpful task management assistant.
Your role is to:
1. Parse natural language requests about tasks
2. Extract task details (title, description, due date, priority)
3. Generate appropriate tool calls for task operations
4. Provide helpful summaries and suggestions

When the user asks to create a task, extract and format:
- title: Clear, concise task title
- description: Detailed description if provided
- due_date: ISO date format if specified
- priority: 'low', 'medium', or 'high' if mentioned

Always respond in a helpful, concise manner.`

export interface ParsedTaskIntent {
  action: 'create' | 'update' | 'delete' | 'list' | 'complete' | 'query'
  task?: Partial<Task>
  task_id?: number
  natural_response: string
}

export async function parseTaskIntent(userInput: string): Promise<ParsedTaskIntent> {
  const prompt = `Parse this user request and identify the task management intent.

User request: "${userInput}"

Respond with JSON:
{
  "action": "create|update|delete|list|complete|query",
  "task": { "title": "...", "description": "...", "due_date": "...", "priority": "..." },
  "task_id": number (if referring to existing task),
  "natural_response": "Brief response acknowledging the request"
}`

  const response = await createGroqCompletion(
    [
      { role: 'system', content: TASK_AGENT_SYSTEM_PROMPT },
      { role: 'user', content: prompt },
    ],
    {
      model: GROQ_MODELS.LLAMA3_70B,
      temperature: 0.3,
      max_tokens: 512,
    }
  )

  try {
    const parsed = JSON.parse(response.choices[0]?.message?.content || '{}')
    return {
      action: parsed.action || 'query',
      task: parsed.task,
      task_id: parsed.task_id,
      natural_response: parsed.natural_response || 'I understand.',
    }
  } catch {
    return {
      action: 'query',
      natural_response: "I'm not sure what you'd like to do with your tasks. Could you clarify?",
    }
  }
}

export async function generateTaskSuggestions(tasks: Task[]): Promise<string[]> {
  const prompt = `Given these tasks:
${tasks.map((t, i) => `${i + 1}. ${t.title} ${t.completed ? '(completed)' : ''}`).join('\n')}

Suggest 3-5 practical, specific suggestions to help the user be more productive.
Format as a JSON array of strings.`

  const response = await createGroqCompletion(
    [
      {
        role: 'system',
        content: 'You are a productivity assistant. Provide actionable, specific suggestions.',
      },
      { role: 'user', content: prompt },
    ],
    {
      model: GROQ_MODELS.LLAMA3_70B,
      temperature: 0.7,
      max_tokens: 256,
    }
  )

  try {
    return JSON.parse(response.choices[0]?.message?.content || '[]')
  } catch {
    return []
  }
}
```

### Task Planner Agent

```tsx
// src/lib/agents/planner-agent.ts
import { createGroqCompletion } from '../groq'
import { GROQ_MODELS } from '../groq'

export interface TaskBreakdown {
  steps: {
    title: string
    description: string
    priority: 'must' | 'should' | 'could'
    estimated_time?: string
  }[]
  total_estimate: string
  recommendations: string[]
}

export async function breakdownTask(userInput: string): Promise<TaskBreakdown> {
  const prompt = `Break down this task/project into actionable steps:

"${userInput}"

Provide a detailed breakdown with:
1. Sequential steps with descriptions
2. Priority levels (must/should/could)
3. Time estimates
4. Recommendations

Respond with JSON:
{
  "steps": [
    { "title": "...", "description": "...", "priority": "must|should|could", "estimated_time": "..." }
  ],
  "total_estimate": "...",
  "recommendations": ["...", "..."]
}`

  const response = await createGroqCompletion(
    [
      {
        role: 'system',
        content: 'You are a project planning assistant. Break down complex tasks into clear, actionable steps.',
      },
      { role: 'user', content: prompt },
    ],
    {
      model: GROQ_MODELS.LLAMA3_70B,
      temperature: 0.5,
      max_tokens: 1024,
    }
  )

  try {
    return JSON.parse(response.choices[0]?.message?.content || '{}')
  } catch {
    return {
      steps: [],
      total_estimate: 'Unknown',
      recommendations: [],
    }
  }
}

export async function prioritizeTasks(
  tasks: { id: number; title: string; due_date?: string }[]
): Promise<number[]> {
  const prompt = `Prioritize these tasks by ID based on urgency and importance:

${tasks.map(t => `ID: ${t.id}, Title: ${t.title}${t.due_date ? `, Due: ${t.due_date}` : ''}`).join('\n')}

Return the task IDs in priority order (most important first) as a JSON array.`

  const response = await createGroqCompletion(
    [
      {
        role: 'system',
        content: 'You are a task prioritization assistant. Consider due dates, urgency, and importance.',
      },
      { role: 'user', content: prompt },
    ],
    {
      model: GROQ_MODELS.LLAMA3_70B,
      temperature: 0.3,
      max_tokens: 128,
    }
  )

  try {
    const prioritized = JSON.parse(response.choices[0]?.message?.content || '[]')
    return tasks.map(t => t.id).filter(id => prioritized.includes(id))
  } catch {
    return tasks.map(t => t.id)
  }
}
```

### Streaming Inference

```tsx
// src/lib/groq.ts (continued)
export async function* streamGroqCompletion(
  messages: { role: 'system' | 'user' | 'assistant'; content: string }[],
  options: GroqCompletionOptions = {}
): AsyncGenerator<string> {
  const stream = await groqClient.chat.completions.create({
    model: options.model || GROQ_MODELS.LLAMA3_70B,
    messages,
    temperature: options.temperature ?? 0.6,
    max_tokens: options.max_tokens ?? 2048,
    stream: true,
  })

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content
    if (content) {
      yield content
    }
  }
}

// Usage
export async function streamTaskAdvice(): Promise<string> {
  let fullResponse = ''

  const stream = streamGroqCompletion([
    {
      role: 'system',
      content: 'You are a productivity expert. Give concise, actionable advice.',
    },
    {
      role: 'user',
      content: 'Give me 3 tips for better task management.',
    },
  ])

  for await (const chunk of stream) {
    fullResponse += chunk
  }

  return fullResponse
}
```

## Examples

### Natural Language Task Creation

```tsx
// src/lib/agents/task-parser.ts
export async function parseNaturalLanguageTask(input: string) {
  const prompt = `Extract task information from this user input:

"${input}"

If this is a task creation request, extract:
- title: Main task title (required)
- description: Additional details (optional)
- due_date: When it should be completed (optional, ISO format)
- priority: urgency level (optional, low/medium/high)

If this is NOT a task creation request, return null for task fields.

Respond in JSON format.`

  const response = await createGroqCompletion(
    [
      {
        role: 'system',
        content: 'You are a task parsing assistant. Extract structured data from natural language.',
      },
      { role: 'user', content: prompt },
    ],
    { temperature: 0.2 }
  )

  return JSON.parse(response.choices[0]?.message?.content || '{}')
}

// Example usage:
// parseNaturalLanguageTask("Remind me to call mom on Friday at 5pm")
// Returns: { title: "Call mom", description: "", due_date: "2024-01-05T17:00:00Z", priority: "medium" }
```

### Smart Task Search

```tsx
// src/lib/agents/task-search.ts
export async function searchTasksSmart(query: string, tasks: Task[]): Promise<Task[]> {
  const taskList = tasks.map(t =>
    `ID:${t.id} Title:${t.title} Desc:${t.description || 'none'} Status:${t.completed ? 'done' : 'pending'}`
  ).join('\n')

  const prompt = `Search for tasks matching this query: "${query}"

Available tasks:
${taskList}

Return the IDs of matching tasks as a JSON array. Consider:
- Keywords in title and description
- Task completion status
- Partial matches
- Related concepts`

  const response = await createGroqCompletion(
    [
      {
        role: 'system',
        content: 'You are a task search assistant. Find relevant matches based on semantic understanding.',
      },
      { role: 'user', content: prompt },
    ],
    { temperature: 0.3, max_tokens: 256 }
  )

  try {
    const ids: number[] = JSON.parse(response.choices[0]?.message?.content || '[]')
    return tasks.filter(t => ids.includes(t.id))
  } catch {
    // Fallback to simple search
    const lowerQuery = query.toLowerCase()
    return tasks.filter(t =>
      t.title.toLowerCase().includes(lowerQuery) ||
      t.description?.toLowerCase().includes(lowerQuery)
    )
  }
}
```

### Batch Processing with Groq

```tsx
// Process multiple tasks in parallel
async function analyzeTaskBatch(tasks: Task[]) {
  const batchPrompt = tasks.map((t, i) =>
    `${i + 1}. "${t.title}" - ${t.description || 'no description'}`
  ).join('\n')

  const prompt = `Analyze these ${tasks.length} tasks and provide:
1. Estimated effort (1-10) for each
2. Potential blockers
3. Suggested order

Tasks:
${batchPrompt}

Respond with JSON array of analysis results.`

  const response = await createGroqCompletion(
    [
      {
        role: 'system',
        content: 'You are a project analyst. Assess tasks objectively.',
      },
      { role: 'user', content: prompt },
    ],
    {
      model: GROQ_MODELS.LLAMA3_70B,
      temperature: 0.5,
      max_tokens: tasks.length * 200,
    }
  )

  return JSON.parse(response.choices[0]?.message?.content || '[]')
}
```
