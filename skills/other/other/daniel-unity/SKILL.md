---
name: daniel-unity
description: Unity 6 WebGL/WebGPU development with React integration. Use when building, optimizing, or debugging Unity Web builds.
license: MIT
---

# Unity 6 WebGL & WebGPU Development

## When to Use

Activate this skill when:

- Building Unity WebGL/WebGPU projects
- Integrating Unity with React (react-unity-webgl)
- Optimizing Unity Web builds (memory, size, performance)
- Debugging Unity WebGL issues
- Setting up JavaScript ↔ Unity communication
- Configuring server deployment for Unity builds
- Working with compute shaders or WebGPU features

## Reference Documentation

**Primary Reference:** `docs/unity-6-webgl-webgpu-reference.md`

Read this file for comprehensive coverage of:

- WebGL vs WebGPU comparison
- Build settings & optimization
- Memory management (GC constraints, NativeArray patterns)
- JavaScript interop (JSLib, SendMessage, DllImport)
- React Unity WebGL integration
- Audio, input, networking limitations
- Browser compatibility
- Deployment configuration
- Common issues & solutions

## Quick Reference

### WebGPU Enable Steps

1. Edit → Project Settings → Player → Web
2. Other Settings → disable Auto Graphics API
3. Add WebGPU, drag to top
4. Keep WebGL2 as fallback

### React → Unity Communication

```tsx
const { sendMessage } = useUnityContext({
  /* config */
});
sendMessage('GameObjectName', 'MethodName', parameter);
```

### Unity → React Communication

**JSLib:** `Assets/Plugins/WebGL/Bridge.jslib`

```javascript
mergeInto(LibraryManager.library, {
  SendToReact: function (dataPtr) {
    var data = UTF8ToString(dataPtr);
    window.dispatchReactUnityEvent('EventName', data);
  },
});
```

**C#:**

```csharp
[DllImport("__Internal")]
private static extern void SendToReact(string data);

#if UNITY_WEBGL && !UNITY_EDITOR
SendToReact(jsonData);
#endif
```

### Memory Optimization

```csharp
// Use NativeArray to bypass GC
using (var data = new NativeArray<byte>(size, Allocator.Temp)) {
    // Operations
} // Disposed immediately

// Never do this - quadratic memory growth
string result = "";
for (int i = 0; i < 10000; i++) {
    result += i.ToString(); // BAD - GC can't run mid-loop
}
```

### Build Settings Checklist

- [ ] Brotli compression (HTTPS)
- [ ] Code stripping: High
- [ ] Strip Engine Code: enabled
- [ ] Exception support: None (release)
- [ ] Name Files As Hashes: enabled
- [ ] Data Caching: enabled

### Server Headers (Brotli)

```
Content-Encoding: br
Content-Type: application/wasm  (for .wasm.br)
```

## Key Limitations to Remember

| Feature         | WebGL2     | WebGPU       |
| --------------- | ---------- | ------------ |
| Compute Shaders | No         | Yes          |
| VFX Graph       | No         | Yes          |
| Status          | Production | Experimental |

**Always:**

- Require user interaction before audio
- Use coroutines (never blocking calls)
- Configure CORS headers for cross-origin requests
- Test on multiple browsers

**Never:**

- Use synchronous GPU readback (WebGPU)
- Use RWBuffer in compute shaders (use RWStructuredBuffer)
- Block on WWW/WebRequest downloads
- Use System.Net classes

## File Locations

| Purpose          | Location                                 |
| ---------------- | ---------------------------------------- |
| JSLib plugins    | `Assets/Plugins/WebGL/*.jslib`           |
| Pre-execution JS | `Assets/Plugins/WebGL/*.jspre`           |
| Web templates    | `Assets/WebGLTemplates/`                 |
| Build output     | `Build/` folder                          |
| Reference doc    | `docs/unity-6-webgl-webgpu-reference.md` |

## Common Issues Quick Fix

| Issue                          | Solution                             |
| ------------------------------ | ------------------------------------ |
| Out of memory                  | Reduce heap size, use AssetBundles   |
| CORS error                     | Add Access-Control headers on server |
| Audio not playing              | Require user click/tap first         |
| Code stripping broke something | Add to `link.xml`                    |
| Incorrect header check         | Configure server compression headers |

## Related Skills

- `theone-unity-standards` - C# coding patterns
- `frontend-development` - React/TypeScript patterns
- `backend-development` - Server configuration
