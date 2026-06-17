#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"

# Post a reply to an existing comment thread.
#
# Usage:
#   comment-reply.sh --artifact <shortId> --parent <rootCommentId> --body <text>
#
# Self-loop fuse: when DISPLAYDEV_ACTOR_TYPE=agent, the helper prepends
# a sentinel ("[claude-bot] " by default) to the body so the matching
# `comments-stream.sh` filter can skip the agent's own replies. Override
# the sentinel with DISPLAYDEV_REPLY_SENTINEL="<prefix>" (or empty
# string to disable). When ACTOR_TYPE is unset / "user", no sentinel is
# added — humans drive the public surface.

ARTIFACT=""; PARENT=""; BODY=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --artifact)
      if [[ $# -lt 2 ]]; then echo "comment-reply.sh: --artifact requires a value" >&2; exit 1; fi
      ARTIFACT="$2"; shift 2 ;;
    --parent)
      if [[ $# -lt 2 ]]; then echo "comment-reply.sh: --parent requires a value" >&2; exit 1; fi
      PARENT="$2"; shift 2 ;;
    --body)
      if [[ $# -lt 2 ]]; then echo "comment-reply.sh: --body requires a value" >&2; exit 1; fi
      BODY="$2"; shift 2 ;;
    *) echo "comment-reply.sh: unrecognized arg: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$ARTIFACT" ]]; then echo "comment-reply.sh: --artifact is required" >&2; exit 1; fi
if [[ -z "$PARENT" ]]; then echo "comment-reply.sh: --parent is required" >&2; exit 1; fi
if [[ -z "$BODY" ]]; then echo "comment-reply.sh: --body is required" >&2; exit 1; fi

if printf '%s' "$ARTIFACT" | LC_ALL=C grep -qE '[^A-Za-z0-9_-]'; then
  echo "comment-reply.sh: --artifact contains invalid characters" >&2; exit 1
fi
# Comment ids are uuidv7 — lowercase hex + hyphens. Reject anything else
# before the path interpolation runs.
if printf '%s' "$PARENT" | LC_ALL=C grep -qE '[^A-Za-z0-9-]'; then
  echo "comment-reply.sh: --parent contains invalid characters" >&2; exit 1
fi

# Prepend the sentinel only on agent-attributed posts that don't already
# carry it. ${BODY#"$SENTINEL"} == $BODY is the bash idiom for "BODY
# doesn't start with SENTINEL" — works when SENTINEL is the empty string
# (every body trivially doesn't start with empty, but the outer guard
# `-n "$SENTINEL"` skips the prefix step in that case anyway).
SENTINEL="${DISPLAYDEV_REPLY_SENTINEL-[claude-bot] }"
if [[ "${DISPLAYDEV_ACTOR_TYPE:-}" == "agent" && -n "$SENTINEL" && "${BODY#"$SENTINEL"}" == "$BODY" ]]; then
  BODY="${SENTINEL}${BODY}"
fi

require_dsp_or_exit
exec $DSP_CMD comment --client-source "$CLIENT_SOURCE" add \
  --artifact "$ARTIFACT" \
  --parent "$PARENT" \
  --body "$BODY"
