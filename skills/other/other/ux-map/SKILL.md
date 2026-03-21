---
name: ux-map
description: Symfony UX Map for interactive maps with Leaflet or Google Maps in Symfony. Covers markers, polygons, polylines, circles, info windows, and LiveComponent integration. Use when displaying maps, placing markers, drawing shapes or routes, handling map events, building store locators, using custom tile layers, or making maps reactive with LiveComponent. Code triggers: <twig:ux:map />, Map(), Point(), Marker(), Polygon(), Polyline(), Circle(), InfoWindow(), MapOptionsInterface, ComponentWithMapTrait, fitBoundsToMarkers, ux:map:marker:before-create, ux:map:connect, SYMFONY_UX_MAP_DSN. Also trigger when the user asks "how to display a map", "how to add markers", "how to draw a polygon on a map", "how to handle map click events", "how to make a reactive map", "how to use Leaflet in Symfony", "how to use Google Maps in Symfony", "map not showing", "map has zero height". Do NOT trigger for SVG icons (use ux-icons) or general frontend interactivity (use stimulus).
license: MIT
metadata:
  author: Simon Andre
  email: smn.andre@gmail.com
  url: https://smnandre.dev
  version: "1.0"
---

# UX Map

Interactive maps in Symfony with Leaflet or Google Maps. Build maps in PHP, render them in Twig, and extend them with Stimulus controllers. Supports markers, polygons, polylines, circles, info windows, and LiveComponent integration.

## Installation

```bash
# Install the base package
composer require symfony/ux-map

# Then install ONE renderer:
composer require symfony/ux-leaflet-map    # Leaflet (free, open source)
# OR
composer require symfony/ux-google-map     # Google Maps (requires API key)
```

## Quick Reference

```
Map                    PHP object, holds markers/shapes/options
Point                  latitude + longitude
Marker                 pin on the map, optional InfoWindow
Polygon                closed shape (array of Points)
Polyline               open line (array of Points)
Circle                 center Point + radius in meters
InfoWindow             popup attached to a Marker, Polygon, or Circle
ux_map(map, attrs)     Twig function to render a Map
<twig:ux:map />        Twig component (requires ux-twig-component)
```

## Building a Map in PHP

```php
use Symfony\UX\Map\Map;
use Symfony\UX\Map\Point;
use Symfony\UX\Map\Marker;
use Symfony\UX\Map\InfoWindow;
use Symfony\UX\Map\Polygon;
use Symfony\UX\Map\Polyline;
use Symfony\UX\Map\Circle;

$map = (new Map())
    ->center(new Point(48.8566, 2.3522))
    ->zoom(12)
    ->minZoom(3)
    ->maxZoom(18);

// Marker with info window
$map->addMarker(new Marker(
    position: new Point(48.8566, 2.3522),
    title: 'Paris',
    infoWindow: new InfoWindow(
        headerContent: '<b>Paris</b>',
        content: 'The capital of France',
    ),
));

// Marker with custom icon (UX Icons integration)
$map->addMarker(new Marker(
    position: new Point(48.8738, 2.2950),
    title: 'Eiffel Tower',
    icon: Icon::ux('mdi:tower-eiffel')->width(32)->height(32),
    extra: ['category' => 'landmark'],
));

// Polygon (closed area)
$map->addPolygon(new Polygon(
    points: [
        new Point(48.8566, 2.3522),
        new Point(48.8606, 2.3376),
        new Point(48.8530, 2.3499),
    ],
    infoWindow: new InfoWindow(content: 'Central Paris area'),
));

// Polyline (open line)
$map->addPolyline(new Polyline(
    points: [
        new Point(48.8566, 2.3522),
        new Point(48.8738, 2.2950),
    ],
));

// Circle (center + radius in meters)
$map->addCircle(new Circle(
    center: new Point(48.8566, 2.3522),
    radius: 500,
    infoWindow: new InfoWindow(content: '500m radius'),
));

// Auto-fit bounds to show all markers
$map->fitBoundsToMarkers();
```

## Rendering in Twig

### Twig Function

```twig
{# Basic rendering #}
{{ ux_map(map, {style: 'height: 400px; width: 100%;'}) }}

{# With custom attributes and Stimulus controller #}
{{ ux_map(map, {
    'data-controller': 'custom-map',
    style: 'height: 400px;',
    class: 'rounded shadow'
}) }}
```

### Twig Component (HTML Syntax)

Requires `symfony/ux-twig-component`. Allows inline map definition without PHP:

```html
<twig:ux:map
    :center="[48.8566, 2.3522]"
    zoom="12"
    :markers='[
        {"position": [48.8566, 2.3522], "title": "Paris"},
        {"position": [48.8738, 2.2950], "title": "Eiffel Tower",
         "infoWindow": {"content": "324m tall"}}
    ]'
    :fitBoundsToMarkers="true"
    style="height: 400px; width: 100%;"
    class="rounded shadow"
/>
```

## Configuration

```yaml
# config/packages/ux_map.yaml
ux_map:
    renderer: '%env(resolve:default::UX_MAP_DSN)%'

    # Google Maps specific
    google_maps:
        default_map_id: null    # Optional: default Map ID for all maps
```

### Renderer DSN

Set in `.env`:

```bash
# Leaflet (free)
UX_MAP_DSN=leaflet://default

# Google Maps (requires API key)
UX_MAP_DSN=google://GOOGLE_MAPS_API_KEY@default
```

## Renderer Options

### Leaflet Options

```php
use Symfony\UX\Map\Bridge\Leaflet\LeafletOptions;
use Symfony\UX\Map\Bridge\Leaflet\Option\TileLayer;
use Symfony\UX\Map\Bridge\Leaflet\Option\ZoomControlOptions;
use Symfony\UX\Map\Bridge\Leaflet\Option\AttributionControlOptions;
use Symfony\UX\Map\Bridge\Leaflet\Option\ControlPosition;

$leafletOptions = (new LeafletOptions())
    ->tileLayer(new TileLayer(
        url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; OpenStreetMap contributors',
        options: ['minZoom' => 5, 'maxZoom' => 18],
    ))
    ->zoomControl(true)
    ->zoomControlOptions(new ZoomControlOptions(ControlPosition::TOP_LEFT))
    ->attributionControl(true)
    ->attributionControlOptions(new AttributionControlOptions(ControlPosition::BOTTOM_LEFT));

$map->options($leafletOptions);
```

### Google Maps Options

```php
use Symfony\UX\Map\Bridge\Google\GoogleOptions;
use Symfony\UX\Map\Bridge\Google\Option\ControlPosition;
use Symfony\UX\Map\Bridge\Google\Option\GestureHandling;
use Symfony\UX\Map\Bridge\Google\Option\MapTypeControlOptions;
use Symfony\UX\Map\Bridge\Google\Option\MapTypeControlStyle;
use Symfony\UX\Map\Bridge\Google\Option\ZoomControlOptions;
use Symfony\UX\Map\Bridge\Google\Option\StreetViewControlOptions;
use Symfony\UX\Map\Bridge\Google\Option\FullscreenControlOptions;

$googleOptions = (new GoogleOptions())
    ->mapId('YOUR_MAP_ID')
    ->gestureHandling(GestureHandling::GREEDY)
    ->backgroundColor('#f00')
    ->doubleClickZoom(true)
    ->zoomControlOptions(new ZoomControlOptions(
        position: ControlPosition::BLOCK_START_INLINE_END,
    ))
    ->mapTypeControlOptions(new MapTypeControlOptions(
        mapTypeIds: ['roadmap'],
        position: ControlPosition::INLINE_END_BLOCK_START,
        style: MapTypeControlStyle::DROPDOWN_MENU,
    ))
    ->streetViewControlOptions(new StreetViewControlOptions(
        position: ControlPosition::BLOCK_END_INLINE_START,
    ))
    ->fullscreenControlOptions(new FullscreenControlOptions(
        position: ControlPosition::INLINE_START_BLOCK_END,
    ));

$map->options($googleOptions);
```

To disable controls:

```php
$googleOptions = (new GoogleOptions())
    ->mapId('YOUR_MAP_ID')
    ->zoomControl(false)
    ->mapTypeControl(false)
    ->streetViewControl(false)
    ->fullscreenControl(false);
```

## Map Events (Stimulus)

Attach a custom Stimulus controller to interact with the underlying map:

```javascript
// assets/controllers/custom-map_controller.js
import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    connect() {
        this.element.addEventListener('ux:map:connect', this._onConnect.bind(this));
        this.element.addEventListener('ux:map:marker:after-create', this._onMarkerCreated.bind(this));
    }

    _onConnect(event) {
        const { map, markers } = event.detail;
        console.log('Map ready:', map);
    }

    _onMarkerCreated(event) {
        const { marker, definition } = event.detail;
        if (definition.extra?.category === 'landmark') {
            console.log('Landmark marker created');
        }
    }
}
```

```twig
{{ ux_map(map, {'data-controller': 'custom-map', style: 'height: 400px;'}) }}
```

### Available Events

| Event | Detail | Description |
|-------|--------|-------------|
| `ux:map:connect` | `{map, markers}` | Map is initialized and ready |
| `ux:map:marker:before-create` | `{definition}` | Before a marker is added |
| `ux:map:marker:after-create` | `{marker, definition}` | After a marker is added |
| `ux:map:polygon:before-create` | `{definition}` | Before a polygon is added |
| `ux:map:polygon:after-create` | `{polygon, definition}` | After a polygon is added |
| `ux:map:polyline:before-create` | `{definition}` | Before a polyline is added |
| `ux:map:polyline:after-create` | `{polyline, definition}` | After a polyline is added |
| `ux:map:circle:before-create` | `{definition}` | Before a circle is added |
| `ux:map:circle:after-create` | `{circle, definition}` | After a circle is added |
| `ux:map:info-window:before-create` | `{definition}` | Before an info window is created |
| `ux:map:info-window:after-create` | `{infoWindow, definition}` | After an info window is created |

## LiveComponent Integration

Use `ComponentWithMapTrait` to make the map reactive:

```php
namespace App\Twig\Components;

use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\Attribute\LiveProp;
use Symfony\UX\LiveComponent\DefaultActionTrait;
use Symfony\UX\Map\InfoWindow;
use Symfony\UX\Map\Live\ComponentWithMapTrait;
use Symfony\UX\Map\Map;
use Symfony\UX\Map\Marker;
use Symfony\UX\Map\Point;

#[AsLiveComponent]
final class MapSearch
{
    use DefaultActionTrait;
    use ComponentWithMapTrait;

    #[LiveProp(writable: true)]
    public string $query = '';

    protected function instantiateMap(): Map
    {
        $map = (new Map())
            ->center(new Point(48.8566, 2.3522))
            ->zoom(12)
            ->fitBoundsToMarkers();

        foreach ($this->getFilteredLocations() as $location) {
            $map->addMarker(new Marker(
                position: new Point($location->lat, $location->lng),
                title: $location->name,
                infoWindow: new InfoWindow($location->name),
            ));
        }

        return $map;
    }

    private function getFilteredLocations(): array
    {
        // Filter based on $this->query
        return [];
    }
}
```

```twig
{# templates/components/MapSearch.html.twig #}
<div {{ attributes }}>
    <input type="search" data-model="debounce(300)|query" placeholder="Search locations...">
    {{ ux_map(this.map, {style: 'height: 400px;'}) }}
</div>
```

## Key Principles

**Build in PHP, render in Twig.** The `Map` object is your data model. Add markers, polygons, circles in PHP (where you have access to your database/services). Render in Twig with a single function call.

**The renderer is swappable.** Leaflet and Google Maps are interchangeable. Your PHP code uses the same `Map`, `Marker`, `Point` classes regardless of renderer. Only renderer-specific options differ.

**Use `extra` for custom data.** The `extra` parameter on markers, polygons, and circles lets you attach arbitrary data that is available in JavaScript events.

**Install a renderer.** The base `symfony/ux-map` package provides the PHP API, but you must also install `symfony/ux-leaflet-map` (free) or `symfony/ux-google-map` (requires API key). Without a renderer, the map will not render.

**`Point(lat, lng)` -- latitude first.** This matches Google Maps convention but is the opposite of GeoJSON `[lng, lat]`. Getting the order wrong puts markers in the wrong place or in the ocean.

**`fitBoundsToMarkers()` is your friend.** Instead of manually calculating center/zoom, let the map auto-fit to show all markers. If there are no markers, the map falls back to the `center` and `zoom` you set -- always provide both as defaults.

## References

- **API** (all classes, methods, options): [references/api.md](references/api.md)
- **Patterns** (common recipes, controllers, dynamic maps): [references/patterns.md](references/patterns.md)
- **Gotchas** (common mistakes, debugging): [references/gotchas.md](references/gotchas.md)
