---
name: ros2-web-integration
description: >
  Patterns and best practices for integrating ROS2 systems with web technologies including REST APIs,
  WebSocket bridges, and browser-based robot interfaces. Use this skill when building web dashboards
  for robots, streaming camera feeds to browsers, exposing ROS2 services as REST endpoints, or
  implementing bidirectional WebSocket communication between web UIs and ROS2 nodes. Trigger whenever
  the user mentions rosbridge, rosbridge_suite, roslibjs, FastAPI with ROS2, Flask with rclpy,
  WebSocket for robot telemetry, MJPEG streaming, WebRTC for robots, REST API wrapping ROS2 services,
  web-based robot control, browser robot interface, robot dashboard, CORS configuration for robots,
  or any web-to-ROS2 bridge pattern. Also trigger for authentication on robot web interfaces, rate
  limiting sensor streams, video streaming from robot cameras to browsers, or running async web
  frameworks alongside the ROS2 executor. Covers rosbridge_suite, FastAPI, Flask, WebSocket, and
  WebRTC approaches.
---

# ROS2 Web Integration Skill

## When to Use This Skill
- Building a web dashboard to monitor or control a robot running ROS2
- Streaming camera feeds (MJPEG, WebRTC, compressed WebSocket) from a robot to a browser
- Exposing ROS2 services and actions as REST API endpoints
- Implementing bidirectional WebSocket communication between a web UI and ROS2 nodes
- Setting up rosbridge_suite for quick prototyping or foxglove integration
- Writing a custom FastAPI or Flask bridge to ROS2 for production deployments
- Adding authentication, rate limiting, or CORS to robot web interfaces
- Running an async web server (uvicorn) alongside the rclpy executor without deadlocks
- Publishing teleop commands from a browser joystick to cmd_vel
- Serving ROS2 parameter configuration pages or diagnostic dashboards over HTTP

## Architecture Overview

### Comparison Table

| Feature | rosbridge_suite | Custom FastAPI Bridge | Custom Flask Bridge |
|---|---|---|---|
| Latency | ~5-15ms (WebSocket) | ~2-5ms (WebSocket), ~10-30ms (REST) | ~10-50ms (REST only without extensions) |
| Throughput | Medium (JSON serialization overhead) | High (binary WebSocket, async) | Low-Medium (sync, GIL-bound) |
| Auth | Basic (rosauth, limited) | Full (JWT, OAuth2, API keys) | Full (Flask-Login, JWT) |
| Complexity | Low (launch and connect) | Medium (must manage two event loops) | Medium (must manage threading) |
| Video Streaming | Requires separate web_video_server | Native (MJPEG, WebSocket binary) | MJPEG via generator responses |
| Production Ready | No (exposes full topic graph) | Yes | Yes (with gunicorn) |
| When to Use | Prototyping, foxglove, quick demos | Production APIs, high-perf streaming | Simple internal tools, legacy systems |

### When to Use rosbridge vs Custom Bridge

Use **rosbridge_suite** when:
- You need a working bridge in under 10 minutes
- The client is foxglove, webviz, or another rosbridge-aware tool
- Security is not a concern (local network, demo environment)
- You do not need custom business logic between web and ROS2

Use a **custom bridge** (FastAPI/Flask) when:
- You need authentication, authorization, or rate limiting
- You want to expose only specific topics/services (not the entire ROS2 graph)
- You need to transform or aggregate data before sending to the client
- You need REST endpoints for integration with non-WebSocket clients
- You are streaming video and need control over encoding and quality
- The system is deployed in production or on a public network

## Pattern 1: rosbridge_suite

### Installation and Launch

```bash
# Install rosbridge_suite
sudo apt install ros-${ROS_DISTRO}-rosbridge-suite

# Launch with default settings (port 9090)
ros2 launch rosbridge_server rosbridge_websocket_launch.xml

# Launch with custom port and SSL
ros2 launch rosbridge_server rosbridge_websocket_launch.xml \
    port:=9091 \
    ssl:=true \
    certfile:=/etc/ssl/certs/robot.pem \
    keyfile:=/etc/ssl/private/robot.key

# Launch with authentication (rosauth)
ros2 launch rosbridge_server rosbridge_websocket_launch.xml \
    authenticate:=true
```

### JavaScript Client (roslibjs)

```javascript
// Connect to rosbridge WebSocket
const ros = new ROSLIB.Ros({ url: 'ws://robot-host:9090' });

ros.on('connection', () => console.log('Connected to rosbridge'));
ros.on('error', (err) => console.error('Connection error:', err));
ros.on('close', () => console.log('Connection closed'));

// Subscribe to compressed camera images
const imageTopic = new ROSLIB.Topic({
  ros: ros,
  name: '/camera/image/compressed',
  messageType: 'sensor_msgs/msg/CompressedImage',
  // Throttle to 10 Hz to avoid flooding the browser
  throttle_rate: 100,
  // Queue size of 1 — drop stale frames
  queue_size: 1
});

imageTopic.subscribe((msg) => {
  // msg.data is base64-encoded JPEG
  const imgElement = document.getElementById('camera-feed');
  imgElement.src = 'data:image/jpeg;base64,' + msg.data;
});

// Call a ROS2 service
const getMapSrv = new ROSLIB.Service({
  ros: ros,
  name: '/map_server/map',
  serviceType: 'nav_msgs/srv/GetMap'
});

getMapSrv.callService(new ROSLIB.ServiceRequest({}), (result) => {
  console.log('Map received:', result.map.info.width, 'x', result.map.info.height);
}, (error) => {
  console.error('Service call failed:', error);
});

// Publish velocity commands from a virtual joystick
const cmdVelTopic = new ROSLIB.Topic({
  ros: ros,
  name: '/cmd_vel',
  messageType: 'geometry_msgs/msg/Twist'
});

function sendVelocity(linearX, angularZ) {
  const twist = new ROSLIB.Message({
    linear: { x: linearX, y: 0.0, z: 0.0 },
    angular: { x: 0.0, y: 0.0, z: angularZ }
  });
  cmdVelTopic.publish(twist);
}

// Publish at 10 Hz while joystick is active; stop on release
let joystickInterval = null;
function onJoystickMove(lx, az) {
  if (!joystickInterval) {
    joystickInterval = setInterval(() => sendVelocity(lx, az), 100);
  }
}
function onJoystickRelease() {
  clearInterval(joystickInterval);
  joystickInterval = null;
  sendVelocity(0.0, 0.0);  // Always send zero on release
}
```

### Limitations and Performance
- **JSON serialization overhead**: All messages are serialized to JSON, including binary data (base64-encoded). A 640x480 JPEG compressed image becomes ~30% larger over the wire.
- **No topic filtering**: By default rosbridge exposes every topic, service, and action on the ROS2 graph. Any connected client can publish to `/cmd_vel`.
- **Single-threaded event loop**: rosbridge_server uses a single Tornado event loop. High-frequency subscriptions from multiple clients can starve the loop.
- **No built-in rate limiting**: Clients can subscribe at any rate. A misbehaving client subscribing to a 30Hz point cloud will consume the server.
- **Authentication is minimal**: rosauth uses MAC-based tokens with shared secrets. It does not support JWT, OAuth2, or role-based access.

## Pattern 2: Custom FastAPI Bridge

### Project Structure

```
robot_web_bridge/
├── robot_web_bridge/
│   ├── __init__.py
│   ├── ros_node.py          # ROS2 node with shared state
│   ├── web_app.py           # FastAPI application
│   ├── main.py              # Entry point: starts both rclpy and uvicorn
│   ├── auth.py              # JWT authentication middleware
│   └── rate_limiter.py      # Token bucket rate limiter
├── config/
│   └── bridge_config.yaml   # Allowed topics, rate limits, auth keys
├── launch/
│   └── web_bridge.launch.py
├── package.xml
├── setup.py
└── setup.cfg
```

### ROS2 Node with Async Executor

```python
# ros_node.py
import threading
import time
from typing import Optional

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_srvs.srv import Trigger


class RobotBridgeNode(Node):
    """ROS2 node that exposes topic data via thread-safe shared state."""

    def __init__(self):
        super().__init__('web_bridge_node')

        # Thread-safe shared state for latest messages
        self._lock = threading.Lock()
        self._latest_image: Optional[bytes] = None
        self._latest_odom: Optional[dict] = None
        self._image_timestamp: float = 0.0

        # QoS for sensor data — best effort, keep last 1
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Subscribers
        self.create_subscription(
            CompressedImage, '/camera/image/compressed',
            self._image_cb, sensor_qos)
        self.create_subscription(
            Odometry, '/odom', self._odom_cb, sensor_qos)

        # Publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Service client for emergency stop
        self.estop_client = self.create_client(Trigger, '/emergency_stop')

        self.get_logger().info('Web bridge node initialized')

    def _image_cb(self, msg: CompressedImage):
        with self._lock:
            self._latest_image = bytes(msg.data)
            self._image_timestamp = time.monotonic()

    def _odom_cb(self, msg: Odometry):
        with self._lock:
            self._latest_odom = {
                'x': msg.pose.pose.position.x,
                'y': msg.pose.pose.position.y,
                'theta': 2.0 * __import__('math').atan2(
                    msg.pose.pose.orientation.z,
                    msg.pose.pose.orientation.w),
                'linear_vel': msg.twist.twist.linear.x,
                'angular_vel': msg.twist.twist.angular.z,
            }

    def get_latest_image(self) -> Optional[bytes]:
        with self._lock:
            return self._latest_image

    def get_latest_odom(self) -> Optional[dict]:
        with self._lock:
            return self._latest_odom.copy() if self._latest_odom else None

    def publish_cmd_vel(self, linear_x: float, angular_z: float):
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)
        self.cmd_vel_pub.publish(msg)
```

### FastAPI App with ROS2 Integration

```python
# web_app.py
import base64
import asyncio
import time
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .ros_node import RobotBridgeNode


class CmdVelRequest(BaseModel):
    linear_x: float = Field(ge=-1.0, le=1.0, description="Linear velocity m/s")
    angular_z: float = Field(ge=-2.0, le=2.0, description="Angular velocity rad/s")


def create_app(ros_node: RobotBridgeNode) -> FastAPI:
    app = FastAPI(title="Robot Web Bridge", version="1.0.0")

    # CORS — restrict to known origins in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://dashboard.example.com"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT"],
        allow_headers=["Authorization", "Content-Type"],
    )

    # Store ros_node in app state so endpoints can access it
    app.state.ros_node = ros_node

    return app
```

### WebSocket Endpoint for Streaming

```python
# Add to web_app.py — WebSocket camera streaming endpoint

@app.websocket("/ws/camera")
async def camera_stream(websocket: WebSocket):
    """Stream compressed camera images as base64 over WebSocket.

    Supports per-client rate limiting via query parameter:
        ws://host/ws/camera?max_fps=10
    """
    await websocket.accept()
    ros_node: RobotBridgeNode = websocket.app.state.ros_node

    # Per-client rate limiting
    max_fps = int(websocket.query_params.get("max_fps", "15"))
    min_interval = 1.0 / max(1, min(max_fps, 30))  # Clamp 1-30 FPS
    last_send_time = 0.0
    last_image_bytes: Optional[bytes] = None

    try:
        while True:
            now = time.monotonic()
            elapsed = now - last_send_time

            if elapsed < min_interval:
                await asyncio.sleep(min_interval - elapsed)
                continue

            image_bytes = ros_node.get_latest_image()
            if image_bytes is None or image_bytes is last_image_bytes:
                # No new image available — avoid sending duplicates
                await asyncio.sleep(0.01)
                continue

            last_image_bytes = image_bytes
            last_send_time = time.monotonic()

            # Send as base64 JSON for browser compatibility
            b64_data = base64.b64encode(image_bytes).decode('ascii')
            await websocket.send_json({
                "type": "image",
                "format": "jpeg",
                "data": b64_data,
                "timestamp": last_send_time,
            })
    except WebSocketDisconnect:
        pass  # Client disconnected — clean exit
    except Exception as e:
        ros_node.get_logger().warn(f'WebSocket error: {e}')
    finally:
        # Graceful disconnect — no cleanup needed for read-only stream
        try:
            await websocket.close()
        except RuntimeError:
            pass  # Already closed
```

### REST Endpoints Wrapping ROS2 Services

```python
# Add to web_app.py — REST endpoints

@app.get("/api/robot/status")
async def get_robot_status():
    """Return current robot odometry and system status."""
    ros_node: RobotBridgeNode = app.state.ros_node
    odom = ros_node.get_latest_odom()
    if odom is None:
        raise HTTPException(status_code=503, detail="No odometry data available yet")
    return {
        "status": "active",
        "odometry": odom,
        "timestamp": time.time(),
    }


@app.post("/api/robot/cmd_vel")
async def post_cmd_vel(cmd: CmdVelRequest):
    """Send a velocity command to the robot."""
    ros_node: RobotBridgeNode = app.state.ros_node
    ros_node.publish_cmd_vel(cmd.linear_x, cmd.angular_z)
    return {"status": "ok", "linear_x": cmd.linear_x, "angular_z": cmd.angular_z}


@app.get("/api/robot/params/{param_name}")
async def get_parameter(param_name: str):
    """Read a ROS2 parameter from the bridge node."""
    ros_node: RobotBridgeNode = app.state.ros_node
    try:
        param = ros_node.get_parameter(param_name)
        return {"name": param_name, "value": param.value}
    except rclpy.exceptions.ParameterNotDeclaredException:
        raise HTTPException(status_code=404, detail=f"Parameter '{param_name}' not declared")


@app.put("/api/robot/params/{param_name}")
async def set_parameter(param_name: str, value: dict):
    """Set a ROS2 parameter on the bridge node.

    Body: {"value": <new_value>}
    """
    ros_node: RobotBridgeNode = app.state.ros_node
    try:
        param_value = value.get("value")
        if param_value is None:
            raise HTTPException(status_code=400, detail="Missing 'value' field")
        ros_node.set_parameters([rclpy.Parameter(param_name, value=param_value)])
        return {"name": param_name, "value": param_value, "status": "updated"}
    except rclpy.exceptions.ParameterNotDeclaredException:
        raise HTTPException(status_code=404, detail=f"Parameter '{param_name}' not declared")


@app.post("/api/robot/emergency_stop")
async def emergency_stop():
    """Call the emergency stop service."""
    ros_node: RobotBridgeNode = app.state.ros_node
    if not ros_node.estop_client.service_is_ready():
        raise HTTPException(status_code=503, detail="Emergency stop service not available")
    future = ros_node.estop_client.call_async(Trigger.Request())
    # Wait for result with timeout — run in executor to avoid blocking
    result = await asyncio.get_event_loop().run_in_executor(
        None, lambda: future.result(timeout=5.0)
    )
    return {"success": result.success, "message": result.message}
```

### Running FastAPI + rclpy Together

This is the critical integration point. Uvicorn runs in the main thread, rclpy spins in a background thread, and shutdown is coordinated via signals.

```python
# main.py
import signal
import sys
import threading

import rclpy
from rclpy.executors import MultiThreadedExecutor
import uvicorn

from .ros_node import RobotBridgeNode
from .web_app import create_app


def main():
    rclpy.init()
    ros_node = RobotBridgeNode()
    app = create_app(ros_node)

    # Spin rclpy in a background thread with a multi-threaded executor
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(ros_node)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    # Shutdown coordination
    shutdown_event = threading.Event()

    def shutdown_handler(signum, frame):
        ros_node.get_logger().info('Shutdown signal received')
        shutdown_event.set()
        # Stop uvicorn by raising KeyboardInterrupt in main thread
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        # Run uvicorn in the main thread
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8080,
            log_level="info",
            # Do NOT use reload in production with rclpy
            reload=False,
        )
    except KeyboardInterrupt:
        pass
    finally:
        ros_node.get_logger().info('Shutting down web bridge...')
        executor.shutdown()
        ros_node.destroy_node()
        rclpy.shutdown()
        spin_thread.join(timeout=5.0)


if __name__ == '__main__':
    main()
```

## Pattern 3: Flask Bridge

### Flask with rclpy Threading

Flask is synchronous. Running rclpy.spin() on the same thread as Flask will block one or the other. The correct approach uses a background thread for the ROS2 executor.

```python
# BAD: Blocking — rclpy.spin() never returns, Flask never starts
import rclpy
from flask import Flask, jsonify

app = Flask(__name__)

def bad_main():
    rclpy.init()
    node = rclpy.create_node('flask_bridge')
    rclpy.spin(node)  # Blocks forever — Flask never starts
    app.run(host='0.0.0.0', port=8080)
```

```python
# GOOD: Threaded executor — rclpy spins in background, Flask serves in main thread
import threading
import rclpy
from rclpy.executors import MultiThreadedExecutor
from flask import Flask, jsonify

app = Flask(__name__)
ros_node = None

class SimpleRosNode(rclpy.node.Node):
    def __init__(self):
        super().__init__('flask_bridge')
        self._lock = threading.Lock()
        self._data = {}
        self.create_subscription(
            Odometry, '/odom', self._odom_cb,
            QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, depth=1))

    def _odom_cb(self, msg):
        with self._lock:
            self._data['x'] = msg.pose.pose.position.x
            self._data['y'] = msg.pose.pose.position.y

    def get_data(self):
        with self._lock:
            return self._data.copy()

@app.route('/api/status')
def status():
    return jsonify(ros_node.get_data())

def main():
    global ros_node
    rclpy.init()
    ros_node = SimpleRosNode()

    executor = MultiThreadedExecutor()
    executor.add_node(ros_node)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    try:
        app.run(host='0.0.0.0', port=8080, threaded=True)
    finally:
        executor.shutdown()
        ros_node.destroy_node()
        rclpy.shutdown()
```

### When Flask Is Enough vs When You Need FastAPI

Use **Flask** when:
- You only need simple REST endpoints (no WebSocket)
- The web bridge is an internal tool with few concurrent users
- Your team is already familiar with Flask and not ready to adopt async
- You do not need OpenAPI/Swagger documentation auto-generation

Use **FastAPI** when:
- You need WebSocket endpoints for real-time streaming
- You need high concurrency (async handlers, many simultaneous clients)
- You want automatic request validation via Pydantic models
- You want auto-generated OpenAPI docs for the robot API
- You are streaming video or sensor data to multiple clients

## Video Streaming Patterns

### MJPEG Streaming

MJPEG streams work in `<img>` tags natively with no JavaScript needed. Useful for simple dashboards.

```python
# mjpeg_stream.py — MJPEG streaming endpoint for FastAPI
import cv2
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .ros_node import RobotBridgeNode


def generate_mjpeg(ros_node: RobotBridgeNode, max_fps: int = 15):
    """Generator that yields MJPEG frames as multipart HTTP response chunks."""
    min_interval = 1.0 / max_fps
    last_send = 0.0

    while True:
        now = time.monotonic()
        if now - last_send < min_interval:
            time.sleep(min_interval - (now - last_send))
            continue

        image_bytes = ros_node.get_latest_image()
        if image_bytes is None:
            time.sleep(0.05)
            continue

        last_send = time.monotonic()
        # Yield as multipart MJPEG frame
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n'
            b'Content-Length: ' + str(len(image_bytes)).encode() + b'\r\n'
            b'\r\n' + image_bytes + b'\r\n'
        )


@app.get("/video/mjpeg")
async def mjpeg_feed():
    ros_node: RobotBridgeNode = app.state.ros_node
    return StreamingResponse(
        generate_mjpeg(ros_node, max_fps=15),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
```

Browser usage — no JavaScript required:

```html
<img src="http://robot-host:8080/video/mjpeg" alt="Robot Camera" />
```

### WebRTC via webrtc_ros

For low-latency, high-quality video streaming, use the `webrtc_ros` package.

```yaml
# webrtc_ros launch config
# webrtc_bridge.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='webrtc_ros',
            executable='webrtc_ros_server_node',
            name='webrtc_server',
            parameters=[{
                'port': 8443,
                'image_transport': 'compressed',
                # Bind to all interfaces for remote access
                'address': '0.0.0.0',
            }],
            remappings=[
                ('image', '/camera/image_raw'),
            ],
        ),
    ])
```

### Compressed Topic Streaming via WebSocket

For a balance between simplicity and performance, stream compressed image topics over a binary WebSocket.

```python
# Binary WebSocket streaming — more efficient than base64 JSON
@app.websocket("/ws/camera/binary")
async def camera_stream_binary(websocket: WebSocket):
    """Stream JPEG frames as binary WebSocket messages.

    ~30% more bandwidth-efficient than base64 JSON encoding.
    Client must handle raw binary blobs.
    """
    await websocket.accept()
    ros_node: RobotBridgeNode = websocket.app.state.ros_node
    min_interval = 1.0 / 15  # 15 FPS max

    try:
        last_bytes = None
        while True:
            image_bytes = ros_node.get_latest_image()
            if image_bytes is not None and image_bytes is not last_bytes:
                last_bytes = image_bytes
                await websocket.send_bytes(image_bytes)
            await asyncio.sleep(min_interval)
    except WebSocketDisconnect:
        pass
```

Client-side JavaScript:

```javascript
const ws = new WebSocket('ws://robot-host:8080/ws/camera/binary');
ws.binaryType = 'arraybuffer';

ws.onmessage = (event) => {
  const blob = new Blob([event.data], { type: 'image/jpeg' });
  const url = URL.createObjectURL(blob);
  const img = document.getElementById('camera-feed');
  // Revoke previous URL to prevent memory leaks
  if (img.src.startsWith('blob:')) URL.revokeObjectURL(img.src);
  img.src = url;
};
```

## Bidirectional Communication

### Web UI to Robot Commands

```python
# teleop_handler.py — WebSocket teleop with command timeout watchdog
import asyncio
import time
from fastapi import WebSocket, WebSocketDisconnect

from .ros_node import RobotBridgeNode


class TeleopHandler:
    """Handles joystick input from browser with safety watchdog.

    If no command is received for 500ms, publishes zero velocity
    to prevent the robot from running away on disconnect.
    """

    COMMAND_TIMEOUT_S = 0.5  # Zero velocity after 500ms silence

    def __init__(self, ros_node: RobotBridgeNode):
        self.ros_node = ros_node
        self.last_command_time = 0.0

    async def handle(self, websocket: WebSocket):
        await websocket.accept()
        self.last_command_time = time.monotonic()

        # Start watchdog task
        watchdog_task = asyncio.create_task(self._watchdog())

        try:
            while True:
                data = await websocket.receive_json()
                # Expected: {"linear_x": 0.5, "angular_z": -0.3}
                linear_x = float(data.get("linear_x", 0.0))
                angular_z = float(data.get("angular_z", 0.0))

                # Clamp values for safety
                linear_x = max(-1.0, min(1.0, linear_x))
                angular_z = max(-2.0, min(2.0, angular_z))

                self.ros_node.publish_cmd_vel(linear_x, angular_z)
                self.last_command_time = time.monotonic()

                # Acknowledge to client
                await websocket.send_json({"ack": True, "t": self.last_command_time})
        except WebSocketDisconnect:
            pass
        finally:
            watchdog_task.cancel()
            # Always send zero on disconnect
            self.ros_node.publish_cmd_vel(0.0, 0.0)

    async def _watchdog(self):
        """Publish zero velocity if no command received within timeout."""
        while True:
            await asyncio.sleep(0.1)
            if time.monotonic() - self.last_command_time > self.COMMAND_TIMEOUT_S:
                self.ros_node.publish_cmd_vel(0.0, 0.0)
```

### Robot Status to Web UI

```python
# Status broadcast — push robot state to all connected WebSocket clients
class StatusBroadcaster:
    """Broadcasts robot status to all connected WebSocket clients."""

    def __init__(self, ros_node: RobotBridgeNode):
        self.ros_node = ros_node
        self.clients: set[WebSocket] = set()

    async def register(self, websocket: WebSocket):
        await websocket.accept()
        self.clients.add(websocket)
        try:
            # Keep connection alive — client sends pings
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            self.clients.discard(websocket)

    async def broadcast_loop(self, interval: float = 0.1):
        """Call this as a background task on app startup."""
        while True:
            odom = self.ros_node.get_latest_odom()
            if odom and self.clients:
                dead_clients = set()
                for client in self.clients.copy():
                    try:
                        await client.send_json({"type": "status", "odom": odom})
                    except Exception:
                        dead_clients.add(client)
                self.clients -= dead_clients
            await asyncio.sleep(interval)
```

### Command Acknowledgment Pattern

For reliable command execution, use a request-response pattern over WebSocket with correlation IDs.

```python
# Client sends:  {"id": "cmd-001", "action": "navigate_to", "x": 1.0, "y": 2.0}
# Server responds: {"id": "cmd-001", "status": "accepted", "estimated_time": 12.5}
# Server updates: {"id": "cmd-001", "status": "in_progress", "progress": 0.45}
# Server completes: {"id": "cmd-001", "status": "completed", "result": "success"}

@app.websocket("/ws/commands")
async def command_channel(websocket: WebSocket):
    await websocket.accept()
    ros_node: RobotBridgeNode = websocket.app.state.ros_node

    while True:
        try:
            data = await websocket.receive_json()
            cmd_id = data.get("id", "unknown")
            action = data.get("action")

            if action == "navigate_to":
                await websocket.send_json({
                    "id": cmd_id, "status": "accepted"
                })
                # Dispatch to ROS2 action client (non-blocking)
                asyncio.create_task(
                    execute_navigation(ros_node, websocket, cmd_id,
                                       data["x"], data["y"])
                )
            else:
                await websocket.send_json({
                    "id": cmd_id, "status": "error",
                    "message": f"Unknown action: {action}"
                })
        except WebSocketDisconnect:
            break
```

## Rate Limiting and Backpressure

### Server-Side Rate Limiting

```python
# rate_limiter.py — Token bucket rate limiter
import time
import threading


class TokenBucketRateLimiter:
    """Token bucket rate limiter for controlling message throughput.

    Usage:
        limiter = TokenBucketRateLimiter(tokens_per_second=10, burst_size=15)
        if limiter.acquire():
            send_message()
        else:
            drop_or_queue()
    """

    def __init__(self, tokens_per_second: float, burst_size: int = 0):
        self.rate = tokens_per_second
        self.burst_size = burst_size or int(tokens_per_second)
        self._tokens = float(self.burst_size)
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> bool:
        """Try to acquire a token. Returns True if allowed, False if rate limited."""
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_refill
            self._tokens = min(
                self.burst_size,
                self._tokens + elapsed * self.rate
            )
            self._last_refill = now

            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True
            return False

    def reset(self):
        """Reset to full burst capacity."""
        with self._lock:
            self._tokens = float(self.burst_size)
            self._last_refill = time.monotonic()
```

### Client-Driven Backpressure

Let clients request their own rate to match their processing capability.

```python
@app.websocket("/ws/sensor/{topic_name}")
async def sensor_stream(websocket: WebSocket, topic_name: str):
    await websocket.accept()

    # Client sends desired rate on connect
    config = await websocket.receive_json()
    requested_hz = config.get("hz", 10)
    requested_hz = max(1, min(requested_hz, 30))  # Clamp to 1-30 Hz
    interval = 1.0 / requested_hz

    ros_node: RobotBridgeNode = websocket.app.state.ros_node

    try:
        while True:
            data = ros_node.get_latest_odom()
            if data:
                await websocket.send_json({"topic": topic_name, "data": data})
            await asyncio.sleep(interval)
    except WebSocketDisconnect:
        pass
```

### Adaptive Quality Reduction

Reduce image quality when bandwidth or client processing cannot keep up.

```python
# Adaptive quality — reduce JPEG quality when send buffer backs up
import cv2
import numpy as np


async def adaptive_camera_stream(websocket: WebSocket, ros_node: RobotBridgeNode):
    quality = 80  # Start at 80% JPEG quality
    send_times = []

    while True:
        image_bytes = ros_node.get_latest_image()
        if image_bytes is None:
            await asyncio.sleep(0.05)
            continue

        # Re-encode with adaptive quality if needed
        if quality < 80:
            np_arr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            _, image_bytes = cv2.imencode(
                '.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])
            image_bytes = image_bytes.tobytes()

        t0 = time.monotonic()
        await websocket.send_bytes(image_bytes)
        send_duration = time.monotonic() - t0

        # Track send times to detect backpressure
        send_times.append(send_duration)
        if len(send_times) > 30:
            send_times.pop(0)

        avg_send = sum(send_times) / len(send_times)
        # If average send time > 50ms, reduce quality
        if avg_send > 0.05 and quality > 20:
            quality -= 5
        elif avg_send < 0.02 and quality < 80:
            quality += 5

        await asyncio.sleep(1.0 / 15)
```

## Security

### TLS/HTTPS with Nginx Reverse Proxy

Never expose the robot web bridge directly to untrusted networks. Use nginx as a TLS-terminating reverse proxy.

```nginx
# /etc/nginx/sites-available/robot-bridge
server {
    listen 443 ssl;
    server_name robot.example.com;

    ssl_certificate /etc/ssl/certs/robot.pem;
    ssl_certificate_key /etc/ssl/private/robot.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    # REST API
    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket endpoints
    location /ws/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;  # Keep WebSocket alive for 24h
    }

    # MJPEG video stream
    location /video/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_buffering off;  # Critical for streaming
        proxy_cache off;
    }
}
```

### Token-Based Auth (JWT)

```python
# auth.py — JWT authentication for FastAPI robot bridge
import time
from typing import Optional

from fastapi import Request, HTTPException, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

SECRET_KEY = "load-from-environment-variable"  # Use os.environ in production
ALGORITHM = "HS256"
TOKEN_EXPIRY_S = 3600  # 1 hour


class RobotAPIAuth(HTTPBearer):
    """JWT bearer token authentication for robot API endpoints."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="No credentials provided")
        return self._verify_token(credentials.credentials)

    @staticmethod
    def _verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("exp", 0) < time.time():
                raise HTTPException(status_code=401, detail="Token expired")
            return payload
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


auth_scheme = RobotAPIAuth()


# Protect REST endpoints
@app.get("/api/robot/status", dependencies=[Depends(auth_scheme)])
async def protected_status():
    return {"status": "active"}


# Protect WebSocket endpoints — check token from query parameter
async def verify_ws_token(websocket: WebSocket) -> Optional[dict]:
    """WebSocket cannot use Authorization header — use query param."""
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="Missing token")
        return None
    try:
        return RobotAPIAuth._verify_token(token)
    except HTTPException:
        await websocket.close(code=4003, reason="Invalid token")
        return None
```

### CORS Configuration

```python
# BAD: Allow all origins — any website can control your robot
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Any website can send requests
    allow_methods=["*"],        # Including DELETE, PATCH
    allow_headers=["*"],
)

# GOOD: Explicit origins — only your dashboard can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://dashboard.example.com",
        "https://monitor.internal.example.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Network Segmentation

Robots should run on isolated networks. The web bridge is the only component with interfaces on both the robot network and the user-facing network.

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Browser /      │     │   Web Bridge      │     │   ROS2 Nodes    │
│   Dashboard      │◄───►│   (FastAPI)        │◄───►│   (DDS network) │
│   (user network) │:443 │   eth0: user net   │     │   (robot VLAN)  │
│                  │     │   eth1: robot net  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

- The web bridge has two network interfaces: one facing users (nginx TLS), one facing the robot DDS network.
- ROS2 DDS discovery is confined to the robot VLAN via `ROS_DOMAIN_ID` and DDS network interface configuration.
- The web bridge translates and filters — never forwards raw DDS traffic.

## ROS2 Parameter Management via REST

```python
# parameter_api.py — Full CRUD for ROS2 parameters via HTTP

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Any
import asyncio

router = APIRouter(prefix="/api/params", tags=["parameters"])


class ParamUpdate(BaseModel):
    value: Any


@router.get("/")
async def list_parameters():
    """List all declared parameters on the bridge node."""
    ros_node = app.state.ros_node
    param_names = ros_node.get_parameters_by_prefix("")
    return {
        "parameters": [
            {"name": name, "value": param.value}
            for name, param in param_names.items()
        ]
    }


@router.get("/{name}")
async def get_param(name: str):
    """Get a single parameter value."""
    ros_node = app.state.ros_node
    try:
        param = ros_node.get_parameter(name)
        return {"name": name, "value": param.value, "type": str(param.type_)}
    except Exception:
        raise HTTPException(404, f"Parameter '{name}' not found")


@router.put("/{name}")
async def set_param(name: str, body: ParamUpdate):
    """Set a parameter value. Notifies WebSocket subscribers."""
    ros_node = app.state.ros_node
    try:
        old_value = ros_node.get_parameter(name).value
        ros_node.set_parameters([
            rclpy.parameter.Parameter(name, value=body.value)
        ])
        # Notify WebSocket subscribers of the change
        await param_broadcaster.notify(name, old_value, body.value)
        return {"name": name, "old_value": old_value, "new_value": body.value}
    except Exception as e:
        raise HTTPException(400, str(e))


# Parameter change notifications via WebSocket
class ParamBroadcaster:
    def __init__(self):
        self.subscribers: set[WebSocket] = set()

    async def notify(self, name: str, old_value: Any, new_value: Any):
        dead = set()
        for ws in self.subscribers.copy():
            try:
                await ws.send_json({
                    "type": "param_change",
                    "name": name,
                    "old_value": old_value,
                    "new_value": new_value,
                })
            except Exception:
                dead.add(ws)
        self.subscribers -= dead

    async def handle_ws(self, websocket: WebSocket):
        await websocket.accept()
        self.subscribers.add(websocket)
        try:
            while True:
                await websocket.receive_text()  # Keep alive
        except WebSocketDisconnect:
            self.subscribers.discard(websocket)


param_broadcaster = ParamBroadcaster()


@router.websocket("/ws")
async def param_ws(websocket: WebSocket):
    """WebSocket endpoint for real-time parameter change notifications."""
    await param_broadcaster.handle_ws(websocket)
```

## Web Integration Anti-Patterns

### 1. Blocking the ROS2 Executor from HTTP Handlers

**Problem:** Calling `rclpy.spin_once()` or `rclpy.spin_until_future_complete()` inside an HTTP handler blocks the web server thread and can deadlock if the ROS2 executor is already spinning in another thread.

**Fix:** Spin the ROS2 executor in a dedicated background thread. Access data via thread-safe shared state (lock-protected attributes). Never call spin functions from request handlers.

```python
# BAD: Spinning inside a Flask route
@app.route('/api/scan')
def get_scan():
    rclpy.spin_once(node, timeout_sec=1.0)  # Blocks the web server thread
    return jsonify(node.latest_scan)

# GOOD: Executor spins in background, handler reads shared state
@app.route('/api/scan')
def get_scan():
    return jsonify(node.get_latest_scan())  # Lock-protected read, non-blocking
```

### 2. Streaming Raw Image Messages Over WebSocket

**Problem:** Sending raw `sensor_msgs/Image` data (uncompressed BGR8, 640x480 = 921,600 bytes per frame) over WebSocket wastes bandwidth and CPU on the client. Base64 encoding inflates it to 1.2MB per frame.

**Fix:** Subscribe to `CompressedImage` topics (JPEG/PNG) or compress on the server side before sending. Use binary WebSocket frames instead of base64 JSON.

```python
# BAD: Subscribing to raw image and base64-encoding it
self.create_subscription(Image, '/camera/image_raw', self._raw_cb, 10)
# Each frame: 921,600 bytes raw -> 1,228,800 bytes base64 -> JSON overhead

# GOOD: Subscribe to compressed topic, send as binary WebSocket frame
self.create_subscription(
    CompressedImage, '/camera/image/compressed', self._compressed_cb,
    QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, depth=1))
# Each frame: ~30,000-80,000 bytes JPEG, sent as binary
await websocket.send_bytes(compressed_image_bytes)
```

### 3. No Rate Limiting on Sensor Subscriptions

**Problem:** A LiDAR publishing at 20Hz with 100K points per scan generates ~8MB/s of data. Forwarding every message to every WebSocket client saturates the network and browser.

**Fix:** Apply server-side rate limiting per client. Use a token bucket or simple time-based throttle. Let clients request their desired rate.

```python
# BAD: Forward every message to every client
def _scan_cb(self, msg):
    for client in self.clients:
        client.send(serialize(msg))  # 20 msgs/s * N clients

# GOOD: Rate-limit per client
def _scan_cb(self, msg):
    with self._lock:
        self._latest_scan = msg  # Just store latest

async def stream_to_client(self, ws, max_hz=5):
    interval = 1.0 / max_hz
    while True:
        scan = self.get_latest_scan()
        if scan:
            await ws.send_json(scan)
        await asyncio.sleep(interval)
```

### 4. Running rosbridge in Production Without Auth

**Problem:** rosbridge_suite with default settings exposes every topic, service, and parameter to any WebSocket client. Any browser on the network can publish to `/cmd_vel` or call `/emergency_stop`.

**Fix:** For production, use a custom bridge with authentication. If you must use rosbridge, enable rosauth, restrict topics via a filter, and run behind an authenticated reverse proxy.

```yaml
# BAD: Default rosbridge launch — full access to everything
ros2 launch rosbridge_server rosbridge_websocket_launch.xml

# GOOD: At minimum, enable authentication and use a reverse proxy
ros2 launch rosbridge_server rosbridge_websocket_launch.xml \
    authenticate:=true \
    topics_glob:="['/camera/image/compressed', '/odom', '/cmd_vel']"
```

### 5. Synchronous Service Calls in Async Handlers

**Problem:** Calling `service_client.call(request)` (synchronous) inside an `async def` FastAPI handler blocks the event loop, freezing all other requests until the service responds.

**Fix:** Use `call_async()` and await the future via `asyncio.get_event_loop().run_in_executor()`, or use a dedicated thread pool.

```python
# BAD: Synchronous service call blocks the async event loop
@app.post("/api/navigate")
async def navigate(goal: NavGoal):
    response = nav_client.call(goal_request)  # Blocks entire event loop
    return {"result": response.result}

# GOOD: Async service call with executor bridge
@app.post("/api/navigate")
async def navigate(goal: NavGoal):
    future = nav_client.call_async(goal_request)
    response = await asyncio.get_event_loop().run_in_executor(
        None, lambda: future.result(timeout=30.0)
    )
    return {"result": response.result}
```

### 6. GIL Contention Between Web Server and ROS2 Spinner

**Problem:** Running uvicorn with multiple worker threads and rclpy.spin in another thread causes GIL contention. Under high load, both the web server and ROS2 callbacks stall each other, leading to dropped messages and increased latency.

**Fix:** Use `MultiThreadedExecutor` with a small thread count (2-4). For high-throughput systems, run the ROS2 node in a separate process and communicate via shared memory, Redis, or a Unix socket.

```python
# BAD: SingleThreadedExecutor competing with uvicorn for the GIL
executor = SingleThreadedExecutor()
executor.add_node(node)
threading.Thread(target=executor.spin).start()
uvicorn.run(app, workers=4)  # 4 workers + 1 spinner = GIL contention

# GOOD: MultiThreadedExecutor with limited threads, single uvicorn worker
executor = MultiThreadedExecutor(num_threads=2)
executor.add_node(node)
threading.Thread(target=executor.spin, daemon=True).start()
uvicorn.run(app, workers=1, host="0.0.0.0", port=8080)
```

### 7. No Connection Lifecycle Management

**Problem:** WebSocket clients disconnect without sending a close frame (browser tab closed, network drop). The server keeps sending data to dead connections, wasting CPU and memory. Over time, the dead client set grows unbounded.

**Fix:** Track connected clients in a set, remove on disconnect, and periodically prune stale connections with a heartbeat check.

```python
# BAD: No tracking of client lifecycle
clients = []

@app.websocket("/ws/data")
async def data_ws(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    while True:
        await ws.send_json(get_data())  # Throws on dead client, never removed

# GOOD: Proper lifecycle management with cleanup
clients: set[WebSocket] = set()

@app.websocket("/ws/data")
async def data_ws(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            # Wait for client messages (ping/pong keepalive)
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        clients.discard(ws)

async def broadcast(data: dict):
    dead = set()
    for client in clients.copy():
        try:
            await client.send_json(data)
        except Exception:
            dead.add(client)
    clients -= dead
```

### 8. Exposing All Topics Unconditionally

**Problem:** The web bridge subscribes to every topic on the ROS2 graph and makes all of them available to web clients. This leaks internal system details (diagnostics, debug topics), wastes bandwidth, and creates a security risk.

**Fix:** Maintain an explicit allowlist of topics that should be exposed. Load it from configuration. Reject requests for topics not on the list.

```python
# BAD: Dynamically subscribe to whatever the client requests
@app.websocket("/ws/topic/{topic_name}")
async def any_topic(ws: WebSocket, topic_name: str):
    # Client can request /rosout, /parameter_events, /diagnostics, etc.
    sub = node.create_subscription(String, topic_name, callback, 10)

# GOOD: Allowlist of exposed topics from configuration
ALLOWED_TOPICS = {
    "/camera/image/compressed": CompressedImage,
    "/odom": Odometry,
    "/battery_state": BatteryState,
    "/cmd_vel": Twist,
}

@app.websocket("/ws/topic/{topic_name:path}")
async def allowed_topic(ws: WebSocket, topic_name: str):
    topic_path = "/" + topic_name
    if topic_path not in ALLOWED_TOPICS:
        await ws.close(code=4004, reason=f"Topic '{topic_path}' not in allowlist")
        return
    msg_type = ALLOWED_TOPICS[topic_path]
    # Proceed with subscription
```

## Web Integration Checklist

1. **Thread separation**: rclpy executor runs in a dedicated background thread; the web server runs in the main thread or its own thread. They never share an event loop.
2. **Shared state is lock-protected**: Every piece of data read by HTTP handlers and written by ROS2 callbacks is guarded by `threading.Lock()`. No bare attribute access across threads.
3. **Graceful shutdown coordination**: Signal handlers set a shutdown event, the executor is stopped before `rclpy.shutdown()`, and the spin thread is joined with a timeout.
4. **Topic allowlist enforced**: Only explicitly listed topics are exposed to web clients. The allowlist is loaded from a configuration file, not hardcoded.
5. **Rate limiting on all streams**: Every WebSocket stream has a per-client rate limiter (token bucket or time-based). Clients can request a lower rate but not exceed the server maximum.
6. **Command timeout watchdog**: Any endpoint that accepts velocity or motion commands publishes zero velocity if no command is received within 500ms, preventing runaway robots on disconnect.
7. **Video is compressed before transmission**: Camera feeds use `CompressedImage` topics or server-side JPEG encoding. Raw `Image` messages are never forwarded to web clients.
8. **TLS termination in front of the bridge**: An nginx or caddy reverse proxy handles TLS. The bridge itself listens on localhost only. WebSocket upgrade headers are properly proxied.
9. **Authentication on all mutation endpoints**: POST, PUT, DELETE endpoints and teleop WebSocket connections require a valid JWT or API key. Read-only status endpoints may be unauthenticated on private networks.
10. **CORS restricts origins**: `allow_origins` lists specific dashboard URLs. Wildcard `*` is never used in production.
11. **Connection lifecycle management**: WebSocket clients are tracked in a set, removed on disconnect, and periodically pruned. Dead client references are never retained.
12. **Binary WebSocket for high-bandwidth data**: Image frames, point clouds, and other binary data use `send_bytes()`, not base64-encoded JSON. This saves ~33% bandwidth and CPU on both sides.
