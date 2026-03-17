---
name: release-manager
description: Build, package, tag, and release Naki app to GitHub. Use when the user asks to "release", "publish", "tag", "build DMG/ZIP", or "upgrade version". Handles the complete release workflow from build to GitHub release creation.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Release Manager Skill

Base directory: {baseDir}

## Quick Release

```bash
# 完整發布腳本 (推薦)
bash {baseDir}/scripts/release.sh <version>
# Example: bash {baseDir}/scripts/release.sh 2.3.1
```

## Release Workflow

```
1. Generate Release Notes → git log $PREV_TAG..HEAD
2. Build App             → xcodebuild -configuration Release
3. Create Packages       → DMG + ZIP in dist/
4. Update Version        → README.md, CLAUDE.md, project.pbxproj
5. Create Git Tag        → git tag -a "v$VERSION"
6. Push to Remote        → git push origin main && git push --tags
7. GitHub Release        → gh release create with assets
```

## Step-by-Step Commands

### 1. Build Release App

```bash
xcodebuild clean build \
  -project Naki.xcodeproj \
  -scheme Naki \
  -configuration Release \
  -derivedDataPath ./build \
  CODE_SIGN_IDENTITY="-" \
  CODE_SIGNING_REQUIRED=NO
```

### 2. Create Packages

```bash
# Locate built app
APP_PATH=$(find ./build -name "Naki.app" -type d | head -1)

# Create dist directory
mkdir -p dist

# ZIP
cd "$(dirname "$APP_PATH")" && zip -r -y ../../../dist/Naki.zip Naki.app && cd -

# DMG
mkdir -p dmg_temp && cp -R "$APP_PATH" dmg_temp/
hdiutil create -volname "Naki" -srcfolder dmg_temp -ov -format UDZO dist/Naki.dmg
rm -rf dmg_temp
```

### 3. Update Version & Tag

```bash
VERSION="2.3.1"  # Set your version

# Update version in files
sed -i '' "s/Version-[0-9.]*-green/Version-$VERSION-green/" README.md
sed -i '' "s/| Version | [0-9.]* |/| Version | $VERSION |/" CLAUDE.md

# Commit and tag
git add README.md CLAUDE.md Naki.xcodeproj/project.pbxproj
git commit -m "chore: Release v$VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin main && git push origin "v$VERSION"
```

### 4. GitHub Release

```bash
gh release create "v$VERSION" \
  --title "Naki v$VERSION" \
  --generate-notes \
  dist/Naki.dmg dist/Naki.zip
```

## Version Guidelines (Semantic Versioning)

| Type | When | Example |
|------|------|---------|
| PATCH | Bug 修復、小調整 | 2.3.0 → 2.3.1 |
| MINOR | 新功能、新工具 | 2.3.0 → 2.4.0 |
| MAJOR | 架構重構、不相容變更 | 2.3.0 → 3.0.0 |

## Pre-release Checklist

- [ ] All changes committed: `git status`
- [ ] Build succeeds without errors
- [ ] On correct branch (usually `main`)
- [ ] Previous tag exists: `git describe --tags --abbrev=0`

## Resource Index

| Resource | Purpose | Load When |
|----------|---------|-----------|
| `{baseDir}/scripts/release.sh` | 完整發布腳本 | 執行完整發布 |
| `{baseDir}/references/reference.md` | 版本位置、構建配置詳情 | 需要詳細參數 |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | `xcodebuild -project Naki.xcodeproj -list` |
| DMG fails | Check disk space: `df -h` |
| gh not authorized | `gh auth login` |
| Tag exists | `git tag -d "v$VERSION"` then retry |

---

**Release Manager v1.1** - Streamlined Release Workflow
