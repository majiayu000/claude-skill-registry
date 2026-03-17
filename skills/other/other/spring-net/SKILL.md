---
name: spring-net
description: >
  USE FOR: XML-based dependency injection in legacy .NET Framework applications, aspect-oriented
  programming (AOP) with method interception, declarative transaction management, and migrating
  Java Spring applications to .NET. DO NOT USE FOR: New .NET 6+ applications (use
  Microsoft.Extensions.DependencyInjection), ASP.NET Core projects, or scenarios where
  convention-over-configuration is preferred.
license: MIT
metadata:
  displayName: "Spring.NET"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Spring.NET Official Website"
    url: "https://springframework.net/"
  - title: "Spring.NET GitHub Repository"
    url: "https://github.com/spring-projects/spring-net"
  - title: "Spring.Core NuGet Package"
    url: "https://www.nuget.org/packages/Spring.Core"
---

# Spring.NET

## Overview

Spring.NET is a port of the Java Spring Framework to .NET, providing a comprehensive application framework built around dependency injection (DI) and aspect-oriented programming (AOP). It uses XML configuration files to define object definitions, dependencies, and AOP advice, following the Inversion of Control (IoC) pattern.

Spring.NET was widely used in .NET Framework applications, particularly in enterprise environments familiar with Java Spring. While it is no longer actively developed and has been superseded by `Microsoft.Extensions.DependencyInjection` for modern .NET, it remains relevant for maintaining existing applications and for teams migrating from Java Spring.

The framework includes modules for DI (Spring.Core), AOP (Spring.Aop), data access (Spring.Data), and web integration (Spring.Web).

## XML-Based Object Configuration

Spring.NET uses XML files to declare objects (beans) and their dependencies.

```xml
<?xml version="1.0" encoding="utf-8"?>
<objects xmlns="http://www.springframework.net">

  <!-- Simple object with constructor injection -->
  <object id="connectionString"
          type="Spring.Objects.Factory.Config.VariablePlaceholderConfigurer, Spring.Core">
    <property name="VariableSources">
      <list>
        <object type="Spring.Objects.Factory.Config.PropertyFileVariableSource, Spring.Core">
          <property name="Location" value="file://~/config/database.properties"/>
        </object>
      </list>
    </property>
  </object>

  <object id="userRepository"
          type="MyApp.Data.SqlUserRepository, MyApp.Data">
    <constructor-arg name="connectionString" value="${db.connection}"/>
  </object>

  <object id="emailService"
          type="MyApp.Services.SmtpEmailService, MyApp.Services">
    <property name="SmtpHost" value="smtp.example.com"/>
    <property name="SmtpPort" value="587"/>
    <property name="FromAddress" value="noreply@example.com"/>
  </object>

  <object id="userService"
          type="MyApp.Services.UserService, MyApp.Services">
    <constructor-arg ref="userRepository"/>
    <constructor-arg ref="emailService"/>
  </object>

</objects>
```

## Resolving Objects from the Container

```csharp
using Spring.Context;
using Spring.Context.Support;

public class Program
{
    public static void Main(string[] args)
    {
        // Load the application context from XML
        IApplicationContext ctx = new XmlApplicationContext("objects.xml");

        // Resolve objects by name
        IUserService userService = (IUserService)ctx.GetObject("userService");

        // Use the service
        User user = userService.GetById(42);
        Console.WriteLine($"User: {user.Name}");
    }
}
```

## Constructor and Property Injection

```csharp
namespace MyApp.Services
{
    public interface IUserService
    {
        User GetById(int id);
        void Register(string name, string email);
    }

    public class UserService : IUserService
    {
        private readonly IUserRepository _repository;
        private readonly IEmailService _emailService;

        // Constructor injection
        public UserService(IUserRepository repository, IEmailService emailService)
        {
            _repository = repository;
            _emailService = emailService;
        }

        public User GetById(int id)
        {
            return _repository.FindById(id);
        }

        public void Register(string name, string email)
        {
            var user = new User { Name = name, Email = email };
            _repository.Save(user);
            _emailService.SendWelcome(user);
        }
    }
}
```

```csharp
namespace MyApp.Services
{
    public class SmtpEmailService : IEmailService
    {
        // Property injection (set via XML configuration)
        public string SmtpHost { get; set; }
        public int SmtpPort { get; set; }
        public string FromAddress { get; set; }

        public void SendWelcome(User user)
        {
            // Send email using configured SMTP settings
            Console.WriteLine($"Sending welcome email to {user.Email} via {SmtpHost}:{SmtpPort}");
        }
    }
}
```

## Aspect-Oriented Programming (AOP)

Spring.NET AOP allows cross-cutting concerns like logging, transactions, and security to be applied declaratively.

```csharp
using AopAlliance.Intercept;

public class LoggingAdvice : IMethodInterceptor
{
    public object Invoke(IMethodInvocation invocation)
    {
        string methodName = invocation.Method.Name;
        string typeName = invocation.TargetType.Name;

        Console.WriteLine($"[LOG] Entering {typeName}.{methodName}");

        try
        {
            object result = invocation.Proceed();
            Console.WriteLine($"[LOG] Exiting {typeName}.{methodName} successfully");
            return result;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[LOG] Exception in {typeName}.{methodName}: {ex.Message}");
            throw;
        }
    }
}
```

```xml
<objects xmlns="http://www.springframework.net">

  <object id="loggingAdvice"
          type="MyApp.Aspects.LoggingAdvice, MyApp"/>

  <object id="userService"
          type="MyApp.Services.UserService, MyApp.Services">
    <constructor-arg ref="userRepository"/>
    <constructor-arg ref="emailService"/>
  </object>

  <!-- AOP proxy that wraps userService with logging -->
  <object id="userServiceProxy"
          type="Spring.Aop.Framework.ProxyFactoryObject, Spring.Aop">
    <property name="Target" ref="userService"/>
    <property name="InterceptorNames">
      <list>
        <value>loggingAdvice</value>
      </list>
    </property>
    <property name="ProxyInterfaces">
      <list>
        <value>MyApp.Services.IUserService, MyApp.Services</value>
      </list>
    </property>
  </object>

</objects>
```

## Declarative Transaction Management

```csharp
using Spring.Transaction.Interceptor;

public class OrderService : IOrderService
{
    private readonly IOrderRepository _orderRepository;
    private readonly IInventoryRepository _inventoryRepository;

    public OrderService(
        IOrderRepository orderRepository,
        IInventoryRepository inventoryRepository)
    {
        _orderRepository = orderRepository;
        _inventoryRepository = inventoryRepository;
    }

    [Transaction]
    public virtual void PlaceOrder(Order order)
    {
        _orderRepository.Save(order);

        foreach (var item in order.Items)
        {
            _inventoryRepository.DecrementStock(item.ProductId, item.Quantity);
        }
    }
}
```

```xml
<objects xmlns="http://www.springframework.net">

  <object id="transactionManager"
          type="Spring.Data.Core.AdoPlatformTransactionManager, Spring.Data">
    <property name="DbProvider" ref="dbProvider"/>
  </object>

  <object id="transactionInterceptor"
          type="Spring.Transaction.Interceptor.TransactionInterceptor, Spring.Data">
    <property name="TransactionManager" ref="transactionManager"/>
    <property name="TransactionAttributeSource">
      <object type="Spring.Transaction.Interceptor.AttributesTransactionAttributeSource, Spring.Data"/>
    </property>
  </object>

  <object id="orderServiceTarget"
          type="MyApp.Services.OrderService, MyApp.Services">
    <constructor-arg ref="orderRepository"/>
    <constructor-arg ref="inventoryRepository"/>
  </object>

  <object id="orderService"
          type="Spring.Aop.Framework.ProxyFactoryObject, Spring.Aop">
    <property name="Target" ref="orderServiceTarget"/>
    <property name="InterceptorNames">
      <list>
        <value>transactionInterceptor</value>
      </list>
    </property>
  </object>

</objects>
```

## Code-Based Configuration

Spring.NET also supports programmatic configuration as an alternative to XML.

```csharp
using Spring.Context.Support;
using Spring.Objects.Factory.Support;

public class AppConfiguration
{
    public static IApplicationContext CreateContext()
    {
        GenericApplicationContext ctx = new GenericApplicationContext();

        ObjectDefinitionBuilder builder;

        // Register userRepository
        builder = ObjectDefinitionBuilder
            .RootObjectDefinition(new DefaultObjectDefinitionFactory(),
                typeof(SqlUserRepository));
        builder.AddConstructorArg("Server=localhost;Database=mydb");
        ctx.RegisterObjectDefinition("userRepository", builder.ObjectDefinition);

        // Register emailService
        builder = ObjectDefinitionBuilder
            .RootObjectDefinition(new DefaultObjectDefinitionFactory(),
                typeof(SmtpEmailService));
        builder.AddPropertyValue("SmtpHost", "smtp.example.com");
        builder.AddPropertyValue("SmtpPort", 587);
        ctx.RegisterObjectDefinition("emailService", builder.ObjectDefinition);

        // Register userService with dependencies
        builder = ObjectDefinitionBuilder
            .RootObjectDefinition(new DefaultObjectDefinitionFactory(),
                typeof(UserService));
        builder.AddConstructorArgReference("userRepository");
        builder.AddConstructorArgReference("emailService");
        ctx.RegisterObjectDefinition("userService", builder.ObjectDefinition);

        ctx.Refresh();
        return ctx;
    }
}
```

## Spring.NET vs Modern .NET DI

| Aspect | Spring.NET | Microsoft.Extensions.DependencyInjection |
|---|---|---|
| Configuration | XML-based (primary) | Code-based (primary) |
| AOP support | Built-in (proxy-based) | Not built-in (use interceptors) |
| Transaction management | Declarative via attributes | Manual or EF Core |
| .NET target | .NET Framework | .NET Core / .NET 5+ |
| Active development | No (legacy) | Yes |
| Learning curve | High (XML, Spring concepts) | Low (fluent API) |
| Ecosystem | Self-contained | Integrates with all Microsoft.Extensions |

## Best Practices

1. Prefer constructor injection over property injection for required dependencies, reserving property injection only for optional dependencies with sensible defaults.
2. Program against interfaces (e.g., `IUserService`, `IUserRepository`) in all object definitions so that implementations can be swapped via configuration without code changes.
3. Keep XML configuration files organized by module or layer (e.g., `data-objects.xml`, `service-objects.xml`) and import them into a root context file to maintain readability.
4. Use `VariablePlaceholderConfigurer` to externalize environment-specific values (connection strings, URLs) into properties files rather than hardcoding them in XML.
5. Mark methods as `virtual` when using AOP proxies, because Spring.NET's proxy mechanism requires virtual methods to intercept calls on class-based proxies.
6. Use the `[Transaction]` attribute with Spring.Data's transaction interceptor for declarative transaction management instead of manually managing `IDbTransaction` in service code.
7. Validate XML configuration files against the Spring.NET schema to catch typos and incorrect attribute usage at application startup rather than at runtime.
8. When migrating from Spring.NET to Microsoft.Extensions.DependencyInjection, replace XML object definitions with `IServiceCollection` registrations incrementally, module by module.
9. Avoid circular dependencies between objects; Spring.NET can resolve some circular references through property injection, but they indicate a design problem that should be refactored.
10. Consider migrating AOP advice to middleware, decorators, or interceptor patterns (e.g., using Scrutor or Castle DynamicProxy) when porting to modern .NET, as these patterns are more idiomatic.
