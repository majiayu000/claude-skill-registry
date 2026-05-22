---
name: "TailAdmin UI Patterns"
description: "TailAdmin dashboard UI framework patterns and Tailwind CSS classes. ALWAYS use this skill when: (1) Building any dashboard or admin panel interface, (2) Creating data tables, cards, charts, or metrics displays, (3) Implementing forms, buttons, alerts, or modals, (4) Building navigation (sidebar, header, breadcrumbs), (5) Any UI work that should follow TailAdmin design. This skill REQUIRES fetching from the official GitHub repository to ensure accurate class usage - NEVER invent classes. Trigger keywords: TailwindCSS, admin, UI, styling, components, dashboard, tailadmin, tables, charts"
---

# TailAdmin UI Patterns Skill

## When to Use This Skill

**ALWAYS invoke this skill for:**
- Dashboard interfaces and admin panels
- Data tables and grid layouts
- Charts, metrics, and KPI displays
- Form components (inputs, selects, checkboxes, toggles)
- Card layouts and stat boxes
- Navigation (sidebar, header, breadcrumbs)
- Buttons, badges, alerts, and modals
- Any UI requiring TailAdmin styling

## Critical Rule: FETCH BEFORE IMPLEMENTING

**NEVER guess or invent classes. ALWAYS fetch from the official repository first.**

```bash
# MANDATORY: Fetch TailAdmin source before ANY UI work
git clone --depth 1 https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template.git /tmp/tailadmin 2>/dev/null || echo "Already cloned"

# Verify the clone
ls /tmp/tailadmin/src/
```

## Repository Reference

| Item | Value |
|------|-------|
| **Repository** | https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template |
| **Branch** | `main` |
| **Source Path** | `src/` |
| **CSS Config** | `tailwind.config.js` |
| **Custom CSS** | `src/css/style.css` |

## Mandatory Fetch Commands

**Before implementing ANY TailAdmin UI, run these commands:**

```bash
# 1. Clone repository (if not already done)
git clone --depth 1 https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template.git /tmp/tailadmin 2>/dev/null

# 2. Check available page templates
ls /tmp/tailadmin/src/*.html

# 3. Check partials (reusable components)
ls /tmp/tailadmin/src/partials/

# 4. View Tailwind config for custom classes
cat /tmp/tailadmin/tailwind.config.js

# 5. View custom CSS definitions
cat /tmp/tailadmin/src/css/style.css
```

## Finding Specific Components

```bash
# Find dashboard/stats card patterns
grep -A 50 'stat\|kpi\|metric' /tmp/tailadmin/src/index.html | head -80

# Find table patterns
cat /tmp/tailadmin/src/tables.html | head -200

# Find form patterns  
cat /tmp/tailadmin/src/form-elements.html | head -200

# Find button patterns
grep -B 5 -A 10 'btn\|button' /tmp/tailadmin/src/*.html | head -100

# Find card patterns
grep -B 5 -A 20 'rounded-sm border' /tmp/tailadmin/src/*.html | head -100

# Find sidebar patterns
cat /tmp/tailadmin/src/partials/sidebar.html

# Find header patterns
cat /tmp/tailadmin/src/partials/header.html

# Find modal patterns
grep -B 5 -A 30 'modal' /tmp/tailadmin/src/*.html | head -100

# Find alert patterns
cat /tmp/tailadmin/src/alerts.html | head -150

# Search for ANY specific class
grep -r 'class-name-here' /tmp/tailadmin/src/
```

## Class Verification Process

**Before using ANY class, verify it exists:**

```bash
# Step 1: Search in HTML files
grep -r 'bg-boxdark' /tmp/tailadmin/src/ | head -5

# Step 2: Search in Tailwind config (for custom classes)
grep 'boxdark' /tmp/tailadmin/tailwind.config.js

# Step 3: Search in custom CSS
grep 'boxdark' /tmp/tailadmin/src/css/style.css

# If class not found in ANY of these = DO NOT USE IT
```

## TailAdmin Custom Tailwind Configuration

**IMPORTANT**: These custom classes are defined in `tailwind.config.js`. Always verify before using:

```bash
# View the full Tailwind config to see ALL custom values
cat /tmp/tailadmin/tailwind.config.js
```

### Custom Colors (from tailwind.config.js)

```javascript
// Verify with: grep -A 100 'colors:' /tmp/tailadmin/tailwind.config.js
colors: {
  current: 'currentColor',
  transparent: 'transparent',
  white: '#FFFFFF',
  black: '#1C2434',
  'black-2': '#010101',
  body: '#64748B',
  bodydark: '#AEB7C0',
  bodydark1: '#DEE4EE',
  bodydark2: '#8A99AF',
  primary: '#3C50E0',
  secondary: '#80CAEE',
  stroke: '#E2E8F0',
  gray: '#EFF4FB',
  graydark: '#333A48',
  'gray-2': '#F7F9FC',
  'gray-3': '#FAFAFA',
  whiten: '#F1F5F9',
  whiter: '#F5F7FD',
  boxdark: '#24303F',
  'boxdark-2': '#1A222C',
  strokedark: '#2E3A47',
  'form-strokedark': '#3d4d60',
  'form-input': '#1d2a39',
  'meta-1': '#DC3545',
  'meta-2': '#EFF2F7',
  'meta-3': '#10B981',
  'meta-4': '#313D4A',
  'meta-5': '#259AE6',
  'meta-6': '#FFBA00',
  'meta-7': '#FF6766',
  'meta-8': '#F0950C',
  'meta-9': '#E5E7EB',
  'meta-10': '#0FADCF',
  success: '#219653',
  danger: '#D34053',
  warning: '#FFA70B',
}
```

### Custom Spacing (from tailwind.config.js)

```javascript
// Verify with: grep -A 50 'spacing:' /tmp/tailadmin/tailwind.config.js
// Or check extend section
spacing: {
  '4.5': '1.125rem',   // 18px
  '5.5': '1.375rem',   // 22px
  '6.5': '1.625rem',   // 26px
  '7.5': '1.875rem',   // 30px
  '8.5': '2.125rem',   // 34px
  '9.5': '2.375rem',   // 38px
  '10.5': '2.625rem',  // 42px
  '11': '2.75rem',     // 44px
  '11.5': '2.875rem',  // 46px
  '12.5': '3.125rem',  // 50px
  '13': '3.25rem',     // 52px
  '14': '3.5rem',      // 56px
  '15': '3.75rem',     // 60px
  '16': '4rem',        // 64px
  '17': '4.25rem',     // 68px
  '18': '4.5rem',      // 72px
  '19': '4.75rem',     // 76px
  '21': '5.25rem',     // 84px
  '22': '5.5rem',      // 88px
  '22.5': '5.625rem',  // 90px
  '25': '6.25rem',     // 100px
  '27': '6.75rem',     // 108px
  '29': '7.25rem',     // 116px
  '30': '7.5rem',      // 120px
  '35': '8.75rem',     // 140px
  '45': '11.25rem',    // 180px
  '46': '11.5rem',     // 184px
  '54': '13.5rem',     // 216px
  '55': '13.75rem',    // 220px
  '60': '15rem',       // 240px
  '65': '16.25rem',    // 260px
  '70': '17.5rem',     // 280px
  '72.5': '18.125rem', // 290px - Sidebar width
  '90': '22.5rem',     // 360px
  '125': '31.25rem',   // 500px
  '142.5': '35.625rem',// 570px - Modal width
  '180': '45rem',      // 720px
  '203': '50.75rem',   // 812px
  '230': '57.5rem',    // 920px
}
```

### Custom Shadows

```javascript
// Verify with: grep -A 20 'boxShadow:' /tmp/tailadmin/tailwind.config.js
boxShadow: {
  default: '0px 8px 13px -3px rgba(0, 0, 0, 0.07)',
  card: '0px 1px 3px rgba(0, 0, 0, 0.12)',
  'card-2': '0px 1px 2px rgba(0, 0, 0, 0.05)',
  switcher: '0px 2px 4px rgba(0, 0, 0, 0.2), inset 0px 2px 2px #FFFFFF, inset 0px -1px 1px rgba(0, 0, 0, 0.1)',
  'switch-1': '0px 0px 5px rgba(0, 0, 0, 0.15)',
  1: '0px 1px 3px rgba(0, 0, 0, 0.08)',
  2: '0px 1px 4px rgba(0, 0, 0, 0.12)',
  3: '0px 1px 5px rgba(0, 0, 0, 0.14)',
  4: '0px 4px 10px rgba(0, 0, 0, 0.12)',
  5: '0px 1px 1px rgba(0, 0, 0, 0.15)',
  6: '0px 3px 15px rgba(0, 0, 0, 0.1)',
  7: '-5px 0 0 #313D4A, 5px 0 0 #313D4A',
  8: '1px 0 0 #313D4A, -1px 0 0 #313D4A, 0 1px 0 #313D4A, 0 -1px 0 #313D4A, 0 3px 13px rgb(0 0 0 / 8%)',
}

// Drop shadows
dropShadow: {
  1: '0px 1px 0px #E2E8F0',
  2: '0px 1px 4px rgba(0, 0, 0, 0.12)',
}
```

## Layout Structure

### Main Layout Wrapper

```html
<!-- Main container with dark mode support -->
<div class="flex h-screen overflow-hidden">
  <!-- Sidebar -->
  <aside class="absolute left-0 top-0 z-9999 flex h-screen w-72.5 flex-col overflow-y-hidden bg-black duration-300 ease-linear dark:bg-boxdark lg:static lg:translate-x-0">
    <!-- Sidebar content -->
  </aside>

  <!-- Content Area -->
  <div class="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
    <!-- Header -->
    <header class="sticky top-0 z-999 flex w-full bg-white drop-shadow-1 dark:bg-boxdark dark:drop-shadow-none">
      <!-- Header content -->
    </header>

    <!-- Main Content -->
    <main>
      <div class="mx-auto max-w-screen-2xl p-4 md:p-6 2xl:p-10">
        <!-- Page content -->
      </div>
    </main>
  </div>
</div>
```

### Page Header / Breadcrumb

```html
<!-- Breadcrumb -->
<div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
  <h2 class="text-title-md2 font-semibold text-black dark:text-white">
    Page Title
  </h2>

  <nav>
    <ol class="flex items-center gap-2">
      <li>
        <a class="font-medium" href="index.html">Dashboard /</a>
      </li>
      <li class="font-medium text-primary">Current Page</li>
    </ol>
  </nav>
</div>
```

## Card Components

### Basic Card

```html
<div class="rounded-sm border border-stroke bg-white px-5 pt-6 pb-2.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
  <h4 class="mb-6 text-xl font-semibold text-black dark:text-white">
    Card Title
  </h4>
  
  <!-- Card content -->
</div>
```

### Stats Card (KPI Card)

```html
<div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
  <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
    <!-- Icon SVG -->
    <svg class="fill-primary dark:fill-white" width="22" height="16" viewBox="0 0 22 16">
      <!-- SVG path -->
    </svg>
  </div>

  <div class="mt-4 flex items-end justify-between">
    <div>
      <h4 class="text-title-md font-bold text-black dark:text-white">
        $3.456K
      </h4>
      <span class="text-sm font-medium">Total Views</span>
    </div>

    <span class="flex items-center gap-1 text-sm font-medium text-meta-3">
      0.43%
      <svg class="fill-meta-3" width="10" height="11" viewBox="0 0 10 11">
        <!-- Up arrow SVG -->
      </svg>
    </span>
  </div>
</div>
```

### Card with Chart

```html
<div class="col-span-12 rounded-sm border border-stroke bg-white px-5 pt-7.5 pb-5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-8">
  <div class="flex flex-wrap items-start justify-between gap-3 sm:flex-nowrap">
    <div class="flex w-full flex-wrap gap-3 sm:gap-5">
      <div class="flex min-w-47.5">
        <span class="mt-1 mr-2 flex h-4 w-full max-w-4 items-center justify-center rounded-full border border-primary">
          <span class="block h-2.5 w-full max-w-2.5 rounded-full bg-primary"></span>
        </span>
        <div class="w-full">
          <p class="font-semibold text-primary">Total Revenue</p>
          <p class="text-sm font-medium">12.04.2022 - 12.05.2022</p>
        </div>
      </div>
    </div>
    
    <div class="flex w-full max-w-45 justify-end">
      <!-- Period selector dropdown -->
    </div>
  </div>

  <!-- Chart container -->
  <div id="chartOne" class="-ml-5"></div>
</div>
```

## Tables

### Basic Table

```html
<div class="rounded-sm border border-stroke bg-white px-5 pt-6 pb-2.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
  <h4 class="mb-6 text-xl font-semibold text-black dark:text-white">
    Table Title
  </h4>

  <div class="flex flex-col">
    <!-- Table Header -->
    <div class="grid grid-cols-3 rounded-sm bg-gray-2 dark:bg-meta-4 sm:grid-cols-5">
      <div class="p-2.5 xl:p-5">
        <h5 class="text-sm font-medium uppercase xsm:text-base">Source</h5>
      </div>
      <div class="p-2.5 text-center xl:p-5">
        <h5 class="text-sm font-medium uppercase xsm:text-base">Visitors</h5>
      </div>
      <div class="p-2.5 text-center xl:p-5">
        <h5 class="text-sm font-medium uppercase xsm:text-base">Revenues</h5>
      </div>
      <div class="hidden p-2.5 text-center sm:block xl:p-5">
        <h5 class="text-sm font-medium uppercase xsm:text-base">Sales</h5>
      </div>
      <div class="hidden p-2.5 text-center sm:block xl:p-5">
        <h5 class="text-sm font-medium uppercase xsm:text-base">Conversion</h5>
      </div>
    </div>

    <!-- Table Rows -->
    <div class="grid grid-cols-3 border-b border-stroke dark:border-strokedark sm:grid-cols-5">
      <div class="flex items-center gap-3 p-2.5 xl:p-5">
        <div class="flex-shrink-0">
          <img src="image.jpg" alt="Brand" />
        </div>
        <p class="hidden text-black dark:text-white sm:block">Google</p>
      </div>

      <div class="flex items-center justify-center p-2.5 xl:p-5">
        <p class="text-black dark:text-white">3.5K</p>
      </div>

      <div class="flex items-center justify-center p-2.5 xl:p-5">
        <p class="text-meta-3">$5,768</p>
      </div>

      <div class="hidden items-center justify-center p-2.5 sm:flex xl:p-5">
        <p class="text-black dark:text-white">590</p>
      </div>

      <div class="hidden items-center justify-center p-2.5 sm:flex xl:p-5">
        <p class="text-meta-5">4.8%</p>
      </div>
    </div>
  </div>
</div>
```

### Data Table with Actions

```html
<div class="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
  <div class="py-6 px-4 md:px-6 xl:px-7.5">
    <h4 class="text-xl font-semibold text-black dark:text-white">
      Top Products
    </h4>
  </div>

  <div class="grid grid-cols-6 border-t border-stroke py-4.5 px-4 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
    <div class="col-span-3 flex items-center">
      <p class="font-medium">Product Name</p>
    </div>
    <div class="col-span-2 hidden items-center sm:flex">
      <p class="font-medium">Category</p>
    </div>
    <div class="col-span-1 flex items-center">
      <p class="font-medium">Price</p>
    </div>
    <div class="col-span-1 flex items-center">
      <p class="font-medium">Sold</p>
    </div>
    <div class="col-span-1 flex items-center">
      <p class="font-medium">Profit</p>
    </div>
  </div>

  <!-- Row -->
  <div class="grid grid-cols-6 border-t border-stroke py-4.5 px-4 dark:border-strokedark sm:grid-cols-8 md:px-6 2xl:px-7.5">
    <div class="col-span-3 flex items-center">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center">
        <div class="h-12.5 w-15 rounded-md">
          <img src="product.jpg" alt="Product" />
        </div>
        <p class="text-sm text-black dark:text-white">Apple Watch Series 7</p>
      </div>
    </div>
    <div class="col-span-2 hidden items-center sm:flex">
      <p class="text-sm text-black dark:text-white">Electronics</p>
    </div>
    <div class="col-span-1 flex items-center">
      <p class="text-sm text-black dark:text-white">$269</p>
    </div>
    <div class="col-span-1 flex items-center">
      <p class="text-sm text-black dark:text-white">22</p>
    </div>
    <div class="col-span-1 flex items-center">
      <p class="text-sm text-meta-3">$45</p>
    </div>
  </div>
</div>
```

## Forms

### Input Field

```html
<div class="mb-4.5">
  <label class="mb-2.5 block text-black dark:text-white">
    Email <span class="text-meta-1">*</span>
  </label>
  <input
    type="email"
    placeholder="Enter your email address"
    class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
  />
</div>
```

### Select Input

```html
<div class="mb-4.5">
  <label class="mb-2.5 block text-black dark:text-white">Subject</label>
  <div class="relative z-20 bg-transparent dark:bg-form-input">
    <select class="relative z-20 w-full appearance-none rounded border border-stroke bg-transparent py-3 px-5 outline-none transition focus:border-primary active:border-primary dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary">
      <option value="">Select subject</option>
      <option value="USA">USA</option>
      <option value="UK">UK</option>
      <option value="Canada">Canada</option>
    </select>
    <span class="absolute top-1/2 right-4 z-30 -translate-y-1/2">
      <svg class="fill-current" width="24" height="24" viewBox="0 0 24 24">
        <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2"/>
      </svg>
    </span>
  </div>
</div>
```

### Textarea

```html
<div class="mb-6">
  <label class="mb-2.5 block text-black dark:text-white">Message</label>
  <textarea
    rows="6"
    placeholder="Type your message"
    class="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
  ></textarea>
</div>
```

### Checkbox

```html
<div>
  <label class="flex cursor-pointer select-none items-center">
    <div class="relative">
      <input type="checkbox" class="sr-only" />
      <div class="box mr-4 flex h-5 w-5 items-center justify-center rounded border border-stroke dark:border-strokedark">
        <span class="opacity-0">
          <svg class="h-3.5 w-3.5 stroke-current" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
          </svg>
        </span>
      </div>
    </div>
    Remember me
  </label>
</div>
```

### Toggle Switch

```html
<div x-data="{ switcherToggle: false }">
  <label for="toggle1" class="flex cursor-pointer select-none items-center">
    <div class="relative">
      <input type="checkbox" id="toggle1" class="sr-only" @change="switcherToggle = !switcherToggle" />
      <div class="block h-8 w-14 rounded-full bg-meta-9 dark:bg-[#5A616B]"></div>
      <div :class="switcherToggle && '!right-1 !translate-x-full !bg-primary dark:!bg-white'" 
           class="absolute left-1 top-1 h-6 w-6 rounded-full bg-white transition">
      </div>
    </div>
  </label>
</div>
```

## Buttons

### Primary Button

```html
<button class="flex w-full justify-center rounded bg-primary p-3 font-medium text-gray hover:bg-opacity-90">
  Sign In
</button>
```

### Secondary Button

```html
<button class="flex justify-center rounded border border-stroke py-2 px-6 font-medium text-black hover:shadow-1 dark:border-strokedark dark:text-white">
  Cancel
</button>
```

### Button with Icon

```html
<button class="inline-flex items-center justify-center gap-2.5 rounded-md bg-primary py-4 px-10 text-center font-medium text-white hover:bg-opacity-90 lg:px-8 xl:px-10">
  <span>
    <svg class="fill-current" width="20" height="20" viewBox="0 0 20 20">
      <!-- Icon SVG -->
    </svg>
  </span>
  Button With Icon
</button>
```

### Button Sizes

```html
<!-- Small -->
<button class="inline-flex items-center justify-center rounded-md bg-primary py-2 px-4 text-center font-medium text-white hover:bg-opacity-90">
  Small
</button>

<!-- Medium (default) -->
<button class="inline-flex items-center justify-center rounded-md bg-primary py-3 px-6 text-center font-medium text-white hover:bg-opacity-90">
  Medium
</button>

<!-- Large -->
<button class="inline-flex items-center justify-center rounded-md bg-primary py-4 px-10 text-center font-medium text-white hover:bg-opacity-90">
  Large
</button>
```

### Status Buttons

```html
<!-- Success -->
<button class="inline-flex items-center justify-center rounded-md bg-meta-3 py-3 px-6 text-center font-medium text-white hover:bg-opacity-90">
  Success
</button>

<!-- Warning -->
<button class="inline-flex items-center justify-center rounded-md bg-warning py-3 px-6 text-center font-medium text-white hover:bg-opacity-90">
  Warning
</button>

<!-- Danger -->
<button class="inline-flex items-center justify-center rounded-md bg-danger py-3 px-6 text-center font-medium text-white hover:bg-opacity-90">
  Danger
</button>
```

## Badges & Tags

```html
<!-- Primary Badge -->
<span class="inline-flex rounded-full bg-primary bg-opacity-10 py-1 px-3 text-sm font-medium text-primary">
  Primary
</span>

<!-- Success Badge -->
<span class="inline-flex rounded-full bg-success bg-opacity-10 py-1 px-3 text-sm font-medium text-success">
  Paid
</span>

<!-- Warning Badge -->
<span class="inline-flex rounded-full bg-warning bg-opacity-10 py-1 px-3 text-sm font-medium text-warning">
  Pending
</span>

<!-- Danger Badge -->
<span class="inline-flex rounded-full bg-danger bg-opacity-10 py-1 px-3 text-sm font-medium text-danger">
  Unpaid
</span>
```

## Alerts

```html
<!-- Warning Alert -->
<div class="flex w-full border-l-6 border-warning bg-warning bg-opacity-[15%] px-7 py-8 shadow-md dark:bg-[#1B1B24] dark:bg-opacity-30 md:p-9">
  <div class="mr-5 flex h-9 w-9 items-center justify-center rounded-lg bg-warning bg-opacity-30">
    <svg class="h-[22px] w-[22px] fill-current text-warning">
      <!-- Warning icon -->
    </svg>
  </div>
  <div class="w-full">
    <h5 class="mb-3 text-lg font-semibold text-[#9D5425]">Attention needed</h5>
    <p class="leading-relaxed text-[#D0915C]">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    </p>
  </div>
</div>

<!-- Success Alert -->
<div class="flex w-full border-l-6 border-[#34D399] bg-[#34D399] bg-opacity-[15%] px-7 py-8 shadow-md dark:bg-[#1B1B24] dark:bg-opacity-30 md:p-9">
  <div class="mr-5 flex h-9 w-full max-w-[36px] items-center justify-center rounded-lg bg-[#34D399]">
    <svg class="h-[18px] w-[18px] fill-current text-white">
      <!-- Check icon -->
    </svg>
  </div>
  <div class="w-full">
    <h5 class="mb-3 font-semibold text-black dark:text-[#34D399]">Message Sent Successfully</h5>
    <p class="text-base leading-relaxed text-body">
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    </p>
  </div>
</div>
```

## Sidebar Navigation

```html
<aside class="absolute left-0 top-0 z-9999 flex h-screen w-72.5 flex-col overflow-y-hidden bg-black duration-300 ease-linear dark:bg-boxdark lg:static lg:translate-x-0">
  <!-- Logo -->
  <div class="flex items-center justify-between gap-2 px-6 py-5.5 lg:py-6.5">
    <a href="index.html">
      <img src="logo.svg" alt="Logo" />
    </a>
  </div>

  <!-- Menu -->
  <div class="no-scrollbar flex flex-col overflow-y-auto duration-300 ease-linear">
    <nav class="mt-5 py-4 px-4 lg:mt-9 lg:px-6">
      <div>
        <h3 class="mb-4 ml-4 text-sm font-semibold text-bodydark2">MENU</h3>

        <ul class="mb-6 flex flex-col gap-1.5">
          <!-- Menu Item -->
          <li>
            <a href="index.html"
               class="group relative flex items-center gap-2.5 rounded-sm py-2 px-4 font-medium text-bodydark1 duration-300 ease-in-out hover:bg-graydark dark:hover:bg-meta-4"
               :class="{ 'bg-graydark dark:bg-meta-4': page === 'dashboard' }">
              <svg class="fill-current" width="18" height="18" viewBox="0 0 18 18">
                <!-- Dashboard icon -->
              </svg>
              Dashboard
            </a>
          </li>

          <!-- Dropdown Menu Item -->
          <li>
            <a href="#"
               class="group relative flex items-center gap-2.5 rounded-sm py-2 px-4 font-medium text-bodydark1 duration-300 ease-in-out hover:bg-graydark dark:hover:bg-meta-4"
               @click.prevent="selected = (selected === 'Forms' ? '' : 'Forms')">
              <svg class="fill-current" width="18" height="18" viewBox="0 0 18 18">
                <!-- Forms icon -->
              </svg>
              Forms
              <svg class="absolute right-4 top-1/2 -translate-y-1/2 fill-current"
                   :class="{ 'rotate-180': selected === 'Forms' }"
                   width="20" height="20" viewBox="0 0 20 20">
                <!-- Chevron icon -->
              </svg>
            </a>

            <!-- Dropdown Menu -->
            <div class="overflow-hidden" :class="selected === 'Forms' ? 'block' : 'hidden'">
              <ul class="mt-4 mb-5.5 flex flex-col gap-2.5 pl-6">
                <li>
                  <a href="form-elements.html"
                     class="group relative flex items-center gap-2.5 rounded-md px-4 font-medium text-bodydark2 duration-300 ease-in-out hover:text-white">
                    Form Elements
                  </a>
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</aside>
```

## Header

```html
<header class="sticky top-0 z-999 flex w-full bg-white drop-shadow-1 dark:bg-boxdark dark:drop-shadow-none">
  <div class="flex flex-grow items-center justify-between py-4 px-4 shadow-2 md:px-6 2xl:px-11">
    <!-- Hamburger (mobile) -->
    <div class="flex items-center gap-2 sm:gap-4 lg:hidden">
      <button class="z-99999 block rounded-sm border border-stroke bg-white p-1.5 shadow-sm dark:border-strokedark dark:bg-boxdark lg:hidden">
        <!-- Menu icon -->
      </button>
    </div>

    <!-- Search -->
    <div class="hidden sm:block">
      <form action="#">
        <div class="relative">
          <button class="absolute top-1/2 left-0 -translate-y-1/2">
            <svg class="fill-body hover:fill-primary dark:fill-bodydark dark:hover:fill-primary" width="20" height="20">
              <!-- Search icon -->
            </svg>
          </button>
          <input type="text" placeholder="Type to search..."
                 class="w-full bg-transparent pr-4 pl-9 focus:outline-none" />
        </div>
      </form>
    </div>

    <!-- Right Side -->
    <div class="flex items-center gap-3 2xsm:gap-7">
      <!-- Dark Mode Toggle -->
      <div class="flex items-center gap-4">
        <!-- Theme toggler -->
      </div>

      <!-- Notification -->
      <div class="relative" x-data="{ dropdownOpen: false }">
        <a href="#" class="relative flex h-8.5 w-8.5 items-center justify-center rounded-full border-[0.5px] border-stroke bg-gray hover:text-primary dark:border-strokedark dark:bg-meta-4 dark:text-white">
          <span class="absolute -top-0.5 right-0 z-1 h-2 w-2 rounded-full bg-meta-1">
            <span class="absolute -z-1 inline-flex h-full w-full animate-ping rounded-full bg-meta-1 opacity-75"></span>
          </span>
          <svg class="fill-current duration-300 ease-in-out" width="18" height="18">
            <!-- Bell icon -->
          </svg>
        </a>
        <!-- Dropdown -->
      </div>

      <!-- User Dropdown -->
      <div class="relative" x-data="{ dropdownOpen: false }">
        <a href="#" class="flex items-center gap-4" @click.prevent="dropdownOpen = !dropdownOpen">
          <span class="hidden text-right lg:block">
            <span class="block text-sm font-medium text-black dark:text-white">Thomas Anree</span>
            <span class="block text-xs">UX Designer</span>
          </span>
          <span class="h-12 w-12 rounded-full">
            <img src="user.jpg" alt="User" />
          </span>
        </a>
        <!-- Dropdown content -->
      </div>
    </div>
  </div>
</header>
```

## Modal

```html
<div x-show="modalOpen" x-transition
     class="fixed top-0 left-0 z-999999 flex h-full min-h-screen w-full items-center justify-center bg-black/90 px-4 py-5">
  <div class="w-full max-w-142.5 rounded-lg bg-white py-12 px-8 text-center dark:bg-boxdark md:py-15 md:px-17.5">
    <span class="mx-auto inline-block">
      <!-- Modal icon -->
    </span>
    <h3 class="mt-5.5 pb-2 text-xl font-bold text-black dark:text-white sm:text-2xl">
      Modal Title
    </h3>
    <p class="mb-10">
      Modal description text goes here.
    </p>
    <div class="flex flex-wrap justify-center gap-4">
      <button class="inline-flex rounded border border-stroke py-2 px-6 font-medium text-black hover:shadow-1 dark:border-strokedark dark:text-white"
              @click="modalOpen = false">
        Cancel
      </button>
      <button class="inline-flex rounded bg-primary py-2 px-6 font-medium text-gray hover:bg-opacity-90">
        Confirm
      </button>
    </div>
  </div>
</div>
```

## Pagination

```html
<div class="p-4 sm:p-6 xl:p-7.5">
  <nav>
    <ul class="flex flex-wrap items-center gap-2">
      <li>
        <a href="#" class="flex items-center justify-center rounded bg-[#EDEFF1] py-1.5 px-3 text-xs font-medium text-black hover:bg-primary hover:text-white dark:bg-graydark dark:text-white dark:hover:bg-primary dark:hover:text-white">
          Previous
        </a>
      </li>
      <li>
        <a href="#" class="flex items-center justify-center rounded py-1.5 px-3 font-medium hover:bg-primary hover:text-white">1</a>
      </li>
      <li>
        <a href="#" class="flex items-center justify-center rounded bg-primary py-1.5 px-3 font-medium text-white">2</a>
      </li>
      <li>
        <a href="#" class="flex items-center justify-center rounded py-1.5 px-3 font-medium hover:bg-primary hover:text-white">3</a>
      </li>
      <li>
        <a href="#" class="flex items-center justify-center rounded bg-[#EDEFF1] py-1.5 px-3 text-xs font-medium text-black hover:bg-primary hover:text-white dark:bg-graydark dark:text-white dark:hover:bg-primary dark:hover:text-white">
          Next
        </a>
      </li>
    </ul>
  </nav>
</div>
```

## Custom TailAdmin Classes Reference

These are custom classes defined in TailAdmin's CSS that extend Tailwind:

### Custom Widths
```
w-72.5      # Sidebar width
max-w-142.5 # Modal max width
max-w-45    # Dropdown width
w-15        # Small image width
h-11.5      # Icon container height
```

### Custom Spacing
```
py-7.5, px-7.5  # Card padding
gap-7.5         # Larger gaps
pb-2.5          # Table padding
mt-5.5          # Modal spacing
```

### Custom Colors
```
bg-boxdark       # Dark mode background (#24303F)
bg-boxdark-2     # Darker background (#1A222C)
bg-strokedark    # Dark mode borders
bg-graydark      # Gray dark variant
bg-meta-1        # Red notification
bg-meta-2        # Icon background
bg-meta-3        # Success green
bg-meta-4        # Active state dark
bg-meta-5        # Info blue
bg-whiter        # Off-white
text-bodydark    # Dark mode body text
text-bodydark1   # Lighter body text
text-bodydark2   # Menu section headers
border-stroke    # Light borders
border-strokedark # Dark borders
```

### Custom Drop Shadows
```
drop-shadow-1    # Header shadow
shadow-default   # Card shadow
shadow-2         # Inner header shadow
```

## Converting to Rails ViewComponents

When converting TailAdmin HTML to ViewComponents:

```ruby
# app/components/dashboard/stats_card_component.rb
class Dashboard::StatsCardComponent < ViewComponent::Base
  def initialize(title:, value:, icon:, trend: nil, trend_value: nil)
    @title = title
    @value = value
    @icon = icon
    @trend = trend
    @trend_value = trend_value
  end

  def trend_color_class
    @trend == :up ? 'text-meta-3' : 'text-meta-1'
  end

  def trend_icon
    @trend == :up ? 'arrow-up' : 'arrow-down'
  end
end
```

```erb
<%# app/components/dashboard/stats_card_component.html.erb %>
<div class="rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark">
  <div class="flex h-11.5 w-11.5 items-center justify-center rounded-full bg-meta-2 dark:bg-meta-4">
    <%= render "icons/#{@icon}" %>
  </div>

  <div class="mt-4 flex items-end justify-between">
    <div>
      <h4 class="text-title-md font-bold text-black dark:text-white">
        <%= @value %>
      </h4>
      <span class="text-sm font-medium"><%= @title %></span>
    </div>

    <% if @trend.present? %>
      <span class="flex items-center gap-1 text-sm font-medium <%= trend_color_class %>">
        <%= @trend_value %>
        <%= render "icons/#{trend_icon}" %>
      </span>
    <% end %>
  </div>
</div>
```

## Anti-Patterns: NEVER Do This

### ❌ Inventing Classes (CRITICAL VIOLATION)

```html
<!-- WRONG: These classes DON'T EXIST in TailAdmin -->
<div class="card-dashboard">         <!-- INVENTED - doesn't exist -->
<div class="tailadmin-header">       <!-- INVENTED - doesn't exist -->
<div class="custom-stat-box">        <!-- INVENTED - doesn't exist -->
<button class="btn-tailadmin">       <!-- INVENTED - doesn't exist -->
<div class="dashboard-widget">       <!-- INVENTED - doesn't exist -->
<div class="admin-card">             <!-- INVENTED - doesn't exist -->
```

**Verify ANY class before using:**
```bash
# If this returns nothing, the class DOES NOT EXIST
grep -r 'class-name' /tmp/tailadmin/src/
grep 'class-name' /tmp/tailadmin/tailwind.config.js
```

### ❌ Wrong Color Names

```html
<!-- WRONG: These color classes don't exist -->
<div class="bg-boxlight">        <!-- Doesn't exist - use bg-white or bg-whiter -->
<div class="text-bodylight">     <!-- Doesn't exist - use text-body -->
<div class="bg-meta-11">         <!-- Only meta-1 through meta-10 exist -->
<div class="bg-primary-light">   <!-- Doesn't exist -->
<div class="border-dark">        <!-- Doesn't exist - use border-strokedark -->
```

### ❌ Wrong Spacing Values

```html
<!-- WRONG: These spacing values don't exist -->
<div class="p-7.6">              <!-- Not defined - use p-7.5 -->
<div class="w-73">               <!-- Not defined - use w-72.5 -->
<div class="mt-5.7">             <!-- Not defined - use mt-5.5 or mt-6 -->
```

### ❌ Mixing Frameworks

```html
<!-- WRONG: Don't mix Bootstrap or other frameworks -->
<div class="card rounded-sm">           <!-- Bootstrap 'card' class -->
<button class="btn btn-primary">        <!-- Bootstrap button classes -->
<div class="container-fluid">           <!-- Bootstrap container -->
<div class="row">                       <!-- Bootstrap grid -->
```

### ✅ Correct Approach: Always Verify First

```bash
# BEFORE using any class:

# 1. Clone repo (first time only)
git clone --depth 1 https://github.com/TailAdmin/tailadmin-free-tailwind-dashboard-template.git /tmp/tailadmin

# 2. Search for the class
grep -r 'the-class-you-want' /tmp/tailadmin/src/

# 3. If found, copy the EXACT pattern from the source
# 4. If NOT found, find an alternative that DOES exist
```

## Verification Checklist Before Any UI Code

```
[ ] Cloned/updated TailAdmin repository to /tmp/tailadmin
[ ] Found example of component type in src/*.html or src/partials/
[ ] Verified ALL custom classes exist in tailwind.config.js
[ ] Copied EXACT HTML structure from source
[ ] Did NOT invent any new classes
[ ] Did NOT modify class names from source
[ ] Tested dark mode classes (dark:*) are correct
```

## Quick Reference: File Locations

| Component Type | Source File |
|---------------|-------------|
| Dashboard/Stats | `src/index.html` |
| Tables | `src/tables.html` |
| Forms | `src/form-elements.html` |
| Buttons | `src/buttons.html` |
| Alerts | `src/alerts.html` |
| Cards | `src/index.html` (search "rounded-sm border") |
| Modals | Various files (search "modal") |
| Sidebar | `src/partials/sidebar.html` |
| Header | `src/partials/header.html` |
| Charts | `src/chart-*.html` |
| Authentication | `src/signin.html`, `src/signup.html` |
| Profile | `src/profile.html` |
| Settings | `src/settings.html` |
