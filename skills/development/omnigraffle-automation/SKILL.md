---
name: omnigraffle-automation
description: OmniGraffle plugin development using Omni Automation. Use when creating, modifying, or debugging OmniGraffle plugins, working with graphics/shapes/lines, or implementing canvas transformations.
---

# OmniGraffle Automation Development Guide

Reference documentation for developing OmniGraffle plugins using Omni Automation JavaScript API.

## Plugin Bundle Structure

OmniGraffle plugins use the `.omnigrafflejs` bundle format:

```
MyPlugin.omnigrafflejs/
├── manifest.json              # Plugin metadata (required)
├── Resources/
│   ├── icon.png               # Plugin icon (optional)
│   ├── MyLibrary.js           # Shared library (optional)
│   ├── MyLibrary.strings      # Library documentation
│   ├── myAction.js            # Action implementation
│   └── en.lproj/
│       ├── manifest.strings   # Localized plugin name
│       └── myAction.strings   # Localized action labels
```

## manifest.json

```json
{
  "author": "Your Name",
  "identifier": "com.example.MyPlugin",
  "version": "1.0",
  "description": "What the plugin does",
  "defaultLocale": "en",
  "libraries": [
    { "identifier": "MyLibrary" }
  ],
  "actions": [
    {
      "identifier": "myAction",
      "image": "star.fill"
    }
  ]
}
```

**Action images**: Use SF Symbol names (macOS 11+/iOS 14+). Examples: `cube.fill`, `arrow.up`, `square.lefthalf.filled`.

## Library Pattern

Libraries provide reusable functions across actions:

```javascript
var _ = function () {
    var MyLibrary = new PlugIn.Library(new Version("1.0"));

    // Constants
    MyLibrary.SOME_CONSTANT = 42;

    // Methods
    MyLibrary.myFunction = function (param) {
        // Implementation
        return result;
    };

    return MyLibrary;
}();
_;
```

**Access from actions**: `var lib = this.MyLibrary;`

**Access externally**:

```javascript
var plugin = PlugIn.find("com.example.MyPlugin");
var lib = plugin.library("MyLibrary");
lib.myFunction(param);
```

### Library Objects Are Frozen

**CRITICAL**: OmniGraffle freezes library objects after loading. You cannot modify properties on them after initialization:

```javascript
// This will NOT work - library objects are frozen
MyLibrary._cachedValue = null;
MyLibrary.getValue = function() {
    if (!this._cachedValue) {
        this._cachedValue = expensiveComputation();  // FAILS - object is frozen
    }
    return this._cachedValue;
};
```

**Verification:**

```javascript
var lib = plugin.library("MyLibrary");
Object.isFrozen(lib);      // true
Object.isSealed(lib);      // true
Object.isExtensible(lib);  // false
```

**Implications:**

- Cannot use lazy initialization patterns that cache on `this`
- Cannot add new properties after plugin loads
- All properties defined during initialization are read-only afterward

### Cross-Library References

When one library needs to access another library in the same plugin, use `this.plugIn.library()`:

```javascript
var _ = function() {
    var MyLibrary = new PlugIn.Library(new Version("1.0"));

    // Access another library (call each time - cannot cache due to freezing)
    MyLibrary.getCommon = function() {
        return this.plugIn.library('CommonLib');
    };

    // Use in methods
    MyLibrary.doSomething = function() {
        var common = this.plugIn.library('CommonLib');
        return common.sharedFunction();
    };

    return MyLibrary;
}();
_;
```

**Note**: Since library objects are frozen, you must call `this.plugIn.library()` each time rather than caching the result. The overhead is minimal.

## Action Pattern

Actions define menu items with validation and execution:

```javascript
var _ = function () {
    var action = new PlugIn.Action(function (selection) {
        var lib = this.MyLibrary;
        var graphics = selection.graphics;
        var canvas = selection.canvas;

        // Perform action on selected graphics
        graphics.forEach(function (g) {
            // Modify graphic
        });
    });

    action.validate = function (selection) {
        // Return true if action should be enabled
        return selection.graphics.length > 0;
    };

    return action;
}();
_;
```

## Form-Based Actions

Use forms for user input before action execution:

```javascript
var action = new PlugIn.Action(function (selection) {
    var form = new Form();

    // Dropdown menu
    var options = ['option1', 'option2'];
    var labels = ['Option 1', 'Option 2'];
    var menu = new Form.Field.Option('fieldName', 'Label', options, labels, 'option1');
    form.addField(menu);

    // Checkbox
    var checkbox = new Form.Field.Checkbox('checkName', 'Check Label', false);
    form.addField(checkbox);

    // Text input
    var textField = new Form.Field.String('textName', 'Text Label', 'default');
    form.addField(textField);

    // Show form and handle result
    form.show('Dialog Title', 'OK Button').then(function (result) {
        var selectedOption = result.values['fieldName'];
        var isChecked = result.values['checkName'];
        var textValue = result.values['textName'];
        // Execute action with form values
    });
});
```

## Localization Strings

**manifest.strings** (in `en.lproj/`):

```
"com.example.MyPlugin" = "My Plugin";
```

**action.strings** (in `en.lproj/`):

```
"label" = "Action Label";
"shortLabel" = "Short";
"mediumLabel" = "Medium Label";
"longLabel" = "Long Label - Full description";
"paletteLabel" = "Palette";
```

## Core Classes Reference

For complete API details, see [api-reference.md](api-reference.md).

### Geometry Classes

- **Point**: `new Point(x, y)` - Canvas coordinates
  - Methods: `add(point)`, `subtract(point)`, `scale(factor)`, `distanceTo(point)`
  - Properties: `x`, `y`, `length`, `negative`, `normalized`

- **Size**: `new Size(width, height)` - Dimensions
  - Properties: `width`, `height`

- **Rect**: `new Rect(x, y, width, height)` - Bounding box
  - Properties: `origin`, `size`, `center`, `minX`, `maxX`, `minY`, `maxY`, `midX`, `midY`
  - Methods: `union(rect)`, `intersect(rect)`, `insetBy(dx, dy)`, `offsetBy(dx, dy)`

### Graphics Classes

- **Graphic**: Abstract base class
  - Properties: `geometry`, `rotation`, `locked`, `name`, `layer`
  - Methods: `remove()`, `orderAbove(graphic)`, `orderBelow(graphic)`, `duplicateTo(point, canvas)`

- **Solid** extends Graphic: Shapes with fill
  - Properties: `fillType`, `fillColor`, `image`, `text`, `magnets`

- **Shape** extends Solid: Geometric shapes
  - Properties: `shape` (shape name), `shapeVertices`, `shapeControlPoints`
  - **Important**: Set `shape = "Bezier"` before modifying control points

- **Line** extends Graphic: Connectors
  - Properties: `points` (array of Point), `lineType`, `head`, `tail`, `headType`, `tailType`

- **Group** extends Graphic: Grouped graphics
  - Constructor: `new Group(graphics)` - Create group from array of graphics
  - Properties: `graphics` (array of child graphics)
  - Methods: `ungroup()` - Dissolve group, returns array of former children
  - **Warning**: Temporary grouping breaks undo (see Undo Behavior section)

### Canvas Class

- Properties: `graphics`, `layers`, `size`, `grid`
- Methods:
  - `addShape(shapeName, rect)` - Create shape (rect optional)
  - `addLine(startPoint, endPoint)` - Create line
  - `addText(string, point)` - Create text
  - `duplicate(graphics)` - Duplicate graphics, returns new array
  - `graphicWithId(id)`, `graphicWithName(name)` - Find graphics

### Layer Class

- Access: `canvas.layers[0]` (default layer)
- Methods: `addShape(shapeName, rect)` - Create shape (rect **required**)
- See [api-reference.md](api-reference.md) for full Layer documentation

### Color Class

- Constructors: `Color.RGB(r, g, b, a)`, `Color.HSB(h, s, b, a)`, `Color.White(w, a)`
- Presets: `Color.black`, `Color.white`, `Color.red`, `Color.blue`, etc.
- Properties: `red`, `green`, `blue`, `alpha`, `hex`
- Methods: `blend(color, fraction)`

## Common Transformation Patterns

### Working with Shape Control Points

```javascript
// Convert to Bezier for point manipulation
if (shape.shape !== "Bezier") {
    shape.shape = "Bezier";
}

// Get and modify control points
var points = shape.shapeControlPoints;
var newPoints = points.map(function (p) {
    return new Point(p.x * scale, p.y + offset);
});
shape.shapeControlPoints = newPoints;
```

### Working with Lines

```javascript
// Modify line points directly
var points = line.points;
var newPoints = points.map(function (p) {
    return new Point(p.x, p.y + offset);
});
line.points = newPoints;
```

### Processing Groups Recursively

```javascript
function getLeafGraphics(graphic) {
    var result = [];
    if (graphic instanceof Group) {
        var queue = [].concat(graphic.graphics);
        while (queue.length) {
            var elt = queue.pop();
            if (elt instanceof Group) {
                queue = queue.concat(elt.graphics);
            } else {
                result.push(elt);
            }
        }
    } else {
        result.push(graphic);
    }
    return result;
}
```

### Preserving Relative Positions (Multi-Object Transforms)

When transforming multiple objects, scale/skew operations on individual bounding boxes break relative positions.

**DO NOT use temporary grouping** - it breaks undo (heights become corrupted after undo). Instead, calculate a shared origin and transform each graphic individually:

```javascript
// Calculate combined bounding box
function getCombinedBounds(graphics) {
    var minX = Infinity, minY = Infinity;
    var maxX = -Infinity, maxY = -Infinity;
    for (var i = 0; i < graphics.length; i++) {
        var geom = graphics[i].geometry;
        minX = Math.min(minX, geom.minX);
        minY = Math.min(minY, geom.minY);
        maxX = Math.max(maxX, geom.maxX);
        maxY = Math.max(maxY, geom.maxY);
    }
    return { minX: minX, minY: minY, maxX: maxX, maxY: maxY };
}

// Scale points horizontally relative to shared origin
function scalePointsX(points, factor, originX) {
    return points.map(function(p) {
        return new Point(originX + (p.x - originX) * factor, p.y);
    });
}

// Transform multiple objects while preserving relative positions
function transformMultiple(graphics, scaleFactor) {
    var bounds = getCombinedBounds(graphics);
    var originX = bounds.minX;  // Shared origin for all graphics

    for (var i = 0; i < graphics.length; i++) {
        var g = graphics[i];
        g.shape = "Bezier";
        var points = g.shapeControlPoints;
        points = scalePointsX(points, scaleFactor, originX);
        g.shapeControlPoints = points;
    }
}
```

This approach:

- Preserves relative positions (same visual result as grouping)
- Works correctly with undo
- Each graphic is transformed independently using the shared origin

### Geometry Transformations

```javascript
// Scale bounding box
var geom = graphic.geometry;
geom.size = new Size(geom.size.width * factor, geom.size.height);
graphic.geometry = geom;

// Rotate graphic
graphic.rotation = graphic.rotation + degrees;

// Vertical shear (skew)
function skewY(points, deg, zeroOffset) {
    var tanDeg = Math.tan(deg * Math.PI / 180);
    return points.map(function (p) {
        return new Point(p.x, p.y + (p.x - zeroOffset) * tanDeg);
    });
}
```

### Duplicating Graphics

```javascript
// Duplicate on same canvas (canvas method, takes array)
var duplicates = canvas.duplicate(graphics);  // Returns array of copies

// Duplicate to specific location (graphic method)
var newGraphic = graphic.duplicateTo(new Point(x, y), targetCanvas);
```

**Note**: Individual graphics don't have a `duplicate()` method - use `canvas.duplicate([graphic])` or `graphic.duplicateTo(point, canvas)`.

## Selection Object

The selection parameter in actions provides:

- `selection.graphics` - Array of selected graphics
- `selection.canvas` - Current canvas
- `selection.document` - Current document
- `selection.view` - Current view

## Undo Behavior

Understanding undo is critical for plugin development.

### Undo Granularity

Each JavaScript execution context is one atomic undo step:

- All operations in a single `evaluate javascript` call undo together
- Plugin actions triggered from UI are one undo step
- Separate AppleScript `evaluate javascript` calls are separate undo steps

### Available Undo API

```javascript
var doc = document;
doc.undo();       // Undo last action
doc.redo();       // Redo last undone action
doc.canUndo;      // Boolean: is undo available?
doc.canRedo;      // Boolean: is redo available?
```

**No UndoManager**: OmniGraffle does not expose `beginUndo()`/`endUndo()` or any undo grouping API. You cannot create custom undo groups within a single action.

### Temporary Grouping Breaks Undo

**CRITICAL BUG**: Using `new Group()` + geometry scaling + `ungroup()` corrupts the undo stack:

```javascript
// DON'T DO THIS - breaks undo!
var group = new Group(graphics);
var geom = group.geometry;
geom.size = new Size(geom.size.width * 0.866, geom.size.height);
group.geometry = geom;
// ... transform children ...
group.ungroup();

// After undo: heights are WRONG (corrupted)
```

**Symptoms**: After undo, width is restored correctly but height is corrupted (e.g., 60 → 26.7 instead of 60).

**Solution**: Transform each graphic individually using a shared origin (see "Preserving Relative Positions" section).

### Testing Undo

**CRITICAL LIMITATION**: `evaluate javascript` via osascript (command line) does **NOT** register undo actions at all. Undo only works for:

- Plugin actions triggered from OmniGraffle's UI (Automation menu)
- Scripts run from OmniGraffle's built-in automation console

```javascript
// Via osascript - no undo registered, even in separate calls
lib.generateTopology(canvas, viewCenter, config);
// Later:
document.canUndo;  // false - nothing to undo!
document.undo();   // Error: "There are no undoable actions."
```

**Why this matters**: Automated tests via shell scripts cannot verify undo behavior. Graphics will be created but won't be undoable via osascript.

**To test undo behavior**:

1. Run the plugin action from OmniGraffle's UI (Automation > Your Plugin > Action)
2. Press Cmd+Z to verify undo works
3. Press Cmd+Shift+Z to verify redo works

**What automated tests CAN verify**:

- Correct number of graphics created
- All graphics created atomically in single call
- Correct properties/positions of created graphics

```javascript
// Automated test pattern - verify atomic creation
var beforeCount = canvas.graphics.length;
lib.generateTopology(canvas, viewCenter, config);
var afterCount = canvas.graphics.length;

// Verify expected count
result.checks.graphicsAdded = (afterCount - beforeCount) === expectedCount;
// Note: When run from UI, this will be one atomic undo step
```

## Best Practices

1. **Always validate selection**: Return `false` from `validate()` if action cannot proceed
2. **Convert to Bezier**: Before modifying `shapeControlPoints`, set `shape = "Bezier"`
3. **Handle Groups**: Use recursive flattening to process all nested graphics
4. **Use shared reference points**: For multi-select transforms, compute shared minX/minY
5. **Avoid temporary grouping**: Don't use `new Group()` + `ungroup()` for transforms - it breaks undo
6. **Test undo behavior**: Verify multi-object transforms undo correctly (manual testing via OmniGraffle UI only)
7. **Preserve originals**: Offer duplicate-first option for destructive operations
8. **Localize strings**: Put all user-visible text in `.strings` files
9. **Test with complex selections**: Groups, lines, shapes, and mixed selections
10. **Z-order preservation**: `ungroup()` preserves z-order; if shapes appear hidden, check for overlapping fills
11. **Rotation normalization**: OmniGraffle normalizes rotations (e.g., -60° becomes 300°)
12. **Library objects are frozen**: Don't try to cache values on library objects - use `this.plugIn.library()` each time for cross-library references
13. **Cross-library access**: Use `this.plugIn.library('OtherLib')` to access other libraries in the same plugin

## Automated Testing via AppleScript

OmniGraffle JavaScript can be executed from the command line via AppleScript, enabling automated testing.

### Basic Execution Pattern

```bash
osascript -e '
tell application "OmniGraffle"
    set jsCode to "
        // Your JavaScript code here
        var result = { success: true };
        JSON.stringify(result);
    "
    evaluate javascript jsCode
end tell
'
```

**Limitations when running via osascript:**

- System Events keystrokes are blocked (`osascript is not allowed to send keystrokes`)
- Cannot use Cmd+Z/Cmd+C/Cmd+V programmatically from command line
- Must use OmniGraffle's JavaScript API directly for all operations
- **Undo does NOT work via osascript** - `evaluate javascript` from command line does not register undo actions at all
- Undo must be tested manually from OmniGraffle's UI (Automation menu)

### Plugin Installation Path

Plugins are installed to:

```
~/Library/Containers/com.omnigroup.OmniGraffle7/Data/Library/Application Support/Plug-Ins/
```

Install/update a plugin:

```bash
cp -R MyPlugin.omnigrafflejs "$HOME/Library/Containers/com.omnigroup.OmniGraffle7/Data/Library/Application Support/Plug-Ins/"
```

### Testing Plugin Functions

```bash
osascript -e '
tell application "OmniGraffle"
    set jsCode to "
        var result = {};
        try {
            // Load plugin library
            var lib = PlugIn.find(\"com.example.MyPlugin\").library(\"MyLibrary\");
            result.version = lib.version.versionString;

            // Get canvas and create test objects
            var canvas = document.windows[0].selection.canvas;
            var rect = canvas.addShape(\"Rectangle\", new Rect(100, 100, 50, 50));
            rect.text = \"Test\";

            // Run transformation
            lib.myFunction([rect]);

            // Verify results
            result.checks = {
                shapeConverted: rect.shape === \"Bezier\",
                textRotated: rect.textRotation === 30
            };
            result.passed = result.checks.shapeConverted && result.checks.textRotated;

        } catch(e) {
            result.error = e.message;
            result.stack = e.stack;
        }
        JSON.stringify(result, null, 2);
    "
    evaluate javascript jsCode
end tell
'
```

### Canvas Management for Tests

```javascript
// Create test canvas
var portfolio = document.portfolio;
var testCanvas = portfolio.addCanvas();
testCanvas.name = "Test Canvas";

// Create shapes directly on a canvas layer
var layer = testCanvas.layers[0];
var rect = layer.addShape("Rectangle", new Rect(50, 50, 100, 80));
rect.fillColor = Color.RGB(0.8, 0.9, 1.0);
rect.text = "Test";

var cross = layer.addShape("Cross", new Rect(200, 50, 80, 80));

// Clean up test canvas when done
testCanvas.remove();
```

**Note on Layer.addShape():** The second argument (Rect) is required, unlike Canvas.addShape() which can take just a shape name.

**Note on portfolio.canvases:** This property is read-only. You cannot assign it to a variable in a for loop initializer. Use index access:

```javascript
// WRONG: var canvases = portfolio.canvases; for (var c in canvases)...
// RIGHT:
for (var i = 0; i < portfolio.canvases.length; i++) {
    var canvas = portfolio.canvases[i];
}
```

### Exporting Canvases for Visual Verification

**Switching canvases via AppleScript:**

```applescript
tell application "OmniGraffle"
    set doc to document 1
    tell front window
        set its canvas to canvas "Canvas Name" of doc
    end tell
end tell
```

**Exporting current canvas to PNG:**

```applescript
tell application "OmniGraffle"
    set doc to document 1

    -- Switch to target canvas first
    tell front window
        set its canvas to canvas "My Canvas" of doc
    end tell

    -- Export with scope
    export front document scope current canvas to POSIX file "/tmp/output.png" as "public.png"
end tell
```

**Export scope options:**

- `scope current canvas` - Export only the current canvas
- `scope all graphics` - Export all graphics (captures negative coordinates)
- `scope entire document` - Export the full document

### Test Result Pattern

```javascript
var results = { tests: [] };

// Test case
(function() {
    var test = { name: "Test Name", passed: false };
    try {
        // Setup
        var before = { /* snapshot state */ };

        // Execute
        lib.myFunction(graphics);

        // Verify
        var after = { /* snapshot state */ };
        test.checks = {
            check1: after.value === expected,
            check2: after.other === expected2
        };
        test.passed = test.checks.check1 && test.checks.check2;

    } catch(e) {
        test.error = e.message;
    }
    results.tests.push(test);
})();

// Summary
results.summary = {
    total: results.tests.length,
    passed: results.tests.filter(function(t) { return t.passed; }).length
};
```

### Edge Cases to Test

- Empty selection (`graphics.length === 0`)
- Single object vs multiple objects
- Pre-existing groups (don't double-wrap)
- Nested groups (deeply nested structures)
- Mixed selections (groups + individual shapes)
- Lines (use `points` not `shapeControlPoints`)
- Pre-rotated shapes (preserve existing rotation)
- Pre-rotated text (rotation should be additive)
- Shapes without text (don't modify textRotation)
- Invalid parameters (should throw meaningful errors)
- **Undo with multi-object selection** (verify heights restore correctly)
- **Undo with single object** (should restore to original state)

## Document and Portfolio Access

```javascript
// Current document
var doc = document;

// Portfolio (contains all canvases)
var portfolio = doc.portfolio;

// Access canvases by index (portfolio.canvases is read-only)
var firstCanvas = portfolio.canvases[0];
var canvasCount = portfolio.canvases.length;

// Current selection
var selection = doc.windows[0].selection;
var canvas = selection.canvas;
var graphics = selection.graphics;

// Find canvas by name
function getCanvasByName(name) {
    for (var i = 0; i < portfolio.canvases.length; i++) {
        if (portfolio.canvases[i].name === name) {
            return portfolio.canvases[i];
        }
    }
    return null;
}
```

## Documentation Resources

- Main docs: <https://omni-automation.com/omnigraffle/>
- API reference: <https://omni-automation.com/omnigraffle/OG-API.html>
- Plugin structure: <https://omni-automation.com/plugins/>
