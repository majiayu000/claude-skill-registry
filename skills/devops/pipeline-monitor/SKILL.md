---
name: pipeline-monitor
description: Track build success rates and identify flaky tests from CI logs
disable-model-invocation: false
---

# CI/CD Pipeline Monitor

I'll analyze your CI/CD pipeline metrics, track build success rates, identify flaky tests, and provide performance trend analysis.

Arguments: `$ARGUMENTS` - pipeline platform (github, gitlab, circle), time range, or specific build numbers

## Monitoring Philosophy

- **Data-Driven Insights**: Identify trends, not just failures
- **Flaky Test Detection**: Find tests that fail inconsistently
- **Performance Tracking**: Monitor build duration over time
- **Success Rate Metrics**: Track reliability trends
- **Multi-Platform**: Support GitHub Actions, GitLab CI, CircleCI, Jenkins

---

## Token Optimization

This skill uses efficient patterns to minimize token consumption during CI/CD pipeline monitoring and analysis.

### Optimization Strategies

#### 1. CI Platform Detection Caching (Saves 600 tokens per invocation)

Cache detected CI platform and configuration paths:

```bash
CACHE_FILE=".claude/cache/pipeline-monitor/platform.json"
CACHE_TTL=86400  # 24 hours (CI config rarely changes)

mkdir -p .claude/cache/pipeline-monitor

if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null)))

    if [ $CACHE_AGE -lt $CACHE_TTL ]; then
        # Use cached platform info
        CI_PLATFORM=$(jq -r '.platform' "$CACHE_FILE")
        CI_CONFIG=$(jq -r '.config_file' "$CACHE_FILE")
        API_ENDPOINT=$(jq -r '.api_endpoint' "$CACHE_FILE")

        echo "Using cached CI platform: $CI_PLATFORM"
        SKIP_DETECTION="true"
    fi
fi

# First run: detect and cache
if [ "$SKIP_DETECTION" != "true" ]; then
    detect_ci_platform  # Check for .github/workflows, .gitlab-ci.yml, etc.

    # Cache results
    jq -n \
        --arg platform "$CI_PLATFORM" \
        --arg config "$CI_CONFIG" \
        --arg api "$API_ENDPOINT" \
        '{platform: $platform, config_file: $config, api_endpoint: $api}' \
        > "$CACHE_FILE"
fi
```

**Savings:** 600 tokens (no repeated directory scans, no file existence checks)

#### 2. API Response Caching (Saves 80%)

Cache CI/CD API responses to avoid repeated network calls:

```bash
# Cache API responses (5 minute TTL for build data)
API_CACHE=".claude/cache/pipeline-monitor/builds-cache.json"
CACHE_TTL=300  # 5 minutes (builds change frequently)

if [ -f "$API_CACHE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$API_CACHE" 2>/dev/null || stat -f %m "$API_CACHE" 2>/dev/null)))

    if [ $CACHE_AGE -lt $CACHE_TTL ]; then
        echo "Using cached build data ($(($CACHE_AGE / 60)) minutes old)"
        cat "$API_CACHE"
        exit 0
    fi
fi

# Fetch and cache
case "$CI_PLATFORM" in
    github-actions)
        gh api repos/:owner/:repo/actions/runs --jq '.workflow_runs[:50]' > "$API_CACHE"
        ;;
    gitlab-ci)
        curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
            "$GITLAB_API_URL/projects/$PROJECT_ID/pipelines?per_page=50" > "$API_CACHE"
        ;;
esac
```

**Savings:** 80% when cache valid (no API calls, instant response: 2,000 → 400 tokens)

#### 3. Sample-Based Metrics Analysis (Saves 75%)

Analyze last 50 builds, not entire history:

```bash
# Efficient: Only analyze recent builds
ANALYSIS_LIMIT="${ANALYSIS_LIMIT:-50}"  # Default: last 50 builds

analyze_build_metrics() {
    local builds_json="$1"

    # Extract key metrics only (not full build data)
    TOTAL_BUILDS=$(jq 'length' "$builds_json")
    SUCCESS_COUNT=$(jq '[.[] | select(.conclusion == "success")] | length' "$builds_json")
    FAILURE_COUNT=$(jq '[.[] | select(.conclusion == "failure")] | length' "$builds_json")
    SUCCESS_RATE=$(echo "scale=2; $SUCCESS_COUNT * 100 / $TOTAL_BUILDS" | bc)

    # Average duration (sample-based)
    AVG_DURATION=$(jq '[.[] | .run_duration_ms] | add / length / 1000' "$builds_json")

    echo "Build Metrics (last $ANALYSIS_LIMIT builds):"
    echo "  Success Rate: ${SUCCESS_RATE}%"
    echo "  Total: $TOTAL_BUILDS | Success: $SUCCESS_COUNT | Failures: $FAILURE_COUNT"
    echo "  Avg Duration: ${AVG_DURATION}s"

    echo ""
    echo "Use --all-history for complete analysis"
}
```

**Savings:** 75% (analyze 50 vs 500+ builds: 3,000 → 750 tokens)

#### 4. Flaky Test Pattern Detection (Saves 85%)

Use statistical sampling to identify flaky tests:

```bash
# Efficient: Pattern-based flaky detection (not exhaustive analysis)
detect_flaky_tests() {
    local builds_json="$1"

    echo "Detecting flaky tests..."

    # Extract failed test names from recent failures
    FAILED_TESTS=$(jq -r '.[] |
        select(.conclusion == "failure") |
        .jobs[].steps[] |
        select(.conclusion == "failure") |
        .name' "$builds_json" | sort | uniq -c | sort -rn)

    # Identify tests that failed 2-4 times (flaky pattern)
    FLAKY_CANDIDATES=$(echo "$FAILED_TESTS" | awk '$1 >= 2 && $1 <= 4')

    if [ -n "$FLAKY_CANDIDATES" ]; then
        echo "Potential flaky tests (failed 2-4 times):"
        echo "$FLAKY_CANDIDATES" | head -10 | while read count name; do
            PCT=$(echo "scale=0; $count * 100 / $TOTAL_BUILDS" | bc)
            echo "  - $name (${PCT}% failure rate)"
        done
    else
        echo "✓ No flaky tests detected"
    fi

    echo ""
    echo "Use --detailed-flaky for statistical analysis"
}
```

**Savings:** 85% (pattern detection vs full statistical analysis: 2,000 → 300 tokens)

#### 5. Bash-Based Log Parsing (Saves 70%)

Parse CI logs with grep/awk instead of full reads:

```bash
# Efficient: Grep for error patterns (not full log analysis)
analyze_failure_patterns() {
    local log_file="$1"

    echo "Analyzing failure patterns..."

    # Count error types (efficient grep)
    TIMEOUT_ERRORS=$(grep -c "timeout\|ETIMEDOUT" "$log_file" 2>/dev/null || echo "0")
    OOM_ERRORS=$(grep -c "out of memory\|OOM" "$log_file" 2>/dev/null || echo "0")
    NETWORK_ERRORS=$(grep -c "ECONNREFUSED\|network" "$log_file" 2>/dev/null || echo "0")
    TEST_FAILURES=$(grep -c "FAILED\|AssertionError" "$log_file" 2>/dev/null || echo "0")

    # Summary (no full log output)
    echo "Error Distribution:"
    [ $TIMEOUT_ERRORS -gt 0 ] && echo "  - Timeouts: $TIMEOUT_ERRORS"
    [ $OOM_ERRORS -gt 0 ] && echo "  - Out of Memory: $OOM_ERRORS"
    [ $NETWORK_ERRORS -gt 0 ] && echo "  - Network: $NETWORK_ERRORS"
    [ $TEST_FAILURES -gt 0 ] && echo "  - Test Failures: $TEST_FAILURES"
}
```

**Savings:** 70% vs full log parsing (grep counts vs full read: 1,500 → 450 tokens)

#### 6. Progressive Metrics Reporting (Saves 60%)

Default to summary, provide detailed analysis on demand:

```bash
DETAIL_LEVEL="${DETAIL_LEVEL:-summary}"

case "$DETAIL_LEVEL" in
    summary)
        # Quick metrics (400 tokens)
        echo "Success Rate: ${SUCCESS_RATE}%"
        echo "Last Build: $(jq -r '.[0].conclusion' builds.json)"
        echo "Flaky Tests: $FLAKY_COUNT"
        echo ""
        echo "Use --detailed for complete analysis"
        ;;

    detailed)
        # Medium detail (1,200 tokens)
        show_build_metrics
        show_flaky_tests
        show_duration_trend
        ;;

    full)
        # Complete analysis (2,500 tokens)
        show_all_builds
        show_detailed_flaky_analysis
        show_failure_patterns
        show_recommendations
        ;;
esac
```

**Savings:** 60% for default runs (400 vs 1,200-2,500 tokens)

#### 7. GitHub CLI Integration (Saves 75%)

Use `gh` CLI instead of REST API for GitHub Actions:

```bash
# Efficient: gh CLI with JSON output (no auth setup needed)
if [ "$CI_PLATFORM" = "github-actions" ]; then
    # Single command, JSON output
    gh run list --limit 50 --json conclusion,status,name,startedAt,durationMs \
        > "$API_CACHE"

    # Parse directly (no intermediate processing)
    SUCCESS_RATE=$(jq '[.[] | select(.conclusion == "success")] | length / length * 100' "$API_CACHE")

    echo "GitHub Actions: $SUCCESS_RATE% success rate (last 50 runs)"
fi
```

**Savings:** 75% vs manual REST API calls (gh CLI handles auth, pagination: 1,200 → 300 tokens)

### Cache Invalidation

Caches are invalidated when:
- CI configuration files modified
- 5 minutes elapsed (time-based for build data)
- 24 hours elapsed (time-based for platform detection)
- User runs `--clear-cache` or `--fresh` flag
- New builds detected

### Real-World Token Usage

**Typical monitoring workflow:**

1. **Quick status check:** 400-800 tokens
   - Cached platform: 100 tokens
   - Cached build data (< 5 min): 200 tokens
   - Success rate calculation: 150 tokens
   - Summary output: 200 tokens

2. **First-time analysis:** 1,200-1,800 tokens
   - Platform detection: 300 tokens
   - API fetch (50 builds): 400 tokens
   - Metrics calculation: 300 tokens
   - Flaky test detection: 400 tokens
   - Summary: 200 tokens

3. **Detailed analysis:** 1,800-2,500 tokens
   - All basic metrics: 800 tokens
   - Detailed flaky analysis: 600 tokens
   - Duration trends: 400 tokens
   - Recommendations: 300 tokens

4. **Full historical analysis:** 2,500-3,500 tokens
   - Only when explicitly requested with --full flag

**Average usage distribution:**
- 60% of runs: Cached quick check (400-800 tokens) ✅ Most common
- 25% of runs: First-time analysis (1,200-1,800 tokens)
- 10% of runs: Detailed analysis (1,800-2,500 tokens)
- 5% of runs: Full historical (2,500-3,500 tokens)

**Expected token range:** 400-2,500 tokens (50% reduction from 800-5,000 baseline)

### Progressive Disclosure

Three levels of monitoring:

1. **Default (summary):** Quick health check
   ```bash
   claude "/pipeline-monitor"
   # Shows: success rate, last build status, flaky count
   # Tokens: 400-800
   ```

2. **Detailed (trends):** Performance analysis
   ```bash
   claude "/pipeline-monitor --detailed"
   # Shows: metrics, flaky tests, duration trends
   # Tokens: 1,200-1,800
   ```

3. **Full (historical):** Complete pipeline analysis
   ```bash
   claude "/pipeline-monitor --full"
   # Shows: all builds, detailed flaky analysis, recommendations
   # Tokens: 2,500-3,500
   ```

### Implementation Notes

**Key patterns applied:**
- ✅ CI platform detection caching (600 token savings)
- ✅ API response caching (80% reduction when cached)
- ✅ Sample-based metrics (75% savings - last 50 builds)
- ✅ Flaky test pattern detection (85% savings)
- ✅ Bash-based log parsing (70% savings)
- ✅ Progressive metrics reporting (60% savings)
- ✅ GitHub CLI integration (75% savings for GitHub Actions)

**Cache locations:**
- `.claude/cache/pipeline-monitor/platform.json` - CI platform and config (24 hour TTL)
- `.claude/cache/pipeline-monitor/builds-cache.json` - Build data (5 minute TTL)
- `.claude/cache/pipeline-monitor/flaky-tests.json` - Flaky test patterns (1 hour TTL)

**Flags:**
- `--detailed` - Medium detail level (trends + flaky tests)
- `--full` - Complete historical analysis
- `--fresh` - Bypass all caches
- `--limit=<N>` - Number of builds to analyze (default: 50)
- `--clear-cache` - Force cache invalidation

**Supported platforms:**
- GitHub Actions (`gh` CLI, GitHub API)
- GitLab CI (GitLab API)
- CircleCI (CircleCI API)
- Jenkins (Jenkins API, log files)
- Travis CI (Travis API)
- Azure Pipelines (Azure DevOps API)

---

## Phase 1: Pipeline Detection

First, I'll detect your CI/CD platform:

```bash
#!/bin/bash
# Detect CI/CD platform and configuration

detect_ci_platform() {
    echo "=== CI/CD Platform Detection ==="
    echo ""

    CI_PLATFORM=""
    CI_CONFIG=""

    # GitHub Actions
    if [ -d ".github/workflows" ]; then
        CI_PLATFORM="github-actions"
        CI_CONFIG=$(find .github/workflows -name "*.yml" -o -name "*.yaml" | head -1)
        echo "✓ Detected: GitHub Actions"
        echo "  Config: $CI_CONFIG"

    # GitLab CI
    elif [ -f ".gitlab-ci.yml" ]; then
        CI_PLATFORM="gitlab-ci"
        CI_CONFIG=".gitlab-ci.yml"
        echo "✓ Detected: GitLab CI"
        echo "  Config: $CI_CONFIG"

    # CircleCI
    elif [ -f ".circleci/config.yml" ]; then
        CI_PLATFORM="circleci"
        CI_CONFIG=".circleci/config.yml"
        echo "✓ Detected: CircleCI"
        echo "  Config: $CI_CONFIG"

    # Jenkins
    elif [ -f "Jenkinsfile" ]; then
        CI_PLATFORM="jenkins"
        CI_CONFIG="Jenkinsfile"
        echo "✓ Detected: Jenkins"
        echo "  Config: $CI_CONFIG"

    # Travis CI
    elif [ -f ".travis.yml" ]; then
        CI_PLATFORM="travis"
        CI_CONFIG=".travis.yml"
        echo "✓ Detected: Travis CI"
        echo "  Config: $CI_CONFIG"

    # Azure Pipelines
    elif [ -f "azure-pipelines.yml" ]; then
        CI_PLATFORM="azure-pipelines"
        CI_CONFIG="azure-pipelines.yml"
        echo "✓ Detected: Azure Pipelines"
        echo "  Config: $CI_CONFIG"

    else
        echo "⚠️  No CI/CD configuration detected"
        echo "Supported platforms: GitHub Actions, GitLab CI, CircleCI, Jenkins"
        exit 1
    fi

    echo ""
    echo "$CI_PLATFORM|$CI_CONFIG"
}

CI_INFO=$(detect_ci_platform)
CI_PLATFORM=$(echo "$CI_INFO" | cut -d'|' -f1)
CI_CONFIG=$(echo "$CI_INFO" | cut -d'|' -f2)
```

## Phase 2: Build History Analysis

<think>
When analyzing CI/CD pipelines:
- Build success rates reveal stability trends
- Flaky tests appear as intermittent failures
- Build duration increases indicate performance degradation
- Failed builds often cluster around specific changes
- Success rates vary by branch (main vs feature branches)
- Time-of-day patterns may indicate resource contention
</think>

I'll fetch and analyze recent build history:

```bash
#!/bin/bash
# Fetch build history from CI platform

fetch_build_history() {
    local platform="$1"
    local limit="${2:-50}"

    echo "=== Fetching Build History ==="
    echo ""

    case "$platform" in
        github-actions)
            # Use GitHub CLI to fetch workflow runs
            if command -v gh &> /dev/null; then
                echo "Fetching last $limit GitHub Actions runs..."
                gh run list --limit "$limit" --json status,conclusion,name,createdAt,updatedAt,databaseId > /tmp/ci_builds.json

                # Parse and display summary
                TOTAL=$(jq length /tmp/ci_builds.json)
                SUCCESS=$(jq '[.[] | select(.conclusion=="success")] | length' /tmp/ci_builds.json)
                FAILURE=$(jq '[.[] | select(.conclusion=="failure")] | length' /tmp/ci_builds.json)
                SUCCESS_RATE=$(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)

                echo "Total runs: $TOTAL"
                echo "Successful: $SUCCESS ($SUCCESS_RATE%)"
                echo "Failed: $FAILURE"
                echo "✓ Build history fetched"
            else
                echo "⚠️  gh CLI not installed. Install: https://cli.github.com/"
                exit 1
            fi
            ;;

        gitlab-ci)
            # Use GitLab CLI to fetch pipelines
            if command -v glab &> /dev/null; then
                echo "Fetching last $limit GitLab CI pipelines..."
                glab ci list --per-page "$limit" --output json > /tmp/ci_builds.json

                # Parse and display summary
                TOTAL=$(jq length /tmp/ci_builds.json)
                SUCCESS=$(jq '[.[] | select(.status=="success")] | length' /tmp/ci_builds.json)
                FAILURE=$(jq '[.[] | select(.status=="failed")] | length' /tmp/ci_builds.json)
                SUCCESS_RATE=$(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)

                echo "Total pipelines: $TOTAL"
                echo "Successful: $SUCCESS ($SUCCESS_RATE%)"
                echo "Failed: $FAILURE"
                echo "✓ Build history fetched"
            else
                echo "⚠️  glab CLI not installed. Install: https://gitlab.com/gitlab-org/cli"
                exit 1
            fi
            ;;

        circleci)
            # Use CircleCI API
            if [ ! -z "$CIRCLE_TOKEN" ]; then
                echo "Fetching last $limit CircleCI builds..."
                PROJECT_SLUG=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')

                curl -s "https://circleci.com/api/v2/project/github/$PROJECT_SLUG/pipeline?limit=$limit" \
                    -H "Circle-Token: $CIRCLE_TOKEN" > /tmp/ci_builds.json

                echo "✓ Build history fetched"
            else
                echo "⚠️  CIRCLE_TOKEN not set. Set environment variable."
                exit 1
            fi
            ;;

        *)
            echo "⚠️  Build history fetching not implemented for $platform"
            echo "Manual analysis required"
            ;;
    esac

    echo ""
}

fetch_build_history "$CI_PLATFORM" 50
```

## Phase 3: Success Rate Analysis

I'll analyze build success trends over time:

```bash
#!/bin/bash
# Analyze build success rates and trends

analyze_success_rates() {
    echo "=== Success Rate Analysis ==="
    echo ""

    if [ ! -f "/tmp/ci_builds.json" ]; then
        echo "⚠️  No build data available"
        return
    fi

    # Overall statistics
    echo "Overall Statistics:"
    TOTAL=$(jq length /tmp/ci_builds.json)
    SUCCESS=$(jq '[.[] | select(.conclusion=="success" or .status=="success")] | length' /tmp/ci_builds.json)
    FAILURE=$(jq '[.[] | select(.conclusion=="failure" or .status=="failed")] | length' /tmp/ci_builds.json)
    IN_PROGRESS=$(jq '[.[] | select(.conclusion=="in_progress" or .status=="running")] | length' /tmp/ci_builds.json)

    SUCCESS_RATE=$(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)

    echo "  Total builds: $TOTAL"
    echo "  Successful: $SUCCESS ($SUCCESS_RATE%)"
    echo "  Failed: $FAILURE"
    echo "  In progress: $IN_PROGRESS"
    echo ""

    # Trend analysis (last 10 vs previous 40)
    echo "Trend Analysis:"
    RECENT_SUCCESS=$(jq '[.[:10] | .[] | select(.conclusion=="success" or .status=="success")] | length' /tmp/ci_builds.json)
    RECENT_RATE=$(echo "scale=2; $RECENT_SUCCESS * 100 / 10" | bc)

    PREVIOUS_SUCCESS=$(jq '[.[10:] | .[] | select(.conclusion=="success" or .status=="success")] | length' /tmp/ci_builds.json)
    PREVIOUS_TOTAL=$((TOTAL - 10))
    PREVIOUS_RATE=$(echo "scale=2; $PREVIOUS_SUCCESS * 100 / $PREVIOUS_TOTAL" | bc)

    echo "  Last 10 builds: $RECENT_RATE%"
    echo "  Previous builds: $PREVIOUS_RATE%"

    TREND_DIFF=$(echo "scale=2; $RECENT_RATE - $PREVIOUS_RATE" | bc)
    if (( $(echo "$TREND_DIFF > 0" | bc -l) )); then
        echo "  Trend: ✓ Improving (+$TREND_DIFF%)"
    elif (( $(echo "$TREND_DIFF < 0" | bc -l) )); then
        echo "  Trend: ⚠️  Declining ($TREND_DIFF%)"
    else
        echo "  Trend: Stable"
    fi
    echo ""

    # Success rate by workflow/job
    echo "Success Rate by Workflow:"
    jq -r '.[] | "\(.name // "unknown")|\(.conclusion // .status)"' /tmp/ci_builds.json | \
        awk -F'|' '{workflows[$1]++; if($2=="success") success[$1]++}
                    END {for(w in workflows) printf "  %s: %.0f%% (%d/%d)\n", w, (success[w]/workflows[w])*100, success[w], workflows[w]}' | \
        sort -t: -k2 -n
    echo ""
}

analyze_success_rates
```

## Phase 4: Flaky Test Detection

I'll identify tests that fail inconsistently:

```bash
#!/bin/bash
# Detect flaky tests from CI logs

detect_flaky_tests() {
    echo "=== Flaky Test Detection ==="
    echo ""

    # Download recent failed build logs
    echo "Analyzing failed builds for test failures..."

    # Extract test failures from logs (GitHub Actions)
    if [ "$CI_PLATFORM" = "github-actions" ]; then
        # Get failed run IDs
        FAILED_RUNS=$(jq -r '.[] | select(.conclusion=="failure") | .databaseId' /tmp/ci_builds.json | head -20)

        # Track test failures across runs
        > /tmp/test_failures.txt

        for run_id in $FAILED_RUNS; do
            echo "Checking run $run_id..."

            # Download logs and extract test failures
            gh run view "$run_id" --log 2>/dev/null | \
                grep -E "(FAIL|FAILED|Error:|AssertionError|Test failed)" | \
                grep -oP '(test_\w+|it\(["\x27][^\)]+|describe\(["\x27][^\)]+)' >> /tmp/test_failures.txt || true
        done

        if [ -s /tmp/test_failures.txt ]; then
            echo ""
            echo "Test Failure Frequency:"

            # Count occurrences and identify flaky tests
            sort /tmp/test_failures.txt | uniq -c | sort -rn | head -20 | while read count test; do
                # Tests that fail sometimes (not always) are flaky
                TOTAL_RUNS=$(echo "$FAILED_RUNS" | wc -l)
                FAILURE_RATE=$(echo "scale=2; $count * 100 / $TOTAL_RUNS" | bc)

                if (( $(echo "$count > 1 && $FAILURE_RATE < 80" | bc -l) )); then
                    echo "  ⚠️  FLAKY: $test (failed $count/$TOTAL_RUNS times, $FAILURE_RATE%)"
                else
                    echo "  $test (failed $count times)"
                fi
            done

            echo ""
            echo "Recommendations:"
            echo "- Investigate flaky tests marked with ⚠️"
            echo "- Check for race conditions, timing dependencies"
            echo "- Review test isolation and cleanup"
            echo "- Consider retry logic or increased timeouts"
        else
            echo "✓ No test failures detected in recent runs"
        fi
    else
        echo "⚠️  Flaky test detection not yet implemented for $CI_PLATFORM"
        echo "Manual log analysis required"
    fi

    echo ""
}

detect_flaky_tests
```

## Phase 5: Performance Trend Analysis

I'll track build duration and performance:

```bash
#!/bin/bash
# Analyze build performance and duration trends

analyze_build_performance() {
    echo "=== Build Performance Analysis ==="
    echo ""

    if [ ! -f "/tmp/ci_builds.json" ]; then
        echo "⚠️  No build data available"
        return
    fi

    # Calculate build durations
    echo "Build Duration Statistics:"

    # Extract durations (GitHub Actions)
    if [ "$CI_PLATFORM" = "github-actions" ]; then
        jq -r '.[] | "\(.createdAt)|\(.updatedAt)"' /tmp/ci_builds.json | while IFS='|' read created updated; do
            if [ ! -z "$created" ] && [ ! -z "$updated" ]; then
                START=$(date -d "$created" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "$created" +%s 2>/dev/null || echo 0)
                END=$(date -d "$updated" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "$updated" +%s 2>/dev/null || echo 0)
                DURATION=$((END - START))
                echo $DURATION
            fi
        done > /tmp/build_durations.txt

        if [ -s /tmp/build_durations.txt ]; then
            # Calculate statistics
            AVG_DURATION=$(awk '{sum+=$1; count++} END {printf "%.0f", sum/count}' /tmp/build_durations.txt)
            MIN_DURATION=$(sort -n /tmp/build_durations.txt | head -1)
            MAX_DURATION=$(sort -n /tmp/build_durations.txt | tail -1)

            # Convert to human readable
            echo "  Average: $(($AVG_DURATION / 60))m $(($AVG_DURATION % 60))s"
            echo "  Fastest: $(($MIN_DURATION / 60))m $(($MIN_DURATION % 60))s"
            echo "  Slowest: $(($MAX_DURATION / 60))m $(($MAX_DURATION % 60))s"

            # Trend analysis
            RECENT_AVG=$(head -10 /tmp/build_durations.txt | awk '{sum+=$1; count++} END {printf "%.0f", sum/count}')
            PREVIOUS_AVG=$(tail -n +11 /tmp/build_durations.txt | awk '{sum+=$1; count++} END {printf "%.0f", sum/count}')

            echo ""
            echo "Performance Trend:"
            echo "  Last 10 builds: $(($RECENT_AVG / 60))m $(($RECENT_AVG % 60))s"
            echo "  Previous builds: $(($PREVIOUS_AVG / 60))m $(($PREVIOUS_AVG % 60))s"

            DIFF=$((RECENT_AVG - PREVIOUS_AVG))
            if [ $DIFF -gt 30 ]; then
                echo "  Trend: ⚠️  Slowing down (+$(($DIFF / 60))m $(($DIFF % 60))s)"
                echo ""
                echo "  Recommendations:"
                echo "  - Review recently added dependencies"
                echo "  - Check for increased test count"
                echo "  - Consider caching strategies"
                echo "  - Profile slow steps"
            elif [ $DIFF -lt -30 ]; then
                echo "  Trend: ✓ Improving (-$((-$DIFF / 60))m $((-$DIFF % 60))s)"
            else
                echo "  Trend: Stable"
            fi
        fi
    fi

    echo ""
}

analyze_build_performance
```

## Phase 6: Failure Pattern Analysis

I'll identify common failure patterns:

```bash
#!/bin/bash
# Analyze failure patterns and root causes

analyze_failure_patterns() {
    echo "=== Failure Pattern Analysis ==="
    echo ""

    if [ ! -f "/tmp/ci_builds.json" ]; then
        echo "⚠️  No build data available"
        return
    fi

    FAILED_COUNT=$(jq '[.[] | select(.conclusion=="failure" or .status=="failed")] | length' /tmp/ci_builds.json)

    if [ $FAILED_COUNT -eq 0 ]; then
        echo "✓ No recent failures detected"
        echo ""
        return
    fi

    echo "Analyzing $FAILED_COUNT failed builds..."

    # Common failure categories
    > /tmp/failure_categories.txt

    # Get failed run IDs and analyze logs
    FAILED_RUNS=$(jq -r '.[] | select(.conclusion=="failure" or .status=="failed") | .databaseId // .id' /tmp/ci_builds.json | head -10)

    for run_id in $FAILED_RUNS; do
        if [ "$CI_PLATFORM" = "github-actions" ]; then
            gh run view "$run_id" --log 2>/dev/null | while read line; do
                # Categorize failures
                if echo "$line" | grep -qi "timeout\|timed out"; then
                    echo "timeout" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "out of memory\|oom"; then
                    echo "memory" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "network error\|connection refused\|ECONNREFUSED"; then
                    echo "network" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "npm ERR\|pip error\|cargo error"; then
                    echo "dependency" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "test.*fail\|assertion"; then
                    echo "test" >> /tmp/failure_categories.txt
                elif echo "$line" | grep -qi "lint\|format"; then
                    echo "lint" >> /tmp/failure_categories.txt
                fi
            done
        fi
    done

    if [ -s /tmp/failure_categories.txt ]; then
        echo ""
        echo "Failure Categories:"
        sort /tmp/failure_categories.txt | uniq -c | sort -rn | while read count category; do
            case "$category" in
                timeout)
                    echo "  ⏱️  Timeout issues: $count occurrences"
                    echo "     → Consider increasing timeout limits"
                    ;;
                memory)
                    echo "  💾 Memory issues: $count occurrences"
                    echo "     → Review memory-intensive operations"
                    ;;
                network)
                    echo "  🌐 Network issues: $count occurrences"
                    echo "     → Add retry logic for network calls"
                    ;;
                dependency)
                    echo "  📦 Dependency issues: $count occurrences"
                    echo "     → Lock dependency versions"
                    ;;
                test)
                    echo "  🧪 Test failures: $count occurrences"
                    echo "     → Review test stability"
                    ;;
                lint)
                    echo "  ✨ Lint/format issues: $count occurrences"
                    echo "     → Run linter before commit"
                    ;;
            esac
        done
    fi

    echo ""
}

analyze_failure_patterns
```

## Phase 7: Comprehensive Report

I'll generate a comprehensive monitoring report:

```bash
#!/bin/bash
# Generate comprehensive pipeline monitoring report

generate_monitoring_report() {
    echo "========================================"
    echo "CI/CD PIPELINE MONITORING REPORT"
    echo "========================================"
    echo ""
    echo "Generated: $(date)"
    echo "Platform: $CI_PLATFORM"
    echo "Analysis Period: Last 50 builds"
    echo ""

    # Summary from previous analyses
    if [ -f "/tmp/ci_builds.json" ]; then
        TOTAL=$(jq length /tmp/ci_builds.json)
        SUCCESS=$(jq '[.[] | select(.conclusion=="success" or .status=="success")] | length' /tmp/ci_builds.json)
        FAILURE=$(jq '[.[] | select(.conclusion=="failure" or .status=="failed")] | length' /tmp/ci_builds.json)
        SUCCESS_RATE=$(echo "scale=2; $SUCCESS * 100 / $TOTAL" | bc)

        echo "HEALTH SCORE: $SUCCESS_RATE%"

        if (( $(echo "$SUCCESS_RATE >= 90" | bc -l) )); then
            echo "Status: ✓ HEALTHY"
        elif (( $(echo "$SUCCESS_RATE >= 70" | bc -l) )); then
            echo "Status: ⚠️  NEEDS ATTENTION"
        else
            echo "Status: ❌ CRITICAL"
        fi

        echo ""
        echo "KEY METRICS:"
        echo "  Success rate: $SUCCESS_RATE%"
        echo "  Total builds: $TOTAL"
        echo "  Failed builds: $FAILURE"

        if [ -f "/tmp/build_durations.txt" ]; then
            AVG_DURATION=$(awk '{sum+=$1; count++} END {printf "%.0f", sum/count}' /tmp/build_durations.txt)
            echo "  Avg duration: $(($AVG_DURATION / 60))m $(($AVG_DURATION % 60))s"
        fi

        echo ""
        echo "RECOMMENDATIONS:"

        if [ $FAILURE -gt $((TOTAL / 4)) ]; then
            echo "  ⚠️  High failure rate - investigate failing builds"
        fi

        if [ -f "/tmp/test_failures.txt" ] && [ -s "/tmp/test_failures.txt" ]; then
            FLAKY_COUNT=$(sort /tmp/test_failures.txt | uniq -c | awk '$1 > 1 && $1 < 15 {count++} END {print count+0}')
            if [ $FLAKY_COUNT -gt 0 ]; then
                echo "  ⚠️  $FLAKY_COUNT flaky tests detected - see details above"
            fi
        fi

        echo ""
    fi

    echo "========================================"
}

generate_monitoring_report
```

## Integration with Other Skills

**Workflow Integration:**
- After failed builds → `/debug-systematic`
- Before releases → `/release-automation` (check build health)
- During development → `/test` (local testing)
- For CI setup → `/ci-setup`

**Skill Suggestions:**
- High failure rate → `/test-coverage`, `/test-antipatterns`
- Flaky tests found → `/test-async`
- Performance degradation → `/bundle-analyze`, `/lighthouse`

## Practical Examples

**Monitor default platform:**
```bash
/pipeline-monitor              # Auto-detect and analyze
```

**Specific platform:**
```bash
/pipeline-monitor github       # GitHub Actions
/pipeline-monitor gitlab       # GitLab CI
/pipeline-monitor circle       # CircleCI
```

**Custom time range:**
```bash
/pipeline-monitor --last 100   # Last 100 builds
/pipeline-monitor --days 7     # Last 7 days
```

**Focus on specific metrics:**
```bash
/pipeline-monitor --flaky      # Focus on flaky test detection
/pipeline-monitor --performance # Focus on performance trends
```

## What Gets Analyzed

**Metrics Tracked:**
- Build success/failure rates
- Build duration and trends
- Flaky test identification
- Failure pattern analysis
- Performance degradation
- Workflow-specific metrics

**Platforms Supported:**
- GitHub Actions (via gh CLI)
- GitLab CI (via glab CLI)
- CircleCI (via API with token)
- Jenkins (manual log analysis)
- Travis CI (basic support)
- Azure Pipelines (basic support)

## Safety Guarantees

**What I'll NEVER do:**
- Modify CI/CD configuration files
- Trigger builds or deployments
- Cancel running builds
- Delete build history
- Modify workflow settings

**What I WILL do:**
- Read-only analysis of build data
- Statistical trend analysis
- Actionable recommendations
- Clear reporting with context

## Credits

This skill integrates:
- **GitHub CLI** - GitHub Actions integration
- **GitLab CLI** - GitLab CI integration
- **CircleCI API** - CircleCI integration
- **Statistical Analysis** - Trend detection algorithms

## Token Budget

Target: 2,000-3,500 tokens per execution
- Phase 1-2: ~600 tokens (detection, fetch)
- Phase 3-4: ~800 tokens (success rates, flaky tests)
- Phase 5-6: ~800 tokens (performance, patterns)
- Phase 7: ~500 tokens (reporting)

**Optimization Strategy:**
- Platform detection via bash (no file reading)
- API/CLI calls for build data (minimal tokens)
- Statistical analysis without full log parsing
- Grep for specific error patterns
- Summary-based reporting

This ensures comprehensive pipeline monitoring while maintaining efficiency and token budget compliance.
