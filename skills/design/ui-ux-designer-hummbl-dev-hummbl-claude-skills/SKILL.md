---
name: ui-ux-designer
description: Modern UI/UX design specialist for web applications, mobile apps, and design systems. Covers design principles, user research, interaction patterns, accessibility (WCAG), responsive design, component libraries (Tailwind, shadcn/ui, Material), prototyping, and usability testing. Creates beautiful, functional interfaces following best practices.
---

# UI/UX Designer Skill

Expert in modern user interface and user experience design for web and mobile applications. Provides comprehensive guidance on design principles, interaction patterns, accessibility, and implementation using modern frameworks and libraries.

## Core Competencies

### 1. Design Principles
- **Visual Hierarchy:** Guide user attention with size, color, spacing, contrast
- **Consistency:** Maintain patterns across entire application
- **Affordance:** Design elements that suggest their function
- **Feedback:** Provide clear response to user actions
- **White Space:** Use breathing room to reduce cognitive load
- **Typography:** Choose readable fonts with proper sizing and spacing
- **Color Theory:** Create harmonious palettes with proper contrast
- **Progressive Disclosure:** Reveal complexity gradually

### 2. User Research & Analysis
- **User Personas:** Define target user archetypes
- **User Journeys:** Map complete user workflows
- **Pain Points:** Identify friction in current experience
- **Task Analysis:** Break down user goals into steps
- **Competitive Analysis:** Learn from similar products
- **Usability Testing:** Validate designs with real users
- **A/B Testing:** Compare design variations empirically
- **Analytics Review:** Use data to inform decisions

### 3. Interaction Patterns
- **Navigation:** Clear, predictable movement through app
- **Forms:** Efficient, error-tolerant data collection
- **Feedback:** Loading states, success/error messages
- **Microinteractions:** Small delightful moments
- **Gestures:** Touch and mouse interactions
- **Transitions:** Smooth, purposeful animations
- **Empty States:** Guide users when no content exists
- **Errors:** Helpful, actionable error messages

### 4. Accessibility (WCAG 2.1)
- **Perceivable:** Content available to all senses
- **Operable:** UI components usable by all
- **Understandable:** Information and operation clear
- **Robust:** Compatible with assistive technologies
- **Color Contrast:** 4.5:1 for normal text, 3:1 for large
- **Keyboard Navigation:** All functions keyboard-accessible
- **Screen Readers:** Semantic HTML, ARIA labels
- **Focus Indicators:** Clear visual focus states

### 5. Responsive Design
- **Mobile First:** Design for smallest screen, enhance up
- **Breakpoints:** Common: 640px, 768px, 1024px, 1280px
- **Flexible Grids:** Use relative units (%, rem, fr)
- **Touch Targets:** Minimum 44x44px for mobile
- **Performance:** Optimize for slow networks
- **Progressive Enhancement:** Core experience works everywhere

## Modern Tech Stack

### CSS Frameworks
**Tailwind CSS** (Recommended)
```html
<button class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors">
  Click Me
</button>
```

**Benefits:**
- Utility-first approach
- No CSS file bloat
- Rapid prototyping
- Consistent spacing/colors
- Easy responsive design

### Component Libraries

**shadcn/ui** (Recommended for React)
- Accessible components (Radix UI primitives)
- Tailwind-styled
- Copy/paste, not npm install
- Full customization

**Material UI (MUI)**
- Comprehensive component set
- Material Design guidelines
- Enterprise-ready
- TypeScript support

**Chakra UI**
- Accessible by default
- Composable components
- Dark mode built-in
- Great developer experience

### Design Tools
- **Figma:** Collaborative design (industry standard)
- **Adobe XD:** Adobe ecosystem integration
- **Sketch:** Mac-only, design systems
- **Framer:** Interactive prototypes
- **Excalidraw:** Quick wireframes

### Icon Libraries
- **Lucide:** Modern, consistent (recommended)
- **Heroicons:** Tailwind-designed
- **Feather:** Minimal, clean
- **Font Awesome:** Comprehensive, classic

## UI/UX Workflow

### Phase 1: Research (20% of time)
1. **Understand Users**
   - Who are they?
   - What are their goals?
   - What's their context?

2. **Define Requirements**
   - Functional requirements
   - Business goals
   - Technical constraints

3. **Competitive Analysis**
   - What works well elsewhere?
   - What should we avoid?
   - Where's the opportunity?

### Phase 2: Ideation (15% of time)
1. **Sketching**
   - Low-fidelity paper sketches
   - Multiple approaches
   - Quick iteration

2. **Wireframing**
   - Digital low-fidelity layouts
   - Focus on structure, not style
   - Tools: Figma, Excalidraw

3. **Information Architecture**
   - Content organization
   - Navigation structure
   - Page hierarchy

### Phase 3: Design (30% of time)
1. **Visual Design**
   - Choose color palette
   - Select typography
   - Create components
   - Design key screens

2. **Design System**
   - Define reusable components
   - Document patterns
   - Create style guide

3. **Prototyping**
   - Interactive mockups
   - Test user flows
   - Validate interactions

### Phase 4: Implementation (30% of time)
1. **Component Development**
   - Build reusable components
   - Implement responsive behavior
   - Add accessibility features

2. **Integration**
   - Connect to backend
   - Handle loading/error states
   - Optimize performance

3. **Polish**
   - Smooth animations
   - Microinteractions
   - Edge case handling

### Phase 5: Testing & Iteration (5% of time)
1. **Usability Testing**
   - Observe real users
   - Identify issues
   - Gather feedback

2. **Accessibility Audit**
   - Screen reader testing
   - Keyboard navigation
   - Color contrast check

3. **Performance Testing**
   - Load times
   - Animation smoothness
   - Mobile performance

## Design System Template

### Color Palette
```css
/* Primary Colors */
--primary-50: #eff6ff;
--primary-500: #3b82f6;
--primary-900: #1e3a8a;

/* Semantic Colors */
--success: #10b981;
--warning: #f59e0b;
--error: #ef4444;
--info: #3b82f6;

/* Neutrals */
--gray-50: #f9fafb;
--gray-500: #6b7280;
--gray-900: #111827;
```

### Typography Scale
```css
/* Tailwind default scale */
text-xs: 0.75rem (12px)
text-sm: 0.875rem (14px)
text-base: 1rem (16px)
text-lg: 1.125rem (18px)
text-xl: 1.25rem (20px)
text-2xl: 1.5rem (24px)
text-3xl: 1.875rem (30px)
text-4xl: 2.25rem (36px)
```

### Spacing Scale
```css
/* Tailwind 4px base unit */
0: 0
1: 0.25rem (4px)
2: 0.5rem (8px)
3: 0.75rem (12px)
4: 1rem (16px)
6: 1.5rem (24px)
8: 2rem (32px)
12: 3rem (48px)
16: 4rem (64px)
```

### Component Variants

**Button Sizes:**
- Small: py-1.5 px-3 text-sm
- Medium: py-2 px-4 text-base
- Large: py-3 px-6 text-lg

**Button Styles:**
- Primary: bg-primary text-white
- Secondary: bg-gray-200 text-gray-900
- Ghost: bg-transparent hover:bg-gray-100
- Danger: bg-red-500 text-white

## Common UI Patterns

### Navigation

**Top Nav (Desktop)**
```html
<nav class="bg-white border-b border-gray-200">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between h-16">
      <div class="flex">
        <!-- Logo -->
        <div class="flex-shrink-0 flex items-center">
          <img class="h-8 w-auto" src="/logo.svg" alt="Logo">
        </div>
        <!-- Nav items -->
        <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
          <a href="#" class="border-b-2 border-blue-500 text-gray-900 px-3 py-2">
            Dashboard
          </a>
          <a href="#" class="border-b-2 border-transparent text-gray-500 hover:text-gray-700 px-3 py-2">
            Projects
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>
```

**Mobile Menu (Hamburger)**
```html
<button class="sm:hidden p-2" aria-label="Open menu">
  <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
  </svg>
</button>
```

### Forms

**Input Field**
```html
<div class="space-y-2">
  <label for="email" class="block text-sm font-medium text-gray-700">
    Email address
  </label>
  <input
    type="email"
    id="email"
    name="email"
    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
    placeholder="you@example.com"
    required
  >
  <p class="text-sm text-gray-500">We'll never share your email.</p>
</div>
```

**Form Validation**
```html
<!-- Error state -->
<input class="border-red-500 focus:ring-red-500 focus:border-red-500">
<p class="mt-1 text-sm text-red-600">This field is required</p>

<!-- Success state -->
<input class="border-green-500 focus:ring-green-500 focus:border-green-500">
<p class="mt-1 text-sm text-green-600">Looks good!</p>
```

### Cards

**Basic Card**
```html
<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  <h3 class="text-lg font-semibold text-gray-900 mb-2">
    Card Title
  </h3>
  <p class="text-gray-600 mb-4">
    Card description goes here.
  </p>
  <button class="text-blue-600 hover:text-blue-700 font-medium">
    Learn more →
  </button>
</div>
```

### Modals/Dialogs

**Modal Structure**
```html
<div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
  <div class="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold">Modal Title</h2>
      <button class="text-gray-400 hover:text-gray-500">
        <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    
    <!-- Content -->
    <div class="mb-6">
      <p class="text-gray-600">Modal content goes here.</p>
    </div>
    
    <!-- Footer -->
    <div class="flex justify-end space-x-3">
      <button class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
        Cancel
      </button>
      <button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
        Confirm
      </button>
    </div>
  </div>
</div>
```

### Loading States

**Spinner**
```html
<svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
</svg>
```

**Skeleton Loading**
```html
<div class="animate-pulse space-y-4">
  <div class="h-4 bg-gray-200 rounded w-3/4"></div>
  <div class="h-4 bg-gray-200 rounded"></div>
  <div class="h-4 bg-gray-200 rounded w-5/6"></div>
</div>
```

### Toasts/Notifications

**Success Toast**
```html
<div class="fixed top-4 right-4 bg-green-50 border border-green-200 rounded-lg p-4 shadow-lg">
  <div class="flex items-start">
    <svg class="h-5 w-5 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
    </svg>
    <div class="ml-3">
      <p class="text-sm font-medium text-green-800">Successfully saved!</p>
    </div>
  </div>
</div>
```

## Accessibility Checklist

### Essential Requirements ✅
- [ ] All images have alt text
- [ ] Forms have associated labels
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] Headings follow logical hierarchy (h1 → h2 → h3)
- [ ] ARIA labels for icon buttons
- [ ] Skip to main content link
- [ ] Error messages associated with inputs
- [ ] No information conveyed by color alone

### Advanced Requirements ✅
- [ ] Screen reader tested (NVDA, JAWS, VoiceOver)
- [ ] Keyboard shortcuts documented
- [ ] Reduced motion respected (prefers-reduced-motion)
- [ ] High contrast mode supported
- [ ] Text can be resized to 200%
- [ ] Content reflows at 320px width
- [ ] Timeout warnings with extension option
- [ ] ARIA landmarks for page regions

## Responsive Design Patterns

### Mobile-First Approach
```html
<!-- Base styles for mobile -->
<div class="p-4 text-sm">
  <!-- Enhanced for tablet -->
  <div class="sm:p-6 sm:text-base">
    <!-- Enhanced for desktop -->
    <div class="lg:p-8 lg:text-lg">
      Content
    </div>
  </div>
</div>
```

### Responsive Grid
```html
<!-- 1 column mobile, 2 tablet, 3 desktop -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Responsive Typography
```html
<h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold">
  Responsive Heading
</h1>
```

### Show/Hide by Screen Size
```html
<!-- Show only on mobile -->
<div class="block sm:hidden">Mobile content</div>

<!-- Hide on mobile -->
<div class="hidden sm:block">Desktop content</div>
```

## Animation Guidelines

### Timing Functions
```css
/* Tailwind defaults */
ease-linear: linear
ease-in: cubic-bezier(0.4, 0, 1, 1)
ease-out: cubic-bezier(0, 0, 0.2, 1)  /* Best for entering */
ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)
```

### Duration Guidelines
- **Instant:** <100ms (hover effects)
- **Quick:** 100-200ms (small transitions)
- **Normal:** 200-300ms (most transitions)
- **Slow:** 300-500ms (large movements)
- **Avoid:** >500ms (feels sluggish)

### Common Transitions
```html
<!-- Hover effects -->
<button class="transition-colors duration-200 hover:bg-blue-600">

<!-- Fade in/out -->
<div class="transition-opacity duration-300 opacity-0 hover:opacity-100">

<!-- Slide in -->
<div class="transition-transform duration-300 transform translate-x-full group-hover:translate-x-0">

<!-- Scale -->
<img class="transition-transform duration-200 hover:scale-105">
```

## Dark Mode Implementation

### Tailwind Dark Mode
```html
<!-- Enable in tailwind.config.js: darkMode: 'class' -->

<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
  <button class="bg-blue-500 dark:bg-blue-600">
    Click me
  </button>
</div>
```

### Dark Mode Toggle
```javascript
// Toggle function
function toggleDarkMode() {
  document.documentElement.classList.toggle('dark');
  localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
}

// Initialize on load
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  document.documentElement.classList.add('dark');
}
```

## Common Pitfalls & Solutions

### Pitfall 1: Too Many Colors
**Problem:** Inconsistent color usage, visual chaos  
**Solution:** Use a constrained palette (1 primary, 1-2 accent, neutrals)

### Pitfall 2: Inconsistent Spacing
**Problem:** Elements feel unaligned, unprofessional  
**Solution:** Use 4px or 8px base unit, stick to spacing scale

### Pitfall 3: Poor Contrast
**Problem:** Text hard to read, fails accessibility  
**Solution:** Use contrast checker, aim for 4.5:1 minimum

### Pitfall 4: Tiny Touch Targets
**Problem:** Hard to tap on mobile  
**Solution:** Minimum 44x44px for all interactive elements

### Pitfall 5: No Loading States
**Problem:** Users unsure if action worked  
**Solution:** Show spinners, disable buttons, provide feedback

### Pitfall 6: Desktop-Only Design
**Problem:** Broken on mobile  
**Solution:** Design mobile-first, test on real devices

### Pitfall 7: Inaccessible Forms
**Problem:** Screen readers can't navigate  
**Solution:** Associate labels, use semantic HTML, add ARIA

## Resources

### Learning
- **Laws of UX:** https://lawsofux.com
- **Refactoring UI:** Book by Adam Wathan & Steve Schoger
- **Don't Make Me Think:** Book by Steve Krug
- **Nielsen Norman Group:** https://www.nngroup.com

### Tools
- **Figma:** https://figma.com (design)
- **Tailwind CSS:** https://tailwindcss.com (CSS framework)
- **shadcn/ui:** https://ui.shadcn.com (components)
- **Lucide Icons:** https://lucide.dev (icons)
- **Coolors:** https://coolors.co (color palettes)
- **WebAIM Contrast Checker:** https://webaim.org/resources/contrastchecker/

### Inspiration
- **Dribbble:** https://dribbble.com
- **Behance:** https://behance.net
- **Mobbin:** https://mobbin.com (mobile patterns)
- **Land-book:** https://land-book.com (landing pages)

## Success Criteria

**Good UI/UX achieves:**
- ✅ Users complete tasks efficiently
- ✅ Zero confusion about how to use interface
- ✅ Accessible to all users (WCAG AA minimum)
- ✅ Works on all screen sizes
- ✅ Fast load times (<3s initial, <1s interactions)
- ✅ Consistent visual language throughout
- ✅ Delightful microinteractions
- ✅ Error messages are helpful
- ✅ Users don't need documentation

**Poor UI/UX results in:**
- ❌ High bounce rates
- ❌ Support tickets about "how to..."
- ❌ Accessibility complaints
- ❌ Mobile users leave immediately
- ❌ Frustrated users, negative reviews
