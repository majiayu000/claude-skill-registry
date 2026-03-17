---
name: benchmark-fetcher
description: Fetch benchmark performance data from 6 leaderboard websites using Playwright MCP and update model manifests with the latest scores. Supports SWE-bench, TerminalBench, SciCode, LiveCodeBench, MMMU, MMMU Pro, and WebDevArena benchmarks.
---

# Benchmark Fetcher Skill

Automate the fetching of benchmark performance data from leaderboard websites and update model manifests with the latest scores using advanced browser automation.

## Overview

This skill extends benchmark data collection by automating visits to 6 major AI model leaderboard websites, extracting performance scores, and updating model manifests in `manifests/models/` with the latest benchmark data.

**Key Features:**
- **Automated Data Collection**: Uses Playwright MCP to visit and extract data from 6 leaderboard websites
- **Intelligent Model Mapping**: Maps website model names to manifest IDs using configurable mappings
- **Always Overwrite**: Updates manifests with latest benchmark values
- **Error Resilient**: Retry logic with exponential backoff and graceful degradation
- **Comprehensive Reporting**: Detailed completion reports with unmapped models and update statistics

## Supported Benchmarks

| Benchmark | Website | Manifest Field | Format |
|-----------|---------|----------------|--------|
| **SWE-bench** | https://www.swebench.com | `sweBench` | Percentage (0-100) |
| **TerminalBench** | https://www.tbench.ai/leaderboard/terminal-bench/2.0 | `terminalBench` | Decimal (0-1) |
| **MMMU** | https://mmmu-benchmark.github.io/#leaderboard | `mmmu`, `mmmuPro` | Percentage (0-100) |
| **SciCode** | https://scicode-bench.github.io/leaderboard/ | `sciCode` | Percentage (0-100) |
| **LiveCodeBench** | https://livecodebench.github.io/leaderboard.html | `liveCodeBench` | Percentage (0-100) |
| **WebDevArena** | https://web.lmarena.ai/leaderboard | `webDevArena` | Percentage (0-100) |

**Note:** TerminalBench uses a decimal format (0-1 scale), while all other benchmarks use percentage format (0-100 scale).

## Usage

### Fetch All Benchmarks

Update all model manifests with latest benchmark data from all 6 websites:

```bash
node .claude/skills/benchmark-fetcher/scripts/fetch-benchmarks.mjs
```

### Fetch Specific Benchmarks

Update only specific benchmarks:

```bash
# Fetch only SWE-bench and TerminalBench
node .claude/skills/benchmark-fetcher/scripts/fetch-benchmarks.mjs --benchmarks swebench,terminalBench

# Fetch only LiveCodeBench
node .claude/skills/benchmark-fetcher/scripts/fetch-benchmarks.mjs --benchmarks liveCodeBench
```

### Fetch for Specific Models

Update benchmarks for specific models only:

```bash
# Update only Claude Sonnet 4.5 and GPT-4o
node .claude/skills/benchmark-fetcher/scripts/fetch-benchmarks.mjs --models claude-sonnet-4-5,gpt-4o
```

### Dry Run Mode

Preview what would be updated without actually modifying manifests:

```bash
node .claude/skills/benchmark-fetcher/scripts/fetch-benchmarks.mjs --dry-run
```

## Model Name Mapping

### How Mapping Works

Each benchmark website uses different naming conventions for models. The `references/model-name-mappings.json` file maps website-specific model names to manifest IDs.

**Example mapping:**

```json
{
  "swebench": {
    "websiteModels": {
      "Claude Sonnet 4.5": "claude-sonnet-4-5",
      "GPT-4o": "gpt-4o",
      "Gemini 2.5 Pro": "gemini-2-5-pro"
    }
  }
}
```

### Mapping Strategy

The mapper uses a 3-tier fallback strategy:

1. **Exact match** (case-sensitive): "Claude Sonnet 4.5" → "claude-sonnet-4-5"
2. **Case-insensitive match**: "claude sonnet 4.5" → "claude-sonnet-4-5"
3. **Fuzzy match** (normalized): "Claude-Sonnet-4.5" → "claude-sonnet-4-5"

**Normalization:** Removes spaces, hyphens, and special characters for fuzzy matching.

### Adding New Mappings

When the script reports unmapped models, add them to `references/model-name-mappings.json`:

```json
{
  "swebench": {
    "websiteModels": {
      "New Model Name": "new-model-id"
    }
  }
}
```

## Data Extraction Process

### High-Level Workflow

1. **Load Configuration**: Read mappings, load all model manifests
2. **Initialize Browser**: Start Chrome DevTools MCP browser instance
3. **Visit Websites**: Sequentially visit each benchmark website
4. **Extract Data**: Parse leaderboard tables from page snapshots
5. **Map Models**: Match website model names to manifest IDs
6. **Update Manifests**: Overwrite benchmark values in manifest files
7. **Generate Report**: Show updates, failures, and unmapped models

### Website-Specific Extractors

Each benchmark has a dedicated extractor function in `scripts/lib/benchmark-extractors.mjs`:

- `extractSWEBench()` - Extracts SWE-bench Verified scores
- `extractTerminalBench()` - Extracts TerminalBench 2.0 accuracy (decimal format)
- `extractMMMU()` - Extracts both MMMU and MMMU Pro scores
- `extractSciCode()` - Extracts SciCode benchmark scores
- `extractLiveCodeBench()` - Extracts LiveCodeBench Pass@1 scores
- `extractWebDevArena()` - Extracts WebDevArena scores

### Special Cases

**TerminalBench Format:**
- Website displays percentages (42.8%)
- Must store as decimal: `0.428` (not `42.8`)
- Extractor handles conversion automatically

**MMMU Dual Benchmarks:**
- Single website has both MMMU and MMMU Pro leaderboards
- Extractor returns both in one visit:
  ```javascript
  {
    mmmu: Map<manifestId, score>,
    mmmuPro: Map<manifestId, score>
  }
  ```

## Update Strategy

### Always Overwrite Policy

The skill uses an **always overwrite** strategy for benchmark values:

- Existing benchmark values are replaced with latest data from websites
- Null values are populated if found on websites
- Non-null values are updated with latest scores
- No confirmation or comparison - latest data always wins

**Rationale:** Benchmark scores represent the latest model performance. Websites are the authoritative source.

### What Gets Preserved

Only benchmark fields are updated. All other manifest fields are preserved:

- ✅ Preserved: `id`, `name`, `description`, `vendor`, `size`, `contextWindow`, etc.
- 🔄 Updated: `benchmarks.sweBench`, `benchmarks.terminalBench`, etc.

### Atomic Updates

Manifests are updated using atomic file writes:

1. Validate JSON structure
2. Write to temporary file (`.tmp`)
3. Atomic rename to target file
4. No partial updates - all or nothing

## Error Handling

### Retry Logic

Each benchmark extraction uses a 3-attempt retry strategy with exponential backoff:

**Attempt 1**: Direct extraction (immediate)
**Attempt 2**: Retry after 2 seconds
**Attempt 3**: Final retry after 4 seconds

After 3 failures:
- Take debug screenshot (`/tmp/benchmark-{id}-error.png`)
- Log error details
- Skip benchmark and continue with others

### Error Categories

**Website Access Errors:**
- Cause: Site down, network timeout, rate limiting
- Handling: Retry 3 times, then skip benchmark

**Extraction Errors:**
- Cause: Page structure changed, data not found
- Handling: Screenshot for debugging, skip benchmark

**Mapping Errors:**
- Cause: Model name not in mapping configuration
- Handling: Log unmapped model, continue with others

**Manifest Update Errors:**
- Cause: File write errors, invalid JSON
- Handling: Atomic write protects against corruption, rollback on error

### Graceful Degradation

The skill continues processing even when errors occur:

- If 1 benchmark fails, others still process
- If 1 model can't be mapped, others still update
- Partial success is better than no success
- Completion report shows exactly what succeeded/failed

## Completion Report

After execution, a detailed report shows:

### Summary Section

```
📊 Benchmark Fetch Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Successfully Fetched (5/6 benchmarks)
   ✓ SWE-bench (swebench.com)
   ✓ TerminalBench (tbench.ai)
   ✓ MMMU + MMMU Pro (mmmu-benchmark.github.io)
   ✓ SciCode (scicode-bench.github.io)
   ✓ LiveCodeBench (livecodebench.github.io)

❌ Failed to Fetch (1/6 benchmarks)
   ✗ WebDevArena (web.lmarena.ai)
     Reason: Timeout after 3 retries
```

### Manifest Updates

```
📝 Manifest Updates

✅ Updated: 15 manifests
   • claude-sonnet-4-5: 3 benchmarks updated
     - sweBench: null → 74.4
     - terminalBench: 0.428 → 0.604
     - liveCodeBench: 47.1 → 52.3

   • gpt-4o: 2 benchmarks updated
     - sweBench: 21.62 → 23.5
     - sciCode: 1.5 → 2.1
```

### Unmapped Models

```
⚠️ Unmapped Models (require manual mapping)

SWE-bench:
  • "Qwen-Coder-2.5" → Add to model-name-mappings.json
  • "DeepSeek-Coder-V2" → Add to model-name-mappings.json

Suggestion: Update references/model-name-mappings.json
```

### Statistics

```
📈 Statistics

Total benchmarks fetched:     247 values
Total manifests updated:      15 files
Execution time:               45.2s
Average time per benchmark:   7.5s
```

### Next Steps

```
✅ Complete! Next steps:

1. Review updated manifests in manifests/models/
2. Add unmapped models to references/model-name-mappings.json
3. Retry failed benchmarks if needed
4. Run validation: npm run test:validate
5. Commit changes when satisfied
```

## Tool Integration

### Chrome DevTools MCP

The skill uses Chrome DevTools MCP tools for browser automation:

**Navigation:**
```javascript
await mcp__chrome-devtools__navigate_page({
  url: 'https://www.swebench.com',
  type: 'url'
})
```

**Wait for Content:**
```javascript
await mcp__chrome-devtools__wait_for({
  text: 'Leaderboard'
})
```

**Take Snapshot:**
```javascript
const snapshot = await mcp__chrome-devtools__take_snapshot()
// Parse snapshot.content for leaderboard data
```

**Debug Screenshots:**
```javascript
await mcp__chrome-devtools__take_screenshot({
  filePath: '/tmp/debug-screenshot.png'
})
```

## Best Practices

### Running the Skill

1. **Run during off-peak hours** to avoid rate limiting
2. **Review unmapped models** and update mappings before next run
3. **Validate manifests** after updates: `npm run test:validate`
4. **Check for website changes** if extraction fails repeatedly
5. **Keep mappings updated** as new models appear on leaderboards

### Maintaining Mappings

1. **Check completion reports** for unmapped models
2. **Add mappings immediately** after discovering new models
3. **Use canonical manifest IDs** as mapping targets
4. **Test mappings** with `--models` flag to verify
5. **Document special cases** in mapping file comments

### Troubleshooting

**Extraction fails for a benchmark:**
- Check if website structure changed
- Review debug screenshots in `/tmp/`
- Update extractor logic if needed

**Model not updating:**
- Verify model exists in `manifests/models/`
- Check mapping configuration
- Ensure model appears on leaderboard website

**TerminalBench shows wrong values:**
- Verify decimal format (0.428 not 42.8)
- Check extractor conversion logic
- Validate against website directly

## Files Modified

After running this skill:

1. **Model manifests**: `manifests/models/*.json` - Updated with latest benchmark scores
2. **No other files modified**: The skill only updates benchmark fields in manifests

## Validation

Always validate manifests after updates:

```bash
# Run schema validation
npm run test:validate

# Check JSON formatting
node -c manifests/models/*.json
```

## Next Steps After Execution

1. **Review updates**: Check manifest changes make sense
2. **Update mappings**: Add newly discovered models to `model-name-mappings.json`
3. **Retry failures**: Re-run with `--benchmarks` for failed benchmarks
4. **Validate**: Run `npm run test:validate` to ensure schema compliance
5. **Commit changes**: Commit updated manifests to repository
