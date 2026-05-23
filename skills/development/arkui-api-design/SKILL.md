---
name: arkui-api-design
description: This skill should be used when the user asks to "design ArkUI API", "add component property", "create Modifier method", "review ArkUI API", "deprecate API", "write JSDOC for ArkUI", or mentions OpenHarmony API design standards. Provides comprehensive guidance for ArkUI component API design following OpenHarmony coding guidelines.
version: 1.0.0
---

# ArkUI API Design Skill

This skill provides comprehensive guidance for designing, reviewing, and maintaining ArkUI component APIs that follow OpenHarmony Application TypeScript/JavaScript coding guidelines.

## Core Design Principles

### 1. Follow OpenHarmony Coding Standards

All API definitions and code examples must comply with the *OpenHarmony Application TypeScript/JavaScript Coding Guide*. Key standards include:

- **Naming conventions**: Use camelCase for properties and methods, PascalCase for types/interfaces
- **Type safety**: Provide proper TypeScript type definitions for all parameters
- **Code style**: Follow 4-space indentation, consistent formatting
- **Documentation**: Comprehensive JSDOC comments for all public APIs

For detailed standards, refer to: **`references/OpenHarmony-Application-Typescript-JavaScript-coding-guide.md`**

### 2. Synchronize Component Properties and Modifiers

When adding or removing component properties and methods, ensure corresponding Modifier methods are created or deprecated:

**Adding new property:**
```typescript
// Interface definition
interface ButtonStyle {
  iconSize?: number;
}

// Modifier method must be added
iconSize(value: number | string): ButtonAttribute;
```

**Deprecating property:**
- Mark interface property as `@deprecated` with migration guidance
- Mark corresponding Modifier method as `@deprecated`
- Provide alternative methods and migration examples

### 3. Support resourceStr for Flexibility

When parameters accept `number | string | Length` types, consider adding `Resource` type support to improve theming and i18n scenarios:

```typescript
// Recommended: Support Resource type
fontSize(value: number | string | Length | Resource): TextAttribute

// Usage examples
Text().fontSize(16)                              // number
Text().fontSize('16vp')                          // string
Text().fontSize($r('app.float.font_size_large')) // Resource type (supports theming)
```

**Benefits:**
- Enables centralized theme management through resource files
- Supports internationalization with locale-specific resources
- Improves developer experience for dynamic theming

### 4. Document undefined/null Behavior

JSDOC comments must explicitly specify how `undefined` and `null` values are handled:

```typescript
/**
 * Sets the font size of the text.
 * @param value Font size value. If undefined, restores to default size (16fp).
 *              If null, removes the font size setting and uses inherited value.
 * @throws {Error} Throws error if value is negative.
 * @since 10
 */
fontSize(value: number | string | Length | Resource | undefined | null): TextAttribute;
```

**Common patterns:**
- `undefined` → Restore default value
- `null` → Remove setting, use inherited value
- Invalid values → Throw error with clear message

### 5. Use vp as Default Length Unit

Always use `vp` (virtual pixels) as the default unit for length measurements:

```typescript
// Good: Default to vp
width(value: number | string): ButtonAttribute  // 100 means 100vp

// Good: Explicit vp
width(value: Length): ButtonAttribute  // Length.type defaults to vp

// Avoid: Require px without good reason
width(value: number): ButtonAttribute  // 100px - avoid unless necessary
```

### 6. Specify Constraints in JSDOC

JSDOC comments must include specification limits and constraints:

```typescript
/**
 * Sets the border radius of the component.
 * @param value Border radius value. Valid range: 0-1000vp.
 *              Values exceeding 1000vp will be clamped to 1000vp.
 *              Negative values are treated as 0.
 * @unit vp
 * @since 10
 */
borderRadius(value: number | string | Length): CommonMethod;
```

**Required documentation:**
- Valid ranges (min/max values)
- Special value handling (negative, zero, etc.)
- Unit of measurement
- Clamping behavior (if applicable)

### 7. Consider Cross-Component Impact

When adding common properties, evaluate the impact on all components:

**Before adding common property:**
1. Check if property applies to most components (layout, style, event)
2. Define consistent behavior across component types
3. Document component-specific exceptions (if any)
4. Consider backward compatibility

**Example common properties:**
- Layout: `width()`, `height()`, `padding()`, `margin()`
- Style: `opacity()`, `visibility()`, `borderRadius()`
- Event: `onClick()`, `onTouch()`

### 8. Respect Interface Directory Boundaries

During compilation verification, modify only files within the `interface/` directory:

**Allowed modifications:**
- `interfaces/inner_api/` - Internal API definitions
- `interfaces/native/` - NDK API definitions
- Type definition files (*.d.ts)

**Do NOT modify:**
- Framework implementation code
- Component pattern files
- Layout or render implementations

**Verification workflow:**
1. Check only interface files for compilation errors
2. Verify type definitions are correct
3. Validate JSDOC comments and metadata
4. Ensure Modifier method signatures match interfaces

## API Design Workflow

### For New Component APIs

1. **Define interface** with proper TypeScript types
2. **Create Modifier methods** for all settable properties
3. **Add JSDOC comments** including:
   - Parameter descriptions
   - undefined/null handling
   - Value constraints and ranges
   - Default values
   - @since version
   - @throws documentation (if applicable)
4. **Support Resource type** for theme-able properties
5. **Specify units** (default to vp for lengths)
6. **Verify cross-component impact** if adding common property
7. **Test compilation** in interface directory only

### For API Reviews

Use the following checklist to verify:
- Compliance with coding standards
- Modifier synchronization
- Resource type support where appropriate
- Complete JSDOC documentation
- Constraint specifications
- Cross-component consistency

### For API Deprecation

1. Mark both interface and Modifier as `@deprecated`
2. Provide migration path in JSDOC
3. Specify removal version
4. Update documentation and examples

## Code Examples

### Complete API Definition

```typescript
/**
 * Sets the opacity of the component.
 * @param value Opacity value. Valid range: 0-1.
 *              If undefined, restores default opacity (1.0).
 *              If null, removes opacity setting.
 *              Values < 0 are treated as 0.
 *              Values > 1 are treated as 1.
 * @throws {TypeError} Throws error if value is not number/string.
 * @since 9
 */
opacity(value: number | string | undefined | null): CommonMethod;

// Implementation considerations:
// - Resource support: Not needed (opacity is numeric, not theme-able)
// - Unit: N/A (ratio, not length)
// - Cross-component: Common property, applies to all components
```

### Example with Resource Type Support

```typescript
/**
 * Sets the font size of text content.
 * @param value Font size in fp. Valid range: 0-1000fp.
 *              If undefined, restores default size (16fp).
 *              Supports resource string for theming ($r('app.float.font_size')).
 * @unit fp
 * @since 10
 */
fontSize(value: number | string | Length | Resource | undefined | null): TextAttribute;
```

## Common Pitfalls

**Missing Modifier synchronization:**
```typescript
// Bad: Interface has property, no Modifier
interface ButtonStyle { iconSize?: number; }

// Good: Both interface and Modifier
interface ButtonStyle { iconSize?: number; }
iconSize(value: number | string): ButtonAttribute;
```

**Incomplete JSDOC:**
```typescript
// Bad: Missing null/undefined handling, constraints
/**
 * Sets the width.
 */
width(value: number): CommonMethod;

// Good: Complete documentation
/**
 * Sets the component width.
 * @param value Width value in vp. Valid range: 0-10000vp.
 *              If undefined, restores default width.
 * @unit vp
 * @since 8
 */
width(value: number | string | Length | undefined): CommonMethod;
```

**Forgetting Resource type:**
```typescript
// Less optimal: Only accepts number/string
fontSize(value: number | string): TextAttribute;

// Better: Supports resource theming
fontSize(value: number | string | Length | Resource): TextAttribute;
```

## Additional Resources

### Coding Standards

- **`references/OpenHarmony-Application-Typescript-JavaScript-coding-guide.md`**
  - OpenHarmony TypeScript/JavaScript Coding Guide (official complete version)
  - Contains naming conventions, type definitions, code formatting, and all coding standards
  - All design principles in this skill are based on this document

### Example Code

- **`examples/interface-definition.ts`** - Complete interface definition example
- **`examples/modifier-implementation.ts`** - Modifier method implementation example
- **`examples/deprecation-pattern.ts`** - API deprecation with migration example

## Quick Reference

### Essential JSDOC Tags

```typescript
/**
 * Brief description.
 * @param paramName Description including undefined/null behavior and constraints.
 * @unit vp | fp | px (for length values)
 * @throws {ErrorType} Description (when errors can occur)
 * @since version (API introduction version)
 * @deprecated Use alternativeMethod() instead (for deprecated APIs)
 */
```

### Type Support Decision Tree

```
Does the parameter accept length values?
├─ Yes → Add Length and Resource types
└─ No → Is it theme-able (color, size, string)?
    ├─ Yes → Add Resource type
    └─ No → Use basic types (number | string | undefined | null)
```

### Default Value Documentation

```typescript
// Document defaults in JSDOC:
"If undefined, restores to default [value] ([unit])."
"If null, removes setting and uses inherited value."
```
