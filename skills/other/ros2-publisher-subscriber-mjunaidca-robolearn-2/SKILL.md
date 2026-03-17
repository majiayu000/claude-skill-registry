---
name: "ros2-publisher-subscriber"
description: "Generate ROS 2 publisher and subscriber code examples for educational content. This skill should be used when creating lessons that teach ROS 2 pub/sub patterns, writing exercises involving topic-based communication, or generating worked examples for rclpy nodes."
version: "1.0.0"
status: "active"
---

# ROS 2 Publisher/Subscriber Skill

**Purpose**: Generate accurate, educational ROS 2 publisher and subscriber code following official ROS 2 Humble patterns for the Physical AI textbook.

## When to Use

- Creating lessons in Chapter 4 (Your First ROS 2 Code)
- Writing publisher/subscriber exercises for any ROS 2 content
- Generating worked examples that demonstrate topic-based communication
- Creating Tier 1 cloud-compatible code examples

## Live Documentation Access

**CRITICAL**: Before generating any code, fetch current ROS 2 documentation using Context7 MCP:

```
Tool: mcp__context7__resolve-library-id
libraryName: "ros2 rclpy"

Then:
Tool: mcp__context7__get-library-docs
context7CompatibleLibraryID: [resolved ID]
topic: "publisher subscriber"
```

This ensures code matches current ROS 2 Humble API.

## Code Generation Principles

### Publisher Pattern (Canonical)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Pattern (Canonical)

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Educational Requirements

### Layer 1 (Manual Foundation)
- Explain node lifecycle (init → spin → shutdown)
- Diagram topic-based communication flow
- Explain QoS basics (queue depth = 10)

### Layer 2 (AI Collaboration)
- Prompt templates for extending nodes
- Error diagnosis with AI assistance
- Refactoring suggestions (Three Roles INVISIBLE)

### Layer 3 (Intelligence Design)
- When patterns should become reusable
- Node composition strategies
- Configuration via parameters (links to ros2-launch-system skill)

## Hardware Tier Compatibility

All code MUST work on:
- **Tier 1**: Cloud ROS 2 (TheConstruct) or MockROS in browser
- **Tier 2+**: Local ROS 2 Humble installation

Include cloud setup instructions:
```bash
# Cloud ROS 2 (TheConstruct)
source /opt/ros/humble/setup.bash
cd ~/ros2_ws && colcon build
source install/setup.bash
```

## Common Mistakes to Prevent

1. **Missing spin()**: Node won't process callbacks without rclpy.spin()
2. **Wrong message type import**: Always match import to actual message type
3. **No cleanup**: Always call destroy_node() and shutdown()
4. **Timer not stored**: Timer needs reference to prevent garbage collection

## Integration with Other Skills

- **ros2-custom-interfaces**: When custom message types needed
- **ros2-launch-system**: When launching multiple pub/sub nodes
- **lesson-generator**: For full lesson structure around examples

## Authoritative Source

All patterns verified against: https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html
