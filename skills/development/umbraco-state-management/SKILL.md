---
name: umbraco-state-management
description: Understand and use state management in Umbraco backoffice (foundational concept)
version: 1.0.0
location: managed
allowed-tools: Read, Write, Edit, WebFetch
---

# Umbraco State Management

## What is it?
States in Umbraco are containers for reactive values that enable communication across component instances using the Observable pattern. An Umbraco State is a container for a value that you can create Observables from, which allows multiple observers to subscribe and automatically receive updates when the state changes. This pattern is particularly useful for sharing data between contexts and elements without tight coupling.

## Documentation
Always fetch the latest docs before implementing:

- **Main docs**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/states
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Context API**: https://docs.umbraco.com/umbraco-cms/customizing/foundation/context-api

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above
2. **Ask questions** - What type of state? Who observes? Where to provide observable?
3. **Generate code** - Implement state with observables based on latest docs
4. **Explain** - Show what was created and how observation works

## Minimal Examples

### Basic State Usage
```typescript
import { UmbStringState } from '@umbraco-cms/backoffice/observable-api';

// Create a state with initial value
const myState = new UmbStringState('initial value');

// Create an observable from the state
const myObservable = myState.asObservable();

// Observe the state (fires immediately and on changes)
this.observe(myObservable, (value) => {
  console.log('Current value:', value);
});

// Update the state (all observers notified)
myState.setValue('updated value');
```

### State in Context Pattern
```typescript
import { UmbContextBase } from '@umbraco-cms/backoffice/class-api';
import { UmbNumberState } from '@umbraco-cms/backoffice/observable-api';

export class MyContext extends UmbContextBase<MyContext> {
  // Private state
  #counter = new UmbNumberState(0);

  // Public observable (readonly)
  readonly counter = this.#counter.asObservable();

  increment() {
    this.#counter.setValue(this.#counter.getValue() + 1);
  }

  decrement() {
    this.#counter.setValue(this.#counter.getValue() - 1);
  }
}
```

### Element Observing Context State
```typescript
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import { MY_CONTEXT } from './my-context.js';

export class MyElement extends UmbLitElement {
  @state()
  private _count = 0;

  constructor() {
    super();

    this.consumeContext(MY_CONTEXT, (context) => {
      // Observe the counter state from context
      this.observe(
        context.counter,
        (count) => {
          this._count = count;
        },
        '_countObserver'
      );
    });
  }

  render() {
    return html`
      <div>Count: ${this._count}</div>
    `;
  }
}
```

### Different State Types
```typescript
import {
  UmbStringState,
  UmbNumberState,
  UmbBooleanState,
  UmbArrayState,
  UmbObjectState
} from '@umbraco-cms/backoffice/observable-api';

// String state
const name = new UmbStringState('John');

// Number state
const age = new UmbNumberState(25);

// Boolean state
const isActive = new UmbBooleanState(true);

// Array state
const items = new UmbArrayState(['item1', 'item2']);

// Object state
const user = new UmbObjectState({ name: 'John', age: 25 });
```

### Observable Parts (Derived State)
```typescript
import { UmbArrayState } from '@umbraco-cms/backoffice/observable-api';

const itemsState = new UmbArrayState(['apple', 'banana', 'cherry']);

// Observe just the first item
const firstItem = itemsState.asObservablePart(data => data?.[0]);

// Observe just the count
const itemCount = itemsState.asObservablePart(data => data.length);

// Use in element
this.observe(firstItem, (first) => {
  console.log('First item:', first);
});

this.observe(itemCount, (count) => {
  console.log('Total items:', count);
});
```

### Array State Operations
```typescript
import { UmbArrayState } from '@umbraco-cms/backoffice/observable-api';

const listState = new UmbArrayState<string>([]);

// Add item
listState.setValue([...listState.getValue(), 'new item']);

// Remove item
listState.setValue(
  listState.getValue().filter(item => item !== 'old item')
);

// Clear all
listState.setValue([]);

// Get current value
const current = listState.getValue();
```

### Complete Context Example
```typescript
import { UmbContextBase } from '@umbraco-cms/backoffice/class-api';
import { UmbStringState, UmbArrayState } from '@umbraco-cms/backoffice/observable-api';

export class TodoContext extends UmbContextBase<TodoContext> {
  #title = new UmbStringState('My Todo List');
  #todos = new UmbArrayState<string>([]);

  readonly title = this.#title.asObservable();
  readonly todos = this.#todos.asObservable();
  readonly todoCount = this.#todos.asObservablePart(data => data.length);

  setTitle(value: string) {
    this.#title.setValue(value);
  }

  addTodo(todo: string) {
    this.#todos.setValue([...this.#todos.getValue(), todo]);
  }

  removeTodo(todo: string) {
    this.#todos.setValue(
      this.#todos.getValue().filter(t => t !== todo)
    );
  }
}
```

## Key Concepts

**State**: Container for a value (private, mutable)

**Observable**: Subscription hook created from state (public, readonly)

**Observer**: Function that reacts to state changes via `observe()`

**State Types**:
- `UmbStringState` - text values
- `UmbNumberState` - numeric values
- `UmbBooleanState` - boolean flags
- `UmbArrayState` - collections
- `UmbObjectState` - complex objects
- `UmbClassState` - class instances

**Observable Parts**: Derived observables that only update when mapped value changes

**Best Practice**: Keep states private, expose observables publicly

**Use Cases**:
- Sharing data between context and elements
- Reactive UI updates
- Cross-component communication
- Derived/computed values

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.
