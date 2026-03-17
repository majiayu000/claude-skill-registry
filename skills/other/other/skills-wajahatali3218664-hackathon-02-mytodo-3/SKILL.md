---
name: openai-chatkit-skill
description: Integrate OpenAI ChatKit for conversational AI interface
when-to-use: Building chat UI, handling messages, tool calls display
---
# OpenAI ChatKit Skill

## Instructions

This skill provides guidance for integrating OpenAI's ChatKit interface for conversational AI experiences.

### Project Structure
```
src/
├── components/
│   └── chat/
│       ├── ChatWindow.tsx      # Main chat container
│       ├── ChatMessage.tsx     # Individual message display
│       ├── ChatInput.tsx       # User input area
│       ├── ChatToolbar.tsx     # Quick actions toolbar
│       └── typing-indicator.tsx
├── hooks/
│   └── useChat.ts              # Chat state management
├── lib/
│   └── openai.ts               # OpenAI client configuration
└── types/
    └── chat.ts                 # Chat type definitions
```

### Type Definitions

```tsx
// src/types/chat.ts
export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  tools?: ToolCall[]
}

export interface ToolCall {
  id: string
  name: string
  arguments: Record<string, unknown>
  result?: unknown
}

export interface ChatState {
  messages: ChatMessage[]
  isLoading: boolean
  error: string | null
}

export interface UseChatReturn extends ChatState {
  sendMessage: (content: string) => Promise<void>
  clearMessages: () => void
  retry: () => Promise<void>
}
```

### OpenAI Client Setup

```tsx
// src/lib/openai.ts
import OpenAI from 'openai'

export const openai = new OpenAI({
  apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY || process.env.OPENAI_API_KEY,
})

export interface ChatCompletionOptions {
  model?: string
  temperature?: number
  max_tokens?: number
  stream?: boolean
}

export async function createChatCompletion(
  messages: ChatMessage[],
  options: ChatCompletionOptions = {}
) {
  const response = await openai.chat.completions.create({
    model: options.model || 'gpt-4o',
    messages: messages.map(m => ({
      role: m.role,
      content: m.content,
    })),
    temperature: options.temperature ?? 0.7,
    max_tokens: options.max_tokens ?? 1024,
    stream: options.stream ?? false,
    tools: getToolDefinitions(),
  })

  return response
}

// Tool definitions for the AI
export function getToolDefinitions() {
  return [
    {
      type: 'function',
      function: {
        name: 'get_tasks',
        description: 'Get all tasks for the current user',
        parameters: {
          type: 'object',
          properties: {},
        },
      },
    },
    {
      type: 'function',
      function: {
        name: 'create_task',
        description: 'Create a new task',
        parameters: {
          type: 'object',
          properties: {
            title: { type: 'string', description: 'Task title' },
            description: { type: 'string', description: 'Optional description' },
            due_date: { type: 'string', description: 'Optional due date' },
          },
          required: ['title'],
        },
      },
    },
    {
      type: 'function',
      function: {
        name: 'update_task',
        description: 'Update an existing task',
        parameters: {
          type: 'object',
          properties: {
            task_id: { type: 'number', description: 'Task ID' },
            title: { type: 'string', description: 'New title' },
            completed: { type: 'boolean', description: 'Completion status' },
          },
          required: ['task_id'],
        },
      },
    },
    {
      type: 'function',
      function: {
        name: 'delete_task',
        description: 'Delete a task',
        parameters: {
          type: 'object',
          properties: {
            task_id: { type: 'number', description: 'Task ID to delete' },
          },
          required: ['task_id'],
        },
      },
    },
  ]
}
```

### Chat Hook

```tsx
// src/hooks/useChat.ts
'use client'

import { useCallback, useState } from 'react'
import { ChatMessage, UseChatReturn } from '@/types/chat'
import { createChatCompletion } from '@/lib/openai'
import { v4 as uuidv4 } from 'uuid'

const SYSTEM_PROMPT = `You are a helpful AI assistant for task management.
You can help users create, update, and manage their tasks through natural language.
Always be helpful, friendly, and concise in your responses.`

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'system',
      role: 'system',
      content: SYSTEM_PROMPT,
      timestamp: new Date(),
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const sendMessage = useCallback(async (content: string) => {
    const userMessage: ChatMessage = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setError(null)

    try {
      const response = await createChatCompletion(
        [...messages, userMessage],
        { stream: false }
      )

      const assistantMessage: ChatMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: response.choices[0]?.message?.content || 'No response',
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setIsLoading(false)
    }
  }, [messages])

  const clearMessages = useCallback(() => {
    setMessages([
      {
        id: 'system',
        role: 'system',
        content: SYSTEM_PROMPT,
        timestamp: new Date(),
      },
    ])
  }, [])

  const retry = useCallback(async () => {
    const lastUserMessage = [...messages].reverse().find(m => m.role === 'user')
    if (lastUserMessage) {
      await sendMessage(lastUserMessage.content)
    }
  }, [messages, sendMessage])

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
    retry,
  }
}
```

### Chat Window Component

```tsx
// src/components/chat/ChatWindow.tsx
'use client'

import { useRef, useEffect } from 'react'
import { useChat } from '@/hooks/useChat'
import { ChatMessage } from './ChatMessage'
import { ChatInput } from './ChatInput'

export function ChatWindow() {
  const { messages, isLoading, error, sendMessage } = useChat()
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (content: string) => {
    await sendMessage(content)
  }

  const assistantMessages = messages.filter(m => m.role === 'assistant')
  const userMessages = messages.filter(m => m.role === 'user')

  return (
    <div className="flex flex-col h-[600px] max-w-2xl mx-auto border rounded-xl overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4">
        <h2 className="text-lg font-semibold">AI Assistant</h2>
        <p className="text-sm opacity-80">Ask me to help with your tasks</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages
          .filter(m => m.role !== 'system')
          .map((message, index) => (
            <ChatMessage
              key={message.id}
              message={message}
              isLatest={index === messages.length - 2}
            />
          ))}

        {isLoading && (
          <div className="flex items-center gap-2 text-gray-500">
            <div className="flex gap-1">
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
            </div>
            <span className="text-sm">AI is thinking...</span>
          </div>
        )}

        {error && (
          <div className="p-3 bg-red-50 text-red-700 rounded-lg">
            Error: {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} isLoading={isLoading} />
    </div>
  )
}
```

### Chat Message Component

```tsx
// src/components/chat/ChatMessage.tsx
import { ChatMessage as ChatMessageType } from '@/types/chat'

interface ChatMessageProps {
  message: ChatMessageType
  isLatest?: boolean
}

export function ChatMessage({ message, isLatest }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`max-w-[80%] ${isUser ? 'order-2' : 'order-1'}`}>
        {/* Avatar */}
        <div className={`flex items-center gap-2 mb-1 ${isUser ? 'flex-row-reverse' : ''}`}>
          <div className={`
            w-8 h-8 rounded-full flex items-center justify-center text-white text-sm
            ${isUser ? 'bg-blue-500' : 'bg-gradient-to-br from-purple-500 to-pink-500'}
          `}>
            {isUser ? 'U' : 'AI'}
          </div>
          <span className="text-xs text-gray-500">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>

        {/* Message bubble */}
        <div className={`
          rounded-2xl px-4 py-3
          ${isUser
            ? 'bg-blue-500 text-white rounded-tr-sm'
            : 'bg-white border shadow-sm rounded-tl-sm'
          }
        `}>
          <p className="whitespace-pre-wrap leading-relaxed">
            {message.content}
          </p>
        </div>

        {/* Tool calls indicator */}
        {message.tools && message.tools.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {message.tools.map(tool => (
              <span
                key={tool.id}
                className="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs"
              >
                <span className="w-2 h-2 bg-purple-500 rounded-full" />
                {tool.name}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
```

### Chat Input Component

```tsx
// src/components/chat/ChatInput.tsx
'use client'

import { useState, useRef, useEffect } from 'react'

interface ChatInputProps {
  onSend: (content: string) => Promise<void>
  isLoading: boolean
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const content = input.trim()
    setInput('')
    await onSend(content)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`
    }
  }, [input])

  return (
    <form onSubmit={handleSubmit} className="p-4 bg-white border-t">
      <div className="flex items-end gap-2">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me to help with your tasks..."
          className="flex-1 resize-none border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent max-h-32"
          rows={1}
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={!input.trim() || isLoading}
          className={`
            px-4 py-2 rounded-lg font-medium transition-colors
            ${input.trim() && !isLoading
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }
          `}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
      <p className="text-xs text-gray-500 mt-2">
        Press Enter to send, Shift+Enter for new line
      </p>
    </form>
  )
}
```

## Streaming Response Example

```tsx
// Streaming chat implementation
export async function* streamChat(messages: ChatMessage[]) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: messages.map(m => ({ role: m.role, content: m.content })),
    stream: true,
  })

  for await (const chunk of response) {
    const content = chunk.choices[0]?.delta?.content
    if (content) {
      yield content
    }
  }
}

// Usage in component
async function handleStreamingSend(content: string) {
  const encoder = new TextEncoder()
  const stream = await streamChat([...messages, userMessage])

  // Display streaming content
  for await (const chunk of stream) {
    setAssistantContent(prev => prev + chunk)
  }
}
```
