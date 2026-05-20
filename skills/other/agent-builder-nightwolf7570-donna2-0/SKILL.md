---
name: "Agent Creating"
description: "Used to create a new agent. Used when a user wants to create a new agent"
---

# Create Skill

## Instructions
Invoked when the user requests to create a new agent or subagent


# Create Skill

## Instructions

When requested to create a new skill, follow these steps:
1. Create a new file in `.claude/agents` with the agent name `xyz.md` (ex: "stripe-implementor" or "code-reviewer")
2. Take the requested input given to you to turn into a re-usable agent.
3. Be sure to have the description field be very clear on what it does and how to use it - 2-4 sentences max
5. Make sure it has a clear persona and goal
6. Below that, give it minimal, clear, actionable Markdown instructions as the primary workflow guide.
7. Be sure it knows the `docs/convexGuidelines.md`

## Examples

code-reviewer.md
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.




## Example when agent is app/API/service specific:


---
name: Nano-banana-editor
description: Implement an image editor powered by Google Gemini image model. Use this when implementing an AI image editor into app
model: inherit
color: blue
---

# Agent: Nano Banana Editor

Prevent these exact errors when implementing AI image editing in React Native + Convex.

## Error Prevention Checklist

### 1. TypeScript Return Types
**WILL ERROR:** `TS7022: 'editImageWithGemini' implicitly has type 'any'`
```typescript
// ❌ This breaks
export const editImageWithGemini = action({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {

// ✅ This works  
export const editImageWithGemini = action({
  args: { userId: v.string() },
  handler: async (ctx, { userId }): Promise<{ success: boolean; versionId?: any }> => {
```

### 2. Gemini Model Names
**WILL ERROR:** `[404 Not Found] models/gemini-2.5-flash-image is not found`
```typescript
// ❌ This breaks
model: 'gemini-2.5-flash-image'

// ✅ This works
model: 'gemini-2.5-flash-image-preview'
```

### 3. Buffer in Convex Environment
**WILL ERROR:** `ReferenceError: Buffer is not defined`
```typescript
// ❌ This breaks
const base64 = Buffer.from(arrayBuffer).toString('base64');
const imageBuffer = Buffer.from(base64Data, 'base64');

// ✅ This works - chunked conversion
const uint8Array = new Uint8Array(arrayBuffer);
let binaryString = '';
const chunkSize = 8192;
for (let i = 0; i < uint8Array.length; i += chunkSize) {
  const chunk = uint8Array.slice(i, i + chunkSize);
  binaryString += String.fromCharCode.apply(null, Array.from(chunk));
}
const base64 = btoa(binaryString);

// For base64 to blob
const binaryString = atob(base64Data);
const uint8Array = new Uint8Array(binaryString.length);
for (let i = 0; i < binaryString.length; i++) {
  uint8Array[i] = binaryString.charCodeAt(i);
}
const blob = new Blob([uint8Array], { type: 'image/jpeg' });
```

### 4. Large Array Spread Operator
**WILL ERROR:** `RangeError: Maximum call stack size exceeded`
```typescript
// ❌ This breaks with large images
const base64 = btoa(String.fromCharCode(...uint8Array));

// ✅ This works - use chunked processing from #3 above
```

### 5. Data URL Fetching
**WILL ERROR:** `Unsupported URL scheme -- http and https are supported (scheme was data)`
```typescript
// ❌ This breaks
const response = await fetch(sourceImageUrl); // fails if data: URL

// ✅ This works
if (sourceImageUrl.startsWith('data:')) {
  const base64Match = sourceImageUrl.match(/^data:image\/[^;]+;base64,(.+)$/);
  if (!base64Match) throw new Error('Invalid data URL format');
  base64Data = base64Match[1];
} else {
  const response = await fetch(sourceImageUrl);
  if (!response.ok) throw new Error(`Failed to fetch: ${response.statusText}`);
  // ... convert to base64 using chunked method
}
```

### 6. Database Size Limits
**WILL ERROR:** `Value is too large (1.76 MiB > maximum size 1 MiB)`
```typescript
// ❌ This breaks - data URLs are huge
await ctx.db.insert("projects", {
  originalImageUrl: asset.uri, // data: URL = several MB
});

// Frontend passes data URL to mutation
const projectId = await createProject({
  originalImageUrl: asset.uri, // BREAKS!
});

// ✅ This works - only storage IDs in database
// Backend generates URL from storage ID
const imageUrl = await ctx.storage.getUrl(originalImageId);
await ctx.db.insert("projects", {
  originalImageId: storageId, // small ID
  originalImageUrl: imageUrl, // generated URL
});

// Frontend only passes storage ID
const projectId = await createProject({
  originalImageId: storageId, // WORKS!
});
```

## Implementation Rules

1. **ALWAYS** add `: Promise<Type>` to all Convex action handlers
2. **ALWAYS** use `gemini-2.5-flash-image-preview` (with -preview suffix)
3. **NEVER** use `Buffer` - use chunked `btoa`/`atob` with 8KB chunks
4. **NEVER** use spread operator on large arrays - use chunked processing
5. **ALWAYS** check `imageUrl.startsWith('data:')` before fetch
6. **NEVER** store data URLs in database - upload to storage first, pass only storage IDs