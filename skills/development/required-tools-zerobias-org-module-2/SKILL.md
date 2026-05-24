---
name: required-tools
description: Required tools and version requirements for module development
---

# Prerequisites and Tool Requirements

## 🚨 CRITICAL REQUIREMENTS

All tools and versions listed below are MANDATORY for module development. Module creation/updates will FAIL without proper tool versions.

## Required Tools

### Core Development Tools

#### Node.js
- **Required Version**: >= 16.0.0
- **Recommended**: 18.x LTS
- **Check**: `node --version`
- **Install**: https://nodejs.org/ or use nvm

#### npm
- **Required Version**: >= 8.0.0
- **Recommended**: 9.x
- **Check**: `npm --version`
- **Install**: Comes with Node.js

#### Git
- **Required Version**: >= 2.25.0
- **Check**: `git --version`
- **Configuration Required**:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```

### Module Generation Tools

#### Yeoman
- **Required Version**: >= 4.0.0
- **Check**: `yo --version`
- **Install**: `npm install -g yo`

#### Yeoman Generator for Modules
- **Package**: `@auditmation/generator-hub-module`
- **Check**: `npm ls -g @auditmation/generator-hub-module`
- **Install**: `npm install -g @auditmation/generator-hub-module`

### Code Generation Tools

#### Java
- **Required Version**: >= 11.0.0
- **Recommended**: 17 LTS
- **Check**: `java -version`
- **Install**: https://adoptium.net/
- **Purpose**: Required for OpenAPI code generator

#### OpenAPI Generator
- **Included**: Usually bundled with module setup
- **Alternative Install**: `npm install -g @openapitools/openapi-generator-cli`

### Build and Validation Tools

#### TypeScript
- **Required Version**: >= 4.5.0
- **Check**: `npx tsc --version`
- **Install**: Included in module dependencies

#### Lerna
- **Required Version**: >= 6.0.0
- **Check**: `npx lerna --version`
- **Install**: Part of monorepo setup

#### swagger-cli
- **Purpose**: API specification validation
- **Check**: `npx swagger-cli --version`
- **Install**: `npm install -g @apidevtools/swagger-cli`

### YAML/JSON Processing Tools

#### yq
- **Purpose**: YAML processing for product discovery
- **Check**: `yq --version`
- **Install**:
  - macOS: `brew install yq`
  - Linux: `snap install yq` or download from GitHub
  - Windows: Download from GitHub releases

#### jq
- **Purpose**: JSON processing
- **Check**: `jq --version`
- **Install**:
  - macOS: `brew install jq`
  - Linux: `apt-get install jq` or `yum install jq`
  - Windows: Download from GitHub releases

## Environment Setup

### Required Environment Variables
None required globally, but modules may need:
- Development credentials in `.env` files
- API tokens for testing

### Directory Structure
```
module/                          # Repository root
├── package/                     # All modules live here
│   ├── {vendor}/
│   │   ├── {service}/          # Individual module
│   │   └── {suite}/
│   │       └── {service}/      # Module with suite
├── .claude/                    # Agent workspace (active system)
├── types/                       # Optional type definitions
└── lerna.json                   # Monorepo configuration
```

### npm Configuration
Ensure access to required registries:
```bash
# Check current registry
npm config get registry

# May need to configure for private packages
npm config set @zerobias-org:registry https://npm.pkg.github.com/
npm config set @auditmation:registry https://npm.pkg.github.com/
npm config set @auditlogic:registry https://npm.pkg.github.com/
```

## Version Check Script

Create `check-prerequisites.sh`:
```bash
#!/bin/bash

echo "Checking prerequisites..."

# Node.js
NODE_VERSION=$(node --version 2>/dev/null | sed 's/v//')
if [ -z "$NODE_VERSION" ]; then
  echo "❌ Node.js not installed"
else
  MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
  if [ "$MAJOR" -ge 16 ]; then
    echo "✅ Node.js $NODE_VERSION"
  else
    echo "❌ Node.js $NODE_VERSION (need >= 16.0.0)"
  fi
fi

# npm
NPM_VERSION=$(npm --version 2>/dev/null)
if [ -z "$NPM_VERSION" ]; then
  echo "❌ npm not installed"
else
  MAJOR=$(echo $NPM_VERSION | cut -d. -f1)
  if [ "$MAJOR" -ge 8 ]; then
    echo "✅ npm $NPM_VERSION"
  else
    echo "❌ npm $NPM_VERSION (need >= 8.0.0)"
  fi
fi

# Yeoman
YO_VERSION=$(yo --version 2>/dev/null)
if [ -z "$YO_VERSION" ]; then
  echo "❌ Yeoman not installed"
else
  MAJOR=$(echo $YO_VERSION | cut -d. -f1)
  if [ "$MAJOR" -ge 4 ]; then
    echo "✅ Yeoman $YO_VERSION"
  else
    echo "❌ Yeoman $YO_VERSION (need >= 4.0.0)"
  fi
fi

# Java
JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
if [ -z "$JAVA_VERSION" ]; then
  echo "❌ Java not installed"
else
  if [ "$JAVA_VERSION" -ge 11 ]; then
    echo "✅ Java $JAVA_VERSION"
  else
    echo "❌ Java $JAVA_VERSION (need >= 11)"
  fi
fi

# Git
GIT_VERSION=$(git --version 2>/dev/null | sed 's/git version //')
if [ -z "$GIT_VERSION" ]; then
  echo "❌ Git not installed"
else
  echo "✅ Git $GIT_VERSION"
fi

# yq
YQ_VERSION=$(yq --version 2>/dev/null)
if [ -z "$YQ_VERSION" ]; then
  echo "⚠️  yq not installed (required for some operations)"
else
  echo "✅ yq installed"
fi

# jq
JQ_VERSION=$(jq --version 2>/dev/null)
if [ -z "$JQ_VERSION" ]; then
  echo "⚠️  jq not installed (optional but recommended)"
else
  echo "✅ jq installed"
fi

echo ""
echo "Generator check:"
npm ls -g @auditmation/generator-hub-module 2>/dev/null || echo "❌ Module generator not installed"
```

## Installation Commands Summary

### Quick Setup (macOS)
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install tools
brew install node@18
brew install yq jq
npm install -g yo @auditmation/generator-hub-module
```

### Quick Setup (Ubuntu/Debian)
```bash
# Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Other tools
sudo apt-get install -y git openjdk-17-jdk
sudo snap install yq
sudo apt-get install -y jq

# npm tools
npm install -g yo @auditmation/generator-hub-module
```

### Quick Setup (Windows)
1. Install Node.js from https://nodejs.org/
2. Install Git from https://git-scm.com/
3. Install Java from https://adoptium.net/
4. Download yq and jq from GitHub releases
5. Run in PowerShell:
   ```powershell
   npm install -g yo @auditmation/generator-hub-module
   ```

## Troubleshooting

### Issue: Permission denied when installing global npm packages
**Solution**:
```bash
# Configure npm to use a different directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### Issue: Yeoman generator not found
**Solution**:
```bash
# Clear npm cache
npm cache clean --force
# Reinstall
npm install -g @auditmation/generator-hub-module
```

### Issue: Java version too old
**Solution**:
- Uninstall old Java version
- Install Java 11+ from https://adoptium.net/
- Set JAVA_HOME environment variable

### Issue: npm registry access denied
**Solution**:
```bash
# Login to GitHub packages
npm login --scope=@zerobias-org --registry=https://npm.pkg.github.com
# Enter GitHub username and personal access token
```

## Validation Checklist

Before starting module development:

- [ ] Node.js >= 16.0.0 installed
- [ ] npm >= 8.0.0 installed
- [ ] Git configured with user name and email
- [ ] Yeoman >= 4.0.0 installed
- [ ] Module generator installed
- [ ] Java >= 11.0.0 installed
- [ ] Repository cloned locally
- [ ] In correct directory (module root)
- [ ] yq installed (for product discovery)
- [ ] npm registries configured (if using private packages)

## CI/CD Requirements

For automated builds, ensure CI environment has:
- Node.js 18.x
- Java 11+
- All npm global packages
- Access to private npm registries
- Git configured for commits

## Platform-Specific Notes

### macOS
- Use Homebrew for most tools
- May need Xcode Command Line Tools: `xcode-select --install`

### Linux
- Use distribution package manager
- May need to add NodeSource repository for recent Node.js
- Consider using snap for some tools

### Windows
- Use Windows installers for Node.js and Java
- Consider using WSL2 for better compatibility
- Git Bash recommended for command line

## Updates and Maintenance

Keep tools updated:
```bash
# Update npm
npm install -g npm@latest

# Update global packages
npm update -g

# Update Yeoman generator
npm install -g @auditmation/generator-hub-module@latest

# Check for outdated packages
npm outdated -g
```

## Support

If prerequisites check fails:
1. Review error messages
2. Install missing tools
3. Verify versions meet minimums
4. Check network access to registries
5. Ensure proper permissions
