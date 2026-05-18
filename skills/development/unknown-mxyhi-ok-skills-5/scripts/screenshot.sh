#!/usr/bin/env bash
#
# screenshot.sh - Capture browser screenshot and save to file
#
# Calls the Kimi WebBridge daemon to take a screenshot, decodes the base64
# response and writes it to disk. Returns the file path instead of raw
# base64, keeping AI agent context clean.
#
# Usage:
#   screenshot.sh                        # save PNG to /tmp/kimi-webbridge-screenshots/
#   screenshot.sh -o ~/Desktop/shot.png  # save to custom path
#   screenshot.sh -s twitter             # use session "twitter"
#   screenshot.sh -f jpeg -q 60          # JPEG at quality 60
#
# Dependencies: curl, jq, base64 (all pre-installed on macOS/Linux)

set -euo pipefail

# Defaults
DAEMON_URL="http://127.0.0.1:10086"
OUTPUT_DIR="/tmp/kimi-webbridge-screenshots"
OUTPUT_PATH=""
SESSION=""
FORMAT="png"
QUALITY=""

usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  -o PATH      Output file path (default: /tmp/kimi-webbridge-screenshots/{timestamp}.{format})
  -s SESSION   Browser session name (e.g., twitter, xhs)
  -f FORMAT    Image format: png (default) or jpeg
  -q QUALITY   JPEG quality 0-100 (only for jpeg format)
  -d URL       Daemon URL (default: http://127.0.0.1:10086)
  -h           Show this help
EOF
  exit 0
}

while getopts "o:s:f:q:d:h" opt; do
  case "$opt" in
    o) OUTPUT_PATH="$OPTARG" ;;
    s) SESSION="$OPTARG" ;;
    f) FORMAT="$OPTARG" ;;
    q) QUALITY="$OPTARG" ;;
    d) DAEMON_URL="$OPTARG" ;;
    h) usage ;;
    *) usage ;;
  esac
done

# Build request body
ARGS=$(jq -n --arg fmt "$FORMAT" '{format: $fmt}')
if [[ -n "$QUALITY" ]]; then
  ARGS=$(echo "$ARGS" | jq --argjson q "$QUALITY" '. + {quality: $q}')
fi

BODY=$(jq -n --arg action "screenshot" --argjson args "$ARGS" '{action: $action, args: $args}')
if [[ -n "$SESSION" ]]; then
  BODY=$(echo "$BODY" | jq --arg s "$SESSION" '. + {session: $s}')
fi

# Call daemon
RESPONSE=$(curl -s -X POST "${DAEMON_URL}/command" \
  -H 'Content-Type: application/json' \
  -d "$BODY" \
  --max-time 30)

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
  ERROR=$(echo "$RESPONSE" | jq -r '.error')
  echo "Error: $ERROR" >&2
  exit 1
fi

# Extract base64 data from the daemon response shape:
# {"ok":true,"data":{"format":"png","dataLength":123,"data":"base64..."}}
B64_DATA=$(echo "$RESPONSE" | jq -er '.data.data | select(type == "string" and length > 0)')
if [[ -z "$B64_DATA" ]]; then
  echo "Error: No image data in response" >&2
  echo "Response: $(echo "$RESPONSE" | head -c 200)" >&2
  exit 1
fi

# Determine output path
if [[ -z "$OUTPUT_PATH" ]]; then
  mkdir -p "$OUTPUT_DIR"
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  EXT="$FORMAT"
  [[ "$EXT" == "jpeg" ]] && EXT="jpg"
  OUTPUT_PATH="${OUTPUT_DIR}/${TIMESTAMP}.${EXT}"
fi

# Decode base64 - handle macOS (base64 -D) vs Linux (base64 -d)
if base64 --help 2>&1 | grep -q '\-D'; then
  echo "$B64_DATA" | base64 -D > "$OUTPUT_PATH"
else
  echo "$B64_DATA" | base64 -d > "$OUTPUT_PATH"
fi

# Output the file path (this is what the AI agent sees)
echo "$OUTPUT_PATH"
