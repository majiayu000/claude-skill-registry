---
name: android-dfm
description: Create Android dynamic feature modules with Gradle, Koin DI, Navigation registration. Use for new features, modularization, feature flags.
---

# Android Dynamic Feature Module Creator

Create new dynamic feature modules for Android projects using Play Feature Delivery.

## When to Use

- Adding new feature modules to modularized Android apps
- Creating install-time, on-demand, or conditional delivery features
- Setting up feature-specific Koin DI modules
- Implementing feature navigation registration

## Quick Reference

Module structure:
```
feature/{name}/
├── build.gradle.kts           # Plugin: android.dynamic.feature
├── src/main/
│   ├── AndroidManifest.xml    # dist:module delivery config
│   ├── kotlin/.../{name}/
│   │   ├── di/{Name}FeatureModule.kt
│   │   ├── navigation/{Name}NavigationProvider.kt
│   │   └── screen/{Name}Route.kt
│   └── res/values/strings.xml # title_{name} required
```

## Creation Steps

1. **Read structure template**: `references/dfm-structure.md`
2. **Create module files**: Build script, manifest, DI, navigation
3. **Register in app**: Update `app/build.gradle.kts` dynamicFeatures
4. **Register in settings**: Add `include(":feature:{name}")`
5. **Register DI**: Add to `FeatureRegistry.KNOWN_FEATURE_INITIALIZERS`
6. **Register Nav**: Add to `FeatureNavigationRegistry.KNOWN_NAVIGATION_PROVIDERS`
7. **Add route**: Create `{Name}RouteData` in `core/navigation/Routes.kt`

## Key Patterns

- **DI**: `{Name}FeatureInitializer : FeatureModuleInitializer` interface
- **Nav**: `{Name}NavigationProvider : FeatureNavigationProvider` interface
- **Build**: `implementation(project(":app"))` required in feature modules
- **Manifest**: Use `<dist:install-time />` for install-time delivery

## References

- [DFM Structure](references/dfm-structure.md) - Complete file templates
- [Delivery Options](references/delivery-options.md) - Install-time, on-demand, conditional
