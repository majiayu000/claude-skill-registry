---
name: flutter-accessibility
description: "Flutter accessibility patterns for WCAG 2.2 Level AA compliance: Semantics widget, screen readers, focus management, dynamic font sizing, gesture alternatives, and touch targets (48x48dp minimum). Use when implementing a11y features, auditing accessibility, or ensuring WCAG 2.2 compliance (government deadline April 24, 2026)."
version: "2.0.0"
last_updated: "2026-01-12"
---

# Flutter Accessibility

## ⚠️ WCAG 2.2 Level AA Compliance (CRITICAL)

**Government Compliance Deadline**: April 24, 2026 for entities with 50k+ population

Flutter has first-class support for WCAG 2.2 accessibility standards. This guide covers all requirements for Level AA compliance.

### WCAG 2.2 New Success Criteria (Added over 2.1)

WCAG 2.2 adds 9 new success criteria that Flutter apps must meet:

| Criterion | Level | Requirement | Flutter Implementation |
|-----------|-------|-------------|------------------------|
| **2.4.11 Focus Appearance** | AA | Visible focus indicator (min 2px, contrast 3:1) | Use `FocusNode` with custom indicator |
| **2.4.12 Focus Not Obscured (Minimum)** | AA | Focused element not fully hidden | Ensure dialogs/overlays don't cover focus |
| **2.4.13 Focus Not Obscured (Enhanced)** | AAA | Focused element fully visible | Not required for AA |
| **2.5.7 Dragging Movements** | AA | Alternative to drag gestures | Provide tap alternative for all drags |
| **2.5.8 Target Size (Minimum)** | AA | 24x24px minimum (except inline text) | Flutter: 48x48dp recommended |
| **3.2.6 Consistent Help** | A | Help in same location | Maintain consistent help button position |
| **3.3.7 Redundant Entry** | A | Don't ask for same info twice | Auto-fill or remember previous inputs |
| **3.3.8 Accessible Authentication** | AA | No cognitive function tests (CAPTCHA) | Use biometric, OTP, or link-based auth |
| **3.3.9 Accessible Authentication (Enhanced)** | AAA | Alternative for object recognition | Not required for AA |

## Key Requirements

| Requirement | WCAG 2.2 Standard | Flutter Target |
|-------------|-------------------|----------------|
| Touch targets | 2.5.8 (AA): 24x24px min | **48x48dp minimum** (exceeds standard) |
| Color contrast | 1.4.3 (AA): 4.5:1 text, 3:1 large | Use Material 3 ColorScheme |
| Focus order | 2.4.3 (A): Logical sequence | Use `FocusTraversalGroup` |
| Focus indicator | 2.4.11 (AA): 2px, 3:1 contrast | Custom `FocusNode` decoration |
| Screen reader | 4.1.2 (A): Name, role, value | Semantics widget |
| Gesture alternatives | 2.5.7 (AA): No drag-only | Provide tap alternatives |
| Font sizing | 1.4.4 (AA): Resize to 200% | Respect `MediaQuery.textScaleFactor` |

## Semantics Widget

```dart
Semantics(
  label: 'Event details',
  hint: 'Double tap to view',
  button: true,
  child: CustomWidget(),
)
```

## Images

```dart
// Informative
Image.asset('hero.png', semanticLabel: 'Dancer performing ballet')

// Decorative
Image.asset('pattern.png', excludeFromSemantics: true)
```

## IconButtons (REQUIRED)

```dart
IconButton(
  icon: const Icon(Icons.delete),
  tooltip: 'Delete event',  // REQUIRED
  onPressed: _delete,
)
```

## Touch Targets

```dart
// Minimum 48x48
SizedBox(
  width: 48,
  height: 48,
  child: IconButton(icon: Icon(Icons.close), onPressed: _close),
)

// Or use padding
InkWell(
  onTap: _tap,
  child: Padding(
    padding: const EdgeInsets.all(12),  // Expand hit area
    child: Icon(Icons.star, size: 24),
  ),
)
```

## Color Contrast

```dart
// Check in theme
final primary = Theme.of(context).colorScheme.primary;
final onPrimary = Theme.of(context).colorScheme.onPrimary;
// onPrimary is designed to have 4.5:1 contrast with primary
```

## MergeSemantics

```dart
// Combine into single announcement
MergeSemantics(
  child: ListTile(
    leading: const Icon(Icons.event),
    title: const Text('Ballet Performance'),
    subtitle: const Text('Tomorrow at 7pm'),
  ),
)
// Announces: "Ballet Performance, Tomorrow at 7pm"
```

## ExcludeSemantics

```dart
ExcludeSemantics(
  child: DecorativeWidget(),  // Skip in screen reader
)
```

## Live Regions

```dart
Semantics(
  liveRegion: true,
  child: Text(statusMessage),  // Announced when changed
)
```

## Testing

```bash
# iOS: Settings > Accessibility > VoiceOver
# Android: Settings > Accessibility > TalkBack

# In tests
testWidgets('has semantic label', (tester) async {
  await tester.pumpWidget(MyWidget());
  expect(find.bySemanticsLabel('Delete event'), findsOneWidget);
});
```

## Focus Management (WCAG 2.4.11)

**Requirement**: Visible focus indicator with minimum 2px thickness and 3:1 contrast ratio.

```dart
class AccessibleButton extends StatefulWidget {
  final VoidCallback onPressed;
  final Widget child;

  const AccessibleButton({required this.onPressed, required this.child});

  @override
  State<AccessibleButton> createState() => _AccessibleButtonState();
}

class _AccessibleButtonState extends State<AccessibleButton> {
  final FocusNode _focusNode = FocusNode();
  bool _isFocused = false;

  @override
  void initState() {
    super.initState();
    _focusNode.addListener(() {
      setState(() {
        _isFocused = _focusNode.hasFocus;
      });
    });
  }

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Focus(
      focusNode: _focusNode,
      child: Container(
        decoration: _isFocused
            ? BoxDecoration(
                border: Border.all(
                  color: Theme.of(context).colorScheme.primary,
                  width: 3,  // WCAG 2.2: Minimum 2px
                ),
                borderRadius: BorderRadius.circular(8),
              )
            : null,
        child: ElevatedButton(
          onPressed: widget.onPressed,
          focusNode: _focusNode,
          child: widget.child,
        ),
      ),
    );
  }
}
```

## Gesture Alternatives (WCAG 2.5.7)

**Requirement**: Provide tap alternative for all drag gestures.

```dart
// ❌ BAD: Drag-only interaction
Draggable(
  data: item,
  child: ItemWidget(item),
  feedback: ItemWidget(item),
);

// ✅ GOOD: Drag with tap alternative
class AccessibleDraggable extends StatelessWidget {
  final Item item;
  final VoidCallback onTap;  // Tap alternative

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,  // Tap to move/select
      onLongPress: () {
        // Show context menu with move options
        showMenu(
          context: context,
          position: RelativeRect.fill,
          items: [
            PopupMenuItem(
              child: Text('Move to top'),
              onTap: () => moveItem(item, 0),
            ),
            PopupMenuItem(
              child: Text('Move to bottom'),
              onTap: () => moveItem(item, -1),
            ),
          ],
        );
      },
      child: Draggable(
        data: item,
        child: Semantics(
          hint: 'Drag to reorder, or tap for options',
          child: ItemWidget(item),
        ),
        feedback: ItemWidget(item),
      ),
    );
  }
}
```

## Dynamic Font Sizing (WCAG 1.4.4)

**Requirement**: Support text resizing up to 200% without loss of functionality.

```dart
// ✅ ALWAYS use MediaQuery.textScaleFactor
class AccessibleText extends StatelessWidget {
  final String text;

  @override
  Widget build(BuildContext context) {
    final textScaleFactor = MediaQuery.of(context).textScaleFactor;

    return Text(
      text,
      style: TextStyle(
        fontSize: 16,  // Base size - will scale automatically
      ),
      // Flutter respects textScaleFactor automatically
    );
  }
}

// ❌ BAD: Fixed size that ignores user preference
Text(
  'Fixed text',
  textScaleFactor: 1.0,  // Don't do this!
);

// ✅ GOOD: Respect user's text size preference
Text(
  'Scales with user preference',
  // textScaleFactor uses MediaQuery by default
);

// Handle layout overflow with text scaling
LayoutBuilder(
  builder: (context, constraints) {
    final textScaleFactor = MediaQuery.of(context).textScaleFactor;

    return SingleChildScrollView(
      child: Text(
        longText,
        style: TextStyle(fontSize: 16),  // Scales automatically
      ),
    );
  },
);
```

## Screen Reader Testing

### TalkBack (Android)

```bash
# Enable TalkBack
Settings > Accessibility > TalkBack > On

# Test navigation
# - Swipe right: Next element
# - Swipe left: Previous element
# - Double tap: Activate
# - Two-finger swipe: Scroll
```

**Test Checklist**:
- [ ] All interactive elements have labels
- [ ] Labels are descriptive ("Delete event" not "Delete")
- [ ] Form fields announce errors
- [ ] Focus order is logical
- [ ] Images have semantic labels or are excluded

### VoiceOver (iOS)

```bash
# Enable VoiceOver
Settings > Accessibility > VoiceOver > On

# Test navigation
# - Swipe right: Next element
# - Swipe left: Previous element
# - Double tap: Activate
# - Three-finger swipe: Scroll
```

### Flutter Semantics Debugger

```dart
// Enable semantics debugger in dev
void main() {
  runApp(
    MaterialApp(
      showSemanticsDebugger: true,  // Shows semantic tree overlay
      home: MyApp(),
    ),
  );
}
```

## Checklist (WCAG 2.2 Level AA)

### Essential (WCAG A)
- [ ] All images have semanticLabel or excluded (1.1.1)
- [ ] Form fields have labels (3.3.2)
- [ ] Focus order is logical (2.4.3)
- [ ] Consistent help location (3.2.6)
- [ ] No redundant data entry (3.3.7)

### Important (WCAG AA)
- [ ] All IconButtons have tooltip (4.1.2)
- [ ] Touch targets >= 48x48dp (2.5.8 requires 24px min)
- [ ] Color contrast >= 4.5:1 text, 3:1 large (1.4.3)
- [ ] Focus indicator visible: 2px, 3:1 contrast (2.4.11)
- [ ] Gesture alternatives provided (2.5.7)
- [ ] Text resizes to 200% (1.4.4)
- [ ] No cognitive auth tests (3.3.8)
- [ ] Dynamic content in live regions (4.1.3)

### Testing
- [ ] Tested with TalkBack (Android)
- [ ] Tested with VoiceOver (iOS)
- [ ] Tested with text scaling (200%)
- [ ] Tested keyboard navigation (web/desktop)
- [ ] Verified color contrast (use DevTools)

---

## Changelog

### v2.0.0 (2026-01-12)
- **CRITICAL: Added WCAG 2.2 Level AA compliance section**
  - Government compliance deadline: April 24, 2026 (entities with 50k+ population)
  - Documented all 9 new WCAG 2.2 success criteria with Flutter implementations:
    1. **2.4.11 Focus Appearance** (AA) - Visible focus indicator (min 2px, contrast 3:1)
    2. **2.4.12 Focus Not Obscured (Minimum)** (AA) - Focused element not fully hidden
    3. **2.5.7 Dragging Movements** (AA) - Alternative to drag gestures
    4. **2.5.8 Target Size (Minimum)** (AA) - 24x24px minimum (Flutter: 48x48dp recommended)
    5. **3.2.6 Consistent Help** (A) - Help in same location
    6. **3.3.7 Redundant Entry** (A) - Don't ask for same info twice
    7. **3.3.8 Accessible Authentication** (AA) - No cognitive function tests
    8. Plus 2 AAA criteria (not required for AA compliance)
  - Added requirements table comparing WCAG 2.2 standard vs Flutter targets
- **Added Focus Management section** with custom FocusNode implementation
- **Added Gesture Alternatives pattern** (WCAG 2.5.7) with tap alternatives for drag gestures
- **Added Dynamic Font Sizing section** (WCAG 1.4.4) - Support 200% text scaling
- **Added Screen Reader Testing workflows**:
  - TalkBack (Android) testing guide
  - VoiceOver (iOS) testing guide
  - Flutter Semantics Debugger usage
- **Added comprehensive WCAG 2.2 Level AA checklist** (Essential + Important + Testing)
- Updated skill description with WCAG 2.2 compliance and deadline
- **Impact**: Legal compliance requirement for government entities, prevents accessibility lawsuits

### v1.0.0 (Initial)
- Basic accessibility patterns (WCAG 2.1)
- Semantics widget usage
- Screen reader support
- Touch target recommendations
- Color contrast guidelines

---

## Related Skills
- **flutter-ui-components**: Widget patterns
- **flutter-theming**: Color contrast, dynamic colors
- **flutter-testing**: Accessibility testing patterns
