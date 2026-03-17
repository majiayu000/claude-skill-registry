---
name: tdd-wada-style
description: t.wada流TDD（テスト駆動開発）。新機能実装、バグ修正、リファクタリング時に自動適用。Red-Green-Refactorサイクル、AAA構造、振る舞いテストの原則に従う。テストを書く、テストファーストで実装する、テストコードをレビューする際に使用。
---

# t.wada流 TDD（テスト駆動開発）

和田卓人氏のTDD哲学に基づき、高品質なテスト駆動開発を実践する。

## Core Philosophy（中核思想）

> 「テストとは、動くことを証明するものではない。間違いを見つけるためのものだ。」
> — t.wada

### 3つの原則

1. **テストは設計行為** — テストを書くことで、使いやすいAPIを設計する
2. **テストは仕様書** — テストコードが最も正確なドキュメントである
3. **小さく回す** — Red → Green → Refactor を短いサイクルで繰り返す

## TDD Cycle（Red-Green-Refactor）

```
🔴 RED      → 失敗するテストを先に書く
     ↓
🟢 GREEN    → 最小限のコードでテストを通す
     ↓
🔵 REFACTOR → テストが通ったまま設計を改善
     ↓
   （繰り返し）
```

## Instructions

### Step 1: 要件を振る舞いで分解

実装前に「〜したとき、〜となる」形式でテストケースをリストアップする。

```markdown
テストケースリスト:
□ 空のリストを渡すと空のリストを返す
□ 1要素のリストはそのまま返す
□ 複数要素は昇順でソートされる
□ 負の数を含んでも正しくソートされる
```

最も単純なケースから始める。

### Step 2: テスト構造（AAA パターン）

すべてのテストは Arrange-Act-Assert の3フェーズで構成する。

```python
def test_振る舞いを日本語で記述():
    # Arrange（準備）
    sut = TargetClass()
    input_data = create_test_data()

    # Act（実行）
    result = sut.target_method(input_data)

    # Assert（検証）
    assert result == expected_value
```

**ポイント:**
- テスト名は日本語で振る舞いを明確に記述
- 1テスト1アサーション（原則）
- 3つのブロックを空行で明確に分離

### Step 3: 境界値と異常系

必ず以下をカバーする:

```python
# 境界値テスト
def test_空入力():
    assert func([]) == []

def test_単一要素():
    assert func([1]) == [1]

def test_最大値():
    assert func([MAX_VALUE]) == expected

def test_最大値プラス1で例外():
    with pytest.raises(ValueError):
        func([MAX_VALUE + 1])

# 異常系テスト
def test_None入力で例外():
    with pytest.raises(TypeError):
        func(None)

def test_不正な型で例外():
    with pytest.raises(TypeError):
        func("not a list")
```

### Step 4: Refactor（リファクタリング）

テストがグリーンの状態を維持しながら:
- 重複の除去
- 命名の改善
- 責務の分離

**ルール:** 振る舞いを変えずに構造を改善する

## Anti-Patterns（避けるべきパターン）

### ❌ 実装詳細のテスト

```python
# Bad: 内部状態に依存
assert obj._internal_cache == {...}
assert obj._call_count == 3

# Good: 振る舞いをテスト
assert obj.get_result() == expected
```

### ❌ テスト間の依存

```python
# Bad: 前のテストの状態に依存
class TestCounter:
    counter = Counter()  # 共有状態

    def test_1(self):
        self.counter.increment()

    def test_2(self):
        assert self.counter.value == 1  # test_1に依存

# Good: 各テストが独立
def test_increment():
    counter = Counter()
    counter.increment()
    assert counter.value == 1
```

### ❌ 過度なモック

```python
# Bad: すべてをモック化（何もテストしていない）
@patch('module.ClassA')
@patch('module.ClassB')
@patch('module.ClassC')
def test_something(mock_a, mock_b, mock_c):
    ...

# Good: 外部境界のみモック化
@patch('module.external_api_client')
def test_something(mock_api):
    ...
```

### ❌ 巨大なテスト

```python
# Bad: 1テストで複数の振る舞い
def test_user_registration():
    # 50行のテストコード...
    assert user.email == ...
    assert user.created_at == ...
    assert email_sent == True
    assert db.users.count() == ...

# Good: 1テスト1振る舞い
def test_ユーザー登録でメールアドレスが保存される():
    ...

def test_ユーザー登録で確認メールが送信される():
    ...
```

## Test Template

新しいテストファイルを作成する際のテンプレート:

```python
"""
{モジュール名}のテスト

テスト対象: {クラス名/関数名}
"""
import pytest
from src.module import TargetClass


class Test{TargetClass}:
    """TargetClassの振る舞いテスト"""

    # ========== 正常系 ==========

    def test_基本的な使用方法(self):
        """最も一般的なユースケース"""
        # Arrange
        sut = TargetClass()

        # Act
        result = sut.do_something("input")

        # Assert
        assert result == "expected"

    # ========== 境界値 ==========

    def test_空入力(self):
        """空の入力を処理できる"""
        sut = TargetClass()
        result = sut.do_something("")
        assert result == ""

    def test_最大長入力(self):
        """最大長の入力を処理できる"""
        sut = TargetClass()
        result = sut.do_something("x" * MAX_LENGTH)
        assert len(result) <= MAX_LENGTH

    # ========== 異常系 ==========

    def test_None入力で例外(self):
        """Noneを渡すとTypeErrorが発生"""
        sut = TargetClass()
        with pytest.raises(TypeError):
            sut.do_something(None)

    def test_不正な入力でValueError(self):
        """不正な入力はValueErrorを発生"""
        sut = TargetClass()
        with pytest.raises(ValueError) as exc_info:
            sut.do_something("invalid")
        assert "不正な入力" in str(exc_info.value)
```

## Checklist

実装完了時の確認項目:

- [ ] すべてのテストがパス
- [ ] 各テストが独立して実行可能
- [ ] テスト名から振る舞いが理解できる
- [ ] AAA構造が明確
- [ ] 境界値がカバーされている
- [ ] 異常系がカバーされている
- [ ] 実装詳細ではなく振る舞いをテスト
- [ ] 過度なモックを使用していない

## References

追加のガイダンスは以下を参照:
- [EXAMPLES.md](EXAMPLES.md) - 具体的なテストパターン例
- [PATTERNS.md](PATTERNS.md) - よくあるテストパターン集
