---
name: web-testing-vue-test-utils
description: Vue Test Utils patterns - mount, shallowMount, wrapper API, trigger, setValue, flushPromises, testing composables, Pinia store mocking
---

# Vue Test Utils Patterns

> **Quick Guide:** Test Vue components with `mount()` for full rendering or `shallowMount()` for isolation. Use `wrapper.find()` with data-test attributes, `await trigger()` for events, `await setValue()` for inputs. Use `flushPromises()` for async operations. Mock Pinia stores with `createTestingPinia()`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST `await` all DOM-updating methods: `trigger()`, `setValue()`, `setProps()`, `setData()`)**

**(You MUST use `flushPromises()` after async operations that Vue doesn't track (API calls, timers))**

**(You MUST use `mount()` by default - only use `shallowMount()` for performance issues or complex isolation)**

**(You MUST use `data-test` attributes for selectors, NOT classes or IDs)**

**(You MUST use `createTestingPinia()` for Pinia stores, NOT manual mocking)**

</critical_requirements>

---

**Auto-detection:** Vue Test Utils, @vue/test-utils, mount, shallowMount, wrapper, VueWrapper, DOMWrapper, trigger, setValue, setProps, setData, flushPromises, findComponent, findAllComponents, createTestingPinia, @pinia/testing

**When to use:**

- Testing Vue 3 components with Composition API
- Testing component behavior through user interactions
- Testing components with Pinia stores
- Testing components with Vue Router
- Testing composables in isolation
- Mocking child components for isolation

**When NOT to use:**

- E2E testing spanning multiple pages (use Playwright)
- Testing pure utility functions without Vue (use unit tests directly)
- Visual regression testing (use visual testing tools)
- Test runner configuration (use Vitest skill)

**Key patterns covered:**

- Mounting components (mount vs shallowMount)
- Wrapper API (find, findAll, trigger, setValue)
- Async testing (flushPromises, nextTick)
- Testing composables
- Pinia store mocking with createTestingPinia
- Vue Router mocking
- Stubbing child components

**Detailed Resources:**

- For code examples, see `examples/` folder:
  - [examples/core.md](examples/core.md) - Mounting, wrapper API, queries
  - [examples/async.md](examples/async.md) - flushPromises, nextTick, async setup
  - [examples/composables.md](examples/composables.md) - Testing composables
  - [examples/mocking.md](examples/mocking.md) - Pinia stores, Vue Router, stubs
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Vue Test Utils provides utilities to mount Vue components in isolation and interact with them through the wrapper API. The guiding principle: "The more your tests resemble the way your software is used, the more confidence they can give you."

**Core Principles:**

1. **Test User Behavior, Not Implementation**: Test what users see and interact with, not internal component state
2. **Prefer Full Rendering**: Use `mount()` by default for realistic testing; `shallowMount()` only when needed
3. **Use Accessible Selectors**: Prefer `data-test` attributes over classes or IDs that may change
4. **Await Async Operations**: Vue updates the DOM asynchronously - always await DOM-updating methods
5. **Minimize Stubbing**: More stubs reduce test fidelity; stub only what's necessary

**When to use Vue Test Utils:**

- Component integration testing with child components
- Testing user interaction flows (clicks, input, form submission)
- Testing reactive state and computed properties
- Testing component lifecycle and watchers
- Testing components with Pinia or Vue Router

**When NOT to use:**

- Full user journey testing (use E2E tests)
- Testing visual appearance (use visual regression tools)
- Testing API endpoints directly (test component behavior with mocked responses)
- Testing third-party library behavior (trust the library's tests)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Mounting Components

Use `mount()` for full rendering with child components. Use `shallowMount()` only when you need isolation or have performance issues.

#### mount vs shallowMount

```typescript
import { mount, shallowMount } from "@vue/test-utils";
import { TodoList } from "./todo-list.vue";

// GOOD: mount() for realistic testing
const wrapper = mount(TodoList, {
  props: {
    todos: [{ id: 1, text: "Test", done: false }],
  },
});

// Use when: You need to test component with its children
// Child components render normally, slots work, events bubble up

// shallowMount() for isolation (use sparingly)
const shallowWrapper = shallowMount(TodoList, {
  props: {
    todos: [{ id: 1, text: "Test", done: false }],
  },
});

// Use when: Component has many heavy children, or you need complete isolation
// All child components are replaced with stubs
```

**Why mount by default:** `shallowMount` makes the component behave differently from production. Child components don't render, slots may not work correctly, and you lose integration coverage.

See [examples/core.md](examples/core.md) for complete mounting examples.

---

### Pattern 2: Wrapper API for Querying

Use `get()` when element must exist (throws on failure). Use `find()` when element may not exist (returns empty wrapper). Use `findAll()` for multiple elements.

#### Querying Elements

```typescript
import { mount } from "@vue/test-utils";
import { SearchForm } from "./search-form.vue";

const DATA_TEST_INPUT = '[data-test="search-input"]';
const DATA_TEST_BUTTON = '[data-test="search-button"]';
const DATA_TEST_RESULT = '[data-test="search-result"]';

test("renders search form elements", () => {
  const wrapper = mount(SearchForm);

  // get() - throws if not found (use for required elements)
  const input = wrapper.get(DATA_TEST_INPUT);
  const button = wrapper.get(DATA_TEST_BUTTON);

  expect(input.exists()).toBe(true);
  expect(button.text()).toBe("Search");
});

test("shows results after search", async () => {
  const wrapper = mount(SearchForm);

  // find() - returns empty wrapper if not found (use for conditional elements)
  expect(wrapper.find(DATA_TEST_RESULT).exists()).toBe(false);

  // After triggering search...
  await wrapper.get(DATA_TEST_INPUT).setValue("test");
  await wrapper.get(DATA_TEST_BUTTON).trigger("click");

  // findAll() - returns array of wrappers
  const results = wrapper.findAll(DATA_TEST_RESULT);
  expect(results.length).toBeGreaterThan(0);
});
```

**Why data-test attributes:** CSS classes and IDs change during styling updates. `data-test` attributes are explicit testing contracts that don't affect production styling.

---

### Pattern 3: User Interactions with trigger and setValue

Always `await` DOM-updating methods. They return a Promise that resolves after Vue updates the DOM.

#### Form Interactions

```typescript
import { mount } from "@vue/test-utils";
import { LoginForm } from "./login-form.vue";

const DATA_TEST_EMAIL = '[data-test="email-input"]';
const DATA_TEST_PASSWORD = '[data-test="password-input"]';
const DATA_TEST_FORM = '[data-test="login-form"]';
const DATA_TEST_ERROR = '[data-test="error-message"]';

const VALID_EMAIL = "test@example.com";
const VALID_PASSWORD = "password123";

test("submits login form", async () => {
  const wrapper = mount(LoginForm);

  // setValue() for input values - MUST await
  await wrapper.get(DATA_TEST_EMAIL).setValue(VALID_EMAIL);
  await wrapper.get(DATA_TEST_PASSWORD).setValue(VALID_PASSWORD);

  // trigger() for events - MUST await
  await wrapper.get(DATA_TEST_FORM).trigger("submit.prevent");

  // Assert emitted events
  expect(wrapper.emitted("submit")).toBeTruthy();
  expect(wrapper.emitted("submit")![0]).toEqual([
    { email: VALID_EMAIL, password: VALID_PASSWORD },
  ]);
});

test("shows validation errors", async () => {
  const wrapper = mount(LoginForm);

  // Submit empty form
  await wrapper.get(DATA_TEST_FORM).trigger("submit.prevent");

  // Check for error message
  expect(wrapper.get(DATA_TEST_ERROR).text()).toContain("Email is required");
});
```

**Why await:** Vue updates the DOM asynchronously. Without `await`, assertions run before Vue finishes updating, causing flaky tests.

---

### Pattern 4: Async Operations with flushPromises

Use `flushPromises()` after async operations that Vue doesn't track (API calls, setTimeout, etc.). Use `nextTick()` only for reactive state updates.

#### Testing Async API Calls

```typescript
import { mount, flushPromises } from "@vue/test-utils";
import { UserProfile } from "./user-profile.vue";
import { vi } from "vitest";

const DATA_TEST_LOADING = '[data-test="loading"]';
const DATA_TEST_NAME = '[data-test="user-name"]';
const DATA_TEST_ERROR = '[data-test="error"]';

const MOCK_USER = { id: 1, name: "John Doe" };

// Mock API module
vi.mock("@/api/users", () => ({
  fetchUser: vi.fn(),
}));

import { fetchUser } from "@/api/users";

test("displays user data after loading", async () => {
  // Arrange: Setup mock to resolve
  vi.mocked(fetchUser).mockResolvedValue(MOCK_USER);

  const wrapper = mount(UserProfile, {
    props: { userId: 1 },
  });

  // Initially shows loading
  expect(wrapper.find(DATA_TEST_LOADING).exists()).toBe(true);

  // Act: Wait for all promises to resolve
  await flushPromises();

  // Assert: Loading gone, data displayed
  expect(wrapper.find(DATA_TEST_LOADING).exists()).toBe(false);
  expect(wrapper.get(DATA_TEST_NAME).text()).toBe("John Doe");
});

test("displays error on API failure", async () => {
  // Arrange: Setup mock to reject
  vi.mocked(fetchUser).mockRejectedValue(new Error("Network error"));

  const wrapper = mount(UserProfile, {
    props: { userId: 1 },
  });

  // Act: Wait for promise to reject
  await flushPromises();

  // Assert: Error displayed
  expect(wrapper.get(DATA_TEST_ERROR).text()).toContain("Network error");
});
```

**Why flushPromises:** Vue's reactivity system doesn't track external promises (HTTP requests, timers). `flushPromises()` resolves all pending promises so the DOM reflects the async result.

See [examples/async.md](examples/async.md) for complete async testing examples.

---

### Pattern 5: Testing Components with findComponent/getComponent

Use `findComponent()` or `getComponent()` to interact with child Vue components directly. Useful for testing component communication.

- **`getComponent()`** - Throws error if not found (use when component **must** exist)
- **`findComponent()`** - Returns empty wrapper if not found (use when component **may not** exist)

#### Component Queries

```typescript
import { mount } from "@vue/test-utils";
import { ParentComponent } from "./parent-component.vue";
import { ChildComponent } from "./child-component.vue";

test("passes props to child component", () => {
  const wrapper = mount(ParentComponent, {
    props: { message: "Hello" },
  });

  // getComponent() - throws if not found (clearer error messages)
  const child = wrapper.getComponent(ChildComponent);

  // Assert props passed correctly
  expect(child.props("message")).toBe("Hello");
});

test("receives emitted events from child", async () => {
  const wrapper = mount(ParentComponent);
  const child = wrapper.getComponent(ChildComponent);

  // Trigger event on child
  await child.vm.$emit("update", "new value");

  // Assert parent handled the event
  expect(wrapper.vm.value).toBe("new value");
});

test("conditionally rendered child component", () => {
  const wrapper = mount(ParentComponent, {
    props: { showChild: false },
  });

  // findComponent() - returns empty wrapper (check with .exists())
  const child = wrapper.findComponent(ChildComponent);

  expect(child.exists()).toBe(false);
});

test("finds component by name", () => {
  const wrapper = mount(ParentComponent);

  // Find by component name (less preferred - use component definition)
  const child = wrapper.findComponent({ name: "ChildComponent" });

  expect(child.exists()).toBe(true);
});
```

**When to use getComponent vs findComponent:**

- Use `getComponent` when the child **must** exist - provides clearer error messages on failure
- Use `findComponent` when the child **may not** exist - check with `.exists()` first

---

### Pattern 6: Global Configuration

Configure global plugins, components, and directives that all tests need. Create a custom mount function for consistency.

#### Test Utils Setup

```typescript
// test-utils.ts
import { mount, type MountingOptions, type VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import type { Component } from "vue";

// Import global components your app uses
import { Button } from "@/components/ui/button.vue";
import { Input } from "@/components/ui/input.vue";

interface ExtendedMountOptions extends MountingOptions<unknown> {
  initialPiniaState?: Record<string, unknown>;
}

function customMount<T extends Component>(
  component: T,
  options: ExtendedMountOptions = {},
): VueWrapper {
  const { initialPiniaState, ...mountOptions } = options;

  return mount(component, {
    global: {
      plugins: [
        createTestingPinia({
          initialState: initialPiniaState,
          stubActions: false,
        }),
      ],
      components: {
        Button,
        Input,
      },
      stubs: {
        // Stub router components by default
        RouterLink: true,
        RouterView: true,
      },
      ...mountOptions.global,
    },
    ...mountOptions,
  });
}

export { customMount as mount };
export * from "@vue/test-utils";
```

**Why custom mount:** Avoids repeating global configuration in every test. Creates consistent test environment matching your app.

See [examples/mocking.md](examples/mocking.md) for complete mocking examples.

</patterns>

---

<integration>

## Integration Guide

**Works with Vitest:**

- Configure test setup file to import global plugins
- Use `vi.mock()` for module mocking
- `flushPromises` works with Vitest's fake timers

**Works with Pinia:**

- Use `@pinia/testing` package for `createTestingPinia()`
- Actions are stubbed by default
- Initialize state via `initialState` option

**Works with Vue Router:**

- Stub `RouterLink` and `RouterView` for unit tests
- Use `router-mock` for integration tests requiring navigation
- Access route params via global mocks

**Works with Axios/Fetch:**

- Mock at module level with `vi.mock()`
- Use MSW for network-level mocking
- Always use `flushPromises()` after async operations

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Not awaiting DOM-updating methods** - Causes flaky tests that pass/fail randomly based on timing
- **Using `shallowMount` by default** - Reduces test fidelity; child components don't render as expected
- **Using classes/IDs as selectors** - Brittle tests that break when styling changes
- **Forgetting `flushPromises()` after API calls** - Assertions run before async operations complete

**Medium Priority Issues:**

- **Testing implementation details** - Accessing `wrapper.vm` directly instead of testing user-visible behavior
- **Over-mocking** - Stubbing everything reduces confidence that code works in production
- **Not using `createTestingPinia()`** - Manual store mocking is error-prone and verbose
- **Using `wrapper.setData()` to set reactive state** - Better to trigger through user interactions

**Common Mistakes:**

- Missing `await` on `trigger()`, `setValue()`, `setProps()`, `setData()`
- Using `find()` instead of `get()` for required elements (hides failures)
- Not resetting mocks between tests (cross-test pollution)
- Using `wrapper.vm.someMethod()` instead of triggering through UI

**Gotchas and Edge Cases:**

- `trigger('click')` doesn't work on disabled elements (expected browser behavior)
- `setValue()` only works on `<input>`, `<textarea>`, and `<select>` elements
- `shallowMount` stubs ALL child components including those from component libraries
- `flushPromises()` only resolves Promises - not `setTimeout` (use fake timers)
- Emitted events array grows across interactions - check specific index for assertions
- **`setData()` does NOT work with Composition API** - it only works with Options API `data()` function
- `isVisible()` requires `attachTo: document.body` to work correctly

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST `await` all DOM-updating methods: `trigger()`, `setValue()`, `setProps()`, `setData()`)**

**(You MUST use `flushPromises()` after async operations that Vue doesn't track (API calls, timers))**

**(You MUST use `mount()` by default - only use `shallowMount()` for performance issues or complex isolation)**

**(You MUST use `data-test` attributes for selectors, NOT classes or IDs)**

**(You MUST use `createTestingPinia()` for Pinia stores, NOT manual mocking)**

**Failure to follow these rules will produce flaky tests that don't reflect real component behavior.**

</critical_reminders>
