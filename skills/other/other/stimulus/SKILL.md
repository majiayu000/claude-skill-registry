---
name: stimulus
description: Stimulus JS framework for Symfony UX. Use when building client-side interactivity with data attributes, creating controllers for DOM manipulation, handling user events, managing component state, or integrating with Symfony's StimulusBundle and AssetMapper. Triggers - stimulus controller, data-controller, data-action, data-target, frontend interactivity, JavaScript behavior, Symfony UX frontend, toggle, dropdown, modal JS, tabs JS, clipboard, chart controller, datepicker, autocomplete JS, lazy controller, stimulusFetch, outlets, keyboard shortcut, global event listener. Also trigger when the user wants to add JavaScript behavior to server-rendered HTML, wrap a third-party JS library, or build client-only interactions that don't need a server round-trip.
license: MIT
metadata:
  author: Simon Andre
  email: smn.andre@gmail.com
  url: https://smnandre.dev
  version: "1.0"
---

# Stimulus

Modest JavaScript framework that connects JS objects to HTML via data attributes. Stimulus does not render HTML -- it augments server-rendered HTML with behavior.

The mental model: HTML is the source of truth, JavaScript controllers attach to elements, and data attributes are the wiring. No build step required with AssetMapper.

## Quick Reference

```
data-controller="name"              attach controller to element
data-name-target="item"             mark element as a target
data-action="event->name#method"    bind event to controller method
data-name-key-value="..."           pass typed data to controller
data-name-key-class="..."           configure CSS class names
data-name-other-outlet=".selector"  reference another controller instance
```

## Controller Skeleton

```javascript
// assets/controllers/example_controller.js
import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = ['input', 'output'];
    static values = { url: String, delay: { type: Number, default: 300 } };
    static classes = ['loading'];
    static outlets = ['other'];

    connect() {
        // Called when controller connects to DOM
    }

    disconnect() {
        // Called when controller disconnects -- clean up here
    }

    submit(event) {
        // Action method
    }
}
```

File naming convention: `hello_controller.js` maps to `data-controller="hello"`. Subdirectories use `--` as separator: `components/modal_controller.js` maps to `data-controller="components--modal"`.

## HTML Wiring Examples

### Basic Controller

```html
<div data-controller="hello">
    <input data-hello-target="name" type="text">
    <button data-action="click->hello#greet">Greet</button>
    <span data-hello-target="output"></span>
</div>
```

### Values from Server (Twig)

Pass server data to controllers via value attributes. Values are typed and automatically parsed.

```html
<div data-controller="map"
     data-map-latitude-value="{{ place.lat }}"
     data-map-longitude-value="{{ place.lng }}"
     data-map-zoom-value="12">
</div>
```

Available types: `String`, `Number`, `Boolean`, `Array`, `Object`. Values trigger `{name}ValueChanged()` callbacks when mutated.

### Actions

The format is `event->controller#method`. Default events exist per element type (click for buttons, input for inputs, submit for forms) so the event can be omitted.

```html
{# Explicit event #}
<button data-action="click->hello#greet">Greet</button>

{# Default event (click for button) #}
<button data-action="hello#greet">Greet</button>

{# Multiple actions on same element #}
<input type="text"
       data-action="focus->field#highlight blur->field#normalize input->field#validate">

{# Prevent default #}
<form data-action="submit->form#validate:prevent">

{# Keyboard shortcuts #}
<div data-action="keydown.esc@window->modal#close">
<input data-action="keydown.enter->modal#submit keydown.ctrl+s->modal#save">

{# Global events (window/document) #}
<div data-action="resize@window->sidebar#adjust click@document->sidebar#closeOutside">
```

### CSS Classes

Externalize CSS class names so controllers stay generic:

```html
<button data-controller="button"
        data-button-loading-class="opacity-50 cursor-wait"
        data-button-active-class="bg-blue-600"
        data-action="click->button#submit">
    Submit
</button>
```

```javascript
// In controller
this.element.classList.add(...this.loadingClasses);
```

### Multiple Controllers

An element can have multiple controllers:

```html
<div data-controller="dropdown tooltip"
     data-action="mouseenter->tooltip#show mouseleave->tooltip#hide">
    <button data-action="click->dropdown#toggle">Menu</button>
    <ul data-dropdown-target="menu" hidden>...</ul>
</div>
```

### Outlets (Cross-Controller Communication)

Reference other controller instances by CSS selector:

```html
<div data-controller="player"
     data-player-playlist-outlet="#playlist">
    <button data-action="click->player#playNext">Next</button>
</div>

<ul id="playlist" data-controller="playlist">
    <li data-playlist-target="track">Song 1</li>
    <li data-playlist-target="track">Song 2</li>
</ul>
```

```javascript
// In player controller
static outlets = ['playlist'];

playNext() {
    const tracks = this.playlistOutlet.trackTargets;
    // ...
}
```

### Lazy Loading (Heavy Dependencies)

Load controller JS only when the element appears in the viewport. Use for controllers with heavy dependencies (chart libs, editors, maps).

```javascript
/* stimulusFetch: 'lazy' */
import { Controller } from '@hotwired/stimulus';
import Chart from 'chart.js';

export default class extends Controller {
    connect() {
        // Chart.js is only loaded when this element enters the viewport
    }
}
```

The `/* stimulusFetch: 'lazy' */` comment must be the very first line of the file.

## Symfony / Twig Integration

Raw data attributes are the recommended approach -- they work everywhere, are easy to read, and need no special helpers.

```twig
{# Raw attributes (preferred) #}
<div data-controller="search"
     data-search-url-value="{{ path('api_search') }}">
```

Twig helpers exist for complex cases or when generating attributes programmatically:

```twig
{# Twig helper #}
<div {{ stimulus_controller('search', { url: path('api_search') }) }}>

{# Chaining multiple controllers #}
<div {{ stimulus_controller('a')|stimulus_controller('b') }}>

{# Target and action helpers #}
<input {{ stimulus_target('search', 'query') }}>
<button {{ stimulus_action('search', 'submit') }}>
```

## Key Principles

**HTML drives, JS responds.** Controllers don't create markup -- they attach behavior to existing HTML. If you find yourself generating DOM in a controller, consider whether a TwigComponent or LiveComponent would be better.

**One controller, one concern.** A dropdown controller handles dropdowns. A tooltip controller handles tooltips. Compose multiple controllers on the same element rather than building mega-controllers.

**Clean up in disconnect().** If `connect()` adds event listeners, timers, or third-party library instances, `disconnect()` must remove them. Turbo navigation will disconnect and reconnect controllers as pages change.

**Values over data attributes.** Use Stimulus values (typed, with change callbacks) rather than raw `data-*` attributes for data that the controller needs to read or watch.

## References

- **Full API** (lifecycle, targets, values, actions, classes, outlets): [references/api.md](references/api.md)
- **Patterns** (debounce, fetch, modals, forms, etc.): [references/patterns.md](references/patterns.md)
- **Gotchas** (common mistakes, debugging, Turbo compatibility): [references/gotchas.md](references/gotchas.md)
