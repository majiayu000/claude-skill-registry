---
name: patterns
description: JavaScript design patterns and architectural best practices.
sasmp_version: "1.3.0"
bonded_agent: 06-modern-es6-advanced
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [pattern_type]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: show_common_patterns

observability:
  entry_log: "Patterns skill activated"
  exit_log: "Patterns reference provided"
---

# JavaScript Patterns Skill

## Quick Reference Card

### Creational Patterns

**Factory**
```javascript
function createUser(type) {
  const users = {
    admin: () => ({ role: 'admin', permissions: ['all'] }),
    user: () => ({ role: 'user', permissions: ['read'] })
  };
  return users[type]?.() ?? users.user();
}
```

**Singleton**
```javascript
class Database {
  static #instance;

  static getInstance() {
    if (!Database.#instance) {
      Database.#instance = new Database();
    }
    return Database.#instance;
  }
}
```

**Builder**
```javascript
class QueryBuilder {
  #query = { select: '*', from: '', where: [] };

  select(fields) { this.#query.select = fields; return this; }
  from(table) { this.#query.from = table; return this; }
  where(condition) { this.#query.where.push(condition); return this; }
  build() { return this.#query; }
}

new QueryBuilder()
  .select('name, email')
  .from('users')
  .where('active = true')
  .build();
```

### Structural Patterns

**Module**
```javascript
const Counter = (function() {
  let count = 0; // Private

  return {
    increment: () => ++count,
    decrement: () => --count,
    get: () => count
  };
})();
```

**Facade**
```javascript
class ApiClient {
  async getUser(id) {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error('Failed');
    return response.json();
  }

  async updateUser(id, data) {
    return this.#request('PUT', `/api/users/${id}`, data);
  }

  #request(method, url, data) {
    return fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(r => r.json());
  }
}
```

**Decorator**
```javascript
function withLogging(fn) {
  return function(...args) {
    console.log('Calling:', fn.name, args);
    const result = fn.apply(this, args);
    console.log('Result:', result);
    return result;
  };
}

const add = withLogging((a, b) => a + b);
```

### Behavioral Patterns

**Observer (Pub/Sub)**
```javascript
class EventEmitter {
  #events = new Map();

  on(event, handler) {
    if (!this.#events.has(event)) this.#events.set(event, []);
    this.#events.get(event).push(handler);
    return () => this.off(event, handler);
  }

  off(event, handler) {
    const handlers = this.#events.get(event) ?? [];
    this.#events.set(event, handlers.filter(h => h !== handler));
  }

  emit(event, data) {
    (this.#events.get(event) ?? []).forEach(h => h(data));
  }
}
```

**Strategy**
```javascript
const validators = {
  email: (v) => /\S+@\S+/.test(v),
  phone: (v) => /^\d{10}$/.test(v),
  required: (v) => v?.trim().length > 0
};

function validate(value, rules) {
  return rules.every(rule => validators[rule]?.(value) ?? true);
}

validate('test@test.com', ['required', 'email']); // true
```

**Command**
```javascript
class CommandManager {
  #history = [];
  #index = -1;

  execute(command) {
    command.execute();
    this.#history = this.#history.slice(0, this.#index + 1);
    this.#history.push(command);
    this.#index++;
  }

  undo() {
    if (this.#index >= 0) {
      this.#history[this.#index--].undo();
    }
  }

  redo() {
    if (this.#index < this.#history.length - 1) {
      this.#history[++this.#index].execute();
    }
  }
}
```

### Modern Patterns

**Composition**
```javascript
const withLogger = (obj) => ({
  ...obj,
  log: (msg) => console.log(`[${obj.name}] ${msg}`)
});

const withValidator = (obj) => ({
  ...obj,
  validate: () => !!obj.value
});

const field = withValidator(withLogger({ name: 'email', value: '' }));
```

**Middleware**
```javascript
function createPipeline(...middlewares) {
  return (input) => middlewares.reduce(
    (acc, fn) => fn(acc),
    input
  );
}

const process = createPipeline(
  (x) => x.trim(),
  (x) => x.toLowerCase(),
  (x) => x.replace(/\s+/g, '-')
);

process('  Hello World  '); // 'hello-world'
```

## Troubleshooting

### When to Use

| Pattern | Use When |
|---------|----------|
| Factory | Multiple similar objects |
| Singleton | Single shared instance |
| Observer | Event-driven communication |
| Strategy | Swappable algorithms |
| Facade | Complex subsystem |

### Anti-Patterns to Avoid

- God objects (do everything)
- Tight coupling
- Callback hell
- Magic numbers/strings
- Premature optimization

## Related

- **Agent 06**: Modern ES6+ (detailed learning)
- **Skill: functions**: Function patterns
- **Skill: modern-javascript**: Classes
