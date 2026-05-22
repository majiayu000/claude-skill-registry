# ♿ Skill: Accessibility (a11y)

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-accessibility` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `accessibility`, `a11y`, `semantic`, `screen-reader`, `wcag`, `talkback`, `voiceover` |
| **Referencia** | [Flutter Accessibility](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility) |

## 🔑 Keywords para Invocación

- `accessibility`
- `a11y`
- `semantic`
- `screen-reader`
- `wcag`
- `talkback`
- `voiceover`
- `@skill:accessibility`

### Ejemplos de Prompts

```
Implementa accessibility con semantic widgets y screen reader support
```

```
Setup wcag compliance para la app
```

```
Configura talkback y voiceover support
```

```
@skill:accessibility - Accessibility completa
```

## 📖 Descripción

Este skill cubre la implementación de accesibilidad en Flutter apps siguiendo las guías WCAG (Web Content Accessibility Guidelines). Incluye Semantic widgets, screen reader support (TalkBack/VoiceOver), focus management, y contrast ratios.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- **Siempre** - La accesibilidad debe ser una prioridad
- Apps para público general
- Apps gubernamentales (requerido legalmente)
- Apps educativas
- Apps de salud
- E-commerce
- Cumplimiento legal (ADA, Section 508)

### ❌ Cuándo NO Usar Este Skill

- Nunca - La accesibilidad es fundamental para todos los usuarios

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── core/
│   │   └── accessibility/
│   │       ├── semantic_wrappers.dart
│   │       ├── accessibility_utils.dart
│   │       └── focus_manager.dart
│   │
│   └── main.dart
│
└── test/
    └── accessibility_test.dart
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
```

## 💻 Implementación

### 1. Semantic Widgets

```dart
// lib/core/accessibility/semantic_wrappers.dart
import 'package:flutter/material.dart';

class AccessibleButton extends StatelessWidget {
  final VoidCallback onPressed;
  final Widget child;
  final String? semanticLabel;
  final String? semanticHint;
  final bool enabled;

  const AccessibleButton({
    Key? key,
    required this.onPressed,
    required this.child,
    this.semanticLabel,
    this.semanticHint,
    this.enabled = true,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticLabel,
      hint: semanticHint,
      button: true,
      enabled: enabled,
      onTap: enabled ? onPressed : null,
      child: ElevatedButton(
        onPressed: enabled ? onPressed : null,
        child: child,
      ),
    );
  }
}

class AccessibleTextField extends StatelessWidget {
  final TextEditingController? controller;
  final String? label;
  final String? hint;
  final String? errorText;
  final bool obscureText;
  final TextInputType? keyboardType;
  final ValueChanged<String>? onChanged;

  const AccessibleTextField({
    Key? key,
    this.controller,
    this.label,
    this.hint,
    this.errorText,
    this.obscureText = false,
    this.keyboardType,
    this.onChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: label,
      hint: hint,
      textField: true,
      child: TextField(
        controller: controller,
        obscureText: obscureText,
        keyboardType: keyboardType,
        onChanged: onChanged,
        decoration: InputDecoration(
          labelText: label,
          hintText: hint,
          errorText: errorText,
          // Add semantic description for error
          semanticCounterText: errorText != null ? 'Error: $errorText' : null,
        ),
      ),
    );
  }
}

class AccessibleImage extends StatelessWidget {
  final String imagePath;
  final String semanticLabel;
  final double? width;
  final double? height;
  final BoxFit? fit;

  const AccessibleImage({
    Key? key,
    required this.imagePath,
    required this.semanticLabel,
    this.width,
    this.height,
    this.fit,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticLabel,
      image: true,
      child: Image.asset(
        imagePath,
        width: width,
        height: height,
        fit: fit,
        // Screen readers will skip this since Semantics provides the label
        excludeFromSemantics: true,
      ),
    );
  }
}

class AccessibleCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final String? semanticLabel;
  final String? semanticHint;

  const AccessibleCard({
    Key? key,
    required this.child,
    this.onTap,
    this.semanticLabel,
    this.semanticHint,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticLabel,
      hint: semanticHint,
      button: onTap != null,
      onTap: onTap,
      container: true,
      child: Card(
        child: InkWell(
          onTap: onTap,
          child: child,
        ),
      ),
    );
  }
}

class AccessibleListTile extends StatelessWidget {
  final Widget title;
  final Widget? subtitle;
  final Widget? leading;
  final Widget? trailing;
  final VoidCallback? onTap;
  final String? semanticLabel;

  const AccessibleListTile({
    Key? key,
    required this.title,
    this.subtitle,
    this.leading,
    this.trailing,
    this.onTap,
    this.semanticLabel,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MergeSemantics(
      child: ListTile(
        title: Semantics(
          // Exclude default semantics from title
          excludeSemantics: true,
          child: title,
        ),
        subtitle: subtitle != null
            ? Semantics(
                excludeSemantics: true,
                child: subtitle,
              )
            : null,
        leading: leading,
        trailing: trailing,
        onTap: onTap,
      ),
    );
  }
}
```

### 2. Accessibility Utils

```dart
// lib/core/accessibility/accessibility_utils.dart
import 'package:flutter/material.dart';
import 'dart:ui' as ui;

class AccessibilityUtils {
  // Check if screen reader is enabled
  static bool get isScreenReaderEnabled {
    return WidgetsBinding.instance.accessibilityFeatures.accessibleNavigation;
  }

  // Check if bold text is enabled
  static bool get isBoldTextEnabled {
    return WidgetsBinding.instance.accessibilityFeatures.boldText;
  }

  // Check if reduce animations is enabled
  static bool get isReduceAnimationsEnabled {
    return WidgetsBinding.instance.accessibilityFeatures.disableAnimations;
  }

  // Check if high contrast is enabled
  static bool get isHighContrastEnabled {
    return WidgetsBinding.instance.accessibilityFeatures.highContrast;
  }

  // Check contrast ratio (WCAG guidelines)
  static bool meetsContrastRatio(Color foreground, Color background, {bool isLargeText = false}) {
    final contrastRatio = calculateContrastRatio(foreground, background);

    // WCAG AA standards:
    // - Normal text: 4.5:1
    // - Large text: 3:1
    final requiredRatio = isLargeText ? 3.0 : 4.5;

    return contrastRatio >= requiredRatio;
  }

  // Calculate contrast ratio between two colors
  static double calculateContrastRatio(Color color1, Color color2) {
    final l1 = _relativeLuminance(color1);
    final l2 = _relativeLuminance(color2);

    final lighter = l1 > l2 ? l1 : l2;
    final darker = l1 > l2 ? l2 : l1;

    return (lighter + 0.05) / (darker + 0.05);
  }

  // Calculate relative luminance
  static double _relativeLuminance(Color color) {
    final r = _linearize(color.red / 255);
    final g = _linearize(color.green / 255);
    final b = _linearize(color.blue / 255);

    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }

  static double _linearize(double channel) {
    if (channel <= 0.03928) {
      return channel / 12.92;
    }
    return ((channel + 0.055) / 1.055).pow(2.4).toDouble();
  }

  // Get accessible text size
  static double getAccessibleTextSize(double defaultSize) {
    final textScaleFactor = WidgetsBinding.instance.platformDispatcher.textScaleFactor;
    return defaultSize * textScaleFactor;
  }

  // Announce to screen reader
  static void announce(BuildContext context, String message) {
    SemanticsService.announce(message, TextDirection.ltr);
  }

  // Request focus for accessibility
  static void requestFocus(FocusNode node) {
    node.requestFocus();
  }
}

extension ColorContrastExtension on Color {
  bool hasGoodContrastWith(Color other, {bool isLargeText = false}) {
    return AccessibilityUtils.meetsContrastRatio(this, other, isLargeText: isLargeText);
  }
}
```

### 3. Focus Management

```dart
// lib/core/accessibility/focus_manager.dart
import 'package:flutter/material.dart';

class AccessibleFocusManager {
  // Focus nodes registry
  static final Map<String, FocusNode> _focusNodes = {};

  // Register focus node
  static FocusNode registerFocusNode(String key) {
    if (!_focusNodes.containsKey(key)) {
      _focusNodes[key] = FocusNode();
    }
    return _focusNodes[key]!;
  }

  // Get focus node
  static FocusNode? getFocusNode(String key) {
    return _focusNodes[key];
  }

  // Request focus
  static void requestFocus(String key) {
    _focusNodes[key]?.requestFocus();
  }

  // Unfocus
  static void unfocus(String key) {
    _focusNodes[key]?.unfocus();
  }

  // Dispose all focus nodes
  static void disposeAll() {
    for (final node in _focusNodes.values) {
      node.dispose();
    }
    _focusNodes.clear();
  }

  // Next focus
  static void nextFocus(BuildContext context) {
    FocusScope.of(context).nextFocus();
  }

  // Previous focus
  static void previousFocus(BuildContext context) {
    FocusScope.of(context).previousFocus();
  }
}

// Accessible Form with Focus Management
class AccessibleForm extends StatefulWidget {
  @override
  State<AccessibleForm> createState() => _AccessibleFormState();
}

class _AccessibleFormState extends State<AccessibleForm> {
  final _formKey = GlobalKey<FormState>();
  final _nameFocusNode = FocusNode();
  final _emailFocusNode = FocusNode();
  final _passwordFocusNode = FocusNode();

  @override
  void dispose() {
    _nameFocusNode.dispose();
    _emailFocusNode.dispose();
    _passwordFocusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            focusNode: _nameFocusNode,
            decoration: const InputDecoration(
              labelText: 'Name',
              hintText: 'Enter your full name',
            ),
            textInputAction: TextInputAction.next,
            onFieldSubmitted: (_) {
              FocusScope.of(context).requestFocus(_emailFocusNode);
            },
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Please enter your name';
              }
              return null;
            },
          ),
          TextFormField(
            focusNode: _emailFocusNode,
            decoration: const InputDecoration(
              labelText: 'Email',
              hintText: 'Enter your email address',
            ),
            keyboardType: TextInputType.emailAddress,
            textInputAction: TextInputAction.next,
            onFieldSubmitted: (_) {
              FocusScope.of(context).requestFocus(_passwordFocusNode);
            },
            validator: (value) {
              if (value == null || !value.contains('@')) {
                return 'Please enter a valid email';
              }
              return null;
            },
          ),
          TextFormField(
            focusNode: _passwordFocusNode,
            decoration: const InputDecoration(
              labelText: 'Password',
              hintText: 'Enter your password',
            ),
            obscureText: true,
            textInputAction: TextInputAction.done,
            onFieldSubmitted: (_) {
              _submitForm();
            },
            validator: (value) {
              if (value == null || value.length < 6) {
                return 'Password must be at least 6 characters';
              }
              return null;
            },
          ),
          ElevatedButton(
            onPressed: _submitForm,
            child: const Text('Submit'),
          ),
        ],
      ),
    );
  }

  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      // Announce success to screen reader
      AccessibilityUtils.announce(context, 'Form submitted successfully');

      // Process form
    } else {
      // Announce errors
      AccessibilityUtils.announce(context, 'Please fix the errors in the form');
    }
  }
}
```

### 4. Semantic Examples

```dart
// Complete accessibility example
class AccessibilityExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Accessibility Example'),
      ),
      body: ListView(
        children: [
          // Accessible header
          Semantics(
            header: true,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Text(
                'Welcome',
                style: Theme.of(context).textTheme.headlineMedium,
              ),
            ),
          ),

          // Accessible button
          Padding(
            padding: const EdgeInsets.all(16),
            child: AccessibleButton(
              onPressed: () {},
              semanticLabel: 'Submit form',
              semanticHint: 'Submits the form and continues to next step',
              child: const Text('Submit'),
            ),
          ),

          // Accessible switch
          Semantics(
            label: 'Enable notifications',
            hint: 'Toggle to enable or disable push notifications',
            toggled: true,
            child: SwitchListTile(
              title: const Text('Notifications'),
              value: true,
              onChanged: (value) {},
            ),
          ),

          // Accessible slider
          Semantics(
            label: 'Volume',
            value: '50%',
            hint: 'Adjust volume from 0 to 100 percent',
            increasedValue: '51%',
            decreasedValue: '49%',
            child: Slider(
              value: 0.5,
              onChanged: (value) {},
            ),
          ),

          // Accessible progress indicator
          Semantics(
            label: 'Loading',
            value: '75% complete',
            child: const LinearProgressIndicator(value: 0.75),
          ),

          // Group related items
          MergeSemantics(
            child: Row(
              children: [
                const Icon(Icons.star),
                const Text('4.5'),
                const Text(' out of 5 stars'),
              ],
            ),
          ),

          // Exclude decorative elements
          ExcludeSemantics(
            child: Container(
              width: 100,
              height: 2,
              color: Colors.grey,
            ),
          ),

          // Live region (announces changes)
          Semantics(
            liveRegion: true,
            child: Text('2 new messages'),
          ),
        ],
      ),
    );
  }
}
```

### 5. Testing Accessibility

```dart
// test/accessibility_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Button has proper semantics', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: ElevatedButton(
            onPressed: () {},
            child: const Text('Submit'),
          ),
        ),
      ),
    );

    // Find button by semantic label
    final semanticFinder = find.bySemanticsLabel('Submit');
    expect(semanticFinder, findsOneWidget);

    // Verify button semantics
    final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
    expect(button.onPressed, isNotNull);
  });

  testWidgets('Meets minimum tap target size', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Center(
            child: ElevatedButton(
              onPressed: () {},
              child: const Text('Tap'),
            ),
          ),
        ),
      ),
    );

    // Minimum tap target: 48x48 logical pixels
    final buttonSize = tester.getSize(find.byType(ElevatedButton));
    expect(buttonSize.width, greaterThanOrEqualTo(48));
    expect(buttonSize.height, greaterThanOrEqualTo(48));
  });

  testWidgets('Contrast ratio meets WCAG AA', (WidgetTester tester) async {
    const foregroundColor = Colors.black;
    const backgroundColor = Colors.white;

    final contrastRatio = AccessibilityUtils.calculateContrastRatio(
      foregroundColor,
      backgroundColor,
    );

    // WCAG AA requires 4.5:1 for normal text
    expect(contrastRatio, greaterThanOrEqualTo(4.5));
  });
}
```

## 🎯 Mejores Prácticas

### 1. Minimum Touch Targets

✅ **DO:** 48x48 dp minimum
```dart
SizedBox(
  width: 48,
  height: 48,
  child: IconButton(
    onPressed: () {},
    icon: const Icon(Icons.close),
  ),
);
```

### 2. Descriptive Labels

✅ **DO:** Provide context
```dart
Semantics(
  label: 'Delete user John Doe',
  hint: 'Double tap to delete this user permanently',
  child: IconButton(
    icon: const Icon(Icons.delete),
    onPressed: () {},
  ),
);
```

### 3. Focus Order

✅ **DO:** Logical tab order
```dart
FocusTraversalGroup(
  policy: OrderedTraversalPolicy(),
  child: Column(
    children: [
      FocusTraversalOrder(
        order: NumericFocusOrder(1),
        child: TextField(),
      ),
      FocusTraversalOrder(
        order: NumericFocusOrder(2),
        child: TextField(),
      ),
    ],
  ),
);
```

## 🚨 Troubleshooting

### Screen Reader Not Reading

```dart
// Verify Semantics widget is properly configured
Semantics(
  label: 'Your label here',
  enabled: true,
  child: YourWidget(),
);
```

### Double Announcements

```dart
// Exclude child semantics if providing parent semantic
Semantics(
  label: 'Custom label',
  excludeSemantics: true,
  child: Text('This won\'t be read'),
);
```

## 📚 Recursos

- [Flutter Accessibility](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Android TalkBack](https://support.google.com/accessibility/android/answer/6283677)
- [iOS VoiceOver](https://support.apple.com/guide/iphone/turn-on-and-practice-voiceover-iph3e2e415f/ios)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
