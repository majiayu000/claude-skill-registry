---
name: add-repository
description: Add a new Git repository to the message registry for automatic message type loading. Use when the user wants to support message types from a new ROS2 repository, or when adding support for a new message package.
---

# Add Repository

This skill guides you through adding a new Git repository to the `zenoh_ros2_sdk/_repositories.py` file to enable automatic message type loading.

## When to Use

- User wants to add support for message types from a new ROS2 repository
- User asks to support a specific repository (e.g., "support geometry2", "add tf2_msgs")
- Message types are not found because the repository isn't registered
- Adding support for new message packages

## 1. Discover Repository Structure

First, identify the repository URL and explore its structure to find message packages.

### A. Get Repository URL

The user may provide:
- Full GitHub URL (e.g., `https://github.com/ros2/geometry2.git`)
- Repository name (e.g., `geometry2`)
- Package name (e.g., `tf2_msgs`)

### B. Explore Repository Contents

Use curl to check the repository structure:

```bash
# List all directories in the repository
curl -s https://api.github.com/repos/ros2/geometry2/contents | \
  python3 -c "import sys, json; data = json.load(sys.stdin); \
  dirs = [item['name'] for item in data if item['type'] == 'dir']; \
  print('\n'.join(sorted(dirs)))"
```

### C. Find Message Packages

Check which directories contain message definitions:

```bash
# Check if a package has a msg directory
curl -s https://api.github.com/repos/ros2/geometry2/contents/tf2_msgs | \
  python3 -c "import sys, json; data = json.load(sys.stdin); \
  print('\n'.join([item['name'] for item in data if item['type'] == 'dir']))"
```

### D. List Available Messages

Check what messages are in a package:

```bash
# List .msg files in a package
curl -s https://api.github.com/repos/ros2/geometry2/contents/tf2_msgs/msg | \
  python3 -c "import sys, json; data = json.load(sys.stdin); \
  msgs = [item['name'] for item in data if item['name'].endswith('.msg')]; \
  print('\n'.join(sorted(msgs)))"
```

## 2. Determine Repository Structure

Identify the repository layout pattern:

### Pattern A: Meta-Repository (Multiple Packages)
Structure: `<repo_root>/<package>/msg/<message>.msg`
- Example: `common_interfaces`, `rcl_interfaces`, `geometry2`
- Contains multiple packages in subdirectories
- Each package has its own `msg/` directory

### Pattern B: Single Package Repository
Structure: `<repo_root>/msg/<message>.msg` or `<repo_root>/<package>/msg/<message>.msg`
- Example: `example_interfaces`
- Single package, messages at repo root or in package subdirectory

## 3. Determine Commit/Tag

Choose an appropriate commit or tag:
- **Recommended**: Use stable ROS2 distribution tags (e.g., `jazzy`, `iron`, `humble`) for consistency with other repositories
- **Default**: Use `jazzy` to match existing repositories (`rcl_interfaces`, `common_interfaces`, `example_interfaces`, `geometry2`)
- **Rolling**: Use `rolling` branch only if you need latest development features
- **Specific version**: Use commit SHA or version tag for reproducibility

Check available tags:
```bash
curl -s https://api.github.com/repos/ros2/geometry2/tags | \
  python3 -c "import sys, json; data = json.load(sys.stdin); \
  print('\n'.join([tag['name'] for tag in data[:10]]))"
```

## 4. Add Repository Entry

Edit `zenoh_ros2_sdk/_repositories.py` and add a new entry to `MESSAGE_REPOSITORIES`:

### Template for Meta-Repository

```python
# Repository name (descriptive, matches repo name)
"repository_name": MessageRepository(
    url="https://github.com/ros2/repository_name.git",
    commit="jazzy",  # Use jazzy for consistency with other repositories
    cache_path="repository_name",  # Local cache directory name
    msg_path="",  # Empty for standard structure: <package>/msg/<message>.msg
    packages=[
        "package1",  # List all message packages in this repository
        "package2",
        # ... more packages
    ],
),
```

### Template for Single Package Repository

```python
"package_name": MessageRepository(
    url="https://github.com/ros2/package_name.git",
    commit="jazzy",  # Use jazzy for consistency, or specific tag/commit
    cache_path="package_name",
    msg_path="",  # Adjust if messages are at repo root vs package subdirectory
    packages=[
        "package_name",  # Single package
    ],
),
```

### Example: Adding geometry2

```python
# Geometry2 (contains tf2_msgs and other TF2-related packages)
# This repository contains TF2 transform message definitions
# Reference: https://github.com/ros2/geometry2
"geometry2": MessageRepository(
    url="https://github.com/ros2/geometry2.git",
    commit="jazzy",  # Use specific commit/tag for reproducibility
    cache_path="geometry2",
    msg_path="",  # Messages are at <package>/msg/<message>.msg
    packages=[
        "tf2_msgs",  # Contains TFMessage, TF2Error messages
    ],
),
```

## 5. Verify Package Mapping

The `PACKAGE_TO_REPOSITORY` mapping is automatically generated at the bottom of the file. Verify it includes your new packages:

```python
# Mapping from message package namespace to repository name
PACKAGE_TO_REPOSITORY: Dict[str, str] = {}
for repo_name, repo in MESSAGE_REPOSITORIES.items():
    for package in repo.packages:
        PACKAGE_TO_REPOSITORY[package] = repo_name
```

This ensures packages like `tf2_msgs` map to `geometry2` repository.

## 6. Check for Linting Errors

Run linting to ensure code quality:

```bash
# Check for linting errors
# (The linter will automatically check when you edit the file)
```

## 7. Test Message Loading (Optional)

Verify the repository works by testing message loading:

```python
from zenoh_ros2_sdk import load_message_type, get_message_class

# Load a message type from the new repository
load_message_type("tf2_msgs/msg/TFMessage")
TFMessage = get_message_class("tf2_msgs/msg/TFMessage")

if TFMessage:
    print("Successfully loaded message from new repository!")
```

## Common Repositories

### Already Supported
- `rcl_interfaces` - Core ROS2 interfaces (builtin_interfaces, action_msgs, etc.)
- `common_interfaces` - Standard messages (std_msgs, geometry_msgs, sensor_msgs, etc.)
- `example_interfaces` - Example messages and services
- `geometry2` - TF2 messages (tf2_msgs)

### Potential Additions
- `ros2_interfaces` - Additional ROS2 interfaces
- `rosidl_defaults` - Default message definitions
- Custom repositories with message definitions

## Notes

- **Cache Location**: Repositories are cached in `~/.cache/zenoh_ros2_sdk/` (or `$ZENOH_ROS2_SDK_CACHE`)
- **Automatic Download**: Messages are downloaded automatically when first requested
- **Dependencies**: Message dependencies are resolved automatically
- **Consistency**: Use `jazzy` as the default commit tag to match existing repositories for consistency and reproducibility
