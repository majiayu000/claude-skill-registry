---
name: ecommerce
description: ECサイト開発 - 商品管理、カート、決済、注文フロー、在庫管理の設計・実装支援
requires-guidelines:
  - common
  - design/ecommerce-platforms
---

# ECサイト開発

## 使用タイミング

- **ECサイト新規構築時**
- **商品・注文・決済機能の設計時**
- **既存ECサイトのレビュー・改善時**

## ドメイン設計

### コアエンティティ

| エンティティ | 責務 |
|-------------|------|
| Product | 商品マスタ（タイトル・説明・画像） |
| Variant | バリエーション（SKU・価格・在庫） |
| Cart | 買い物かご |
| Order | 注文（ステータス・配送・支払） |
| Customer | 顧客情報 |
| Payment | 決済情報 |

### 状態遷移

```
注文: [作成] → [支払待ち] → [支払済] → [発送準備] → [発送済] → [完了]
在庫: [在庫あり] ←→ [残りわずか] → [在庫切れ] → [入荷待ち]
```

## 要件チェックリスト

### 商品管理
- [ ] 商品CRUD
- [ ] バリエーション（サイズ・色）
- [ ] 在庫管理（リアルタイム）
- [ ] カテゴリ・タグ
- [ ] 検索・フィルタ

### カート・購入
- [ ] カート操作
- [ ] クーポン・割引
- [ ] 送料計算
- [ ] 配送日時指定
- [ ] ギフト設定

### 決済
- [ ] クレジットカード
- [ ] コンビニ払い
- [ ] 後払い / 電子マネー
- [ ] 定期購入

### 顧客管理
- [ ] 会員登録・ログイン
- [ ] 住所帳
- [ ] 注文履歴
- [ ] ポイント

### 法令対応
- [ ] 特定商取引法に基づく表記
- [ ] プライバシーポリシー
- [ ] 利用規約

## 技術設計

### 在庫確保パターン

```typescript
// 楽観的ロック
async function reserveStock(variantId: string, qty: number) {
  const result = await db.variant.updateMany({
    where: {
      id: variantId,
      inventory: { gte: qty },
      version: currentVersion,
    },
    data: {
      inventory: { decrement: qty },
      version: { increment: 1 },
    },
  });
  
  if (result.count === 0) {
    throw new StockNotAvailableError();
  }
}
```

### 決済フロー

```
1. カート確定 → 在庫仮押さえ
2. 決済開始 → 決済サービス呼び出し
3. 成功 → 注文確定・在庫確定
4. 失敗 → 在庫解放
5. タイムアウト（15分） → 在庫解放
```

### API設計

```yaml
GET    /products          # 商品一覧
GET    /products/:id      # 商品詳細
POST   /cart/items        # カート追加
DELETE /cart/items/:id    # カート削除
POST   /orders            # 注文作成
GET    /orders/:id        # 注文詳細
```

## セキュリティ

- [ ] HTTPS強制
- [ ] PCI DSS準拠（カード情報非保持）
- [ ] CSRF / XSS対策
- [ ] 認証（2FA推奨）
- [ ] 監査ログ

## パフォーマンス目標

| 指標 | 目標 |
|------|------|
| ページ読み込み | < 3秒 |
| 検索応答 | < 500ms |
| 決済処理 | < 5秒 |

## プラットフォーム別

### Shopify
- context7: `/websites/shopify_dev`
- Storefront API / Admin GraphQL
- Hydrogen（ヘッドレス）

### STORES
- API: https://heyinc.github.io/retail-api-docs/
- OAuth 2.0 / スタンダードプラン以上

### 自社開発
- Stripe / GMO / PAY.JP
- Algolia / Elasticsearch

## 出力形式

### 設計時
```
📋 ドメインモデル
📦 エンティティ一覧
🔄 状態遷移図
✅ 要件チェックリスト
```

### レビュー時
```
🔴 Critical: 問題点 - 修正案
🟡 Warning: 改善推奨 - 提案
📊 Summary: カバー率 X%
```

## 外部知識ベース

context7で最新ドキュメント確認:
- `/websites/shopify_dev` - Shopify開発
- `/shopify/hydrogen` - ヘッドレスEC
- `/woocommerce/woocommerce` - WooCommerce
- `/medusajs/medusa` - Medusa（OSS）
