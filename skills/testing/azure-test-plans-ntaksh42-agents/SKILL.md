---
name: azure-test-plans
description: Create and manage Azure Test Plans including test cases, suites, and execution. Use when setting up test plans or managing QA processes.
---

# Azure Test Plans Skill

Azure Test Plansでテスト管理を行うスキルです。

## 主な機能

- **テストケース作成**: 手動・自動テスト
- **テストスイート**: グループ化
- **テスト実行**: 結果記録
- **バグ報告**: テスト失敗からバグ作成

## テストケース作成

### REST API (Python)

```python
import requests
import json

organization = "myorg"
project = "MyProject"
pat = "your-pat"

url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Test Case?api-version=7.0"

headers = {
    "Content-Type": "application/json-patch+json",
    "Authorization": f"Basic {pat}"
}

test_case = [
    {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "ログイン機能のテスト"
    },
    {
        "op": "add",
        "path": "/fields/Microsoft.VSTS.TCM.Steps",
        "value": "<steps><step id='1'><parameterizedString>1. ログインページを開く</parameterizedString><expectedResult>ログインフォームが表示される</expectedResult></step><step id='2'><parameterizedString>2. メールアドレスとパスワードを入力</parameterizedString></step><step id='3'><parameterizedString>3. ログインボタンをクリック</parameterizedString><expectedResult>ダッシュボードにリダイレクトされる</expectedResult></step></steps>"
    },
    {
        "op": "add",
        "path": "/fields/Microsoft.VSTS.TCM.AutomatedTestName",
        "value": "LoginTests.TestSuccessfulLogin"
    }
]

response = requests.post(url, headers=headers, data=json.dumps(test_case))
print(response.json())
```

## テストスイート作成

```bash
# テストプラン作成
az boards test-plan create \
  --name "Sprint 1 Tests" \
  --area-path "MyProject" \
  --iteration "MyProject\\Sprint 1"

# テストスイート作成
az boards test-suite create \
  --plan-id 1 \
  --name "Login Tests" \
  --suite-type "StaticTestSuite"
```

## 自動テスト統合

```yaml
# Azure Pipeline with Test Results
steps:
  - task: VSTest@2
    inputs:
      testSelector: 'testAssemblies'
      testAssemblyVer2: |
        **\*test*.dll
        !**\*TestAdapter.dll
        !**\obj\**
      searchFolder: '$(System.DefaultWorkingDirectory)'
      codeCoverageEnabled: true
      testRunTitle: 'Automated Tests'
      publishRunAttachments: true
```

## バージョン情報
- Version: 1.0.0
