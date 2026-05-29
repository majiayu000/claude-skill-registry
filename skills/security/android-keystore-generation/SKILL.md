---
name: android-keystore-generation
description: Generate production and local development keystores for Android release signing
category: android
version: 1.0.0
inputs:
  - project_path: Path to Android project
  - organization: Organization name for certificate
  - country_code: 2-letter country code (optional)
outputs:
  - keystores/production-release.jks
  - keystores/local-dev-release.jks
  - keystores/KEYSTORE_INFO.txt
verify: "ls keystores/*.jks && cat keystores/KEYSTORE_INFO.txt"
---

# Android Keystore Generation

Generates dual keystores for Android release signing: production (CI/CD only) and local development.

## Prerequisites

- JDK installed (`keytool` command available)
- Write access to project directory

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| project_path | Yes | . | Android project root |
| organization | Yes | - | Organization name for certificate DN |
| country_code | No | US | 2-letter country code |

## Process

### Organization Name

**ALWAYS prompt the user, but provide the auto-detected value as default.**

**Step 1: Detect organization from package name**
```bash
# Extract package name from build.gradle.kts
PACKAGE=$(grep "applicationId" app/build.gradle.kts | sed 's/.*"\(.*\)".*/\1/')
echo "Package: $PACKAGE"

# Extract second segment: com.{ORG}.app → ORG
ORG=$(echo $PACKAGE | cut -d. -f2)
echo "Detected organization: $ORG"
```

**Step 2: MANDATORY - Ask the user for confirmation**

⛔ **DO NOT SKIP THIS PROMPT**

Ask the user:
> "The detected organization name is **{ORG}**.
> Press Enter to use this, or type a different name:"

Wait for user response. Use their input if provided, otherwise use the detected default.

**Step 3: Store the confirmed organization name**
```bash
ORGANIZATION="{confirmed_org_name}"
echo "Using organization: $ORGANIZATION"
```

**Why this matters:** The organization appears in the certificate's Distinguished Name.
While it doesn't affect app functionality, users may want to customize it.

### Password Generation Options

**Choose one option for keystore passwords:**

#### Option 1 (Recommended): User-Provided Password

Ask the user to provide a password for the production keystore:

> "Please enter a password for the production keystore (minimum 12 characters, mix of letters, numbers, and symbols):"

**Security benefits:**
- Password never visible to the agent during the conversation
- User has complete control over password strength and storage
- Reduces risk of password exposure in logs or conversation history

**Instructions for user:**
```bash
# User will run keytool command manually with their chosen password
# Example:
keytool -genkeypair -v \
  -keystore keystores/production-release.jks \
  -storetype PKCS12 \
  -alias upload \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass "YOUR_PASSWORD_HERE" \
  -keypass "YOUR_PASSWORD_HERE" \
  -dname "CN=Android Release, OU=Android, O={ORGANIZATION}, C=US"
```

#### Option 2: Generated Password

If the user prefers a generated password, use the automated generation steps below.

**Note:** The agent will have access to this password during the session. The password will be stored in temporary files and KEYSTORE_INFO.txt.

> "Would you like me to generate a secure password? (The agent will see this password during generation)"

If yes, proceed with the automated generation steps.

### Step 1: Create Keystores Directory

```bash
mkdir -p keystores
```

### Step 2: Generate Production Keystore

**SECURITY:** This keystore is for CI/CD only. Never use locally.

**⚠️ IMPORTANT: Run each command in a SEPARATE bash call. Do NOT combine commands.**

**Step 2a: Generate password and save to file**
```bash
openssl rand -base64 24 | tr -d '/+=' | head -c 24 > /tmp/prod_password.txt
```

**Step 2b: Read and display the password**
```bash
cat /tmp/prod_password.txt
```
📝 **Copy this password now** - you'll need it for the keytool command and KEYSTORE_INFO.txt

**Step 2c: Generate the keystore**

Replace `{PASSWORD}` with the password from Step 2b, and `{ORGANIZATION}` with the confirmed organization name:

```bash
keytool -genkeypair -v \
  -keystore keystores/production-release.jks \
  -storetype PKCS12 \
  -alias upload \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass "{PASSWORD}" \
  -keypass "{PASSWORD}" \
  -dname "CN=Android Release, OU=Android, O={ORGANIZATION}, C=US"
```

**If keytool prompts for confirmation**, type `yes` and press Enter.

**Step 2d: Verify keystore was created**
```bash
ls -la keystores/production-release.jks
```

**Expected output:**
```
-rw-------  1 user  staff  2557 Dec 11 10:30 keystores/production-release.jks
```

### Step 3: Generate Local Development Keystore

**⚠️ IMPORTANT: Run each command in a SEPARATE bash call. Do NOT combine commands.**

**Step 3a: Generate password and save to file**
```bash
openssl rand -base64 24 | tr -d '/+=' | head -c 24 > /tmp/local_password.txt
```

**Step 3b: Read and display the password**
```bash
cat /tmp/local_password.txt
```
📝 **Copy this password now** - you'll need it for the keytool command and KEYSTORE_INFO.txt

**Step 3c: Generate the keystore**

Replace `{PASSWORD}` with the password from Step 3b:

```bash
keytool -genkeypair -v \
  -keystore keystores/local-dev-release.jks \
  -storetype PKCS12 \
  -alias local-dev \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -storepass "{PASSWORD}" \
  -keypass "{PASSWORD}" \
  -dname "CN=Local Development, OU=Development, O=Local, C=US"
```

**If keytool prompts for confirmation**, type `yes` and press Enter.

**Step 3d: Verify keystore was created**
```bash
ls -la keystores/local-dev-release.jks
```

**Expected output:**
```
-rw-------  1 user  staff  2557 Dec 11 10:30 keystores/local-dev-release.jks
```

### Step 4: Create Credentials File

```bash
cat > keystores/KEYSTORE_INFO.txt << EOF
Production Keystore
===================
File: production-release.jks
Alias: upload
Store Password: $PROD_PASSWORD
Key Password: $PROD_PASSWORD (same as store - PKCS12 requirement)

⚠️ SECURITY: CI/CD ONLY - Never use on developer machines

GitHub Secrets:
  SIGNING_KEY_STORE_BASE64: $(base64 -w 0 keystores/production-release.jks 2>/dev/null || base64 -i keystores/production-release.jks)
  SIGNING_KEY_ALIAS: upload
  SIGNING_STORE_PASSWORD: $PROD_PASSWORD
  SIGNING_KEY_PASSWORD: $PROD_PASSWORD

---

Local Development Keystore
==========================
File: local-dev-release.jks
Alias: local-dev
Store Password: $LOCAL_PASSWORD
Key Password: $LOCAL_PASSWORD

Add to ~/.gradle/gradle.properties:
  SIGNING_KEY_STORE_PATH=$(pwd)/keystores/local-dev-release.jks
  SIGNING_KEY_ALIAS=local-dev
  SIGNING_STORE_PASSWORD=$LOCAL_PASSWORD
  SIGNING_KEY_PASSWORD=$LOCAL_PASSWORD
EOF
```

### Step 5: Update .gitignore

```bash
# Add to .gitignore if not present
grep -q "keystores/" .gitignore 2>/dev/null || echo "keystores/" >> .gitignore
grep -q "*.jks" .gitignore 2>/dev/null || echo "*.jks" >> .gitignore
```

## Verification

**MANDATORY:** Run these commands:

```bash
# Verify keystores exist
ls -la keystores/*.jks

# Verify credentials documented
cat keystores/KEYSTORE_INFO.txt

# Verify gitignored
grep "keystores" .gitignore
```

**Expected output:**
- Two .jks files in keystores/
- KEYSTORE_INFO.txt with passwords
- keystores/ in .gitignore

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Production keystore | keystores/production-release.jks | For CI/CD only |
| Local keystore | keystores/local-dev-release.jks | For local testing |
| Credentials | keystores/KEYSTORE_INFO.txt | Passwords and setup info |

## Troubleshooting

### "keytool: command not found"
**Cause:** JDK not installed or not in PATH
**Fix:** Install JDK 17: `brew install openjdk@17` (macOS) or `apt install openjdk-17-jdk` (Linux)

### "openssl: command not found"
**Cause:** OpenSSL not installed
**Fix:** Use alternative password generation: `head -c 24 /dev/urandom | base64`

## Completion Criteria

- [ ] `keystores/production-release.jks` exists
- [ ] `keystores/local-dev-release.jks` exists
- [ ] `keystores/KEYSTORE_INFO.txt` exists with passwords
- [ ] `keystores/` is in `.gitignore`
