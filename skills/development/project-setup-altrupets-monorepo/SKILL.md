---
name: project-setup
description: '| ID | flutter-project-setup |'
---

# ⚙️ Skill: Project Setup

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-project-setup` |
| **Nivel** | 🟢 Básico |
| **Versión** | 1.0.0 |
| **Keywords** | `setup`, `init`, `scaffold`, `config`, `initialization` |

## 🔑 Keywords para Invocación

- `setup`
- `init`
- `scaffold`
- `config`
- `initialization`
- `@skill:flutter-project-setup`

### Ejemplos de Prompts

```
Crea el setup inicial para un proyecto Flutter
```

```
Necesito scaffold básico con configuración estándar
```

```
@skill:project-setup - Configura proyecto con flavors y análisis estático
```

## 📖 Descripción

Configuración estándar para cualquier proyecto Flutter con mejores prácticas, incluyendo análisis estático, flavors, temas, y estructura básica.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

## 🚀 Scripts de Inicialización Automática

Este skill incluye scripts automatizados para inicializar un proyecto Flutter en una estructura de monorepo:

### 1. Setup del Proyecto

#### Windows (PowerShell)

```powershell
.\skills\flutter\project-setup\scripts\setup.ps1
```

#### Linux/macOS (Bash)

```bash
chmod +x skills/flutter/project-setup/scripts/setup.sh
./skills/flutter/project-setup/scripts/setup.sh
```

Los scripts de setup realizan automáticamente:
1. ✅ Verificación de instalación de Flutter
2. ✅ Creación de estructura de monorepo (`backend/` y `mobile/`)
3. ✅ Inicialización del proyecto Flutter en `mobile/`
4. ✅ Instalación de dependencias
5. ✅ Creación de archivos de configuración básicos (`.env-sample`, `.gitignore`)
6. ✅ Generación de README para el proyecto mobile

**Nota:** Los scripts están diseñados para ejecutarse desde la raíz del proyecto monorepo.

### 2. Creación de Symlinks para Herramientas de IA

Para que los skills agénticos estén disponibles en diferentes herramientas de IA (Cursor, Kiro, Claude, Gemini, OpenAI Codex), puedes crear symlinks automáticamente:

#### Windows (PowerShell - Requiere permisos de administrador)

```powershell
.\skills\flutter\project-setup\scripts\create-symlinks.ps1
```

#### Linux/macOS (Bash)

```bash
chmod +x skills/flutter/project-setup/scripts/create-symlinks.sh
./skills/flutter/project-setup/scripts/create-symlinks.sh
```

Los scripts de symlinks crean enlaces simbólicos desde `skills/` hacia:
- **Cursor Rules:** `.cursor/rules/skills`
- **Kiro Steering:** `.kilocode/rules/skills`
- **Claude Skills:** `.claude/skills/*` (un symlink por skill)
- **Gemini Extensions:** `~/.gemini/extensions/flutter-agent-skills`
- **OpenAI Codex:** `codex/skills/*` (un symlink por skill)

**Nota:** En Windows, este script requiere ejecutarse como administrador debido a las restricciones de creación de symlinks.

### ✅ Cuándo Usar Este Skill

- Al iniciar cualquier nuevo proyecto Flutter
- Necesitas configuración estándar y profesional
- Quieres evitar configuraciones manuales repetitivas
- Deseas seguir mejores prácticas desde el inicio

## 🏗️ Estructura Base

```
lib/
├── config/
│   ├── theme/
│   │   ├── app_theme.dart
│   │   ├── colors.dart
│   │   └── text_styles.dart
│   ├── routes/
│   │   ├── app_router.dart
│   │   └── route_names.dart
│   ├── constants/
│   │   ├── app_constants.dart
│   │   └── api_constants.dart
│   └── env/
│       ├── env_config.dart
│       ├── dev_config.dart
│       ├── staging_config.dart
│       └── prod_config.dart
├── l10n/
│   ├── app_en.arb
│   └── app_es.arb
├── core/
│   ├── utils/
│   └── extensions/
└── main.dart
```

## ⚙️ Configuraciones Incluidas

### 1. Analysis Options

```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
  errors:
    invalid_annotation_target: ignore
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true

linter:
  rules:
    - always_declare_return_types
    - always_put_required_named_parameters_first
    - always_use_package_imports
    - avoid_print
    - avoid_unnecessary_containers
    - avoid_web_libraries_in_flutter
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables
    - prefer_final_fields
    - prefer_single_quotes
    - sort_constructors_first
    - use_build_context_synchronously
```

### 2. Flavors Configuration

```dart
// config/env/env_config.dart
abstract class EnvConfig {
  String get apiBaseUrl;
  String get appName;
  bool get isDevelopment;
}

// config/env/dev_config.dart
class DevConfig implements EnvConfig {
  @override
  String get apiBaseUrl => 'https://dev-api.example.com';

  @override
  String get appName => 'MyApp DEV';

  @override
  bool get isDevelopment => true;
}

// config/env/prod_config.dart
class ProdConfig implements EnvConfig {
  @override
  String get apiBaseUrl => 'https://api.example.com';

  @override
  String get appName => 'MyApp';

  @override
  bool get isDevelopment => false;
}
```

### 3. Theme Configuration

```dart
// config/theme/app_theme.dart
import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        brightness: Brightness.light,
      ),
      textTheme: AppTextStyles.textTheme,
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primary,
        brightness: Brightness.dark,
      ),
      textTheme: AppTextStyles.textTheme,
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
      ),
    );
  }
}
```

### 4. Routing Configuration

```dart
// config/routes/app_router.dart
import 'package:flutter/material.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case RouteNames.home:
        return MaterialPageRoute(
          builder: (_) => const HomePage(),
        );
      case RouteNames.details:
        return MaterialPageRoute(
          builder: (_) => const DetailsPage(),
        );
      default:
        return MaterialPageRoute(
          builder: (_) => const NotFoundPage(),
        );
    }
  }
}
```

### 5. Internacionalización (i18n)

```dart
// l10n/app_en.arb
{
  "@@locale": "en",
  "appTitle": "My Application",
  "welcome": "Welcome",
  "loading": "Loading..."
}

// l10n/app_es.arb
{
  "@@locale": "es",
  "appTitle": "Mi Aplicación",
  "welcome": "Bienvenido",
  "loading": "Cargando..."
}
```

### 6. Main.dart

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'config/theme/app_theme.dart';
import 'config/routes/app_router.dart';
import 'generated/l10n.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      onGenerateRoute: AppRouter.generateRoute,
      localizationsDelegates: const [
        S.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: S.delegate.supportedLocales,
    );
  }
}
```

## 📦 Dependencias Básicas

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: ^0.18.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
```

## ✅ Checklist de Configuración

- [ ] Ejecutar script de inicialización (`setup.ps1` o `setup.sh`)
- [ ] Configurar `analysis_options.yaml`
- [ ] Configurar flavors (dev, staging, production)
- [ ] Configurar internacionalización (i18n)
- [ ] Configurar tema oscuro/claro
- [ ] Configurar navegación
- [ ] Configurar constantes
- [ ] Configurar estructura de carpetas
- [ ] Agregar dependencias básicas

## 📁 Archivos del Skill

Este skill incluye los siguientes archivos:

- `SKILL.md` - Documentación completa del skill
- `scripts/setup.ps1` - Script de inicialización para Windows (PowerShell)
- `scripts/setup.sh` - Script de inicialización para Linux/macOS (Bash)
- `scripts/create-symlinks.ps1` - Script para crear symlinks en Windows (PowerShell, requiere admin)
- `scripts/create-symlinks.sh` - Script para crear symlinks en Linux/macOS (Bash)

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.0
