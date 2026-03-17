---
name: android-playstore-api-validation
description: Create and run validation script to test Play Store API connection
category: android
version: 1.0.0
inputs:
  - service_account_json_path: Path to service account JSON
  - package_name: Android app package name
outputs:
  - scripts/validate-playstore.py
verify: "python3 scripts/validate-playstore.py"
---

# Android Play Store API Validation

Creates a validation script to test Play Store API connection and permissions.

## Prerequisites

- Service account created (run `android-service-account-guide` first)
- Service account JSON file downloaded
- Python 3 installed
- Package name known

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| service_account_json_path | Yes | - | Path to JSON key file |
| package_name | Yes | - | App package name |

## Process

### Step 1: Create Validation Script

Create `scripts/validate-playstore.py`:

```python
#!/usr/bin/env python3
"""
Validate Google Play Store API connection and permissions.

Usage:
    python3 validate-playstore.py SERVICE_ACCOUNT.json com.example.app
"""

import sys
import json
from pathlib import Path

def validate_json_file(json_path):
    """Validate service account JSON file."""
    print(f"📋 Validating service account JSON: {json_path}")

    if not Path(json_path).exists():
        print(f"❌ File not found: {json_path}")
        return False

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        missing = [f for f in required_fields if f not in data]

        if missing:
            print(f"❌ Missing required fields: {', '.join(missing)}")
            return False

        if data['type'] != 'service_account':
            print(f"❌ Invalid type: {data['type']} (expected: service_account)")
            return False

        print(f"✅ Service account JSON is valid")
        print(f"   Project: {data['project_id']}")
        print(f"   Email: {data['client_email']}")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False

def test_api_connection(json_path, package_name):
    """Test Play Developer API connection."""
    print(f"\n🔌 Testing Play Developer API connection...")
    print(f"   Package: {package_name}")

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(
            json_path,
            scopes=['https://www.googleapis.com/auth/androidpublisher']
        )

        # Build service
        service = build('androidpublisher', 'v3', credentials=credentials)

        # Test API call - get app details
        try:
            edit_request = service.edits().insert(
                body={},
                packageName=package_name
            )
            edit = edit_request.execute()
            edit_id = edit['id']

            # Clean up edit
            service.edits().delete(
                editId=edit_id,
                packageName=package_name
            ).execute()

            print(f"✅ Successfully connected to Play Developer API")
            print(f"✅ Can access package: {package_name}")
            return True

        except Exception as e:
            error_msg = str(e)
            if '404' in error_msg:
                print(f"❌ Package not found: {package_name}")
                print(f"   Make sure app exists in Play Console")
            elif '403' in error_msg or 'permission' in error_msg.lower():
                print(f"❌ Permission denied")
                print("Error: Service account needs 'Release apps to production tracks' permission.")
                print("In Play Console: Setup > API access > Grant access > select your service account")
                print("Required: 'Release to production, exclude devices, and use Play App Signing'")
            else:
                print(f"❌ API error: {error_msg}")
            return False

    except ImportError:
        print(f"❌ Required libraries not installed")
        print(f"   Run: pip install google-auth google-api-python-client")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main validation function."""
    if len(sys.argv) != 3:
        print("Usage: python3 validate-playstore.py SERVICE_ACCOUNT.json PACKAGE_NAME")
        print("")
        print("Example:")
        print("  python3 validate-playstore.py ~/service-account.json com.example.app")
        sys.exit(1)

    json_path = sys.argv[1]
    package_name = sys.argv[2]

    print("=" * 60)
    print("Google Play Store API Validation")
    print("=" * 60)

    # Step 1: Validate JSON
    if not validate_json_file(json_path):
        sys.exit(1)

    # Step 2: Test API connection
    if not test_api_connection(json_path, package_name):
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✅ All validations passed!")
    print("=" * 60)
    print("\nYour Play Store API setup is ready for deployment.")
    print("\nNext steps:")
    print("  1. Add SERVICE_ACCOUNT_JSON_PLAINTEXT to GitHub Secrets")
    print("  2. Run: /devtools:android-playstore-publish")
    print("  3. Deploy your app!")

if __name__ == '__main__':
    main()
```

### Step 2: Make Script Executable

```bash
chmod +x scripts/validate-playstore.py
```

### Step 3: Create Requirements File

Create `scripts/requirements-playstore.txt`:

```
google-auth==2.23.0
google-api-python-client==2.100.0
```

### Step 4: Create Validation Documentation

Add to `distribution/PLAY_CONSOLE_SETUP.md`:

```markdown
## Validation

After completing setup, validate your configuration:

```bash
# Install required packages
pip install -r scripts/requirements-playstore.txt

# Run validation
python3 scripts/validate-playstore.py \
  ~/path/to/service-account.json \
  com.example.yourapp
```

Expected output:
```
✅ Service account JSON is valid
✅ Successfully connected to Play Developer API
✅ Can access package: com.example.yourapp
✅ All validations passed!
```

If validation fails, check:
- Service account has "Release" permission in Play Console
- Play Developer API is enabled
- Package name matches exactly
- Waited 5-10 minutes for permissions to propagate
```
```

## Verification

**MANDATORY:** Run the validation script:

### Step 1: Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 2: Install dependencies

```bash
pip install google-auth google-api-python-client
```

### Step 3: Run validation

```bash
python3 scripts/validate-playstore.py \
  /path/to/service-account.json \
  com.example.app
```

### Step 4: Deactivate when done

```bash
deactivate
```

**Expected output:**
```
✅ Service account JSON is valid
✅ Successfully connected to Play Developer API
✅ Can access package: com.example.app
✅ All validations passed!
```

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Validation script | scripts/validate-playstore.py | API connection tester |
| Requirements | scripts/requirements-playstore.txt | Python dependencies |

## Troubleshooting

### "Package not found"
**Cause:** App doesn't exist in Play Console or package name mismatch
**Fix:** Create app in Play Console first, verify exact package name

### "Permission denied"
**Cause:** Service account lacks permissions
**Fix:** Grant "Release" permission in Play Console → API access

### "Libraries not installed"
**Cause:** Missing Python packages
**Fix:** `pip install google-auth google-api-python-client`

### "403 Forbidden"
**Cause:** Permissions not yet propagated
**Fix:** Wait 5-10 minutes after granting permissions, then retry

## Completion Criteria

- [ ] `scripts/validate-playstore.py` exists
- [ ] `scripts/requirements-playstore.txt` exists
- [ ] Script is executable
- [ ] Validation script runs successfully
- [ ] API connection confirmed
