---
name: wechat-automation
description: 当用户要求"微信监听"、"消息提取"、"Agent 开发"、"wxauto"、"Accessibility API"、"UI 自动化"、"输入框控制"、"Platform Agent"，或者提到"微信自动化"、"消息监控"、"WeChat monitoring"时使用此技能。用于开发 WeReply 的 Platform Agent（Windows wxauto 或 macOS Accessibility API）、实现微信消息监听、消息提取、输入框控制和 Agent 错误处理。
version: 1.0.0
---

# WeChat Automation Skill

Expert guidance for WeChat monitoring and automation using wxauto (Windows) and Accessibility API (macOS).

## Overview

WeReply uses Platform-specific Agents to monitor WeChat conversations and control the input box:
- **Windows Agent**: Python 3.12 + wxauto v4
- **macOS Agent**: Swift + Accessibility API
- **Communication**: JSON protocol via stdin/stdout with Rust Orchestrator

## Architecture Pattern

```
微信窗口
   ↓ (UI Automation)
Platform Agent
   ├→ 监听消息（定时轮询）
   ├→ 提取消息内容
   ├→ 发送到 Orchestrator (JSON via stdout)
   └→ 接收命令 (JSON via stdin)
       ↓
   控制输入框（写入建议）
```

## Windows Agent - wxauto v4

### Installation and Setup

```bash
# 安装依赖
pip install wxauto==4.0.0

# 确保微信已登录且窗口可见
```

### Message Monitoring Pattern

```python
import json
import time
import sys
from wxauto import WeChat

class WeChatMonitor:
    def __init__(self, interval_ms: int = 500):
        """
        初始化微信监听器

        Args:
            interval_ms: 监听间隔（毫秒），默认 500ms
        """
        self.wechat = WeChat()
        self.interval_ms = interval_ms
        self.last_message_id = None

    def start_monitoring(self):
        """开始监听微信消息"""
        try:
            while True:
                # 获取当前聊天窗口的最新消息
                messages = self.wechat.GetAllMessage()

                if messages and len(messages) > 0:
                    latest_message = messages[-1]

                    # 检查是否是新消息（避免重复处理）
                    message_id = self._generate_message_id(latest_message)
                    if message_id != self.last_message_id:
                        self.last_message_id = message_id
                        self._send_message_to_orchestrator(latest_message)

                # 间隔等待
                time.sleep(self.interval_ms / 1000.0)

        except KeyboardInterrupt:
            self._send_error("监听被用户中断")
        except Exception as e:
            self._send_error(f"监听错误: {str(e)}")

    def _generate_message_id(self, message) -> str:
        """生成消息唯一ID（用于去重）"""
        # 结合时间戳、发送者、内容生成ID
        content = message.get('content', '')
        sender = message.get('sender', '')
        timestamp = message.get('time', '')
        return f"{sender}:{timestamp}:{hash(content)}"

    def _send_message_to_orchestrator(self, message):
        """
        发送消息到 Rust Orchestrator

        格式：
        {
            "type": "MessageNew",
            "content": "消息内容",
            "sender": "发送者",
            "timestamp": "2024-01-23T10:30:00"
        }
        """
        payload = {
            "type": "MessageNew",
            "content": message.get('content', ''),
            "sender": message.get('sender', ''),
            "timestamp": message.get('time', '')
        }

        # 输出到 stdout（Rust 会读取）
        print(json.dumps(payload, ensure_ascii=False), flush=True)

    def _send_error(self, error_message: str):
        """发送错误信息到 Orchestrator"""
        payload = {
            "type": "Error",
            "message": error_message
        }
        print(json.dumps(payload, ensure_ascii=False), flush=True)

# 使用示例
if __name__ == '__main__':
    monitor = WeChatMonitor(interval_ms=500)
    monitor.start_monitoring()
```

### Input Box Control Pattern

```python
class WeChatInputWriter:
    def __init__(self):
        self.wechat = WeChat()

    def write_to_input(self, content: str) -> bool:
        """
        写入内容到微信输入框

        Args:
            content: 要写入的文本

        Returns:
            bool: 写入是否成功
        """
        try:
            # 使用 wxauto 写入输入框
            self.wechat.SendMsg(content)
            return True
        except Exception as e:
            self._send_error(f"写入失败: {str(e)}")
            return False

    def clear_input(self) -> bool:
        """清空输入框"""
        try:
            # wxauto v4 提供的清空方法
            self.wechat.ClearMsg()
            return True
        except Exception as e:
            self._send_error(f"清空失败: {str(e)}")
            return False

    def _send_error(self, error_message: str):
        """发送错误到 Orchestrator"""
        payload = {
            "type": "Error",
            "message": error_message
        }
        print(json.dumps(payload, ensure_ascii=False), flush=True)
```

### Command Handling Pattern

```python
import sys
import json
import threading

class AgentCommandHandler:
    def __init__(self):
        self.input_writer = WeChatInputWriter()
        self.running = True

    def start_command_listener(self):
        """监听来自 Orchestrator 的命令（stdin）"""
        thread = threading.Thread(target=self._listen_commands, daemon=True)
        thread.start()

    def _listen_commands(self):
        """从 stdin 读取命令"""
        try:
            for line in sys.stdin:
                if not self.running:
                    break

                try:
                    command = json.loads(line.strip())
                    self._handle_command(command)
                except json.JSONDecodeError:
                    self._send_error(f"无效的 JSON 命令: {line}")

        except Exception as e:
            self._send_error(f"命令监听错误: {str(e)}")

    def _handle_command(self, command: dict):
        """处理命令"""
        cmd_type = command.get('type')

        if cmd_type == 'WriteInput':
            content = command.get('content', '')
            success = self.input_writer.write_to_input(content)
            self._send_response(success)

        elif cmd_type == 'ClearInput':
            success = self.input_writer.clear_input()
            self._send_response(success)

        elif cmd_type == 'HealthCheck':
            self._send_health_status()

        else:
            self._send_error(f"未知命令类型: {cmd_type}")

    def _send_response(self, success: bool):
        """发送命令执行结果"""
        payload = {
            "type": "CommandResponse",
            "success": success
        }
        print(json.dumps(payload, ensure_ascii=False), flush=True)

    def _send_health_status(self):
        """发送健康状态"""
        payload = {
            "type": "HealthStatus",
            "status": "ok",
            "agent_type": "windows_wxauto"
        }
        print(json.dumps(payload, ensure_ascii=False), flush=True)

    def _send_error(self, error_message: str):
        """发送错误"""
        payload = {
            "type": "Error",
            "message": error_message
        }
        print(json.dumps(payload, ensure_ascii=False), flush=True)
```

## macOS Agent - Accessibility API

### Swift Implementation Pattern

```swift
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
        // 请求 Accessibility 权限
        if !AXIsProcessTrusted() {
            let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true]
            AXIsProcessTrustedWithOptions(options as CFDictionary)
            return
        }

        // 启动定时器
        monitoringTimer = Timer.scheduledTimer(
            withTimeInterval: TimeInterval(intervalMs) / 1000.0,
            repeats: true
        ) { [weak self] _ in
            self?.checkForNewMessages()
        }

        RunLoop.main.run()
    }

    private func checkForNewMessages() {
        guard let wechatApp = getWeChatApplication() else {
            return
        }

        // 使用 Accessibility API 获取消息
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
        // 使用 Accessibility API 提取消息列表
        // 这需要深入分析微信的 UI 层次结构

        var messagesValue: AnyObject?
        let result = AXUIElementCopyAttributeValue(app, kAXChildrenAttribute as CFString, &messagesValue)

        guard result == .success, let windows = messagesValue as? [AXUIElement] else {
            return nil
        }

        // 遍历窗口，找到聊天窗口，提取消息
        // 具体实现需要根据微信的 UI 结构调整

        return nil // Placeholder
    }

    private func generateMessageId(message: [String: String]) -> String {
        let content = message["content"] ?? ""
        let sender = message["sender"] ?? ""
        let timestamp = message["timestamp"] ?? ""
        return "\(sender):\(timestamp):\(content.hashValue)"
    }

    private func sendMessageToOrchestrator(message: [String: String]) {
        let payload: [String: Any] = [
            "type": "MessageNew",
            "content": message["content"] ?? "",
            "sender": message["sender"] ?? "",
            "timestamp": message["timestamp"] ?? ""
        ]

        if let jsonData = try? JSONSerialization.data(withJSONObject: payload),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            print(jsonString, terminator: "\n")
            fflush(stdout)
        }
    }
}
```

### Input Writer (Swift)

```swift
class WeChatInputWriter {
    func writeToInput(content: String) -> Bool {
        guard let wechatApp = getWeChatApplication() else {
            sendError(message: "未找到微信应用")
            return false
        }

        // 查找输入框
        guard let inputField = findInputField(in: wechatApp) else {
            sendError(message: "未找到输入框")
            return false
        }

        // 写入内容
        var value = content as CFTypeRef
        let result = AXUIElementSetAttributeValue(inputField, kAXValueAttribute as CFString, value)

        if result == .success {
            return true
        } else {
            sendError(message: "写入失败: \(result.rawValue)")
            return false
        }
    }

    private func findInputField(in app: AXUIElement) -> AXUIElement? {
        // 使用 Accessibility API 查找输入框
        // 需要遍历 UI 层次结构找到输入框元素
        return nil // Placeholder
    }

    private func getWeChatApplication() -> AXUIElement? {
        // 同上
        return nil
    }

    private func sendError(message: String) {
        let payload: [String: Any] = [
            "type": "Error",
            "message": message
        ]

        if let jsonData = try? JSONSerialization.data(withJSONObject: payload),
           let jsonString = String(data: jsonData, encoding: .utf8) {
            print(jsonString, terminator: "\n")
            fflush(stdout)
        }
    }
}
```

## Message Deduplication Strategy

### Time-based Deduplication

```python
from datetime import datetime, timedelta

class MessageDeduplicator:
    def __init__(self, window_seconds: int = 5):
        """
        消息去重器

        Args:
            window_seconds: 去重时间窗口（秒）
        """
        self.seen_messages = {}  # {message_id: timestamp}
        self.window_seconds = window_seconds

    def is_duplicate(self, message_id: str) -> bool:
        """检查消息是否重复"""
        now = datetime.now()

        # 清理过期的消息记录
        self._clean_old_messages(now)

        # 检查是否已见过
        if message_id in self.seen_messages:
            return True

        # 记录新消息
        self.seen_messages[message_id] = now
        return False

    def _clean_old_messages(self, now: datetime):
        """清理过期的消息记录"""
        cutoff = now - timedelta(seconds=self.window_seconds)
        self.seen_messages = {
            msg_id: timestamp
            for msg_id, timestamp in self.seen_messages.items()
            if timestamp > cutoff
        }
```

## Performance Optimization

### Polling Interval Tuning

```python
class AdaptiveMonitor:
    def __init__(self, min_interval_ms: int = 200, max_interval_ms: int = 1000):
        """
        自适应监听间隔

        当有活跃消息时，使用较短间隔（200ms）
        当长时间无消息时，逐渐增加到最大间隔（1000ms）
        """
        self.min_interval = min_interval_ms / 1000.0
        self.max_interval = max_interval_ms / 1000.0
        self.current_interval = self.min_interval
        self.idle_count = 0

    def get_next_interval(self, has_new_message: bool) -> float:
        """获取下次轮询间隔"""
        if has_new_message:
            # 有新消息，使用最短间隔
            self.current_interval = self.min_interval
            self.idle_count = 0
        else:
            # 无新消息，逐渐增加间隔
            self.idle_count += 1
            if self.idle_count > 5:  # 5次无消息后开始增加间隔
                self.current_interval = min(
                    self.current_interval * 1.2,
                    self.max_interval
                )

        return self.current_interval
```

### Memory Optimization

```python
import gc

class MemoryEfficientMonitor:
    def __init__(self):
        self.message_buffer_size = 100  # 只保留最近100条消息
        self.message_buffer = []

    def add_message(self, message):
        """添加消息到缓冲区"""
        self.message_buffer.append(message)

        # 超过缓冲区大小，清理旧消息
        if len(self.message_buffer) > self.message_buffer_size:
            self.message_buffer = self.message_buffer[-self.message_buffer_size:]
            gc.collect()  # 触发垃圾回收
```

## Error Handling and Recovery

### Graceful Degradation

```python
class RobustAgent:
    def __init__(self):
        self.max_retries = 3
        self.retry_delay_seconds = 2

    def monitor_with_retry(self):
        """带重试的监听"""
        retry_count = 0

        while retry_count < self.max_retries:
            try:
                self.start_monitoring()
                break  # 成功，跳出循环
            except Exception as e:
                retry_count += 1
                self._send_error(f"监听失败 (尝试 {retry_count}/{self.max_retries}): {str(e)}")

                if retry_count < self.max_retries:
                    time.sleep(self.retry_delay_seconds)
                else:
                    self._send_error("监听失败次数过多，Agent 退出")
                    sys.exit(1)
```

### Health Check

```python
class HealthMonitor:
    def __init__(self):
        self.last_heartbeat = time.time()
        self.heartbeat_interval = 10  # 每10秒发送一次心跳

    def send_heartbeat(self):
        """发送心跳到 Orchestrator"""
        payload = {
            "type": "Heartbeat",
            "timestamp": time.time(),
            "status": "ok"
        }
        print(json.dumps(payload, ensure_ascii=False), flush=True)
        self.last_heartbeat = time.time()
```

## Security Considerations

### Input Validation

```python
def validate_command(command: dict) -> bool:
    """验证来自 Orchestrator 的命令"""
    # 检查命令类型
    if 'type' not in command:
        return False

    cmd_type = command['type']

    # 只接受预定义的命令类型
    valid_types = ['WriteInput', 'ClearInput', 'HealthCheck', 'Stop']
    if cmd_type not in valid_types:
        return False

    # 验证内容长度（防止恶意超长内容）
    if cmd_type == 'WriteInput':
        content = command.get('content', '')
        if len(content) > 10000:  # 最大10KB
            return False

    return True
```

### Privacy Protection

```python
def sanitize_message_for_logging(message: dict) -> dict:
    """清理消息中的敏感信息（用于日志）"""
    sanitized = message.copy()

    # 不记录完整的消息内容
    if 'content' in sanitized:
        content = sanitized['content']
        if len(content) > 50:
            sanitized['content'] = content[:50] + '...'

    return sanitized
```

## Testing Guidelines

### Unit Testing

```python
import unittest
from unittest.mock import Mock, patch

class TestWeChatMonitor(unittest.TestCase):
    def test_message_deduplication(self):
        """测试消息去重"""
        deduplicator = MessageDeduplicator(window_seconds=5)

        message_id = "test_message_1"

        # 第一次应该不是重复
        self.assertFalse(deduplicator.is_duplicate(message_id))

        # 第二次应该是重复
        self.assertTrue(deduplicator.is_duplicate(message_id))

    @patch('wxauto.WeChat')
    def test_monitor_initialization(self, mock_wechat):
        """测试监听器初始化"""
        monitor = WeChatMonitor(interval_ms=500)
        self.assertEqual(monitor.interval_ms, 500)
        self.assertIsNone(monitor.last_message_id)
```

## When to Use This Skill

Activate this skill when:
- Implementing WeChat message monitoring
- Developing Platform Agents (Windows/macOS)
- Working with wxauto or Accessibility API
- Handling message extraction and deduplication
- Implementing input box control
- Optimizing Agent performance
- Handling Agent errors and recovery
- Setting up IPC communication with Orchestrator
