---
name: troubleshooting-bugs
description: Standard protocol for debugging and fixing issues across the stack. Use when encountering errors or unexpected behavior.
---

# Debugging and Troubleshooting

## When to use this skill
- UI is not rendering as expected.
- Appwrite API calls are failing.
- Next.js build errors or hydration mismatches.

## Protocol
1.  **Check Browser Console**: Look for hydration errors or JavaScript crashes.
2.  **Check Network Tab**: Inspect the request/response payload for Appwrite calls.
3.  **Check Appwrite Console**: View "Logs" and "Permissions" for the failing collection.
4.  **Check Terminal**: Look for `use server` or promise-related errors in the Next.js dev server.

## Common Fixes
- **Auth Error (401)**: User is not logged in or doesn't have permissions.
- **Hydration Error**: Ensure `useState` or browser-only APIs are wrapped in `useEffect`.
- **Forbidden (403)**: Check Appwrite "Document Security" settings.

## Instructions
- **Log specifically**: Use `console.error('[Appwrite Error]:', error)` for clarity.
