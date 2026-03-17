---
name: gof-patterns
description: "Gang of Four design patterns reference. Use this skill when implementing, discussing, or choosing object-oriented design patterns. Auto-activates for architecture decisions, refactoring, and decoupling concerns. Comprehensive coverage of all 23 GoF patterns with pseudocode examples."
---

# GoF Design Patterns Reference

A comprehensive reference for the Gang of Four design patterns. This skill provides language-agnostic guidance with pseudocode examples that can be translated to any programming language.

## When This Skill Activates

This skill automatically activates when you:
- Ask about or need to implement a design pattern
- Need to choose between patterns for a design problem
- Are refactoring code and considering structural improvements
- Discuss architecture, decoupling, or extensibility
- Mention specific patterns: factory, singleton, observer, decorator, etc.

## Quick Pattern Reference

### Creational Patterns (Object Creation)
| Pattern | Intent | Use When |
|---------|--------|----------|
| [Abstract Factory](gof-creational/abstract-factory.md) | Create families of related objects | Need platform/theme independence |
| [Builder](gof-creational/builder.md) | Construct complex objects step-by-step | Object has many optional parts |
| [Factory Method](gof-creational/factory-method.md) | Let subclasses decide which class to instantiate | Don't know concrete types ahead of time |
| [Prototype](gof-creational/prototype.md) | Clone existing objects | Object creation is expensive |
| [Singleton](gof-creational/singleton.md) | Ensure single instance | Need exactly one shared instance |

### Structural Patterns (Composition)
| Pattern | Intent | Use When |
|---------|--------|----------|
| [Adapter](gof-structural/adapter.md) | Convert interface to expected interface | Integrating incompatible interfaces |
| [Bridge](gof-structural/bridge.md) | Separate abstraction from implementation | Need to vary both independently |
| [Composite](gof-structural/composite.md) | Treat individual and groups uniformly | Have tree structures |
| [Decorator](gof-structural/decorator.md) | Add responsibilities dynamically | Need flexible extension |
| [Facade](gof-structural/facade.md) | Simplified interface to subsystem | Complex subsystem needs simple API |
| [Flyweight](gof-structural/flyweight.md) | Share common state efficiently | Many similar objects needed |
| [Proxy](gof-structural/proxy.md) | Control access to object | Need lazy loading, access control, logging |

### Behavioral Patterns (Communication)
| Pattern | Intent | Use When |
|---------|--------|----------|
| [Chain of Responsibility](gof-behavioral/chain-of-responsibility.md) | Pass request along handler chain | Multiple handlers, unknown which handles |
| [Command](gof-behavioral/command.md) | Encapsulate request as object | Need undo, queue, or log operations |
| [Interpreter](gof-behavioral/interpreter.md) | Define grammar and interpret sentences | Have a simple language to parse |
| [Iterator](gof-behavioral/iterator.md) | Sequential access without exposing internals | Need to traverse collections |
| [Mediator](gof-behavioral/mediator.md) | Centralize complex communications | Many objects communicate in complex ways |
| [Memento](gof-behavioral/memento.md) | Capture and restore object state | Need undo/snapshot functionality |
| [Observer](gof-behavioral/observer.md) | Notify dependents of state changes | One-to-many dependency |
| [State](gof-behavioral/state.md) | Alter behavior when state changes | Object behavior depends on state |
| [Strategy](gof-behavioral/strategy.md) | Encapsulate interchangeable algorithms | Need to swap algorithms at runtime |
| [Template Method](gof-behavioral/template-method.md) | Define skeleton, let subclasses fill in | Algorithm structure fixed, steps vary |
| [Visitor](gof-behavioral/visitor.md) | Add operations without changing classes | Need to add many operations to stable structure |

## Decision Guide

See [Pattern Selection Guide](pattern-selection.md) for help choosing the right pattern.

## How to Use This Reference

1. **Choosing a pattern**: Start with the decision guide or tables above
2. **Learning a pattern**: Read the full documentation with examples
3. **Quick reminder**: Use the tables above for at-a-glance reference
4. **Implementation**: Follow the pseudocode, adapt to your language

## Language Translation Notes

The pseudocode in this reference uses these conventions:
- `class` for type definitions
- `function` for methods/functions
- `->` for method calls on objects
- `//` for comments
- Type hints shown as `name: Type`

Translate to your language:
- **PHP**: `class`, `function`, `->`, `//`, type hints in docblocks or PHP 8+
- **JavaScript/TypeScript**: `class`, `function`/arrow, `.`, `//`, TS types
- **Python**: `class`, `def`, `.`, `#`, type hints
- **Java/C#**: Direct mapping with `new`, generics

---

*Based on concepts from "Design Patterns: Elements of Reusable Object-Oriented Software" by Gamma, Helm, Johnson, and Vlissides (Gang of Four), 1994.*
