---
name: constitution-checker
description: プロジェクト憲法への準拠を検証します。実装完了時やPR作成時に全Articleをチェックし、違反がないことを確認します。
allowed-tools: Read Glob Grep Bash
---

# Constitution Checker スキル

このスキルは、`.specify/memory/constitution.md` で定義されたプロジェクト憲法への準拠を検証します。

## 起動条件

以下の状況で起動します：

1. **実装完了時**: 機能実装が完了し、コミット前にチェックが必要な場合
2. **PR作成前**: プルリクエストを作成する前の最終チェック
3. **コードレビュー時**: 他者のコードをレビューする際
4. **明示的な依頼**: ユーザーが憲法準拠チェックを依頼した場合

## チェック項目

### 非交渉的原則（例外なし）

#### Article 1: Test-First Imperative

- [ ] テストファイルが実装ファイルより先に作成されているか
- [ ] テストファイルと実装ファイルが1:1で対応しているか
- [ ] テストが失敗状態（Red）から開始されているか

```bash
# テストファイルの存在確認
uv run pytest --collect-only
```

#### Article 5: Code Quality Standards

- [ ] ruff check がエラーなしで通過するか
- [ ] ruff format で差分が発生しないか
- [ ] mypy がエラーなしで通過するか

```bash
# 品質チェックの実行
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

#### Article 6: Data Accuracy Mandate

- [ ] マジックナンバーが直接埋め込まれていないか
- [ ] ハードコードされた文字列がないか
- [ ] 暗黙的なフォールバック（`= "default"` 等）がないか

```bash
# ハードコード検出（ヒューリスティック）
grep -rn "= 30\|= 60\|= 100" --include="*.py" src/
grep -rn '= "default"\|= "none"' --include="*.py" src/
```

#### Article 7: DRY Principle

- [ ] 同一ロジックが複数箇所に存在しないか
- [ ] 類似コードが3回以上繰り返されていないか

#### Article 9: Python Type Safety Mandate

- [ ] すべての関数に型アノテーションがあるか
- [ ] 戻り値に型アノテーションがあるか
- [ ] `Any` 型の使用が最小限か

```bash
# 型アノテーションなし関数の検出
grep -rn "def .*(" --include="*.py" src/ | grep -v ":"
```

#### Article 11: SpecKit Naming Convention

- [ ] ディレクトリ名が `<3桁番号>-<name>` 形式か
- [ ] ブランチ名が同一の命名規則に従っているか

### 推奨チェック項目

#### Article 2: Documentation Integrity

- [ ] 実装が仕様と一致しているか
- [ ] ドキュメントが最新の状態か

#### Article 3: MCP Protocol Compliance

- [ ] MCPツールにスキーマ定義があるか
- [ ] 入力がPydanticモデルで検証されているか
- [ ] エラーレスポンスが適切な形式か

#### Article 10: Python Docstring Standards

- [ ] 公開関数にdocstringがあるか
- [ ] Google-style形式を使用しているか

## 実行プロセス

### 1. 自動チェック実行

```bash
# 全品質チェック
uv run ruff check --fix . && uv run ruff format . && uv run mypy .

# テスト実行
uv run pytest
```

### 2. 手動チェック項目の確認

自動化できない項目を目視確認：
- コードの重複
- 仕様との整合性
- 適切な抽象化

### 3. レポート生成

チェック結果を以下の形式で報告：

```
## Constitution Compliance Report

### 非交渉的原則
- [✓] Article 1: Test-First Imperative
- [✓] Article 5: Code Quality Standards
- [✓] Article 6: Data Accuracy Mandate
- [✓] Article 7: DRY Principle
- [✓] Article 9: Python Type Safety Mandate
- [✓] Article 11: SpecKit Naming Convention

### 推奨項目
- [✓] Article 2: Documentation Integrity
- [✓] Article 3: MCP Protocol Compliance
- [✓] Article 10: Python Docstring Standards

### 総合判定: PASS / FAIL
```

## 違反検出時の対応

1. **作業を停止**: 違反が解消されるまで次工程に進まない
2. **違反内容を報告**: 具体的な違反箇所と修正方法を提示
3. **修正を支援**: 必要に応じて修正コードを提案
4. **再チェック**: 修正後に再度チェックを実行

## 注意事項

- 非交渉的原則（Article 1, 5, 6, 7, 9, 11）は例外なく遵守が必要
- 時間制約、緊急性を理由とした例外は認められない
- すべてのチェック項目がPASSするまでコミット・PRは行わない
