---
name: terraform
description: Infrastructure as Code tool with installation, initialization, and provisioning workflow commands.
---

# Terraform — Provisioning

**Install Script**

```bash
echo "⚙️ Installing Terraform..."
if command -v terraform &> /dev/null
then
    echo "✅ Terraform is already installed."
    terraform version
else
    wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update && sudo apt install -y terraform
    if [ $? -eq 0 ]; then
        echo "✅ Terraform installed successfully."
        terraform version
    else
        echo "❌ Error installing Terraform. Please check the output above."
        exit 1
    fi
fi

```

**Workflow**

```bash
terraform init
terraform plan
terraform apply -auto-approve -var key=value
terraform destroy
terraform fmt
terraform validate
terraform version

terraform state rm $RESOURCE
```