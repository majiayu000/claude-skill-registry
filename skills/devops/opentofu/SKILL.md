---
name: opentofu
description: Open-source Terraform alternative for infrastructure provisioning with installation and workflow commands.
---

# OpenTofu — Terraform Alternative

**Installer**

```bash
echo "⚙️ Installing OpenTofu..."
if command -v tofu &> /dev/null
then
    echo "✅ OpenTofu is already installed."
    tofu version
else
    curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o install-opentofu.sh
    chmod +x install-opentofu.sh

    echo "ℹ️ Please inspect the downloaded OpenTofu installer script (install-opentofu.sh) if you wish."
    read -p "Proceed with OpenTofu installation? (y/N): " confirm_tofu
    if [[ "$confirm_tofu" =~ ^[Yy]$ ]]; then
        sudo ./install-opentofu.sh --install-method deb
        rm -f install-opentofu.sh
        if [ $? -eq 0 ]; then
            echo "✅ OpenTofu installed successfully."
            tofu version
        else
            echo "❌ Error installing OpenTofu. Please check the output above."
        fi
    else
        echo "⏩ Skipping OpenTofu installation."
        rm -f install-opentofu.sh
    fi
fi
```

**Workflow**

```bash
tofu init
tofu plan
tofu apply -auto-approve -var key=value
tofu destroy
tofu fmt
tofu validate
tofu version
```