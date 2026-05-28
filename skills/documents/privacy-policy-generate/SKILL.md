---
name: privacy-policy-generate
description: Generate privacy policy for Android apps with GitHub Pages hosting
category: android
version: 1.0.0
inputs:
  - project_path: Path to Android project
  - developer_name: Developer or company name
  - contact_email: Contact email address
outputs:
  - docs/privacy-policy.md
  - docs/PRIVACY_SETUP.md
verify: "test -f docs/privacy-policy.md && grep -q 'Privacy Policy' docs/privacy-policy.md"
---

# Privacy Policy Generator

Generates a comprehensive privacy policy for Android apps by scanning the project and creating a GitHub Pages-ready Markdown document.

## Overview

**Why this is needed:**
- Google Play requires a privacy policy URL for all apps
- Privacy policy must be on a publicly accessible, non-geofenced URL
- Cannot be a PDF (must be HTML or plain text)
- Health Connect apps have additional disclosure requirements

**What this skill does:**
1. Scans AndroidManifest.xml for permissions and features
2. Analyzes build.gradle for third-party SDKs
3. Detects Health Connect integration
4. Prompts for missing information
5. Generates privacy policy in Markdown
6. Provides GitHub Pages setup instructions

## Prerequisites

- Android project with AndroidManifest.xml
- Git repository (for GitHub Pages hosting)
- Build configuration files (build.gradle.kts)

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| project_path | Yes | . | Android project root |
| developer_name | No | Prompted | Developer or company name |
| contact_email | No | Prompted | Contact email address |

## Process

### Step 1: Scan Project for App Information

**Extract from AndroidManifest.xml:**

```bash
# Get package name
PACKAGE_NAME=$(grep "package=" app/src/main/AndroidManifest.xml | head -1 | sed 's/.*package="\([^"]*\)".*/\1/')
echo "Package: $PACKAGE_NAME"

# Get app name (from strings.xml)
APP_NAME=$(grep 'name="app_name"' app/src/main/res/values/strings.xml | sed 's/.*>\([^<]*\)<.*/\1/')
echo "App name: $APP_NAME"

# Check for permissions
echo "Scanning permissions..."
PERMISSIONS=$(grep "<uses-permission" app/src/main/AndroidManifest.xml | sed 's/.*android:name="\([^"]*\)".*/\1/')

# Check for Health Connect
HEALTH_CONNECT=$(echo "$PERMISSIONS" | grep -i "health" || echo "")
if [[ -n "$HEALTH_CONNECT" ]]; then
    echo "✓ Health Connect detected"
fi
```

### Step 2: Analyze Third-Party SDKs

**Scan build.gradle.kts for common libraries:**

```bash
echo "Scanning dependencies..."

# Check for analytics
ANALYTICS=""
grep -q "firebase-analytics" app/build.gradle.kts && ANALYTICS="$ANALYTICS Firebase Analytics,"
grep -q "google-analytics" app/build.gradle.kts && ANALYTICS="$ANALYTICS Google Analytics,"

# Check for ads
ADS=""
grep -q "admob" app/build.gradle.kts && ADS="$ADS AdMob,"
grep -q "facebook-ads" app/build.gradle.kts && ADS="$ADS Facebook Audience Network,"

# Check for crash reporting
CRASH_REPORTING=""
grep -q "crashlytics" app/build.gradle.kts && CRASH_REPORTING="$CRASH_REPORTING Firebase Crashlytics,"

echo "Analytics: ${ANALYTICS:-None}"
echo "Ads: ${ADS:-None}"
echo "Crash reporting: ${CRASH_REPORTING:-None}"
```

### Step 3: Detect Health Connect Data Types

If Health Connect is detected, extract data types:

```bash
# Scan for Health Connect permission declarations
HEALTH_PERMISSIONS=$(grep "health.permission" app/src/main/AndroidManifest.xml || echo "")

# Common Health Connect data types
echo "Health data types detected:"
echo "$HEALTH_PERMISSIONS" | grep -i "STEPS" && echo "  - Steps (read/write)"
echo "$HEALTH_PERMISSIONS" | grep -i "HEART_RATE" && echo "  - Heart rate (read)"
echo "$HEALTH_PERMISSIONS" | grep -i "SLEEP" && echo "  - Sleep sessions (read)"
echo "$HEALTH_PERMISSIONS" | grep -i "EXERCISE" && echo "  - Exercise sessions (read/write)"
```

### Step 4: Prompt User for Missing Information

**Ask user for required information:**

> **Developer/Company Name:**
> (Detected from git config: {git config user.name})
> Press Enter to use detected value, or type a different name:

> **Contact Email:**
> (Detected from git config: {git config user.email})
> Press Enter to use detected value, or type a different email:

> **App Type:**
> 1. Free (no ads, no purchases)
> 2. Free with ads
> 3. Free with in-app purchases
> 4. Paid
> 5. Open source
> Select option (1-5):

> **Data Storage:**
> 1. All data stays on device (no cloud sync)
> 2. Data synced to cloud (specify service)
> 3. Both local and cloud storage
> Select option (1-3):

### Step 5: Generate Privacy Policy

Create `docs/privacy-policy.md` using the template:

```markdown
# Privacy Policy for {APP_NAME}

**Last updated:** {CURRENT_DATE}

{DEVELOPER_NAME} built the {APP_NAME} app as {APP_TYPE}. This SERVICE is provided at no cost and is intended for use as is.

## Information Collection and Use

For a better experience while using our Service, we may require you to provide us with certain personally identifiable information. The information that we request will be retained on your device and is not collected by us in any way.

{IF HEALTH_CONNECT}
## Health Data

This app integrates with **Health Connect** to access your health and fitness data.

**Health Data Types Accessed:**
{HEALTH_DATA_TYPES_LIST}

**Purpose:** This app collects health data to {HEALTH_PURPOSE}.

**Data Storage:** {DATA_STORAGE_DESCRIPTION}

**Data Sharing:** Your health data is not shared with third parties.
{/IF}

{IF THIRD_PARTY_SERVICES}
## Third-Party Services

This app uses the following third-party services:

{THIRD_PARTY_LIST}
{/IF}

{IF ADS}
## Advertising

This app displays advertisements using {AD_NETWORKS}. These services may collect information about your device and usage patterns.
{/IF}

## Log Data

In case of an error in the app, we collect data called Log Data. This Log Data may include information such as your device's Internet Protocol ("IP") address, device name, operating system version, the configuration of the app, the time and date of your use of the Service, and other statistics.

## Security

We value your trust in providing us your Personal Information, thus we are striving to use commercially acceptable means of protecting it. But remember that no method of transmission over the internet, or method of electronic storage is 100% secure and reliable, and we cannot guarantee its absolute security.

## Children's Privacy

This Service does not address anyone under the age of 13. We do not knowingly collect personally identifiable information from children under 13.

## Changes to This Privacy Policy

We may update our Privacy Policy from time to time. Thus, you are advised to review this page periodically for any changes. We will notify you of any changes by posting the new Privacy Policy on this page.

## Contact Us

If you have any questions or suggestions about our Privacy Policy, do not hesitate to contact us at: {CONTACT_EMAIL}

---

*This privacy policy is hosted on [GitHub Pages](https://{USERNAME}.github.io/{REPO}/privacy-policy)*
```

### Step 6: Create Privacy Setup Instructions

Create `docs/PRIVACY_SETUP.md`:

```markdown
# Privacy Policy Setup for GitHub Pages

## Overview

Your privacy policy has been generated at `docs/privacy-policy.md` and is ready to be hosted on GitHub Pages.

## Setup Steps

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under "Source", select **Deploy from a branch**
4. Select branch: **main** (or **master**)
5. Select folder: **/docs**
6. Click **Save**

### 2. Wait for Deployment

GitHub Pages will automatically build and deploy your site. This usually takes 1-2 minutes.

You can check the deployment status under **Actions** tab.

### 3. Verify Privacy Policy URL

Once deployed, your privacy policy will be available at:

**https://{USERNAME}.github.io/{REPO}/privacy-policy**

Test the URL in your browser to confirm it's accessible.

### 4. Add URL to Play Console

1. Open [Google Play Console](https://play.google.com/console)
2. Select your app
3. Go to **App content** → **Privacy policy**
4. Enter the URL: `https://{USERNAME}.github.io/{REPO}/privacy-policy`
5. Click **Save**

## Custom Domain (Optional)

If you want to use a custom domain:

1. Add a `CNAME` file to `docs/`:
   ```
   privacy.yourdomain.com
   ```

2. Configure DNS at your domain registrar:
   - Type: CNAME
   - Name: privacy (or your subdomain)
   - Value: {USERNAME}.github.io

3. Update the privacy policy URL in Play Console

## Health Apps Declaration

⚠️ **Important:** If your app uses Health Connect, you must also:

1. Go to Play Console → **App content** → **Health**
2. Complete the Health Apps declaration form
3. List all health data types your app accesses
4. Explain how the data is used
5. Confirm your privacy policy includes health data disclosure

## Troubleshooting

### "404 Not Found"
- Wait 2-3 minutes for deployment to complete
- Verify GitHub Pages is enabled in repository settings
- Check that `docs/privacy-policy.md` exists on main branch

### "Privacy policy URL required"
- Ensure URL is publicly accessible (not behind login)
- URL must use HTTPS
- Cannot be a PDF or editable document

## Next Steps

After privacy policy is live:
- Test the URL is publicly accessible
- Add URL to Play Console
- Complete other Play Console requirements (content rating, data safety, etc.)
- Run `/devtools:android-playstore-scan` to verify all requirements
```

## Verification

**MANDATORY:** Run these commands:

```bash
# Verify privacy policy created
test -f docs/privacy-policy.md && echo "✓ Privacy policy created"

# Verify setup guide created
test -f docs/PRIVACY_SETUP.md && echo "✓ Setup guide created"

# Check privacy policy contains required sections
grep -q "Privacy Policy" docs/privacy-policy.md && echo "✓ Title present"
grep -q "Contact" docs/privacy-policy.md && echo "✓ Contact info present"

# Check for Health Connect section if applicable
if grep -q "health.permission" app/src/main/AndroidManifest.xml; then
    grep -q "Health Data" docs/privacy-policy.md && echo "✓ Health data section present"
fi
```

**Expected output:**
- ✓ Privacy policy created
- ✓ Setup guide created
- ✓ Title present
- ✓ Contact info present
- (✓ Health data section present - if Health Connect is used)

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Privacy policy | docs/privacy-policy.md | Generated privacy policy |
| Setup guide | docs/PRIVACY_SETUP.md | GitHub Pages setup instructions |

## Templates

### Health Connect Data Purpose Examples

For the health data purpose section, use one of these based on user input:

- **Fitness tracking:** "to track your fitness activities and provide insights into your health patterns"
- **Health monitoring:** "to monitor your health metrics and help you achieve your wellness goals"
- **Data sync:** "to sync your health data across devices"
- **Custom:** User provides their own description

### Third-Party Service Links

Common third-party services and their privacy policy URLs:

- **Health Connect:** https://support.google.com/android/answer/12098244
- **Firebase Analytics:** https://firebase.google.com/policies/analytics
- **Google Analytics:** https://policies.google.com/privacy
- **AdMob:** https://support.google.com/admob/answer/6128543
- **Crashlytics:** https://firebase.google.com/support/privacy

## Troubleshooting

### "Cannot find app name"
**Cause:** app_name not defined in strings.xml
**Fix:** Add `<string name="app_name">Your App Name</string>` to res/values/strings.xml

### "Git config not found"
**Cause:** Git user not configured
**Fix:** Run `git config --global user.name "Your Name"` and `git config --global user.email "email@example.com"`

### "Health permissions not detected"
**Cause:** Health Connect permissions not declared in manifest
**Fix:** Verify permissions are correctly declared in AndroidManifest.xml

## Play Console Requirements

Your privacy policy MUST:
- ✅ Be hosted on a publicly accessible URL (HTTPS)
- ✅ Be non-editable (static page is fine)
- ✅ Not be a PDF
- ✅ Not be geofenced (accessible worldwide)
- ✅ Include health data disclosure (if using Health Connect)
- ✅ Be linked from your app or store listing

## Completion Criteria

- [ ] `docs/privacy-policy.md` exists with complete content
- [ ] `docs/PRIVACY_SETUP.md` exists with setup instructions
- [ ] Privacy policy includes all detected features (Health Connect, ads, etc.)
- [ ] Developer name and contact email are correct
- [ ] Privacy policy reviewed and customized as needed
- [ ] Ready to enable GitHub Pages
