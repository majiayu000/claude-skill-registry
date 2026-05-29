#!/bin/bash
# validate-pattern.sh
# Test if a CSS selector is stable across multiple snapshots of the same page

SESSION_ID=$1
TAB_ID=$2
SELECTOR=$3
SNAPSHOTS=${4:-5}

if [[ -z "$SESSION_ID" || -z "$TAB_ID" || -z "$SELECTOR" ]]; then
  echo "Usage: validate-pattern.sh <session-id> <tab-id> <selector> [snapshots=5]"
  exit 1
fi

echo "Testing selector stability: $SELECTOR"
echo "Snapshots: $SNAPSHOTS"
echo "---"

for i in $(seq 1 $SNAPSHOTS); do
  # Get initial count
  COUNT=$(pagerunner evaluate "$SESSION_ID" "$TAB_ID" "document.querySelectorAll('$SELECTOR').length")
  echo "Snapshot $i: $COUNT elements found"
  
  # Trigger page update (click, scroll, etc.)
  pagerunner scroll "$SESSION_ID" "$TAB_ID" --y 300
  
  sleep 1
done

echo "---"
echo "If counts are consistent, selector is stable."
