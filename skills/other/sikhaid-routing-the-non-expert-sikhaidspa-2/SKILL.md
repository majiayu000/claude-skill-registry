---
name: sikhaid-routing
description: Use when adding routes, navigation, or understanding URL structure in SikhAid project. Covers SvelteKit file-based routing, dynamic routes with slugs, layout hierarchy, admin routes, and navigation patterns.
allowed-tools: Read, Write, Edit, Glob
---

# SikhAid Routing & Navigation

## SvelteKit File-Based Routing

### Routing Convention
- **File:** `src/routes/[path]/+page.svelte` → **URL:** `/[path]`
- **Layout:** `+layout.svelte` wraps all child routes
- **Dynamic:** `[param]` creates dynamic route segments

### Route Structure Overview
```
src/routes/
├── +layout.svelte           → Wraps ALL routes
├── +page.svelte             → / (home)
│
├── about/
│   └── +page.svelte         → /about
│
├── campaigns/
│   ├── +page.svelte         → /campaigns (all campaigns)
│   └── [slug]/
│       └── +page.svelte     → /campaigns/:slug (dynamic)
│
├── blog/
│   ├── +page.svelte         → /blog (all posts)
│   └── [slug]/
│       └── +page.svelte     → /blog/:slug (dynamic)
│
├── contact/
│   └── +page.svelte         → /contact
│
├── donate/
│   └── +page.svelte         → https://donate.sikhaid.ngo/
│
├── volunteering/
│   └── +page.svelte         → /volunteering
│
├── csr/
│   └── +page.svelte         → /csr (CSR partnerships)
│
├── payment/
│   ├── success/
│   │   └── +page.svelte     → /payment/success
│   └── failure/
│       └── +page.svelte     → /payment/failure
│
└── admin/
    ├── +layout.svelte       → Nested admin layout
    ├── +page.svelte         → /admin (dashboard)
    ├── formsubmissions/
    │   └── +page.svelte     → /admin/formsubmissions
    ├── blogs/
    │   └── +page.svelte     → /admin/blogs
    ├── campaigns/
    │   └── +page.svelte     → /admin/campaigns
    ├── donations/
    │   └── +page.svelte     → /admin/donations (Added Nov 2025)
    └── content/
        └── +page.svelte     → /admin/content (Added Nov 2025)
```

## All Routes Reference

### Public Routes

| URL | File | Purpose | Navigation Link |
|-----|------|---------|-----------------|
| `/` | `routes/+page.svelte` | Home page with hero, campaigns, impact | Header logo |
| `/about` | `routes/about/+page.svelte` | About organization | Header nav |
| `/campaigns` | `routes/campaigns/+page.svelte` | All campaigns listing | Header nav |
| `/campaigns/:slug` | `routes/campaigns/[slug]/+page.svelte` | Single campaign details | Campaign cards |
| `/blog` | `routes/blog/+page.svelte` | All blog posts | Header nav |
| `/blog/:slug` | `routes/blog/[slug]/+page.svelte` | Single blog post | Blog cards |
| `https://donate.sikhaid.ngo/` | `routeshttps://donate.sikhaid.ngo//+page.svelte` | Donation page with payment form | Header CTA, Hero CTA |
| `/contact` | `routes/contact/+page.svelte` | Contact form | Footer |
| `/volunteering` | `routes/volunteering/+page.svelte` | Volunteer opportunities & form | Header dropdown |
| `/csr` | `routes/csr/+page.svelte` | CSR partnership inquiry | Header dropdown |
| `/payment/success` | `routes/payment/success/+page.svelte` | Payment success confirmation | Razorpay redirect |
| `/payment/failure` | `routes/payment/failure/+page.svelte` | Payment failure page | Razorpay redirect |

### Protected Admin Routes

| URL | File | Purpose | Access |
|-----|------|---------|--------|
| `/admin` | `routes/admin/+page.svelte` | Admin dashboard | Login required |
| `/admin/formsubmissions` | `routes/admin/formsubmissions/+page.svelte` | View all form submissions | Login required |
| `/admin/blogs` | `routes/admin/blogs/+page.svelte` | Manage blog posts | Login required |
| `/admin/campaigns` | `routes/admin/campaigns/+page.svelte` | Manage campaigns | Login required |
| `/admin/donations` | `routes/admin/donations/+page.svelte` | View all donations (Added Nov 2024) | Login required |
| `/admin/content` | `routes/admin/content/+page.svelte` | Manage celebrity endorsements and testimonials (Added Nov 2025) | Login required |

## Layout Hierarchy

### Root Layout
**File:** `src/routes/+layout.svelte`

**Wraps:** All routes

**Contains:**
- Header component (conditionally hidden on admin routes)
- Footer component (conditionally hidden on admin routes)
- Razorpay script loader
- Page slot: `<slot />`

**Key Logic:**
```svelte
<script lang="ts">
  import { page } from '$app/stores';
  import Header from '$lib/components/Header.svelte';
  import Footer from '$lib/components/Footer.svelte';

  $: isAdminRoute = $page.url.pathname.startsWith('/admin');
</script>

{#if !isAdminRoute}
  <Header />
{/if}

<slot />

{#if !isAdminRoute}
  <Footer />
{/if}
```

### Admin Nested Layout
**File:** `src/routes/admin/+layout.svelte`

**Wraps:** All `/admin/*` routes

**Contains:**
- Admin-specific styling
- Admin navigation (if any)
- Inherits from root layout

## Dynamic Routes

### Campaign Dynamic Route
**File:** `src/routes/campaigns/[slug]/+page.svelte`

**Purpose:** Display individual campaign based on URL slug

**Pattern:**
```svelte
<script lang="ts">
  import { page } from '$app/stores';
  import { campaigns } from '$lib/data/campaigns';
  import type { Campaign } from '$lib/types/campaign';

  // Extract slug from URL
  $: slug = $page.params.slug;

  // Find campaign by slug
  $: campaign = campaigns.find((c: Campaign) => c.slug === slug);

  // Handle not found
  $: if (!campaign) {
    // Optionally redirect or show 404
  }
</script>

<div>
  <h1>{campaign.title}</h1>
  <p>{campaign.fullDescription}</p>
  <!-- Campaign content -->
</div>
```

**Example URLs:**
- `/campaigns/langar-aid` → Shows Langar Aid campaign
- `/campaigns/blanket-distribution` → Shows Blanket Distribution campaign
- `/campaigns/punjab-floods-2025` → Shows Punjab Floods campaign

### Blog Dynamic Route
**File:** `src/routes/blog/[slug]/+page.svelte`

**Purpose:** Display individual blog post based on URL slug

**Pattern:** Same as campaigns, uses `$page.params.slug`

**Example URLs:**
- `/blog/langar-seva-impact` → Shows specific blog post
- `/blog/winter-relief-2024` → Shows another blog post

## Navigation Patterns

### Programmatic Navigation
```svelte
<script lang="ts">
  import { goto } from '$app/navigation';

  function navigateToCampaign(slug: string) {
    goto(`/campaigns/${slug}`);
  }

  function goBack() {
    goto(-1); // Go back one page
  }
</script>

<button on:click={() => goto('https://donate.sikhaid.ngo/')}>
  Donate Now
</button>

<button on:click={() => navigateToCampaign('langar-aid')}>
  View Campaign
</button>
```

### Link Navigation (Standard)
```svelte
<a href="/about">About Us</a>
<a href="/campaigns">View Campaigns</a>
<a href={`/campaigns/${campaign.slug}`}>View {campaign.title}</a>
```

### Active Route Highlighting
```svelte
<script lang="ts">
  import { page } from '$app/stores';

  $: currentPath = $page.url.pathname;
  $: isActive = (path: string) => currentPath === path;
</script>

<nav>
  <a
    href="/about"
    class="nav-link"
    class:active={isActive('/about')}
  >
    About
  </a>
  <a
    href="/campaigns"
    class="nav-link"
    class:active={isActive('/campaigns')}
  >
    Campaigns
  </a>
</nav>

<style>
  .nav-link.active {
    color: var(--orange);
    font-weight: 600;
  }
</style>
```

### Dropdown Menu Navigation
**Example from Header.svelte:**
```svelte
<script lang="ts">
  let isDropdownOpen = false;
</script>

<div class="relative">
  <button
    on:click={() => isDropdownOpen = !isDropdownOpen}
    class="dropdown-trigger"
  >
    Get Involved
  </button>

  {#if isDropdownOpen}
    <div class="dropdown-menu">
      <a href="/volunteering" on:click={() => isDropdownOpen = false}>
        Volunteer
      </a>
      <a href="/csr" on:click={() => isDropdownOpen = false}>
        CSR Partnerships
      </a>
    </div>
  {/if}
</div>
```

## Admin Authentication Flow

### Login Process
1. User clicks "Admin" in Footer
2. Modal popup with password input
3. Password validation: `Raunak@123` (hardcoded in Footer.svelte:29)
4. On success: Set cookie `admin_session=raunak_${timestamp}`
5. Cookie expires after 3600 seconds (1 hour)
6. Navigate to `/admin`

### Cookie Check (Client-Side)
```javascript
// Check if admin session exists
const cookies = document.cookie.split(';');
const hasAdminSession = cookies.some(cookie =>
  cookie.trim().startsWith('admin_session=')
);

if (!hasAdminSession) {
  // Redirect to home or show login
  goto('/');
}
```

### Logout
```javascript
// Clear cookie
document.cookie = 'admin_session=; max-age=0; path=/';
goto('/');
```

## Header Navigation Structure

**File:** `src/lib/components/Header.svelte`

### Desktop Navigation
```
Logo | About | Campaigns | Blog | [Get Involved ▼] | Donate (CTA)
                                   ├─ Volunteer
                                   └─ CSR Partnerships
```

### Mobile Navigation
```
Logo                    [☰ Menu]

[When menu open:]
├─ About
├─ Campaigns
├─ Blog
├─ Get Involved
│  ├─ Volunteer
│  └─ CSR
└─ Donate
```

## Footer Navigation Structure

**File:** `src/lib/components/Footer.svelte`

### Sections
1. **About Section** - Organization description
2. **Quick Links**
   - Home
   - About Us
   - Campaigns
   - Contact
3. **Get Involved**
   - Volunteer
   - CSR Partnerships
4. **Contact Info**
   - Address
   - Email
   - Phone
5. **Social Media Links**
6. **Admin Login** (hidden link/button)

## Scroll Behaviors

### Smooth Scroll to Section
```svelte
<script lang="ts">
  function scrollToDonation() {
    const element = document.getElementById('donation-form');
    element?.scrollIntoView({ behavior: 'smooth' });
  }
</script>

<button on:click={scrollToDonation}>
  Donate Now
</button>
```

### Scroll to Top on Navigation
```svelte
<script lang="ts">
  import { afterNavigate } from '$app/navigation';

  afterNavigate(() => {
    window.scrollTo(0, 0);
  });
</script>
```

## Route Parameters & Query Strings

### Accessing Route Parameters
```svelte
<script lang="ts">
  import { page } from '$app/stores';

  // URL: /campaigns/langar-aid
  $: slug = $page.params.slug; // 'langar-aid'
</script>
```

### Accessing Query Parameters
```svelte
<script lang="ts">
  import { page } from '$app/stores';

  // URL: /campaigns?category=education&status=ongoing
  $: category = $page.url.searchParams.get('category'); // 'education'
  $: status = $page.url.searchParams.get('status'); // 'ongoing'
</script>
```

### Setting Query Parameters
```svelte
<script lang="ts">
  import { goto } from '$app/navigation';

  function filterCampaigns(category: string) {
    goto(`/campaigns?category=${category}`);
  }
</script>

<button on:click={() => filterCampaigns('education')}>
  Education Campaigns
</button>
```

## Preloading Patterns

### Hover Preload (Default)
SvelteKit automatically preloads routes on hover (configured in `app.html`):
```html
<body data-sveltekit-preload-data="hover">
```

### Programmatic Preload
```svelte
<script lang="ts">
  import { preloadData } from '$app/navigation';

  async function preloadCampaign(slug: string) {
    await preloadData(`/campaigns/${slug}`);
  }
</script>

<a
  href="/campaigns/langar-aid"
  on:mouseenter={() => preloadCampaign('langar-aid')}
>
  Langar Aid Campaign
</a>
```

## Adding New Routes

### Step-by-Step: Add New Public Page

1. **Create route file:**
   ```
   src/routes/new-page/+page.svelte
   ```

2. **Add basic page structure:**
   ```svelte
   <script lang="ts">
     // Imports and logic
   </script>

   <main class="container mx-auto px-4 py-16">
     <h1 class="text-5xl font-bold text-navy-custom mb-8">
       New Page Title
     </h1>
     <!-- Page content -->
   </main>
   ```

3. **Add to Header navigation:**
   Open `src/lib/components/Header.svelte`, add link:
   ```svelte
   <a href="/new-page" class:active={isActive('/new-page')}>
     New Page
   </a>
   ```

4. **Test route:**
   - Navigate to `http://localhost:5173/new-page`
   - Verify Header/Footer appear
   - Check mobile responsiveness

### Step-by-Step: Add Dynamic Route

1. **Create dynamic route folder:**
   ```
   src/routes/resources/[id]/+page.svelte
   ```

2. **Access parameter:**
   ```svelte
   <script lang="ts">
     import { page } from '$app/stores';
     $: resourceId = $page.params.id;
   </script>
   ```

3. **Fetch or filter data:**
   ```svelte
   <script lang="ts">
     import { resources } from '$lib/data/resources';
     $: resource = resources.find(r => r.id === resourceId);
   </script>
   ```

### Step-by-Step: Add Admin Route

1. **Create route under admin:**
   ```
   src/routes/admin/new-section/+page.svelte
   ```

2. **Add authentication check:**
   ```svelte
   <script lang="ts">
     import { onMount } from 'svelte';
     import { goto } from '$app/navigation';

     onMount(() => {
       const hasSession = document.cookie.includes('admin_session=');
       if (!hasSession) {
         goto('/');
       }
     });
   </script>
   ```

3. **Add to admin navigation** (if admin has nav menu)

4. **Route automatically inherits admin layout** (no Header/Footer)

## Common Routing Patterns

### Redirect After Action
```svelte
<script lang="ts">
  import { goto } from '$app/navigation';

  async function handleSubmit() {
    await submitForm();
    goto('/thank-you');
  }
</script>
```

### Conditional Navigation
```svelte
<script lang="ts">
  import { goto } from '$app/navigation';

  function navigateBasedOnRole(role: string) {
    if (role === 'admin') {
      goto('/admin');
    } else {
      goto('/dashboard');
    }
  }
</script>
```

### External Links
```svelte
<!-- Opens in new tab -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  External Link
</a>

<!-- Programmatic -->
<button on:click={() => window.open('https://example.com', '_blank')}>
  Open External
</button>
```

## Route-Specific Metadata

### Page Title & Meta Tags
```svelte
<svelte:head>
  <title>Campaign Name - Sikh Aid</title>
  <meta name="description" content="Campaign description..." />
  <meta property="og:title" content="Campaign Name" />
  <meta property="og:image" content="/images/campaign.jpg" />
</svelte:head>

<main>
  <!-- Page content -->
</main>
```

## When to Use This Skill
- Adding new pages or routes
- Creating dynamic routes with parameters
- Understanding navigation structure
- Implementing navigation patterns
- Setting up admin routes
- Working with route parameters or query strings
- Configuring layouts and route hierarchies

## Related Skills
- `sikhaid-overview` - Project structure and setup
- `sikhaid-components` - Header and navigation components
- `sikhaid-data` - Data loading for dynamic routes
