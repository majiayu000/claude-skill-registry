---
name: ros2-perception
description: "Perception: image_transport, cv_bridge, vision_msgs, depth_image_proc, laser_geometry, pcl_ros."
---

# ROS 2 Perception & Computer Vision Instructions (Ubuntu 24.04 LTS & ROS 2 Jazzy)

## 1. Documentation Entry Points

Any Jazzy package's API docs live at **`https://docs.ros.org/en/jazzy/p/<package>/`** — build the URL from the package name rather than looking one up.

Packages in this domain: `image_transport` (transport plugins, compressed), `cv_bridge` (OpenCV conversion), `vision_msgs` (2D/3D detections), `depth_image_proc` (depth→cloud, registration), `pointcloud_to_laserscan`, `laser_geometry` (scan projection), `pcl_ros` (PCL bridge).

Verify message field names against the installation itself: `ros2 interface show sensor_msgs/msg/Image`.

## 2. Key Concepts & Patterns

### `cv_bridge` OpenCV Conversion (C++)
```cpp
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <cv_bridge/cv_bridge.hpp>
#include <opencv2/imgproc/imgproc.hpp>

void process_image(const sensor_msgs::msg::Image::ConstSharedPtr & msg) {
  cv_bridge::CvImagePtr cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
  cv::circle(cv_ptr->image, cv::Point(50, 50), 10, CV_RGB(255, 0, 0), 2);
  sensor_msgs::msg::Image::SharedPtr out_msg = cv_ptr->toImageMsg();
}
```

## 3. Symptom -> Root Cause -> Action

| Symptom | Likely root cause | Action |
| :--- | :--- | :--- |
| Image topic listed but callback never fires | QoS mismatch: camera drivers publish BestEffort, subscriber defaults Reliable | Subscribe with sensor-data QoS — **C++ `rclcpp::SensorDataQoS()`, Python `rclpy.qos.qos_profile_sensor_data`** (there is no `rclcpp` module in Python); confirm with `ros2 topic info <topic> -v` |
| Detection boxes drawn at wrong image positions | Processing the rectified topic but projecting with the raw camera matrix (or vice versa) | Pair `image_rect` with `P` (projection) matrix, raw `image` with `K`; don't mix |
