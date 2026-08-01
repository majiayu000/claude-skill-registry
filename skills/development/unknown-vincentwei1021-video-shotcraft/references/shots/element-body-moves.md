---
name: element-body-moves
一句话: 元素身体感两式——axial-stretch 轴向拉伸糖稀拉丝、contact-shadow-lift 接触阴影离面抬升
适用: 给"位置在变"之外补"身体在变"：高速飞入给速度肉身（A）、卡片点名给悬浮证据（B）；A 配横冲入场，B 配 2.5D 运镜与逐张点名
时长: A ~4.7s / B ~5.3s
能量: A 中高 / B 低中
---

## 意图
库内运动卡全在管"位置在变"——飞入、滑动、弹跳，元素本身始终是刚体。
这两式管**身体在变**：A 给速度一个可见的肉身——飞得越快沿运动轴拉得
越长，一块糖稀，落点压扁回弹收正，squash & stretch 的 UI 翻译；B 给
悬浮一个可信的证据——卡抬起时正下方阴影同步放大变淡，纸片离桌，
staging 法则给 2.5D 运镜垫的物理台词。与 smear-multiples 的区别：那是
可数残像（离散鬼影），A 是连续拉伸（糖稀不断丝）；与 CameraMotionBlur
的区别：快门拖影是相机的事，拉伸是身体的事，同一元素别叠加。

## 两式选型
| 式 | 做法 | 适用 |
|----|------|------|
| A axial-stretch | 速度差分驱动轴向 scale：v=\|p(f)−p(f−1)\|，v<2px/f 不拉伸、≥140px/f 满拉伸（scaleX 2.2 / scaleY 0.72）；落点 8f 压扁回弹 | 高速飞入/横冲入场；多卡错峰填坑 |
| B contact-shadow-lift | 抬起 10f out-cubic：卡 translateY(−28px)+scale(1.08)，独立椭圆阴影 scale 1→1.72 / opacity 0.55→0.18 同进度反向；落回 8f in-cubic + 2f 微压卡壳 | 逐张点名强调；2.5D 段落的离面铺垫 |

## 参数表
| 参数 | 典型值 | 调节手感 |
|------|--------|----------|
| A 拉伸映射 | v∈[2,140]px/f → 拉伸 0→满（scaleX 2.2/scaleY 0.72） | 峰值 <1.6 不可感；>2.6 读作故障拉丝 |
| A origin/顺序 | transformOrigin 设运动后缘（右飞 100% 50%）；translate 再 scale | origin 居中读作缩放不是拉伸；顺序反了位移跟着放大 |
| A 落点回弹 | 8f out-cubic：scaleX 过冲 0.85、scaleY 1.1 再回 1 | 无回弹的拉伸像刹不住车 |
| A 错峰 | 三卡起飞间隔 12f，飞行 36f | 同帧齐飞读不出各自的拉丝 |
| B 抬升幅度 | −28px + scale 1.08 | 判例锁死：<12px 禁用（见已知坑） |
| B 阴影 | 独立 radial-gradient 椭圆 div；卡本体 boxShadow: none | box-shadow 跟卡走，给不出"影子留在桌上" |
| B 落地 | scale 0.99 卡壳 2f 再 5f 回弹到 1 | 无微压读作飘落，没有重量 |
| 收尾 | A 末卡回弹后 62f / B 全落回后 35f 真静止 | 收尾帧须与 rest 态逐像素一致 |

## 已知坑
- demo 在灰阶/占位素材上调校通过——参数是调校起点非实战定稿，
  首次实战须以真实素材回验
- B 微幅加码判例：原案 8px 抬升不可感，加码到 28px 才过——实战禁回调到 12px 以下，宁可不用不可用弱
- A 速度必须位置差分实算，不许拿 easing 进度近似——差分才保证
  "低于阈值不拉伸"，起步与将落时自动收正
- A 竖向运动轴要换：竖飞拉 scaleY 压 scaleX，origin 设上/下缘，
  照抄横版参数会拉错轴（原案就把轴写反过）
- B 一次只抬一张——两张同时离桌，观众找不到被点名的是谁（P4）
- 声音：A 落点一声闷撞、B 抬起轻吸/落回轻放（sound-design §4.5）

## 参考实现
demos/element-body-moves/
（AxialStretch.tsx / ContactShadowLift.tsx）
