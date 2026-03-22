---
name: "wpf-webview-threading"
description: "Thread-safe WebView2 bridge messaging in WPF with async handlers"
domain: "desktop-platform"
confidence: "high"
source: "file-dialog-first-try-bug-fix"
---

## Context

Use this pattern when building a WPF desktop application that hosts a WebView2 control and needs to exchange messages with web content. Especially important when bridge handlers perform async I/O that uses `.ConfigureAwait(false)`.

## Problem

WebView2 bridge handlers that call `CoreWebView2.PostWebMessageAsJson()` after async operations using `.ConfigureAwait(false)` will fail intermittently because execution resumes on a thread pool thread, but WPF controls require UI thread access.

## Pattern

### 1. Service Initialization Timing

Initialize services that capture `Application.Current.Dispatcher` AFTER `InitializeComponent()`:

```csharp
public MainWindow()
{
    InitializeComponent();  // FIRST
    
    // THEN initialize services that need dispatcher
    _fileDialogService = new NativeFileDialogService();
    // ... other services
}
```

**Not:**
```csharp
// BAD: Field initializer runs before InitializeComponent()
private readonly IFileDialogService _fileDialogService = new NativeFileDialogService();
```

### 2. Thread-Safe WebView2 Message Posting

Always marshal WebView2 message posts to the UI thread:

```csharp
private void Post(BridgeMessageEnvelope message)
{
    if (!_webView.Dispatcher.CheckAccess())
    {
        _webView.Dispatcher.Invoke(() => Post(message));
        return;
    }

    var json = JsonSerializer.Serialize(message, BridgeJson.SerializerOptions);
    _webView.CoreWebView2.PostWebMessageAsJson(json);
}
```

### 3. Async Handler Context

For the event handler, prefer `.ConfigureAwait(true)` to try staying on original context, but rely on the `Post` dispatcher check as the robust guarantee:

```csharp
private async void HandleWebMessageReceived(object? sender, CoreWebView2WebMessageReceivedEventArgs e)
{
    // ... deserialize request ...
    
    var response = await _dispatcher.DispatchAsync(request).ConfigureAwait(true);
    
    if (response is not null)
    {
        Post(response);  // Safe: Post checks thread
    }
}
```

## Why It Helps

- File dialogs and other UI operations get a valid dispatcher reference
- WebView2 message posts never fail due to cross-thread access violations
- Async handlers using `.ConfigureAwait(false)` (recommended for I/O) don't break message flow
- First-try operations work reliably instead of requiring retry

## Symptoms Without This Pattern

- File operations work on second try but not first
- Intermittent "cross-thread operation" exceptions
- Messages posted from background threads don't reach web content
- Dialogs fail to show or show on wrong thread

## Testing Strategy

- Unit test file dialog service with explicit dispatcher
- Manual test: verify first-try file open/import succeeds
- Look for thread ID mismatches in logs if issues persist
