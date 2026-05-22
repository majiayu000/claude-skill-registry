---
name: typescript-shims
description: Generates TypeScript declaration files (shims-vue.d.ts, shims-svg.d.ts) to enable type-safe imports of Vue components and SVG files.
---

# TypeScript Shims Skill

## Purpose
Generate TypeScript declaration files (shims) to enable type-safe imports of non-TypeScript modules in a Vue 3 application.

## Output
Create the files:
- `/src/shims-vue.d.ts`
- `/src/shims-svg.d.ts`

## Configuration Requirements

### Vue Component Shims (`shims-vue.d.ts`)

#### Purpose
Enable TypeScript to recognize and properly type `.vue` single-file components when imported into TypeScript files.

#### Requirements
- **Module Declaration**: Declare a module pattern for `*.vue` files
- **Vue Integration**: Import the appropriate component type from the Vue package
- **Component Type**: Type the default export as a Vue component definition
- **Generic Typing**: Use appropriate generic parameters to allow flexibility in component props, emits, and other options

#### Key Concepts
- Without this file, TypeScript cannot understand what a `.vue` file exports
- The shim tells TypeScript that any `.vue` import is a valid Vue component
- Should use Vue 3's component typing system (not Vue 2's)
- Must align with your Vue version's type definitions

### SVG Asset Shims (`shims-svg.d.ts`)

#### Purpose
Enable importing SVG files in multiple ways: as Vue components or as URL strings.

#### Requirements

**SVG as Component Import**
- **Module Declaration**: Declare a module pattern for `*.svg` files
- **Component Type**: Type the default export as a Vue component
- **Use Case**: Allows inline SVG usage as `<MySvgIcon />` in templates

**SVG as URL Import**
- **Module Declaration**: Declare a module pattern for `*.svg?url` files (with query parameter)
- **String Type**: Type the default export as a string (URL path)
- **Use Case**: Allows using SVG as image source: `<img :src="logoUrl" />`

#### Key Concepts
- Supports Vite's asset handling with query parameters
- Two import styles for different use cases:
  - Direct import: treats SVG as inline component
  - Query parameter import: treats SVG as static asset URL
- Aligns with modern bundler conventions (Vite, Webpack 5+)

## Implementation Guidelines

### Vue Shims Best Practices
- Import component types from the main Vue package (not from separate type packages)
- Use the most current component definition types available in your Vue version
- Keep generic parameters flexible unless specific constraints are needed
- Ensure compatibility with `<script setup>` and Options API components

### SVG Shims Best Practices
- Support both component and URL import patterns
- Use query parameter syntax that matches your bundler (typically `?url` for Vite)
- Keep shims minimal and focused on typing, not implementation
- Consider supporting additional query parameters if your build tool offers them (e.g., `?raw`, `?component`)

## Validation

After generating the shims:
1. **Vue Import Test**: Verify you can import `.vue` files without TypeScript errors
2. **SVG Component Test**: Verify you can import and use SVG as a component
3. **SVG URL Test**: Verify you can import SVG with `?url` suffix and use as string
4. **IDE Support**: Check that autocomplete and type hints work for these imports
5. **Build Success**: Ensure the application builds without type errors

## Integration Notes

### TypeScript Configuration
- Include these shim files in your `tsconfig.json` include array
- Example: `"include": ["src/**/*.d.ts"]` or explicitly list the shim files

### Build Tool Compatibility
- **Vite**: Uses `?url` query parameter syntax for asset URLs
- **Webpack**: May use different loaders; adjust query parameters as needed
- **Other Bundlers**: Consult documentation for asset import conventions

### Vue Version Compatibility
- **Vue 3**: Use modern component type definitions (e.g., `DefineComponent`)
- **Future Versions**: Adopt new type definitions as Vue evolves
- **Type-only Imports**: Consider using `import type` for type-only imports to avoid runtime overhead

## Extension Possibilities

As your application grows, you may need additional shims for:
- **Image Files**: `.png`, `.jpg`, `.webp` imports
- **Font Files**: `.woff`, `.woff2`, `.ttf` imports
- **JSON Files**: If not covered by TypeScript's `resolveJsonModule`
- **CSS Modules**: `.module.css`, `.module.scss` imports
- **Web Workers**: `.worker.ts` imports
- **WASM Modules**: `.wasm` imports

Follow the same pattern: declare the module, specify the import type, and ensure alignment with your bundler's behavior.

## Philosophy

These shims exist to:
- **Bridge the Gap**: Connect TypeScript's type system with non-TypeScript assets
- **Enable Type Safety**: Catch import errors at compile time rather than runtime
- **Support Modern Workflows**: Work seamlessly with modern build tools and asset handling
- **Stay Minimal**: Provide just enough typing without overcomplicating

## Future Compatibility

When TypeScript or Vue evolves:
- Update to use the latest component type definitions from Vue
- Adopt new TypeScript declaration syntax as it becomes available
- Adjust module patterns to match bundler conventions
- Maintain the core principle: type-safe imports for all asset types
- Remove deprecated type definitions and replace with modern equivalents