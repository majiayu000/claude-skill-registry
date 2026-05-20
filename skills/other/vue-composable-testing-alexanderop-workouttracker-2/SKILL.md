---
name: vue-composable-testing
description: Test Vue 3 composables with Vitest following best practices. Use when writing tests for composables, creating test helpers for Vue reactivity, or when asked to "test a composable", "write tests for use*", or "help test Vue composition functions". Covers independent composables (direct testing) and dependent composables (lifecycle/inject testing with helpers).
---

# Vue Composable Testing Guide

Test composables based on their dependency type: **Independent** (direct testing) or **Dependent** (requires component context).

## Quick Classification

| Type | Characteristics | Testing Approach |
|------|----------------|------------------|
| Independent | Uses only reactivity APIs (ref, computed, watch) | Test directly like functions |
| Dependent | Uses lifecycle hooks (onMounted) or inject | Use `withSetup` or `useInjectedSetup` helpers |

## Testing Independent Composables

Independent composables use only Vue's reactivity system without lifecycle hooks or dependency injection.

```ts
// useSum.ts - Independent composable
import type { ComputedRef, Ref } from 'vue'
import { computed } from 'vue'

export function useSum(a: Ref<number>, b: Ref<number>): ComputedRef<number> {
  return computed(() => a.value + b.value)
}
```

```ts
import { describe, expect, it } from 'vitest'
// useSum.spec.ts - Direct testing
import { ref } from 'vue'
import { useSum } from '../useSum'

describe('useSum', () => {
  it('computes sum of two numbers', () => {
    const num1 = ref(2)
    const num2 = ref(3)
    const sum = useSum(num1, num2)

    expect(sum.value).toBe(5)
  })

  it('reacts to value changes', () => {
    const num1 = ref(1)
    const num2 = ref(1)
    const sum = useSum(num1, num2)

    num1.value = 10
    expect(sum.value).toBe(11)
  })
})
```

## Testing Dependent Composables

### With Lifecycle Hooks

Composables using `onMounted`, `onUnmounted`, etc. require a component context. Use the `withSetup` helper.

```ts
// useLocalStorage.ts - Uses onMounted
import { onMounted, ref, watch } from 'vue'

export function useLocalStorage<TValue>(key: string, initialValue: TValue) {
  const value = ref<TValue>(initialValue)

  onMounted(() => {
    const stored = localStorage.getItem(key)
    if (stored !== null) {
      value.value = JSON.parse(stored)
    }
  })

  watch(value, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue))
  })

  return { value }
}
```

```ts
// useLocalStorage.spec.ts - Using withSetup
import { beforeEach, describe, expect, it } from 'vitest'
import { useLocalStorage } from '../useLocalStorage'
import { withSetup } from './helpers/withSetup'

describe('useLocalStorage', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('loads initial value', () => {
    const [result] = withSetup(() => useLocalStorage('key', 'initial'))
    expect(result.value.value).toBe('initial')
  })

  it('loads value from localStorage on mount', () => {
    localStorage.setItem('key', JSON.stringify('stored'))
    const [result] = withSetup(() => useLocalStorage('key', 'initial'))
    expect(result.value.value).toBe('stored')
  })

  it('persists changes to localStorage', () => {
    const [result] = withSetup(() => useLocalStorage('key', 'initial'))
    result.value.value = 'updated'
    expect(JSON.parse(localStorage.getItem('key')!)).toBe('updated')
  })
})
```

### With Inject

Composables using `inject` require provided values. Use the `useInjectedSetup` helper.

```ts
// useMessage.ts - Uses inject
import type { InjectionKey } from 'vue'
import { inject } from 'vue'

export const MessageKey: InjectionKey<string> = Symbol('message')

export function useMessage() {
  const message = inject(MessageKey)

  if (!message) {
    throw new Error('Message must be provided')
  }

  return {
    message,
    getUpperCase: () => message.toUpperCase(),
    getReversed: () => message.split('').reverse().join(''),
  }
}
```

```ts
// useMessage.spec.ts - Using useInjectedSetup
import { describe, expect, it } from 'vitest'
import { MessageKey, useMessage } from '../useMessage'
import { useInjectedSetup } from './helpers/useInjectedSetup'

describe('useMessage', () => {
  it('uses injected message', () => {
    const result = useInjectedSetup(
      () => useMessage(),
      [{ key: MessageKey, value: 'hello world' }]
    )

    expect(result.message).toBe('hello world')
    expect(result.getUpperCase()).toBe('HELLO WORLD')
    expect(result.getReversed()).toBe('dlrow olleh')

    result.unmount()
  })

  it('throws when message not provided', () => {
    expect(() => {
      useInjectedSetup(() => useMessage(), [])
    }).toThrow('Message must be provided')
  })
})
```

## Helper Functions

Create these helpers in your test utilities. See `references/test-helpers.md` for complete implementations.

### withSetup

Mounts a minimal Vue app to trigger lifecycle hooks:

```ts
import type { App } from 'vue'
import { createApp } from 'vue'

export function withSetup<TResult>(composable: () => TResult): [TResult, App] {
  let result: TResult
  const app = createApp({
    setup() {
      result = composable()
      return () => {}
    },
  })
  app.mount(document.createElement('div'))
  return [result!, app]
}
```

### useInjectedSetup

Creates a provider component for inject-dependent composables:

```ts
import type { InjectionKey } from 'vue'
import { createApp, defineComponent, h, provide } from 'vue'

interface InjectionConfig {
  key: InjectionKey<unknown> | string
  value: unknown
}

export function useInjectedSetup<TResult>(
  setup: () => TResult,
  injections: ReadonlyArray<InjectionConfig> = []
): TResult & { unmount: () => void } {
  let result!: TResult

  const Comp = defineComponent({
    setup() {
      result = setup()
      return () => h('div')
    },
  })

  const Provider = defineComponent({
    setup() {
      injections.forEach(({ key, value }) => {
        provide(key, value)
      })
      return () => h(Comp)
    },
  })

  const el = document.createElement('div')
  const app = createApp(Provider)
  app.mount(el)

  return {
    ...result,
    unmount: () => app.unmount(),
  }
}
```

## Testing Patterns

### Async Composables

```ts
describe('useAsyncData', () => {
  it('handles async operations', async () => {
    const [result] = withSetup(() => useAsyncData())

    expect(result.isLoading.value).toBe(true)

    await result.fetch()

    expect(result.isLoading.value).toBe(false)
    expect(result.data.value).toBeDefined()
  })
})
```

### Error States

```ts
describe('useFetch', () => {
  it('captures errors', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('Network error'))

    const [result] = withSetup(() => useFetch('/api/data'))
    await result.execute()

    expect(result.error.value).toBeInstanceOf(Error)
    expect(result.error.value?.message).toBe('Network error')
  })
})
```

### Cleanup

```ts
describe('useInterval', () => {
  it('cleans up on unmount', () => {
    const clearSpy = vi.spyOn(globalThis, 'clearInterval')

    const [, app] = withSetup(() => useInterval(() => {}, 1000))
    app.unmount()

    expect(clearSpy).toHaveBeenCalled()
  })
})
```

## Best Practices

1. **Classify first** - Determine if composable is independent or dependent before writing tests
2. **Always unmount** - Call `app.unmount()` or `result.unmount()` to prevent memory leaks
3. **Test reactivity** - Verify computed values update when dependencies change
4. **Mock external APIs** - Use `vi.spyOn` or `vi.mock` for fetch, localStorage, etc.
5. **Test error paths** - Verify composables expose errors correctly
6. **Clear state** - Use `beforeEach` to reset mocks and external state like localStorage
