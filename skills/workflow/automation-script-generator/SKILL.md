---
name: automation-script-generator
description: 繰り返し作業の自動化スクリプト生成スキル。Shell、Python、PowerShell、Node.jsスクリプトを生成。ファイル操作、データ処理、API連携、CI/CD、バックアップ、監視、レポート生成を自動化。
---

# Automation Script Generator Skill

繰り返し作業を自動化するスクリプトを生成するスキルです。

## 概要

このスキルは、日常的な繰り返し作業を自動化するスクリプトを生成します。ファイル操作、データ処理、API連携、バックアップ、監視、レポート生成など、あらゆる定型作業を効率化します。複数のスクリプト言語に対応し、エラーハンドリング、ログ出力、スケジュール実行にも対応します。

## 主な機能

- **マルチ言語対応**: Bash, Python, PowerShell, Node.js, Ruby
- **ファイル操作**: 一括リネーム、コピー、移動、圧縮、削除
- **データ処理**: CSV/JSON変換、フィルタリング、集計、マージ
- **API連携**: REST API呼び出し、認証、エラーハンドリング
- **バックアップ自動化**: ファイル、DB、クラウドストレージ
- **監視・アラート**: リソース監視、ヘルスチェック、通知
- **レポート生成**: ログ分析、メトリクス集計、HTML/PDFレポート
- **CI/CDスクリプト**: ビルド、テスト、デプロイの自動化
- **スケジュール実行**: cron, タスクスケジューラ設定
- **エラーハンドリング**: 堅牢なエラー処理とリトライ機能

## スクリプトタイプ

### 1. ファイル操作

#### 一括リネーム（Bash）

```bash
#!/bin/bash

# 画像ファイルを日付順にリネーム
# 使用例: ./rename_images.sh /path/to/images

set -euo pipefail

SOURCE_DIR="${1:-.}"
PREFIX="photo"
EXTENSION="jpg"

# カウンター初期化
counter=1

# ファイルを更新日時順でソート
find "$SOURCE_DIR" -type f -name "*.$EXTENSION" -print0 | \
  sort -z | \
  while IFS= read -r -d '' file; do
    # 新しいファイル名を生成（ゼロパディング）
    new_name=$(printf "%s_%04d.%s" "$PREFIX" "$counter" "$EXTENSION")
    new_path="$SOURCE_DIR/$new_name"

    # リネーム実行
    if [ "$file" != "$new_path" ]; then
      mv -v "$file" "$new_path"
      echo "Renamed: $(basename "$file") -> $new_name"
    fi

    ((counter++))
  done

echo "✓ リネーム完了: $((counter - 1)) ファイル"
```

#### ファイル整理（Python）

```python
#!/usr/bin/env python3
"""
ダウンロードフォルダを拡張子別に整理
使用例: python organize_files.py ~/Downloads
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import logging

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 拡張子とフォルダのマッピング
EXTENSION_MAPPING = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv'],
    'Audio': ['.mp3', '.wav', '.flac', '.m4a'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Code': ['.py', '.js', '.java', '.cpp', '.html', '.css'],
}

def organize_files(source_dir: str, dry_run: bool = False):
    """ファイルを拡張子別に整理"""
    source_path = Path(source_dir)

    if not source_path.exists():
        logging.error(f"ディレクトリが存在しません: {source_dir}")
        return

    files_moved = 0

    for file_path in source_path.iterdir():
        # ディレクトリはスキップ
        if file_path.is_dir():
            continue

        # 拡張子を取得
        extension = file_path.suffix.lower()

        # 対応するフォルダを特定
        target_folder = None
        for folder, extensions in EXTENSION_MAPPING.items():
            if extension in extensions:
                target_folder = folder
                break

        # マッピングにない拡張子は "Others" に
        if target_folder is None:
            target_folder = "Others"

        # 移動先ディレクトリを作成
        dest_dir = source_path / target_folder
        if not dry_run:
            dest_dir.mkdir(exist_ok=True)

        # ファイルを移動
        dest_path = dest_dir / file_path.name

        # 同名ファイルが存在する場合、タイムスタンプを追加
        if dest_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = dest_path.stem
            suffix = dest_path.suffix
            dest_path = dest_dir / f"{stem}_{timestamp}{suffix}"

        if dry_run:
            logging.info(f"[DRY RUN] {file_path.name} -> {target_folder}/")
        else:
            shutil.move(str(file_path), str(dest_path))
            logging.info(f"移動: {file_path.name} -> {target_folder}/")

        files_moved += 1

    logging.info(f"✓ 完了: {files_moved} ファイルを整理しました")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用法: python organize_files.py <ディレクトリパス> [--dry-run]")
        sys.exit(1)

    source_dir = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    organize_files(source_dir, dry_run)
```

### 2. データ処理

#### CSV to JSON変換（Node.js）

```javascript
#!/usr/bin/env node
/**
 * CSVファイルをJSONに変換
 * 使用例: node csv_to_json.js input.csv output.json
 */

const fs = require('fs');
const csv = require('csv-parser');

function csvToJson(inputFile, outputFile) {
  const results = [];

  fs.createReadStream(inputFile)
    .pipe(csv())
    .on('data', (data) => results.push(data))
    .on('end', () => {
      // JSONファイルに書き込み
      fs.writeFileSync(
        outputFile,
        JSON.stringify(results, null, 2),
        'utf-8'
      );

      console.log(`✓ 変換完了: ${results.length} レコード`);
      console.log(`出力: ${outputFile}`);
    })
    .on('error', (error) => {
      console.error('エラー:', error.message);
      process.exit(1);
    });
}

// コマンドライン引数
const [inputFile, outputFile] = process.argv.slice(2);

if (!inputFile || !outputFile) {
  console.error('使用法: node csv_to_json.js <input.csv> <output.json>');
  process.exit(1);
}

csvToJson(inputFile, outputFile);
```

#### データ集計（Python）

```python
#!/usr/bin/env python3
"""
ログファイルから統計情報を集計
使用例: python analyze_logs.py access.log
"""

import re
from collections import Counter, defaultdict
from datetime import datetime
import json

def analyze_access_log(log_file: str):
    """アクセスログを分析"""

    # Apache/Nginx形式のログパターン
    log_pattern = re.compile(
        r'(?P<ip>[\d.]+) - - \[(?P<datetime>[^\]]+)\] '
        r'"(?P<method>\w+) (?P<path>[^\s]+) HTTP/[\d.]+" '
        r'(?P<status>\d+) (?P<size>\d+)'
    )

    stats = {
        'total_requests': 0,
        'status_codes': Counter(),
        'methods': Counter(),
        'paths': Counter(),
        'ips': Counter(),
        'hourly_distribution': defaultdict(int),
    }

    with open(log_file, 'r') as f:
        for line in f:
            match = log_pattern.match(line)
            if not match:
                continue

            data = match.groupdict()

            stats['total_requests'] += 1
            stats['status_codes'][data['status']] += 1
            stats['methods'][data['method']] += 1
            stats['paths'][data['path']] += 1
            stats['ips'][data['ip']] += 1

            # 時間帯別の集計
            try:
                dt = datetime.strptime(data['datetime'], '%d/%b/%Y:%H:%M:%S %z')
                hour = dt.hour
                stats['hourly_distribution'][hour] += 1
            except ValueError:
                pass

    # レポート生成
    print("=" * 60)
    print("アクセスログ分析レポート")
    print("=" * 60)
    print(f"\n総リクエスト数: {stats['total_requests']:,}")

    print("\n--- ステータスコード別 ---")
    for status, count in stats['status_codes'].most_common():
        print(f"{status}: {count:,}")

    print("\n--- HTTPメソッド別 ---")
    for method, count in stats['methods'].most_common():
        print(f"{method}: {count:,}")

    print("\n--- トップ10 パス ---")
    for path, count in stats['paths'].most_common(10):
        print(f"{count:,} - {path}")

    print("\n--- トップ10 IPアドレス ---")
    for ip, count in stats['ips'].most_common(10):
        print(f"{count:,} - {ip}")

    print("\n--- 時間帯別分布 ---")
    for hour in range(24):
        count = stats['hourly_distribution'][hour]
        bar = '█' * (count // 100)
        print(f"{hour:02d}:00 | {bar} {count:,}")

    # JSON出力
    output_file = log_file.replace('.log', '_stats.json')
    with open(output_file, 'w') as f:
        # Counterをdictに変換
        stats_dict = {
            'total_requests': stats['total_requests'],
            'status_codes': dict(stats['status_codes']),
            'methods': dict(stats['methods']),
            'top_paths': dict(stats['paths'].most_common(20)),
            'top_ips': dict(stats['ips'].most_common(20)),
            'hourly_distribution': dict(stats['hourly_distribution']),
        }
        json.dump(stats_dict, f, indent=2)

    print(f"\n✓ 詳細統計を保存: {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用法: python analyze_logs.py <log_file>")
        sys.exit(1)

    analyze_access_log(sys.argv[1])
```

### 3. API連携

#### REST API自動化（Python）

```python
#!/usr/bin/env python3
"""
GitHub API経由でリポジトリ情報を取得
使用例: python github_stats.py <username>
環境変数: GITHUB_TOKEN
"""

import os
import requests
from datetime import datetime
import json

GITHUB_API_BASE = "https://api.github.com"

def get_user_repos(username: str, token: str = None):
    """ユーザーのリポジトリ一覧を取得"""

    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    url = f"{GITHUB_API_BASE}/users/{username}/repos"
    params = {'per_page': 100, 'sort': 'updated'}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"エラー: {e}")
        return []

def generate_report(username: str, repos: list):
    """レポート生成"""

    if not repos:
        print("リポジトリが見つかりませんでした")
        return

    # 統計計算
    total_stars = sum(repo['stargazers_count'] for repo in repos)
    total_forks = sum(repo['forks_count'] for repo in repos)
    languages = {}

    for repo in repos:
        lang = repo.get('language')
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    # レポート出力
    print("=" * 60)
    print(f"GitHub リポジトリ統計: {username}")
    print("=" * 60)
    print(f"\n総リポジトリ数: {len(repos)}")
    print(f"総スター数: {total_stars:,}")
    print(f"総フォーク数: {total_forks:,}")

    print("\n--- 使用言語 ---")
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
        print(f"{lang}: {count}")

    print("\n--- トップ10 スター数 ---")
    top_repos = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)[:10]
    for repo in top_repos:
        print(f"{repo['stargazers_count']:,} ⭐ - {repo['name']}")
        print(f"  {repo['html_url']}")

    # JSON出力
    output_file = f"{username}_github_stats.json"
    with open(output_file, 'w') as f:
        json.dump({
            'username': username,
            'total_repos': len(repos),
            'total_stars': total_stars,
            'total_forks': total_forks,
            'languages': languages,
            'top_repos': [
                {
                    'name': repo['name'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'language': repo.get('language'),
                    'url': repo['html_url'],
                }
                for repo in top_repos
            ],
            'generated_at': datetime.now().isoformat(),
        }, f, indent=2)

    print(f"\n✓ レポートを保存: {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用法: python github_stats.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    token = os.environ.get('GITHUB_TOKEN')

    repos = get_user_repos(username, token)
    generate_report(username, repos)
```

### 4. バックアップ自動化

#### データベースバックアップ（Bash）

```bash
#!/bin/bash

# PostgreSQLデータベースの自動バックアップ
# 使用例: ./backup_postgres.sh

set -euo pipefail

# 設定
DB_NAME="mydb"
DB_USER="postgres"
BACKUP_DIR="/var/backups/postgres"
RETENTION_DAYS=7

# タイムスタンプ
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

# ログ関数
log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# バックアップディレクトリ作成
mkdir -p "$BACKUP_DIR"

# バックアップ実行
log "バックアップ開始: $DB_NAME"
pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  log "✓ バックアップ成功: $BACKUP_FILE"

  # ファイルサイズ表示
  SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
  log "ファイルサイズ: $SIZE"
else
  log "✗ バックアップ失敗"
  exit 1
fi

# 古いバックアップを削除（保持期間を過ぎたもの）
log "古いバックアップを削除（${RETENTION_DAYS}日以前）"
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql.gz" -type f -mtime +$RETENTION_DAYS -delete

# 現在のバックアップ一覧
log "現在のバックアップ:"
ls -lh "$BACKUP_DIR/${DB_NAME}_"*.sql.gz

log "バックアップ処理完了"
```

#### クラウドストレージ同期（Python）

```python
#!/usr/bin/env python3
"""
ローカルファイルをS3にバックアップ
使用例: python backup_to_s3.py /path/to/local s3://bucket-name/prefix
要件: pip install boto3
"""

import os
import boto3
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def backup_to_s3(local_path: str, s3_uri: str):
    """ローカルディレクトリをS3にバックアップ"""

    # S3クライアント
    s3 = boto3.client('s3')

    # S3 URI解析
    if not s3_uri.startswith('s3://'):
        raise ValueError("無効なS3 URI")

    parts = s3_uri[5:].split('/', 1)
    bucket = parts[0]
    prefix = parts[1] if len(parts) > 1 else ''

    local_path = Path(local_path)

    if not local_path.exists():
        logging.error(f"パスが存在しません: {local_path}")
        return

    files_uploaded = 0
    total_size = 0

    # 再帰的にファイルをアップロード
    for file_path in local_path.rglob('*'):
        if file_path.is_file():
            # S3キーを生成
            relative_path = file_path.relative_to(local_path)
            s3_key = f"{prefix}/{relative_path}".replace('\\', '/')

            # ファイルサイズ
            file_size = file_path.stat().st_size

            try:
                # アップロード
                s3.upload_file(
                    str(file_path),
                    bucket,
                    s3_key,
                    ExtraArgs={'StorageClass': 'STANDARD_IA'}
                )

                logging.info(f"アップロード: {relative_path} ({file_size:,} bytes)")
                files_uploaded += 1
                total_size += file_size

            except Exception as e:
                logging.error(f"アップロード失敗 {relative_path}: {e}")

    logging.info(f"✓ 完了: {files_uploaded} ファイル ({total_size:,} bytes)")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("使用法: python backup_to_s3.py <local_path> <s3_uri>")
        sys.exit(1)

    local_path = sys.argv[1]
    s3_uri = sys.argv[2]

    backup_to_s3(local_path, s3_uri)
```

### 5. 監視・アラート

#### サーバー監視（PowerShell）

```powershell
# サーバーリソース監視スクリプト
# 使用例: .\monitor_server.ps1

# 閾値設定
$CPU_THRESHOLD = 80
$MEMORY_THRESHOLD = 85
$DISK_THRESHOLD = 90

# ログファイル
$LOG_FILE = "C:\Logs\server_monitor.log"

function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Out-File -FilePath $LOG_FILE -Append
    Write-Host "$timestamp - $Message"
}

function Send-Alert {
    param($Subject, $Body)
    # ここにメール送信やSlack通知のロジックを実装
    Write-Log "ALERT: $Subject - $Body"
}

# CPU使用率チェック
$cpu = (Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples.CookedValue
if ($cpu -gt $CPU_THRESHOLD) {
    Send-Alert "CPU使用率が高い" "CPU使用率: $([math]::Round($cpu, 2))%"
}

# メモリ使用率チェック
$os = Get-CimInstance Win32_OperatingSystem
$totalMemory = $os.TotalVisibleMemorySize
$freeMemory = $os.FreePhysicalMemory
$usedMemoryPercent = (($totalMemory - $freeMemory) / $totalMemory) * 100

if ($usedMemoryPercent -gt $MEMORY_THRESHOLD) {
    Send-Alert "メモリ使用率が高い" "メモリ使用率: $([math]::Round($usedMemoryPercent, 2))%"
}

# ディスク使用率チェック
Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 } | ForEach-Object {
    $usedPercent = ($_.Used / ($_.Used + $_.Free)) * 100

    if ($usedPercent -gt $DISK_THRESHOLD) {
        Send-Alert "ディスク使用率が高い" "ドライブ $($_.Name): $([math]::Round($usedPercent, 2))%"
    }
}

# ステータスログ
Write-Log "監視実行完了 - CPU: $([math]::Round($cpu, 2))% | Memory: $([math]::Round($usedMemoryPercent, 2))%"
```

### 6. CI/CDスクリプト

#### ビルド＆デプロイ（Bash）

```bash
#!/bin/bash

# Node.jsアプリのビルド＆デプロイ
# 使用例: ./deploy.sh production

set -euo pipefail

ENV="${1:-staging}"
PROJECT_NAME="myapp"
BUILD_DIR="dist"
DEPLOY_SERVER="user@production-server.com"
DEPLOY_PATH="/var/www/$PROJECT_NAME"

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# 環境変数読み込み
if [ -f ".env.$ENV" ]; then
  log "環境変数読み込み: .env.$ENV"
  export $(cat ".env.$ENV" | xargs)
fi

# 依存関係インストール
log "依存関係インストール中..."
npm ci

# テスト実行
log "テスト実行中..."
npm test

if [ $? -ne 0 ]; then
  log "✗ テスト失敗 - デプロイ中止"
  exit 1
fi

# ビルド
log "ビルド実行中..."
npm run build

if [ ! -d "$BUILD_DIR" ]; then
  log "✗ ビルド失敗 - $BUILD_DIR が見つかりません"
  exit 1
fi

# バックアップ
log "デプロイ先でバックアップ作成中..."
ssh "$DEPLOY_SERVER" "cd $DEPLOY_PATH && tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz * || true"

# デプロイ
log "デプロイ中: $ENV"
rsync -avz --delete "$BUILD_DIR/" "$DEPLOY_SERVER:$DEPLOY_PATH/"

# サービス再起動
log "サービス再起動中..."
ssh "$DEPLOY_SERVER" "sudo systemctl restart $PROJECT_NAME"

# ヘルスチェック
log "ヘルスチェック実行中..."
sleep 5

HEALTH_URL="https://production-server.com/health"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL")

if [ "$STATUS" == "200" ]; then
  log "✓ デプロイ成功 - ヘルスチェックOK"
else
  log "✗ ヘルスチェック失敗 (HTTP $STATUS)"
  exit 1
fi
```

## スケジュール実行

### cron設定例

```bash
# 毎日午前2時にバックアップ実行
0 2 * * * /path/to/backup_script.sh >> /var/log/backup.log 2>&1

# 毎時0分にログ分析
0 * * * * /usr/bin/python3 /path/to/analyze_logs.py

# 5分ごとに監視スクリプト実行
*/5 * * * * /path/to/monitor_server.sh

# 毎週月曜日午前3時にクリーンアップ
0 3 * * 1 /path/to/cleanup_old_files.sh
```

### Windowsタスクスケジューラ（PowerShell）

```powershell
# タスクスケジューラにジョブを登録

$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
  -Argument "-File C:\Scripts\backup.ps1"

$trigger = New-ScheduledTaskTrigger -Daily -At 2am

$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" `
  -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask -TaskName "DailyBackup" `
  -Action $action `
  -Trigger $trigger `
  -Principal $principal `
  -Description "毎日午前2時にバックアップを実行"
```

## エラーハンドリング

### リトライ機能（Python）

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1, backoff=2):
    """リトライデコレータ"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise

                    print(f"エラー: {e}")
                    print(f"リトライ {attempts}/{max_attempts} - {current_delay}秒後に再試行...")
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator

@retry(max_attempts=3, delay=2, backoff=2)
def fetch_data_from_api(url):
    import requests
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
```

## 使用例

### 基本的な使い方

```
画像ファイルを日付順にリネームするBashスクリプトを生成してください。
```

### 具体的なタスク

```
以下の要件を満たすPythonスクリプトを生成してください：

タスク: ダウンロードフォルダを拡張子別に整理
要件:
- 拡張子ごとにフォルダを作成（Images, Documents, Videos等）
- 同名ファイルはタイムスタンプを付与
- ログ出力
- ドライラン機能

出力: Python 3.8以上
```

### API連携スクリプト

```
GitHub APIを使用して、ユーザーのリポジトリ統計を取得するスクリプトを生成してください：

機能:
- リポジトリ一覧取得
- スター数、フォーク数集計
- 使用言語の統計
- JSON形式でレポート出力
- 認証トークン対応

言語: Python
```

### バックアップ自動化

```
PostgreSQLデータベースのバックアップスクリプトを生成してください：

要件:
- 圧縮バックアップ（gzip）
- タイムスタンプ付きファイル名
- 7日以上前のバックアップを自動削除
- ログ出力
- エラーハンドリング

言語: Bash
出力: cron設定例も含めて
```

## ベストプラクティス

1. **エラーハンドリング**: すべての外部コマンド・API呼び出しにエラー処理
2. **ログ出力**: 実行状況を詳細にログ
3. **べき等性**: 複数回実行しても安全
4. **ドライラン**: 実際の処理前に確認可能
5. **設定の外部化**: ハードコードせず、環境変数や設定ファイルを使用
6. **バックアップ**: 破壊的操作の前にバックアップ
7. **通知**: 重要な処理の成功/失敗を通知
8. **ドキュメント**: 使用方法をコメントやREADMEに記載

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-11-22

---

## 使用例まとめ

### シンプルな自動化

```
ファイルをリネームするスクリプトを作成してください。
```

### 詳細な要件

```
以下のタスクを自動化するスクリプトを生成してください：
{詳細な要件}

言語: Python/Bash/PowerShell
エラーハンドリング: 含む
ログ出力: 含む
```

このスキルで、日々の繰り返し作業を自動化しましょう！
