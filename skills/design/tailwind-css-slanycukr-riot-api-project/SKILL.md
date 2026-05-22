---
name: "Tailwind CSS"
description: "Utility-first CSS framework for rapidly building custom user interfaces"
when_to_use: "When you need to style HTML/React components with utility classes, create responsive layouts, or build UI components with Tailwind CSS"
requirements: ["Node.js", "Tailwind CSS installed", "PostCSS configuration"]
---

# Tailwind CSS

## Quick Start

```html
<!-- Basic card component -->
<div class="max-w-sm mx-auto bg-white rounded-xl shadow-md p-6">
  <h2 class="text-xl font-bold text-gray-800 mb-2">Card Title</h2>
  <p class="text-gray-600">Card content goes here</p>
  <button
    class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
  >
    Action
  </button>
</div>
```

```jsx
// React component example
function Button({ variant = "primary", children, ...props }) {
  const baseClasses = "font-semibold py-2 px-4 rounded transition-colors";
  const variantClasses = {
    primary: "bg-blue-500 hover:bg-blue-700 text-white",
    secondary: "bg-gray-200 hover:bg-gray-300 text-gray-800",
  };

  return (
    <button className={`${baseClasses} ${variantClasses[variant]}`} {...props}>
      {children}
    </button>
  );
}
```

## Common Patterns

### Layout Systems

```html
<!-- Flexbox centering -->
<div class="flex items-center justify-center min-h-screen">
  <div class="text-center">Centered content</div>
</div>

<!-- Grid layout -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div class="bg-white p-6 rounded-lg shadow">Item 1</div>
  <div class="bg-white p-6 rounded-lg shadow">Item 2</div>
  <div class="bg-white p-6 rounded-lg shadow">Item 3</div>
</div>

<!-- Responsive container -->
<div class="container mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Content -->
</div>
```

### Responsive Design

```html
<!-- Responsive text sizing -->
<h1 class="text-2xl md:text-3xl lg:text-4xl font-bold">Responsive Heading</h1>

<!-- Responsive spacing -->
<div class="py-4 sm:py-6 lg:py-8">
  <!-- Content with responsive padding -->
</div>

<!-- Mobile-first approach -->
<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- Full width on mobile, half on tablet, third on desktop -->
</div>
```

### Component Patterns

```html
<!-- Navigation bar -->
<nav class="bg-white shadow-lg">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between h-16">
      <div class="flex items-center">
        <div class="text-xl font-bold text-gray-800">Logo</div>
      </div>
      <div class="hidden md:flex items-center space-x-8">
        <a href="#" class="text-gray-600 hover:text-gray-800">Home</a>
        <a href="#" class="text-gray-600 hover:text-gray-800">About</a>
        <a href="#" class="text-gray-600 hover:text-gray-800">Contact</a>
      </div>
    </div>
  </div>
</nav>

<!-- Form inputs -->
<div class="space-y-4">
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
    <input
      type="email"
      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
    />
  </div>
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-2">Message</label>
    <textarea
      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      rows="4"
    ></textarea>
  </div>
</div>

<!-- Card with hover effects -->
<div
  class="transform transition-all duration-200 hover:scale-105 hover:shadow-xl"
>
  <div class="bg-white rounded-lg overflow-hidden shadow-lg">
    <img src="image.jpg" alt="Card image" class="w-full h-48 object-cover" />
    <div class="p-6">
      <h3 class="text-lg font-semibold mb-2">Card Title</h3>
      <p class="text-gray-600">Card description with hover effects</p>
    </div>
  </div>
</div>
```

### Utility Combinations

```html
<!-- Text with gradient -->
<div
  class="bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent"
>
  Gradient Text
</div>

<!-- Glass morphism effect -->
<div class="backdrop-blur-md bg-white/20 border border-white/30 rounded-lg p-6">
  Glass effect card
</div>

<!-- Custom spacing with arbitrary values -->
<div class="p-[2.5rem] m-[1.75rem]">Custom padding and margin</div>

<!-- Aspect ratio containers -->
<div class="aspect-w-16 aspect-h-9">
  <iframe src="video-url" class="w-full h-full"></iframe>
</div>
```

### Dark Mode

```html
<!-- Dark mode aware component -->
<div
  class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-lg p-6"
>
  <h2 class="text-xl font-bold mb-4">Dark Mode Compatible</h2>
  <p class="text-gray-600 dark:text-gray-300">
    This content adapts to dark/light theme
  </p>
</div>

<!-- Toggle button -->
<button
  class="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white px-4 py-2 rounded"
>
  Toggle Theme
</button>
```

## Interactive Elements

```html
<!-- Buttons with states -->
<button
  class="bg-blue-500 hover:bg-blue-700 active:bg-blue-800 text-white font-bold py-2 px-4 rounded transition-colors"
>
  Interactive Button
</button>

<!-- Dropdown menu -->
<div class="relative">
  <button
    class="bg-white border border-gray-300 rounded-md px-4 py-2 text-left"
  >
    Select Option
  </button>
  <div
    class="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-md shadow-lg"
  >
    <a href="#" class="block px-4 py-2 hover:bg-gray-100">Option 1</a>
    <a href="#" class="block px-4 py-2 hover:bg-gray-100">Option 2</a>
  </div>
</div>
```

## Animation & Transitions

```html
<!-- Fade in animation -->
<div class="animate-fade-in opacity-0 animation-fill-forwards">
  Fade in content
</div>

<!-- Smooth transitions -->
<div class="transform transition-transform duration-300 hover:translate-x-2">
  Slide on hover
</div>

<!-- Loading spinner -->
<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
```

## Custom CSS Integration

```css
/* tailwind.config.js */
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: '#3B82F6',
        'brand-dark': '#1E40AF',
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
      },
    },
  },
  plugins: [],
}
```

```html
<!-- Using custom theme values -->
<div class="bg-brand text-white p-4">Custom brand color</div>
<div class="p-72">Custom spacing</div>
```

## Best Practices

1. **Component-based approach**: Extract repeated class combinations into components
2. **Mobile-first**: Use responsive prefixes (`md:`, `lg:`) to enhance mobile designs
3. **Consistent spacing**: Use the spacing scale (`p-4`, `m-6`, `gap-8`) consistently
4. **Semantic naming**: Use utility classes that describe their function
5. **Responsive images**: Always include `object-cover` or `object-contain` for images

## Performance Tips

- Use PurgeCSS/JIT mode to remove unused utilities
- Group related classes together
- Use CSS variables for dynamic values
- Leverage container queries for component-based responsive design
- Consider using `@apply` sparingly for truly reusable patterns
