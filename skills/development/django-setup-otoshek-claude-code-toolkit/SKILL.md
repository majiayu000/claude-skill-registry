---
name: django-setup
description: Initialize Django projects for HTTPS development with virtual environments and mkcert SSL certificates
---

## Overview

**This skill sets up Django for HTTPS development** with virtual environments and local SSL certificates.

# Artifacts Builder

To set up Django for HTTPS development with virtual environments and local SSL certificates, follow these steps:
1. Verify/Install Python
2. Create Virtual Environment
3. Install Django and Dependencies
4. Create Django Project
5. Set Up HTTPS
6. Configure settings.py
7. Create a health API
8. Add import and URL routes to urls.py
9. Apply Initial Migrations
10. Test HTTPS Server
11. Create .gitignore



## Step 1: Verify/Install Python

### Check for Python 3.8 - 3.13

**Check all available Python versions:**
Detect the operating system by running `uname -s 2>/dev/null || echo %OS% 2>/dev/null || ver`

Execute the platform-specific command based on the detected system.

```bash
# macOS/Linux
for v in 3.8 3.9 3.10 3.11 3.12 3.13; do
  if command -v python$v >/dev/null 2>&1; then
    echo "✅ Python $v found: $(python$v --version)"
  else
    echo "❌ Python $v not found"
  fi
done
```

```bash
# Windows
$versions = 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
foreach ($v in $versions) {
    try {
        $output = py -$v --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python $v found: $output"
        } else {
            Write-Host "❌ Python $v not found"
        }
    } catch {
        Write-Host "❌ Python $v not found"
    }
}
```

**Strategy:**
- If you have **any** Python 3.8 - 3.13, use the **highest version**
- If no compatible Python found, install **Python 3.13**

### Install Python 3.13 (if needed)

**No compatible Python?** See platform-specific installation:
- macOS → [platform-install/macos.md](platform-install/macos.md)
- Ubuntu/Debian → [platform-install/linux-ubuntu.md](platform-install/linux-ubuntu.md)
- Fedora/RHEL → [platform-install/linux-fedora.md](platform-install/linux-fedora.md)
- Windows → [platform-install/windows.md](platform-install/windows.md)

**Verify installation:**
```bash
python3.13 --version  # or python3.12, python3.11, etc.
which python3.13      # macOS/Linux
where python          # Windows
```

---

## Step 2: Create Virtual Environment

**Create venv with your Python version:**
```bash
# Use highest available version
python3.13 -m venv venv  # macOS/Linux
py -3.13 -m venv venv    # Windows

# Or use default python3
python3 -m venv venv
```

**Verify creation:**
```bash
ls venv/bin/activate     # macOS/Linux - should exist
dir venv\Scripts\activate  # Windows - should exist
```

**Errors?** See [troubleshooting/venv-issues.md](troubleshooting/venv-issues.md)

---

## Step 3: Install Django and Dependencies

**Activate virtual environment and upgrade pip:**
```bash
# macOS/Linux
source venv/bin/activate
pip install --upgrade pip

# Windows (PowerShell)
venv\Scripts\Activate.ps1
pip install --upgrade pip

# Windows (CMD)
venv\Scripts\activate.bat
pip install --upgrade pip
```

**Install core dependencies:**
```bash
pip install Django python-dotenv djangorestframework
```

**What's installed:**
- **Django** - Web framework
- **python-dotenv** - Environment variable management (for secrets)
- **djangorestframework** - REST API toolkit (optional but recommended)

**Update requirements.txt:**
```bash
pip freeze > requirements.txt
```

**Installation issues?** See [troubleshooting/pip-problems.md](troubleshooting/pip-problems.md)

---

## Step 4: Create Django Project

**Create project in current directory (flat structure):**
```bash
django-admin startproject backend .
```

**Important:** The `.` creates the project in your current directory, not a subdirectory.

**Verify creation:**
```bash
ls manage.py  # Should exist
ls backend/settings.py  # Should exist
```

---

## Step 5: Set Up HTTPS with mkcert

### Detect Operating System

Detect the operating system if you have not done it yet by running:
```bash
uname -s 2>/dev/null || echo %OS% 2>/dev/null || ver
```

### Platform-Specific Instructions

Follow the instructions for your operating system:

- **macOS** → [platform-https/mkcert-https-setup-macos.md](platform-https/mkcert-https-setup-macos.md)
- **Ubuntu/Debian (Linux)** → [platform-https/mkcert-https-setup-linux.md](platform-https/mkcert-https-setup-linux.md)
- **Windows** → [platform-https/mkcert-https-setup-windows.md](platform-https/mkcert-https-setup-windows.md)

**What these guides cover:**
1. Installing mkcert
2. Installing local certificate authority
3. Creating SSL certificates directory
4. Installing Uvicorn (ASGI server with SSL support)
5. Updating requirements.txt
6. Creating platform-specific run script (run.sh or run.bat)

**Note:** Replace `backend` with your project name if different in the run scripts.

### Create VS Code launch configuration:**

For debugging in VS Code, create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django HTTPS (Uvicorn)",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "backend.asgi:application",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--ssl-keyfile", "./certs/localhost+2-key.pem",
        "--ssl-certfile", "./certs/localhost+2.pem",
        "--reload"
      ],
      "django": true,
      "justMyCode": true,
      "python": "${workspaceFolder}/venv/bin/python"
    }
  ]
}
```

---

## Step 6: Configure `settings.py`

### Find the settings file using Glob tool with pattern "**/*settings.py"

**Editing steps for `settings.py`:**
- Add FRONTEND_URL, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS AND CSRF_TRUSTED_ORIGINS
- Update INSTALLED_APPS
- Update MIDDLEWARE


### Add FRONTEND_URL, ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS AND CSRF_TRUSTED_ORIGINS
Find the line `ALLOWED_HOSTS = []` in settings.py and replace that single line with:

```python
FRONTEND_URL = 'https://localhost:5173'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]

CSRF_TRUSTED_ORIGINS = [
    FRONTEND_URL,
]
```

### Update INSTALLED_APPS

Find the `INSTALLED_APPS` list and append the following to the end of the list:
```python

    # Cross-Origin Resource Sharing
    'corsheaders',

    # REST API support
    'rest_framework',
```

### Update MIDDLEWARE

Find the `MIDDLEWARE` list. After `'django.contrib.sessions.middleware.SessionMiddleware',`, add:
```python
'corsheaders.middleware.CorsMiddleware',
```

**Critical:**
- `CorsMiddleware` must come AFTER `SessionMiddleware` and BEFORE `CommonMiddleware`

**Expected result:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # ← Add here
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## Step 7: Create a health API

### Create backend/views.py (next to settings.py/urls.py):
```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

def api_health(request):
    return JsonResponse({
        "status": "ok",
        "message": "Django is alive and speaking HTTPS",
    })

@csrf_exempt
def csrf_token_view(request):
    # This forces Django to generate/set the csrftoken cookie
    token = get_token(request)
    return JsonResponse({"csrftoken": token})
```
---

## Step 8: Add import and URL routes to `urls.py`

first add `from .views import api_health, csrf_token_view` to imports and then add these endpoints to `urls.py`:
   ```python
    path('api/health/', api_health),
    path('api/csrf/', csrf_token_view),
   ```
---

## Step 9: Apply Initial Migrations

**Run database migrations:**
```bash
python manage.py migrate
```

**Creates:**
- `db.sqlite3` database file
- Default tables for auth, admin, sessions

---

## Step 10: Test HTTPS Server

**Start the HTTPS server:**

**macOS/Linux:**
```bash
./run.sh
```

**Windows:**
```bat
run.bat
```

**Expected output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on https://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Open browser and visit:**
```
https://localhost:8000
```

**Expected:**
- ✅ Django welcome page (rocket ship)
- ✅ **No certificate warnings** (padlock icon shows secure)
- ✅ URL shows `https://` not `http://`

**If you see certificate warnings:** mkcert CA not properly installed. Run `mkcert -install` again and restart browser.

**Stop server:** Press `Ctrl+C`

**Issues?** See [mkcert-https-setup troubleshooting](../mkcert-https-setup/SKILL.md#common-issues--solutions)

---

## Step 11: Create .gitignore

**Strategy: Check for existing .gitignore first, then create or enhance accordingly.**

### Check if .gitignore already exists

**First, check if .gitignore exists in the project root:**
```bash
ls -la <path-to-root>/.gitignore 
```

### Option A: No .gitignore exists

**If .gitignore does not exist, create it using the script at `scripts/create_gitignore.py`:**

```bash
# Create .gitignore in project root
python <path-to-this-skill>/django-setup/scripts/create_gitignore.py --output .
```

**Verify creation at project root:**
```bash
ls -la <path-to-root>/.gitignore    # Should exist at project root
cat <path-to-root>/.gitignore       # Review contents
```

### Option B: .gitignore already exists

**If .gitignore already exists, enhance it manually by reading both files and merging missing entries:**

1. **Read the existing .gitignore** to understand what's already covered
2. **Read the template** at `.claude/skills/django-setup/examples/.gitignore-template`
3. **Compare both files** to identify missing entries from the template
4. **Use the Edit tool** to append missing sections/entries to the existing .gitignore, preserving the existing content
5. **Avoid duplicates** - only add entries that don't already exist (case-insensitive comparison)

---
