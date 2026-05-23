---
name: image-extraction-debug
description: Debug Gemini/GPT vision API issues in puzzle image extraction
allowed-tools: [Read, Edit, Grep, Bash]
---

# Image Extraction Debug

Debug and fix issues with AI-powered puzzle image extraction (GPT-5.2 via OpenRouter).

## When to Use

- Grid extraction returns wrong dimensions (e.g., 5×5 instead of 7×9)
- Domino count mismatches (extracted 12 dominoes, expected 15)
- Region detection failures (missing regions, wrong constraints)
- Pip counting errors (AI reads "5" as "6")
- Constraint badge misinterpretation (reads "Σ10" as "equal")
- API errors or timeouts

## Architecture Overview

**File:** `src/lib/services/gemini.ts`

The extraction uses a **dual-image approach**:

1. **User crops image into two parts** (DualImageCropper component):
   - **Domino image**: Just the domino tiles
   - **Grid image**: Just the grid with constraints

2. **Domino extraction** (line 117-211):
   - Model: `openai/gpt-5.2`
   - Counts pips on each domino half
   - Returns: `[(3,5), (0,0), (2,6), ...]`

3. **Grid extraction** (line 260-400):
   - Model: `openai/gpt-5.2`
   - Identifies regions, constraints, holes
   - Returns: JSON with grid structure

## Common Issues & Solutions

### Issue 1: Wrong Grid Dimensions

**Symptom**: AI extracts 5×5 grid but puzzle is 7×9

**Cause**: AI guesses dimensions from visible cells only, ignoring holes

**Solution**: User provides size hints via `GridSizeHintModal`

**Code location:** `src/lib/services/gemini.ts` line 268-282

```typescript
if (sizeHint) {
  const expectedCells = sizeHint.dominoCount * 2;
  const totalGridCells = sizeHint.cols * sizeHint.rows;
  const expectedHoles = totalGridCells - expectedCells;

  prompt = `${GRID_EXTRACTION_PROMPT}

IMPORTANT SIZE HINTS (from user):
- Grid dimensions: ${sizeHint.cols} columns × ${sizeHint.rows} rows
- Expected valid cells: ${expectedCells}
- Expected holes: ${expectedHoles}`;
}
```

**Test**: Verify size hints are passed through:
1. User provides hints in modal
2. `handleSizeHintConfirm()` stores hints (index.tsx line 283)
3. `extractDualPuzzle()` passes to API (line 315-319)

### Issue 2: Domino Count Mismatch

**Symptom**: "Invalid puzzle: 18 cells but 12 dominoes (need 24 cells)"

**Root causes**:
1. **AI missed dominoes in image**
2. **AI counted same domino twice**
3. **User cropped image poorly** (cut off dominoes)

**Debug steps**:

1. **Check console logs** (line 171):
```typescript
console.log('[AI] GPT-5.2 domino response:', text);
console.log('[AI] Parsed dominoes:', dominoes.map(d => d.pips));
```

2. **Verify parsing** (line 174-210):
   - AI might return different formats
   - Check if regex correctly captures all dominoes

3. **Test with expectedCount hint** (line 123-125):
```typescript
const prompt = expectedCount
  ? `${DOMINO_EXTRACTION_PROMPT}\n\nThere should be EXACTLY ${expectedCount} dominoes in the image.`
  : DOMINO_EXTRACTION_PROMPT;
```

**Fix**: Add domino count hint to dual extraction:

```typescript
// In extractDualPuzzle() function (add parameter)
async function extractDualPuzzle(
  dominoImageUri: string,
  gridImageUri: string,
  sizeHint?: GridSizeHint  // Already has this
) {
  // Pass expectedCount to domino extraction
  const dominoes = await extractDominoesFromImage(
    dominoBase64,
    sizeHint?.dominoCount  // NEW: pass count hint
  );
}
```

### Issue 3: Wrong Pip Counts

**Symptom**: AI reads [3,5] domino as [3,6] or [4,5]

**Causes**:
- Blurry image
- Unusual pip patterns
- Shadows obscuring dots

**Debug**: Check raw AI response (line 171):
```typescript
console.log('[AI] GPT-5.2 domino response:', text);
```

**Solutions**:

**A) Improve prompt specificity** (line 103-110):
```typescript
HOW TO COUNT PIPS (dots) ON EACH HALF:
- 0: blank/empty (no dots at all)
- 1: one center dot
- 2: two dots (diagonal)
- 3: three dots (diagonal line)
- 4: four dots (corners)
- 5: five dots (corners + center)
- 6: six dots (2 columns of 3)
```

Add examples:
```typescript
COMMON MISTAKES TO AVOID:
- Don't count shadows as dots
- 5 pips = 4 corners + 1 center (NOT 6)
- 3 pips = diagonal line (NOT triangle)
```

**B) Lower temperature** (line 159):
```typescript
temperature: 0.1,  // Already low, could go to 0.0
```

**C) Request confidence scores**:
```typescript
Output format:
[
  {"pips": [3,5], "confidence": "high"},
  {"pips": [2,6], "confidence": "medium"},
  ...
]
```

### Issue 4: Constraint Badge Misinterpretation

**Symptom**: "Σ10" badge read as "equal" or "any"

**Cause**: OCR errors, ambiguous badges

**Debug location:** Grid extraction response parsing (line 380-450)

**Check console**:
```typescript
console.log('[AI] GPT-5.2 grid response:', text);
```

**Fix prompt** (line 239-245):
```typescript
Constraint badge meanings:
- "Σ" + number or just a number = sum constraint (type: "sum", value: N)
- "=" = equal (all same value) (type: "equal")
- "≠" = different (all unique) (type: "different")
- ">" + number = greater than (type: "greater", value: N)
- "<" + number = less than (type: "less", value: N)
- No badge = any constraint (type: "any")
```

Add visual examples:
```typescript
EXAMPLES:
- Badge shows "10" or "Σ10" → {"constraint_type": "sum", "constraint_value": 10}
- Badge shows "=" → {"constraint_type": "equal"}
- Badge shows "≠" → {"constraint_type": "different"}
- No badge visible → {"constraint_type": "any"}
```

### Issue 5: Region Contiguity Failures

**Symptom**: "Region A has non-contiguous cells"

**Cause**: AI grouped cells by color instead of dashed boundaries

**Code location:** `checkRegionContiguity()` function (line 60-87)

**This validates** that all cells in a region are connected by edges (not diagonals).

**Debug**:
1. Check if AI properly identified dashed boundaries
2. Verify region cell lists in console output

**Fix prompt** (line 233-235):
```typescript
Rules:
- Do not merge regions by color — only by dashed boundaries.
- Each dashed boundary encloses ONE region.
```

Make more explicit:
```typescript
CRITICAL: Dashed boundaries define regions, NOT colors.
- Two cells of the same color but separated by a dashed line = TWO different regions
- Cells can only be in the same region if connected WITHOUT crossing a dashed boundary
```

### Issue 6: API Errors (401, 429, 500)

**Symptom**: "GPT-5.2 API error: 401" or timeout

**Causes**:
- Invalid API key
- Rate limiting
- OpenRouter service issues

**Debug** (line 163-167):
```typescript
if (!response.ok) {
  const errorText = await response.text();
  console.error('[AI] GPT-5.2 API error:', errorText);
  throw new Error(`GPT-5.2 API error: ${response.status}`);
}
```

**Solutions**:

**A) Check API key** (line 14):
```typescript
const OPENROUTER_API_KEY = process.env.EXPO_PUBLIC_VIBECODE_OPENROUTER_API_KEY;
```

Verify in `.env` file or Vibecode ENV tab.

**B) Add retry logic**:
```typescript
async function extractWithRetry(fn: () => Promise<any>, retries = 3): Promise<any> {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

**C) Add timeout** (currently none):
```typescript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000);

const response = await fetch(OPENROUTER_ENDPOINT, {
  signal: controller.signal,
  // ... other options
});

clearTimeout(timeoutId);
```

## Testing Extraction Changes

### Use Built-in Test Puzzles

**File:** `src/lib/services/gemini.ts`

1. **Sample puzzle** (line 500+): `createSamplePuzzle()`
2. **L-shaped puzzle** (line 600+): `createLShapedPuzzle()`

These bypass AI extraction - useful for testing solver independently.

### Add Debug Extraction Function

Add this to `gemini.ts`:

```typescript
export async function debugExtraction(
  imageUri: string,
  sizeHint?: GridSizeHint
): Promise<{
  rawDominoResponse: string;
  rawGridResponse: string;
  parsedDominoes: ExtractedDomino[];
  parsedGrid: GridExtractionResponse;
}> {
  // Same extraction but returns raw + parsed data
  // ... implementation
}
```

Call from app:
```typescript
const debug = await debugExtraction(imageUri, sizeHint);
console.log('Raw responses:', debug);
```

### Log Image Base64 Size

Add to verify images aren't too large:

```typescript
console.log('[AI] Image size:', Math.round(base64Image.length / 1024), 'KB');

if (base64Image.length > 1024 * 1024) { // 1MB
  console.warn('[AI] Image very large, may cause issues');
}
```

## Prompt Engineering Tips

### For Better Domino Detection

Current prompt (line 92-115) is good but can improve:

**Add**:
```
DETECTION RULES:
1. Each domino is a rectangular tile divided into two square halves
2. Tiles may be rotated but are always rectangular
3. Read ALL tiles visible in image, even if partially cut off
4. Count each unique tile exactly once

OUTPUT VERIFICATION:
Before submitting, verify your count matches the number of distinct rectangular tiles visible.
```

### For Better Grid Detection

Current prompt (line 216-258) is comprehensive but could add:

**Add**:
```
COMMON MISTAKES TO AVOID:
1. Don't assume grid is square (rows ≠ cols)
2. Don't skip holes - mark every # explicitly
3. Don't merge adjacent regions unless boundary is absent
4. Don't guess constraint values if badge is unclear

SELF-CHECK:
- Total cells (regions + holes) = width × height
- Every region ID appears in ascii_grid
- Every coordinate uses 0-indexed (R0,C0 is top-left)
```

## Key Files Reference

```
src/lib/services/gemini.ts            - AI extraction logic
src/components/DualImageCropper.tsx   - Image cropping UI
src/components/GridSizeHintModal.tsx  - Size hint input
src/app/index.tsx                     - Extraction flow orchestration
```

## Example Debugging Session

**Problem**: Grid extracted as 5×5 but should be 7×9 with holes

**Steps**:

1. **Check console logs**:
```bash
# Look for:
[AI] GPT-5.2 grid response: {"width": 5, "height": 5, ...}
```

2. **Verify size hints were passed**:
```typescript
// Add log in extractGridFromImage (line 267)
console.log('[DEBUG] Size hint:', sizeHint);
```

3. **Check if hint is in prompt**:
```typescript
// Should see in console:
IMPORTANT SIZE HINTS (from user):
- Grid dimensions: 7 columns × 9 rows
```

4. **If hint not passed, trace back**:
```typescript
// index.tsx handleSizeHintConfirm
console.log('[DEBUG] Hint confirmed:', cols, rows, dominoCount);

// index.tsx handleDualCropperComplete
console.log('[DEBUG] Passing hint to extraction:', pendingSizeHint);
```

5. **If hint passed but ignored**:
   - AI may have strong visual cues contradicting hint
   - Try stronger prompt language: "The grid MUST be exactly..."
   - Or post-process: force resize grid after extraction

## Validation After Extraction

After AI returns data, run these checks:

```typescript
// 1. Cell count validation
const totalCells = grid.regions.reduce((sum, r) => sum + r.cells.length, 0);
const expectedCells = sizeHint.dominoCount * 2;

if (totalCells !== expectedCells) {
  console.error(`Cell count mismatch: got ${totalCells}, expected ${expectedCells}`);
}

// 2. Grid dimension validation
if (sizeHint && (grid.width !== sizeHint.cols || grid.height !== sizeHint.rows)) {
  console.error(`Dimension mismatch: got ${grid.width}×${grid.height}, expected ${sizeHint.cols}×${sizeHint.rows}`);
}

// 3. Domino count validation
if (dominoes.length !== sizeHint.dominoCount) {
  console.error(`Domino count mismatch: got ${dominoes.length}, expected ${sizeHint.dominoCount}`);
}

// 4. Constraint value sanity check
for (const region of grid.regions) {
  if (region.constraint_type === 'sum' && region.constraint_value) {
    const maxPossible = region.size * 6; // Max pip value is 6
    if (region.constraint_value > maxPossible) {
      console.warn(`Impossible sum: region size ${region.size} can't sum to ${region.constraint_value}`);
    }
  }
}
```

## Performance Optimization

### Reduce Image Size Before Sending

Large images = slow API calls + high token costs.

```typescript
// Add image compression before base64 conversion
import { manipulateAsync, SaveFormat } from 'expo-image-manipulator';

async function compressImage(uri: string): Promise<string> {
  const compressed = await manipulateAsync(
    uri,
    [{ resize: { width: 1024 } }], // Max width 1024px
    { compress: 0.8, format: SaveFormat.JPEG }
  );
  return compressed.uri;
}
```

Use before extraction:
```typescript
const compressedUri = await compressImage(imageUri);
const base64 = await FileSystem.readAsStringAsync(compressedUri, {
  encoding: FileSystem.EncodingType.Base64,
});
```

### Cache Repeated Extractions

If user re-extracts same image:

```typescript
const extractionCache = new Map<string, PuzzleData>();

// Key by image hash
const imageHash = await crypto.digest('SHA-256', base64Image);

if (extractionCache.has(imageHash)) {
  console.log('[Cache] Returning cached extraction');
  return extractionCache.get(imageHash)!;
}

// ... do extraction ...

extractionCache.set(imageHash, result);
```

## Best Practices

1. **Always provide size hints** when possible
   - Dramatically improves accuracy
   - User knows dimensions from puzzle context

2. **Use dual image cropping**
   - Cleaner images = better extraction
   - Separate concerns (dominoes vs grid)

3. **Log everything during debug**
   - Raw AI responses
   - Parsed structures
   - Validation failures

4. **Test with known puzzles first**
   - Use `createSamplePuzzle()` to verify solver works
   - Then test extraction on real images

5. **Handle API errors gracefully**
   - Add retries for transient failures
   - Show user-friendly error messages
   - Don't lose user's image if extraction fails

6. **Validate aggressively**
   - Check cell counts match
   - Verify constraints are possible
   - Confirm regions are contiguous
