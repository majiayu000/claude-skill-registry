---
name: api-pattern
description: Provides Vue component structure templates for Composition API and Options API. Used when generating .vue components and views to match user's selected API pattern preference.
---

# API Pattern Skill

## Purpose
Provides Vue component structure templates and patterns for both Composition API and Options API styles.

## User Choice
The user selects their preferred Vue API pattern:
- `composition-api`: Modern functional approach (recommended for Vue 3)
- `options-api`: Traditional object-based approach (familiar from Vue 2)

## When to Use

Use this skill when generating:
- Vue components (`src/components/**/*.vue`)
- View components (`src/views/**/*.vue`)
- Root App component (`src/App.vue`)
- Any `.vue` single-file component

## Pattern Selection Logic

**Composition API** should be used when:
- User explicitly selects `composition-api`
- Building new Vue 3 applications (recommended default)
- Need better TypeScript integration
- Want improved code reusability via composables
- Working with complex component logic

**Options API** should be used when:
- User explicitly selects `options-api`
- Migrating from Vue 2 applications
- Team preference for object-based structure
- Developer familiarity with Vue 2 patterns

## Templates

See `examples.md` for complete component templates including:
- Basic component structure
- Component with props and emits
- Component with lifecycle hooks
- Component with computed properties
- Component with watchers
- Component with composables/mixins
- View component examples
- Store integration examples

## Key Differences Summary

### Composition API
- Uses `<script setup lang="ts">`
- Reactivity via `ref()`, `reactive()`, `computed()`
- Lifecycle hooks as functions (`onMounted`, `onUpdated`, etc.)
- Code organized by logical concern
- Better tree-shaking and TypeScript inference

### Options API
- Uses `defineComponent()`
- Reactivity via `data()` return object
- Lifecycle hooks as methods (`mounted()`, `updated()`, etc.)
- Code organized by option type
- Familiar structure for Vue 2 developers

## Notes
- Always use TypeScript (`lang="ts"`)
- Always use scoped styles (`<style scoped lang="scss">`)
- Import theme variables: `@use '@/theme/' as *;`
- Follow naming conventions: PascalCase for component names
- Include proper type definitions for props and emits
