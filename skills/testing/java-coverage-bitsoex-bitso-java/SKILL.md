---
name: java-coverage
description: >
  JaCoCo code coverage configuration for Java/Gradle projects. Covers report
  generation, coverage thresholds, multi-module aggregation, and SonarQube
  integration. Use when setting up or troubleshooting code coverage.
compatibility: Java projects using Gradle with JaCoCo plugin
metadata:
  version: "2.0.0"
  technology: java
  category: quality
  tags:
    - java
    - jacoco
    - coverage
    - testing
---

# Java Coverage

JaCoCo code coverage configuration for Java/Gradle projects.

## When to use this skill

- Setting up code coverage reporting
- Configuring coverage thresholds
- Aggregating coverage across modules
- Integrating with SonarQube
- Troubleshooting coverage reports
- When asked to "improve test coverage"

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L23-L31)
- [Quick Start](#quick-start) (L57-L94)
- [Coverage Thresholds](#coverage-thresholds) (L95-L119)
- [Exclusions](#exclusions) (L120-L139)
- [Multi-Module Aggregation](#multi-module-aggregation) (L140-L190)
- [SonarQube Integration](#sonarqube-integration) (L191-L201)
- [References](#references) (L202-L208)
- [Related Rules](#related-rules) (L209-L212)
- [Related Skills](#related-skills) (L213-L219)

### Available Resources

**📚 references/** - Detailed documentation
- [coverage targets](references/coverage-targets.md)
- [exclusion patterns](references/exclusion-patterns.md)
- [improvement workflow](references/improvement-workflow.md)
- [multi module](references/multi-module.md)
- [prioritization](references/prioritization.md)

---

## Quick Start

### 1. Apply JaCoCo Plugin

```groovy
plugins {
    id 'jacoco'
}

jacoco {
    toolVersion = "0.8.14"
}
```

### 2. Configure Report Task

```groovy
jacocoTestReport {
    dependsOn test

    reports {
        xml.required = true  // For SonarQube
        html.required = true // For local viewing
    }
}

test {
    finalizedBy jacocoTestReport
}
```

### 3. Run Coverage

```bash
./gradlew test jacocoTestReport
# Report at: build/reports/jacoco/test/html/index.html
```

## Coverage Thresholds

```groovy
jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                minimum = 0.80  // 80% minimum coverage
            }
        }

        rule {
            element = 'CLASS'
            excludes = ['*.generated.*', '*.config.*']
            limit {
                counter = 'LINE'
                minimum = 0.70
            }
        }
    }
}

check.dependsOn jacocoTestCoverageVerification
```

## Exclusions

Common patterns to exclude from coverage:

```groovy
jacocoTestReport {
    afterEvaluate {
        classDirectories.setFrom(files(classDirectories.files.collect {
            fileTree(dir: it, exclude: [
                '**/generated/**',
                '**/config/**',
                '**/*Config.class',
                '**/*Properties.class',
                '**/Application.class'
            ])
        }))
    }
}
```

## Multi-Module Aggregation

For aggregated reports across modules, use the modern `jacoco-report-aggregation` plugin (Gradle 7.4+):

```groovy
// In root build.gradle
plugins {
    id 'base'
    id 'jacoco-report-aggregation'
}

// Ensure subprojects are evaluated first
subprojects.each { evaluationDependsOn(it.path) }

dependencies {
    subprojects.each { jacocoAggregation it }
}

reporting {
    reports {
        testCodeCoverageReport(JacocoCoverageReport) {
            testType = TestSuiteType.UNIT_TEST
        }
    }
}
```

For older Gradle versions, use a manual task with defensive filtering:

```groovy
// In root build.gradle (Gradle < 7.4)
task jacocoRootReport(type: JacocoReport) {
    dependsOn subprojects*.test

    // Use defensive filtering to avoid missing-directory errors
    def srcDirs = files(subprojects*.sourceSets*.main*.allSource*.srcDirs).filter { it.exists() }
    def classDirs = files(subprojects*.sourceSets*.main*.output).filter { it.exists() }
    def execData = files(subprojects*.jacocoTestReport*.executionData).filter { it.exists() }

    additionalSourceDirs.from(srcDirs)
    sourceDirectories.from(srcDirs)
    classDirectories.from(classDirs)
    executionData.from(execData)

    reports {
        xml.required = true
        html.required = true
    }
}
```

## SonarQube Integration

```groovy
sonar {
    properties {
        property 'sonar.coverage.jacoco.xmlReportPaths',
            "${projectDir}/build/reports/jacoco/test/jacocoTestReport.xml"
    }
}
```

## References

| Reference | Description |
|-----------|-------------|
| [references/exclusion-patterns.md](references/exclusion-patterns.md) | Common exclusion patterns |
| [references/multi-module.md](references/multi-module.md) | Multi-module aggregation |

## Related Rules

- [java-jacoco-coverage](.cursor/rules/java-jacoco-coverage/java-jacoco-coverage.mdc) - Full JaCoCo reference

## Related Skills

| Skill | Purpose |
|-------|---------|
| [java-testing](.claude/skills/java-testing/SKILL.md) | Test configuration |
| [fix-sonarqube](.claude/skills/fix-sonarqube/SKILL.md) | SonarQube setup |
| [gradle-standards](.claude/skills/gradle-standards/SKILL.md) | Gradle configuration |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/java-coverage/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

