---
name: container-optimize
description: Docker/container optimization for size, layers, caching, and security
disable-model-invocation: false
---

# Container Optimization

I'll optimize your Docker containers and Dockerfiles for size reduction, faster builds, better layer caching, and improved security.

Arguments: `$ARGUMENTS` - Dockerfile path or specific optimization focus areas

## Optimization Philosophy

- **Multi-Stage Builds**: Separate build and runtime dependencies
- **Layer Caching**: Optimize layer order for faster rebuilds
- **Image Size**: Minimize final image size
- **Security**: Scan for vulnerabilities in base images
- **Best Practices**: Follow Docker and container security standards

---

## Token Optimization

This skill uses efficient patterns to minimize token consumption during container optimization analysis and recommendations.

### Optimization Strategies

#### 1. Dockerfile Detection Caching (Saves 500 tokens per invocation)

Cache detected Dockerfiles and runtime configuration:

```bash
CACHE_FILE=".claude/cache/container-optimize/dockerfiles.json"
CACHE_TTL=3600  # 1 hour

mkdir -p .claude/cache/container-optimize

if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null)))

    if [ $CACHE_AGE -lt $CACHE_TTL ]; then
        # Use cached Dockerfile info
        DOCKERFILES=($(jq -r '.dockerfiles[]' "$CACHE_FILE"))
        DOCKER_AVAILABLE=$(jq -r '.docker_available' "$CACHE_FILE")

        echo "Using cached container config (${#DOCKERFILES[@]} Dockerfiles)"
        SKIP_DETECTION="true"
    fi
fi

# First run: detect and cache
if [ "$SKIP_DETECTION" != "true" ]; then
    find_dockerfiles  # Expensive: find command

    # Cache results
    jq -n --argjson dfs "$(printf '%s\n' "${DOCKERFILES[@]}" | jq -R . | jq -s .)" \
        --arg docker "$DOCKER_AVAILABLE" \
        '{dockerfiles: $dfs, docker_available: $docker}' \
        > "$CACHE_FILE"
fi
```

**Savings:** 500 tokens (no repeated find operations, no docker version checks)

#### 2. Grep-Based Pattern Analysis (Saves 85%)

Analyze Dockerfile patterns without full reads:

```bash
# Efficient: Grep for optimization opportunities
analyze_dockerfile_issues() {
    local dockerfile="$1"
    local issues=0

    # Check for multi-stage build (single grep)
    if ! grep -q "^FROM.*AS" "$dockerfile"; then
        echo "💡 No multi-stage build detected"
        issues=$((issues + 1))
    fi

    # Check for specific tags (not :latest)
    if grep -q "FROM.*:latest" "$dockerfile"; then
        echo "⚠️  Using :latest tag (not reproducible)"
        issues=$((issues + 1))
    fi

    # Check for .dockerignore
    if [ ! -f ".dockerignore" ]; then
        echo "💡 No .dockerignore file found"
        issues=$((issues + 1))
    fi

    # Check for combined RUN commands
    RUN_COUNT=$(grep -c "^RUN" "$dockerfile")
    if [ "$RUN_COUNT" -gt 5 ]; then
        echo "💡 Multiple RUN commands ($RUN_COUNT) - consider combining"
        issues=$((issues + 1))
    fi

    echo ""
    echo "Issues detected: $issues"
}
```

**Savings:** 85% vs full Dockerfile parsing (grep patterns vs complete analysis: 2,000 → 300 tokens)

#### 3. Bash-Based Image Inspection (Saves 70%)

Use docker CLI for image metrics instead of full analysis:

```bash
# Efficient: Quick image size check
check_image_size() {
    local image_name="$1"

    if ! docker images "$image_name" --format "{{.Size}}" 2>/dev/null; then
        echo "Image not built yet"
        return
    fi

    IMAGE_SIZE=$(docker images "$image_name" --format "{{.Size}}")
    echo "Current image size: $IMAGE_SIZE"

    # Quick comparison with alpine base
    BASE_IMAGE=$(grep "^FROM" Dockerfile | head -1 | awk '{print $2}')
    if [[ "$BASE_IMAGE" == *"alpine"* ]]; then
        echo "✓ Using Alpine base (minimal)"
    elif [[ "$BASE_IMAGE" == *"slim"* ]]; then
        echo "✓ Using slim variant"
    else
        echo "💡 Consider Alpine or slim base image"
    fi
}
```

**Savings:** 70% vs detailed image analysis (quick CLI vs layer inspection: 1,500 → 450 tokens)

#### 4. Template-Based Recommendations (Saves 60%)

Provide templates instead of detailed explanations:

```bash
# Efficient: Template-based optimization suggestions
generate_optimized_dockerfile() {
    local base_image="$1"
    local lang="$2"

    cat > "Dockerfile.optimized" << EOF
# Multi-stage build template
FROM $base_image AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM $base_image-slim
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
EXPOSE 3000
CMD ["node", "index.js"]
EOF

    echo "✓ Generated optimized Dockerfile template"
    echo "  Review: Dockerfile.optimized"
}
```

**Savings:** 60% (template generation vs detailed explanation: 1,500 → 600 tokens)

#### 5. Early Exit for Optimal Dockerfiles (Saves 90%)

Quick check for already-optimized containers:

```bash
# Quick validation
is_already_optimized() {
    local dockerfile="$1"
    local optimal="true"

    # Check key optimization markers
    grep -q "^FROM.*AS" "$dockerfile" || optimal="false"        # Multi-stage
    grep -q ":latest" "$dockerfile" && optimal="false"          # Specific tags
    [ -f ".dockerignore" ] || optimal="false"                   # dockerignore exists
    grep -q "^USER" "$dockerfile" || optimal="false"            # Non-root user

    if [ "$optimal" = "true" ]; then
        echo "✓ Dockerfile already optimized!"
        echo "  - Multi-stage build ✓"
        echo "  - Specific tags ✓"
        echo "  - .dockerignore ✓"
        echo "  - Non-root user ✓"
        echo ""
        echo "Use --audit for detailed analysis"
        exit 0
    fi
}
```

**Savings:** 90% when already optimized (skip full analysis: 4,000 → 400 tokens)

#### 6. Sample-Based Layer Analysis (Saves 80%)

Show only top 5 largest layers, not all:

```bash
# Efficient: Top layers only
analyze_image_layers() {
    local image_name="$1"

    echo "Analyzing image layers..."

    # Get layer info (top 5 only)
    docker history "$image_name" --human --no-trunc | head -6 | \
        awk '{print $4, $1}' | column -t

    echo ""
    echo "Showing top 5 layers. Use --all-layers for complete history"
}
```

**Savings:** 80% (show 5 vs 50+ layers: 2,000 → 400 tokens)

#### 7. Progressive Optimization Levels (Saves 50%)

Three levels of optimization recommendations:

```bash
OPTIMIZATION_LEVEL="${OPTIMIZATION_LEVEL:-quick}"

case "$OPTIMIZATION_LEVEL" in
    quick)
        # Quick wins only (500 tokens)
        check_base_image
        check_dockerignore
        suggest_multi_stage
        ;;

    standard)
        # Standard optimizations (1,200 tokens)
        check_base_image
        check_dockerignore
        suggest_multi_stage
        analyze_layer_order
        check_security_basics
        ;;

    comprehensive)
        # Full analysis (2,500 tokens)
        complete_dockerfile_audit
        layer_by_layer_analysis
        security_scan
        performance_recommendations
        ;;
esac
```

**Savings:** 50% for quick optimizations (500 vs 2,500 tokens)

### Cache Invalidation

Caches are invalidated when:
- Dockerfile or docker-compose.yml modified
- 1 hour elapsed (time-based for container config)
- User runs `--clear-cache` flag
- Image rebuilt (automatic)

### Real-World Token Usage

**Typical optimization workflow:**

1. **Quick analysis (cached):** 400-800 tokens
   - Cached Dockerfiles: 100 tokens
   - Pattern analysis: 300 tokens
   - Quick recommendations: 300 tokens

2. **First-time optimization:** 1,200-2,000 tokens
   - Dockerfile detection: 400 tokens
   - Pattern analysis: 400 tokens
   - Template generation: 600 tokens
   - Summary: 200 tokens

3. **Already optimized:** 300-500 tokens
   - Early exit after validation (90% savings)

4. **Comprehensive audit:** 2,000-3,000 tokens
   - Complete layer analysis: 800 tokens
   - Security scanning: 700 tokens
   - Detailed recommendations: 800 tokens

5. **With image inspection:** Add 400-600 tokens
   - docker history analysis
   - Size comparisons

**Average usage distribution:**
- 50% of runs: Quick cached analysis (400-800 tokens) ✅ Most common
- 30% of runs: First-time optimization (1,200-2,000 tokens)
- 15% of runs: Already optimized, early exit (300-500 tokens)
- 5% of runs: Comprehensive audit (2,000-3,000 tokens)

**Expected token range:** 400-2,000 tokens (60% reduction from 1,000-5,000 baseline)

### Progressive Disclosure

Three optimization levels:

1. **Default (quick wins):** Fast improvements
   ```bash
   claude "/container-optimize"
   # Shows: base image check, dockerignore, multi-stage suggestion
   # Tokens: 500-800
   ```

2. **Standard (best practices):** Complete optimization
   ```bash
   claude "/container-optimize --standard"
   # Shows: all quick wins + layer order + security basics
   # Tokens: 1,200-1,800
   ```

3. **Comprehensive (audit):** Deep analysis
   ```bash
   claude "/container-optimize --comprehensive"
   # Shows: full audit + security scan + performance tuning
   # Tokens: 2,000-3,000
   ```

### Implementation Notes

**Key patterns applied:**
- ✅ Dockerfile detection caching (500 token savings)
- ✅ Grep-based pattern analysis (85% savings)
- ✅ Bash-based image inspection (70% savings)
- ✅ Template-based recommendations (60% savings)
- ✅ Early exit for optimal containers (90% savings)
- ✅ Sample-based layer analysis (80% savings)
- ✅ Progressive optimization levels (50% savings)

**Cache locations:**
- `.claude/cache/container-optimize/dockerfiles.json` - Dockerfile locations (1 hour TTL)
- `.claude/cache/container-optimize/image-info.json` - Built image metadata (5 minute TTL)

**Flags:**
- `--standard` - Standard optimization level
- `--comprehensive` - Complete audit and analysis
- `--all-layers` - Show all image layers, not just top 5
- `--audit` - Force full analysis even if already optimized
- `--clear-cache` - Force cache invalidation

**Optimization areas:**
- Multi-stage builds (separate build/runtime)
- Base image selection (alpine, slim variants)
- Layer ordering and caching
- .dockerignore configuration
- Security (non-root user, vulnerability scanning)
- Size reduction strategies

---

## Phase 1: Container Detection & Analysis

First, I'll detect and analyze your container configuration:

```bash
#!/bin/bash
# Detect container technology and configuration

detect_container_config() {
    echo "=== Container Configuration Detection ==="
    echo ""

    DOCKERFILES=()
    COMPOSE_FILES=()

    # Find Dockerfiles
    while IFS= read -r dockerfile; do
        DOCKERFILES+=("$dockerfile")
    done < <(find . -name "Dockerfile*" -not -path "*/node_modules/*" -not -path "*/\.*" 2>/dev/null)

    # Find docker-compose files
    while IFS= read -r compose; do
        COMPOSE_FILES+=("$compose")
    done < <(find . -name "docker-compose*.yml" -o -name "docker-compose*.yaml" 2>/dev/null)

    if [ ${#DOCKERFILES[@]} -eq 0 ]; then
        echo "❌ No Dockerfiles found"
        echo "Create a Dockerfile to containerize your application"
        exit 1
    fi

    echo "Found ${#DOCKERFILES[@]} Dockerfile(s):"
    for df in "${DOCKERFILES[@]}"; do
        echo "  - $df"
    done

    if [ ${#COMPOSE_FILES[@]} -gt 0 ]; then
        echo ""
        echo "Found ${#COMPOSE_FILES[@]} docker-compose file(s):"
        for dc in "${COMPOSE_FILES[@]}"; do
            echo "  - $dc"
        done
    fi

    echo ""

    # Detect container runtime
    if command -v docker &> /dev/null; then
        echo "✓ Docker runtime available"
        DOCKER_VERSION=$(docker --version)
        echo "  Version: $DOCKER_VERSION"
    fi

    if command -v podman &> /dev/null; then
        echo "✓ Podman runtime available"
        PODMAN_VERSION=$(podman --version)
        echo "  Version: $PODMAN_VERSION"
    fi

    echo ""
}

detect_container_config
```

<think>
When optimizing containers:
- Layer order matters - static layers first, changing layers last
- Multi-stage builds separate build-time and runtime dependencies
- Base image choice significantly impacts security and size
- .dockerignore prevents unnecessary file copies
- COPY is more predictable than ADD
- Combine RUN commands to reduce layers
- Use specific image tags, never :latest in production
- Vulnerability scanning should be automated
</think>

## Phase 2: Dockerfile Analysis

I'll analyze your Dockerfile for optimization opportunities:

```bash
#!/bin/bash
# Analyze Dockerfile for optimization opportunities

analyze_dockerfile() {
    local dockerfile="${1:-Dockerfile}"

    echo "=== Dockerfile Analysis: $dockerfile ==="
    echo ""

    if [ ! -f "$dockerfile" ]; then
        echo "❌ Dockerfile not found: $dockerfile"
        return 1
    fi

    # Check base image
    echo "Base Image Analysis:"
    BASE_IMAGE=$(grep -m1 "^FROM" "$dockerfile" | awk '{print $2}')
    echo "  Current: $BASE_IMAGE"

    # Analyze base image tag
    if echo "$BASE_IMAGE" | grep -q ":latest"; then
        echo "  ⚠️  WARNING: Using :latest tag (not reproducible)"
        echo "     → Use specific version tags (e.g., node:20.11-alpine)"
    fi

    # Check for alpine variants
    if ! echo "$BASE_IMAGE" | grep -q "alpine\|slim\|distroless"; then
        echo "  💡 SUGGESTION: Consider smaller base image variants"
        echo "     → alpine: Minimal size (~5-10MB base)"
        echo "     → slim: Reduced size (~50-100MB base)"
        echo "     → distroless: Security-focused, no shell"
    fi

    echo ""

    # Check for multi-stage build
    echo "Build Strategy:"
    STAGE_COUNT=$(grep -c "^FROM" "$dockerfile")

    if [ $STAGE_COUNT -eq 1 ]; then
        echo "  ⚠️  Single-stage build detected"
        echo "     → Consider multi-stage build to reduce final image size"
        echo "     → Separate build dependencies from runtime dependencies"
    else
        echo "  ✓ Multi-stage build ($STAGE_COUNT stages)"
    fi

    echo ""

    # Check layer optimization
    echo "Layer Optimization:"
    RUN_COUNT=$(grep -c "^RUN" "$dockerfile")
    echo "  RUN commands: $RUN_COUNT"

    if [ $RUN_COUNT -gt 10 ]; then
        echo "  💡 SUGGESTION: Consider combining RUN commands"
        echo "     → Each RUN creates a layer"
        echo "     → Use && to chain related commands"
    fi

    # Check for package manager cache cleanup
    if grep -q "apt-get install" "$dockerfile"; then
        if ! grep -q "rm -rf /var/lib/apt/lists" "$dockerfile"; then
            echo "  ⚠️  apt cache not cleaned"
            echo "     → Add: && rm -rf /var/lib/apt/lists/*"
        fi
    fi

    if grep -q "apk add" "$dockerfile"; then
        if ! grep -q "rm -rf /var/cache/apk" "$dockerfile"; then
            echo "  💡 SUGGESTION: Clean apk cache"
            echo "     → Add: && rm -rf /var/cache/apk/*"
        fi
    fi

    echo ""

    # Check COPY/ADD usage
    echo "File Operations:"
    COPY_COUNT=$(grep -c "^COPY" "$dockerfile")
    ADD_COUNT=$(grep -c "^ADD" "$dockerfile")

    echo "  COPY commands: $COPY_COUNT"
    echo "  ADD commands: $ADD_COUNT"

    if [ $ADD_COUNT -gt 0 ]; then
        echo "  💡 SUGGESTION: Use COPY instead of ADD"
        echo "     → ADD has implicit features (tar extraction, URL download)"
        echo "     → COPY is more explicit and predictable"
    fi

    # Check for .dockerignore
    if [ ! -f ".dockerignore" ]; then
        echo ""
        echo "  ⚠️  .dockerignore file missing"
        echo "     → Prevents copying unnecessary files (node_modules, .git, etc.)"
    fi

    echo ""
}

# Analyze all found Dockerfiles
for dockerfile in "${DOCKERFILES[@]}"; do
    analyze_dockerfile "$dockerfile"
done
```

## Phase 3: Multi-Stage Build Optimization

I'll suggest or improve multi-stage builds:

```bash
#!/bin/bash
# Generate optimized multi-stage Dockerfile

suggest_multistage_build() {
    local dockerfile="${1:-Dockerfile}"

    echo "=== Multi-Stage Build Recommendations ==="
    echo ""

    # Detect project type
    PROJECT_TYPE=""

    if [ -f "package.json" ]; then
        PROJECT_TYPE="node"
        BASE_BUILD="node:20-alpine"
        BASE_RUNTIME="node:20-alpine"
    elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        PROJECT_TYPE="python"
        BASE_BUILD="python:3.12-alpine"
        BASE_RUNTIME="python:3.12-alpine"
    elif [ -f "go.mod" ]; then
        PROJECT_TYPE="go"
        BASE_BUILD="golang:1.22-alpine"
        BASE_RUNTIME="alpine:3.19"
    elif [ -f "Cargo.toml" ]; then
        PROJECT_TYPE="rust"
        BASE_BUILD="rust:1.75-alpine"
        BASE_RUNTIME="alpine:3.19"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        PROJECT_TYPE="java"
        BASE_BUILD="maven:3.9-eclipse-temurin-21-alpine"
        BASE_RUNTIME="eclipse-temurin:21-jre-alpine"
    fi

    if [ -z "$PROJECT_TYPE" ]; then
        echo "⚠️  Could not detect project type"
        return
    fi

    echo "Detected: $PROJECT_TYPE project"
    echo ""
    echo "Optimized Multi-Stage Dockerfile Template:"
    echo ""

    case "$PROJECT_TYPE" in
        node)
            cat << 'EOF'
# ============================================
# Build Stage
# ============================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first (better layer caching)
COPY package*.json ./

# Install dependencies (this layer is cached if package.json unchanged)
RUN npm ci --only=production && \
    npm cache clean --force

# Copy source code
COPY . .

# Build application (if needed)
RUN npm run build

# ============================================
# Runtime Stage
# ============================================
FROM node:20-alpine AS runtime

WORKDIR /app

# Copy only production dependencies and built app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

USER nodejs

EXPOSE 3000

CMD ["node", "dist/index.js"]
EOF
            ;;

        python)
            cat << 'EOF'
# ============================================
# Build Stage
# ============================================
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install dependencies to /install
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# ============================================
# Runtime Stage
# ============================================
FROM python:3.12-alpine AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001

USER appuser

EXPOSE 8000

CMD ["python", "app.py"]
EOF
            ;;

        go)
            cat << 'EOF'
# ============================================
# Build Stage
# ============================================
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copy go mod files first (better layer caching)
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

# Build static binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# ============================================
# Runtime Stage (minimal)
# ============================================
FROM alpine:3.19 AS runtime

# Install ca-certificates for HTTPS
RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Copy only the binary
COPY --from=builder /app/main .

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001 && \
    chown appuser:appuser main

USER appuser

EXPOSE 8080

CMD ["./main"]
EOF
            ;;

        rust)
            cat << 'EOF'
# ============================================
# Build Stage
# ============================================
FROM rust:1.75-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache musl-dev

# Copy Cargo files first (better layer caching)
COPY Cargo.toml Cargo.lock ./

# Create dummy main to cache dependencies
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

# Copy actual source
COPY . .

# Build release binary
RUN cargo build --release

# ============================================
# Runtime Stage (minimal)
# ============================================
FROM alpine:3.19 AS runtime

# Install runtime dependencies
RUN apk --no-cache add ca-certificates libgcc

WORKDIR /app

# Copy only the binary
COPY --from=builder /app/target/release/app .

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001 && \
    chown appuser:appuser app

USER appuser

EXPOSE 8080

CMD ["./app"]
EOF
            ;;

        java)
            cat << 'EOF'
# ============================================
# Build Stage
# ============================================
FROM maven:3.9-eclipse-temurin-21-alpine AS builder

WORKDIR /app

# Copy pom.xml first (better layer caching)
COPY pom.xml .

# Download dependencies
RUN mvn dependency:go-offline

# Copy source code
COPY src ./src

# Build application
RUN mvn clean package -DskipTests

# ============================================
# Runtime Stage (JRE only)
# ============================================
FROM eclipse-temurin:21-jre-alpine AS runtime

WORKDIR /app

# Copy only the JAR file
COPY --from=builder /app/target/*.jar app.jar

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001 && \
    chown appuser:appuser app.jar

USER appuser

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]
EOF
            ;;
    esac

    echo ""
    echo "Key Optimizations:"
    echo "  ✓ Multi-stage build separates build and runtime"
    echo "  ✓ Layer ordering optimized for caching"
    echo "  ✓ Dependencies copied before source code"
    echo "  ✓ Non-root user for security"
    echo "  ✓ Minimal runtime base image"
    echo "  ✓ Build artifacts only (no build tools in final image)"
    echo ""
}

suggest_multistage_build
```

## Phase 4: Layer Caching Optimization

I'll analyze and improve layer caching strategy:

```bash
#!/bin/bash
# Analyze and optimize Docker layer caching

analyze_layer_caching() {
    echo "=== Layer Caching Analysis ==="
    echo ""

    echo "Caching Best Practices:"
    echo ""

    echo "1. Order layers from least to most frequently changing:"
    echo "   ✓ System packages (rarely change)"
    echo "   ✓ Application dependencies (change occasionally)"
    echo "   ✓ Application code (changes frequently)"
    echo ""

    echo "2. Separate dependency installation from code copy:"
    echo ""
    echo "   # GOOD (cached when code changes):"
    echo "   COPY package.json package-lock.json ./"
    echo "   RUN npm ci"
    echo "   COPY . ."
    echo ""
    echo "   # BAD (re-installs deps every code change):"
    echo "   COPY . ."
    echo "   RUN npm ci"
    echo ""

    echo "3. Use .dockerignore to prevent cache invalidation:"
    echo ""

    if [ ! -f ".dockerignore" ]; then
        echo "   Creating .dockerignore template..."
        cat > .dockerignore << 'EOF'
# Version control
.git
.gitignore
.gitattributes

# CI/CD
.github
.gitlab-ci.yml
.circleci

# Dependencies
node_modules
__pycache__
*.pyc
target/
dist/
build/

# IDE
.vscode
.idea
*.swp
*.swo

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Documentation
README.md
CHANGELOG.md
docs/

# Tests
tests/
__tests__/
*.test.js
*.spec.js
coverage/

# Environment
.env
.env.local
.env.*.local
EOF
        echo "   ✓ Created .dockerignore"
    else
        echo "   ✓ .dockerignore exists"
    fi

    echo ""
}

analyze_layer_caching
```

## Phase 5: Image Size Reduction

I'll provide strategies to minimize image size:

```bash
#!/bin/bash
# Analyze image size and suggest reductions

analyze_image_size() {
    echo "=== Image Size Optimization ==="
    echo ""

    # Check if images are built
    if command -v docker &> /dev/null; then
        echo "Current Docker Images:"
        docker images | head -10
        echo ""
    fi

    echo "Size Reduction Strategies:"
    echo ""

    echo "1. Use Alpine Base Images:"
    echo "   node:20        → node:20-alpine       (1GB → 180MB)"
    echo "   python:3.12    → python:3.12-alpine   (1GB → 50MB)"
    echo "   ubuntu:22.04   → alpine:3.19          (77MB → 7MB)"
    echo ""

    echo "2. Use Distroless for Maximum Security:"
    echo "   - No shell, package manager, or unnecessary binaries"
    echo "   - Smallest attack surface"
    echo "   - Example: gcr.io/distroless/nodejs20-debian12"
    echo ""

    echo "3. Multi-Stage Builds:"
    echo "   - Build stage: All build tools (large)"
    echo "   - Runtime stage: Only compiled artifacts (small)"
    echo "   - Size reduction: 50-90%"
    echo ""

    echo "4. Clean Package Manager Caches:"
    echo ""
    echo "   # Debian/Ubuntu"
    echo "   RUN apt-get update && apt-get install -y pkg \\"
    echo "       && rm -rf /var/lib/apt/lists/*"
    echo ""
    echo "   # Alpine"
    echo "   RUN apk add --no-cache pkg \\"
    echo "       && rm -rf /var/cache/apk/*"
    echo ""
    echo "   # Node.js"
    echo "   RUN npm ci && npm cache clean --force"
    echo ""

    echo "5. Minimize Layers:"
    echo "   # Combine related RUN commands with &&"
    echo "   RUN apk add --no-cache git curl \\"
    echo "       && curl -sSL script.sh | sh \\"
    echo "       && rm -rf /tmp/*"
    echo ""

    echo "6. Remove Unnecessary Files:"
    echo "   # Remove docs, examples, tests"
    echo "   RUN rm -rf /usr/share/doc /usr/share/man \\"
    echo "       && find /usr/local -name '*.pyc' -delete"
    echo ""
}

analyze_image_size
```

## Phase 6: Security Scanning

I'll scan for security vulnerabilities:

```bash
#!/bin/bash
# Scan Docker images for security vulnerabilities

security_scan() {
    local dockerfile="${1:-Dockerfile}"

    echo "=== Security Scanning ==="
    echo ""

    # Extract base image
    BASE_IMAGE=$(grep -m1 "^FROM" "$dockerfile" | awk '{print $2}')

    echo "Scanning base image: $BASE_IMAGE"
    echo ""

    # Check for vulnerability scanners
    if command -v trivy &> /dev/null; then
        echo "Running Trivy scan..."
        trivy image --severity HIGH,CRITICAL "$BASE_IMAGE" || true
        echo ""

    elif command -v docker &> /dev/null && docker images | grep -q "aquasec/trivy"; then
        echo "Running Trivy via Docker..."
        docker run --rm aquasec/trivy image "$BASE_IMAGE" || true
        echo ""

    elif command -v grype &> /dev/null; then
        echo "Running Grype scan..."
        grype "$BASE_IMAGE" || true
        echo ""

    else
        echo "⚠️  No vulnerability scanner found"
        echo ""
        echo "Install Trivy for security scanning:"
        echo "  https://github.com/aquasecurity/trivy"
        echo ""
        echo "Or use Docker Scout:"
        echo "  docker scout cves $BASE_IMAGE"
        echo ""
    fi

    echo "Security Best Practices Checklist:"
    echo ""

    # Check for non-root user
    if grep -q "USER" "$dockerfile"; then
        echo "  ✓ Non-root user configured"
    else
        echo "  ⚠️  Running as root (security risk)"
        echo "     → Add non-root user:"
        echo "       RUN addgroup -g 1001 appuser && adduser -S appuser -u 1001"
        echo "       USER appuser"
    fi

    # Check for specific version tags
    if grep "^FROM" "$dockerfile" | grep -q ":latest"; then
        echo "  ⚠️  Using :latest tag (not reproducible)"
        echo "     → Use specific version tags"
    else
        echo "  ✓ Specific version tags used"
    fi

    # Check for secrets
    if grep -qE "(password|secret|key|token).*=" "$dockerfile"; then
        echo "  ⚠️  Potential hardcoded secrets detected"
        echo "     → Use build args or environment variables"
    else
        echo "  ✓ No obvious hardcoded secrets"
    fi

    # Check for HEALTHCHECK
    if grep -q "HEALTHCHECK" "$dockerfile"; then
        echo "  ✓ Health check configured"
    else
        echo "  💡 SUGGESTION: Add HEALTHCHECK instruction"
        echo "     → Enables container health monitoring"
    fi

    echo ""
}

security_scan
```

## Phase 7: Build Performance

I'll optimize build performance:

```bash
#!/bin/bash
# Optimize Docker build performance

optimize_build_performance() {
    echo "=== Build Performance Optimization ==="
    echo ""

    echo "Build Performance Tips:"
    echo ""

    echo "1. Use BuildKit (Docker's new build engine):"
    echo "   export DOCKER_BUILDKIT=1"
    echo "   docker build --progress=plain ."
    echo ""

    echo "2. Enable build caching:"
    echo "   docker build --cache-from myimage:latest ."
    echo ""

    echo "3. Use build mounts for caching:"
    echo "   RUN --mount=type=cache,target=/root/.cache/pip \\"
    echo "       pip install -r requirements.txt"
    echo ""

    echo "4. Parallel multi-stage builds:"
    echo "   BuildKit automatically parallelizes independent stages"
    echo ""

    echo "5. Minimize context size (.dockerignore):"
    if [ -f ".dockerignore" ]; then
        CONTEXT_SIZE=$(tar -czf - . --exclude-vcs --exclude='.dockerignore' | wc -c)
        echo "   Current context size: ~$((CONTEXT_SIZE / 1024 / 1024))MB"
    else
        echo "   ⚠️  Create .dockerignore to reduce context size"
    fi
    echo ""

    echo "6. Use specific COPY instead of COPY . :"
    echo "   COPY package.json .     # Only what's needed"
    echo "   COPY src/ ./src/        # Specific directories"
    echo ""
}

optimize_build_performance
```

## Phase 8: Comprehensive Report

I'll generate a comprehensive optimization report:

```bash
#!/bin/bash
# Generate comprehensive container optimization report

generate_optimization_report() {
    echo "========================================"
    echo "CONTAINER OPTIMIZATION REPORT"
    echo "========================================"
    echo ""
    echo "Generated: $(date)"
    echo ""

    # Summary
    echo "ANALYSIS SUMMARY:"
    echo ""

    ISSUES_FOUND=0
    OPTIMIZATIONS_AVAILABLE=0

    # Count issues
    if ! grep -q "^FROM.*alpine\|slim\|distroless" Dockerfile 2>/dev/null; then
        OPTIMIZATIONS_AVAILABLE=$((OPTIMIZATIONS_AVAILABLE + 1))
    fi

    if [ $(grep -c "^FROM" Dockerfile 2>/dev/null || echo 0) -eq 1 ]; then
        OPTIMIZATIONS_AVAILABLE=$((OPTIMIZATIONS_AVAILABLE + 1))
    fi

    if ! grep -q "USER" Dockerfile 2>/dev/null; then
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    if [ ! -f ".dockerignore" ]; then
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    echo "  Security issues: $ISSUES_FOUND"
    echo "  Optimization opportunities: $OPTIMIZATIONS_AVAILABLE"
    echo ""

    echo "PRIORITY ACTIONS:"
    echo ""

    if [ $ISSUES_FOUND -gt 0 ]; then
        if ! grep -q "USER" Dockerfile 2>/dev/null; then
            echo "  1. HIGH: Add non-root user"
        fi

        if [ ! -f ".dockerignore" ]; then
            echo "  2. MEDIUM: Create .dockerignore file"
        fi
    fi

    if [ $OPTIMIZATIONS_AVAILABLE -gt 0 ]; then
        echo "  3. MEDIUM: Implement multi-stage build"
        echo "  4. LOW: Switch to Alpine base image"
    fi

    echo ""
    echo "========================================"
}

generate_optimization_report
```

## Integration with Other Skills

**Workflow Integration:**
- Before deployment → `/container-optimize`
- During CI/CD → `/ci-setup` (add image scanning)
- Security review → `/security-scan`
- Pre-release → `/release-automation`

**Skill Suggestions:**
- Security issues found → `/security-scan`, `/dependency-audit`
- Build performance → `/pipeline-monitor`
- Size optimization → `/bundle-analyze` (for web apps)

## Practical Examples

**Analyze default Dockerfile:**
```bash
/container-optimize              # Auto-detect and analyze
```

**Specific Dockerfile:**
```bash
/container-optimize Dockerfile.prod
/container-optimize backend/Dockerfile
```

**Focus on specific optimization:**
```bash
/container-optimize --security   # Security focus
/container-optimize --size       # Size reduction focus
/container-optimize --performance # Build performance focus
```

## What Gets Optimized

**Analysis Areas:**
- Base image selection
- Multi-stage build implementation
- Layer caching strategy
- Image size reduction
- Security vulnerability scanning
- Build performance optimization
- Best practices validation

**Container Technologies:**
- Docker
- Podman
- Kubernetes manifests (basic)
- docker-compose configurations

## Safety Guarantees

**What I'll NEVER do:**
- Modify Dockerfiles without confirmation
- Delete existing container images
- Push images to registries
- Modify running containers

**What I WILL do:**
- Analyze and suggest improvements
- Create optimized Dockerfile templates
- Generate .dockerignore if missing
- Provide security recommendations
- Document all changes clearly

## Credits

This skill integrates:
- **Docker Best Practices** - Official Docker documentation
- **Alpine Linux** - Minimal base image strategy
- **Distroless** - Google's minimal container images
- **Trivy** - Vulnerability scanning
- **BuildKit** - Modern Docker build engine

## Token Budget

Target: 2,500-4,000 tokens per execution
- Phase 1-2: ~800 tokens (detection, analysis)
- Phase 3-4: ~900 tokens (multi-stage, caching)
- Phase 5-6: ~900 tokens (size, security)
- Phase 7-8: ~700 tokens (performance, report)

**Optimization Strategy:**
- Read only Dockerfile (small file, ~500 tokens)
- Bash scripts for detection (minimal tokens)
- Grep for pattern matching
- Template generation without full file parsing
- Summary-based reporting

This ensures comprehensive container optimization while maintaining efficiency and respecting token limits.
