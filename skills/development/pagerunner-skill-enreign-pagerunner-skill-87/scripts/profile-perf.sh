#!/bin/bash
# profile-perf.sh
# Benchmark Pagerunner operations

SESSION_ID=$1
TAB_ID=$2

if [[ -z "$SESSION_ID" || -z "$TAB_ID" ]]; then
  echo "Usage: profile-perf.sh <session-id> <tab-id>"
  exit 1
fi

echo "Pagerunner Performance Profile"
echo "---"

# Measure get_content
START=$(date +%s%N)
pagerunner get-content "$SESSION_ID" "$TAB_ID" > /dev/null
END=$(date +%s%N)
TIME=$(( (END - START) / 1000000 ))
echo "get_content: ${TIME}ms"

# Measure evaluate
START=$(date +%s%N)
pagerunner evaluate "$SESSION_ID" "$TAB_ID" "document.querySelectorAll('*').length" > /dev/null
END=$(date +%s%N)
TIME=$(( (END - START) / 1000000 ))
echo "evaluate: ${TIME}ms"

# Measure screenshot
START=$(date +%s%N)
pagerunner screenshot "$SESSION_ID" "$TAB_ID" --base64 > /dev/null
END=$(date +%s%N)
TIME=$(( (END - START) / 1000000 ))
echo "screenshot: ${TIME}ms"

echo "---"
echo "Higher times = slower operations. Optimize selectors if evaluate is slow."
