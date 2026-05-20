---
name: ipc-communication
description: 当用户要求"IPC 通信"、"进程通信"、"Agent 协议"、"stdin/stdout"、"JSON 消息"、"Orchestrator 通信"、"消息序列化"，或者提到"进程间通信"、"Agent 集成"、"消息协议"时使用此技能。用于实现 Rust Orchestrator 和 Platform Agents 之间的 IPC 通信，包括消息格式定义、序列化、错误处理和性能优化。
version: 1.0.0
---

# IPC Communication Skill

Expert guidance for implementing Inter-Process Communication between Rust Orchestrator and Platform Agents using JSON protocol via stdin/stdout.

## Overview

WeReply uses JSON-based IPC protocol for communication:
- **Protocol**: JSON messages via stdin/stdout
- **Direction**: Bidirectional (Orchestrator ↔ Agent)
- **Message Format**: Line-delimited JSON (one message per line)
- **Character Encoding**: UTF-8

## Message Protocol Design

### Message Types

```rust
use serde::{Deserialize, Serialize};
use specta::Type;

// Agent → Orchestrator 消息
#[derive(Serialize, Deserialize, Type, Debug)]
#[serde(tag = "type")]
pub enum AgentMessage {
    MessageNew {
        content: String,
        sender: String,
        timestamp: String,
    },
    CommandResponse {
        success: bool,
        #[serde(skip_serializing_if = "Option::is_none")]
        error: Option<String>,
    },
    HealthStatus {
        status: String,  // "ok", "degraded", "error"
        agent_type: String,  // "windows_wxauto", "macos_accessibility"
    },
    Heartbeat {
        timestamp: f64,
    },
    Error {
        message: String,
        #[serde(skip_serializing_if = "Option::is_none")]
        code: Option<String>,
    },
}

// Orchestrator → Agent 消息
#[derive(Serialize, Deserialize, Type, Debug)]
#[serde(tag = "type")]
pub enum OrchestratorCommand {
    WriteInput {
        content: String,
    },
    ClearInput,
    HealthCheck,
    Stop,
}
```

### Message Format Examples

```json
// Agent → Orchestrator: 新消息
{
  "type": "MessageNew",
  "content": "你好，最近怎么样？",
  "sender": "张三",
  "timestamp": "2024-01-23T10:30:00"
}

// Orchestrator → Agent: 写入输入框
{
  "type": "WriteInput",
  "content": "很好，谢谢！"
}

// Agent → Orchestrator: 命令响应
{
  "type": "CommandResponse",
  "success": true
}

// Agent → Orchestrator: 错误
{
  "type": "Error",
  "message": "无法访问微信窗口",
  "code": "ACCESS_DENIED"
}
```

## Rust Orchestrator Implementation

### Agent Process Manager

```rust
use tokio::process::{Child, Command};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use std::process::Stdio;

pub struct AgentProcess {
    child: Child,
    stdin: tokio::process::ChildStdin,
    stdout_reader: BufReader<tokio::process::ChildStdout>,
}

impl AgentProcess {
    pub async fn spawn(agent_path: &str) -> anyhow::Result<Self> {
        let mut child = Command::new(agent_path)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()?;

        let stdin = child.stdin.take()
            .ok_or_else(|| anyhow!("无法获取 Agent stdin"))?;

        let stdout = child.stdout.take()
            .ok_or_else(|| anyhow!("无法获取 Agent stdout"))?;

        let stdout_reader = BufReader::new(stdout);

        Ok(Self {
            child,
            stdin,
            stdout_reader,
        })
    }

    pub async fn send_command(&mut self, command: OrchestratorCommand) -> anyhow::Result<()> {
        let json = serde_json::to_string(&command)?;
        self.stdin.write_all(json.as_bytes()).await?;
        self.stdin.write_all(b"\n").await?;
        self.stdin.flush().await?;
        Ok(())
    }

    pub async fn read_message(&mut self) -> anyhow::Result<AgentMessage> {
        let mut line = String::new();
        self.stdout_reader.read_line(&mut line).await?;

        if line.is_empty() {
            return Err(anyhow!("Agent 已关闭输出"));
        }

        let message = serde_json::from_str(&line)?;
        Ok(message)
    }

    pub async fn kill(&mut self) -> anyhow::Result<()> {
        self.child.kill().await?;
        Ok(())
    }
}
```

### Message Handler Pattern

```rust
use tokio::sync::mpsc;

pub struct AgentHandler {
    agent: AgentProcess,
    message_tx: mpsc::UnboundedSender<AgentMessage>,
}

impl AgentHandler {
    pub async fn start(agent_path: &str) -> anyhow::Result<(Self, mpsc::UnboundedReceiver<AgentMessage>)> {
        let agent = AgentProcess::spawn(agent_path).await?;
        let (message_tx, message_rx) = mpsc::unbounded_channel();

        let handler = Self {
            agent,
            message_tx,
        };

        Ok((handler, message_rx))
    }

    pub async fn run(mut self) {
        loop {
            match self.agent.read_message().await {
                Ok(message) => {
                    if self.message_tx.send(message).is_err() {
                        tracing::error!("消息接收器已关闭");
                        break;
                    }
                }
                Err(e) => {
                    tracing::error!(error = %e, "读取 Agent 消息失败");
                    break;
                }
            }
        }
    }

    pub async fn send_command(&mut self, command: OrchestratorCommand) -> anyhow::Result<()> {
        self.agent.send_command(command).await
    }
}
```

### Error Handling with Timeout

```rust
use tokio::time::{timeout, Duration};

pub async fn send_command_with_timeout(
    agent: &mut AgentProcess,
    command: OrchestratorCommand,
    timeout_secs: u64,
) -> anyhow::Result<()> {
    timeout(
        Duration::from_secs(timeout_secs),
        agent.send_command(command)
    )
    .await
    .map_err(|_| anyhow!("发送命令超时"))?
}

pub async fn read_message_with_timeout(
    agent: &mut AgentProcess,
    timeout_secs: u64,
) -> anyhow::Result<AgentMessage> {
    timeout(
        Duration::from_secs(timeout_secs),
        agent.read_message()
    )
    .await
    .map_err(|_| anyhow!("读取消息超时"))?
}
```

## Python Agent Implementation

### Message Sender Pattern

```python
import json
import sys
from typing import Dict, Any

class MessageSender:
    """发送消息到 Rust Orchestrator (stdout)"""

    @staticmethod
    def send_message(message: Dict[str, Any]):
        """
        发送 JSON 消息到 stdout

        Args:
            message: 消息字典，必须包含 'type' 字段
        """
        json_str = json.dumps(message, ensure_ascii=False)
        print(json_str, flush=True)

    @staticmethod
    def send_message_new(content: str, sender: str, timestamp: str):
        """发送新消息通知"""
        message = {
            "type": "MessageNew",
            "content": content,
            "sender": sender,
            "timestamp": timestamp
        }
        MessageSender.send_message(message)

    @staticmethod
    def send_command_response(success: bool, error: str = None):
        """发送命令响应"""
        message = {
            "type": "CommandResponse",
            "success": success
        }
        if error:
            message["error"] = error
        MessageSender.send_message(message)

    @staticmethod
    def send_error(error_message: str, code: str = None):
        """发送错误"""
        message = {
            "type": "Error",
            "message": error_message
        }
        if code:
            message["code"] = code
        MessageSender.send_message(message)

    @staticmethod
    def send_heartbeat(timestamp: float):
        """发送心跳"""
        message = {
            "type": "Heartbeat",
            "timestamp": timestamp
        }
        MessageSender.send_message(message)
```

### Command Receiver Pattern

```python
import threading
from typing import Callable, Dict, Any

class CommandReceiver:
    """从 Rust Orchestrator 接收命令 (stdin)"""

    def __init__(self):
        self.handlers: Dict[str, Callable] = {}
        self.running = True

    def register_handler(self, command_type: str, handler: Callable):
        """注册命令处理器"""
        self.handlers[command_type] = handler

    def start_listening(self):
        """开始监听命令（阻塞）"""
        try:
            for line in sys.stdin:
                if not self.running:
                    break

                try:
                    command = json.loads(line.strip())
                    self.handle_command(command)
                except json.JSONDecodeError as e:
                    MessageSender.send_error(f"JSON 解析失败: {str(e)}", "JSON_PARSE_ERROR")
                except Exception as e:
                    MessageSender.send_error(f"处理命令失败: {str(e)}", "COMMAND_HANDLER_ERROR")

        except KeyboardInterrupt:
            pass
        except Exception as e:
            MessageSender.send_error(f"命令监听错误: {str(e)}", "LISTENER_ERROR")

    def start_listening_async(self):
        """在后台线程中监听命令"""
        thread = threading.Thread(target=self.start_listening, daemon=True)
        thread.start()
        return thread

    def handle_command(self, command: Dict[str, Any]):
        """处理收到的命令"""
        command_type = command.get('type')

        if command_type not in self.handlers:
            MessageSender.send_error(f"未知命令类型: {command_type}", "UNKNOWN_COMMAND")
            return

        try:
            handler = self.handlers[command_type]
            result = handler(command)

            # 如果处理器返回 True，发送成功响应
            if result is True or result is None:
                MessageSender.send_command_response(success=True)
            elif result is False:
                MessageSender.send_command_response(success=False, error="处理失败")

        except Exception as e:
            MessageSender.send_command_response(success=False, error=str(e))

    def stop(self):
        """停止监听"""
        self.running = False
```

### Complete Agent Example

```python
from wechat_monitor import WeChatMonitor
from input_writer import WeChatInputWriter

class Agent:
    def __init__(self):
        self.monitor = WeChatMonitor()
        self.input_writer = WeChatInputWriter()
        self.command_receiver = CommandReceiver()

        # 注册命令处理器
        self.command_receiver.register_handler("WriteInput", self.handle_write_input)
        self.command_receiver.register_handler("ClearInput", self.handle_clear_input)
        self.command_receiver.register_handler("HealthCheck", self.handle_health_check)
        self.command_receiver.register_handler("Stop", self.handle_stop)

    def handle_write_input(self, command: Dict[str, Any]) -> bool:
        """处理写入输入框命令"""
        content = command.get('content', '')
        return self.input_writer.write_to_input(content)

    def handle_clear_input(self, command: Dict[str, Any]) -> bool:
        """处理清空输入框命令"""
        return self.input_writer.clear_input()

    def handle_health_check(self, command: Dict[str, Any]) -> bool:
        """处理健康检查"""
        message = {
            "type": "HealthStatus",
            "status": "ok",
            "agent_type": "windows_wxauto"
        }
        MessageSender.send_message(message)
        return None  # 不发送 CommandResponse

    def handle_stop(self, command: Dict[str, Any]) -> bool:
        """处理停止命令"""
        self.command_receiver.stop()
        return True

    def run(self):
        """启动 Agent"""
        # 启动命令监听（后台线程）
        self.command_receiver.start_listening_async()

        # 启动微信监听（主线程，阻塞）
        self.monitor.start_monitoring()

if __name__ == '__main__':
    agent = Agent()
    agent.run()
```

## Swift Agent Implementation

### Message Sender Pattern

```swift
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
}
```

### Command Receiver Pattern

```swift
class CommandReceiver {
    private var handlers: [String: (([String: Any]) -> Bool)] = [:]
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

## Message Validation

### Rust Validation

```rust
pub fn validate_agent_message(message: &AgentMessage) -> Result<(), String> {
    match message {
        AgentMessage::MessageNew { content, sender, .. } => {
            if content.is_empty() {
                return Err("消息内容为空".to_string());
            }
            if sender.is_empty() {
                return Err("发送者为空".to_string());
            }
            if content.len() > 100000 {
                return Err("消息内容过长".to_string());
            }
        }
        AgentMessage::Error { message, .. } => {
            if message.is_empty() {
                return Err("错误消息为空".to_string());
            }
        }
        _ => {}
    }
    Ok(())
}
```

### Python Validation

```python
def validate_command(command: Dict[str, Any]) -> bool:
    """验证命令格式"""
    # 检查必需字段
    if 'type' not in command:
        return False

    cmd_type = command['type']

    # 验证特定命令的字段
    if cmd_type == 'WriteInput':
        if 'content' not in command:
            return False
        content = command['content']
        if len(content) > 10000:  # 最大 10KB
            return False

    return True
```

## Performance Optimization

### Batch Message Processing

```rust
pub struct MessageBatcher {
    buffer: Vec<AgentMessage>,
    max_batch_size: usize,
    flush_interval: Duration,
    last_flush: Instant,
}

impl MessageBatcher {
    pub fn new(max_batch_size: usize, flush_interval: Duration) -> Self {
        Self {
            buffer: Vec::new(),
            max_batch_size,
            flush_interval,
            last_flush: Instant::now(),
        }
    }

    pub fn add_message(&mut self, message: AgentMessage) -> Option<Vec<AgentMessage>> {
        self.buffer.push(message);

        // 达到批量大小或超时，返回批次
        if self.buffer.len() >= self.max_batch_size
            || self.last_flush.elapsed() >= self.flush_interval
        {
            return Some(self.flush());
        }

        None
    }

    pub fn flush(&mut self) -> Vec<AgentMessage> {
        let messages = std::mem::take(&mut self.buffer);
        self.last_flush = Instant::now();
        messages
    }
}
```

### Async Message Queue

```rust
use tokio::sync::mpsc;

pub struct AsyncMessageQueue {
    tx: mpsc::UnboundedSender<AgentMessage>,
    rx: mpsc::UnboundedReceiver<AgentMessage>,
}

impl AsyncMessageQueue {
    pub fn new() -> Self {
        let (tx, rx) = mpsc::unbounded_channel();
        Self { tx, rx }
    }

    pub fn sender(&self) -> mpsc::UnboundedSender<AgentMessage> {
        self.tx.clone()
    }

    pub async fn receive(&mut self) -> Option<AgentMessage> {
        self.rx.recv().await
    }
}
```

## Testing

### Mock Agent Process

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tokio::io::{duplex, AsyncWriteExt};

    #[tokio::test]
    async fn test_send_command() {
        let (mut client, mut server) = duplex(1024);

        // 模拟发送命令
        let command = OrchestratorCommand::WriteInput {
            content: "测试内容".to_string(),
        };
        let json = serde_json::to_string(&command).unwrap();
        client.write_all(json.as_bytes()).await.unwrap();
        client.write_all(b"\n").await.unwrap();

        // 模拟接收
        let mut buf = String::new();
        use tokio::io::AsyncBufReadExt;
        let mut reader = BufReader::new(server);
        reader.read_line(&mut buf).await.unwrap();

        let received: OrchestratorCommand = serde_json::from_str(&buf).unwrap();
        match received {
            OrchestratorCommand::WriteInput { content } => {
                assert_eq!(content, "测试内容");
            }
            _ => panic!("错误的命令类型"),
        }
    }
}
```

## When to Use This Skill

Activate this skill when:
- Implementing IPC between Orchestrator and Agents
- Designing message protocols
- Working with stdin/stdout communication
- Handling JSON serialization/deserialization
- Implementing message validation
- Optimizing IPC performance
- Testing Agent communication
- Debugging IPC issues
