---
name: behavioral
description: |
    Behavioral design patterns from the Gang of Four — Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, and Visitor. Patterns that manage algorithms, relationships, and responsibilities between objects.
    USE FOR: object communication, event handling, state management, algorithm encapsulation, request handling chains, undo/redo, publish-subscribe
    DO NOT USE FOR: object creation (use creational), structural composition (use structural)
license: MIT
metadata:
  displayName: "Behavioral Patterns"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Refactoring.Guru — Behavioral Design Patterns"
    url: "https://refactoring.guru/design-patterns/behavioral-patterns"
  - title: "Behavioral Pattern — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Behavioral_pattern"
---

# Behavioral Design Patterns

## Overview
Behavioral patterns are concerned with algorithms and the assignment of responsibilities between objects. They describe not just patterns of objects or classes but also the patterns of communication between them. These patterns characterize complex control flow that is difficult to follow at run-time — they shift your focus away from flow of control to the way objects are interconnected.

---

## 1. Chain of Responsibility

### Intent
Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it.

### Structure

```
┌──────────────────┐
│    Handler        │◀────────────┐
│    (interface)    │             │ next
├──────────────────┤             │
│ + handle(req)     │─────────────┘
│ + setNext(h)      │
└──────┬───────────┘
       │ implements
       ├──────────────┬──────────────┐
       ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ HandlerA    │ │ HandlerB    │ │ HandlerC    │
└────────────┘ └────────────┘ └────────────┘
```

### Participants
- **Handler** — defines an interface for handling requests; optionally links to a successor
- **ConcreteHandler** — handles requests it is responsible for; forwards unhandled requests to the next handler
- **Client** — initiates the request to a handler in the chain

### When to Use
- More than one object may handle a request, and the handler is not known a priori
- You want to issue a request to one of several objects without specifying the receiver explicitly
- The set of handlers should be configurable dynamically (e.g., middleware pipelines)

### TypeScript Example

```typescript
// Handler interface
interface SupportHandler {
  setNext(handler: SupportHandler): SupportHandler;
  handle(issue: { level: string; message: string }): string;
}

// Base handler
abstract class BaseSupportHandler implements SupportHandler {
  private next: SupportHandler | null = null;

  setNext(handler: SupportHandler): SupportHandler {
    this.next = handler;
    return handler;
  }

  handle(issue: { level: string; message: string }): string {
    if (this.next) {
      return this.next.handle(issue);
    }
    return `No handler found for: ${issue.message}`;
  }
}

// Concrete handlers
class TierOneSupport extends BaseSupportHandler {
  handle(issue: { level: string; message: string }): string {
    if (issue.level === "basic") {
      return `[Tier 1] Resolved: ${issue.message}`;
    }
    return super.handle(issue);
  }
}

class TierTwoSupport extends BaseSupportHandler {
  handle(issue: { level: string; message: string }): string {
    if (issue.level === "intermediate") {
      return `[Tier 2] Resolved: ${issue.message}`;
    }
    return super.handle(issue);
  }
}

class EngineeringSupport extends BaseSupportHandler {
  handle(issue: { level: string; message: string }): string {
    if (issue.level === "critical") {
      return `[Engineering] Resolved: ${issue.message}`;
    }
    return super.handle(issue);
  }
}

// Usage — build the chain
const tier1 = new TierOneSupport();
const tier2 = new TierTwoSupport();
const engineering = new EngineeringSupport();

tier1.setNext(tier2).setNext(engineering);

console.log(tier1.handle({ level: "basic", message: "Password reset" }));
// [Tier 1] Resolved: Password reset
console.log(tier1.handle({ level: "critical", message: "Data corruption" }));
// [Engineering] Resolved: Data corruption
```

---

## 2. Command

### Intent
Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

### Structure

```
┌──────────┐       ┌──────────────────┐       ┌──────────────┐
│  Invoker  │──────▶│    Command        │       │   Receiver    │
│           │       │    (interface)    │       ├──────────────┤
└──────────┘       ├──────────────────┤       │ + action()    │
                    │ + execute()       │       └──────┬───────┘
                    │ + undo()          │              │
                    └──────┬───────────┘              │
                           │ implements                │
                           ▼                           │
                    ┌──────────────────┐              │
                    │ ConcreteCommand   │──────────────┘
                    ├──────────────────┤   calls
                    │ - receiver        │
                    │ - state           │
                    │ + execute()       │
                    │ + undo()          │
                    └──────────────────┘
```

### Participants
- **Command** — declares an interface for executing an operation
- **ConcreteCommand** — binds a Receiver to an action; implements execute/undo
- **Invoker** — asks the command to carry out the request
- **Receiver** — knows how to perform the operations associated with the request

### When to Use
- You need to parameterize objects with an action to perform
- You need to specify, queue, and execute requests at different times
- You need to support undo/redo
- You need to support logging changes so they can be reapplied after a crash

### TypeScript Example

```typescript
// Receiver
class TextEditor {
  content = "";

  insert(text: string, position: number): void {
    this.content = this.content.slice(0, position) + text + this.content.slice(position);
  }

  delete(position: number, length: number): string {
    const deleted = this.content.slice(position, position + length);
    this.content = this.content.slice(0, position) + this.content.slice(position + length);
    return deleted;
  }
}

// Command interface
interface EditorCommand {
  execute(): void;
  undo(): void;
}

// Concrete commands
class InsertCommand implements EditorCommand {
  constructor(
    private editor: TextEditor,
    private text: string,
    private position: number
  ) {}

  execute(): void {
    this.editor.insert(this.text, this.position);
  }

  undo(): void {
    this.editor.delete(this.position, this.text.length);
  }
}

class DeleteCommand implements EditorCommand {
  private deletedText = "";

  constructor(
    private editor: TextEditor,
    private position: number,
    private length: number
  ) {}

  execute(): void {
    this.deletedText = this.editor.delete(this.position, this.length);
  }

  undo(): void {
    this.editor.insert(this.deletedText, this.position);
  }
}

// Invoker with undo/redo
class CommandHistory {
  private undoStack: EditorCommand[] = [];
  private redoStack: EditorCommand[] = [];

  execute(command: EditorCommand): void {
    command.execute();
    this.undoStack.push(command);
    this.redoStack = []; // clear redo on new action
  }

  undo(): void {
    const cmd = this.undoStack.pop();
    if (cmd) {
      cmd.undo();
      this.redoStack.push(cmd);
    }
  }

  redo(): void {
    const cmd = this.redoStack.pop();
    if (cmd) {
      cmd.execute();
      this.undoStack.push(cmd);
    }
  }
}

// Usage
const editor = new TextEditor();
const history = new CommandHistory();

history.execute(new InsertCommand(editor, "Hello", 0));
history.execute(new InsertCommand(editor, " World", 5));
console.log(editor.content); // "Hello World"

history.undo();
console.log(editor.content); // "Hello"

history.redo();
console.log(editor.content); // "Hello World"
```

---

## 3. Iterator

### Intent
Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

### Structure

```
┌──────────────────┐        ┌──────────────────┐
│   Aggregate       │───────▶│    Iterator       │
│   (interface)     │creates │    (interface)    │
├──────────────────┤        ├──────────────────┤
│ + createIterator()│        │ + hasNext(): bool │
└──────────────────┘        │ + next(): T       │
                             └──────────────────┘
```

### Participants
- **Iterator** — defines an interface for accessing and traversing elements
- **ConcreteIterator** — implements the Iterator interface; tracks the current position
- **Aggregate** — defines an interface for creating an Iterator object
- **ConcreteAggregate** — returns an instance of the ConcreteIterator

### When to Use
- You want to access a collection's elements without exposing its internal structure
- You want to support multiple traversals of the same collection
- You want a uniform interface for traversing different types of collections

### TypeScript Example

```typescript
// Iterator interface
interface Iterator<T> {
  hasNext(): boolean;
  next(): T;
  reset(): void;
}

// Concrete collection with custom iterator
class TreeNode<T> {
  children: TreeNode<T>[] = [];
  constructor(public value: T) {}

  add(...nodes: TreeNode<T>[]): this {
    this.children.push(...nodes);
    return this;
  }
}

// Depth-first iterator
class DepthFirstIterator<T> implements Iterator<T> {
  private stack: TreeNode<T>[];

  constructor(private root: TreeNode<T>) {
    this.stack = [root];
  }

  hasNext(): boolean {
    return this.stack.length > 0;
  }

  next(): T {
    if (!this.hasNext()) throw new Error("No more elements");
    const node = this.stack.pop()!;
    // Push children in reverse so left child is processed first
    for (let i = node.children.length - 1; i >= 0; i--) {
      this.stack.push(node.children[i]);
    }
    return node.value;
  }

  reset(): void {
    this.stack = [this.root];
  }
}

// Breadth-first iterator
class BreadthFirstIterator<T> implements Iterator<T> {
  private queue: TreeNode<T>[];

  constructor(private root: TreeNode<T>) {
    this.queue = [root];
  }

  hasNext(): boolean {
    return this.queue.length > 0;
  }

  next(): T {
    if (!this.hasNext()) throw new Error("No more elements");
    const node = this.queue.shift()!;
    this.queue.push(...node.children);
    return node.value;
  }

  reset(): void {
    this.queue = [this.root];
  }
}

// Usage
const tree = new TreeNode("A")
  .add(
    new TreeNode("B").add(new TreeNode("D"), new TreeNode("E")),
    new TreeNode("C").add(new TreeNode("F"))
  );

const dfs = new DepthFirstIterator(tree);
const dfsResult: string[] = [];
while (dfs.hasNext()) dfsResult.push(dfs.next());
console.log("DFS:", dfsResult.join(" -> ")); // A -> B -> D -> E -> C -> F

const bfs = new BreadthFirstIterator(tree);
const bfsResult: string[] = [];
while (bfs.hasNext()) bfsResult.push(bfs.next());
console.log("BFS:", bfsResult.join(" -> ")); // A -> B -> C -> D -> E -> F
```

---

## 4. Mediator

### Intent
Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly, and it lets you vary their interaction independently.

### Structure

```
┌──────────────────┐        ┌──────────────────┐
│    Mediator       │◀───────│   Colleague       │
│    (interface)    │        │   (interface)     │
├──────────────────┤        ├──────────────────┤
│ + notify(sender,  │        │ - mediator        │
│         event)    │        └──────┬───────────┘
└──────┬───────────┘               │ implements
       │ implements                 ├──────────┐
       ▼                           ▼          ▼
┌──────────────────┐       ┌──────────┐┌──────────┐
│ ConcreteMediator  │       │ColleagueA││ColleagueB│
│                   │       └──────────┘└──────────┘
│ - colleagueA      │
│ - colleagueB      │
└──────────────────┘
```

### Participants
- **Mediator** — defines an interface for communicating with Colleague objects
- **ConcreteMediator** — implements cooperative behavior by coordinating Colleague objects
- **Colleague** — each Colleague knows its Mediator and communicates with it instead of other Colleagues

### When to Use
- A set of objects communicate in well-defined but complex ways
- Reusing an object is difficult because it refers to and communicates with many other objects
- A behavior distributed between several classes should be customizable without subclassing

### TypeScript Example

```typescript
// Mediator interface
interface ChatMediator {
  sendMessage(message: string, sender: ChatUser): void;
  addUser(user: ChatUser): void;
}

// Colleague
class ChatUser {
  private messages: string[] = [];

  constructor(
    public name: string,
    private mediator: ChatMediator
  ) {
    mediator.addUser(this);
  }

  send(message: string): void {
    console.log(`${this.name} sends: ${message}`);
    this.mediator.sendMessage(message, this);
  }

  receive(message: string, from: string): void {
    const formatted = `${from}: ${message}`;
    this.messages.push(formatted);
    console.log(`  ${this.name} received <- ${formatted}`);
  }

  getHistory(): string[] {
    return [...this.messages];
  }
}

// Concrete mediator
class ChatRoom implements ChatMediator {
  private users: ChatUser[] = [];

  addUser(user: ChatUser): void {
    this.users.push(user);
  }

  sendMessage(message: string, sender: ChatUser): void {
    for (const user of this.users) {
      if (user !== sender) {
        user.receive(message, sender.name);
      }
    }
  }
}

// Usage — users never reference each other directly
const room = new ChatRoom();
const alice = new ChatUser("Alice", room);
const bob = new ChatUser("Bob", room);
const charlie = new ChatUser("Charlie", room);

alice.send("Hello everyone!");
// Alice sends: Hello everyone!
//   Bob received <- Alice: Hello everyone!
//   Charlie received <- Alice: Hello everyone!

bob.send("Hey Alice!");
// Bob sends: Hey Alice!
//   Alice received <- Bob: Hey Alice!
//   Charlie received <- Bob: Hey Alice!
```

---

## 5. Memento

### Intent
Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.

### Structure

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Caretaker    │────▶│    Memento        │◀────│  Originator   │
├──────────────┤keeps│    (opaque)       │saves├──────────────┤
│ - mementos[]  │     ├──────────────────┤     │ - state       │
└──────────────┘     │ + getState()      │     │ + save()      │
                      └──────────────────┘     │ + restore(m)  │
                                                └──────────────┘
```

### Participants
- **Memento** — stores internal state of the Originator; protects against access by objects other than the Originator
- **Originator** — creates a Memento containing a snapshot of its current state; uses a Memento to restore
- **Caretaker** — responsible for keeping the Memento; never operates on or examines its contents

### When to Use
- A snapshot of an object's state must be saved so it can be restored later
- A direct interface to obtaining the state would expose implementation details and break encapsulation

### TypeScript Example

```typescript
// Memento
class EditorMemento {
  constructor(
    private readonly content: string,
    private readonly cursorPos: number,
    private readonly timestamp: Date
  ) {}

  getContent(): string { return this.content; }
  getCursorPos(): number { return this.cursorPos; }
  getTimestamp(): Date { return this.timestamp; }
}

// Originator
class DocumentEditor {
  private content = "";
  private cursorPos = 0;

  type(text: string): void {
    this.content =
      this.content.slice(0, this.cursorPos) +
      text +
      this.content.slice(this.cursorPos);
    this.cursorPos += text.length;
  }

  moveCursor(pos: number): void {
    this.cursorPos = Math.max(0, Math.min(pos, this.content.length));
  }

  save(): EditorMemento {
    return new EditorMemento(this.content, this.cursorPos, new Date());
  }

  restore(memento: EditorMemento): void {
    this.content = memento.getContent();
    this.cursorPos = memento.getCursorPos();
  }

  toString(): string {
    return `"${this.content}" (cursor@${this.cursorPos})`;
  }
}

// Caretaker
class EditorHistory {
  private snapshots: EditorMemento[] = [];

  push(memento: EditorMemento): void {
    this.snapshots.push(memento);
  }

  pop(): EditorMemento | undefined {
    return this.snapshots.pop();
  }
}

// Usage
const doc = new DocumentEditor();
const history = new EditorHistory();

doc.type("Hello");
history.push(doc.save());

doc.type(" World");
history.push(doc.save());

doc.type("!!!");
console.log(doc.toString()); // "Hello World!!!" (cursor@14)

doc.restore(history.pop()!);
console.log(doc.toString()); // "Hello World" (cursor@11)

doc.restore(history.pop()!);
console.log(doc.toString()); // "Hello" (cursor@5)
```

---

## 6. Observer

### Intent
Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

### Structure

```
┌──────────────────┐         ┌──────────────────┐
│    Subject        │────────▶│    Observer       │
├──────────────────┤ notifies│    (interface)    │
│ - observers[]     │         ├──────────────────┤
│ + attach(obs)     │         │ + update(data)    │
│ + detach(obs)     │         └──────┬───────────┘
│ + notify()        │                │ implements
└──────────────────┘                ▼
                              ┌──────────────────┐
                              │ ConcreteObserver   │
                              ├──────────────────┤
                              │ + update(data)    │
                              └──────────────────┘
```

### Participants
- **Subject** — knows its observers; provides an interface for attaching and detaching Observer objects
- **Observer** — defines an updating interface for objects that should be notified of changes
- **ConcreteSubject** — stores state of interest; sends a notification when state changes
- **ConcreteObserver** — maintains a reference to a ConcreteSubject; implements the update interface

### When to Use
- When a change to one object requires changing others, and you do not know how many objects need to change
- When an object should notify other objects without making assumptions about who those objects are

### TypeScript Example

```typescript
// Observer interface
interface EventListener<T> {
  update(event: string, data: T): void;
}

// Subject — generic event emitter
class EventEmitter<T> {
  private listeners = new Map<string, Set<EventListener<T>>>();

  subscribe(event: string, listener: EventListener<T>): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);

    // Return unsubscribe function
    return () => this.listeners.get(event)?.delete(listener);
  }

  protected notify(event: string, data: T): void {
    this.listeners.get(event)?.forEach(listener => listener.update(event, data));
  }
}

// Concrete subject
class Store extends EventEmitter<{ key: string; value: unknown }> {
  private state = new Map<string, unknown>();

  set(key: string, value: unknown): void {
    const old = this.state.get(key);
    this.state.set(key, value);
    this.notify("change", { key, value });
    if (old === undefined) {
      this.notify("add", { key, value });
    }
  }

  get(key: string): unknown {
    return this.state.get(key);
  }
}

// Concrete observers
class LoggingObserver implements EventListener<{ key: string; value: unknown }> {
  update(event: string, data: { key: string; value: unknown }): void {
    console.log(`[LOG] ${event}: ${data.key} = ${JSON.stringify(data.value)}`);
  }
}

class ValidationObserver implements EventListener<{ key: string; value: unknown }> {
  update(event: string, data: { key: string; value: unknown }): void {
    if (data.key === "email" && typeof data.value === "string") {
      if (!data.value.includes("@")) {
        console.log(`[WARN] Invalid email: ${data.value}`);
      }
    }
  }
}

// Usage
const store = new Store();
const unsubLog = store.subscribe("change", new LoggingObserver());
store.subscribe("change", new ValidationObserver());

store.set("name", "Alice");    // [LOG] change: name = "Alice"
store.set("email", "invalid"); // [LOG] change: email = "invalid"
                                // [WARN] Invalid email: invalid

unsubLog(); // unsubscribe logger
store.set("name", "Bob");      // (no log output, validation still active)
```

---

## 7. State

### Intent
Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

### Structure

```
┌──────────────────┐        ┌──────────────────┐
│    Context        │───────▶│     State         │
├──────────────────┤ has-a  │    (interface)    │
│ - state: State    │        ├──────────────────┤
│ + request()       │        │ + handle(ctx)     │
└──────────────────┘        └──────┬───────────┘
                                   │ implements
                            ┌──────┼──────────┐
                            ▼      ▼          ▼
                     ┌─────────┐┌─────────┐┌─────────┐
                     │ StateA   ││ StateB   ││ StateC   │
                     └─────────┘└─────────┘└─────────┘
```

### Participants
- **Context** — maintains an instance of a ConcreteState subclass that defines the current state
- **State** — defines an interface for encapsulating the behavior associated with a particular state
- **ConcreteState** — each subclass implements behavior associated with a state of the Context

### When to Use
- An object's behavior depends on its state, and it must change behavior at runtime
- Operations have large multipart conditional statements that depend on the object's state

### TypeScript Example

```typescript
// State interface
interface OrderState {
  next(order: Order): void;
  cancel(order: Order): void;
  toString(): string;
}

// Context
class Order {
  private state: OrderState;

  constructor(public readonly id: string) {
    this.state = new PendingState();
  }

  setState(state: OrderState): void {
    console.log(`  Order ${this.id}: ${this.state} -> ${state}`);
    this.state = state;
  }

  next(): void { this.state.next(this); }
  cancel(): void { this.state.cancel(this); }
  getStatus(): string { return this.state.toString(); }
}

// Concrete states
class PendingState implements OrderState {
  next(order: Order): void { order.setState(new PaidState()); }
  cancel(order: Order): void { order.setState(new CancelledState()); }
  toString(): string { return "PENDING"; }
}

class PaidState implements OrderState {
  next(order: Order): void { order.setState(new ShippedState()); }
  cancel(order: Order): void {
    console.log(`  Refunding order ${order.id}...`);
    order.setState(new CancelledState());
  }
  toString(): string { return "PAID"; }
}

class ShippedState implements OrderState {
  next(order: Order): void { order.setState(new DeliveredState()); }
  cancel(order: Order): void {
    console.log(`  Cannot cancel — order ${order.id} already shipped`);
  }
  toString(): string { return "SHIPPED"; }
}

class DeliveredState implements OrderState {
  next(order: Order): void {
    console.log(`  Order ${order.id} already delivered`);
  }
  cancel(order: Order): void {
    console.log(`  Cannot cancel — order ${order.id} already delivered`);
  }
  toString(): string { return "DELIVERED"; }
}

class CancelledState implements OrderState {
  next(order: Order): void {
    console.log(`  Order ${order.id} is cancelled — no further transitions`);
  }
  cancel(order: Order): void {
    console.log(`  Order ${order.id} is already cancelled`);
  }
  toString(): string { return "CANCELLED"; }
}

// Usage
const order = new Order("ORD-001");
order.next();   // PENDING -> PAID
order.next();   // PAID -> SHIPPED
order.cancel(); // Cannot cancel — already shipped
order.next();   // SHIPPED -> DELIVERED
```

---

## 8. Strategy

### Intent
Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

### Structure

```
┌──────────────────┐        ┌──────────────────┐
│    Context        │───────▶│    Strategy       │
├──────────────────┤ has-a  │    (interface)    │
│ - strategy        │        ├──────────────────┤
│ + execute()       │        │ + execute(data)   │
└──────────────────┘        └──────┬───────────┘
                                   │ implements
                            ┌──────┼──────────┐
                            ▼      ▼          ▼
                     ┌────────┐┌────────┐┌────────┐
                     │ StratA  ││ StratB  ││ StratC  │
                     └────────┘└────────┘└────────┘
```

### Participants
- **Strategy** — declares an interface common to all supported algorithms
- **ConcreteStrategy** — implements the algorithm using the Strategy interface
- **Context** — is configured with a ConcreteStrategy; delegates to its Strategy

### When to Use
- Many related classes differ only in their behavior
- You need different variants of an algorithm
- An algorithm uses data that clients should not know about
- A class defines many behaviors, and these appear as multiple conditional statements

### TypeScript Example

```typescript
// Strategy interface
interface CompressionStrategy {
  compress(data: string): string;
  name: string;
}

// Concrete strategies
class GzipStrategy implements CompressionStrategy {
  name = "gzip";
  compress(data: string): string {
    return `[gzip:${data.length}]${data.substring(0, 10)}...`;
  }
}

class BrotliStrategy implements CompressionStrategy {
  name = "brotli";
  compress(data: string): string {
    return `[br:${data.length}]${data.substring(0, 8)}...`;
  }
}

class NoCompressionStrategy implements CompressionStrategy {
  name = "none";
  compress(data: string): string {
    return data;
  }
}

// Context
class FileCompressor {
  constructor(private strategy: CompressionStrategy) {}

  setStrategy(strategy: CompressionStrategy): void {
    this.strategy = strategy;
  }

  compressFile(filename: string, content: string): string {
    const result = this.strategy.compress(content);
    return `${filename} compressed with ${this.strategy.name}: ${result}`;
  }
}

// Usage — swap algorithms at runtime
const compressor = new FileCompressor(new GzipStrategy());
console.log(compressor.compressFile("data.json", "a]".repeat(1000)));

compressor.setStrategy(new BrotliStrategy());
console.log(compressor.compressFile("data.json", "a".repeat(1000)));

// Strategy selection based on file size
function selectStrategy(size: number): CompressionStrategy {
  if (size > 10000) return new BrotliStrategy();
  if (size > 1000) return new GzipStrategy();
  return new NoCompressionStrategy();
}
```

---

## 9. Template Method

### Intent
Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure.

### Structure

```
┌──────────────────────┐
│   AbstractClass       │
├──────────────────────┤
│ + templateMethod()    │  ← calls step1, step2, step3 in order
│ + step1()            │  ← may have default implementation
│ + step2()            │  ← abstract — subclass MUST implement
│ + step3()            │  ← hook — subclass CAN override
└──────┬───────────────┘
       │ extends
       ▼
┌──────────────────────┐
│   ConcreteClass       │
├──────────────────────┤
│ + step2()            │  ← implements required step
│ + step3()            │  ← optionally overrides hook
└──────────────────────┘
```

### Participants
- **AbstractClass** — defines the template method (the skeleton); declares abstract steps and optional hooks
- **ConcreteClass** — implements the abstract steps; optionally overrides hooks

### When to Use
- You want to implement the invariant parts of an algorithm once and let subclasses fill in the varying parts
- You want to control which parts of an algorithm subclasses can override (hooks vs. required steps)
- Common behavior among subclasses should be factored and localized in a common class to avoid duplication

### TypeScript Example

```typescript
// Abstract class with template method
abstract class DataPipeline {
  // Template method — defines the skeleton
  run(source: string): string {
    const raw = this.extract(source);
    const validated = this.validate(raw);
    const transformed = this.transform(validated);
    this.beforeLoad(transformed); // hook
    const result = this.load(transformed);
    this.afterLoad(result); // hook
    return result;
  }

  // Abstract steps — subclasses MUST implement
  protected abstract extract(source: string): string[];
  protected abstract transform(data: string[]): string[];
  protected abstract load(data: string[]): string;

  // Default step — can be overridden
  protected validate(data: string[]): string[] {
    return data.filter(item => item.trim().length > 0);
  }

  // Hooks — do nothing by default, subclasses CAN override
  protected beforeLoad(_data: string[]): void {}
  protected afterLoad(_result: string): void {}
}

// Concrete implementation
class CsvToJsonPipeline extends DataPipeline {
  protected extract(source: string): string[] {
    return source.split("\n");
  }

  protected transform(data: string[]): string[] {
    const headers = data[0].split(",");
    return data.slice(1).map(row => {
      const values = row.split(",");
      const obj: Record<string, string> = {};
      headers.forEach((h, i) => obj[h.trim()] = values[i]?.trim() ?? "");
      return JSON.stringify(obj);
    });
  }

  protected load(data: string[]): string {
    return `[${data.join(",")}]`;
  }

  protected afterLoad(result: string): void {
    console.log(`Loaded ${JSON.parse(result).length} records`);
  }
}

// Usage
const pipeline = new CsvToJsonPipeline();
const csv = "name,age\nAlice,30\nBob,25\n";
const json = pipeline.run(csv);
console.log(json); // [{"name":"Alice","age":"30"},{"name":"Bob","age":"25"}]
// Loaded 2 records
```

---

## 10. Visitor

### Intent
Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

### Structure

```
┌──────────────────┐       ┌──────────────────────┐
│    Visitor        │       │     Element           │
│    (interface)    │       │     (interface)       │
├──────────────────┤       ├──────────────────────┤
│ + visitA(elemA)   │       │ + accept(visitor)     │
│ + visitB(elemB)   │       └──────┬───────────────┘
└──────┬───────────┘              │ implements
       │ implements                ├──────────┐
       ▼                          ▼          ▼
┌────────────────┐         ┌──────────┐┌──────────┐
│ConcreteVisitor  │         │ ElementA  ││ ElementB  │
├────────────────┤         ├──────────┤├──────────┤
│ + visitA(elemA) │         │ accept(v) ││ accept(v) │
│ + visitB(elemB) │         │{v.visitA} ││{v.visitB} │
└────────────────┘         └──────────┘└──────────┘
```

### Participants
- **Visitor** — declares a visit operation for each class of ConcreteElement
- **ConcreteVisitor** — implements each visit operation
- **Element** — defines an accept(visitor) method
- **ConcreteElement** — implements accept by calling the appropriate visitor method

### When to Use
- An object structure contains many classes with differing interfaces, and you want to perform operations that depend on their concrete classes
- Many distinct and unrelated operations need to be performed on objects in a structure, and you want to avoid "polluting" their classes
- The classes in the structure rarely change, but you often define new operations over the structure

### TypeScript Example

```typescript
// Visitor interface
interface ASTVisitor<R> {
  visitNumber(node: NumberNode): R;
  visitBinaryOp(node: BinaryOpNode): R;
  visitUnaryOp(node: UnaryOpNode): R;
}

// Element interface
interface ASTNode {
  accept<R>(visitor: ASTVisitor<R>): R;
}

// Concrete elements
class NumberNode implements ASTNode {
  constructor(public value: number) {}

  accept<R>(visitor: ASTVisitor<R>): R {
    return visitor.visitNumber(this);
  }
}

class BinaryOpNode implements ASTNode {
  constructor(
    public operator: "+" | "-" | "*" | "/",
    public left: ASTNode,
    public right: ASTNode
  ) {}

  accept<R>(visitor: ASTVisitor<R>): R {
    return visitor.visitBinaryOp(this);
  }
}

class UnaryOpNode implements ASTNode {
  constructor(public operator: "-", public operand: ASTNode) {}

  accept<R>(visitor: ASTVisitor<R>): R {
    return visitor.visitUnaryOp(this);
  }
}

// Concrete visitor — evaluator
class EvaluatorVisitor implements ASTVisitor<number> {
  visitNumber(node: NumberNode): number { return node.value; }

  visitBinaryOp(node: BinaryOpNode): number {
    const l = node.left.accept(this);
    const r = node.right.accept(this);
    switch (node.operator) {
      case "+": return l + r;
      case "-": return l - r;
      case "*": return l * r;
      case "/": return l / r;
    }
  }

  visitUnaryOp(node: UnaryOpNode): number {
    return -node.operand.accept(this);
  }
}

// Concrete visitor — printer
class PrinterVisitor implements ASTVisitor<string> {
  visitNumber(node: NumberNode): string { return String(node.value); }

  visitBinaryOp(node: BinaryOpNode): string {
    return `(${node.left.accept(this)} ${node.operator} ${node.right.accept(this)})`;
  }

  visitUnaryOp(node: UnaryOpNode): string {
    return `(-${node.operand.accept(this)})`;
  }
}

// Usage — same AST, different operations without modifying nodes
// Represents: (3 + 4) * (-2)
const ast = new BinaryOpNode("*",
  new BinaryOpNode("+", new NumberNode(3), new NumberNode(4)),
  new UnaryOpNode("-", new NumberNode(2))
);

console.log(ast.accept(new PrinterVisitor()));    // ((3 + 4) * (-2))
console.log(ast.accept(new EvaluatorVisitor()));  // -14
```

---

## 11. Interpreter

### Intent
Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language.

### Note on Usage
The Interpreter pattern is the **least commonly used** GoF pattern in modern practice. Most real-world expression evaluation is handled by parser generators, embedded scripting engines (Lua, JS), or expression libraries. Use Interpreter only for simple, well-defined grammars (e.g., query filters, configuration rules).

### Structure

```
┌───────────────────────┐
│  AbstractExpression    │
│  (interface)           │
├───────────────────────┤
│ + interpret(context)   │
└──────┬────────────────┘
       │ implements
       ├──────────────────┐
       ▼                  ▼
┌──────────────────┐ ┌──────────────────┐
│TerminalExpression │ │NonterminalExpr.  │
│(literal values)   │ │(rules/operators) │
└──────────────────┘ └──────────────────┘
```

### When to Use
- The grammar is simple and efficiency is not a critical concern
- You want to evaluate simple rule expressions, search filters, or configuration DSLs

### TypeScript Example

```typescript
// Context
interface InterpretContext {
  variables: Record<string, boolean>;
}

// Abstract expression
interface BoolExpression {
  interpret(ctx: InterpretContext): boolean;
  toString(): string;
}

// Terminal expression
class Variable implements BoolExpression {
  constructor(private name: string) {}
  interpret(ctx: InterpretContext): boolean {
    return ctx.variables[this.name] ?? false;
  }
  toString(): string { return this.name; }
}

// Nonterminal expressions
class AndExpression implements BoolExpression {
  constructor(private left: BoolExpression, private right: BoolExpression) {}
  interpret(ctx: InterpretContext): boolean {
    return this.left.interpret(ctx) && this.right.interpret(ctx);
  }
  toString(): string { return `(${this.left} AND ${this.right})`; }
}

class OrExpression implements BoolExpression {
  constructor(private left: BoolExpression, private right: BoolExpression) {}
  interpret(ctx: InterpretContext): boolean {
    return this.left.interpret(ctx) || this.right.interpret(ctx);
  }
  toString(): string { return `(${this.left} OR ${this.right})`; }
}

class NotExpression implements BoolExpression {
  constructor(private expr: BoolExpression) {}
  interpret(ctx: InterpretContext): boolean {
    return !this.expr.interpret(ctx);
  }
  toString(): string { return `NOT(${this.expr})`; }
}

// Usage — evaluate: (isAdmin OR (isActive AND NOT(isBanned)))
const expr = new OrExpression(
  new Variable("isAdmin"),
  new AndExpression(
    new Variable("isActive"),
    new NotExpression(new Variable("isBanned"))
  )
);

console.log(`Rule: ${expr}`);
console.log(expr.interpret({ variables: { isAdmin: false, isActive: true, isBanned: false } })); // true
console.log(expr.interpret({ variables: { isAdmin: false, isActive: true, isBanned: true } }));  // false
console.log(expr.interpret({ variables: { isAdmin: true, isActive: false, isBanned: true } }));  // true
```

---

## Commonly Confused Pairs

### Strategy vs State

| Aspect | Strategy | State |
|--------|----------|-------|
| **Intent** | Swap an algorithm from outside | Change behavior as internal state changes |
| **Who decides** | The client selects the strategy | The state objects trigger transitions |
| **Awareness** | Strategies are unaware of each other | States often know about sibling states |
| **Typical trigger** | Client calls `setStrategy()` | Internal condition triggers `setState()` |
| **Example** | Choose sort algorithm | Order status lifecycle (Pending -> Paid -> Shipped) |

**Rule of thumb**: If the client picks the behavior, it is Strategy. If the object changes its own behavior based on internal conditions, it is State.

### Command vs Memento

| Aspect | Command | Memento |
|--------|---------|---------|
| **Intent** | Encapsulate an action as an object | Capture a snapshot of state |
| **What it stores** | An operation + its parameters | An object's internal state |
| **Undo mechanism** | Reverse the operation (execute inverse) | Restore the saved state |
| **Scope** | One action at a time | Full state snapshot |
| **Example** | "Insert text at position 5" (undo = delete) | "Save entire document state" (undo = restore) |

**Rule of thumb**: Command stores *what to do* (and how to undo it). Memento stores *what things looked like* (so you can go back).

### Observer vs Mediator

| Aspect | Observer | Mediator |
|--------|----------|----------|
| **Direction** | One-to-many (subject -> observers) | Many-to-many (colleagues <-> mediator) |
| **Coupling** | Observers subscribe to a subject | Colleagues only know the mediator |
| **Awareness** | Subject does not know observer types | Mediator knows all colleague types |
| **Typical use** | Event notification, data binding | Complex UI interactions, chat rooms |
| **Distribution** | Distributed — each subject manages its list | Centralized — one mediator coordinates all |

**Rule of thumb**: Observer is for broadcasting events. Mediator is for coordinating complex interactions between many objects.

---

## Full Comparison Table

| Pattern | Key Mechanism | Problem It Solves |
|---------|--------------|-------------------|
| **Chain of Responsibility** | Linked handler chain | Decouple sender from receiver; multiple potential handlers |
| **Command** | Request as object | Parameterize, queue, log, undo operations |
| **Interpreter** | Grammar tree evaluation | Evaluate simple expressions and DSLs |
| **Iterator** | Sequential traversal interface | Access elements without exposing internals |
| **Mediator** | Central coordinator | Reduce N:M coupling between collaborating objects |
| **Memento** | State snapshot | Save/restore state without breaking encapsulation |
| **Observer** | Publish-subscribe | Notify dependents of state changes automatically |
| **State** | State-driven delegation | Change object behavior when state changes |
| **Strategy** | Algorithm delegation | Swap algorithms at runtime |
| **Template Method** | Skeleton + hooks | Reuse algorithm structure, vary individual steps |
| **Visitor** | Double dispatch | Add operations to class hierarchies without modifying them |

## Decision Guide

```
How do objects communicate or behave?
│
├─ Pass request along until someone handles it?
│  └──▶ Chain of Responsibility
│
├─ Encapsulate a request for undo/redo/queuing?
│  └──▶ Command
│
├─ Traverse a collection without exposing internals?
│  └──▶ Iterator
│
├─ Reduce coupling between many interacting objects?
│  └──▶ Mediator
│
├─ Save and restore object state?
│  └──▶ Memento
│
├─ Notify others when state changes?
│  └──▶ Observer
│
├─ Change behavior based on internal state?
│  └──▶ State
│
├─ Swap algorithms at runtime?
│  └──▶ Strategy
│
├─ Reuse algorithm skeleton, vary steps?
│  └──▶ Template Method
│
├─ Add operations across a class hierarchy?
│  └──▶ Visitor
│
└─ Evaluate simple grammar or expressions?
   └──▶ Interpreter (but consider a parser library first)
```
