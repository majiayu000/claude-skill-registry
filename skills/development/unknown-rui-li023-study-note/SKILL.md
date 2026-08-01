---
name: unknown-rui-li023-study-note
description: 官网：https://www.maniskill.ai/research
---

# SAPIEN Open-Source Manipulation Skill (ManiSkill)

官网：https://www.maniskill.ai/research

## 自定义任务构建

1. 继承自`BaseEnv`
2. 环境注册是通过 `@register_env(env_id, max_episode_steps=...)`

```python
import sapien
from mani_skill.utils import sapien_utils, common
from mani_skill.envs.sapien_env import BaseEnv
from mani_skill.utils.registration import register_env

@register_env("PushCube-v1", max_episode_steps=50)
class PushCubeEnv(BaseEnv):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
```

### Loading

环境调用 `env._reconfigure()` 来加载机器人、资产、关节、照明等，加载完成后环境会被冻结，资产无法添加或者移除，直到下一次 `env._reconfigure()` 被调用，所以通常只会被调用一次，目标是简单地以初始姿势加载对象，以确保它们不会在第一步发生碰撞。

#### 加载机器人

通过 init 函数指定添加的默认机器人。在 PushCube 中，这是通过添加 `SUPPORTED_ROBOTS` 来完成的，以确保用户只能使用选定的机器人运行您的任务。如果您愿意，您可以进一步添加 `agent` 类属性的类型。



#### 加载Actor

使用`builder.build_kinematic`构建运动学actor，并使用`builder.build_static`构建静态actor。

- 能使用静态的就不要使用动态的
- 运动和静态角色固定在适当的位置，但可以阻止物体穿过它们（例如墙壁、厨房柜台）。
- 运动演员可以随时改变姿势。静态演员在通过builder.initial_pose = ...调用build_static之前必须设置初始姿势



## 加载 Actors 和 Articulations

### 加载Actors

有两种方法，直接从现有的模拟就绪资产数据集加载，或通过较低级别的 ActorBuilder API 加载。

#### 从现有数据集加载

目前仅仅支持 [YCB数据库](https://www.ycbbenchmarks.com/)


#### 使用 ActorBuilder API


#### 使用 URDF 加载器




### 加载关节


## 高级功能



### 自定义机器人



### 传感器/相机





### 自定义可重复使用场景



### 域随机化


## 概念

### Simulation and Robotics

一般约定：

- Pose 由 xyz 和 四元数组成
- 四元数使用wxyz格式
- z轴定义是向上的

#### 模拟物体

ManiSkill/SAPIEN 有两个通用的物体类别： Actor 和 Articulations

##### Actor

Actors 通常是“单一”物体，当受到某种力（如机器人）的物理作用时，整个物体会一起移动而不会产生任何变形。演员可以是棒球棒、玻璃杯、墙壁等。演员具有以下属性：


- 姿势：演员在 3D 空间中的位置。 3D 位置以米为单位。
- 线速度：演员在 x、y 和 z 轴上的平移速度（米/秒）
- 角速度：角色在 x、y 和 z 旋转轴上的角速度（弧度/秒）


Actor 由两个主要元素组成：碰撞形状和视觉形状。

- 碰撞形状：定义了对象在模拟中的行为方式。模拟中单个角色也可以由多个凸碰撞形状组成。
    - 请注意：对象不一定非要有碰撞形状，可以是透明的
- 视觉形状：视觉形状定义了对象在模拟中的渲染方式，与物理模拟无关。

**Actor的三种类别：**
- Dynamic: Actors是完全物理模拟的，如果对Actor施加任何力，它会像在现实世界中一样做出相应的反应。
- Kinematic: Actors是部分物理模拟的。如果对Actor施加任何力，它不会变形或移动一厘米。然而，与该角色交互的动态对象将受到反作用力。然而，与Dynamic相比，Kinematic使用更少的 cpu/gpu 内存，并且模拟速度更快
- Static: 它们与运动学 actor 完全相同，但使用更少的 cpu/gpu 内存，并且模拟速度更快，但代价是加载到模拟后无法更改其姿势。


墙壁、地板、橱柜等物体通常被构建为kinematic/static，因为在现实生活中你通常无法移动/摧毁它们。

根据您要模拟的任务，您可能希望使某些对象动态化。对于要模拟拿起杯子并将其移动到架子上的任务，杯子本身是动态的(dynamic)，而架子可能是运动/静态的(kinematic/static)。

##### Articulations

Aritculations 由 Links 和 Joint 组成


### GPU Simulattion

ManiSkill 利用 PhysX 在GPU上并行执行物理模拟。

**PhysX** 是由 NVIDIA 开发的一款**物理引擎**，主要用于在视频游戏和模拟软件中实现物理效果。它最初由 Ageia 公司开发，后来被 NVIDIA 收购。PhysX 的核心功能是通过模拟现实世界中的物理现象，如碰撞、重力、流体、布料和刚体等，以增强虚拟环境的真实感。以下是 PhysX 的几个关键作用：

1. **碰撞检测和响应**：在游戏和模拟中，物体之间的碰撞是常见现象。PhysX 提供了高效的碰撞检测算法和响应机制，可以确保不同物体之间的交互真实自然，例如人物撞到墙壁、物体跌落等。

2. **刚体动力学**：刚体是指不发生变形的物体，PhysX 能精确地模拟刚体的运动、旋转和碰撞效果。在游戏中，这类物体包括石头、木块、机械部件等。

3. **柔体和流体模拟**：相比于刚体，柔体（如布料）和流体的模拟更为复杂。PhysX 可以用来模拟柔体的变形，例如角色的衣服、旗帜、绳索等，还支持简单的流体模拟，使水、油等流体的运动更加逼真。

4. **粒子系统**：在特效中，粒子系统通常用来模拟烟雾、火焰、爆炸等效果。PhysX 提供了粒子系统，结合物理模拟可以实现更具真实感的视觉效果。

5. **跨平台支持**：PhysX 可以在多种平台上运行，包括 PC、主机（如 PlayStation 和 Xbox）和移动设备（如 Android 和 iOS）。这使得它在不同类型的游戏和应用中广泛应用。

6. **GPU 加速**：PhysX 是一个支持 GPU 加速的物理引擎，尤其在 NVIDIA 自家的显卡上。通过 GPU 加速，可以显著提升物理模拟的计算速度，从而让复杂的物理效果在保证帧率的情况下实时呈现出来。

#### 场景与子场景

在 Maniskill 中，将所有的Actors和Articulations放入同一个PhysX场景中，为每个任务分配一个独立的工作区，被称为子场景。

![alt text](assets/physx_scene_subscene_relationship.png)

请注意，如果你设置的spacing过小，可能会导致子场景重叠而影响任务。


### GPU Sim 生命周期


#### GPU上的数据

### ManiSkill 设计原则


## 相关文件

### SAPIEN

SAPIEN 模拟器为机器人、刚体和铰接物体提供物理模拟。它通过纯 Python 界面为强化学习和机器人技术提供支持。它还提供多种渲染模式，包括深度图、法线图、光流、主动光和光线追踪。

[Sapien文档](https://sapien-sim.github.io/docs/user_guide/getting_started/installation.html)

### PartNet-Mobility Dataset

PartNet-Mobility 数据集是带有运动注释和渲染材质的 2K 铰接对象的集合。该数据集为通用计算机视觉和操作的研究提供了动力。该数据集是 ShapeNet 和 PartNet 的延续。

https://sapien.ucsd.edu/browse