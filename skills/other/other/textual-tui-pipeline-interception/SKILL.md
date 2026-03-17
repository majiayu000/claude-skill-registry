---
name: textual-tui-pipeline-interception
description: "Use when adding an interactive review/approval step to a CLI pipeline using Textual TUI with immutable state."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-10"
---

# Textual TUI Pipeline Interception
# Textual TUI パイプライン挿入パターン

**Extracted / 抽出日:** 2026-02-10
**Context / コンテキスト:** CLI パイプラインに対話的レビュー/承認ステップを Textual で挿入するパターン

---

## Problem / 課題

CLIツールのパイプラインは `生成 → 出力` と直結しがち。ユーザーが結果を確認・編集してから出力したい場合、パイプライン途中に対話ステップを挿入する必要がある。

課題:
- 既存パイプラインを壊さずに TUI を挿入したい
- TUI の状態管理を不変にしたい（frozen dataclass パターンとの一貫性）
- Textual の非同期 UI と同期 CLI パイプラインを統合したい
- テスト可能にしたい（Textual Pilot API）

---

## Solution / 解決策

### 1. パイプライン挿入パターン

TUI を `生成 → [レビュー] → 出力` の間に挿入。`launch_review()` は同じ型を受け取り返す。

```python
# main.py — 挿入ポイント
result = generate(input_data)  # 既存処理

# NEW: --review フラグ時のみ TUI 起動
if review and result.items:
    from myapp.tui import launch_review
    result = launch_review(result)  # 同じ型 in/out

write_output(result)  # 既存処理（変更不要）
```

### 2. 不変状態モデル

TUI 状態を frozen dataclass で管理。状態変更は純粋関数。

```python
from dataclasses import dataclass
from enum import StrEnum

class ItemStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

@dataclass(frozen=True)
class ReviewItem:
    """レビュー対象アイテム。不変。"""
    data: MyModel           # 元データ (Pydantic frozen)
    original_index: int
    status: ItemStatus = ItemStatus.PENDING

@dataclass(frozen=True)
class ReviewState:
    """レビューセッション全体の不変状態。"""
    items: tuple[ReviewItem, ...]
    current_index: int = 0
    filter_status: ItemStatus | None = None  # None = 全件

    @property
    def stats(self) -> dict[str, int]:
        return {s.value: sum(1 for i in self.items if i.status == s) for s in ItemStatus}

    def filtered_items(self) -> list[ReviewItem]:
        if self.filter_status is None:
            return list(self.items)
        return [i for i in self.items if i.status == self.filter_status]
```

### 3. 純粋関数で状態変更

```python
def set_item_status(state: ReviewState, idx: int, status: ItemStatus) -> ReviewState:
    """ステータスを変更した新 ReviewState を返す。元は不変。"""
    items = list(state.items)
    old = items[idx]
    items[idx] = ReviewItem(
        data=old.data, original_index=old.original_index,
        status=status,
    )
    return ReviewState(
        items=tuple(items),
        current_index=state.current_index,
        filter_status=state.filter_status,
    )

def edit_item(state: ReviewState, idx: int, **updates: Any) -> ReviewState:
    """Pydantic model_copy でアイテムデータを編集。"""
    items = list(state.items)
    old = items[idx]
    new_data = old.data.model_copy(update=updates)  # Pydantic frozen
    items[idx] = ReviewItem(data=new_data, original_index=old.original_index, status=old.status)
    return ReviewState(items=tuple(items), current_index=state.current_index, filter_status=state.filter_status)

def navigate(state: ReviewState, delta: int) -> ReviewState:
    """循環ナビゲーション。"""
    filtered = state.filtered_items()
    if not filtered:
        return state
    new_idx = (state.current_index + delta) % len(filtered)
    return ReviewState(items=state.items, current_index=new_idx, filter_status=state.filter_status)
```

### 4. Textual App パターン

```python
from textual.app import App
from textual.binding import Binding

class ReviewApp(App[None]):
    BINDINGS = [
        Binding("a", "accept", "Accept"),
        Binding("r", "reject", "Reject"),
        Binding("e", "edit", "Edit"),
        Binding("n", "next", "Next"),
        Binding("s", "save_quit", "Save"),
        Binding("q", "quit_app", "Quit"),
    ]

    def __init__(self, initial_state: ReviewState) -> None:
        self.state = initial_state
        self.save_requested = False
        super().__init__()

    # 状態更新パターン: state 置換 → UI リフレッシュ
    def action_accept(self) -> None:
        idx = self._current_original_index()
        self.state = set_item_status(self.state, idx, ItemStatus.ACCEPTED)
        self.state = navigate(self.state, +1)
        self._refresh_ui()

    def action_save_quit(self) -> None:
        self.save_requested = True
        self.exit()

    def _refresh_ui(self) -> None:
        """全ウィジェットを現在の state で更新。"""
        self.query_one(StatsBar).update_stats(self.state.stats)
        self.query_one(ItemDisplay).show(self.state.current_item)
```

### 5. 公開 API（同じ型 in/out）

```python
def launch_review(result: MyResult) -> MyResult:
    """TUI を起動し、承認済みアイテムのみ含む Result を返す。"""
    state = create_initial_state(result.items)
    app = ReviewApp(state)
    app.run()  # ブロッキング（Textual が内部で async 処理）

    if not app.save_requested:
        return result  # 保存せず終了 → 元データそのまま

    accepted = [item.data for item in app.state.items if item.status == ItemStatus.ACCEPTED]
    return result.model_copy(update={"items": accepted})
```

### 6. Textual Pilot テスト

```python
import pytest

@pytest.mark.asyncio
async def test_accept_card():
    state = create_initial_state(sample_items)
    app = ReviewApp(state)
    async with app.run_test() as pilot:
        await pilot.press("a")
        assert app.state.items[0].status == ItemStatus.ACCEPTED

async def test_save_exits_app():
    app = ReviewApp(create_initial_state(sample_items))
    async with app.run_test() as pilot:
        await pilot.press("s")
        assert app.save_requested is True
```

---

## Key Design Choices / 設計上のポイント

| 選択 | 理由 |
|------|------|
| `launch_review()` が同じ型を返す | パイプラインに透過的に挿入可能 |
| frozen dataclass + 純粋関数 | 既存コードベースの不変性パターンと一貫 |
| `self.state = new_state` パターン | Textual では reactive よりシンプル |
| `_refresh_ui()` を毎回呼ぶ | 明示的 UI 更新で挙動が予測可能 |
| `save_requested` フラグ | quit vs save を区別 |
| CSS インライン | 小規模 TUI では `.tcss` ファイル管理不要 |

---

## When to Use / 使用すべき場面

- CLI ツールに対話的レビュー/承認ステップを追加したい
- 生成結果（LLM出力、変換結果等）をユーザーが確認してから出力したい
- Accept/Reject/Edit のワークフローが必要
- 既存の不変データモデル（Pydantic frozen, frozen dataclass）と統合したい

---

## When NOT to Use / 使用すべきでない場面

- 単純な yes/no 確認（`typer.confirm()` で十分）
- Web UI が必要な場合（Textual はターミナル専用）
- リアルタイムデータストリーム（Textual は静的データのレビュー向き）

---

## Related Patterns / 関連パターン

- `python-immutable-accumulator.md` — 不変蓄積の基本パターン
- `backward-compatible-frozen-extension.md` — frozen モデルの後方互換拡張
- `cost-aware-llm-pipeline.md` — `process → [review] → write` パイプラインの元パターン
