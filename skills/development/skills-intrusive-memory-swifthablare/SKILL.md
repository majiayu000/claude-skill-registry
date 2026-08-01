---
name: skills-intrusive-memory-swifthablare
description: Use this skill when you need to add a new VoiceProvider implementation
  and expose it through the shared
---

# Skill: Register a Custom Voice Provider

Use this skill when you need to add a new `VoiceProvider` implementation and expose it through the shared
`VoiceProviderRegistry`.

## Steps

1. **Create the provider type**
   - Add a new file under `Sources/SwiftHablare/Providers/` (or a nested folder) that defines a type conforming to `VoiceProvider`.
   - Implement `isConfigured()` to verify the provider’s own persisted settings (API keys, model IDs, etc.).
   - Keep persistence local to the provider—use `UserDefaults`, the keychain, or custom storage as needed.
   - Supply a SwiftUI configuration panel by implementing `makeConfigurationView(onConfigured:)` when SwiftUI is available.

2. **Declare a descriptor**
   - Extend the provider with a static `descriptor` property returning `VoiceProviderDescriptor`.
   - Populate the descriptor with a stable identifier, display name, enablement defaults, and a factory closure that returns a
     new instance of the provider.
   - If the provider needs custom configuration UI, pass a configuration panel builder (otherwise the registry uses
     `makeConfigurationView(onConfigured:)`).

3. **Register the provider**
   - During startup (for example in `SwiftHablare.configureVoiceProviders()` or app initialization), call
     `await VoiceProviderRegistry.shared.register(NewProvider.descriptor)` **or** subclass
     `VoiceProviderAutoRegistrar` to register automatically when the module loads on Objective-C platforms.
   - The registry persists enablement state automatically and will call the provider’s `isConfigured()` before returning it from
     `configuredProvider(for:)`.

4. **Surface configuration UI**
   - Use `VoiceProviderRegistry.shared.configurationPanel(for:onConfigured:)` when the user enables the provider or wants to
     edit its settings.
   - Ensure the configuration view saves credentials/settings and calls the completion handler with `true` upon success so the
     registry can mark the provider as enabled.

5. **Verify integration**
   - Fetch the updated catalog with `VoiceProviderRegistry.shared.availableProviders()` and confirm the new provider appears
     with the correct enablement and configuration status.
   - Run any relevant unit tests or add new coverage specific to the provider.

## References
- `Sources/SwiftHablare/VoiceProvider.swift`
- `Sources/SwiftHablare/VoiceProviderRegistry.swift`
- `Sources/SwiftHablare/Providers/AppleVoiceProvider.swift`
- `Sources/SwiftHablare/Providers/ElevenLabsVoiceProvider.swift`
