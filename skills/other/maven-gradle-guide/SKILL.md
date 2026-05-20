---
name: maven-gradle-guide
description: >
  Maven and Gradle build tool patterns including pom.xml structure, build.gradle.kts configuration,
  multi-module projects, dependency management, plugins, and BOMs. Use when the user is setting up
  Java/Kotlin build configurations, managing dependencies, creating multi-module projects, or
  troubleshooting build issues. Trigger on any mention of Maven, Gradle, pom.xml, build.gradle,
  dependency management, or Java build tools.
---

# Maven and Gradle Guide

Build tool configuration patterns for Java and Kotlin projects.

## When to Use
- User is setting up a new Maven or Gradle project
- User needs to manage dependencies or resolve conflicts
- User is creating a multi-module project
- User asks about BOMs, plugins, or build lifecycle
- User is migrating between Maven and Gradle

## Core Patterns

### Maven pom.xml Structure

A well-organized POM with property management, dependency management, and plugin configuration.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>my-service</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <properties>
        <java.version>21</java.version>
        <testcontainers.version>1.19.3</testcontainers.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

### Gradle Kotlin DSL (build.gradle.kts)

The equivalent Gradle configuration using the Kotlin DSL for type-safe build scripts.

```kotlin
plugins {
    java
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "com.example"
version = "1.0.0-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")

    runtimeOnly("org.postgresql:postgresql")

    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.testcontainers:postgresql:1.19.3")
}

tasks.test {
    useJUnitPlatform()
}
```

### Multi-Module Project (Maven)

Parent POM manages shared configuration; child modules inherit.

```xml
<!-- parent pom.xml -->
<project>
    <groupId>com.example</groupId>
    <artifactId>my-platform</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>
    <modules>
        <module>common</module>
        <module>api</module>
        <module>service</module>
    </modules>
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>com.example</groupId>
                <artifactId>common</artifactId>
                <version>${project.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>

<!-- service/pom.xml -- inherits parent, version from dependencyManagement -->
<project>
    <parent>
        <groupId>com.example</groupId>
        <artifactId>my-platform</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>
    <artifactId>service</artifactId>
    <dependencies>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>common</artifactId>
        </dependency>
    </dependencies>
</project>
```

### Multi-Module Project (Gradle)

```kotlin
// settings.gradle.kts
rootProject.name = "my-platform"
include("common", "api", "service")

// build.gradle.kts (root)
subprojects {
    apply(plugin = "java")
    group = "com.example"
    version = "1.0.0-SNAPSHOT"
    repositories { mavenCentral() }
    java { sourceCompatibility = JavaVersion.VERSION_21 }
    tasks.test { useJUnitPlatform() }
}

// service/build.gradle.kts
dependencies {
    implementation(project(":common"))
    implementation("org.springframework.boot:spring-boot-starter-web")
}
```

### BOM (Bill of Materials)

Use BOMs to align versions across a family of libraries. Prevents version conflicts.

```xml
<!-- Maven: import BOM in dependencyManagement -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>testcontainers-bom</artifactId>
            <version>1.19.3</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<!-- Now use without version -->
<dependencies>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>postgresql</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

```kotlin
// Gradle: import BOM via platform()
dependencies {
    implementation(platform("org.testcontainers:testcontainers-bom:1.19.3"))
    testImplementation("org.testcontainers:postgresql") // no version needed
}
```

## Anti-Patterns

- **Specifying versions in child modules** -- Manage all versions in the parent POM's `<dependencyManagement>` or via BOMs. Child modules should omit version tags.
- **Using the Groovy DSL for new Gradle projects** -- The Kotlin DSL (`build.gradle.kts`) provides type safety, auto-completion, and compile-time checks. Prefer it for new projects.
- **Fat JARs without Spring Boot plugin** -- Using the `maven-shade-plugin` when Spring Boot's plugin handles fat JAR packaging correctly. Use the right tool.
- **Dependency version conflicts** -- Not using BOMs and having transitive dependency conflicts. Run `mvn dependency:tree` or `gradle dependencies` to diagnose.
- **Putting test dependencies in compile scope** -- Always use `<scope>test</scope>` in Maven or `testImplementation` in Gradle for test-only libraries.

## Quick Reference

```
Maven lifecycle:
  mvn clean compile       -- Compile sources
  mvn test                -- Run tests
  mvn package             -- Build JAR/WAR
  mvn install             -- Install to local repo
  mvn dependency:tree     -- Show dependency tree

Gradle tasks:
  gradle build            -- Compile + test + package
  gradle test             -- Run tests
  gradle dependencies     -- Show dependency tree
  gradle bootRun          -- Run Spring Boot app

Dependency scopes:
  Maven           Gradle
  compile     ->  implementation
  provided    ->  compileOnly
  runtime     ->  runtimeOnly
  test        ->  testImplementation
```
