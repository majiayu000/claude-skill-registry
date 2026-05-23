---
name: stress-test-flow
description: 実装完了後のマルチ視点ストレステストフロー。複数の検証エージェントが並列で品質を検証し、コード生成なしで問題を検出
---

# ストレステストフロー

> **目的**: 実装完了後、複数の視点から品質を検証。
> **Token最適化**: 検証エージェントはコードを生成せず、読み取り・報告のみ。

---

## 1. 概要

### 1.1 ストレステストとは

通常のレビューに加え、**複数の専門エージェントが並列で**実装を検証するプロセス。
各エージェントは**コードを生成せず**、問題の検出と報告のみを行う。

```
実装完了
   ↓
品質レビュー（9点以上）
   ↓
ストレステスト（並列）
├── security-tester: セキュリティ脆弱性チェック
├── performance-tester: パフォーマンス問題チェック
├── edge-case-tester: 境界条件・エッジケースチェック
└── integration-tester: 統合・互換性チェック
   ↓
統合レポート
   ↓
PR作成 or 修正
```

### 1.2 Token効率

| 役割 | Token消費 | 理由 |
|------|-----------|------|
| **メイン実装エージェント** | 高 | コード生成 |
| **ストレステスター** | **低** | 読み取り・報告のみ |
| **品質レビュアー** | 中 | 評価・スコアリング |

**効果**: 1つのエージェントが全視点をカバーするより、専門テスターが並列実行する方が**総Token消費が少ない**。

---

## 2. ストレステスター定義

### 2.1 セキュリティテスター

```python
SECURITY_TESTER_PROMPT = """
## ロール
セキュリティ専門の検証エージェント。コード生成禁止、問題検出のみ。

## チェック項目
1. SQLインジェクション脆弱性
2. XSS脆弱性
3. 認証・認可バイパス
4. 機密情報のハードコード
5. 安全でない暗号化
6. CSRF対策の欠如
7. パストラバーサル
8. コマンドインジェクション

## 出力形式（JSON）
{
  "severity": "critical|high|medium|low|none",
  "findings": [
    {
      "type": "脆弱性タイプ",
      "file": "ファイルパス",
      "line": 行番号,
      "description": "問題の説明",
      "recommendation": "推奨対策"
    }
  ],
  "overall_assessment": "概要評価"
}

## ⛔ 禁止事項
- コードの修正・生成
- 実装の提案（recommendationは抽象的に）
"""
```

### 2.2 パフォーマンステスター

```python
PERFORMANCE_TESTER_PROMPT = """
## ロール
パフォーマンス専門の検証エージェント。コード生成禁止、問題検出のみ。

## チェック項目
1. N+1クエリ問題
2. 不要なループ・再帰
3. メモリリーク可能性
4. 非効率なアルゴリズム（O(n²)以上）
5. 不要な同期処理
6. キャッシュ未使用
7. 大量データの一括読み込み
8. 不要な再レンダリング（フロントエンド）

## 出力形式（JSON）
{
  "severity": "critical|high|medium|low|none",
  "findings": [
    {
      "type": "問題タイプ",
      "file": "ファイルパス",
      "line": 行番号,
      "description": "問題の説明",
      "impact": "想定される影響"
    }
  ],
  "overall_assessment": "概要評価"
}

## ⛔ 禁止事項
- コードの修正・生成
- 具体的な実装提案
"""
```

### 2.3 エッジケーステスター

```python
EDGE_CASE_TESTER_PROMPT = """
## ロール
境界条件・エッジケース専門の検証エージェント。コード生成禁止、問題検出のみ。

## チェック項目
1. null/undefined/None の未処理
2. 空配列・空文字列の未処理
3. 最大値・最小値の境界
4. 負数の未処理
5. 非ASCII文字（絵文字、特殊文字）
6. タイムゾーン・日付境界
7. 並行アクセス競合
8. ネットワーク障害時の動作

## 出力形式（JSON）
{
  "severity": "critical|high|medium|low|none",
  "findings": [
    {
      "type": "エッジケースタイプ",
      "file": "ファイルパス",
      "line": 行番号,
      "description": "未処理のケース",
      "test_scenario": "テストシナリオ例"
    }
  ],
  "overall_assessment": "概要評価"
}

## ⛔ 禁止事項
- コードの修正・生成
- テストコードの生成
"""
```

### 2.4 統合テスター

```python
INTEGRATION_TESTER_PROMPT = """
## ロール
統合・互換性専門の検証エージェント。コード生成禁止、問題検出のみ。

## チェック項目
1. API契約の違反
2. 型の不整合
3. 依存関係の循環
4. 破壊的変更
5. 後方互換性の欠如
6. 設計書との乖離
7. 既存コードとの整合性
8. 環境依存コード

## 出力形式（JSON）
{
  "severity": "critical|high|medium|low|none",
  "findings": [
    {
      "type": "問題タイプ",
      "file": "ファイルパス",
      "line": 行番号,
      "description": "問題の説明",
      "affected_components": ["影響を受けるコンポーネント"]
    }
  ],
  "overall_assessment": "概要評価"
}

## ⛔ 禁止事項
- コードの修正・生成
- 具体的な実装提案
"""
```

---

## 3. 実行フロー

### 3.1 ストレステスト呼び出し

```python
def run_stress_tests(env_id: str, impl_files: list[str]) -> StressTestResult:
    """ストレステストを並列実行"""
    
    # 実装ファイルの内容を取得
    file_contents = {}
    for file_path in impl_files:
        content = container_use_environment_file_read(
            environment_id=env_id,
            target_file=file_path,
            should_read_entire_file=True
        )
        file_contents[file_path] = content
    
    # 並列でストレステスト実行
    results = []
    
    # 並列タスク起動
    tasks = [
        background_task(
            agent="oracle",  # 汎用分析エージェント
            description="Security stress test",
            prompt=f"{SECURITY_TESTER_PROMPT}\n\n## 対象ファイル\n{json.dumps(file_contents)}"
        ),
        background_task(
            agent="oracle",
            description="Performance stress test",
            prompt=f"{PERFORMANCE_TESTER_PROMPT}\n\n## 対象ファイル\n{json.dumps(file_contents)}"
        ),
        background_task(
            agent="oracle",
            description="Edge case stress test",
            prompt=f"{EDGE_CASE_TESTER_PROMPT}\n\n## 対象ファイル\n{json.dumps(file_contents)}"
        ),
        background_task(
            agent="oracle",
            description="Integration stress test",
            prompt=f"{INTEGRATION_TESTER_PROMPT}\n\n## 対象ファイル\n{json.dumps(file_contents)}"
        ),
    ]
    
    # 結果収集
    for task_id in tasks:
        result = background_output(task_id=task_id, block=True)
        results.append(json.loads(result))
    
    return aggregate_results(results)
```

### 3.2 結果集約

```python
def aggregate_results(results: list[dict]) -> StressTestResult:
    """ストレステスト結果を集約"""
    
    all_findings = []
    max_severity = "none"
    severity_order = ["none", "low", "medium", "high", "critical"]
    
    for result in results:
        all_findings.extend(result.get("findings", []))
        if severity_order.index(result["severity"]) > severity_order.index(max_severity):
            max_severity = result["severity"]
    
    return StressTestResult(
        passed=max_severity in ["none", "low"],
        max_severity=max_severity,
        total_findings=len(all_findings),
        findings=all_findings,
        summary=generate_summary(all_findings)
    )
```

---

## 4. 判定基準

| 最大重大度 | アクション |
|-----------|----------|
| **none** | ✅ PR作成へ |
| **low** | ✅ PR作成へ（警告付き） |
| **medium** | ⚠️ 修正推奨、ユーザー判断 |
| **high** | ❌ 修正必須 |
| **critical** | ❌ 即時修正必須 |

---

## 5. ストレステストレポート

```markdown
## 🔬 ストレステストレポート

### サマリ
- **総合判定**: ✅ PASSED / ❌ FAILED
- **最大重大度**: {max_severity}
- **検出件数**: {total_findings}件

### カテゴリ別結果

| カテゴリ | 重大度 | 検出件数 |
|---------|--------|---------|
| セキュリティ | {severity} | {count}件 |
| パフォーマンス | {severity} | {count}件 |
| エッジケース | {severity} | {count}件 |
| 統合 | {severity} | {count}件 |

### 検出事項（重大度順）

{findings_list}

### 推奨アクション

{recommendations}
```

---

## 6. 使用タイミング

| 状況 | ストレステスト |
|------|--------------|
| 通常のSubtask実装 | 任意（品質レビュー9点以上で十分） |
| 重要な機能（認証、決済等） | **必須** |
| 外部API連携 | **必須** |
| パフォーマンスクリティカル | **必須** |
| セキュリティクリティカル | **必須** |
| リファクタリング | 推奨 |

---

## 7. Token効率の比較

| 方式 | Token消費 | 品質 |
|------|-----------|------|
| 単一エージェントで全チェック | 高（5000-10000） | 中（網羅性に限界） |
| **並列ストレステスト** | **中（2000-4000）** | **高（専門性×並列）** |

**効果**: 専門テスターは「読み取り・報告のみ」のためToken効率が高い。

---

## 変更履歴

| 日付 | バージョン | 変更内容 |
|:---|:---|:---|
| 2026-01-10 | 1.0.0 | 初版作成（ai-framework stress.sh からの着想） |
