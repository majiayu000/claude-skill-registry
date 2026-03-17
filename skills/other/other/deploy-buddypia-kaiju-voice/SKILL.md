---
name: deploy
description: |
  Cloud Run へのデプロイを実行するスキル。
  品質ゲート検証 → gcloud run deploy --source . → デプロイ検証 → リビジョン記録 の4フェーズで安全にデプロイする。

  **核心機能**:
  - 品質ゲート通過後のみデプロイ実行（--skip-checks で省略可）
  - Secret Manager 連携による安全な環境変数管理
  - デプロイ後のヘルスチェック自動実行
  - リビジョン履歴を docs/deployments/DEPLOY-LOG.md に自動記録

  "デプロイ", "deploy", "本番反映", "Cloud Runにデプロイ" 等の要求でトリガーされる。

  <example>
  user: "デプロイして"
  assistant: "deploy スキルを使用して Cloud Run へデプロイします"
  </example>

  <example>
  user: "品質チェック省略してデプロイ"
  assistant: "deploy スキルを --skip-checks オプション付きで実行します"
  </example>
---

# Deploy (Cloud Run デプロイ)

> **核心コンセプト**: "品質保証付きワンコマンドデプロイ"

`gcloud run deploy --source .` を活用した軽量デプロイスキル。
Terraform不要、gcloud CLI のみで Cloud Run にデプロイする。

## 核心原則

1. **品質ファースト**: デプロイ前に品質ゲート（Critical checks）を通過必須
2. **シークレット安全管理**: API キーは Secret Manager から取得、平文コマンド禁止
3. **検証可能**: デプロイ後にヘルスチェックで動作確認
4. **追跡可能**: 全デプロイのリビジョン・Git Commit・ステータスを自動記録

---

## デプロイ設定

以下のデフォルト値を使用する。オーバーライドする場合はオプションで指定。

| 設定                | デフォルト値          | 環境変数 / オプション               |
| ------------------- | --------------------- | ----------------------------------- |
| **GCPプロジェクト** | `gemini-3-tokyo-hackathon` | `--project <id>`                    |
| **リージョン**      | `asia-northeast1`     | `--region <region>`                 |
| **サービス名**      | `hackathon-project`       | `--service <name>`                  |
| **認証**            | 未認証アクセス許可    | `--no-allow-unauthenticated` で変更 |

### 環境変数（Cloud Run に設定）

| 変数             | 取得元                                        |
| ---------------- | --------------------------------------------- |
| `GEMINI_API_KEY` | Secret Manager (`gemini-api-key`) or 直接指定 |

---

## 実行プロトコル

### Phase 1: Pre-flight (品質ゲート)

```
1. git status 確認 — uncommitted changes の警告
2. make q.critical 実行 — Critical checks 全通過必須
   - format.check, analyze, architecture, ui-flow, codegen.check, test, build
3. Standalone バンドル検証:
   a. next.config.ts に serverExternalPackages: ['sucrase'] が設定されているか確認
   b. npm run build を実行し .next/standalone/ を生成
   c. .next/standalone/node_modules/sucrase が存在するか確認
   d. sucrase の transform() が standalone 環境で動作するか確認
   失敗時 → デプロイ中止（sucrase 未バンドルだと sandbox/serve でトランスパイル不可）
4. 失敗時 → デプロイ中止、修正を促す
```

`--skip-checks` 指定時: Phase 1 をスキップ（緊急時のみ）

### Phase 2: デプロイ実行

```
1. gcloud run deploy 実行:
   gcloud run deploy <service> \
     --source . \
     --region <region> \
     --allow-unauthenticated \
     --project <project>

2. 環境変数の設定:
   - Secret Manager が利用可能な場合:
     --set-secrets "GEMINI_API_KEY=gemini-api-key:latest"
   - Secret Manager 未設定の場合:
     --set-env-vars "GEMINI_API_KEY=$(gcloud secrets versions access latest --secret=gemini-api-key --project=<project>)"
   - フォールバック (Secret Manager なし):
     ユーザーに GEMINI_API_KEY の指定を求める
```

### Phase 3: Post-flight (デプロイ検証)

```
1. gcloud run revisions list で最新リビジョン名を取得
2. gcloud run services describe でサービス URL を取得
3. curl でヘルスチェック (HTTP 200 確認)
```

### Phase 4: リビジョン記録

```
1. デプロイ成功時のみ記録 (失敗時はスキップ)
2. docs/deployments/DEPLOY-LOG.md にエントリ追記:
   - 連番, 日時, リビジョン名, Git Commit (hash + message), ステータス, 品質ゲート, URL
3. 最新のデプロイが最上部に表示される (降順)
```

**記録フォーマット**:

```markdown
| #   | 日時             | リビジョン                | Git Commit               | ステータス | 品質ゲート | URL         |
| --- | ---------------- | ------------------------- | ------------------------ | :--------: | :--------: | ----------- |
| 3   | 2026-02-15 15:00 | `hackathon-project-00003-xyz` | `abc1234 feat: add quiz` |     OK     |   PASSED   | https://... |
| 2   | 2026-02-15 14:00 | `hackathon-project-00002-def` | `def5678 fix: streaming` |     OK     |  SKIPPED   | https://... |
```

---

## 制約事項

1. **平文キー禁止**: `--set-env-vars GEMINI_API_KEY=AIza...` のような平文指定は禁止。Secret Manager を使用する
2. **未コミット変更警告**: uncommitted changes がある場合は警告を表示（デプロイは続行可能）
3. **gcloud CLI 必須**: `gcloud` コマンドがインストール・認証済みであること
4. **プロジェクト権限**: Cloud Run Admin, Cloud Build Editor, Storage Admin 権限が必要
5. **Standalone バンドル必須**: `next.config.ts` の `serverExternalPackages: ['sucrase']` は削除禁止。sucrase は API route (`/api/sandbox/serve`) でサーバーサイドのJSX/TypeScriptトランスパイルに使用しており、webpack バンドルでは正常動作しない場合がある。NFT (Node File Tracing) が `.next/standalone/node_modules/` に自動コピーする

---

## 出力例

```markdown
# Deploy 実行結果

> **実行時間**: 2026-02-15 14:30:00 JST

## Pre-flight

| チェック        | 結果 |
| --------------- | :--: |
| Git Status      |  OK  |
| Format          |  OK  |
| Lint + Security |  OK  |
| Architecture    |  OK  |
| Tests           |  OK  |
| Build           |  OK  |

## デプロイ

| 項目           | 値                                       |
| -------------- | ---------------------------------------- |
| サービス       | hackathon-project                            |
| リージョン     | asia-northeast1                          |
| プロジェクト   | gemini-3-tokyo-hackathon                      |
| URL            | https://hackathon-project-xxxxx-an.a.run.app |
| ヘルスチェック | HTTP 200 OK                              |

## ステータス: DEPLOYED
```

---

## 使用例

```bash
# 基本デプロイ（品質ゲート付き）
/deploy

# 品質チェック省略（緊急時）
/deploy --skip-checks

# プロジェクト指定
/deploy --project my-other-project

# リージョン指定
/deploy --region us-central1
```

---

## Makefile 連携

```bash
# CLI から直接デプロイ
make deploy

# dry-run（デプロイせずにビルドのみ確認）
make deploy.dry-run
```

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                        |
| ---------- | ---------- | --------------------------------------------------------------- |
| 2026-02-15 | v1.2       | Standalone バンドル検証追加 (sucrase NFT チェック, 制約事項 #5) |
| 2026-02-15 | v1.1       | リビジョン記録機能追加 (Phase 4, DEPLOY-LOG.md)                 |
| 2026-02-15 | v1.0       | 新規作成 - gcloud CLI ベースの Cloud Run デプロイ               |
