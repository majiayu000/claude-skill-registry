---
description: Chrome extension development patterns and conventions
---

# Chrome Extension Development

## Architecture Overview

Brief's Chrome extension provides AI chat directly in the browser using **Side Panel** architecture.

**Key Components:**
- **Manifest V3**: Modern Chrome extension format
- **Side Panel**: Chrome's native side panel API (not content scripts)
- **OAuth Authentication**: chrome.identity.launchWebAuthFlow with PKCE
- **Shared Business Logic**: Imports from `@briefhq/chat-ui` package
- **Context Awareness**: Tracks active tab URL for contextual assistance

## Side Panel Architecture

Brief uses Chrome's Side Panel API, **NOT content script injection**:

```typescript
// sidepanel.tsx - Main entry point
export default function SidePanel() {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [contextUrl, setContextUrl] = useState<string | undefined>();

  // Check auth on mount
  useEffect(() => {
    const token = await getValidAccessToken();
    setAccessToken(token);
  }, []);

  // Track active tab URL
  useEffect(() => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      setContextUrl(tabs[0]?.url);
    });

    chrome.tabs.onActivated.addListener(handleTabChange);
    chrome.tabs.onUpdated.addListener(handleUrlChange);
  }, []);

  return <ChatInterface accessToken={accessToken} contextUrl={contextUrl} />;
}
```

**Manifest Configuration:**
```json
{
  "manifest_version": 3,
  "permissions": ["sidePanel", "activeTab", "storage", "tabs", "identity"],
  "side_panel": {
    "default_path": "sidepanel.html"
  },
  "commands": {
    "toggle-side-panel": {
      "suggested_key": {
        "default": "Ctrl+Shift+B",
        "mac": "Command+Shift+B"
      }
    }
  }
}
```

## Shared Code from @briefhq/chat-ui

The extension reuses business logic from the `@briefhq/chat-ui` package (monorepo sibling):

### Shared Hooks

| Hook | Purpose |
|------|---------|
| `useChatTransport` | Manages streaming, messages, conversation state |
| `useConversationHistory` | Load/save/delete conversations |
| `usePresets` | Fetch and select chat presets |
| `useContextStatus` | Track token usage in context window |
| `useMessageFeedback` | Submit thumbs up/down to Helicone |
| `useFileAttachments` | File selection, validation, removal |
| `useMentions` | Document search and @-mention selection |

### Shared UI Components

| Component | Purpose |
|-----------|---------|
| `Conversation`, `ConversationContent` | Scroll container |
| `Message`, `MessageContent` | Message bubbles |
| `Response` | Markdown rendering |
| `Tool`, `ToolHeader`, `ToolContent`, `ToolInput`, `ToolOutput` | Tool call display |
| `Reasoning`, `ReasoningTrigger`, `ReasoningContent` | Extended thinking UI |
| `Loader` | Loading indicator |

### Import Pattern

```typescript
// ✅ GOOD - Import shared hooks and components from @briefhq/chat-ui
import {
  useChatTransport,
  useConversationHistory,
  usePresets,
  Conversation,
  Message,
  Response,
  Tool,
  Loader,
} from "@briefhq/chat-ui";

// Extension-specific orchestration
export function ChatInterface({ accessToken, contextUrl }: Props) {
  const transport = useChatTransport({ defaultModel: "claude-sonnet-4-5" });
  const history = useConversationHistory({ api, onConversationLoaded });
  const presets = usePresets({ api });

  // Extension-specific logic here
  return (
    <div>
      <ChatHeader presets={presets} onSignOut={onSignOut} />
      <Conversation>
        {messages.map(msg => <Message key={msg.id} message={msg} />)}
      </Conversation>
      <ChatInputArea onSubmit={handleSubmit} />
    </div>
  );
}
```

```typescript
// ❌ BAD - Don't recreate what exists in @briefhq/chat-ui
export function ChatInterface() {
  // Don't reimplement shared business logic
  const [messages, setMessages] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);

  // This should use useChatTransport instead
  const handleSubmit = async (input: string) => {
    // Streaming logic...
  };
}
```

## When to Create Extension-Specific Components

Create components in `packages/chrome-extension/components/` ONLY when:

1. **Chrome API Integration**: Component uses chrome.tabs, chrome.storage, chrome.identity
2. **Extension-Specific UI**: Component is unique to side panel context (e.g., sign-in flow, header with sign-out)
3. **Extension-Specific Configuration**: Wrapper needed for extension constraints

**Example - Extension-specific header:**
```typescript
// components/chat/views/ChatHeader.tsx
// Extension-specific because it has sign-out, model selector, history toggle
export function ChatHeader({ presets, onSignOut }: Props) {
  return (
    <header className="flex items-center justify-between px-4 py-3 border-b">
      <PresetSelector presets={presets} />
      <ModelSelector models={AVAILABLE_MODELS} />
      <button onClick={onSignOut}>Sign out</button>
    </header>
  );
}
```

## OAuth Authentication

Brief uses **chrome.identity API** with PKCE for OAuth 2.0:

```typescript
// lib/oauth.ts

// Start OAuth flow
export async function startOAuthFlow() {
  // Generate PKCE challenge
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);

  // Launch web auth flow
  const redirectUrl = chrome.identity.getRedirectURL();
  const authUrl = `${BRIEF_URL}/oauth/authorize?` +
    `client_id=${CLIENT_ID}&` +
    `redirect_uri=${redirectUrl}&` +
    `response_type=code&` +
    `code_challenge=${codeChallenge}&` +
    `code_challenge_method=S256`;

  const responseUrl = await chrome.identity.launchWebAuthFlow({
    url: authUrl,
    interactive: true,
  });

  // Exchange code for tokens
  const code = extractCodeFromUrl(responseUrl);
  const tokens = await exchangeCodeForTokens(code, codeVerifier);

  // Store in chrome.storage.local
  await chrome.storage.local.set({
    access_token: tokens.access_token,
    refresh_token: tokens.refresh_token,
    expires_at: Date.now() + tokens.expires_in * 1000,
  });

  return tokens;
}

// Get valid token (auto-refresh if needed)
export async function getValidAccessToken(): Promise<string | null> {
  const { access_token, expires_at, refresh_token } =
    await chrome.storage.local.get(["access_token", "expires_at", "refresh_token"]);

  if (!access_token) return null;

  // Check if token needs refresh
  if (Date.now() >= expires_at - 60000) {
    return await refreshAccessToken(refresh_token);
  }

  return access_token;
}
```

## API Integration

Extension calls Brief API with OAuth Bearer tokens:

```typescript
// hooks/use-extension-api.ts
export function useExtensionApi(accessToken: string) {
  return {
    async chat(messages, options) {
      const response = await fetch(`${BRIEF_URL}/api/v1/chat`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages,
          model: options.model,
          contextUrl: options.contextUrl, // Current tab URL
        }),
      });
      return response.body; // Streaming response
    },

    async fetchConversations() {
      const response = await fetch(`${BRIEF_URL}/api/v1/conversations`, {
        headers: { "Authorization": `Bearer ${accessToken}` },
      });
      return response.json();
    },

    async searchDocuments(query: string) {
      const response = await fetch(
        `${BRIEF_URL}/api/v1/documents/search?q=${query}`,
        {
          headers: { "Authorization": `Bearer ${accessToken}` },
        }
      );
      return response.json();
    },
  };
}
```

## Component Organization

```text
packages/chrome-extension/
├── sidepanel.tsx          # Main entry (auth + ChatInterface)
├── background.ts          # Service worker (keyboard shortcuts)
├── lib/
│   ├── oauth.ts           # OAuth 2.0 with PKCE
│   └── utils.ts           # Utility functions
├── components/chat/
│   ├── ChatInterface.tsx  # Main orchestrator (~400 LOC)
│   ├── hooks/
│   │   └── use-extension-api.ts  # Extension-specific API wrapper
│   ├── views/             # Extension-specific UI
│   │   ├── ChatHeader.tsx        # Header with sign-out
│   │   ├── ChatHistoryView.tsx   # History sidebar
│   │   ├── ChatEmptyState.tsx    # Empty state
│   │   └── ChatInputArea.tsx     # Input with @-mentions
│   ├── MentionExtension.tsx      # TipTap mention config
│   ├── MentionList.tsx           # Mention dropdown
│   ├── ContextRing.tsx           # Context indicator
│   └── EnhancedFileContent.tsx   # File preview
└── __tests__/             # Vitest unit tests
```

**Rule:** Extension components ONLY in `components/chat/`. Shared components come from `@briefhq/chat-ui`.

## Development Workflow

### Local Setup

```bash
cd packages/chrome-extension
pnpm install

# Create environment file
cp .env.dev.example .env.dev

# Start dev server (hot reload)
pnpm run dev
```

### Load Extension in Chrome

1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `packages/chrome-extension/build/chrome-mv3-dev`

### Build for Different Environments

| Environment | Command | Target |
|-------------|---------|--------|
| Dev | `pnpm run build` | localhost:3000 |
| Staging | `pnpm run build:staging` | staging.briefhq.ai |
| QA | `pnpm run build:qa` | app.briefhq.ai (internal) |
| Production | `pnpm run build:production` | app.briefhq.ai (public) |

### Package for Distribution

```bash
# QA build (.crx for internal testing)
pnpm run package:qa

# Production build (for Chrome Web Store)
pnpm run package:production
```

## Testing

Brief extension uses Vitest for unit tests:

```typescript
import { describe, it, expect, vi } from "vitest";
import { render, waitFor } from "@testing-library/react";
import { ChatInterface } from "./ChatInterface";

// Mock Chrome APIs
vi.mock("chrome", () => ({
  tabs: {
    query: vi.fn(),
    onActivated: { addListener: vi.fn(), removeListener: vi.fn() },
    onUpdated: { addListener: vi.fn(), removeListener: vi.fn() },
  },
  storage: {
    local: {
      get: vi.fn(),
      set: vi.fn(),
    },
  },
}));

describe("ChatInterface", () => {
  it("renders chat UI when authenticated", () => {
    const { getByRole } = render(
      <ChatInterface accessToken="test-token" contextUrl="https://example.com" />
    );

    expect(getByRole("textbox")).toBeInTheDocument();
  });

  it("passes contextUrl to chat API", async () => {
    const { getByRole, getByText } = render(
      <ChatInterface
        accessToken="test-token"
        contextUrl="https://example.com/page"
      />
    );

    const input = getByRole("textbox");
    await userEvent.type(input, "Summarize this page");
    await userEvent.click(getByText("Send"));

    // Verify contextUrl passed to API
    expect(fetchMock).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        body: expect.stringContaining("https://example.com/page"),
      })
    );
  });
});
```

### Run Tests

```bash
pnpm test                # Run all tests
pnpm run test:watch      # Watch mode
pnpm run test:coverage   # Coverage report
```

## Key Differences from Web App

| Feature | Web App | Extension |
|---------|---------|-----------|
| **Architecture** | Next.js pages | Side Panel |
| **Authentication** | Clerk session cookies | OAuth Bearer tokens |
| **API URL** | Relative (`/api/...`) | Absolute (`https://app.briefhq.ai/api/...`) |
| **Context** | Current page (server-side) | Active tab URL (chrome.tabs API) |
| **Presets** | All presets | Excludes "onboarding" preset |
| **Storage** | Supabase + Clerk | chrome.storage.local for tokens |

## Common Patterns

### Passing Context URL

```typescript
// ✅ GOOD - Use current tab URL for context
export function ChatInterface({ contextUrl }: Props) {
  const handleSubmit = async (input: string) => {
    await api.chat(messages, {
      contextUrl, // Current tab URL
      model: selectedModel,
    });
  };
}
```

### Model Selection

```typescript
// ✅ GOOD - Store model selection in state
const [selectedModel, setSelectedModel] = useState<ModelId>("claude-sonnet-4-5");

// Pass to useChatTransport
const transport = useChatTransport({
  defaultModel: selectedModel,
});
```

### File Attachments

```typescript
// ✅ GOOD - Use useFileAttachments hook from @briefhq/chat-ui
const fileAttachments = useFileAttachments({
  maxFiles: 10,
  maxSize: 32 * 1024 * 1024, // 32MB
  allowedTypes: ["image/*", "application/pdf", "text/*"],
});

// In UI
<ChatInputArea
  files={fileAttachments.files}
  onFilesSelected={fileAttachments.addFiles}
  onFileRemove={fileAttachments.removeFile}
/>
```

### Document @-Mentions

```typescript
// ✅ GOOD - Use useMentions hook from @briefhq/chat-ui
const mentions = useMentions({
  api,
  onMentionSelected: (doc: MentionDocument) => {
    // Append to input
  },
});

// In TipTap editor
<Editor
  extensions={[
    StarterKit,
    Mention.configure({
      suggestion: mentions.suggestionOptions,
    }),
  ]}
/>
```

## Troubleshooting

### OAuth Issues

**Problem:** "Authentication failed" error
- **Check:** Extension ID in OAuth client redirect URIs
- **Fix:** Add `https://{extension-id}.chromiumapp.org/` to allowed redirect URIs

**Problem:** Token expired
- **Check:** Token refresh logic in `lib/oauth.ts`
- **Fix:** Implement automatic refresh 60 seconds before expiry

### API Issues

**Problem:** CORS errors
- **Check:** `host_permissions` in manifest.json
- **Fix:** Add API domain to `host_permissions`

### Build Issues

**Problem:** Hot reload not working
- **Check:** Plasmo dev server running
- **Fix:** Run `pnpm run dev` and reload extension

## Documentation References

- Chrome Extension Architecture: `/docs/CHROME_EXTENSION_ARCHITECTURE.md`
- Extension README: `/packages/chrome-extension/README.md`
- Shared Chat UI: `/packages/chat-ui/`

## Related Code

- OAuth flow: `packages/chrome-extension/lib/oauth.ts`
- Chat interface: `packages/chrome-extension/components/chat/ChatInterface.tsx`
- Side panel entry: `packages/chrome-extension/sidepanel.tsx`
- Extension API: `packages/chrome-extension/components/chat/hooks/use-extension-api.ts`
