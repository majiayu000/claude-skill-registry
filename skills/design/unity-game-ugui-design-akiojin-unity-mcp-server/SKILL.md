---
name: unity-game-ugui-design
description: 'Game UI design using Unity''s uGUI (Canvas/RectTransform/Anchors). Includes
  game UI elements like HUD, health bars, inventory, skill bars, mobile responsive
  design, and Safe Area support. Use when: gam'
---

---
name: unity-game-ugui-design
description: Game UI design using Unity's uGUI (Canvas/RectTransform/Anchors). Includes game UI elements like HUD, health bars, inventory, skill bars, mobile responsive design, and Safe Area support. Use when: game UI design, HUD creation, Canvas setup, mobile UI, Anchors configuration
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
  - mcp__unity-mcp-server__get_component_types
  - mcp__unity-mcp-server__create_gameobject
  - mcp__unity-mcp-server__modify_gameobject
  - mcp__unity-mcp-server__find_gameobject
  - mcp__unity-mcp-server__get_hierarchy
  - mcp__unity-mcp-server__edit_structured
  - mcp__unity-mcp-server__create_class
  - mcp__unity-mcp-server__read
  - mcp__unity-mcp-server__get_symbols
---

# Unity Game uGUI Design Skill

A skill for game UI design using Unity's uGUI (Unity GUI) system. Provides a comprehensive game UI design guide including implementation patterns for game UI elements like HUD, health bars, inventory, dialogs, mobile responsive design, and Safe Area support.

## Quick Start

### Basic Canvas Setup

```javascript
// 1. Create Canvas
mcp__unity-mcp-server__create_gameobject({
  name: "Canvas"
})

// 2. Add Canvas component
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas",
  componentType: "Canvas",
  properties: {
    renderMode: 0  // ScreenSpaceOverlay
  }
})

// 3. Add CanvasScaler (responsive design)
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas",
  componentType: "CanvasScaler",
  properties: {
    uiScaleMode: 1,  // ScaleWithScreenSize
    referenceResolution: { x: 1080, y: 1920 },  // Reference resolution
    screenMatchMode: 0,  // MatchWidthOrHeight
    matchWidthOrHeight: 0  // 0=Portrait priority, 1=Landscape priority
  }
})

// 4. Add GraphicRaycaster (for interaction)
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas",
  componentType: "GraphicRaycaster"
})
```

## Game UI Types

Game UI is classified into 4 types based on placement and representation.

### 1. Diegetic UI

UI that exists within the game world. Characters can also perceive it.

- **Examples**: Enemy HP bar above head, car dashboard, in-game signboards
- **Canvas Setting**: World Space
- **Features**: High immersion, 3D space display

```javascript
// World Space Canvas (enemy HP bar above head)
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Enemy/HealthCanvas",
  componentType: "Canvas",
  properties: { renderMode: 2 }  // WorldSpace
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Enemy/HealthCanvas",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 100, y: 20 }
})
```

### 2. Non-Diegetic UI

Overlay UI visible only to the player.

- **Examples**: HUD, score display, minimap, skill bar
- **Canvas Setting**: Screen Space - Overlay
- **Features**: Always in front, screen-fixed

```javascript
// HUD overlay Canvas
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas",
  componentType: "Canvas",
  properties: { renderMode: 0 }  // ScreenSpaceOverlay
})
```

### 3. Spatial UI

UI that exists in 3D space but is not part of the game world.

- **Examples**: Destination marker, interact icon, quest marker
- **Canvas Setting**: Screen Space - Camera or World Space
- **Features**: Billboard (always faces camera)

```javascript
// Billboard marker
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/QuestMarker/Canvas",
  componentType: "Canvas",
  properties: { renderMode: 2 }  // WorldSpace
})

// Add billboard script
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/QuestMarker/Canvas",
  componentType: "BillboardUI"
})
```

### 4. Meta UI

Full-screen effect UI.

- **Examples**: Damage red flash, stamina depletion vignette, status effect overlay
- **Canvas Setting**: Screen Space - Overlay (frontmost sorting order)
- **Features**: Full screen, transparency animation

```javascript
// Damage flash Canvas
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/EffectCanvas",
  componentType: "Canvas",
  properties: {
    renderMode: 0,
    sortingOrder: 100  // Frontmost
  }
})

// Flash Image (full screen)
mcp__unity-mcp-server__create_gameobject({
  name: "DamageFlash",
  parentPath: "/EffectCanvas"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/EffectCanvas/DamageFlash",
  componentType: "Image",
  properties: {
    color: { r: 1, g: 0, b: 0, a: 0 }  // Transparent red
  }
})
```

---

## HUD Screen Layout

Game HUDs have industry-standard placement conventions.

### Standard Layout Diagram

```
┌─────────────────────────────────────────────────────┐
│  [HP/MP Bar]              [Mini Map] [Settings]     │  ← Top
│  ★ Top-Left: HP/MP/Stamina    Top-Right: Minimap, Settings
│                                                     │
│                                                     │
│  [Quest]                               [Buff Icons] │  ← Upper-Middle
│  ★ Quest objectives        Buff/Debuff icons        │
│                                                     │
│                      [Center]                       │
│                   Crosshair/Interact                │
│                                                     │
│  [Chat]                              [Inventory]    │  ← Lower-Middle
│                                                     │
│                                                     │
│          [Skill Bar]    [Action Buttons]            │  ← Bottom
│          ★ Skills/Items   Action buttons            │
└─────────────────────────────────────────────────────┘
```

### Placement Principles

| Position | Anchor | UI Elements | Reason |
|----------|--------|-------------|--------|
| Top-Left | (0,1) | HP/MP/Stamina | Critical info, minimal eye movement |
| Top-Right | (1,1) | Minimap, Settings | Auxiliary info, non-intrusive |
| Bottom-Left | (0,0) | Chat, Logs | Infrequently viewed info |
| Bottom-Right | (1,0) | Inventory, Buttons | Easy right-hand access |
| Bottom-Center | (0.5,0) | Skill bar | Two-hand access, high importance |
| Center | (0.5,0.5) | Crosshair, Interact | Center of vision |

### uGUI Implementation Example

```javascript
// HP Bar (top-left placement)
mcp__unity-mcp-server__create_gameobject({
  name: "HPBar",
  parentPath: "/HUDCanvas/SafeArea"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/HPBar",
  componentType: "RectTransform",
  fieldPath: "anchorMin",
  value: { x: 0, y: 1 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/HPBar",
  componentType: "RectTransform",
  fieldPath: "anchorMax",
  value: { x: 0, y: 1 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/HPBar",
  componentType: "RectTransform",
  fieldPath: "pivot",
  value: { x: 0, y: 1 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/HPBar",
  componentType: "RectTransform",
  fieldPath: "anchoredPosition",
  value: { x: 20, y: -20 }  // 20px margin from top-left
})

// Minimap (top-right placement)
mcp__unity-mcp-server__create_gameobject({
  name: "Minimap",
  parentPath: "/HUDCanvas/SafeArea"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/Minimap",
  componentType: "RectTransform",
  fieldPath: "anchorMin",
  value: { x: 1, y: 1 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/Minimap",
  componentType: "RectTransform",
  fieldPath: "anchorMax",
  value: { x: 1, y: 1 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/Minimap",
  componentType: "RectTransform",
  fieldPath: "pivot",
  value: { x: 1, y: 1 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/Minimap",
  componentType: "RectTransform",
  fieldPath: "anchoredPosition",
  value: { x: -20, y: -20 }  // 20px margin from top-right
})

// Skill Bar (bottom-center placement)
mcp__unity-mcp-server__create_gameobject({
  name: "SkillBar",
  parentPath: "/HUDCanvas/SafeArea"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar",
  componentType: "RectTransform",
  fieldPath: "anchorMin",
  value: { x: 0.5, y: 0 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar",
  componentType: "RectTransform",
  fieldPath: "anchorMax",
  value: { x: 0.5, y: 0 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar",
  componentType: "RectTransform",
  fieldPath: "pivot",
  value: { x: 0.5, y: 0 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar",
  componentType: "RectTransform",
  fieldPath: "anchoredPosition",
  value: { x: 0, y: 20 }  // 20px margin from bottom
})
```

---

## Game UI Elements

### 1. Health Bar / Resource Bar

Implements delayed damage display (red gauge gradually decreases after taking damage).

#### Prefab Structure

```
HealthBar (RectTransform)
├── Background (Image) - Background
├── DelayedFill (Image) - Delayed gauge (red)
├── Fill (Image) - Current value gauge (green)
└── Text (TextMeshProUGUI) - "100/100"
```

#### MCP Implementation

```javascript
// Create health bar
mcp__unity-mcp-server__create_gameobject({
  name: "HealthBar",
  parentPath: "/HUDCanvas/SafeArea"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/HealthBar",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 200, y: 24 }
})

// Background
mcp__unity-mcp-server__create_gameobject({
  name: "Background",
  parentPath: "/HUDCanvas/SafeArea/HealthBar"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/HealthBar/Background",
  componentType: "Image",
  properties: {
    color: { r: 0.1, g: 0.1, b: 0.1, a: 0.8 }
  }
})

// Delayed gauge (Filled Image)
mcp__unity-mcp-server__create_gameobject({
  name: "DelayedFill",
  parentPath: "/HUDCanvas/SafeArea/HealthBar"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/HealthBar/DelayedFill",
  componentType: "Image",
  properties: {
    color: { r: 0.8, g: 0.2, b: 0.2, a: 1 },
    type: 3,  // Filled
    fillMethod: 0,  // Horizontal
    fillAmount: 1.0
  }
})

// Current value gauge
mcp__unity-mcp-server__create_gameobject({
  name: "Fill",
  parentPath: "/HUDCanvas/SafeArea/HealthBar"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/HealthBar/Fill",
  componentType: "Image",
  properties: {
    color: { r: 0.2, g: 0.8, b: 0.2, a: 1 },
    type: 3,  // Filled
    fillMethod: 0,  // Horizontal
    fillAmount: 1.0
  }
})

// Text
mcp__unity-mcp-server__create_gameobject({
  name: "Text",
  parentPath: "/HUDCanvas/SafeArea/HealthBar"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/HealthBar/Text",
  componentType: "TextMeshProUGUI",
  properties: {
    text: "100/100",
    fontSize: 14,
    alignment: 514  // Center
  }
})
```

#### C# Controller

```csharp
// HealthBarController.cs
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class HealthBarController : MonoBehaviour
{
    [SerializeField] private Image fillImage;
    [SerializeField] private Image delayedFillImage;
    [SerializeField] private TextMeshProUGUI text;

    [SerializeField] private float delayedFillSpeed = 0.5f;

    private float currentHealth = 100f;
    private float maxHealth = 100f;
    private float delayedHealth = 100f;

    public void SetHealth(float health, float max)
    {
        currentHealth = Mathf.Clamp(health, 0, max);
        maxHealth = max;

        float ratio = currentHealth / maxHealth;
        fillImage.fillAmount = ratio;
        text.text = $"{(int)currentHealth}/{(int)maxHealth}";

        // When taking damage, delayed gauge stays
        // On healing, update immediately
        if (delayedHealth < currentHealth)
        {
            delayedHealth = currentHealth;
            delayedFillImage.fillAmount = ratio;
        }
    }

    void Update()
    {
        // Gradually decrease delayed gauge
        if (delayedHealth > currentHealth)
        {
            delayedHealth = Mathf.MoveTowards(
                delayedHealth,
                currentHealth,
                maxHealth * delayedFillSpeed * Time.deltaTime
            );
            delayedFillImage.fillAmount = delayedHealth / maxHealth;
        }
    }
}
```

---

### 2. Skill Cooldown

Displays remaining time with darkened overlay + rotating mask during cooldown.

#### Prefab Structure

```
SkillSlot (RectTransform)
├── Icon (Image) - Skill icon
├── CooldownOverlay (Image) - Darkened overlay (Radial Fill)
├── CooldownText (TextMeshProUGUI) - Remaining seconds
└── KeyHint (TextMeshProUGUI) - "Q"
```

#### MCP Implementation

```javascript
// Create skill slot
mcp__unity-mcp-server__create_gameobject({
  name: "SkillSlot",
  parentPath: "/HUDCanvas/SafeArea/SkillBar"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 64, y: 64 }
})

// Icon
mcp__unity-mcp-server__create_gameobject({
  name: "Icon",
  parentPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot/Icon",
  componentType: "Image"
})

// Cooldown overlay (Radial Fill)
mcp__unity-mcp-server__create_gameobject({
  name: "CooldownOverlay",
  parentPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot/CooldownOverlay",
  componentType: "Image",
  properties: {
    color: { r: 0, g: 0, b: 0, a: 0.7 },
    type: 3,  // Filled
    fillMethod: 4,  // Radial360
    fillOrigin: 2,  // Top
    fillClockwise: false,
    fillAmount: 0
  }
})

// Cooldown text
mcp__unity-mcp-server__create_gameobject({
  name: "CooldownText",
  parentPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot/CooldownText",
  componentType: "TextMeshProUGUI",
  properties: {
    text: "",
    fontSize: 20,
    alignment: 514,  // Center
    fontStyle: 1  // Bold
  }
})

// Key hint
mcp__unity-mcp-server__create_gameobject({
  name: "KeyHint",
  parentPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/SkillBar/SkillSlot/KeyHint",
  componentType: "TextMeshProUGUI",
  properties: {
    text: "Q",
    fontSize: 12,
    alignment: 257  // BottomLeft
  }
})
```

#### C# Controller

```csharp
// SkillSlotController.cs
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class SkillSlotController : MonoBehaviour
{
    [SerializeField] private Image icon;
    [SerializeField] private Image cooldownOverlay;
    [SerializeField] private TextMeshProUGUI cooldownText;

    private float cooldownDuration;
    private float cooldownRemaining;

    public void SetIcon(Sprite sprite)
    {
        icon.sprite = sprite;
    }

    public void StartCooldown(float duration)
    {
        cooldownDuration = duration;
        cooldownRemaining = duration;
    }

    public bool IsOnCooldown => cooldownRemaining > 0;

    void Update()
    {
        if (cooldownRemaining > 0)
        {
            cooldownRemaining -= Time.deltaTime;

            float ratio = cooldownRemaining / cooldownDuration;
            cooldownOverlay.fillAmount = ratio;

            if (cooldownRemaining > 1)
                cooldownText.text = Mathf.CeilToInt(cooldownRemaining).ToString();
            else if (cooldownRemaining > 0)
                cooldownText.text = cooldownRemaining.ToString("F1");
            else
            {
                cooldownText.text = "";
                cooldownOverlay.fillAmount = 0;
            }
        }
    }
}
```

---

### 3. Inventory Grid

Rarity-based border colors, stack count display, drag & drop support.

#### Prefab Structure

```
InventoryGrid (RectTransform + GridLayoutGroup)
└── ItemSlot (multiple)
    ├── Background (Image) - Rarity border
    ├── Icon (Image) - Item icon
    ├── StackCount (TextMeshProUGUI) - "x99"
    └── SelectionHighlight (Image) - Selection highlight
```

#### MCP Implementation

```javascript
// Create inventory grid
mcp__unity-mcp-server__create_gameobject({
  name: "InventoryGrid",
  parentPath: "/InventoryCanvas/Panel"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/InventoryCanvas/Panel/InventoryGrid",
  componentType: "GridLayoutGroup",
  properties: {
    cellSize: { x: 64, y: 64 },
    spacing: { x: 4, y: 4 },
    startCorner: 0,  // UpperLeft
    startAxis: 0,    // Horizontal
    childAlignment: 0,  // UpperLeft
    constraint: 1,  // FixedColumnCount
    constraintCount: 6  // 6 columns
  }
})

// Create item slot
mcp__unity-mcp-server__create_gameobject({
  name: "ItemSlot",
  parentPath: "/InventoryCanvas/Panel/InventoryGrid"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 64, y: 64 }
})

// Background (rarity border)
mcp__unity-mcp-server__create_gameobject({
  name: "Background",
  parentPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot/Background",
  componentType: "Image",
  properties: {
    color: { r: 0.3, g: 0.3, b: 0.3, a: 1 }  // Default (Common)
  }
})

// Icon
mcp__unity-mcp-server__create_gameobject({
  name: "Icon",
  parentPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot/Icon",
  componentType: "Image"
})

// Stack count
mcp__unity-mcp-server__create_gameobject({
  name: "StackCount",
  parentPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot/StackCount",
  componentType: "TextMeshProUGUI",
  properties: {
    text: "",
    fontSize: 12,
    alignment: 260  // BottomRight
  }
})

// Selection highlight
mcp__unity-mcp-server__create_gameobject({
  name: "SelectionHighlight",
  parentPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/InventoryCanvas/Panel/InventoryGrid/ItemSlot/SelectionHighlight",
  componentType: "Image",
  properties: {
    color: { r: 1, g: 1, b: 1, a: 0.3 },
    raycastTarget: false
  }
})
```

#### Rarity Color Definition

```csharp
// ItemRarity.cs
using UnityEngine;

public enum ItemRarity
{
    Common,    // Gray
    Uncommon,  // Green
    Rare,      // Blue
    Epic,      // Purple
    Legendary  // Orange
}

public static class RarityColors
{
    public static Color GetColor(ItemRarity rarity) => rarity switch
    {
        ItemRarity.Common => new Color(0.6f, 0.6f, 0.6f),
        ItemRarity.Uncommon => new Color(0.2f, 0.8f, 0.2f),
        ItemRarity.Rare => new Color(0.2f, 0.4f, 0.9f),
        ItemRarity.Epic => new Color(0.6f, 0.2f, 0.9f),
        ItemRarity.Legendary => new Color(1.0f, 0.5f, 0.0f),
        _ => Color.white
    };
}
```

---

### 4. Damage Numbers (Floating Text)

Effect where numbers float up and fade from the damage location.

#### Prefab Structure

```
DamageNumber (RectTransform)
└── Text (TextMeshProUGUI) - Damage value
```

#### MCP Implementation

```javascript
// Create damage number prefab
mcp__unity-mcp-server__create_gameobject({
  name: "DamageNumber",
  parentPath: "/WorldCanvas"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/WorldCanvas/DamageNumber",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 100, y: 40 }
})

// Text
mcp__unity-mcp-server__create_gameobject({
  name: "Text",
  parentPath: "/WorldCanvas/DamageNumber"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/WorldCanvas/DamageNumber/Text",
  componentType: "TextMeshProUGUI",
  properties: {
    text: "999",
    fontSize: 24,
    alignment: 514,  // Center
    fontStyle: 1,    // Bold
    color: { r: 1, g: 0.2, b: 0.2, a: 1 }
  }
})
```

#### C# Controller (with animation)

```csharp
// DamageNumberController.cs
using UnityEngine;
using TMPro;

public class DamageNumberController : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI text;
    [SerializeField] private float floatSpeed = 50f;
    [SerializeField] private float fadeSpeed = 2f;
    [SerializeField] private float lifetime = 1.5f;

    private float elapsed;
    private Color originalColor;
    private Vector3 randomOffset;

    public void Setup(int damage, bool isCritical = false)
    {
        text.text = damage.ToString();

        if (isCritical)
        {
            text.fontSize *= 1.5f;
            text.color = new Color(1f, 0.8f, 0f);  // Yellow
        }

        originalColor = text.color;
        randomOffset = new Vector3(Random.Range(-20f, 20f), 0, 0);
    }

    void Update()
    {
        elapsed += Time.deltaTime;

        // Float upward
        transform.localPosition += (Vector3.up * floatSpeed + randomOffset) * Time.deltaTime;
        randomOffset *= 0.95f;  // Dampen horizontal movement

        // Fade out
        if (elapsed > lifetime * 0.5f)
        {
            float alpha = Mathf.Lerp(originalColor.a, 0,
                (elapsed - lifetime * 0.5f) / (lifetime * 0.5f));
            text.color = new Color(originalColor.r, originalColor.g, originalColor.b, alpha);
        }

        if (elapsed >= lifetime)
        {
            Destroy(gameObject);
        }
    }
}
```

---

### 5. Minimap

Top-down minimap using RawImage and RenderTexture.

#### Structure

```
MinimapContainer (RectTransform)
├── MapImage (RawImage + Mask) - Map display
├── PlayerIcon (Image) - Player icon
├── Border (Image) - Border
└── CompassText (TextMeshProUGUI) - "N"
```

#### MCP Implementation

```javascript
// Minimap container
mcp__unity-mcp-server__create_gameobject({
  name: "MinimapContainer",
  parentPath: "/HUDCanvas/SafeArea"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/MinimapContainer",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 150, y: 150 }
})

// Map display (RawImage)
mcp__unity-mcp-server__create_gameobject({
  name: "MapImage",
  parentPath: "/HUDCanvas/SafeArea/MinimapContainer"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/MinimapContainer/MapImage",
  componentType: "RawImage"
})

// Circular mask
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/MinimapContainer/MapImage",
  componentType: "Mask",
  properties: {
    showMaskGraphic: false
  }
})

// Player icon (centered)
mcp__unity-mcp-server__create_gameobject({
  name: "PlayerIcon",
  parentPath: "/HUDCanvas/SafeArea/MinimapContainer"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/MinimapContainer/PlayerIcon",
  componentType: "Image"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/HUDCanvas/SafeArea/MinimapContainer/PlayerIcon",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 16, y: 16 }
})

// Border
mcp__unity-mcp-server__create_gameobject({
  name: "Border",
  parentPath: "/HUDCanvas/SafeArea/MinimapContainer"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/HUDCanvas/SafeArea/MinimapContainer/Border",
  componentType: "Image",
  properties: {
    raycastTarget: false
  }
})
```

---

### 6. Dialog System

RPG-style conversation window. Displays speaker name, text, and choices.

#### Prefab Structure

```
DialogPanel (RectTransform + CanvasGroup)
├── SpeakerName (TextMeshProUGUI)
├── Portrait (Image) - Speaker portrait
├── DialogText (TextMeshProUGUI) - Dialog text
├── ChoicesContainer (VerticalLayoutGroup)
│   └── ChoiceButton (Button + TextMeshProUGUI)
└── ContinueIndicator (Image) - Continue arrow
```

#### MCP Implementation

```javascript
// Dialog panel
mcp__unity-mcp-server__create_gameobject({
  name: "DialogPanel",
  parentPath: "/DialogCanvas"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/DialogCanvas/DialogPanel",
  componentType: "Image",
  properties: {
    color: { r: 0, g: 0, b: 0, a: 0.85 }
  }
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/DialogCanvas/DialogPanel",
  componentType: "CanvasGroup"
})

// Bottom stretch placement
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/DialogCanvas/DialogPanel",
  componentType: "RectTransform",
  fieldPath: "anchorMin",
  value: { x: 0, y: 0 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/DialogCanvas/DialogPanel",
  componentType: "RectTransform",
  fieldPath: "anchorMax",
  value: { x: 1, y: 0.3 }
})

// Speaker name
mcp__unity-mcp-server__create_gameobject({
  name: "SpeakerName",
  parentPath: "/DialogCanvas/DialogPanel"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/DialogCanvas/DialogPanel/SpeakerName",
  componentType: "TextMeshProUGUI",
  properties: {
    text: "Villager A",
    fontSize: 20,
    fontStyle: 1,  // Bold
    color: { r: 1, g: 0.9, b: 0.4, a: 1 }
  }
})

// Portrait
mcp__unity-mcp-server__create_gameobject({
  name: "Portrait",
  parentPath: "/DialogCanvas/DialogPanel"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/DialogCanvas/DialogPanel/Portrait",
  componentType: "Image"
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/DialogCanvas/DialogPanel/Portrait",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 100, y: 100 }
})

// Dialog text
mcp__unity-mcp-server__create_gameobject({
  name: "DialogText",
  parentPath: "/DialogCanvas/DialogPanel"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/DialogCanvas/DialogPanel/DialogText",
  componentType: "TextMeshProUGUI",
  properties: {
    text: "Hello, traveler.",
    fontSize: 18,
    alignment: 257  // TopLeft
  }
})

// Choices container
mcp__unity-mcp-server__create_gameobject({
  name: "ChoicesContainer",
  parentPath: "/DialogCanvas/DialogPanel"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/DialogCanvas/DialogPanel/ChoicesContainer",
  componentType: "VerticalLayoutGroup",
  properties: {
    spacing: 8,
    childAlignment: 4  // MiddleCenter
  }
})

// Continue indicator
mcp__unity-mcp-server__create_gameobject({
  name: "ContinueIndicator",
  parentPath: "/DialogCanvas/DialogPanel"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/DialogCanvas/DialogPanel/ContinueIndicator",
  componentType: "Image"
})
```

#### Typewriter Effect

```csharp
// DialogController.cs
using System.Collections;
using UnityEngine;
using TMPro;

public class DialogController : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI dialogText;
    [SerializeField] private GameObject continueIndicator;
    [SerializeField] private float charactersPerSecond = 30f;

    private string fullText;
    private bool isTyping;
    private bool skipRequested;

    public void ShowDialog(string text)
    {
        fullText = text;
        StartCoroutine(TypeText());
    }

    IEnumerator TypeText()
    {
        isTyping = true;
        continueIndicator.SetActive(false);
        dialogText.text = "";

        foreach (char c in fullText)
        {
            if (skipRequested)
            {
                dialogText.text = fullText;
                break;
            }

            dialogText.text += c;
            yield return new WaitForSeconds(1f / charactersPerSecond);
        }

        isTyping = false;
        skipRequested = false;
        continueIndicator.SetActive(true);
    }

    public void OnClick()
    {
        if (isTyping)
            skipRequested = true;
        else
            // Proceed to next dialog
            OnDialogComplete();
    }

    void OnDialogComplete()
    {
        // Implementation: Show next line or finish
    }
}
```

---

## Core Concepts

### 1. Canvas Render Mode

| Mode | Use Case | Features |
|------|----------|----------|
| Screen Space - Overlay | General UI | Rendered in front, no camera needed |
| Screen Space - Camera | UI with 3D effects | Camera reference, depth sorting |
| World Space | In-world UI | VR/AR, in-game signboards |

### 2. RectTransform

RectTransform is the component that controls UI element position and size.

```javascript
// Key RectTransform properties
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/Button",
  componentType: "RectTransform",
  fieldPath: "anchoredPosition",
  value: { x: 0, y: 100 }  // Position relative to anchor
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/Button",
  componentType: "RectTransform",
  fieldPath: "sizeDelta",
  value: { x: 200, y: 60 }  // Size
})
```

### 3. Anchors

Anchors are the core of responsive design. They specify relative position to parent element using normalized values from 0 to 1.

#### Anchor Preset Reference

| Preset | anchorMin | anchorMax | Use Case |
|--------|-----------|-----------|----------|
| Center | (0.5, 0.5) | (0.5, 0.5) | Popup, Dialog |
| Top-Left | (0, 1) | (0, 1) | Status display |
| Top-Right | (1, 1) | (1, 1) | Settings button |
| Bottom-Left | (0, 0) | (0, 0) | Chat input |
| Bottom-Right | (1, 0) | (1, 0) | Action buttons |
| Top Stretch | (0, 1) | (1, 1) | Header |
| Bottom Stretch | (0, 0) | (1, 0) | Footer |
| Left Stretch | (0, 0) | (0, 1) | Side menu |
| Full Stretch | (0, 0) | (1, 1) | Background |

```javascript
// Full stretch example
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/Background",
  componentType: "RectTransform",
  fieldPath: "anchorMin",
  value: { x: 0, y: 0 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/Background",
  componentType: "RectTransform",
  fieldPath: "anchorMax",
  value: { x: 1, y: 1 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/Background",
  componentType: "RectTransform",
  fieldPath: "offsetMin",
  value: { x: 0, y: 0 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/Background",
  componentType: "RectTransform",
  fieldPath: "offsetMax",
  value: { x: 0, y: 0 }
})
```

## Mobile Responsive Design

### Canvas Scaler Settings

The key to mobile responsive design is proper `CanvasScaler` configuration.

#### Portrait Priority

```javascript
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas",
  componentType: "CanvasScaler",
  fieldPath: "uiScaleMode",
  value: 1  // ScaleWithScreenSize
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas",
  componentType: "CanvasScaler",
  fieldPath: "referenceResolution",
  value: { x: 1080, y: 1920 }  // 9:16 portrait reference
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas",
  componentType: "CanvasScaler",
  fieldPath: "matchWidthOrHeight",
  value: 0  // 0 = Match width (optimal for portrait)
})
```

#### Landscape Priority

```javascript
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas",
  componentType: "CanvasScaler",
  fieldPath: "referenceResolution",
  value: { x: 1920, y: 1080 }  // 16:9 landscape reference
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas",
  componentType: "CanvasScaler",
  fieldPath: "matchWidthOrHeight",
  value: 1  // 1 = Match height (optimal for landscape)
})
```

#### Both Orientations (Dynamic Match)

For supporting both orientations, switch Match at runtime.

```csharp
// OrientationHandler.cs
using UnityEngine;
using UnityEngine.UI;

public class OrientationHandler : MonoBehaviour
{
    private CanvasScaler canvasScaler;
    private ScreenOrientation lastOrientation;

    void Start()
    {
        canvasScaler = GetComponent<CanvasScaler>();
        UpdateMatch();
    }

    void Update()
    {
        if (Screen.orientation != lastOrientation)
        {
            UpdateMatch();
            lastOrientation = Screen.orientation;
        }
    }

    void UpdateMatch()
    {
        bool isPortrait = Screen.height > Screen.width;
        canvasScaler.matchWidthOrHeight = isPortrait ? 0f : 1f;
    }
}
```

### Safe Area Support (Notch Support)

Safe Area support for devices with notches or punch-hole cameras.

```csharp
// SafeAreaHandler.cs
using UnityEngine;

public class SafeAreaHandler : MonoBehaviour
{
    private RectTransform panelRectTransform;
    private Rect lastSafeArea;

    void Start()
    {
        panelRectTransform = GetComponent<RectTransform>();
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

        // Convert to normalized coordinates
        Vector2 anchorMin = safeArea.position;
        Vector2 anchorMax = safeArea.position + safeArea.size;

        anchorMin.x /= Screen.width;
        anchorMin.y /= Screen.height;
        anchorMax.x /= Screen.width;
        anchorMax.y /= Screen.height;

        panelRectTransform.anchorMin = anchorMin;
        panelRectTransform.anchorMax = anchorMax;
    }
}
```

```javascript
// Create Safe Area panel
mcp__unity-mcp-server__create_gameobject({
  name: "SafeAreaPanel",
  parentPath: "/Canvas"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/SafeAreaPanel",
  componentType: "RectTransform"
})

// Set to full stretch
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/SafeAreaPanel",
  componentType: "RectTransform",
  fieldPath: "anchorMin",
  value: { x: 0, y: 0 }
})

mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/SafeAreaPanel",
  componentType: "RectTransform",
  fieldPath: "anchorMax",
  value: { x: 1, y: 1 }
})

// Add SafeAreaHandler script
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/SafeAreaPanel",
  componentType: "SafeAreaHandler"
})
```

## Layout Groups

Layout Group components for automatic layouts.

### Horizontal Layout Group

```javascript
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/ButtonContainer",
  componentType: "HorizontalLayoutGroup",
  properties: {
    spacing: 10,
    childAlignment: 4,  // MiddleCenter
    childControlWidth: true,
    childControlHeight: true,
    childForceExpandWidth: false,
    childForceExpandHeight: false
  }
})
```

### Vertical Layout Group

```javascript
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/MenuList",
  componentType: "VerticalLayoutGroup",
  properties: {
    spacing: 5,
    childAlignment: 1,  // UpperCenter
    padding: { left: 10, right: 10, top: 10, bottom: 10 }
  }
})
```

### Grid Layout Group

```javascript
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/ItemGrid",
  componentType: "GridLayoutGroup",
  properties: {
    cellSize: { x: 100, y: 100 },
    spacing: { x: 10, y: 10 },
    startCorner: 0,  // UpperLeft
    startAxis: 0,    // Horizontal
    childAlignment: 4,  // MiddleCenter
    constraint: 1,  // FixedColumnCount
    constraintCount: 4
  }
})
```

### Content Size Fitter

Automatically adjusts parent to fit child elements.

```javascript
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/AutoSizePanel",
  componentType: "ContentSizeFitter",
  properties: {
    horizontalFit: 2,  // PreferredSize
    verticalFit: 2     // PreferredSize
  }
})
```

## Tool Selection Guide

| Purpose | Recommended Tool |
|---------|------------------|
| Create Canvas | `create_gameobject` + `add_component` |
| Add UI element | `create_gameobject` + `add_component` |
| Set anchors | `set_component_field` (RectTransform) |
| Configure Canvas Scaler | `set_component_field` (CanvasScaler) |
| Add Layout Group | `add_component` |
| Search UI elements | `find_ui_elements` |
| Test UI click | `click_ui_element` |
| Check UI state | `get_ui_element_state` |
| Create script | `create_class` |

## Common Workflows

### 1. Creating Mobile Portrait UI

```javascript
// Step 1: Create Canvas
mcp__unity-mcp-server__create_gameobject({ name: "MobileCanvas" })
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/MobileCanvas",
  componentType: "Canvas",
  properties: { renderMode: 0 }
})
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/MobileCanvas",
  componentType: "CanvasScaler",
  properties: {
    uiScaleMode: 1,
    referenceResolution: { x: 1080, y: 1920 },
    matchWidthOrHeight: 0
  }
})
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/MobileCanvas",
  componentType: "GraphicRaycaster"
})

// Step 2: Safe Area panel
mcp__unity-mcp-server__create_gameobject({
  name: "SafeArea",
  parentPath: "/MobileCanvas"
})

// Step 3: Header (top stretch)
mcp__unity-mcp-server__create_gameobject({
  name: "Header",
  parentPath: "/MobileCanvas/SafeArea"
})
// Set anchors to top stretch...

// Step 4: Content (center stretch)
mcp__unity-mcp-server__create_gameobject({
  name: "Content",
  parentPath: "/MobileCanvas/SafeArea"
})

// Step 5: Footer (bottom stretch)
mcp__unity-mcp-server__create_gameobject({
  name: "Footer",
  parentPath: "/MobileCanvas/SafeArea"
})
```

### 2. Creating a Scroll View

```javascript
// Create ScrollView
mcp__unity-mcp-server__create_gameobject({
  name: "ScrollView",
  parentPath: "/Canvas"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/ScrollView",
  componentType: "ScrollRect"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/ScrollView",
  componentType: "Image"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/ScrollView",
  componentType: "Mask"
})

// Create Content
mcp__unity-mcp-server__create_gameobject({
  name: "Content",
  parentPath: "/Canvas/ScrollView"
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/ScrollView/Content",
  componentType: "VerticalLayoutGroup",
  properties: {
    childControlHeight: false,
    childForceExpandHeight: false
  }
})

mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/ScrollView/Content",
  componentType: "ContentSizeFitter",
  properties: {
    verticalFit: 2  // PreferredSize
  }
})
```

## Common Mistakes

### 1. Incorrect Anchor Configuration

**NG**: Fixed position UI placement
```javascript
// UI goes off-screen when screen size changes
anchoredPosition: { x: 500, y: 800 }
```

**OK**: Relative placement using anchors
```javascript
// Fixed to parent's bottom-right
anchorMin: { x: 1, y: 0 }
anchorMax: { x: 1, y: 0 }
anchoredPosition: { x: -50, y: 50 }  // Margin
```

### 2. Missing Canvas Scaler Configuration

**NG**: Left as Constant Pixel Size
```javascript
uiScaleMode: 0  // UI size becomes inappropriate when resolution changes
```

**OK**: Scale With Screen Size
```javascript
uiScaleMode: 1
referenceResolution: { x: 1080, y: 1920 }
matchWidthOrHeight: 0  // or 1
```

### 3. No Safe Area Support

**NG**: Placing important UI directly under Canvas
- UI gets hidden by notch
- Overlaps with home indicator area

**OK**: Place within Safe Area panel
- Dynamic adjustment with SafeAreaHandler script
- Place important UI within Safe Area

### 4. Excessive Use of Layout Groups

**NG**: Applying Layout Groups to all UI
- Performance degradation
- Unintended layout changes

**OK**: Use only for dynamically changing lists
- Manual placement for static UI
- Use for scroll view content

### 5. Insufficient Aspect Ratio Consideration

**NG**: Assuming only 16:9
```javascript
referenceResolution: { x: 1920, y: 1080 }
// Breaks on 9:16, 18:9, 21:9, etc.
```

**OK**: Consider multiple aspect ratios
- Test with major aspect ratios
- Anchor settings that don't break on extreme ratios
- Use Aspect Ratio Fitter when needed

## Tool Reference

### find_ui_elements
```javascript
mcp__unity-mcp-server__find_ui_elements({
  elementType: "Button",      // UI component type
  tagFilter: "MainMenu",      // GameObject tag
  namePattern: "Btn_*",       // Name pattern
  includeInactive: false,     // Include inactive
  canvasFilter: "MainCanvas"  // Parent Canvas name
})
```

### click_ui_element
```javascript
mcp__unity-mcp-server__click_ui_element({
  elementPath: "/Canvas/Button",
  clickType: "left",     // left, right, middle
  holdDuration: 0,       // ms
  position: { x: 0.5, y: 0.5 }  // 0-1 normalized
})
```

### get_ui_element_state
```javascript
mcp__unity-mcp-server__get_ui_element_state({
  elementPath: "/Canvas/Button",
  includeChildren: false,
  includeInteractableInfo: true
})
```

### set_ui_element_value
```javascript
mcp__unity-mcp-server__set_ui_element_value({
  elementPath: "/Canvas/InputField",
  value: "Hello World",
  triggerEvents: true
})
```

### set_component_field (RectTransform)
```javascript
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas/Panel",
  componentType: "RectTransform",
  fieldPath: "anchorMin",  // anchorMin, anchorMax, pivot, anchoredPosition, sizeDelta, offsetMin, offsetMax
  value: { x: 0, y: 0 }
})
```

### set_component_field (CanvasScaler)
```javascript
mcp__unity-mcp-server__set_component_field({
  gameObjectPath: "/Canvas",
  componentType: "CanvasScaler",
  fieldPath: "matchWidthOrHeight",  // uiScaleMode, referenceResolution, screenMatchMode, matchWidthOrHeight
  value: 0.5
})
```
