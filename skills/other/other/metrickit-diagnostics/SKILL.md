---
name: metrickit-diagnostics
description: "Collect and analyze on-device performance metrics and crash diagnostics using MetricKit. Use when setting up MXMetricManager, handling MXMetricPayload or MXDiagnosticPayload, processing crash/hang/disk-write diagnostics via MXCallStackTree, adding custom signpost metrics, or uploading telemetry to an analytics backend."
---

# MetricKit Diagnostics

Collect aggregated performance metrics and crash diagnostics from production
devices using MetricKit. The framework delivers daily metric payloads (CPU,
memory, launch time, hang rate, animation hitches, network usage) and
immediate diagnostic payloads (crashes, hangs, disk-write exceptions) with
full call-stack trees for triage.

## Contents

- [Subscriber Setup](#subscriber-setup)
- [Receiving Metric Payloads](#receiving-metric-payloads)
- [Receiving Diagnostic Payloads](#receiving-diagnostic-payloads)
- [Key Metrics](#key-metrics)
- [Call Stack Trees](#call-stack-trees)
- [Custom Signpost Metrics](#custom-signpost-metrics)
- [Exporting and Uploading Payloads](#exporting-and-uploading-payloads)
- [Extended Launch Measurement](#extended-launch-measurement)
- [Xcode Organizer Integration](#xcode-organizer-integration)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Subscriber Setup

Register a subscriber as early as possible — ideally in
`application(_:didFinishLaunchingWithOptions:)` or `App.init`. MetricKit
starts accumulating reports after the first access to `MXMetricManager.shared`.

```swift
import MetricKit

final class MetricsSubscriber: NSObject, MXMetricManagerSubscriber {
    static let shared = MetricsSubscriber()

    func subscribe() {
        MXMetricManager.shared.add(self)
    }

    func unsubscribe() {
        MXMetricManager.shared.remove(self)
    }

    func didReceive(_ payloads: [MXMetricPayload]) {
        // Handle daily metrics
    }

    func didReceive(_ payloads: [MXDiagnosticPayload]) {
        // Handle diagnostics (crashes, hangs, disk writes)
    }
}
```

### UIKit Registration

```swift
func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
) -> Bool {
    MetricsSubscriber.shared.subscribe()
    return true
}
```

### SwiftUI Registration

```swift
@main
struct MyApp: App {
    init() {
        MetricsSubscriber.shared.subscribe()
    }
    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

## Receiving Metric Payloads

`MXMetricPayload` arrives approximately once per 24 hours containing
aggregated metrics. The array may contain multiple payloads if prior
deliveries were missed.

```swift
func didReceive(_ payloads: [MXMetricPayload]) {
    for payload in payloads {
        let begin = payload.timeStampBegin
        let end = payload.timeStampEnd
        let version = payload.latestApplicationVersion

        // Persist raw JSON before processing
        let jsonData = payload.jsonRepresentation()
        persistPayload(jsonData, from: begin, to: end)

        processMetrics(payload)
    }
}
```

**Availability**: `MXMetricPayload` — iOS 13.0+, macOS 10.15+, visionOS 1.0+

## Receiving Diagnostic Payloads

`MXDiagnosticPayload` delivers crash, hang, CPU exception, disk-write, and
app-launch diagnostics. On iOS 15+ and macOS 12+, diagnostics arrive
immediately rather than bundled with the daily report.

```swift
func didReceive(_ payloads: [MXDiagnosticPayload]) {
    for payload in payloads {
        let jsonData = payload.jsonRepresentation()
        persistPayload(jsonData)

        if let crashes = payload.crashDiagnostics {
            for crash in crashes {
                handleCrash(crash)
            }
        }
        if let hangs = payload.hangDiagnostics {
            for hang in hangs {
                handleHang(hang)
            }
        }
        if let diskWrites = payload.diskWriteExceptionDiagnostics {
            for diskWrite in diskWrites {
                handleDiskWrite(diskWrite)
            }
        }
        if let cpuExceptions = payload.cpuExceptionDiagnostics {
            for cpuException in cpuExceptions {
                handleCPUException(cpuException)
            }
        }
        if let launchDiags = payload.appLaunchDiagnostics {
            for launchDiag in launchDiags {
                handleSlowLaunch(launchDiag)
            }
        }
    }
}
```

**Availability**: `MXDiagnosticPayload` — iOS 14.0+, macOS 12.0+, visionOS 1.0+

## Key Metrics

### Launch Time — MXAppLaunchMetric

```swift
if let launch = payload.applicationLaunchMetrics {
    let firstDraw = launch.histogrammedTimeToFirstDraw
    let optimized = launch.histogrammedOptimizedTimeToFirstDraw
    let resume = launch.histogrammedApplicationResumeTime
    let extended = launch.histogrammedExtendedLaunch
}
```

### Run Time — MXAppRunTimeMetric

```swift
if let runTime = payload.applicationTimeMetrics {
    let fg = runTime.cumulativeForegroundTime    // Measurement<UnitDuration>
    let bg = runTime.cumulativeBackgroundTime
    let bgAudio = runTime.cumulativeBackgroundAudioTime
    let bgLocation = runTime.cumulativeBackgroundLocationTime
}
```

### CPU, Memory, and Responsiveness

```swift
if let cpu = payload.cpuMetrics {
    let cpuTime = cpu.cumulativeCPUTime              // Measurement<UnitDuration>
}
if let memory = payload.memoryMetrics {
    let peakMemory = memory.peakMemoryUsage           // Measurement<UnitInformationStorage>
}
if let responsiveness = payload.applicationResponsivenessMetrics {
    let hangTime = responsiveness.histogrammedApplicationHangTime
}
if let animation = payload.animationMetrics {
    let scrollHitchRate = animation.scrollHitchTimeRatio  // Measurement<Unit>
}
```

### Network and Cellular

```swift
if let network = payload.networkTransferMetrics {
    let wifiUp = network.cumulativeWifiUpload          // Measurement<UnitInformationStorage>
    let wifiDown = network.cumulativeWifiDownload
    let cellUp = network.cumulativeCellularUpload
    let cellDown = network.cumulativeCellularDownload
}
```

### App Exit Metrics

```swift
if let exits = payload.applicationExitMetrics {
    let fg = exits.foregroundExitData
    let bg = exits.backgroundExitData
    // Inspect normal, abnormal, watchdog, memory, etc.
}
```

## Call Stack Trees

`MXCallStackTree` is attached to each diagnostic (crash, hang, CPU exception,
disk write, app launch). Use `jsonRepresentation()` to extract and symbolicate.

```swift
func handleCrash(_ crash: MXCrashDiagnostic) {
    let tree = crash.callStackTree
    let treeJSON = tree.jsonRepresentation()

    let exceptionType = crash.exceptionType
    let signal = crash.signal
    let reason = crash.terminationReason

    uploadDiagnostic(
        type: "crash",
        exceptionType: exceptionType,
        signal: signal,
        reason: reason,
        callStack: treeJSON
    )
}

func handleHang(_ hang: MXHangDiagnostic) {
    let tree = hang.callStackTree
    let duration = hang.hangDuration  // Measurement<UnitDuration>
    uploadDiagnostic(type: "hang", duration: duration, callStack: tree.jsonRepresentation())
}
```

The JSON structure contains an array of call stack frames with binary name,
offset, and address. Symbolicate using `atos` or upload dSYMs to your
analytics service.

**Availability**: `MXCallStackTree` — iOS 14.0+, macOS 12.0+, visionOS 1.0+

## Custom Signpost Metrics

Use `mxSignpost` with a MetricKit log handle to capture custom performance
intervals. These appear in the daily `MXMetricPayload` under `signpostMetrics`.

### Creating a Log Handle

```swift
let metricLog = MXMetricManager.makeLogHandle(category: "Networking")
```

### Emitting Signposts

```swift
import os

func fetchData() async throws -> Data {
    let signpostID = MXSignpostIntervalData.makeSignpostID(log: metricLog)

    mxSignpost(.begin, log: metricLog, name: "DataFetch", signpostID: signpostID)
    let data = try await URLSession.shared.data(from: url).0
    mxSignpost(.end, log: metricLog, name: "DataFetch", signpostID: signpostID)

    return data
}
```

### Reading Custom Metrics from Payload

```swift
if let signposts = payload.signpostMetrics {
    for metric in signposts {
        let name = metric.signpostName       // "DataFetch"
        let category = metric.signpostCategory // "Networking"
        let count = metric.totalCount
        if let intervalData = metric.signpostIntervalData {
            let avgMemory = intervalData.averageMemory
            let cumulativeCPUTime = intervalData.cumulativeCPUTime
        }
    }
}
```

> The system limits the number of custom signpost metrics per log to reduce
> on-device overhead. Reserve custom metrics for critical code paths.

## Exporting and Uploading Payloads

Both payload types conform to `NSSecureCoding` and provide
`jsonRepresentation()` for easy serialization.

```swift
func persistPayload(_ jsonData: Data, from: Date? = nil, to: Date? = nil) {
    let fileName = "metrics_\(ISO8601DateFormatter().string(from: Date())).json"
    let url = FileManager.default.temporaryDirectory.appending(path: fileName)
    try? jsonData.write(to: url)
}

func uploadPayloads(_ jsonData: Data) {
    Task.detached(priority: .utility) {
        var request = URLRequest(url: URL(string: "https://api.example.com/metrics")!)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        _ = try? await URLSession.shared.data(for: request)
    }
}
```

### Retrieving Past Payloads

If the subscriber was not registered when payloads arrived, retrieve them
using `pastPayloads` and `pastDiagnosticPayloads`. These return reports
generated since the last allocation of the shared manager.

```swift
let pastMetrics = MXMetricManager.shared.pastPayloads
let pastDiags = MXMetricManager.shared.pastDiagnosticPayloads
```

## Extended Launch Measurement

Track post-first-draw setup work (loading databases, restoring state) as
part of the launch metric using extended launch measurement.

```swift
let taskID = MXLaunchTaskID("com.example.app.loadDatabase")

MXMetricManager.shared.extendLaunchMeasurement(forTaskID: taskID)
// Perform extended launch work...
await database.load()
MXMetricManager.shared.finishExtendedLaunchMeasurement(forTaskID: taskID)
```

Extended launch times appear under `histogrammedExtendedLaunch` in
`MXAppLaunchMetric`.

## Xcode Organizer Integration

Xcode Organizer shows the same MetricKit data aggregated across all users
who have opted in to share diagnostics. Use Organizer for trend analysis:

- **Metrics tab**: Battery, performance, and disk-write metrics over time
- **Regressions tab**: Automatic detection of metric regressions per version
- **Crashes tab**: Crash logs with symbolicated stack traces

MetricKit on-device collection complements Organizer by letting you route
raw data to your own backend for custom dashboards, alerting, and filtering
by user cohort.

## Common Mistakes

### DON'T: Subscribe to MXMetricManager too late

The system may deliver pending payloads shortly after launch. Subscribing
late (e.g., in a view controller) risks missing them entirely.

```swift
// WRONG — subscribing in a view controller
override func viewDidLoad() {
    super.viewDidLoad()
    MXMetricManager.shared.add(self)
}

// CORRECT — subscribe in application(_:didFinishLaunchingWithOptions:)
func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions opts: [UIApplication.LaunchOptionsKey: Any]?
) -> Bool {
    MXMetricManager.shared.add(metricsSubscriber)
    return true
}
```

### DON'T: Ignore MXDiagnosticPayload

Only handling `MXMetricPayload` means you miss crash, hang, and disk-write
diagnostics — the most actionable data MetricKit provides.

```swift
// WRONG — only implementing metric callback
func didReceive(_ payloads: [MXMetricPayload]) { /* ... */ }

// CORRECT — implement both callbacks
func didReceive(_ payloads: [MXMetricPayload]) { /* ... */ }
func didReceive(_ payloads: [MXDiagnosticPayload]) { /* ... */ }
```

### DON'T: Process payloads without persisting first

The system delivers each payload once. If your subscriber crashes during
processing, the data is lost permanently.

```swift
// WRONG — process inline, crash loses data
func didReceive(_ payloads: [MXDiagnosticPayload]) {
    for p in payloads {
        riskyProcessing(p)  // If this crashes, payload is gone
    }
}

// CORRECT — persist raw JSON first, then process
func didReceive(_ payloads: [MXDiagnosticPayload]) {
    for p in payloads {
        let json = p.jsonRepresentation()
        try? json.write(to: localCacheURL())   // Safe on disk
        Task.detached { self.processAsync(json) }
    }
}
```

### DON'T: Do heavy work synchronously in didReceive

The callback runs on an arbitrary thread. Blocking it with heavy processing
or synchronous network calls delays delivery of subsequent payloads.

```swift
// WRONG — synchronous upload in callback
func didReceive(_ payloads: [MXMetricPayload]) {
    for p in payloads {
        let data = p.jsonRepresentation()
        URLSession.shared.uploadTask(with: request, from: data).resume()  // sync wait
    }
}

// CORRECT — persist and dispatch async
func didReceive(_ payloads: [MXMetricPayload]) {
    for p in payloads {
        let json = p.jsonRepresentation()
        persistLocally(json)
        Task.detached(priority: .utility) {
            await self.uploadToBackend(json)
        }
    }
}
```

### DON'T: Expect immediate data in development

MetricKit aggregates data over 24-hour windows. Payloads do not arrive
immediately after instrumenting. Use Xcode Organizer or simulated payloads
for faster iteration during development.

## Review Checklist

- [ ] `MXMetricManager.shared.add(subscriber)` called in `application(_:didFinishLaunchingWithOptions:)` or `App.init`
- [ ] Subscriber conforms to `MXMetricManagerSubscriber` and inherits `NSObject`
- [ ] Both `didReceive(_: [MXMetricPayload])` and `didReceive(_: [MXDiagnosticPayload])` implemented
- [ ] Raw `jsonRepresentation()` persisted to disk before processing
- [ ] Heavy processing dispatched asynchronously off the callback thread
- [ ] `MXCallStackTree` JSON uploaded with dSYMs for symbolication
- [ ] Custom signpost metrics limited to critical code paths
- [ ] `pastPayloads` and `pastDiagnosticPayloads` checked on launch for missed deliveries
- [ ] Extended launch tasks call both `extendLaunchMeasurement` and `finishExtendedLaunchMeasurement`
- [ ] Analytics backend accepts and stores MetricKit JSON format
- [ ] Xcode Organizer reviewed for regression trends alongside on-device data

## References

- [MetricKit framework](https://sosumi.ai/documentation/metrickit)
- [MXMetricManager](https://sosumi.ai/documentation/metrickit/mxmetricmanager)
- [MXMetricManagerSubscriber](https://sosumi.ai/documentation/metrickit/mxmetricmanagersubscriber)
- [MXMetricPayload](https://sosumi.ai/documentation/metrickit/mxmetricpayload)
- [MXDiagnosticPayload](https://sosumi.ai/documentation/metrickit/mxdiagnosticpayload)
- [MXCallStackTree](https://sosumi.ai/documentation/metrickit/mxcallstacktree)
- [MXSignpostMetric](https://sosumi.ai/documentation/metrickit/mxsignpostmetric)
- [MXAppLaunchMetric](https://sosumi.ai/documentation/metrickit/mxapplaunchmetric)
- [MXAppRunTimeMetric](https://sosumi.ai/documentation/metrickit/mxappruntimemetric)
- [MXCrashDiagnostic](https://sosumi.ai/documentation/metrickit/mxcrashdiagnostic)
- [Analyzing the performance of your shipping app](https://sosumi.ai/documentation/xcode/analyzing-the-performance-of-your-shipping-app)
