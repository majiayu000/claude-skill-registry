---
name: gemini-api-caching
description: Best practices for Gemini API caching strategy including cache versioning, entity-stable keys, and cache busting for WescoBar
---

# Gemini API Caching

## Purpose

Implement robust caching strategies for Gemini API calls to reduce cost, improve latency, and provide better user experience while supporting cache invalidation when needed.

## When to Use

- Implementing any Gemini API feature
- Generating character portraits or world images
- Caching AI-generated content
- Reducing API quota usage
- Improving app performance

## Caching Strategy

From AGENTS.md Section 3: "A robust, multi-layered local storage cache"

### 1. Cache Versioning
### 2. Entity-Stable Keys
### 3. Cache Busting

## Instructions

### Step 1: Define Cache Version

```typescript
// Global cache version constant
const CACHE_VERSION = 'v2';

// Prepend to all cache keys
const getCacheKey = (entity: string, id: string) => {
  return `${CACHE_VERSION}-${entity}:${id}`;
};

// Example
const portraitKey = getCacheKey('character-portrait', 'core-pablo');
// Result: "v2-character-portrait:core-pablo"
```

**Purpose**: Instant global cache invalidation by bumping version

**When to bump**:
- Prompt template changes
- Image generation model updates
- Quality improvements needed
- Global regeneration required

### Step 2: Use Entity-Stable Keys

```typescript
// ✅ CORRECT: Entity-based key (stable)
const cacheKey = `${CACHE_VERSION}-character-portrait:${character.id}`;

// ❌ WRONG: Prompt-based key (invalidates on prompt changes)
const cacheKey = `${CACHE_VERSION}-${fullPromptText}`;
```

**Why entity-stable**:
- Same character = same cache key
- Minor prompt tweaks don't invalidate cache
- Consistent across sessions
- Reduces unnecessary regeneration

**Entity Types**:
- `character-portrait:<id>` - Character portraits
- `world-scene:<id>` - World/location images
- `story-illustration:<id>` - Story illustrations
- `ui-element:<name>` - UI-generated images

### Step 3: Implement Cache Read

```typescript
async function getCharacterPortrait(
  character: Character,
  options?: { forceRebuild?: boolean }
): Promise<string> {
  // Check force rebuild flag
  if (options?.forceRebuild) {
    return await generateNewPortrait(character);
  }

  // Build cache key
  const cacheKey = `${CACHE_VERSION}-character-portrait:${character.id}`;

  // Check localStorage cache
  const cached = localStorage.getItem(cacheKey);

  if (cached) {
    console.log(`✅ Cache hit: ${cacheKey}`);
    return cached; // Return cached URL
  }

  console.log(`⚠️ Cache miss: ${cacheKey}`);

  // Generate new image
  const imageUrl = await generateNewPortrait(character);

  // Store in cache
  localStorage.setItem(cacheKey, imageUrl);

  return imageUrl;
}
```

### Step 4: Implement Cache Write

```typescript
async function generateAndCachePortrait(
  character: Character
): Promise<string> {
  // Generate image via Gemini API
  const imageUrl = await geminiService.generateImage({
    prompt: buildCharacterPrompt(character),
    // ... other options
  });

  // Cache the result
  const cacheKey = `${CACHE_VERSION}-character-portrait:${character.id}`;
  localStorage.setItem(cacheKey, imageUrl);

  console.log(`💾 Cached: ${cacheKey}`);

  return imageUrl;
}
```

### Step 5: Implement Cache Busting

```typescript
// Option 1: Force rebuild via flag
async function regeneratePortrait(character: Character) {
  const imageUrl = await getCharacterPortrait(character, {
    forceRebuild: true // Bypass cache
  });
  return imageUrl;
}

// Option 2: Clear specific cache entry
function clearPortraitCache(character: Character) {
  const cacheKey = `${CACHE_VERSION}-character-portrait:${character.id}`;
  localStorage.removeItem(cacheKey);
  console.log(`🗑️ Cleared cache: ${cacheKey}`);
}

// Option 3: Clear all portraits
function clearAllPortraits() {
  const prefix = `${CACHE_VERSION}-character-portrait:`;

  Object.keys(localStorage)
    .filter(key => key.startsWith(prefix))
    .forEach(key => localStorage.removeItem(key));

  console.log(`🗑️ Cleared all portrait cache`);
}

// Option 4: Bump global version
// Change CACHE_VERSION = 'v2' → 'v3'
// All old caches become stale automatically
```

### Step 6: Handle Cache Expiration (Optional)

```typescript
interface CachedImage {
  url: string;
  timestamp: number;
  version: string;
}

function getCachedImage(key: string, maxAge: number = 7 * 24 * 60 * 60 * 1000): string | null {
  const cached = localStorage.getItem(key);

  if (!cached) return null;

  try {
    const data: CachedImage = JSON.parse(cached);

    // Check version
    if (data.version !== CACHE_VERSION) {
      localStorage.removeItem(key);
      return null;
    }

    // Check age
    const age = Date.now() - data.timestamp;
    if (age > maxAge) {
      localStorage.removeItem(key);
      return null;
    }

    return data.url;
  } catch {
    // Invalid format - clear cache
    localStorage.removeItem(key);
    return null;
  }
}

function setCachedImage(key: string, url: string) {
  const data: CachedImage = {
    url,
    timestamp: Date.now(),
    version: CACHE_VERSION
  };

  localStorage.setItem(key, JSON.stringify(data));
}
```

## Integration Patterns

### With Rate Limiting Skill

Combine with `gemini-api-rate-limiting` skill:

```typescript
async function generateImagesSequentially(characters: Character[]) {
  for (const character of characters) {
    // Check cache first (from this skill)
    const cached = await getCharacterPortrait(character);

    if (cached) {
      updateCharacterImage(character.id, cached);
      continue; // Skip API call
    }

    // Cache miss - generate with rate limiting
    // (from gemini-api-rate-limiting skill)
    try {
      const imageUrl = await generateWithTimeout(character, 30000);
      updateCharacterImage(character.id, imageUrl);
    } catch (error) {
      handleGenerationError(character.id, error);
    }

    // Delay between calls (rate limiting)
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}
```

### UI Integration

```typescript
// In React component
function CharacterCard({ character }: { character: Character }) {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [isRegenerating, setIsRegenerating] = useState(false);

  useEffect(() => {
    // Load from cache or generate
    getCharacterPortrait(character).then(setImageUrl);
  }, [character.id]);

  const handleRegenerate = async () => {
    setIsRegenerating(true);

    // Force rebuild (cache busting)
    const newUrl = await regeneratePortrait(character);
    setImageUrl(newUrl);

    setIsRegenerating(false);
  };

  return (
    <div>
      <img src={imageUrl || placeholderImage} alt={character.name} />
      <button onClick={handleRegenerate} disabled={isRegenerating}>
        {isRegenerating ? 'Regenerating...' : 'Regenerate Portrait'}
      </button>
    </div>
  );
}
```

## Cache Management UI

```typescript
// Admin/settings panel for cache management
function CacheManagement() {
  const [stats, setStats] = useState({ portraits: 0, scenes: 0, total: 0 });

  useEffect(() => {
    // Calculate cache stats
    const portraitKeys = Object.keys(localStorage)
      .filter(key => key.includes('character-portrait'));

    setStats({
      portraits: portraitKeys.length,
      scenes: 0, // Add scene counting
      total: localStorage.length
    });
  }, []);

  const clearAllCache = () => {
    const confirmed = window.confirm('Clear all cached images? This will regenerate on next load.');

    if (confirmed) {
      Object.keys(localStorage)
        .filter(key => key.startsWith(CACHE_VERSION))
        .forEach(key => localStorage.removeItem(key));

      alert('Cache cleared!');
      window.location.reload();
    }
  };

  return (
    <div>
      <h3>Gemini API Cache</h3>
      <p>Cached portraits: {stats.portraits}</p>
      <p>Total cached items: {stats.total}</p>
      <button onClick={clearAllCache}>Clear All Cache</button>
    </div>
  );
}
```

## Best Practices

1. **Always check cache first** - Reduce API calls
2. **Use entity-stable keys** - Don't invalidate on prompt changes
3. **Version globally** - Easy bulk invalidation
4. **Provide regenerate option** - Let users force refresh
5. **Consider expiration** - For time-sensitive content
6. **Monitor cache size** - localStorage has limits (~5-10MB)
7. **Handle cache errors** - Fallback to generation

## Related Skills

- `gemini-api-rate-limiting` - Combine cache with rate limiting
- `gemini-api-error-handling` - Handle cache failures

## Storage Limits

### localStorage Limits

- **Size**: ~5-10MB depending on browser
- **Monitor usage**: Track total cache size
- **Cleanup strategy**: Remove oldest entries when full

```typescript
function getCacheSize(): number {
  let total = 0;

  for (const key in localStorage) {
    if (localStorage.hasOwnProperty(key)) {
      total += localStorage[key].length + key.length;
    }
  }

  return total; // bytes
}

// If approaching limit, clear old entries
if (getCacheSize() > 5 * 1024 * 1024) { // 5MB
  clearOldestEntries();
}
```

## Notes

- Caching reduces API costs significantly
- Entity-stable keys prevent unnecessary cache invalidation
- Global version bumping enables instant cache refresh
- Force rebuild option gives users control
- Combine with rate limiting for complete API management
