---
name: vue-nuxt
description: Vue 3 and Nuxt 3 for JARVIS AI Assistant UI development with security-first patterns
model: sonnet
risk_level: MEDIUM
version: 1.0.0
---

# Vue 3 / Nuxt 3 Development Skill

> **File Organization**: This skill uses split structure. See `references/` for advanced patterns and security examples.

## 1. Overview

This skill provides expertise for building the JARVIS AI Assistant user interface using Vue 3 and Nuxt 3. It focuses on creating responsive, performant 3D HUD interfaces with security-first development practices.

**Risk Level**: MEDIUM - Handles user input, renders dynamic content, potential XSS vectors

**Primary Use Cases**:
- Building reactive 3D HUD components for JARVIS interface
- Server-side rendering for initial load performance
- Client-side state management integration
- Secure handling of user inputs and API responses

## 2. Core Responsibilities

### 2.1 Fundamental Principles

1. **TDD First**: Write tests before implementation - red/green/refactor cycle
2. **Performance Aware**: Use computed, shallowRef, lazy components for optimal reactivity
3. **Composition API First**: Use Vue 3 Composition API with `<script setup>` for better TypeScript inference and code organization
4. **Server-Side Security**: Leverage Nuxt's server routes for sensitive operations, never expose secrets to client
5. **Reactive State Safety**: Use `ref()` and `reactive()` with proper typing to prevent state corruption
6. **Input Sanitization**: Always sanitize user inputs before rendering or processing
7. **Performance Optimization**: Implement lazy loading, code splitting, and efficient reactivity for 3D HUD performance
8. **Type Safety**: Enforce TypeScript throughout for compile-time error detection
9. **Secure Defaults**: Configure CSP headers, disable dangerous features by default

## 3. Technology Stack & Versions

### 3.1 Recommended Versions

| Package | Version | Security Notes |
|---------|---------|----------------|
| Vue | ^3.4.0 | Latest stable with improved reactivity |
| Nuxt | ^3.12.4+ | **CRITICAL**: Fixes CVE-2024-34344 RCE |
| @nuxt/devtools | ^1.3.9+ | **CRITICAL**: Fixes CVE-2024-23657 |
| vite | ^5.0.0 | Latest with security patches |

### 3.2 Security-Critical Dependencies

```json
{
  "dependencies": {
    "nuxt": "^3.12.4",
    "vue": "^3.4.0",
    "dompurify": "^3.0.6",
    "isomorphic-dompurify": "^2.0.0"
  },
  "devDependencies": {
    "@nuxt/devtools": "^1.3.9",
    "eslint-plugin-vue": "^9.0.0",
    "eslint-plugin-security": "^2.0.0"
  }
}
```

## 4. Implementation Patterns

### 4.1 Secure Component Structure

```vue
<script setup lang="ts">
// ✅ Type-safe props with validation
interface Props {
  hudData: HUDDisplayData
  userId: string
}

const props = defineProps<Props>()

// ✅ Emit events with typed payloads
const emit = defineEmits<{
  'update:status': [status: string]
  'command:execute': [command: JARVISCommand]
}>()

// ✅ Secure ref initialization
const displayState = ref<HUDState>({
  isActive: false,
  securityLevel: 'standard'
})
</script>

<template>
  <!-- ✅ Use v-text for user content to prevent XSS -->
  <div class="hud-panel">
    <span v-text="props.hudData.title" />
  </div>
</template>
```

### 4.2 Input Sanitization Pattern

```typescript
// composables/useSanitize.ts
import DOMPurify from 'isomorphic-dompurify'

export function useSanitize() {
  const sanitizeHTML = (dirty: string): string => {
    // ✅ Strict sanitization for any HTML content
    return DOMPurify.sanitize(dirty, {
      ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'span'],
      ALLOWED_ATTR: ['class']
    })
  }

  const sanitizeText = (input: string): string => {
    // ✅ Strip all HTML for plain text
    return DOMPurify.sanitize(input, { ALLOWED_TAGS: [] })
  }

  return { sanitizeHTML, sanitizeText }
}
```

### 4.3 Secure API Route Pattern

```typescript
// server/api/jarvis/command.post.ts
import { z } from 'zod'

// ✅ Define strict schema for command validation
const commandSchema = z.object({
  action: z.enum(['status', 'control', 'query']),
  target: z.string().max(100).regex(/^[a-zA-Z0-9-_]+$/),
  parameters: z.record(z.string()).optional()
})

export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  // ✅ Validate input against schema
  const result = commandSchema.safeParse(body)
  if (!result.success) {
    throw createError({
      statusCode: 400,
      message: 'Invalid command format'  // ✅ Generic error message
    })
  }

  // ✅ Process validated command
  const command = result.data

  // Never log sensitive data
  console.log(`Processing command: ${command.action}`)

  return { success: true, commandId: generateSecureId() }
})
```

### 4.4 Secure Environment Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  // ✅ Security headers
  routeRules: {
    '/**': {
      headers: {
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block'
      }
    }
  },

  // ✅ Runtime config - secrets stay server-side
  runtimeConfig: {
    apiSecret: process.env.API_SECRET,  // Server only
    public: {
      apiBase: '/api'  // Client accessible
    }
  },

  // ✅ Disable devtools in production
  devtools: { enabled: process.env.NODE_ENV === 'development' }
})
```

### 4.5 3D HUD Component Integration

```vue
<script setup lang="ts">
// components/HUDDisplay.vue
import { TresCanvas } from '@tresjs/core'

const props = defineProps<{
  metrics: SystemMetrics
}>()

// ✅ Validate metrics before rendering
const validatedMetrics = computed(() => {
  return {
    cpu: Math.min(100, Math.max(0, props.metrics.cpu)),
    memory: Math.min(100, Math.max(0, props.metrics.memory)),
    status: sanitizeText(props.metrics.status)
  }
})
</script>

<template>
  <TresCanvas>
    <HUDMetricsDisplay :data="validatedMetrics" />
  </TresCanvas>
</template>
```

## 5. Implementation Workflow (TDD)

### 5.1 Step 1: Write Failing Test First

Always start by writing tests that define expected behavior:

```typescript
// tests/components/VoiceIndicator.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import VoiceIndicator from '@/components/VoiceIndicator.vue'

describe('VoiceIndicator', () => {
  it('displays idle state by default', () => {
    const wrapper = mount(VoiceIndicator)
    expect(wrapper.find('.indicator').classes()).toContain('idle')
    expect(wrapper.text()).toContain('Ready')
  })

  it('shows listening state when active', async () => {
    const wrapper = mount(VoiceIndicator, {
      props: { isListening: true }
    })
    expect(wrapper.find('.indicator').classes()).toContain('listening')
    expect(wrapper.find('.pulse-animation').exists()).toBe(true)
  })

  it('emits cancel event on escape key', async () => {
    const wrapper = mount(VoiceIndicator, {
      props: { isListening: true }
    })
    await wrapper.trigger('keydown.escape')
    expect(wrapper.emitted('cancel')).toBeTruthy()
  })
})
```

### 5.2 Step 2: Implement Minimum to Pass

Write only enough code to make the tests pass:

```vue
<script setup lang="ts">
const props = defineProps<{ isListening?: boolean }>()
const emit = defineEmits<{ 'cancel': [] }>()

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') emit('cancel')
}
</script>

<template>
  <div
    class="indicator"
    :class="isListening ? 'listening' : 'idle'"
    @keydown="handleKeydown"
    tabindex="0"
  >
    <span v-if="!isListening">Ready</span>
    <div v-else class="pulse-animation" />
  </div>
</template>
```

### 5.3 Step 3: Refactor if Needed

After tests pass, improve code quality without changing behavior. Re-run tests after each refactor.

### 5.4 Step 4: Run Full Verification

```bash
# Run all verification steps before committing
npx vitest run                    # Unit tests
npx eslint . --ext .vue,.ts       # Linting
npx nuxi typecheck                # Type checking
npm run build                     # Build verification
```

## 6. Performance Patterns

### 6.1 Computed Properties for Derived State

```typescript
// ❌ BAD - Recalculates in template on every render
<template>
  <div>{{ items.filter(i => i.active).length }} active</div>
</template>

// ✅ GOOD - Cached until dependencies change
const activeCount = computed(() => items.value.filter(i => i.active).length)
<template>
  <div>{{ activeCount }} active</div>
</template>
```

### 6.2 shallowRef for Large Objects

```typescript
// ❌ BAD - Deep reactivity on large 3D data
const meshData = ref<MeshData>({ vertices: new Float32Array(100000), ... })

// ✅ GOOD - Shallow reactivity, manual trigger
const meshData = shallowRef<MeshData>({ vertices: new Float32Array(100000), ... })
// Trigger update explicitly
meshData.value = { ...newData }
triggerRef(meshData)
```

### 6.3 defineAsyncComponent for Lazy Loading

```typescript
// ❌ BAD - All components loaded upfront
import HeavyChart from '@/components/HeavyChart.vue'

// ✅ GOOD - Load only when needed
const HeavyChart = defineAsyncComponent(() =>
  import('@/components/HeavyChart.vue')
)

// With loading state
const HeavyChart = defineAsyncComponent({
  loader: () => import('@/components/HeavyChart.vue'),
  loadingComponent: LoadingSpinner,
  delay: 200
})
```

### 6.4 v-memo for List Optimization

```vue
<!-- ❌ BAD - Re-renders all items on any change -->
<div v-for="item in items" :key="item.id">
  <ExpensiveComponent :data="item" />
</div>

<!-- ✅ GOOD - Skip re-render if item unchanged -->
<div v-for="item in items" :key="item.id" v-memo="[item.id, item.updated]">
  <ExpensiveComponent :data="item" />
</div>
```

### 6.5 Virtual Scrolling for Long Lists

```vue
<script setup lang="ts">
import { useVirtualList } from '@vueuse/core'

const { list, containerProps, wrapperProps } = useVirtualList(
  items,
  { itemHeight: 50 }
)
</script>

<template>
  <!-- ✅ Only renders visible items -->
  <div v-bind="containerProps" class="h-[400px] overflow-auto">
    <div v-bind="wrapperProps">
      <div v-for="{ data, index } in list" :key="index">
        {{ data.name }}
      </div>
    </div>
  </div>
</template>
```

### 6.6 Debounced Watchers

```typescript
// ❌ BAD - Fires on every keystroke
watch(searchQuery, async (query) => {
  results.value = await searchAPI(query)
})

// ✅ GOOD - Debounced to reduce API calls
import { watchDebounced } from '@vueuse/core'

watchDebounced(
  searchQuery,
  async (query) => {
    results.value = await searchAPI(query)
  },
  { debounce: 300 }
)

// Alternative with manual debounce
watch(searchQuery, useDebounceFn(async (query) => {
  results.value = await searchAPI(query)
}, 300))
```

## 7. Security Standards

### 7.1 Known Vulnerabilities (CVE Research)

| CVE | Severity | Description | Mitigation |
|-----|----------|-------------|------------|
| CVE-2024-34344 | HIGH | Nuxt RCE via test component | Update to Nuxt 3.12.4+ |
| CVE-2024-23657 | HIGH | Devtools path traversal/RCE | Update devtools to 1.3.9+ |
| CVE-2023-3224 | CRITICAL | Dev server code injection | Update to Nuxt 3.4.4+, never expose dev server |

**See**: `references/security-examples.md` for detailed mitigation code

### 5.2 OWASP Top 10 Coverage

| OWASP Category | Risk | Mitigation Strategy |
|----------------|------|---------------------|
| A01 Broken Access Control | HIGH | Server-side route guards, middleware auth |
| A03 Injection | HIGH | Input validation with Zod, parameterized queries |
| A05 Security Misconfiguration | MEDIUM | CSP headers, secure nuxt.config |
| A07 XSS | HIGH | v-text directive, DOMPurify sanitization |

### 5.3 Input Validation Framework

```typescript
// ❌ DANGEROUS - Direct v-html with user input
<div v-html="userMessage" />

// ✅ SECURE - Sanitized HTML or plain text
<div v-html="sanitizeHTML(userMessage)" />
<span v-text="userMessage" />
```

### 5.4 Authentication Middleware

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to) => {
  const { authenticated } = useAuthState()

  if (!authenticated.value && to.meta.requiresAuth) {
    return navigateTo('/login')
  }
})
```

## 6. Testing & Quality

### 6.1 Security Testing

```typescript
// tests/security/xss.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HUDPanel from '@/components/HUDPanel.vue'

describe('XSS Prevention', () => {
  it('should sanitize malicious input', () => {
    const wrapper = mount(HUDPanel, {
      props: {
        title: '<script>alert("xss")</script>Hello'
      }
    })

    expect(wrapper.html()).not.toContain('<script>')
    expect(wrapper.text()).toContain('Hello')
  })
})
```

### 6.2 Component Testing

```typescript
// tests/components/HUDDisplay.test.ts
describe('HUDDisplay', () => {
  it('validates metric bounds', () => {
    const wrapper = mount(HUDDisplay, {
      props: {
        metrics: { cpu: 150, memory: -10, status: 'active' }
      }
    })

    // Should clamp values to valid range
    expect(wrapper.vm.validatedMetrics.cpu).toBe(100)
    expect(wrapper.vm.validatedMetrics.memory).toBe(0)
  })
})
```

## 7. Common Patterns / Workflows

### 7.1 JARVIS HUD Component Workflow

1. **Define TypeScript interfaces** for all data structures
2. **Create composable** for shared logic
3. **Implement component** with Composition API
4. **Add input validation** at component boundary
5. **Write security tests** for XSS/injection
6. **Integrate with 3D scene** via TresJS

### 7.2 API Integration Workflow

1. **Define Zod schema** for request/response
2. **Create server route** with validation
3. **Implement client composable** with error handling
4. **Add loading/error states** to UI
5. **Test error cases** and edge conditions

## 8. Common Mistakes & Anti-Patterns

### 8.1 Critical Security Anti-Patterns

#### Never: Use v-html with Unsanitized Input

```vue
<!-- ❌ DANGEROUS - XSS vulnerability -->
<div v-html="userProvidedContent" />

<!-- ✅ SECURE - Sanitized content -->
<div v-html="sanitizeHTML(userProvidedContent)" />

<!-- ✅ BEST - Plain text when HTML not needed -->
<span v-text="userProvidedContent" />
```

#### Never: Expose Secrets in Client Code

```typescript
// ❌ DANGEROUS - Secret in public config
runtimeConfig: {
  public: {
    apiKey: process.env.API_KEY  // Exposed to client!
  }
}

// ✅ SECURE - Secrets stay server-side
runtimeConfig: {
  apiKey: process.env.API_KEY,  // Server only
  public: {
    apiBase: '/api'
  }
}
```

#### Never: Trust Client-Side Validation Alone

```typescript
// ❌ DANGEROUS - Client-only validation
const handleSubmit = () => {
  if (isValidEmail(email.value)) {
    $fetch('/api/subscribe', { body: { email: email.value } })
  }
}

// ✅ SECURE - Server-side validation
// server/api/subscribe.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const result = emailSchema.safeParse(body)
  if (!result.success) {
    throw createError({ statusCode: 400, message: 'Invalid email' })
  }
  // Process validated email
})
```

### 8.2 Performance Anti-Patterns

#### Avoid: Reactive Arrays in Computed

```typescript
// ❌ BAD - Creates new array on every access
const filtered = computed(() => {
  return items.value.filter(i => i.active).sort()
})

// ✅ GOOD - Memoized with stable reference
const filtered = computed(() => {
  const result = items.value.filter(i => i.active)
  result.sort((a, b) => a.name.localeCompare(b.name))
  return result
})
```

## 9. Quick Reference

### Essential Commands

```bash
# Development
npx nuxi dev --host  # Never expose to public network!

# Security audit
npm audit --audit-level=high
npx nuxi typecheck

# Production build
npx nuxi build
```

### Key Composables

```typescript
// State management
const state = useState<T>('key', () => initialValue)

// Runtime config access
const config = useRuntimeConfig()

// Route navigation
const router = useRouter()
await navigateTo('/path')
```

## 13. Pre-Deployment Checklist

### Security Verification

- [ ] Nuxt version >= 3.12.4 (CVE-2024-34344 fix)
- [ ] Devtools version >= 1.3.9 (CVE-2024-23657 fix)
- [ ] CSP headers configured in nuxt.config
- [ ] No secrets in `runtimeConfig.public`
- [ ] All user inputs sanitized with DOMPurify
- [ ] Server routes validate with Zod schemas
- [ ] Authentication middleware on protected routes
- [ ] Devtools disabled in production

### Build Verification

- [ ] `npm audit` shows no high/critical vulnerabilities
- [ ] TypeScript compilation passes
- [ ] All security tests pass
- [ ] Production build completes without errors

## 14. Summary

This Vue/Nuxt skill provides secure patterns for building the JARVIS AI Assistant HUD interface:

1. **Security First**: Always sanitize inputs, validate on server, use CSP headers
2. **Type Safety**: TypeScript throughout with strict validation schemas
3. **Performance**: Composition API, lazy loading, efficient reactivity
4. **Maintainability**: Clear component structure, composables for reuse

**Remember**: The JARVIS HUD handles sensitive system data. Every component must treat user input as potentially malicious and validate all data boundaries.

---

**References**:
- `references/advanced-patterns.md` - Complex component patterns
- `references/security-examples.md` - Detailed security implementations
