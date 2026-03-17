# ⚡ Skill: Performance Optimization

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-performance` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `performance`, `optimization`, `profiling`, `memory`, `rendering` |
| **Referencia** | [Flutter Performance Best Practices](https://docs.flutter.dev/perf/best-practices) |

## 🔑 Keywords para Invocación

- `performance`
- `optimization`
- `profiling`
- `memory-leak`
- `rendering-optimization`
- `@skill:performance`

### Ejemplos de Prompts

```
Optimiza el performance de la app
```

```
Reduce el rebuild y mejora el rendering
```

```
@skill:performance - Implementa mejores prácticas de performance
```

## 📖 Descripción

Performance Optimization cubre técnicas para mejorar velocidad, fluidez y eficiencia de apps Flutter: reducir rebuilds, optimizar listas, gestión de memoria, lazy loading, code splitting, image optimization y profiling.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- App tiene lag o stuttering
- Tiempos de carga lentos
- Consumo excesivo de memoria
- Frame drops en animaciones
- Listas largas con scrolling lento
- Build times largos

### ❌ Cuándo NO Usar Este Skill

- Premature optimization en prototipos
- Performance ya es aceptable

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── performance/
│   │   ├── performance_monitor.dart
│   │   ├── memory_tracker.dart
│   │   └── build_tracker.dart
│   └── widgets/
│       ├── optimized/
│       │   ├── optimized_list_view.dart
│       │   ├── cached_network_image_wrapper.dart
│       │   └── sliver_performance_widget.dart
│       └── lazy/
│           └── lazy_indexed_stack.dart
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Image optimization
  cached_network_image: ^3.3.0
  flutter_cache_manager: ^3.3.1

  # Performance monitoring
  performance: ^0.2.0

  # Utils
  equatable: ^2.0.5

dev_dependencies:
  # Performance testing
  integration_test:
    sdk: flutter
  flutter_driver:
    sdk: flutter
```

## 💻 Implementación

### 1. Reducir Rebuilds con const

```dart
// ❌ BAD: Widget se reconstruye en cada frame
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text('Hello'),
    );
  }
}

// ✅ GOOD: Widget es const, no se reconstruye
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return const Text('Hello');
  }
}
```

### 2. Usar Keys Correctamente

```dart
// ✅ GOOD: ValueKey para identificar widgets únicamente
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    final item = items[index];
    return ItemWidget(
      key: ValueKey(item.id),  // Ayuda a Flutter a identificar el widget
      item: item,
    );
  },
)
```

### 3. Optimizar ListView con ListView.builder

```dart
// ❌ BAD: Crea todos los widgets a la vez
ListView(
  children: items.map((item) => ItemWidget(item: item)).toList(),
)

// ✅ GOOD: Crea widgets solo cuando son visibles
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ItemWidget(item: items[index]);
  },
)

// ✅ BETTER: Con separadores eficientes
ListView.separated(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(item: items[index]),
  separatorBuilder: (context, index) => const Divider(height: 1),
)
```

### 4. Usar RepaintBoundary

```dart
// Aislar widgets que se repintan frecuentemente
class AnimatedWidget extends StatefulWidget {
  @override
  _AnimatedWidgetState createState() => _AnimatedWidgetState();
}

class _AnimatedWidgetState extends State<AnimatedWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Widget estático, no necesita repaint
        const Text('Static Header'),

        // Widget animado, aislado con RepaintBoundary
        RepaintBoundary(
          child: AnimatedBuilder(
            animation: _controller,
            builder: (context, child) {
              return Transform.rotate(
                angle: _controller.value * 2 * 3.14159,
                child: child,
              );
            },
            child: const Icon(Icons.refresh, size: 100),
          ),
        ),

        // Otro widget estático
        const Text('Static Footer'),
      ],
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

### 5. Optimizar Imágenes

```dart
// lib/core/widgets/optimized/optimized_image.dart
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';

class OptimizedImage extends StatelessWidget {
  final String imageUrl;
  final double? width;
  final double? height;
  final BoxFit fit;

  const OptimizedImage({
    super.key,
    required this.imageUrl,
    this.width,
    this.height,
    this.fit = BoxFit.cover,
  });

  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: imageUrl,
      width: width,
      height: height,
      fit: fit,

      // Progressive loading
      progressIndicatorBuilder: (context, url, downloadProgress) {
        return Center(
          child: CircularProgressIndicator(
            value: downloadProgress.progress,
          ),
        );
      },

      // Error handling
      errorWidget: (context, url, error) {
        return const Icon(Icons.error);
      },

      // Memory cache
      memCacheWidth: width?.toInt(),
      memCacheHeight: height?.toInt(),

      // Fade in animation
      fadeInDuration: const Duration(milliseconds: 300),
    );
  }
}

// Uso
OptimizedImage(
  imageUrl: 'https://example.com/image.jpg',
  width: 100,
  height: 100,
  fit: BoxFit.cover,
)
```

### 6. Lazy Loading con AutomaticKeepAliveClientMixin

```dart
// Mantener estado de tabs sin reconstruir
class ProductsTab extends StatefulWidget {
  const ProductsTab({super.key});

  @override
  State<ProductsTab> createState() => _ProductsTabState();
}

class _ProductsTabState extends State<ProductsTab>
    with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true;  // Mantener estado

  @override
  Widget build(BuildContext context) {
    super.build(context);  // IMPORTANTE: Llamar super.build

    return ListView.builder(
      itemCount: 100,
      itemBuilder: (context, index) {
        return ListTile(title: Text('Product $index'));
      },
    );
  }
}
```

### 7. Optimizar Slivers

```dart
class OptimizedScrollView extends StatelessWidget {
  const OptimizedScrollView({super.key});

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        // App bar que se colapsa
        SliverAppBar(
          expandedHeight: 200,
          pinned: true,
          flexibleSpace: FlexibleSpaceBar(
            title: const Text('Products'),
            background: Image.network(
              'https://example.com/header.jpg',
              fit: BoxFit.cover,
            ),
          ),
        ),

        // Lista optimizada con builder
        SliverList(
          delegate: SliverChildBuilderDelegate(
            (context, index) {
              return ProductCard(index: index);
            },
            childCount: 1000,
          ),
        ),

        // Grid optimizado
        SliverGrid(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
          ),
          delegate: SliverChildBuilderDelegate(
            (context, index) {
              return GridItem(index: index);
            },
            childCount: 100,
          ),
        ),
      ],
    );
  }
}
```

### 8. Evitar Funciones en build()

```dart
// ❌ BAD: Función se ejecuta en cada build
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Text(
      _formatDate(DateTime.now()),  // Se calcula en cada build
      style: _getTextStyle(),        // Se crea en cada build
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }

  TextStyle _getTextStyle() {
    return const TextStyle(fontSize: 16, fontWeight: FontWeight.bold);
  }
}

// ✅ GOOD: Valores se calculan una vez
class MyWidget extends StatelessWidget {
  final String formattedDate;
  static const textStyle = TextStyle(fontSize: 16, fontWeight: FontWeight.bold);

  MyWidget({super.key}) : formattedDate = _formatDate(DateTime.now());

  static String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }

  @override
  Widget build(BuildContext context) {
    return Text(formattedDate, style: textStyle);
  }
}
```

### 9. Usar Selector para Actualizaciones Específicas

```dart
// Con flutter_bloc
class ProductPriceText extends StatelessWidget {
  const ProductPriceText({super.key});

  @override
  Widget build(BuildContext context) {
    // Solo se reconstruye cuando el precio cambia
    final price = context.select((ProductBloc bloc) => bloc.state.price);

    return Text('\$$price');
  }
}

// Con Provider
class ProductPriceText extends StatelessWidget {
  const ProductPriceText({super.key});

  @override
  Widget build(BuildContext context) {
    // Solo se reconstruye cuando el precio cambia
    final price = context.select<ProductModel, double>((product) => product.price);

    return Text('\$$price');
  }
}
```

### 10. Lazy IndexedStack

```dart
// lib/core/widgets/lazy/lazy_indexed_stack.dart
class LazyIndexedStack extends StatefulWidget {
  final int index;
  final List<Widget> children;

  const LazyIndexedStack({
    super.key,
    required this.index,
    required this.children,
  });

  @override
  State<LazyIndexedStack> createState() => _LazyIndexedStackState();
}

class _LazyIndexedStackState extends State<LazyIndexedStack> {
  late List<bool> _activated;

  @override
  void initState() {
    super.initState();
    _activated = List.generate(widget.children.length, (i) => i == widget.index);
  }

  @override
  void didUpdateWidget(LazyIndexedStack oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.index != widget.index) {
      _activated[widget.index] = true;
    }
  }

  @override
  Widget build(BuildContext context) {
    return IndexedStack(
      index: widget.index,
      children: List.generate(
        widget.children.length,
        (i) => _activated[i] ? widget.children[i] : const SizedBox.shrink(),
      ),
    );
  }
}
```

### 11. Performance Monitoring

```dart
// lib/core/performance/performance_monitor.dart
import 'package:flutter/scheduler.dart';

class PerformanceMonitor {
  static void trackBuildTime(String widgetName, VoidCallback buildFunction) {
    final stopwatch = Stopwatch()..start();

    buildFunction();

    stopwatch.stop();

    if (stopwatch.elapsedMilliseconds > 16) {  // 60 FPS = 16ms per frame
      print('⚠️ Slow build: $widgetName took ${stopwatch.elapsedMilliseconds}ms');
    }
  }

  static void trackFrameTime() {
    SchedulerBinding.instance.addTimingsCallback((timings) {
      for (final timing in timings) {
        final buildTime = timing.buildDuration.inMilliseconds;
        final rasterTime = timing.rasterDuration.inMilliseconds;

        if (buildTime > 16 || rasterTime > 16) {
          print('⚠️ Frame drop: Build=${buildTime}ms, Raster=${rasterTime}ms');
        }
      }
    });
  }
}

// Uso
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return PerformanceMonitor.trackBuildTime('MyWidget', () {
      return Container(
        // widget content
      );
    }) as Widget;
  }
}
```

### 12. Code Splitting con Deferred Loading

```dart
// lib/features/settings/settings.dart
library settings;

export 'presentation/screens/settings_screen.dart';
export 'presentation/widgets/settings_list.dart';

// main.dart
import 'features/settings/settings.dart' deferred as settings;

// Cargar módulo cuando sea necesario
void navigateToSettings() async {
  await settings.loadLibrary();  // Carga el código
  Navigator.push(
    context,
    MaterialPageRoute(builder: (_) => settings.SettingsScreen()),
  );
}
```

## 🎯 Mejores Prácticas

### 1. Profiling con DevTools

```bash
# Abrir Flutter DevTools
flutter pub global activate devtools
flutter pub global run devtools

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Ejecutar app en profile mode
cd mobile
flutter run --profile
cd ..

# Performance overlay en código
void main() {
  runApp(MyApp());

  if (kProfileMode) {
    WidgetsApp.debugShowWidgetInspector = true;
  }
}
```

### 2. Build Mode Correcto

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Debug (desarrollo) - Sin optimizaciones
cd mobile
flutter run
cd ..

# Profile (testing performance) - Optimizado pero con DevTools
cd mobile
flutter run --profile
cd ..

# Release (producción) - Totalmente optimizado
cd mobile
flutter run --release
cd ..
```

### 3. Avoid Doing Work in Build

```dart
// ❌ BAD
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Cálculos pesados aquí
    final expensiveData = _performExpensiveCalculation();
    return Text(expensiveData);
  }
}

// ✅ GOOD
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late String _cachedData;

  @override
  void initState() {
    super.initState();
    _cachedData = _performExpensiveCalculation();
  }

  @override
  Widget build(BuildContext context) {
    return Text(_cachedData);
  }
}
```

### 4. Dispose Correctly

```dart
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late AnimationController _controller;
  late StreamSubscription _subscription;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);
    _subscription = someStream.listen((_) {});
  }

  @override
  void dispose() {
    _controller.dispose();  // ✅ Siempre dispose
    _subscription.cancel(); // ✅ Siempre cancel
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
```

## 📊 Performance Checklist

- [ ] Usar `const` constructors donde sea posible
- [ ] ListView.builder en lugar de ListView con children
- [ ] RepaintBoundary para widgets que se repintan frecuentemente
- [ ] Imágenes optimizadas y cacheadas
- [ ] Dispose de controllers, streams y subscriptions
- [ ] Lazy loading de tabs con AutomaticKeepAliveClientMixin
- [ ] Keys apropiadas en listas
- [ ] Evitar funciones anónimas en build()
- [ ] Code splitting con deferred loading
- [ ] Profiling regular con DevTools

## 📚 Recursos Adicionales

- [Flutter Performance Best Practices](https://docs.flutter.dev/perf/best-practices)
- [Flutter DevTools](https://docs.flutter.dev/development/tools/devtools/overview)
- [Performance Profiling](https://docs.flutter.dev/perf/rendering/ui-performance)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md)
- [Testing Strategy](../testing/SKILL.md)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
