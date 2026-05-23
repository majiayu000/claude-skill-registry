---
name: ec2-sync
description: JRA-VANデータ同期・EC2操作簡素化（複雑なSSMコマンドをシンプルなインターフェースでラップ）
version: 1.0.0
tools:
  - Bash
  - Read
skill_type: workflow
auto_invoke: false
---

# EC2データ同期・操作簡素化

## 概要

JRA-VAN データ同期とEC2操作を簡単なコマンドで実行できるようにします。複雑なAWS SSMコマンドを簡潔なインターフェースでラップし、ミスを防止します。

## 主要機能

1. **ファイルアップロード**: Base64エンコード自動化
2. **データ差分同期**: 最新データのみ取得
3. **指定日からの完全同期**: 特定日以降のデータを再取得
4. **ログ確認**: リアルタイムログ表示

## 入力形式

```
/ec2-sync <操作>

操作:
  upload <ファイル名>       - ファイルをEC2に送信
  sync                      - 差分同期実行
  sync-from <YYYYMMDD>      - 指定日からの完全同期
  logs                      - ログ確認
  status                    - EC2インスタンス状態確認
```

## 実行プロセス

### 操作1: ファイルアップロード

**コマンド**:
```
/ec2-sync upload sync_jvlink.py
```

**実行内容**:
1. EC2インスタンスIDを自動取得
2. ファイルをBase64エンコード
3. SSM経由でEC2に送信
4. 送信完了を確認

**内部コマンド**:
```bash
# インスタンスID取得
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*jravan*" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text)

# Base64エンコード＆送信
FILE_B64=$(base64 jravan-api/sync_jvlink.py | tr -d '\n')
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\sync_jvlink.py -Encoding UTF8 -Force\"]"

echo "✅ sync_jvlink.py を送信しました"
```

### 操作2: データ差分同期

**コマンド**:
```
/ec2-sync sync
```

**実行内容**:
1. EC2で `sync_jvlink.py` を実行
2. 最新データのみ取得
3. 進捗をログで確認

**内部コマンド**:
```bash
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*jravan*" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text)

aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py"]'

echo "✅ データ差分同期を開始しました"
echo "ログ確認: /ec2-sync logs"
```

### 操作3: 指定日からの完全同期

**コマンド**:
```
/ec2-sync sync-from 20260101
```

**実行内容**:
1. 2026年1月1日以降のデータを完全に再取得
2. 既存データは上書き
3. 大量データの場合は時間がかかる

**内部コマンド**:
```bash
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*jravan*" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text)

aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py --from 20260101"]'

echo "✅ 2026/01/01 からの完全同期を開始しました"
echo "⚠️  大量データのため、完了まで数時間かかる場合があります"
echo "ログ確認: /ec2-sync logs"
```

### 操作4: ログ確認

**コマンド**:
```
/ec2-sync logs
```

**実行内容**:
1. CloudWatch Logs から最新ログを取得
2. リアルタイムでログをフォロー

**内部コマンド**:
```bash
aws logs tail /aws/ec2/jravan --follow
```

**出力例**:
```
2026-01-23 15:30:00 [INFO] 同期開始: 2026-01-20 から
2026-01-23 15:30:05 [INFO] レースデータ取得中: 東京 1R
2026-01-23 15:30:10 [INFO] レースデータ取得中: 東京 2R
...
2026-01-23 15:35:00 [INFO] 同期完了: 36レース
```

### 操作5: EC2インスタンス状態確認

**コマンド**:
```
/ec2-sync status
```

**実行内容**:
1. EC2インスタンスの状態を確認
2. SSMエージェントの接続状態を確認

**内部コマンド**:
```bash
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*jravan*" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text)

# インスタンス状態
aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,LaunchTime]' \
  --output table

# SSM接続状態
aws ssm describe-instance-information \
  --filters "Key=InstanceIds,Values=$INSTANCE_ID" \
  --query 'InstanceInformationList[].[InstanceId,PingStatus,LastPingDateTime]' \
  --output table
```

**出力例**:
```
---------------------------------------------------------
|                 DescribeInstances                     |
+------------------------+----------+--------------------+
|  i-0123456789abcdef0  | running  | 2026-01-23T10:00:00|
+------------------------+----------+--------------------+

---------------------------------------------------------
|         DescribeInstanceInformation                    |
+------------------------+-----------+--------------------+
|  i-0123456789abcdef0  | Online    | 2026-01-23T15:45:00|
+------------------------+-----------+--------------------+
```

## 出力形式

### ファイルアップロード成功時

```
📤 ファイルアップロード

ファイル: sync_jvlink.py
送信先: EC2 (i-0123456789abcdef0)

実行中...

✅ 送信完了

次のアクション:
- [ ] データ同期: /ec2-sync sync
```

### データ同期開始時

```
🔄 データ差分同期

インスタンス: i-0123456789abcdef0
実行コマンド: python sync_jvlink.py

✅ 同期を開始しました

進捗確認:
- /ec2-sync logs でリアルタイムログ表示
```

### 完全同期開始時

```
🔄 完全同期（2026/01/01 から）

インスタンス: i-0123456789abcdef0
実行コマンド: python sync_jvlink.py --from 20260101

✅ 完全同期を開始しました

⚠️  注意:
- 大量データのため、完了まで数時間かかる場合があります
- 既存データは上書きされます

進捗確認:
- /ec2-sync logs でリアルタイムログ表示
```

## よくある操作フロー

### フロー1: スクリプト更新 → データ同期

```
1. /ec2-sync upload sync_jvlink.py
   → スクリプトをEC2に送信

2. /ec2-sync sync
   → 差分同期実行

3. /ec2-sync logs
   → 進捗確認
```

### フロー2: 特定期間のデータ再取得

```
1. /ec2-sync sync-from 20260120
   → 2026/01/20 以降のデータを完全同期

2. /ec2-sync logs
   → 進捗確認（数時間かかる可能性）
```

### フロー3: EC2状態確認

```
1. /ec2-sync status
   → インスタンス状態とSSM接続確認

2. エラーの場合はAWSコンソールで確認
```

## エラーハンドリング

### よくあるエラー

1. **インスタンスIDが見つからない**
   ```
   Error: No instances found with tag 'jravan'
   ```
   - 対処: EC2インスタンスが起動しているか確認
   - コマンド: `aws ec2 describe-instances`

2. **SSMエージェント未接続**
   ```
   Error: TargetNotConnected
   ```
   - 対処: SSMエージェントの起動を確認
   - コマンド: `/ec2-sync status`

3. **ファイルが見つからない**
   ```
   Error: File not found: jravan-api/sync_jvlink.py
   ```
   - 対処: カレントディレクトリを確認
   - コマンド: `ls jravan-api/`

4. **同期スクリプトエラー**
   ```
   Error in sync_jvlink.py
   ```
   - 対処: ログを確認してスクリプトを修正
   - コマンド: `/ec2-sync logs`

## セキュリティ

- **認証**: AWS認証情報が必要（`aws configure`）
- **IAM権限**: EC2, SSM, CloudWatch Logs の読み取り・書き込み権限
- **データ保護**: スクリプト内に機密情報をハードコードしない

## 対象ファイル

### アップロード可能なファイル
- `sync_jvlink.py` - データ同期スクリプト（メイン）
- `race_api.py` - FastAPI サーバー
- `config.py` - 設定ファイル
- `requirements.txt` - Python依存関係

### EC2配置先
- `C:\jravan-api\<ファイル名>`

## 使用例

### 例1: スクリプト更新と同期

```
/ec2-sync upload sync_jvlink.py

📤 ファイルアップロード
ファイル: sync_jvlink.py
✅ 送信完了

/ec2-sync sync

🔄 データ差分同期
✅ 同期を開始しました

/ec2-sync logs

2026-01-23 15:30:00 [INFO] 同期開始
2026-01-23 15:30:05 [INFO] レースデータ取得中: 東京 1R
...
2026-01-23 15:35:00 [INFO] 同期完了: 36レース
```

### 例2: 特定日からの再同期

```
/ec2-sync sync-from 20260115

🔄 完全同期（2026/01/15 から）
✅ 完全同期を開始しました

⚠️  数時間かかる可能性があります

/ec2-sync logs

2026-01-23 16:00:00 [INFO] 完全同期開始: 2026-01-15 から
2026-01-23 16:00:30 [INFO] 処理中: 2026-01-15 東京
...
```

## 参照

- **CLAUDE.md**: `main/CLAUDE.md` の「EC2 コード更新」セクション
- **同期スクリプト**: `jravan-api/sync_jvlink.py`
- **AWS SSM**: https://docs.aws.amazon.com/systems-manager/
- **CloudWatch Logs**: https://docs.aws.amazon.com/cloudwatch/

## 注意事項

- **同期時間**: 大量データは数時間かかる
- **データ上書き**: 完全同期は既存データを上書き
- **SSM制限**: コマンド実行は最大30分でタイムアウト
- **ログ保持**: CloudWatch Logs は7日間保持
