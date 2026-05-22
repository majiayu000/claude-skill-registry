---
name: tauri-dev
description: Tauri desktop application development patterns. Use when building the SpecFlux desktop app, implementing IPC communication between Rust and React, managing windows, or testing Tauri commands.
---

# Tauri Development Patterns

## IPC Communication

Always define IPC commands with TypeScript types:

```rust
// src-tauri/src/main.rs
#[tauri::command]
fn start_agent(task_id: i32) -> Result<(), String> {
    // Implementation
    Ok(())
}
```

```typescript
// frontend/src/api/tauri.ts
import { invoke } from '@tauri-apps/api/tauri';

export async function startAgent(taskId: number): Promise<void> {
  await invoke('start_agent', { taskId });
}
```

## Window Management

Create windows programmatically:

```typescript
import { WebviewWindow } from '@tauri-apps/api/window';

const taskWindow = new WebviewWindow('task-detail', {
  url: '/task/42',
  title: 'Task #42',
  width: 800,
  height: 600
});
```

## Testing Tauri Commands

```typescript
// tests/tauri.test.ts
import { mockIPC } from '@tauri-apps/api/mocks';

describe('Tauri IPC', () => {
  beforeEach(() => {
    mockIPC((cmd, args) => {
      if (cmd === 'start_agent') {
        return Promise.resolve();
      }
    });
  });

  test('starts agent', async () => {
    await expect(startAgent(42)).resolves.toBeUndefined();
  });
});
```
