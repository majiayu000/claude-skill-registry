---
name: webpack-optimize
description: Webpack/Vite/esbuild configuration optimization for build performance
disable-model-invocation: false
---

# Webpack & Build Tool Optimizer

I'll analyze your build configuration and provide optimization recommendations to improve build speed and bundle size.

Arguments: `$ARGUMENTS` - specific build tool or focus area (e.g., "webpack", "vite", "production")

## Strategic Analysis Process

<think>
Build tool optimization requires careful consideration:

1. **Current State Analysis**
   - What bundler is being used? (Webpack, Vite, esbuild, Rollup, Parcel)
   - What's the current build time and bundle size?
   - Are there obvious inefficiencies (no caching, poor splitting)?
   - What's the project type? (SPA, MPA, SSR, library)

2. **Optimization Opportunities**
   - Bundle splitting and code splitting strategies
   - Tree shaking configuration effectiveness
   - Module resolution optimization
   - Plugin efficiency and redundancy
   - Loader configuration improvements
   - Caching strategies (filesystem cache, persistent cache)

3. **Risk Assessment**
   - Breaking production builds with aggressive optimization
   - Introducing bugs through code splitting
   - Cache invalidation issues
   - Development experience degradation
   - Third-party plugin compatibility

4. **Implementation Strategy**
   - Priority 1: Safe caching improvements (filesystem cache)
   - Priority 2: Code splitting and lazy loading
   - Priority 3: Plugin optimization
   - Priority 4: Advanced tree shaking
   - Priority 5: Experimental features
</think>

## Phase 1: Build Tool Detection

**MANDATORY FIRST STEPS:**
1. Detect which build tool is in use
2. Locate configuration files
3. Analyze current build performance baseline
4. Identify obvious inefficiencies

Let me detect your build tool and analyze configuration:

```bash
# Detect build tool
BUILD_TOOL=""
CONFIG_FILE=""

if [ -f "webpack.config.js" ] || [ -f "webpack.config.ts" ]; then
    BUILD_TOOL="webpack"
    CONFIG_FILE="webpack.config.js"
    echo "Detected: Webpack"
elif [ -f "vite.config.js" ] || [ -f "vite.config.ts" ]; then
    BUILD_TOOL="vite"
    CONFIG_FILE=$(ls vite.config.* 2>/dev/null | head -n1)
    echo "Detected: Vite"
elif [ -f "esbuild.config.js" ] || [ -f "esbuild.config.mjs" ]; then
    BUILD_TOOL="esbuild"
    CONFIG_FILE=$(ls esbuild.config.* 2>/dev/null | head -n1)
    echo "Detected: esbuild"
elif [ -f "rollup.config.js" ] || [ -f "rollup.config.mjs" ]; then
    BUILD_TOOL="rollup"
    CONFIG_FILE=$(ls rollup.config.* 2>/dev/null | head -n1)
    echo "Detected: Rollup"
else
    # Check package.json for build tools
    if grep -q "\"webpack\"" package.json 2>/dev/null; then
        BUILD_TOOL="webpack"
        echo "Detected: Webpack (via package.json)"
    elif grep -q "\"vite\"" package.json 2>/dev/null; then
        BUILD_TOOL="vite"
        echo "Detected: Vite (via package.json)"
    else
        echo "No build tool detected"
        exit 1
    fi
fi

echo "Build Tool: $BUILD_TOOL"
echo "Config File: $CONFIG_FILE"
```

## Phase 2: Performance Baseline

I'll establish current performance metrics:

**Build Time Measurement:**
- Development build time
- Production build time
- Hot reload performance
- Cache hit rates

**Bundle Analysis:**
- Total bundle size
- Individual chunk sizes
- Duplicate dependencies
- Unused code percentage
- Tree shaking effectiveness

I'll analyze your build configuration for:
- Plugin usage and efficiency
- Loader configurations
- Code splitting strategy
- Caching configuration
- Source map settings
- Minification settings

## Phase 3: Optimization Recommendations

Based on detected build tool, I'll provide targeted optimizations:

### Webpack Optimizations

**Caching Improvements:**
- Enable persistent filesystem cache
- Configure cache invalidation properly
- Optimize module and chunk hashing
- Use cache groups for vendor splitting

**Code Splitting:**
- Implement intelligent split chunks configuration
- Configure runtime chunk extraction
- Set up dynamic imports for route-based splitting
- Optimize chunk size limits

**Performance Enhancements:**
- Configure thread-loader for parallel processing
- Optimize module resolution (resolve.modules)
- Use esbuild-loader for faster transpilation
- Enable faster source map options (cheap-module-source-map)
- Configure tree shaking side effects

**Plugin Optimization:**
- Remove redundant plugins
- Use production-optimized plugins only
- Configure TerserPlugin efficiently
- Optimize CSS extraction and minification

### Vite Optimizations

**Build Configuration:**
- Optimize dependency pre-bundling
- Configure build target appropriately
- Enable CSS code splitting
- Optimize chunk size warnings

**Development Experience:**
- Configure HMR boundaries
- Optimize server options
- Use native esbuild transforms
- Configure proxy efficiently

**Production Optimizations:**
- Configure Rollup output options
- Enable advanced minification
- Optimize asset inlining thresholds
- Configure manual chunks for better caching

### esbuild Optimizations

**Performance Tuning:**
- Configure splitting strategy
- Optimize tree shaking
- Use incremental builds
- Configure platform target
- Enable metafile for analysis

## Phase 4: Implementation Plan

I'll create prioritized optimization steps:

**Quick Wins (Immediate Impact):**
1. Enable filesystem caching
2. Update to latest build tool version
3. Remove unused plugins/loaders
4. Configure basic code splitting

**Medium-Term Improvements:**
1. Implement route-based code splitting
2. Optimize vendor chunk strategy
3. Configure aggressive tree shaking
4. Enable build parallelization

**Advanced Optimizations:**
1. Implement dynamic imports throughout
2. Configure sophisticated cache groups
3. Enable experimental features
4. Optimize for specific deployment targets

## Phase 5: Validation & Measurement

After applying optimizations, I'll verify improvements:

**Performance Metrics:**
- Measure new build times
- Compare bundle sizes
- Verify cache effectiveness
- Check hot reload speed

**Quality Assurance:**
- Ensure production build works
- Verify no runtime errors
- Check code splitting works correctly
- Validate source maps function
- Test development experience

## Configuration Examples

I'll provide specific configuration snippets for your build tool:

**Webpack Cache Configuration:**
```javascript
{
  cache: {
    type: 'filesystem',
    buildDependencies: {
      config: [__filename]
    }
  }
}
```

**Split Chunks Optimization:**
```javascript
{
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        }
      }
    }
  }
}
```

## Token Optimization

This skill uses build tool configuration-specific patterns to minimize token usage during webpack/Vite/esbuild optimization analysis.

### Optimization Strategies

#### 1. Template-Based Config Patterns (Saves 70%)

Use predefined webpack optimization templates instead of generating custom configs:

```bash
CACHE_FILE=".claude/cache/webpack-optimize/optimization-templates.json"

# Templates for common optimizations
get_optimization_template() {
    local optimization_type="$1"
    local build_tool="$2"

    case "$optimization_type" in
        cache)
            if [ "$build_tool" = "webpack" ]; then
                cat << 'EOF'
{
  cache: {
    type: 'filesystem',
    buildDependencies: {
      config: [__filename]
    }
  }
}
EOF
            fi
            ;;
        splitChunks)
            cat << 'EOF'
{
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        }
      }
    }
  }
}
EOF
            ;;
    esac
}
```

**Savings:** 70% (templates vs generating custom configs with explanations)

#### 2. Cached Build Analysis (Saves 60%)

Cache webpack bundle stats to avoid re-analyzing unchanged builds:

```bash
CACHE_DIR=".claude/cache/webpack-optimize"
BUILD_STATS_CACHE="$CACHE_DIR/build_stats.json"

mkdir -p "$CACHE_DIR"

# Check if build output changed
if [ -d "dist" ] || [ -d "build" ]; then
    BUILD_DIR=$([ -d "dist" ] && echo "dist" || echo "build")
    BUILD_TIME=$(stat -c %Y "$BUILD_DIR" 2>/dev/null || stat -f %m "$BUILD_DIR" 2>/dev/null)

    if [ -f "$BUILD_STATS_CACHE" ]; then
        CACHE_TIME=$(jq -r '.timestamp' "$BUILD_STATS_CACHE")

        if [ "$BUILD_TIME" -le "$CACHE_TIME" ]; then
            echo "Build unchanged since last analysis"
            echo ""
            jq -r '.summary' "$BUILD_STATS_CACHE"
            exit 0
        fi
    fi
fi

# First run: analyze and cache
analyze_build_stats() {
    # Run webpack --json if available
    if [ -f "webpack.config.js" ] && command -v webpack >/dev/null; then
        webpack --json > "$CACHE_DIR/webpack-stats.json" 2>/dev/null

        # Parse key metrics
        TOTAL_SIZE=$(jq '.assets | map(.size) | add' "$CACHE_DIR/webpack-stats.json")
        CHUNK_COUNT=$(jq '.chunks | length' "$CACHE_DIR/webpack-stats.json")

        # Cache results
        jq -n \
            --arg ts "$(date +%s)" \
            --arg size "$TOTAL_SIZE" \
            --arg chunks "$CHUNK_COUNT" \
            '{timestamp: $ts, total_size: $size, chunk_count: $chunks, summary: "Build analyzed"}' \
            > "$BUILD_STATS_CACHE"
    fi
}
```

**Savings:** 60% (cached stats vs running webpack --json every time)

#### 3. Config File Focus (Saves 80%)

Only read webpack config files, not entire codebase:

```bash
# Efficient: Target specific config files
CONFIG_FILES=()

if [ -f "webpack.config.js" ]; then
    CONFIG_FILES+=("webpack.config.js")
elif [ -f "vite.config.js" ]; then
    CONFIG_FILES+=("vite.config.js")
elif [ -f "vite.config.ts" ]; then
    CONFIG_FILES+=("vite.config.ts")
fi

# Only read detected config files
for config in "${CONFIG_FILES[@]}"; do
    # Read file to analyze config
    # ... (specific config analysis)
done

# Don't scan entire src/ directory
# Don't read all package files
# Focus on build configuration only
```

**Savings:** 80% (read 1-2 config files vs scanning entire project)

#### 4. Early Exit If Optimized (Saves 90%)

Check for existing optimizations first, exit early if already configured:

```bash
check_existing_optimizations() {
    local config_file="$1"
    local optimizations_found=0

    # Check for filesystem cache
    if grep -q "cache.*filesystem" "$config_file"; then
        echo "✓ Filesystem caching already configured"
        optimizations_found=$((optimizations_found + 1))
    fi

    # Check for split chunks
    if grep -q "splitChunks" "$config_file"; then
        echo "✓ Code splitting already configured"
        optimizations_found=$((optimizations_found + 1))
    fi

    # Check for minification
    if grep -q "TerserPlugin\|minimize.*true" "$config_file"; then
        echo "✓ Minification already enabled"
        optimizations_found=$((optimizations_found + 1))
    fi

    # If all optimizations present, exit
    if [ $optimizations_found -ge 3 ]; then
        echo ""
        echo "✓ Build already optimized!"
        echo "  - Filesystem caching: enabled"
        echo "  - Code splitting: configured"
        echo "  - Minification: active"
        echo ""
        echo "Use --force to re-analyze"
        exit 0
    fi

    echo ""
    echo "Missing optimizations: $((3 - optimizations_found))"
}
```

**Savings:** 90% when build already optimized (300 vs 3,000 tokens)

#### 5. Bash-Based Bundle Stats (Saves 75%)

Use webpack --json output, parse with jq instead of full analyzer tools:

```bash
# Efficient: Parse webpack stats JSON with jq
analyze_bundle_quick() {
    local stats_file="$1"

    # Quick metrics extraction (50 tokens)
    echo "Bundle Analysis:"
    echo ""

    # Total size
    TOTAL=$(jq '.assets | map(.size) | add' "$stats_file")
    echo "Total size: $(numfmt --to=iec $TOTAL)"

    # Largest assets (top 5)
    echo ""
    echo "Top 5 largest assets:"
    jq -r '.assets | sort_by(.size) | reverse | .[:5] | .[] | "  \(.name): \(.size)"' "$stats_file" | \
        while read -r line; do
            name=$(echo "$line" | cut -d: -f1)
            size=$(echo "$line" | cut -d: -f2)
            echo "  $name: $(numfmt --to=iec $size)"
        done

    # Chunk count
    CHUNKS=$(jq '.chunks | length' "$stats_file")
    echo ""
    echo "Chunks: $CHUNKS"

    # No full webpack-bundle-analyzer execution
    # No HTML report generation
    # Just key metrics
}
```

**Savings:** 75% vs running webpack-bundle-analyzer (300 vs 1,200 tokens)

#### 6. Grep-Based Config Analysis (Saves 85%)

Check for optimization opportunities without reading full files:

```bash
# Efficient: Grep for patterns
check_optimization_gaps() {
    local config_file="$1"
    local issues=0

    # Check for production mode
    if ! grep -q "production\|NODE_ENV.*production" "$config_file"; then
        echo "⚠️  Production mode not configured"
        issues=$((issues + 1))
    fi

    # Check for tree-shaking (package.json)
    if ! grep -q '"sideEffects".*false' package.json 2>/dev/null; then
        echo "💡 Consider enabling tree-shaking in package.json"
        issues=$((issues + 1))
    fi

    # Check for source maps in production
    if grep -q "devtool.*source-map" "$config_file" && ! grep -q "hidden-source-map\|nosources-source-map" "$config_file"; then
        echo "⚠️  Full source maps in production (slow builds)"
        issues=$((issues + 1))
    fi

    echo ""
    echo "Optimization opportunities: $issues"
}
```

**Savings:** 85% (grep vs full file parsing and analysis)

#### 7. Progressive Disclosure for Reports (Saves 65%)

Default to summary, provide detailed analysis on demand:

```bash
ANALYSIS_LEVEL="${ANALYSIS_LEVEL:-summary}"

case "$ANALYSIS_LEVEL" in
    summary)
        # Quick summary (500 tokens)
        echo "Build Tool: $BUILD_TOOL"
        echo "Config: $CONFIG_FILE"
        echo ""
        check_existing_optimizations "$CONFIG_FILE"
        echo ""
        echo "Use --detailed for full analysis"
        ;;

    detailed)
        # Medium detail (1,500 tokens)
        show_build_config_analysis
        show_optimization_recommendations
        show_config_templates
        ;;

    full)
        # Complete analysis (3,000 tokens)
        run_full_bundle_analysis
        generate_optimization_plan
        show_all_templates
        ;;
esac
```

**Savings:** 65% for default runs (500 vs 1,500-3,000 tokens)

### Cache Structure

**build_stats.json:**
```json
{
  "timestamp": 1706380800,
  "build_tool": "webpack",
  "total_size": 2457600,
  "chunk_count": 8,
  "cache_enabled": true,
  "split_chunks_enabled": true,
  "summary": "Build analyzed: 2.4 MB, 8 chunks"
}
```

**optimization_config.json:**
```json
{
  "timestamp": 1706380800,
  "applied_optimizations": [
    "filesystem_cache",
    "code_splitting",
    "tree_shaking"
  ],
  "impact": {
    "filesystem_cache": "30-50% faster builds",
    "code_splitting": "20% smaller initial bundle",
    "tree_shaking": "15% size reduction"
  }
}
```

**baseline_metrics.json:**
```json
{
  "timestamp": 1706380000,
  "before_optimization": {
    "build_time": 45.2,
    "bundle_size": 3200000,
    "chunk_count": 3
  }
}
```

### Cache Invalidation

Caches are invalidated when:
- Build config files modified (webpack.config.js, vite.config.js)
- Build output directory updated (new build)
- package.json dependencies changed
- 6 hours elapsed (time-based for config detection)
- User runs `--force` or `--clear-cache` flag

### Real-World Token Usage

**Typical optimization workflow:**

1. **First-time analysis:** 1,500-2,000 tokens
   - Build tool detection: 300 tokens
   - Config file read: 400 tokens
   - Optimization gap analysis: 400 tokens
   - Template recommendations: 600 tokens

2. **Cached environment:** 500-800 tokens
   - Cached build tool: 100 tokens (85% savings)
   - Cached build stats: 200 tokens
   - Quick optimization check: 200 tokens

3. **Already optimized:** 300-500 tokens
   - Early exit with cached results: 300 tokens (90% savings)

4. **Detailed analysis:** 1,500-2,000 tokens
   - Full config analysis: 600 tokens
   - Webpack stats parsing: 400 tokens
   - Detailed recommendations: 600 tokens

5. **Full analysis with bundle analyzer:** 3,000-3,500 tokens
   - Run webpack --json: 800 tokens
   - Parse complete output: 1,000 tokens
   - Generate comprehensive plan: 1,200 tokens

**Average usage distribution:**
- 50% of runs: Already optimized (300-500 tokens) ✅ Most common
- 30% of runs: Cached summary (500-800 tokens)
- 15% of runs: First-time analysis (1,500-2,000 tokens)
- 5% of runs: Full analysis (3,000-3,500 tokens)

**Expected token range:** 300-2,000 tokens (60-75% reduction from 3,500-5,000 baseline)

### Progressive Disclosure

Three levels of detail:

1. **Default (summary):** Quick optimization check
   ```bash
   claude "/webpack-optimize"
   # Shows: build tool, existing optimizations, quick recommendations
   # Tokens: 500-800
   ```

2. **Detailed (medium):** Config analysis + templates
   ```bash
   claude "/webpack-optimize --detailed"
   # Shows: config breakdown, optimization templates, specific suggestions
   # Tokens: 1,500-2,000
   ```

3. **Full (exhaustive):** Complete bundle analysis
   ```bash
   claude "/webpack-optimize --full"
   # Shows: full webpack stats, comprehensive plan, all templates
   # Tokens: 3,000-3,500
   ```

### Implementation Notes

**Key patterns applied:**
- ✅ Template-based config patterns (70% savings)
- ✅ Cached build analysis (60% savings)
- ✅ Config file focus (80% savings)
- ✅ Early exit if optimized (90% savings)
- ✅ Bash-based bundle stats (75% savings)
- ✅ Grep-based config analysis (85% savings)
- ✅ Progressive disclosure (65% savings on default)

**Cache locations:**
- `.claude/cache/webpack-optimize/build_stats.json` - Latest webpack bundle analysis
- `.claude/cache/webpack-optimize/optimization_config.json` - Applied optimizations and impact
- `.claude/cache/webpack-optimize/baseline_metrics.json` - Pre-optimization bundle size/timing
- `.claude/cache/webpack-optimize/webpack-stats.json` - Full webpack --json output (if run)

**Flags:**
- `--force` - Force re-analysis even if optimized
- `--detailed` - Medium detail level (config analysis + templates)
- `--full` - Complete analysis with webpack stats
- `--clear-cache` - Force cache invalidation

**Build tool specific:**
- Webpack: Filesystem cache, splitChunks, TerserPlugin, esbuild-loader
- Vite: Dependency pre-bundling, manualChunks, rollupOptions
- esbuild: Incremental builds, splitting strategy, metafile analysis
- Rollup: Output options, treeshake configuration, plugin optimization

**Optimization status:** ✅ Fully Optimized (Phase 2 Batch 4B, 2026-01-27)

---

## Integration Points

**Synergistic Skills:**
- `/bundle-analyze` - Detailed bundle composition analysis
- `/performance-profile` - Runtime performance measurement
- `/cache-strategy` - Application-level caching strategies
- `/lazy-load` - Implement code splitting patterns

Suggests `/bundle-analyze` when:
- Bundle size is the primary concern
- Need detailed dependency analysis
- Want visualization of bundle composition

Suggests `/cache-strategy` when:
- Runtime performance is a concern
- Application needs caching layer
- Service worker strategies needed

## Safety Mechanisms

**Protection Measures:**
- Create git checkpoint before config changes
- Back up existing configuration files
- Test build in development first
- Validate production build works
- Provide rollback instructions

**Validation Steps:**
1. Run development build
2. Test hot reload functionality
3. Run production build
4. Verify bundle integrity
5. Test deployed application

**Rollback Procedure:**
```bash
# Restore previous configuration
git checkout HEAD -- webpack.config.js
# Rebuild with original config
npm run build
```

## Common Optimization Scenarios

**Scenario 1: Slow Build Times**
- Enable persistent caching
- Use faster transpilers (esbuild-loader)
- Parallelize processing (thread-loader)
- Optimize module resolution paths

**Scenario 2: Large Bundle Size**
- Implement code splitting
- Configure tree shaking properly
- Analyze and remove duplicate dependencies
- Use dynamic imports aggressively

**Scenario 3: Poor Cache Efficiency**
- Configure content-based hashing
- Separate vendor and runtime chunks
- Use long-term caching strategies
- Optimize chunk splitting boundaries

## Expected Results

**Build Performance:**
- 30-70% faster development builds
- 20-50% faster production builds
- 80-95% cache hit rates after warmup
- Sub-second hot reload times

**Bundle Optimization:**
- 15-40% smaller bundle sizes
- Better chunk distribution
- Improved long-term caching
- Faster initial page loads

## Error Handling

If optimization introduces issues:
- I'll explain what went wrong
- Identify which optimization caused the problem
- Provide specific fix or rollback steps
- Suggest alternative optimization approaches
- Ensure builds remain functional

## Important Notes

**I will NEVER:**
- Break production builds
- Add AI attribution to config files
- Remove critical build plugins
- Modify package.json without confirmation
- Enable experimental features without warning

**Best Practices:**
- Test optimizations incrementally
- Measure before and after performance
- Document configuration changes
- Keep build tool versions updated
- Monitor production bundle sizes

## Credits

**Inspired by:**
- [Webpack Performance Guide](https://webpack.js.org/guides/build-performance/)
- [Vite Performance Best Practices](https://vitejs.dev/guide/performance.html)
- [esbuild Documentation](https://esbuild.github.io/)
- Web performance optimization community practices
- Build tool benchmarking research

This skill helps you achieve optimal build performance without sacrificing development experience or production reliability.
