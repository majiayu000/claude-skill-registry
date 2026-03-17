---
name: scala-expert
version: 1.0.0
description: Expert-level Scala, functional programming, Akka, and reactive systems
category: languages
tags: [scala, functional-programming, akka, cats, zio]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(scala:*, sbt:*)
---

# Scala Expert

Expert guidance for Scala development, functional programming, Akka actors, and reactive systems.

## Core Concepts

### Scala Fundamentals
- Immutability
- Pattern matching
- Case classes
- Traits and mixins
- Implicit conversions
- For comprehensions

### Functional Programming
- Higher-order functions
- Monads (Option, Either, Try)
- Functors and Applicatives
- Type classes
- Pure functions
- Referential transparency

### Reactive Systems
- Akka actors
- Akka Streams
- Akka HTTP
- Play Framework
- Cats Effect
- ZIO

## Scala Basics

```scala
// Case classes
case class User(id: String, name: String, email: String, age: Int)

// Pattern matching
def processUser(user: User): String = user match {
  case User(_, name, _, age) if age < 18 => s"$name is a minor"
  case User(_, name, _, age) if age >= 65 => s"$name is a senior"
  case User(_, name, _, _) => s"$name is an adult"
}

// Options instead of null
def findUser(id: String): Option[User] = {
  database.get(id)
}

val userName = findUser("123") match {
  case Some(user) => user.name
  case None => "Unknown"
}

// Or using map
val name = findUser("123").map(_.name).getOrElse("Unknown")

// For comprehensions
def getUserWithPosts(userId: String): Option[(User, List[Post])] = {
  for {
    user <- findUser(userId)
    posts <- findPosts(userId)
  } yield (user, posts)
}

// Traits and mixins
trait Serializable {
  def toJson: String
}

trait Loggable {
  def log(message: String): Unit = println(s"[LOG] $message")
}

case class Person(name: String, age: Int) extends Serializable with Loggable {
  def toJson: String = s"""{"name":"$name","age":$age}"""
}

// Implicit classes (extension methods)
implicit class StringOps(s: String) {
  def isValidEmail: Boolean = s.contains("@") && s.contains(".")
}

"test@example.com".isValidEmail // true
```

## Functional Programming

```scala
import cats._
import cats.implicits._

// Functor
val numbers = List(1, 2, 3, 4, 5)
val doubled = numbers.map(_ * 2)

// Applicative
val result = (Option(1), Option(2), Option(3)).mapN { (a, b, c) =>
  a + b + c
}

// Monad (flatMap)
def fetchUser(id: String): Future[Option[User]] = ???
def fetchPosts(userId: String): Future[List[Post]] = ???

val userWithPosts: Future[Option[(User, List[Post])]] = {
  fetchUser("123").flatMap {
    case Some(user) =>
      fetchPosts(user.id).map(posts => Some((user, posts)))
    case None =>
      Future.successful(None)
  }
}

// Or with for-comprehension
val result: Future[Option[(User, List[Post])]] = for {
  userOpt <- fetchUser("123")
  posts <- fetchPosts(userOpt.map(_.id).getOrElse(""))
} yield userOpt.map(user => (user, posts))

// Either for error handling
sealed trait Error
case class NotFound(id: String) extends Error
case class ValidationError(message: String) extends Error

def validateUser(user: User): Either[Error, User] = {
  if (user.email.isValidEmail) Right(user)
  else Left(ValidationError("Invalid email"))
}

def saveUser(user: User): Either[Error, User] = {
  for {
    validated <- validateUser(user)
    saved <- database.save(validated)
  } yield saved
}

// Type classes
trait Show[A] {
  def show(a: A): String
}

object Show {
  def apply[A](implicit sh: Show[A]): Show[A] = sh

  implicit val stringShow: Show[String] = new Show[String] {
    def show(s: String): String = s
  }

  implicit val intShow: Show[Int] = new Show[Int] {
    def show(i: Int): String = i.toString
  }

  implicit def listShow[A: Show]: Show[List[A]] = new Show[List[A]] {
    def show(list: List[A]): String = {
      list.map(Show[A].show).mkString("[", ", ", "]")
    }
  }
}

def print[A: Show](a: A): Unit = {
  println(Show[A].show(a))
}
```

## Akka Actors

```scala
import akka.actor.typed._
import akka.actor.typed.scaladsl._

// Actor definition
object UserActor {
  sealed trait Command
  final case class GetUser(id: String, replyTo: ActorRef[Response]) extends Command
  final case class CreateUser(user: User, replyTo: ActorRef[Response]) extends Command

  sealed trait Response
  final case class UserFound(user: User) extends Response
  final case class UserNotFound(id: String) extends Response
  final case class UserCreated(user: User) extends Response

  def apply(): Behavior[Command] = {
    Behaviors.setup { context =>
      var users = Map.empty[String, User]

      Behaviors.receiveMessage {
        case GetUser(id, replyTo) =>
          users.get(id) match {
            case Some(user) =>
              replyTo ! UserFound(user)
            case None =>
              replyTo ! UserNotFound(id)
          }
          Behaviors.same

        case CreateUser(user, replyTo) =>
          users = users + (user.id -> user)
          replyTo ! UserCreated(user)
          Behaviors.same
      }
    }
  }
}

// Using the actor
val system: ActorSystem[UserActor.Command] =
  ActorSystem(UserActor(), "user-system")

import akka.actor.typed.scaladsl.AskPattern._
import akka.util.Timeout
import scala.concurrent.duration._

implicit val timeout: Timeout = 3.seconds

val response: Future[UserActor.Response] =
  system.ask(ref => UserActor.GetUser("123", ref))
```

## Akka Streams

```scala
import akka.stream._
import akka.stream.scaladsl._
import akka.actor.ActorSystem

implicit val system = ActorSystem("streams")
implicit val materializer = ActorMaterializer()

// Simple stream
val source = Source(1 to 10)
val flow = Flow[Int].map(_ * 2)
val sink = Sink.foreach[Int](println)

source.via(flow).runWith(sink)

// Backpressure handling
val throttled = Source(1 to 100)
  .throttle(10, 1.second)
  .map { n =>
    println(s"Processing $n")
    n * 2
  }
  .runWith(Sink.ignore)

// Error handling
val resilient = Source(1 to 10)
  .map { n =>
    if (n == 5) throw new Exception("Error at 5")
    n * 2
  }
  .recover {
    case e: Exception => -1
  }
  .runWith(Sink.seq)

// Parallelism
val parallel = Source(1 to 100)
  .mapAsync(parallelism = 4) { n =>
    Future {
      // Async operation
      Thread.sleep(100)
      n * 2
    }
  }
  .runWith(Sink.seq)
```

## Akka HTTP

```scala
import akka.http.scaladsl.Http
import akka.http.scaladsl.server.Directives._
import akka.http.scaladsl.marshallers.sprayjson.SprayJsonSupport._
import spray.json.DefaultJsonProtocol._

// JSON protocol
case class User(id: String, name: String, email: String)

object JsonProtocol {
  implicit val userFormat = jsonFormat3(User)
}

import JsonProtocol._

// Routes
val routes =
  pathPrefix("api") {
    pathPrefix("users") {
      get {
        path(Segment) { userId =>
          // GET /api/users/:userId
          complete(findUser(userId))
        } ~
        pathEnd {
          // GET /api/users
          complete(getAllUsers())
        }
      } ~
      post {
        pathEnd {
          // POST /api/users
          entity(as[User]) { user =>
            complete(createUser(user))
          }
        }
      }
    }
  }

// Start server
val bindingFuture = Http().newServerAt("localhost", 8080).bind(routes)
```

## Cats Effect / ZIO

```scala
import cats.effect._
import cats.effect.implicits._

// Pure functional effects with Cats Effect
def fetchUser(id: String): IO[User] = IO {
  // Effectful computation
  database.get(id)
}

def saveUser(user: User): IO[Unit] = IO {
  database.save(user)
}

val program: IO[Unit] = for {
  user <- fetchUser("123")
  updated = user.copy(name = "Updated")
  _ <- saveUser(updated)
} yield ()

// Error handling
val safeProgram: IO[Either[Throwable, Unit]] = program.attempt

// Parallel execution
val parallel: IO[List[User]] = {
  List("1", "2", "3")
    .parTraverse(id => fetchUser(id))
}

// ZIO
import zio._

def fetchUserZIO(id: String): Task[User] = ZIO.attempt {
  database.get(id)
}

val zioProgram: Task[Unit] = for {
  user <- fetchUserZIO("123")
  _ <- Console.printLine(s"Found user: ${user.name}")
} yield ()
```

## Best Practices

### Functional Programming
- Prefer immutability
- Use pure functions
- Avoid side effects
- Use Option/Either over null/exceptions
- Leverage type classes
- Use for-comprehensions
- Apply functional composition

### Scala Style
- Follow naming conventions
- Use case classes for data
- Prefer vals over vars
- Use pattern matching
- Avoid null
- Use implicits carefully
- Write idiomatic code

### Performance
- Use lazy evaluation
- Stream large datasets
- Avoid unnecessary allocations
- Use tail recursion
- Profile before optimizing
- Consider parallelism

## Anti-Patterns

❌ Using null
❌ Mutable state everywhere
❌ God objects
❌ Excessive implicits
❌ Not handling errors
❌ Blocking operations
❌ Not using type safety

## Resources

- Scala Documentation: https://docs.scala-lang.org/
- Akka Documentation: https://doc.akka.io/
- Cats: https://typelevel.org/cats/
- ZIO: https://zio.dev/
- Functional Programming in Scala (Red Book)
