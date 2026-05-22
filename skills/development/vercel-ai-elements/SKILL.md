---
name: vercel-ai-elements
description: This skill provides comprehensive documentation for all 23 Vercel AI Elements components organized by category (Message, Conversation, Input/Interaction, Content Display, AI Processing, Advanced Features). Use when users ask about building AI chatbots, need component documentation, want API references for Vercel AI Elements, or need integration examples with the AI SDK.
---

# Vercel AI Elements Skill

## Overview

This skill provides complete documentation for Vercel AI Elements - a comprehensive UI component library for building conversational AI interfaces with the Vercel AI SDK. It covers 23 production-ready React components organized into 6 functional categories, from basic message display to advanced features like web previews and tool execution.

Use this skill when users need:
- Documentation on specific AI Elements components
- Installation and usage instructions
- Props and API references
- Integration examples with AI SDK
- Help choosing the right component for their use case
- Guidance on combining components for common patterns

## Core Capabilities

The Vercel AI Elements library provides components across 6 functional categories:

### 1. Message Components
Display chat messages with variants (contained/flat), automatic alignment, avatars, and markdown support. Perfect for rendering user and assistant messages in conversational interfaces.

**Components:** Message, MessageContent, MessageAvatar

**Reference:** `references/vercel-ai-elements-message-components.md`

### 2. Conversation Management
Wrap and manage message lists with automatic scrolling, scroll-to-bottom buttons, and empty states. Handles the container and layout for multi-message conversations.

**Components:** Conversation, ConversationContent, ConversationEmptyState, ConversationScrollButton

**Reference:** `references/vercel-ai-elements-conversation-management.md`

### 3. Input & Interaction
Enable user input with file attachments, model selection, suggestions, and task lists. Covers all user interaction patterns for sending messages and managing workflows.

**Components:** Actions, Prompt Input (with subcomponents), Suggestion, Task

**Reference:** `references/vercel-ai-elements-input-interaction.md`

### 4. Content Display
Render generated content including code, images, markdown responses, and structured artifacts. Handles all types of content output from AI models.

**Components:** Artifact, CodeBlock, Image, Response

**Reference:** `references/vercel-ai-elements-content-display.md`

### 5. AI Processing UI
Visualize AI processing steps including branching conversations, reasoning chains, loading states, execution plans, and shimmer effects. Shows the "thinking" process.

**Components:** Branch, Chain of Thought, Loader, Plan, Reasoning, Shimmer

**Reference:** `references/vercel-ai-elements-ai-processing.md`

### 6. Advanced Features
Specialized components for context tracking, citations, tool execution, source attribution, web previews, and cross-platform sharing.

**Components:** Context, Inline Citation, Open In Chat, Queue, Sources, Tool, Web Preview

**Reference:** `references/vercel-ai-elements-advanced-features.md`

## How to Use This Skill

### Finding Component Documentation

When a user asks about a specific component:

1. **Identify the component name** - e.g., "How do I use the Message component?"
2. **Locate the category** - determine which of the 6 categories the component belongs to
3. **Reference the appropriate file** - load the category reference file from `references/`
4. **Provide component details** - installation, basic usage, features, and props

### Common Usage Patterns

#### Pattern 1: Simple Chat Interface
Combine Message + Conversation + PromptInput + Response to build a basic chatbot UI.

#### Pattern 2: Enhanced Chat with Actions
Add Actions component to Message components for retry, copy, and regenerate functionality.

#### Pattern 3: AI Process Visualization
Use Reasoning, ChainOfThought, or Plan to show AI's thinking process during streaming.

#### Pattern 4: Advanced Document Generation
Combine Artifact, CodeBlock, Image, and Response for generating complex multi-media content.

#### Pattern 5: Multi-Platform Chat Share
Add OpenInChat to allow users to copy conversations to ChatGPT, Claude, etc.

### Integration with AI SDK

All components are designed to work with `@ai-sdk/react` hooks like:
- `useChat()` - for message management
- `useCompletion()` - for streaming text
- `experimental_useObject()` - for structured outputs

Reference files include complete AI SDK integration examples for each component category.

## Component Quick Reference

### Installation Pattern

All components use the same installation pattern:
```
npx ai-elements@latest add [component-name]
```

Where component names are lowercase with hyphens, e.g., `prompt-input`, `code-block`, `chain-of-thought`.

### Props Documentation

Each component reference file includes comprehensive props tables with:
- Prop name and type
- Description of functionality
- Whether prop is optional
- Default values where applicable

### Streaming Support

Many components have built-in streaming support:
- **Response**: parseIncompleteMarkdown handles streaming markdown
- **Plan**: isStreaming prop enables shimmer animations
- **Reasoning**: isStreaming auto-opens/closes the panel
- **Shimmer**: animation shows loading state

## Key Features Across Components

### TypeScript Support
All components have full type definitions for TypeScript projects.

### Accessibility
Components include proper ARIA labels, keyboard navigation, and semantic HTML.

### Responsive Design
All components adapt to different screen sizes with mobile-friendly interactions.

### Theme Integration
Components use CSS custom properties and currentColor for automatic theme support.

### Compound Components
Most components use compound component patterns (parent + child components) for flexible composition.

## Search Strategies

Use the reference files to search for:
- **By component name**: Search files for exact component name (e.g., "Message")
- **By feature**: Search for capability (e.g., "streaming", "copy button", "citations")
- **By use case**: Search for patterns (e.g., "loading", "error", "completed")
- **By props**: Search for specific prop names when users ask about customization

## Important Notes

### CSS Configuration
The Response component requires this CSS addition:
```css
@source "../node_modules/streamdown/dist/index.js";
```

### AI SDK Setup
Most components assume use of the AI SDK with proper backend routes. Reference files include backend example code.

### Component Dependencies
Many components depend on shadcn/ui primitives and icons from lucide-react. Users need these dependencies installed.

### Branching Implementation
The Branch component manages UI for multiple message branches but doesn't implement branching in the AI SDK - that requires custom backend logic.

## Resource Organization

### Reference Files (organized by category)
- `vercel-ai-elements-message-components.md` - Message display
- `vercel-ai-elements-conversation-management.md` - Conversation containers
- `vercel-ai-elements-input-interaction.md` - User input and actions
- `vercel-ai-elements-content-display.md` - Content rendering
- `vercel-ai-elements-ai-processing.md` - Processing UI and visualization
- `vercel-ai-elements-advanced-features.md` - Specialized components

Each reference file contains:
- Component descriptions and installation instructions
- Basic usage examples
- Complete props references
- Key features and capabilities
- Integration patterns with AI SDK

All reference files are organized by category for quick lookup when users ask about specific components or features.
