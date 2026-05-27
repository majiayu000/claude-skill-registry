---
name: collaboration-hub
description: Develop and modify the AILANG Collaboration Hub UI. Use when user asks to add features to the monitoring dashboard, modify the approval queue, update the message center, or make changes to the React frontend.
---

# Collaboration Hub Developer

Build and modify the AILANG Collaboration Hub - a React-based UI for multi-agent coordination.

## Quick Start

**Starting the server:**
```bash
ailang serve                    # Start on default port 1957
ailang serve --port 8080        # Use custom port
```

**After making UI changes:**
```bash
cd ui && npm run build                              # Build React app
cp -r ui/dist/* internal/server/dist/               # Copy to server
ailang serve                                        # Restart server
```

## When to Use This Skill

Use this skill when the user asks to:
- Add features to the monitoring dashboard
- Modify the approval queue UI
- Update the message center or thread list
- Make changes to the React frontend
- Style or theme the Collaboration Hub
- Add new tabs or components

## Architecture Overview

**Backend (Go):**
- `internal/server/server.go` - HTTP server, REST API, WebSocket
- `internal/server/monitor.go` - Process monitoring endpoints
- `internal/server/telemetry.go` - Real-time telemetry WebSocket

**Frontend (React + TypeScript + Vite):**
```
ui/
├── src/
│   ├── App.tsx                 # Main app, tabs, agent selector
│   ├── main.tsx                # React entry point
│   ├── types/index.ts          # TypeScript interfaces
│   ├── styles/                 # CSS variables and themes
│   └── components/
│       ├── MessageCenter/      # Thread-based messaging
│       │   ├── MessageCenter.tsx    # Main container, WebSocket
│       │   ├── ThreadList.tsx       # Conversation list sidebar
│       │   └── ConversationView.tsx # Message display and input
│       ├── ApprovalQueue/      # Effect approval workflow
│       │   └── ApprovalQueue.tsx    # Pending + history
│       └── Monitor/            # Process monitoring
│           └── Monitor.tsx          # Live stats, telemetry
├── dist/                       # Built assets (after npm run build)
└── package.json
```

**Database:**
- SQLite at `~/.ailang/state/collaboration.db`
- Tables: threads, messages, approvals

## Key Components

### App.tsx
- Tab navigation (Messages, Approvals, Monitor)
- Agent selector dropdown
- Approval state management with history
- WebSocket URL construction

### MessageCenter.tsx
- WebSocket connection management
- Thread CRUD operations
- Message sending with workspace support
- Unread counts tracking

### ConversationView.tsx
- Thread header with title and agent badge
- Message list with auto-scroll
- Markdown rendering for agent responses
- Message input with kind selector

### ThreadList.tsx
- Conversation list with status dots
- New thread creation form
- Unread badge display
- Timestamp formatting

### ApprovalQueue.tsx
- Pending approval cards with effect deltas
- Expand/collapse details
- Approve/reject with notes
- Review history section (collapsible)

### Monitor.tsx
- Process grid with live stats
- Telemetry overlay (tokens, cost)
- History section for completed processes
- Source badges (ui, eval, cli, agent)

## CSS Variables

The UI uses CSS custom properties defined in `ui/src/styles/`:

```css
/* Colors */
--color-primary: #25C2A0;
--color-success: #10B981;
--color-warning: #F59E0B;
--color-danger: #EF4444;

/* Backgrounds */
--bg-base: #0D1117;
--bg-surface: #161B22;
--bg-elevated: #21262D;
--bg-hover: #30363D;

/* Text */
--text-primary: #E6EDF3;
--text-secondary: #8B949E;
--text-tertiary: #6E7681;

/* Spacing */
--space-1 through --space-8

/* Typography */
--text-xs through --text-xl
--font-medium, --font-semibold, --font-bold
```

## REST API Endpoints

**Threads:**
- `GET /api/threads` - List all threads
- `POST /api/threads` - Create thread
- `GET /api/threads/:id/messages` - Get messages

**Messages:**
- `POST /api/messages` - Send message

**Approvals:**
- `GET /api/approvals?status=pending` - Pending approvals
- `GET /api/approvals?status=approved` - Approved history
- `GET /api/approvals?status=rejected` - Rejected history
- `POST /api/approvals/:id/approve` - Approve with notes
- `POST /api/approvals/:id/reject` - Reject with notes

**Monitor:**
- `GET /api/monitor` - Process stats + history

**WebSocket:**
- `ws://localhost:1957/ws` - Real-time events
  - `new_message` - New message in thread
  - `thread_state` - Thread status change
  - `telemetry` - Live process metrics

## TypeScript Interfaces

Key types in `ui/src/types/index.ts`:

```typescript
interface Thread {
  id: string;
  title: string;
  status: 'active' | 'paused' | 'resolved' | 'archived';
  target_agent?: string;
  last_seq: number;
  // ...
}

interface Message {
  id: string;
  thread_id: string;
  kind: 'directive' | 'status' | 'result' | 'approval_request';
  content: string;
  sender_type: 'human' | 'agent';
  // ...
}

interface Approval {
  id: string;
  status: 'pending' | 'approved' | 'rejected';
  proposal: string;
  impact: 'low' | 'medium' | 'high';
  estimated_cost: number;
  effect_delta_json: string;
  reviewed_by?: string;
  review_notes?: string;
  // ...
}
```

## Common Tasks

### Adding a New Tab

1. Add tab state in `App.tsx`:
   ```typescript
   const [activeTab, setActiveTab] = useState<'messages' | 'approvals' | 'monitor' | 'newtab'>
   ```

2. Add tab button in nav:
   ```tsx
   <button className={`tab ${activeTab === 'newtab' ? 'active' : ''}`}
           onClick={() => setActiveTab('newtab')}>
     New Tab
   </button>
   ```

3. Add component render:
   ```tsx
   {activeTab === 'newtab' && <NewComponent />}
   ```

### Adding a New API Endpoint

1. Add handler in `internal/server/server.go`
2. Register route in `setupRoutes()`
3. Add TypeScript interface if needed
4. Create fetch function in component

### Styling Components

Use CSS-in-JS pattern with `<style>` tags:
```tsx
<div className="my-component">
  {/* content */}
  <style>{`
    .my-component {
      background: var(--bg-surface);
      padding: var(--space-4);
      border-radius: var(--radius-md);
    }
  `}</style>
</div>
```

## Development Workflow

1. **Make changes** in `ui/src/`
2. **Build**: `cd ui && npm run build`
3. **Copy**: `cp -r ui/dist/* internal/server/dist/`
4. **Test**: `ailang serve` and open browser
5. **Iterate** as needed

For hot reload during development:
```bash
cd ui && npm run dev  # Runs Vite dev server on :5173
# But you'll need to proxy API calls - easier to just rebuild
```

## Troubleshooting

**Server won't start:**
- Check if port 1957 is in use: `lsof -i :1957`
- Use different port: `ailang serve --port 8080`

**UI changes not appearing:**
- Rebuild: `cd ui && npm run build`
- Copy to dist: `cp -r ui/dist/* internal/server/dist/`
- Hard refresh browser: Cmd+Shift+R

**WebSocket not connecting:**
- Check browser console for errors
- Verify server is running on correct port
- Check CORS if using different origins
