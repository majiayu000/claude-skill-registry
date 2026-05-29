---
name: "webview2-user-data-relocation"
description: "Keep WebView2 profile/cache data out of installed payload directories"
domain: "desktop-host"
confidence: "high"
source: "installer-revision"
---

## Context

Calling `EnsureCoreWebView2Async()` without an explicit environment lets WebView2 create `App.exe.WebView2` beside the executable. That is fine for loose local runs, but it breaks MSI uninstall cleanliness because the install root is no longer immutable after first launch.

## Pattern

Define a stable app-owned folder under `%LOCALAPPDATA%`, then bootstrap WebView2 with an explicit environment:

```csharp
Directory.CreateDirectory(userDataFolder);
var environment = await CoreWebView2Environment.CreateAsync(userDataFolder: userDataFolder);
await webView.EnsureCoreWebView2Async(environment);
```

## PanelNester Convention

- Put desktop mutable state behind `DesktopStoragePaths`.
- Current WebView2 profile path: `%LOCALAPPDATA%\PanelNester\WebView2\UserData`
- Keep MSI payload under `%LOCALAPPDATA%\Programs\PanelNester` strictly for installed binaries and bundled web assets.

## When To Apply

- Per-user MSI installs
- Any installer that must uninstall back to a clean install root
- Any desktop host where browser cache/profile data must stay separate from shipped files

## Validation Checklist

1. Install the MSI as a standard user.
2. Launch once and wait long enough for WebView2 initialization.
3. Confirm no `*.exe.WebView2` folder appears beside the installed EXE.
4. Confirm the explicit `%LOCALAPPDATA%\AppName\...` profile folder exists.
5. Uninstall and verify the install root is removed cleanly.
