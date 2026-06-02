---
name: cesiumjs-core-utilities
description: "CesiumJS core utilities and networking - Resource, Color, Event, Request, RequestScheduler, error handling, helper functions, feature detection. Use when fetching remote data, managing HTTP requests, working with colors, handling events, debugging errors, or using utility functions like defined, clone, or buildModuleUrl."
---
# CesiumJS Core Utilities & Networking

Version baseline: CesiumJS v1.139+ (ES module imports, `defaultValue` removed in v1.134)

## Breaking Change: defaultValue Removed (v1.134)

```js
// WRONG (removed in v1.134)
const name = defaultValue(options.name, "default");
const opts = defaultValue(options, defaultValue.EMPTY_OBJECT);

// CORRECT (v1.134+)
import { Frozen } from "cesium";
const name = options.name ?? "default";
const opts = options ?? Frozen.EMPTY_OBJECT;
```

`Frozen.EMPTY_OBJECT` is `Object.freeze({})` and `Frozen.EMPTY_ARRAY` is `Object.freeze([])`. Use them as safe defaults for options objects and array parameters.

## Resource: HTTP Requests and Data Fetching

`Resource` is the unified class for all HTTP operations. It wraps URL construction, query parameters, headers, proxying, and retry logic.

### Fetching Data

```js
import { Resource } from "cesium";

// Static shorthand: accepts a URL string or options object
const jsonData = await Resource.fetchJson({ url: "https://api.example.com/data.json" });

// Instance-based: construct once, reuse for multiple fetches
const resource = new Resource({
  url: "https://api.example.com/features",
  queryParameters: { format: "json", limit: "100" },
  headers: { "Authorization": "Bearer my-token" },
});
const features = await resource.fetchJson();
const text = await resource.fetchText();           // string
const buffer = await resource.fetchArrayBuffer();  // ArrayBuffer
const blob = await resource.fetchBlob();           // Blob
const image = await resource.fetchImage();         // HTMLImageElement or ImageBitmap
```

### Derived Resources and Template Values

```js
import { Resource } from "cesium";

const api = new Resource({
  url: "https://tiles.example.com/{version}/tiles/{z}/{x}/{y}.png",
  templateValues: { version: "v2" },
  headers: { "X-Api-Key": "abc123" },
});

// getDerivedResource inherits headers, proxy, and retry settings
const tile = api.getDerivedResource({
  templateValues: { z: "10", x: "512", y: "384" },
});
const tileImage = await tile.fetchImage();

// Modify query parameters on an existing resource
resource.setQueryParameters({ access_token: "new-token" });
resource.appendQueryParameters({ extra: "param" });
```

### Retry and Proxy

```js
import { Resource, DefaultProxy } from "cesium";

// Retry on specific HTTP status codes
const resource = new Resource({
  url: "https://api.example.com/unstable",
  retryAttempts: 3,
  retryCallback: (resource, error) => {
    if (error.statusCode === 429) {
      return new Promise((resolve) => setTimeout(() => resolve(true), 2000));
    }
    return false;
  },
});

// DefaultProxy appends the target URL as a query parameter
const proxied = new Resource({
  url: "https://external-server.com/data.json",
  proxy: new DefaultProxy("/proxy/"),
});
// Request goes to: /proxy/?https%3A%2F%2Fexternal-server.com%2Fdata.json
```

### POST and PUT

```js
import { Resource } from "cesium";

const resource = new Resource({ url: "https://api.example.com/upload" });
const result = await resource.post(JSON.stringify({ name: "test" }), {
  headers: { "Content-Type": "application/json" },
});
// resource.put() works the same way
```

## Color

RGBA components as floats [0.0, 1.0]. Over 140 named constants as frozen static properties (e.g., `Color.RED`, `Color.CORNFLOWERBLUE`, `Color.TRANSPARENT`).

### Creating Colors

```js
import { Color } from "cesium";

const red = Color.RED;                                        // frozen constant
const custom = new Color(0.2, 0.6, 0.8, 1.0);               // float constructor
const blue = Color.fromCssColorString("#3498db");             // hex string
const semiRed = Color.fromCssColorString("rgba(255,0,0,0.5)"); // CSS rgba()
const coral = Color.fromBytes(255, 127, 80, 255);            // 0-255 bytes
const hsl = Color.fromHsl(0.58, 0.8, 0.5, 1.0);             // hue/sat/light
const bright = Color.fromRandom({                             // constrained random
  minimumRed: 0.75, minimumGreen: 0.75, minimumBlue: 0.75, alpha: 1.0,
});
```

### Manipulation and Conversion

```js
import { Color } from "cesium";

const base = Color.fromCssColorString("#3498db");
const translucent = base.withAlpha(0.5);                // new Color with alpha
const lighter = base.brighten(0.3, new Color());        // requires result param
const darker = base.darken(0.3, new Color());
const css = base.toCssColorString();                    // "rgb(52,152,219)"
const hex = base.toCssHexString();                      // "#3498db"
const bytes = base.toBytes();                           // [52, 152, 219, 255]
const equal = Color.RED.equals(new Color(1.0, 0.0, 0.0, 1.0)); // true
```

## Event System

`Event` is the publish-subscribe mechanism used throughout CesiumJS. Classes expose Event properties like `Viewer.selectedEntityChanged` and `Cesium3DTileset.tileLoad`.

### Basic Usage

```js
import { Event } from "cesium";

const onDataReceived = new Event();

// addEventListener returns a removal function
const removeListener = onDataReceived.addEventListener((data) => {
  console.log("Received:", data);
});

onDataReceived.raiseEvent({ id: 1, value: "test" }); // invoke all listeners
removeListener(); // unsubscribe
```

### EventHelper for Batch Cleanup

```js
import { EventHelper } from "cesium";

const helper = new EventHelper();
helper.add(viewer.selectedEntityChanged, (entity) => {
  console.log("Selected:", entity?.name);
});
helper.add(viewer.clock.onTick, (clock) => { /* per-frame logic */ });
helper.add(viewer.scene.globe.tileLoadProgressEvent, (queueLength) => {
  console.log("Tiles loading:", queueLength);
});

// Remove all listeners at once (e.g., in a destroy method)
helper.removeAll();
```

## RequestScheduler Configuration

`RequestScheduler` is a singleton that manages concurrent request limits. `Request` objects represent individual HTTP requests with priority and throttling (primarily internal).

```js
import { RequestScheduler } from "cesium";

RequestScheduler.maximumRequests = 64;            // global max (default: 50)
RequestScheduler.maximumRequestsPerServer = 12;   // per-server max (default: 18)

// Override for known HTTP/2 servers
RequestScheduler.requestsByServer = {
  "api.cesium.com:443": 32,
  "assets.cesium.com:443": 32,
};
```

## Error Handling

- **DeveloperError** -- bug in calling code (invalid args). Thrown only in debug builds; fix the code, do not catch.
- **RuntimeError** -- runtime failure (network, shader compile). Catch in production.

```js
import { RuntimeError, formatError, Cesium3DTileset } from "cesium";

try {
  const tileset = await Cesium3DTileset.fromUrl("https://example.com/tileset.json");
  viewer.scene.primitives.add(tileset);
} catch (error) {
  if (error instanceof RuntimeError) {
    console.error("Failed to load tileset:", error.message);
  } else {
    console.error(formatError(error)); // extracts name, message, stack
  }
}
```

## Helper Functions

### defined, clone, combine

```js
import { defined, clone, combine } from "cesium";

// defined: returns true if value is neither null nor undefined
if (defined(entity.billboard)) {
  entity.billboard.scale = 2.0;
}

// clone: shallow by default, pass true for deep
const obj = clone({ a: 1, nested: { b: 2 } }, true);

// combine: merge objects, first arg's keys take precedence
const merged = combine({ size: 20 }, { size: 10, color: "red" });
// { size: 20, color: "red" }
```

### createGuid, buildModuleUrl

```js
import { createGuid, buildModuleUrl } from "cesium";

const id = createGuid(); // "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"

// Resolve paths relative to Cesium installation
const iconUrl = buildModuleUrl("Assets/Textures/maki/marker.png");
```

### URL Utilities

```js
import { objectToQuery, queryToObject, getExtensionFromUri, getBaseUri } from "cesium";

const qs = objectToQuery({ key1: "value 1", key2: ["x", "y"] });
// "key1=value%201&key2=x&key2=y"

const parsed = queryToObject("key1=value%201&key2=x&key2=y");
// { key1: "value 1", key2: ["x", "y"] }

getExtensionFromUri("https://example.com/model.glb?v=2"); // "glb"
getBaseUri("https://example.com/data/model.glb");          // "https://example.com/data/"
```

### destroyObject

Replaces all methods on an object with functions that throw `DeveloperError`, and sets `isDestroyed()` to return `true`. Standard cleanup pattern for objects holding native resources.

```js
import { destroyObject } from "cesium";

class MyWidget {
  constructor(viewer) {
    this._handler = new Cesium.ScreenSpaceEventHandler(viewer.canvas);
  }
  isDestroyed() { return false; }
  destroy() {
    this._handler.destroy();
    return destroyObject(this);
  }
}
```

## AssociativeArray

O(1) key lookup with a live `values` array for allocation-free iteration in render loops.

```js
import { AssociativeArray } from "cesium";

const items = new AssociativeArray();
items.set("building-1", { height: 50 });
items.set("building-2", { height: 80 });

items.get("building-1");       // { height: 50 }
items.contains("building-1");  // true

// Iterate without per-frame allocations
const values = items.values;
for (let i = 0; i < values.length; i++) { /* process values[i] */ }

items.remove("building-1");
items.removeAll();
```

## PinBuilder

Generates map pin canvas elements with colors, text, maki icons, or custom images.

```js
import { PinBuilder, Color, Cartesian3, VerticalOrigin } from "cesium";

const pin = new PinBuilder();
const redPin = pin.fromColor(Color.RED, 48);                         // solid color
const textPin = pin.fromText("A", Color.BLUE, 48);                   // text label
const iconPin = await pin.fromMakiIconId("hospital", Color.GREEN, 48); // maki icon
const urlPin = await pin.fromUrl("/icons/custom.png", Color.YELLOW, 48);

viewer.entities.add({
  position: Cartesian3.fromDegrees(-75.17, 39.95),
  billboard: {
    image: pin.fromText("1", Color.ROYALBLUE, 48),
    verticalOrigin: VerticalOrigin.BOTTOM,
  },
});
```

## DistanceDisplayCondition

Controls entity/billboard/label visibility based on camera distance.

```js
import { DistanceDisplayCondition, Cartesian3, Color } from "cesium";

viewer.entities.add({
  position: Cartesian3.fromDegrees(-75.17, 39.95),
  billboard: {
    image: "/icons/marker.png",
    distanceDisplayCondition: new DistanceDisplayCondition(100.0, 50000.0),
  },
});
```

## Feature Detection and Fullscreen

```js
import { FeatureDetection, Fullscreen } from "cesium";

if (FeatureDetection.supportsWebAssembly()) { /* WASM workers OK */ }
if (FeatureDetection.supportsTypedArrays()) { /* TypedArrays OK */ }

if (Fullscreen.supportsFullscreen()) {
  Fullscreen.requestFullscreen(viewer.container);
}
```

## TaskProcessor

Wraps Web Workers for background computation. Worker is created lazily on first `scheduleTask`.

```js
import { TaskProcessor, defined } from "cesium";

const processor = new TaskProcessor("myWorkerModule");
const promise = processor.scheduleTask({ data: largeArray, op: "simplify" });

if (!defined(promise)) {
  // Too many active tasks; retry next frame
} else {
  const result = await promise;
}
processor.destroy(); // release worker when done
```

## TrustedServers

Credentials (cookies, auth headers) are sent only to registered servers.

```js
import { TrustedServers } from "cesium";

TrustedServers.add("secure-tiles.example.com", 443);
TrustedServers.contains("https://secure-tiles.example.com/tileset.json"); // true
TrustedServers.remove("secure-tiles.example.com", 443);
```

## Performance Tips

1. **Reuse Resource instances** -- `getDerivedResource` inherits proxy, headers, and retry config without re-parsing the URL.
2. **Tune RequestScheduler for HTTP/2** -- increase `maximumRequests` and per-server limits via `requestsByServer` for faster tile loading.
3. **Use `Frozen.EMPTY_OBJECT` for defaults** -- avoids allocating a new `{}` on every call in hot paths.
4. **Prefer `defined()` over truthiness** -- correctly distinguishes `0`, `""`, and `false` from `null`/`undefined`.
5. **Use AssociativeArray in render loops** -- its `values` array avoids per-frame `Object.keys()` allocations.
6. **Set retryAttempts conservatively** -- gate retries on specific status codes (401, 429, 503) via `retryCallback`.
7. **Destroy TaskProcessors when done** -- idle workers still consume memory.
8. **Never mutate frozen Color constants** -- call `.clone()` or `.withAlpha()` first.
9. **Use `formatError` in catch blocks** -- extracts name, message, and stack from any error type.
10. **Cache PinBuilder output** -- store canvas references when generating many identical pins across frames.

## See Also

- **cesiumjs-viewer-setup** -- Viewer initialization, Ion token, scene configuration
- **cesiumjs-imagery** -- Imagery providers that consume `Resource` for tile fetching
- **cesiumjs-entities** -- Entity API using `Color`, `DistanceDisplayCondition`, and `PinBuilder`
