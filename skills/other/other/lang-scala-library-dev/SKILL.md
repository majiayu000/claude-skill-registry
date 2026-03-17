---
name: lang-scala-library-dev
description: Scala-specific library development patterns. Use when creating Scala libraries, designing public APIs with immutability, configuring sbt/Mill build tools, managing cross-Scala version builds, publishing to Maven Central, and writing ScalaDoc. Extends lang-scala-dev with library-specific tooling and patterns.
---

# Scala Library Development

Scala-specific patterns for library development. This skill extends `lang-scala-dev` with library tooling, API design patterns, and ecosystem practices for publishing reusable Scala libraries.

## This Skill Extends

- `lang-scala-dev` - Foundational Scala patterns (immutability, traits, pattern matching, type system)

For general Scala concepts like case classes, for-comprehensions, and collections, see the base skill first.

## This Skill Adds

- **Build tooling**: sbt and Mill configuration, project structure, multi-module builds
- **Library API design**: Public API patterns with Scala idioms, binary compatibility
- **Publishing**: Maven Central publishing, cross-building, versioning strategies
- **Documentation**: ScalaDoc best practices, documentation generation
- **Testing**: Library-specific testing patterns, property-based testing

## This Skill Does NOT Cover

- General Scala patterns - see `lang-scala-dev`
- Application development - see `lang-scala-play-dev` or framework-specific skills
- Akka libraries - see `lang-scala-akka-dev`
- Spark libraries - see `lang-scala-spark-dev`

---

## Quick Reference

| Task | sbt Command | Mill Command |
|------|-------------|--------------|
| New library project | `sbt new scala/scala-seed.g8` | `mill init com-lihaoyi/mill-scala-hello.g8` |
| Compile | `sbt compile` | `mill _.compile` |
| Test | `sbt test` | `mill _.test` |
| Package JAR | `sbt package` | `mill _.jar` |
| Generate docs | `sbt doc` | `mill _.docJar` |
| Publish local | `sbt publishLocal` | `mill _.publishLocal` |
| Publish signed | `sbt publishSigned` | `mill mill.scalalib.PublishModule/publish` |
| Cross build | `sbt +compile` | `mill __.compile` |
| Check binary compat | `sbt mimaReportBinaryIssues` | N/A (use sbt-mima plugin) |

---

## Build Tool Configuration

### sbt Project Structure

```
my-library/
├── build.sbt               # Build configuration
├── project/
│   ├── build.properties    # sbt version
│   ├── plugins.sbt         # sbt plugins
│   └── Dependencies.scala  # Dependency management (optional)
├── src/
│   ├── main/
│   │   └── scala/          # Library source code
│   ├── test/
│   │   └── scala/          # Tests
│   └── it/                 # Integration tests (optional)
│       └── scala/
└── docs/                   # Documentation (optional)
```

### build.sbt Configuration

**Required fields for publishing:**

```scala
// build.sbt
ThisBuild / organization := "com.example"
ThisBuild / version      := "0.1.0"
ThisBuild / scalaVersion := "2.13.12"

lazy val root = (project in file("."))
  .settings(
    name := "my-library",

    // Library dependencies
    libraryDependencies ++= Seq(
      "org.typelevel" %% "cats-core" % "2.10.0",
      "org.scalatest" %% "scalatest" % "3.2.17" % Test
    ),

    // Publishing metadata
    publishMavenStyle := true,
    licenses := Seq("Apache-2.0" -> url("http://www.apache.org/licenses/LICENSE-2.0")),
    homepage := Some(url("https://github.com/username/my-library")),
    scmInfo := Some(
      ScmInfo(
        url("https://github.com/username/my-library"),
        "scm:git@github.com:username/my-library.git"
      )
    ),
    developers := List(
      Developer(
        id    = "username",
        name  = "Your Name",
        email = "you@example.com",
        url   = url("https://github.com/username")
      )
    ),

    // Maven Central publishing
    publishTo := {
      val nexus = "https://oss.sonatype.org/"
      if (isSnapshot.value) Some("snapshots" at nexus + "content/repositories/snapshots")
      else Some("releases" at nexus + "service/local/staging/deploy/maven2")
    }
  )
```

### Cross-Building for Multiple Scala Versions

```scala
// build.sbt
lazy val scala213 = "2.13.12"
lazy val scala3   = "3.3.1"

ThisBuild / crossScalaVersions := Seq(scala213, scala3)
ThisBuild / scalaVersion       := scala213  // Default

// Version-specific dependencies
libraryDependencies ++= {
  CrossVersion.partialVersion(scalaVersion.value) match {
    case Some((2, 13)) =>
      Seq("org.scala-lang.modules" %% "scala-parallel-collections" % "1.0.4")
    case Some((3, _)) =>
      Seq.empty  // Not needed in Scala 3
    case _ =>
      Seq.empty
  }
}

// Version-specific source directories
Compile / unmanagedSourceDirectories ++= {
  val sourceDir = (Compile / sourceDirectory).value
  CrossVersion.partialVersion(scalaVersion.value) match {
    case Some((2, n)) => Seq(sourceDir / s"scala-2.$n")
    case Some((3, _)) => Seq(sourceDir / "scala-3")
    case _ => Seq.empty
  }
}
```

**Cross-build commands:**

```bash
# Compile for all versions
sbt +compile

# Test all versions
sbt +test

# Publish all versions
sbt +publishSigned
```

### Mill Configuration

```scala
// build.sc
import mill._, scalalib._, publish._

object mylibrary extends PublishModule with ScalaModule {
  def scalaVersion = "2.13.12"

  def publishVersion = "0.1.0"

  def pomSettings = PomSettings(
    description = "My Scala library",
    organization = "com.example",
    url = "https://github.com/username/my-library",
    licenses = Seq(License.`Apache-2.0`),
    versionControl = VersionControl.github("username", "my-library"),
    developers = Seq(
      Developer("username", "Your Name", "https://github.com/username")
    )
  )

  def ivyDeps = Agg(
    ivy"org.typelevel::cats-core:2.10.0"
  )

  object test extends Tests with TestModule.ScalaTest {
    def ivyDeps = Agg(
      ivy"org.scalatest::scalatest:3.2.17"
    )
  }
}
```

**Cross-building with Mill:**

```scala
// build.sc
import mill._, scalalib._

val scala213 = "2.13.12"
val scala3   = "3.3.1"

trait MyModule extends ScalaModule with PublishModule {
  def publishVersion = "0.1.0"
  // ... common settings
}

object mylibrary extends Cross[MyLibraryModule](scala213, scala3)
class MyLibraryModule(val crossScalaVersion: String) extends MyModule {
  def scalaVersion = crossScalaVersion
}
```

---

## Library API Design

### Public API Patterns

**Prefer immutable data types:**

```scala
// Good: Immutable case class
case class Config(
  timeout: Duration,
  retries: Int,
  baseUrl: String
)

// Modification returns new instance
val updated = config.copy(retries = 5)

// Avoid: Mutable class
class Config {
  var timeout: Duration = _
  var retries: Int = _
  // ...
}
```

**Use sealed traits for ADTs:**

```scala
sealed trait Result[+A]
case class Success[A](value: A) extends Result[A]
case class Failure(error: String) extends Result[Nothing]
case object Pending extends Result[Nothing]

// Exhaustive pattern matching
def handle[A](result: Result[A]): String = result match {
  case Success(value) => s"Got: $value"
  case Failure(error) => s"Error: $error"
  case Pending => "Waiting..."
}
```

**Builder pattern for complex configuration:**

```scala
case class HttpClient private (
  timeout: Duration,
  retries: Int,
  followRedirects: Boolean,
  userAgent: String
)

object HttpClient {
  def builder(): Builder = Builder()

  case class Builder private[HttpClient] (
    timeout: Duration = Duration(30, TimeUnit.SECONDS),
    retries: Int = 3,
    followRedirects: Boolean = true,
    userAgent: String = "MyLibrary/1.0"
  ) {
    def withTimeout(timeout: Duration): Builder = copy(timeout = timeout)
    def withRetries(retries: Int): Builder = copy(retries = retries)
    def withFollowRedirects(follow: Boolean): Builder = copy(followRedirects = follow)
    def withUserAgent(ua: String): Builder = copy(userAgent = ua)

    def build(): HttpClient = HttpClient(timeout, retries, followRedirects, userAgent)
  }
}

// Usage
val client = HttpClient.builder()
  .withTimeout(Duration(60, TimeUnit.SECONDS))
  .withRetries(5)
  .build()
```

**Type classes for extensibility:**

```scala
trait Encoder[A] {
  def encode(value: A): String
}

object Encoder {
  def apply[A](implicit enc: Encoder[A]): Encoder[A] = enc

  def instance[A](f: A => String): Encoder[A] = new Encoder[A] {
    def encode(value: A): String = f(value)
  }

  // Instances
  implicit val intEncoder: Encoder[Int] = instance(_.toString)
  implicit val stringEncoder: Encoder[String] = instance(identity)

  // Derived instance
  implicit def optionEncoder[A](implicit enc: Encoder[A]): Encoder[Option[A]] = {
    instance {
      case Some(value) => enc.encode(value)
      case None => "null"
    }
  }
}

// Usage
def toJson[A: Encoder](value: A): String = {
  Encoder[A].encode(value)
}
```

### API Stability and Versioning

**Use `@deprecated` for gradual migration:**

```scala
object MyLibrary {
  @deprecated("Use newMethod instead", "1.2.0")
  def oldMethod(): Unit = newMethod()

  def newMethod(): Unit = {
    // New implementation
  }
}
```

**Package private for internal APIs:**

```scala
// Visible only within package
private[mylibrary] class InternalHelper {
  // ...
}

// Visible to this module only
private[this] val internalState = mutable.Map.empty[String, Int]
```

**Use opaque types (Scala 3) for type safety:**

```scala
// Scala 3
opaque type UserId = Long

object UserId {
  def apply(value: Long): UserId = value

  extension (id: UserId) {
    def toLong: Long = id
  }
}

// Cannot accidentally pass Long where UserId expected
val userId: UserId = UserId(123L)
val rawId: Long = userId.toLong
```

---

## Binary Compatibility

### MiMa (Migration Manager for Scala)

**Setup in build.sbt:**

```scala
// project/plugins.sbt
addSbtPlugin("com.typesafe" % "sbt-mima-plugin" % "1.1.3")

// build.sbt
import com.typesafe.tools.mima.plugin.MimaPlugin.autoImport._

lazy val root = (project in file("."))
  .enablePlugins(MimaPlugin)
  .settings(
    mimaPreviousArtifacts := Set(organization.value %% name.value % "0.1.0"),

    // Binary compatibility checks
    mimaReportBinaryIssues := {
      mimaReportBinaryIssues.value
      // Fail build on incompatibilities
    },

    // Allow specific breakages
    mimaBinaryIssueFilters ++= Seq(
      // Example: Allow removal of private class
      ProblemFilters.exclude[MissingClassProblem]("com.example.internal.PrivateClass")
    )
  )
```

**Check compatibility:**

```bash
# Report binary compatibility issues
sbt mimaReportBinaryIssues

# Allow breaking changes for major version
sbt "set mimaPreviousArtifacts := Set()" publishLocal
```

### Compatibility Guidelines

| Change | Binary Compatible? | Source Compatible? |
|--------|-------------------|-------------------|
| Add method to class | ✓ Yes | ✓ Yes |
| Add method to trait | ✗ No (before Scala 2.12) | ✓ Yes |
| Remove public method | ✗ No | ✗ No |
| Add parameter with default | ✓ Yes | ✓ Yes |
| Add parameter without default | ✗ No | ✗ No |
| Change return type | ✗ No | ✗ No |
| Make final class | ✗ No | Depends |
| Seal trait | ✗ No | ✗ No |
| Add case to sealed trait | ✗ No | ✗ No |
| Widen visibility | ✓ Yes | ✓ Yes |
| Narrow visibility | ✗ No | ✗ No |

---

## Publishing to Maven Central

### Setup Requirements

1. **Create Sonatype JIRA account**: https://issues.sonatype.org/
2. **Request namespace** (e.g., `com.github.username` or `io.github.username`)
3. **Setup GPG key** for signing artifacts
4. **Configure credentials**

### GPG Signing

**Generate GPG key:**

```bash
# Generate key
gpg --gen-key

# List keys
gpg --list-keys

# Export public key to keyserver
gpg --keyserver keyserver.ubuntu.com --send-keys YOUR_KEY_ID
```

**Configure sbt-pgp:**

```scala
// project/plugins.sbt
addSbtPlugin("com.github.sbt" % "sbt-pgp" % "2.2.1")

// build.sbt
useGpg := true  // Use GPG command-line tool
```

### Credentials Configuration

**Create `~/.sbt/1.0/sonatype.sbt`:**

```scala
credentials += Credentials(
  "Sonatype Nexus Repository Manager",
  "oss.sonatype.org",
  "your-sonatype-username",
  "your-sonatype-password"
)
```

**Or use environment variables:**

```scala
credentials += Credentials(
  "Sonatype Nexus Repository Manager",
  "oss.sonatype.org",
  sys.env.getOrElse("SONATYPE_USERNAME", ""),
  sys.env.getOrElse("SONATYPE_PASSWORD", "")
)
```

### Publishing Workflow

**Using sbt-sonatype plugin:**

```scala
// project/plugins.sbt
addSbtPlugin("org.xerial.sbt" % "sbt-sonatype" % "3.10.0")
addSbtPlugin("com.github.sbt" % "sbt-pgp" % "2.2.1")

// build.sbt
import xerial.sbt.Sonatype._

sonatypeProjectHosting := Some(GitHubHosting("username", "project", "you@example.com"))
sonatypeCredentialHost := "s01.oss.sonatype.org"  // For new projects

publishTo := sonatypePublishToBundle.value
```

**Publish commands:**

```bash
# 1. Update version in build.sbt (remove -SNAPSHOT for release)
# 2. Create git tag
git tag -a v0.1.0 -m "Release 0.1.0"

# 3. Publish and sign
sbt +publishSigned

# 4. Release to Maven Central (bundle workflow)
sbt sonatypeBundleRelease

# Or manual workflow:
# sbt sonatypeClose    # Close staging repo
# sbt sonatypeRelease  # Release to Maven Central

# 5. Push tag
git push origin v0.1.0
```

### Release Checklist

- [ ] Update version in build.sbt (remove `-SNAPSHOT`)
- [ ] Update CHANGELOG.md
- [ ] Run tests: `sbt +test`
- [ ] Check binary compatibility: `sbt mimaReportBinaryIssues`
- [ ] Build for all Scala versions: `sbt +package`
- [ ] Generate and check docs: `sbt doc`
- [ ] Create git tag: `git tag -a vX.Y.Z -m "Release X.Y.Z"`
- [ ] Publish signed artifacts: `sbt +publishSigned`
- [ ] Release to Maven Central: `sbt sonatypeBundleRelease`
- [ ] Push tag: `git push origin vX.Y.Z`
- [ ] Create GitHub release with release notes
- [ ] Bump version to next SNAPSHOT: `X.Y.Z-SNAPSHOT`

---

## ScalaDoc

### ScalaDoc Syntax

```scala
/**
 * Parses a JSON string into a case class.
 *
 * This method uses the implicit [[Decoder]] to convert the JSON string
 * into the target type `A`.
 *
 * @param json the JSON string to parse
 * @tparam A the target type (must have an implicit Decoder)
 * @return a [[scala.util.Try]] containing the parsed value or error
 * @throws IllegalArgumentException if the JSON is malformed
 * @see [[Decoder]] for information on creating custom decoders
 * @example
 * {{{
 * case class Person(name: String, age: Int)
 * implicit val decoder: Decoder[Person] = ...
 *
 * val result = parseJson[Person]("""{"name":"Alice","age":30}""")
 * // result: Success(Person("Alice", 30))
 * }}}
 */
def parseJson[A: Decoder](json: String): Try[A] = ???
```

### ScalaDoc Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `@param` | Parameter description | `@param name the user's name` |
| `@tparam` | Type parameter | `@tparam A the element type` |
| `@return` | Return value | `@return the parsed result` |
| `@throws` | Exception thrown | `@throws IOException if file not found` |
| `@see` | Reference | `@see [[OtherClass]]` |
| `@example` | Code example | `@example {{{ ... }}}` |
| `@note` | Important note | `@note This method is thread-safe` |
| `@since` | Version added | `@since 1.2.0` |
| `@deprecated` | Deprecation notice | `@deprecated("Use newMethod", "1.3.0")` |

### Documentation Generation

**sbt:**

```bash
# Generate API docs
sbt doc

# Open in browser
open target/scala-2.13/api/index.html

# Generate for all Scala versions
sbt +doc
```

**Mill:**

```bash
# Generate docs
mill mylibrary.docJar

# Extract and view
unzip out/mylibrary/docJar.dest/out.jar -d docs
```

### Package-Level Documentation

**Create `package.scala`:**

```scala
/**
 * Core library for JSON parsing and serialization.
 *
 * == Overview ==
 * This package provides type-safe JSON encoding and decoding using type classes.
 *
 * == Quick Start ==
 * {{{
 * import com.example.json._
 *
 * case class User(name: String, age: Int)
 * implicit val decoder = Decoder.derive[User]
 *
 * val json = """{"name":"Alice","age":30}"""
 * val user = parseJson[User](json)
 * }}}
 *
 * @see [[Encoder]] for creating custom encoders
 * @see [[Decoder]] for creating custom decoders
 */
package object json {
  // Package-level type aliases
  type Result[A] = Either[JsonError, A]
}
```

---

## Testing Patterns

### Unit Testing with ScalaTest

```scala
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class ConfigSpec extends AnyFlatSpec with Matchers {

  "Config" should "parse valid configuration" in {
    val config = Config.parse("timeout=30,retries=3")

    config shouldBe defined
    config.get.timeout shouldBe Duration(30, TimeUnit.SECONDS)
    config.get.retries shouldBe 3
  }

  it should "reject invalid timeout values" in {
    val config = Config.parse("timeout=-1")

    config shouldBe empty
  }

  it should "use default values when not specified" in {
    val config = Config.parse("")

    config shouldBe defined
    config.get.retries shouldBe 3  // Default
  }
}
```

### Property-Based Testing with ScalaCheck

```scala
import org.scalacheck.Properties
import org.scalacheck.Prop.forAll

object JsonPropertiesSpec extends Properties("Json") {

  property("roundtrip") = forAll { (user: User) =>
    val json = toJson(user)
    val parsed = fromJson[User](json)

    parsed == Right(user)
  }

  property("never crashes") = forAll { (s: String) =>
    try {
      fromJson[User](s)
      true
    } catch {
      case _: Exception => false
    }
  }
}
```

### Integration Testing

**Create `src/it/scala/` directory:**

```scala
// src/it/scala/HttpClientIntegrationSpec.scala
import org.scalatest.flatspec.AnyFlatSpec

class HttpClientIntegrationSpec extends AnyFlatSpec {

  "HttpClient" should "make real HTTP requests" in {
    val client = HttpClient.builder().build()

    val response = client.get("https://httpbin.org/get")

    assert(response.status == 200)
  }
}
```

**Configure in build.sbt:**

```scala
lazy val IntegrationTest = config("it") extend Test

lazy val root = (project in file("."))
  .configs(IntegrationTest)
  .settings(
    Defaults.itSettings,
    IntegrationTest / scalaSource := baseDirectory.value / "src/it/scala"
  )

// Run integration tests
// sbt it:test
```

---

## Multi-Module Projects

### sbt Multi-Module Setup

```scala
// build.sbt
lazy val commonSettings = Seq(
  organization := "com.example",
  scalaVersion := "2.13.12",
  version := "0.1.0"
)

lazy val core = (project in file("core"))
  .settings(
    commonSettings,
    name := "my-library-core",
    libraryDependencies ++= Seq(
      "org.typelevel" %% "cats-core" % "2.10.0"
    )
  )

lazy val http = (project in file("http"))
  .dependsOn(core)
  .settings(
    commonSettings,
    name := "my-library-http",
    libraryDependencies ++= Seq(
      "org.http4s" %% "http4s-dsl" % "0.23.23"
    )
  )

lazy val json = (project in file("json"))
  .dependsOn(core)
  .settings(
    commonSettings,
    name := "my-library-json",
    libraryDependencies ++= Seq(
      "io.circe" %% "circe-core" % "0.14.6"
    )
  )

lazy val root = (project in file("."))
  .aggregate(core, http, json)
  .settings(
    commonSettings,
    name := "my-library",
    publish / skip := true  // Don't publish root
  )
```

**Module commands:**

```bash
# Build specific module
sbt core/compile

# Test all modules
sbt test

# Publish specific module
sbt core/publishSigned

# Publish all modules
sbt +publishSigned
```

### Mill Multi-Module Setup

```scala
// build.sc
import mill._, scalalib._

trait CommonModule extends ScalaModule {
  def scalaVersion = "2.13.12"
  def publishVersion = "0.1.0"
}

object core extends CommonModule {
  def ivyDeps = Agg(
    ivy"org.typelevel::cats-core:2.10.0"
  )
}

object http extends CommonModule {
  def moduleDeps = Seq(core)
  def ivyDeps = Agg(
    ivy"org.http4s::http4s-dsl:0.23.23"
  )
}

object json extends CommonModule {
  def moduleDeps = Seq(core)
  def ivyDeps = Agg(
    ivy"io.circe::circe-core:0.14.6"
  )
}
```

---

## Anti-Patterns

### 1. Breaking Binary Compatibility

```scala
// v1.0.0
trait Parser {
  def parse(input: String): Result
}

// v1.1.0 - WRONG! Breaks binary compatibility
trait Parser {
  def parse(input: String): Result
  def parseWithOptions(input: String, options: Options): Result
}

// v1.1.0 - Correct: Provide default implementation
trait Parser {
  def parse(input: String): Result

  def parseWithOptions(input: String, options: Options): Result = {
    // Default implementation
    parse(input)
  }
}
```

### 2. Exposing Mutable Collections

```scala
// Bad: Exposes mutable collection
class Registry {
  private val items = mutable.ListBuffer.empty[Item]
  def getItems: mutable.ListBuffer[Item] = items  // Dangerous!
}

// Good: Return immutable view
class Registry {
  private val items = mutable.ListBuffer.empty[Item]
  def getItems: List[Item] = items.toList  // Safe copy
}
```

### 3. Overusing Implicits

```scala
// Bad: Too many implicit conversions
implicit def intToString(x: Int): String = x.toString
implicit def stringToInt(s: String): Int = s.toInt

// Good: Explicit type classes
trait Show[A] {
  def show(a: A): String
}

implicit val intShow: Show[Int] = (a: Int) => a.toString
```

---

## References

- `lang-scala-dev` - Foundational Scala patterns
- [sbt Documentation](https://www.scala-sbt.org/)
- [Mill Documentation](https://mill-build.org/)
- [Maven Central Publishing Guide](https://central.sonatype.org/publish/)
- [MiMa GitHub](https://github.com/lightbend/mima)
- [ScalaDoc Style Guide](https://docs.scala-lang.org/style/scaladoc.html)
- [Scala Library Design Guidelines](https://contributors.scala-lang.org/t/library-design-guidelines/4905)
