---
name: macos-agent-development
description: macOS Agent 开发规范（Swift + Accessibility API），包括项目结构、Accessibility API 使用、UI Automation、IPC 通信集成、错误处理和测试。
version: 1.0.0
---

# macOS Agent Development Skill

Expert guidance for developing macOS Platform Agent using Swift + Accessibility API.

## Project Structure

```
platform_agents/macos_agent/
├── main.swift              # 主入口
├── WeChatMonitor.swift     # 微信监听模块
├── InputWriter.swift       # 输入框控制模块
├── IPC/                    # IPC 通信模块
│   ├── MessageSender.swift
│   └── CommandReceiver.swift
├── Utils/                  # 工具模块
│   └── Logger.swift
├── Package.swift           # Swift Package Manager 配置
└── README.md
```

## Accessibility API Setup

### Requesting Permissions

```swift
import Cocoa
import ApplicationServices

func requestAccessibilityPermissions() -> Bool {
    let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true]
    let accessEnabled = AXIsProcessTrustedWithOptions(options as CFDictionary)

    if !accessEnabled {
        print("请在系统偏好设置 -> 安全性与隐私 -> 辅助功能 中授权")
    }

    return accessEnabled
}
```

### Main Entry Point

```swift
// main.swift
import Foundation

class MacOSAgent {
    let monitor: WeChatMonitor
    let inputWriter: InputWriter
    let commandReceiver: CommandReceiver

    init() {
        self.monitor = WeChatMonitor(intervalMs: 500)
        self.inputWriter = InputWriter()
        self.commandReceiver = CommandReceiver()
        setupCommandHandlers()
    }

    func setupCommandHandlers() {
        commandReceiver.registerHandler(commandType: "WriteInput") { command in
            guard let content = command["content"] as? String else {
                return false
            }
            return self.inputWriter.writeToInput(content: content)
        }

        commandReceiver.registerHandler(commandType: "ClearInput") { _ in
            return self.inputWriter.clearInput()
        }

        commandReceiver.registerHandler(commandType: "HealthCheck") { _ in
            MessageSender.sendHealthStatus(status: "ok", agentType: "macos_accessibility")
            return true
        }

        commandReceiver.registerHandler(commandType: "Stop") { _ in
            self.commandReceiver.stop()
            return true
        }
    }

    func run() {
        // 检查权限
        guard requestAccessibilityPermissions() else {
            MessageSender.sendError(message: "未授予辅助功能权限", code: "PERMISSION_DENIED")
            return
        }

        // 启动命令监听（后台线程）
        commandReceiver.startListeningAsync()

        // 启动微信监听（主线程）
        monitor.startMonitoring()

        // 运行 RunLoop
        RunLoop.main.run()
    }
}

// 启动 Agent
let agent = MacOSAgent()
agent.run()
```

## WeChat Monitoring with Accessibility API

### Finding WeChat Application

```swift
// WeChatMonitor.swift
import Cocoa
import ApplicationServices

class WeChatMonitor {
    private var monitoringTimer: Timer?
    private var lastMessageId: String?
    private let intervalMs: Int

    init(intervalMs: Int = 500) {
        self.intervalMs = intervalMs
    }

    func startMonitoring() {
        monitoringTimer = Timer.scheduledTimer(
            withTimeInterval: TimeInterval(intervalMs) / 1000.0,
            repeats: true
        ) { [weak self] _ in
            self?.checkForNewMessages()
        }
    }

    func stopMonitoring() {
        monitoringTimer?.invalidate()
        monitoringTimer = nil
    }

    private func checkForNewMessages() {
        guard let wechatApp = getWeChatApplication() else {
            return
        }

        if let messages = extractMessages(from: wechatApp) {
            if let latestMessage = messages.last {
                let messageId = generateMessageId(message: latestMessage)

                if messageId != lastMessageId {
                    lastMessageId = messageId
                    sendMessageToOrchestrator(message: latestMessage)
                }
            }
        }
    }

    private func getWeChatApplication() -> AXUIElement? {
        let runningApps = NSWorkspace.shared.runningApplications
        guard let wechatApp = runningApps.first(where: { $0.bundleIdentifier == "com.tencent.xinWeChat" }) else {
            return nil
        }

        return AXUIElementCreateApplication(wechatApp.processIdentifier)
    }

    private func extractMessages(from app: AXUIElement) -> [[String: String]]? {
        // 获取微信窗口
        var windowsValue: AnyObject?
        let windowsResult = AXUIElementCopyAttributeValue(
            app,
            kAXWindowsAttribute as CFString,
            &windowsValue
        )

        guard windowsResult == .success,
              let windows = windowsValue as? [AXUIElement],
              !windows.isEmpty else {
            return nil
        }

        // 遍历窗口查找聊天窗口
        for window in windows {
            if let messages = extractMessagesFromWindow(window: window) {
                return messages
            }
        }

        return nil
    }

    private func extractMessagesFromWindow(window: AXUIElement) -> [[String: String]]? {
        // 获取窗口的子元素
        var childrenValue: AnyObject?
        let childrenResult = AXUIElementCopyAttributeValue(
            window,
            kAXChildrenAttribute as CFString,
            &childrenValue
        )

        guard childrenResult == .success,
              let children = childrenValue as? [AXUIElement] else {
            return nil
        }

        // 递归查找消息列表
        // 具体实现需要根据微信的 UI 层次结构调整
        var messages: [[String: String]] = []

        for child in children {
            if let messageElements = findMessageElements(in: child) {
                messages.append(contentsOf: messageElements)
            }
        }

        return messages.isEmpty ? nil : messages
    }

    private func findMessageElements(in element: AXUIElement) -> [[String: String]]? {
        // 获取元素的 Role
        var roleValue: AnyObject?
        AXUIElementCopyAttributeValue(element, kAXRoleAttribute as CFString, &roleValue)

        guard let role = roleValue as? String else {
            return nil
        }

        // 查找文本元素（消息内容）
        if role == "AXStaticText" {
            var valueValue: AnyObject?
            AXUIElementCopyAttributeValue(element, kAXValueAttribute as CFString, &valueValue)

            if let content = valueValue as? String {
                return [["content": content, "sender": "Unknown", "timestamp": ""]]
            }
        }

        // 递归查找子元素
        var childrenValue: AnyObject?
        AXUIElementCopyAttributeValue(element, kAXChildrenAttribute as CFString, &childrenValue)

        if let children = childrenValue as? [AXUIElement] {
            var allMessages: [[String: String]] = []
            for child in children {
                if let messages = findMessageElements(in: child) {
                    allMessages.append(contentsOf: messages)
                }
            }
            return allMessages.isEmpty ? nil : allMessages
        }

        return nil
    }

    private func generateMessageId(message: [String: String]) -> String {
        let content = message["content"] ?? ""
        let sender = message["sender"] ?? ""
        let timestamp = message["timestamp"] ?? ""
        return "\(sender):\(timestamp):\(content.hashValue)"
    }

    private func sendMessageToOrchestrator(message: [String: String]) {
        MessageSender.sendMessageNew(
            content: message["content"] ?? "",
            sender: message["sender"] ?? "",
            timestamp: message["timestamp"] ?? ""
        )
    }
}
```

## Input Control with Accessibility API

```swift
// InputWriter.swift
import Cocoa
import ApplicationServices

class InputWriter {
    func writeToInput(content: String) -> Bool {
        guard let wechatApp = getWeChatApplication() else {
            MessageSender.sendError(message: "未找到微信应用", code: "APP_NOT_FOUND")
            return false
        }

        guard let inputField = findInputField(in: wechatApp) else {
            MessageSender.sendError(message: "未找到输入框", code: "INPUT_NOT_FOUND")
            return false
        }

        // 设置输入框的值
        var value = content as CFTypeRef
        let result = AXUIElementSetAttributeValue(
            inputField,
            kAXValueAttribute as CFString,
            value
        )

        if result == .success {
            return true
        } else {
            MessageSender.sendError(
                message: "写入失败: \(result.rawValue)",
                code: "WRITE_FAILED"
            )
            return false
        }
    }

    func clearInput() -> Bool {
        guard let wechatApp = getWeChatApplication() else {
            return false
        }

        guard let inputField = findInputField(in: wechatApp) else {
            return false
        }

        var value = "" as CFTypeRef
        let result = AXUIElementSetAttributeValue(
            inputField,
            kAXValueAttribute as CFString,
            value
        )

        return result == .success
    }

    private func getWeChatApplication() -> AXUIElement? {
        let runningApps = NSWorkspace.shared.runningApplications
        guard let wechatApp = runningApps.first(where: { $0.bundleIdentifier == "com.tencent.xinWeChat" }) else {
            return nil
        }
        return AXUIElementCreateApplication(wechatApp.processIdentifier)
    }

    private func findInputField(in app: AXUIElement) -> AXUIElement? {
        // 查找输入框
        // 需要遍历 UI 层次结构找到文本输入框（AXTextField）
        return findElement(in: app, role: "AXTextField")
    }

    private func findElement(in element: AXUIElement, role targetRole: String) -> AXUIElement? {
        var roleValue: AnyObject?
        AXUIElementCopyAttributeValue(element, kAXRoleAttribute as CFString, &roleValue)

        if let role = roleValue as? String, role == targetRole {
            return element
        }

        var childrenValue: AnyObject?
        AXUIElementCopyAttributeValue(element, kAXChildrenAttribute as CFString, &childrenValue)

        if let children = childrenValue as? [AXUIElement] {
            for child in children {
                if let found = findElement(in: child, role: targetRole) {
                    return found
                }
            }
        }

        return nil
    }
}
```

## IPC Communication

### Message Sender

```swift
// IPC/MessageSender.swift
import Foundation

class MessageSender {
    static func sendMessage(_ message: [String: Any]) {
        guard let jsonData = try? JSONSerialization.data(withJSONObject: message),
              let jsonString = String(data: jsonData, encoding: .utf8) else {
            return
        }

        print(jsonString)
        fflush(stdout)
    }

    static func sendMessageNew(content: String, sender: String, timestamp: String) {
        let message: [String: Any] = [
            "type": "MessageNew",
            "content": content,
            "sender": sender,
            "timestamp": timestamp
        ]
        sendMessage(message)
    }

    static func sendCommandResponse(success: Bool, error: String? = nil) {
        var message: [String: Any] = [
            "type": "CommandResponse",
            "success": success
        ]
        if let error = error {
            message["error"] = error
        }
        sendMessage(message)
    }

    static func sendError(message errorMessage: String, code: String? = nil) {
        var message: [String: Any] = [
            "type": "Error",
            "message": errorMessage
        ]
        if let code = code {
            message["code"] = code
        }
        sendMessage(message)
    }

    static func sendHealthStatus(status: String, agentType: String) {
        let message: [String: Any] = [
            "type": "HealthStatus",
            "status": status,
            "agent_type": agentType
        ]
        sendMessage(message)
    }
}
```

### Command Receiver

```swift
// IPC/CommandReceiver.swift
import Foundation

class CommandReceiver {
    private var handlers: [String: ([String: Any]) -> Bool] = [:]
    private var running = true

    func registerHandler(commandType: String, handler: @escaping ([String: Any]) -> Bool) {
        handlers[commandType] = handler
    }

    func startListening() {
        while running {
            guard let line = readLine() else {
                break
            }

            guard let data = line.data(using: .utf8),
                  let command = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
                MessageSender.sendError(message: "JSON 解析失败", code: "JSON_PARSE_ERROR")
                continue
            }

            handleCommand(command)
        }
    }

    func startListeningAsync() {
        DispatchQueue.global(qos: .userInitiated).async {
            self.startListening()
        }
    }

    private func handleCommand(_ command: [String: Any]) {
        guard let commandType = command["type"] as? String else {
            MessageSender.sendError(message: "命令缺少 type 字段", code: "INVALID_COMMAND")
            return
        }

        guard let handler = handlers[commandType] else {
            MessageSender.sendError(message: "未知命令类型: \(commandType)", code: "UNKNOWN_COMMAND")
            return
        }

        let success = handler(command)
        MessageSender.sendCommandResponse(success: success)
    }

    func stop() {
        running = false
    }
}
```

## Error Handling

### Accessibility API Error Handling

```swift
func safelyAccessElement(_ element: AXUIElement, attribute: String) -> AnyObject? {
    var value: AnyObject?
    let result = AXUIElementCopyAttributeValue(element, attribute as CFString, &value)

    switch result {
    case .success:
        return value
    case .failure:
        MessageSender.sendError(message: "访问元素失败", code: "AX_FAILURE")
        return nil
    case .invalidUIElement:
        MessageSender.sendError(message: "无效的 UI 元素", code: "AX_INVALID_ELEMENT")
        return nil
    case .cannotComplete:
        MessageSender.sendError(message: "操作无法完成", code: "AX_CANNOT_COMPLETE")
        return nil
    default:
        MessageSender.sendError(message: "未知错误: \(result.rawValue)", code: "AX_UNKNOWN")
        return nil
    }
}
```

## Building and Deployment

### Swift Package Manager

```swift
// Package.swift
// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "MacOSAgent",
    platforms: [
        .macOS(.v11)
    ],
    products: [
        .executable(name: "macos_agent", targets: ["MacOSAgent"])
    ],
    targets: [
        .executableTarget(
            name: "MacOSAgent",
            dependencies: []
        )
    ]
)
```

### Building

```bash
# 构建
swift build -c release

# 输出：.build/release/macos_agent

# 运行
.build/release/macos_agent
```

## Testing

### Unit Tests

```swift
// Tests/MacOSAgentTests/MessageSenderTests.swift
import XCTest
@testable import MacOSAgent

final class MessageSenderTests: XCTestCase {
    func testSendMessageNew() {
        // 测试消息发送
        // 需要模拟 stdout 捕获
    }
}
```

## When to Use This Skill

Activate this skill when:
- Developing macOS Platform Agent
- Working with Accessibility API
- Implementing Swift-based automation
- Handling UI element inspection
- Testing macOS Agent
- Building Swift applications
- Debugging Accessibility issues
