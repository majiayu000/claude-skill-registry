// sck-record.swift — record the main display + SYSTEM AUDIO to an .mp4 using
// ScreenCaptureKit (macOS 13+). No loopback / no install needed; just Screen
// Recording permission (same as `screencapture`). Captures the Mac's own output
// (e.g. `say` voices), which `screencapture -g` (mic only) cannot.
//   swift sck-record.swift <out.mp4> <seconds> [--no-cursor]
// --no-cursor omits the system cursor from the capture — useful when a
// post-production step overlays a synthetic (smoothed) cursor instead.
import Foundation
import ScreenCaptureKit
import AVFoundation
import CoreMedia

var argv = CommandLine.arguments
let showCursor = !argv.contains("--no-cursor")
argv.removeAll { $0 == "--no-cursor" }
let outPath = argv.count > 1 ? argv[1] : NSHomeDirectory() + "/Desktop/sck.mp4"
let seconds = argv.count > 2 ? (Double(argv[2]) ?? 20) : 20

final class Recorder: NSObject, SCStreamOutput, SCStreamDelegate {
    var stream: SCStream!
    var writer: AVAssetWriter!
    var vInput: AVAssetWriterInput!
    var aInput: AVAssetWriterInput!
    var started = false
    let q = DispatchQueue(label: "sck.rec")

    func start() async throws {
        let content = try await SCShareableContent.excludingDesktopWindows(false, onScreenWindowsOnly: true)
        guard let display = content.displays.first else { fatalError("no display") }
        let filter = SCContentFilter(display: display, excludingApplications: [], exceptingWindows: [])
        let cfg = SCStreamConfiguration()
        let scale = 2   // retina backing; cap width to keep file sane
        cfg.width = min(display.width * scale, 2560)
        cfg.height = Int(Double(cfg.width) * Double(display.height) / Double(display.width))
        cfg.minimumFrameInterval = CMTime(value: 1, timescale: 30)
        cfg.queueDepth = 6
        cfg.showsCursor = showCursor
        cfg.capturesAudio = true
        cfg.sampleRate = 48000
        cfg.channelCount = 2

        let url = URL(fileURLWithPath: outPath)
        try? FileManager.default.removeItem(at: url)
        writer = try AVAssetWriter(outputURL: url, fileType: .mp4)
        vInput = AVAssetWriterInput(mediaType: .video, outputSettings: [
            AVVideoCodecKey: AVVideoCodecType.h264,
            AVVideoWidthKey: cfg.width, AVVideoHeightKey: cfg.height,
            AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 8_000_000]
        ])
        vInput.expectsMediaDataInRealTime = true
        aInput = AVAssetWriterInput(mediaType: .audio, outputSettings: [
            AVFormatIDKey: kAudioFormatMPEG4AAC, AVSampleRateKey: 48000,
            AVNumberOfChannelsKey: 2, AVEncoderBitRateKey: 160_000
        ])
        aInput.expectsMediaDataInRealTime = true
        writer.add(vInput); writer.add(aInput)

        stream = SCStream(filter: filter, configuration: cfg, delegate: self)
        try stream.addStreamOutput(self, type: .screen, sampleHandlerQueue: q)
        try stream.addStreamOutput(self, type: .audio, sampleHandlerQueue: q)
        try await stream.startCapture()
    }

    func stream(_ stream: SCStream, didOutputSampleBuffer sb: CMSampleBuffer, of type: SCStreamOutputType) {
        guard CMSampleBufferDataIsReady(sb) else { return }
        if type == .screen {
            // only keep "complete" frames
            guard let attach = CMSampleBufferGetSampleAttachmentsArray(sb, createIfNecessary: false) as? [[SCStreamFrameInfo: Any]],
                  let statusRaw = attach.first?[.status] as? Int, let status = SCFrameStatus(rawValue: statusRaw),
                  status == .complete else { return }
            if !started {
                started = true
                writer.startWriting()
                writer.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sb))
            }
            if vInput.isReadyForMoreMediaData { vInput.append(sb) }
        } else if type == .audio, started, aInput.isReadyForMoreMediaData {
            aInput.append(sb)
        }
    }

    func finish() async {
        try? await stream.stopCapture()
        vInput.markAsFinished(); aInput.markAsFinished()
        await writer.finishWriting()
    }
}

let rec = Recorder()
let sem = DispatchSemaphore(value: 0)
Task {
    do { try await rec.start() } catch { FileHandle.standardError.write("start error: \(error)\n".data(using: .utf8)!); exit(1) }
    try? await Task.sleep(nanoseconds: UInt64(seconds * 1_000_000_000))
    await rec.finish()
    sem.signal()
}
sem.wait()
print(outPath)
