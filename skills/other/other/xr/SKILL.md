---
name: xr
description: Vuer VR/AR/WebXR - hand tracking, controllers, AR mesh, haptics (plugin:vuer@vuer)
---

# Vuer XR

Requires wss://. Use ngrok: `ngrok http 8012` then `https://vuer.ai?ws=wss://xxxx.ngrok.io`

## Hand Tracking

```python
session.set @ DefaultScene(Hands(key="hands", stream=True))

@app.add_handler("HAND_MOVE")
async def on_hands(event, session):
    left = event.value.get('left')
    if left:
        wrist = left['wrist']
        pinch = left.get('pinchStrength', 0)
```

Joints: `wrist`, `thumbTip`, `indexTip`, `middleTip`, `ringTip`, `pinkyTip`, `pinchStrength`, `matrix`

## Controllers

```python
session.set @ DefaultScene(MotionController(key="ctrl", stream=True))

@app.add_handler("CONTROLLER_MOVE")
async def on_ctrl(event, session):
    right = event.value.get('right')
    if right:
        pos, rot, buttons = right['position'], right['rotation'], right['buttons']
```

## Gripper

```python
@app.add_handler("HAND_MOVE")
async def update_gripper(event, session):
    r = event.value.get('right')
    if r:
        session.upsert @ Gripper(key="g", position=r['wrist'],
                                  pinchWidth=0.08 * (1 - r.get('pinchStrength', 0)))
```

## AR Mesh

```python
session.set @ DefaultScene(WebXRMesh(key="mesh", stream=False))
await asyncio.sleep(2)
mesh_data = await session.get_webxr_mesh(key="mesh")
for m in mesh_data.value.get('meshes', []):
    vertices, indices, label = m['vertices'], m['indices'], m.get('semanticLabel')
```

## Haptics

```python
from vuer.events import HapticActuatorPulse
session @ HapticActuatorPulse(left={"strength": 0.5, "duration": 100},
                               right={"strength": 1.0, "duration": 200})
```
