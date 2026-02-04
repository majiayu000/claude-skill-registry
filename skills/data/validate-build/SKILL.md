---
description: Validates YARS build by running braitenberg test and comparing logfile output with reference
version: 1.0.0
allowed-tools: [Bash, Read, Glob]
---

# Validate YARS Build

This skill ensures that code changes haven't broken YARS simulation functionality by:

1. Compiling YARS in the ./build directory
2. Running the braitenberg_logging.xml test with 1000 iterations and 60s timeout
3. Comparing the generated logfile with the reference logfile
4. Reporting success only if compilation succeeds, simulation runs without errors, and logfiles match

## Usage

Automatically invoked when:
- User asks to validate changes
- After significant code modifications
- Before committing changes
- When testing build integrity

## Validation Steps

```bash
# Navigate to build directory
cd build

# Verify all dependencies are installed
echo "Checking dependencies..."
brew list boost xerces-c bullet sdl2 2>/dev/null || echo "Missing dependencies - install with: brew install boost xerces-c bullet sdl2"

# Compile YARS (with Boost path for macOS Homebrew)
cmake -DCMAKE_PREFIX_PATH=/opt/homebrew .. && make -j4

# Check if build succeeded
if [ ! -f ./bin/yars ]; then
  echo "Build failed - binary not created"
  exit 1
fi

# Run braitenberg test with timeout
timeout 60s ./bin/yars --iterations 1000 --xml ../xml/braitenberg_logging.xml

# Compare logfiles
diff braitenberg-*.csv ../reference_logfile.csv
```

## Success Criteria

- ✅ All dependencies installed (Boost, Xerces-C++, Bullet, SDL2)
- ✅ CMake configuration completes without errors
- ✅ Compilation completes without errors or warnings
- ✅ YARS binary created successfully
- ✅ YARS runs without crashes or timeouts
- ✅ Generated logfile matches reference exactly (diff shows no differences)

## Dependency Requirements

**Required Libraries:**
- Boost (program_options, circular_buffer)
- Xerces-C++ (XML parsing)
- Bullet Physics (physics simulation)
- SDL2 (windowing)
- Ogre3D (in ext/ogre/install/)

**Install on macOS:**
```bash
brew install boost xerces-c bullet sdl2
```

## Notes

- Always run from project root, using ./build subdirectory
- On macOS, must specify CMAKE_PREFIX_PATH=/opt/homebrew for Homebrew libs
- Timeout prevents infinite loops if GUI doesn't close properly
- Any difference in logfile output indicates behavior regression
- Build must be 100% clean before validation passes
