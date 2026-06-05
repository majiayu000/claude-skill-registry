#!/bin/bash
# debug-selector.sh
# Interactive tool to test CSS selectors

SESSION_ID=$1
TAB_ID=$2

if [[ -z "$SESSION_ID" || -z "$TAB_ID" ]]; then
  echo "Usage: debug-selector.sh <session-id> <tab-id>"
  exit 1
fi

echo "Selector Debugger"
echo "Enter CSS selectors to test (quit to exit)"
echo "---"

while true; do
  read -p "Enter selector: " SELECTOR
  
  if [[ "$SELECTOR" == "quit" ]]; then
    break
  fi
  
  COUNT=$(pagerunner evaluate "$SESSION_ID" "$TAB_ID" "document.querySelectorAll('$SELECTOR').length")
  TEXT=$(pagerunner evaluate "$SESSION_ID" "$TAB_ID" "document.querySelector('$SELECTOR')?.textContent?.substring(0, 100)")
  
  echo "Found: $COUNT elements"
  echo "Text: $TEXT"
  echo ""
done

echo "Done."
