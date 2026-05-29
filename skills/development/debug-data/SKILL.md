---
name: debug-data
description: Debug data storage and persistence issues. Use when troubleshooting lost data, storage problems, or state persistence bugs.
---

Debug data storage issues in the Weekly Report Builder:

1. **Check localStorage hook:**
   - Review `App.tsx` for `useLocalStorage` hook implementation
   - Verify the storage key is consistent
   - Check if data is being read on mount

2. **Verify useEffect dependencies:**
   - All dependencies should be in the array
   - Watch for missing dependencies that could cause stale closures
   - Check for infinite loops from incorrect dependencies

3. **Check JSON parsing:**
   - Ensure all `JSON.parse` calls are wrapped in try/catch
   - Verify `JSON.stringify` handles circular references
   - Check for proper null/undefined handling

4. **Debug steps:**
   ```javascript
   // Add to browser console:
   console.log(localStorage.getItem('YOUR_KEY'));
   ```

5. **Common issues:**
   - Storage quota exceeded
   - Parsing errors on corrupted data
   - Race conditions between read/write
   - Effects running before hydration

6. **Check server-side storage:**
   - Review `server/index.ts` for file-based persistence
   - Check `data/` directory for JSON files
