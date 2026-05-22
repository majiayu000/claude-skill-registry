---
name: podman
description: Container engine alternative to Docker with Windows installation, initialization, and basic usage.
---

# Podman — Container Engine

**Windows Installation**

```powershell
winget install -e --id RedHat.Podman
winget install -e --id RedHat.Podman-Desktop
```

**Initialize Podman**

```powershell
podman machine init
podman machine set --rootful
podman machine start
```

**Uninstallation**

```powershell
podman machine stop
podman machine rm -f
winget uninstall -e --id RedHat.Podman
winget uninstall -e --id RedHat.Podman-Desktop
```

**Run Example**

```bash
podman run --rm -it -v E:\data:/mnt/data alpine sh
```