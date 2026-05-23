# Phase 2 Monitoring Stack

Prometheus + Grafana + Loki + Alertmanager によるオブザーバビリティ基盤。

## When to Use

- システムメトリクスの監視
- ログの集約・検索
- アラート設定・管理
- ダッシュボード作成

## Components

### Core Services

| サービス | ポート | 説明 |
|---------|-------|------|
| **Prometheus** | 9090 | メトリクス収集・保存 |
| **Grafana** | 3001 | ダッシュボード・可視化 |
| **Loki** | 3100 | ログ集約 |
| **Alertmanager** | 9093 | アラートルーティング |

### Exporters

| エクスポーター | ポート | 説明 |
|--------------|-------|------|
| **Node Exporter** | 9100 | ホストメトリクス |
| **cAdvisor** | 8081 | コンテナメトリクス |
| **Promtail** | - | ログ収集 |

## Usage

```bash
# 監視スタック起動
make monitoring-up

# ヘルスチェック
make monitoring-health

# メトリクス確認
make monitoring-metrics

# アラート確認
make monitoring-alerts

# 監視スタック停止
make monitoring-down
```

## Dashboards

### TAISUN Overview
- CPU使用率（ゲージ + 時系列）
- メモリ使用率（ゲージ + 時系列）
- ディスク使用率
- サービスステータス

### アクセス
- Grafana: http://localhost:3001
- ログイン: admin / taisun2024

## Alert Rules

### Critical Alerts

| アラート | 条件 | 説明 |
|---------|------|------|
| `LowDiskSpace` | ディスク < 15% | ディスク容量不足 |
| `ContainerDown` | コンテナ停止 | TAISUNコンテナダウン |
| `PrometheusTargetDown` | ターゲット停止 | 監視対象ダウン |

### Warning Alerts

| アラート | 条件 | 説明 |
|---------|------|------|
| `HighCPUUsage` | CPU > 80% (5分) | CPU高負荷 |
| `HighMemoryUsage` | メモリ > 85% (5分) | メモリ高負荷 |
| `ContainerHighCPU` | コンテナCPU > 80% | コンテナCPU高負荷 |
| `ContainerHighMemory` | コンテナメモリ > 80% | コンテナメモリ高負荷 |

## Configuration Files

```
config/monitoring/
├── prometheus.yml      # Prometheus設定
├── alerts.yml          # アラートルール
├── alertmanager.yml    # Alertmanager設定
├── loki.yml            # Loki設定
├── promtail.yml        # Promtail設定
└── grafana/
    ├── provisioning/
    │   ├── datasources/
    │   │   └── datasources.yml
    │   └── dashboards/
    │       └── dashboards.yml
    └── dashboards/
        └── taisun-overview.json
```

## Data Retention

| サービス | 保持期間 |
|---------|---------|
| Prometheus | 15日 |
| Loki | 7日 |

## Notification Setup

### Webhook設定（例）

`config/monitoring/alertmanager.yml` を編集：

```yaml
receivers:
  - name: 'slack-notifications'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/xxx'
        channel: '#alerts'
```

## Related Skills

- `setup-monitoring` - 監視セットアップコマンド
- `phase1-tools` - Phase 1 ドキュメント処理
