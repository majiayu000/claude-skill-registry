---
name: unity-textmeshpro
description: TextMeshPro (TMPro) expert for Unity text rendering with advanced typography, performance optimization, and professional text effects. Masters font asset creation, dynamic fonts, rich text formatting, material presets, and text mesh optimization. Use PROACTIVELY for text rendering, font management, localization text, UI text performance, or text effects implementation.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity TextMeshPro - Professional Text Rendering

## Overview

TextMeshPro (TMPro) is Unity's advanced text rendering solution using Signed Distance Field (SDF) technology for resolution-independent, high-quality text with minimal performance overhead.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType), `unity-ui` (UI systems, Canvas, UGUI)

**Core Topics**:
- SDF font asset creation and configuration
- Dynamic vs static font assets
- Rich text formatting and styling
- Material presets and text effects
- Performance optimization patterns
- Localization and dynamic text handling

## Quick Start

### Basic Text Setup

```csharp
using TMPro;
using UnityEngine;

public class TextController : MonoBehaviour
{
    [SerializeField] private TMP_Text mDisplayText;

    void Start()
    {
        mDisplayText.text = "Hello, World!";
        mDisplayText.fontSize = 36;
        mDisplayText.color = Color.white;
    }
}
```

### TMP_Text vs TextMeshProUGUI vs TextMeshPro

```csharp
// TMP_Text - Base class, use for serialization (works with both)
[SerializeField] private TMP_Text mText;

// TextMeshProUGUI - Canvas UI text (most common)
[SerializeField] private TextMeshProUGUI mUiText;

// TextMeshPro - 3D world space text (MeshRenderer)
[SerializeField] private TextMeshPro mWorldText;
```

### Rich Text Formatting

```csharp
// Basic formatting
text.text = "<b>Bold</b> and <i>Italic</i>";
text.text = "<size=48>Large</size> and <size=24>Small</size>";
text.text = "<color=#FF0000>Red</color> text";

// Advanced formatting
text.text = "<mark=#FFFF00AA>Highlighted</mark>";
text.text = "H<sub>2</sub>O and E=mc<sup>2</sup>";
text.text = "<s>Strikethrough</s> and <u>Underline</u>";

// Sprite embedding
text.text = "Score: 100 <sprite=0>";
```

## Component Selection Guide

| Scenario | Component | Reason |
|----------|-----------|--------|
| UI Canvas text | TextMeshProUGUI | Canvas integration, auto-batching |
| 3D world labels | TextMeshPro | MeshRenderer, world-space |
| Serialized reference | TMP_Text | Works with both types |
| Input field | TMP_InputField | Built-in input handling |
| Dropdown | TMP_Dropdown | Built-in dropdown UI |

## Font Asset Best Practices

### Font Asset Types

```
Static Font Asset:
- Pre-generated character set
- Best performance (no runtime generation)
- Use for: Known character sets, optimized builds

Dynamic Font Asset:
- Runtime character generation
- Flexible but slower initial render
- Use for: Localization, user input, unknown characters
```

### Creating Optimal Font Assets

1. **Font Asset Creator** (Window > TextMeshPro > Font Asset Creator)
   - Set appropriate Atlas Resolution (1024x1024 for basic, 2048x2048 for CJK)
   - Use "Custom Character List" for known character sets
   - Enable Multi Atlas Textures for large character sets

2. **Sampling Point Size**: Use highest size that fits atlas (better quality)

3. **Padding**: 5-9 for normal use, higher for effects (outline, glow)

## Performance Guidelines

### Text Update Optimization

```csharp
// BAD: Frequent text changes trigger mesh rebuild
void Update()
{
    scoreText.text = $"Score: {score}"; // Rebuilds every frame
}

// GOOD: Update only when value changes
private int mLastScore = -1;

void Update()
{
    if (score != mLastScore)
    {
        mLastScore = score;
        scoreText.text = $"Score: {score}";
    }
}

// BETTER: Use SetText for formatted updates (less allocation)
void UpdateScore(int score)
{
    scoreText.SetText("Score: {0}", score);
}
```

### Memory-Efficient Patterns

```csharp
// Use StringBuilder for complex text construction
private readonly StringBuilder mSb = new StringBuilder(256);

void BuildComplexText()
{
    mSb.Clear();
    mSb.Append("Player: ");
    mSb.Append(playerName);
    mSb.Append(" | Score: ");
    mSb.Append(score);
    displayText.SetText(mSb);
}

// Prefer SetText with parameters over string interpolation
text.SetText("{0}/{1}", currentHP, maxHP);  // Less GC
// Instead of
text.text = $"{currentHP}/{maxHP}";         // More GC
```

## Material Presets

```csharp
// Apply material preset at runtime
[SerializeField] private Material mHighlightMaterial;
[SerializeField] private Material mNormalMaterial;

void Highlight(bool active)
{
    mText.fontMaterial = active ? mHighlightMaterial : mNormalMaterial;
}

// Modify material properties
mText.fontMaterial.SetFloat(ShaderUtilities.ID_OutlineWidth, 0.2f);
mText.fontMaterial.SetColor(ShaderUtilities.ID_OutlineColor, Color.black);
```

## Reference Documentation

### [Fundamentals](references/fundamentals.md)
Core TextMeshPro concepts:
- SDF technology explanation
- Font asset creation workflow
- Character sets and fallback fonts
- Sprite assets integration
- Style sheets usage

### [Performance Optimization](references/performance-optimization.md)
Optimization techniques:
- Mesh geometry optimization
- Dynamic batching strategies
- Font atlas memory management
- Text update minimization patterns
- Profiling text rendering

### [Advanced Patterns](references/advanced-patterns.md)
Advanced usage patterns:
- Custom shaders and effects
- Text animation techniques
- Localization integration
- Typewriter effects
- Link and event handling

## Key Principles

1. **Use TMP_Text for References**: Base class works with both UI and 3D text
2. **Prefer SetText() over .text**: Reduces GC allocations for dynamic values
3. **Update Only When Changed**: Avoid unnecessary mesh rebuilds
4. **Choose Appropriate Font Assets**: Static for performance, Dynamic for flexibility
5. **Batch Similar Text**: Group text with same material for draw call reduction

## Common Anti-Patterns

```csharp
// AVOID: Creating new materials per text instance
text.fontMaterial = new Material(text.fontMaterial); // Memory leak risk

// AVOID: Updating text in Update() without change check
void Update() { text.text = score.ToString(); } // Constant rebuild

// AVOID: Excessive rich text nesting
text.text = "<b><i><color=#FF0000><size=48>...</size></color></i></b>";

// AVOID: Dynamic fonts for static content
// Use pre-generated static font assets instead
```

## Platform Considerations

- **Mobile**: Use static font assets, minimize atlas size, avoid complex effects
- **WebGL**: Pre-load font assets, avoid dynamic font generation
- **VR/AR**: Consider text readability, use larger fonts, avoid thin outlines

## Integration with Other Skills

- **unity-ui**: TextMeshPro integrates with Canvas and UI Toolkit
- **unity-performance**: Text rendering impacts draw calls and memory
- **unity-mobile**: Font asset optimization critical for mobile
- **unity-async**: Async font loading with Addressables
