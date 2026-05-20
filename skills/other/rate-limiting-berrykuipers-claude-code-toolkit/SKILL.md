---
name: gemini-api-rate-limiting
description: Best practices for handling Gemini API rate limits, implementing sequential queues, and preventing 429 RESOURCE_EXHAUSTED errors in WescoBar
---

# Gemini API Rate Limiting

## Purpose

Provide proven patterns and best practices for handling Google Gemini API rate limits in the WescoBar Universe Storyteller application, preventing `429 RESOURCE_EXHAUSTED` errors.

## When to Use

- Implementing any feature that calls Gemini API
- Debugging 429 rate limit errors
- Designing image generation workflows
- Planning bulk API operations
- Optimizing API usage patterns

## Problem Statement

Making many simultaneous Gemini API calls (e.g., generating portraits for all core characters on startup) results in:
- `429 RESOURCE_EXHAUSTED` errors
- Stuck UI with perpetual loading spinners
- Poor user experience
- Wasted API quota

## Solution: Sequential Asynchronous Queue

### Core Pattern

```typescript
// ✅ CORRECT: Sequential queue with delays
async function processImageQueue(characters: Character[]) {
  for (const character of characters) {
    // Process one at a time
    await generateImage(character);

    // Add delay between calls to respect API limits
    await new Promise(resolve => setTimeout(resolve, 2000)); // 2 second delay
  }
}
```

```typescript
// ❌ WRONG: Parallel requests
async function processImageQueue(characters: Character[]) {
  // This will trigger rate limits!
  await Promise.all(
    characters.map(char => generateImage(char))
  );
}
```

## Implementation Guidelines

### 1. Use for...of Loop for Sequential Processing

```typescript
// In WorldContext or similar service
const needsImages = characters.filter(c => !c.imageUrl);

for (const character of needsImages) {
  try {
    const imageUrl = await geminiService.generatePortrait(character);
    updateCharacterImage(character.id, imageUrl);
  } catch (error) {
    handleGenerationError(character.id, error);
  }

  // Hard-coded delay to prevent burst traffic
  await new Promise(resolve => setTimeout(resolve, 2000));
}
```

### 2. Implement API Timeouts

Race API calls against timeouts to prevent hung requests:

```typescript
async function generateWithTimeout(character: Character, timeoutMs = 30000) {
  return Promise.race([
    geminiService.generatePortrait(character),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Generation timed out')), timeoutMs)
    )
  ]);
}
```

### 3. Add Queue Status Indicators

Show users progress during sequential processing:

```typescript
// Update UI with queue progress
setGenerationQueue({
  total: needsImages.length,
  current: index + 1,
  inProgress: true,
  character: character.name
});
```

## Cache Strategy

Reduce API calls through robust caching:

### Cache Key Design

```typescript
// ✅ Entity-stable keys (won't invalidate on prompt changes)
const cacheKey = `${CACHE_VERSION}-character-portrait:${character.id}`;

// ❌ Prompt-based keys (invalidate too often)
const cacheKey = `${CACHE_VERSION}-${fullPromptText}`;
```

### Cache Versioning

```typescript
// Global cache version for instant invalidation
const CACHE_VERSION = 'v2'; // Bump to invalidate all caches

// Prepend to all cache keys
const cacheKey = `${CACHE_VERSION}-character-portrait:${id}`;
```

### Cache Busting

```typescript
// For explicit regeneration (e.g., "Regenerate" button)
async function regenerateImage(character: Character) {
  const imageUrl = await geminiService.generatePortrait(
    character,
    { forceRebuild: true } // Bypasses cache
  );
  return imageUrl;
}
```

## Rate Limit Best Practices

### 1. Delay Between Requests

```typescript
// Minimum 2 seconds between API calls
const RATE_LIMIT_DELAY_MS = 2000;

await new Promise(resolve => setTimeout(resolve, RATE_LIMIT_DELAY_MS));
```

### 2. Exponential Backoff on 429

```typescript
async function callWithBackoff(fn: () => Promise<any>, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429 && i < maxRetries - 1) {
        const delayMs = Math.pow(2, i) * 1000; // 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, delayMs));
      } else {
        throw error;
      }
    }
  }
}
```

### 3. Queue Size Limits

```typescript
// Limit concurrent queue size
const MAX_QUEUE_SIZE = 10;

if (queue.length > MAX_QUEUE_SIZE) {
  // Process in batches or show warning
  console.warn(`Queue size ${queue.length} exceeds maximum ${MAX_QUEUE_SIZE}`);
}
```

## Error Handling

### Categorize Errors

```typescript
function handleGeminiError(error: any, character: Character) {
  if (error.status === 429) {
    // Rate limit - add to retry queue
    retryQueue.push(character);
  } else if (error.message?.includes('timeout')) {
    // Timeout - set error state
    setCharacterError(character.id, 'Generation timed out');
  } else if (error.status >= 500) {
    // Server error - temporary, retry later
    setCharacterError(character.id, 'Server error, retry later');
  } else {
    // Other error - likely permanent
    setCharacterError(character.id, 'Generation failed');
  }
}
```

## Real-World Example from WescoBar

From `WorldContext.tsx`:

```typescript
// On startup, identify all core characters needing images
useEffect(() => {
  const coreCharacters = characters.filter(
    c => c.isCoreCharacter && !c.imageUrl
  );

  if (coreCharacters.length === 0) return;

  async function generateImagesSequentially() {
    for (const character of coreCharacters) {
      try {
        // Race against timeout
        const imageUrl = await Promise.race([
          geminiService.generateCharacterPortrait(character),
          new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Timeout')), 30000)
          )
        ]);

        // Update state
        updateCharacter(character.id, { imageUrl });
      } catch (error) {
        // Store error on character object
        updateCharacter(character.id, {
          generationError: error.message
        });
      }

      // Hard-coded delay
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }

  generateImagesSequentially();
}, [characters]);
```

## Quick Reference

| Scenario | Pattern | Delay |
|----------|---------|-------|
| Bulk generation (10+ items) | Sequential for...of loop | 2 seconds |
| Single generation (user-initiated) | Direct call with timeout | No delay |
| Retry after 429 | Exponential backoff | 1s → 2s → 4s |
| Cache miss | Check cache → API → cache store | 2 seconds between misses |

## Related Skills

- `gemini-api/error-handling` - Comprehensive error handling patterns
- `gemini-api/caching-strategies` - Advanced caching techniques
- `gemini-api/image-generation` - Complete image generation workflows

## Additional Resources

See `REFERENCE.md` for:
- Gemini API rate limit documentation
- Full WorldContext implementation example
- Cache version management strategies
- Performance optimization patterns
