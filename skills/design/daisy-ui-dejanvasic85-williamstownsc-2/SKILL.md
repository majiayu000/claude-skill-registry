---
name: daisy-ui
description: A Tailwind CSS component library that provides a set of pre-designed UI components. Use for accessible, themed components that match Williamstown SC brand.
---

# daisy-ui

## Instructions

Follow documentation from [./llms.txt](./llms.txt) to produce code that uses DaisyUI components and themes according to the project's tech stack and coding standards outlined in the main [CLAUDE.md](../../CLAUDE.md) file.

## Theme Customization

Configure DaisyUI theme in `tailwind.config.js` for Williamstown SC brand identity:

### Primary Colors

- `primary`: #062174 (Club blue - traditional, trustworthy)
- `secondary`: #DEB100 (Club yellow/gold - energy, visibility)
- `accent`: #10B981 (Green - soccer field aesthetic)
- `neutral`: #1F2937 (Dark gray for text)
- `base-100`: #FFFFFF (White backgrounds)
- `base-200`: #F3F4F6 (Light gray backgrounds)
- `base-300`: #E5E7EB (Medium gray borders)

### Typography Guidelines

- Use `font-sans` with system fonts or Inter
- Ensure minimum 16px base font size for accessibility
- Apply proper line-height (1.5+ for body text)
- Use font-weight variations: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### Theme Configuration Example

```js
// tailwind.config.js
module.exports = {
	plugins: [require('daisyui')],
	daisyui: {
		themes: [
			{
				williamstown: {
					primary: '#062174', // Club blue
					'primary-content': '#FFFFFF',
					secondary: '#DEB100', // Club gold
					'secondary-content': '#000000',
					accent: '#10B981', // Soccer green
					'accent-content': '#FFFFFF',
					neutral: '#1F2937',
					'neutral-content': '#FFFFFF',
					'base-100': '#FFFFFF', // White
					'base-200': '#F3F4F6', // Light gray
					'base-300': '#E5E7EB', // Medium gray
					'base-content': '#1F2937',
					info: '#3ABFF8',
					'info-content': '#000000',
					success: '#36D399',
					'success-content': '#000000',
					warning: '#FBBD23',
					'warning-content': '#000000',
					error: '#F87272',
					'error-content': '#000000'
				}
			}
		]
	}
};
```

## Component Selection

### Use DaisyUI Components For

**Navigation & Menus:**

- `navbar` - Top navigation bar
- `menu` - Vertical/horizontal menu lists
- `dropdown` - Dropdown menus
- `drawer` - Mobile slide-out navigation
- `breadcrumbs` - Page navigation trail

**Actions:**

- `btn` - Buttons with variants (btn-primary, btn-secondary, btn-ghost, btn-outline)
- `btn-group` - Grouped button sets
- `swap` - Toggle/swap icons (menu hamburger)
- `link` - Styled links

**Data Display:**

- `card` - Content cards for news, fixtures, players
- `badge` - Labels and tags
- `avatar` - Profile pictures
- `stat` - Statistics display (goals, wins, etc.)
- `table` - Data tables for fixtures/results
- `timeline` - Match history timeline

**Forms:**

- `input` - Text inputs with validation states
- `textarea` - Multi-line text
- `select` - Dropdown select
- `checkbox` - Checkboxes
- `radio` - Radio buttons
- `toggle` - Toggle switches
- `range` - Range sliders
- `file-input` - File upload

**Feedback:**

- `alert` - Notifications and messages
- `modal` - Modal dialogs
- `toast` - Toast notifications
- `loading` - Loading spinners
- `skeleton` - Loading skeletons
- `progress` - Progress bars

**Layout:**

- `divider` - Section dividers
- `stack` - Vertical stacking
- `join` - Join elements together
- `indicator` - Notification indicators

### Use Custom Tailwind For

- Hero sections with glassmorphism effects
- Complex asymmetric layouts
- Custom animations and transitions
- Grid-breaking designs from frontend-design skill
- Unique spacing patterns
- Advanced visual effects (backdrop-blur, gradients)

## Accessibility Patterns

### WCAG AA Compliance

1. **Color Contrast:**
   - DaisyUI automatically ensures contrast for text/background combinations
   - Verify custom colors meet 4.5:1 ratio for normal text
   - Verify custom colors meet 3:1 ratio for large text (18px+)

2. **Touch Targets:**
   - Use `btn-lg` for primary CTAs (ensures 44x44px minimum)
   - Default `btn` is 48px height (meets requirements)
   - Use `btn-sm` sparingly, only for secondary actions

3. **Form Accessibility:**

   ```jsx
   <label className="form-control w-full">
   	<div className="label">
   		<span className="label-text">Email address</span>
   	</div>
   	<input
   		type="email"
   		placeholder="you@example.com"
   		className="input input-bordered w-full"
   		aria-required="true"
   	/>
   	<div className="label">
   		<span className="label-text-alt">We'll never share your email</span>
   	</div>
   </label>
   ```

4. **Focus States:**
   - DaisyUI includes visible focus indicators by default
   - Test all interactive elements with keyboard navigation
   - Use `focus:` variants for custom styling

5. **Semantic HTML:**
   - DaisyUI components use proper semantic HTML
   - Add ARIA labels where needed: `aria-label`, `aria-describedby`
   - Use `role` attribute for custom components

## Common Patterns for Sports Clubs

### Match/Fixture Card

```jsx
<div className="card bg-base-100 shadow-xl">
	<div className="card-body">
		<div className="flex items-center justify-between">
			<h3 className="card-title text-lg">Round 5</h3>
			<div className="badge badge-primary">Home</div>
		</div>
		<div className="my-4 flex items-center justify-between">
			<div className="flex-1 text-center">
				<p className="text-xl font-bold">Williamstown SC</p>
			</div>
			<div className="px-4 text-center">
				<p className="text-3xl font-bold">2 - 1</p>
			</div>
			<div className="flex-1 text-center">
				<p className="text-xl font-bold">Opposition FC</p>
			</div>
		</div>
		<div className="card-actions justify-end">
			<button className="btn btn-ghost">Match Report</button>
		</div>
	</div>
</div>
```

### News Card

```jsx
<div className="card bg-base-100 shadow-xl">
	<figure>
		<img src="/news-image.jpg" alt="News headline" />
	</figure>
	<div className="card-body">
		<div className="flex gap-2">
			<div className="badge badge-secondary">News</div>
			<div className="badge badge-outline">Senior Men</div>
		</div>
		<h2 className="card-title">2026 Senior Men's Coaching Team</h2>
		<p>Exciting announcement about our coaching lineup for the upcoming season...</p>
		<div className="card-actions mt-4 items-center justify-between">
			<span className="text-base-content/70 text-sm">2 days ago</span>
			<button className="btn btn-primary">Read More</button>
		</div>
	</div>
</div>
```

### Navigation Header

```jsx
<div className="navbar bg-primary text-primary-content">
	<div className="navbar-start">
		<div className="dropdown">
			<button tabIndex={0} className="btn btn-ghost lg:hidden">
				<svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path
						strokeLinecap="round"
						strokeLinejoin="round"
						strokeWidth={2}
						d="M4 6h16M4 12h8m-8 6h16"
					/>
				</svg>
			</button>
			<ul
				tabIndex={0}
				className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
			>
				<li>
					<a>HOME</a>
				</li>
				<li>
					<a>ABOUT</a>
				</li>
				<li>
					<a>FIXTURES</a>
				</li>
			</ul>
		</div>
		<a className="btn btn-ghost text-xl">WILLIAMSTOWN SC</a>
	</div>
	<div className="navbar-center hidden lg:flex">
		<ul className="menu menu-horizontal px-1">
			<li>
				<a>HOME</a>
			</li>
			<li>
				<a>ABOUT</a>
			</li>
			<li>
				<a>MEMBER INFO</a>
			</li>
			<li>
				<a>FIXTURES</a>
			</li>
			<li>
				<a>CALENDAR</a>
			</li>
			<li>
				<a>CONTACT</a>
			</li>
			<li>
				<a>SHOP</a>
			</li>
		</ul>
	</div>
	<div className="navbar-end">
		<button className="btn btn-ghost btn-circle">
			<svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path
					strokeLinecap="round"
					strokeLinejoin="round"
					strokeWidth={2}
					d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
				/>
			</svg>
		</button>
	</div>
</div>
```

### Player Card

```jsx
<div className="card card-compact bg-base-100 shadow-xl">
	<figure>
		<img src="/player-photo.jpg" alt="Player name" className="h-64 w-full object-cover" />
	</figure>
	<div className="card-body">
		<div className="flex items-start justify-between">
			<div>
				<h3 className="card-title">John Smith</h3>
				<p className="text-base-content/70 text-sm">Midfielder</p>
			</div>
			<div className="badge badge-lg badge-primary">15</div>
		</div>
		<div className="stats stats-vertical mt-2 shadow">
			<div className="stat p-2">
				<div className="stat-title text-xs">Appearances</div>
				<div className="stat-value text-lg">24</div>
			</div>
			<div className="stat p-2">
				<div className="stat-title text-xs">Goals</div>
				<div className="stat-value text-lg">8</div>
			</div>
		</div>
	</div>
</div>
```

### Event Card

```jsx
<div className="card bg-base-100 shadow-xl">
	<div className="card-body">
		<div className="flex items-start gap-4">
			<div className="text-center">
				<div className="text-primary text-4xl font-bold">15</div>
				<div className="text-base-content/70 text-sm">NOV</div>
			</div>
			<div className="flex-1">
				<h3 className="card-title">Season Launch Event</h3>
				<p className="text-base-content/70 mb-2 text-sm">6:00 PM - 9:00 PM</p>
				<p>Join us for the official 2026 season launch with the new coaching team...</p>
				<div className="card-actions mt-4 justify-end">
					<button className="btn btn-primary">RSVP</button>
				</div>
			</div>
		</div>
	</div>
</div>
```

## Responsive Utilities

### Breakpoint Classes

Use DaisyUI's responsive modifiers with Tailwind breakpoints:

```jsx
// Button sizes
<button className="btn btn-sm md:btn-md lg:btn-lg">
  Responsive Button
</button>

// Card layout
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Cards adapt to screen size */}
</div>

// Navigation drawer (mobile)
<div className="drawer lg:drawer-open">
  <input id="drawer" type="checkbox" className="drawer-toggle" />
  <div className="drawer-content">
    {/* Page content */}
  </div>
  <div className="drawer-side">
    {/* Sidebar menu */}
  </div>
</div>
```

### Mobile-First Patterns

```jsx
// Hide on mobile, show on desktop
<div className="hidden lg:block">Desktop Menu</div>

// Show on mobile, hide on desktop
<div className="lg:hidden">Mobile Menu</div>

// Collapse for accordion on mobile
<div className="collapse lg:collapse-open">
  <input type="checkbox" />
  <div className="collapse-title">Click to expand</div>
  <div className="collapse-content">Content</div>
</div>
```

## Form Validation States

```jsx
// Success state
<input
  type="text"
  className="input input-bordered input-success w-full"
  defaultValue="valid@email.com"
/>

// Error state
<input
  type="text"
  className="input input-bordered input-error w-full"
  aria-invalid="true"
  aria-describedby="email-error"
/>
<span id="email-error" className="text-error text-sm">
  Please enter a valid email address
</span>

// Warning state
<input
  type="text"
  className="input input-bordered input-warning w-full"
/>

// Disabled state
<input
  type="text"
  className="input input-bordered w-full"
  disabled
/>
```

## Loading States

```jsx
// Button loading
<button className="btn btn-primary">
  <span className="loading loading-spinner"></span>
  Loading...
</button>

// Skeleton loader
<div className="flex flex-col gap-4">
  <div className="skeleton h-32 w-full"></div>
  <div className="skeleton h-4 w-28"></div>
  <div className="skeleton h-4 w-full"></div>
  <div className="skeleton h-4 w-full"></div>
</div>

// Card skeleton
<div className="card bg-base-100 shadow-xl">
  <div className="skeleton h-48 w-full"></div>
  <div className="card-body">
    <div className="skeleton h-4 w-3/4"></div>
    <div className="skeleton h-4 w-1/2"></div>
  </div>
</div>
```

## Modal Patterns

```jsx
// Basic modal
<dialog id="my_modal" className="modal">
  <div className="modal-box">
    <h3 className="font-bold text-lg">Match Report</h3>
    <p className="py-4">Detailed match information goes here...</p>
    <div className="modal-action">
      <form method="dialog">
        <button className="btn">Close</button>
      </form>
    </div>
  </div>
</dialog>

// Modal with backdrop
<dialog id="my_modal_2" className="modal modal-bottom sm:modal-middle">
  <div className="modal-box">
    <h3 className="font-bold text-lg">Confirm Action</h3>
    <p className="py-4">Are you sure you want to proceed?</p>
    <div className="modal-action">
      <form method="dialog">
        <button className="btn btn-ghost">Cancel</button>
        <button className="btn btn-primary">Confirm</button>
      </form>
    </div>
  </div>
  <form method="dialog" className="modal-backdrop">
    <button>close</button>
  </form>
</dialog>
```

## Performance Considerations

### Bundle Size

- DaisyUI adds approximately 25KB gzipped to your bundle
- Components are CSS-only (no JavaScript overhead)
- Use Tailwind's JIT mode for optimal bundle size
- Purge unused styles in production

### Optimization Tips

```js
// tailwind.config.js - Limit DaisyUI themes for smaller bundle
daisyui: {
  themes: ['williamstown'], // Only include what you need
  darkTheme: false,          // Disable if not using dark mode
  base: true,
  styled: true,
  utils: true,
}
```

### Tree Shaking

DaisyUI components are automatically tree-shaken when not used. Only include components you actually reference in your HTML/JSX.

## Combining DaisyUI with Custom Styles

### When to Mix

```jsx
// DaisyUI component with custom Tailwind
<div className="card bg-base-100 shadow-xl backdrop-blur-xl bg-opacity-80">
  <div className="card-body">
    {/* Glassmorphism effect added to DaisyUI card */}
  </div>
</div>

// DaisyUI with custom animations
<button className="btn btn-primary hover:scale-105 transition-transform duration-200">
  Hover Me
</button>
```

### Extending DaisyUI Components

```js
// tailwind.config.js
module.exports = {
	theme: {
		extend: {
			// Add custom animations
			animation: {
				'fade-in': 'fadeIn 0.3s ease-in'
			},
			keyframes: {
				fadeIn: {
					'0%': { opacity: '0', transform: 'translateY(10px)' },
					'100%': { opacity: '1', transform: 'translateY(0)' }
				}
			}
		}
	}
};
```

## Component Composition

### Building Complex Components

```jsx
// Fixture list with stats
const FixtureList = () => (
	<div className="overflow-x-auto">
		<table className="table-zebra table">
			<thead>
				<tr>
					<th>Date</th>
					<th>Home</th>
					<th>Score</th>
					<th>Away</th>
					<th>Status</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>Nov 15</td>
					<td className="font-bold">Williamstown SC</td>
					<td className="text-center">2 - 1</td>
					<td>Opposition FC</td>
					<td>
						<div className="badge badge-success">Win</div>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
);
```

## Best Practices

1. **Always use semantic HTML** - DaisyUI builds on proper semantic elements
2. **Test keyboard navigation** - Ensure all interactive elements are keyboard accessible
3. **Verify color contrast** - Use tools to check WCAG compliance
4. **Use consistent spacing** - Stick to Tailwind's spacing scale (p-4, gap-4, etc.)
5. **Leverage data-theme** - Apply theme to container elements: `<div data-theme="williamstown">`
6. **Mobile-first design** - Start with mobile styles, add responsive modifiers
7. **Avoid !important** - Use Tailwind's specificity instead
8. **Document custom variants** - Keep track of custom component combinations

## Common Pitfalls

❌ **Don't:**

- Mix inline styles with DaisyUI classes
- Override DaisyUI CSS variables without understanding the system
- Create custom components when DaisyUI has a solution
- Ignore accessibility features built into components

✅ **Do:**

- Use DaisyUI's theme system for customization
- Extend with Tailwind utilities when needed
- Test components across breakpoints
- Maintain consistent spacing and sizing
- Follow the component composition patterns above

## Quick Reference

### Component Class Patterns

```
Button:     btn btn-{variant} btn-{size}
Card:       card card-{variant}
Input:      input input-{variant} input-{size}
Badge:      badge badge-{variant} badge-{size}
Alert:      alert alert-{variant}
Modal:      modal modal-{position}
```

### Color Variants

```
primary, secondary, accent, neutral, info, success, warning, error, ghost
```

### Size Modifiers

```
xs, sm, md (default), lg, xl
```

### State Modifiers

```
disabled, loading, active, focus
```
