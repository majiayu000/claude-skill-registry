---
name: idb-state-persistence
description: IndexedDB patterns for local-first state persistence using the idb library. Use when implementing features that require persistent state across navigation and sessions. Covers data modeling, defaults, CRUD operations, state managers, and reset patterns. Integrates with web-components for reactive UI updates.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# IDB State Persistence Architecture

## Philosophy

**Local Database First**: IndexedDB (IDB) is the primary source of truth for all application state. Every user interaction that changes state MUST persist to IDB immediately to survive navigation, page refreshes, and session restarts.

This architecture treats IDB as a **local database**, not a cache. State lives in IDB first, components read from it, and all mutations write through to IDB synchronously (no debouncing or batching by default).

**Why IDB over localStorage:**
- Structured data storage (objects, arrays, not just strings)
- Indexed queries for efficient retrieval
- Larger storage limits (hundreds of MB vs 5-10 MB)
- Async API that doesn't block main thread

**Relationship with Other Skills:**
- **`javascript`**: Provides error handling (Rule 1), timeout patterns (Rule 2), cleanup (Rule 4)
- **`web-components`**: Components subscribe to IDB state changes via event listeners
- **Integration**: State Managers act as the bridge between IDB and UI components

---

## Core Patterns Overview

This project uses **three IDB patterns** working together:

1. **StateStore** - Generic key-value store (simple CRUD, single object store)
2. **Specialized Stores** - Domain-specific stores with indexes (StoryStore, PracticeProgressStore)
3. **State Managers** - Wrapper classes that use StateStore + event system (GameStateManager, PracticeStateManager)

**Architecture**: Web Components → State Manager (#cache, #listeners) → StateStore/Specialized Store → IndexedDB

---

## Data Modeling Pattern

**Principle**: Define data structures using TypeScript-style JSDoc typedefs BEFORE writing any IDB code. Start with primitives, build objects, then compose arrays and nested structures.

### Step 1: Define Types with JSDoc

```javascript
/**
 * @typedef {Object} ActivityProgress
 * @property {string} activityId - Unique activity identifier
 * @property {number} tier - Tier number (1-5)
 * @property {number} highScore - Best score achieved
 * @property {number} totalAttempts - Total play count
 * @property {number} currentStreak - Consecutive successful days
 * @property {number} lastPlayed - Timestamp of last session
 */

/**
 * @typedef {Object} PracticeSession
 * @property {number} [id] - Auto-generated ID (optional, IDB creates it)
 * @property {string} activityId - References ActivityProgress
 * @property {number} timestamp - When session occurred
 * @property {number} score - Session score (0-100)
 * @property {string[]} phonemesTested - Array of phoneme IDs
 */
```

**Conventions:**
- **Primitives first**: string, number, boolean
- **Timestamps**: Always use `Date.now()` (milliseconds since epoch)
- **Optional fields**: Use `[id]` syntax in JSDoc for auto-generated or conditional fields
- **References**: Use matching ID fields (activityId links to ActivityProgress.activityId)
- **Arrays of objects**: Define the object type first, then reference in array

### Step 2: Define Default State

Create a module-level constant with complete initial state:

```javascript
const DEFAULT_PRACTICE_STATE = {
  words: [],
  phonemes: [],
  currentTier: 1,
  currentWordIndex: 0,
  settings: {
    autoAdvance: true,
    soundEnabled: true,
    showHints: true,
    tierUnlocked: 5
  },
  status: 'loading' // loading, ready, error
};
```

**Conventions:**
- **Complete structure**: Include ALL fields, even empty arrays/objects
- **Smart defaults**: Choose sensible starting values (tier: 1, index: 0)
- **Status field**: Always include a status field ('loading', 'ready', 'error')
- **Nested objects**: Define full shape, don't use null for object properties
- **Use CONST**: Defaults are immutable references, clone when using

---

## Database Initialization Pattern

### Pattern: Lazy Initialization with Module-Level Cache

```javascript
import { openDB } from 'idb';

const DB_NAME = 'fantasy-phonics-practice';
const DB_VERSION = 1;
const STORE_NAME = 'progress';

// Module-level promise cache (singleton pattern)
let dbPromise = null;

function getDB() {
  if (!dbPromise) {
    dbPromise = openDB(DB_NAME, DB_VERSION, {
      upgrade(db) {
        // Schema creation ONLY runs when DB doesn't exist or version changes
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          const store = db.createObjectStore(STORE_NAME, {
            keyPath: 'activityId' // Primary key from data
          });
          // Create indexes for common queries
          store.createIndex('tier', 'tier', { unique: false });
          store.createIndex('lastPlayed', 'lastPlayed', { unique: false });
        }
      }
    });
  }
  return dbPromise;
}
```

**Key Points:**
- **One database per feature area**: Separate DBs for game vs practice vs stories
- **Lazy init**: Only create connection when first needed
- **Module-level cache**: `dbPromise` is reused across all operations
- **Upgrade callback**: Runs ONLY on version increment or first creation
- **Check existence**: Always `if (!db.objectStoreNames.contains(...))`

### Schema Design Principles

**Object Store Naming:**
- Plural nouns: `sessions`, `stories`, `achievements`
- Lowercase, no hyphens: `phoneme_mastery` (underscore OK for multi-word)

**Key Paths:**
- **keyPath**: Use existing property for primary key (`activityId`, `id`)
- **autoIncrement**: Use when IDs are auto-generated (`{ keyPath: 'id', autoIncrement: true }`)
- **Out-of-line keys**: Don't use if you can use keyPath (simpler API)

**Indexes:**
- Create for **frequently filtered** fields (tier, date, timestamp)
- Create for **sorting** operations (createdAt, lastPlayed)
- Keep **unique: false** unless truly unique constraint needed

---

## CRUD Operations

### Pattern 1: Generic StateStore (Simple Key-Value)

Use this for **single-document state** (game state, settings, user profile).

```javascript
export const StateStore = {
  async get(key) {
    const db = await getDB();
    return db.get(STORE_NAME, key);
  },

  async set(key, value) {
    const db = await getDB();
    return db.put(STORE_NAME, value, key);
  },

  async delete(key) {
    const db = await getDB();
    return db.delete(STORE_NAME, key);
  },

  async clear() {
    const db = await getDB();
    return db.clear(STORE_NAME);
  },

  // Helper: Get with fallback
  async getOrDefault(key, fallback) {
    const value = await this.get(key);
    return value ?? fallback;
  },

  // Helper: Update function pattern
  async update(key, updater) {
    const current = await this.get(key);
    const updated = updater(current);
    await this.set(key, updated);
    return updated;
  }
};
```

**When to use**: Single state object per key (gameState, practiceMode, userSettings).

### Pattern 2: Specialized Store with Indexes

Use this for **collections with queries** (stories, sessions, achievements).

```javascript
export const StoryStore = {
  // CREATE
  async save(storyData) {
    const db = await getDB();
    const story = {
      id: generateId(), // Custom ID generation
      wordSeq: storyData.wordSeq,
      createdAt: Date.now(),
      answers: storyData.answers
    };
    await db.put(STORE_NAME, story);
    return story;
  },

  // READ - Single
  async getById(id) {
    const db = await getDB();
    return db.get(STORE_NAME, id);
  },

  // READ - Collection (all)
  async getAll() {
    const db = await getDB();
    return db.getAll(STORE_NAME);
  },

  // READ - Indexed query
  async getByWord(wordSeq) {
    const db = await getDB();
    return db.getAllFromIndex(STORE_NAME, 'wordSeq', wordSeq);
  },

  // UPDATE
  async update(id, updates) {
    const db = await getDB();
    const existing = await db.get(STORE_NAME, id);
    if (!existing) throw new Error(`Not found: ${id}`);

    const updated = { ...existing, ...updates };
    await db.put(STORE_NAME, updated);
    return updated;
  },

  // DELETE
  async delete(id) {
    const db = await getDB();
    await db.delete(STORE_NAME, id);
  },

  // CLEAR ALL
  async clear() {
    const db = await getDB();
    await db.clear(STORE_NAME);
  }
};
```

**Index Queries:**
- `db.getAllFromIndex(store, indexName, value)` - Get all matching value
- `db.getAllFromIndex(store, indexName)` - Get all, sorted by index
- Use `openCursor()` for pagination or limit results

**When to use**: Multiple documents with filtering/sorting needs (story versions, practice sessions).

### Pattern 3: State Manager with Cache

Use this for **complex state with business logic** (game progression, navigation).

```javascript
class GameStateManager {
  #cache = null;
  #listeners = new Map();
  #ready;

  constructor() {
    this.#ready = this.#init();
  }

  async #init() {
    const stored = await StateStore.get(KEY);
    this.#cache = stored ? { ...DEFAULT, ...stored } : { ...DEFAULT };
    if (!this.#cache.answers) this.#cache.answers = {}; // Ensure nested objects
    return this;
  }

  async ready() { await this.#ready; return this; }

  getState() { return { ...this.#cache }; }

  async submitAnswer(text) {
    this.#cache.answers[this.#cache.currentSeq] = { answer: text, timestamp: Date.now() };
    await this.#persist();
    this.#notify('answerSubmitted', { answer: text });
  }

  async #persist() { await StateStore.set(KEY, this.#cache); }

  onChange(event, callback) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, new Set());
    this.#listeners.get(event).add(callback);
    return () => this.#listeners.get(event)?.delete(callback);
  }

  #notify(event, data) { this.#listeners.get(event)?.forEach(cb => cb(data)); }
}

export const gameState = new GameStateManager(); // Singleton
```

**Key**: Private cache, write-through persistence, pub/sub events, singleton export, async init pattern.

---

## State Lifecycle Patterns

### Initialization Flow

```javascript
async connectedCallback() {
  await gameState.ready();
  await gameState.loadAllData(); // Fetch JSON if needed
  this.#unsubscribe = gameState.onChange('state', (data) => this.#render(data));
}

disconnectedCallback() {
  if (this.#unsubscribe) this.#unsubscribe();
}
```

**Pattern**: Constructor starts `#init()` → `ready()` awaits → load data → subscribe → cleanup in disconnectedCallback.

### Persistence Triggers

**Write-Through Pattern** (current implementation):

```javascript
async updateSetting(key, value) {
  this.#cache.settings[key] = value;
  await this.#persist(); // Immediate write
  this.#notify('settingsChanged', this.#cache.settings);
}
```

**When to persist:**
- ✅ After every state mutation (current pattern)
- ✅ After data loading completes
- ✅ After navigation/phase changes
- ⚠️ NOT after every keystroke (implement debouncing at component level if needed)

**Alternative: Debounced Persistence** (not currently used, but valid):

```javascript
#persistTimeout = null;

async #debouncedPersist(delay = 500) {
  clearTimeout(this.#persistTimeout);
  this.#persistTimeout = setTimeout(async () => {
    await StateStore.set(this.KEY, this.#cache);
  }, delay);
}
```

---

## Reset and Clear Patterns

### Pattern 1: Full Reset (Delete & Reinitialize)

```javascript
async resetAll() {
  // Clear cache to defaults
  this.#cache = { ...DEFAULT_GAME_STATE };
  this.#cache.answers = {};
  this.#cache.completedWords = [];

  // Persist clean state
  await this.#persist();

  // Reload external data
  await this.loadAllData();

  // Notify
  this.#notify('reset', null);
  this.#notify('state', this.getState());
}
```

**Use when**: User requests "Start Over" or "Reset Progress"

### Pattern 2: Selective Clear (Delete by Key)

```javascript
async clearProgress(activityId) {
  const db = await getDB();
  await db.delete(STORES.PROGRESS, activityId);
}

async clearAllProgress() {
  const db = await getDB();
  await db.clear(STORES.PROGRESS);
}
```

**Use when**: Removing specific entries without affecting other data

### Pattern 3: StateStore Clear (Entire Store)

```javascript
async clearAll() {
  await StateStore.clear(); // Clears entire state object store
}
```

**Use when**: Nuking all app state (debug, testing, logout)

### Default Restoration Logic

**Merge pattern** ensures missing fields get defaults:

```javascript
async #init() {
  const stored = await StateStore.get(KEY);

  // Merge stored with defaults (stored wins for existing keys)
  this.#cache = stored ? { ...DEFAULT_STATE, ...stored } : { ...DEFAULT_STATE };

  // Explicitly ensure nested objects exist (spread doesn't deep merge)
  if (!this.#cache.answers) this.#cache.answers = {};
  if (!this.#cache.settings) this.#cache.settings = { ...DEFAULT_STATE.settings };
}
```

**Critical**: Spread operator (`...`) only does **shallow merge**. Nested objects need explicit checks.

---

## Integration with Web Components

State Managers provide the bridge between IDB and UI via event subscriptions.

### Pattern: Subscribe in connectedCallback

```javascript
class MyComponent extends HTMLElement {
  #unsubscribe = null;

  async connectedCallback() {
    await gameState.ready();

    // Subscribe to state changes
    this.#unsubscribe = gameState.onChange('state', (newState) => {
      this.#handleStateChange(newState);
    });

    // Initial render
    this.#handleStateChange(gameState.getState());
  }

  disconnectedCallback() {
    // CRITICAL: Clean up subscription
    if (this.#unsubscribe) this.#unsubscribe();
  }

  #handleStateChange(state) {
    // Update attributes (triggers re-render via attributeChangedCallback)
    this.setAttribute('current-phase', state.currentPhase);
    this.setAttribute('progress', state.overallProgress);
  }
}
```

### Pattern: User Action → State Update → Persistence

```javascript
class AnswerInput extends HTMLElement {
  handleEvent(e) {
    if (e.type === 'submit') {
      e.preventDefault();
      const answer = this.getAttribute('value');

      // Trigger state update (which persists internally)
      gameState.submitAnswer(answer);

      // State change notification will trigger re-render
    }
  }
}
```

**Flow:**
1. User interacts with component
2. Component calls State Manager method
3. State Manager updates `#cache`, persists to IDB, notifies subscribers
4. Component receives notification, updates attributes
5. Attribute change triggers re-render (per `web-components` skill)

---

## Advanced Patterns

**Cursor Pagination**: Use `index.openCursor(null, 'prev')` + `while` loop for large collections.

**Aggregation**: Load all with `getAll()`, reduce in memory (fine for <1000 records).

**Versioning**: Query existing count, increment version field: `version = existing.length + 1`.

---

## Error Handling and Recovery

### Pattern: Try-Catch with Context (from javascript skill)

```javascript
async loadAllData() {
  try {
    const data = await this.#fetchWithTimeout('/data/words.json');
    this.#cache.words = data;
    this.#cache.status = 'ready';
    await this.#persist();
    this.#notify('dataLoaded', true);
    return true;
  } catch (error) {
    const errorMessage = error.name === 'AbortError'
      ? `Data load timed out after ${TIMEOUT}ms`
      : error.message;

    console.error('Failed to load data:', errorMessage, error);
    this.#cache.status = 'error';
    this.#notify('error', errorMessage);
    return false;
  }
}
```

**Apply javascript Rule 1**: Provide specific error context in catch blocks.

### Timeout Pattern for Fetches (from javascript skill)

```javascript
async #fetchWithTimeout(url, timeout = 5_000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } finally {
    clearTimeout(timeoutId);
  }
}
```

**Apply javascript Rule 2**: Time-bound all async operations.

---

## Anti-Patterns (What NOT to Do)

❌ **Don't use localStorage** - Max 5-10MB, blocks main thread, no indexing
❌ **Don't store state in component fields** - Lost on navigation/refresh
❌ **Don't access IDB from components** - Bypasses State Manager, breaks reactivity
❌ **Don't forget `await ready()`** - Cache is null before init completes
❌ **Don't mutate cache without persisting** - Changes lost on refresh
❌ **Don't use nested transactions for simple ops** - Single-store operations don't need transactions

---

## Migration and Versioning

**Schema Migration**: Increment `DB_VERSION`, check `oldVersion` in upgrade callback:
```javascript
upgrade(db, oldVersion) {
  if (oldVersion < 2) {
    const store = transaction.objectStore(STORE_NAME);
    if (!store.indexNames.contains('category')) {
      store.createIndex('category', 'category', { unique: false });
    }
  }
}
```

**Data Migration**: Iterate records in upgrade, add missing fields with defaults. Test thoroughly—migrations run once per user.

---

## Quick Reference: Adding a New Feature with IDB

### Checklist

1. **Define data model** (JSDoc typedefs for all entities)
2. **Define DEFAULT state** (complete structure with sensible values)
3. **Choose pattern**:
   - Simple key-value? → Use StateStore directly
   - Collection with queries? → Create specialized store with indexes
   - Complex state with navigation? → Create State Manager class
4. **Implement CRUD** (get, set, update, delete, clear)
5. **Add persistence triggers** (call persist after mutations)
6. **Implement reset** (clear → defaults → persist)
7. **Export singleton** (if using State Manager)
8. **Integrate with components**:
   - `await manager.ready()` in connectedCallback
   - Subscribe via `onChange()`
   - Clean up in disconnectedCallback
9. **Test lifecycle**:
   - Fresh state (no IDB data)
   - Existing state (reload page)
   - Reset flow
   - Navigation persistence

---

## Common Pitfalls

1. **Forgot `await ready()`** → Cache is null, methods fail
2. **Shallow merge loses nested objects** → Explicitly check nested fields after merge
3. **No cleanup in disconnectedCallback** → Memory leaks from subscriptions
4. **Direct cache mutation without persist** → Changes lost on refresh
5. **Using getAll() on large collections** → Use cursors for pagination
6. **Not handling IDB errors** → Quota exceeded, corrupted DB crashes app
7. **Storing functions/classes** → IDB only supports structured cloneable data

---

## Related Skills

- **`javascript`**: Error handling (Rule 1), timeouts (Rule 2), cleanup (Rule 4)
- **`web-components`**: Component lifecycle, event-driven updates, attribute patterns
- **`js-micro-utilities`**: Use `debounce` from utilities if implementing debounced persistence

---

## Reference: Current Project Stores

### StateStore (Generic KV)
- **File**: `js/services/StateStore.js`
- **DB**: `fantasy-phonics-db`
- **Store**: `state` (single object store, no keyPath)
- **Usage**: Game state, practice mode state, word progress

### StoryStore (Specialized)
- **File**: `js/services/StoryStore.js`
- **DB**: `fantasy-phonics-stories`
- **Store**: `stories` (keyPath: `id`)
- **Indexes**: `wordSeq`, `createdAt`
- **Usage**: Saved story versions

### PracticeProgressStore (Specialized)
- **File**: `js/services/PracticeProgressStore.js`
- **DB**: `fantasy-phonics-practice`
- **Stores**: `progress`, `sessions`, `achievements`, `phoneme_mastery`
- **Indexes**: Various per store
- **Usage**: Practice mode analytics and progress tracking

### State Managers
- **GameStateManager**: Wraps StateStore, manages 28-word progression
- **PracticeStateManager**: Wraps StateStore, manages tier/word navigation
- **WordProgressManager**: Wraps StateStore, tracks phase completion
