---
name: live-component
description: Symfony UX LiveComponent for dynamic server-rendered UI. Use when building interactive components that re-render via AJAX, real-time forms, data binding, live validation, or reactive UI without writing JavaScript. Triggers - live component, AsLiveComponent, LiveProp, LiveAction, data-model, real-time form, dynamic UI, AJAX component, reactive PHP, two-way binding, server re-render, live search, live filter, live validation, ComponentWithFormTrait, emit, LiveListener, polling, defer, lazy component, data-loading, writable prop, URL binding, component communication. Also trigger when the user wants a component that updates itself based on user input without writing JavaScript, or wants Vue/React-like reactivity in PHP.
license: MIT
metadata:
  author: Simon Andre
  email: smn.andre@gmail.com
  url: https://smnandre.dev
  version: "1.0"
---

# LiveComponent

TwigComponents that re-render dynamically via AJAX. Build reactive UIs in PHP + Twig with zero JavaScript. Every user interaction triggers a server round-trip that re-renders the component and morphs the DOM.

## When to Use LiveComponent

Use LiveComponent when a component's output depends on user interaction -- search results that update as you type, forms with real-time validation, filters that refine a list, anything where the UI needs to change based on user input and that change requires server-side data or logic.

If the component never re-renders after initial load, use TwigComponent instead (less overhead, no AJAX). If the interaction is purely client-side (toggle, animation), use Stimulus instead.

## Installation

```bash
composer require symfony/ux-live-component
```

## Quick Reference

```
#[AsLiveComponent]           Make component live (re-renderable via AJAX)
#[LiveProp]                  State that persists across re-renders
#[LiveProp(writable: true)]  State that the frontend can modify
#[LiveAction]                Server method callable from frontend
data-model="prop"            Two-way bind input to LiveProp
data-action="live#action"    Call LiveAction on event
data-loading="..."           Show/hide/style elements during AJAX
{{ attributes }}             REQUIRED on root element (wires the Stimulus controller)
```

## Basic Example

```php
// src/Twig/Components/Counter.php
namespace App\Twig\Components;

use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\Attribute\LiveProp;
use Symfony\UX\LiveComponent\Attribute\LiveAction;
use Symfony\UX\LiveComponent\DefaultActionTrait;

#[AsLiveComponent]
final class Counter
{
    use DefaultActionTrait;

    #[LiveProp]
    public int $count = 0;

    #[LiveAction]
    public function increment(): void
    {
        $this->count++;
    }

    #[LiveAction]
    public function decrement(): void
    {
        $this->count--;
    }
}
```

```twig
{# templates/components/Counter.html.twig #}
<div {{ attributes }}>
    <button data-action="live#action" data-live-action-param="decrement">-</button>
    <span>{{ count }}</span>
    <button data-action="live#action" data-live-action-param="increment">+</button>
</div>
```

**Critical:** The root element must render `{{ attributes }}`. This injects the Stimulus `data-controller="live"` attribute that makes the whole system work. Without it, nothing re-renders.

## LiveProp

State that persists between AJAX re-renders. Props are serialized to the frontend and sent back on every request.

### Basic Props

```php
#[LiveProp]
public string $query = '';

#[LiveProp]
public int $page = 1;

#[LiveProp]
public ?User $user = null;  // Entities auto-hydrate by ID
```

### Writable Props (Two-way Binding)

Only writable props can be modified from the frontend via `data-model`:

```php
#[LiveProp(writable: true)]
public string $search = '';

// Writable with specific fields for objects
#[LiveProp(writable: ['email', 'name'])]
public User $user;
```

### URL Binding

Sync a prop to a URL query parameter -- enables bookmarkable/shareable state:

```php
#[LiveProp(writable: true, url: true)]
public string $query = '';
// URL becomes: ?query=search+term

// Custom parameter name
use Symfony\UX\LiveComponent\Metadata\UrlMapping;

#[LiveProp(writable: true, url: new UrlMapping(as: 'q'))]
public string $query = '';
// URL becomes: ?q=search+term
```

### Hydration

Doctrine entities auto-hydrate by ID. For custom types:

```php
#[LiveProp(hydrateWith: 'hydrateStatus', dehydrateWith: 'dehydrateStatus')]
public Status $status;

public function hydrateStatus(string $value): Status
{
    return Status::from($value);
}

public function dehydrateStatus(Status $status): string
{
    return $status->value;
}
```

## Data Binding (data-model)

Bind inputs to writable LiveProps. When the input changes, the component re-renders with the new value.

```twig
{# Re-render on change (default) #}
<input type="text" data-model="search">

{# Debounced -- wait 300ms after last keystroke #}
<input type="text" data-model="search" data-model-debounce="300">

{# Only update on blur #}
<input type="text" data-model="on(blur)|search">

{# Update model but don't re-render yet #}
<input type="text" data-model="norender|search">

{# Checkbox, radio, select #}
<input type="checkbox" data-model="enabled">
<select data-model="category">
    <option value="1">Category 1</option>
</select>
```

### Validation Modifiers (since 2025)

```twig
{# Only re-render when input meets criteria #}
<input data-model="min_length(3)|search">
<input data-model="max_length(100)|bio">
<input data-model="min_value(0)|quantity">
<input data-model="max_value(999)|price">
```

## LiveAction

Server methods callable from the frontend:

```php
#[LiveAction]
public function save(): void
{
    // Called via data-action="live#action" data-live-action-param="save"
}

#[LiveAction]
public function delete(#[LiveArg] int $id): void
{
    // With typed argument via data-live-id-param="123"
}
```

### Calling Actions from Twig

```twig
{# Button click #}
<button data-action="live#action" data-live-action-param="save">Save</button>

{# With arguments #}
<button
    data-action="live#action"
    data-live-action-param="delete"
    data-live-id-param="{{ item.id }}"
>Delete</button>

{# Form submit (prevent default) #}
<form data-action="live#action:prevent" data-live-action-param="submit">
```

## Search Example (Complete)

```php
#[AsLiveComponent]
final class ProductSearch
{
    use DefaultActionTrait;

    #[LiveProp(writable: true, url: true)]
    public string $query = '';

    #[LiveProp(writable: true)]
    public string $category = '';

    public function __construct(
        private readonly ProductRepository $products,
    ) {}

    public function getProducts(): array
    {
        return $this->products->search($this->query, $this->category);
    }
}
```

```twig
<div {{ attributes }}>
    <input type="search" data-model="debounce(300)|query" placeholder="Search...">

    <select data-model="category">
        <option value="">All Categories</option>
        {% for cat in categories %}
            <option value="{{ cat.id }}">{{ cat.name }}</option>
        {% endfor %}
    </select>

    <div data-loading="addClass(opacity-50)">
        {% for product in this.products %}
            <div>{{ product.name }}</div>
        {% endfor %}
    </div>
</div>
```

## Loading States

Show visual feedback during AJAX re-renders:

```twig
{# Add/remove class while loading #}
<div data-loading="addClass(opacity-50)">
<div data-loading="removeClass(hidden)">

{# Show/hide element while loading #}
<span data-loading="show">Loading...</span>
<div data-loading="hide">Content</div>

{# Disable button while loading #}
<button data-loading="attr(disabled)">Submit</button>

{# Scoped to specific action or model #}
<span data-loading="action(save)|show">Saving...</span>
<span data-loading="model(query)|show">Searching...</span>

{# Delay before showing (avoid flicker on fast responses) #}
<span data-loading="delay(300)|show">Loading...</span>
```

## Form Integration

```php
use Symfony\Component\Form\FormInterface;
use Symfony\UX\LiveComponent\ComponentWithFormTrait;

#[AsLiveComponent]
final class RegistrationForm extends AbstractController
{
    use DefaultActionTrait;
    use ComponentWithFormTrait;

    #[LiveProp]
    public ?User $initialFormData = null;

    protected function instantiateForm(): FormInterface
    {
        return $this->createForm(UserType::class, $this->initialFormData);
    }

    #[LiveAction]
    public function save(EntityManagerInterface $em): Response
    {
        $this->submitForm();
        $user = $this->getForm()->getData();
        $em->persist($user);
        $em->flush();

        return $this->redirectToRoute('app_success');
    }
}
```

```twig
<div {{ attributes }}>
    {{ form_start(form, {
        attr: {
            'data-action': 'live#action:prevent',
            'data-live-action-param': 'save'
        }
    }) }}

    {{ form_row(form.email) }}
    {{ form_row(form.password) }}

    <button type="submit" data-loading="attr(disabled)">Register</button>

    {{ form_end(form) }}
</div>
```

### Real-time Validation

```twig
{{ form_row(form.email, {
    attr: {'data-model': 'on(blur)|validatedFields'}
}) }}
```

## Component Communication

### Emit Events (Child to Parent)

```php
use Symfony\UX\LiveComponent\ComponentToolsTrait;

#[AsLiveComponent]
final class ChildComponent
{
    use DefaultActionTrait;
    use ComponentToolsTrait;

    #[LiveAction]
    public function save(): void
    {
        // ... save logic
        $this->emit('itemSaved', ['id' => $this->item->getId()]);
    }
}
```

### Listen to Events (Parent)

```php
use Symfony\UX\LiveComponent\Attribute\LiveListener;

#[AsLiveComponent]
final class ParentComponent
{
    use DefaultActionTrait;

    #[LiveListener('itemSaved')]
    public function onItemSaved(#[LiveArg] int $id): void
    {
        // Component re-renders automatically after this method
    }
}
```

### Browser Events (LiveComponent to Stimulus)

```php
$this->dispatchBrowserEvent('modal:close');
```

```html
<!-- Stimulus picks it up -->
<div data-action="modal:close@window->modal#close">
```

## Polling

Auto-refresh a component on a timer:

```twig
{# Default: every 2 seconds #}
<div {{ attributes }} data-poll>

{# Custom interval #}
<div {{ attributes }} data-poll="delay(5000)">

{# Call specific action on each poll #}
<div {{ attributes }} data-poll="action(refresh)">
```

## Lazy / Deferred Loading

```twig
{# Load component after page renders (deferred AJAX call) #}
<twig:HeavyComponent defer />

{# Load when element scrolls into viewport (IntersectionObserver) #}
<twig:HeavyComponent lazy />

{# Placeholder while loading #}
<twig:HeavyComponent lazy>
    <div>Loading...</div>
</twig:HeavyComponent>
```

## Data Preservation

```twig
{# Prevent re-render from modifying this subtree #}
<div data-live-ignore>
    {# Third-party widget, contenteditable, etc. #}
</div>

{# Preserve specific attribute during DOM morph #}
<input data-live-preserve="value">
```

## Computed Properties

Same as TwigComponent -- `getXxx()` methods are accessible as `this.xxx`. Use `computed.xxx` for caching within a single render cycle (avoids calling the method multiple times in a loop).

```php
public function getFilteredItems(): array
{
    return array_filter($this->items, fn($i) => $i->isActive());
}
```

```twig
{# Uncached -- called each time #}
{% for item in this.filteredItems %}

{# Cached within this render #}
{% for item in computed.filteredItems %}
```

## Key Principles

**Every interaction is a server round-trip.** LiveComponent is not a client-side framework. Each re-render sends the full component state to the server, re-executes PHP, and morphs the DOM. For high-frequency interactions (drag-and-drop, real-time drawing), use Stimulus instead.

**Keep components small.** Large components with many LiveProps and complex templates are slow to re-render. Split into smaller, focused components that communicate via emit/listen.

**Use `norender` and `on(blur)` to reduce requests.** Not every keystroke needs a server call. Debounce text inputs, defer binding to blur events for fields that don't need instant feedback.

**`{{ attributes }}` on root element is non-negotiable.** Without it, the live behavior Stimulus controller is never attached and nothing works.

## References

- **Full API** (props, actions, forms, events, all options): [references/api.md](references/api.md)
- **Patterns** (search, CRUD, modals, validation, real-world examples): [references/patterns.md](references/patterns.md)
- **Gotchas** (props, hydration, performance, common mistakes): [references/gotchas.md](references/gotchas.md)
