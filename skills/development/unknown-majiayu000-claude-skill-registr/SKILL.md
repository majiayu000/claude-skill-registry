---
name: ddd-check
description: DDD設計原則チェッカー（AIDLC ドキュメントと実装コードの一貫性を検証）
version: 1.0.0
tools:
  - Read
  - Grep
  - Glob
skill_type: verification
auto_invoke: false
---

# DDD設計原則チェッカー

## 概要

ドメイン駆動設計（DDD）の原則に従った実装がなされているかを検証します。AIDLC（AI-Driven Life Cycle）ドキュメントと実装コードの一貫性を確認し、ドメインモデル違反を早期に検出します。

## 入力形式

スキル呼び出し時に検証対象を指定できます:

```
/ddd-check
```

または特定のファイル/ディレクトリのみ検証:

```
/ddd-check --domain-only
/ddd-check --file src/domain/entities/cart.py
```

## 実行プロセス

### ステップ1: ユビキタス言語の整合性チェック

**検証内容**:
- `aidlc-docs/construction/unit_01_ai_dialog_public/docs/ubiquitous_language.md` で定義された用語がコード内で正しく使用されているか

**確認ファイル**:
```bash
# ユビキタス言語定義を読む
main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/ubiquitous_language.md

# コードで使用されている用語を確認
main/backend/src/domain/**/*.py
```

**チェック項目**:

#### 1. コアドメイン用語の使用

| 日本語 | 英語 | コード内での使用例 |
|--------|------|-------------------|
| 買い目 | BetSelection | `class BetSelection` (値オブジェクト) |
| カート | Cart | `class Cart` (エンティティ) |
| カートアイテム | CartItem | `class CartItem` (エンティティ) |
| 相談セッション | ConsultationSession | `class ConsultationSession` (集約ルート) |
| メッセージ | Message | `class Message` (エンティティ) |
| データフィードバック | DataFeedback | `class DataFeedback` (値オブジェクト) |
| 掛け金フィードバック | AmountFeedback | `class AmountFeedback` (値オブジェクト) |

**検証方法**:
```bash
# 用語が正しく使用されているか確認
grep -r "class BetSelection" main/backend/src/domain/value_objects/
grep -r "class Cart" main/backend/src/domain/entities/
```

**違反パターン**:
- ❌ `BettingSelection` (誤った用語)
- ❌ `ShoppingCart` (別ドメインの用語混入)
- ❌ `OrderItem` (ECサイトの用語混入)

#### 2. サポートドメイン用語の使用

| 日本語 | 英語 | 扱い |
|--------|------|------|
| レース | Race | 外部データ（Read Model） |
| 開催場 | Venue | 外部データ |
| 出走馬 | Runner | 外部データ |
| 騎手 | Jockey | 外部データ |
| オッズ | Odds | 外部データ |

**検証方法**:
- サポートドメインの概念はポート（`RaceDataProvider`）経由でのみ取得
- ドメインエンティティとして内部実装してはいけない

**違反パターン**:
- ❌ `class Race(Entity)` をドメイン層に実装
- ❌ `Race` クラスにビジネスロジックを追加

### ステップ2: レイヤー分離の検証

**ディレクトリ構造チェック**:
```
main/backend/src/
├── domain/              # ドメイン層（ビジネスロジック）
│   ├── entities/        # エンティティ（識別子を持つ）
│   ├── value_objects/   # 値オブジェクト（イミュータブル）
│   ├── services/        # ドメインサービス
│   ├── ports/           # インターフェース（ポート）
│   ├── identifiers/     # 識別子（ID型）
│   └── enums/           # 列挙型
├── application/         # アプリケーション層（ユースケース）
│   └── use_cases/
├── infrastructure/      # インフラ層（外部システム連携）
│   ├── providers/       # プロバイダー（アダプター）
│   └── repositories/
└── api/                 # API層（Lambda ハンドラー）
    └── handlers/
```

**検証ルール**:

#### 依存関係の方向

```
API層 → アプリケーション層 → ドメイン層 ← インフラ層
```

**許可される依存**:
- ✅ API層 → アプリケーション層
- ✅ アプリケーション層 → ドメイン層
- ✅ インフラ層 → ドメイン層（ポート実装）

**禁止される依存**:
- ❌ ドメイン層 → インフラ層
- ❌ ドメイン層 → API層
- ❌ アプリケーション層 → インフラ層（直接依存）

**検証方法**:
```bash
# ドメイン層がインフラ層をインポートしていないか確認
grep -r "from src.infrastructure" main/backend/src/domain/
# → 何も見つからないはず

# ドメイン層がAPI層をインポートしていないか確認
grep -r "from src.api" main/backend/src/domain/
# → 何も見つからないはず
```

### ステップ3: エンティティと値オブジェクトの検証

#### エンティティのルール

**必須条件**:
1. 識別子（ID）を持つ
2. ライフサイクルがある（生成→更新→削除）
3. 同一性は識別子で判断（`__eq__` の実装）

**検証パターン**:
```python
@dataclass
class Cart:
    """カートエンティティ."""

    cart_id: CartId  # ✅ 識別子を持つ
    items: list[CartItem]  # ✅ 可変な状態

    def add_item(self, item: CartItem) -> None:
        """アイテムを追加."""  # ✅ 振る舞いを持つ
        self.items.append(item)
```

**違反パターン**:
```python
# ❌ frozen=True はエンティティに使わない（値オブジェクト用）
@dataclass(frozen=True)
class Cart:
    cart_id: CartId
    items: list[CartItem]
```

#### 値オブジェクトのルール

**必須条件**:
1. イミュータブル（`frozen=True`）
2. 識別子を持たない
3. 等価性は値で判断

**検証パターン**:
```python
@dataclass(frozen=True)
class BetSelection:
    """買い目（値オブジェクト）."""

    bet_type: BetType
    horse_numbers: HorseNumbers
    amount: Money

    # ✅ 振る舞いは新しいインスタンスを返す
    def change_amount(self, new_amount: Money) -> "BetSelection":
        return BetSelection(
            bet_type=self.bet_type,
            horse_numbers=self.horse_numbers,
            amount=new_amount,
        )
```

**違反パターン**:
```python
# ❌ frozen=True がない
@dataclass
class BetSelection:
    bet_type: BetType
    horse_numbers: HorseNumbers
    amount: Money

# ❌ 値オブジェクトが識別子を持つ
@dataclass(frozen=True)
class BetSelection:
    selection_id: str  # ❌ 識別子は不要
    bet_type: BetType
```

### ステップ4: 集約の境界検証

**集約のルール**:
1. 集約ルートを通じてのみ内部エンティティにアクセス
2. トランザクション境界 = 集約境界
3. 集約間の参照は識別子のみ

**検証例**:

#### 正しい集約設計

```python
@dataclass
class ConsultationSession:
    """相談セッション（集約ルート）."""

    session_id: SessionId  # 識別子
    user_id: UserId
    messages: list[Message]  # 内部エンティティ

    def add_message(self, message: Message) -> None:
        """メッセージを追加."""  # ✅ 集約ルート経由
        self.messages.append(message)
```

**違反パターン**:
```python
# ❌ 集約を越えた直接参照
@dataclass
class Message:
    message_id: MessageId
    consultation_session: ConsultationSession  # ❌ 集約全体を参照
```

**正しいパターン**:
```python
# ✅ 識別子のみで参照
@dataclass
class Message:
    message_id: MessageId
    session_id: SessionId  # ✅ 識別子のみ
```

### ステップ5: ドメインサービスの検証

**ドメインサービスの条件**:
1. ステートレス（状態を持たない）
2. 複数のエンティティにまたがるロジック
3. エンティティや値オブジェクトに置けないロジック

**検証パターン**:
```python
class FeedbackGenerator:
    """フィードバック生成ドメインサービス."""

    def __init__(self, ai_client: AiClient) -> None:
        self._ai_client = ai_client  # ✅ 依存性注入

    def generate_feedback(
        self,
        bet_selection: BetSelection,
        race_data: RaceData,
        runner_data: list[RunnerData],
    ) -> DataFeedback:
        """買い目のフィードバックを生成."""
        # ✅ 複数のドメインオブジェクトを使用するロジック
        ...
```

**違反パターン**:
```python
# ❌ 状態を持つドメインサービス
class FeedbackGenerator:
    def __init__(self) -> None:
        self._cache: dict = {}  # ❌ 状態を持つ

# ❌ エンティティに置けるロジックをサービスに配置
class CartService:
    def add_item(self, cart: Cart, item: CartItem) -> None:
        cart.items.append(item)  # ❌ これはCartエンティティのメソッドにすべき
```

### ステップ6: ポート・アダプターパターンの検証

**ポート（インターフェース）の検証**:

```python
# ✅ 正しいポート定義
class RaceDataProvider(ABC):
    """レースデータ取得インターフェース."""

    @abstractmethod
    def get_race(self, race_id: RaceId) -> RaceData | None:
        pass  # ✅ インターフェースのみ

# ✅ 正しいアダプター実装
class JraVanRaceDataProvider(RaceDataProvider):
    """JRA-VAN からデータ取得."""

    def get_race(self, race_id: RaceId) -> RaceData | None:
        # 外部API呼び出し
        ...
```

**違反パターン**:
```python
# ❌ ポートに実装を含む
class RaceDataProvider(ABC):
    def get_race(self, race_id: RaceId) -> RaceData | None:
        # ❌ デフォルト実装を含む
        return None
```

## 出力形式

### 全チェック通過時

```
✅ DDD設計原則チェック完了

検証項目:
- [✅] ユビキタス言語の整合性
- [✅] レイヤー分離
- [✅] エンティティと値オブジェクトの区別
- [✅] 集約の境界
- [✅] ドメインサービスの適切性
- [✅] ポート・アダプターパターン

🎉 DDD原則に従った実装がなされています。
```

### 違反検出時

```
🔴 DDD設計原則違反を検出

検証項目:
- [✅] ユビキタス言語の整合性
- [🔴] レイヤー分離 - 1件の違反
- [✅] エンティティと値オブジェクトの区別
- [⚠️] 集約の境界 - 1件の警告
- [✅] ドメインサービスの適切性
- [✅] ポート・アダクターパターン

---
🔴 違反 #1: レイヤー依存関係違反

ファイル: src/domain/entities/cart.py:15
違反内容: ドメイン層がインフラ層をインポート

コード:
```python
from src.infrastructure.repositories import CartRepository  # ❌
```

理由: ドメイン層はインフラ層に依存してはいけない

修正案:
1. CartRepository をポート（インターフェース）として domain/ports/ に定義
2. domain層では CartRepository ポートを使用
3. infrastructure層で CartRepository を実装

---
⚠️ 警告 #1: 集約の境界が曖昧

ファイル: src/domain/entities/message.py:10
警告内容: 集約を越えた直接参照

コード:
```python
consultation_session: ConsultationSession  # ⚠️
```

理由: 集約間の参照は識別子のみが推奨

推奨修正:
```python
session_id: SessionId  # ✅ 識別子のみで参照
```

---

次のアクション:
- [ ] 違反の修正
- [ ] 警告の確認（必要に応じて修正）
- [ ] 再検証: /ddd-check
```

## 参照ドキュメント

### AIDLC ドキュメント

- **ユビキタス言語**: `main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/ubiquitous_language.md`
- **エンティティ**: `main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/entities.md`
- **値オブジェクト**: `main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/value_objects.md`
- **集約**: `main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/aggregates.md`
- **ドメインサービス**: `main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/domain_services.md`
- **アーキテクチャ**: `main/aidlc-docs/construction/unit_01_ai_dialog_public/docs/architecture.md`

### 実装コード

- **ドメイン層**: `main/backend/src/domain/`
- **アプリケーション層**: `main/backend/src/application/`
- **インフラ層**: `main/backend/src/infrastructure/`
- **API層**: `main/backend/src/api/`

## 注意事項

- **ユビキタス言語**: ドキュメントとコードで用語を統一
- **レイヤー分離**: ドメイン層は外部に依存しない
- **イミュータブル**: 値オブジェクトは必ず `frozen=True`
- **集約境界**: トランザクション境界を意識
- **ポート・アダプター**: 外部依存はインターフェース経由
