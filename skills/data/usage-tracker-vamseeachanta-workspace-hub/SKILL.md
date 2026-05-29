---
name: usage-tracker
version: 1.0.0
description: Track and analyze usage metrics with timestamped logging
author: workspace-hub
category: bash
tags: [bash, metrics, logging, analytics, tracking, reporting]
platforms: [linux, macos]
---

# Usage Tracker

Patterns for tracking usage metrics, generating reports, and analyzing trends. Extracted from workspace-hub's Claude usage monitoring system.

## When to Use This Skill

✅ **Use when:**
- Need to track tool/resource usage over time
- Generating usage reports (daily, weekly, monthly)
- Monitoring quotas or limits
- Analyzing usage patterns
- Building dashboards

❌ **Avoid when:**
- Real-time metrics (use proper monitoring tools)
- High-frequency events (>100/second)
- Sensitive data without encryption

## Core Capabilities

### 1. Basic Usage Logging

Pipe-delimited log format for easy parsing:

```bash
#!/bin/bash
# ABOUTME: Basic usage tracking with timestamped logs
# ABOUTME: Pattern from workspace-hub check_claude_usage.sh

# Configuration
USAGE_LOG="${HOME}/.workspace-hub/usage.log"
USAGE_DIR="$(dirname "$USAGE_LOG")"

# Ensure directory exists
mkdir -p "$USAGE_DIR"

# Initialize log if needed
if [[ ! -f "$USAGE_LOG" ]]; then
    cat > "$USAGE_LOG" << EOF
# Usage Log
# Format: TIMESTAMP|CATEGORY|ITEM|VALUE|METADATA
# Created: $(date)
EOF
fi

# Log a usage event
log_usage() {
    local category="$1"
    local item="$2"
    local value="${3:-1}"
    local metadata="${4:-}"
    local timestamp=$(date '+%Y-%m-%d_%H:%M:%S')

    echo "${timestamp}|${category}|${item}|${value}|${metadata}" >> "$USAGE_LOG"
}

# Examples
log_usage "model" "opus" "1" "task:architecture"
log_usage "model" "sonnet" "1" "task:implementation"
log_usage "api" "requests" "100" "endpoint:/data"
log_usage "tokens" "input" "2500" "model:opus"
```

### 2. Usage Aggregation

Aggregate usage by time period:

```bash
#!/bin/bash
# ABOUTME: Usage aggregation functions
# ABOUTME: Summarize by day, week, month

# Get usage for a specific period
get_usage_period() {
    local period="$1"  # today, week, month
    local category="${2:-}"
    local filter_date

    case "$period" in
        today)
            filter_date=$(date +%Y-%m-%d)
            ;;
        week)
            filter_date=$(date -d '7 days ago' +%Y-%m-%d)
            ;;
        month)
            filter_date=$(date -d '30 days ago' +%Y-%m-%d)
            ;;
        *)
            filter_date=$(date +%Y-%m-%d)
            ;;
    esac

    if [[ -n "$category" ]]; then
        grep "$filter_date" "$USAGE_LOG" 2>/dev/null | grep "|${category}|" || true
    else
        grep "$filter_date" "$USAGE_LOG" 2>/dev/null || true
    fi
}

# Count usage by category
count_by_category() {
    local period="$1"

    get_usage_period "$period" | \
        awk -F'|' '{count[$2]+=$4} END {for (c in count) print c, count[c]}' | \
        sort -k2 -nr
}

# Count usage by item within category
count_by_item() {
    local period="$1"
    local category="$2"

    get_usage_period "$period" "$category" | \
        awk -F'|' '{count[$3]+=$4} END {for (i in count) print i, count[i]}' | \
        sort -k2 -nr
}

# Get total usage
get_total() {
    local period="$1"
    local category="${2:-}"

    get_usage_period "$period" "$category" | \
        awk -F'|' '{sum+=$4} END {print sum+0}'
}
```

### 3. Usage Summary Reports

Generate human-readable reports:

```bash
#!/bin/bash
# ABOUTME: Usage summary report generation
# ABOUTME: Pattern from check_claude_usage.sh

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Generate usage summary
generate_summary() {
    local period="${1:-today}"

    # Get counts
    local opus_count=$(count_by_item "$period" "model" | grep opus | awk '{print $2}')
    local sonnet_count=$(count_by_item "$period" "model" | grep sonnet | awk '{print $2}')
    local haiku_count=$(count_by_item "$period" "model" | grep haiku | awk '{print $2}')

    opus_count=${opus_count:-0}
    sonnet_count=${sonnet_count:-0}
    haiku_count=${haiku_count:-0}

    local total=$((opus_count + sonnet_count + haiku_count))

    if [[ $total -eq 0 ]]; then
        echo -e "${YELLOW}No usage recorded for $period${NC}"
        return
    fi

    # Calculate percentages
    local opus_pct=$((opus_count * 100 / total))
    local sonnet_pct=$((sonnet_count * 100 / total))
    local haiku_pct=$((haiku_count * 100 / total))

    # Display report
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}  Usage Summary - ${period}${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""
    echo -e "  Total tasks: ${BLUE}${total}${NC}"
    echo ""
    echo -e "  ${GREEN}Opus:${NC}   ${opus_count} tasks (${opus_pct}%)"
    echo -e "  ${BLUE}Sonnet:${NC} ${sonnet_count} tasks (${sonnet_pct}%)"
    echo -e "  ${YELLOW}Haiku:${NC}  ${haiku_count} tasks (${haiku_pct}%)"
    echo ""

    # Recommendations
    if [[ $sonnet_pct -gt 50 ]]; then
        echo -e "${RED}⚠️  High Sonnet usage (${sonnet_pct}%)${NC}"
        echo -e "   Consider shifting tasks to Opus or Haiku"
        echo ""
    fi

    if [[ $haiku_pct -lt 20 ]]; then
        echo -e "${YELLOW}ℹ️  Low Haiku usage (${haiku_pct}%)${NC}"
        echo -e "   Opportunity to use Haiku for quick tasks"
        echo ""
    fi

    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "  ${GREEN}Target Distribution:${NC}"
    echo -e "  Opus: 30% | Sonnet: 40% | Haiku: 30%"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
}
```

### 4. Threshold Monitoring

Monitor against limits and thresholds:

```bash
#!/bin/bash
# ABOUTME: Threshold monitoring with alerts
# ABOUTME: Check usage against limits

# Thresholds
declare -A THRESHOLDS=(
    ["opus_daily"]=50
    ["sonnet_daily"]=100
    ["haiku_daily"]=200
    ["total_daily"]=250
    ["warning_pct"]=70
    ["critical_pct"]=90
)

# Check single threshold
check_threshold() {
    local current="$1"
    local limit="$2"
    local name="$3"

    if [[ $limit -eq 0 ]]; then
        return 0
    fi

    local pct=$((current * 100 / limit))

    if [[ $pct -ge ${THRESHOLDS[critical_pct]} ]]; then
        echo -e "${RED}⚠️  CRITICAL: $name at ${pct}% (${current}/${limit})${NC}"
        return 2
    elif [[ $pct -ge ${THRESHOLDS[warning_pct]} ]]; then
        echo -e "${YELLOW}⚠️  WARNING: $name at ${pct}% (${current}/${limit})${NC}"
        return 1
    else
        echo -e "${GREEN}✓ $name: ${pct}% (${current}/${limit})${NC}"
        return 0
    fi
}

# Check all thresholds
check_all_thresholds() {
    local period="${1:-today}"
    local status=0

    echo -e "${CYAN}Checking usage thresholds...${NC}"
    echo ""

    local opus=$(count_by_item "$period" "model" | grep opus | awk '{print $2}')
    local sonnet=$(count_by_item "$period" "model" | grep sonnet | awk '{print $2}')
    local haiku=$(count_by_item "$period" "model" | grep haiku | awk '{print $2}')
    local total=$((${opus:-0} + ${sonnet:-0} + ${haiku:-0}))

    check_threshold "${opus:-0}" "${THRESHOLDS[opus_daily]}" "Opus" || status=$?
    check_threshold "${sonnet:-0}" "${THRESHOLDS[sonnet_daily]}" "Sonnet" || status=$?
    check_threshold "${haiku:-0}" "${THRESHOLDS[haiku_daily]}" "Haiku" || status=$?
    check_threshold "$total" "${THRESHOLDS[total_daily]}" "Total" || status=$?

    return $status
}
```

### 5. Trend Analysis

Analyze usage trends over time:

```bash
#!/bin/bash
# ABOUTME: Usage trend analysis
# ABOUTME: Compare periods and identify patterns

# Get daily totals for last N days
get_daily_trend() {
    local days="${1:-7}"
    local category="${2:-}"

    for i in $(seq $days -1 0); do
        local date=$(date -d "$i days ago" +%Y-%m-%d)
        local count

        if [[ -n "$category" ]]; then
            count=$(grep "$date" "$USAGE_LOG" 2>/dev/null | \
                    grep "|${category}|" | \
                    awk -F'|' '{sum+=$4} END {print sum+0}')
        else
            count=$(grep "$date" "$USAGE_LOG" 2>/dev/null | \
                    awk -F'|' '{sum+=$4} END {print sum+0}')
        fi

        echo "$date $count"
    done
}

# Calculate moving average
moving_average() {
    local window="${1:-3}"
    local values=("${@:2}")
    local sum=0
    local count=0

    for val in "${values[@]}"; do
        sum=$((sum + val))
        count=$((count + 1))

        if [[ $count -ge $window ]]; then
            echo $((sum / window))
            sum=$((sum - ${values[$((count - window))]}))
        fi
    done
}

# Display trend chart (ASCII)
display_trend_chart() {
    local days="${1:-14}"
    local max_width=40

    echo ""
    echo "Usage Trend (Last $days days)"
    echo "────────────────────────────────────────"

    local max_val=0
    declare -a daily_data

    while read -r date count; do
        daily_data+=("$date:$count")
        [[ $count -gt $max_val ]] && max_val=$count
    done < <(get_daily_trend "$days")

    [[ $max_val -eq 0 ]] && max_val=1

    for entry in "${daily_data[@]}"; do
        local date="${entry%:*}"
        local count="${entry#*:}"
        local bar_len=$((count * max_width / max_val))
        local bar=$(printf "%${bar_len}s" | tr ' ' '█')

        printf "%s │%s %d\n" "${date:5}" "$bar" "$count"
    done

    echo "────────────────────────────────────────"
}
```

### 6. Export and Reporting

Export data for external analysis:

```bash
#!/bin/bash
# ABOUTME: Export usage data to various formats
# ABOUTME: CSV, JSON, Markdown reports

# Export to CSV
export_csv() {
    local period="${1:-week}"
    local output="${2:-usage_export.csv}"

    echo "timestamp,category,item,value,metadata" > "$output"
    get_usage_period "$period" | tr '|' ',' >> "$output"

    echo "Exported to $output"
}

# Export to JSON
export_json() {
    local period="${1:-week}"
    local output="${2:-usage_export.json}"

    echo "[" > "$output"
    local first=true

    while IFS='|' read -r ts cat item val meta; do
        [[ "$ts" =~ ^#.*$ ]] && continue
        [[ -z "$ts" ]] && continue

        [[ "$first" == "false" ]] && echo "," >> "$output"
        first=false

        cat >> "$output" << EOF
  {
    "timestamp": "$ts",
    "category": "$cat",
    "item": "$item",
    "value": $val,
    "metadata": "$meta"
  }
EOF
    done < <(get_usage_period "$period")

    echo "]" >> "$output"
    echo "Exported to $output"
}

# Generate markdown report
generate_markdown_report() {
    local period="${1:-week}"
    local output="${2:-usage_report.md}"

    cat > "$output" << EOF
# Usage Report - Week of $(date +%Y-%m-%d)

## Summary

$(generate_summary "$period" | sed 's/\x1b\[[0-9;]*m//g')

## Daily Breakdown

| Date | Opus | Sonnet | Haiku | Total |
|------|------|--------|-------|-------|
EOF

    for i in $(seq 6 -1 0); do
        local date=$(date -d "$i days ago" +%Y-%m-%d)
        local opus=$(grep "$date" "$USAGE_LOG" | grep "|opus|" | wc -l)
        local sonnet=$(grep "$date" "$USAGE_LOG" | grep "|sonnet|" | wc -l)
        local haiku=$(grep "$date" "$USAGE_LOG" | grep "|haiku|" | wc -l)
        local total=$((opus + sonnet + haiku))

        echo "| $date | $opus | $sonnet | $haiku | $total |" >> "$output"
    done

    cat >> "$output" << EOF

## Recommendations

Based on current usage patterns:
$(generate_recommendations)

---
Generated: $(date)
EOF

    echo "Report generated: $output"
}
```

## Complete Example: Usage Monitor CLI

```bash
#!/bin/bash
# ABOUTME: Complete usage monitoring CLI tool
# ABOUTME: Track, analyze, and report on usage metrics

set -e

# ─────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────

SCRIPT_NAME="usage-monitor"
USAGE_DIR="${HOME}/.${SCRIPT_NAME}"
USAGE_LOG="$USAGE_DIR/usage.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ─────────────────────────────────────────────────────────────────
# Core Functions
# ─────────────────────────────────────────────────────────────────

init() {
    mkdir -p "$USAGE_DIR"
    [[ -f "$USAGE_LOG" ]] || echo "# Usage Log" > "$USAGE_LOG"
}

log_usage() {
    local category="$1"
    local item="$2"
    local value="${3:-1}"
    local metadata="${4:-}"

    echo "$(date '+%Y-%m-%d_%H:%M:%S')|${category}|${item}|${value}|${metadata}" >> "$USAGE_LOG"
    echo -e "${GREEN}✓ Logged: ${category}/${item} = ${value}${NC}"
}

show_summary() {
    local period="${1:-today}"

    # Get filter date
    case "$period" in
        today) filter=$(date +%Y-%m-%d) ;;
        week)  filter=$(date -d '7 days ago' +%Y-%m-%d) ;;
        month) filter=$(date -d '30 days ago' +%Y-%m-%d) ;;
    esac

    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo -e "${CYAN}  Usage Summary - ${period}${NC}"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
    echo ""

    # Category breakdown
    echo "By Category:"
    grep "$filter" "$USAGE_LOG" 2>/dev/null | \
        awk -F'|' '{count[$2]+=$4} END {for (c in count) printf "  %-15s %d\n", c, count[c]}' | \
        sort -k2 -nr

    echo ""
    echo "Total: $(grep "$filter" "$USAGE_LOG" 2>/dev/null | awk -F'|' '{sum+=$4} END {print sum+0}')"
    echo -e "${CYAN}═══════════════════════════════════════${NC}"
}

show_help() {
    cat << EOF
Usage: $SCRIPT_NAME <command> [options]

Commands:
    log <category> <item> [value] [metadata]
        Log a usage event

    summary [today|week|month]
        Show usage summary

    check
        Check against thresholds

    export <csv|json> [filename]
        Export usage data

    report [filename]
        Generate markdown report

    trend [days]
        Show usage trend chart

Examples:
    $SCRIPT_NAME log model opus 1 "task:architecture"
    $SCRIPT_NAME summary week
    $SCRIPT_NAME export csv usage.csv
    $SCRIPT_NAME trend 14

EOF
}

# ─────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────

init

case "${1:-}" in
    log)
        shift
        [[ $# -lt 2 ]] && { echo "Usage: $0 log <category> <item> [value] [metadata]"; exit 1; }
        log_usage "$@"
        ;;
    summary)
        show_summary "${2:-today}"
        ;;
    check)
        check_all_thresholds "${2:-today}"
        ;;
    export)
        case "${2:-csv}" in
            csv)  export_csv "${3:-week}" "${4:-usage_export.csv}" ;;
            json) export_json "${3:-week}" "${4:-usage_export.json}" ;;
        esac
        ;;
    report)
        generate_markdown_report "${2:-week}" "${3:-usage_report.md}"
        ;;
    trend)
        display_trend_chart "${2:-14}"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
```

## Best Practices

1. **Consistent Log Format** - Use pipe-delimited for easy parsing
2. **Include Timestamps** - Always log when events occur
3. **Add Metadata** - Extra context helps debugging
4. **Rotate Logs** - Prevent unbounded growth
5. **Validate Input** - Sanitize before logging

## Resources

- [awk One-Liners](https://catonmat.net/awk-one-liners-explained-part-one)
- [sed/awk Tutorial](https://www.grymoire.com/Unix/Awk.html)
- [Date Manipulation in Bash](https://www.cyberciti.biz/faq/linux-unix-formatting-dates-for-display/)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - extracted from workspace-hub check_claude_usage.sh
