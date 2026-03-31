---
name: jspecify-skill
description: >
  Use this skill when asked to perform any of the following actions in a Java project:
    - To add jspecify support
    - To prevent NullPointerExceptions
    - To better handle Nullability

  This skill will add jspecify dependency, configure Maven or Gradle build to automatically use jspecify for checking Nullability issues.
---

Jspecify provides a set of annotations to explicitly declare the nullness expectations of the Java code.

## Add jSpecify support in Maven projects
If you are using Maven, then add the jspecify dependency in `pom.xml`.
In `pom.xml`, update or add the `maven-compiler-plugin`, to include the following configuration.

```xml
<dependencies>
    <dependency>
        <groupId>org.jspecify</groupId>
        <artifactId>jspecify</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.14.1</version>
            <configuration>
                <release>25</release>
                <encoding>UTF-8</encoding>
                <fork>true</fork>
                <compilerArgs>
                    <arg>-XDcompilePolicy=simple</arg>
                    <arg>--should-stop=ifError=FLOW</arg>
                    <arg>-Xplugin:ErrorProne -XepDisableAllChecks -Xep:NullAway:ERROR -XepOpt:NullAway:OnlyNullMarked -XepOpt:NullAway:JSpecifyMode=true</arg>
                    <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED</arg>
                    <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED</arg>
                    <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED</arg>
                    <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED</arg>
                    <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED</arg>
                    <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED</arg>
                    <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED</arg>
                    <arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED</arg>
                    <arg>-J--add-opens=jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED</arg>
                    <arg>-J--add-opens=jdk.compiler/com.sun.tools.javac.comp=ALL-UNNAMED</arg>
                </compilerArgs>
                <annotationProcessorPaths>
                    <path>
                        <groupId>com.google.errorprone</groupId>
                        <artifactId>error_prone_core</artifactId>
                        <version>2.42.0</version>
                    </path>
                    <path>
                        <groupId>com.uber.nullaway</groupId>
                        <artifactId>nullaway</artifactId>
                        <version>0.12.12</version>
                    </path>
                </annotationProcessorPaths>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## Add jSpecify support in Gradle projects
If you are using Gradle, then add the jspecify dependency.
In `build.gradle` or `build.gradle.kts`, update or add the following jspecify configuration.

```groovy
plugins {
    id("net.ltgt.errorprone") version "4.3.0"
}

tasks.withType(JavaCompile).configureEach {
    options.errorprone {
        disableAllChecks = true // Other error prone checks are disabled
        option("NullAway:OnlyNullMarked", "true") // Enable nullness checks only in null-marked code
        error("NullAway") // bump checks from warnings (default) to errors
        option("NullAway:JSpecifyMode", "true") // https://github.com/uber/NullAway/wiki/JSpecify-Support
    }
    // Keep a JDK 25 baseline
    options.release = 25
}

dependencies {
    implementation("org.jspecify:jspecify:1.0.0")
    errorprone("com.google.errorprone:error_prone_core:2.42.0")
    errorprone("com.uber.nullaway:nullaway:0.12.12")
}
```

## Add @NullMarked to package-info.java files
In every java package under the application main source code (`src/main/java`), 
create `package-info.java` if not exists already, and add the `@NullMarked` annotation as follows:

```java
@org.jspecify.annotations.NullMarked
package com.mycompnay.myproject;
```

If `package-info.java` file already exists, update the file to add `@org.jspecify.annotations.NullMarked` annotation.
DO NOT REMOVE ANY OTHER EXISTING CODE IN `package-info.java` FILE.

## Verify jSpecify support
If python is installed, after adding the jSpecify support, run `scripts/verify_nullmarked.py` 
to check if all non-empty packages has `package-info.java` file or not.
