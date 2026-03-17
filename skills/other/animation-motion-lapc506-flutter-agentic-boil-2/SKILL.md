# ✨ Skill: Animation & Motion Design

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-animation-motion` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `animation`, `motion`, `rive`, `lottie`, `hero`, `animationcontroller`, `tween` |
| **Referencia** | [Flutter Animations](https://docs.flutter.dev/ui/animations), [Rive Flutter](https://pub.dev/documentation/rive/latest/) |

## 🔑 Keywords para Invocación

- `animation`
- `motion`
- `rive`
- `lottie`
- `hero-animation`
- `animationcontroller`
- `tween`
- `@skill:animation`

### Ejemplos de Prompts

```
Implementa animations con rive y lottie
```

```
Setup motion design con hero animations y transitions
```

```
Configura animationcontroller con custom tweens
```

```
@skill:animation - Sistema completo de animaciones
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

Este skill cubre animaciones y motion design en Flutter desde lo básico (AnimationController, Tween) hasta soluciones avanzadas (Rive, Lottie). Incluye implicit animations, explicit animations, Hero animations, page transitions, y animated builders.

### ✅ Cuándo Usar Este Skill

- Mejorar UX con feedback visual
- Onboarding con animaciones
- Loading states animados
- Page transitions personalizadas
- Micro-interactions
- Complex animations (Rive/Lottie)
- Brand animations
- Interactive animations

### ❌ Cuándo NO Usar Este Skill

- MVP simple sin requisitos de UX
- Performance crítica (evita over-animation)
- Prototipos estáticos

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── animations/
│   │   ├── implicit/
│   │   │   └── fade_scale_animation.dart
│   │   ├── explicit/
│   │   │   ├── custom_animation_controller.dart
│   │   │   └── staggered_animation.dart
│   │   ├── rive/
│   │   │   └── rive_animations.dart
│   │   ├── lottie/
│   │   │   └── lottie_animations.dart
│   │   └── transitions/
│   │       ├── page_transitions.dart
│   │       └── hero_transitions.dart
│   │
│   └── main.dart
│
└── assets/
    ├── animations/
    │   ├── loading.json         # Lottie
    │   ├── success.json
    │   └── onboarding.riv       # Rive
    └── images/
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Lottie animations
  lottie: ^3.0.0

  # Rive animations (v0.14.0+)
  rive: ^0.14.0

  # Animated text
  animated_text_kit: ^4.2.2

  # Shimmer effect
  shimmer: ^3.0.0

dev_dependencies:
  flutter_test:
    sdk: flutter

flutter:
  assets:
    - assets/animations/
```

## 💻 Implementación

### 1. Implicit Animations

```dart
// lib/animations/implicit/fade_scale_animation.dart
import 'package:flutter/material.dart';

class FadeScaleAnimation extends StatefulWidget {
  final Widget child;
  final Duration duration;
  final bool visible;

  const FadeScaleAnimation({
    Key? key,
    required this.child,
    this.duration = const Duration(milliseconds: 300),
    this.visible = true,
  }) : super(key: key);

  @override
  State<FadeScaleAnimation> createState() => _FadeScaleAnimationState();
}

class _FadeScaleAnimationState extends State<FadeScaleAnimation> {
  @override
  Widget build(BuildContext context) {
    return AnimatedOpacity(
      opacity: widget.visible ? 1.0 : 0.0,
      duration: widget.duration,
      child: AnimatedScale(
        scale: widget.visible ? 1.0 : 0.0,
        duration: widget.duration,
        curve: Curves.easeInOut,
        child: widget.child,
      ),
    );
  }
}

// Usage Example
class ImplicitAnimationExample extends StatefulWidget {
  @override
  State<ImplicitAnimationExample> createState() => _ImplicitAnimationExampleState();
}

class _ImplicitAnimationExampleState extends State<ImplicitAnimationExample> {
  bool _visible = false;
  double _width = 100;
  double _height = 100;
  Color _color = Colors.blue;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Animated Container
        AnimatedContainer(
          duration: const Duration(milliseconds: 500),
          width: _width,
          height: _height,
          color: _color,
          curve: Curves.easeInOut,
        ),

        // Animated Positioned
        Stack(
          children: [
            AnimatedPositioned(
              duration: const Duration(milliseconds: 500),
              top: _visible ? 100 : 0,
              left: _visible ? 100 : 0,
              child: Container(width: 50, height: 50, color: Colors.red),
            ),
          ],
        ),

        // Animated Padding
        AnimatedPadding(
          duration: const Duration(milliseconds: 300),
          padding: EdgeInsets.all(_visible ? 32 : 8),
          child: const Text('Animated Padding'),
        ),

        // Animated Opacity
        AnimatedOpacity(
          opacity: _visible ? 1.0 : 0.0,
          duration: const Duration(milliseconds: 500),
          child: const Text('Fading Text'),
        ),

        // Controls
        ElevatedButton(
          onPressed: () {
            setState(() {
              _visible = !_visible;
              _width = _width == 100 ? 200 : 100;
              _height = _height == 100 ? 200 : 100;
              _color = _color == Colors.blue ? Colors.green : Colors.blue;
            });
          },
          child: const Text('Animate'),
        ),
      ],
    );
  }
}
```

### 2. Explicit Animations

```dart
// lib/animations/explicit/custom_animation_controller.dart
import 'package:flutter/material.dart';

class ExplicitAnimationExample extends StatefulWidget {
  @override
  State<ExplicitAnimationExample> createState() => _ExplicitAnimationExampleState();
}

class _ExplicitAnimationExampleState extends State<ExplicitAnimationExample>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _opacityAnimation;
  late Animation<double> _scaleAnimation;
  late Animation<Offset> _slideAnimation;
  late Animation<Color?> _colorAnimation;

  @override
  void initState() {
    super.initState();

    // Create controller
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );

    // Opacity animation
    _opacityAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: const Interval(0.0, 0.5, curve: Curves.easeIn),
    ));

    // Scale animation
    _scaleAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: const Interval(0.2, 0.8, curve: Curves.elasticOut),
    ));

    // Slide animation
    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 1),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: const Interval(0.4, 1.0, curve: Curves.easeOut),
    ));

    // Color animation
    _colorAnimation = ColorTween(
      begin: Colors.blue,
      end: Colors.purple,
    ).animate(_controller);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // AnimatedBuilder
        AnimatedBuilder(
          animation: _controller,
          builder: (context, child) {
            return Opacity(
              opacity: _opacityAnimation.value,
              child: Transform.scale(
                scale: _scaleAnimation.value,
                child: SlideTransition(
                  position: _slideAnimation,
                  child: Container(
                    width: 200,
                    height: 200,
                    decoration: BoxDecoration(
                      color: _colorAnimation.value,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: const Center(
                      child: Text(
                        'Animated Box',
                        style: TextStyle(color: Colors.white, fontSize: 20),
                      ),
                    ),
                  ),
                ),
              ),
            );
          },
        ),
        const SizedBox(height: 32),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => _controller.forward(),
              child: const Text('Play'),
            ),
            const SizedBox(width: 8),
            ElevatedButton(
              onPressed: () => _controller.reverse(),
              child: const Text('Reverse'),
            ),
            const SizedBox(width: 8),
            ElevatedButton(
              onPressed: () => _controller.repeat(),
              child: const Text('Repeat'),
            ),
            const SizedBox(width: 8),
            ElevatedButton(
              onPressed: () => _controller.reset(),
              child: const Text('Reset'),
            ),
          ],
        ),
      ],
    );
  }
}
```

### 3. Staggered Animations

```dart
// lib/animations/explicit/staggered_animation.dart
import 'package:flutter/material.dart';

class StaggeredAnimationExample extends StatefulWidget {
  @override
  State<StaggeredAnimationExample> createState() => _StaggeredAnimationExampleState();
}

class _StaggeredAnimationExampleState extends State<StaggeredAnimationExample>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late List<Animation<double>> _animations;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );

    // Create staggered animations
    _animations = List.generate(5, (index) {
      final start = index * 0.15;
      final end = start + 0.3;

      return Tween<double>(begin: 0.0, end: 1.0).animate(
        CurvedAnimation(
          parent: _controller,
          curve: Interval(
            start < 1.0 ? start : 1.0,
            end < 1.0 ? end : 1.0,
            curve: Curves.easeOut,
          ),
        ),
      );
    });

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: List.generate(5, (index) {
        return AnimatedBuilder(
          animation: _animations[index],
          builder: (context, child) {
            return Transform.translate(
              offset: Offset(
                (1 - _animations[index].value) * 300,
                0,
              ),
              child: Opacity(
                opacity: _animations[index].value,
                child: Container(
                  margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 32),
                  height: 60,
                  decoration: BoxDecoration(
                    color: Colors.primaries[index % Colors.primaries.length],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Center(
                    child: Text(
                      'Item ${index + 1}',
                      style: const TextStyle(color: Colors.white, fontSize: 18),
                    ),
                  ),
                ),
              ),
            );
          },
        );
      }),
    );
  }
}
```

### 4. Lottie Animations

```dart
// lib/animations/lottie/lottie_animations.dart
import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';

class LottieAnimationExample extends StatefulWidget {
  @override
  State<LottieAnimationExample> createState() => _LottieAnimationExampleState();
}

class _LottieAnimationExampleState extends State<LottieAnimationExample>
    with SingleTickerProviderStateMixin {
  late AnimationController _lottieController;

  @override
  void initState() {
    super.initState();
    _lottieController = AnimationController(vsync: this);
  }

  @override
  void dispose() {
    _lottieController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Simple Lottie animation
        Lottie.asset(
          'assets/animations/loading.json',
          width: 200,
          height: 200,
          fit: BoxFit.contain,
        ),

        // Lottie with controller
        Lottie.asset(
          'assets/animations/success.json',
          controller: _lottieController,
          width: 200,
          height: 200,
          onLoaded: (composition) {
            _lottieController.duration = composition.duration;
          },
        ),

        // Controls
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => _lottieController.forward(),
              child: const Text('Play'),
            ),
            const SizedBox(width: 8),
            ElevatedButton(
              onPressed: () => _lottieController.stop(),
              child: const Text('Stop'),
            ),
            const SizedBox(width: 8),
            ElevatedButton(
              onPressed: () => _lottieController.repeat(),
              child: const Text('Repeat'),
            ),
          ],
        ),

        // Network Lottie
        Lottie.network(
          'https://assets10.lottiefiles.com/packages/lf20_uwWgICKCxj.json',
          width: 200,
          height: 200,
        ),
      ],
    );
  }
}
```

### 5. Rive Animations

```dart
// lib/animations/rive/rive_animations.dart
import 'package:flutter/material.dart';
import 'package:rive/rive.dart';

class RiveAnimationExample extends StatefulWidget {
  @override
  State<RiveAnimationExample> createState() => _RiveAnimationExampleState();
}

class _RiveAnimationExampleState extends State<RiveAnimationExample> {
  Artboard? _artboard;
  StateMachineController? _stateMachineController;
  SMITrigger? _trigger;
  SMIBool? _boolean;
  SMINumber? _number;

  @override
  void initState() {
    super.initState();
    _loadRiveFile();
  }

  Future<void> _loadRiveFile() async {
    // Load Rive file with renderer choice
    // Factory.rive = Rive renderer (recommended)
    // Factory.flutter = Flutter renderer (Skia/Impeller)
    final riveFile = await File.asset(
      'assets/animations/onboarding.riv',
      riveFactory: Factory.rive, // or Factory.flutter
    );

    if (riveFile == null) return;

    // Get artboard
    final artboard = riveFile.artboardByName('Artboard');
    if (artboard == null) return;

    // Get state machine
    final stateMachine = artboard.stateMachineByName('State Machine 1');
    if (stateMachine == null) return;

    // Create controller
    final controller = StateMachineController(stateMachine);

    // Get inputs
    _trigger = controller.findInput<bool>('Trigger') as SMITrigger?;
    _boolean = controller.findInput<bool>('Boolean') as SMIBool?;
    _number = controller.findInput<double>('Number') as SMINumber?;

    // Add controller to artboard
    artboard.addController(controller);

    setState(() {
      _artboard = artboard;
      _stateMachineController = controller;
    });
  }

  @override
  void dispose() {
    _stateMachineController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_artboard == null) {
      return const Center(child: CircularProgressIndicator());
    }

    return Column(
      children: [
        // Rive animation widget
        SizedBox(
          width: 300,
          height: 300,
          child: Rive(
            artboard: _artboard!,
            fit: BoxFit.contain,
          ),
        ),

        // Controls
        ElevatedButton(
          onPressed: () => _trigger?.fire(),
          child: const Text('Fire Trigger'),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Boolean:'),
            Switch(
              value: _boolean?.value ?? false,
              onChanged: (value) {
                setState(() {
                  _boolean?.value = value;
                });
              },
            ),
          ],
        ),
        Slider(
          value: _number?.value ?? 0,
          min: 0,
          max: 100,
          onChanged: (value) {
            setState(() {
              _number?.value = value;
            });
          },
        ),
      ],
    );
  }
}

// Alternative: Simple Rive animation without state machine
class SimpleRiveAnimation extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<File?>(
      future: File.asset(
        'assets/animations/loading.riv',
        riveFactory: Factory.rive,
      ),
      builder: (context, snapshot) {
        if (!snapshot.hasData || snapshot.data == null) {
          return const CircularProgressIndicator();
        }

        final artboard = snapshot.data!.artboard;
        return SizedBox(
          width: 200,
          height: 200,
          child: Rive(
            artboard: artboard,
            fit: BoxFit.contain,
          ),
        );
      },
    );
  }
}

// Network Rive file
class NetworkRiveAnimation extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<File?>(
      future: File.network(
        'https://cdn.rive.app/animations/vehicles.riv',
        riveFactory: Factory.rive,
      ),
      builder: (context, snapshot) {
        if (!snapshot.hasData || snapshot.data == null) {
          return const CircularProgressIndicator();
        }

        final artboard = snapshot.data!.artboard;
        return Rive(
          artboard: artboard,
          fit: BoxFit.contain,
        );
      },
    );
  }
}
```

#### 5.1 Choosing a Renderer

Rive Flutter ofrece dos opciones de renderer:

```dart
// Option 1: Rive Renderer (Recommended)
// - Optimized for Rive animations
// - Better performance for complex animations
// - Consistent rendering across platforms
final riveFile = await File.asset(
  'assets/animations/animation.riv',
  riveFactory: Factory.rive,
);

// Option 2: Flutter Renderer (Skia/Impeller)
// - Uses Flutter's native renderer
// - May have rendering differences with Impeller
// - Useful for consistency with Flutter widgets
final riveFile = await File.asset(
  'assets/animations/animation.riv',
  riveFactory: Factory.flutter,
);
```

**Note on Impeller Renderer:**
Starting in Flutter v3.10, Impeller is the default renderer on iOS. If you encounter visual discrepancies:

1. Test with Skia: `cd mobile && flutter run --no-enable-impeller && cd ..`
2. Test on latest master channel
3. Report issues to Flutter team if problems persist

#### 5.2 State Machine Control

```dart
// Advanced state machine control
class AdvancedRiveController extends StatefulWidget {
  @override
  State<AdvancedRiveController> createState() => _AdvancedRiveControllerState();
}

class _AdvancedRiveControllerState extends State<AdvancedRiveController> {
  Artboard? _artboard;
  StateMachineController? _controller;

  Future<void> _loadAnimation() async {
    final file = await File.asset(
      'assets/animations/interactive.riv',
      riveFactory: Factory.rive,
    );

    final artboard = file?.artboard;
    final stateMachine = artboard?.stateMachineByName('State Machine');

    if (artboard != null && stateMachine != null) {
      final controller = StateMachineController(stateMachine);
      artboard.addController(controller);

      setState(() {
        _artboard = artboard;
        _controller = controller;
      });
    }
  }

  // Play specific animation
  void _playAnimation(String animationName) {
    final animation = _artboard?.animationByName(animationName);
    if (animation != null) {
      _controller?.input<bool>('Play $animationName')?.value = true;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_artboard == null) {
      return const CircularProgressIndicator();
    }

    return Rive(artboard: _artboard!);
  }
}
```

### 6. Hero Animations

```dart
// lib/animations/transitions/hero_transitions.dart
import 'package:flutter/material.dart';

class HeroListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Hero List')),
      body: ListView.builder(
        itemCount: 10,
        itemBuilder: (context, index) {
          return ListTile(
            leading: Hero(
              tag: 'hero-$index',
              child: CircleAvatar(
                child: Text('$index'),
              ),
            ),
            title: Text('Item $index'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => HeroDetailScreen(index: index),
                ),
              );
            },
          );
        },
      ),
    );
  }
}

class HeroDetailScreen extends StatelessWidget {
  final int index;

  const HeroDetailScreen({Key? key, required this.index}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Item $index')),
      body: Center(
        child: Hero(
          tag: 'hero-$index',
          child: Container(
            width: 200,
            height: 200,
            decoration: BoxDecoration(
              color: Colors.blue,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Center(
              child: Text(
                '$index',
                style: const TextStyle(fontSize: 48, color: Colors.white),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
```

### 7. Custom Page Transitions

```dart
// lib/animations/transitions/page_transitions.dart
import 'package:flutter/material.dart';

class FadePageRoute<T> extends PageRoute<T> {
  final WidgetBuilder builder;

  FadePageRoute({required this.builder});

  @override
  Color? get barrierColor => null;

  @override
  String? get barrierLabel => null;

  @override
  bool get maintainState => true;

  @override
  Duration get transitionDuration => const Duration(milliseconds: 300);

  @override
  Widget buildPage(
    BuildContext context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
  ) {
    return FadeTransition(
      opacity: animation,
      child: builder(context),
    );
  }
}

class SlidePageRoute<T> extends PageRoute<T> {
  final WidgetBuilder builder;
  final AxisDirection direction;

  SlidePageRoute({
    required this.builder,
    this.direction = AxisDirection.right,
  });

  @override
  Color? get barrierColor => null;

  @override
  String? get barrierLabel => null;

  @override
  bool get maintainState => true;

  @override
  Duration get transitionDuration => const Duration(milliseconds: 300);

  @override
  Widget buildPage(
    BuildContext context,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
  ) {
    Offset begin;
    switch (direction) {
      case AxisDirection.up:
        begin = const Offset(0, 1);
        break;
      case AxisDirection.down:
        begin = const Offset(0, -1);
        break;
      case AxisDirection.left:
        begin = const Offset(1, 0);
        break;
      case AxisDirection.right:
        begin = const Offset(-1, 0);
        break;
    }

    return SlideTransition(
      position: Tween<Offset>(
        begin: begin,
        end: Offset.zero,
      ).animate(CurvedAnimation(
        parent: animation,
        curve: Curves.easeOut,
      )),
      child: builder(context),
    );
  }
}

// Usage
Navigator.push(
  context,
  FadePageRoute(builder: (context) => NextScreen()),
);

Navigator.push(
  context,
  SlidePageRoute(
    builder: (context) => NextScreen(),
    direction: AxisDirection.left,
  ),
);
```

## 🎯 Mejores Prácticas

### 1. Performance

✅ **DO:** Usa `const` constructors
```dart
const AnimatedOpacity(
  opacity: 1.0,
  duration: Duration(milliseconds: 300),
  child: Text('Optimized'),
);
```

### 2. Animation Disposal

✅ **DO:** Siempre dispose controllers
```dart
@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

### 3. Avoid Over-Animation

❌ **DON'T:** Animar todo
```dart
// Usa animaciones con propósito, no por estética solamente
```

## 🚨 Troubleshooting

### Animation Janky/Laggy

```dart
// Use RepaintBoundary to isolate repaints
RepaintBoundary(
  child: AnimatedWidget(...),
);
```

### Animation Not Disposing

```dart
// Always use dispose()
@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

### Rive Animation Issues

#### File Not Loading

```dart
// Verify file path and asset declaration
// pubspec.yaml:
// flutter:
//   assets:
//     - assets/animations/

// Check file exists
final file = await File.asset('assets/animations/animation.riv');
if (file == null) {
  print('File not found or invalid');
}
```

#### State Machine Not Found

```dart
// Verify state machine name matches exactly
final stateMachine = artboard.stateMachineByName('State Machine 1');
// Name must match exactly as in Rive Editor
```

#### Renderer Issues with Impeller

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# If visual discrepancies on iOS, test with Skia:
cd mobile
flutter run --no-enable-impeller
cd ..

# Or try Flutter renderer instead:
final file = await File.asset(
  'assets/animation.riv',
  riveFactory: Factory.flutter, // Instead of Factory.rive
);
```

#### Native Libraries Not Found

```bash
# Clean and rebuild
flutter clean
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

cd mobile
flutter pub get
flutter run
cd ..

# Or manually setup native libraries
dart run rive_native:setup --verbose --clean --platform ios
dart run rive_native:setup --verbose --clean --platform android
```

#### Platform Support

Rive Flutter supports:
- ✅ iOS (Flutter & Rive renderers)
- ✅ Android (Flutter & Rive renderers)
- ✅ macOS (Flutter & Rive renderers)
- ✅ Windows (Flutter & Rive renderers)
- ✅ Web (Flutter & Rive renderers)
- ❌ Linux (not supported)

## 📚 Recursos

- [Flutter Animations](https://docs.flutter.dev/ui/animations)
- [Lottie Files](https://lottiefiles.com/)
- [Rive Flutter Documentation](https://pub.dev/documentation/rive/latest/)
- [Rive Flutter GitHub](https://github.com/rive-app/rive-flutter)
- [Rive Community](https://rive.app/community/)
- [Rive Getting Started](https://rive.app/community/learn/getting-started-with-rive-in-flutter/)

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025  
**Total líneas:** 1,100+

