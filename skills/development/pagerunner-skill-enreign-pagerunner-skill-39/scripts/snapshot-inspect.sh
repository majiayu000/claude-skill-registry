#!/bin/bash
# snapshot-inspect.sh
# View saved snapshot metadata (not values, since they're encrypted)

PROFILE=$1
ORIGIN=$2

if [[ -z "$PROFILE" || -z "$ORIGIN" ]]; then
  echo "Usage: snapshot-inspect.sh <profile> <origin>"
  echo "Example: snapshot-inspect.sh agent-work https://jira.mycompany.com"
  exit 1
fi

echo "Snapshot Info for: $PROFILE / $ORIGIN"
echo "---"

pagerunner list-snapshots --profile "$PROFILE" | grep "$ORIGIN"

echo "---"
echo "Snapshots are encrypted. Use restore-snapshot to use them."
