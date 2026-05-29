---
name: jravan-ec2
description: JRA-VAN API（EC2）へのファイル送信とコード更新ガイド
version: 1.0.0
tools:
  - Bash
  - Read
skill_type: knowledge
auto_invoke: false
---

# JRA-VAN EC2コード更新ガイド

## 概要

JRA-VAN API（EC2 Windows Server）にコードを送信し、更新する際の定型コマンドを提供します。EC2にはGitがインストールされていないため、AWS SSM経由で直接ファイルを送信します。

## 背景

- **環境**: EC2 Windows Server
- **制約**: Gitがインストールされていない
- **転送方法**: AWS SSM + Base64エンコード
- **対象ファイル**: `jravan-api/*.py`

## 実行プロセス

### ステップ1: EC2インスタンスID確認

**コマンド**:
```bash
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*jravan*" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text)

echo "Instance ID: $INSTANCE_ID"
```

**出力例**:
```
Instance ID: i-0123456789abcdef0
```

### ステップ2: ファイルをBase64エンコードして送信

**コマンドテンプレート**:
```bash
# 1. ファイルをBase64エンコード
FILE_B64=$(base64 jravan-api/<ファイル名>.py | tr -d '\n')

# 2. SSM経由でEC2に送信
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\<ファイル名>.py -Encoding UTF8 -Force\"]"
```

**実行例（sync_jvlink.py を送信）**:
```bash
FILE_B64=$(base64 jravan-api/sync_jvlink.py | tr -d '\n')
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\sync_jvlink.py -Encoding UTF8 -Force\"]"
```

### ステップ3: データ再同期

#### 差分同期（デフォルト）

**コマンド**:
```bash
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py"]'
```

#### 指定日からの完全同期

**コマンド**:
```bash
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py --from 20260101"]'
```

**引数**:
- `--from YYYYMMDD`: 指定日付からデータを同期

### ステップ4: ログ確認

**コマンド**:
```bash
# CloudWatch Logsでログを確認
aws logs tail /aws/ec2/jravan --follow
```

## ワンライナーコマンド集

### ファイル送信ワンライナー

```bash
# sync_jvlink.py を送信
INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=*jravan*" --query 'Reservations[].Instances[].InstanceId' --output text) && \
FILE_B64=$(base64 jravan-api/sync_jvlink.py | tr -d '\n') && \
aws ssm send-command --instance-ids "$INSTANCE_ID" --document-name "AWS-RunPowerShellScript" --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\sync_jvlink.py -Encoding UTF8 -Force\"]"
```

### 複数ファイル一括送信

```bash
# 複数ファイルをループで送信
for file in sync_jvlink.py race_api.py; do
  FILE_B64=$(base64 jravan-api/$file | tr -d '\n')
  aws ssm send-command \
    --instance-ids "$INSTANCE_ID" \
    --document-name "AWS-RunPowerShellScript" \
    --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\$file -Encoding UTF8 -Force\"]"
  echo "Sent: $file"
  sleep 2
done
```

### 送信 → 同期 → ログ確認（一連の流れ）

```bash
# 1. ファイル送信
INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=*jravan*" --query 'Reservations[].Instances[].InstanceId' --output text)
FILE_B64=$(base64 jravan-api/sync_jvlink.py | tr -d '\n')
aws ssm send-command --instance-ids "$INSTANCE_ID" --document-name "AWS-RunPowerShellScript" --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\sync_jvlink.py -Encoding UTF8 -Force\"]"

# 2. 5秒待機
sleep 5

# 3. データ再同期
aws ssm send-command --instance-ids "$INSTANCE_ID" --document-name "AWS-RunPowerShellScript" --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py"]'

# 4. ログ確認
aws logs tail /aws/ec2/jravan --follow
```

## エラーハンドリング

### よくあるエラー

1. **インスタンスIDが見つからない**
   ```
   Error: An error occurred (InvalidInstanceID.NotFound)
   ```
   - 対処: EC2インスタンスが起動しているか確認
   - コマンド: `aws ec2 describe-instances --filters "Name=tag:Name,Values=*jravan*"`

2. **SSMエージェント未起動**
   ```
   Error: TargetNotConnected
   ```
   - 対処: EC2でSSMエージェントが起動しているか確認
   - 確認方法: AWSコンソール > Systems Manager > Fleet Manager

3. **PowerShell構文エラー**
   ```
   Error: At line:1 char:...
   ```
   - 対処: PowerShellコマンドのエスケープを確認
   - Base64エンコードの改行削除 `tr -d '\n'` を確認

4. **ファイルが見つからない**
   ```
   base64: jravan-api/sync_jvlink.py: No such file or directory
   ```
   - 対処: カレントディレクトリを確認、`ls jravan-api/` で存在確認

## セキュリティ上の注意

- **認証情報**: スクリプトに認証情報をハードコードしない
- **環境変数**: 機密情報は環境変数で管理
- **IAM権限**: 最小権限の原則（EC2, SSM のみ）

## 対象ファイル

### 主要ファイル
- `sync_jvlink.py` - JV-Linkデータ同期スクリプト
- `race_api.py` - レースAPIサーバー（FastAPI）
- `config.py` - 設定ファイル

## 使用例

### 例1: sync_jvlink.py を更新して差分同期

```
/jravan-ec2

ファイル: sync_jvlink.py
同期モード: 差分

実行コマンド:

# 1. インスタンスID取得
INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=*jravan*" --query 'Reservations[].Instances[].InstanceId' --output text)

# 2. ファイル送信
FILE_B64=$(base64 jravan-api/sync_jvlink.py | tr -d '\n')
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\sync_jvlink.py -Encoding UTF8 -Force\"]"

# 3. 差分同期実行
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py"]'

完了。ログを確認してください。
```

### 例2: 特定日からの完全同期

```
/jravan-ec2

同期モード: 2026年1月1日から完全同期

実行コマンド:

aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py --from 20260101"]'
```

## 関連ドキュメント

- **AWS SSM**: https://docs.aws.amazon.com/systems-manager/
- **CLAUDE.md**: `main/CLAUDE.md` の「EC2 コード更新」セクション
- **JV-Link仕様**: `main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/jra-van_setup.md`

## 注意事項

- **Windows Server**: PowerShellコマンドを使用
- **Base64エンコード**: 改行を必ず削除（`tr -d '\n'`）
- **タイムアウト**: SSMコマンドは最大30分でタイムアウト
- **同期時間**: 大量データ同期は時間がかかる（数時間）
