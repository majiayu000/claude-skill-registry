# music-beat-sync — BGM 节奏分析与卡点方法论

强节奏 BGM 的片子，**所有转场和关键动效必须落在拍上**。本文档给出从
"拿到一首曲子"到"成片切点误差 ≤3 帧"的完整可复现流程。实测：一支
70s、18 镜、131.97 BPM 的强鼓点宣传片按此法制作，渲后回测全部切点
误差 ≤2.2f（感知阈值约 3f）。

## 0. 何时启用

阶段 0 就问用户：**是否已选好音乐？**
- 已选好 → 走本文档：先分析节奏，再让分镜的每个切点/动效锚到拍号
- 未选 → BGM 选型放到阶段 5（见 pipeline.md），此时动效时间线按
  内容节奏排，不强行卡点

## 1. 节拍网格测定（不要相信 beat_track 的 tempo 标量）

用 `uv run --with librosa --with scipy --python 3.11` 跑一次性脚本：

```python
import numpy as np, librosa

y, sr = librosa.load("bgm.mp3", sr=None, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, tightness=400, units="time")

# 关键一步：对 beat 序列做最小二乘等距网格拟合，求真实 BPM 与相位。
# beat_track 返回的 tempo 标量可能偏差 2%+（实测 129.2 vs 真值 131.97），
# 但它输出的 beat 时刻序列本身是好的——用整个序列拟合直线 t_i = t0 + i*T：
i = np.arange(len(beats))
A = np.vstack([i, np.ones_like(i)]).T
(T, t0), *_ = np.linalg.lstsq(A, beats, rcond=None)
bpm = 60.0 / T
residual = beats - (t0 + i * T)
print(f"BPM={bpm:.2f}  t0={t0:.4f}s  T={T:.5f}s  残差±{np.abs(residual).max()*1000:.0f}ms")
```

验收标准：残差 ≤ ±15ms（半帧内）说明曲子是机器鼓点、网格可信；
残差大说明有变速段，需要分段拟合。

## 2. 鼓点/重音定位（决定大 slam 钉在哪一拍）

```python
from scipy.signal import butter, sosfilt
sos = butter(4, [40, 160], btype="band", fs=sr, output="sos")  # kick 频段
kick = sosfilt(sos, y)
env = librosa.onset.onset_strength(y=kick, sr=sr)
times = librosa.times_like(env, sr=sr)
# 把每个整数拍位置的 env 能量列出来，排序找最强 hit：
for n in range(int((times[-1]-t0)/T)):
    t = t0 + n*T
    e = env[np.argmin(np.abs(times - t))]
    # 记录 (拍号 n, 能量 e)，取 top 若干作为"大 slam 候选拍"
```

产出两样东西进设计 spec：
- **音乐结构表**：能量从第几拍起满、breakdown/静默段在第几拍——
  分镜的能量曲线要贴着它排（breakdown 处放品牌呼吸位是天然结构）
- **最强 hit 拍号清单**：全片 2–3 个最大 slam（开题/高潮/收尾）
  必须钉在这些拍上

**易错点（实测踩过）**：最大 slam 钉在了 b52.5（两拍之间）而最强
kick 在整数拍 b52 上，渲后回测偏差 +5.75f。强鼓点曲的重音几乎总在
整数拍上，半拍钉点必须有 env 数据支持，不能凭听感。

## 3. 时间线用拍号写，不用帧号写

Remotion 项目里把网格常量化，一切镜头边界/动效关键帧用 `beatF()` 表达：

```ts
export const FPS = 30;
export const BEAT0 = 0.2244;   // t0，秒
export const BEAT_INT = 0.45465; // T，秒
export const beatT = (n: number) => BEAT0 + n * BEAT_INT;          // 拍→秒
export const beatF = (n: number) => Math.round(beatT(n) * FPS);    // 拍→帧

export const SHOTS = {
  s0_open:  { from: 0,        to: beatF(8) },
  s1_slam:  { from: beatF(8), to: beatF(16) },
  // …每个镜头边界都是 beatF(整数拍)；镜头内部动效用局部拍：
};
export const localBeat = (shot: {from: number}, n: number) => beatF(n) - shot.from;
```

好处：换曲/换段落时改两个常量全片重排；SFX 钉帧表也写 `beatF(n)`，
与画面共用同一事实源，永不错位。

设计规矩：
- 镜头时长以拍为单位（4/8 拍一镜），加速段可用半拍/四分之一拍阶梯
  （如 CUT_BEATS = [48, 49.5, 50.5, 51, 51.25] 的收敛逼近）
- 每拍一动作的步进类镜头（清单逐项、马赛克逐格）直接 map 拍号
- BGM 鼓点已密时 SFX 克制：只钉画面独有动作，大 slam 只给 2–3 处，
  其余让位给 BGM 的鼓

## 4. 渲后回测（闭环，必做）

```bash
ffmpeg -i out/promo.mp4 -vn -acodec pcm_s16le /tmp/render-audio.wav
```

对渲出音轨重跑第 1 步的网格拟合（BGM 从视频里量，不从源文件量——
这样连音频编码/对齐偏移一起验），然后逐一对比：
**设计切点帧号 vs 最近测得拍的帧号**，输出误差表。

| 判定 | 误差 |
|------|------|
| 合格 | ≤3f（感知阈值） |
| 理想 | ≤1.5f |
| 必修 | >3f 的任何切点 |

误差超标的钉点回第 3 步改拍号或帧偏移，重渲再测，直到全表合格。

## 5. 工具备忘

- librosa 不在系统 python：`uv run --with librosa --with scipy --python 3.11 script.py`
- 只有人声/复杂编曲的曲子 beat_track 会漂：先用 `librosa.effects.hpss`
  分离打击成分再测
- 变速曲（DJ 转场、accelerando）：按能量段分段拟合，各段各自 t0/T
