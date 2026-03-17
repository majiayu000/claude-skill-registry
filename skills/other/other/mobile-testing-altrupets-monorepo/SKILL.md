# 📱 Skill: Mobile Testing y Debugging con Flutter MCP

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-mobile-testing` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.2.0 |
| **Keywords** | `mobile-testing`, `integration-test`, `flutter-mcp`, `dart-mcp`, `debugging`, `logic-analysis`, `widget-inspection`, `device-testing` |
| **Referencia** | [Dart and Flutter MCP server](https://docs.flutter.dev/ai/mcp-server) \| [Mobile MCP](https://github.com/mobile-next/mobile-mcp) |

## 🔑 Keywords para Invocación

- `mobile-testing`
- `integration-test-mobile`
- `flutter-mcp`
- `dart-mcp`
- `mobile-mcp`
- `mobile-automation`
- `ui-testing-mobile`
- `device-testing`
- `simulator-testing`
- `emulator-testing`
- `@skill:mobile-testing`

### Ejemplos de Prompts

```
Crea pruebas de integración móvil usando mobile-mcp para validar el flujo de login
```

```
Automatiza pruebas en iOS simulator para la feature de productos
```

```
@skill:mobile-testing - Prueba el flujo completo de checkout en Android emulator
```

Mobile Testing proporciona herramientas para la automatización de pruebas de integración y debugging avanzado usando el servidor oficial de **Dart and Flutter MCP** y el servidor de [Mobile Next](https://github.com/mobile-next/mobile-mcp). Permite no solo ejecutar pruebas en dispositivos reales y simuladores, sino también inspeccionar el árbol de widgets en tiempo real, analizar errores de layout (como el RenderFlex overflow) y gestionar dependencias de forma inteligente.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- Pruebas de integración end-to-end en dispositivos móviles
- Validación de flujos de usuario completos
- Testing de UI automatizado
- Pruebas en múltiples dispositivos/simuladores
- Validación de workflows complejos
- Testing de integración con servicios externos
- Verificación de comportamiento en iOS y Android

### ❌ Cuándo NO Usar Este Skill

- Unit tests (usa el skill de testing estándar)
- Widget tests aislados
- Pruebas que no requieren interacción con dispositivos
- Testing de lógica de negocio pura

## 🏗️ Estructura del Proyecto

```
lib/
├── integration_test/
│   ├── mobile/
│   │   ├── test_flows/
│   │   │   ├── auth_flow_test.dart
│   │   │   ├── checkout_flow_test.dart
│   │   │   └── product_browse_test.dart
│   │   ├── helpers/
│   │   │   ├── mobile_test_helper.dart
│   │   │   └── assertions_helper.dart
│   │   └── config/
│   │       └── mobile_test_config.dart
│   └── app_test.dart
│
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Testing
  integration_test:
    sdk: flutter
  flutter_test:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
```

## ⚙️ Configuración Inicial

### 1. Prerequisitos

**Para iOS (macOS/Linux):**
- Xcode command line tools
- iOS Simulator disponible

**Para Android:**
- Android SDK configurado (ANDROID_HOME o ANDROID_SDK_ROOT)
- Android Platform Tools (adb) en PATH
- AVD (Android Virtual Device) creado y configurado
- Opcional: Android Studio para gestionar AVDs fácilmente

**General:**
- Node.js v22+
- MCP server configurado (ver `mcp.json`)

### 2. Configuración del MCP Server

Es altamente recomendado configurar el servidor oficial de Flutter para debugging profundo, además de `mobile-mcp` para interacciones de bajo nivel:

#### Configuración de Dart/Flutter MCP (Recomendado para Debugging)
```json
{
  "mcpServers": {
    "dart-mcp-server": {
      "command": "dart",
      "args": ["mcp-server"],
      "env": {}
    }
  }
}
```

#### Configuración de Mobile MCP (Para Interacción con Hardware/SO)
```json
{
  "mcpServers": {
    "mobile-mcp": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@latest"],
      "env": {}
    }
  }
}
```

### 2.1. Crear y Configurar AVD (Android Virtual Device)

**Usando Android Studio (Recomendado):**
1. Abre Android Studio
2. Ve a "Tools" > "Device Manager" o "AVD Manager"
3. Haz clic en "Create Virtual Device"
4. Selecciona un dispositivo (ej: Pixel 5)
5. Selecciona una imagen de sistema (Android 11+ recomendado)
6. Configura opciones avanzadas si es necesario
7. Finaliza la creación

**Usando línea de comandos:**
```bash
# Listar imágenes de sistema disponibles
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --list | grep "system-images"

# Crear AVD usando avdmanager
$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager create avd \
  -n Pixel_5_API_33 \
  -k "system-images;android-33;google_apis;x86_64" \
  -d "pixel_5"

# Listar AVDs creados
$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager list avd
```

**Verificar configuración:**
```bash
# Verificar que Flutter detecta el emulador
flutter devices

# Si el emulador no aparece, verifica:
# 1. ANDROID_HOME está configurado correctamente
# 2. El emulador está en PATH o usa la ruta completa
# 3. El AVD está creado correctamente
```

**Validación automática de configuración:**

Usa los scripts de validación incluidos para verificar que todo esté correctamente configurado:

**Linux:**
```bash
# Desde la raíz del proyecto
chmod +x skills/flutter/mobile-testing/scripts/validate_android_setup_linux.sh
./skills/flutter/mobile-testing/scripts/validate_android_setup_linux.sh
```

**macOS:**
```bash
# Desde la raíz del proyecto
chmod +x skills/flutter/mobile-testing/scripts/validate_android_setup_macos.sh
./skills/flutter/mobile-testing/scripts/validate_android_setup_macos.sh
```

**Windows (PowerShell):**
```powershell
# Desde la raíz del proyecto
.\skills\flutter\mobile-testing\scripts\validate_android_setup.ps1
```

Los scripts verifican:
- ✅ Variables de entorno `ANDROID_HOME` o `ANDROID_SDK_ROOT`
- ✅ `adb` disponible en PATH
- ✅ `emulator` disponible en PATH
- ✅ `avdmanager` disponible
- ✅ AVDs creados y disponibles
- ✅ Dispositivos conectados

Ver [README de scripts](./scripts/README.md) para más detalles.

### 3. Configuración de Dispositivos

**iOS Simulator:**
```bash
# Listar simuladores disponibles
xcrun simctl list

# Iniciar un simulador específico
xcrun simctl boot "iPhone 16"

# Listar dispositivos disponibles con Flutter
flutter devices
```

**Android Emulator (AVD):**
```bash
# Opción 1: Usar Flutter para listar dispositivos (recomendado)
flutter devices

# Opción 2: Listar AVDs disponibles desde Android SDK
# Asegúrate de tener ANDROID_HOME configurado
$ANDROID_HOME/emulator/emulator -list-avds

# O si tienes emulator en PATH:
emulator -list-avds

# Iniciar un emulador específico desde Android SDK
$ANDROID_HOME/emulator/emulator -avd Pixel_5_API_33 &

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# O usando Flutter (inicia automáticamente si no está corriendo)
cd mobile
flutter run -d emulator-5554
cd ..
```

**Nota:** Flutter puede iniciar automáticamente el emulador si no está corriendo cuando ejecutas `flutter run`. Para crear nuevos AVDs, usa Android Studio > Device Manager o el comando `avdmanager`.

## 💻 Implementación

### 1. Helper para Mobile Testing

```dart
// lib/integration_test/mobile/helpers/mobile_test_helper.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

/// Helper para interactuar con dispositivos móviles vía MCP
class MobileTestHelper {
  final IntegrationTestWidgetsFlutterBinding binding;

  MobileTestHelper(this.binding);

  /// Espera a que un widget esté visible
  Future<void> waitForWidget(WidgetTester tester, Finder finder, {
    Duration timeout = const Duration(seconds: 30),
  }) async {
    await tester.pumpAndSettle();
    expect(finder, findsOneWidget, reason: 'Widget not found');
  }

  /// Toca un widget específico
  Future<void> tapWidget(WidgetTester tester, Finder finder) async {
    await waitForWidget(tester, finder);
    await tester.tap(finder);
    await tester.pumpAndSettle();
  }

  /// Escribe texto en un campo
  Future<void> enterText(WidgetTester tester, Finder finder, String text) async {
    await waitForWidget(tester, finder);
    await tester.enterText(finder, text);
    await tester.pumpAndSettle();
  }

  /// Desliza hacia abajo
  Future<void> scrollDown(WidgetTester tester, Finder finder) async {
    await tester.drag(finder, const Offset(0, -300));
    await tester.pumpAndSettle();
  }

  /// Desliza hacia arriba
  Future<void> scrollUp(WidgetTester tester, Finder finder) async {
    await tester.drag(finder, const Offset(0, 300));
    await tester.pumpAndSettle();
  }

  /// Espera un tiempo específico
  Future<void> wait(Duration duration) async {
    await Future.delayed(duration);
  }

  /// Toma un screenshot (requiere configuración adicional)
  Future<void> takeScreenshot(String name) async {
    // Implementación depende de la configuración de screenshots
    await binding.convertFlutterSurfaceToImage();
    await binding.takeScreenshot(name);
  }
}
```

### 2. Flujo de Autenticación

```dart
// lib/integration_test/mobile/test_flows/auth_flow_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import '../helpers/mobile_test_helper.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Authentication Flow', () {
    late MobileTestHelper helper;
    late WidgetTester tester;

    setUpAll(() async {
      final binding = IntegrationTestWidgetsFlutterBinding.instance;
      helper = MobileTestHelper(binding);
    });

    testWidgets('Login completo con email y password', (WidgetTester testTester) async {
      tester = testTester;

      // 1. Iniciar la app
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // 2. Navegar a la pantalla de login
      final loginButton = find.text('Login');
      await helper.tapWidget(tester, loginButton);
      await helper.wait(const Duration(seconds: 1));

      // 3. Ingresar email
      final emailField = find.byKey(const Key('email_field'));
      await helper.enterText(tester, emailField, 'test@example.com');
      await helper.wait(const Duration(milliseconds: 500));

      // 4. Ingresar password
      final passwordField = find.byKey(const Key('password_field'));
      await helper.enterText(tester, passwordField, 'password123');
      await helper.wait(const Duration(milliseconds: 500));

      // 5. Presionar botón de login
      final submitButton = find.byKey(const Key('login_button'));
      await helper.tapWidget(tester, submitButton);
      await helper.wait(const Duration(seconds: 2));

      // 6. Verificar que se navegó a la pantalla principal
      expect(find.text('Welcome'), findsOneWidget);
      expect(find.text('test@example.com'), findsOneWidget);
    });

    testWidgets('Login con Google Sign-In', (WidgetTester testTester) async {
      tester = testTester;

      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Navegar a login
      await helper.tapWidget(tester, find.text('Login'));

      // Presionar botón de Google Sign-In
      final googleButton = find.byKey(const Key('google_sign_in_button'));
      await helper.tapWidget(tester, googleButton);
      await helper.wait(const Duration(seconds: 3));

      // Verificar login exitoso
      expect(find.text('Welcome'), findsOneWidget);
    });

    testWidgets('Recuperación de contraseña', (WidgetTester testTester) async {
      tester = testTester;

      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Ir a login
      await helper.tapWidget(tester, find.text('Login'));

      // Presionar "Forgot Password"
      final forgotPasswordLink = find.text('Forgot Password?');
      await helper.tapWidget(tester, forgotPasswordLink);
      await helper.wait(const Duration(seconds: 1));

      // Ingresar email
      final emailField = find.byKey(const Key('reset_email_field'));
      await helper.enterText(tester, emailField, 'test@example.com');

      // Enviar
      final sendButton = find.byKey(const Key('send_reset_button'));
      await helper.tapWidget(tester, sendButton);
      await helper.wait(const Duration(seconds: 2));

      // Verificar mensaje de confirmación
      expect(find.text('Password reset email sent'), findsOneWidget);
    });
  });
}
```

### 3. Flujo de Checkout

```dart
// lib/integration_test/mobile/test_flows/checkout_flow_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import '../helpers/mobile_test_helper.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Checkout Flow', () {
    late MobileTestHelper helper;

    setUpAll(() {
      final binding = IntegrationTestWidgetsFlutterBinding.instance;
      helper = MobileTestHelper(binding);
    });

    testWidgets('Flujo completo de compra', (WidgetTester tester) async {
      // 1. Login (asumiendo que ya existe)
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // 2. Buscar producto
      final searchField = find.byKey(const Key('search_field'));
      await helper.enterText(tester, searchField, 'laptop');
      await helper.wait(const Duration(seconds: 1));

      // 3. Seleccionar primer resultado
      final firstProduct = find.byKey(const Key('product_item_0'));
      await helper.tapWidget(tester, firstProduct);
      await helper.wait(const Duration(seconds: 1));

      // 4. Agregar al carrito
      final addToCartButton = find.byKey(const Key('add_to_cart_button'));
      await helper.tapWidget(tester, addToCartButton);
      await helper.wait(const Duration(seconds: 1));

      // 5. Ir al carrito
      final cartIcon = find.byIcon(Icons.shopping_cart);
      await helper.tapWidget(tester, cartIcon);
      await helper.wait(const Duration(seconds: 1));

      // 6. Proceder al checkout
      final checkoutButton = find.text('Checkout');
      await helper.tapWidget(tester, checkoutButton);
      await helper.wait(const Duration(seconds: 1));

      // 7. Completar información de envío
      final addressField = find.byKey(const Key('address_field'));
      await helper.enterText(tester, addressField, '123 Main St');

      final cityField = find.byKey(const Key('city_field'));
      await helper.enterText(tester, cityField, 'New York');

      // 8. Seleccionar método de pago
      final paymentMethod = find.text('Credit Card');
      await helper.tapWidget(tester, paymentMethod);
      await helper.wait(const Duration(seconds: 1));

      // 9. Confirmar compra
      final confirmButton = find.text('Confirm Purchase');
      await helper.tapWidget(tester, confirmButton);
      await helper.wait(const Duration(seconds: 2));

      // 10. Verificar confirmación
      expect(find.text('Order Confirmed'), findsOneWidget);
      expect(find.text('Thank you for your purchase'), findsOneWidget);
    });

    testWidgets('Validar carrito vacío', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Ir al carrito sin productos
      final cartIcon = find.byIcon(Icons.shopping_cart);
      await helper.tapWidget(tester, cartIcon);
      await helper.wait(const Duration(seconds: 1));

      // Verificar mensaje de carrito vacío
      expect(find.text('Your cart is empty'), findsOneWidget);
      expect(find.text('Start shopping'), findsOneWidget);
    });
  });
}
```

### 4. Flujo de Navegación de Productos

```dart
// lib/integration_test/mobile/test_flows/product_browse_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import '../helpers/mobile_test_helper.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Product Browsing', () {
    late MobileTestHelper helper;

    setUpAll(() {
      final binding = IntegrationTestWidgetsFlutterBinding.instance;
      helper = MobileTestHelper(binding);
    });

    testWidgets('Navegar por categorías y productos', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // 1. Seleccionar categoría
      final electronicsCategory = find.text('Electronics');
      await helper.tapWidget(tester, electronicsCategory);
      await helper.wait(const Duration(seconds: 1));

      // 2. Scroll para ver más productos
      final productList = find.byKey(const Key('product_list'));
      await helper.scrollDown(tester, productList);
      await helper.wait(const Duration(seconds: 1));

      // 3. Seleccionar un producto
      final productCard = find.byKey(const Key('product_card_2'));
      await helper.tapWidget(tester, productCard);
      await helper.wait(const Duration(seconds: 1));

      // 4. Verificar detalles del producto
      expect(find.text('Product Details'), findsOneWidget);
      expect(find.byKey(const Key('product_image')), findsOneWidget);
      expect(find.byKey(const Key('product_price')), findsOneWidget);

      // 5. Volver atrás
      final backButton = find.byIcon(Icons.arrow_back);
      await helper.tapWidget(tester, backButton);
      await helper.wait(const Duration(seconds: 1));

      // 6. Verificar que volvió a la lista
      expect(find.byKey(const Key('product_list')), findsOneWidget);
    });

    testWidgets('Filtrar y ordenar productos', (WidgetTester tester) async {
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // 1. Abrir filtros
      final filterButton = find.byKey(const Key('filter_button'));
      await helper.tapWidget(tester, filterButton);
      await helper.wait(const Duration(seconds: 1));

      // 2. Aplicar filtro de precio
      final priceFilter = find.text('Price: \$0 - \$100');
      await helper.tapWidget(tester, priceFilter);
      await helper.wait(const Duration(seconds: 1));

      // 3. Aplicar filtro
      final applyButton = find.text('Apply');
      await helper.tapWidget(tester, applyButton);
      await helper.wait(const Duration(seconds: 2));

      // 4. Verificar que los productos se filtraron
      final productList = find.byKey(const Key('product_list'));
      expect(productList, findsOneWidget);

      // 5. Ordenar por precio
      final sortButton = find.byKey(const Key('sort_button'));
      await helper.tapWidget(tester, sortButton);
      await helper.wait(const Duration(seconds: 1));

      final sortByPrice = find.text('Price: Low to High');
      await helper.tapWidget(tester, sortByPrice);
      await helper.wait(const Duration(seconds: 2));

      // 6. Verificar ordenamiento
      expect(find.byKey(const Key('product_list')), findsOneWidget);
    });
  });
}
```

### 5. Configuración de Tests

```dart
// lib/integration_test/mobile/config/mobile_test_config.dart
class MobileTestConfig {
  // Timeouts
  static const Duration defaultTimeout = Duration(seconds: 30);
  static const Duration shortTimeout = Duration(seconds: 5);
  static const Duration longTimeout = Duration(seconds: 60);

  // Delays entre acciones
  static const Duration defaultDelay = Duration(milliseconds: 500);
  static const Duration shortDelay = Duration(milliseconds: 200);
  static const Duration longDelay = Duration(seconds: 2);

  // Configuración de dispositivos
  static const Map<String, dynamic> deviceConfig = {
    'ios': {
      'simulator': 'iPhone 16',
      'os_version': '18.0',
    },
    'android': {
      'emulator': 'Pixel_5_API_33',
      'api_level': 33,
    },
  };

  // Screenshots
  static const bool enableScreenshots = true;
  static const String screenshotPath = 'test/screenshots';
}
```

## 🎯 Mejores Prácticas

### 1. Estructura de Tests

- **Organiza por flujos de usuario**: Cada archivo de test debe representar un flujo completo
- **Usa grupos lógicos**: Agrupa tests relacionados con `group()`
- **Nombres descriptivos**: Los nombres de test deben describir el comportamiento esperado

### 2. Esperas y Timeouts

```dart
// ✅ Bueno: Esperas explícitas con timeouts
await helper.waitForWidget(tester, finder, timeout: Duration(seconds: 30));

// ❌ Malo: Esperas fijas sin validación
await Future.delayed(Duration(seconds: 5));
```

### 3. Assertions

```dart
// ✅ Bueno: Assertions específicas con mensajes
expect(find.text('Welcome'), findsOneWidget,
  reason: 'User should see welcome message after login');

// ❌ Malo: Assertions genéricas
expect(something, isNotNull);
```

### 4. Manejo de Errores

```dart
testWidgets('Test con manejo de errores', (tester) async {
  try {
    await helper.tapWidget(tester, finder);
  } catch (e) {
    // Tomar screenshot en caso de error
    await helper.takeScreenshot('error_${DateTime.now().millisecondsSinceEpoch}');
    rethrow;
  }
});
```

### 5. Screenshots para Debugging

```dart
// Tomar screenshots en puntos clave
await helper.takeScreenshot('after_login');
await helper.takeScreenshot('before_checkout');
await helper.takeScreenshot('after_purchase');
```

### 6. Tests Independientes

```dart
// ✅ Bueno: Cada test es independiente
testWidgets('Test 1', (tester) async {
  // Setup completo
});

testWidgets('Test 2', (tester) async {
  // Setup completo (no depende de Test 1)
});

// ❌ Malo: Tests dependen unos de otros
testWidgets('Test 1', (tester) async {
  // Crea estado
});

testWidgets('Test 2', (tester) async {
  // Asume que Test 1 ya corrió
});
```

## 🚀 Ejecución de Tests

### Comando Básico

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Ejecutar todos los tests de integración
cd mobile
flutter test integration_test/
cd ..

# Ejecutar un test específico
cd mobile
flutter test integration_test/mobile/test_flows/auth_flow_test.dart
cd ..
```

### Con Dispositivo Específico

**iOS Simulator:**
```bash
# Listar dispositivos disponibles
flutter devices

# Iniciar simulador (si no está corriendo)
xcrun simctl boot "iPhone 16"

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Ejecutar tests en simulador específico
cd mobile
flutter test integration_test/ --device-id=<device-id>
cd ..
# Ejemplo: flutter test integration_test/ --device-id=00008030-001A4D1234567890
```

**Android Emulator (AVD):**
```bash
# Listar dispositivos disponibles (incluye emuladores)
flutter devices

# Opción 1: Iniciar emulador manualmente y luego ejecutar tests
# Iniciar emulador desde Android SDK
$ANDROID_HOME/emulator/emulator -avd Pixel_5_API_33 &

# Esperar a que el emulador esté listo (verificar con flutter devices)
flutter devices

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Ejecutar tests en el emulador
cd mobile
flutter test integration_test/ --device-id=emulator-5554
cd ..

# Opción 2: Flutter iniciará el emulador automáticamente si está configurado
# Primero verifica que el AVD existe:
$ANDROID_HOME/emulator/emulator -list-avds

# Luego ejecuta los tests (Flutter iniciará el emulador si no está corriendo)
cd mobile
flutter test integration_test/ --device-id=emulator-5554
cd ..
```

**Verificar dispositivos conectados:**
```bash
# Ver todos los dispositivos disponibles (reales, simuladores y emuladores)
flutter devices

# Salida de ejemplo:
# 2 connected devices:
# iPhone 16 (mobile) • 00008030-001A4D1234567890 • ios • com.apple.CoreSimulator.SimRuntime.iOS-18-0
# emulator-5554 (mobile) • emulator-5554 • android-x86 • Android 13 (API 33) (emulator)
```

### Con Screenshots

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Habilitar screenshots
cd mobile
flutter test integration_test/ --screenshots
cd ..
```

## 📚 Recursos Adicionales

- [Mobile MCP GitHub](https://github.com/mobile-next/mobile-mcp)
- [Flutter Integration Testing](https://docs.flutter.dev/testing/integration-tests)
- [Mobile MCP Wiki](https://github.com/mobile-next/mobile-mcp/wiki)

## 🔗 Skills Relacionados

- [Testing Strategy](../testing/SKILL.md) - Para unit y widget tests
- [Firebase](../firebase/SKILL.md) - Para testing de integración con Firebase
- [Clean Architecture](../clean-architecture/SKILL.md) - Para estructura de tests

## 💡 Ejemplos de Uso con MCP

El servidor Mobile MCP permite automatizar interacciones complejas. Aquí hay ejemplos de prompts que puedes usar con tu asistente de IA:

### Ejemplo 1: Validar Flujo de Login

```
Usa mobile-mcp para automatizar el siguiente flujo:
1. Abrir la app Flutter
2. Navegar a la pantalla de login
3. Ingresar email "test@example.com"
4. Ingresar password "password123"
5. Presionar botón de login
6. Verificar que se muestra la pantalla de bienvenida
7. Tomar screenshot del resultado
```

### Ejemplo 2: Probar Checkout Completo

```
Automatiza el flujo de checkout:
1. Login con credenciales de prueba
2. Buscar producto "laptop"
3. Agregar al carrito
4. Ir al carrito
5. Proceder al checkout
6. Completar información de envío
7. Seleccionar método de pago
8. Confirmar compra
9. Verificar mensaje de confirmación
```

### Ejemplo 3: Testing Multi-Dispositivo

```
Ejecuta los tests de integración en:
- iOS Simulator (iPhone 16)
- Android Emulator (Pixel 5)
Compara los resultados y genera un reporte
```

---

**Versión:** 1.0.0
**Última actualización:** Febrero 2026

---

## 📝 Logging de HTTP Requests

El proyecto incluye un `LoggingInterceptor` que guarda logs de todas las peticiones HTTP a archivo.

### Configuración

**En `Environment`:**

```dart
// lib/core/config/environment_manager.dart

static const development = Environment(
  name: 'development',
  apiBaseUrl: 'http://localhost:3000',
  requestTimeoutSeconds: 30,
  enableLogging: true,
  logsPath: '/home/kvttvrsis/Documentos/GitHub/altrupets-monorepo/logs/mobile',
);
```

### Ubicación de Logs

Por defecto se guardan en: `logs/mobile/http_logs_<timestamp>.log`

### Ver Logs en Tiempo Real

```bash
tail -f logs/mobile/http_logs_$(ls -t logs/mobile/ | head -1)
```
