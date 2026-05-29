# 🌍 Skill: Internacionalización (i18n)

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-i18n` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `i18n`, `l10n`, `internationalization`, `localization`, `translations` |
| **Referencia** | [Flutter Intl Documentation](https://docs.flutter.dev/development/accessibility-and-localization/internationalization) |

## 🔑 Keywords para Invocación

- `i18n`
- `l10n`
- `internationalization`
- `localization`
- `translations`
- `multi-language`
- `@skill:i18n`

### Ejemplos de Prompts

```
Agrega soporte para múltiples idiomas usando i18n
```

```
Implementa internacionalización con español e inglés
```

```
@skill:i18n - Configura traducciones para la app
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

Internacionalización (i18n) y Localización (l10n) permiten que tu app soporte múltiples idiomas y regiones. Este skill cubre el uso de `flutter_localizations` con ARB files, cambio dinámico de idioma, formateo de fechas/números, y plurales.

### ✅ Cuándo Usar Este Skill

- App dirigida a múltiples países
- Necesitas soportar varios idiomas
- Requieres formateo regional (fechas, monedas)
- Quieres alcance internacional
- Cumplimiento de requisitos de mercado global

### ❌ Cuándo NO Usar Este Skill

- App solo para un mercado/idioma específico
- Prototipo sin planes de expansión

## 🏗️ Estructura del Proyecto

```
lib/
├── l10n/
│   ├── app_en.arb          # Inglés (base)
│   ├── app_es.arb          # Español
│   ├── app_fr.arb          # Francés
│   ├── app_de.arb          # Alemán
│   └── app_pt.arb          # Portugués
│
├── core/
│   ├── localization/
│   │   ├── locale_provider.dart
│   │   └── supported_locales.dart
│   └── utils/
│       ├── date_formatters.dart
│       └── currency_formatters.dart
│
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  flutter_localizations:
    sdk: flutter

  # intl está incluido automáticamente con flutter_localizations
  # No es necesario especificarlo manualmente, Flutter lo pinnea automáticamente

  # State management para cambio de idioma (opcional)
  flutter_bloc: ^8.1.3
  # O
  riverpod: ^2.4.9
  # O
  shared_preferences: ^2.2.2  # Para persistir preferencia de idioma
```

### Configuración en mobile/pubspec.yaml

```yaml
flutter:
  generate: true  # Habilita generación automática
  uses-material-design: true
```

### l10n.yaml

**⚠️ IMPORTANTE:** Este archivo debe estar en la raíz del proyecto Flutter (`mobile/l10n.yaml`), no en `lib/`.

```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
nullable-getter: false
synthetic-package: false
output-class: AppLocalizations
```

**Nota:** Cuando usas `l10n.yaml` con `arb-dir: lib/l10n`, los archivos generados se crean directamente en `lib/l10n/app_localizations.dart`, **NO** en `flutter_gen/gen_l10n/`. El import correcto es:

```dart
import 'package:tu_app/l10n/app_localizations.dart';
// O si estás en lib/:
import 'l10n/app_localizations.dart';
```

## 💻 Implementación

### 0. Generar Archivos de Localización

Después de crear los archivos ARB y configurar `l10n.yaml`, ejecuta:

**Windows (PowerShell):**
```powershell
# Desde la raíz del proyecto (donde está mobile/)
Push-Location mobile; flutter gen-l10n; Pop-Location
```

**Linux/macOS (Bash):**
```bash
# Desde la raíz del proyecto (donde está mobile/)
cd mobile && flutter gen-l10n
```

**⚠️ IMPORTANTE:**
- Los archivos generados se crearán en `lib/l10n/app_localizations.dart` (no en `flutter_gen/gen_l10n/`) cuando usas `l10n.yaml` con `arb-dir: lib/l10n`.
- En Windows, usa `Push-Location` y `Pop-Location` en lugar de `cd` para evitar problemas con rutas duplicadas.

### 1. ARB Files (Application Resource Bundle)

#### app_en.arb (Base - Inglés)

```json
{
  "@@locale": "en",

  "appTitle": "My App",
  "@appTitle": {
    "description": "The title of the application"
  },

  "welcome": "Welcome",
  "@welcome": {
    "description": "Welcome message"
  },

  "welcomeMessage": "Welcome, {name}!",
  "@welcomeMessage": {
    "description": "Welcome message with user name",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "John"
      }
    }
  },

  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": {
    "description": "Number of items in cart",
    "placeholders": {
      "count": {
        "type": "int",
        "example": "5"
      }
    }
  },

  "price": "{amount, plural, =0{Free} other{{currency}{amount}}}",
  "@price": {
    "description": "Product price",
    "placeholders": {
      "amount": {
        "type": "double",
        "format": "currency",
        "example": "9.99"
      },
      "currency": {
        "type": "String",
        "example": "$"
      }
    }
  },

  "lastUpdate": "Last updated: {date}",
  "@lastUpdate": {
    "description": "Last update timestamp",
    "placeholders": {
      "date": {
        "type": "DateTime",
        "format": "yMMMd",
        "example": "Jan 1, 2024"
      }
    }
  },

  "login": "Login",
  "logout": "Logout",
  "email": "Email",
  "password": "Password",
  "forgotPassword": "Forgot password?",
  "dontHaveAccount": "Don't have an account?",
  "register": "Register",

  "home": "Home",
  "products": "Products",
  "cart": "Cart",
  "profile": "Profile",

  "addToCart": "Add to Cart",
  "removeFromCart": "Remove from Cart",
  "checkout": "Checkout",
  "total": "Total",

  "errorGeneric": "An error occurred. Please try again.",
  "errorNetwork": "Network error. Check your connection.",
  "errorAuth": "Authentication failed. Please login again.",

  "confirm": "Confirm",
  "cancel": "Cancel",
  "save": "Save",
  "delete": "Delete",
  "edit": "Edit",
  "ok": "OK",

  "loading": "Loading...",
  "noData": "No data available",
  "tryAgain": "Try Again"
}
```

#### app_es.arb (Español)

```json
{
  "@@locale": "es",

  "appTitle": "Mi Aplicación",
  "welcome": "Bienvenido",
  "welcomeMessage": "¡Bienvenido, {name}!",

  "itemCount": "{count, plural, =0{Sin artículos} =1{1 artículo} other{{count} artículos}}",

  "price": "{amount, plural, =0{Gratis} other{{currency}{amount}}}",

  "lastUpdate": "Última actualización: {date}",

  "login": "Iniciar sesión",
  "logout": "Cerrar sesión",
  "email": "Correo electrónico",
  "password": "Contraseña",
  "forgotPassword": "¿Olvidaste tu contraseña?",
  "dontHaveAccount": "¿No tienes cuenta?",
  "register": "Registrarse",

  "home": "Inicio",
  "products": "Productos",
  "cart": "Carrito",
  "profile": "Perfil",

  "addToCart": "Agregar al carrito",
  "removeFromCart": "Quitar del carrito",
  "checkout": "Pagar",
  "total": "Total",

  "errorGeneric": "Ocurrió un error. Por favor intenta de nuevo.",
  "errorNetwork": "Error de red. Verifica tu conexión.",
  "errorAuth": "Autenticación fallida. Por favor inicia sesión de nuevo.",

  "confirm": "Confirmar",
  "cancel": "Cancelar",
  "save": "Guardar",
  "delete": "Eliminar",
  "edit": "Editar",
  "ok": "OK",

  "loading": "Cargando...",
  "noData": "No hay datos disponibles",
  "tryAgain": "Intentar de nuevo"
}
```

### 2. Setup en Main

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:tu_app/l10n/app_localizations.dart';  // Ajusta 'tu_app' al nombre de tu paquete

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'i18n App',

      // Configuración de localización
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],

      // Idiomas soportados
      supportedLocales: AppLocalizations.supportedLocales,
      // O manualmente:
      // supportedLocales: const [
      //   Locale('en', ''), // Inglés
      //   Locale('es', ''), // Español
      //   Locale('fr', ''), // Francés
      //   Locale('de', ''), // Alemán
      //   Locale('pt', ''), // Portugués
      // ],

      // Idioma por defecto
      locale: const Locale('en'),

      // Callback cuando el sistema cambia de idioma
      localeResolutionCallback: (locale, supportedLocales) {
        // Verificar si el idioma del dispositivo está soportado
        for (var supportedLocale in supportedLocales) {
          if (supportedLocale.languageCode == locale?.languageCode) {
            return supportedLocale;
          }
        }
        // Fallback al primer idioma soportado (inglés)
        return supportedLocales.first;
      },

      home: const HomeScreen(),
    );
  }
}
```

### 3. Uso de Traducciones en Widgets

```dart
// lib/features/home/presentation/screens/home_screen.dart
import 'package:flutter/material.dart';
import 'package:tu_app/l10n/app_localizations.dart';  // Ajusta 'tu_app' al nombre de tu paquete

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Obtener instancia de localización
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.appTitle),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Texto simple
            Text(
              l10n.welcome,
              style: Theme.of(context).textTheme.headlineMedium,
            ),

            const SizedBox(height: 16),

            // Texto con parámetro
            Text(
              l10n.welcomeMessage('John'),
              style: Theme.of(context).textTheme.titleLarge,
            ),

            const SizedBox(height: 16),

            // Plural
            Text(l10n.itemCount(0)),  // "No items" / "Sin artículos"
            Text(l10n.itemCount(1)),  // "1 item" / "1 artículo"
            Text(l10n.itemCount(5)),  // "5 items" / "5 artículos"

            const SizedBox(height: 16),

            // Precio con formato
            Text(l10n.price(0, '\$')),      // "Free" / "Gratis"
            Text(l10n.price(9.99, '\$')),   // "$9.99"

            const SizedBox(height: 16),

            // Fecha formateada
            Text(l10n.lastUpdate(DateTime.now())),

            const SizedBox(height: 32),

            // Botones con traducciones
            ElevatedButton(
              onPressed: () {},
              child: Text(l10n.login),
            ),

            const SizedBox(height: 8),

            TextButton(
              onPressed: () {},
              child: Text(l10n.forgotPassword),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: [
          BottomNavigationBarItem(
            icon: const Icon(Icons.home),
            label: l10n.home,
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.shopping_bag),
            label: l10n.products,
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.shopping_cart),
            label: l10n.cart,
          ),
          BottomNavigationBarItem(
            icon: const Icon(Icons.person),
            label: l10n.profile,
          ),
        ],
      ),
    );
  }
}
```

### 4. Cambio Dinámico de Idioma con BLoC

```dart
// lib/core/localization/locale_cubit.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LocaleCubit extends Cubit<Locale> {
  static const String _localeKey = 'app_locale';
  final SharedPreferences prefs;

  LocaleCubit(this.prefs) : super(const Locale('en')) {
    _loadSavedLocale();
  }

  void _loadSavedLocale() {
    final savedLocale = prefs.getString(_localeKey);
    if (savedLocale != null) {
      emit(Locale(savedLocale));
    }
  }

  Future<void> changeLocale(String languageCode) async {
    await prefs.setString(_localeKey, languageCode);
    emit(Locale(languageCode));
  }

  Future<void> clearLocale() async {
    await prefs.remove(_localeKey);
    emit(const Locale('en'));
  }
}
```

```dart
// lib/main.dart (con cambio dinámico)
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:tu_app/l10n/app_localizations.dart';  // Ajusta 'tu_app' al nombre de tu paquete
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final prefs = await SharedPreferences.getInstance();

  runApp(MyApp(prefs: prefs));
}

class MyApp extends StatelessWidget {
  final SharedPreferences prefs;

  const MyApp({super.key, required this.prefs});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => LocaleCubit(prefs),
      child: BlocBuilder<LocaleCubit, Locale>(
        builder: (context, locale) {
          return MaterialApp(
            title: 'i18n App',

            localizationsDelegates: const [
              AppLocalizations.delegate,
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],

            supportedLocales: AppLocalizations.supportedLocales,
            // O manualmente:
            // supportedLocales: const [
            //   Locale('en'),
            //   Locale('es'),
            //   Locale('fr'),
            //   Locale('de'),
            //   Locale('pt'),
            // ],

            locale: locale,  // Idioma actual desde BLoC

            home: const HomeScreen(),
          );
        },
      ),
    );
  }
}
```

### 5. Widget para Cambiar Idioma

```dart
// lib/core/widgets/language_selector.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:tu_app/l10n/app_localizations.dart';  // Ajusta 'tu_app' al nombre de tu paquete
import '../localization/locale_cubit.dart';

class LanguageSelector extends StatelessWidget {
  const LanguageSelector({super.key});

  static const Map<String, String> _languages = {
    'en': '🇺🇸 English',
    'es': '🇪🇸 Español',
    'fr': '🇫🇷 Français',
    'de': '🇩🇪 Deutsch',
    'pt': '🇵🇹 Português',
  };

  @override
  Widget build(BuildContext context) {
    final currentLocale = context.watch<LocaleCubit>().state;

    return PopupMenuButton<String>(
      icon: const Icon(Icons.language),
      tooltip: 'Change Language',
      onSelected: (String languageCode) {
        context.read<LocaleCubit>().changeLocale(languageCode);
      },
      itemBuilder: (BuildContext context) {
        return _languages.entries.map((entry) {
          return PopupMenuItem<String>(
            value: entry.key,
            child: Row(
              children: [
                Text(entry.value),
                if (currentLocale.languageCode == entry.key)
                  const Padding(
                    padding: EdgeInsets.only(left: 8.0),
                    child: Icon(Icons.check, size: 18),
                  ),
              ],
            ),
          );
        }).toList();
      },
    );
  }
}

// Uso en AppBar
AppBar(
  title: Text(l10n.appTitle),
  actions: const [
    LanguageSelector(),
  ],
)
```

### 6. Formateo de Fechas y Números

```dart
// lib/core/utils/formatters.dart
import 'package:intl/intl.dart';
import 'package:flutter/material.dart';

class AppFormatters {
  // Formatear fecha según locale
  static String formatDate(DateTime date, Locale locale) {
    return DateFormat.yMMMd(locale.toString()).format(date);
  }

  static String formatDateShort(DateTime date, Locale locale) {
    return DateFormat.yMd(locale.toString()).format(date);
  }

  static String formatDateLong(DateTime date, Locale locale) {
    return DateFormat.yMMMMEEEEd(locale.toString()).format(date);
  }

  static String formatTime(DateTime time, Locale locale) {
    return DateFormat.jm(locale.toString()).format(time);
  }

  // Formatear moneda según locale
  static String formatCurrency(double amount, Locale locale, String symbol) {
    final format = NumberFormat.currency(
      locale: locale.toString(),
      symbol: symbol,
      decimalDigits: 2,
    );
    return format.format(amount);
  }

  // Formatear número según locale
  static String formatNumber(num number, Locale locale) {
    final format = NumberFormat('#,##0.##', locale.toString());
    return format.format(number);
  }

  // Formatear porcentaje
  static String formatPercentage(double value, Locale locale) {
    final format = NumberFormat.percentPattern(locale.toString());
    return format.format(value);
  }

  // Tiempo relativo (hace 2 horas, etc.)
  static String formatRelativeTime(
    DateTime dateTime,
    AppLocalizations l10n,
  ) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);

    if (difference.inDays > 365) {
      final years = (difference.inDays / 365).floor();
      return '$years ${years == 1 ? "year" : "years"} ago';
    } else if (difference.inDays > 30) {
      final months = (difference.inDays / 30).floor();
      return '$months ${months == 1 ? "month" : "months"} ago';
    } else if (difference.inDays > 0) {
      return '${difference.inDays} ${difference.inDays == 1 ? "day" : "days"} ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours} ${difference.inHours == 1 ? "hour" : "hours"} ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes} ${difference.inMinutes == 1 ? "minute" : "minutes"} ago';
    } else {
      return 'Just now';
    }
  }
}

// Uso
class ProductCard extends StatelessWidget {
  final Product product;

  const ProductCard({required this.product});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final locale = Localizations.localeOf(context);

    return Card(
      child: Column(
        children: [
          Text(product.name),
          Text(
            AppFormatters.formatCurrency(product.price, locale, '\$'),
          ),
          Text(
            AppFormatters.formatDate(product.createdAt, locale),
          ),
        ],
      ),
    );
  }
}
```

## 🎯 Mejores Prácticas

### 1. Organización de Traducciones

✅ **DO:**
```json
{
  "auth_login": "Login",
  "auth_logout": "Logout",
  "auth_register": "Register",

  "products_title": "Products",
  "products_addToCart": "Add to Cart",

  "error_network": "Network error",
  "error_auth": "Authentication error"
}
```

### 2. Usar Descripciones

✅ **DO:**
```json
{
  "welcome": "Welcome",
  "@welcome": {
    "description": "Welcome message shown on home screen"
  }
}
```

### 3. Placeholders Tipados

✅ **DO:**
```json
{
  "price": "Price: {amount}",
  "@price": {
    "placeholders": {
      "amount": {
        "type": "double",
        "format": "currency"
      }
    }
  }
}
```

## ⚠️ Notas Importantes

### Ubicación de Archivos Generados

Cuando usas `l10n.yaml` con la configuración:
```yaml
arb-dir: lib/l10n
output-localization-file: app_localizations.dart
```

Los archivos generados se crean en:
- `lib/l10n/app_localizations.dart`
- `lib/l10n/app_localizations_en.dart`
- `lib/l10n/app_localizations_es.dart`
- etc.

**NO** se crean en `flutter_gen/gen_l10n/` a menos que uses `flutter_gen` como herramienta separada.

### Imports Correctos

```dart
// ✅ CORRECTO - Cuando usas l10n.yaml con arb-dir: lib/l10n
import 'package:tu_app/l10n/app_localizations.dart';

// ❌ INCORRECTO - Solo si usas flutter_gen como herramienta separada
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
```

### Comandos de Generación

```bash
# Desde la raíz del proyecto (donde está mobile/)
cd mobile
flutter gen-l10n

# O desde la raíz usando Push-Location (PowerShell)
Push-Location mobile; flutter gen-l10n; Pop-Location
```

## 📚 Recursos Adicionales

- [Flutter Internationalization](https://docs.flutter.dev/development/accessibility-and-localization/internationalization)
- [Intl Package](https://pub.dev/packages/intl)
- [ARB File Format](https://github.com/google/app-resource-bundle)

## 🔗 Skills Relacionados

- [Theming](../theming/SKILL.md) - Temas adaptados a regiones
- [Project Setup](../project-setup/SKILL.md) - Configuración inicial

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
