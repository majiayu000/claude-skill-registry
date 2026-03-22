---
name: focus
description: This skill should be used when the user asks questions about OpenHarmony ArkUI focus system, including focus navigation (direction keys, Tab key), focus events (onFocus, onBlur, onKey), focus properties (focusOnTouch, defaultFocus, tabIndex, groupDefaultFocus), focus styles (FocusBox, FocusPattern), FocusManager, FocusView, FocusHub, FocusEventHandler, FocusModifier, keyboard navigation, remote control navigation, accessibility focus support, focus chain management, and focus rendering. Covers both ArkTS application layer and C++ implementation layer.
version: 1.0.0
---

# OpenHarmony ArkUI Focus System Skill

This skill provides comprehensive support for analyzing and understanding OpenHarmony ArkUI focus system, including focus navigation, event handling, style rendering, and accessibility support.

## Focus System Overview

OpenHarmony ArkUI implements a comprehensive focus management system that handles user interface focus interactions for keyboard, remote control, touch, and other input methods.

### Core Architecture

The focus system consists of three main layers:

**Application Layer (ArkTS/JS)**:
- Focus properties: `focusOnTouch`, `defaultFocus`, `tabIndex`
- Focus events: `onFocus`, `onBlur`, `onKey`

**Bridge Layer**:
- JSFocusFunction
- ArkTS Native Interface (ANI)

**C++ Implementation Layer**:
- FocusManager: Global focus management
- FocusView: View container management
- FocusHub: Core focus hub
- FocusEventHandler: Event processing
- FocusModifier: Focus box rendering

### Key Components

- **FocusManager**: Global focus state manager, manages FocusView stack
- **FocusView**: Focusable view container (Window, Dialog, Overlay)
- **FocusHub**: Core focus hub, manages node focus state
- **FocusEventHandler**: Handles keyboard and direction key events
- **FocusBox**: Defines focus box visual style
- **FocusPattern**: Defines node focus behavior pattern
- **FocusModifier**: Renders focus box in RenderService layer

## Code Locations

### Core Focus Code

Located at: `/home/z00576141/workspace/lxc_rom_0202/code/foundation/arkui/ace_engine/frameworks/core/components_ng/`

```
components_ng/
├── event/                        # Focus event layer
│   ├── focus_hub.h               # Core focus hub (line 45)
│   ├── focus_event_handler.h     # Focus event handler (line 106)
│   ├── focus_box.h               # Focus box style (line 29)
│   ├── focus_state.h             # Focus state definitions
│   └── focus_type.h              # Focus type definitions (line 23)
├── manager/focus/                # Focus management layer
│   ├── focus_manager.h           # FocusManager class (line 171)
│   └── focus_view.h              # FocusView class (line 30)
└── render/adapter/               # Focus render layer
    ├── focus_modifier.h          # Focus rendering modifier
    ├── focus_state_modifier.h    # Focus state modifier
    └── focus_animation_modifier.h # Focus animation modifier
```

### Accessibility Support

Located at: `/home/z00576141/workspace/lxc_rom_0202/code/foundation/arkui/ace_engine/adapter/ohos/osal/accessibility/focus_move/`

**Key files**:
- `accessibility_focus_strategy.cpp/h` - Focus movement strategy
- `accessibility_focus_move_osal.cpp/h` - Focus movement OSAL
- `accessibility_focus_frame_node_utils.cpp/h` - FrameNode utilities
- `accessibility_third_node_utils.cpp/h` - Third-party node utilities

### Bridge Layer

Located at: `/home/z00576141/workspace/lxc_rom_0202/code/foundation/arkui/ace_engine/frameworks/bridge/declarative_frontend/engine/functions/`

**Key files**:
- `js_focus_function.cpp/h` - JS focus function interface

Located at: `/home/z00576141/workspace/lxc_rom_0202/code/foundation/arkui/ace_engine/frameworks/bridge/declarative_frontend/engine/jsi/nativeModule/`

**Key files**:
- `arkts_native_common_bridge.cpp` - ANI bridge implementations

## Focus Type System

### FocusType Enum

**File**: `focus_type.h:23`

```cpp
enum class FocusType : int32_t {
    DISABLE = 0,  // Focus disabled
    NODE = 1,     // Focusable leaf node (Button, TextInput)
    SCOPE = 2,    // Focusable container (Row, Column, Grid)
};
```

**Usage**:
- **DISABLE**: Node does not participate in focus system
- **NODE**: Focusable terminal node
- **SCOPE**: Focus container that manages child node focus

### FocusStyleType Enum

**File**: `focus_type.h:29`

```cpp
enum class FocusStyleType : int32_t {
    NONE = -1,           // No style
    INNER_BORDER = 0,    // Inner border
    OUTER_BORDER = 1,    // Outer border
    CUSTOM_BORDER = 2,   // Custom border
    CUSTOM_REGION = 3,   // Custom region
    FORCE_BORDER = 4,    // Force border
    FORCE_NONE = 5,      // Force no border
};
```

### FocusStep Enum

**File**: `focus_type.h:48`

```cpp
enum class FocusStep : int32_t {
    NONE = 0x0,
    LEFT = 0x1,       // Move left
    UP = 0x2,         // Move up
    RIGHT = 0x11,     // Move right
    DOWN = 0x12,      // Move down
    LEFT_END = 0x3,   // Move left to edge
    UP_END = 0x4,     // Move up to edge
    RIGHT_END = 0x13,  // Move right to edge
    DOWN_END = 0x14,  // Move down to edge
    SHIFT_TAB = 0x5,  // Previous (Shift+Tab)
    TAB = 0x15,        // Next (Tab)
};
```

### FocusIntension Enum

**File**: `focus_event_handler.h:45`

```cpp
enum class FocusIntension : int32_t {
    NONE = 0,
    LEFT, UP, RIGHT, DOWN,  // Direction keys
    TAB, SHIFT_TAB,          // Tab navigation
    HOME, END,               // Home/End keys
    SELECT, SPACE, ESC,      // Other keys
};
```

## Focus Navigation Flow

### Direction Key Navigation

```
User presses direction key
    ↓
KeyEvent dispatched to FocusHub
    ↓
FocusEventHandler.OnKeyEvent()
    ↓
Parse FocusIntension (LEFT/UP/RIGHT/DOWN)
    ↓
HandleFocusTravel() [focus_event_handler.h:127]
    ↓
Find next focusable node based on FocusStep
    ↓
FocusManager.RequestFocus(newFocusHub) [focus_manager.h:171]
    ↓
Focus switch successful
```

**Algorithm Key Points**:

1. **Current node check**: Check current focus node type (NODE/SCOPE)
2. **Child traversal**: SCOPE type traverses children to find candidate
3. **Parent delegation**: Delegate to parent SCOPE if unable to handle
4. **Candidate evaluation**: Evaluate candidates based on geometry, Tab order

### Tab Key Navigation

```
User presses Tab/Shift+Tab
    ↓
KeyEvent dispatched to FocusHub
    ↓
Parse as FocusStep::TAB or SHIFT_TAB
    ↓
Find next node by tabIndex order
    ↓
Request focus to target node
    ↓
Update focus state
```

**Tab Order Rules**:
1. Priority by `tabIndex` ascending
2. Same `tabIndex` by document order
3. `tabIndex < 0` not in Tab navigation

### Default Focus

```
FocusView shows
    ↓
RequestDefaultFocus() [focus_view.h:67]
    ↓
Find defaultFocus=true node
    ↓
Find tabIndex minimum node
    ↓
Request focus to default node
    ↓
Focus set successfully
```

**Default Focus Priority**:
1. `defaultFocus=true` and `isGroupDefault=true` nodes
2. `defaultFocus=true` nodes
3. Smallest `tabIndex` focusable node

## Common Development Scenarios

### Scenario 1: Custom Focus Style

**Requirement**: Custom component focus box style

**Solution (ArkTS)**:

```typescript
@Component
struct CustomFocusButton {
  @State isFocused: boolean = false

  build() {
    Button('Click Me')
      .border({
        width: this.isFocused ? 2 : 0,
        color: this.isFocused ? Color.Blue : Color.Transparent,
        radius: 8
      })
      .onFocus(() => {
        this.isFocused = true
      })
      .onBlur(() => {
        this.isFocused = false
      })
  }
}
```

**C++ Layer Implementation**:
- `focus_modifier.h:30` - FocusModifier sets focus box
- `focus_box.h:29` - FocusBox style definition

### Scenario 2: Focus Navigation Control

**Requirement**: Custom direction key navigation logic

**Solution (ArkTS)**:

```typescript
@Component
struct CustomFocusNavigation {
  @State currentIndex: number = 0
  private items: string[] = ['Item 1', 'Item 2', 'Item 3', 'Item 4']

  build() {
    Column() {
      ForEach(this.items, (item: string, index: number) => {
        Text(item)
          .tabIndex(index + 1)
          .borderWidth(this.currentIndex === index ? 2 : 1)
          .onFocus(() => {
            this.currentIndex = index
          })
      })
    }
  }
}
```

**C++ Layer**:
- `focus_event_handler.h:127` - `HandleFocusTravel()` virtual function
- `focus_type.h:48` - `FocusStep` enum definition

### Scenario 3: Focus Group Management

**Requirement**: Manage focus between multiple areas

**Solution (ArkTS)**:

```typescript
@Component
struct FocusGroupExample {
  @State activeGroup: number = 1

  build() {
    Column() {
      // Group 1
      Row() {
        Button('A1').tabIndex(1)
        Button('A2').tabIndex(2)
      }
      .groupDefaultFocus(this.activeGroup === 1)
      .onFocus(() => {
        this.activeGroup = 1
      })

      // Group 2
      Row() {
        Button('B1').tabIndex(3)
        Button('B2').tabIndex(4)
      }
      .groupDefaultFocus(this.activeGroup === 2)
      .onFocus(() => {
        this.activeGroup = 2
      })
    }
  }
}
```

**C++ Layer**:
- `focus_hub.h:97` - `isDefaultGroupFocus_` group default focus
- `focus_manager.h:171` - FocusType::SCOPE management

### Scenario 4: Default Focus Setting

**Requirement**: Auto-focus on specified element when page loads

**Solution (ArkTS)**:

```typescript
@Entry
@Component
struct DefaultFocusPage {
  build() {
    Column() {
      TextInput({ placeholder: 'Username' })
        .defaultFocus(true)    // Auto-focus on page load
        .tabIndex(1)

      TextInput({ placeholder: 'Password' })
        .tabIndex(2)

      Button('Login')
        .tabIndex(3)
    }
  }
}
```

### Scenario 5: Focus Event Handling

**Requirement**: Monitor and handle various focus events

**Solution (ArkTS)**:

```typescript
@Component
struct FocusEventExample {
  build() {
    Column() {
      Button('Focus Event Demo')
        .onFocus(() => {
          console.log('Gained focus')
        })
        .onBlur(() => {
          console.log('Lost focus')
        })
        .onKey((event: KeyEvent) => {
          // Handle key events
          switch (event.type) {
            case KeyType.Down:
              console.log('Key down: ' + event.keyCode)
              break
            case KeyType.Up:
              console.log('Key up: ' + event.keyCode)
              break
          }
        })
    }
  }
}
```

**C++ Layer Event Dispatch**:
- `focus_event_handler.h:130` - Event callback macro definitions
- `focus_event_handler.h:106` - FocusIntention enum

## API Mapping

### ArkTS to C++ Layer Mapping

| ArkTS Property | C++ Property | Setter Method |
|----------------|-------------|---------------|
| `focusOnTouch` | FocusPattern::focusOnTouch | `SetFocusOnTouch()` |
| `defaultFocus` | FocusPattern::defaultFocus | `SetDefaultFocus()` |
| `tabIndex` | FocusPattern::tabIndex | `SetTabIndex()` |
| `groupDefaultFocus` | FocusPattern::isGroupDefault | `SetIsGroupDefault()` |
| `onFocus` | FocusCallbackEvents::onFocusCallback_ | `SetOnFocusCallback()` |
| `onBlur` | FocusCallbackEvents::onBlurCallback_ | `SetOnBlurCallback()` |
| `onKey` | FocusCallbackEvents::onKeyEventCallback_ | `SetOnKeyCallback()` |

### Bridge Code Example

**File**: `frameworks/bridge/declarative_frontend/engine/jsi/nativeModule/arkts_native_common_bridge.cpp`

```cpp
// Set focusOnTouch
ArkUINativeModuleValue SetFocusOnTouch(ArkUIRuntimeCallInfo* runtimeCallInfo)
{
    EcmaVM* vm = runtimeCallInfo->GetVM();
    Local<JSValueRef> firstArg = runtimeCallInfo->GetCallArgRef(0);  // Node
    Local<JSValueRef> secondArg = runtimeCallInfo->GetCallArgRef(1); // Value

    auto node = nodePtr(firstArg->ToNativePointer(vm)->Value());
    bool focusOnTouch = secondArg->ToBoolean(vm)->Value();

    auto frameNode = GetFrameNodeByNode(node);
    CHECK_NULL_RETURN(frameNode, panda::JSValueRef::Undefined(vm));

    auto focusHub = frameNode->GetFocusHub();
    CHECK_NULL_RETURN(focusHub, panda::JSValueRef::Undefined(vm));

    focusHub->SetFocusOnTouch(focusOnTouch);

    return panda::JSValueRef::Undefined(vm);
}
```

## Debugging Tips

### 1. Focus State Checking

```typescript
// Print focus state in component
.onFocus(() => {
  console.log(`Element focused: ${this.id}`)
  console.log(`Is focused: ${this.isFocused}`)
})
```

### 2. Focus Tree Viewing

```bash
# View focus tree using hdc tool
hdc shell aa dump --focus
```

### 3. Log Tracing (C++ Layer)

```cpp
// Add logs at key locations
LOGI("FocusHub::RequestFocusImmediately nodeId=%{public}d", id_);
LOGI("FocusManager::RequestFocus result=%{public}d", result);
```

## Common Issues

### Issue 1: Focus Box Not Visible

**Checklist**:
- [ ] Component `focusable` property is true
- [ ] `FocusStyleType` configuration is correct
- [ ] `FocusBox` style is set
- [ ] `FocusModifier` is correctly applied
- [ ] Node actually has focus (`IsFocused()` returns true)

### Issue 2: Focus Cannot Move

**Possible causes**:
1. Focus chain configuration error
2. Parent node not set as SCOPE type
3. Node disabled or hidden
4. Focus priority conflict

### Issue 3: Tab Key Order Incorrect

**Check points**:
- `tabIndex` values set as expected
- No negative `tabIndex` (not in Tab navigation)
- Document order for same `tabIndex` nodes

**Correct configuration**:
```typescript
Column() {
  Button('First').tabIndex(1)     // First focus
  Button('Second').tabIndex(2)    // Second
  Button('Third').tabIndex(3)     // Third
  Button('Skip').tabIndex(-1)     // Not in Tab nav
}
```

## Best Practices

### 1. Focus Design Principles

- **Predictability**: Focus movement should be intuitive (left→right, top→bottom)
- **Visibility**: Focus box should be clearly visible
- **Consistency**: Same component types should have same focus behavior
- **Efficiency**: Minimize focus movement steps

### 2. Performance Optimization

- Avoid deep focus tree nesting (< 5 layers recommended)
- Use SCOPE type appropriately to reduce traversal range
- Lazy load complex interface focus trees
- Reuse FocusHub instances

### 3. Accessibility Support

- Set appropriate `tabIndex` for all interactive elements
- Provide meaningful `onFocus`/`onBlur` callbacks
- Support keyboard navigation
- Implement focus movement logic for custom components

## Search Patterns

```bash
# Find focus-related files
find ace_engine -name "*focus*"

# Find FocusHub usage
grep -r "GetFocusHub()" frameworks/core/components_ng

# Find focus event handling
grep -r "OnKeyEvent\|OnFocus\|OnBlur" frameworks/core/components_ng

# Find focus styles
grep -r "FocusBox\|FocusPattern" frameworks/core/components_ng
```

## Reference Files

| File | Description |
|------|-------------|
| `focus_hub.h:45` | FocusHub class definition |
| `focus_manager.h:171` | FocusManager class definition |
| `focus_view.h:30` | FocusView class definition |
| `focus_type.h:23` | FocusType enum |
| `focus_event_handler.h:125` | HandleFocusTravel method |
| `focus_modifier.h:30` | FocusModifier rendering |

---

**Skill version**: 1.0.0
**Last updated**: 2025-02-04
**Applicable version**: OpenHarmony API 12+
