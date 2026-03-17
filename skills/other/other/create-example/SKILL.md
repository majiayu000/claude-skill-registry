---
name: create-example
description: Create new publish/subscribe examples for ROS2 message types. Use when the user wants to add a new example, create pub/sub for a new message type, or add trajectory/sensor/geometry message examples.
---

# Create Example

This skill guides you through creating new publish/subscribe examples for the zenoh-ros2-sdk.

## When to Use

- User wants to add a new example for a message type
- User wants to create publisher/subscriber for a new ROS2 message
- Adding support for trajectory, sensor, geometry, or other message types

## Project Structure

Examples are in `examples/` with numbered filenames:
- Odd numbers: publishers (e.g., `11_publish_*.py`)
- Even numbers: subscribers (e.g., `12_subscribe_*.py`)

## 1. Determine Next Example Numbers

Check existing examples in `examples/` directory. Use the next available odd number for publisher, next even for subscriber.

## 2. Look Up Message Definition

Find the ROS2 message definition. Key resources:
- https://docs.ros2.org/foxy/api/{package}/msg/{MessageName}.html
- Common packages: `std_msgs`, `geometry_msgs`, `sensor_msgs`, `trajectory_msgs`, `nav_msgs`

## 3. Publisher Template

Create `examples/{NN}_publish_{msg_name}.py`:

```python
#!/usr/bin/env python3
"""
{NN} - Publish {MessageName} Messages

Demonstrates how to publish {package}/msg/{MessageName} messages to a ROS2 topic.
{Brief description of what this message type is used for.}
"""
import time
import numpy as np

from zenoh_ros2_sdk import ROS2Publisher, get_message_class


def main():
    print("{NN} - Publish {MessageName} Messages")
    print("Publishing to /{topic_name} topic...\n")

    # Get message classes for easy object creation
    Header = get_message_class("std_msgs/msg/Header")
    Time = get_message_class("builtin_interfaces/msg/Time")
    {MessageName} = get_message_class("{package}/msg/{MessageName}")
    # Add nested message classes as needed

    if not all([Header, Time, {MessageName}]):
        print("Error: Failed to get message classes")
        return

    # Create publisher
    pub = ROS2Publisher(
        topic="/{topic_name}",
        msg_type="{package}/msg/{MessageName}"
    )

    try:
        print("Publishing {MessageName} messages...")
        print("Press Ctrl+C to stop\n")

        counter = 0
        while True:
            # Get current time
            now = time.time()
            sec = int(now)
            nanosec = int((now - sec) * 1e9)

            # Create header with timestamp
            header = Header(
                stamp=Time(sec=sec, nanosec=nanosec),
                frame_id="base_link"
            )

            # Create and populate message fields
            # Note: Arrays need to be numpy arrays for proper serialization

            # Publish message - pass fields as kwargs matching message structure
            pub.publish(
                header=header,
                # ... other fields
            )

            print(f"Published {MessageName} {counter}")
            counter += 1
            time.sleep(0.1)  # 10 Hz

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        pub.close()
        print("Publisher closed")


if __name__ == "__main__":
    main()
```

## 4. Subscriber Template

Create `examples/{NN+1}_subscribe_{msg_name}.py`:

```python
#!/usr/bin/env python3
"""
{NN+1} - Subscribe to {MessageName} Messages

Demonstrates how to subscribe to a ROS2 topic and receive {package}/msg/{MessageName} messages.
{Brief description of what this message type is used for.}
"""
import time

from zenoh_ros2_sdk import ROS2Subscriber


def main():
    print("{NN+1} - Subscribe to {MessageName} Messages")
    print("Subscribing to /{topic_name} topic...\n")

    message_count = [0]  # Use list to allow modification in nested function

    def on_message(msg):
        """Callback function called when a {MessageName} message is received."""
        message_count[0] += 1

        # Extract information from the message
        timestamp = msg.header.stamp
        frame_id = msg.header.frame_id
        # ... extract other fields

        # Display received data
        print(f"\n--- {MessageName} Message #{message_count[0]} ---")
        print(f"Timestamp: {timestamp.sec}.{timestamp.nanosec:09d}")
        print(f"Frame ID: {frame_id}")
        # ... print other fields

    # Create subscriber
    sub = ROS2Subscriber(
        topic="/{topic_name}",
        msg_type="{package}/msg/{MessageName}",
        callback=on_message
    )

    try:
        print("Waiting for {MessageName} messages... Press Ctrl+C to stop")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        sub.close()
        print("Subscriber closed")


if __name__ == "__main__":
    main()
```

## 5. Update README

Add entries to `examples/README.md`:

```markdown
### [`{NN}_publish_{msg_name}.py`]({NN}_publish_{msg_name}.py)
Demonstrates how to publish `{package}/msg/{MessageName}` messages. {Description}.

**Usage:**
\```bash
python3 examples/{NN}_publish_{msg_name}.py
\```

### [`{NN+1}_subscribe_{msg_name}.py`]({NN+1}_subscribe_{msg_name}.py)
Demonstrates how to subscribe to `{package}/msg/{MessageName}` messages. {Description}.

**Usage:**
\```bash
python3 examples/{NN+1}_subscribe_{msg_name}.py
\```
```

## 6. Key Patterns

### Arrays
Use numpy arrays for proper CDR serialization:
```python
positions = np.array([0.0, 0.1, 0.2], dtype=np.float64)
```

### Nested Messages
Get nested message classes and construct them:
```python
Point = get_message_class("trajectory_msgs/msg/JointTrajectoryPoint")
Duration = get_message_class("builtin_interfaces/msg/Duration")

point = Point(
    positions=np.array([0.0, 0.1], dtype=np.float64),
    time_from_start=Duration(sec=1, nanosec=0)
)
```

### Common Topic Names
- `/joint_states` - JointState
- `/cmd_vel` - Twist
- `/joint_trajectory` - JointTrajectory
- `/odom` - Odometry
- `/tf` - TransformStamped
