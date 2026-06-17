#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"

# Mark a comment thread resolved.
#
# Usage:
#   thread-resolve.sh --root <rootCommentId>
#
# Permission rules apply server-side: thread participant (any comment
# in the thread), artifact creator, or org admin. Anyone else → 403.

ROOT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      if [[ $# -lt 2 ]]; then echo "thread-resolve.sh: --root requires a value" >&2; exit 1; fi
      ROOT="$2"; shift 2 ;;
    *) echo "thread-resolve.sh: unrecognized arg: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$ROOT" ]]; then echo "thread-resolve.sh: --root is required" >&2; exit 1; fi
if printf '%s' "$ROOT" | LC_ALL=C grep -qE '[^A-Za-z0-9-]'; then
  echo "thread-resolve.sh: --root contains invalid characters" >&2; exit 1
fi

require_dsp_or_exit
exec $DSP_CMD thread --client-source "$CLIENT_SOURCE" resolve "$ROOT"
