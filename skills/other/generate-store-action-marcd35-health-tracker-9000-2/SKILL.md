---
name: generate-store-action
description: Generate Zustand async action with loading/error states and toast notifications. Use when adding new API calls to the health store.
allowed-tools: Read, Edit, Grep
---

# Generate Store Action

Generate a Zustand async action for the health store with loading/error state management.

## Usage

When user requests to add a store action, ask for:

1. **Action name** (e.g., "fetchWaterLogs", "addSleepLog", "updateWeight")
2. **API endpoint** (e.g., "/api/water-intake", "/api/sleep")
3. **HTTP method** (GET, POST, PUT, DELETE)
4. **Request/response types**
5. **State updates** needed (what gets stored in Zustand)

## Implementation Pattern

Based on `src/lib/store/healthStore.ts` existing patterns.

### Pattern Structure

Add to existing store in `src/lib/store/healthStore.ts`:

```typescript
// In HealthState interface:
interface HealthState {
  // ... existing state ...
  waterLogs: WaterLog[];

  // ... existing actions ...
  fetchWaterLogs: (date: string) => Promise<void>;
  addWaterLog: (log: Omit<WaterLog, 'id' | 'createdAt'>) => Promise<void>;
  deleteWaterLog: (id: string) => Promise<void>;
}

// In the store creation:
export const useHealthStore = create<HealthState>((set, get) => ({
  // ... existing state ...
  waterLogs: [],

  // ... existing actions ...

  fetchWaterLogs: async (date: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`/api/water-intake?date=${date}`);
      if (!response.ok) throw new Error('Failed to fetch water logs');
      const data = await response.json();
      set({ waterLogs: data, isLoading: false });
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
      toast.error(err.message || 'Failed to fetch water logs');
    }
  },

  addWaterLog: async (log: Omit<WaterLog, 'id' | 'createdAt'>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch('/api/water-intake', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(log),
      });
      if (!response.ok) throw new Error('Failed to add water log');
      const newLog = await response.json();
      set({
        waterLogs: [...get().waterLogs, newLog],
        isLoading: false,
      });
      toast.success('Water intake logged');
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
      toast.error(err.message || 'Failed to add water log');
    }
  },

  deleteWaterLog: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`/api/water-intake?id=${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Failed to delete water log');
      set({
        waterLogs: get().waterLogs.filter((log) => log.id !== id),
        isLoading: false,
      });
      toast.success('Water log deleted');
    } catch (err: any) {
      set({ error: err.message, isLoading: false });
      toast.error(err.message || 'Failed to delete water log');
    }
  },
}));
```

## Key Conventions

- Always wrap in `set({ isLoading: true, error: null })`
- Use `await fetch()` with proper method and headers
- Check `!response.ok` to handle HTTP errors
- Parse response with `await response.json()`
- Use `get()` to access current state in actions
- Update state with `set()` including `isLoading: false`
- Call `toast.success()` on success
- Call `toast.error()` on failure
- Include error message in toast: `err.message || 'Default message'`
- For arrays: use spread operator to create new array
- State updates are immutable (don't mutate existing state)

## Steps

1. Ask user for action name, API endpoint, method, and types
2. Open `src/lib/store/healthStore.ts`
3. Add action type to HealthState interface
4. Add initial state if needed (empty array, null, etc.)
5. Implement action function following the pattern above
6. Include proper error handling and toast notifications
7. Format with Prettier

## Implementation Checklist

- [ ] Action added to HealthState interface
- [ ] Initial state added if new data field
- [ ] Async action with try-catch
- [ ] Loading state managed (set/unset)
- [ ] Error state managed
- [ ] API endpoint correct
- [ ] HTTP method correct
- [ ] Response validation (!response.ok)
- [ ] Toast notifications added
- [ ] State updates are immutable
- [ ] get() used to access current state
