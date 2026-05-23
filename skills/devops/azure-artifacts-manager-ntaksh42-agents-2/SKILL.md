---
name: azure-artifacts-manager
description: Manage Azure Artifacts including package feeds, versions, and dependencies. Use when publishing or managing artifact packages.
---

# Azure Artifacts Manager Skill

Azure Artifactsでパッケージを管理するスキルです。

## 主な機能

- **Feedの作成**: npm、NuGet、Maven、Python
- **パッケージ公開**: ビルド成果物の公開
- **パッケージ管理**: バージョン管理
- **アクセス制御**: 権限設定

## Feed作成

```bash
# npm Feed作成
az artifacts feed create \
  --name "my-npm-feed" \
  --feed-type npm

# NuGet Feed
az artifacts feed create \
  --name "my-nuget-feed" \
  --feed-type nuget

# Universal Packages
az artifacts feed create \
  --name "my-universal-feed" \
  --feed-type universal
```

## パッケージ公開

### npm

```yaml
steps:
  - task: Npm@1
    inputs:
      command: 'publish'
      publishRegistry: 'useFeed'
      publishFeed: 'my-npm-feed'
```

### NuGet

```yaml
steps:
  - task: NuGetCommand@2
    inputs:
      command: 'push'
      packagesToPush: '$(Build.ArtifactStagingDirectory)/**/*.nupkg'
      nuGetFeedType: 'internal'
      publishVstsFeed: 'my-nuget-feed'
```

### Universal Packages

```bash
az artifacts universal publish \
  --organization https://dev.azure.com/myorg \
  --feed my-universal-feed \
  --name my-package \
  --version 1.0.0 \
  --path ./dist
```

## .npmrc設定

```ini
registry=https://pkgs.dev.azure.com/myorg/_packaging/my-npm-feed/npm/registry/
always-auth=true
```

## バージョン情報
- Version: 1.0.0
