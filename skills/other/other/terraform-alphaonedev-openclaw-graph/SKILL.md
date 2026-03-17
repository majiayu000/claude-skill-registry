---
name: terraform
cluster: devops-sre
description: "Tool for defining, provisioning, and managing infrastructure as code using declarative HCL configuration files."
tags: ["terraform","iac","devops"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "infrastructure as code iac provisioning terraform hcl cloud devops"
---

# terraform

## Purpose
Terraform is a command-line tool for defining and provisioning infrastructure as code using declarative HCL (HashiCorp Configuration Language) files. It enables users to create, update, and destroy cloud resources in a repeatable, version-controlled manner.

## When to Use
Use Terraform for managing multi-cloud environments, automating infrastructure deployments, or when you need version-controlled IaC for resources like VMs, networks, or databases. Apply it in scenarios involving AWS, Azure, or GCP provisioning, especially for dynamic scaling, disaster recovery setups, or CI/CD pipelines to ensure consistency.

## Key Capabilities
- Declarative HCL syntax for defining resources, e.g., `resource "aws_instance" "example" { ami = "ami-123456" instance_type = "t2.micro" }`.
- Provider support for over 100 services; configure with blocks like `provider "aws" { region = "us-west-2" }`.
- State management via local files or remote backends (e.g., S3) to track resource changes.
- Module reuse for composing configurations; import with `module "vpc" { source = "./modules/vpc" }`.
- Variable interpolation and functions, such as `count` for loops or `templatefile` for dynamic configs.

## Usage Patterns
To use Terraform, start by writing an HCL file (e.g., main.tf) defining resources and providers. Initialize the workspace with `terraform init`, review changes via `terraform plan`, and apply them with `terraform apply`. For automation, wrap commands in scripts and use environment variables for secrets. Always version control your .tf files in Git. For multi-environment setups, use workspaces: `terraform workspace new dev` then switch with `terraform workspace select dev`.

## Common Commands/API
Run Terraform via CLI; key commands include:
- `terraform init`: Download providers and modules; use `-upgrade` to update dependencies.
- `terraform plan -out=plan.tfplan -var="instance_type=t2.medium"`: Generate an execution plan; specify variables via flags or files.
- `terraform apply plan.tfplan`: Apply the plan; add `-auto-approve` for non-interactive runs.
- `terraform destroy -target=aws_instance.example`: Destroy specific resources; use `-force` cautiously.
For API integration, use Terraform's remote backend or the Terraform Cloud API (e.g., POST to `https://app.terraform.io/api/v2/runs` for runs), but require authentication via `$TERRAFORM_TOKEN`. Set provider credentials as env vars, e.g., `export AWS_ACCESS_KEY_ID=$AWS_API_KEY` and `export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_KEY`.

## Integration Notes
Integrate Terraform with CI/CD tools like GitHub Actions or Jenkins by adding steps in your workflow YAML, e.g.:
```
- name: Terraform Init
  run: terraform init
- name: Terraform Apply
  run: terraform apply -auto-approve
```
Use remote state backends for collaboration, e.g., configure in main.tf with `terraform { backend "s3" { bucket = "my-terraform-state" key = "path/to/state" region = "us-west-2" } }`. For secrets, inject via env vars (e.g., `$AWS_ACCESS_KEY_ID`) or tools like Vault. Ensure provider versions are pinned in .tf files, like `terraform { required_providers { aws = { source = "hashicorp/aws" version = "~> 4.0" } } }`, to avoid breaking changes.

## Error Handling
Handle errors by running `terraform validate` first to check HCL syntax; fix issues like missing brackets or invalid attributes. For provider errors, verify credentials (e.g., check `$AWS_ACCESS_KEY_ID` is set) and use `terraform plan -detailed-exitcode` to get specific codes (e.g., 2 for errors). Common patterns: wrap commands in try-catch blocks in scripts, e.g.:
```
try {
  terraform apply
} catch {
  echo "Error: Apply failed; check logs for details"
}
```
Debug with `TF_LOG=DEBUG terraform apply` to log provider interactions, and use `terraform state pull` to inspect state files for inconsistencies.

## Usage Examples
1. Create an AWS EC2 instance: Define in main.tf as `resource "aws_instance" "web" { ami = "ami-0c55b159cbfafe1f0" instance_type = "t2.micro" tags = { Name = "web-server" } }`. Then run `terraform init`, followed by `terraform apply -auto-approve` to provision it.
2. Manage a simple VPC: In main.tf, add `resource "aws_vpc" "main" { cidr_block = "10.0.0.0/16" }` and `resource "aws_subnet" "subnet1" { vpc_id = aws_vpc.main.id cidr_block = "10.0.1.0/24" }`. Execute `terraform plan` to review, then `terraform apply` for deployment.

## Graph Relationships
- Connected to cluster: devops-sre
- Related tags: terraform, iac, devops
- Links to other skills: via devops-sre (e.g., ansible for configuration management), and iac-related tools like pulumi or cloudformation for alternative provisioning methods.
