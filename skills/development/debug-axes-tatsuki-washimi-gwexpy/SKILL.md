---
name: debug_axes
description: プロットのスケール（対数軸など）、目盛、表示範囲の不具合を診断し、意図した見た目に修正する
---

# Debug Plot Axes Skill

このスキルは、gwexpyにおけるプロットの軸スケール（特に対数軸）や表示範囲（ylim/xlim）が意図通りに表示されない問題を解決するためのものです。

## 診断手順

1.  **内部状態の確認**:
    *   再現スクリプトを作成し、`ax.get_yscale()` や `ax.get_ylim()` を出力して、内部的な設定が 'log' になっているか確認する。

2.  **視覚的リニア問題の特定**:
    *   内部状態が 'log' なのに見た目が線形（Linear）に見える場合、データ範囲が狭すぎることが原因であることが多い（例: 1.0 vs 2.23）。
    *   目盛（ticks）が適切に振られているか、`ax.get_yticks()` で確認する。

3.  **判定ロジックの確認**:
    *   `gwexpy/plot/defaults.py` の `determine_yscale` や `determine_xscale` が正しくデータを認識しているか、デバッグプリント等で確認する。

## 修正ガイドライン

1.  **スケールの強制適用**:
    *   `gwexpy/plot/plot.py` の `Plot.__init__` 内で、`super().__init__` の後に明示的に `ax.set_yscale()` を呼び出す。
    *   適用後には必ず `ax.autoscale_view()` を呼び出して、視覚的な更新を強制する。

2.  **表示範囲の自動拡張 (Log Scale 特有)**:
    *   データ範囲が100倍（2桁）未満の場合、対数軸では目盛がほとんど表示されないため、線形に見えやすい。
    *   `determine_ylim` ロジックを実装/修正し、データの中央値を中心に約2桁分の範囲を確保するように `ylim` を設定する。

3.  **堅牢な型判定**:
    *   `isinstance` チェックが環境（インポート元）の違いで失敗する場合があるため、`type(obj).__name__` や `hasattr(obj, 'frequencies')` などのダックタイピングを併用して判定を行う。

4.  **IPython/Jupyterの重複表示防止**:
    *   `Plot` クラスで `_repr_html_ = None` を設定し、重複表示（reprとplt.show）を防止する。
