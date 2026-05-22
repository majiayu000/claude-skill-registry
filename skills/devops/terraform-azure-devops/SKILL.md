---
name: terraform-azure-devops
description: Generate Terraform configurations for Azure DevOps resources. Use when managing Azure DevOps infrastructure as code.
---

# Terraform Azure DevOps Skill

TerraformでAzure DevOpsリソースを管理するスキルです。

## 主な機能

- **プロジェクト管理**: Terraform でプロジェクト作成
- **リポジトリ**: Gitリポジトリ管理
- **パイプライン**: IaC化
- **変数グループ**: コード管理

## プロバイダー設定

```hcl
terraform {
  required_providers {
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = "~> 0.10.0"
    }
  }
}

provider "azuredevops" {
  org_service_url       = "https://dev.azure.com/myorg"
  personal_access_token = var.pat
}
```

## プロジェクト作成

```hcl
resource "azuredevops_project" "project" {
  name               = "My Terraform Project"
  description        = "Project managed by Terraform"
  visibility         = "private"
  version_control    = "Git"
  work_item_template = "Agile"

  features = {
    "boards"       = "enabled"
    "repositories" = "enabled"
    "pipelines"    = "enabled"
    "testplans"    = "disabled"
    "artifacts"    = "enabled"
  }
}
```

## リポジトリ作成

```hcl
resource "azuredevops_git_repository" "repo" {
  project_id = azuredevops_project.project.id
  name       = "my-app"
  
  initialization {
    init_type = "Clean"
  }
}
```

## ビルドパイプライン

```hcl
resource "azuredevops_build_definition" "build" {
  project_id = azuredevops_project.project.id
  name       = "CI Pipeline"

  ci_trigger {
    use_yaml = true
  }

  repository {
    repo_type   = "TfsGit"
    repo_id     = azuredevops_git_repository.repo.id
    branch_name = azuredevops_git_repository.repo.default_branch
    yml_path    = "azure-pipelines.yml"
  }
}
```

## 変数グループ

```hcl
resource "azuredevops_variable_group" "vars" {
  project_id   = azuredevops_project.project.id
  name         = "Production Variables"
  description  = "Variables for production"
  allow_access = true

  variable {
    name  = "DATABASE_HOST"
    value = "prod-db.database.windows.net"
  }

  variable {
    name      = "DATABASE_PASSWORD"
    secret_value = var.db_password
    is_secret = true
  }
}
```

## バージョン情報
- Version: 1.0.0
