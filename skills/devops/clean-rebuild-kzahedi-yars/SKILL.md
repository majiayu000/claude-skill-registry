---
description: Performs a complete clean rebuild of YARS from scratch
version: 1.0.0
allowed-tools: [Bash]
---

# Clean Rebuild

This skill performs a complete clean rebuild of YARS when build state is questionable or after major changes.

## Usage

Automatically invoked when:
- User asks for a clean build or fresh build
- Build errors suggest stale build artifacts
- After major CMake configuration changes
- When switching between build configurations

## Steps

```bash
# Check and install dependencies if needed (macOS)
echo "Verifying dependencies..."
brew list boost xerces-c bullet sdl2 2>/dev/null || {
  echo "Installing missing dependencies..."
  brew install boost xerces-c bullet sdl2
}

# Remove entire build directory
rm -rf build

# Create fresh build directory
mkdir build && cd build

# Configure with CMake (specify Homebrew path on macOS)
cmake -DCMAKE_PREFIX_PATH=/opt/homebrew ..

# Build with parallel jobs
make -j4

# Verify binary was created
if [ -f ./bin/yars ]; then
  echo "✅ Build successful - binary created at ./bin/yars"
else
  echo "❌ Build failed - binary not found"
  exit 1
fi
```

## Success Criteria

- ✅ All dependencies installed
- ✅ Build directory successfully removed and recreated
- ✅ CMake configuration completes without errors
- ✅ Compilation completes without errors or warnings
- ✅ YARS binary successfully created at build/bin/yars

## Dependency Requirements

**macOS (Homebrew):**
```bash
brew install boost xerces-c bullet sdl2
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libboost-all-dev libxerces-c-dev libbullet-dev libsdl2-dev
```

## Notes

- Always executed from project root
- Removes ALL build artifacts including CMake cache
- Use this when incremental builds fail or behave oddly
- Takes longer than incremental build but guarantees clean state
- On macOS, requires CMAKE_PREFIX_PATH=/opt/homebrew for Homebrew libraries
- Ogre3D should be pre-built in ext/ogre/install/
