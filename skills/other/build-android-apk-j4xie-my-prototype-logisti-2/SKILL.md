---
name: build-android-apk
description: 自动化构建 React Native Android APK。包括依赖检查、Debug/Release 构建、设备安装。使用此 Skill 来构建 APK、测试安装、或排查构建问题。
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Android APK 构建 Skill

## 项目信息

| 项目 | 值 |
|------|-----|
| 应用 ID | `com.cretas.foodtrace` |
| 前端目录 | `frontend/CretasFoodTrace` |
| 构建脚本 | `scripts/build-android-apk.sh` |

## 一键构建

```bash
cd /Users/jietaoxie/my-prototype-logistics

# Debug APK（推荐测试）
./scripts/build-android-apk.sh

# Release APK
./scripts/build-android-apk.sh -t release

# 构建并安装到设备
./scripts/build-android-apk.sh -c -i
```

## 环境依赖

```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home
export ANDROID_HOME=/Users/jietaoxie/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

## 手动构建

```bash
cd frontend/CretasFoodTrace

# 1. 安装依赖 + prebuild
npm install
npx expo prebuild --platform android

# 2. 构建 APK
cd android
./gradlew assembleDebug --no-daemon   # Debug
./gradlew assembleRelease --no-daemon # Release

# 3. APK 输出位置
ls app/build/outputs/apk/debug/app-debug.apk
ls app/build/outputs/apk/release/app-release.apk
```

## 安装到设备

```bash
$ANDROID_HOME/platform-tools/adb devices                    # 检查设备
$ANDROID_HOME/platform-tools/adb install -r app-debug.apk  # 安装
$ANDROID_HOME/platform-tools/adb shell am start -n com.cretas.foodtrace/.MainActivity
```

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| `JAVA_HOME not set` | `export JAVA_HOME=...jdk-17.jdk/Contents/Home` |
| `SDK location not found` | `export ANDROID_HOME=~/Library/Android/sdk` |
| `No connected devices` | 启动模拟器: `$ANDROID_HOME/emulator/emulator -avd <name>` |
| Build failed | `./gradlew clean` 或删除 `.gradle` 目录 |
| Out of memory | 增加 `gradle.properties` 中 `org.gradle.jvmargs` |

## 清理缓存

```bash
cd frontend/CretasFoodTrace/android
./gradlew --stop && ./gradlew clean
rm -rf ~/.gradle/caches .gradle app/build
```

## Release 签名

```bash
# 生成密钥库
keytool -genkeypair -v -storetype PKCS12 -keystore cretas-release.keystore \
  -alias cretas -keyalg RSA -keysize 2048 -validity 10000

# 配置 android/gradle.properties
MYAPP_RELEASE_STORE_FILE=cretas-release.keystore
MYAPP_RELEASE_KEY_ALIAS=cretas
MYAPP_RELEASE_STORE_PASSWORD=your_password
```
