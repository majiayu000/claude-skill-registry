---
name: jackson
description: Use when working with Jackson JSON serialization - migrating from Jackson 2.x to 3.x, configuring JsonMapper, handling date/time types, or troubleshooting serialization issues.
---

# Jackson 3 Skill

Guidance for working with Jackson 3.x JSON serialization in the lib-electronic-components library.

## Overview

This project uses **Jackson 3.0.3** for JSON serialization. Jackson 3 is a major version upgrade with significant API changes from Jackson 2.x.

## Quick Reference

### Import Changes

```java
// Jackson 2.x
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

// Jackson 3.x
import tools.jackson.databind.json.JsonMapper;
import tools.jackson.databind.SerializationFeature;
// No JavaTimeModule needed - built-in
```

### Creating a Mapper

```java
// Simple mapper
JsonMapper mapper = JsonMapper.builder().build();

// With configuration
JsonMapper mapper = JsonMapper.builder()
    .enable(SerializationFeature.INDENT_OUTPUT)
    .build();
```

### Serialization

```java
JsonMapper mapper = JsonMapper.builder().build();

// To JSON string
String json = mapper.writeValueAsString(object);

// Pretty print
String prettyJson = mapper.writerWithDefaultPrettyPrinter()
    .writeValueAsString(object);
```

### Deserialization

```java
JsonMapper mapper = JsonMapper.builder().build();

// From JSON string
MyClass obj = mapper.readValue(json, MyClass.class);

// From file
MyClass obj = mapper.readValue(new File("data.json"), MyClass.class);
```

## Maven Dependencies

```xml
<properties>
    <jackson.version>3.0.3</jackson.version>
</properties>

<dependencies>
    <!-- Jackson 3.x core -->
    <dependency>
        <groupId>tools.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>${jackson.version}</version>
    </dependency>

    <!-- Annotations stay on 2.x -->
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-annotations</artifactId>
        <version>2.20</version>
    </dependency>

    <!-- XML format (optional) -->
    <dependency>
        <groupId>tools.jackson.dataformat</groupId>
        <artifactId>jackson-dataformat-xml</artifactId>
        <version>${jackson.version}</version>
    </dependency>
</dependencies>
```

## Module System (JPMS)

```java
module my.module {
    // Jackson 3.x modules
    requires transitive tools.jackson.core;
    requires transitive tools.jackson.databind;

    // Annotations still use 2.x module name
    requires transitive com.fasterxml.jackson.annotation;

    // Open packages for Jackson reflection
    opens my.package.model to tools.jackson.databind;
}
```

## Annotations

Annotations **stay on Jackson 2.x** (`com.fasterxml.jackson.annotation`):

```java
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.annotation.JsonSubTypes;

public class MyClass {
    @JsonProperty("custom_name")
    private String name;

    @JsonIgnore
    private String internal;

    @JsonCreator
    public MyClass(@JsonProperty("name") String name) {
        this.name = name;
    }
}
```

## Date/Time Handling

Jackson 3.x has **built-in** support for Java 8 date/time types:

```java
// No module registration needed!
JsonMapper mapper = JsonMapper.builder().build();

public class Event {
    private LocalDate date;           // "2024-03-15"
    private LocalDateTime timestamp;  // "2024-03-15T10:30:00"
    private Instant instant;          // "2024-03-15T10:30:00Z"
    private Duration duration;        // "PT1H30M"
}
```

## Common Configuration

```java
JsonMapper mapper = JsonMapper.builder()
    // Pretty print output
    .enable(SerializationFeature.INDENT_OUTPUT)

    // Don't fail on unknown properties
    .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)

    // Include null values
    .serializationInclusion(JsonInclude.Include.ALWAYS)

    .build();
```

## Migration from Jackson 2.x

### Step-by-Step

1. **Update pom.xml**
   - Change groupId: `com.fasterxml.jackson.core` → `tools.jackson.core`
   - Remove `jackson-datatype-jdk8` and `jackson-datatype-jsr310` (built-in)
   - Keep annotations at `com.fasterxml.jackson.core:jackson-annotations:2.20`

2. **Update module-info.java**
   - Change: `com.fasterxml.jackson.databind` → `tools.jackson.databind`
   - Change opens: `to com.fasterxml.jackson.databind` → `to tools.jackson.databind`
   - Remove jsr310/jdk8 module requires

3. **Update code**
   - `ObjectMapper` → `JsonMapper`
   - `new ObjectMapper()` → `JsonMapper.builder().build()`
   - Remove `mapper.registerModule(new JavaTimeModule())`
   - Update imports: `com.fasterxml.jackson.databind` → `tools.jackson.databind.json`

4. **Keep annotations unchanged**
   - `@JsonProperty`, `@JsonCreator`, etc. stay at `com.fasterxml.jackson.annotation`

### Before/After Examples

```java
// BEFORE (Jackson 2.x)
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

ObjectMapper mapper = new ObjectMapper();
mapper.registerModule(new JavaTimeModule());
mapper.enable(SerializationFeature.INDENT_OUTPUT);
mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
String json = mapper.writeValueAsString(obj);

// AFTER (Jackson 3.x)
import tools.jackson.databind.json.JsonMapper;
import tools.jackson.databind.SerializationFeature;

JsonMapper mapper = JsonMapper.builder()
    .enable(SerializationFeature.INDENT_OUTPUT)
    .build();
String json = mapper.writeValueAsString(obj);
```

---

## Learnings & Quirks

### ObjectMapper vs JsonMapper
- `ObjectMapper` still exists in Jackson 3 but is deprecated
- Use `JsonMapper` which provides the builder pattern
- `JsonMapper.builder().build()` is the canonical way

### Annotations Compatibility
- Jackson 3 databind works with Jackson 2 annotations
- This is intentional to ease migration
- Don't try to find Jackson 3 annotations - they don't exist

### Maven Central Search Lag
- Maven Central's search API may not show the latest Jackson 3 versions
- The artifacts download fine with Maven
- Trust `mvn dependency:tree` over search.maven.org

### SerializationFeature Location
- `SerializationFeature` moved to `tools.jackson.databind.SerializationFeature`
- Not in `tools.jackson.databind.json`

### No More Fluent Configuration on Instance
- Jackson 2: `mapper.enable(feature)` returns `this`
- Jackson 3: Use builder pattern instead

<!-- Add new learnings above this line -->
