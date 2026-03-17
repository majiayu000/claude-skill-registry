---
description: Use this skill when the user asks about "Storybook with Tauri", "Storybook with Electron", "desktop app components", "Tauri IPC mocking", "Electron limitations", mentions "cross-platform development", "native APIs in Storybook", or wants to develop Storybook stories for Tauri or Electron applications. This skill provides platform-specific guidance and architectural patterns for multi-platform component development.
---

# Platform Support Skill

## Overview

Develop Storybook components for desktop applications (Tauri and Electron) with platform-specific guidance, IPC mocking patterns, and architectural best practices for maximum testability.

This skill provides comprehensive documentation on integrating Storybook with Tauri (full support) and Electron (partial support with workarounds).

## What This Skill Provides

### Platform Compatibility Guide
Understand support levels for each platform:
- **Web**: Full support (100%)
- **Tauri**: Full support (100%) - Excellent compatibility
- **Electron**: Partial support (~60%) - Requires architectural patterns

### Tauri Support
Complete guidance for Tauri applications:
- **Development workflow**: Parallel dev servers
- **IPC mocking**: Mock Tauri API calls in stories
- **Component architecture**: Dependency injection patterns
- **Testing strategies**: Unit, integration, and E2E testing

### Electron Support
Limitations documentation and workarounds:
- **What works**: Pure UI components, design systems
- **What doesn't work**: Direct Electron module imports, IPC in iframes
- **Architectural solutions**: Container/presentational pattern
- **Testing alternatives**: E2E tests with Playwright

### Best Practices
Platform-agnostic component patterns:
- Dependency injection for IPC calls
- Container/presentational separation
- Mock providers for stories
- Type-safe API abstractions

## Tauri Support - Full Compatibility ✅

### Why It Works

Tauri and Storybook work **excellently** together:

- **Separate processes**: No conflicts between Storybook and Tauri runtime
- **Independent development**: Develop UI without Tauri rebuilds
- **Parallel dev servers**: Run both simultaneously
- **Full testing**: All components testable in Storybook

### Development Workflow

Run Tauri and Storybook in parallel:

```bash
# Terminal 1: Tauri development server
npm run tauri dev
# Runs on http://localhost:5173

# Terminal 2: Storybook
npm run storybook
# Runs on http://localhost:6006

# Terminal 3: Tests in watch mode
npm run test:watch
```

### Component Architecture Pattern

**Best Practice: Dependency Injection**

Keep components Tauri-agnostic by injecting IPC functionality:

```typescript
// ✅ Good: Testable component
interface ApiClient {
  readFile: (path: string) => Promise<string>;
  writeFile: (path: string, content: string) => Promise<void>;
}

function FileEditor({ apiClient }: { apiClient: ApiClient }) {
  const [content, setContent] = useState('');

  const handleSave = async () => {
    await apiClient.writeFile('file.txt', content);
  };

  return <textarea value={content} onChange={(e) => setContent(e.target.value)} />;
}

// In Tauri app: Inject real API
<FileEditor apiClient={tauriApiClient} />

// In Storybook: Inject mock API
<FileEditor apiClient={mockApiClient} />
```

### IPC Mocking in Storybook

Create mock providers for Tauri API calls:

```typescript
// .storybook/tauri-mocks.ts
export const mockTauriApi = {
  invoke: async (cmd: string, args?: any) => {
    switch (cmd) {
      case 'read_file':
        return 'Mock file content';
      case 'write_file':
        return { success: true };
      default:
        return null;
    }
  },
};

// In story
export const WithTauriAPI: Story = {
  decorators: [
    (Story) => {
      if (typeof window !== 'undefined') {
        window.__TAURI__ = mockTauriApi;
      }
      return <Story />;
    },
  ],
};
```

### Project Structure

Recommended structure for Tauri + Storybook:

```
tauri-app/
├── src/
│   ├── components/           # UI components (testable)
│   │   ├── Button.tsx
│   │   ├── Button.stories.tsx
│   │   ├── FileEditor.tsx
│   │   └── FileEditor.stories.tsx
│   ├── api/
│   │   └── tauri.ts         # Tauri IPC abstraction
│   └── main.tsx
├── src-tauri/                # Rust backend
│   ├── src/
│   └── tauri.conf.json
├── .storybook/
│   ├── main.ts
│   ├── preview.ts
│   └── tauri-mocks.ts       # IPC mocks
└── package.json
```

## Electron Support - Partial Compatibility ⚠️

### Major Limitation

**Iframe Incompatibility:**
- Storybook renders stories in iframes
- Electron modules (`ipcRenderer`) are not available in iframe context
- Webpack `electron-renderer` target creates externals that fail

**Impact:**
- ❌ Components with direct `electron` imports won't work
- ❌ IPC calls cannot be tested in Storybook
- ❌ Main process code cannot be accessed

### What Works ✅

#### 1. Pure UI Components

Components without Electron dependencies work perfectly:

```typescript
// ✅ Works perfectly
function Button({ variant, onClick }) {
  return (
    <button className={`btn-${variant}`} onClick={onClick}>
      Click Me
    </button>
  );
}
```

#### 2. Design System Components

UI libraries work without issues:

```typescript
// ✅ Works - Material UI, shadcn/ui, etc.
import { Card } from '@mui/material';

function ProfileCard({ name, bio }) {
  return <Card>{/* UI content */}</Card>;
}
```

#### 3. State Management

Redux, Zustand, Context API all work:

```typescript
// ✅ Works
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### What Doesn't Work ❌

```typescript
// ❌ Won't work in Storybook
import { ipcRenderer } from 'electron';

function FileReader() {
  const readFile = () => {
    ipcRenderer.invoke('read-file', '/path/to/file');
  };
  // This will fail in Storybook iframe
}
```

### Architectural Solution: Container/Presentational Pattern

**Separate concerns to maximize testability:**

```typescript
// ✅ Presentational Component (testable in Storybook)
interface FileListProps {
  files: string[];
  isLoading: boolean;
  error?: string;
  onRefresh: () => void;
}

function FileList({ files, isLoading, error, onRefresh }: FileListProps) {
  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <button onClick={onRefresh}>Refresh</button>
      <ul>
        {files.map(file => <li key={file}>{file}</li>)}
      </ul>
    </div>
  );
}

// ❌ Container Component (not testable in Storybook)
function FileListContainer() {
  const [files, setFiles] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const loadFiles = async () => {
    setLoading(true);
    const result = await window.api.readDir('/path');
    setFiles(result);
    setLoading(false);
  };

  return <FileList files={files} isLoading={loading} onRefresh={loadFiles} />;
}
```

**In Storybook, test the presentational component:**

```typescript
export const Default: Story = {
  args: {
    files: ['file1.txt', 'file2.txt', 'file3.txt'],
    isLoading: false,
    onRefresh: fn(),
  },
};

export const Loading: Story = {
  args: {
    files: [],
    isLoading: true,
    onRefresh: fn(),
  },
};

export const Error: Story = {
  args: {
    files: [],
    isLoading: false,
    error: 'Failed to load files',
    onRefresh: fn(),
  },
};
```

### Testing Strategy for Electron

**Use multiple testing approaches:**

1. **Storybook**: Test presentational components (60% of UI)
2. **Vitest**: Test business logic and utilities
3. **Playwright/Spectron**: E2E tests for full application flow

```bash
# Storybook: UI component testing
npm run storybook

# Vitest: Unit tests
npm run test

# Playwright: E2E tests with Electron
npm run test:e2e
```

## Best Practices for Multi-Platform Components

### 1. Abstraction Layer Pattern

Create platform-agnostic API clients:

```typescript
// api/client.ts
export interface FileSystemClient {
  readFile: (path: string) => Promise<string>;
  writeFile: (path: string, content: string) => Promise<void>;
  listFiles: (dir: string) => Promise<string[]>;
}

// api/tauri-client.ts
export const tauriClient: FileSystemClient = {
  readFile: (path) => invoke('read_file', { path }),
  writeFile: (path, content) => invoke('write_file', { path, content }),
  listFiles: (dir) => invoke('list_files', { dir }),
};

// api/electron-client.ts
export const electronClient: FileSystemClient = {
  readFile: (path) => window.api.readFile(path),
  writeFile: (path, content) => window.api.writeFile(path, content),
  listFiles: (dir) => window.api.listFiles(dir),
};

// api/mock-client.ts (for Storybook)
export const mockClient: FileSystemClient = {
  readFile: async () => 'Mock content',
  writeFile: async () => {},
  listFiles: async () => ['file1.txt', 'file2.txt'],
};
```

### 2. Context Provider Pattern

Use React Context to inject platform APIs:

```typescript
// contexts/PlatformContext.tsx
const PlatformContext = createContext<FileSystemClient>(mockClient);

export function PlatformProvider({ client, children }) {
  return (
    <PlatformContext.Provider value={client}>
      {children}
    </PlatformContext.Provider>
  );
}

export function usePlatform() {
  return useContext(PlatformContext);
}

// In component
function FileViewer() {
  const platform = usePlatform();
  const [content, setContent] = useState('');

  useEffect(() => {
    platform.readFile('file.txt').then(setContent);
  }, []);

  return <pre>{content}</pre>;
}
```

**In Storybook:**

```typescript
export const Default: Story = {
  decorators: [
    (Story) => (
      <PlatformProvider client={mockClient}>
        <Story />
      </PlatformProvider>
    ),
  ],
};
```

### 3. Feature Detection Pattern

Check for platform capabilities:

```typescript
function isElectron() {
  return typeof window !== 'undefined' && window.api !== undefined;
}

function isTauri() {
  return typeof window !== 'undefined' && window.__TAURI__ !== undefined;
}

function useFileSystem() {
  if (isTauri()) return tauriClient;
  if (isElectron()) return electronClient;
  return mockClient; // Fallback for Storybook/web
}
```

## Platform-Specific Storybook Configuration

### For Tauri Projects

Add to `.storybook/preview.ts`:

```typescript
import { mockTauriApi } from './tauri-mocks';

export const decorators = [
  (Story) => {
    if (typeof window !== 'undefined') {
      window.__TAURI__ = mockTauriApi;
    }
    return <Story />;
  },
];
```

### For Electron Projects

Add to `.storybook/preview.ts`:

```typescript
import { mockElectronApi } from './electron-mocks';

export const decorators = [
  (Story) => {
    if (typeof window !== 'undefined') {
      window.api = mockElectronApi;
    }
    return <Story />;
  },
];
```

## References

### Tauri Documentation
- **Setup Guide**: `tauri/setup_guide.md` - Complete Tauri + Storybook integration guide
- IPC mocking patterns
- Development workflow examples
- Project structure recommendations

### Electron Documentation
- **Limitations Guide**: `electron/limitations.md` - Known issues and workarounds
- Container/presentational pattern examples
- Testing strategy recommendations
- Architectural solutions

## Summary

| Platform | Support Level | Storybook Works | IPC Testable | Recommended Pattern |
|----------|--------------|-----------------|--------------|---------------------|
| Web | 100% | ✅ Yes | N/A | Standard components |
| Tauri | 100% | ✅ Yes | ✅ Yes (mocking) | Dependency injection |
| Electron | ~60% | ⚠️ Partial | ❌ No (E2E only) | Container/presentational |

**Key Takeaway:**
- **Tauri**: Use dependency injection, mock IPC in stories
- **Electron**: Separate presentational components, use E2E for containers
- **Both**: Create platform-agnostic abstractions for maximum testability
