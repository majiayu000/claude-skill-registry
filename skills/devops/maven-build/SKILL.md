---
name: maven-build
description: Maven build configuration for the crypto-scout multi-module Java 25 project
license: MIT
compatibility: opencode
metadata:
  tool: maven
  language: java
  version: "25"
---

## What I Do

Provide guidance for building, testing, and packaging the crypto-scout multi-module Maven project.

## Project Structure

```
crypto-scout/
├── pom.xml                    # Root aggregator POM
├── crypto-scout-test/
│   └── pom.xml               # Test library
├── crypto-scout-client/
│   └── pom.xml               # Data collection service
├── crypto-scout-collector/
│   └── pom.xml               # Data persistence service
└── crypto-scout-analyst/
    └── pom.xml               # Analysis service
```

## Build Commands

### Full Build
```bash
# Clean and build all modules
mvn clean install

# Build without tests (faster)
mvn -q -DskipTests install
```

### Module-Specific Builds
```bash
# Build specific module
cd crypto-scout-client
mvn clean package

# Build with dependency resolution from root
cd crypto-scout-collector
mvn clean package -DskipTests
```

### Testing
```bash
# Run all tests
mvn test

# Run tests for specific module
cd crypto-scout-test && mvn test

# Run single test class
mvn test -Dtest=AmqpPublisherTest

# Run single test method
mvn test -Dtest=AmqpPublisherTest#shouldPublishPayloadToStream

# Run with extended timeout (slow environments)
mvn -q -Dpodman.compose.up.timeout.min=5 test

# Custom database URL for tests
mvn -q -Dtest.db.jdbc.url=jdbc:postgresql://localhost:5432/crypto_scout test
```

### Clean Build
```bash
# Clean all modules
mvn clean

# Clean and rebuild single module
cd crypto-scout-client && mvn clean package -DskipTests
```

## POM Configuration

### Root POM (Aggregator)
```xml
<project>
    <groupId>com.github.akarazhev.cryptoscout</groupId>
    <artifactId>crypto-scout</artifactId>
    <version>0.0.1</version>
    <packaging>pom</packaging>
    
    <modules>
        <module>crypto-scout-test</module>
        <module>crypto-scout-client</module>
        <module>crypto-scout-collector</module>
        <module>crypto-scout-analyst</module>
    </modules>
</project>
```

### Module POM Structure
```xml
<project>
    <parent>
        <groupId>com.github.akarazhev.cryptoscout</groupId>
        <artifactId>crypto-scout</artifactId>
        <version>0.0.1</version>
    </parent>
    
    <artifactId>crypto-scout-client</artifactId>
    <packaging>jar</packaging>
    
    <properties>
        <java.version>25</java.version>
        <maven.compiler.release>25</maven.compiler.release>
        <activej.version>6.0-rc2</activej.version>
        <stream-client.version>1.4.0</stream-client.version>
    </properties>
    
    <build>
        <plugins>
            <!-- Compiler plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.14.1</version>
                <configuration>
                    <release>25</release>
                </configuration>
            </plugin>
            
            <!-- Shade plugin for fat JAR -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>3.6.1</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <transformers>
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <mainClass>com.github.akarazhev.cryptoscout.Client</mainClass>
                                </transformer>
                            </transformers>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

## Key Dependencies by Module

### crypto-scout-test
- `jcryptolib` - JSON utilities
- `junit-jupiter` - JUnit 6 testing
- `stream-client` - RabbitMQ Streams
- `amqp-client` - RabbitMQ AMQP
- `postgresql` - PostgreSQL driver

### crypto-scout-client
- `jcryptolib` - JSON utilities, clients
- `activej-servicegraph` - DI and lifecycle
- `activej-jmx` - JMX monitoring
- `stream-client` - RabbitMQ Streams

### crypto-scout-collector
- `jcryptolib` - JSON utilities
- `activej-servicegraph` - DI and lifecycle
- `activej-jmx` - JMX monitoring
- `activej-datastream` - Data streaming
- `stream-client` - RabbitMQ Streams
- `amqp-client` - RabbitMQ AMQP
- `postgresql` - PostgreSQL driver
- `HikariCP` - Connection pooling

### crypto-scout-analyst
- Same as crypto-scout-collector

## Build Artifacts

### Output Locations
| Module | Artifact | Location |
|--------|----------|----------|
| crypto-scout-test | JAR library | `target/crypto-scout-test-0.0.1.jar` |
| crypto-scout-client | Fat JAR | `target/crypto-scout-client-0.0.1.jar` |
| crypto-scout-collector | Fat JAR | `target/crypto-scout-collector-0.0.1.jar` |
| crypto-scout-analyst | Fat JAR | `target/crypto-scout-analyst-0.0.1.jar` |

### Running Fat JARs
```bash
# crypto-scout-client
java -jar crypto-scout-client/target/crypto-scout-client-0.0.1.jar

# crypto-scout-collector
java -jar crypto-scout-collector/target/crypto-scout-collector-0.0.1.jar

# crypto-scout-analyst
java -jar crypto-scout-analyst/target/crypto-scout-analyst-0.0.1.jar
```

## Troubleshooting

### Build Failures
```bash
# Clear local repo and rebuild
rm -rf ~/.m2/repository/com/github/akarazhev
mvn clean install

# Debug dependency tree
mvn dependency:tree

# Check for updates
mvn versions:display-dependency-updates
```

### Test Failures
```bash
# Run with verbose output
mvn test -X

# Skip tests temporarily
mvn install -DskipTests

# Run specific test with debug
mvn test -Dtest=ClassName -Dmaven.surefire.debug
```

## When to Use Me

Use this skill when:
- Building the project for the first time
- Running tests across modules
- Creating new module POMs
- Troubleshooting build failures
- Configuring Maven plugins
- Understanding dependency management
- Packaging services for deployment
