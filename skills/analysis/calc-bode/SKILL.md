---
name: calc_bode
description: python-controlを使用して、メカニカルシステムの状態空間モデルから伝達関数（Bode Plot）を計算・表示する
---

# `calc_bode_control`

このスキルは、質量行列(M)や剛性行列(K)を持つ力学系から状態空間モデル(State Space)を構築し、`python-control`ライブラリを用いて周波数応答（Bode Plot）を生成します。

## ワークフロー

1.  **システム行列の取得**:
    -   物理モデルや線形化ツールから $M$ 行列と $K$ 行列を抽出します。
    -   必要に応じて減衰行列 $C$ (通常は剛性に比例、またはモード減衰) を定義します。

2.  **状態空間の構築**:
    -   状態ベクトルを $x = [q, v]^T$ ( $q$: 変位, $v$: 速度) と定義します。
    -   システムの運動方程式 $M \ddot{q} + C \dot{q} + K q = F u$ を、標準的な状態空間形式 $\dot{x} = Ax + Bu$ に変換します。
    -   $A = \begin{bmatrix} 0 & I \\ -M^{-1}K & -M^{-1}C \end{bmatrix}$
    -   $B = \begin{bmatrix} 0 \\ M^{-1}F \end{bmatrix}$

3.  **python-control の利用**:
    -   `import control as ct` を行います。
    -   `sys = ct.ss(A, B, C, D)` でシステムオブジェクトを作成します。

4.  **IO選択 (MIMOの場合)**:
    -   `sys_siso = sys[output_idx, input_idx]` を使用して、目的の入出力チャネルを選択します。

5.  **プロットと分析**:
    -   `ct.bode_plot(sys_siso, ...)` を使用してBodeプロットを生成します。
    -   `Hz=True`, `dB=True`, `deg=True` などのフラグを活用します。
    -   必要に応じて `sys.poles()` を確認して安定性をチェックします。

## 注意事項
- KAGRAのトップステージのような逆振子 (Inverted Pendulum) を含む系では、安定化制御をかける前の開ループ極が不安定側に存在することがあるため注意が必要です。
- 周波数範囲は `np.logspace(np.log10(start_hz * 2*np.pi), np.log10(end_hz * 2*np.pi), n_points)` のように角周波数(rad/s)で指定し、`bode_plot` 側で `Hz=True` を指定するのが確実です。
