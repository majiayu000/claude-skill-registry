---
name: ai-elements
description: Vercel AI Elements for workflow UI components. Use when building chat interfaces, displaying tool execution, showing reasoning/thinking, or creating job queues. Triggers on ai-elements, Queue, Confirmation, Tool, Reasoning, Shimmer, Loader, Message, Conversation, PromptInput.
---

# AI Elements

AI Elements is a comprehensive React component library for building AI-powered user interfaces. The library provides 30+ components specifically designed for chat interfaces, tool execution visualization, reasoning displays, and workflow management.

## Installation

Install via shadcn registry:

```bash
npx shadcn@latest add https://ai-elements.vercel.app/r/[component-name]
```

**Import Pattern**: Components are imported from individual files, not a barrel export:

```tsx
// Correct - import from specific files
import { Conversation } from "@/components/ai-elements/conversation";
import { Message } from "@/components/ai-elements/message";
import { PromptInput } from "@/components/ai-elements/prompt-input";

// Incorrect - no barrel export
import { Conversation, Message } from "@/components/ai-elements";
```

## Component Categories

### Conversation Components
Components for displaying chat-style interfaces with messages, attachments, and auto-scrolling behavior.

- **Conversation**: Container with auto-scroll capabilities
- **Message**: Individual message display with role-based styling
- **MessageAttachment**: File and image attachments
- **MessageBranch**: Alternative response navigation

See [references/conversation.md](references/conversation.md) for details.

### Prompt Input Components
Advanced text input with file attachments, drag-and-drop, speech input, and state management.

- **PromptInput**: Form container with file handling
- **PromptInputTextarea**: Auto-expanding textarea
- **PromptInputSubmit**: Status-aware submit button
- **PromptInputAttachments**: File attachment display
- **PromptInputProvider**: Global state management

See [references/prompt-input.md](references/prompt-input.md) for details.

### Workflow Components
Components for displaying job queues, tool execution, and approval workflows.

- **Queue**: Job queue container
- **QueueItem**: Individual queue items with status
- **Tool**: Tool execution display with collapsible states
- **Confirmation**: Approval workflow component
- **Reasoning**: Collapsible thinking/reasoning display

See [references/workflow.md](references/workflow.md) for details.

### Visualization Components
ReactFlow-based components for workflow visualization and custom node types.

- **Canvas**: ReactFlow wrapper with aviation-specific defaults
- **Node**: Custom node component with handles
- **Edge**: Temporary and Animated edge types
- **Controls, Panel, Toolbar**: Navigation and control elements

See [references/visualization.md](references/visualization.md) for details.

## Integration with shadcn/ui

AI Elements is built on top of shadcn/ui and integrates seamlessly with its theming system:

- Uses shadcn/ui's design tokens (colors, spacing, typography)
- Respects light/dark mode via CSS variables
- Compatible with shadcn/ui components (Button, Card, Collapsible, etc.)
- Follows shadcn/ui's component composition patterns

## Key Design Patterns

### Component Composition
AI Elements follows a composition-first approach where larger components are built from smaller primitives:

```tsx
<Tool>
  <ToolHeader title="search" type="tool-call-search" state="output-available" />
  <ToolContent>
    <ToolInput input={{ query: "AI tools" }} />
    <ToolOutput output={results} errorText={undefined} />
  </ToolContent>
</Tool>
```

### Context-Based State
Many components use React Context for state management:

- `PromptInputProvider` for global input state
- `MessageBranch` for alternative response navigation
- `Confirmation` for approval workflow state
- `Reasoning` for collapsible thinking state

### Controlled vs Uncontrolled
Components support both controlled and uncontrolled patterns:

```tsx
// Uncontrolled (self-managed state)
<PromptInput onSubmit={handleSubmit} />

// Controlled (external state)
<PromptInputProvider initialInput="">
  <PromptInput onSubmit={handleSubmit} />
</PromptInputProvider>
```

## Tool State Machine

The Tool component follows the Vercel AI SDK's state machine:

1. `input-streaming`: Parameters being received
2. `input-available`: Ready to execute
3. `approval-requested`: Awaiting user approval (SDK v6)
4. `approval-responded`: User responded (SDK v6)
5. `output-available`: Execution completed
6. `output-error`: Execution failed
7. `output-denied`: Approval denied

## Queue Patterns

Queue components support hierarchical organization:

```tsx
<Queue>
  <QueueSection defaultOpen={true}>
    <QueueSectionTrigger>
      <QueueSectionLabel count={3} label="tasks" icon={<Icon />} />
    </QueueSectionTrigger>
    <QueueSectionContent>
      <QueueList>
        <QueueItem>
          <QueueItemIndicator completed={false} />
          <QueueItemContent>Task description</QueueItemContent>
        </QueueItem>
      </QueueList>
    </QueueSectionContent>
  </QueueSection>
</Queue>
```

## Auto-Scroll Behavior

The Conversation component uses the `use-stick-to-bottom` hook for intelligent auto-scrolling:

- Automatically scrolls to bottom when new messages arrive
- Pauses auto-scroll when user scrolls up
- Provides scroll-to-bottom button when not at bottom
- Supports smooth and instant scroll modes

## File Attachment Handling

PromptInput provides comprehensive file handling:

- Drag-and-drop support (local or global)
- Paste image/file support
- File type validation (accept prop)
- File size limits (maxFileSize prop)
- Maximum file count (maxFiles prop)
- Preview for images, icons for files
- Automatic blob URL to data URL conversion on submit

## Speech Input

The PromptInputSpeechButton uses the Web Speech API for voice input:

- Browser-based speech recognition
- Continuous recognition mode
- Interim results support
- Automatic text insertion into textarea
- Visual feedback during recording

## Reasoning Auto-Collapse

The Reasoning component provides auto-collapse behavior:

- Opens automatically when streaming starts
- Closes 1 second after streaming ends
- Tracks thinking duration in seconds
- Displays "Thinking..." with shimmer effect during streaming
- Shows "Thought for N seconds" when complete

## TypeScript Types

All components are fully typed with TypeScript:

```typescript
import type { ToolUIPart, FileUIPart, UIMessage } from "ai";

type ToolProps = ComponentProps<typeof Collapsible>;
type QueueItemProps = ComponentProps<"li">;
type MessageAttachmentProps = HTMLAttributes<HTMLDivElement> & {
  data: FileUIPart;
  onRemove?: () => void;
};
```

## Common Use Cases

### Chat Interface
Combine Conversation, Message, and PromptInput for a complete chat UI:

```tsx
import { Conversation, ConversationContent, ConversationScrollButton } from "@/components/ai-elements/conversation";
import { Message, MessageContent, MessageResponse } from "@/components/ai-elements/message";
import {
  PromptInput,
  PromptInputTextarea,
  PromptInputFooter,
  PromptInputTools,
  PromptInputButton,
  PromptInputSubmit
} from "@/components/ai-elements/prompt-input";

<div className="flex flex-col h-screen">
  <Conversation>
    <ConversationContent>
      {messages.map(msg => (
        <Message key={msg.id} from={msg.role}>
          <MessageContent>
            <MessageResponse>{msg.content}</MessageResponse>
          </MessageContent>
        </Message>
      ))}
    </ConversationContent>
    <ConversationScrollButton />
  </Conversation>

  <PromptInput onSubmit={handleSubmit}>
    <PromptInputTextarea />
    <PromptInputFooter>
      <PromptInputTools>
        <PromptInputButton onClick={() => attachments.openFileDialog()}>
          <PaperclipIcon />
        </PromptInputButton>
      </PromptInputTools>
      <PromptInputSubmit status={chatStatus} />
    </PromptInputFooter>
  </PromptInput>
</div>
```

### Tool Execution Display
Show tool execution with expandable details:

```tsx
import { Tool, ToolHeader, ToolContent, ToolInput, ToolOutput } from "@/components/ai-elements/tool";

{toolInvocations.map(tool => (
  <Tool key={tool.id}>
    <ToolHeader
      title={tool.toolName}
      type={`tool-call-${tool.toolName}`}
      state={tool.state}
    />
    <ToolContent>
      <ToolInput input={tool.args} />
      {tool.result && (
        <ToolOutput output={tool.result} errorText={tool.error} />
      )}
    </ToolContent>
  </Tool>
))}
```

### Approval Workflow
Request user confirmation before executing actions:

```tsx
import {
  Confirmation,
  ConfirmationTitle,
  ConfirmationRequest,
  ConfirmationActions,
  ConfirmationAction,
  ConfirmationAccepted,
  ConfirmationRejected
} from "@/components/ai-elements/confirmation";

<Confirmation approval={tool.approval} state={tool.state}>
  <ConfirmationTitle>
    Approve deletion of {resource}?
  </ConfirmationTitle>

  <ConfirmationRequest>
    <ConfirmationActions>
      <ConfirmationAction onClick={approve} variant="default">
        Approve
      </ConfirmationAction>
      <ConfirmationAction onClick={reject} variant="outline">
        Reject
      </ConfirmationAction>
    </ConfirmationActions>
  </ConfirmationRequest>

  <ConfirmationAccepted>
    Action approved and executed.
  </ConfirmationAccepted>

  <ConfirmationRejected>
    Action rejected.
  </ConfirmationRejected>
</Confirmation>
```

### Job Queue Management
Display task lists with completion status:

```tsx
import {
  Queue,
  QueueSection,
  QueueSectionTrigger,
  QueueSectionLabel,
  QueueSectionContent,
  QueueList,
  QueueItem,
  QueueItemIndicator,
  QueueItemContent,
  QueueItemDescription
} from "@/components/ai-elements/queue";

<Queue>
  <QueueSection>
    <QueueSectionTrigger>
      <QueueSectionLabel count={todos.length} label="todos" />
    </QueueSectionTrigger>
    <QueueSectionContent>
      <QueueList>
        {todos.map(todo => (
          <QueueItem key={todo.id}>
            <QueueItemIndicator completed={todo.status === 'completed'} />
            <QueueItemContent completed={todo.status === 'completed'}>
              {todo.title}
            </QueueItemContent>
            {todo.description && (
              <QueueItemDescription completed={todo.status === 'completed'}>
                {todo.description}
              </QueueItemDescription>
            )}
          </QueueItem>
        ))}
      </QueueList>
    </QueueSectionContent>
  </QueueSection>
</Queue>
```

## Accessibility

Components include accessibility features:

- ARIA labels and roles
- Keyboard navigation support
- Screen reader announcements
- Focus management
- Semantic HTML elements

## Animation

Many components use Framer Motion for smooth animations:

- Shimmer effect for loading states
- Collapsible content transitions
- Edge animations in Canvas
- Loader spinner rotation

## References

- [Conversation Components](references/conversation.md)
- [Prompt Input Components](references/prompt-input.md)
- [Workflow Components](references/workflow.md)
- [Visualization Components](references/visualization.md)
