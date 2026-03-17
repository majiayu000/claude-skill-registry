---
name: clean-code
description: Clean code principles for readable, maintainable software
---

# Clean Code Principles

Write code that humans can understand. Code is read far more often than it's written.

## Naming

### Variables
```typescript
// BAD
const d = 86400000; // what is this?
const yyyymmdd = formatDate(date);
const list = getUsers();

// GOOD
const MILLISECONDS_PER_DAY = 86400000;
const formattedDate = formatDate(date);
const users = getUsers();
```

### Functions
```typescript
// BAD - unclear what it does
function handle(data) { }
function process(item) { }
function doIt() { }

// GOOD - verb + noun, describes action
function validateUserInput(input) { }
function calculateTotalPrice(items) { }
function sendWelcomeEmail(user) { }
```

### Booleans
```typescript
// BAD
const open = true;
const write = false;
const fruit = true;

// GOOD - is/has/can/should prefix
const isOpen = true;
const canWrite = false;
const hasFruit = true;
```

## Functions

### Single Responsibility
```typescript
// BAD - does too much
function createUserAndSendEmailAndLogActivity(data) {
  const user = db.insert(data);
  mailer.send(user.email, 'Welcome!');
  logger.log(`User ${user.id} created`);
  return user;
}

// GOOD - one thing each
function createUser(data) {
  return db.insert(data);
}

function sendWelcomeEmail(user) {
  mailer.send(user.email, 'Welcome!');
}

function logUserCreation(user) {
  logger.log(`User ${user.id} created`);
}
```

### Few Parameters
```typescript
// BAD - too many parameters
function createUser(name, email, age, country, role, department, manager) { }

// GOOD - use object
function createUser(options: CreateUserOptions) { }

interface CreateUserOptions {
  name: string;
  email: string;
  age?: number;
  country?: string;
  role: Role;
  department?: string;
  manager?: string;
}
```

### Avoid Flag Arguments
```typescript
// BAD - boolean changes behavior
function createFile(name: string, temp: boolean) {
  if (temp) {
    fs.create(`/tmp/${name}`);
  } else {
    fs.create(name);
  }
}

// GOOD - separate functions
function createFile(name: string) {
  fs.create(name);
}

function createTempFile(name: string) {
  fs.create(`/tmp/${name}`);
}
```

### Return Early
```typescript
// BAD - nested conditionals
function getPayAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = 0;
  } else {
    if (employee.isRetired) {
      result = employee.pension;
    } else {
      result = employee.salary;
    }
  }
  return result;
}

// GOOD - early returns
function getPayAmount(employee) {
  if (employee.isSeparated) return 0;
  if (employee.isRetired) return employee.pension;
  return employee.salary;
}
```

## Comments

### Don't Comment Bad Code - Rewrite It
```typescript
// BAD
// Check if employee is eligible for benefits
if ((employee.flags & 0x0F) && (employee.age > 65)) { }

// GOOD - code explains itself
const isEligibleForBenefits = employee.hasHealthPlan && employee.isRetired;
if (isEligibleForBenefits) { }
```

### Good Comments
```typescript
// Regex matches ISO 8601 date format
const DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;

// TODO: Refactor when API v2 launches
// WARNING: This must run before database migration
// NOTE: Third-party API has 100ms minimum delay
```

## Error Handling

### Don't Return Null
```typescript
// BAD
function getUser(id: string): User | null {
  return db.find(id) || null;
}

// GOOD - throw or return Result type
function getUser(id: string): User {
  const user = db.find(id);
  if (!user) throw new UserNotFoundError(id);
  return user;
}

// OR use Result type
function getUser(id: string): Result<User, NotFoundError> { }
```

### Don't Pass Null
```typescript
// BAD
function calculateArea(width: number | null, height: number | null) {
  if (width === null || height === null) {
    throw new Error('Invalid dimensions');
  }
  return width * height;
}

// GOOD - require valid inputs
function calculateArea(width: number, height: number) {
  return width * height;
}
```

## Formatting

### Consistent Style
- Pick a style guide (Prettier, StandardJS, Black)
- Automate with formatters
- Never debate style in code review

### Vertical Density
```typescript
// BAD - unrelated code together
const user = getUser(id);
const config = loadConfig();
const result = processData(user, config);
logger.log(result);
sendNotification(user);

// GOOD - group related code
const user = getUser(id);
sendNotification(user);

const config = loadConfig();
const result = processData(user, config);
logger.log(result);
```

## Code Smells to Avoid

| Smell | Problem | Solution |
|-------|---------|----------|
| Long Method | Hard to understand | Extract methods |
| Long Parameter List | Complex interface | Parameter object |
| Duplicate Code | Change in multiple places | Extract function |
| Dead Code | Confusion, maintenance | Delete it |
| Magic Numbers | Unclear meaning | Named constants |
| Deep Nesting | Hard to follow | Early returns, extract |
| Feature Envy | Wrong location | Move method |
| Data Clumps | Always together | Create class |

## The Boy Scout Rule

> Leave the code cleaner than you found it.

Every commit should improve code quality slightly. Small, incremental improvements compound over time.

## Checklist

Before committing, ask:

- [ ] Can I understand this code in 6 months?
- [ ] Would a new team member understand it?
- [ ] Are names descriptive and searchable?
- [ ] Does each function do one thing?
- [ ] Are there any magic numbers/strings?
- [ ] Is error handling appropriate?
- [ ] Did I remove all dead code?
