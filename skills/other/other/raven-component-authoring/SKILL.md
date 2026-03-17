---
name: raven-component-authoring
description: Create or extend Raven UI components and modifiers (rendering to VNode/DOM, wiring events, managing state), including JavaScriptKit interop guidelines (DOMBridge, JSClosure, @MainActor).
---

# Raven Component Authoring

Use this skill when adding a new built-in Raven `View`/modifier (or fixing an existing one), especially if it needs custom DOM structure, event handling, or JavaScriptKit interop.

## Where Code Usually Goes

- New views:
  - `Sources/Raven/Views/Primitives/` for leaf-ish controls (Button, TextField, Toggle, etc.)
  - `Sources/Raven/Views/Layout/` for layout containers (VStack, Grid, ScrollView, etc.)
  - `Sources/Raven/Views/Navigation/` for navigation primitives
- New modifiers/wrappers:
  - `Sources/Raven/Modifiers/`
- DOM/JavaScriptKit bridge code:
  - `Sources/Raven/Rendering/DOMBridge.swift`
- Runtime rendering pipeline (coordinator/renderer):
  - `Sources/RavenRuntime/RenderLoop.swift`
  - `Sources/RavenRuntime/DOMRenderer.swift`

## Pick The Rendering Strategy

### 1) Composite View (no custom DOM work)

If the component is just composition, make it a normal `View` with a `body`:

```swift
@MainActor
public struct MyCard<Content: View>: View, Sendable {
    private let title: String
    private let content: Content

    @MainActor
    public init(_ title: String, @ViewBuilder content: () -> Content) {
        self.title = title
        self.content = content()
    }

    @MainActor public var body: some View {
        VStack(spacing: 12) {
            Text(title).font(.headline)
            content
        }
        .padding()
    }
}
```

### 2) Primitive View (custom DOM via VNode)

If you need to emit a specific DOM element tree, make it `PrimitiveView` (`Body == Never`).

Important rule of thumb:
- If you need to render child views and/or wire events: implement `_CoordinatorRenderable` (preferred).
- If it is truly a leaf and has no child views and no event wiring: `toVNode()` can be enough.

#### Preferred: `_CoordinatorRenderable` for events and child rendering

Implement `_render(with:)` so you can:
- render children via `context.renderChild(...)`
- register stable handlers via `context.registerClickHandler(...)` and `context.registerInputHandler(...)`
- persist controllers via `context.persistentState(create:)`

```swift
public struct MyButtonLike<Label: View>: View, PrimitiveView, Sendable {
    public typealias Body = Never

    private let action: @Sendable @MainActor () -> Void
    private let label: Label

    @MainActor
    public init(action: @escaping @Sendable @MainActor () -> Void, @ViewBuilder label: () -> Label) {
        self.action = action
        self.label = label()
    }
}

extension MyButtonLike: _CoordinatorRenderable {
    @MainActor public func _render(with context: any _RenderContext) -> VNode {
        let handlerID = context.registerClickHandler(action)
        let props: [String: VProperty] = [
            "onClick": .eventHandler(event: "click", handlerID: handlerID),
            "cursor": .style(name: "cursor", value: "pointer"),
        ]
        return VNode.element("button", props: props, children: [context.renderChild(label)])
    }
}
```

#### Leaf: `toVNode()` (only if you do not need coordinator services)

```swift
public struct Badge: View, PrimitiveView, Sendable {
    public typealias Body = Never
    private let text: String

    @MainActor public init(_ text: String) { self.text = text }

    @MainActor public func toVNode() -> VNode {
        VNode.element(
            "span",
            props: ["class": .attribute(name: "class", value: "raven-badge")],
            children: [.text(text)]
        )
    }
}
```

If you put `.eventHandler(...)` in `toVNode()` you will not be able to register the handler with the coordinator, so prefer `_CoordinatorRenderable` for anything interactive.

### 3) Modifier Wrapper: `_ModifierRenderable` (common pattern)

If the modifier is “wrap one child, add styles/attrs”, implement `_ModifierRenderable`:
- `toVNode()` builds the wrapper element (no children)
- default `_render(with:)` renders the wrapped content and splices it in

See: `Sources/Raven/Core/RenderProtocols.swift`.

## Event Handling Patterns

### Click-like events (no event payload)

- Use `context.registerClickHandler { ... }`
- Put the returned UUID into `.eventHandler(event: "click", handlerID: id)`

### Input/DOM events (need event payload)

- Use `context.registerInputHandler { (event: JSValue) in ... }`
- Common reads:
  - text input: `event.target.value.string`
  - checkbox: `event.target.checked.boolean`

Example (TextField-style):

```swift
let handlerID = context.registerInputHandler { event in
    if let newValue = event.target.value.string {
        binding.wrappedValue = newValue
    }
}

props["onInput"] = .eventHandler(event: "input", handlerID: handlerID)
props["value"] = .attribute(name: "value", value: binding.wrappedValue)
```

## State Guidance (Swift 6.2, WASM-Friendly)

- Local value state: `@State` (requires `Value: Sendable`).
- Two-way parent/child: `@Binding` for the child, pass `$state` from the parent.
- Shared model state:
  - Owner view: `@StateObject`
  - Child views: `@ObservedObject`
  - If using `ObservableObject` + `@Published`, call `setupPublished()` in `init()`.
- Non-view “controller” objects that must persist across renders (and may hold JSClosures/JSObjects):
  - In a `_CoordinatorRenderable` view, use `context.persistentState(create:)`.
  - Pattern example: `NavigationStack` in `Sources/Raven/Views/Navigation/NavigationStack.swift`.

## Keys And Stable Identity

Raven assigns stable `NodeID`s based on structural position after conversion. If your component produces a variable-length list of children and you need stable identity across inserts/removes/reorders, set `VNode.key` for each repeated child.

Rule of thumb: if you would use `ForEach(..., id:)` in SwiftUI, make sure the corresponding VNodes have stable keys somewhere along that repeated subtree.

## JavaScriptKit Interop Guidelines (DOMBridge Interface)

Default stance: components should describe DOM via `VNode` and let `DOMRenderer` + `DOMBridge` do the JS work. Only reach for JavaScriptKit directly when you truly need an imperative browser API.

When you do need JS interop:

- Keep JS-facing code `@MainActor`.
  - `JSObject`/`JSValue` are not `Sendable`; do not stash them in `Sendable` structs unless they are actor-isolated.
- Preserve JavaScript `this` binding.
  - Call methods directly on the object: `_ = element.setAttribute!(...)`, `_ = parent.appendChild!(...)`.
  - If you need helpers for tricky cases (like `addEventListener`), prefer the existing injected helpers:
    - `__ravenAddEventListener` / `__ravenRemoveEventListener` (in `Sources/RavenCLI/Generator/HTMLGenerator.swift`)
- JSClosure lifetime matters.
  - If you create a `JSClosure`, store it somewhere (dictionary/property) or it will be deallocated and stop firing.
  - Prefer putting JSClosure management inside `DOMBridge` or a persistent controller (`context.persistentState(create:)`).
- Avoid “fire-and-forget Task” from JS callbacks unless you know it runs in WASM’s event loop.
  - `DOMBridge.addGestureEventListener` intentionally calls handlers synchronously for reliability in WASM.

## Build / Validate (Don’t Overbuild)

1. Package checks:

```bash
swift test
```

2. If the change affects DOM behavior, verify via a WASM example build (prefer example apps to avoid unrelated CLI failures):

```bash
cd Examples/TodoApp
swift build --swift-sdk swift-6.2.3-RELEASE_wasm
```

3. Optional browser validation loop: use the existing `$raven-dev` skill.

