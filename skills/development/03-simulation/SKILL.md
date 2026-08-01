---
name: 03-simulation
description: ManiSkill은 GPU 가속 병렬 시뮬레이션을 제공하는 강화학습 전용 로봇 환경입니다.
---

# 3.5 ManiSkill 강화학습 환경

ManiSkill은 GPU 가속 병렬 시뮬레이션을 제공하는 강화학습 전용 로봇 환경입니다.

## 목차
- [ManiSkill 소개](#maniskill-소개)
- [환경 설정](#환경-설정)
- [XLeRobot 에이전트](#xlerobot-에이전트)
- [키보드 제어 실습](#키보드-제어-실습)
- [강화학습 학습](#강화학습-학습)
- [커스텀 태스크 생성](#커스텀-태스크-생성)

---

## ManiSkill 소개

### ManiSkill이란?

**ManiSkill**은 로봇 조작(manipulation) 강화학습을 위한 벤치마크 환경으로, **SAPIEN** 물리 엔진 기반의 GPU 병렬 시뮬레이션을 제공합니다.

```
┌─────────────────────────────────────┐
│       ManiSkill 아키텍처             │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Gymnasium API             │   │
│  │   (RL 표준 인터페이스)       │   │
│  └─────────────────────────────┘   │
│              ↓                      │
│  ┌─────────────────────────────┐   │
│  │   SAPIEN (물리 엔진)         │   │
│  │   - GPU 병렬화               │   │
│  │   - PhysX 기반               │   │
│  └─────────────────────────────┘   │
│              ↓                      │
│  ┌─────────────────────────────┐   │
│  │   로봇 에이전트              │   │
│  │   - XLeRobot                │   │
│  │   - Fetch, Panda 등          │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

### 주요 특징

1. **GPU 병렬 시뮬레이션**: 수백 개 환경 동시 실행
2. **Gymnasium 호환**: 표준 RL 인터페이스
3. **벤치마크 태스크**: PushCube, PickPlace, AssemblyTask 등
4. **다양한 로봇**: Fetch, Panda, XLeRobot 등
5. **사실적인 환경**: ReplicaCAD 씬 (실제 방 스캔)

### MuJoCo vs ManiSkill 비교

| 항목 | MuJoCo | ManiSkill |
|------|--------|-----------|
| **목적** | 제어 개발 | 강화학습 |
| **병렬화** | 1개 환경 | 수백 개 (GPU) |
| **Gym 호환** | 수동 래핑 | 네이티브 |
| **태스크** | 직접 구현 | 사전 정의됨 |
| **학습 속도** | 느림 (CPU) | 빠름 (GPU) |
| **커스터마이징** | 쉬움 | 중간 |

---

## 환경 설정

### 시스템 요구사항

| 구성 요소 | 최소 | 권장 |
|-----------|------|------|
| **OS** | Ubuntu 20.04 | Ubuntu 22.04 |
| **Python** | 3.8 | 3.10+ |
| **GPU** | NVIDIA GTX 1060 (6GB) | RTX 3060 (12GB) |
| **CUDA** | 11.8+ | 12.0+ |
| **RAM** | 8GB | 16GB |
| **디스크** | 10GB | 20GB |

### 1단계: ManiSkill 설치

```bash
# XLeRobot ManiSkill 디렉토리로 이동
cd ~/XLeRobot/simulation/Maniskill/

# Python 가상 환경 생성
python3 -m venv .venv
source .venv/bin/activate

# ManiSkill 설치 (최신 버전)
pip install mani-skill

# 추가 의존성
pip install gymnasium
pip install sapien
pip install numpy
pip install torch  # PyTorch (선택, RL 학습용)
```

**설치 시간**: 5-10분

---

### 2단계: XLeRobot 에이전트 등록 확인

```bash
# XLeRobot 에이전트 파일 확인
ls ~/XLeRobot/simulation/Maniskill/agents/xlerobot/

# 예상 출력:
# __init__.py
# xlerobot.py
```

**`agents/xlerobot/xlerobot.py`** 파일에 XLeRobot 에이전트 정의되어 있음:
- `xlerobot_single`: 단일 팔 버전
- `xlerobot_dual`: 듀얼 팔 버전

---

### 3단계: 첫 실행 테스트

```bash
# ManiSkill 디렉토리에서
cd ~/XLeRobot/simulation/Maniskill/

# 가상 환경 활성화
source .venv/bin/activate

# 간단한 시뮬레이션 실행
python run_xlerobot_sim.py
```

**예상 출력**:
```
Starting XLeRobot simulation...
Environment created successfully!
Observation space: Dict(...)
Action space: Box(...)
Control mode: pd_joint_delta_pos
Reward mode: normalized_dense

Simulation is running. Close the viewer window to exit.

Keyboard Controls:
- W/S: Base Forward/Back
- A/D: Base Rotation
- Arrow keys: Arm control
- Space: Pause/Resume
```

**3D 뷰어 창**이 열리고 XLeRobot이 PushCube 태스크 환경에 있어야 합니다.

---

## XLeRobot 에이전트

### 에이전트 종류

ManiSkill XLeRobot 구현에는 2가지 버전이 있습니다:

#### 1. `xlerobot_single` (단일 팔)

```python
robot_uids = "xlerobot_single"
```

**구성**:
- 옴니휠 베이스 (3자유도)
- 단일 SO-100 팔 (6자유도)
- 그리퍼 (1자유도)
- **총 10 DOF**

**용도**: 단순한 pick-and-place 태스크

---

#### 2. `xlerobot_dual` (듀얼 팔)

```python
robot_uids = "xlerobot_dual"
```

**구성**:
- 옴니휠 베이스 (3자유도)
- 왼팔 SO-100 (6자유도)
- 오른팔 SO-100 (6자유도)
- 양손 그리퍼 (2자유도)
- **총 17 DOF**

**용도**: 양손 협업 작업 (조립, 정리 등)

---

### 제어 모드

ManiSkill은 여러 제어 모드를 지원합니다:

| 모드 | 설명 | 입력 차원 | 난이도 |
|------|------|-----------|--------|
| `pd_joint_delta_pos` | 관절 증분 위치 | DOF 수 | ⭐⭐ 쉬움 |
| `pd_joint_pos` | 관절 절대 위치 | DOF 수 | ⭐⭐ 쉬움 |
| `pd_joint_vel` | 관절 속도 | DOF 수 | ⭐⭐⭐ 중간 |
| `pd_ee_delta_pose` | 엔드이펙터 증분 포즈 | 7 (pos + quat) | ⭐⭐⭐⭐ 어려움 |
| `pd_ee_target_pose` | 엔드이펙터 목표 포즈 | 7 | ⭐⭐⭐⭐ 어려움 |

**추천**: `pd_joint_delta_pos` (학습 초기)

---

### 관찰 모드

| 모드 | 설명 | 크기 | 용도 |
|------|------|------|------|
| `state` | 로봇 상태 (관절 각도, 속도) | ~20-50 | 초기 학습 |
| `rgbd` | RGB-D 이미지 | (H, W, 4) | 비전 기반 정책 |
| `pointcloud` | 포인트 클라우드 | (N, 3) | 3D 인식 |
| `sensor` | 모든 센서 데이터 | 가변 | 복합 정책 |

**추천**: `state` (학습 초기)

---

## 키보드 제어 실습

ManiSkill에서 XLeRobot을 키보드로 제어하며 환경을 이해합니다.

### 실행 방법

```bash
cd ~/XLeRobot/simulation/Maniskill/
source .venv/bin/activate

# 키보드 제어 예제 실행 (단일 팔)
python examples/demo_ctrl_action_ee_keyboard_single.py \
  -e "ReplicaCAD_SceneManipulation-v1" \
  -r "xlerobot_single" \
  --render-mode="human" \
  --shader="rt-fast" \
  -c "pd_joint_delta_pos"
```

**파라미터 설명**:
- `-e`: 환경 ID (`ReplicaCAD_SceneManipulation-v1`)
- `-r`: 로봇 UID (`xlerobot_single`)
- `--render-mode`: 렌더링 모드 (`human` = GUI)
- `--shader`: 셰이더 (`rt-fast` = 빠른 렌더링)
- `-c`: 제어 모드 (`pd_joint_delta_pos`)

---

### 키보드 제어 키

#### 베이스 제어

| 키 | 동작 |
|----|------|
| `W` | 전진 |
| `S` | 후진 |
| `A` | 좌회전 |
| `D` | 우회전 |
| `Q` | 좌이동 |
| `E` | 우이동 |

#### 팔 제어 (화살표 키)

| 키 | 동작 |
|----|------|
| `↑` | 팔 위로 |
| `↓` | 팔 아래로 |
| `←` | 팔 왼쪽으로 |
| `→` | 팔 오른쪽으로 |
| `[` | 팔 앞으로 |
| `]` | 팔 뒤로 |

#### 그리퍼

| 키 | 동작 |
|----|------|
| `G` | 그리퍼 열기 |
| `H` | 그리퍼 닫기 |

#### 시스템

| 키 | 동작 |
|----|------|
| `Space` | 일시정지/재개 |
| `R` | 환경 리셋 |
| `ESC` | 종료 |

---

### 실습: PushCube 태스크

**목표**: 큐브를 목표 위치로 밀기

**절차**:
1. 프로그램 실행 (위 명령어)
2. 뷰어 창에서 큐브와 목표 영역 확인
3. `W/A/S/D`로 베이스 이동
4. 화살표 키로 팔 위치 조정
5. 큐브에 접근하여 밀기
6. 목표 영역에 큐브가 들어가면 성공!

**성공 기준**:
- 큐브가 녹색 목표 영역 안에 위치
- Reward 값이 1.0에 가까워짐

---

## 강화학습 학습

ManiSkill의 진정한 강점은 **GPU 병렬 시뮬레이션**을 통한 빠른 RL 학습입니다.

### 1. Gymnasium 환경 생성

```python
# simple_rl_example.py
import gymnasium as gym
import numpy as np
from mani_skill.envs.sapien_env import BaseEnv

# 병렬 환경 생성 (64개)
env_kwargs = dict(
    obs_mode="state",
    control_mode="pd_joint_delta_pos",
    render_mode=None,  # 학습 시에는 렌더링 OFF
    robot_uids="xlerobot_single",
    num_envs=64,  # GPU 병렬화!
    sim_backend="gpu",  # GPU 시뮬레이션
)

env: BaseEnv = gym.make("PushCube-v1", **env_kwargs)

# 환경 리셋
obs, info = env.reset(seed=0)

print(f"Observation shape: {obs['agent']['qpos'].shape}")  # (64, 10)
print(f"Action shape: {env.action_space.shape}")  # (64, 10)

# 랜덤 액션 실행
for _ in range(100):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    print(f"Mean reward: {reward.mean():.3f}")

    if terminated.any():
        env.reset()

env.close()
```

**실행**:
```bash
python simple_rl_example.py
```

**출력**:
```
Observation shape: (64, 10)  ← 64개 환경 병렬
Action shape: (64, 10)
Mean reward: -0.124
Mean reward: -0.089
...
```

---

### 2. PPO 학습 예제

**Stable Baselines3**를 사용한 PPO 학습:

```bash
# Stable Baselines3 설치
pip install stable-baselines3
```

```python
# train_ppo.py
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# 환경 생성 함수
def make_env():
    env = gym.make(
        "PushCube-v1",
        obs_mode="state",
        control_mode="pd_joint_delta_pos",
        robot_uids="xlerobot_single",
        num_envs=1,
        render_mode=None,
    )
    return env

# 벡터화된 환경 (8개 병렬)
env = DummyVecEnv([make_env for _ in range(8)])

# PPO 모델 생성
model = PPO(
    "MultiInputPolicy",
    env,
    verbose=1,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    device="cuda",  # GPU 사용
)

# 학습 시작 (100만 스텝)
model.learn(total_timesteps=1_000_000)

# 모델 저장
model.save("xlerobot_pushcube_ppo")

print("Training complete!")
```

**실행**:
```bash
python train_ppo.py
```

**예상 학습 시간**:
- CPU: 8-12시간
- GPU (RTX 3060): 2-3시간

---

### 3. 학습된 모델 평가

```python
# eval_policy.py
import gymnasium as gym
from stable_baselines3 import PPO

# 모델 로드
model = PPO.load("xlerobot_pushcube_ppo")

# 환경 생성 (렌더링 ON)
env = gym.make(
    "PushCube-v1",
    obs_mode="state",
    control_mode="pd_joint_delta_pos",
    robot_uids="xlerobot_single",
    num_envs=1,
    render_mode="human",
)

# 평가 루프
obs, _ = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()

    if terminated or truncated:
        obs, _ = env.reset()

env.close()
```

**실행**:
```bash
python eval_policy.py
```

**관찰 포인트**:
- 로봇이 자동으로 큐브를 목표 위치로 이동
- 부드러운 움직임 (학습된 정책)

---

## 커스텀 태스크 생성

ManiSkill에서 자신만의 태스크를 만들 수 있습니다.

### 예제: PickAndPlace 태스크

```python
# custom_task.py
import numpy as np
import sapien
from mani_skill.envs.sapien_env import BaseEnv
from mani_skill.utils import sapien_utils
from mani_skill.utils.registration import register_env

@register_env("XLeRobotPickPlace-v1", max_episode_steps=200)
class XLeRobotPickPlaceEnv(BaseEnv):
    """XLeRobot Pick and Place 태스크"""

    SUPPORTED_ROBOTS = ["xlerobot_single"]
    agent: "XLeRobotSingle"

    def __init__(self, *args, robot_uids="xlerobot_single", **kwargs):
        super().__init__(*args, robot_uids=robot_uids, **kwargs)

    def _load_scene(self, options: dict):
        """씬 로드: 바닥, 테이블, 큐브, 목표 영역"""
        # 바닥
        self.scene.add_ground(altitude=0)

        # 테이블
        builder = self.scene.create_actor_builder()
        builder.add_box_collision(half_size=[0.4, 0.4, 0.02])
        builder.add_box_visual(half_size=[0.4, 0.4, 0.02], color=[0.8, 0.6, 0.4])
        self.table = builder.build_static(name="table")
        self.table.set_pose(sapien.Pose([0.5, 0, 0.4]))

        # 큐브 (집을 물체)
        builder = self.scene.create_actor_builder()
        builder.add_box_collision(half_size=[0.02, 0.02, 0.02])
        builder.add_box_visual(half_size=[0.02, 0.02, 0.02], color=[1, 0, 0])
        self.cube = builder.build(name="cube")

        # 목표 위치 시각화
        builder = self.scene.create_actor_builder()
        builder.add_sphere_visual(radius=0.03, color=[0, 1, 0, 0.5])
        self.goal_site = builder.build_static(name="goal")

    def _initialize_episode(self, env_idx: np.ndarray, options: dict):
        """에피소드 초기화: 로봇, 큐브, 목표 위치 랜덤 배치"""
        # 큐브 위치 랜덤 (테이블 위)
        cube_pos = np.array([0.5, 0, 0.45]) + np.random.uniform(-0.1, 0.1, 3)
        cube_pos[2] = 0.45  # Z는 고정
        self.cube.set_pose(sapien.Pose(cube_pos))

        # 목표 위치 랜덤
        goal_pos = np.array([0.5, 0, 0.45]) + np.random.uniform(-0.15, 0.15, 3)
        goal_pos[2] = 0.45
        self.goal_site.set_pose(sapien.Pose(goal_pos))

        # 로봇 초기 위치
        self.agent.robot.set_pose(sapien.Pose([0, 0, 0]))

    def evaluate(self):
        """보상 계산"""
        # 큐브와 목표 사이 거리
        cube_pos = self.cube.pose.p
        goal_pos = self.goal_site.pose.p
        distance = np.linalg.norm(cube_pos - goal_pos)

        # 거리 기반 보상
        reward = -distance

        # 성공 판정 (거리 < 5cm)
        success = distance < 0.05

        return {
            "success": success,
            "distance": distance,
            "reward": reward,
        }

    def compute_dense_reward(self, obs, action, info):
        """Dense reward"""
        return info["reward"]

    def compute_normalized_dense_reward(self, obs, action, info):
        """Normalized reward [0, 1]"""
        max_dist = 0.5
        return np.clip(1 - info["distance"] / max_dist, 0, 1)
```

**사용 방법**:

```python
# test_custom_task.py
import gymnasium as gym
from custom_task import XLeRobotPickPlaceEnv

env = gym.make(
    "XLeRobotPickPlace-v1",
    obs_mode="state",
    control_mode="pd_joint_delta_pos",
    render_mode="human",
)

obs, _ = env.reset()
for _ in range(1000):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()

    print(f"Reward: {reward:.3f}, Distance: {info['distance']:.3f}")

    if terminated or truncated:
        obs, _ = env.reset()

env.close()
```

---

## 고급 기능

### 1. 데이터셋 수집

```python
# collect_dataset.py
import gymnasium as gym
from mani_skill.utils.wrappers import RecordEpisode

# 환경 래핑 (데이터 기록)
env = gym.make("PushCube-v1", render_mode="cameras")
env = RecordEpisode(
    env,
    output_dir="./demos",
    save_trajectory=True,
    save_video=True,
)

# 데모 수집 (키보드 텔레오퍼레이션)
# ... 키보드로 제어하며 데이터 수집

# 저장된 데이터:
# - demos/trajectory_0.h5 (상태, 액션)
# - demos/video_0.mp4 (비디오)
```

**활용**: Imitation Learning (BC, GAIL)

---

### 2. ReplicaCAD 씬

```python
# ReplicaCAD: 실제 방 스캔 데이터 기반 환경
env = gym.make(
    "ReplicaCAD_SceneManipulation-v1",
    robot_uids="xlerobot_single",
    render_mode="human",
)

# 사실적인 가구, 물체 배치
# 복잡한 네비게이션 + 조작 태스크
```

---

### 3. Multi-Task Learning

```python
# 여러 태스크 동시 학습
tasks = ["PushCube-v1", "PickCube-v1", "StackCube-v1"]

for task in tasks:
    env = gym.make(task, robot_uids="xlerobot_dual")
    # ... 학습
```

---

## 문제 해결

### 문제 1: `ImportError: cannot import name 'XLeRobotSingle'`

**원인**: XLeRobot 에이전트가 등록되지 않음

**해결**:
```python
# 스크립트 맨 위에 추가
import sys
sys.path.insert(0, "/home/사용자명/XLeRobot/simulation/Maniskill")
from agents.xlerobot import xlerobot
```

---

### 문제 2: GPU 메모리 부족

**원인**: `num_envs` 너무 큼

**해결**:
```python
# num_envs 줄이기
env_kwargs = dict(
    num_envs=16,  # 64 → 16
    sim_backend="gpu",
)
```

---

### 문제 3: 렌더링 느림

**원인**: 고급 셰이더 사용

**해결**:
```bash
# rt-fast 대신 minimal 사용
--shader="minimal"
```

---

## 요약

### 핵심 포인트

1. **ManiSkill**: GPU 병렬 RL 환경 (수백 개 동시 실행)
2. **XLeRobot 에이전트**: `xlerobot_single`, `xlerobot_dual`
3. **제어 모드**: `pd_joint_delta_pos` (초보자 추천)
4. **학습**: PPO, SAC 등 표준 RL 알고리즘 사용
5. **커스텀 태스크**: `BaseEnv` 상속으로 쉽게 생성

### 다음 단계

- [3.6 URDF/MJCF 모델 →](https://github.com/dinnerandcoffee/xlerobot-learning-guide/blob/main/learning_guide/03_simulation/06_robot_models.md): 로봇 모델 파일 구조 이해
- [4장 하드웨어 →](https://github.com/dinnerandcoffee/xlerobot-learning-guide/blob/main/learning_guide/04_hardware/README.md): 실제 로봇 조립

---

[← 3.4 Isaac Sim](https://github.com/dinnerandcoffee/xlerobot-learning-guide/blob/main/learning_guide/03_simulation/04_isaac_sim.md) | [3장 목차](https://github.com/dinnerandcoffee/xlerobot-learning-guide/blob/main/learning_guide/03_simulation/README.md) | [다음: 3.6 로봇 모델 →](https://github.com/dinnerandcoffee/xlerobot-learning-guide/blob/main/learning_guide/03_simulation/06_robot_models.md)
