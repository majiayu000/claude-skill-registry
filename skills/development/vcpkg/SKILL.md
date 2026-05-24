---
name: vcpkg
description: C++ package manager for Windows with installation, environment setup, and package installation commands.
---

# Vcpkg — C++ Package Manager

**Bootstrap**

```powershell
git clone https://github.com/microsoft/vcpkg
cd vcpkg; .\bootstrap-vcpkg.bat
```

**Env Setup**

```powershell
$env:VCPKG_ROOT = "D:\git\vcpkg"
$env:PATH = "$env:VCPKG_ROOT;$env:PATH"
```

**Install Package**

```powershell
vcpkg install libxml2:x64-windows
vcpkg integrate install
```

🔗 [Official Guide](https://learn.microsoft.com/en-us/vcpkg/get_started/get-started?pivots=shell-powershell)