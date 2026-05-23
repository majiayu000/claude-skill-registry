---
name: unity-mobile
description: Optimize Unity games for mobile platforms with IL2CPP, platform-specific code, and memory management. Masters iOS/Android deployment, app size reduction, and battery optimization. Use for mobile builds, platform issues, or device-specific optimization.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity Mobile Optimization

## Overview

Mobile platform optimization for Unity focusing on iOS and Android performance, battery life, and deployment.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType, null-safe coding)

**Core Topics**:
- IL2CPP compilation and optimization
- Memory management and profiling
- Touch input and mobile UI
- Battery life optimization
- App size reduction
- Platform-specific code

## Quick Start

```csharp
// Platform-specific code
#if UNITY_IOS
    // iOS-specific code
    Application.targetFrameRate = 60;
#elif UNITY_ANDROID
    // Android-specific code
    Application.targetFrameRate = 30;
#endif

// Touch input
if (Input.touchCount > 0)
{
    Touch touch = Input.GetTouch(0);
    if (touch.phase == TouchPhase.Began)
    {
        HandleTouch(touch.position);
    }
}
```

## Platform Constraints

- **iOS**: Metal rendering, App Store guidelines, 150MB initial download
- **Android**: Vulkan/OpenGL ES, API level fragmentation, 150MB initial
- **Memory**: 1-2GB low-end, 4-6GB high-end
- **Thermal**: Throttling after 5-10 minutes

## Optimization Checklist

- ✅ Texture compression: ASTC (mobile), ETC2 (Android), PVRTC (iOS)
- ✅ Audio compression: AAC (iOS), Vorbis (Android)
- ✅ Reduce draw calls: <100 mobile, batching
- ✅ IL2CPP optimization: Strip engine code, managed stripping
- ✅ Battery: Lower target framerate, reduce update frequency

## Best Practices

1. **Profile on device**: Not just Unity Editor
2. **Minimize allocations**: Reduce GC pressure
3. **Touch-friendly UI**: 44pt minimum touch target
4. **Handle pause**: OnApplicationPause lifecycle
5. **Test on low-end**: Target lowest common denominator
