---
name: unity-game-ui-toolkit-design
description: 'Game UI design using Unity''s UI Toolkit (USS/UXML/Flexbox). Includes
  game UI elements like HUD, health bars, inventory, skill bars, PanelSettings scaling,
  and Safe Area support. Use when: game UI desi'
---

---
name: unity-game-ui-toolkit-design
description: Game UI design using Unity's UI Toolkit (USS/UXML/Flexbox). Includes game UI elements like HUD, health bars, inventory, skill bars, PanelSettings scaling, and Safe Area support. Use when: game UI design, HUD creation, USS/UXML styling, Flexbox layout, PanelSettings configuration
allowed-tools:
  - mcp__unity-mcp-server__find_ui_elements
  - mcp__unity-mcp-server__click_ui_element
  - mcp__unity-mcp-server__get_ui_element_state
  - mcp__unity-mcp-server__set_ui_element_value
  - mcp__unity-mcp-server__simulate_ui_input
  - mcp__unity-mcp-server__add_component
  - mcp__unity-mcp-server__modify_component
  - mcp__unity-mcp-server__set_component_field
  - mcp__unity-mcp-server__list_components
  - mcp__unity-mcp-server__create_gameobject
  - mcp__unity-mcp-server__modify_gameobject
  - mcp__unity-mcp-server__find_gameobject
  - mcp__unity-mcp-server__manage_asset_database
  - mcp__unity-mcp-server__edit_structured
  - mcp__unity-mcp-server__create_class
  - mcp__unity-mcp-server__read
  - mcp__unity-mcp-server__get_symbols
---

# Unity Game UI Toolkit Design Skill

A skill for game UI design using Unity's UI Toolkit (USS/UXML/Flexbox). This comprehensive game UI design guide covers implementation patterns for game UI elements like HUD, health bars, inventory, dialogs, screen scaling with PanelSettings, and Safe Area support.

## Overview

UI Toolkit is Unity's next-generation UI system that builds UIs with an approach similar to web technologies (HTML/CSS).

| Feature | Details |
|---------|---------|
| Layout Engine | Yoga (CSS Flexbox subset implementation) |
| Styling | USS (Unity Style Sheets, CSS-like) |
| Markup | UXML (HTML-like) |
| Supported Version | Unity 2021.2+ (Unity 6.0+ recommended) |
| Use Cases | Game UI, Editor extensions |

## Game UI Types

Game UIs are classified into 4 types based on purpose and presentation method. Before starting implementation, clarify which type your UI belongs to.

### 1. Diegetic

UI that physically exists within the game world. Characters can also perceive it.

| Example | Game |
|---------|------|
| HP bar on suit's back | Dead Space |
| Car dashboard | Racing Games |
| Ammo count on weapon | Metro Exodus |
| Handheld map | Far Cry 2 |

```xml
<!-- UXML - Diegetic UI (placed in 3D space) -->
<ui:VisualElement class="diegetic-display">
    <ui:VisualElement class="diegetic-display__screen">
        <ui:Label class="diegetic-display__value" text="87" />
        <ui:Label class="diegetic-display__unit" text="%" />
    </ui:VisualElement>
</ui:VisualElement>
```

### 2. Non-Diegetic

Screen overlay. Pure player-facing information that characters cannot perceive.

| Example | Placement |
|---------|-----------|
| HP bar | Top-left |
| Minimap | Top-right |
| Skill bar | Bottom-center |
| Quest objectives | Right side |

```xml
<!-- UXML - Non-Diegetic HUD structure -->
<ui:VisualElement class="hud">
    <!-- Top-left: Player status -->
    <ui:VisualElement class="hud__top-left">
        <ui:VisualElement class="health-bar" />
        <ui:VisualElement class="mana-bar" />
    </ui:VisualElement>

    <!-- Top-right: Minimap -->
    <ui:VisualElement class="hud__top-right">
        <ui:VisualElement class="minimap" />
    </ui:VisualElement>

    <!-- Bottom-center: Action bar -->
    <ui:VisualElement class="hud__bottom-center">
        <ui:VisualElement class="action-bar" />
    </ui:VisualElement>
</ui:VisualElement>
```

### 3. Spatial

UI that exists within the game world but characters cannot perceive.

| Example |
|---------|
| HP bar above enemy's head |
| NPC name display |
| Interactable object icons |
| Path guide lines |

### 4. Meta

Expresses game state through screen effects. Not direct UI elements.

| Example | Representation |
|---------|----------------|
| Damage | Red vignette at screen edges |
| Low HP | Red pulse across entire screen |
| Status effects | Screen distortion/color changes |
| Underwater | Blue overlay |

```css
/* USS - Meta effect */
.meta-overlay {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(255, 0, 0, 0);
    transition-duration: 0.3s;
}

.meta-overlay--damage {
    background-color: rgba(255, 0, 0, 0.3);
}

.meta-overlay--low-health {
    /* Pulse animation */
}
```

## HUD Screen Layout

Game HUDs have established placement conventions. Players unconsciously expect this layout.

```
┌─────────────────────────────────────────────────────┐
│ [HP/MP/Status]                    [Minimap/Compass] │
│ [Buff/Debuff icons]               [Quest Objectives]│
│                                                     │
│                     Game Screen                     │
│                    (Focus Area)                     │
│                                                     │
│ [Chat]                                              │
│ [Log/Notifications]  [Skill Bar/Items] [Quick Slots]│
└─────────────────────────────────────────────────────┘
```

### Placement Principles

| Area | Elements | Reason |
|------|----------|--------|
| **Top-left** | HP, MP, Stamina | Most important status, gaze naturally goes there |
| **Top-right** | Minimap, Compass | Navigation info, frequently checked |
| **Bottom-center** | Skill bar, Action bar | Feels close to hands, corresponds to keyboard layout |
| **Bottom-right** | Inventory, Quick slots | Secondary info, affinity with mouse operation |
| **Bottom-left** | Chat, Log | Text info, social elements |
| **Right side vertical** | Quest objectives, Notifications | Additional info, temporary display |
| **Screen center** | Avoid | Don't obstruct gameplay visibility |

```css
/* USS - HUD grid layout */
.hud {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
}

.hud__top-left {
    position: absolute;
    left: 16px;
    top: 16px;
}

.hud__top-right {
    position: absolute;
    right: 16px;
    top: 16px;
}

.hud__bottom-center {
    position: absolute;
    left: 50%;
    bottom: 16px;
    translate: -50% 0;
}

.hud__bottom-left {
    position: absolute;
    left: 16px;
    bottom: 16px;
}

.hud__bottom-right {
    position: absolute;
    right: 16px;
    bottom: 80px; /* Above action bar */
}

.hud__right-side {
    position: absolute;
    right: 16px;
    top: 200px;
    width: 250px;
}
```

## Quick Start

### Basic UIDocument Setup

```javascript
// 1. Create GameObject with UIDocument
mcp__unity-mcp-server__create_gameobject({
  name: "UIManager"
})

// 2. Add UIDocument component
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/UIManager",
  componentType: "UIDocument"
})

// 3. Configure PanelSettings
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/UIManager",
  componentType: "UIDocument",
  fieldPath: "panelSettings",
  valueType: "objectReference",
  objectReference: {
    assetPath: "Assets/UI/PanelSettings.asset"
  }
})
```

## Core Concepts

### 1. PanelSettings (Screen Scaling)

PanelSettings is equivalent to uGUI's Canvas Scaler and controls UI scaling based on screen size.

#### Scale Mode List

| Mode | Use Case | Features |
|------|----------|----------|
| Constant Pixel Size | Desktop | 1:1 pixel correspondence (default) |
| Constant Physical Size | Multi-DPI | DPI independent, constant physical size |
| Scale With Screen Size | Mobile | Scales relative to reference resolution |

#### Scale With Screen Size Settings

```csharp
// PanelSettings configuration example
[CreateAssetMenu(menuName = "UI/Panel Settings")]
public class ResponsivePanelSettings : ScriptableObject
{
    // Create PanelSettings asset and configure:
    // Scale Mode: Scale With Screen Size
    // Reference Resolution: 1080 x 1920 (Portrait) or 1920 x 1080 (Landscape)
    // Screen Match Mode: Match Width Or Height
    // Match: 0 (Width priority for Portrait) / 1 (Height priority for Landscape)
}
```

#### Runtime Match Switching

```csharp
// OrientationScaleHandler.cs
using UnityEngine;
using UnityEngine.UIElements;

public class OrientationScaleHandler : MonoBehaviour
{
    [SerializeField] private PanelSettings panelSettings;
    private ScreenOrientation lastOrientation;

    void Update()
    {
        if (Screen.orientation != lastOrientation)
        {
            bool isPortrait = Screen.height > Screen.width;
            panelSettings.match = isPortrait ? 0f : 1f;
            lastOrientation = Screen.orientation;
        }
    }
}
```

### 2. Flexbox Layout

UI Toolkit uses the Yoga (Flexbox) layout engine. Web developers will find this CSS layout model familiar.

#### flex-direction

```css
/* USS - Vertical layout (default) */
.vertical-container {
    flex-direction: column;
}

/* USS - Horizontal layout */
.horizontal-container {
    flex-direction: row;
}
```

#### flex-grow / flex-shrink / flex-basis

```css
/* USS - Equal distribution */
.equal-child {
    flex-grow: 1;
    flex-basis: 0;  /* Ignore content size for equal distribution */
}

/* USS - Fixed size + flexible */
.fixed-header {
    flex-grow: 0;
    flex-shrink: 0;
    height: 60px;
}

.flexible-content {
    flex-grow: 1;
    flex-shrink: 1;
}
```

#### Percentage-based Sizing

```css
/* USS - Responsive sizing */
.responsive-panel {
    width: 80%;
    height: 100%;
    max-width: 600px;
}

.half-width {
    width: 50%;
}
```

#### align-items / justify-content

```css
/* USS - Center alignment */
.center-container {
    align-items: center;      /* Cross-axis center */
    justify-content: center;  /* Main-axis center */
}

/* USS - Space between + equal spacing */
.space-between-container {
    justify-content: space-between;
}

/* USS - End alignment */
.end-aligned {
    align-items: flex-end;
    justify-content: flex-end;
}
```

### 3. USS (Unity Style Sheets)

Define styles with CSS-like syntax.

#### Basic Syntax

```css
/* USS - Selector types */
.class-selector { }      /* Class selector */
#name-selector { }       /* Name selector */
Button { }               /* Type selector */
.parent > .child { }     /* Direct child selector */
.parent .descendant { }  /* Descendant selector */
.element:hover { }       /* Pseudo-class */
```

#### BEM Naming Convention

```css
/* Block */
.menu { }

/* Element */
.menu__item { }
.menu__title { }

/* Modifier */
.menu--horizontal { }
.menu__item--active { }
.menu__item--disabled { }
```

### 4. UXML (UI Markup Language)

Define UI structure with HTML-like syntax.

```xml
<?xml version="1.0" encoding="utf-8"?>
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:VisualElement class="root">
        <ui:VisualElement class="header">
            <ui:Label text="Title" class="header__title" />
        </ui:VisualElement>

        <ui:VisualElement class="content">
            <ui:ScrollView class="content__scroll">
                <ui:VisualElement class="content__list">
                    <!-- Dynamic items -->
                </ui:VisualElement>
            </ui:ScrollView>
        </ui:VisualElement>

        <ui:VisualElement class="footer">
            <ui:Button text="Action" class="footer__button" />
        </ui:VisualElement>
    </ui:VisualElement>
</ui:UXML>
```

## Mobile Responsive Design

### Responsive Layout Structure

```css
/* USS - Mobile responsive basic structure */
.root {
    flex-grow: 1;
    flex-direction: column;
}

.header {
    flex-shrink: 0;
    height: 60px;
    flex-direction: row;
    align-items: center;
    padding: 0 16px;
}

.content {
    flex-grow: 1;
    flex-shrink: 1;
}

.footer {
    flex-shrink: 0;
    height: 80px;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: 0 16px;
}
```

### Safe Area Support

UI Toolkit requires coordinate system conversion (Screen.safeArea uses bottom-left origin, UI Toolkit uses top-left origin).

```csharp
// SafeAreaController.cs
using UnityEngine;
using UnityEngine.UIElements;

public class SafeAreaController : MonoBehaviour
{
    private UIDocument uiDocument;
    private VisualElement safeAreaContainer;
    private Rect lastSafeArea;

    void Start()
    {
        uiDocument = GetComponent<UIDocument>();
        safeAreaContainer = uiDocument.rootVisualElement.Q<VisualElement>("safe-area");
        ApplySafeArea();
    }

    void Update()
    {
        if (Screen.safeArea != lastSafeArea)
        {
            ApplySafeArea();
        }
    }

    void ApplySafeArea()
    {
        Rect safeArea = Screen.safeArea;
        lastSafeArea = safeArea;

        // Convert to UI Toolkit coordinate system (top-left origin)
        float left = safeArea.x;
        float right = Screen.width - (safeArea.x + safeArea.width);
        float top = Screen.height - (safeArea.y + safeArea.height);
        float bottom = safeArea.y;

        // Consider PanelSettings scale
        var panelSettings = uiDocument.panelSettings;
        float scale = GetCurrentScale(panelSettings);

        safeAreaContainer.style.paddingLeft = left / scale;
        safeAreaContainer.style.paddingRight = right / scale;
        safeAreaContainer.style.paddingTop = top / scale;
        safeAreaContainer.style.paddingBottom = bottom / scale;
    }

    float GetCurrentScale(PanelSettings settings)
    {
        // Calculate scale for Scale With Screen Size
        if (settings.scaleMode == PanelScaleMode.ScaleWithScreenSize)
        {
            var refRes = settings.referenceResolution;
            float widthRatio = Screen.width / refRes.x;
            float heightRatio = Screen.height / refRes.y;
            return Mathf.Lerp(widthRatio, heightRatio, settings.match);
        }
        return 1f;
    }
}
```

```css
/* USS - Safe Area container */
#safe-area {
    flex-grow: 1;
    /* padding is set dynamically from C# */
}
```

### Dynamic Layout Switching (Media Query Alternative)

UI Toolkit doesn't support CSS @media queries, so switch styles dynamically with C#.

```csharp
// ResponsiveLayoutController.cs
using UnityEngine;
using UnityEngine.UIElements;

public class ResponsiveLayoutController : MonoBehaviour
{
    private UIDocument uiDocument;
    private VisualElement root;
    private bool wasPortrait;

    void Start()
    {
        uiDocument = GetComponent<UIDocument>();
        root = uiDocument.rootVisualElement;
        ApplyOrientationLayout();
    }

    void Update()
    {
        bool isPortrait = Screen.height > Screen.width;
        if (isPortrait != wasPortrait)
        {
            ApplyOrientationLayout();
            wasPortrait = isPortrait;
        }
    }

    void ApplyOrientationLayout()
    {
        bool isPortrait = Screen.height > Screen.width;

        root.RemoveFromClassList("landscape");
        root.RemoveFromClassList("portrait");
        root.AddToClassList(isPortrait ? "portrait" : "landscape");

        // Layout based on screen width
        float screenWidth = Screen.width;
        root.RemoveFromClassList("narrow");
        root.RemoveFromClassList("wide");

        if (screenWidth < 600)
        {
            root.AddToClassList("narrow");
        }
        else
        {
            root.AddToClassList("wide");
        }
    }
}
```

```css
/* USS - Orientation-based styles */
.portrait .sidebar {
    display: none;
}

.landscape .sidebar {
    display: flex;
    width: 250px;
}

/* USS - Screen width-based styles */
.narrow .content__grid {
    flex-direction: column;
}

.wide .content__grid {
    flex-direction: row;
    flex-wrap: wrap;
}

.narrow .card {
    width: 100%;
}

.wide .card {
    width: 48%;
    margin: 1%;
}
```

## Game UI Elements Implementation

### 1. Health Bar / Resource Bar

```xml
<!-- UXML - Health bar -->
<ui:VisualElement class="resource-bar health-bar">
    <ui:VisualElement class="resource-bar__background">
        <ui:VisualElement class="resource-bar__fill" name="health-fill" />
        <ui:VisualElement class="resource-bar__delayed-fill" name="health-delayed" />
    </ui:VisualElement>
    <ui:Label class="resource-bar__text" name="health-text" text="100/100" />
</ui:VisualElement>
```

```css
/* USS - Resource bar */
.resource-bar {
    width: 200px;
    height: 24px;
    flex-direction: row;
    align-items: center;
}

.resource-bar__background {
    flex-grow: 1;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 4px;
    overflow: hidden;
}

.resource-bar__fill {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 100%;
    background-color: #e74c3c;
    transition-duration: 0.2s;
}

.resource-bar__delayed-fill {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 100%;
    background-color: #c0392b;
    transition-duration: 0.5s;
    transition-delay: 0.3s;
}

.resource-bar__text {
    position: absolute;
    left: 0;
    right: 0;
    -unity-text-align: middle-center;
    color: white;
    font-size: 12px;
    text-shadow: 1px 1px 2px black;
}

/* Variations */
.mana-bar .resource-bar__fill {
    background-color: #3498db;
}

.stamina-bar .resource-bar__fill {
    background-color: #2ecc71;
}

.xp-bar .resource-bar__fill {
    background-color: #9b59b6;
}
```

```csharp
// ResourceBarController.cs
public class ResourceBarController
{
    private VisualElement fill;
    private VisualElement delayedFill;
    private Label text;

    public void SetValue(float current, float max)
    {
        float percent = current / max;
        fill.style.width = Length.Percent(percent * 100);
        delayedFill.style.width = Length.Percent(percent * 100);
        text.text = $"{(int)current}/{(int)max}";
    }
}
```

### 2. Skill Cooldown

```xml
<!-- UXML - Skill slot -->
<ui:VisualElement class="skill-slot">
    <ui:VisualElement class="skill-slot__icon" />
    <ui:VisualElement class="skill-slot__cooldown-overlay" name="cooldown-overlay" />
    <ui:Label class="skill-slot__cooldown-text" name="cooldown-text" />
    <ui:Label class="skill-slot__keybind" text="Q" />
</ui:VisualElement>
```

```css
/* USS - Skill slot */
.skill-slot {
    width: 64px;
    height: 64px;
    margin: 4px;
    background-color: rgba(0, 0, 0, 0.6);
    border-width: 2px;
    border-color: #555;
    border-radius: 8px;
}

.skill-slot__icon {
    position: absolute;
    left: 4px;
    top: 4px;
    right: 4px;
    bottom: 4px;
    background-image: resource("Icons/skill_placeholder");
}

.skill-slot__cooldown-overlay {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    /* Circular mask implemented with shader */
}

.skill-slot__cooldown-text {
    position: absolute;
    left: 0;
    right: 0;
    top: 50%;
    translate: 0 -50%;
    -unity-text-align: middle-center;
    font-size: 20px;
    color: white;
    -unity-font-style: bold;
}

.skill-slot__keybind {
    position: absolute;
    right: 2px;
    bottom: 2px;
    font-size: 12px;
    color: #aaa;
    background-color: rgba(0, 0, 0, 0.5);
    padding: 2px 4px;
    border-radius: 2px;
}

.skill-slot--ready {
    border-color: #f39c12;
}

.skill-slot--active {
    border-color: #2ecc71;
    border-width: 3px;
}
```

### 3. Inventory Grid

```xml
<!-- UXML - Inventory -->
<ui:VisualElement class="inventory-panel">
    <ui:VisualElement class="inventory-panel__header">
        <ui:Label text="Inventory" class="inventory-panel__title" />
        <ui:Button class="inventory-panel__close" text="×" />
    </ui:VisualElement>
    <ui:VisualElement class="inventory-panel__grid" name="inventory-grid">
        <!-- Dynamically generated -->
    </ui:VisualElement>
    <ui:VisualElement class="inventory-panel__footer">
        <ui:Label name="gold-label" text="Gold: 0" />
        <ui:Label name="weight-label" text="Weight: 0/100" />
    </ui:VisualElement>
</ui:VisualElement>
```

```css
/* USS - Inventory */
.inventory-panel {
    width: 400px;
    background-color: rgba(20, 20, 30, 0.95);
    border-width: 2px;
    border-color: #444;
    border-radius: 8px;
}

.inventory-panel__header {
    height: 40px;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    background-color: rgba(0, 0, 0, 0.3);
    border-bottom-width: 1px;
    border-bottom-color: #333;
}

.inventory-panel__grid {
    flex-direction: row;
    flex-wrap: wrap;
    padding: 8px;
}

.inventory-slot {
    width: 48px;
    height: 48px;
    margin: 2px;
    background-color: rgba(0, 0, 0, 0.4);
    border-width: 1px;
    border-color: #333;
    border-radius: 4px;
}

.inventory-slot:hover {
    border-color: #666;
    background-color: rgba(255, 255, 255, 0.1);
}

.inventory-slot--selected {
    border-color: #f39c12;
    border-width: 2px;
}

.inventory-slot__icon {
    position: absolute;
    left: 4px;
    top: 4px;
    right: 4px;
    bottom: 12px;
}

.inventory-slot__count {
    position: absolute;
    right: 2px;
    bottom: 2px;
    font-size: 10px;
    color: white;
    background-color: rgba(0, 0, 0, 0.6);
    padding: 1px 3px;
    border-radius: 2px;
}

/* Item rarity */
.inventory-slot--common { border-color: #aaa; }
.inventory-slot--uncommon { border-color: #2ecc71; }
.inventory-slot--rare { border-color: #3498db; }
.inventory-slot--epic { border-color: #9b59b6; }
.inventory-slot--legendary { border-color: #f39c12; }
```

### 4. Damage Numbers (Floating Text)

```csharp
// DamageNumberController.cs
using UnityEngine;
using UnityEngine.UIElements;

public class DamageNumberController : MonoBehaviour
{
    [SerializeField] private UIDocument uiDocument;
    [SerializeField] private VisualTreeAsset damageNumberTemplate;

    public void SpawnDamageNumber(Vector3 worldPos, int damage, DamageType type)
    {
        var root = uiDocument.rootVisualElement;
        var damageLabel = damageNumberTemplate.Instantiate();

        var label = damageLabel.Q<Label>("damage-text");
        label.text = damage.ToString();

        // Style based on damage type
        switch (type)
        {
            case DamageType.Critical:
                label.AddToClassList("damage-number--critical");
                label.text = damage.ToString() + "!";
                break;
            case DamageType.Heal:
                label.AddToClassList("damage-number--heal");
                label.text = "+" + damage.ToString();
                break;
        }

        // Convert world coordinates to screen coordinates
        Vector2 screenPos = Camera.main.WorldToScreenPoint(worldPos);
        // Convert to UI Toolkit coordinate system (Y-axis inverted)
        float uiY = Screen.height - screenPos.y;

        damageLabel.style.position = Position.Absolute;
        damageLabel.style.left = screenPos.x;
        damageLabel.style.top = uiY;

        root.Add(damageLabel);

        // Remove after animation
        damageLabel.schedule.Execute(() => {
            damageLabel.RemoveFromHierarchy();
        }).ExecuteLater(1000);
    }
}
```

```css
/* USS - Damage numbers */
.damage-number {
    position: absolute;
    font-size: 24px;
    color: white;
    -unity-font-style: bold;
    text-shadow: 2px 2px 4px black;
    transition-property: translate, opacity;
    transition-duration: 1s;
    translate: 0 0;
    opacity: 1;
}

.damage-number--animate {
    translate: 0 -50px;
    opacity: 0;
}

.damage-number--critical {
    font-size: 36px;
    color: #e74c3c;
}

.damage-number--heal {
    color: #2ecc71;
}

.damage-number--miss {
    color: #888;
    font-size: 18px;
}
```

### 5. Minimap

```xml
<!-- UXML - Minimap -->
<ui:VisualElement class="minimap">
    <ui:VisualElement class="minimap__frame">
        <ui:VisualElement class="minimap__content" name="minimap-content">
            <!-- RenderTexture set as background -->
        </ui:VisualElement>
        <ui:VisualElement class="minimap__player-icon" />
        <ui:VisualElement class="minimap__markers" name="minimap-markers">
            <!-- Dynamic markers -->
        </ui:VisualElement>
    </ui:VisualElement>
    <ui:VisualElement class="minimap__compass">
        <ui:Label text="N" class="minimap__compass-label" />
    </ui:VisualElement>
</ui:VisualElement>
```

```css
/* USS - Minimap */
.minimap {
    width: 180px;
    height: 180px;
}

.minimap__frame {
    width: 100%;
    height: 100%;
    border-radius: 90px; /* Circular */
    border-width: 3px;
    border-color: rgba(0, 0, 0, 0.8);
    overflow: hidden;
}

.minimap__content {
    width: 100%;
    height: 100%;
    /* RenderTexture set from C# */
}

.minimap__player-icon {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 12px;
    height: 12px;
    translate: -50% -50%;
    background-color: #3498db;
    border-radius: 6px;
    border-width: 2px;
    border-color: white;
}

.minimap__marker {
    position: absolute;
    width: 8px;
    height: 8px;
    border-radius: 4px;
}

.minimap__marker--enemy {
    background-color: #e74c3c;
}

.minimap__marker--quest {
    background-color: #f39c12;
}

.minimap__marker--poi {
    background-color: #2ecc71;
}
```

### 6. Dialog System

```xml
<!-- UXML - Dialog box -->
<ui:VisualElement class="dialog-box">
    <ui:VisualElement class="dialog-box__portrait" name="portrait" />
    <ui:VisualElement class="dialog-box__content">
        <ui:Label class="dialog-box__speaker" name="speaker-name" />
        <ui:Label class="dialog-box__text" name="dialog-text" />
    </ui:VisualElement>
    <ui:VisualElement class="dialog-box__choices" name="choices-container">
        <!-- Dynamic choices -->
    </ui:VisualElement>
    <ui:VisualElement class="dialog-box__continue-indicator" />
</ui:VisualElement>
```

```css
/* USS - Dialog box */
.dialog-box {
    position: absolute;
    left: 10%;
    right: 10%;
    bottom: 10%;
    min-height: 150px;
    background-color: rgba(0, 0, 0, 0.85);
    border-width: 2px;
    border-color: #444;
    border-radius: 8px;
    flex-direction: row;
    padding: 16px;
}

.dialog-box__portrait {
    width: 120px;
    height: 120px;
    border-width: 2px;
    border-color: #666;
    border-radius: 4px;
    margin-right: 16px;
    flex-shrink: 0;
}

.dialog-box__content {
    flex-grow: 1;
    flex-direction: column;
}

.dialog-box__speaker {
    font-size: 18px;
    color: #f39c12;
    -unity-font-style: bold;
    margin-bottom: 8px;
}

.dialog-box__text {
    font-size: 16px;
    color: white;
    white-space: normal;
    flex-grow: 1;
}

.dialog-box__choices {
    flex-direction: column;
    margin-top: 12px;
}

.dialog-choice {
    padding: 8px 16px;
    margin: 4px 0;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    color: white;
}

.dialog-choice:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

.dialog-choice--selected {
    background-color: rgba(243, 156, 18, 0.3);
    border-left-width: 3px;
    border-left-color: #f39c12;
}

.dialog-box__continue-indicator {
    position: absolute;
    right: 16px;
    bottom: 16px;
    width: 16px;
    height: 16px;
    /* For blink animation */
}
```

## Performance Best Practices

### 1. Avoid Inline Styles

```csharp
// NG - Performance degradation
element.style.backgroundColor = Color.red;
element.style.width = 100;
element.style.height = 50;

// OK - Use USS classes
element.AddToClassList("highlighted-button");
```

### 2. :hover Pseudo-class Optimization

```css
/* NG - :hover on all elements degrades performance */
.button:hover {
    background-color: #444;
}

/* OK - Use only when necessary, or combine with :focus */
.interactive-button:hover,
.interactive-button:focus {
    background-color: #444;
}
```

### 3. Avoid Deep Nesting

```xml
<!-- NG - Too deep nesting -->
<ui:VisualElement>
    <ui:VisualElement>
        <ui:VisualElement>
            <ui:VisualElement>
                <ui:Label text="Deep" />
            </ui:VisualElement>
        </ui:VisualElement>
    </ui:VisualElement>
</ui:VisualElement>

<!-- OK - Flat structure -->
<ui:VisualElement class="container">
    <ui:Label text="Flat" />
</ui:VisualElement>
```

### 4. VisualElement Pooling

```csharp
// Use pooling for large numbers of dynamic elements
private Queue<VisualElement> elementPool = new Queue<VisualElement>();

VisualElement GetPooledElement()
{
    if (elementPool.Count > 0)
    {
        return elementPool.Dequeue();
    }
    return new VisualElement();
}

void ReturnToPool(VisualElement element)
{
    element.RemoveFromHierarchy();
    element.ClearClassList();
    elementPool.Enqueue(element);
}
```

## Tool Selection Guide

| Purpose | Recommended Tool |
|---------|------------------|
| UIDocument GameObject creation | `create_gameobject` + `add_component` |
| PanelSettings configuration | `set_component_field` |
| C# controller creation | `create_class` |
| UXML/USS file creation | `manage_asset_database` |
| UI element search | `find_ui_elements` |
| UI testing | `click_ui_element`, `simulate_ui_input` |
| UI state check | `get_ui_element_state` |

## Common Workflows

### 1. Creating Mobile Responsive UI

```javascript
// Step 1: Create GameObject for UIDocument
mcp__unity-mcp-server__create_gameobject({
  name: "ResponsiveUI"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/ResponsiveUI",
  componentType: "UIDocument"
})

// Step 2: Add responsive controller
mcp__unity-mcp-server__create_class({
  path: "Assets/Scripts/UI/ResponsiveLayoutController.cs",
  className: "ResponsiveLayoutController",
  baseType: "MonoBehaviour",
  namespace: "Game.UI",
  apply: true
})

// Step 3: Add Safe Area controller
mcp__unity-mcp-server__create_class({
  path: "Assets/Scripts/UI/SafeAreaController.cs",
  className: "SafeAreaController",
  baseType: "MonoBehaviour",
  namespace: "Game.UI",
  apply: true
})
```

### 2. Creating a Scroll View

```xml
<!-- UXML -->
<ui:ScrollView class="scroll-view" mode="Vertical">
    <ui:VisualElement class="scroll-content">
        <!-- Content items -->
    </ui:VisualElement>
</ui:ScrollView>
```

```css
/* USS */
.scroll-view {
    flex-grow: 1;
}

.scroll-content {
    flex-direction: column;
    padding: 16px;
}
```

### 3. Data Binding

```csharp
// DataBindingController.cs
using UnityEngine;
using UnityEngine.UIElements;

public class DataBindingController : MonoBehaviour
{
    [SerializeField] private UIDocument uiDocument;

    void Start()
    {
        var root = uiDocument.rootVisualElement;

        // Label binding
        var scoreLabel = root.Q<Label>("score-label");
        scoreLabel.text = "Score: 0";

        // Button event
        var button = root.Q<Button>("action-button");
        button.clicked += OnButtonClicked;

        // ListView
        var listView = root.Q<ListView>("item-list");
        listView.makeItem = () => new Label();
        listView.bindItem = (element, index) =>
        {
            (element as Label).text = $"Item {index}";
        };
        listView.itemsSource = new List<string> { "A", "B", "C" };
    }
}
```

## Common Mistakes

### 1. PanelSettings Not Configured

**NG**: UIDocument's PanelSettings is not set
- UI doesn't display
- Scaling doesn't work

**OK**: Create and set PanelSettings asset
- Select Scale With Screen Size
- Set Reference Resolution

### 2. flex-grow: 0 Unchanged

**NG**: Child elements don't fill parent
```css
.container { }  /* flex-grow: 0 is default */
```

**OK**: Explicitly set flex-grow
```css
.container {
    flex-grow: 1;
}
```

### 3. Safe Area Coordinate System Confusion

**NG**: Using Screen.safeArea directly
```csharp
// Position is off due to different coordinate systems
element.style.top = Screen.safeArea.y;
```

**OK**: Convert to UI Toolkit coordinate system
```csharp
float top = Screen.height - (Screen.safeArea.y + Screen.safeArea.height);
element.style.paddingTop = top / scale;
```

### 4. Using @media Queries

**NG**: Writing CSS media queries
```css
/* Does not work in UI Toolkit */
@media screen and (max-width: 600px) { }
```

**OK**: Switch classes dynamically with C#
```csharp
root.AddToClassList(isNarrow ? "narrow" : "wide");
```

### 5. Performance-Unaware Styles

**NG**: Frequent inline style changes
```csharp
void Update()
{
    element.style.left = Mathf.Sin(Time.time) * 100;
}
```

**OK**: Use transform
```csharp
void Update()
{
    element.transform.position = new Vector3(Mathf.Sin(Time.time) * 100, 0, 0);
}
```

## Tool Reference

### PanelSettings Scale Modes

| Property | Type | Description |
|----------|------|-------------|
| scaleMode | PanelScaleMode | Constant Pixel Size / Constant Physical Size / Scale With Screen Size |
| referenceResolution | Vector2Int | Reference resolution (for Scale With Screen Size) |
| screenMatchMode | PanelScreenMatchMode | Match Width Or Height / Expand / Shrink |
| match | float | 0 = Width priority, 1 = Height priority |
| referenceDpi | float | Reference DPI (for Constant Physical Size) |

### USS Flexbox Properties

| Property | Values | Default |
|----------|--------|---------|
| display | flex, none | flex |
| flex-direction | row, column, row-reverse, column-reverse | column |
| flex-grow | number | 0 |
| flex-shrink | number | 1 |
| flex-basis | length, auto | auto |
| align-items | flex-start, flex-end, center, stretch | stretch |
| justify-content | flex-start, flex-end, center, space-between, space-around | flex-start |
| flex-wrap | nowrap, wrap, wrap-reverse | nowrap |

### USS Size Properties

| Property | Values |
|----------|--------|
| width | length, %, auto |
| height | length, %, auto |
| min-width | length, % |
| max-width | length, % |
| min-height | length, % |
| max-height | length, % |

### C# VisualElement API

```csharp
// Class operations
element.AddToClassList("class-name");
element.RemoveFromClassList("class-name");
element.ToggleInClassList("class-name");
element.EnableInClassList("class-name", enabled);

// Style operations
element.style.display = DisplayStyle.Flex;
element.style.flexGrow = 1;
element.style.width = Length.Percent(100);

// Queries
root.Q<Button>("button-name");
root.Q<VisualElement>(className: "class-name");
root.Query<Label>().ToList();
```

## References

- [Unity Manual: Panel Settings](https://docs.unity3d.com/Manual/UIE-Runtime-Panel-Settings.html)
- [Unity Manual: USS Properties](https://docs.unity3d.com/Manual/UIE-USS-SupportedProperties.html)
- [Unity Manual: Layout Engine](https://docs.unity3d.com/Manual/UIE-LayoutEngine.html)
- [CSS Tricks: Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [2024 Guide to UI Toolkit](https://flexbuilder.ninja/2024/04/12/2024-guide-to-uitoolkit-for-unity-games/)
