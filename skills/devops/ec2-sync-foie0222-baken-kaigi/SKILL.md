---
name: ec2-sync
description: EC2操作簡素化（複雑なSSMコマンドをシンプルなインターフェースでラップ）
version: 2.0.0
tools:
  - Bash
  - Read
skill_type: workflow
auto_invoke: false
---

# EC2操作簡素化

## 概要

EC2操作を簡単なコマンドで実行できるようにします。複雑なAWS SSMコマンドを簡潔なインターフェースでラップし、ミスを防止します。

> **Note**: JRA-VANデータの同期はPC-KEIBAソフトで行います。

## 主要機能

1. **ファイルアップロード**: Base64エンコード自動化
2. **ログ確認**: リアルタイムログ表示
3. **状態確認**: EC2インスタンス状態確認

## 入力形式

```
/ec2-sync <操作>

操作:
  upload <ファイル名>       - ファイルをEC2に送信
  logs                      - ログ確認
  status                    - EC2インスタンス状態確認
```

## 実行プロセス

### 操作1: ファイルアップロード

**コマンド**:
```
/ec2-sync upload main.py
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
FILE_B64=$(base64 jravan-api/main.py | tr -d '\n')
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\main.py -Encoding UTF8 -Force\"]"

echo "✅ main.py を送信しました"
```

### 操作2: ログ確認

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

### 操作3: EC2インスタンス状態確認

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

## 出力形式

### ファイルアップロード成功時

```
📤 ファイルアップロード

ファイル: main.py
送信先: EC2 (i-0123456789abcdef0)

実行中...

✅ 送信完了
```

### 状態確認時

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
   Error: File not found: jravan-api/main.py
   ```
   - 対処: カレントディレクトリを確認
   - コマンド: `ls jravan-api/`

## セキュリティ

- **認証**: AWS認証情報が必要（`aws configure`）
- **IAM権限**: EC2, SSM, CloudWatch Logs の読み取り・書き込み権限
- **データ保護**: スクリプト内に機密情報をハードコードしない

## 対象ファイル

### アップロード可能なファイル
- `main.py` - FastAPI サーバー
- `database.py` - データベースアクセス層
- `requirements.txt` - Python依存関係

### EC2配置先
- `C:\jravan-api\<ファイル名>`

## 参照

- **AWS操作ガイド**: `.claude/docs/aws-operations.md` の「EC2操作」セクション
- **AWS SSM**: https://docs.aws.amazon.com/systems-manager/
- **CloudWatch Logs**: https://docs.aws.amazon.com/cloudwatch/

## 注意事項

- **SSM制限**: コマンド実行は最大30分でタイムアウト
- **ログ保持**: CloudWatch Logs は7日間保持
- **データ同期**: PC-KEIBAソフトで行う（このスキルでは行わない）
