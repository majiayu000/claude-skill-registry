---
name: android-app-icon
description: Generate Android adaptive icons from Iconify's 200k+ open source icons
category: android
---

# Android App Icon

Generate Android adaptive icons using VectorDrawables from Iconify's 200k+ icon library.

## How This Skill Works

This skill uses **executable scripts** for reliable, deterministic icon generation. The agent's role is to:

1. Run scripts with user-confirmed parameters
2. Present results and wait for user decisions
3. Verify output

**Scripts location:** `~/claude-devtools/skills/android-app-icon/scripts/`

| Script | Purpose |
|--------|---------|
| `search-icons.sh <term>` | Search Iconify for icons |
| `generate-app-icons.sh <icon-id>` | Generate all icon assets |

---

## Checklist

### Prerequisites

- [ ] Project has `minSdk >= 26` → [Verify](#verifying-minsdk)
- [ ] `curl` is installed
- [ ] `python3` is installed
- [ ] `rsvg-convert` is installed → [Install instructions](#installing-rsvg-convert)

### Steps

- [ ] **Step 1:** Check for existing legacy icons → [Details](#step-1-check-for-existing-legacy-icons)
- [ ] ⏸️ **WAIT:** If legacy icons found, ask user whether to delete them
- [ ] **Step 2:** Get search term from user → [Details](#step-2-get-search-term)
- [ ] ⏸️ **WAIT:** User confirms or provides search term
- [ ] **Step 3:** Run search script → [Details](#step-3-search-for-icons)
- [ ] ⏸️ **WAIT:** User selects icon from results
- [ ] **Step 4:** Run generate script → [Details](#step-4-generate-icons)
- [ ] **Step 5:** Verify build → [Details](#step-5-verify)

### Completion Criteria

- [ ] All legacy icons removed (if user confirmed)
- [ ] `app/src/main/res/drawable/ic_launcher_foreground.xml` exists
- [ ] `app/src/main/res/drawable/ic_launcher_background.xml` exists
- [ ] `app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml` exists
- [ ] `app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml` exists
- [ ] `fastlane/metadata/android/en-US/images/icon.png` exists
- [ ] `./gradlew assembleDebug` succeeds

---

## Reference Details

### Verifying minSdk

Check `app/build.gradle.kts` or `app/build.gradle`:

```kotlin
android {
    defaultConfig {
        minSdk = 26  // Must be 26 or higher
    }
}
```

### Installing rsvg-convert

**macOS:**
```bash
brew install librsvg
```

**Ubuntu/Debian:**
```bash
sudo apt install librsvg2-bin
```

**Verify:**
```bash
rsvg-convert --version
```

---

### Step 1: Check for Existing Legacy Icons

Check for legacy raster icons that are not needed for minSdk 26+:

```bash
find app/src/main/res/mipmap-mdpi app/src/main/res/mipmap-hdpi \
     app/src/main/res/mipmap-xhdpi app/src/main/res/mipmap-xxhdpi \
     app/src/main/res/mipmap-xxxhdpi \
     \( -name "ic_launcher*.webp" -o -name "ic_launcher*.png" \) \
     2>/dev/null
```

**If files are found, present to user:**

> "I found existing legacy icon files:
> - `mipmap-mdpi/ic_launcher.webp`
> - `mipmap-hdpi/ic_launcher.webp`
> - ... (list all)
>
> These are not needed for minSdk 26+ (VectorDrawables are used instead).
>
> Would you like me to delete them? (y/n)"

**If user confirms deletion:**
```bash
find app/src/main/res/mipmap-mdpi app/src/main/res/mipmap-hdpi \
     app/src/main/res/mipmap-xhdpi app/src/main/res/mipmap-xxhdpi \
     app/src/main/res/mipmap-xxxhdpi \
     \( -name "ic_launcher*.webp" -o -name "ic_launcher*.png" \) \
     -delete 2>/dev/null
```

---

### Step 2: Get Search Term

Auto-detect from project context:

```bash
# From package name in build.gradle.kts
grep -E 'namespace|applicationId' app/build.gradle.kts 2>/dev/null

# From app name in strings.xml
grep 'name="app_name"' app/src/main/res/values/strings.xml 2>/dev/null
```

**Present to user:**

> "Based on your project, I suggest searching for: `{detected_term}`
>
> Would you like to:
> 1. Use `{detected_term}`
> 2. Enter a different search term"

---

### Step 3: Search for Icons

Run the search script with the confirmed search term:

```bash
~/claude-devtools/skills/android-app-icon/scripts/search-icons.sh "<search-term>"
```

**Present results to user:**

> "Found icons matching '{search-term}':
>
> 1. `mdi:heart-pulse` - Material Design Icons (Apache 2.0)
> 2. `healthicons:health-worker` - Health Icons (MIT)
> 3. ...
>
> Preview: https://icon-sets.iconify.design/mdi/heart-pulse/
>
> Enter a number to select, or type a different search term:"

---

### Step 4: Generate Icons

Run the generate script from the project root:

```bash
cd /path/to/android/project
~/claude-devtools/skills/android-app-icon/scripts/generate-app-icons.sh "<icon-id>"
```

The script auto-detects:
- Background color from `themes.xml` → `colors.xml`
- Scale factor (default 1.15)
- Output paths

**Optional overrides (if user requests):**
```bash
ICON_BACKGROUND="#2196F3" ICON_SCALE="1.2" \
  ~/claude-devtools/skills/android-app-icon/scripts/generate-app-icons.sh <icon-id>
```

---

### Step 5: Verify

```bash
./gradlew assembleDebug
```

Check all files exist:
```bash
test -f app/src/main/res/drawable/ic_launcher_foreground.xml && echo "✓ foreground"
test -f app/src/main/res/drawable/ic_launcher_background.xml && echo "✓ background"
test -f app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml && echo "✓ ic_launcher"
test -f app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml && echo "✓ ic_launcher_round"
test -f fastlane/metadata/android/en-US/images/icon.png && echo "✓ play store icon"
```

---

## Troubleshooting

### Icon appears cut off
Reduce scale: `ICON_SCALE=1.0 generate-app-icons.sh <icon>`

### rsvg-convert not found
See [Installing rsvg-convert](#installing-rsvg-convert)

### Icon not found
Verify icon ID at https://icon-sets.iconify.design/
