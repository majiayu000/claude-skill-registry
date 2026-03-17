---
title: "GraphQL Integration"
description: "Integración completa con GraphQL: queries, mutations, subscriptions en tiempo real y cache automático"
keywords: ["graphql", "apollo", "graphql-client", "subscriptions", "queries", "mutations"]
level: "🔴 Avanzado"
tags: ["backend", "frontend", "api", "data-fetching"]
---

# GraphQL Integration Skill

## 📋 Descripción

Este skill proporciona patrones y mejores prácticas para integrar GraphQL en aplicaciones Flutter, incluyendo:

- Configuración de clientes GraphQL (Apollo, Hive)
- Queries, mutations y subscriptions
- Gestión de caché y estado
- Manejo de errores y reintentos
- Optimización de rendimiento
- Testing de operaciones GraphQL

## 🎯 Cuándo Usar Este Skill

Usa este skill cuando necesites:

- Integrar una API GraphQL en tu aplicación Flutter
- Implementar queries y mutations complejas
- Manejar subscriptions en tiempo real
- Optimizar el caché de datos
- Implementar paginación y lazy loading
- Testing de operaciones GraphQL

## 🚀 Configuración Inicial

### 1. Agregar Dependencias

```yaml
dependencies:
  graphql: ^5.0.0
  graphql_flutter: ^5.0.0
  # O si prefieres Apollo:
  # apollo_flutter: ^0.x.x
```

### 2. Configurar el Cliente GraphQL

```dart
import 'package:graphql_flutter/graphql_flutter.dart';

final HttpLink httpLink = HttpLink(
  'https://api.example.com/graphql',
);

final AuthLink authLink = AuthLink(
  getToken: () async => 'Bearer YOUR_TOKEN',
);

final Link link = authLink.concat(httpLink);

final GraphQLClient graphQLClient = GraphQLClient(
  link: link,
  cache: GraphQLCache(store: HiveStore()),
);
```

## 📝 Queries

### Query Simple

```dart
const String GET_USER = '''
  query GetUser(\$id: ID!) {
    user(id: \$id) {
      id
      name
      email
    }
  }
''';

Future<void> fetchUser(String userId) async {
  final QueryOptions options = QueryOptions(
    document: gql(GET_USER),
    variables: {'id': userId},
  );

  final QueryResult result = await graphQLClient.query(options);

  if (result.hasException) {
    print(result.exception);
  } else {
    final user = result.data?['user'];
    print('User: $user');
  }
}
```

### Query con Paginación

```dart
const String GET_USERS_PAGINATED = '''
  query GetUsers(\$first: Int!, \$after: String) {
    users(first: \$first, after: \$after) {
      edges {
        node {
          id
          name
        }
        cursor
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
''';

Future<void> fetchUsersPaginated({
  required int pageSize,
  String? cursor,
}) async {
  final QueryOptions options = QueryOptions(
    document: gql(GET_USERS_PAGINATED),
    variables: {
      'first': pageSize,
      'after': cursor,
    },
    fetchPolicy: FetchPolicy.networkOnly,
  );

  final QueryResult result = await graphQLClient.query(options);
  // Procesar resultados...
}
```

## ✏️ Mutations

### Mutation Simple

```dart
const String CREATE_USER = '''
  mutation CreateUser(\$input: CreateUserInput!) {
    createUser(input: \$input) {
      id
      name
      email
    }
  }
''';

Future<void> createUser({
  required String name,
  required String email,
}) async {
  final MutationOptions options = MutationOptions(
    document: gql(CREATE_USER),
    variables: {
      'input': {
        'name': name,
        'email': email,
      }
    },
  );

  final QueryResult result = await graphQLClient.mutate(options);

  if (result.hasException) {
    print('Error: ${result.exception}');
  } else {
    final newUser = result.data?['createUser'];
    print('User created: $newUser');
  }
}
```

### Mutation con Optimistic Response

```dart
const String UPDATE_USER = '''
  mutation UpdateUser(\$id: ID!, \$input: UpdateUserInput!) {
    updateUser(id: \$id, input: \$input) {
      id
      name
      email
    }
  }
''';

Future<void> updateUserOptimistic({
  required String userId,
  required String name,
  required String email,
}) async {
  final MutationOptions options = MutationOptions(
    document: gql(UPDATE_USER),
    variables: {
      'id': userId,
      'input': {'name': name, 'email': email}
    },
    optimisticResult: {
      'updateUser': {
        'id': userId,
        'name': name,
        'email': email,
      }
    },
  );

  final QueryResult result = await graphQLClient.mutate(options);
  // Manejar resultado...
}
```

## 🔄 Subscriptions

### Subscription en Tiempo Real

```dart
const String ON_USER_UPDATED = '''
  subscription OnUserUpdated(\$userId: ID!) {
    userUpdated(userId: \$userId) {
      id
      name
      email
      updatedAt
    }
  }
''';

Stream<QueryResult> subscribeToUserUpdates(String userId) {
  final SubscriptionOptions options = SubscriptionOptions(
    document: gql(ON_USER_UPDATED),
    variables: {'userId': userId},
  );

  return graphQLClient.subscribe(options);
}

// Usar en Widget
class UserSubscriptionWidget extends StatelessWidget {
  final String userId;

  const UserSubscriptionWidget({required this.userId});

  @override
  Widget build(BuildContext context) {
    return Subscription(
      options: SubscriptionOptions(
        document: gql(ON_USER_UPDATED),
        variables: {'userId': userId},
      ),
      builder: (result) {
        if (result.hasException) {
          return Text('Error: ${result.exception}');
        }

        if (result.isLoading) {
          return const CircularProgressIndicator();
        }

        final user = result.data?['userUpdated'];
        return Text('User: ${user?['name']}');
      },
    );
  }
}
```

## 💾 Gestión de Caché

### Configurar Políticas de Caché

```dart
// Cache-first: Usar caché si está disponible
final QueryOptions cacheFirstOptions = QueryOptions(
  document: gql(GET_USER),
  variables: {'id': userId},
  fetchPolicy: FetchPolicy.cacheFirst,
);

// Network-first: Intentar red, fallback a caché
final QueryOptions networkFirstOptions = QueryOptions(
  document: gql(GET_USER),
  variables: {'id': userId},
  fetchPolicy: FetchPolicy.networkFirst,
);

// Network-only: Siempre desde red
final QueryOptions networkOnlyOptions = QueryOptions(
  document: gql(GET_USER),
  variables: {'id': userId},
  fetchPolicy: FetchPolicy.networkOnly,
);

// Cache-and-network: Caché inmediato + actualizar desde red
final QueryOptions cacheAndNetworkOptions = QueryOptions(
  document: gql(GET_USER),
  variables: {'id': userId},
  fetchPolicy: FetchPolicy.cacheAndNetwork,
);
```

### Actualizar Caché Manualmente

```dart
void updateUserInCache(String userId, Map<String, dynamic> userData) {
  final cacheMap = graphQLClient.cache.read(
    'User:$userId',
  );

  graphQLClient.cache.write(
    'User:$userId',
    {...?cacheMap, ...userData},
  );
}

void invalidateUserCache(String userId) {
  graphQLClient.cache.delete('User:$userId');
}
```

## ⚠️ Manejo de Errores

### Clasificar Errores GraphQL

```dart
Future<void> handleGraphQLError(QueryResult result) async {
  if (result.hasException) {
    final exception = result.exception;

    if (exception is OperationException) {
      // Errores de GraphQL
      for (final error in exception.graphqlErrors) {
        print('GraphQL Error: ${error.message}');
        print('Extensions: ${error.extensions}');

        // Clasificar por tipo
        if (error.extensions?['code'] == 'UNAUTHENTICATED') {
          // Manejar autenticación
          await refreshToken();
        } else if (error.extensions?['code'] == 'FORBIDDEN') {
          // Manejar autorización
          showPermissionError();
        }
      }

      // Errores de red
      if (exception.linkException != null) {
        print('Network Error: ${exception.linkException}');
      }
    }
  }
}
```

### Reintentos Automáticos

```dart
final Link retryLink = RetryLink(
  attempts: 3,
  delay: (attemptCount) {
    return Duration(seconds: attemptCount);
  },
  test: (exception) {
    // Reintentar solo en errores de red, no en errores GraphQL
    return exception is NetworkException;
  },
);

final Link link = authLink.concat(retryLink).concat(httpLink);
```

## 🧪 Testing

### Test de Query

```dart
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:mockito/mockito.dart';
import 'package:test/test.dart';

void main() {
  group('GraphQL Queries', () {
    late GraphQLClient mockClient;

    setUp(() {
      mockClient = MockGraphQLClient();
    });

    test('fetchUser returns user data', () async {
      final mockResult = QueryResult(
        data: {
          'user': {
            'id': '1',
            'name': 'John Doe',
            'email': 'john@example.com',
          }
        },
      );

      when(mockClient.query(any)).thenAnswer((_) async => mockResult);

      // Ejecutar query
      final result = await mockClient.query(
        QueryOptions(document: gql(GET_USER)),
      );

      expect(result.data?['user']['name'], 'John Doe');
    });
  });
}
```

### Test de Mutation

```dart
test('createUser creates new user', () async {
  final mockResult = QueryResult(
    data: {
      'createUser': {
        'id': '123',
        'name': 'Jane Doe',
        'email': 'jane@example.com',
      }
    },
  );

  when(mockClient.mutate(any)).thenAnswer((_) async => mockResult);

  final result = await mockClient.mutate(
    MutationOptions(document: gql(CREATE_USER)),
  );

  expect(result.data?['createUser']['id'], '123');
});
```

## 🔐 Seguridad

### Validación de Queries

```dart
// Usar variables en lugar de string interpolation
// ❌ MAL
const String badQuery = '''
  query {
    user(id: "$userId") { ... }
  }
''';

// ✅ BIEN
const String goodQuery = '''
  query GetUser(\$id: ID!) {
    user(id: \$id) { ... }
  }
''';

final options = QueryOptions(
  document: gql(goodQuery),
  variables: {'id': userId},
);
```

### Proteger Tokens

```dart
final AuthLink authLink = AuthLink(
  getToken: () async {
    // Obtener token de almacenamiento seguro
    final token = await secureStorage.read(key: 'auth_token');
    return 'Bearer $token';
  },
  resetToken: () async {
    // Limpiar token en caso de error 401
    await secureStorage.delete(key: 'auth_token');
  },
);
```

## 📊 Optimización de Rendimiento

### Lazy Loading

```dart
const String GET_POSTS_LAZY = '''
  query GetPosts(\$first: Int!, \$after: String) {
    posts(first: \$first, after: \$after) {
      edges {
        node {
          id
          title
          # No cargar contenido completo
          excerpt
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
''';

// Cargar contenido completo solo cuando sea necesario
const String GET_POST_FULL = '''
  query GetPost(\$id: ID!) {
    post(id: \$id) {
      id
      title
      content
      author { ... }
      comments { ... }
    }
  }
''';
```

### Batching de Queries

```dart
const String BATCH_QUERIES = '''
  query BatchQueries(\$userId: ID!, \$postId: ID!) {
    user(id: \$userId) { ... }
    post(id: \$postId) { ... }
  }
''';

// Ejecutar múltiples queries en una sola solicitud
final result = await graphQLClient.query(
  QueryOptions(
    document: gql(BATCH_QUERIES),
    variables: {
      'userId': userId,
      'postId': postId,
    },
  ),
);
```

## 🔗 Recursos

- [GraphQL Official Docs](https://graphql.org/)
- [graphql_flutter Package](https://pub.dev/packages/graphql_flutter)
- [Apollo Client Documentation](https://www.apollographql.com/docs/flutter/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)

## 📚 Mejores Prácticas

1. **Usar variables en queries** - Evita inyección de código
2. **Implementar caché inteligente** - Reduce solicitudes de red
3. **Manejar errores explícitamente** - Proporciona feedback al usuario
4. **Usar subscriptions para datos en tiempo real** - No polling
5. **Validar datos en cliente** - Mejora UX
6. **Documentar esquema GraphQL** - Facilita mantenimiento
7. **Testing exhaustivo** - Queries, mutations y subscriptions
8. **Monitorear rendimiento** - Latencia y tamaño de payloads

---

**Última actualización:** Febrero 2026
**Versión:** 1.0.0
