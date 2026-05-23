---
name: quantization-evaluation-pipeline
description: Execute GGUF quantization with imatrix protection, perform statistical benchmark evaluation with error bars, generate academic-style methodology documentation, and create comprehensive scorecards. Use when evaluating model quantization quality, comparing quantization methods, or generating publication-ready evaluation results with subagent execution and PowerShell progress visualization.
---

# GGUF量子化評価パイプライン

## 概要

このスキルは、GGUF量子化におけるimatrix保護を使用した高度な評価パイプラインを実行します。統計的ベンチマーク評価、エラーバー付きグラフ生成、学術文献形式の手法記述、そしてサブエージェントによる実行とPowerShell進捗可視化を提供します。

## 主な機能

### 1. GGUF量子化 with imatrix保護
- imatrixデータ収集と重要度ベース量子化
- BF16/Q8_0/Q4_K_Mなどの量子化形式対応
- 量子化劣化の最小化

### 2. 統計的ベンチマーク評価
- GSM8K, MATH, ARC-Challenge, ELYZA Tasks 100
- 複数回実行による統計的信頼性確保
- エラーバー付き性能グラフ生成

### 3. 学術文献形式ドキュメント
- 手法の詳細な記述
- 実験設定と結果の体系的整理
- 出版-readyなフォーマット

### 4. サブエージェント実行
- 並列処理による効率化
- リアルタイム進捗監視
- エラー回復機能

### 5. PowerShell進捗可視化
- リアルタイム進捗バー
- リソース使用量表示
- 推定残り時間計算

## 使用方法

### 基本実行

```bash
# 量子化評価パイプライン実行
python scripts/quantization_evaluation_pipeline.py --model models/aegis_v25_final --quantizations bf16,q8_0,q4_k_m
```

### パラメータ

- `--model`: 評価対象モデルパス
- `--quantizations`: 量子化形式（カンマ区切り）
- `--benchmarks`: 評価ベンチマーク（デフォルト: gsm8k,math,arc_challenge,elyza）
- `--runs`: 各評価の繰り返し回数（デフォルト: 5）
- `--subagent`: サブエージェント使用（デフォルト: true）

### PowerShell進捗可視化

```powershell
# 進捗監視スクリプト実行
.\scripts\monitor_quantization_progress.ps1 -PipelineId $pipelineId
```

## 実行フロー

### Phase 1: imatrixデータ収集
```bash
# imatrixデータ生成
python scripts/quantization/collect_imatrix_data.py --model models/aegis_v25_final --output imatrix_data/model_v2.5.imatrix
```

### Phase 2: GGUF量子化実行
```bash
# 複数量子化形式での変換
python scripts/quantization/quantize_with_imatrix.py --model models/aegis_v25_final --imatrix imatrix_data/model_v2.5.imatrix --formats bf16,q8_0,q4_k_m
```

### Phase 3: 統計的評価
```bash
# 複数回実行による統計評価
python scripts/evaluation/statistical_benchmark_evaluation.py --models quantized_models/ --benchmarks gsm8k,math,arc_challenge,elyza --runs 5
```

### Phase 4: 結果可視化とドキュメント生成
```bash
# エラーバー付きグラフ生成
python scripts/visualization/generate_quantization_comparison.py --results evaluation_results/quantization_comparison.json --output charts/quantization_performance.png

# 学術文献形式スコアカード生成
python scripts/documentation/generate_academic_scorecard.py --results evaluation_results/quantization_comparison.json --methodology techniques/quantization_methodology.md --output scorecards/quantization_evaluation.pdf
```

## 出力ファイル

### 評価結果
- `evaluation_results/quantization_comparison.json`: 詳細評価データ
- `evaluation_results/statistical_analysis.json`: 統計分析結果
- `charts/quantization_performance.png`: エラーバー付き性能比較グラフ
- `charts/quantization_efficiency.png`: サイズ vs 性能トレードオフグラフ

### ドキュメント
- `scorecards/quantization_evaluation.pdf`: 学術文献形式スコアカード
- `methodology/quantization_methodology.md`: 手法詳細文書
- `reports/quantization_analysis_report.md`: 包括的分析レポート

## 技術仕様

### imatrix保護アルゴリズム

```
1. 重要度行列計算:
   - 各トークンの重要度を活性化パターンから算出
   - 数学・科学関連トークンの優先保護

2. 量子化スケーリング:
   - imatrixに基づく動的スケーリング適用
   - 保護対象トークンの高精度維持

3. 劣化評価:
   - 量子化前後での性能比較
   - 保護効果の定量評価
```

### 統計的評価手法

```
評価指標:
- 平均性能 (μ)
- 標準偏差 (σ)
- 95%信頼区間
- Cohen's d効果量

エラーバー計算:
error_bar = 1.96 * (σ / √n)
```

### サブエージェントアーキテクチャ

```
メインエージェント (orchestrator)
├── 量子化エージェント (quantization_worker)
├── 評価エージェント (evaluation_worker)
├── 可視化エージェント (visualization_worker)
└── ドキュメントエージェント (documentation_worker)
```

## PowerShell進捗可視化

### リアルタイムモニタリング

```powershell
function Show-QuantizationProgress {
    param(
        [string]$PipelineId,
        [int]$UpdateInterval = 2
    )

    while ($true) {
        $progress = Get-PipelineProgress -Id $PipelineId

        # 進捗バー表示
        Write-ProgressBar -Current $progress.Current -Total $progress.Total -Activity "GGUF量子化評価パイプライン"

        # リソース使用量表示
        Show-ResourceUsage -ProcessId $progress.ProcessId

        # 推定残り時間計算
        $eta = Calculate-ETA -Current $progress.Current -Total $progress.Total -Elapsed $progress.Elapsed
        Write-Host "推定残り時間: $eta"

        Start-Sleep -Seconds $UpdateInterval
    }
}
```

### 進捗バー表示例

```
GGUF量子化評価パイプライン
[██████████████████████████████      ] 85%
Phase: 統計的評価実行中
CPU使用率: 78% | メモリ: 12.4GB/32GB
推定残り時間: 00:12:34
```

## トラブルシューティング

### 一般的な問題

#### imatrixデータ収集失敗
```bash
# 解決策: データセットサイズを調整
python scripts/quantization/collect_imatrix_data.py --dataset-size 100000
```

#### 量子化性能劣化が大きい
```bash
# 解決策: より積極的な保護設定
python scripts/quantization/quantize_with_imatrix.py --protection-level high
```

#### PowerShell可視化が表示されない
```powershell
# 解決策: 実行ポリシーを確認
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 拡張機能

### カスタム量子化形式追加

```python
# scripts/quantization/custom_formats.py
QUANTIZATION_CONFIGS = {
    'custom_q4': {
        'method': 'q4_0',
        'bits': 4,
        'protection': 'high'
    }
}
```

### 新規ベンチマーク追加

```python
# scripts/evaluation/custom_benchmarks.py
def evaluate_custom_benchmark(model_path, benchmark_config):
    # カスタム評価ロジック
    pass
```

## 参考文献

1. "Imatrix: Importance Matrix for Quantization-Aware Training" (2024)
2. "GGUF: Efficient Model Format for Large Language Models" (2023)
3. "Statistical Evaluation of Quantized Neural Networks" (2023)

## 結論

このスキルは、GGUF量子化の品質評価を体系的かつ学術的に行うための包括的なソリューションを提供します。imatrix保護、エラーバー付き統計評価、学術文献形式ドキュメント、そしてPowerShell進捗可視化により、量子化モデルの性能を正確に評価し、比較することができます。