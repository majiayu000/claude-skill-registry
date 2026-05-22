---
name: javascript-ember
description: Expert-level Ember.js development. Use when asked to (1) write Ember.js applications with components, services, routes, or controllers, (2) implement Ember Data models and adapters, (3) work with Ember Octane patterns (Glimmer components, tracked properties, modifiers), (4) optimize Ember application performance, (5) write Ember tests with QUnit or testing-library, or when phrases like "Ember component", "Ember route", "Glimmer", "tracked property", "Ember addon" appear.
---

# Expert Ember.js Development

Write modern, performant Ember.js applications following Ember Octane conventions and current best practices.

## Critical First Step: Use context7 MCP

**ALWAYS use context7 MCP before writing or editing ANY Ember code** - Before generating, modifying, or reviewing any Ember code, you MUST use the context7 MCP to check for relevant documentation. Context7 provides project-specific conventions, architectural patterns, coding standards, and technical decisions that override these general guidelines.

### When to Use context7

Use context7 MCP in these situations:
- Before writing any new Ember component, route, service, or model
- Before modifying existing Ember code
- When implementing features that might have project-specific patterns
- When unsure about architectural decisions
- Before suggesting refactors or improvements

### How to Use context7

```javascript
// Example: Check for Ember component patterns before creating a component
// Use the context7 MCP to search for relevant documentation
// Query examples:
// - "ember component patterns"
// - "ember routing conventions" 
// - "ember data models"
// - "ember testing standards"
// - "glimmer component lifecycle"

// Apply the documentation from context7 to your implementation
```

**If context7 returns relevant documentation, follow it EXACTLY even if it conflicts with this skill's general guidance.** Project-specific conventions always take precedence.

## Core Principles

1. **Embrace Ember Octane** - Use Glimmer components, tracked properties, and native classes
2. **Convention over configuration** - Follow Ember's resolver patterns and file structure
3. **Use the platform** - Prefer native JavaScript features over framework-specific abstractions when possible
4. **Composition through services and modifiers** - Extract reusable logic into services and UI behavior into modifiers
5. **Data down, actions up (DDAU)** - Maintain clear data flow patterns

## Context7 MCP Workflow

Before implementing any Ember code, follow this workflow:

1. **Query context7** - Search for relevant documentation using specific terms:
   - Component type (e.g., "ember glimmer component")
   - Feature area (e.g., "ember routing", "ember data")
   - Specific pattern (e.g., "form validation", "authentication")

2. **Review results** - Read any returned documentation carefully
   - Note project-specific naming conventions
   - Identify required patterns or abstractions
   - Check for mandatory testing requirements
   - Look for deprecated approaches to avoid

3. **Apply documentation** - Implement code following context7 guidance
   - Use project-specific utilities and helpers
   - Follow established architectural patterns
   - Match existing code style and structure
   - Include required metadata or annotations

4. **Fall back to general patterns** - If context7 has no relevant docs, use this skill's patterns
   - Apply standard Ember Octane conventions
   - Follow community best practices
   - Use examples from this skill as templates

**Remember: context7 documentation always overrides this skill's general guidance.**

### Context7 Query Examples

When implementing different types of Ember code, use these query patterns:

**For Components:**
```
- "ember component patterns"
- "ember component architecture"
- "glimmer component conventions"
- "[specific component type]" (e.g., "button component", "form component")
- "component props" or "component arguments"
- "component lifecycle"
- "component testing"
```

**For Routes:**
```
- "ember routing patterns"
- "ember route conventions"
- "route data loading"
- "route guards" or "route authentication"
- "nested routes"
- "query parameters"
```

**For Ember Data:**
```
- "ember data models"
- "ember data adapters"
- "ember data serializers"
- "api integration"
- "data relationships"
- "data layer patterns"
```

**For Services:**
```
- "ember services"
- "service patterns"
- "shared state management"
- "[specific service]" (e.g., "authentication service", "api service")
```

**For Testing:**
```
- "ember testing"
- "component testing"
- "integration tests"
- "acceptance tests"
- "test patterns"
- "test data" or "fixtures"
```

**For Styling:**
```
- "ember styling"
- "css conventions"
- "component styles"
- "tailwind" or "[css framework]"
```

**When Editing Existing Code:**
```
- Search for the specific feature: "user profile", "login form", etc.
- Search for the pattern you're implementing: "form validation", "dropdown menu"
- Search for utilities you might need: "validation utilities", "date helpers"
```

## Modern Ember Patterns (Octane+)

### Glimmer Components

```javascript
// app/components/user-profile.js
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class UserProfileComponent extends Component {
  @service currentUser;
  @service router;
  
  @tracked isEditing = false;
  @tracked formData = null;

  constructor(owner, args) {
    super(owner, args);
    // Use constructor for one-time setup
    this.formData = { ...this.args.user };
  }

  @action
  toggleEdit() {
    this.isEditing = !this.isEditing;
    if (this.isEditing) {
      this.formData = { ...this.args.user };
    }
  }

  @action
  async saveUser(event) {
    event.preventDefault();
    
    try {
      await this.args.onSave(this.formData);
      this.isEditing = false;
    } catch (error) {
      // Handle error
      console.error('Save failed:', error);
    }
  }

  @action
  updateField(field, event) {
    this.formData = {
      ...this.formData,
      [field]: event.target.value
    };
  }
}
```

```handlebars
{{! app/components/user-profile.hbs }}
<div class="user-profile">
  {{#if this.isEditing}}
    <form {{on "submit" this.saveUser}}>
      <label>
        Name:
        <input 
          type="text" 
          value={{this.formData.name}}
          {{on "input" (fn this.updateField "name")}}
        />
      </label>
      
      <label>
        Email:
        <input 
          type="email" 
          value={{this.formData.email}}
          {{on "input" (fn this.updateField "email")}}
        />
      </label>
      
      <button type="submit">Save</button>
      <button type="button" {{on "click" this.toggleEdit}}>Cancel</button>
    </form>
  {{else}}
    <div class="profile-display">
      <h2>{{@user.name}}</h2>
      <p>{{@user.email}}</p>
      
      {{#if this.currentUser.canEdit}}
        <button {{on "click" this.toggleEdit}}>Edit Profile</button>
      {{/if}}
    </div>
  {{/if}}
</div>
```

### Tracked Properties and Getters

```javascript
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { cached } from '@glimmer/tracking';

export default class DataGridComponent extends Component {
  @tracked sortColumn = 'name';
  @tracked sortDirection = 'asc';
  @tracked filterText = '';

  // Use @cached for expensive computations that depend on tracked properties
  @cached
  get filteredData() {
    const { filterText } = this;
    if (!filterText) return this.args.data;
    
    const lower = filterText.toLowerCase();
    return this.args.data.filter(item => 
      item.name.toLowerCase().includes(lower) ||
      item.email.toLowerCase().includes(lower)
    );
  }

  @cached
  get sortedData() {
    const data = [...this.filteredData];
    const { sortColumn, sortDirection } = this;
    
    return data.sort((a, b) => {
      const aVal = a[sortColumn];
      const bVal = b[sortColumn];
      const result = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
      return sortDirection === 'asc' ? result : -result;
    });
  }
}
```

### Services

```javascript
// app/services/notification.js
import Service from '@ember/service';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';

export default class NotificationService extends Service {
  @tracked notifications = [];
  
  @action
  add(message, type = 'info', duration = 5000) {
    const id = Date.now() + Math.random();
    const notification = { id, message, type };
    
    this.notifications = [...this.notifications, notification];
    
    if (duration > 0) {
      setTimeout(() => this.remove(id), duration);
    }
    
    return id;
  }
  
  @action
  remove(id) {
    this.notifications = this.notifications.filter(n => n.id !== id);
  }
  
  @action
  success(message, duration) {
    return this.add(message, 'success', duration);
  }
  
  @action
  error(message, duration = 10000) {
    return this.add(message, 'error', duration);
  }
  
  @action
  clear() {
    this.notifications = [];
  }
}
```

### Custom Modifiers

```javascript
// app/modifiers/click-outside.js
import { modifier } from 'ember-modifier';

export default modifier((element, [callback]) => {
  function handleClick(event) {
    if (!element.contains(event.target)) {
      callback(event);
    }
  }
  
  document.addEventListener('click', handleClick, true);
  
  return () => {
    document.removeEventListener('click', handleClick, true);
  };
});
```

```handlebars
{{! Usage }}
<div {{click-outside this.closeDropdown}} class="dropdown">
  {{! dropdown content }}
</div>
```

## Routing

### Route Definitions

```javascript
// app/router.js
import EmberRouter from '@ember/routing/router';
import config from 'my-app/config/environment';

export default class Router extends EmberRouter {
  location = config.locationType;
  rootURL = config.rootURL;
}

Router.map(function () {
  this.route('dashboard', { path: '/' });
  
  this.route('users', function () {
    this.route('index', { path: '/' });
    this.route('new');
    this.route('user', { path: '/:user_id' }, function () {
      this.route('edit');
      this.route('settings');
    });
  });
  
  this.route('not-found', { path: '/*path' });
});
```

### Route Class

```javascript
// app/routes/users/user.js
import Route from '@ember/routing/route';
import { inject as service } from '@ember/service';

export default class UsersUserRoute extends Route {
  @service store;
  @service router;

  async model(params) {
    try {
      return await this.store.findRecord('user', params.user_id, {
        include: 'profile,settings'
      });
    } catch (error) {
      if (error.errors?.[0]?.status === '404') {
        this.router.transitionTo('not-found');
      }
      throw error;
    }
  }

  // Redirect if user doesn't have permission
  afterModel(model) {
    if (!this.currentUser.canViewUser(model)) {
      this.router.transitionTo('dashboard');
    }
  }

  // Reset controller state on exit
  resetController(controller, isExiting) {
    if (isExiting) {
      controller.setProperties({
        queryParams: {},
        isEditing: false
      });
    }
  }
}
```

### Loading and Error States

```javascript
// app/routes/users/user/loading.js
import Route from '@ember/routing/route';

export default class UsersUserLoadingRoute extends Route {}
```

```handlebars
{{! app/templates/users/user/loading.hbs }}
<div class="loading-spinner">
  <p>Loading user...</p>
</div>
```

## Ember Data

### Models

```javascript
// app/models/user.js
import Model, { attr, hasMany, belongsTo } from '@ember-data/model';

export default class UserModel extends Model {
  @attr('string') name;
  @attr('string') email;
  @attr('date') createdAt;
  @attr('boolean', { defaultValue: true }) isActive;
  @attr('number') loginCount;
  
  @belongsTo('profile', { async: true, inverse: 'user' }) profile;
  @hasMany('post', { async: true, inverse: 'author' }) posts;
  
  // Computed properties still work but use native getters
  get displayName() {
    return this.name || this.email?.split('@')[0] || 'Anonymous';
  }
  
  get isNewUser() {
    const daysSinceCreation = (Date.now() - this.createdAt) / (1000 * 60 * 60 * 24);
    return daysSinceCreation < 7;
  }
}
```

### Custom Adapters

```javascript
// app/adapters/application.js
import JSONAPIAdapter from '@ember-data/adapter/json-api';
import { inject as service } from '@ember/service';

export default class ApplicationAdapter extends JSONAPIAdapter {
  @service session;
  
  host = 'https://api.example.com';
  namespace = 'v1';

  get headers() {
    const headers = {};
    
    if (this.session.isAuthenticated) {
      headers['Authorization'] = `Bearer ${this.session.data.authenticated.token}`;
    }
    
    return headers;
  }

  handleResponse(status, headers, payload, requestData) {
    if (status === 401) {
      this.session.invalidate();
    }
    
    return super.handleResponse(status, headers, payload, requestData);
  }
}
```

### Custom Serializers

```javascript
// app/serializers/application.js
import JSONAPISerializer from '@ember-data/serializer/json-api';

export default class ApplicationSerializer extends JSONAPISerializer {
  // Normalize date strings to Date objects
  normalizeDateFields(hash) {
    const dateFields = ['createdAt', 'updatedAt', 'publishedAt'];
    
    dateFields.forEach(field => {
      if (hash[field]) {
        hash[field] = new Date(hash[field]);
      }
    });
    
    return hash;
  }

  normalize(modelClass, resourceHash) {
    this.normalizeDateFields(resourceHash.attributes || {});
    return super.normalize(modelClass, resourceHash);
  }
}
```

## Testing

### Component Integration Tests

```javascript
// tests/integration/components/user-profile-test.js
import { module, test } from 'qunit';
import { setupRenderingTest } from 'ember-qunit';
import { render, click, fillIn } from '@ember/test-helpers';
import { hbs } from 'ember-cli-htmlbars';

module('Integration | Component | user-profile', function (hooks) {
  setupRenderingTest(hooks);

  test('it displays user information', async function (assert) {
    this.set('user', {
      name: 'Jane Doe',
      email: 'jane@example.com'
    });

    await render(hbs`<UserProfile @user={{this.user}} />`);

    assert.dom('h2').hasText('Jane Doe');
    assert.dom('p').hasText('jane@example.com');
  });

  test('it allows editing when canEdit is true', async function (assert) {
    this.owner.lookup('service:current-user').canEdit = true;
    this.set('user', {
      name: 'Jane Doe',
      email: 'jane@example.com'
    });
    this.set('onSave', () => {});

    await render(hbs`
      <UserProfile @user={{this.user}} @onSave={{this.onSave}} />
    `);

    await click('button:contains("Edit Profile")');
    
    assert.dom('form').exists();
    assert.dom('input[type="text"]').hasValue('Jane Doe');
    
    await fillIn('input[type="text"]', 'Jane Smith');
    await click('button[type="submit"]');
    
    assert.dom('form').doesNotExist();
  });
});
```

### Route/Acceptance Tests

```javascript
// tests/acceptance/user-flow-test.js
import { module, test } from 'qunit';
import { visit, currentURL, click, fillIn } from '@ember/test-helpers';
import { setupApplicationTest } from 'ember-qunit';
import { setupMirage } from 'ember-cli-mirage/test-support';

module('Acceptance | user flow', function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  test('visiting /users and creating a new user', async function (assert) {
    await visit('/users');
    
    assert.strictEqual(currentURL(), '/users');
    assert.dom('h1').hasText('Users');
    
    await click('a:contains("New User")');
    assert.strictEqual(currentURL(), '/users/new');
    
    await fillIn('[data-test-name-input]', 'John Doe');
    await fillIn('[data-test-email-input]', 'john@example.com');
    await click('[data-test-submit]');
    
    assert.strictEqual(currentURL(), '/users/1');
    assert.dom('[data-test-user-name]').hasText('John Doe');
  });
});
```

## Performance Optimization

See [references/performance.md](references/performance.md) for comprehensive optimization strategies.

### Quick Reference

| Problem | Solution |
|---------|----------|
| Unnecessary component re-renders | Use `@cached` for expensive getters |
| Large lists | Use `ember-collection` or virtual scrolling |
| Slow Ember Data queries | Optimize includes, use custom serializers |
| Bundle size | Use route-based code splitting, lazy engines |
| Memory leaks | Properly clean up in willDestroy, cancel timers |

### Critical Anti-patterns

```javascript
// ❌ Mutating tracked properties directly
this.items.push(newItem); // Won't trigger reactivity

// ✅ Replace the entire array
this.items = [...this.items, newItem];

// ❌ Creating new functions in templates
{{on "click" (fn this.handleClick item)}}

// ✅ Use actions or stable references
@action handleItemClick(item) { /* ... */ }
{{on "click" (fn this.handleItemClick item)}}

// ❌ Not using @cached for expensive computations
get expensiveComputation() {
  return this.data.filter(/* complex logic */);
}

// ✅ Use @cached
@cached
get expensiveComputation() {
  return this.data.filter(/* complex logic */);
}
```

## Project Structure

```
app/
├── components/           # Glimmer components
│   └── user-profile/
│       ├── component.js
│       ├── index.hbs
│       └── styles.css
├── controllers/          # Controllers (use sparingly in Octane)
├── helpers/             # Template helpers
├── modifiers/           # Custom modifiers
├── models/              # Ember Data models
├── routes/              # Route classes
├── services/            # Services
├── templates/           # Route templates
├── adapters/            # Ember Data adapters
├── serializers/         # Ember Data serializers
├── styles/              # Global styles
└── app.js

tests/
├── integration/         # Component tests
├── unit/               # Unit tests (models, services, etc.)
└── acceptance/         # Full application tests
```

## Tooling Recommendations

| Category | Tool | Notes |
|----------|------|-------|
| CLI | ember-cli | Official tooling |
| Testing | QUnit + ember-qunit | Built-in, well integrated |
| Linting | ESLint + ember-template-lint | Catch template issues |
| Formatting | Prettier | Use with ember-template-lint |
| Mocking | ember-cli-mirage | API mocking for tests |
| State management | Services + tracked | Built-in, no extra deps |
| HTTP | fetch or ember-fetch | Native or polyfilled |

## Common Patterns

### Form Handling with Validation

```javascript
// app/components/registration-form.js
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import { inject as service } from '@ember/service';

export default class RegistrationFormComponent extends Component {
  @service notification;
  
  @tracked email = '';
  @tracked password = '';
  @tracked confirmPassword = '';
  @tracked errors = {};
  @tracked isSubmitting = false;

  get isValid() {
    return (
      this.email &&
      this.password.length >= 8 &&
      this.password === this.confirmPassword &&
      Object.keys(this.errors).length === 0
    );
  }

  @action
  updateEmail(event) {
    this.email = event.target.value;
    this.validateEmail();
  }

  @action
  updatePassword(event) {
    this.password = event.target.value;
    this.validatePassword();
  }

  @action
  updateConfirmPassword(event) {
    this.confirmPassword = event.target.value;
    this.validateConfirmPassword();
  }

  validateEmail() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!this.email) {
      this.errors = { ...this.errors, email: 'Email is required' };
    } else if (!emailRegex.test(this.email)) {
      this.errors = { ...this.errors, email: 'Invalid email format' };
    } else {
      const { email, ...rest } = this.errors;
      this.errors = rest;
    }
  }

  validatePassword() {
    if (this.password.length < 8) {
      this.errors = { ...this.errors, password: 'Password must be at least 8 characters' };
    } else {
      const { password, ...rest } = this.errors;
      this.errors = rest;
    }
    
    // Re-validate confirm password if it's filled
    if (this.confirmPassword) {
      this.validateConfirmPassword();
    }
  }

  validateConfirmPassword() {
    if (this.password !== this.confirmPassword) {
      this.errors = { ...this.errors, confirmPassword: 'Passwords do not match' };
    } else {
      const { confirmPassword, ...rest } = this.errors;
      this.errors = rest;
    }
  }

  @action
  async submit(event) {
    event.preventDefault();
    
    if (!this.isValid) return;
    
    this.isSubmitting = true;
    
    try {
      await this.args.onSubmit({
        email: this.email,
        password: this.password
      });
      
      this.notification.success('Registration successful!');
    } catch (error) {
      this.notification.error(error.message || 'Registration failed');
    } finally {
      this.isSubmitting = false;
    }
  }
}
```

### Infinite Scroll with Modifier

```javascript
// app/modifiers/infinite-scroll.js
import { modifier } from 'ember-modifier';

export default modifier((element, [callback], { threshold = 200 }) => {
  let isLoading = false;
  
  function handleScroll() {
    if (isLoading) return;
    
    const { scrollTop, scrollHeight, clientHeight } = element;
    const distanceFromBottom = scrollHeight - (scrollTop + clientHeight);
    
    if (distanceFromBottom < threshold) {
      isLoading = true;
      callback().finally(() => {
        isLoading = false;
      });
    }
  }
  
  element.addEventListener('scroll', handleScroll, { passive: true });
  
  return () => {
    element.removeEventListener('scroll', handleScroll);
  };
});
```

## TypeScript Support

Ember has strong TypeScript support. Enable it with:

```bash
ember install ember-cli-typescript
```

```typescript
// app/components/user-profile.ts
import Component from '@glimmer/component';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';
import type { TOC } from '@ember/component/template-only';

interface UserProfileArgs {
  user: {
    name: string;
    email: string;
    avatarUrl?: string;
  };
  onSave: (data: UserData) => Promise<void>;
  canEdit?: boolean;
}

interface UserData {
  name: string;
  email: string;
}

export default class UserProfileComponent extends Component<UserProfileArgs> {
  @tracked isEditing = false;
  @tracked formData: UserData | null = null;

  @action
  async saveUser(event: SubmitEvent): Promise<void> {
    event.preventDefault();
    
    if (!this.formData) return;
    
    await this.args.onSave(this.formData);
    this.isEditing = false;
  }
}

// Template-only component signature
export interface GreetingSignature {
  Element: HTMLDivElement;
  Args: {
    name: string;
  };
}

const Greeting: TOC<GreetingSignature> = <template>
  <div ...attributes>Hello {{@name}}!</div>
</template>;

export default Greeting;
```

## Remember: Always Use context7 MCP First!

Before implementing any Ember code, query the context7 MCP for relevant project documentation. Context7 provides project-specific guidelines that always supersede these general best practices.

### Quick context7 Query Guide

**Before writing components:**
- Query: "ember component patterns", "glimmer component", "component architecture"

**Before routing work:**
- Query: "ember routing", "route patterns", "navigation"

**Before Ember Data:**
- Query: "ember data models", "api integration", "data layer"

**Before tests:**
- Query: "ember testing", "test patterns", "test requirements"

**When editing existing code:**
- Query the specific feature or pattern you're working with

The context7 MCP is your source of truth for this project's Ember conventions.
