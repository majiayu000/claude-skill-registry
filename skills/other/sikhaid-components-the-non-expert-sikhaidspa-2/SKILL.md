---
name: sikhaid-components
description: Use when creating, modifying, or understanding Svelte components in SikhAid project. Covers component naming conventions, file organization, component hierarchy, import patterns, and reusable UI patterns.
allowed-tools: Read, Edit, Write, Glob
---

# SikhAid Component Patterns

## Component Hierarchy

### 1. Layout Components
**Purpose:** Wrapper components that provide consistent structure across pages

- **`src/routes/+layout.svelte`** - Root layout
  - Wraps all pages with Header and Footer
  - Conditionally hides Header/Footer on admin routes
  - Loads Razorpay script
  - Includes global styles

- **`src/routes/admin/+layout.svelte`** - Admin nested layout
  - Adds admin-specific styling and structure
  - Inherits from root layout

### 2. Page Components
**Purpose:** Route-specific entry points

- Located in `src/routes/`
- Named `+page.svelte`
- Compose feature and UI components
- Example: `src/routes/+page.svelte` (home page)

### 3. Feature Components
**Purpose:** Reusable sections that combine multiple UI elements

**Location:** `src/lib/components/`

Examples:
- `Header.svelte` - Navigation with dropdown menu, responsive mobile menu
- `Footer.svelte` - Footer with quick links, admin login modal
- `Hero.svelte` - Hero section with background image and CTA
- `CampaignCarousel.svelte` - Featured campaigns with Swiper/carousel
- `PaymentForm.svelte` - Complete donation form with Razorpay integration

**Home-specific features:**
- Location: `src/lib/components/home/`
- Examples: `ImpactCounterSection.svelte`, `MissionSection.svelte`

**Admin-specific features:**
- Location: `src/lib/components/admin/`
- Examples: `SubmissionModal.svelte`

### 4. UI Components
**Purpose:** Small, highly reusable elements

- Buttons, inputs, cards, modals
- Often accept props for customization
- Example: Modal components, form inputs with validation

## Naming Conventions

### Component Files
- **Format:** PascalCase
- **Pattern:** `[Descriptor][Type].svelte`
- **Examples:**
  - `PaymentForm.svelte` - Form for payments
  - `CampaignCarousel.svelte` - Carousel for campaigns
  - `ImpactCounterSection.svelte` - Section with impact counters
  - `SubmissionModal.svelte` - Modal for form submissions

### Component Organization
```
src/lib/components/
├── Header.svelte           # Global components at root
├── Footer.svelte
├── PaymentForm.svelte
├── Hero.svelte
├── CampaignCarousel.svelte
├── home/                   # Home page specific
│   ├── ImpactCounterSection.svelte
│   ├── MissionSection.svelte
│   └── ...
└── admin/                  # Admin specific
    ├── SubmissionModal.svelte
    └── ...
```

## Component Structure Pattern

### Standard Component Template
```svelte
<script lang="ts">
  // 1. Imports
  import { Icon } from '@iconify/svelte';
  import { storeName } from '$lib/stores/storeName';

  // 2. Props (if any)
  export let propName: string;
  export let optionalProp: number = 0;

  // 3. Local state
  let localVariable = '';
  let isLoading = false;

  // 4. Reactive declarations
  $: computedValue = propName.toUpperCase();

  // 5. Functions
  async function handleSubmit() {
    // Event handler logic
  }
</script>

<!-- 6. Markup -->
<div class="container">
  <!-- Component content -->
</div>

<!-- 7. Component-specific styles (if needed) -->
<style>
  .custom-class {
    /* Scoped styles */
  }
</style>
```

## Import Patterns

### Importing Components
```svelte
// From lib/components
import Header from '$lib/components/Header.svelte';
import PaymentForm from '$lib/components/PaymentForm.svelte';

// From subdirectories
import ImpactCounter from '$lib/components/home/ImpactCounterSection.svelte';
import SubmissionModal from '$lib/components/admin/SubmissionModal.svelte';
```

### Importing Stores
```svelte
import { selectedAmount, setDonationAmount } from '$lib/stores/donation';
import { contactSubmissions } from '$lib/stores/contact';
```

### Importing Types
```svelte
import type { Campaign } from '$lib/types/campaign';
import type { ContactSubmission } from '$lib/stores/contact';
```

### Importing Data
```svelte
import { campaigns } from '$lib/data/campaigns';
```

### Importing Icons
```svelte
import { Icon } from '@iconify/svelte';

// Usage:
<Icon icon="mdi:heart" />
<Icon icon="mdi:email" />
```

## Common Component Patterns

### 1. Form Component Pattern
**Example:** `PaymentForm.svelte`

**Key Features:**
- Two-way binding: `bind:value={formData.field}`
- Validation on submit
- Loading states: `isSubmitting`
- Success/error messages
- Prevent default: `on:submit|preventDefault={handleSubmit}`

```svelte
<script lang="ts">
  let formData = { name: '', email: '', phone: '' };
  let isSubmitting = false;
  let errorMessage = '';

  async function handleSubmit() {
    if (!validateForm()) return;

    isSubmitting = true;
    try {
      // Submit logic
      await addToFirestore(formData);
    } catch (error) {
      errorMessage = 'Submission failed';
    } finally {
      isSubmitting = false;
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <input type="text" bind:value={formData.name} required />
  <button type="submit" disabled={isSubmitting}>
    {isSubmitting ? 'Submitting...' : 'Submit'}
  </button>
</form>
```

### 2. Navigation Component Pattern
**Example:** `Header.svelte`

**Key Features:**
- Dropdown menus with state
- Mobile responsive menu toggle
- Active route highlighting with `$page.url.pathname`
- Conditional rendering

```svelte
<script lang="ts">
  import { page } from '$app/stores';

  let isMenuOpen = false;
  let isDropdownOpen = false;

  $: currentPath = $page.url.pathname;
  $: isActive = (path: string) => currentPath === path;
</script>

<nav>
  <a href="/about" class:active={isActive('/about')}>About</a>

  <button on:click={() => isMenuOpen = !isMenuOpen}>
    Menu
  </button>
</nav>
```

### 3. Modal Component Pattern
**Example:** `SubmissionModal.svelte` in admin

**Key Features:**
- Show/hide state
- Backdrop click to close
- Slot for content
- Escape key handling

```svelte
<script lang="ts">
  export let isOpen = false;
  export let onClose: () => void;

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }
</script>

{#if isOpen}
  <div class="modal-backdrop" on:click={handleBackdropClick}>
    <div class="modal-content">
      <slot />
      <button on:click={onClose}>Close</button>
    </div>
  </div>
{/if}
```

### 4. Data Display Component Pattern
**Example:** Campaign cards, blog cards

**Key Features:**
- Props for data
- Click handlers
- Conditional rendering with `{#if}`
- Iteration with `{#each}`

```svelte
<script lang="ts">
  import type { Campaign } from '$lib/types/campaign';
  import { campaigns } from '$lib/data/campaigns';

  function handleCampaignClick(slug: string) {
    goto(`/campaigns/${slug}`);
  }
</script>

<div class="grid">
  {#each campaigns as campaign}
    <div class="card" on:click={() => handleCampaignClick(campaign.slug)}>
      <h3>{campaign.title}</h3>
      <p>{campaign.shortDescription}</p>
      {#if campaign.status === 'ongoing'}
        <span class="badge">Active</span>
      {/if}
    </div>
  {/each}
</div>
```

## Reactivity Patterns

### Store Subscriptions
```svelte
<script lang="ts">
  import { selectedAmount } from '$lib/stores/donation';

  // Auto-subscribes with $ prefix
  $: amount = $selectedAmount;
</script>

<div>Selected: ₹{$selectedAmount}</div>
```

### Reactive Declarations
```svelte
<script lang="ts">
  let count = 0;

  // Recomputes when count changes
  $: doubled = count * 2;

  // Reactive statement
  $: if (count > 10) {
    console.log('Count exceeded 10!');
  }
</script>
```

### Reactive Bindings
```svelte
<script lang="ts">
  let value = '';

  $: valueLength = value.length;
</script>

<input bind:value />
<p>Length: {valueLength}</p>
```

## Event Handling Patterns

### Standard Events
```svelte
<button on:click={handleClick}>Click</button>
<form on:submit|preventDefault={handleSubmit}>...</form>
<input on:input={handleInput} on:blur={handleBlur} />
```

### Event Modifiers
- `preventDefault` - Prevent default behavior
- `stopPropagation` - Stop event bubbling
- `once` - Fire handler only once
- `self` - Only fire if event.target is the element itself

```svelte
<form on:submit|preventDefault={handleSubmit}>
<div on:click|self={handleBackdrop}>
```

### Custom Events (Component Communication)
```svelte
<!-- Child component -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function emitEvent() {
    dispatch('custom-event', { data: 'value' });
  }
</script>

<!-- Parent component -->
<ChildComponent on:custom-event={handleCustomEvent} />
```

## Styling Patterns

### Tailwind Classes (Primary Method)
```svelte
<div class="container mx-auto px-4 py-8">
  <h1 class="text-3xl md:text-5xl font-bold text-navy-custom">
    Title
  </h1>
</div>
```

### Conditional Classes
```svelte
<div class="btn" class:active={isActive} class:disabled={isDisabled}>
  Button
</div>
```

### Component-Scoped Styles (When Needed)
```svelte
<style>
  .custom-animation {
    animation: fade-in 0.6s ease-out;
  }

  /* Scoped to this component only */
  h1 {
    color: var(--navy);
  }
</style>
```

## Component Communication

### Parent → Child (Props)
```svelte
<!-- Parent -->
<ChildComponent title="Hello" count={5} />

<!-- Child -->
<script lang="ts">
  export let title: string;
  export let count: number;
</script>
```

### Child → Parent (Events)
```svelte
<!-- Child -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
</script>
<button on:click={() => dispatch('clicked', { data })}>Click</button>

<!-- Parent -->
<Child on:clicked={handleClick} />
```

### Sibling Components (Stores)
```svelte
<!-- Component A -->
<script lang="ts">
  import { selectedAmount } from '$lib/stores/donation';
  $selectedAmount = 1000;
</script>

<!-- Component B -->
<script lang="ts">
  import { selectedAmount } from '$lib/stores/donation';
</script>
<div>Amount: {$selectedAmount}</div>
```

## Accessibility Patterns

### Semantic HTML
```svelte
<nav>...</nav>
<main>...</main>
<section>...</section>
<form>...</form>
```

### ARIA Labels
```svelte
<button aria-label="Close menu" on:click={closeMenu}>
  <Icon icon="mdi:close" />
</button>

<input
  type="email"
  aria-label="Email address"
  aria-required="true"
/>
```

### Form Labels
```svelte
<label for="name">Full Name *</label>
<input id="name" name="name" type="text" required />
```

## When to Use This Skill
- Creating new Svelte components
- Refactoring existing components
- Understanding component structure
- Implementing forms, navigation, or modals
- Setting up component communication
- Adding interactivity or reactivity

## Related Skills
- `sikhaid-styling` - Tailwind patterns and design system
- `sikhaid-forms` - Form-specific patterns and validation
- `sikhaid-data` - Store usage and data fetching
