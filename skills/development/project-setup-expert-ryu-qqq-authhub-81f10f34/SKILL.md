---
name: project-setup-expert
version: 3.0.0
description: |
  Multi-module 구조 설계, Gradle 설정, Version Catalog, 의존성 관리.
  헥사고날 아키텍처 모듈 분리. Domain 외부 의존성 금지, 순환 의존성 금지.
  QA 도구 (Checkstyle, SpotBugs, PMD, JaCoCo) 설정.
author: claude-spring-standards
created: 2024-11-01
updated: 2025-12-05
tags: [project, setup, gradle, multi-module, version-catalog, hexagonal, qa]
---

# Project Setup Expert (프로젝트 설정 전문가)

## 목적 (Purpose)

**Multi-module 헥사고날 아키텍처** 프로젝트 구조를 설계하고,
**Version Catalog** 기반 의존성 관리와 **QA 도구** 설정을 담당합니다.

## 활성화 조건

- 프로젝트 초기 설정 시
- `/plan` 실행 후 모듈 구조 변경 필요 시
- gradle, multi-module, version catalog, 의존성, checkstyle, spotbugs 키워드 언급 시

## 산출물 (Output)

| 컴포넌트 | 파일명 패턴 | 위치 |
|----------|-------------|------|
| Version Catalog | `libs.versions.toml` | `gradle/` |
| 루트 Gradle | `build.gradle` | 프로젝트 루트 |
| 모듈 Gradle | `build.gradle` | 각 모듈 루트 |
| 설정 파일 | `settings.gradle` | 프로젝트 루트 |
| QA 설정 | `checkstyle.xml`, `pmd-ruleset.xml` | `config/` |

## 완료 기준 (Acceptance Criteria)

- [ ] 6개 프로덕션 모듈 구조 설정
- [ ] Version Catalog (`libs.versions.toml`) 설정
- [ ] 의존성 방향: domain ← application ← adapter (단방향)
- [ ] Domain 외부 의존성 없음 (Pure Java)
- [ ] testFixtures 소스셋 활성화
- [ ] QA 도구 설정 (Checkstyle, SpotBugs, PMD, JaCoCo)
- [ ] ArchUnit 모듈 의존성 검증 테스트
- [ ] `./gradlew clean build` 통과

---

## 모듈 구조 (6개 프로덕션 모듈)

```
project/
│
├── domain/                              ⭐ Domain Layer (Pure Java)
│   ├── src/main/java/
│   │   └── com/company/domain/
│   │       ├── common/                  # DomainEvent, DomainException
│   │       └── {boundedContext}/        # order, product, customer
│   │           ├── aggregate/           # Aggregate Root
│   │           ├── vo/                  # Value Object
│   │           ├── event/               # Domain Event
│   │           └── exception/           # Domain Exception
│   └── src/testFixtures/java/           # Test Fixtures
│
├── application/                         ⭐ Application Layer
│   ├── src/main/java/
│   │   └── com/company/application/
│   │       ├── common/                  # 공통 Port, Config
│   │       └── {boundedContext}/
│   │           ├── assembler/           # Domain ↔ Response
│   │           ├── dto/                 # Command, Query, Response, Bundle
│   │           ├── facade/              # 2+ Manager 조합
│   │           ├── factory/             # Command/Query Factory
│   │           ├── manager/             # Transaction/Read Manager
│   │           ├── port/                # Port-In, Port-Out
│   │           └── service/             # UseCase 구현
│   └── src/testFixtures/java/
│
├── adapter-in/                          ⭐ Inbound Adapters
│   └── rest-api/
│       ├── src/main/java/
│       │   └── com/company/adapter/in/rest/
│       │       ├── common/              # GlobalExceptionHandler
│       │       └── {boundedContext}/
│       │           ├── controller/      # REST Controller
│       │           ├── dto/             # Request/Response DTO
│       │           ├── mapper/          # API ↔ UseCase DTO
│       │           └── error/           # ErrorMapper
│       └── src/testFixtures/java/
│
├── adapter-out/                         ⭐ Outbound Adapters
│   ├── persistence-mysql/
│   │   ├── src/main/java/
│   │   │   └── com/company/adapter/out/persistence/
│   │   │       ├── config/              # JPA, Flyway Config
│   │   │       └── {boundedContext}/
│   │   │           ├── adapter/         # Command/Query Adapter
│   │   │           ├── entity/          # JPA Entity
│   │   │           ├── mapper/          # Entity ↔ Domain
│   │   │           └── repository/      # JPA/QueryDSL
│   │   └── src/testFixtures/java/
│   │
│   └── persistence-redis/
│       ├── src/main/java/
│       │   └── com/company/adapter/out/redis/
│       │       ├── config/              # Lettuce, Redisson
│       │       └── {boundedContext}/
│       │           └── adapter/         # Cache/Lock Adapter
│       └── src/testFixtures/java/
│
└── bootstrap/                           ⭐ Bootstrap Module
    └── bootstrap-web-api/
        └── src/main/java/
            └── com/company/
                └── BootstrapWebApiApplication.java
```

---

## 코드 템플릿

### 1. settings.gradle

```gradle
rootProject.name = 'spring-hexagonal-template'

// ========================================
// Core Modules (Hexagonal Architecture)
// ========================================
include 'domain'
include 'application'

// ========================================
// Adapter Modules (Ports & Adapters)
// ========================================
// Inbound Adapters (Driving)
include 'adapter-in:rest-api'

// Outbound Adapters (Driven)
include 'adapter-out:persistence-mysql'
include 'adapter-out:persistence-redis'

// ========================================
// Bootstrap Modules (Runnable Applications)
// ========================================
include 'bootstrap:bootstrap-web-api'

// ========================================
// Project Structure
// ========================================
project(':domain').projectDir = file('domain')
project(':application').projectDir = file('application')

project(':adapter-in:rest-api').projectDir = file('adapter-in/rest-api')
project(':adapter-out:persistence-mysql').projectDir = file('adapter-out/persistence-mysql')
project(':adapter-out:persistence-redis').projectDir = file('adapter-out/persistence-redis')

project(':bootstrap:bootstrap-web-api').projectDir = file('bootstrap/bootstrap-web-api')
```

### 2. libs.versions.toml (Version Catalog)

```toml
# gradle/libs.versions.toml

[versions]
# ========================================
# Spring & Framework
# ========================================
springBoot = "3.5.6"
springDependencyManagement = "1.1.5"

# ========================================
# Database & Persistence
# ========================================
querydsl = "5.1.0"
flyway = "10.10.0"
mysql = "42.7.3"
mysql = "8.3.0"

# ========================================
# Redis
# ========================================
redisson = "3.27.0"

# ========================================
# UUID
# ========================================
uuidCreator = "6.0.0"

# ========================================
# Testing
# ========================================
archunit = "1.2.1"
testcontainers = "1.19.7"

# ========================================
# QA Tools
# ========================================
checkstyle = "10.14.0"
spotbugs = "4.8.3"
spotbugsPlugin = "6.0.9"
pmd = "7.0.0"
jacoco = "0.8.11"
spotless = "7.0.0.BETA4"

[libraries]
# ========================================
# Spring Boot Starters (BOM 관리 - 버전 생략)
# ========================================
spring-boot-starter = { module = "org.springframework.boot:spring-boot-starter" }
spring-boot-starter-web = { module = "org.springframework.boot:spring-boot-starter-web" }
spring-boot-starter-data-jpa = { module = "org.springframework.boot:spring-boot-starter-data-jpa" }
spring-boot-starter-data-redis = { module = "org.springframework.boot:spring-boot-starter-data-redis" }
spring-boot-starter-validation = { module = "org.springframework.boot:spring-boot-starter-validation" }
spring-boot-starter-test = { module = "org.springframework.boot:spring-boot-starter-test" }

# ========================================
# Spring (Non-Starter)
# ========================================
spring-context = { module = "org.springframework:spring-context" }
spring-tx = { module = "org.springframework:spring-tx" }

# ========================================
# Database
# ========================================
querydsl-jpa-jakarta = { module = "com.querydsl:querydsl-jpa", version.ref = "querydsl" }
querydsl-apt-jakarta = { module = "com.querydsl:querydsl-apt", version.ref = "querydsl" }
flyway-core = { module = "org.flywaydb:flyway-core", version.ref = "flyway" }
flyway-mysql = { module = "org.flywaydb:flyway-mysql", version.ref = "flyway" }
mysql-connector = { module = "com.mysql:mysql-connector-j", version.ref = "mysql" }
mysql = { module = "org.mysql:mysql", version.ref = "mysql" }

# ========================================
# Redis
# ========================================
redisson-spring-boot-starter = { module = "org.redisson:redisson-spring-boot-starter", version.ref = "redisson" }

# ========================================
# UUID
# ========================================
uuid-creator = { module = "com.github.f4b6a3:uuid-creator", version.ref = "uuidCreator" }

# ========================================
# Testing
# ========================================
junit-jupiter = { module = "org.junit.jupiter:junit-jupiter" }
assertj-core = { module = "org.assertj:assertj-core" }
mockito-core = { module = "org.mockito:mockito-core" }
archunit-junit5 = { module = "com.tngtech.archunit:archunit-junit5", version.ref = "archunit" }
testcontainers-junit = { module = "org.testcontainers:junit-jupiter", version.ref = "testcontainers" }
testcontainers-mysql = { module = "org.testcontainers:mysql", version.ref = "testcontainers" }
testcontainers-mysql = { module = "org.testcontainers:mysql", version.ref = "testcontainers" }

# ========================================
# Jakarta
# ========================================
jakarta-annotation-api = { module = "jakarta.annotation:jakarta.annotation-api" }
jakarta-persistence-api = { module = "jakarta.persistence:jakarta.persistence-api" }

[bundles]
# ========================================
# Dependency Bundles
# ========================================
testing-basic = ["junit-jupiter", "assertj-core", "mockito-core"]
testcontainers = ["testcontainers-junit", "testcontainers-mysql"]
querydsl = ["querydsl-jpa-jakarta"]

[plugins]
# ========================================
# Gradle Plugins
# ========================================
spring-boot = { id = "org.springframework.boot", version.ref = "springBoot" }
spring-dependency-management = { id = "io.spring.dependency-management", version.ref = "springDependencyManagement" }
spotbugs = { id = "com.github.spotbugs", version.ref = "spotbugsPlugin" }
spotless = { id = "com.diffplug.spotless", version.ref = "spotless" }
```

**핵심 규칙**:
- [versions]에 버전 정의
- [libraries]에서 `version.ref` 참조
- Spring Boot BOM 관리 의존성은 버전 생략 가능
- 하드코딩 버전 금지

### 3. 루트 build.gradle

```gradle
import org.springframework.boot.gradle.plugin.SpringBootPlugin

plugins {
    id 'java'
    alias(libs.plugins.spring.boot) apply false
    alias(libs.plugins.spring.dependency.management) apply false
    id 'checkstyle'
    alias(libs.plugins.spotbugs) apply false
    id 'pmd'
    alias(libs.plugins.spotless) apply false
}

allprojects {
    group = 'com.company.template'
    version = '1.0.0-SNAPSHOT'

    repositories {
        mavenCentral()
    }
}

subprojects {
    apply plugin: 'java'
    apply plugin: 'io.spring.dependency-management'
    apply plugin: 'checkstyle'
    apply plugin: 'com.github.spotbugs'
    apply plugin: 'pmd'
    apply plugin: 'com.diffplug.spotless'
    apply plugin: 'jacoco'

    java {
        sourceCompatibility = JavaVersion.VERSION_21
        targetCompatibility = JavaVersion.VERSION_21
    }

    dependencyManagement {
        imports {
            mavenBom SpringBootPlugin.BOM_COORDINATES
        }
    }

    // ========================================
    // Checkstyle
    // ========================================
    checkstyle {
        toolVersion = rootProject.libs.versions.checkstyle.get()
        configFile = rootProject.file('config/checkstyle/checkstyle.xml')
        ignoreFailures = false
        maxWarnings = 0
    }

    // ========================================
    // SpotBugs
    // ========================================
    spotbugs {
        toolVersion = rootProject.libs.versions.spotbugs.get()
        effort = 'max'
        reportLevel = 'low'
        excludeFilter = rootProject.file('config/spotbugs/spotbugs-exclude.xml')
    }

    // ========================================
    // PMD (Law of Demeter)
    // ========================================
    pmd {
        toolVersion = rootProject.libs.versions.pmd.get()
        consoleOutput = true
        ruleSetFiles = files(rootProject.file('config/pmd/pmd-ruleset.xml'))
        ruleSets = []
        ignoreFailures = false
    }

    // ========================================
    // Spotless (Code Formatting)
    // ========================================
    spotless {
        java {
            googleJavaFormat('1.22.0').aosp().reflowLongStrings()
            target 'src/*/java/**/*.java'
            targetExclude '**/generated/**', '**/Q*.java'
        }
    }

    // ========================================
    // JaCoCo (Coverage)
    // ========================================
    jacoco {
        toolVersion = rootProject.libs.versions.jacoco.get()
    }

    tasks.named('jacocoTestReport') {
        dependsOn 'test'
        reports {
            xml.required = true
            html.required = true
        }
    }

    // ========================================
    // Common Dependencies
    // ========================================
    dependencies {
        testImplementation rootProject.libs.junit.jupiter
        testImplementation rootProject.libs.assertj.core
        testImplementation rootProject.libs.archunit.junit5
    }

    // ========================================
    // JavaCompile Options
    // ========================================
    tasks.withType(JavaCompile) {
        options.encoding = 'UTF-8'
        options.compilerArgs.addAll([
            '-Xlint:unchecked',
            '-Xlint:deprecation',
            '-parameters'
        ])
    }

    // ========================================
    // Build Task Dependencies
    // ========================================
    tasks.named('build') {
        dependsOn 'spotlessCheck'
        dependsOn 'jacocoTestReport'
    }
}

// ========================================
// Custom Tasks
// ========================================
tasks.register('checkNoLombok') {
    group = 'verification'
    description = 'Verify Lombok is not used in any module'

    doLast {
        subprojects.each { project ->
            project.configurations.each { config ->
                config.dependencies.each { dep ->
                    if (dep.group == 'org.projectlombok' && dep.name == 'lombok') {
                        throw new GradleException("""
❌ LOMBOK DETECTED in ${project.name}
Lombok is strictly prohibited in this project.
""")
                    }
                }
            }
        }
    }
}

tasks.register('verifyVersionCatalog') {
    group = 'verification'
    description = 'Verify all versions use version.ref in libs.versions.toml'

    doLast {
        def catalogFile = rootProject.file('gradle/libs.versions.toml')
        if (!catalogFile.exists()) {
            throw new GradleException('libs.versions.toml not found')
        }

        def content = catalogFile.text
        def librariesSection = false
        def violations = []

        content.eachLine { line, lineNum ->
            if (line.trim() == '[libraries]') {
                librariesSection = true
            } else if (line.trim().startsWith('[') && line.trim() != '[libraries]') {
                librariesSection = false
            }

            if (librariesSection && line.contains('version = "')) {
                violations << "Line ${lineNum + 1}: ${line.trim()}"
            }
        }

        if (!violations.isEmpty()) {
            throw new GradleException("""
❌ VERSION CATALOG CONSISTENCY VIOLATION

Hardcoded versions found in [libraries] section.
Use 'version.ref' referencing [versions] section.

Violations:
${violations.join('\n')}
""")
        }
    }
}
```

### 4. domain/build.gradle

```gradle
plugins {
    id 'java-library'
    id 'java-test-fixtures'
}

dependencies {
    // ========================================
    // Domain은 외부 의존성 없음 (Pure Java)
    // ========================================
    // ❌ Lombok 금지
    // ❌ Spring 의존성 금지
    // ❌ JPA 의존성 금지

    // ✅ 허용: UUID 생성 유틸리티
    implementation rootProject.libs.uuid.creator

    // ========================================
    // Test Dependencies
    // ========================================
    testImplementation rootProject.libs.junit.jupiter
    testImplementation rootProject.libs.assertj.core
    testImplementation rootProject.libs.archunit.junit5
}
```

### 5. application/build.gradle

```gradle
plugins {
    id 'java-library'
    id 'java-test-fixtures'
}

dependencies {
    // ========================================
    // Core Dependencies
    // ========================================
    api project(':domain')

    // Spring (Context, TX only)
    implementation rootProject.libs.spring.context
    implementation rootProject.libs.spring.tx

    // ========================================
    // Test Dependencies
    // ========================================
    testImplementation rootProject.libs.spring.boot.starter.test
    testImplementation testFixtures(project(':domain'))

    // ========================================
    // Test Fixtures Dependencies
    // ========================================
    testFixturesApi project(':domain')
    testFixturesApi testFixtures(project(':domain'))
}
```

### 6. adapter-out/persistence-mysql/build.gradle

```gradle
plugins {
    id 'java-library'
    id 'java-test-fixtures'
}

dependencies {
    // ========================================
    // Core Dependencies
    // ========================================
    api project(':application')
    api project(':domain')

    // Spring Boot Data JPA
    implementation rootProject.libs.spring.boot.starter.data.jpa

    // QueryDSL
    implementation rootProject.libs.querydsl.jpa.jakarta
    annotationProcessor rootProject.libs.querydsl.apt.jakarta
    annotationProcessor rootProject.libs.jakarta.annotation.api
    annotationProcessor rootProject.libs.jakarta.persistence.api

    // Flyway
    implementation rootProject.libs.flyway.core
    implementation rootProject.libs.flyway.mysql

    // Database Drivers
    runtimeOnly rootProject.libs.mysql.connector

    // ========================================
    // Test Dependencies
    // ========================================
    testImplementation rootProject.libs.spring.boot.starter.test
    testImplementation rootProject.libs.testcontainers.mysql
    testImplementation rootProject.libs.testcontainers.junit
    testImplementation testFixtures(project(':domain'))

    // ========================================
    // Test Fixtures Dependencies
    // ========================================
    testFixturesApi project(':domain')
    testFixturesApi testFixtures(project(':domain'))
}
```

### 7. bootstrap/bootstrap-web-api/build.gradle

```gradle
plugins {
    id 'java'
    alias(libs.plugins.spring.boot)
    alias(libs.plugins.spring.dependency.management)
}

dependencies {
    // ========================================
    // All Modules
    // ========================================
    implementation project(':domain')
    implementation project(':application')
    implementation project(':adapter-in:rest-api')
    implementation project(':adapter-out:persistence-mysql')
    implementation project(':adapter-out:persistence-redis')

    // Spring Boot
    implementation rootProject.libs.spring.boot.starter

    // ========================================
    // Test Dependencies
    // ========================================
    testImplementation rootProject.libs.spring.boot.starter.test
    testImplementation testFixtures(project(':domain'))
    testImplementation testFixtures(project(':application'))
}

bootJar {
    enabled = true
}

jar {
    enabled = false
}
```

---

## 의존성 흐름

### 의존성 규칙 매트릭스

| From ↓ / To → | domain | application | rest-api | persistence | bootstrap |
|---------------|--------|-------------|----------|-------------|-----------|
| **domain** | - | ❌ | ❌ | ❌ | ❌ |
| **application** | ✅ | - | ❌ | ❌ | ❌ |
| **rest-api** | ✅ | ✅ | - | ❌ | ❌ |
| **persistence** | ✅ | ✅ | ❌ | - | ❌ |
| **bootstrap** | ✅ | ✅ | ✅ | ✅ | - |

**핵심 규칙**:
- domain: 외부 의존성 없음 (Pure Java)
- application: domain만 의존
- adapter: application + domain만 의존
- adapter-in ↔ adapter-out: 상호 의존 금지

### 의존성 다이어그램

```
                    ┌─────────────────────────┐
                    │    bootstrap-web-api    │
                    │    (Spring Boot App)    │
                    └───────────┬─────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────────┐
│   rest-api    │    │  persistence  │    │  persistence      │
│ (adapter-in)  │    │    (mysql)    │    │    (redis)        │
└───────┬───────┘    └───────┬───────┘    └─────────┬─────────┘
        │                    │                      │
        └────────────────────┼──────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   application   │
                    │   (UseCase)     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     domain      │
                    │  (Pure Java)    │
                    └─────────────────┘
```

---

## Zero-Tolerance 규칙

### ✅ MANDATORY (필수)

| 규칙 | 설명 |
|------|------|
| Version Catalog | `libs.versions.toml` 중앙 관리 |
| `version.ref` 사용 | 버전 하드코딩 금지 |
| 단방향 의존성 | domain ← application ← adapter |
| Domain Pure Java | 외부 의존성 금지 (Spring, JPA, Lombok) |
| testFixtures | `java-test-fixtures` 플러그인 |
| ArchUnit 검증 | 모듈 의존성 자동 검증 |
| JaCoCo 커버리지 | 모듈별 최소 커버리지 |

### ❌ PROHIBITED (금지)

| 항목 | 이유 |
|------|------|
| Lombok | Plain Java 원칙, `checkNoLombok` 검증 |
| 버전 하드코딩 | `verifyVersionCatalog` 검증 |
| 순환 의존성 | 단방향 의존성 원칙 |
| Domain Spring 의존성 | Pure Java 원칙 |
| adapter-in ↔ adapter-out | 독립성 원칙 |

---

## QA 도구 설정

### 도구별 역할

| 도구 | 역할 | 설정 파일 |
|------|------|----------|
| Checkstyle | 코드 스타일 (Lombok 금지 포함) | `config/checkstyle/checkstyle.xml` |
| SpotBugs | 버그 패턴 탐지 | `config/spotbugs/spotbugs-exclude.xml` |
| PMD | Law of Demeter 강제 | `config/pmd/pmd-ruleset.xml` |
| JaCoCo | 테스트 커버리지 | build.gradle 내 설정 |
| Spotless | 코드 포맷팅 | build.gradle 내 설정 |

### 모듈별 커버리지 기준

| 모듈 | 최소 커버리지 | 근거 |
|------|-------------|------|
| domain | 90% | 핵심 비즈니스 로직 |
| application | 80% | UseCase 로직 |
| adapter-* | 70% | 인프라 통합 코드 |
| bootstrap | 70% | 설정 및 진입점 |

---

## 체크리스트 (Output Checklist)

### 프로젝트 초기화
- [ ] `settings.gradle` 6개 모듈 등록
- [ ] `gradle/libs.versions.toml` 생성
- [ ] 루트 `build.gradle` 작성
- [ ] 모듈별 `build.gradle` 작성

### Version Catalog
- [ ] [versions] 섹션 정의
- [ ] [libraries] `version.ref` 참조
- [ ] [plugins] 정의
- [ ] `./gradlew verifyVersionCatalog` 통과

### 의존성 규칙
- [ ] domain: 외부 의존성 없음
- [ ] application: domain만 의존
- [ ] adapter: application + domain만 의존
- [ ] adapter-in ↔ adapter-out 독립

### testFixtures
- [ ] `java-test-fixtures` 플러그인 적용
- [ ] `src/testFixtures/java/` 디렉토리 생성
- [ ] `testFixtures(project(':...'))` 의존성

### QA 도구
- [ ] `config/checkstyle/checkstyle.xml` 설정
- [ ] `config/spotbugs/spotbugs-exclude.xml` 설정
- [ ] `config/pmd/pmd-ruleset.xml` 설정
- [ ] JaCoCo 커버리지 기준 설정

### 검증
- [ ] `./gradlew clean build` 통과
- [ ] `./gradlew checkNoLombok` 통과
- [ ] `./gradlew verifyVersionCatalog` 통과
- [ ] ArchUnit 테스트 통과

---

## ArchUnit 모듈 의존성 테스트

```java
package com.company.template.architecture;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

@DisplayName("Multi-Module Dependency ArchUnit Tests")
class ModuleDependencyArchTest {

    private static JavaClasses classes;

    @BeforeAll
    static void setUp() {
        classes = new ClassFileImporter()
            .importPackages("com.company.template");
    }

    @Test
    @DisplayName("domain은 application, adapter를 의존할 수 없다")
    void domain_MustNotDependOnOtherModules() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAnyPackage(
                "..application..",
                "..adapter.."
            );

        rule.check(classes);
    }

    @Test
    @DisplayName("application은 adapter를 의존할 수 없다")
    void application_MustNotDependOnAdapter() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..application..")
            .should().dependOnClassesThat().resideInAPackage("..adapter..");

        rule.check(classes);
    }

    @Test
    @DisplayName("adapter-in은 adapter-out을 의존할 수 없다")
    void adapterIn_MustNotDependOnAdapterOut() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..adapter.in..")
            .should().dependOnClassesThat().resideInAPackage("..adapter.out..");

        rule.check(classes);
    }

    @Test
    @DisplayName("adapter-out은 adapter-in을 의존할 수 없다")
    void adapterOut_MustNotDependOnAdapterIn() {
        ArchRule rule = noClasses()
            .that().resideInAPackage("..adapter.out..")
            .should().dependOnClassesThat().resideInAPackage("..adapter.in..");

        rule.check(classes);
    }
}
```

---

## 빌드 명령어

```bash
# 전체 빌드
./gradlew clean build

# Version Catalog 검증
./gradlew verifyVersionCatalog

# Lombok 금지 검증
./gradlew checkNoLombok

# 코드 스타일 검사
./gradlew checkstyleMain checkstyleTest

# 버그 패턴 검사
./gradlew spotbugsMain

# Law of Demeter 검사
./gradlew pmdMain

# 포맷팅 검사/적용
./gradlew spotlessCheck
./gradlew spotlessApply

# 커버리지 리포트
./gradlew jacocoTestReport

# ArchUnit 테스트만
./gradlew test --tests "*ArchTest"

# 모듈별 빌드
./gradlew :domain:build
./gradlew :application:build
```

---

## 참조 문서

- **Multi-Module Structure**: `docs/coding_convention/00-project-setup/multi-module-structure.md`
- **Gradle Configuration**: `docs/coding_convention/00-project-setup/gradle-configuration.md`
- **Version Management**: `docs/coding_convention/00-project-setup/version-management.md`
- **Test Fixtures Guide**: `docs/coding_convention/05-testing/test-fixtures/01_test-fixtures-guide.md`
