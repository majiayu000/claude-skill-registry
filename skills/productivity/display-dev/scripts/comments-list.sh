#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"

# One-shot list of comment threads on an artifact. Mirrors the wire
# shape of `GET /v1/artifacts/:shortId/comments` exactly — the response
# body is written to stdout as a single JSON object with `data`,
# `nextCursor`, and `totalCount` keys (see ListCommentsResponseDto on
# the server). Non-2xx exits with the error message on stderr.
#
# Usage:
#   comments-list.sh --artifact <shortId> [--since <iso>] [--status open|resolved|all]
#
# Defaults: --status open (server-side default).

ARTIFACT=""; SINCE=""; STATUS=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --artifact)
      if [[ $# -lt 2 ]]; then echo "comments-list.sh: --artifact requires a value" >&2; exit 1; fi
      ARTIFACT="$2"; shift 2 ;;
    --since)
      if [[ $# -lt 2 ]]; then echo "comments-list.sh: --since requires a value" >&2; exit 1; fi
      SINCE="$2"; shift 2 ;;
    --status)
      if [[ $# -lt 2 ]]; then echo "comments-list.sh: --status requires a value" >&2; exit 1; fi
      STATUS="$2"; shift 2 ;;
    *) echo "comments-list.sh: unrecognized arg: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$ARTIFACT" ]]; then
  echo "comments-list.sh: --artifact is required" >&2; exit 1
fi

# Reject characters that don't appear in real shortIds — the value is
# interpolated into the URL path. shortIds are nanoid-shaped
# (alphanumeric + `-`, `_`), so anything outside that set is either a
# typo or an attempt to break out of the path segment.
if printf '%s' "$ARTIFACT" | LC_ALL=C grep -qE '[^A-Za-z0-9_-]'; then
  echo "comments-list.sh: --artifact contains invalid characters" >&2; exit 1
fi

ARGS=(--artifact "$ARTIFACT")
if [[ -n "$SINCE" ]]; then
  # ISO-8601 charset: digits + `T`/`Z` + punctuation. The server
  # @IsISO8601() validates the actual format; this regex keeps the
  # wrapper error message crisp before delegating to `dsp`.
  if printf '%s' "$SINCE" | LC_ALL=C grep -qE '[^0-9A-Za-z:.+-]'; then
    echo "comments-list.sh: --since contains invalid characters (expected ISO-8601)" >&2; exit 1
  fi
  ARGS+=(--since "$SINCE")
fi
if [[ -n "$STATUS" ]]; then
  case "$STATUS" in
    open|resolved|all) ;;
    *) echo "comments-list.sh: --status must be open|resolved|all" >&2; exit 1 ;;
  esac
  ARGS+=(--status "$STATUS")
fi

require_dsp_or_exit
exec $DSP_CMD comment --client-source "$CLIENT_SOURCE" list "${ARGS[@]}"
