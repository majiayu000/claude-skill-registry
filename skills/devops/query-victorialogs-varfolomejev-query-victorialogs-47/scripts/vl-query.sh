#!/bin/bash
set -euo pipefail

VL_URL="${VL_URL:?VL_URL environment variable required (e.g. http://34.77.54.45:9428)}"
QUERY="${1:?Usage: vl-query.sh <logsql_query> [limit] [start] [end]}"
LIMIT="${2:-500}"
START="${3:-}"
END="${4:-}"

ARGS=("--data-urlencode" "query=$QUERY" "-d" "limit=$LIMIT")
[[ -n "$START" ]] && ARGS+=("-d" "start=$START")
[[ -n "$END" ]] && ARGS+=("-d" "end=$END")

curl -s "$VL_URL/select/logsql/query" \
  -H 'Accept: application/stream+json' \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  "${ARGS[@]}" \
  --insecure
