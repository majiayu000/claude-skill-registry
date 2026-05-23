---
name: grove-vineyard
description: Build a Vineyard showcase page for any Grove property using @autumnsgrove/groveengine/vineyard components. Vineyard is the consistent /vineyard route where each tool demos its features, documents its API, and shows its roadmap. Use when creating or updating a property's vineyard page.
---

# Grove Vineyard Skill

## When to Activate

Activate this skill when:
- Creating a `/vineyard` route for a Grove property
- Adding features or demos to an existing vineyard page
- User mentions "vineyard", "showcase page", or "tool demo page"
- Implementing feature cards, roadmaps, or demo containers for a tool

## What Is Vineyard?

Every Grove property implements a `/vineyard` route on its subdomain — a consistent way to explore what each tool does, see working demos, and understand the roadmap.

```
amber.grove.place/vineyard      → Storage showcase
ivy.grove.place/vineyard        → Email client showcase
foliage.grove.place/vineyard    → Theming showcase
meadow.grove.place/vineyard     → Social layer showcase
heartwood.grove.place/vineyard  → Auth showcase
forage.grove.place/vineyard     → Domain discovery showcase
```

## Package

Vineyard lives inside the GroveEngine monorepo at `packages/vineyard` and is re-exported through the engine. No separate install needed — it comes with GroveEngine.

```typescript
import { VineyardLayout, FeatureCard, StatusBadge, ... } from '@autumnsgrove/groveengine/vineyard';
```

## Available Components

| Component | Purpose |
|-----------|---------|
| `VineyardLayout` | Full page wrapper — hero, status badge, philosophy quote, related tools footer |
| `FeatureCard` | Showcase a feature with icon, status, description, and optional demo slot |
| `StatusBadge` | Status pill: ready, preview, demo, coming-soon, in-development |
| `DemoContainer` | Wrapper for interactive demos with mock data indicator |
| `CodeExample` | Code block with language label, filename, and copy-to-clipboard |
| `TierGate` | Tier-based access control with blur preview and upgrade prompt |
| `RoadmapSection` | Visual timeline: built / in-progress / planned |
| `AuthButton` | Better Auth sign in/out button |
| `UserMenu` | User profile menu with avatar and email |

## Types

```typescript
type VineyardStatus = 'ready' | 'preview' | 'demo' | 'coming-soon' | 'in-development';
type GroveTool = 'amber' | 'ivy' | 'foliage' | 'meadow' | 'rings' | 'trails' | 'heartwood' | 'forage';
type GroveTier = 'seedling' | 'sapling' | 'oak' | 'grove';
```

## Minimal Implementation

Create `src/routes/vineyard/+page.svelte`:

```svelte
<script lang="ts">
  import {
    VineyardLayout,
    FeatureCard,
    RoadmapSection,
    DemoContainer
  } from '@autumnsgrove/groveengine/vineyard';
</script>

<VineyardLayout
  tool="amber"
  tagline="Your files, preserved"
  status="preview"
>
  <!-- Feature Cards -->
  <div class="feature-grid">
    <FeatureCard
      title="Storage Overview"
      description="See usage across posts and media"
      status="ready"
      icon="HardDrive"
    />

    <FeatureCard
      title="File Browser"
      description="Browse and manage uploaded files"
      status="ready"
      icon="FolderOpen"
    />

    <FeatureCard
      title="Export Your Data"
      description="Download everything in one click"
      status="coming-soon"
      icon="Download"
    />
  </div>

  <!-- Roadmap -->
  <RoadmapSection
    built={['Core storage view', 'Usage breakdown', 'File browser']}
    inProgress={['Export functionality']}
    planned={['Bulk delete', 'Storage alerts', 'External backup']}
  />
</VineyardLayout>

<style>
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
  }
</style>
```

## Component Details

### VineyardLayout

Handles the full page structure automatically:
- **Hero**: Tool name (capitalized from `tool` prop), tagline, status badge, philosophy quote
- **Content**: Renders children in a max-width container with padding
- **Footer**: "Works well with" section linking related tools' vineyards

```svelte
<VineyardLayout tool="ivy" tagline="Messages that grow on you" status="in-development">
  <!-- All your content goes here -->
</VineyardLayout>
```

The philosophy quotes and related tool mappings are built-in. No configuration needed.

### FeatureCard

Icons are any valid [lucide-svelte](https://lucide.dev) icon name as a string:

```svelte
<FeatureCard
  title="Theme Picker"
  description="Choose from curated seasonal themes"
  status="ready"
  icon="Palette"
>
  {#snippet demo()}
    <!-- Optional: interactive demo renders below the description -->
    <ThemePicker themes={sampleThemes} />
  {/snippet}
</FeatureCard>
```

### DemoContainer

Wraps interactive demos with a header, description, and optional "Mock Data" indicator:

```svelte
<DemoContainer
  title="Email Composer"
  description="Try the rich text editor"
  mockData={true}
>
  <RichTextEditor value={sampleDraft} />
</DemoContainer>
```

When `mockData={true}`:
- Shows a blue "Mock Data" pill in the header
- Adds a dashed blue border around the demo content

### CodeExample

Code blocks with copy-to-clipboard and language/filename labels:

```svelte
<CodeExample language="typescript" filename="src/routes/+layout.svelte">
{`import { initAmber } from '@autumnsgrove/amber';

const storage = initAmber({
  tenant: 'my-site',
  tier: 'sapling'
});`}
</CodeExample>
```

### TierGate

Shows content only if user meets tier requirement. Otherwise shows blur preview + upgrade prompt:

```svelte
<TierGate required="oak" current={userTier} showPreview={true}>
  <AdvancedStoragePanel />

  {#snippet fallback()}
    <!-- Optional custom fallback (default shows upgrade button) -->
    <p>Upgrade to Oak for advanced storage features</p>
  {/snippet}
</TierGate>
```

Tier hierarchy: `seedling` < `sapling` < `oak` < `grove`

### RoadmapSection

Three-column (desktop) / stacked (mobile) timeline:

```svelte
<RoadmapSection
  built={['Feature A', 'Feature B']}
  inProgress={['Feature C']}
  planned={['Feature D', 'Feature E']}
/>
```

- Built items get green dots
- In-progress items get pulsing orange dots
- Planned items get hollow gray circles

### Authentication

```svelte
<script>
  import { AuthButton, UserMenu, getSession } from '@autumnsgrove/groveengine/vineyard';
  import { onMount } from 'svelte';

  let user = $state(null);

  onMount(async () => {
    const session = await getSession();
    user = session.user;
  });
</script>

{#if user}
  <UserMenu showAvatar={true} showEmail={true} />
{:else}
  <AuthButton provider="google" signInText="Sign in to explore" />
{/if}
```

## Status Badge Meanings

| Status | Visual | Use When |
|--------|--------|----------|
| `ready` | Green solid pill | Feature is complete and stable |
| `preview` | Amber dashed border | Functional but API may change |
| `demo` | Blue solid pill | Interactive example, not real data |
| `coming-soon` | Gray subtle pill | Designed but not built yet |
| `in-development` | Orange pulsing pill | Actively being built right now |

## Design System

Vineyard components use Grove's built-in aesthetic:
- **Colors**: Amber tones (#f59e0b, #d97706) on stone neutrals
- **Glass**: Semi-transparent backgrounds with backdrop-blur
- **Typography**: Lexend font (loaded by VineyardLayout)
- **Interactions**: Hover lift on cards, smooth transitions

No additional styling framework needed — components are self-contained with scoped CSS.

## Content Strategy

### For Ready Tools
- Working demos with real or realistic mock data
- Complete feature cards with all statuses "ready"
- Full code examples and API reference
- Getting started guide

### For Preview/In Development Tools
- Mix of "ready" and "coming-soon" feature cards
- Demo containers with `mockData={true}`
- Roadmap section showing progress
- TierGate for features not yet available

### For Coming Soon Tools
- Minimal vineyard: VineyardLayout + philosophy + roadmap
- All feature cards as "coming-soon"
- No interactive demos needed yet

## Grove Terminology

When vineyard pages reference Grove-themed terms (tool names, feature names, user roles), use GroveTerm components to respect the user's Grove Mode setting. New visitors see standard terms by default.

```svelte
import { GroveTerm, GroveText } from '@autumnsgrove/groveengine/ui';
import groveTermManifest from '$lib/data/grove-term-manifest.json';

<!-- Use GroveText for data-driven content with [[term]] syntax -->
<GroveText content="Manage your [[bloom|posts]] and [[garden|blog]] appearance." manifest={groveTermManifest} />

<!-- Or GroveTerm for individual interactive terms -->
<p>Customize how your <GroveTerm term="garden" manifest={groveTermManifest} /> looks.</p>
```

## Checklist

Before shipping a vineyard page:
- [ ] `VineyardLayout` with correct `tool`, `tagline`, and `status`
- [ ] At least 3 `FeatureCard` components with appropriate statuses
- [ ] `RoadmapSection` with honest built/inProgress/planned arrays
- [ ] At least one interactive demo (even with mock data)
- [ ] Works on mobile (feature grid responsive)
- [ ] Icons are valid lucide-svelte names
- [ ] Status badges accurately reflect feature state
- [ ] Grove terminology uses GroveTerm components (not hardcoded)
