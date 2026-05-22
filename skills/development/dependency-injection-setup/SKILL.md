---
name: Dependency Injection Setup
description: Add new services to DIContainer, create protocol-based implementations, set up singletons or factories for Leavn app dependency injection
allowed-tools: Read, Edit, Grep
---

# Dependency Injection Setup

## Instructions

Add new services to Leavn's DIContainer:

1. **Create service protocol**:
   ```swift
   // Services/MyDomain/MyServiceProtocol.swift
   public protocol MyServiceProtocol {
       func doSomething() async throws -> Result
   }
   ```

2. **Create implementation**:
   ```swift
   // Services/MyDomain/MyServiceLive.swift
   public final class MyServiceLive: MyServiceProtocol {
       public init() { }

       public func doSomething() async throws -> Result {
           // Implementation
       }
   }
   ```

3. **Register in DIContainer**:
   ```swift
   // For singletons (stateful services):
   private lazy var _myService = MyServiceLive()
   var myService: MyServiceProtocol {
       _myService
   }

   // For factories (stateless services):
   var myService: MyServiceProtocol {
       MyServiceLive()
   }
   ```

4. **Use in ViewModels**:
   ```swift
   let service = DIContainer.shared.myService
   ```

Use this skill when: Creating new service, adding dependency, setting up DI, refactoring to protocol-oriented design
