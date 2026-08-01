---
name: claude-skills-connection-pooling-skill-md
description: このスキルは、データベース接続管理の設計と実装に関する
---

---
name: .claude/skills/connection-pooling/SKILL.md
description: |
    データベース接続管理の専門スキル。
    サーバーレス環境での接続管理、Tursoの接続管理とEmbedded Replicas、
    高負荷時の接続最適化を専門とします。
    専門分野:
    - 接続管理設計: 環境に応じた最適な接続設定
    - サーバーレス対応: TursoでのlibSQL接続管理とEmbedded Replicas
    - Drizzle ORM統合: DrizzleでのlibSQL接続設定
    - 障害対策: 接続エラーハンドリングとリトライ
    - 監視: 接続状態の監視とアラート
    使用タイミング:
    - 新規プロジェクトでDB接続を設定する時
    - 接続設定のサイジングを決める時
    - サーバーレス環境での接続問題を解決する時
    - 接続エラーが頻発する時
    - 高負荷時の接続最適化が必要な時
    Use proactively when setting up database connections,
    troubleshooting connection issues, or optimizing for serverless.

  📚 リソース参照:
  このスキルには以下のリソースが含まれています。
  必要に応じて該当するリソースを参照してください:

  - `.claude/skills/connection-pooling/resources/error-handling.md`: 接続エラーのハンドリングとリトライ戦略
  - `.claude/skills/connection-pooling/resources/pool-sizing-guide.md`: 環境別プールサイズ設定と計算式
  - `.claude/skills/connection-pooling/resources/serverless-connections.md`: TursoでのサーバーレスlibSQL接続管理
  - `.claude/skills/connection-pooling/templates/drizzle-config-template.ts`: Drizzle ORM接続設定テンプレート
  - `.claude/skills/connection-pooling/scripts/check-connections.mjs`: 接続状態の確認と診断スクリプト

version: 1.0.0
---

# Connection Pooling

## 概要

このスキルは、データベース接続管理の設計と実装に関する
知識を提供します。特にサーバーレス環境（Turso）での
libSQL接続管理とEmbedded Replicasに焦点を当てています。

**主要な価値**:

- サーバーレス環境での安定した接続
- Embedded Replicasによるローカル↔クラウド同期
- 高負荷時のパフォーマンス維持
- 接続リソースの効率的な利用

**対象ユーザー**:

- `.claude/agents/dba-mgr.md`エージェント
- バックエンド開発者
- DevOpsエンジニア
- SREチーム

## リソース構造

```
connection-pooling/
├── SKILL.md                                    # 本ファイル
├── resources/
│   ├── pool-sizing-guide.md                   # プールサイジング
│   ├── serverless-connections.md              # サーバーレス接続
│   └── error-handling.md                      # エラーハンドリング
├── scripts/
│   └── check-connections.mjs                  # 接続状態確認
└── templates/
    └── drizzle-config-template.ts             # Drizzle設定テンプレート
```

## コマンドリファレンス

### リソース読み取り

```bash
# プールサイジング
cat .claude/skills/connection-pooling/resources/pool-sizing-guide.md

# サーバーレス接続
cat .claude/skills/connection-pooling/resources/serverless-connections.md

# エラーハンドリング
cat .claude/skills/connection-pooling/resources/error-handling.md
```

### スクリプト実行

```bash
# 接続状態確認
node .claude/skills/connection-pooling/scripts/check-connections.mjs
```

## いつ使うか

### シナリオ1: 新規プロジェクトセットアップ

**状況**: 新しいプロジェクトでDB接続を設定する

**適用条件**:

- [ ] データベースサービスが決定済み
- [ ] 想定負荷が見積もられている
- [ ] 実行環境が決まっている

**期待される成果**: 最適な接続プール設定

### シナリオ2: 接続エラーの解決

**状況**: 「too many connections」などのエラーが発生

**適用条件**:

- [ ] エラーの発生パターンが把握できている
- [ ] 現在の設定が確認できる
- [ ] 接続数の監視ができる

**期待される成果**: 安定した接続設定

### シナリオ3: サーバーレス移行

**状況**: サーバーレス環境への移行で接続管理を見直す

**適用条件**:

- [ ] サーバーレスプラットフォームが決定
- [ ] 接続パターンが理解されている
- [ ] Embedded Replicasの使用を検討している

**期待される成果**: サーバーレス対応の接続設定

## ワークフロー

### Phase 1: 要件分析

**目的**: 接続要件を明確化する

**ステップ**:

1. **環境の確認**:
   - サーバーレス vs 常駐サーバー
   - Turso Cloud / Embedded Replicas / Self-hosted
   - ワーカー数・インスタンス数

2. **負荷の見積もり**:
   - 同時リクエスト数
   - クエリの実行時間
   - ピーク時の負荷

**判断基準**:

- [ ] 実行環境が明確か？
- [ ] 負荷の見積もりがあるか？
- [ ] Embedded Replicasの使用を検討したか？

**リソース**: `resources/serverless-connections.md`

### Phase 2: 接続設計

**目的**: 適切な接続設定を決定する

**ステップ**:

1. **接続設定の実装**:

   ```typescript
   // Turso接続設定
   const config = {
     url: process.env.TURSO_DATABASE_URL,
     authToken: process.env.TURSO_AUTH_TOKEN,
   };
   ```

2. **Embedded Replicas設定**:
   ```typescript
   const client = createClient({
     url: "file:local.db", // ローカルレプリカ
     syncUrl: process.env.TURSO_DATABASE_URL,
     authToken: process.env.TURSO_AUTH_TOKEN,
     syncInterval: 60, // 60秒ごとに同期
   });
   ```

**判断基準**:

- [ ] 接続URLとトークンは設定されているか？
- [ ] Embedded Replicasの使用を検討したか？
- [ ] 同期間隔は適切か？
- [ ] リトライ設定があるか？

**リソース**: `resources/pool-sizing-guide.md`

### Phase 3: エラーハンドリング

**目的**: 接続エラーに対する回復力を確保する

**ステップ**:

1. **リトライ戦略**:
   - 指数バックオフ
   - 最大リトライ回数
   - リトライ可能なエラーの定義

2. **サーキットブレーカー**:
   - 連続失敗時のオープン
   - 回復試行間隔
   - 半開状態の管理

**判断基準**:

- [ ] リトライ戦略が実装されているか？
- [ ] タイムアウトが設定されているか？
- [ ] エラーログが記録されるか？

**リソース**: `resources/error-handling.md`

### Phase 4: 監視

**目的**: 接続状態を継続的に監視する

**ステップ**:

1. **メトリクスの収集**:
   - アクティブ接続数
   - 待機中の接続
   - 接続エラー率

2. **アラート設定**:
   - 接続枯渇の警告
   - エラー率の閾値
   - レイテンシの監視

**判断基準**:

- [ ] 接続数の監視があるか？
- [ ] アラートが設定されているか？
- [ ] ダッシュボードがあるか？

## 核心概念

### 接続プールの基本

```
アプリケーション
    │
    ├── リクエスト1 ──→ [接続1]
    ├── リクエスト2 ──→ [接続2]  ←── 接続プール
    ├── リクエスト3 ──→ [接続3]       (再利用)
    └── リクエスト4 ──→ [待機...]
                           │
                           ▼
                      データベース
```

### プールモード

| モード      | 説明                           | 用途                 |
| ----------- | ------------------------------ | -------------------- |
| Session     | 接続をセッション全体で保持     | 長いトランザクション |
| Transaction | トランザクション単位で割り当て | 一般的なWeb          |
| Statement   | ステートメント単位で割り当て   | 高速なクエリ         |

### サーバーレス特有の課題

```
Lambda/Edge Function
    │
    ├── コールドスタート → 新規接続
    │                      (オーバーヘッド)
    ├── ウォームスタート → 既存接続再利用
    │                      (高速)
    └── スケールアウト → 接続爆発のリスク
                          (プーラーで制御)
```

## ベストプラクティス

### すべきこと

1. **適切な接続方式を選択する**:
   - Turso Cloud: HTTPSベースの接続
   - Embedded Replicas: ローカルファイル + クラウド同期
   - Self-hosted: libSQL Server

2. **接続を適切にリリースする**:

   ```typescript
   try {
     const result = await client.execute("SELECT * FROM users");
     return result;
   } finally {
     // libSQLクライアントは自動的に接続を管理
     // Embedded Replicasの場合は定期的に同期
   }
   ```

3. **同期設定を最適化する**:
   ```typescript
   const config = {
     syncInterval: 60, // 同期間隔（秒）
     syncOnWrite: true, // 書き込み時に同期
     readYourWrites: true, // 自分の書き込みを即座に読み取り
   };
   ```

### 避けるべきこと

1. **接続のリーク**:
   - ❌ 接続を閉じ忘れる
   - ✅ try-finallyで確実にリリース

2. **不適切な同期設定**:
   - ❌ 同期間隔が短すぎる（ネットワーク負荷）
   - ✅ アプリケーション要件に応じた適切な間隔

3. **Embedded Replicasの未活用**:
   - ❌ サーバーレス環境で常にリモート接続
   - ✅ Embedded Replicasでローカル読み取り + クラウド同期

## トラブルシューティング

### 問題1: 同期エラー

**症状**: Embedded Replicasの同期が失敗

**原因**:

- ネットワーク接続の問題
- 認証トークンの期限切れ
- 同期URLの設定ミス

**解決策**:

```typescript
// 同期状態の確認
const syncStatus = await client.sync();
console.log("Sync completed:", syncStatus);

// 手動で強制同期
await client.sync();

// 同期エラーのハンドリング
client.on("sync-error", (error) => {
  console.error("Sync failed:", error);
  // リトライロジック
});
```

### 問題2: 接続タイムアウト

**症状**: Tursoへの接続がタイムアウト

**原因**:

- ネットワーク遅延
- 認証トークンの問題
- リージョンが遠い

**解決策**:

```typescript
// Embedded Replicasを使用してローカル接続
const client = createClient({
  url: "file:local.db",
  syncUrl: process.env.TURSO_DATABASE_URL,
  authToken: process.env.TURSO_AUTH_TOKEN,
});

// リトライ戦略
const retryConfig = {
  retries: 3,
  factor: 2,
  minTimeout: 1000,
  maxTimeout: 5000,
};
```

### 問題3: コールドスタートの遅延

**症状**: Lambda/Edgeの初回リクエストが遅い

**原因**:

- リモートDB接続の確立
- HTTPS通信のオーバーヘッド
- 認証処理

**解決策**:

- Embedded Replicasの使用（ローカルファイルアクセス）
- Provisioned Concurrencyの使用
- クライアントインスタンスのキャッシング

## 関連スキル

- **.claude/skills/query-performance-tuning/SKILL.md** (`.claude/skills/query-performance-tuning/SKILL.md`): クエリ最適化
- **.claude/skills/backup-recovery/SKILL.md** (`.claude/skills/backup-recovery/SKILL.md`): バックアップ戦略

## メトリクス

### 接続プール健全性指標

| 指標           | 目標値  | 警告値  |
| -------------- | ------- | ------- |
| 接続使用率     | < 80%   | > 90%   |
| 待機リクエスト | 0       | > 10    |
| 接続エラー率   | < 0.1%  | > 1%    |
| 平均接続時間   | < 100ms | > 500ms |

## 変更履歴

| バージョン | 日付       | 変更内容                  |
| ---------- | ---------- | ------------------------- |
| 1.0.0      | 2025-11-27 | 初版作成 - 接続プール管理 |

## 参考文献

- **Turso Documentation**: https://docs.turso.tech/
- **libSQL**: https://github.com/tursodatabase/libsql
- **Embedded Replicas**: https://docs.turso.tech/features/embedded-replicas
