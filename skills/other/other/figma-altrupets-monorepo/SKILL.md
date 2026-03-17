# 🎨 Skill: Figma Dev Mode Integration

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `figma-dev-mode` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `figma`, `design`, `assets`, `components`, `dev-mode`, `design-system` |
| **Referencia** | [Figma MCP Server Guide](https://github.com/figma/mcp-server-guide/) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `figma`
- `design`
- `assets`
- `components`
- `dev-mode`
- `design-system`
- `@skill:figma`

### Ejemplos de Prompts

```
Extrae los assets del diseño de Figma
```

```
Implementa este componente según el diseño de Figma
```

```
@skill:figma - Obtén los estilos y colores desde el archivo de diseño
```

## 📖 Descripción

El Figma MCP Server permite a los agentes de IA acceder directamente a archivos de diseño de Figma, extraer assets, componentes, estilos y tokens de diseño. Esto facilita la conversión de diseños a código manteniendo fidelidad absoluta con el diseño original.

### ✅ Cuándo Usar Este Skill

- Necesitas convertir diseños de Figma a código
- Quieres extraer assets (imágenes, SVGs, iconos)
- Deseas implementar un design system desde Figma
- Necesitas mantener sincronización entre diseño y código
- Trabajas en un equipo con diseñadores que usan Figma

### ❌ Cuándo NO Usar Este Skill

- No tienes acceso a archivos de Figma
- Los diseños no están en Figma
- El proyecto no requiere fidelidad exacta con diseños

## 🏗️ Configuración del Figma MCP Server

### Prerrequisitos

- Cuenta de Figma con acceso al archivo de diseño
- Token de acceso personal de Figma
- Cliente MCP compatible (Cursor, Claude Code, etc.)

### Instalación

#### 1. Obtener Token de Figma

1. Ve a tu cuenta de Figma → Settings
2. Ve a **Personal Access Tokens**
3. Genera un nuevo token con permisos de lectura
4. Guarda el token de forma segura

#### 2. Configurar MCP Server

El Figma MCP Server ya está configurado en el archivo `mcp.json` del proyecto.

**⚠️ Importante:** Debes configurar tu token de Figma como variable de entorno:

```bash
# Linux/Mac - Agrega a ~/.bashrc o ~/.zshrc
export FIGMA_TOKEN="tu-token-personal-de-figma"

# Windows - PowerShell
$env:FIGMA_TOKEN="tu-token-aqui"

# Windows - Permanente
[Environment]::SetEnvironmentVariable("FIGMA_TOKEN", "tu-token", "User")
```

**Configuración por IDE:**

El proyecto usa un único archivo `mcp.json` en la raíz. Para configurar tu IDE específico:

👉 **Ver [`../../docs/MCP_SETUP.md`](../../docs/MCP_SETUP.md)** para instrucciones detalladas de:
- Cursor (ya configurado)
- Cline, Windsurf, Gemini CLI, Firebase Studio, etc.

#### 3. Verificar Instalación

Reinicia tu cliente MCP y verifica que el servidor está activo:

- **Cursor:** Abre el chat y pregunta "¿Está activo el servidor MCP de Figma?"
- **Claude Code:** Usa el comando para listar servidores MCP

## 🎯 Capacidades del Figma MCP Server

### 1. Extracción de Assets

El servidor puede servir imágenes y SVGs directamente desde Figma:

```
Prompt: "Extrae todos los iconos del archivo de Figma"
```

El agente obtendrá los assets con URLs localhost que puedes usar directamente.

### 2. Obtención de Componentes

Extrae información de componentes y sus propiedades:

```
Prompt: "Dame la estructura del componente Button del design system"
```

### 3. Tokens de Diseño

Obtén colores, tipografías, espaciados y otros tokens:

```
Prompt: "Extrae todos los colores y crea un archivo de tema"
```

### 4. Especificaciones de Diseño

Obtén medidas, espaciados, y especificaciones técnicas:

```
Prompt: "Dame las especificaciones del componente Card"
```

## 📝 Mejores Prácticas

### 1. Uso de Assets

**❌ Incorrecto:**
```dart
// NO uses placeholders si Figma proporciona el asset
Icon(Icons.placeholder)
```

**✅ Correcto:**
```dart
// USA el asset directamente desde Figma
Image.network('http://localhost:8080/asset/icon-home.svg')
```

### 2. Fidelidad al Diseño

**Regla de oro:** Prioriza la fidelidad exacta al diseño de Figma.

```
Prompt guidelines:
- "Implementa EXACTAMENTE como está en Figma"
- "Usa los valores exactos del diseño, sin aproximaciones"
- "Mantén todos los espaciados y medidas del diseño original"
```

### 3. Componentes del Design System

Si tienes un design system en tu codebase:

```
Prompt: "Usa los componentes de /lib/design_system cuando sea posible.
Si el componente no existe, créalo basándote en el diseño de Figma."
```

### 4. Tokens de Diseño

Evita valores hardcodeados:

**❌ Incorrecto:**
```dart
Container(
  color: Color(0xFF2196F3), // Valor hardcodeado
  padding: EdgeInsets.all(16),
)
```

**✅ Correcto:**
```dart
Container(
  color: AppColors.primary, // Token desde Figma
  padding: AppSpacing.medium, // Token desde Figma
)
```

### 5. Divide Selecciones Grandes

Para archivos grandes de Figma:

1. Extrae componentes individualmente (Card, Button, Header)
2. Implementa sección por sección
3. Combina al final

Esto previene timeouts y errores por contexto muy grande.

## 🔧 Configuración Recomendada

### Reglas de Cursor (.cursor/rules.md)

Crea reglas personalizadas para tu equipo:

```markdown
---
description: Figma MCP server rules
globs:
alwaysApply: true
---

## Reglas de Figma MCP Server

- El servidor Figma MCP proporciona un endpoint de assets que puede servir imágenes y SVGs
- IMPORTANTE: Si el servidor MCP de Figma retorna una fuente localhost para una imagen o SVG, usa esa fuente directamente
- IMPORTANTE: NO importes/agregues nuevos paquetes de iconos, todos los assets deben venir del payload de Figma
- IMPORTANTE: NO uses o crees placeholders si se proporciona una fuente localhost

## Reglas de Calidad

- IMPORTANTE: Siempre usa componentes de `/lib/design_system` cuando sea posible
- Prioriza la fidelidad a Figma para coincidir exactamente con los diseños
- Evita valores hardcodeados, usa tokens de diseño de Figma donde estén disponibles
- Sigue los requisitos WCAG para accesibilidad
- Agrega documentación a los componentes
- Coloca componentes UI en `/lib/design_system`; evita estilos inline a menos que sea realmente necesario
```

### Variables de Entorno

Crea un archivo `.env` (no lo commits):

```env
# Figma Configuration
FIGMA_TOKEN=tu-token-personal-de-figma
FIGMA_FILE_ID=id-del-archivo-de-figma
```

## 📊 Workflow Típico

### 1. Extraer Assets

```
Prompt: "Del archivo de Figma [URL], extrae todos los iconos y guárdalos en assets/icons/"
```

### 2. Crear Tema

```
Prompt: "Extrae los colores del design system de Figma y crea un AppTheme en lib/config/theme/"
```

### 3. Implementar Componente

```
Prompt: "Implementa el componente ProductCard exactamente como está en Figma, usando el design system existente donde sea posible"
```

### 4. Crear Pantalla Completa

```
Prompt: "Implementa la pantalla Home según el diseño de Figma. Divide en componentes reutilizables."
```

## 🎨 Ejemplo: De Figma a Flutter

### Paso 1: Extraer Tokens de Diseño

```
Prompt: "Extrae los colores, tipografías y espaciados del design system de Figma"
```

Resultado esperado:

```dart
// lib/config/theme/app_colors.dart
class AppColors {
  // Extraído desde Figma
  static const primary = Color(0xFF2196F3);
  static const secondary = Color(0xFFFFC107);
  static const background = Color(0xFFF5F5F5);
  // ...
}

// lib/config/theme/app_spacing.dart
class AppSpacing {
  static const small = 8.0;
  static const medium = 16.0;
  static const large = 24.0;
}
```

### Paso 2: Implementar Componente

```
Prompt: "Implementa el componente Button del design system de Figma con todas sus variantes"
```

Resultado esperado:

```dart
// lib/design_system/button.dart
class AppButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final ButtonVariant variant;

  const AppButton({
    Key? key,
    required this.label,
    this.onPressed,
    this.variant = ButtonVariant.primary,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: _getStyle(),
      child: Text(label),
    );
  }

  ButtonStyle _getStyle() {
    switch (variant) {
      case ButtonVariant.primary:
        return ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          padding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.large,
            vertical: AppSpacing.medium,
          ),
        );
      case ButtonVariant.secondary:
        return ElevatedButton.styleFrom(
          backgroundColor: AppColors.secondary,
        );
    }
  }
}
```

## 🔍 Troubleshooting

### Problema: No se conecta al servidor MCP

**Solución:**
1. Verifica que el token de Figma es válido
2. Reinicia el cliente MCP
3. Revisa los logs del servidor MCP

### Problema: Assets no se cargan

**Solución:**
1. Verifica permisos del archivo de Figma
2. Asegúrate de que el archivo está publicado o compartido
3. Verifica la conexión a internet

### Problema: Componente no coincide con diseño

**Solución:**
1. Divide la selección en partes más pequeñas
2. Sé más específico en el prompt sobre qué debe coincidir
3. Verifica que estás viendo la versión correcta en Figma

## 📚 Recursos Adicionales

- [Figma MCP Server GitHub](https://github.com/figma/mcp-server-guide/)
- [Figma Dev Mode Documentation](https://help.figma.com/hc/en-us/articles/32132100833559)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 🔗 Integración con Otros Skills

Este skill se combina bien con:

- `flutter/mvvm` - Implementa componentes con patrón MVVM
- `flutter/clean-architecture` - Crea componentes siguiendo Clean Architecture
- `flutter/project-setup` - Configura tema y design system inicial
- `cicd` - Automatiza la extracción de assets en el pipeline

### Ejemplo de Combinación

```
Prompt: "Usando figma, extrae el componente ProductCard e impleméntalo con mvvm para la app de e-commerce"
```

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.0
