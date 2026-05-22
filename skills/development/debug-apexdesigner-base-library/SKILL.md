---
name: Debug
description: Conventions and tools for the `debug` npm package. Run tests with debug output.
allowed-tools:
  - Bash
---

# debug

Conventions for the `debug` npm package.

## Setup

```typescript
import createDebug from 'debug';

// Server: include app/library name
const Debug = createDebug('MyApp:ClassName');

// Client: class name only
const Debug = createDebug('ClassName');
```

## In Methods

```typescript
async processOrder(orderId: string, items: Item[]) {
  const debug = Debug.extend('processOrder');
  debug('orderId %j', orderId);
  debug('items.length %j', items.length);  // Don't log large arrays

  const result = await this.orderService.create(orderId, items);
  debug('result %j', result);

  return result;
}

// Extend again inside callbacks when needed
items.forEach((item, index) => {
  const cbDebug = debug.extend(`item-${index}`);
  cbDebug('processing %j', item);
});
```

## Rules

1. **Blank line after debug statements** - separates logging from logic
   ```typescript
   // Good
   debug('orderId %j', orderId);
   debug('items.length %j', items.length);

   const result = await this.process(orderId);
   debug('result %j', result);

   return result;

   // Bad - debug mixed with logic
   debug('orderId %j', orderId);
   const result = await this.process(orderId);
   debug('result %j', result);
   return result;
   ```

2. **One item per debug statement**
   ```typescript
   // Good
   debug('this.userId %j', this.userId);
   debug('this.token %j', this.token);

   // Bad
   debug('userId=%s token=%s', this.userId, this.token);
   ```

3. **Keep labels simple** - use variable name, not prose
   ```typescript
   // Good
   debug('order %j', order);

   // Bad
   debug('The current order is: %j', order);
   ```

4. **Label must match value** - no transformations
   ```typescript
   // Good - label matches value exactly
   debug('this.maxDate', this.maxDate);

   // Bad - label says maxDate but value is toISO() result
   debug('this.maxDate', this.maxDate.toISO());
   ```

5. **Prose-only for flow markers** - when there's no value to log
   ```typescript
   debug('initialized');
   debug('enter pressed');
   debug('no loader registered');
   ```

6. **Use %j for Server Side Only** (usually)
   ```typescript
   // Server: always use %j
   debug('config %j', config);

   // Client: don't use %j - browser console lets you inspect objects
   debug('config', config);

   // Exception: use %j client-side for timing issues where you need
   // to see object state at multiple points in time (otherwise you
   // only see the final state when you expand the object)
   ```

7. **Log length for arrays** - don't flood output
   ```typescript
   debug('users.length %j', users.length);
   ```

8. **Debug early returns** - so you can trace why execution stopped
   ```typescript
   if (!date) {
     debug('date %j', date);

     this.control.setValue(null);
     return;
   }
   ```

9. **Debug inputs and outputs** - trace execution flow
   ```typescript
   async getUser(id: string) {
     const debug = Debug.extend('getUser');
     debug('id %j', id);

     const user = await this.db.findUser(id);
     debug('user %j', user);

     return user;
   }
   ```

10. **Debug intermediate results** - after each method call
   ```typescript
   const user = await this.userService.getUser(id);
   debug('user %j', user);

   const permissions = await this.authService.getPermissions(user.role);
   debug('permissions %j', permissions);

   const filtered = permissions.filter(p => p.active);
   debug('filtered.length %j', filtered.length);
   ```

11. **Debug loop iterations** when needed
   ```typescript
   for (const item of items) {
     debug('item %j', item);
     // ... process item
   }
   ```

12. **Use console for always-on logging**
   ```typescript
   console.log('Server started on port', port);  // Always show
   console.error('Fatal error:', err);           // Always show
   debug('request %j', req);                     // Only when DEBUG enabled
   ```

## Enabling Debug Output

Server-side DEBUG strings can get long. Remember that wildcards work well:

```bash
# Full namespace
DEBUG=MyApp:OrderService:processOrder node app.js

# Wildcard - often sufficient
DEBUG=*processOrder node app.js
DEBUG=*Order* node app.js
```

## Running Tests with Debug

Use the debug-test script to run tests with DEBUG output:

```bash
# Run specific test file with debug output
bash .claude/skills/debug/scripts/debug-test.sh '*OrderService*' -- src/order.spec.ts

# Run test by name pattern
bash .claude/skills/debug/scripts/debug-test.sh '*processOrder*' -- -t "should process order"

# Run all tests in a directory with debug
bash .claude/skills/debug/scripts/debug-test.sh 'MyApp:*' -- src/services/
```

The script sets the DEBUG environment variable and passes remaining arguments to `npm test`.
