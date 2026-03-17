---
name: mini-apps
description: Create standalone React mini-apps via the Mini-Apps toolchain. Use when asked to build apps, forms, schedulers, dashboards, or shareable web components. Do not write app code directly to the repo.
---

# Mini-Apps Creation Skill

Create standalone React applications using the Mini-Apps architecture. Use this skill when asked to create apps, forms, schedulers, dashboards, or any shareable web component.

## Trigger Phrases

Use this skill when the user says:

- "Create an app to..."
- "Build a form for..."
- "Make a scheduling app like Calendly"
- "Create a poll/survey"
- "Build a dashboard to show..."
- "Generate an artifact"
- "Create a mini-app"

## CRITICAL: What NOT to Do

**NEVER** do the following when asked to create an app:

1. ❌ Write code directly to project files using `write` or `edit` tools
2. ❌ Use `bash` to create files or run npm commands
3. ❌ Modify `src/`, `apps/`, or any project source files directly
4. ❌ Create new TypeScript/React files manually

**ALWAYS** use the Mini-Apps tools instead:

1. ✅ Use `ai_first_create_app` to generate new apps
2. ✅ Use `ai_first_update_app` to modify existing apps
3. ✅ Apps are created via PR for review, not direct commits

## Available Tools

| Tool                  | Purpose                        |
| --------------------- | ------------------------------ |
| `ai_first_create_app` | Create a new app from a prompt |
| `ai_first_list_apps`  | List all available apps        |
| `ai_first_get_app`    | Get details of a specific app  |
| `ai_first_share_app`  | Generate a shareable link      |
| `ai_first_update_app` | Update an existing app         |

## Workflow

### Creating a New App

1. **Understand the request**: Ask clarifying questions if needed
2. **Craft a detailed prompt**: Include functionality, UI elements, integrations
3. **Call the tool**:

```
ai_first_create_app({
  prompt: "Create a meeting scheduler app that shows a calendar with available time slots. Users can select a date and time, enter their name and email, and confirm the booking. The app should integrate with Google Calendar to check availability.",
  name: "meeting-scheduler"  // optional
})
```

4. **Share results**: The tool returns:
   - `prUrl`: Link to the PR for review
   - `previewUrl`: Where the app will be hosted
   - `explanation`: What the AI generated

### Updating an Existing App

```
ai_first_update_app({
  name: "meeting-scheduler",
  updateRequest: "Add a dropdown to select meeting duration (15, 30, 45, or 60 minutes)"
})
```

## Writing Good Prompts

The quality of the generated app depends on the prompt. Include:

1. **Core functionality**: What should the app do?
2. **UI elements**: Calendar, forms, buttons, lists, etc.
3. **Integrations**: Calendar, Slack, email, etc.
4. **User flow**: Step-by-step what happens when user interacts

### Example Prompts

**Meeting Scheduler:**

```
Create a meeting scheduler app similar to Calendly. Features:
- Calendar view showing the next 2 weeks
- Time slots in 30-minute increments
- Form to collect: name, email, meeting topic
- Confirmation message after booking
- Integration with Google Calendar for availability
```

**Feedback Form:**

```
Build a feedback collection form with:
- 5-star rating for different categories (quality, speed, communication)
- Text area for detailed comments
- Optional name/email fields
- Submit button that sends results to Slack
- Thank you message after submission
```

**Team Poll:**

```
Create a poll app for team decisions:
- Question text at the top
- Multiple choice options (2-6)
- Show results as percentage bars after voting
- Allow changing vote before closing
- Results visible to all participants
```

## Architecture Notes

Mini-Apps are:

- Standalone React applications in the `apps/` directory
- Built with Vite and shared UI components
- Have their own `APP.yaml` manifest defining permissions
- Can access calendar, Slack, scheduler via a runtime bridge
- Shared via secret links with optional expiry

The `ai_first_create_app` tool:

1. Uses Claude to generate React code
2. Creates the app in a git worktree
3. Commits and pushes to a feature branch
4. Opens a PR for review
5. Returns the PR URL

This ensures:

- ✅ Code review before deployment
- ✅ No direct changes to production
- ✅ Proper git history
- ✅ Design system compliance

## Bridge Capabilities Reference

Mini-apps access backend services through the `useBridge()` hook. The bridge provides five capability domains:

### Import and Initialize

```typescript
import { useBridge } from '../../_shared/hooks';

function MyApp() {
  const { bridge, isReady, isPreviewMode } = useBridge();

  if (!isReady) return <div>Loading...</div>;

  // Use bridge.calendar, bridge.scheduler, etc.
}
```

### 1. Calendar Integration (Google Calendar)

**Permission required in APP.yaml:**

```yaml
permissions:
  calendar:
    read: true # For listEvents
    write: true # For createEvent, updateEvent, deleteEvent
```

**Available methods:**

| Method                                    | Description              | Parameters                                            |
| ----------------------------------------- | ------------------------ | ----------------------------------------------------- |
| `bridge.calendar.listEvents(start, end)`  | Get events in date range | `start: Date, end: Date`                              |
| `bridge.calendar.createEvent(params)`     | Create a calendar event  | See below                                             |
| `bridge.calendar.updateEvent(id, params)` | Update existing event    | `eventId: string, params: Partial<CreateEventParams>` |
| `bridge.calendar.deleteEvent(id)`         | Delete an event          | `eventId: string`                                     |

**CreateEventParams:**

```typescript
{
  summary: string;          // Event title
  description?: string;     // Event description
  start: Date;              // Start time
  duration: number;         // Duration in minutes
  attendees?: string[];     // Email addresses
  location?: string;        // Location or video link
  createMeetLink?: boolean; // Auto-create Google Meet
}
```

**Example - Create a meeting:**

```typescript
const event = await bridge.calendar.createEvent({
  summary: 'Team Standup',
  description: 'Daily sync meeting',
  start: new Date('2026-01-20T10:00:00'),
  duration: 30,
  attendees: ['alice@company.com', 'bob@company.com'],
  createMeetLink: true,
});
console.log('Created event:', event.id, 'Meet link:', event.meetLink);
```

**Example - Check availability:**

```typescript
const events = await bridge.calendar.listEvents(
  new Date(), // Start of range
  new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days ahead
);
const busyTimes = events.map((e) => ({ start: e.start, end: e.end }));
```

### 2. Scheduler (Built-in Capability)

Schedule messages to be sent via WhatsApp or Slack at specific times.

**Permission required in APP.yaml:**

```yaml
capabilities:
  scheduler:
    enabled: true
    max_jobs: 10 # Maximum concurrent scheduled jobs
```

**Available methods:**

| Method                               | Description             | Parameters      |
| ------------------------------------ | ----------------------- | --------------- |
| `bridge.scheduler.createJob(params)` | Schedule a message      | See below       |
| `bridge.scheduler.listJobs()`        | List all scheduled jobs | None            |
| `bridge.scheduler.cancelJob(id)`     | Cancel a scheduled job  | `jobId: number` |

**CreateJobParams:**

```typescript
{
  name: string;                              // Unique job name
  scheduleType: 'once' | 'recurring' | 'cron';
  runAt?: Date;                              // For 'once' type
  cronExpression?: string;                   // For 'cron' type (e.g., "0 9 * * 1-5")
  intervalMinutes?: number;                  // For 'recurring' type
  provider: 'whatsapp' | 'slack';
  target: string;                            // Channel/phone/email
  messageTemplate: string;                   // Message to send
}
```

**Example - One-time reminder:**

```typescript
await bridge.scheduler.createJob({
  name: `reminder-${eventId}`,
  scheduleType: 'once',
  runAt: new Date(meetingTime.getTime() - 15 * 60 * 1000), // 15 min before
  provider: 'slack',
  target: '#team-channel',
  messageTemplate: '📅 Reminder: Team meeting starts in 15 minutes!',
});
```

**Example - Daily standup reminder:**

```typescript
await bridge.scheduler.createJob({
  name: 'daily-standup-reminder',
  scheduleType: 'cron',
  cronExpression: '0 9 * * 1-5', // 9 AM, Mon-Fri
  provider: 'slack',
  target: '#engineering',
  messageTemplate: '🌅 Good morning! Time for standup.',
});
```

### 3. Webhooks (Built-in Capability)

Receive data from external services via webhook endpoints.

**Permission required in APP.yaml:**

```yaml
capabilities:
  webhooks:
    enabled: true
```

**Available methods:**

| Method                                              | Description              | Parameters                                       |
| --------------------------------------------------- | ------------------------ | ------------------------------------------------ |
| `bridge.webhooks.getEndpointUrl(name)`              | Get webhook URL to share | `endpointName: string`                           |
| `bridge.webhooks.onWebhookReceived(name, callback)` | Listen for incoming data | `endpointName: string, callback: (data) => void` |

**Example - Form submission webhook:**

```typescript
// Get the webhook URL to embed in external forms
const webhookUrl = await bridge.webhooks.getEndpointUrl('form-submit');
console.log('Share this URL:', webhookUrl);

// Listen for incoming submissions
useEffect(() => {
  const cleanup = bridge.webhooks.onWebhookReceived('form-submit', (data) => {
    console.log('Received submission:', data);
    setSubmissions((prev) => [...prev, data]);
  });
  return cleanup;
}, [bridge]);
```

### 4. Storage (Backend Persistence)

Persist data to the backend database. Unlike localStorage (browser-only), storage data persists across devices and sessions.

**Permission required in APP.yaml:**

```yaml
capabilities:
  storage:
    enabled: true
```

**Available methods:**

| Method                           | Description           | Parameters                    | Returns              |
| -------------------------------- | --------------------- | ----------------------------- | -------------------- |
| `bridge.storage.set(key, value)` | Store a value         | `key: string, value: unknown` | `Promise<void>`      |
| `bridge.storage.get(key)`        | Retrieve a value      | `key: string`                 | `Promise<T \| null>` |
| `bridge.storage.delete(key)`     | Delete a key          | `key: string`                 | `Promise<boolean>`   |
| `bridge.storage.list()`          | List all keys for app | None                          | `Promise<string[]>`  |
| `bridge.storage.clear()`         | Delete all app data   | None                          | `Promise<number>`    |

**Example - Persist todo list:**

```typescript
// Save todos
await bridge.storage.set('todos', [
  { id: '1', text: 'Buy milk', completed: false },
  { id: '2', text: 'Walk dog', completed: true },
]);

// Load todos
const todos = await bridge.storage.get<Todo[]>('todos');
if (todos) {
  setTodos(todos);
}

// Delete a specific key
await bridge.storage.delete('todos');

// List all keys
const keys = await bridge.storage.list();
console.log('Stored keys:', keys);

// Clear all app data
const deletedCount = await bridge.storage.clear();
```

**Example - User preferences:**

```typescript
interface UserPrefs {
  theme: 'light' | 'dark';
  notifications: boolean;
}

// Save preferences
await bridge.storage.set('prefs', { theme: 'dark', notifications: true });

// Load with type safety
const prefs = await bridge.storage.get<UserPrefs>('prefs');
if (prefs) {
  setTheme(prefs.theme);
}
```

**localStorage vs bridge.storage:**

| Feature             | localStorage | bridge.storage        |
| ------------------- | ------------ | --------------------- |
| Persistence         | Browser only | Backend database      |
| Cross-device        | No           | Yes                   |
| Storage limit       | ~5MB         | Unlimited (practical) |
| Data format         | String only  | Any JSON-serializable |
| Survives clear data | No           | Yes                   |
| Requires capability | No           | Yes (in APP.yaml)     |

**When to use each:**

- **localStorage**: Quick, temporary data; draft content; UI state
- **bridge.storage**: User data that must persist; shared state; production data

### 5. Slack Messaging

Send messages to Slack channels or users.

**Permission required in APP.yaml:**

```yaml
permissions:
  slack:
    read: false # Not yet implemented
    write: true # For sendDM, sendChannel
```

**Available methods:**

| Method                             | Description         | Parameters                            |
| ---------------------------------- | ------------------- | ------------------------------------- |
| `bridge.slack.sendDM(params)`      | Send direct message | `{ target: string, message: string }` |
| `bridge.slack.sendChannel(params)` | Post to channel     | `{ target: string, message: string }` |

**Example - Send notification:**

```typescript
await bridge.slack.sendChannel({
  target: '#notifications',
  message: `New booking: ${userName} scheduled a meeting for ${formatDate(dateTime)}`,
});
```

**Example - Send confirmation DM:**

```typescript
await bridge.slack.sendDM({
  target: userEmail, // Slack will resolve to user
  message: `Your meeting "${title}" has been confirmed for ${formatDate(dateTime)}.`,
});
```

### 6. App Metadata

Access app configuration and sharing info.

**Available methods (no permissions needed):**

| Method                     | Description                     |
| -------------------------- | ------------------------------- |
| `bridge.app.getManifest()` | Get APP.yaml as object          |
| `bridge.app.getShareUrl()` | Get shareable link for this app |

**Example:**

```typescript
const shareUrl = await bridge.app.getShareUrl();
navigator.clipboard.writeText(shareUrl);
alert('Link copied!');
```

## APP.yaml Permission Reference

Every mini-app must declare its permissions in `APP.yaml`:

```yaml
name: my-app
version: 1.0.0
title: My App Title
description: What the app does

# External service permissions
permissions:
  calendar:
    read: true # Can view events
    write: true # Can create/modify events
  slack:
    read: false
    write: true # Can send messages

# Built-in capabilities
capabilities:
  scheduler:
    enabled: true
    max_jobs: 5
  webhooks:
    enabled: true
  storage:
    enabled: true

# Sharing configuration
sharing:
  mode: secret_link # or 'public' or 'private'
  expires_after_days: 30

# Build configuration
build:
  entry: src/App.tsx
  output: dist/
```

**Permission Rules:**

- Bridge calls will fail if the required permission is not declared
- Request only the permissions the app actually needs
- `read` vs `write` are checked separately

## Crafting Prompts with Integrations

When generating apps, include specific integration requirements in the prompt:

**Good prompt with integrations:**

```
Create a meeting scheduler app with these features:
- Form to collect: title, attendees (comma-separated emails), date/time, duration
- Use bridge.calendar.createEvent to book the meeting with createMeetLink: true
- Use bridge.scheduler.createJob to schedule a Slack reminder 15 minutes before
- Show success message with the Google Meet link
- Permissions needed: calendar (read+write), scheduler enabled
```

**The generated APP.yaml should include:**

```yaml
permissions:
  calendar:
    read: true
    write: true
capabilities:
  scheduler:
    enabled: true
    max_jobs: 5
```

## Post-Creation Verification

After creating or updating an app, **always verify it compiles**:

### Step 1: Build the App

```bash
cd apps/<app-name> && npm install && npm run build
```

### Step 2: Check for TypeScript Errors

If the build fails, common issues include:

1. **React types not found** (`Cannot find module 'react'`):
   - Ensure `@types/react` and `@types/react-dom` are in `devDependencies`
   - Check that `tsconfig.json` includes proper `typeRoots`

2. **Shared component type errors** (missing `className`, `children`):
   - Props interfaces should extend `React.HTMLAttributes<HTMLElement>`
   - Example: `interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>`

3. **Index signature errors**:
   - Add `[key: string]: unknown;` to interface if needed for dynamic props

### Step 3: Verify the App Loads

After a successful build:

1. Run `curl -s -X POST http://localhost/api/apps/reload` to refresh the cache
2. Check status: `curl http://localhost/api/apps/<app-name>` should show `"status": "published"`, `"isBuilt": true`
3. Preview at: `http://localhost/apps/<app-name>/`

### tsconfig.json Template for Apps

If an app has compilation issues with shared components, ensure the tsconfig includes:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "baseUrl": ".",
    "paths": {
      "@shared/*": ["../_shared/*"]
    },
    "typeRoots": ["./node_modules/@types"]
  },
  "include": ["src", "../_shared"]
}
```

## Dashboard Integration

Apps are viewable in the Dashboard:

1. Navigate to **Mini-Apps** in the sidebar
2. See all apps with their build status (Published/Building)
3. Click **Preview** to test a built app
4. Click **Copy Link** to share the preview URL

## Serving Mini-Apps (Static Files)

Mini-apps are served as static files from the dashboard server at `/apps/:appName/`. This section covers the architecture and configuration required.

### Dashboard Server Architecture

The dashboard server (`packages/dashboard/src/server/index.ts`) serves mini-apps via Express static file serving:

```typescript
// In createDashboardServer()
if (services.appsService) {
  app.use('/apps/:appName', (req, res, next) => {
    const app = appsService.getApp(req.params.appName);
    if (!app || !app.isBuilt) {
      return res.status(404).json({ error: 'App not found or not built' });
    }

    // Serve static files from app's dist directory
    express.static(app.distPath)(req, res, () => {
      // Fallback to index.html for SPA routing
      const indexPath = path.join(app.distPath, 'index.html');
      if (fs.existsSync(indexPath)) {
        res.sendFile(indexPath);
      } else {
        next();
      }
    });
  });
}
```

Nginx routes `/apps/` to the dashboard server:

```nginx
location /apps/ {
    proxy_pass http://dashboard_api_local/apps/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
}
```

### Vite Base Path Configuration

**CRITICAL**: Mini-apps must use relative asset paths to work correctly when served at `/apps/:appName/`.

Every mini-app's `vite.config.ts` must include:

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  base: './', // REQUIRED: Use relative paths for assets
  resolve: {
    alias: {
      '@shared': path.resolve(__dirname, '../_shared'),
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
});
```

**Why `base: './'` is required:**

Without this setting, Vite generates absolute paths like `/assets/index.js`. When the app is served at `/apps/my-app/`, the browser tries to load `/assets/index.js` from the root, which fails.

With `base: './'`, paths become `./assets/index.js`, which resolves correctly relative to the app's URL.

### Troubleshooting Asset Loading Issues

| Symptom                    | Cause                                                    | Solution                                                         |
| -------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------- |
| JS/CSS returns HTML        | Absolute paths (`/assets/...`) routed to Vite dev server | Add `base: './'` to vite.config.ts and rebuild                   |
| 404 on assets              | Missing base path config                                 | Ensure `base: './'` in vite.config.ts                            |
| App loads but shows blank  | JS execution error                                       | Check browser console; rebuild with correct base                 |
| Preview button returns 404 | App not built or routes not configured                   | Run `npm run build`, ensure dashboard has `/apps/:appName` route |

### Verifying App Serving

After building an app, verify it's accessible:

```bash
# Check HTML is served
curl http://localhost:3080/apps/my-app/

# Check assets use relative paths (should see ./assets/...)
curl http://localhost:3080/apps/my-app/ | grep -o 'src="[^"]*"'

# Check assets are served correctly (should return JS, not HTML)
curl http://localhost:3080/apps/my-app/assets/index-xxxxx.js | head -c 100
```

## Troubleshooting

| Issue                                      | Solution                                        |
| ------------------------------------------ | ----------------------------------------------- |
| App shows "Building" status                | Run `npm run build` in the app directory        |
| Preview returns 404                        | Ensure the app has a `dist/` folder after build |
| API shows 503 "Apps service not available" | Restart the dev server                          |
| Shared components not found                | Check `tsconfig.json` paths and includes        |
| Assets return HTML instead of JS/CSS       | Add `base: './'` to vite.config.ts and rebuild  |

## Database Schema Design Patterns

When adding persistent storage capabilities to mini-apps, follow these patterns for SQLite database services.

### Database Initialization

Use better-sqlite3 for synchronous SQLite operations:

```typescript
import Database from 'better-sqlite3';
import { createServiceLogger } from '@orientbot/core';

const logger = createServiceLogger('storage-db');

export class MyDatabase {
  private db: Database.Database;

  constructor(dbPath?: string) {
    const path = dbPath || process.env.SQLITE_DB_PATH || './data/orient.db';
    this.db = new Database(path);
    this.db.pragma('journal_mode = WAL'); // Better concurrent access
    this.db.pragma('foreign_keys = ON');
  }

  // Always close when shutting down
  close(): void {
    this.db.close();
  }
}
```

**Key points:**

- Use WAL mode for better concurrent read performance
- Enable foreign keys if using relationships
- SQLite operations are synchronous, simplifying code
- Always implement `close()` for graceful shutdown

### Table Schema Design

Follow these conventions for mini-app database tables:

```sql
CREATE TABLE IF NOT EXISTS app_feature (
  -- Primary key
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  -- App identification (always required for multi-tenant isolation)
  app_name TEXT NOT NULL,

  -- Your feature-specific columns
  key TEXT NOT NULL,
  value TEXT NOT NULL,           -- Store JSON as TEXT

  -- Timestamps (always include these)
  created_at INTEGER DEFAULT (unixepoch()),
  updated_at INTEGER DEFAULT (unixepoch()),

  -- Unique constraints for app-scoped uniqueness
  UNIQUE(app_name, key)
);
```

**Best practices:**

- Always include `app_name` for multi-tenant isolation
- Use `INTEGER PRIMARY KEY AUTOINCREMENT` for auto-incrementing IDs
- Store timestamps as Unix epoch integers
- Store JSON as TEXT (SQLite has no native JSON type but supports json functions)
- Add `UNIQUE` constraints for natural keys within an app scope

### Index Design

Create indexes for common query patterns:

```sql
-- Composite index for app-scoped lookups (most common pattern)
CREATE INDEX IF NOT EXISTS idx_app_feature_app_key
  ON app_feature(app_name, key);

-- Single column index if you query by app_name alone
CREATE INDEX IF NOT EXISTS idx_app_feature_app_name
  ON app_feature(app_name);

-- Partial index for enabled/active records
CREATE INDEX IF NOT EXISTS idx_app_feature_active
  ON app_feature(app_name) WHERE enabled = 1;
```

**Index guidelines:**

- Create indexes for columns used in `WHERE` clauses
- Composite indexes should match query column order
- Use partial indexes for frequently filtered conditions

### Transaction Handling

Use transactions for multi-statement operations:

```typescript
initialize(): void {
  const createTables = this.db.transaction(() => {
    this.db.exec(`CREATE TABLE IF NOT EXISTS ...`);
    this.db.exec(`CREATE INDEX IF NOT EXISTS ...`);
  });

  try {
    createTables();
    logger.info('Database initialized successfully');
  } catch (error) {
    logger.error('Database initialization failed', { error });
    throw error;
  }
}
```

**Transaction rules:**

- Use `db.transaction()` for atomic operations
- Transactions in better-sqlite3 are automatic COMMIT on success, ROLLBACK on error
- Log both success and failure for debugging

### Query Patterns

**Simple queries:**

```typescript
get(appName: string, key: string): unknown | null {
  const stmt = this.db.prepare(
    'SELECT value FROM app_storage WHERE app_name = ? AND key = ?'
  );
  const row = stmt.get(appName, key) as { value: string } | undefined;
  return row ? JSON.parse(row.value) : null;
}
```

**Upsert pattern (INSERT OR REPLACE):**

```typescript
set(appName: string, key: string, value: unknown): void {
  const stmt = this.db.prepare(`
    INSERT INTO app_storage (app_name, key, value, updated_at)
    VALUES (?, ?, ?, unixepoch())
    ON CONFLICT (app_name, key)
    DO UPDATE SET value = excluded.value, updated_at = unixepoch()
  `);
  stmt.run(appName, key, JSON.stringify(value));
}
```

**Returning results after modification:**

```typescript
create(data: CreateInput): Record {
  const stmt = this.db.prepare(`
    INSERT INTO my_table (name, value)
    VALUES (?, ?)
    RETURNING *
  `);
  const row = stmt.get(data.name, data.value);
  return this.rowToRecord(row);
}
```

### Row Mapping

Convert database rows to TypeScript types:

```typescript
interface StorageEntry {
  appName: string;
  key: string;
  value: unknown;
  createdAt: Date;
  updatedAt: Date;
}

private rowToEntry(row: Record<string, unknown>): StorageEntry {
  return {
    appName: row.app_name as string,      // snake_case to camelCase
    key: row.key as string,
    value: JSON.parse(row.value as string),  // Parse JSON manually
    createdAt: new Date((row.created_at as number) * 1000),
    updatedAt: new Date((row.updated_at as number) * 1000),
  };
}
```

### Initialization Pattern

Use an `initialized` flag to prevent duplicate setup:

```typescript
export class MyDatabase {
  private initialized: boolean = false;

  initialize(): void {
    if (this.initialized) return; // Idempotent - safe to call multiple times

    // ... create tables and indexes ...

    this.initialized = true;
  }
}
```

### Complete Example: StorageDatabase

Here's the full pattern used by the storage capability:

```typescript
import Database from 'better-sqlite3';
import { createServiceLogger } from '@orientbot/core';

const logger = createServiceLogger('storage-db');

export class StorageDatabase {
  private db: Database.Database;
  private initialized: boolean = false;

  constructor(dbPath?: string) {
    const path = dbPath || process.env.SQLITE_DB_PATH || './data/orient.db';
    this.db = new Database(path);
    this.db.pragma('journal_mode = WAL');
  }

  initialize(): void {
    if (this.initialized) return;

    this.db.exec(`
      CREATE TABLE IF NOT EXISTS app_storage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_name TEXT NOT NULL,
        key TEXT NOT NULL,
        value TEXT NOT NULL,
        created_at INTEGER DEFAULT (unixepoch()),
        updated_at INTEGER DEFAULT (unixepoch()),
        UNIQUE(app_name, key)
      )
    `);

    this.db.exec(`
      CREATE INDEX IF NOT EXISTS idx_app_storage_app_key
        ON app_storage(app_name, key);
    `);

    this.initialized = true;
  }

  set(appName: string, key: string, value: unknown): void {
    const stmt = this.db.prepare(`
      INSERT INTO app_storage (app_name, key, value, updated_at)
      VALUES (?, ?, ?, unixepoch())
      ON CONFLICT (app_name, key)
      DO UPDATE SET value = excluded.value, updated_at = unixepoch()
    `);
    stmt.run(appName, key, JSON.stringify(value));
  }

  get(appName: string, key: string): unknown | null {
    const stmt = this.db.prepare('SELECT value FROM app_storage WHERE app_name = ? AND key = ?');
    const row = stmt.get(appName, key) as { value: string } | undefined;
    return row ? JSON.parse(row.value) : null;
  }

  delete(appName: string, key: string): boolean {
    const stmt = this.db.prepare('DELETE FROM app_storage WHERE app_name = ? AND key = ?');
    const result = stmt.run(appName, key);
    return result.changes > 0;
  }

  list(appName: string): string[] {
    const stmt = this.db.prepare('SELECT key FROM app_storage WHERE app_name = ? ORDER BY key');
    const rows = stmt.all(appName) as { key: string }[];
    return rows.map((row) => row.key);
  }

  clear(appName: string): number {
    const stmt = this.db.prepare('DELETE FROM app_storage WHERE app_name = ?');
    const result = stmt.run(appName);
    return result.changes;
  }

  close(): void {
    this.db.close();
  }
}
```

## Bridge API Endpoint Handler Patterns

The bridge API (`/api/apps/bridge`) handles method invocations from mini-apps. This section documents the request/response format and handler patterns.

### Request Format

All bridge calls use POST with JSON body:

```typescript
// Frontend call (from useBridge.ts)
const response = await fetch('/api/apps/bridge', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    appName: 'my-app', // Required: identifies the app
    method: 'storage.get', // Required: the method to invoke
    params: { key: 'todos' }, // Optional: method-specific parameters
  }),
});
```

### Response Format

**Success response:**

```json
{
  "data": {
    /* method-specific result */
  }
}
```

**Error responses:**

| Status | Error                                         | When                                |
| ------ | --------------------------------------------- | ----------------------------------- |
| 400    | `appName and method are required`             | Missing required fields             |
| 400    | `key is required`                             | Missing method-specific parameter   |
| 403    | `Storage capability not enabled for this app` | Capability not declared in APP.yaml |
| 404    | `App "name" not found`                        | App doesn't exist                   |
| 501    | `Method "x" not implemented`                  | Unknown method                      |
| 503    | `Storage service not available`               | Backend service not initialized     |
| 500    | `Bridge call failed`                          | Unexpected server error             |

### Handler Structure

The bridge endpoint uses a switch statement for method routing:

```typescript
router.post('/bridge', async (req: Request, res: Response) => {
  try {
    const { appName, method, params } = req.body;

    // 1. Validate required fields
    if (!appName || !method) {
      return res.status(400).json({ error: 'appName and method are required' });
    }

    // 2. Get the app (validates it exists)
    const app = appsService.getApp(appName);
    if (!app) {
      return res.status(404).json({ error: `App "${appName}" not found` });
    }

    logger.debug('Bridge call', { appName, method, params });

    // 3. Route to method handler
    switch (method) {
      case 'storage.set': {
        // Check service availability
        if (!bridgeServices?.storageDb) {
          return res.status(503).json({ error: 'Storage service not available' });
        }
        // Check capability
        const cap = app.manifest.capabilities?.storage;
        if (!cap?.enabled) {
          return res.status(403).json({ error: 'Storage capability not enabled' });
        }
        // Validate params
        const { key, value } = params || {};
        if (!key || typeof key !== 'string') {
          return res.status(400).json({ error: 'key is required' });
        }
        // Execute
        await bridgeServices.storageDb.set(appName, key, value);
        return res.json({ data: { success: true } });
      }

      // ... other methods

      default:
        logger.warn('Unknown bridge method', { appName, method });
        return res.status(501).json({ error: `Method "${method}" not implemented` });
    }
  } catch (error) {
    logger.error('Bridge call failed', {
      error: error instanceof Error ? error.message : String(error),
    });
    res.status(500).json({ error: 'Bridge call failed' });
  }
});
```

### Method Handler Pattern

Each method handler follows this pattern:

```typescript
case 'category.methodName': {
  // 1. Check service availability (503 if not available)
  if (!bridgeServices?.myService) {
    return res.status(503).json({ error: 'MyService not available' });
  }

  // 2. Check capability (403 if not enabled)
  const capability = app.manifest.capabilities?.myCapability;
  if (!capability?.enabled) {
    return res.status(403).json({ error: 'MyCapability not enabled for this app' });
  }

  // 3. Extract and validate parameters (400 if invalid)
  const { requiredParam, optionalParam } = params || {};
  if (!requiredParam || typeof requiredParam !== 'string') {
    return res.status(400).json({ error: 'requiredParam is required' });
  }

  // 4. Execute the operation
  const result = await bridgeServices.myService.doSomething(appName, requiredParam);

  // 5. Return success with data wrapper
  return res.json({ data: result });
}
```

### Capability Checking Pattern

Always check capability before processing:

```typescript
// For capabilities (scheduler, webhooks, storage)
const cap = app.manifest.capabilities?.storage;
if (!cap?.enabled) {
  return res.status(403).json({ error: 'Storage capability not enabled for this app' });
}

// For permissions (calendar, slack, jira)
const perm = app.manifest.permissions?.calendar;
if (!perm?.write) {
  return res.status(403).json({ error: 'Calendar write permission not granted' });
}
```

### Parameter Validation Patterns

```typescript
// Required string parameter
const { key } = params || {};
if (!key || typeof key !== 'string') {
  return res.status(400).json({ error: 'key is required' });
}

// Required number parameter
const { id } = params || {};
if (typeof id !== 'number') {
  return res.status(400).json({ error: 'id must be a number' });
}

// Optional parameter with default
const { limit = 100 } = params || {};

// Array parameter
const { items } = params || {};
if (!Array.isArray(items)) {
  return res.status(400).json({ error: 'items must be an array' });
}
```

### Return Value Patterns

```typescript
// Simple success
return res.json({ data: { success: true } });

// Return single value
return res.json({ data: value }); // value can be null

// Return object
return res.json({ data: { id: 1, name: 'test' } });

// Return array
return res.json({ data: ['key1', 'key2', 'key3'] });

// Return with count
return res.json({ data: { deleted: true } });
return res.json({ data: { cleared: 5 } });
```

### Frontend Bridge Call Pattern

The frontend `callBridge` function handles the request/response:

```typescript
async function callBridge<T>(method: string, params: Record<string, unknown>): Promise<T> {
  // Check permissions before making request
  checkPermissions(method, capabilities);

  const response = await fetch('/api/apps/bridge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ appName, method, params }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Bridge call failed');
  }

  const result = await response.json();
  return result.data as T;
}
```

### Adding a New Method

When adding a new bridge method:

1. **Choose a method name**: Use `category.action` format (e.g., `storage.set`, `calendar.listEvents`)

2. **Add the handler case** in the switch statement following the pattern above

3. **Update frontend bridge**:

   ```typescript
   // In useBridge.ts AppBridge interface
   myCategory: {
     myMethod: (params) => callBridge('myCategory.myMethod', params),
   },
   ```

4. **Add permission check** if needed:
   ```typescript
   // In checkPermissions function
   if (method.startsWith('myCategory.')) {
     if (!capabilities?.myCategory?.enabled) {
       throw new Error('Capability denied: myCategory not enabled in APP.yaml');
     }
   }
   ```

## Frontend Bridge Implementation Patterns

This section covers how to implement bridge methods in the frontend (`apps/_shared/hooks/useBridge.ts`).

### The callBridge Utility Function

The `callBridge` function is the core utility for making bridge API calls:

```typescript
/**
 * Make a bridge API call with type safety
 * @template T - The expected return type
 * @param method - The method name (e.g., 'storage.get')
 * @param params - Method-specific parameters
 * @returns Promise resolving to the typed result
 */
async function callBridge<T>(method: string, params: Record<string, unknown>): Promise<T> {
  // 1. Check permissions before making the network request
  checkPermissions(method, capabilities);

  // 2. Make the API call
  const response = await fetch('/api/apps/bridge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ appName, method, params }),
  });

  // 3. Handle errors
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Bridge call failed');
  }

  // 4. Return typed result
  const result = await response.json();
  return result.data as T;
}
```

### Type-Safe Bridge Method Implementations

Define typed methods in the `AppBridge` interface:

```typescript
export interface AppBridge {
  storage: {
    set(key: string, value: unknown): Promise<void>;
    get<T = unknown>(key: string): Promise<T | null>;
    delete(key: string): Promise<boolean>;
    list(): Promise<string[]>;
    clear(): Promise<number>;
  };
}
```

Implement methods with proper typing:

```typescript
const bridge: AppBridge = {
  storage: {
    // Simple void return
    set: async (key: string, value: unknown): Promise<void> => {
      await callBridge('storage.set', { key, value });
    },

    // Generic return type
    get: async <T = unknown>(key: string): Promise<T | null> => {
      return callBridge<T | null>('storage.get', { key });
    },

    // Extract nested result
    delete: async (key: string): Promise<boolean> => {
      const result = await callBridge<{ deleted: boolean }>('storage.delete', { key });
      return result.deleted;
    },

    // Direct array return
    list: (): Promise<string[]> => callBridge('storage.list', {}),

    // Extract count from result
    clear: async (): Promise<number> => {
      const result = await callBridge<{ cleared: number }>('storage.clear', {});
      return result.cleared;
    },
  },
};
```

### Permission Checking Pattern

Check capabilities before making API calls:

```typescript
interface Capabilities {
  scheduler?: { enabled?: boolean; max_jobs?: number };
  webhooks?: { enabled?: boolean };
  storage?: { enabled?: boolean };
}

function checkPermissions(method: string, capabilities: Capabilities | undefined): void {
  // Scheduler capability
  if (method.startsWith('scheduler.')) {
    if (!capabilities?.scheduler?.enabled) {
      throw new Error('Capability denied: scheduler not enabled in APP.yaml');
    }
  }

  // Webhooks capability
  if (method.startsWith('webhooks.')) {
    if (!capabilities?.webhooks?.enabled) {
      throw new Error('Capability denied: webhooks not enabled in APP.yaml');
    }
  }

  // Storage capability
  if (method.startsWith('storage.')) {
    if (!capabilities?.storage?.enabled) {
      throw new Error('Capability denied: storage not enabled in APP.yaml');
    }
  }
}
```

### Error Handling Patterns

Handle bridge errors in your app:

```typescript
// Pattern 1: Try-catch with user feedback
const loadData = async () => {
  try {
    const data = await bridge.storage.get<MyData>('key');
    setData(data);
  } catch (error) {
    console.error('Failed to load data:', error);
    setError('Could not load data. Please try again.');
  }
};

// Pattern 2: Silent failure with fallback
const loadWithFallback = async () => {
  try {
    const data = await bridge.storage.get<MyData>('key');
    return data ?? defaultData;
  } catch {
    return defaultData;
  }
};

// Pattern 3: Optimistic update with rollback
const saveData = async (newData: MyData) => {
  const oldData = data;
  setData(newData); // Optimistic update

  try {
    await bridge.storage.set('key', newData);
  } catch (error) {
    setData(oldData); // Rollback on failure
    console.error('Failed to save:', error);
  }
};
```

### Async/Await Best Practices

```typescript
// Good: Separate loading state from ready state
const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
  if (!isReady) return;

  const loadData = async () => {
    try {
      const stored = await bridge.storage.get<Data>('key');
      if (stored) setData(stored);
    } finally {
      setIsLoading(false);
    }
  };

  loadData();
}, [isReady, bridge]);

// Good: Save after state update
const updateData = async (newData: Data) => {
  setData(newData);
  await bridge.storage.set('key', newData);
};

// Good: Memoize save function to avoid dependency issues
const saveData = useCallback(
  async (data: Data) => {
    try {
      await bridge.storage.set('key', data);
    } catch (error) {
      console.error('Save failed:', error);
    }
  },
  [bridge]
);
```

### Adding a New Frontend Bridge Method

1. **Update the interface** in `AppBridge`:

   ```typescript
   export interface AppBridge {
     myCategory: {
       myMethod(param: string): Promise<Result>;
     };
   }
   ```

2. **Update the Capabilities interface**:

   ```typescript
   interface Capabilities {
     myCategory?: { enabled?: boolean };
   }
   ```

3. **Add permission check**:

   ```typescript
   if (method.startsWith('myCategory.')) {
     if (!capabilities?.myCategory?.enabled) {
       throw new Error('Capability denied: myCategory not enabled');
     }
   }
   ```

4. **Implement the method**:
   ```typescript
   myCategory: {
     myMethod: async (param: string): Promise<Result> => {
       return callBridge<Result>('myCategory.myMethod', { param });
     },
   },
   ```

### Testing Bridge Methods

Mock the bridge in tests:

```typescript
const mockBridge = {
  storage: {
    set: vi.fn().mockResolvedValue(undefined),
    get: vi.fn().mockResolvedValue(null),
    delete: vi.fn().mockResolvedValue(true),
    list: vi.fn().mockResolvedValue([]),
    clear: vi.fn().mockResolvedValue(0),
  },
};

// Test usage
it('should save data', async () => {
  await mockBridge.storage.set('key', { foo: 'bar' });
  expect(mockBridge.storage.set).toHaveBeenCalledWith('key', { foo: 'bar' });
});
```

## Implementing New Bridge Capabilities

This guide explains how to add a new capability to the mini-apps bridge (like storage, scheduler, webhooks). Follow these steps when implementing new backend services that mini-apps can access.

### Architecture Overview

Bridge capabilities flow through these layers:

```
Frontend (useBridge.ts) → Bridge API (/api/apps/bridge) → Database Service → SQLite
     ↓                           ↓                              ↓
 Permission check           Route handler               SQL operations
```

### Step 1: Define Types (packages/apps/src/types.ts)

Add a Zod schema and TypeScript type for the new capability:

```typescript
/**
 * MyFeature capability configuration
 */
export const MyFeatureCapabilitySchema = z.object({
  enabled: z.boolean().default(false),
  // Add any configuration options here
  max_items: z.number().int().positive().optional(),
});

export type MyFeatureCapability = z.infer<typeof MyFeatureCapabilitySchema>;
```

Add to `AppCapabilitiesSchema`:

```typescript
export const AppCapabilitiesSchema = z.object({
  scheduler: SchedulerCapabilitySchema.optional(),
  webhooks: WebhookCapabilitySchema.optional(),
  storage: StorageCapabilitySchema.optional(),
  myFeature: MyFeatureCapabilitySchema.optional(), // Add new capability
});
```

Update `generateAppManifestTemplate()` and `serializeManifestToYaml()` to include the new capability.

### Step 2: Create Database Service (packages/dashboard/src/services/)

Create a new file `myFeatureDatabase.ts`:

```typescript
import Database from 'better-sqlite3';
import { createServiceLogger } from '@orientbot/core';

const logger = createServiceLogger('myfeature-db');

export class MyFeatureDatabase {
  private db: Database.Database;
  private initialized: boolean = false;

  constructor(dbPath?: string) {
    const path = dbPath || process.env.SQLITE_DB_PATH || './data/orient.db';
    this.db = new Database(path);
    this.db.pragma('journal_mode = WAL');
  }

  initialize(): void {
    if (this.initialized) return;

    // Create your table
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS my_feature (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_name TEXT NOT NULL,
        -- your columns here
        created_at INTEGER DEFAULT (unixepoch()),
        updated_at INTEGER DEFAULT (unixepoch())
      )
    `);

    // Create indexes
    this.db.exec(`
      CREATE INDEX IF NOT EXISTS idx_my_feature_app ON my_feature(app_name);
    `);

    this.initialized = true;
    logger.info('MyFeature database tables initialized');
  }

  // Implement your CRUD methods
  create(appName: string, data: unknown): void { ... }
  get(appName: string, id: string): unknown { ... }
  list(appName: string): unknown[] { ... }
  delete(appName: string, id: string): boolean { ... }

  close(): void {
    this.db.close();
  }
}
```

### Step 3: Register Service (packages/dashboard/src/server/index.ts)

Import and add to `DashboardServices` interface:

```typescript
import { MyFeatureDatabase } from '../services/myFeatureDatabase.js';

export interface DashboardServices {
  // ... existing services
  myFeatureDb?: MyFeatureDatabase;
}
```

Initialize in `initializeServices()`:

```typescript
// Initialize myFeature database
const myFeatureDb = new MyFeatureDatabase(databaseUrl);
await myFeatureDb.initialize();
logger.info('MyFeature database initialized');
```

Add to the return object:

```typescript
return {
  // ... existing services
  myFeatureDb,
};
```

### Step 4: Add Bridge Handler (packages/dashboard/src/server/routes/apps.routes.ts)

Update the `BridgeServices` interface:

```typescript
interface BridgeServices {
  storageDb?: StorageDatabase;
  myFeatureDb?: MyFeatureDatabase;
}
```

Add method handlers in the bridge endpoint switch statement:

```typescript
case 'myFeature.create': {
  if (!bridgeServices?.myFeatureDb) {
    return res.status(503).json({ error: 'MyFeature service not available' });
  }
  // Check capability
  const cap = app.manifest.capabilities?.myFeature;
  if (!cap?.enabled) {
    return res.status(403).json({ error: 'MyFeature capability not enabled' });
  }
  // Validate and process
  const { data } = params || {};
  await bridgeServices.myFeatureDb.create(appName, data);
  return res.json({ data: { success: true } });
}
```

### Step 5: Update Route Registration (packages/dashboard/src/server/routes.ts)

Pass the new service to apps routes:

```typescript
if (appsService) {
  router.use(
    '/apps',
    createAppsRoutes(appsService, requireAuth, {
      storageDb,
      myFeatureDb, // Add new service
    })
  );
}
```

### Step 6: Add Frontend Bridge Methods (apps/\_shared/hooks/useBridge.ts)

Update the `AppBridge` interface:

```typescript
export interface AppBridge {
  // ... existing capabilities

  myFeature: {
    create(data: unknown): Promise<void>;
    get(id: string): Promise<unknown | null>;
    list(): Promise<unknown[]>;
    delete(id: string): Promise<boolean>;
  };
}
```

Update the `Capabilities` interface:

```typescript
interface Capabilities {
  scheduler?: { enabled?: boolean; max_jobs?: number };
  webhooks?: { enabled?: boolean };
  storage?: { enabled?: boolean };
  myFeature?: { enabled?: boolean };
}
```

Add permission check:

```typescript
if (method.startsWith('myFeature.')) {
  if (!capabilities?.myFeature?.enabled) {
    throw new Error('Capability denied: myFeature not enabled in APP.yaml');
  }
}
```

Add the bridge implementation:

```typescript
const bridge: AppBridge = {
  // ... existing capabilities

  myFeature: {
    create: (data) => callBridge('myFeature.create', { data }),
    get: (id) => callBridge('myFeature.get', { id }),
    list: () => callBridge('myFeature.list', {}),
    delete: async (id) => {
      const result = await callBridge<{ deleted: boolean }>('myFeature.delete', { id });
      return result.deleted;
    },
  },
};
```

### Step 7: Write Tests

Create `tests/dashboard/myFeature.test.ts`:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import express from 'express';
import request from 'supertest';

// Test database service methods
describe('MyFeatureDatabase Service', () => {
  // Test initialize, create, get, list, delete
});

// Test bridge API endpoints
describe('Bridge API MyFeature Endpoints', () => {
  // Test permission checks
  // Test CRUD operations
});
```

### Step 8: Update Documentation

Add a section to this skill document describing the new capability, including:

- APP.yaml configuration
- Available methods
- Example usage code
- When to use this capability

### Checklist

When adding a new bridge capability, ensure you have:

- [ ] Added Zod schema and TypeScript type in `packages/apps/src/types.ts`
- [ ] Created database service in `packages/dashboard/src/services/`
- [ ] Added to `DashboardServices` interface and initialization
- [ ] Added bridge method handlers in `apps.routes.ts`
- [ ] Passed service to routes in `routes.ts`
- [ ] Added frontend bridge interface and implementation in `useBridge.ts`
- [ ] Added permission checking for the new capability
- [ ] Written tests for database service and bridge API
- [ ] Updated skill documentation with usage examples
- [ ] Rebuilt the `@orientbot/apps` package (`pnpm --filter @orientbot/apps exec tsc`)
