# 🏷️ Skill: Versioning Management

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `versioning-management` |
| **Nivel** | 🟢 Básico |
| **Versión** | 1.0.0 |
| **Keywords** | `semver`, `versioning`, `changelog`, `semantic-versioning`, `release-notes` |
| **Lenguajes Soportados** | Universal (Markdown) |

## 🔑 Keywords para Invocación

- `semver`
- `versioning`
- `changelog`
- `semantic-versioning`
- `release-management`
- `@skill:versioning-management`

### Ejemplos de Prompts

```
Documenta los cambios de esta versión usando SemVer
```

```
Crea un changelog para la versión v1.2.0
```

```
@skill:versioning-management - Genera notas de lanzamiento para el backend
```

## 📖 Descripción

Skill para gestionar el versionamiento semántico (SemVer) de proyectos Flutter. Este skill define la estructura y el proceso para documentar cambios en el backend y en la aplicación móvil, asegurando que cada release tenga un registro claro de adiciones, cambios y eliminaciones.

### ✅ Cuándo Usar Este Skill

- Al completar una nueva funcionalidad (Feature)
- Al corregir un error (Bug Fix)
- Antes de realizar un despliegue a Staging o Producción
- Cuando se requiere sincronizar versiones entre distintos microservicios

### ❌ Cuándo NO Usar Este Skill

- Para commits internos o cambios menores en el código que no afectan la funcionalidad pública
- Documentación puramente técnica de código (usar JSDoc/DartDoc en su lugar)

## 🛠️ Estándar de Versionamiento

Seguimos el estándar [SemVer 2.0.0](https://semver.org/):
- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Funcionalidad nueva compatible hacia atrás
- **PATCH**: Corrección de errores compatible hacia atrás

## 📂 Estructura de Archivos

La documentación de versiones se almacena en `docs/versioning/`:

```
docs/versioning/
├── backend/
│   ├── CHANGELOG-vX.Y.Z.md
│   └── ...
└── mobile/
    ├── CHANGELOG-vX.Y.Z.md
    └── ...
```

## 📝 Formato del Changelog (Basado en [Keep a Changelog](https://keepachangelog.com/))

Cada archivo debe seguir esta estructura:

```markdown
# Changelog - Version X.Y.Z

## [X.Y.Z] - YYYY-MM-DD

### Added
- [ ] Descripción de nueva funcionalidad

### Changed
- [ ] Descripción de cambios en funcionalidad existente

### Deprecated
- [ ] Funcionalidades que serán eliminadas pronto

### Removed
- [ ] Funcionalidades eliminadas en esta versión

### Fixed
- [ ] Corrección de errores

### Security
- [ ] Mejoras de seguridad o parches de vulnerabilidades
```

## 🚀 Proceso de Actualización

1. **Identificar el tipo de cambio**: ¿Es Major, Minor o Patch?
2. **Localizar el componente**: ¿Backend, Mobile o ambos?
3. **Crear/Actualizar el archivo**: Usar el template anterior en la ruta correspondiente.
4. **Verificar consistencia**: Asegurarse de que la fecha y la versión coincidan con los tags de Git si se utilizan.
