---
description: Upload firmware hex files and configurator packages to GitHub releases
triggers:
  - upload release assets
  - upload to release
  - upload firmware
  - upload configurator
  - upload hex files
  - upload packages
---

# Upload Release Assets

Upload files/artifacts/assets to a GitHub release.

## Usage

Invoke this skill when you need to upload firmware hex files or configurator packages to a GitHub release.

## Parameters

When invoking this skill, provide:
- **repo**: The repository (e.g., `iNavFlight/inav` or `iNavFlight/inav-configurator`)
- **tag**: The release tag (e.g., `9.0.0-RC2`)
- **source_dir**: Directory containing files to upload

## Procedure

1. **Navigate to the source directory:**

```bash
cd {source_dir}
```

2. **Rename files if needed (firmware only):**

Files from nightly builds have CI suffixes that must be removed before upload.

```bash
# For RC releases (e.g., 9.0.0-RC2):
# Changes: inav_9.0.0_ZEEZF7_ci-20251129-0e9f842.hex -> inav_9.0.0_RC2_ZEEZF7.hex
RC_NUM="RC2"  # Set to empty string for final releases
for f in *_ci-*.hex 2>/dev/null; do
  [ -e "$f" ] || continue  # Skip if no matches
  target=$(echo "$f" | sed -E 's/inav_[0-9]+\.[0-9]+\.[0-9]+_(.*)_ci-.*/\1/')
  version=$(echo "$f" | sed -E 's/inav_([0-9]+\.[0-9]+\.[0-9]+)_.*/\1/')
  if [ -n "$RC_NUM" ]; then
    newname="inav_${version}_${RC_NUM}_${target}.hex"
  else
    newname="inav_${version}_${target}.hex"
  fi
  mv "$f" "$newname"
done
```

Expected file name formats after renaming:
- RC release: `inav_9.0.0_RC2_MATEKF405.hex`
- Final release: `inav_9.0.0_MATEKF405.hex`

3. **Count files to upload:**

```bash
ls -1 | wc -l
```

4. **Upload all files to the release:**

```bash
gh release upload {tag} * --repo {repo}
```

Or for specific file types:

```bash
# Hex files only
gh release upload {tag} *.hex --repo {repo}

# Configurator packages
gh release upload {tag} *.deb *.rpm *.zip *.dmg *.msi --repo {repo}
```

5. **Verify upload:**

```bash
gh release view {tag} --repo {repo} --json assets --jq '.assets | length'
```

## Notes

- The `gh release upload` command works for both draft and published releases
- If a file with the same name already exists, the upload will fail unless you use `--clobber`
- For large uploads (200+ files), this may take several minutes
- Upload progress is not shown; wait for the command to complete
- **Firmware:** Source directory should be FLAT (no subdirectories)
- **Configurator:** Source directory should have platform subdirectories (linux/, macos/, windows/)

## Examples

### Upload firmware hex files

```bash
cd claude/release-manager/downloads/firmware-9.0.0-rc2
gh release upload 9.0.0-RC2 *.hex --repo iNavFlight/inav
```

### Upload configurator packages (BY PLATFORM)

**IMPORTANT:** Configurator artifacts are organized by platform. Upload each platform separately.

```bash
cd claude/release-manager/downloads/configurator-9.0.0-rc2

# Upload Linux packages
gh release upload 9.0.0-RC2 linux/* --repo iNavFlight/inav-configurator

# Upload macOS packages
gh release upload 9.0.0-RC2 macos/* --repo iNavFlight/inav-configurator

# Upload Windows packages
gh release upload 9.0.0-RC2 windows/* --repo iNavFlight/inav-configurator
```

### Overwrite existing files

```bash
gh release upload 9.0.0-RC2 *.hex --repo iNavFlight/inav --clobber
```

## Typical Workflow

1. Clear existing assets (see `remove-release-assets` skill)
2. Upload new assets using this skill
3. Verify the count matches expected files

---

## Related Skills

- **download-release-artifacts** - Download artifacts before uploading
- **remove-release-assets** - Remove old assets before uploading new ones
