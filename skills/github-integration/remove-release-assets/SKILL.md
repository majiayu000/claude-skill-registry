---
description: Remove all files/artifacts/assets from a GitHub release
triggers:
  - remove release assets
  - delete release assets
  - clear release files
---

# Remove Release Assets

Remove all files/artifacts/assets from a GitHub release.

## Usage

Invoke this skill when you need to clear all assets from a release before uploading new ones.

## Parameters

When invoking this skill, provide:
- **repo**: The repository (e.g., `iNavFlight/inav` or `iNavFlight/inav-configurator`)
- **tag**: The release tag (e.g., `9.0.0-RC2`)

## Procedure

1. **Get asset IDs from the release:**

```bash
gh api repos/{repo}/releases --jq '.[] | select(.tag_name=="{tag}") | .assets[].id' > /tmp/asset_ids.txt
```

2. **Check how many assets exist:**

```bash
wc -l /tmp/asset_ids.txt
```

3. **Delete each asset via the GitHub API:**

```bash
count=0
total=$(wc -l < /tmp/asset_ids.txt)
while IFS= read -r id; do
  ((count++))
  gh api -X DELETE "repos/{repo}/releases/assets/$id" 2>/dev/null && echo "Deleted $count/$total"
done < /tmp/asset_ids.txt
echo "Done"
```

4. **Verify deletion:**

```bash
gh release view {tag} --repo {repo} --json assets --jq '.assets | length'
```

Should return `0`.

## Notes

- The `gh release delete-asset` command does not exist in older versions of `gh`, so we use the API directly
- This works for both draft and published releases
- Assets are deleted immediately and cannot be recovered
- For large releases (100+ assets), this may take a few minutes

## Example

To remove all assets from the INAV 9.0.0-RC2 draft release:

```bash
# Get asset IDs
gh api repos/iNavFlight/inav/releases --jq '.[] | select(.tag_name=="9.0.0-RC2") | .assets[].id' > /tmp/asset_ids.txt

# Delete all
while IFS= read -r id; do
  gh api -X DELETE "repos/iNavFlight/inav/releases/assets/$id"
done < /tmp/asset_ids.txt

# Verify
gh release view 9.0.0-RC2 --repo iNavFlight/inav --json assets --jq '.assets | length'
```

---

## Related Skills

- **upload-release-assets** - Upload new assets after removal
