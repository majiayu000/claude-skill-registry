---
name: riverpod-cancel
description: Cancel or debounce Riverpod async requests with ref.onDispose; cancel when user leaves the page, debounce rapid refreshes. Use when the user asks about cancelling requests, debouncing, or cleaning up when a provider is disposed.
---

# Riverpod — Cancelling and debouncing requests

## Instructions

Use **ref.onDispose** together with **auto-dispose** (or ref.watch) to cancel in-flight requests when the user leaves the page, or to debounce rapid refreshes.

### Cancelling when leaving the page

Ensure the provider is **auto-dispose**. When the user navigates away, the provider loses its listeners and is disposed; **ref.onDispose** runs. In that callback, cancel the request (e.g. close the HTTP client used for the request).

Example pattern: create an `http.Client()` in the provider, pass it to your fetch logic, and call **ref.onDispose(client.close)**. When the provider is disposed, the client closes and the request is cancelled. Exact API depends on your HTTP package.

### Debouncing refreshes

If the user triggers refresh multiple times quickly, you can delay the actual request until they stop (e.g. 500ms). Pattern:

1. In the provider, set a flag (e.g. `didDispose = false`) and **ref.onDispose(() => didDispose = true)**.
2. **await Future.delayed(duration)**.
3. If **didDispose** is true, the user triggered another refresh during the delay; **throw** to abort (Riverpod catches and ignores). Otherwise create the client, register **onDispose(client.close)**, and run the request.

So: delay first, then create client and run request; disposal during the delay aborts, disposal after creates client cancels the request.

### Reusable extension

You can implement an extension on **Ref** that returns a debounced/cancellable client:

- Use **onDispose** to set a "cancelled" flag.
- Wait for the debounce duration; if disposed, throw.
- Create the client, **onDispose(client.close)**, return the client.

Use this extension in your activity/provider so all call sites get debounce + cancel behavior. See the official Riverpod "cancel" how-to for a full extension example.
