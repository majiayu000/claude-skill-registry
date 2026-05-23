---
name: update-types
description: Safely update the core data schema and types. Use when changing data models, adding fields, or modifying the report structure.
---

When updating types in the Weekly Report Builder, follow this sequence:

1. **Modify the type definition:**
   - Edit `client/src/types.ts` (or `src/types.ts`)
   - Add/modify the field with proper typing
   - Add JSDoc comments for complex fields

2. **Update initialization:**
   - Check `src/App.tsx` or `client/src/App.tsx` for `emptyReport` initialization
   - Ensure new fields have sensible default values
   - Example: `newField: ''` or `newField: []`

3. **Check update handlers:**
   - Review `src/components/ReportEditor.tsx` generic update handlers
   - Ensure they can handle the new field type

4. **Update any serialization:**
   - Check `data/` directory for JSON schemas
   - Update any API endpoints that use the type

5. **Verify:**
   - Run `npm run build` to catch type errors
   - Search for usages of the modified type to ensure compatibility
