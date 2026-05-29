---
description: Download firmware hex files and configurator builds for an INAV release
triggers:
  - download release artifacts
  - download release files
  - download firmware
  - download configurator builds
  - get release artifacts
  - fetch release files
---

# Download Release Artifacts

This skill downloads firmware hex files from inav-nightly and configurator builds from GitHub Actions CI.

## Step 1: Get Release Version

Ask the user for the release version (e.g., "9.0.0-RC2").

```
VERSION="<user-provided>"
```

## Step 2: Download Firmware Hex Files

### Find the matching nightly release:

```bash
gh release list --repo iNavFlight/inav-nightly --limit 10
```

### Verify the nightly matches the firmware commit:

```bash
cd inav
git log -1 --format="%h %s" HEAD
```

### Download hex files:

```bash
NIGHTLY_TAG="<matching-tag>"  # e.g., v9.0.0-20251129.175

mkdir -p claude/release-manager/downloads/firmware-${VERSION}
cd claude/release-manager/downloads/firmware-${VERSION}
gh release download ${NIGHTLY_TAG} --repo iNavFlight/inav-nightly --pattern "*.hex"
```

### Verify firmware download:

```bash
ls *.hex | wc -l  # Should be ~219 files
```

### Rename firmware files:

Remove the CI build suffix and add RC number if applicable:

```bash
# For RC releases (e.g., 9.0.0-RC2):
# Changes: inav_9.0.0_ZEEZF7_ci-20251129-0e9f842.hex -> inav_9.0.0_RC2_ZEEZF7.hex
RC_NUM="RC2"  # Set to empty string for final releases
for f in *.hex; do
  # Extract target name (between version and _ci-)
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

```bash
# Verify renamed files
ls *.hex | head -5
```

## Step 3: Download Configurator Builds

### Find the CI workflow run:

```bash
cd inav-configurator
gh run list --limit 10 --json databaseId,headBranch,status,conclusion
```

### Download and organize artifacts by platform:

**CRITICAL:** Keep each platform in separate subdirectories to prevent cross-platform contamination.

```bash
RUN_ID="<run-id>"

# Create platform-specific directories
BASE_DIR="claude/release-manager/downloads/configurator-${VERSION}"
mkdir -p "${BASE_DIR}"/{linux,macos,windows}

# Download all artifacts to temp directory
cd "${BASE_DIR}"
mkdir -p _temp
cd _temp
gh run download ${RUN_ID} --repo iNavFlight/inav-configurator
```

### Organize by platform:

```bash
# Move Linux artifacts
find . -name "*linux*" -o -name "*_DEB" -o -name "*_RPM" | while read artifact; do
  find "$artifact" -type f -exec mv {} ../linux/ \;
done

# Move macOS artifacts
find . -name "*MacOS*" -o -name "*darwin*" -o -name "*_DMG" | while read artifact; do
  find "$artifact" -type f -exec mv {} ../macos/ \;
done

# Move Windows artifacts
find . -name "*Win*" -o -name "*_MSI" | while read artifact; do
  find "$artifact" -type f -exec mv {} ../windows/ \;
done

# Remove temp directory and empty subdirs
cd ..
rm -rf _temp
```

### Verify organization:

```bash
echo "=== Linux artifacts ==="
ls -lh linux/
echo "=== macOS artifacts ==="
ls -lh macos/
echo "=== Windows artifacts ==="
ls -lh windows/
```

### Verify macOS DMG contents:

**CRITICAL:** Before upload, verify DMGs don't contain Windows executables.

```bash
cd macos/

for dmg in *.dmg; do
  echo "Verifying: $dmg"

  # Mount the DMG
  hdiutil attach "$dmg" -quiet

  # Find mount point
  MOUNT_POINT=$(hdiutil info | grep "/Volumes/INAV" | awk '{print $3}')

  # Check for Windows executables (SHOULD BE NONE)
  echo "  Checking for .exe files..."
  EXE_COUNT=$(find "$MOUNT_POINT" -name "*.exe" 2>/dev/null | wc -l)
  if [ "$EXE_COUNT" -gt 0 ]; then
    echo "  ❌ ERROR: Found .exe files in macOS DMG!"
    find "$MOUNT_POINT" -name "*.exe"
  else
    echo "  ✅ No .exe files found"
  fi

  # Check architecture
  echo "  Checking architecture..."
  APP_PATH=$(find "$MOUNT_POINT" -name "*.app" -maxdepth 2 | head -1)
  if [ -n "$APP_PATH" ]; then
    BINARY="$APP_PATH/Contents/MacOS/inav-configurator"
    if [ -f "$BINARY" ]; then
      ARCH=$(lipo -info "$BINARY" 2>/dev/null | tail -1)
      echo "  Architecture: $ARCH"
    fi
  fi

  # Unmount
  hdiutil detach "$MOUNT_POINT" -quiet
  echo ""
done

cd ..
```

## Step 4: Report Summary

After downloading, report:
- Firmware: Number of hex files downloaded
- Configurator: List of packages downloaded
- Any missing or failed downloads

## Directory Structure

Downloads will be organized as:

```
claude/release-manager/downloads/
├── firmware-<version>/           # Hex files (flat)
│   ├── inav_9.0.0_RC2_MATEKF405.hex
│   └── ...
└── configurator-<version>/       # Configurator packages (BY PLATFORM)
    ├── linux/
    │   ├── INAV-Configurator_linux_x64_9.0.0.deb
    │   └── ...
    ├── macos/
    │   ├── INAV-Configurator_MacOS_arm64_9.0.0.dmg
    │   └── ...
    └── windows/
        ├── INAV-Configurator_Win64_9.0.0.msi
        └── ...
```

**Why platform separation?** In the 9.0.0 release, a Windows .exe was found inside a Mac DMG. The cause is uncertain, but platform separation and verification help prevent this type of contamination.

## Human Action Required

After downloads complete, the human must:
1. Verify file counts look reasonable
2. Upload files to the draft GitHub releases
3. Test at least one firmware and configurator build
4. Publish the releases

---

## Related Skills

- **upload-release-assets** - Upload downloaded artifacts to GitHub releases
