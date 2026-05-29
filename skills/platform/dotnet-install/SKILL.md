---
name: dotnet-install
version: 1.0.0
description: .NET SDK and runtime installation across Windows, macOS, and Linux. Handles version detection, platform-specific installers (WinGet, Homebrew, apt, dnf), SDK vs runtime selection, offline installation, Docker setup, and troubleshooting. Auto-activates for .NET installation, setup, version management, and multi-platform deployment.
activation_keywords:
  - "install .NET"
  - "setup dotnet"
  - "install SDK"
  - ".NET runtime"
  - "dotnet version"
  - "global.json"
token_budget: 5000
references:
  - https://learn.microsoft.com/en-us/dotnet/core/install/
  - https://dotnet.microsoft.com/download
---

# .NET Installation Skill

Automated .NET SDK and runtime installation with intelligent platform detection, version management, and troubleshooting guidance.

## Quick Start

### Check Current Installation

```bash
dotnet --version
# Output: 8.0.100

dotnet --list-sdks
# Output: 8.0.100 [/usr/local/share/dotnet/sdk]

dotnet --list-runtimes
# Output: Microsoft.NETCore.App 8.0.0 [/usr/local/share/dotnet/shared/Microsoft.NETCore.App]
```

### Platform Detection

The skill automatically detects your operating system and recommends the best installation method:

```bash
# Detected: macOS 14.2 (arm64)
# Recommended: Official installer package (.pkg)
# Alternative: Homebrew (brew install dotnet)
```

### Quick Install (Recommended Methods)

**Windows (WinGet)**:

```powershell
# Install .NET 8 SDK (LTS)
winget install Microsoft.DotNet.SDK.8

# Verify installation
dotnet --version
# Output: 8.0.100
```

**macOS (Official Installer)**:

```bash
# Download and install from:
# https://dotnet.microsoft.com/download/dotnet/8.0

# Or use Homebrew:
brew install dotnet

# Verify installation
dotnet --version
# Output: 8.0.100
```

**Linux (Ubuntu/Debian)**:

```bash
# Add Microsoft package repository
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

# Install .NET 8 SDK
sudo apt-get update
sudo apt-get install -y dotnet-sdk-8.0

# Verify installation
dotnet --version
# Output: 8.0.100
```

### SDK vs Runtime Decision

**Install SDK when:**

- Building applications
- Developing locally
- Running `dotnet build` or `dotnet run`
- Need the complete toolchain

**Install Runtime only when:**

- Deploying production apps
- Running pre-compiled applications
- Minimizing installation size
- Production servers

```bash
# Install SDK (includes runtime)
sudo apt-get install dotnet-sdk-8.0

# Install runtime only (smaller)
sudo apt-get install aspnetcore-runtime-8.0  # For ASP.NET Core apps
sudo apt-get install dotnet-runtime-8.0      # For console apps
```

## Practical Guide

### Windows Installation Methods

#### Method 1: WinGet (Recommended)

```powershell
# List available .NET versions
winget search Microsoft.DotNet.SDK

# Install .NET 8 SDK (LTS)
winget install Microsoft.DotNet.SDK.8

# Install specific version
winget install Microsoft.DotNet.SDK.8 --version 8.0.100

# Update existing installation
winget upgrade Microsoft.DotNet.SDK.8
```

#### Method 2: Visual Studio Installer

```powershell
# Visual Studio 2022 detected at: C:\Program Files\Visual Studio\2022\Community
# .NET 8 SDK available via: Modify Installation → .NET desktop development
```

Installation steps:

1. Launch Visual Studio Installer
2. Click "Modify" on your installation
3. Select ".NET desktop development" workload
4. Apply changes

#### Method 3: Standalone Installer

```powershell
# Download: https://dotnet.microsoft.com/download/dotnet/8.0
# File: dotnet-sdk-8.0.100-win-x64.exe
# SHA512: [verification hash]

# Run installer (GUI)
.\dotnet-sdk-8.0.100-win-x64.exe

# Or silent install
.\dotnet-sdk-8.0.100-win-x64.exe /install /quiet /norestart
```

#### Method 4: PowerShell Script

```powershell
# Download install script
Invoke-WebRequest -Uri https://dot.net/v1/dotnet-install.ps1 -OutFile dotnet-install.ps1

# Install latest .NET 8 SDK
.\dotnet-install.ps1 -Channel 8.0

# Install to custom location
.\dotnet-install.ps1 -Channel 8.0 -InstallDir "C:\Program Files\dotnet"

# Install runtime only
.\dotnet-install.ps1 -Channel 8.0 -Runtime dotnet
```

### macOS Installation Methods

#### Method 1: Official Installer Package (Recommended)

```bash
# Detected: Apple Silicon (arm64)
# Recommended: dotnet-sdk-8.0.100-osx-arm64.pkg

# Download from: https://dotnet.microsoft.com/download/dotnet/8.0
# Double-click .pkg file to install

# Verify installation location
which dotnet
# Output: /usr/local/share/dotnet/dotnet
```

#### Method 2: Homebrew

```bash
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install .NET SDK
brew install dotnet

# Install specific version (if available)
brew install dotnet@8

# Update existing installation
brew upgrade dotnet
```

#### Method 3: Install Script

```bash
# Download install script
curl -sSL https://dot.net/v1/dotnet-install.sh -o dotnet-install.sh
chmod +x dotnet-install.sh

# Install latest .NET 8 SDK
./dotnet-install.sh --channel 8.0

# Install to custom location
./dotnet-install.sh --channel 8.0 --install-dir ~/.dotnet

# Add to PATH
echo 'export PATH="$HOME/.dotnet:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Linux Installation Methods

#### Ubuntu/Debian

```bash
# Ubuntu 22.04 LTS
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

# Ubuntu 20.04 LTS
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

# Install SDK
sudo apt-get update
sudo apt-get install -y dotnet-sdk-8.0

# Install runtime only
sudo apt-get install -y aspnetcore-runtime-8.0
```

#### Fedora/RHEL/CentOS

```bash
# Fedora 39
sudo dnf install dotnet-sdk-8.0

# RHEL/CentOS (register Microsoft repository first)
sudo dnf install https://packages.microsoft.com/config/rhel/9/packages-microsoft-prod.rpm
sudo dnf install dotnet-sdk-8.0
```

#### Arch Linux

```bash
# Install from official repositories
sudo pacman -S dotnet-sdk

# Install runtime only
sudo pacman -S aspnet-runtime
```

#### Alpine Linux

```bash
# Add Microsoft repository
wget https://dot.net/v1/dotnet-install.sh
chmod +x dotnet-install.sh

# Install .NET 8
./dotnet-install.sh --channel 8.0 --install-dir /usr/share/dotnet

# Add to PATH
export PATH="$PATH:/usr/share/dotnet"
```

### Version Management with global.json

Control which .NET SDK version your project uses:

```bash
# Create global.json for .NET 8
dotnet new globaljson --sdk-version 8.0.100

# View current global.json
cat global.json
```

```json
{
  "sdk": {
    "version": "8.0.100",
    "rollForward": "latestPatch"
  }
}
```

**Roll-forward policies**:

- `latestPatch` - Use latest patch (8.0.x)
- `latestFeature` - Use latest feature band (8.x.x)
- `latestMinor` - Use latest minor (x.x.x)
- `disable` - Exact version required

## Deep Dive

### SDK vs Runtime Architecture

**SDK Components**:

```
.NET SDK 8.0.100
├── Runtime (8.0.0)
├── Compiler (Roslyn)
├── CLI Tools (dotnet build, run, publish)
├── Templates (dotnet new)
└── MSBuild
```

**Runtime-Only Components**:

```
.NET Runtime 8.0.0
├── CoreCLR (execution engine)
├── Base Class Libraries
└── Framework assemblies
```

**Size comparison**:

- SDK: ~200-400 MB
- Runtime: ~50-150 MB

### Installing Multiple Versions Side-by-Side

.NET supports multiple versions installed simultaneously:

```bash
# List all installed SDKs
dotnet --list-sdks
# Output:
# 6.0.420 [/usr/local/share/dotnet/sdk]
# 7.0.410 [/usr/local/share/dotnet/sdk]
# 8.0.100 [/usr/local/share/dotnet/sdk]

# Install additional versions
sudo apt-get install dotnet-sdk-7.0  # Adds to existing installation

# Project selects version via global.json
cd my-project
cat global.json
# { "sdk": { "version": "7.0.410" } }

dotnet --version
# Output: 7.0.410 (selected by global.json)
```

### Offline Installation

For air-gapped environments or restricted networks:

#### Windows

```powershell
# Download offline installer
# https://dotnet.microsoft.com/download/dotnet/8.0
# Select: x64 | Binaries

# Extract to destination
Expand-Archive dotnet-sdk-8.0.100-win-x64.zip -DestinationPath "C:\Program Files\dotnet"

# Add to PATH
$env:PATH = "C:\Program Files\dotnet;$env:PATH"
[Environment]::SetEnvironmentVariable("PATH", $env:PATH, "Machine")
```

#### Linux

```bash
# Download tarball
wget https://download.visualstudio.microsoft.com/download/pr/[hash]/dotnet-sdk-8.0.100-linux-x64.tar.gz

# Extract to system location
sudo mkdir -p /usr/local/share/dotnet
sudo tar -xzf dotnet-sdk-8.0.100-linux-x64.tar.gz -C /usr/local/share/dotnet

# Create symlink
sudo ln -s /usr/local/share/dotnet/dotnet /usr/local/bin/dotnet
```

### Docker Installation

```dockerfile
# Use official .NET SDK image
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Copy and restore project
COPY *.csproj ./
RUN dotnet restore

# Build application
COPY . ./
RUN dotnet publish -c Release -o out

# Runtime image (smaller)
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/out .
ENTRYPOINT ["dotnet", "MyApp.dll"]
```

### Common Troubleshooting

#### PATH Not Updated

```bash
# Verify dotnet location
which dotnet  # macOS/Linux
where.exe dotnet  # Windows

# If not found, add to PATH manually:

# macOS/Linux (bash)
echo 'export PATH="$PATH:/usr/local/share/dotnet"' >> ~/.bashrc
source ~/.bashrc

# macOS (zsh)
echo 'export PATH="$PATH:/usr/local/share/dotnet"' >> ~/.zshrc
source ~/.zshrc

# Windows (PowerShell)
$env:PATH = "$env:PATH;C:\Program Files\dotnet"
```

#### SDK Not Found After Installation

```bash
# Check installation location
dotnet --info
# Look for "Base Path:" in output

# Register installation manually (Linux)
sudo ln -s /usr/local/share/dotnet/dotnet /usr/bin/dotnet

# Clear NuGet cache if corrupted
dotnet nuget locals all --clear
```

#### Version Conflicts

```bash
# Remove specific SDK version
sudo apt-get remove dotnet-sdk-7.0  # Linux
winget uninstall Microsoft.DotNet.SDK.7  # Windows

# Force project to use available SDK
# Edit global.json:
{
  "sdk": {
    "version": "8.0.100",
    "rollForward": "latestMinor"  # More permissive
  }
}
```

## References

**Comprehensive Details**: See [reference.md](./reference.md) for:

- Complete platform-specific installation commands
- Advanced version management strategies
- Enterprise deployment patterns
- CI/CD integration examples
- Performance optimization tips

**Official Documentation**:

- [.NET Installation Guide](https://learn.microsoft.com/en-us/dotnet/core/install/)
- [Download .NET](https://dotnet.microsoft.com/download)
- [SDK vs Runtime](https://learn.microsoft.com/en-us/dotnet/core/introduction#sdk-and-runtimes)
- [global.json Reference](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json)
