---
name: add-event-type
description: Add a new event type to the frontend feed system with corresponding React component. Use when user mentions "new event", "add event type", "event block", "new block type", or wants to display new agent output types.
---

# Add Event Type

## Instructions
1. Read current event types in `frontend/src/App.tsx`:
   - Find the `EventType` union type definition
   - Review existing block components (UserMessageBlock, PlanBlock, TodoBlock, etc.)

2. Define the new event type interface:
   ```typescript
   type NewEventType = {
     type: 'new_type';
     // Add required fields
   };
   ```

3. Add to EventType union:
   ```typescript
   type EventType = UserMessage | Plan | Todo | ... | NewEventType;
   ```

4. Create a new block component following existing patterns:
   ```typescript
   function NewTypeBlock({ event }: { event: NewEventType }) {
     return (
       <div className="p-3 bg-zinc-800/50 rounded-lg border border-zinc-700/50">
         {/* Render event data */}
       </div>
     );
   }
   ```

5. Add case to the feed rendering switch/conditional in the main component

6. Update WebSocket message handler if backend sends this event type

## Examples
- "Add a new 'search_result' event type"
- "Create a block for displaying errors"
- "Add event type for progress updates"

## Guardrails
- Follow existing naming conventions (PascalCase components, snake_case event types)
- Use existing Tailwind classes for consistent styling
- Ensure TypeScript types are complete (no `any`)
- Test by sending mock event through WebSocket
