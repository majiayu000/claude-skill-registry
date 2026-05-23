---
name: ios-performance
description: "iOSアプリのパフォーマンス最適化支援スキル。Instruments活用、メモリ/CPU/GPU使用率分析、アプリ起動時間・バッテリー消費の最適化をサポート。Use when: パフォーマンス問題の調査、アプリ最適化、メモリリーク検出、起動時間短縮、バッテリー消費改善。"
---

# iOS Performance（パフォーマンス最適化支援）

## 概要

iOSアプリケーションのパフォーマンス最適化を包括的に支援するスキル。
Instruments等のツールを活用した計測から、具体的な改善施策の実装までをカバーする。

### 対象領域

- **メモリ使用量**: リーク検出、メモリフットプリント最適化
- **CPU使用率**: 処理の効率化、バックグラウンド処理最適化
- **GPU使用率**: レンダリング最適化、フレームレート改善
- **起動時間**: Cold/Warm起動の高速化
- **バッテリー消費**: 電力効率の改善
- **ネットワーク**: 通信効率の最適化

## 実行条件

以下の状況でこのスキルを起動する：

- アプリの動作が遅いと感じる時
- メモリ使用量が高いと報告された時
- バッテリー消費が多いと指摘された時
- App Store Connect でパフォーマンス警告が出た時
- ユーザーからパフォーマンスに関するフィードバックがあった時
- 新機能追加後のパフォーマンス影響を確認したい時
- リリース前のパフォーマンス検証を行う時

## プロセス

### Phase 1: パフォーマンス計測

#### 1.1 計測指標の定義

| 指標 | 目標値 | 計測方法 |
|------|--------|---------|
| 起動時間（Cold） | < 400ms | Instruments / MetricKit |
| 起動時間（Warm） | < 200ms | Instruments / MetricKit |
| メモリ使用量 | < 100MB（基本機能） | Instruments / Xcode Memory Gauge |
| CPU使用率（アイドル） | < 1% | Instruments |
| フレームレート | 60fps / 120fps | Instruments / CADisplayLink |
| バッテリー消費 | 低〜中 | Instruments / MetricKit |

#### 1.2 Instruments の選択

詳細は `references/instruments-guide.md` を参照。

| 問題 | 推奨 Instrument |
|------|----------------|
| メモリリーク | Leaks |
| メモリ使用量 | Allocations |
| CPU使用率 | Time Profiler |
| UI性能 | Core Animation / Animation Hitches |
| 起動時間 | App Launch |
| バッテリー | Energy Log |
| ネットワーク | Network |

### Phase 2: メモリ最適化

詳細は `references/memory-optimization.md` を参照。

#### 2.1 メモリリーク検出

```swift
// 循環参照の典型例と修正

// Bad: 循環参照
class ViewController: UIViewController {
    var completion: (() -> Void)?
    
    func setup() {
        completion = {
            self.doSomething()  // strong reference cycle
        }
    }
}

// Good: weak self で循環参照を回避
class ViewController: UIViewController {
    var completion: (() -> Void)?
    
    func setup() {
        completion = { [weak self] in
            self?.doSomething()
        }
    }
}
```

#### 2.2 メモリフットプリント削減

```swift
// 画像メモリ最適化
// Bad: 大きな画像をそのまま保持
let image = UIImage(named: "large_image")

// Good: 適切なサイズにリサイズ
func resizedImage(_ image: UIImage, targetSize: CGSize) -> UIImage {
    let renderer = UIGraphicsImageRenderer(size: targetSize)
    return renderer.image { _ in
        image.draw(in: CGRect(origin: .zero, size: targetSize))
    }
}

// Better: ImageIO でメモリ効率的に読み込み
func downsampledImage(at url: URL, to pointSize: CGSize, scale: CGFloat) -> UIImage? {
    let imageSourceOptions = [kCGImageSourceShouldCache: false] as CFDictionary
    guard let imageSource = CGImageSourceCreateWithURL(url as CFURL, imageSourceOptions) else {
        return nil
    }
    
    let maxDimensionInPixels = max(pointSize.width, pointSize.height) * scale
    let downsampleOptions = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceShouldCacheImmediately: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: maxDimensionInPixels
    ] as CFDictionary
    
    guard let downsampledImage = CGImageSourceCreateThumbnailAtIndex(imageSource, 0, downsampleOptions) else {
        return nil
    }
    
    return UIImage(cgImage: downsampledImage)
}
```

### Phase 3: CPU最適化

詳細は `references/cpu-optimization.md` を参照。

#### 3.1 Time Profiler による分析

```swift
// 重い処理の特定と最適化

// Bad: メインスレッドでの重い処理
func processData() {
    let result = heavyComputation(data)  // UI がブロックされる
    updateUI(with: result)
}

// Good: バックグラウンドスレッドで処理
func processData() {
    Task.detached(priority: .userInitiated) {
        let result = heavyComputation(data)
        await MainActor.run {
            updateUI(with: result)
        }
    }
}
```

#### 3.2 計算の最適化

```swift
// アルゴリズムの改善
// Bad: O(n^2) の検索
func findDuplicates(in array: [Int]) -> [Int] {
    var duplicates: [Int] = []
    for i in 0..<array.count {
        for j in (i+1)..<array.count {
            if array[i] == array[j] && !duplicates.contains(array[i]) {
                duplicates.append(array[i])
            }
        }
    }
    return duplicates
}

// Good: O(n) の検索
func findDuplicates(in array: [Int]) -> [Int] {
    var seen = Set<Int>()
    var duplicates = Set<Int>()
    for element in array {
        if seen.contains(element) {
            duplicates.insert(element)
        } else {
            seen.insert(element)
        }
    }
    return Array(duplicates)
}
```

### Phase 4: GPU/レンダリング最適化

詳細は `references/rendering-optimization.md` を参照。

#### 4.1 フレームドロップの検出

```swift
// CADisplayLink でフレームレート監視
class FrameRateMonitor {
    private var displayLink: CADisplayLink?
    private var lastTimestamp: CFTimeInterval = 0
    
    func start() {
        displayLink = CADisplayLink(target: self, selector: #selector(tick))
        displayLink?.add(to: .main, forMode: .common)
    }
    
    @objc private func tick(_ link: CADisplayLink) {
        if lastTimestamp > 0 {
            let duration = link.timestamp - lastTimestamp
            let fps = 1.0 / duration
            if fps < 55 {  // 60fps を下回ったら警告
                print("Frame drop detected: \(fps) fps")
            }
        }
        lastTimestamp = link.timestamp
    }
    
    func stop() {
        displayLink?.invalidate()
        displayLink = nil
    }
}
```

#### 4.2 オフスクリーンレンダリングの回避

```swift
// Bad: オフスクリーンレンダリングを発生させる
view.layer.cornerRadius = 10
view.layer.masksToBounds = true
view.layer.shadowColor = UIColor.black.cgColor
view.layer.shadowOffset = CGSize(width: 0, height: 2)
view.layer.shadowOpacity = 0.3

// Good: 別レイヤーで影を描画
view.layer.cornerRadius = 10
view.layer.masksToBounds = true

let shadowView = UIView(frame: view.frame)
shadowView.layer.shadowColor = UIColor.black.cgColor
shadowView.layer.shadowOffset = CGSize(width: 0, height: 2)
shadowView.layer.shadowOpacity = 0.3
shadowView.layer.shadowPath = UIBezierPath(
    roundedRect: view.bounds,
    cornerRadius: 10
).cgPath

// Better: SwiftUI の compositingGroup
view
    .cornerRadius(10)
    .compositingGroup()
    .shadow(radius: 5)
```

### Phase 5: 起動時間最適化

詳細は `references/launch-optimization.md` を参照。

#### 5.1 起動フェーズの理解

```
Cold Launch:
1. dyld: ライブラリ読み込み
2. Runtime: クラス初期化、+load メソッド
3. UIKit: AppDelegate/SceneDelegate 初期化
4. Initial Frame: 最初の画面描画

Warm Launch:
- プロセスは生きているが、バックグラウンドから復帰
- UIの再構築が必要
```

#### 5.2 起動時間計測

```swift
// アプリ起動時間の計測
class AppLaunchTimer {
    static let shared = AppLaunchTimer()
    
    private let processStartTime: CFAbsoluteTime
    
    init() {
        // プロセス起動時刻を取得
        var kinfo = kinfo_proc()
        var size = MemoryLayout<kinfo_proc>.stride
        var mib: [Int32] = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
        sysctl(&mib, u_int(mib.count), &kinfo, &size, nil, 0)
        
        let startTime = kinfo.kp_proc.p_starttime
        processStartTime = CFAbsoluteTime(startTime.tv_sec) + CFAbsoluteTime(startTime.tv_usec) / 1_000_000
    }
    
    func markFirstFrame() {
        let now = CFAbsoluteTimeGetCurrent()
        let launchTime = now - processStartTime
        print("App launch time: \(launchTime * 1000) ms")
    }
}

// AppDelegate で使用
func application(_ application: UIApplication, 
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    // 最初のフレーム描画後に計測
    DispatchQueue.main.async {
        AppLaunchTimer.shared.markFirstFrame()
    }
    return true
}
```

#### 5.3 起動最適化テクニック

```swift
// 1. 遅延初期化
class HeavyService {
    static let shared = HeavyService()  // lazy by default
    
    private init() {
        // 重い初期化処理
    }
}

// 2. バックグラウンドでの初期化
func application(_ application: UIApplication,
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    
    // 起動に必須な処理のみメインスレッドで
    setupCriticalServices()
    
    // 非必須の処理はバックグラウンドで
    DispatchQueue.global(qos: .utility).async {
        self.setupAnalytics()
        self.warmUpCache()
        self.preloadData()
    }
    
    return true
}

// 3. 静的初期化の回避
// Bad: グローバル変数の重い初期化
let heavyFormatter: DateFormatter = {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: "ja_JP")
    formatter.dateStyle = .full
    return formatter
}()

// Good: 必要時に初期化
class DateFormatterProvider {
    private var _formatter: DateFormatter?
    
    var formatter: DateFormatter {
        if _formatter == nil {
            let f = DateFormatter()
            f.locale = Locale(identifier: "ja_JP")
            f.dateStyle = .full
            _formatter = f
        }
        return _formatter!
    }
}
```

### Phase 6: バッテリー最適化

詳細は `references/battery-optimization.md` を参照。

#### 6.1 バッテリー消費の主要因

| 要因 | 影響度 | 対策 |
|------|--------|------|
| 位置情報 | 高 | 精度を下げる、バックグラウンド更新を制限 |
| ネットワーク | 高 | バッチ処理、適切なタイミングで通信 |
| CPU | 中 | 処理の効率化、アイドル時の処理削減 |
| GPU | 中 | 不要なアニメーション削減 |
| センサー | 低〜中 | 必要時のみ使用 |

#### 6.2 位置情報の最適化

```swift
// Bad: 常に高精度
locationManager.desiredAccuracy = kCLLocationAccuracyBest
locationManager.allowsBackgroundLocationUpdates = true
locationManager.startUpdatingLocation()

// Good: 用途に応じた精度
// ナビゲーション時
locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation

// 大まかな位置のみ必要な場合
locationManager.desiredAccuracy = kCLLocationAccuracyKilometer

// 重要な位置変化のみ
locationManager.startMonitoringSignificantLocationChanges()
```

#### 6.3 ネットワーク最適化

```swift
// バッチ処理でネットワークアクセスをまとめる
class BatchNetworkManager {
    private var pendingRequests: [URLRequest] = []
    private var batchTimer: Timer?
    
    func enqueue(_ request: URLRequest) {
        pendingRequests.append(request)
        
        // 5秒後にバッチ実行
        batchTimer?.invalidate()
        batchTimer = Timer.scheduledTimer(withTimeInterval: 5.0, repeats: false) { [weak self] _ in
            self?.executeBatch()
        }
    }
    
    private func executeBatch() {
        guard !pendingRequests.isEmpty else { return }
        
        // バッチリクエストを実行
        let requests = pendingRequests
        pendingRequests = []
        
        // 実行処理...
    }
}
```

### Phase 7: MetricKit によるモニタリング

```swift
import MetricKit

class MetricsManager: NSObject, MXMetricManagerSubscriber {
    
    static let shared = MetricsManager()
    
    private override init() {
        super.init()
        MXMetricManager.shared.add(self)
    }
    
    // iOS 13+: 日次レポート
    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads {
            // 起動時間
            if let launchMetrics = payload.applicationLaunchMetrics {
                analyzelaunchMetrics(launchMetrics)
            }
            
            // メモリ
            if let memoryMetrics = payload.memoryMetrics {
                analyzeMemoryMetrics(memoryMetrics)
            }
            
            // CPU
            if let cpuMetrics = payload.cpuMetrics {
                analyzeCPUMetrics(cpuMetrics)
            }
        }
    }
    
    // iOS 14+: 診断レポート
    func didReceive(_ payloads: [MXDiagnosticPayload]) {
        for payload in payloads {
            // クラッシュ
            if let crashDiagnostics = payload.crashDiagnostics {
                analyzeCrashes(crashDiagnostics)
            }
            
            // ハング
            if let hangDiagnostics = payload.hangDiagnostics {
                analyzeHangs(hangDiagnostics)
            }
        }
    }
    
    private func analyzelaunchMetrics(_ metrics: MXAppLaunchMetric) {
        let resumeTime = metrics.histogrammedApplicationResumeTime
        let launchTime = metrics.histogrammedTimeToFirstDraw
        
        // 閾値を超えたらアラート
        // ...
    }
}
```

## 出力形式

### パフォーマンスレポート

```markdown
# パフォーマンス分析レポート

## 概要
- 分析日: YYYY-MM-DD
- 対象バージョン: x.x.x
- テストデバイス: iPhone 15 Pro (iOS 17.2)

## 計測結果

### 起動時間
| 種別 | 計測値 | 目標 | 判定 |
|-----|--------|-----|------|
| Cold Launch | 350ms | <400ms | OK |
| Warm Launch | 180ms | <200ms | OK |

### メモリ使用量
| 状態 | 使用量 | 目標 | 判定 |
|-----|--------|-----|------|
| 起動直後 | 45MB | <50MB | OK |
| リスト表示 | 80MB | <100MB | OK |
| ピーク | 150MB | <200MB | OK |

### CPU使用率
| 状態 | 使用率 | 目標 | 判定 |
|-----|--------|-----|------|
| アイドル | 0.5% | <1% | OK |
| スクロール中 | 25% | <30% | OK |

## 検出された問題

### 問題1: メモリリーク
- 場所: ProfileViewController
- 原因: クロージャでのstrong reference cycle
- 影響: 画面遷移ごとに2MB増加
- 推奨修正: [weak self] の追加

### 問題2: フレームドロップ
- 場所: ProductListView
- 原因: セル再利用時の画像デコード
- 影響: スクロール時に55fps以下
- 推奨修正: 画像のプリフェッチと適切なサイズへのダウンサンプリング

## 改善提案

1. **優先度: 高**
   - メモリリークの修正
   - 推定効果: メモリ使用量 20% 削減

2. **優先度: 中**
   - 画像処理の最適化
   - 推定効果: スクロール性能 30% 向上
```

## ガードレール

### 必須遵守事項

1. **計測前後の比較**: 最適化前後で必ず計測し効果を検証
2. **複数デバイスでの検証**: 最低スペックのサポートデバイスでテスト
3. **リリース構成でのテスト**: Debug ではなく Release でプロファイリング
4. **継続的モニタリング**: MetricKit でリリース後も監視

### 禁止事項

1. **早すぎる最適化**: 計測なしでの最適化は行わない
2. **可読性の犠牲**: 極端な最適化で保守性を損なわない
3. **機能の削減**: パフォーマンスのためにUXを損なわない

### 警告事項

1. **シミュレータでの計測**: 実機と性能特性が異なる
2. **デバッグビルド**: オーバーヘッドが大きい
3. **サンプルサイズ**: 複数回計測して平均を取る
4. **環境要因**: バッテリー残量、温度、他アプリの影響

## 参照

- `references/instruments-guide.md`: Instruments活用ガイド
- `references/memory-optimization.md`: メモリ最適化詳細
- `references/cpu-optimization.md`: CPU最適化詳細
- `references/rendering-optimization.md`: レンダリング最適化詳細
- `references/launch-optimization.md`: 起動時間最適化詳細
- `references/battery-optimization.md`: バッテリー最適化詳細
