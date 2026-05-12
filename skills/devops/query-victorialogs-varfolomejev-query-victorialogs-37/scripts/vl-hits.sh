#!/bin/bash
set -euo pipefail

VL_URL="${VL_URL:?VL_URL environment variable required (e.g. http://34.77.54.45:9428)}"
QUERY="${1:?Usage: vl-hits.sh <logsql_query> [step] [start] [end]}"
STEP="${2:-60000ms}"
START="${3:-}"
END="${4:-}"

ARGS=("--data-urlencode" "query=$QUERY" "-d" "step=$STEP")
[[ -n "$START" ]] && ARGS+=("-d" "start=$START")
[[ -n "$END" ]] && ARGS+=("-d" "end=$END")

curl -s "$VL_URL/select/logsql/hits" \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  "${ARGS[@]}" \
  --insecure
