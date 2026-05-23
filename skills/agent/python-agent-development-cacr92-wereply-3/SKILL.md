---
name: python-agent-development
description: Python Agent 开发规范（Windows wxauto v4），包括项目结构、模块化、wxauto 使用、IPC 集成、错误处理、测试和部署。
version: 1.0.0
---

# Python Agent Development Skill (Windows)

Expert guidance for developing Windows Platform Agent using Python 3.12 + wxauto v4.

## Project Structure

```
platform_agents/windows_agent/
├── agent.py                # 主入口
├── wechat_monitor.py      # 微信监听模块
├── input_writer.py        # 输入框控制模块
├── ipc/                   # IPC 通信模块
│   ├── message_sender.py
│   └── command_receiver.py
├── utils/                 # 工具模块
│   ├── logger.py
│   └── config.py
├── requirements.txt       # 依赖列表
├── tests/                 # 测试目录
│   ├── test_monitor.py
│   └── test_writer.py
└── README.md
```

## Dependencies (requirements.txt)

```txt
wxauto==4.0.0
pywin32>=305
```

## Main Entry Point

```python
# agent.py
import sys
import time
from wechat_monitor import WeChatMonitor
from input_writer import WeChatInputWriter
from ipc.message_sender import MessageSender
from ipc.command_receiver import CommandReceiver

class WindowsAgent:
    def __init__(self):
        self.monitor = WeChatMonitor(interval_ms=500)
        self.input_writer = WeChatInputWriter()
        self.command_receiver = CommandReceiver()
        self.setup_command_handlers()

    def setup_command_handlers(self):
        """注册命令处理器"""
        self.command_receiver.register_handler("WriteInput", self.handle_write_input)
        self.command_receiver.register_handler("ClearInput", self.handle_clear_input)
        self.command_receiver.register_handler("HealthCheck", self.handle_health_check)
        self.command_receiver.register_handler("Stop", self.handle_stop)

    def handle_write_input(self, command):
        content = command.get('content', '')
        success = self.input_writer.write_to_input(content)
        return success

    def handle_clear_input(self, command):
        success = self.input_writer.clear_input()
        return success

    def handle_health_check(self, command):
        MessageSender.send_health_status("ok", "windows_wxauto")
        return None  # 不发送 CommandResponse

    def handle_stop(self, command):
        self.command_receiver.stop()
        return True

    def run(self):
        """启动 Agent"""
        try:
            # 启动命令监听（后台线程）
            self.command_receiver.start_listening_async()

            # 启动微信监听（主线程）
            self.monitor.start_monitoring()

        except KeyboardInterrupt:
            MessageSender.send_error("Agent 被用户中断")
        except Exception as e:
            MessageSender.send_error(f"Agent 运行错误: {str(e)}")
        finally:
            sys.exit(0)

if __name__ == '__main__':
    agent = WindowsAgent()
    agent.run()
```

## Code Organization Best Practices

### Modular Design

```python
# wechat_monitor.py
from wxauto import WeChat
from ipc.message_sender import MessageSender
import time

class WeChatMonitor:
    def __init__(self, interval_ms=500):
        self.wechat = WeChat()
        self.interval_ms = interval_ms
        self.last_message_id = None

    def start_monitoring(self):
        while True:
            try:
                messages = self.wechat.GetAllMessage()
                if messages:
                    self.process_messages(messages)
                time.sleep(self.interval_ms / 1000.0)
            except Exception as e:
                MessageSender.send_error(f"监听错误: {str(e)}")
                time.sleep(1)  # 错误后延迟

    def process_messages(self, messages):
        if not messages:
            return

        latest = messages[-1]
        message_id = self.generate_message_id(latest)

        if message_id != self.last_message_id:
            self.last_message_id = message_id
            MessageSender.send_message_new(
                content=latest.get('content', ''),
                sender=latest.get('sender', ''),
                timestamp=latest.get('time', '')
            )

    @staticmethod
    def generate_message_id(message):
        content = message.get('content', '')
        sender = message.get('sender', '')
        timestamp = message.get('time', '')
        return f"{sender}:{timestamp}:{hash(content)}"
```

### Type Hints

```python
from typing import Dict, Any, Optional, List

def process_command(command: Dict[str, Any]) -> Optional[bool]:
    """
    处理命令

    Args:
        command: 命令字典

    Returns:
        Optional[bool]: True 成功，False 失败，None 不需要响应
    """
    pass
```

## Error Handling

### Try-Except Patterns

```python
def safe_operation() -> bool:
    """执行可能失败的操作"""
    try:
        # 执行操作
        result = perform_operation()
        return True
    except SpecificException as e:
        # 处理特定异常
        MessageSender.send_error(f"操作失败: {str(e)}", "OPERATION_FAILED")
        return False
    except Exception as e:
        # 处理通用异常
        MessageSender.send_error(f"未知错误: {str(e)}", "UNKNOWN_ERROR")
        return False
```

### Graceful Degradation

```python
class RobustMonitor:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def start_with_retry(self):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                self.start_monitoring()
                break
            except Exception as e:
                retry_count += 1
                MessageSender.send_error(f"监听失败 (尝试 {retry_count}/{self.max_retries}): {str(e)}")
                if retry_count < self.max_retries:
                    time.sleep(2)
                else:
                    sys.exit(1)
```

## Logging

```python
# utils/logger.py
import logging
import sys

def setup_logger(name: str, level=logging.INFO):
    """设置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stderr)  # 输出到 stderr（不影响 stdout IPC）
    handler.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

# 使用
logger = setup_logger(__name__)
logger.info("Agent started")
logger.error("Error occurred", exc_info=True)
```

## Testing

### Unit Tests

```python
# tests/test_monitor.py
import unittest
from unittest.mock import Mock, patch
from wechat_monitor import WeChatMonitor

class TestWeChatMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = WeChatMonitor(interval_ms=500)

    def test_generate_message_id(self):
        message = {
            'content': '测试消息',
            'sender': '张三',
            'time': '2024-01-23 10:30:00'
        }
        message_id = WeChatMonitor.generate_message_id(message)
        self.assertIsInstance(message_id, str)
        self.assertIn('张三', message_id)

    @patch('wxauto.WeChat')
    def test_monitoring_initialization(self, mock_wechat):
        monitor = WeChatMonitor()
        self.assertEqual(monitor.interval_ms, 500)
        self.assertIsNone(monitor.last_message_id)

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

```python
# tests/test_integration.py
import unittest
import json
import sys
from io import StringIO
from agent import WindowsAgent

class TestAgentIntegration(unittest.TestCase):
    def test_command_handling(self):
        agent = WindowsAgent()

        # 模拟命令
        command = {"type": "HealthCheck"}
        result = agent.handle_health_check(command)

        self.assertIsNone(result)  # 健康检查不返回 CommandResponse
```

## Performance Optimization

### Memory Management

```python
class MemoryEfficientMonitor:
    def __init__(self):
        self.message_buffer_size = 100
        self.message_buffer = []

    def add_message(self, message):
        self.message_buffer.append(message)
        if len(self.message_buffer) > self.message_buffer_size:
            self.message_buffer = self.message_buffer[-self.message_buffer_size:]
            import gc
            gc.collect()
```

### Async Operations (Optional)

```python
import asyncio

class AsyncMonitor:
    async def monitor_async(self):
        """异步监听（可选）"""
        while True:
            messages = await asyncio.to_thread(self.wechat.GetAllMessage)
            if messages:
                self.process_messages(messages)
            await asyncio.sleep(self.interval_ms / 1000.0)
```

## Deployment

### Build Executable (PyInstaller)

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包为单文件可执行程序
pyinstaller --onefile --name windows_agent agent.py

# 输出：dist/windows_agent.exe
```

### Build Configuration (pyinstaller.spec)

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['agent.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['wxauto'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='windows_agent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 保留控制台（用于 stdin/stdout）
)
```

## Security Best Practices

### Input Validation

```python
def validate_content(content: str) -> bool:
    """验证输入内容"""
    if not content:
        return False
    if len(content) > 10000:  # 最大 10KB
        return False
    return True
```

### Avoid Hardcoded Credentials

```python
# ✓ Good - 从环境变量读取
import os
api_key = os.getenv('DEEPSEEK_API_KEY')

# ✗ Bad - 硬编码
api_key = "sk-xxxxx"  # 不要这样做
```

## When to Use This Skill

Activate this skill when:
- Developing Windows Platform Agent
- Working with wxauto library
- Implementing Python-based automation
- Handling IPC in Python
- Testing Python Agents
- Packaging Python applications
- Debugging Windows Agent issues
