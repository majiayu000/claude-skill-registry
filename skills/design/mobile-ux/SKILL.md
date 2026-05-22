---
name: mobile-ux
description: Master mobile UX - iOS HIG, Material Design, gestures, responsive design, platform optimization
sasmp_version: "1.3.0"
bonded_agent: 06-mobile-ux
bond_type: PRIMARY_BOND
---

# Mobile UX Skill

> **Atomic Skill**: Design native-feeling mobile experiences for iOS and Android platforms

## Purpose

This skill provides platform-specific guidance for creating optimal mobile user experiences.

## Skill Invocation

```
Skill("custom-plugin-ux-design:mobile-ux")
```

## Parameter Schema

### Input Parameters
```typescript
interface MobileUXParams {
  // Required
  task: "ios" | "android" | "cross-platform" | "responsive" | "gesture";
  scope: string;

  // Optional
  platform_priority?: "ios" | "android" | "equal";
  app_type?: "native" | "hybrid" | "pwa";
  device_targets?: ("phone" | "tablet" | "foldable")[];
  os_versions?: {
    ios?: string;
    android?: string;
  };
}
```

### Validation Rules
```yaml
task:
  type: enum
  required: true
  values: [ios, android, cross-platform, responsive, gesture]

scope:
  type: string
  required: true
  min_length: 5

platform_priority:
  type: enum
  default: "equal"
```

## Execution Flow

```
MOBILE UX EXECUTION
────────────────────────────────────────────

Step 1: ANALYZE REQUIREMENTS
├── Identify target platforms
├── Define device matrix
└── Set priority platform

Step 2: RESEARCH GUIDELINES
├── Review platform HIG
├── Study native patterns
└── Identify constraints

Step 3: DESIGN PATTERNS
├── Navigation structure
├── Touch interactions
├── Platform-specific components
└── Gesture mapping

Step 4: ADAPT FOR PLATFORMS
├── iOS adaptations
├── Android adaptations
├── Cross-platform unification
└── Responsive breakpoints

Step 5: VALIDATE
├── Test on device matrix
├── Verify platform compliance
└── Document exceptions

────────────────────────────────────────────
```

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff_type: exponential
  initial_delay_ms: 1000
  max_delay_ms: 10000
  retryable_errors:
    - DEVICE_SYNC_FAILED
    - PREVIEW_TIMEOUT
```

## Logging Hooks

```typescript
interface MobileUXLog {
  timestamp: string;
  event: "pattern_selected" | "adaptation_created" | "device_tested";
  platform: string;
  device: string;
  compliance_score: number;
}
```

## Learning Modules

### Module 1: iOS Human Interface Guidelines
```
iOS DESIGN PRINCIPLES
├── Clarity (legible, clear icons)
├── Deference (content first)
├── Depth (layers, motion)

iOS NAVIGATION
├── Tab bar (5 max)
├── Navigation bar
├── Tool bar
├── Side bar (iPad)
└── Search

iOS COMPONENTS
├── SF Symbols
├── System controls
├── Sheets
├── Popovers
└── Action sheets
```

### Module 2: Material Design 3
```
MATERIAL PRINCIPLES
├── Material as metaphor
├── Bold, graphic, intentional
├── Motion provides meaning

MATERIAL NAVIGATION
├── Bottom navigation
├── Navigation drawer
├── Navigation rail
├── Tabs
└── Search

MATERIAL COMPONENTS
├── FAB (Floating Action Button)
├── Cards
├── Chips
├── Dialogs
└── Bottom sheets
```

### Module 3: Touch & Gestures
```
TOUCH TARGETS
├── iOS: 44x44 pt minimum
├── Android: 48x48 dp minimum
├── Spacing: 8dp between targets

STANDARD GESTURES
├── Tap (select, activate)
├── Long press (context menu)
├── Swipe (navigate, actions)
├── Pinch (zoom)
├── Rotate (rotate content)
├── Pan (scroll, move)
└── Edge swipe (back navigation)

GESTURE CONFLICTS
├── System gesture areas
├── Platform-specific gestures
└── Custom gesture rules
```

### Module 4: Responsive Mobile Design
```
BREAKPOINTS
├── Small phone: 320-375pt
├── Regular phone: 375-414pt
├── Large phone: 414-428pt
├── Small tablet: 768-834pt
├── Large tablet: 834-1024pt
└── Foldable: Variable

ADAPTIVE LAYOUTS
├── Compact (phone portrait)
├── Regular (phone landscape, tablet)
├── Expanded (tablet landscape)

SAFE AREAS
├── Status bar
├── Home indicator
├── Notch/Dynamic Island
├── Gesture areas
└── Camera cutouts
```

### Module 5: Platform Optimization
```
PERFORMANCE
├── 60fps animations
├── Lazy loading
├── Image optimization
├── Memory management
└── Network efficiency

NATIVE FEEL
├── Platform animations
├── Haptic feedback
├── System sounds
├── Platform typography
└── Native controls
```

## Platform Comparison

| Aspect | iOS (HIG) | Android (Material) |
|--------|-----------|-------------------|
| Touch target | 44x44 pt | 48x48 dp |
| Navigation | Tab bar (bottom) | Bottom nav / Drawer |
| Back navigation | Swipe edge, button | System back |
| Typography | SF Pro | Roboto |
| Icons | SF Symbols | Material Icons |
| Elevation | Subtle | Card elevation |
| Haptics | Taptic Engine | Vibration patterns |

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `MUX-001` | Touch target too small | Increase size |
| `MUX-002` | Platform violation | Use native pattern |
| `MUX-003` | Gesture conflict | Redesign gesture |
| `MUX-004` | Safe area ignored | Add insets |
| `MUX-005` | Layout overflow | Use flexible layout |

## Troubleshooting

### Problem: App doesn't feel native
```
Diagnosis:
├── Check: Navigation patterns
├── Check: Component usage
├── Check: Animation timing
└── Solution: Align with platform

Steps:
1. Audit against HIG/Material
2. Replace custom with native
3. Match platform animations
4. Test with platform users
```

### Problem: Touch interactions unreliable
```
Diagnosis:
├── Check: Touch target sizes
├── Check: Gesture areas
├── Check: Feedback timing
└── Solution: Optimize touch

Steps:
1. Measure all targets
2. Increase to minimum
3. Add haptic feedback
4. Test with real devices
```

## Unit Test Templates

```typescript
describe("MobileUXSkill", () => {
  describe("platform compliance", () => {
    it("should meet iOS touch target requirements", async () => {
      const result = await invoke({
        task: "ios",
        scope: "button component"
      });
      expect(result.touch_target.width).toBeGreaterThanOrEqual(44);
      expect(result.touch_target.height).toBeGreaterThanOrEqual(44);
    });

    it("should meet Android touch target requirements", async () => {
      const result = await invoke({
        task: "android",
        scope: "button component"
      });
      expect(result.touch_target.width).toBeGreaterThanOrEqual(48);
      expect(result.touch_target.height).toBeGreaterThanOrEqual(48);
    });
  });

  describe("responsive adaptation", () => {
    it("should provide breakpoint specifications", async () => {
      const result = await invoke({
        task: "responsive",
        scope: "navigation layout"
      });
      expect(result.breakpoints.compact).toBeDefined();
      expect(result.breakpoints.regular).toBeDefined();
    });
  });
});
```

## Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Platform compliance | > 95% | HIG/Material audit |
| Touch target compliance | 100% | Size verification |
| Device coverage | > 90% | Matrix testing |
| Performance score | > 90 | Lighthouse/tools |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-30 | Production-grade upgrade |
