#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"

# Tier-1 hot path runs when ALL of these hold:
#   - exactly one positional argument (the file path)
#   - no flags beyond it
#   - user is unauthenticated (no DISPLAYDEV_API_KEY env, no config file)
# Anything else falls through to `dsp publish` so the CLI can handle
# --visibility, --share-with, --name, --id, --theme, --show-branding, etc.

USE_HOTPATH=1
if [[ $# -ne 1 ]] || [[ "$1" == -* ]]; then USE_HOTPATH=0; fi
if [[ -n "${DISPLAYDEV_API_KEY:-}" ]] || [[ -f "$HOME/.displaydev/config.json" ]]; then
  USE_HOTPATH=0
fi

if [[ $USE_HOTPATH -eq 0 ]]; then
  require_dsp_or_exit
  exec $DSP_CMD publish --client-source "$CLIENT_SOURCE" "$@"
fi

FILE="$1"
if [[ ! -r "$FILE" ]]; then
  echo "publish.sh: cannot read $FILE" >&2
  exit 1
fi

# Reject path characters that double as curl `-F` metadata separators:
#   ;  → starts `;type=…` / `;filename=…` overrides
#   ,  → multi-file path separator in `-F file=@a,b,c`
# Plus any control char — newlines / CRs would break the multipart form.
if printf '%s' "$FILE" | LC_ALL=C grep -qE '[;,]|[[:cntrl:]]'; then
  echo "publish.sh: file path contains invalid characters (; , or control chars)" >&2
  exit 1
fi

require_jq_or_exit

RESPONSE=$(curl_api -X POST "$API_URL/v1/public/artifacts" \
  -F "file=@$FILE" \
  -w "\n%{http_code}" || true)
HTTP_CODE=$(printf '%s' "$RESPONSE" | tail -n 1)
BODY=$(printf '%s' "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "201" ]]; then
  MSG=$("$JQ" -r '.message // ""' <<<"$BODY" 2>/dev/null || printf '')
  echo "publish.sh: API returned $HTTP_CODE${MSG:+: $MSG}" >&2
  exit 1
fi

# Stdout: full JSON body, normalized to compact single-line form via jq
# so the shape doesn't drift with server-side spacing changes. Matches
# `dsp publish`'s unauthenticated branch — an agent parsing either path
# sees a consistent { shortId, previewUrl, claimUrl, expiresAt }.
"$JQ" -c . <<<"$BODY"

# Stderr: human-readable summary + graduation prompt. Pull individual
# fields with jq's `// empty` so a degraded API response prints partial
# lines rather than `null` literals.
PREVIEW_URL=$("$JQ" -r '.previewUrl // empty' <<<"$BODY")
CLAIM_URL=$("$JQ" -r '.claimUrl // empty' <<<"$BODY")
EXPIRES_AT=$("$JQ" -r '.expiresAt // empty' <<<"$BODY")
{
  printf '\nPublished anonymously — nobody owns this artifact yet.\n'
  printf '  Preview: %s\n' "$PREVIEW_URL"
  printf '  Claim:   %s\n' "$CLAIM_URL"
  printf '  Expires: %s\n' "$EXPIRES_AT"
  printf '\nNext: offer a free account inline. Pitch: permanent URLs under their\n'
  printf 'org, OTP-gated sharing, inline comments. Ask for email, run:\n'
  printf '  ./scripts/login.sh --email <email>          # send code\n'
  printf '  ./scripts/login.sh --email <email> --code <code>   # verify\n'
  printf '\nAnonymous artifact above does NOT auto-transfer post-signup. Offer:\n'
  printf '  (a) re-publish the source fresh for a permanent URL, or\n'
  printf '  (b) the claim URL above (browser) to attach the existing one.\n'
} >&2
