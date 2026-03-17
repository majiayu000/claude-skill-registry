---
name: migrating-to-swift-concurrency
description: Provides the complete Swift Concurrency Migration Guide. Use when migrating to Swift 6, resolving data-race safety errors, understanding Sendable and actor isolation, or incrementally adopting async/await.
---

# Swift Concurrency Migration Guide

The complete content of the Swift Concurrency Migration Guide by Apple. This guide helps you migrate your code to take advantage of Swift's data-race safety guarantees and the Swift 6 language mode.

## Documentation

- **Data Race Safety** ([Guide/DataRaceSafety.md](Guide/DataRaceSafety.md)): Learn about the fundamental concepts Swift uses to enable data-race-free
- **Migration Strategy** ([Guide/MigrationStrategy.md](Guide/MigrationStrategy.md)): Get started migrating your project to the Swift 6 language mode.
- **Enable data-race safety checking** ([Guide/EnableDataRaceSafety.md](Guide/EnableDataRaceSafety.md)): Use Swift 6 to get full data-race safety checking or add checking to an existing Swift 5 project.
- **Common Compiler Errors** ([Guide/CommonProblems.md](Guide/CommonProblems.md)): Identify, understand, and address common problems you can encounter while
- **Incremental Adoption** ([Guide/IncrementalAdoption.md](Guide/IncrementalAdoption.md)): Learn how you can introduce Swift concurrency features into your project
- **Migrating to upcoming language features** ([Guide/FeatureMigration.md](Guide/FeatureMigration.md)): Migrate your project to upcoming language features.
- **Source Compatibility** ([Guide/SourceCompatibility.md](Guide/SourceCompatibility.md)): See an overview of potential source compatibility issues.
- **Library Evolution** ([Guide/LibraryEvolution.md](Guide/LibraryEvolution.md)): Annotate library APIs for concurrency while preserving source and ABI
- **Runtime Behavior** ([Guide/RuntimeBehavior.md](Guide/RuntimeBehavior.md)): Learn how Swift concurrency runtime semantics differ from other runtimes you may

## Code Examples

Swift source files demonstrating migration patterns and concurrency concepts:

- **Boundaries.swift** ([Examples/Boundaries.swift](Examples/Boundaries.swift)): Example code demonstrating Boundaries.
- **ConformanceMismatches.swift** ([Examples/ConformanceMismatches.swift](Examples/ConformanceMismatches.swift)): Example code demonstrating ConformanceMismatches.
- **DispatchQueue_PendingWork.swift** ([Examples/DispatchQueue_PendingWork.swift](Examples/DispatchQueue_PendingWork.swift)): Example code demonstrating DispatchQueue PendingWork.
- **Globals.swift** ([Examples/Globals.swift](Examples/Globals.swift)): Example code demonstrating Globals.
- **IncrementalMigration.swift** ([Examples/IncrementalMigration.swift](Examples/IncrementalMigration.swift)): Example code demonstrating IncrementalMigration.
- **PreconcurrencyImport.swift** ([Examples/PreconcurrencyImport.swift](Examples/PreconcurrencyImport.swift)): Example code demonstrating PreconcurrencyImport.
- **main.swift** ([Examples/main.swift](Examples/main.swift)): Example code demonstrating main.

## Usage Notes

- Start with Data Race Safety to understand the core concepts
- Follow the Migration Strategy for a recommended approach
- Refer to Common Problems for solutions to typical issues
- Use the Code Examples as reference implementations

## License & Attribution

### Content License

The documentation and example code in this skill are from the [Swift Concurrency Migration Guide](https://github.com/swiftlang/swift-migration-guide.git), copyright Apple Inc. and the Swift project authors, distributed under the [Apache 2.0 License](LICENSE.txt).

### Skill Structure License

The structure and organization of this skill (this index file) is copyright Kyle Hughes, distributed under the MIT License.
