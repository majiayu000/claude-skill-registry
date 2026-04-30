---
name: nuxt-ui-v4
description: Nuxt UI v4 component library for building Nuxt v4 applications. 125+ accessible components with Tailwind v4, Reka UI, dark mode, theming. Use for dashboards, forms, overlays, editors, page layouts, pricing pages, or encountering component, theming, or TypeScript errors.
license: MIT
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
---

# Nuxt UI v4 - Production Component Library

**Version**: Nuxt UI v4.6+ | Nuxt v4.0.0 | **125+ Components**
**Last Verified**: 2026-03-30

A comprehensive production-ready component library with 125+ accessible components, Tailwind CSS v4, Reka UI accessibility, and first-class AI integration. Works with Nuxt and plain Vue apps (Vite, Inertia, SSR).

**MCP Integration**: This plugin includes the official Nuxt UI MCP server for live component data.

---

## When to Use / NOT Use

**Use when**: Building Nuxt v4 dashboards, AI chat interfaces, landing pages, forms, admin panels, pricing pages, blogs, documentation sites, or any UI with Nuxt UI components

**DON'T use**: React projects, Nuxt 3 or earlier, Tailwind CSS v3. Vue-only projects ARE supported via Vite plugin.

---

## Quick Start

```bash
bunx nuxi init my-app && cd my-app
bun add @nuxt/ui tailwindcss
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/ui'],
  css: ['~/assets/css/main.css']
})
```

```css
/* assets/css/main.css */
@import "tailwindcss";
@import "@nuxt/ui";
```

```vue
<!-- app.vue -->
<template><UApp><NuxtPage /></UApp></template>
```

**Or use a template**:
```bash
npm create nuxt@latest -- -t ui             # Starter
npm create nuxt@latest -- -t ui/dashboard    # Dashboard
npm create nuxt@latest -- -t ui/chat         # AI Chat
npm create nuxt@latest -- -t ui/landing      # Landing page
npm create nuxt@latest -- -t ui/saas         # SaaS
npm create nuxt@latest -- -t ui/docs         # Documentation
npm create nuxt@latest -- -t ui/portfolio    # Portfolio
npm create nuxt@latest -- -t ui/changelog    # Changelog
npm create nuxt@latest -- -t ui/editor       # Rich text editor
```

**Commands available**: `/nuxt-ui-v4:setup`, `/nuxt-ui:migrate`, `/nuxt-ui:theme`, `/nuxt-ui:component`

---

## Component Categories (125+ Total)

### Dashboard (10 components) - NEW
Complete admin interface system:
- **DashboardGroup** - Fixed layout wrapper with sidebar state management
- **DashboardSidebar** - Resizable, collapsible sidebar
- **DashboardPanel** - Main content panel with header/body/footer slots
- **DashboardNavbar** - Top navigation bar
- **DashboardToolbar** - Secondary toolbar under navbar
- **DashboardSearch** - CommandPalette for dashboard search
- **DashboardSearchButton** - Button to trigger search
- **DashboardSidebarCollapse** - Collapse button for desktop
- **DashboardSidebarToggle** - Toggle button for mobile
- **DashboardResizeHandle** - Resize handle for sidebar/panels

```vue
<template>
  <UDashboardGroup>
    <UDashboardSidebar>
      <UNavigationMenu :items="menuItems" />
    </UDashboardSidebar>
    <UDashboardPanel>
      <template #header><UDashboardNavbar /></template>
      <template #body><NuxtPage /></template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>
```

**Details**: Load `references/dashboard-components.md` for complete dashboard patterns

---

### Chat / AI (8 components)
Purpose-built for AI chatbots with AI SDK v5:
- **ChatMessage** - Single message with icon, avatar, actions
- **ChatMessages** - Message list with auto-scroll, status indicator
- **ChatPalette** - Chat interface inside an overlay
- **ChatPrompt** - Enhanced Textarea for AI prompts
- **ChatPromptSubmit** - Submit button with status handling
- **ChatReasoning** - Collapsible AI reasoning/thinking process (NEW v4.6)
- **ChatTool** - Collapsible AI tool invocation status (NEW v4.6)
- **ChatShimmer** - Text shimmer animation for streaming states (NEW v4.6)

```vue
<script setup lang="ts">
import { isReasoningUIPart, isTextUIPart, isToolUIPart, getToolName } from 'ai'
import { Chat } from '@ai-sdk/vue'
import { isReasoningStreaming, isToolStreaming } from '@nuxt/ui/utils/ai'

const input = ref('')
const chat = new Chat({
  onError(error) { console.error(error) }
})

function onSubmit() {
  chat.sendMessage({ text: input.value })
  input.value = ''
}
</script>

<template>
  <UChatMessages :messages="chat.messages" :status="chat.status">
    <template #content="{ message }">
      <template v-for="(part, index) in message.parts" :key="`${message.id}-${part.type}-${index}`">
        <UChatReasoning v-if="isReasoningUIPart(part)" :text="part.text" :streaming="isReasoningStreaming(message, index, chat)" />
        <UChatTool v-else-if="isToolUIPart(part)" :text="getToolName(part)" :streaming="isToolStreaming(part)" />
        <template v-else-if="isTextUIPart(part)">
          <MDC v-if="message.role === 'assistant'" :value="part.text" :cache-key="`${message.id}-${index}`" />
          <p v-else-if="message.role === 'user'" class="whitespace-pre-wrap">{{ part.text }}</p>
        </template>
      </template>
    </template>
  </UChatMessages>
  <UChatPrompt v-model="input" @submit="onSubmit">
    <UChatPromptSubmit :status="chat.status" @stop="chat.stop()" @reload="chat.regenerate()" />
  </UChatPrompt>
</template>
```

**Details**: Load `references/chat-components.md` for full AI SDK integration, streaming, reasoning, tool calling

---

### Editor (6 components) - NEW
Rich text editing with TipTap:
- **Editor** - TipTap-based editor with markdown/HTML/JSON support
- **EditorToolbar** - Fixed, bubble, or floating toolbar
- **EditorDragHandle** - Drag handle for reordering blocks
- **EditorMentionMenu** - @ mention suggestions
- **EditorEmojiMenu** - : emoji picker
- **EditorSuggestionMenu** - / command menu

```vue
<template>
  <UEditor v-model="content" :extensions="extensions">
    <template #toolbar>
      <UEditorToolbar />
    </template>
  </UEditor>
</template>
```

**Details**: Load `references/editor-components.md` for TipTap setup, extensions, toolbar customization

---

### Page Layout (16 components) - NEW
Landing pages and content layouts:
- **Page** - Grid layout with left/right columns
- **PageHeader** - Responsive page header
- **PageHero** - Hero section with title, description, CTAs
- **PageSection** - Content section container
- **PageGrid** - Responsive grid system
- **PageColumns** - Multi-column layout
- **PageFeature** - Feature showcase component
- **PageCTA** - Call-to-action section
- **PageCard** - Pre-styled card with title, description, link
- **PageList** - Vertical list layout
- **PageLogos** - Logo showcase
- **PageAnchors** - Anchor link list
- **PageAside** - Sticky sidebar
- **PageBody** - Main content area
- **PageLinks** - Link list

```vue
<template>
  <UPage>
    <UPageHero title="Welcome" description="Get started today" :links="heroLinks" />
    <UPageSection>
      <UPageGrid>
        <UPageFeature v-for="f in features" v-bind="f" />
      </UPageGrid>
    </UPageSection>
    <UPageCTA title="Ready?" :links="ctaLinks" />
  </UPage>
</template>
```

**Details**: Load `references/page-layout-components.md` for landing page patterns

---

### Content (7 components) - NEW
Documentation and blog content:
- **BlogPost** - Article display component
- **BlogPosts** - Blog grid layout
- **ChangelogVersion** - Version entry display
- **ChangelogVersions** - Changelog timeline
- **ContentNavigation** - Accordion-style nav for docs
- **ContentSearch** - Documentation search CommandPalette
- **ContentSearchButton** - Button to open search
- **ContentSurround** - Prev/next navigation
- **ContentToc** - Sticky table of contents

```vue
<template>
  <UBlogPosts>
    <UBlogPost v-for="post in posts" v-bind="post" />
  </UBlogPosts>
</template>
```

**Details**: Load `references/content-components.md` for blog and documentation patterns

---

### Pricing (3 components) - NEW
SaaS pricing pages:
- **PricingPlan** - Individual plan card
- **PricingPlans** - Responsive plan grid
- **PricingTable** - Feature comparison table

```vue
<template>
  <UPricingPlans>
    <UPricingPlan
      v-for="plan in plans"
      :title="plan.title"
      :price="plan.price"
      :features="plan.features"
    />
  </UPricingPlans>
</template>
```

**Details**: Load `references/pricing-components.md` for pricing page patterns

---

### Forms (22 components)
Input, InputDate, InputTime, InputNumber, InputTags, InputMenu, Select, SelectMenu, Textarea, Checkbox, CheckboxGroup, RadioGroup, Switch, Slider, Calendar, ColorPicker, PinInput, Form, FormField, FileUpload, FieldGroup, AuthForm

```vue
<UForm :state="state" :schema="schema" @submit="onSubmit">
  <UFormField name="email" label="Email">
    <UInput v-model="state.email" type="email" />
  </UFormField>
  <UButton type="submit">Submit</UButton>
</UForm>
```

**Details**: Load `references/form-components-reference.md` for validation, nested forms, file uploads

---

### Navigation (8 components)
Tabs, Breadcrumb, Link, Pagination, CommandPalette, NavigationMenu, Stepper, Tree

```vue
<UTabs v-model="tab" :items="items" />
<UCommandPalette :groups="groups" placeholder="Search..." />
<UStepper v-model="step" :items="steps" />
```

**Details**: Load `references/navigation-components-reference.md` for patterns

---

### Overlays (8 components)
Modal, Drawer, Slideover, Dialog, Popover, DropdownMenu, ContextMenu, Tooltip

```vue
<UModal v-model="isOpen"><UCard>Content</UCard></UModal>
<UDrawer v-model="isOpen" side="right">...</UDrawer>
```

**Details**: Load `references/overlay-decision-guide.md` for when to use each

---

### Feedback (7 components)
Alert, Toast, Progress, Skeleton, Empty, Error, Banner

```vue
<UAlert color="warning" title="Warning message" />
<UEmpty icon="i-heroicons-inbox" title="No items" />
<UBanner title="Important announcement" />
```

**Details**: Load `references/feedback-components-reference.md`

---

### Layout (6 components)
Card, Container, Main, Header, Footer, FooterColumns, Separator

---

### Data (2 components)
Table (with virtualization), ScrollArea

---

### General (15 components)
Button, FieldGroup, Avatar, AvatarGroup, Badge, Accordion, Carousel, Chip, Collapsible, Icon, Kbd, Marquee, Timeline, User, App

---

### Color Mode (6 components)
ColorModeAvatar, ColorModeButton, ColorModeImage, ColorModeSelect, ColorModeSwitch, LocaleSelect

---

## Composables

**Core**: `useToast`, `useOverlay`, `useFormField`, `useScrollShadow`
**Utilities**: `defineShortcuts`, `defineLocale`, `extendLocale`, `extractShortcuts`

```typescript
const { add } = useToast()
add({ title: 'Success', color: 'success' })

defineShortcuts({ 'meta_k': () => openSearch() })
```

**AI Utilities**: `isReasoningStreaming`, `isToolStreaming`, `getTextFromMessage` (from `@nuxt/ui/utils/ai`)

---

## Common Errors (Top 5)

**1. Missing UApp Wrapper** → Wrap app with `<UApp>`
**2. CSS Import Order** → `@import "tailwindcss"` FIRST, then `@import "@nuxt/ui"`
**3. Missing tailwindcss package** → `bun add @nuxt/ui tailwindcss` (both required)
**4. Module Not Found** → Add `'@nuxt/ui'` to `modules` in nuxt.config.ts
**5. useChat not found** → AI SDK v5 uses `new Chat()` class, not `useChat()` composable

**Full list**: Load `references/COMMON_ERRORS_DETAILED.md` for 25+ error solutions

---

## When to Load References

**Dashboard/Admin**: `dashboard-components.md`
**AI Chat**: `chat-components.md`, `ai-sdk-v5-integration.md`
**Chat Sub-components**: `chat-reasoning.md`, `chat-tool.md`, `chat-shimmer.md`
**Rich Text**: `editor-components.md`
**Landing Pages**: `page-layout-components.md`
**Pricing/SaaS**: `pricing-components.md`
**Blog/Docs**: `content-components.md`
**Auth/Login**: `auth-form.md`
**Forms**: `form-components-reference.md`, `form-validation-patterns.md`
**Theming**: `semantic-color-system.md`, `component-theming-guide.md`
**Troubleshooting**: `COMMON_ERRORS_DETAILED.md`

---

## Available Commands

- `/nuxt-ui-v4:setup` - Initialize Nuxt UI in project
- `/nuxt-ui:migrate` - Migrate from v2/v3 to v4
- `/nuxt-ui:theme` - Generate theme configuration
- `/nuxt-ui:component` - Scaffold component with Nuxt UI patterns

## Available Agents

- **nuxt-ui-component-selector** - Recommends best components for use cases
- **nuxt-ui-migration-assistant** - Guides v2/v3 → v4 migration
- **nuxt-ui-troubleshooter** - Diagnoses and fixes common issues

## MCP Integration

This plugin includes the official Nuxt UI MCP server (`https://ui.nuxt.com/mcp`) providing:
- Component listing and metadata
- Documentation access
- Migration guides
- Template discovery
