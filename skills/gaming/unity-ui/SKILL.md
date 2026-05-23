---
name: unity-ui
description: Build and optimize Unity UI with UI Toolkit and UGUI. Masters responsive layouts, event systems, and performance optimization. Use for UI implementation, Canvas optimization, or cross-platform UI challenges.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity UI - User Interface Systems

## Overview

Unity UI systems covering both UI Toolkit (modern) and UGUI (Canvas-based legacy).

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType, null-safe coding)

**Core Topics**:
- UI Toolkit (UIElements) for editor and runtime
- UGUI (Canvas) for game UI
- Responsive layouts and anchors
- Event systems
- UI performance optimization
- Data binding patterns

## Quick Start

### UGUI Button

```csharp
using UnityEngine.UI;

public class UIController : MonoBehaviour
{
    [SerializeField] private Button mActionButton;
    [SerializeField] private Text mStatusText;

    void Start()
    {
        mActionButton.onClick.AddListener(OnButtonClick);
    }

    void OnButtonClick()
    {
        mStatusText.text = "Button clicked!";
    }
}
```

### UI Toolkit (Runtime)

```csharp
using UnityEngine.UIElements;

public class UIController : MonoBehaviour
{
    void OnEnable()
    {
        UIDocument uiDocument;
        if (TryGetComponent(out uiDocument))
        {
            VisualElement root = uiDocument.rootVisualElement;
            Button button = root.Q<Button>("action-button");
            button.clicked += OnButtonClick;
        }
    }

    void OnButtonClick()
    {
        Debug.Log("Button clicked!");
    }
}
```

## UI Systems Comparison

| Feature | UI Toolkit | UGUI |
|---------|-----------|------|
| Performance | Better | Good |
| Styling | USS (CSS-like) | Inspector |
| Layout | Flexbox | RectTransform |
| Best For | Complex UI, tools | Game UI |
| Learning Curve | Steeper | Easier |

## Canvas Optimization (UGUI)

```csharp
// Separate static and dynamic UI into different canvases
// Static canvas: rarely changes
// Dynamic canvas: updates frequently

// Disable raycasting on non-interactive elements
[SerializeField] private Image mBackground;

void Start()
{
    mBackground.raycastTarget = false; // Not clickable
}

// Use CanvasGroup for fade effects (TryGetComponent for null-safe access)
CanvasGroup canvasGroup;
if (panel.TryGetComponent(out canvasGroup))
{
    canvasGroup.alpha = 0.5f; // Fade without rebuilding Canvas
}
```

## Responsive Layout

```csharp
// Use anchors for responsive design
// Anchor presets: Stretch, Top-Left, Center, etc.

// Canvas Scaler settings (TryGetComponent pattern)
CanvasScaler scaler;
if (TryGetComponent(out scaler))
{
    scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
    scaler.referenceResolution = new Vector2(1920, 1080);
    scaler.matchWidthOrHeight = 0.5f; // Balance between width/height
}
```

## Best Practices

1. **Separate canvases**: Static vs dynamic content
2. **Disable raycasts**: On non-interactive elements
3. **Use CanvasGroup**: For fade effects without rebuild
4. **Atlas textures**: Pack UI sprites for batching
5. **Hide instead of destroy**: Pool UI elements
6. **Test multiple resolutions**: Ensure responsive design
7. **Profile UI**: Check Canvas rebuild overhead
