# 🔗 Skill: GraphQL Integration

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-graphql` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `graphql`, `apollo`, `graphql-client`, `subscriptions` |
| **Referencia** | [GraphQL Flutter](https://pub.dev/packages/graphql_flutter) |

## 🔑 Keywords para Invocación

- `graphql`
- `apollo`
- `graphql-client`
- `subscriptions`
- `mutations`
- `@skill:graphql`

### Ejemplos de Prompts

```
Integra GraphQL para consultas y mutaciones
```

```
Implementa GraphQL con subscriptions en tiempo real
```

```
@skill:graphql - Configura cliente GraphQL con cache
```

## 📖 Descripción

GraphQL Integration permite consultar APIs GraphQL con queries, mutations y subscriptions en tiempo real. Incluye cache automático, optimistic updates, paginación, manejo de errores y code generation.

### ✅ Cuándo Usar Este Skill

- Backend usa GraphQL
- Necesitas queries flexibles
- Datos en tiempo real (subscriptions)
- Optimistic UI updates
- Cache inteligente del lado del cliente
- Reducir over-fetching/under-fetching

### ❌ Cuándo NO Usar Este Skill

- Backend solo REST
- App muy simple
- Team no familiarizado con GraphQL

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── graphql/
│   │   ├── graphql_client.dart
│   │   ├── graphql_config.dart
│   │   ├── graphql_link.dart
│   │   └── cache_config.dart
│   └── utils/
│       └── graphql_helpers.dart
│
├── features/
│   └── products/
│       ├── data/
│       │   ├── datasources/
│       │   │   └── products_graphql_datasource.dart
│       │   ├── models/
│       │   │   └── product_model.dart
│       │   └── repositories/
│       │       └── products_repository_impl.dart
│       ├── domain/
│       │   ├── entities/
│       │   │   └── product.dart
│       │   └── repositories/
│       │       └── products_repository.dart
│       └── presentation/
│           ├── bloc/
│           │   └── products_bloc.dart
│           └── screens/
│               └── products_screen.dart
│
└── graphql/
    ├── queries/
    │   ├── get_products.graphql
    │   └── get_product.graphql
    ├── mutations/
    │   ├── create_product.graphql
    │   ├── update_product.graphql
    │   └── delete_product.graphql
    └── subscriptions/
        └── product_updated.graphql
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # GraphQL Client
  graphql_flutter: ^5.1.2

  # Code Generation (opcional)
  gql: ^1.0.0
  ferry: ^0.15.0
  ferry_flutter: ^0.9.0

  # Utils
  equatable: ^2.0.5
  dartz: ^0.10.1

  # State Management
  flutter_bloc: ^8.1.3

dev_dependencies:
  # Code Generation
  build_runner: ^2.4.6
  ferry_generator: ^0.10.0
  gql_code_builder: ^0.7.0
```

### graphql/schema.graphql

```graphql
type Query {
  products(limit: Int, offset: Int): [Product!]!
  product(id: ID!): Product
  searchProducts(query: String!): [Product!]!
}

type Mutation {
  createProduct(input: CreateProductInput!): Product!
  updateProduct(id: ID!, input: UpdateProductInput!): Product!
  deleteProduct(id: ID!): Boolean!
}

type Subscription {
  productUpdated(id: ID!): Product!
  productCreated: Product!
}

type Product {
  id: ID!
  name: String!
  description: String!
  price: Float!
  imageUrl: String!
  stock: Int!
  createdAt: String!
  updatedAt: String!
}

input CreateProductInput {
  name: String!
  description: String!
  price: Float!
  imageUrl: String!
  stock: Int!
}

input UpdateProductInput {
  name: String
  description: String
  price: Float
  imageUrl: String
  stock: Int
}
```

## 💻 Implementación

### 1. GraphQL Client Configuration

```dart
// lib/core/graphql/graphql_config.dart
import 'package:graphql_flutter/graphql_flutter.dart';

class GraphQLConfig {
  static const String _endpoint = 'https://api.example.com/graphql';
  static const String _wsEndpoint = 'wss://api.example.com/graphql';

  static HttpLink get httpLink => HttpLink(_endpoint);

  static WebSocketLink get websocketLink => WebSocketLink(
        _wsEndpoint,
        config: const SocketClientConfig(
          autoReconnect: true,
          inactivityTimeout: Duration(seconds: 30),
        ),
      );

  static AuthLink get authLink => AuthLink(
        getToken: () async {
          // Obtener token de autenticación
          // final token = await SecureStorage.getToken();
          return 'Bearer YOUR_TOKEN';
        },
      );

  static Link get link {
    final Link httpLinkWithAuth = authLink.concat(httpLink);

    // Combinar HTTP y WebSocket links
    return Link.split(
      (request) => request.isSubscription,
      websocketLink,
      httpLinkWithAuth,
    );
  }

  static GraphQLClient getClient() {
    return GraphQLClient(
      link: link,
      cache: GraphQLCache(
        store: HiveStore(),
      ),
      defaultPolicies: DefaultPolicies(
        query: Policies(
          fetch: FetchPolicy.cacheFirst,
          error: ErrorPolicy.all,
          cacheReread: CacheRereadPolicy.mergeOptimistic,
        ),
        mutate: Policies(
          fetch: FetchPolicy.networkOnly,
          error: ErrorPolicy.all,
        ),
        subscribe: Policies(
          fetch: FetchPolicy.networkOnly,
          error: ErrorPolicy.all,
        ),
      ),
    );
  }
}
```

### 2. GraphQL Queries

```graphql
# graphql/queries/get_products.graphql
query GetProducts($limit: Int, $offset: Int) {
  products(limit: $limit, offset: $offset) {
    id
    name
    description
    price
    imageUrl
    stock
    createdAt
    updatedAt
  }
}
```

```graphql
# graphql/queries/get_product.graphql
query GetProduct($id: ID!) {
  product(id: $id) {
    id
    name
    description
    price
    imageUrl
    stock
    createdAt
    updatedAt
  }
}
```

```graphql
# graphql/queries/search_products.graphql
query SearchProducts($query: String!) {
  searchProducts(query: $query) {
    id
    name
    description
    price
    imageUrl
    stock
  }
}
```

### 3. GraphQL Mutations

```graphql
# graphql/mutations/create_product.graphql
mutation CreateProduct($input: CreateProductInput!) {
  createProduct(input: $input) {
    id
    name
    description
    price
    imageUrl
    stock
    createdAt
    updatedAt
  }
}
```

```graphql
# graphql/mutations/update_product.graphql
mutation UpdateProduct($id: ID!, $input: UpdateProductInput!) {
  updateProduct(id: $id, input: $input) {
    id
    name
    description
    price
    imageUrl
    stock
    updatedAt
  }
}
```

```graphql
# graphql/mutations/delete_product.graphql
mutation DeleteProduct($id: ID!) {
  deleteProduct(id: $id)
}
```

### 4. GraphQL Subscriptions

```graphql
# graphql/subscriptions/product_updated.graphql
subscription ProductUpdated($id: ID!) {
  productUpdated(id: $id) {
    id
    name
    description
    price
    imageUrl
    stock
    updatedAt
  }
}
```

```graphql
# graphql/subscriptions/product_created.graphql
subscription ProductCreated {
  productCreated {
    id
    name
    description
    price
    imageUrl
    stock
    createdAt
  }
}
```

### 5. DataSource Implementation

```dart
// lib/features/products/data/datasources/products_graphql_datasource.dart
import 'package:graphql_flutter/graphql_flutter.dart';
import '../models/product_model.dart';

abstract class ProductsGraphQLDataSource {
  Future<List<ProductModel>> getProducts({int? limit, int? offset});
  Future<ProductModel> getProduct(String id);
  Future<List<ProductModel>> searchProducts(String query);
  Future<ProductModel> createProduct(ProductModel product);
  Future<ProductModel> updateProduct(ProductModel product);
  Future<bool> deleteProduct(String id);
  Stream<ProductModel> subscribeToProductUpdates(String id);
}

class ProductsGraphQLDataSourceImpl implements ProductsGraphQLDataSource {
  final GraphQLClient client;

  ProductsGraphQLDataSourceImpl(this.client);

  static const String _getProductsQuery = r'''
    query GetProducts($limit: Int, $offset: Int) {
      products(limit: $limit, offset: $offset) {
        id
        name
        description
        price
        imageUrl
        stock
        createdAt
        updatedAt
      }
    }
  ''';

  static const String _getProductQuery = r'''
    query GetProduct($id: ID!) {
      product(id: $id) {
        id
        name
        description
        price
        imageUrl
        stock
        createdAt
        updatedAt
      }
    }
  ''';

  static const String _searchProductsQuery = r'''
    query SearchProducts($query: String!) {
      searchProducts(query: $query) {
        id
        name
        description
        price
        imageUrl
        stock
      }
    }
  ''';

  static const String _createProductMutation = r'''
    mutation CreateProduct($input: CreateProductInput!) {
      createProduct(input: $input) {
        id
        name
        description
        price
        imageUrl
        stock
        createdAt
        updatedAt
      }
    }
  ''';

  static const String _updateProductMutation = r'''
    mutation UpdateProduct($id: ID!, $input: UpdateProductInput!) {
      updateProduct(id: $id, input: $input) {
        id
        name
        description
        price
        imageUrl
        stock
        updatedAt
      }
    }
  ''';

  static const String _deleteProductMutation = r'''
    mutation DeleteProduct($id: ID!) {
      deleteProduct(id: $id)
    }
  ''';

  static const String _productUpdatedSubscription = r'''
    subscription ProductUpdated($id: ID!) {
      productUpdated(id: $id) {
        id
        name
        description
        price
        imageUrl
        stock
        updatedAt
      }
    }
  ''';

  @override
  Future<List<ProductModel>> getProducts({int? limit, int? offset}) async {
    final result = await client.query(
      QueryOptions(
        document: gql(_getProductsQuery),
        variables: {
          'limit': limit,
          'offset': offset,
        },
        fetchPolicy: FetchPolicy.cacheFirst,
      ),
    );

    if (result.hasException) {
      throw Exception(result.exception.toString());
    }

    final List<dynamic> productsJson = result.data?['products'] ?? [];
    return productsJson
        .map((json) => ProductModel.fromJson(json))
        .toList();
  }

  @override
  Future<ProductModel> getProduct(String id) async {
    final result = await client.query(
      QueryOptions(
        document: gql(_getProductQuery),
        variables: {'id': id},
        fetchPolicy: FetchPolicy.cacheFirst,
      ),
    );

    if (result.hasException) {
      throw Exception(result.exception.toString());
    }

    final productJson = result.data?['product'];
    if (productJson == null) {
      throw Exception('Product not found');
    }

    return ProductModel.fromJson(productJson);
  }

  @override
  Future<List<ProductModel>> searchProducts(String query) async {
    final result = await client.query(
      QueryOptions(
        document: gql(_searchProductsQuery),
        variables: {'query': query},
        fetchPolicy: FetchPolicy.networkOnly,
      ),
    );

    if (result.hasException) {
      throw Exception(result.exception.toString());
    }

    final List<dynamic> productsJson = result.data?['searchProducts'] ?? [];
    return productsJson
        .map((json) => ProductModel.fromJson(json))
        .toList();
  }

  @override
  Future<ProductModel> createProduct(ProductModel product) async {
    final result = await client.mutate(
      MutationOptions(
        document: gql(_createProductMutation),
        variables: {
          'input': {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'imageUrl': product.imageUrl,
            'stock': product.stock,
          },
        },
        // Optimistic response
        optimisticResult: {
          'createProduct': product.toJson(),
        },
      ),
    );

    if (result.hasException) {
      throw Exception(result.exception.toString());
    }

    return ProductModel.fromJson(result.data?['createProduct']);
  }

  @override
  Future<ProductModel> updateProduct(ProductModel product) async {
    final result = await client.mutate(
      MutationOptions(
        document: gql(_updateProductMutation),
        variables: {
          'id': product.id,
          'input': {
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'imageUrl': product.imageUrl,
            'stock': product.stock,
          },
        },
        optimisticResult: {
          'updateProduct': product.toJson(),
        },
      ),
    );

    if (result.hasException) {
      throw Exception(result.exception.toString());
    }

    return ProductModel.fromJson(result.data?['updateProduct']);
  }

  @override
  Future<bool> deleteProduct(String id) async {
    final result = await client.mutate(
      MutationOptions(
        document: gql(_deleteProductMutation),
        variables: {'id': id},
      ),
    );

    if (result.hasException) {
      throw Exception(result.exception.toString());
    }

    return result.data?['deleteProduct'] ?? false;
  }

  @override
  Stream<ProductModel> subscribeToProductUpdates(String id) {
    final subscription = client.subscribe(
      SubscriptionOptions(
        document: gql(_productUpdatedSubscription),
        variables: {'id': id},
      ),
    );

    return subscription.map((result) {
      if (result.hasException) {
        throw Exception(result.exception.toString());
      }

      return ProductModel.fromJson(result.data?['productUpdated']);
    });
  }
}
```

### 6. Usage in Widgets

```dart
// lib/features/products/presentation/screens/products_screen.dart
import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

class ProductsScreen extends StatelessWidget {
  const ProductsScreen({super.key});

  static const String _getProductsQuery = r'''
    query GetProducts($limit: Int, $offset: Int) {
      products(limit: $limit, offset: $offset) {
        id
        name
        description
        price
        imageUrl
        stock
      }
    }
  ''';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Products'),
      ),
      body: Query(
        options: QueryOptions(
          document: gql(_getProductsQuery),
          variables: const {
            'limit': 20,
            'offset': 0,
          },
          fetchPolicy: FetchPolicy.cacheAndNetwork,
          pollInterval: const Duration(seconds: 30),
        ),
        builder: (result, {fetchMore, refetch}) {
          // Loading state
          if (result.isLoading && result.data == null) {
            return const Center(child: CircularProgressIndicator());
          }

          // Error state
          if (result.hasException) {
            return Center(
              child: Text('Error: ${result.exception.toString()}'),
            );
          }

          // Success state
          final products = result.data?['products'] as List<dynamic>? ?? [];

          return RefreshIndicator(
            onRefresh: () async {
              await refetch?.call();
            },
            child: ListView.builder(
              itemCount: products.length,
              itemBuilder: (context, index) {
                final product = products[index];
                return ProductCard(
                  id: product['id'],
                  name: product['name'],
                  price: product['price'],
                  imageUrl: product['imageUrl'],
                );
              },
            ),
          );
        },
      ),
    );
  }
}
```

```dart
// Mutation Example
class CreateProductButton extends StatelessWidget {
  final ProductModel product;

  const CreateProductButton({required this.product});

  static const String _createProductMutation = r'''
    mutation CreateProduct($input: CreateProductInput!) {
      createProduct(input: $input) {
        id
        name
        price
      }
    }
  ''';

  @override
  Widget build(BuildContext context) {
    return Mutation(
      options: MutationOptions(
        document: gql(_createProductMutation),
        onCompleted: (dynamic resultData) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Product created!')),
          );
        },
        onError: (error) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error: $error')),
          );
        },
      ),
      builder: (runMutation, result) {
        return ElevatedButton(
          onPressed: result?.isLoading ?? false
              ? null
              : () {
                  runMutation({
                    'input': {
                      'name': product.name,
                      'description': product.description,
                      'price': product.price,
                      'imageUrl': product.imageUrl,
                      'stock': product.stock,
                    },
                  });
                },
          child: result?.isLoading ?? false
              ? const CircularProgressIndicator()
              : const Text('Create Product'),
        );
      },
    );
  }
}
```

```dart
// Subscription Example
class ProductDetailScreen extends StatelessWidget {
  final String productId;

  const ProductDetailScreen({required this.productId});

  static const String _productUpdatedSubscription = r'''
    subscription ProductUpdated($id: ID!) {
      productUpdated(id: $id) {
        id
        name
        price
        stock
        updatedAt
      }
    }
  ''';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Product Detail')),
      body: Subscription(
        options: SubscriptionOptions(
          document: gql(_productUpdatedSubscription),
          variables: {'id': productId},
        ),
        builder: (result) {
          if (result.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (result.hasException) {
            return Center(child: Text('Error: ${result.exception}'));
          }

          final product = result.data?['productUpdated'];
          if (product == null) {
            return const Center(child: Text('No data'));
          }

          return Column(
            children: [
              Text('Name: ${product['name']}'),
              Text('Price: \$${product['price']}'),
              Text('Stock: ${product['stock']}'),
              Text('Updated: ${product['updatedAt']}'),
            ],
          );
        },
      ),
    );
  }
}
```

## 🎯 Mejores Prácticas

### 1. Fragment Reusability

```graphql
fragment ProductFields on Product {
  id
  name
  description
  price
  imageUrl
  stock
}

query GetProducts {
  products {
    ...ProductFields
  }
}
```

### 2. Optimistic Updates

```dart
optimisticResult: {
  'createProduct': {
    '__typename': 'Product',
    'id': 'temp-id',
    ...product.toJson(),
  },
}
```

### 3. Error Handling

```dart
if (result.hasException) {
  final exception = result.exception;
  if (exception?.graphqlErrors != null) {
    // Handle GraphQL errors
  }
  if (exception?.linkException != null) {
    // Handle network errors
  }
}
```

## 📚 Recursos Adicionales

- [GraphQL Flutter](https://pub.dev/packages/graphql_flutter)
- [GraphQL Official](https://graphql.org/)
- [Ferry Code Generator](https://ferrygraphql.com/)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md)
- [Offline-First](../offline-first/SKILL.md)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
