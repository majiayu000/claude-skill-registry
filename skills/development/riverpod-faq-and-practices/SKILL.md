---
name: riverpod-faq-and-practices
description: Answers Riverpod FAQ (ref.refresh vs invalidate, ConsumerWidget vs StatelessWidget, Ref vs WidgetRef, reset all providers, ref after unmount) and do/don't best practices (avoid init in widgets, avoid ephemeral state in providers, avoid side effects in provider init, static providers, riverpod_lint). Use when the user asks Riverpod FAQ, best practices, or do/don't guidelines.
---

# Riverpod — FAQ and best practices

## FAQ

### ref.refresh vs ref.invalidate

**ref.refresh** = **ref.invalidate** + **ref.read**: it invalidates the provider and returns the new value. Use **invalidate** when you don't need the new value (e.g. "recompute when the user pulls to refresh"). Use **refresh** when you need the result right away. After invalidate alone, recomputation can happen at the next frame or when the provider is next read; refresh forces immediate recomputation by reading.

### Why no shared interface between Ref and WidgetRef?

Ref (in providers) and WidgetRef (in widgets) are kept separate on purpose so you don't write code that conditionally depends on both; they have subtle differences and mixing would be error-prone. Prefer **Ref**: put logic in a Notifier and call **ref.read(notifierProvider.notifier).yourMethod()** from the UI; the method uses the Notifier's Ref.

### Why ConsumerWidget instead of StatelessWidget?

InheritedWidget (and thus BuildContext) cannot support "on change" listeners like **ref.listen**, cannot know when widgets stop listening (needed for auto-dispose and family), and has lifecycle quirks (e.g. with GlobalKeys). Riverpod needs a Ref that isn't tied to BuildContext for these features. Hence ConsumerWidget (and Consumer) provide a Ref.

### Why doesn't hooks_riverpod export flutter_hooks?

So each package can be versioned independently; a breaking change in one doesn't force the other to break.

### Reset all providers at once?

There is no API to reset all providers; it's considered an anti-pattern. For "logout and clear state", have providers that depend on the current user **ref.watch** a user provider; when the user logs out, that provider changes and dependents recompute or clear. Only user-dependent state resets; the rest stays.

### "Using ref when a widget is about to or has been unmounted is unsafe"

This (or "No ProviderScope found") happens when **ref** is used after an **await** in a widget that may have been disposed. After any **await**, check **if (!context.mounted) return;** before using **ref** (same pattern as with BuildContext).

---

## Do / Don't

### AVOID initializing providers in a widget

Providers should initialize themselves. Don't call something like **ref.read(provider).init()** from **initState**. If initialization depends on user action (e.g. navigation), trigger it from the action (e.g. **onPressed** before **Navigator.push**).

### AVOID using providers for ephemeral state

Use providers for **shared business state**, not for: selected tab/item, form state (which should reset on leave/back), animations, or controller-like state (e.g. TextEditingController). For local widget state use **flutter_hooks** or local state. Storing "selected item" in a global provider can break back navigation (e.g. back from /books/21 should show /books/42, but the provider still holds 21).

### DON'T perform side effects during provider initialization

Providers should represent "read" operations. Don't use a provider's build to perform "write" operations (e.g. submitting a form). That can lead to skipped or duplicated side effects. For loading/error of a side effect use **mutations** (see riverpod-mutations).

### PREFER statically known providers with ref.watch/read/listen

Use **ref.watch(provider)** where **provider** is a top-level final (or otherwise statically known). Avoid passing a provider as a parameter and then watching it so that static analysis and riverpod_lint can work.

### AVOID dynamically creating providers

Define providers as **top-level final** variables. Don't create them inside classes or as instance fields; that can cause memory leaks and unsupported behavior. Static final in a class is allowed but not supported by code generation.

Enable **riverpod_lint** (see riverpod-getting-started) to enforce many of these practices.
