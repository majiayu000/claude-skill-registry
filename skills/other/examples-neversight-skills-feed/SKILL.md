---
name: examples
description: Common Vuer patterns - animation, URDF, point clouds, interactivity, batch updates (plugin:vuer@vuer)
---

# Vuer Examples

## Animation Loop

```python
@app.spawn(start=True)
async def main(session: VuerSession):
    session.set @ DefaultScene()
    t = 0
    while True:
        t += 0.05
        session.upsert @ Box(key="box", position=[np.sin(t), 0.5, np.cos(t)], rotation=[0, t, 0])
        await asyncio.sleep(0.016)
```

## URDF Robot

```python
session.set @ DefaultScene(
    Urdf(key="robot", src="/static/panda.urdf",
         jointValues={"panda_joint1": 0, "panda_joint2": -0.5, "panda_joint4": -2.0})
)
```

## Point Cloud

```python
vertices = np.random.randn(10000, 3).astype(np.float16) * 2
colors = (np.random.rand(10000, 3) * 255).astype(np.uint8)
session.set @ DefaultScene(PointCloud(key="pcd", vertices=vertices, colors=colors, size=0.02))
```

## Interactive Movable

```python
session.set @ DefaultScene(Movable(key="m", children=[Box(key="box", color="green")]))

@app.add_handler("OBJECT_MOVE")
async def on_move(event, session):
    print(event.value)
```

## Batch Updates

```python
while True:
    session.upsert @ [Box(key=f"box-{i}", position=pos) for i, pos in enumerate(positions)]
    await asyncio.sleep(0.016)
```

## Frame Capture

```python
await asyncio.sleep(1)
render = await session.grab_render(quality=0.9)
render.value.save("screenshot.png")
```

## Hierarchical Scene

```python
session.set @ DefaultScene(
    group(key="arm", children=[
        Box(key="base", args=[0.5, 0.1, 0.5]),
        group(key="link1", position=[0, 0.1, 0], children=[
            Cylinder(key="j1", args=[0.05, 0.05, 0.3]),
            group(key="link2", position=[0, 0.3, 0], children=[...])
        ])
    ])
)
```
