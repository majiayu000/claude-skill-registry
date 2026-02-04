---
name: canvas-code-execution
description: Develops Canvas code execution features with Pyodide/iframe sandboxing. Use when working on Python/JS execution, package management, or sandbox security.
allowed-tools: Read, Write, Edit, Glob
context: fork
---

# Canvas Code Execution Skill

## When to Use

Use this skill when:

- Implementing Python execution via Pyodide
- Adding JavaScript execution via iframe sandbox
- Working with package management (micropip)
- Handling execution errors and timeouts
- Adding new supported languages

## Architecture Overview

```
lib/canvas/
├── execution-errors.ts    # Typed error handling with user-friendly messages
├── import-detector.ts     # Python import parsing and package detection
├── package-manager.ts     # Pyodide singleton + micropip integration
├── package-security.ts    # Allowlist/blocklist for packages
├── monaco-loader.ts       # Monaco editor with CDN fallback
└── types.ts               # Canvas types and language support

components/canvas/
├── canvas-preview.tsx     # Execution preview with Pyodide/iframe
├── canvas-editor.tsx      # Monaco editor wrapper
└── canvas-panel.tsx       # Full Canvas panel with split view
```

## Security Model (NEVER VIOLATE)

### 1. Package Allowlist Only

```typescript
// ✅ CORRECT: Check allowlist before loading
import { isPackageAllowed, isPackageBlocked } from '@/lib/canvas/package-security';

if (!isPackageAllowed(packageName)) {
  throw new CanvasExecutionError({
    code: CanvasErrorCode.PACKAGE_NOT_ALLOWED,
    context: { packageName }
  });
}
```

### 2. Block Dynamic Imports

```typescript
// DANGEROUS_PATTERNS in import-detector.ts blocks:
// - __import__()
// - importlib.import_module()
// - exec()
// - eval()
// - compile() with 'exec'
// - getattr(__import__)
// - builtins.__import__
```

### 3. Iframe Sandbox Restrictions

```typescript
// For JavaScript execution - minimal permissions
const sandbox = [
  'allow-scripts',
  // NO allow-same-origin
  // NO allow-forms
  // NO allow-popups
].join(' ');
```

### 4. Execution Timeouts

```typescript
// Always enforce timeouts
const EXECUTION_TIMEOUT = 30_000;      // 30s for code
const PYODIDE_LOAD_TIMEOUT = 60_000;   // 60s for Pyodide init
const PACKAGE_INSTALL_TIMEOUT = 120_000; // 2min for packages
```

## Error Handling Pattern

### CanvasExecutionError Class

```typescript
import { CanvasExecutionError, CanvasErrorCode } from '@/lib/canvas/execution-errors';

// Creating errors
throw new CanvasExecutionError({
  code: CanvasErrorCode.EXECUTION_SYNTAX_ERROR,
  context: {
    lineNumber: 5,
    traceback: pythonTraceback,
  },
});

// Factory methods
CanvasExecutionError.fromPythonError(traceback, duration);
CanvasExecutionError.timeout(duration, 'execution');
CanvasExecutionError.packageError(packageName, 'not_allowed');

// For UI display (user-friendly)
const display = error.toUserDisplay();
// { title, message, recovery[], severity, showRefresh }
```

### Error Severity Levels

| Severity          | Meaning                            | Action               |
| ----------------- | ---------------------------------- | -------------------- |
| `user`            | Code error (syntax, runtime)       | Show fix suggestions |
| `recoverable`     | Timeout, network                   | Retry button         |
| `reload_required` | Memory exceeded, crash             | Refresh button       |
| `fatal`           | CDN unreachable, sandbox violation | Feature unavailable  |

## Import Detection

### Analyzing Code for Packages

```typescript
import { analyzeImports, validateImports } from '@/lib/canvas/import-detector';

const analysis = analyzeImports(pythonCode);

// analysis.packagesToLoad: string[]     - External packages needed
// analysis.blockedPackages: {...}[]     - Blocked with reasons
// analysis.stdlibPackages: string[]     - Python stdlib (no action)
// analysis.unknownPackages: string[]    - Unknown (may work)
// analysis.canExecute: boolean          - Safe to run
// analysis.warnings: string[]           - User warnings
// analysis.estimatedDownloadKB: number  - Total download size
```

### Quick Validation

```typescript
const { valid, errors, warnings } = validateImports(code);
if (!valid) {
  // Show errors to user
}
```

## Package Manager Usage

### Singleton Pattern

```typescript
import { PyodidePackageManager, getPackageManager } from '@/lib/canvas/package-manager';

const manager = getPackageManager({
  verbose: process.env.NODE_ENV === 'development',
  onProgress: (progress) => {
    // Update UI with progress.message, progress.packagesLoaded, etc.
  },
});

// Initialize once per page
await manager.initialize();

// Execute with automatic package loading
const result = await manager.executeWithPackages(code);
// { success, output, error, returnValue, durationMs }
```

### Progress Callbacks

```typescript
interface PackageLoadProgress {
  status: 'analyzing' | 'downloading' | 'installing' | 'complete' | 'error';
  currentPackage: string | null;
  packagesTotal: number;
  packagesLoaded: number;
  estimatedSizeKB: number;
  downloadedKB: number;
  message: string;
}
```

## Adding New Packages

### 1. Add to Allowlist

```typescript
// In package-security.ts ALLOWED_PACKAGES
newpackage: {
  name: "newpackage",
  displayName: "New Package",
  description: "Short student-friendly description",
  tier: PackageTier.STANDARD,        // or DATA_SCIENCE, PURE_PYTHON
  category: PackageCategory.DATA,     // or MATH, VISUALIZATION, etc.
  sizeKB: 2000,                       // Download size
  memoryKB: 15_000,                   // RAM when loaded
  isPurePython: true,                 // Or false for C extensions
  aliases: ["np"],                    // Import aliases
  dependencies: ["numpy"],            // Auto-installed
  warnSlowLoad: false,
  warnMemory: false,
},
```

### 2. Update Blocklist If Needed

```typescript
// In BLOCKED_PACKAGES
dangerouspackage: {
  reason: "Security reason visible to students",
  alternatives: ["safe-alternative"],
},
```

## Monaco Editor Integration

### Loading with Fallback

```typescript
import { initializeMonaco, isMonacoReady, resetMonacoLoader } from '@/lib/canvas/monaco-loader';

// CDN fallback chain:
// 1. jsdelivr (primary)
// 2. unpkg
// 3. cdnjs

// Handle AMD conflicts with Pyodide
// - Monaco and Pyodide both use AMD loaders
// - package-manager.ts sets __pyodideLoadingAMD flag
// - monaco-loader.ts waits for this flag before loading
```

### Reset on Error

```typescript
try {
  await initializeMonaco();
} catch (error) {
  resetMonacoLoader();
  // Retry or show error
}
```

## Language Support

### Execution Matrix

```typescript
// From types.ts
export const EXECUTION_SUPPORT: Record<string, 'pyodide' | 'iframe' | 'none'> = {
  python: 'pyodide',
  javascript: 'iframe',
  typescript: 'iframe',  // Transpiled
  html: 'iframe',
  react: 'iframe',
  css: 'iframe',
  sql: 'none',
  java: 'none',
  // etc.
};
```

### Adding New Language

1. Add to `SUPPORTED_LANGUAGES` tiers in `types.ts`
2. Set execution support in `EXECUTION_SUPPORT`
3. Add Monaco language ID mapping in `getMonacoLanguage()`
4. Add file extension in `getFileExtension()`

## Component Integration

### Canvas Preview

```tsx
// In canvas-preview.tsx
<CanvasPreview
  content={code}
  language="python"
  onExecutionResult={(result) => {
    // Handle output, errors
  }}
  onExecutionStart={() => {
    // Show loading
  }}
/>
```

### Error Display

```tsx
import { CanvasExecutionError } from '@/lib/canvas/execution-errors';

function ExecutionErrorDisplay({ error }: { error: CanvasExecutionError }) {
  const display = error.toUserDisplay();

  return (
    <div className={cn('p-4 rounded-lg', severityStyles[display.severity])}>
      <h4 className="font-medium">{display.title}</h4>
      <p className="text-sm mt-1">{display.message}</p>
      {display.recovery.length > 0 && (
        <ul className="text-xs mt-2 space-y-1">
          {display.recovery.map((r, i) => (
            <li key={i}>• {r}</li>
          ))}
        </ul>
      )}
      {display.showRefresh && (
        <Button onClick={() => window.location.reload()} size="sm">
          Refresh Page
        </Button>
      )}
    </div>
  );
}
```

## Testing Checklist

- [ ] Python execution with imports works
- [ ] Package loading shows progress
- [ ] Blocked packages show helpful alternatives
- [ ] Timeouts trigger with recovery options
- [ ] Mobile memory warnings appear
- [ ] Monaco loads (check AMD conflicts)
- [ ] Iframe sandbox restrictions enforced
- [ ] Error messages are student-friendly
- [ ] Dynamic import patterns are blocked
