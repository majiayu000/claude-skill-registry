---
name: ros2-package
description: "Package & build wiring: ros2 pkg create, package.xml, ament_cmake CMakeLists, ament_python setup.py, colcon build/source, installing launch & config, custom .msg/.srv interface packages."
---

# ROS 2 Package Creation & Build Wiring (Ubuntu 24.04 LTS & ROS 2 Jazzy)

Most "it built fine but doesn't run" bugs are wiring, not code. This skill covers
the seams between a source file and a runnable node.

## 1. Documentation Entry Points

| For | Entry point |
| :--- | :--- |
| ament_cmake reference (install, exports, testing hooks) | `https://docs.ros.org/en/jazzy/How-To-Guides/Ament-CMake-Documentation.html` |
| Package creation, custom interfaces, colcon tutorials | `https://docs.ros.org/en/jazzy/Tutorials/` |

Ground truth beats both: read a working installed package under
`/opt/ros/jazzy/share/<pkg>/` and copy its structure.

## 2. The Wiring That Makes a Node Runnable

**`ament_cmake`**: executables must install to `lib/${PROJECT_NAME}` exactly —
that is the only place `ros2 run` looks. `launch/` and `params/` are not
installed by default and need their own `install(DIRECTORY ...)` into
`share/${PROJECT_NAME}`. `ament_package()` comes last, exactly once.

**`ament_python`**: `package.xml` needs
`<export><build_type>ament_python</build_type></export>`, or colcon configures
the package as `ament_cmake` and fails looking for a `CMakeLists.txt` that was
never meant to exist.

`setup.cfg` needs the ROS-specific install location, not just `[metadata]`:
```ini
[develop]
script_dir=$base/lib/my_package
[install]
install_scripts=$base/lib/my_package
```
Without it, `console_scripts` still builds and installs, just not to
`lib/${PROJECT_NAME}` — the same place `ros2 run` looks for `ament_cmake`
executables — so the node is present but undiscoverable.

## 3. Custom Interfaces (`.msg` / `.srv`)

Interfaces require an **`ament_cmake`** package — they cannot live in an `ament_python`
package. Standard practice is a dedicated `<project>_interfaces` package that your
node packages depend on.

```cmake
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}     # first arg must start with the package name
  "msg/Num.msg"
  "srv/AddThreeInts.srv"
  DEPENDENCIES geometry_msgs
)
```
```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

Verify the result with `ros2 interface show my_pkg/msg/Num` — if that fails, the
generation never ran.

## 4. Strict Rules
After adding any new file, directory, or entry point: rebuild **and** re-source
before concluding something is broken.
