#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"

require_dsp_or_exit
exec $DSP_CMD login --client-source "$CLIENT_SOURCE" "$@"
