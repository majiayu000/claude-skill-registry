---
name: temet-run-tui-patterns
description: |
  Builds temet-run TUI components following project patterns for daemon monitoring, agent management, and observability integration. Use when implementing agent dashboards, status displays, log viewers, multi-agent layouts, IPC integration, and OpenTelemetry instrumentation in Textual widgets. Specific to temet-run's architecture and requirements.
allowed-tools: Read, Write, Edit, Bash
---

# temet-run TUI Patterns

## Purpose
Implement temet-run TUI components following the project's functional programming principles, type safety, observability patterns, and daemon/agent architecture. This skill covers patterns specific to monitoring autonomous agents.

## Quick Start

```python
from temet_run.config import Settings
from temet_run.tui.widgets import AgentListWidget
from textual.app import App, ComposeResult

class TemedRunTUI(App):
    """temet-run TUI dashboard."""

    def __init__(self) -> None:
        super().__init__()
        self._settings = Settings()

    def compose(self) -> ComposeResult:
        yield AgentListWidget(
            settings=self._settings,
            id="agent-list",
        )

    async def on_mount(self) -> None:
        """Initialize dashboard."""
        self._settings = Settings()
        agent_list = self.query_one("#agent-list", AgentListWidget)
        await agent_list.refresh_agents()
```

## Instructions

### Step 1: Integrate with Settings Configuration

Use temet-run's Pydantic Settings for configuration:

```python
from temet_run.config import Settings
from textual.widgets import Static
from textual.app import ComposeResult

class DaemonMonitorWidget(Static):
    """Monitor daemon using temet-run settings."""

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        try:
            self._settings = Settings()  # Loads from .env and environment
        except Exception as e:
            self._settings = None
            self._error = str(e)

    def render(self) -> str:
        """Render daemon paths."""
        if not self._settings:
            return f"Configuration error: {self._error}"

        return (
            f"PID Dir: {self._settings.daemon_pid_file.parent}\n"
            f"Socket Dir: {self._settings.daemon_socket_path.parent}\n"
            f"Log Dir: {self._settings.log_dir}\n"
            f"Memory Dir: {self._settings.memory_dir}"
        )

    def get_agent_paths(self, agent_id: str) -> dict[str, Path]:
        """Get paths for specific agent."""
        if not self._settings:
            return {}

        return {
            "pid_file": self._settings.get_agent_pid_file(agent_id),
            "socket": self._settings.get_agent_socket_path(agent_id),
            "log": self._settings.get_agent_log_file(agent_id),
        }
```

**Settings Pattern:**
- Settings loads from `.env` and environment variables
- Use `Settings()` to create validated config
- Call `get_agent_pid_file(agent_id)` to get agent-specific paths
- Handle `ValidationError` for invalid configuration

### Step 2: Implement Agent Discovery and Status Checking

Monitor running agents using PID files:

```python
import os
from pathlib import Path
from textual.widgets import Static
from temet_run.config import Settings
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentStatus:
    """Agent status information."""
    agent_id: str
    is_running: bool
    pid: int | None
    status: str  # "running", "idle", "busy", "stopped"

class AgentDiscoveryMixin:
    """Mixin for discovering running agents."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def _find_running_agents(self) -> list[AgentStatus]:
        """Discover all running agents from PID files.

        Returns:
            List of running agent statuses.
        """
        statuses: list[AgentStatus] = []
        pid_dir = self._settings.daemon_pid_file.parent

        if not pid_dir.exists():
            return statuses

        # Find all temet-run PID files
        pid_files = list(pid_dir.glob("temet-run-*.pid"))

        for pid_file in sorted(pid_files):
            # Extract agent_id from filename: temet-run-{agent_id}.pid
            agent_id = pid_file.stem.replace("temet-run-", "")

            # Read PID and check if process exists
            try:
                pid_str = pid_file.read_text().strip()
                pid = int(pid_str)

                # Signal 0 check: raises ProcessLookupError if not running
                os.kill(pid, 0)

                status = AgentStatus(
                    agent_id=agent_id,
                    is_running=True,
                    pid=pid,
                    status="running",  # TODO: Get actual status via IPC
                )
                statuses.append(status)

            except (ValueError, OSError, ProcessLookupError):
                # PID file invalid or process not running
                statuses.append(AgentStatus(
                    agent_id=agent_id,
                    is_running=False,
                    pid=None,
                    status="stopped",
                ))

        return statuses
```

**Discovery Pattern:**
- Check PID files in `settings.daemon_pid_file.parent`
- Files named `temet-run-{agent_id}.pid`
- Use `os.kill(pid, 0)` to check if process exists
- Handle stale PID files gracefully

### Step 3: Integrate IPC for Agent Communication

Use IPCClient to communicate with running agents:

```python
import asyncio
from temet_run.ipc.client import IPCClient
from textual.widgets import Static

class AgentCommandWidget(Static):
    """Send commands to agent via IPC."""

    def __init__(self, agent_id: str, socket_path: Path, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._agent_id = agent_id
        self._socket_path = socket_path
        self._response = ""

    async def execute_command(self, prompt: str) -> str:
        """Execute command on agent via IPC.

        Args:
            prompt: User prompt/command.

        Returns:
            Agent response text.

        Raises:
            FileNotFoundError: If agent socket not found.
            ConnectionError: If IPC connection fails.
        """
        if not self._socket_path.exists():
            msg = f"Agent socket not found: {self._socket_path}"
            raise FileNotFoundError(msg)

        response_parts: list[str] = []

        try:
            async with IPCClient(self._socket_path) as client:
                # Stream responses from agent
                async for response in client.execute_command(prompt=prompt):
                    response_type = response.get("type")

                    if response_type == "message_response":
                        content = response.get("content", "")
                        if isinstance(content, str):
                            response_parts.append(content)

                    elif response_type == "status_response":
                        status = response.get("status")
                        if status == "completed":
                            self._response = "".join(response_parts)
                            return self._response
                        elif status == "failed":
                            error = response.get("error", "Unknown error")
                            raise RuntimeError(f"Agent error: {error}")

        except Exception as e:
            msg = f"IPC communication failed: {e}"
            raise RuntimeError(msg) from e

        return self._response

    async def get_agent_status(self) -> dict[str, object]:
        """Get agent status via IPC.

        Returns:
            Status dict with agent information.
        """
        async with IPCClient(self._socket_path) as client:
            response = await client.get_status()
            return response
```

**IPC Pattern:**
- Check socket exists before connecting
- Use `async with IPCClient(path)` for safe connection
- Stream responses for long operations
- Handle connection errors gracefully
- Log errors via observability system

### Step 4: Implement Observability Instrumentation

Add OpenTelemetry tracing to TUI widgets:

```python
from temet_run.observability import get_logger, instrument_async
from textual.widgets import Static
import asyncio

logger = get_logger(__name__)

class ObservedWidget(Static):
    """Widget with OpenTelemetry instrumentation."""

    async def refresh_data(self) -> None:
        """Refresh data with tracing."""
        with logger.context("refresh_data", widget_id=self.id):
            try:
                data = await self._fetch_data()
                await self._update_display(data)
                logger.info("refresh_complete", items_loaded=len(data))
            except Exception as e:
                logger.exception("refresh_failed", error=str(e))

    @instrument_async
    async def _fetch_data(self) -> list[dict]:
        """Fetch data with automatic tracing."""
        # Decorated function automatically creates spans
        await asyncio.sleep(0.5)
        return [{"id": "1", "status": "running"}]

    async def _update_display(self, data: list[dict]) -> None:
        """Update widget display."""
        logger.debug("updating_display", item_count=len(data))
        # Update UI
```

**Observability Pattern:**
- Import logger: `from temet_run.observability import get_logger`
- Use `logger.context()` for structured context
- Log at appropriate levels: debug, info, warning, exception
- Use `@instrument_async` decorator for automatic spans
- Include relevant fields in log context

### Step 5: Implement Auto-Refresh with Timers

Set up periodic refresh with proper lifecycle:

```python
from textual.widgets import Static
from temet_run.observability import get_logger

logger = get_logger(__name__)

class AutoRefreshWidget(Static):
    """Widget with auto-refresh timer."""

    REFRESH_INTERVAL = 3.0  # Seconds

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._timer_id: str | None = None
        self._last_error: str | None = None

    async def on_mount(self) -> None:
        """Set up auto-refresh on mount."""
        # Initial load with notification
        try:
            await self._refresh_with_notification()
        except Exception as e:
            self._last_error = str(e)
            logger.exception("initial_refresh_failed", error=str(e))

        # Set up periodic auto-refresh (silent)
        self._timer_id = self.set_interval(
            self.REFRESH_INTERVAL,
            self._on_refresh_timer,
        )

    def _on_refresh_timer(self) -> None:
        """Timer callback - silent refresh."""
        self.run_worker(self._refresh_silent())

    async def _refresh_with_notification(self) -> None:
        """Refresh and show notification."""
        await self._do_refresh()
        self.app.notify("Dashboard refreshed", severity="information")

    async def _refresh_silent(self) -> None:
        """Refresh silently (errors logged, no notification)."""
        try:
            await self._do_refresh()
        except Exception as e:
            self._last_error = str(e)
            logger.debug("silent_refresh_failed", error=str(e))

    async def _do_refresh(self) -> None:
        """Core refresh logic."""
        # Override in subclasses
        pass

    def on_unmount(self) -> None:
        """Clean up timer on unmount."""
        if self._timer_id:
            self.remove_timer(self._timer_id)
            self._timer_id = None
```

**Auto-Refresh Pattern:**
- Set interval in `on_mount()`
- Use `run_worker()` for async refresh
- Silent refresh hides errors, user-triggered refresh notifies
- Clean up timer in `on_unmount()`
- Log errors for debugging

### Step 6: Follow Type Safety and Functional Patterns

Implement widgets with temet-run's quality standards:

```python
from typing import Any, TypedDict
from dataclasses import dataclass
from textual.widgets import Static
from textual.app import ComposeResult

@dataclass(frozen=True)
class AgentMetric:
    """Immutable agent metric data."""
    agent_id: str
    cpu_percent: float
    memory_percent: float
    task_count: int

class TypeSafeWidget(Static):
    """Widget with full type annotations."""

    def __init__(
        self,
        agent_id: str,
        metrics: list[AgentMetric] | None = None,
        *,
        name: str | None = None,
        id: str | None = None,  # noqa: A002
    ) -> None:
        """Initialize widget with type hints.

        Args:
            agent_id: Agent identifier.
            metrics: Historical metrics data.
            name: Widget name.
            id: Widget ID.

        Raises:
            ValueError: If agent_id is empty.
        """
        super().__init__(name=name, id=id)

        if not agent_id:
            msg = "agent_id cannot be empty"
            raise ValueError(msg)

        self._agent_id: str = agent_id
        self._metrics: list[AgentMetric] = metrics or []

    def render(self) -> str:
        """Render widget with type hints.

        Returns:
            Rendered widget content.
        """
        if not self._metrics:
            return "No metrics available"

        latest = self._metrics[-1]
        return (
            f"Agent: {latest.agent_id}\n"
            f"CPU: {latest.cpu_percent:.1f}%\n"
            f"Memory: {latest.memory_percent:.1f}%\n"
            f"Tasks: {latest.task_count}"
        )

    def add_metric(self, metric: AgentMetric) -> None:
        """Add metric point (immutable append).

        Args:
            metric: New metric to add.
        """
        # Create new list (functional style)
        self._metrics = self._metrics + [metric]
        self.refresh()

    def get_stats(self) -> dict[str, float] | None:
        """Get current statistics.

        Returns:
            Stats dict or None if no metrics.
        """
        if not self._metrics:
            return None

        latest = self._metrics[-1]
        return {
            "cpu": latest.cpu_percent,
            "memory": latest.memory_percent,
            "tasks": float(latest.task_count),
        }
```

**Type Safety Pattern:**
- Full type hints on all functions
- Use `TypedDict` and `dataclass` for structured data
- Use immutable data (frozen dataclasses)
- Raise specific exceptions with context
- Return `Optional` types explicitly

## Examples

### Example 1: Complete Agent Dashboard Widget

```python
from temet_run.config import Settings
from temet_run.tui.widgets.daemon_status.daemon_status import DaemonStatusWidget
from temet_run.observability import get_logger
from textual.widgets import Static
from textual.containers import Vertical
from textual.app import ComposeResult
from dataclasses import dataclass

logger = get_logger(__name__)

@dataclass(frozen=True)
class DashboardState:
    """Immutable dashboard state."""
    agents: list[str]
    last_refresh: str
    refresh_count: int

class AgentDashboard(Vertical):
    """temet-run agent dashboard."""

    REFRESH_INTERVAL = 3.0

    def __init__(self, settings: Settings, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._settings = settings
        self._state = DashboardState(
            agents=[],
            last_refresh="Never",
            refresh_count=0,
        )
        self._timer_id: str | None = None

    def compose(self) -> ComposeResult:
        """Compose dashboard."""
        yield Static("Agent Dashboard", id="title")
        yield Vertical(id="agents-container")
        yield Static("", id="status-bar")

    async def on_mount(self) -> None:
        """Initialize dashboard."""
        self._timer_id = self.set_interval(
            self.REFRESH_INTERVAL,
            self._on_refresh_timer,
        )
        await self._refresh_agents()

    def _on_refresh_timer(self) -> None:
        """Periodic refresh callback."""
        self.run_worker(self._refresh_agents())

    async def _refresh_agents(self) -> None:
        """Discover and display agents."""
        try:
            agents = self._find_running_agents()
            container = self.query_one("#agents-container", Vertical)
            await container.remove_children()

            if not agents:
                await container.mount(
                    Static("No agents running", id="no-agents-msg")
                )
                return

            for agent_id in agents:
                pid_file = self._settings.get_agent_pid_file(agent_id)
                socket_path = self._settings.get_agent_socket_path(agent_id)

                await container.mount(DaemonStatusWidget(
                    pid_file=pid_file,
                    socket_path=socket_path,
                    agent_id=agent_id,
                ))

            # Update state
            self._state = DashboardState(
                agents=agents,
                last_refresh=str(datetime.now()),
                refresh_count=self._state.refresh_count + 1,
            )

            # Update status bar
            status = self.query_one("#status-bar", Static)
            status.update(
                f"Agents: {len(agents)} | "
                f"Refreshed: {self._state.last_refresh} | "
                f"Updates: {self._state.refresh_count}"
            )

        except Exception as e:
            logger.exception("dashboard_refresh_failed", error=str(e))
            self.app.notify(
                f"Dashboard refresh error: {e}",
                severity="error",
            )

    def _find_running_agents(self) -> list[str]:
        """Find running agents from PID files."""
        agents = []
        pid_dir = self._settings.daemon_pid_file.parent

        if not pid_dir.exists():
            return agents

        for pid_file in sorted(pid_dir.glob("temet-run-*.pid")):
            agent_id = pid_file.stem.replace("temet-run-", "")

            try:
                pid = int(pid_file.read_text().strip())
                os.kill(pid, 0)
                agents.append(agent_id)
            except (ValueError, OSError, ProcessLookupError):
                # Stale PID file
                with contextlib.suppress(OSError):
                    pid_file.unlink()

        return agents

    def on_unmount(self) -> None:
        """Cleanup on unmount."""
        if self._timer_id:
            self.remove_timer(self._timer_id)
```

## Requirements
- Textual >= 0.45.0
- temet-run installed with all dependencies
- Understanding of temet-run's daemon, IPC, and observability systems

## Architecture Guidelines

**Follow temet-run principles:**
1. **Functional programming** - Immutable data, pure functions
2. **Type safety** - Full type hints, no `Any` without justification
3. **Error handling** - Explicit exceptions, no silent failures
4. **Observability** - Structured logging with context
5. **Testing** - Unit tests for widgets, integration tests for workflows
6. **Async patterns** - Use `async`/`await` properly, handle cancellation

## Common Patterns Summary

| Pattern | When | Example |
|---------|------|---------|
| Discovery | Start app, periodic refresh | Find running agents from PID files |
| IPC | Agent interaction | Send commands, get status |
| Auto-refresh | Real-time updates | Periodic refresh with timer |
| State management | Complex widgets | Use immutable dataclasses |
| Error handling | Operations | Log with context, notify user |
| Observability | Debugging | Structured logging, spans |

## See Also
- [textual-app-lifecycle.md](../textual-app-lifecycle) - App setup and lifecycle
- [textual-widget-development.md](../textual-widget-development) - Widget building
- [textual-data-display.md](../textual-data-display) - Displaying agent data
