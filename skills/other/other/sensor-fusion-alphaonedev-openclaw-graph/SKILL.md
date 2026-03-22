---
name: sensor-fusion
cluster: iot
description: "Combining IoT sensor data using algorithms like Kalman filters for improved accuracy and reliability"
tags: ["iot","sensor"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "sensor-fusion iot"
---

# sensor-fusion

## Purpose
This skill enables the fusion of IoT sensor data using algorithms like Kalman filters to enhance accuracy and reliability in real-time applications. It processes inputs from multiple sensors, applies fusion techniques, and outputs refined data streams for downstream use.

## When to Use
Use this skill when dealing with noisy or inconsistent sensor data, such as in autonomous vehicles for obstacle detection, smart home systems for environmental monitoring, or industrial IoT for predictive maintenance. Apply it in scenarios requiring real-time data smoothing, like merging GPS and accelerometer data, or when sensor redundancy improves decision-making.

## Key Capabilities
- Implements Kalman and Extended Kalman filters for state estimation and noise reduction.
- Supports data fusion from up to 10 sensor types (e.g., temperature, humidity, motion) via JSON input streams.
- Handles real-time processing with configurable update rates (e.g., 10-100 Hz).
- Provides output in standardized formats like CSV or JSON for easy integration.
- Includes adaptive thresholding to detect and ignore faulty sensor readings.
- Offers visualization hooks for debugging fused data outputs.

## Usage Patterns
To use this skill, first set the environment variable for authentication: `export OPENCLAW_API_KEY=your_api_key`. Then, invoke via CLI or API, providing sensor configurations in a JSON file. For CLI, pipe sensor data directly; for API, send POST requests with data payloads. Always specify the fusion algorithm and sensors in the command or request body to avoid defaults.

Example pattern 1: CLI command for fusing two sensors:
```bash
claw sensor-fusion fuse --sensors temp,humidity --algorithm kalman --config config.json
```
Example pattern 2: API call in a script:
```python
import requests
response = requests.post('https://api.openclaw.io/sensor-fusion', headers={'Authorization': f'Bearer {os.environ["OPENCLAW_API_KEY"]}'}, json={'sensors': ['temp', 'humidity'], 'algorithm': 'kalman'})
print(response.json())
```

## Common Commands/API
- CLI: `claw sensor-fusion fuse --sensors <list> --algorithm <name> --rate <Hz>`: Fuses specified sensors with the given algorithm and update rate (e.g., `--rate 50` for 50 Hz).
- CLI: `claw sensor-fusion simulate --data <file> --output results.csv`: Simulates fusion on a sample data file and saves output.
- API Endpoint: POST /api/sensor-fusion: Requires JSON body like `{"sensors": ["temp", "pressure"], "algorithm": "ekf", "config": {"noise_variance": 0.01}}`; returns fused data array.
- API Endpoint: GET /api/sensor-fusion/status: Checks fusion job status using query param `job_id`, e.g., `GET /api/sensor-fusion/status?job_id=123`.
- Config Format: JSON, e.g., `{"sensors": [{"name": "temp", "type": "analog", "weight": 0.5}], "algorithm": {"type": "kalman", "parameters": {"Q": 0.01, "R": 0.1}}}`.
Use `$OPENCLAW_API_KEY` in headers for all API calls.

## Integration Notes
Integrate by importing the OpenClaw SDK in your project: `pip install openclaw`. Reference this skill in code with `from openclaw.skills import sensor_fusion`. Ensure sensor data is formatted as arrays of {timestamp, value} objects. For multi-skill workflows, chain with other IoT skills by passing outputs via shared variables, e.g., set `output_fused_data` as input for a downstream analytics skill. Handle dependencies like NumPy for matrix operations. Test integrations in a sandbox environment first, using mock sensor data to verify fusion accuracy.

## Error Handling
Check for errors by parsing response codes: HTTP 400 for invalid sensor lists, 401 for authentication failures with `$OPENCLAW_API_KEY`. In CLI, errors like "Sensor not found" appear if --sensors flag is mismatched; use `--verbose` to debug. Handle algorithm-specific errors, e.g., if Kalman filter diverges, catch with try-except in code: ```python
try: fused_data = sensor_fusion.fuse(data, algorithm='kalman')
except ValueError as e: print(f"Error: {e} - Check sensor data format")
``` Implement retries for transient issues, like network failures in API calls, using exponential backoff.

## Graph Relationships
- Related to: iot-cluster (parent cluster for shared IoT functionalities)
- Connected to: data-processing (for preprocessing sensor inputs)
- Links with: machine-learning (for advanced algorithm training on fused data)
