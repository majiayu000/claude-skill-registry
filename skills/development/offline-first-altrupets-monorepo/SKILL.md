# 📴 Skill: Offline-First Architecture

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-offline-first` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `offline-first`, `cache`, `sync`, `local-storage`, `connectivity` |
| **Referencia** | [Offline-First Apps](https://developer.android.com/topic/architecture/data-layer/offline-first) |

## 🔑 Keywords para Invocación

- `offline-first`
- `offline`
- `cache`
- `sync`
- `local-storage`
- `connectivity`
- `@skill:offline-first`

### Ejemplos de Prompts

```
Implementa arquitectura offline-first con sincronización
```

```
Crea una app que funcione sin conexión
```

```
@skill:offline-first - Agrega soporte offline completo
```

## 📖 Descripción

Offline-First Architecture prioriza el almacenamiento y acceso local de datos, permitiendo que la app funcione sin conexión a internet. Implementa cache inteligente, sincronización bidireccional, detección de conectividad y resolución de conflictos.

### ✅ Cuándo Usar Este Skill

- App que debe funcionar sin internet
- Conectividad intermitente o lenta
- Necesitas performance ultra-rápida
- Sincronización de datos bidireccional
- Apps para zonas rurales o en movimiento
- Reducir consumo de datos móviles

### ❌ Cuándo NO Usar Este Skill

- App requiere datos en tiempo real constante
- No hay necesidad de funcionar offline
- Datos altamente sensibles que no deben cachearse

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── network/
│   │   ├── connectivity_service.dart
│   │   ├── network_info.dart
│   │   └── dio_client.dart
│   ├── storage/
│   │   ├── local_storage.dart
│   │   ├── cache_manager.dart
│   │   └── secure_storage.dart
│   ├── sync/
│   │   ├── sync_service.dart
│   │   ├── sync_queue.dart
│   │   └── conflict_resolver.dart
│   └── error/
│       └── failures.dart
│
├── features/
│   └── products/
│       ├── data/
│       │   ├── datasources/
│       │   │   ├── products_local_datasource.dart
│       │   │   └── products_remote_datasource.dart
│       │   ├── models/
│       │   │   ├── product_model.dart
│       │   │   └── sync_item_model.dart
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
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Local Database
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  sqflite: ^2.3.0
  path: ^1.8.3

  # Networking
  dio: ^5.4.0
  connectivity_plus: ^5.0.2

  # Utils
  dartz: ^0.10.1
  equatable: ^2.0.5
  uuid: ^4.2.2

  # State Management
  flutter_bloc: ^8.1.3

dev_dependencies:
  hive_generator: ^2.0.1
  build_runner: ^2.4.6
```

## 💻 Implementación

### 1. Connectivity Service

```dart
// lib/core/network/connectivity_service.dart
import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:dio/dio.dart';

enum ConnectivityStatus {
  online,
  offline,
  unknown,
}

class ConnectivityService {
  final Connectivity _connectivity = Connectivity();
  final Dio _dio;

  late StreamController<ConnectivityStatus> _statusController;
  Stream<ConnectivityStatus> get statusStream => _statusController.stream;

  ConnectivityStatus _currentStatus = ConnectivityStatus.unknown;
  ConnectivityStatus get currentStatus => _currentStatus;

  ConnectivityService(this._dio) {
    _statusController = StreamController<ConnectivityStatus>.broadcast();
    _init();
  }

  void _init() {
    // Verificar conectividad inicial
    _checkConnectivity();

    // Escuchar cambios de conectividad
    _connectivity.onConnectivityChanged.listen((result) {
      _checkConnectivity();
    });
  }

  Future<void> _checkConnectivity() async {
    try {
      final connectivityResult = await _connectivity.checkConnectivity();

      if (connectivityResult == ConnectivityResult.none) {
        _updateStatus(ConnectivityStatus.offline);
        return;
      }

      // Verificar conectividad real con ping al servidor
      final hasInternet = await _pingServer();
      _updateStatus(
        hasInternet ? ConnectivityStatus.online : ConnectivityStatus.offline,
      );
    } catch (e) {
      _updateStatus(ConnectivityStatus.offline);
    }
  }

  Future<bool> _pingServer() async {
    try {
      final response = await _dio.get(
        '/ping',
        options: Options(
          receiveTimeout: const Duration(seconds: 3),
          sendTimeout: const Duration(seconds: 3),
        ),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  void _updateStatus(ConnectivityStatus status) {
    if (_currentStatus != status) {
      _currentStatus = status;
      _statusController.add(status);
    }
  }

  void dispose() {
    _statusController.close();
  }
}
```

### 2. Local Storage con Hive

```dart
// lib/core/storage/local_storage.dart
import 'package:hive_flutter/hive_flutter.dart';

class LocalStorage {
  static const String _productsBox = 'products';
  static const String _syncQueueBox = 'sync_queue';
  static const String _metadataBox = 'metadata';

  static Future<void> init() async {
    await Hive.initFlutter();

    // Registrar adapters
    // Hive.registerAdapter(ProductModelAdapter());
    // Hive.registerAdapter(SyncItemAdapter());

    // Abrir boxes
    await Hive.openBox(_productsBox);
    await Hive.openBox(_syncQueueBox);
    await Hive.openBox(_metadataBox);
  }

  static Box get productsBox => Hive.box(_productsBox);
  static Box get syncQueueBox => Hive.box(_syncQueueBox);
  static Box get metadataBox => Hive.box(_metadataBox);

  static Future<void> clearAll() async {
    await productsBox.clear();
    await syncQueueBox.clear();
    await metadataBox.clear();
  }
}
```

### 3. Sync Queue

```dart
// lib/core/sync/sync_item_model.dart
import 'package:hive/hive.dart';
import 'package:uuid/uuid.dart';

part 'sync_item_model.g.dart';

enum SyncAction {
  create,
  update,
  delete,
}

@HiveType(typeId: 1)
class SyncItem extends HiveObject {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String entityId;

  @HiveField(2)
  final String entityType;

  @HiveField(3)
  final SyncAction action;

  @HiveField(4)
  final Map<String, dynamic> data;

  @HiveField(5)
  final DateTime createdAt;

  @HiveField(6)
  int retryCount;

  @HiveField(7)
  bool isSyncing;

  SyncItem({
    String? id,
    required this.entityId,
    required this.entityType,
    required this.action,
    required this.data,
    DateTime? createdAt,
    this.retryCount = 0,
    this.isSyncing = false,
  })  : id = id ?? const Uuid().v4(),
        createdAt = createdAt ?? DateTime.now();
}
```

```dart
// lib/core/sync/sync_service.dart
import 'dart:async';
import 'package:dio/dio.dart';
import '../storage/local_storage.dart';
import '../network/connectivity_service.dart';
import 'sync_item_model.dart';

class SyncService {
  final Dio _dio;
  final ConnectivityService _connectivityService;
  Timer? _syncTimer;
  bool _isSyncing = false;

  SyncService(this._dio, this._connectivityService) {
    _init();
  }

  void _init() {
    // Escuchar cambios de conectividad
    _connectivityService.statusStream.listen((status) {
      if (status == ConnectivityStatus.online && !_isSyncing) {
        syncPendingItems();
      }
    });

    // Sincronización periódica cada 5 minutos
    _syncTimer = Timer.periodic(
      const Duration(minutes: 5),
      (_) => syncPendingItems(),
    );
  }

  Future<void> addToQueue(SyncItem item) async {
    final box = LocalStorage.syncQueueBox;
    await box.add(item);

    // Intentar sincronizar inmediatamente si hay conexión
    if (_connectivityService.currentStatus == ConnectivityStatus.online) {
      syncPendingItems();
    }
  }

  Future<void> syncPendingItems() async {
    if (_isSyncing) return;
    if (_connectivityService.currentStatus != ConnectivityStatus.online) return;

    _isSyncing = true;

    try {
      final box = LocalStorage.syncQueueBox;
      final items = box.values.cast<SyncItem>().where((item) => !item.isSyncing).toList();

      for (final item in items) {
        try {
          // Marcar como sincronizando
          item.isSyncing = true;
          await item.save();

          // Realizar sincronización
          await _syncItem(item);

          // Eliminar del queue si fue exitoso
          await item.delete();
        } catch (e) {
          // Incrementar retry count
          item.retryCount++;
          item.isSyncing = false;
          await item.save();

          // Si falló muchas veces, remover (o manejar de otra forma)
          if (item.retryCount > 5) {
            await item.delete();
            // Log error o notificar al usuario
          }
        }
      }
    } finally {
      _isSyncing = false;
    }
  }

  Future<void> _syncItem(SyncItem item) async {
    switch (item.action) {
      case SyncAction.create:
        await _dio.post(
          '/${item.entityType}',
          data: item.data,
        );
        break;

      case SyncAction.update:
        await _dio.put(
          '/${item.entityType}/${item.entityId}',
          data: item.data,
        );
        break;

      case SyncAction.delete:
        await _dio.delete('/${item.entityType}/${item.entityId}');
        break;
    }
  }

  void dispose() {
    _syncTimer?.cancel();
  }
}
```

### 4. Repository Implementation (Offline-First)

```dart
// lib/features/products/data/repositories/products_repository_impl.dart
import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../../../../core/network/connectivity_service.dart';
import '../../../../core/sync/sync_service.dart';
import '../../../../core/sync/sync_item_model.dart';
import '../../domain/entities/product.dart';
import '../../domain/repositories/products_repository.dart';
import '../datasources/products_local_datasource.dart';
import '../datasources/products_remote_datasource.dart';
import '../models/product_model.dart';

class ProductsRepositoryImpl implements ProductsRepository {
  final ProductsLocalDataSource localDataSource;
  final ProductsRemoteDataSource remoteDataSource;
  final ConnectivityService connectivityService;
  final SyncService syncService;

  ProductsRepositoryImpl({
    required this.localDataSource,
    required this.remoteDataSource,
    required this.connectivityService,
    required this.syncService,
  });

  @override
  Future<Either<Failure, List<Product>>> getProducts() async {
    try {
      // 1. Siempre devolver datos del cache primero (Offline-First)
      final localProducts = await localDataSource.getProducts();

      // 2. Si hay conexión, actualizar en background
      if (connectivityService.currentStatus == ConnectivityStatus.online) {
        _refreshProductsInBackground();
      }

      // 3. Devolver datos locales inmediatamente
      return Right(localProducts.map((model) => model.toEntity()).toList());
    } catch (e) {
      return Left(CacheFailure());
    }
  }

  Future<void> _refreshProductsInBackground() async {
    try {
      final remoteProducts = await remoteDataSource.getProducts();
      await localDataSource.cacheProducts(remoteProducts);
    } catch (e) {
      // Silenciosamente fallar, ya devolvimos datos del cache
    }
  }

  @override
  Future<Either<Failure, Product>> getProduct(String id) async {
    try {
      // Intentar obtener del cache primero
      final localProduct = await localDataSource.getProduct(id);

      if (localProduct != null) {
        // Actualizar en background si hay conexión
        if (connectivityService.currentStatus == ConnectivityStatus.online) {
          _refreshProductInBackground(id);
        }
        return Right(localProduct.toEntity());
      }

      // Si no existe localmente y hay conexión, obtener del servidor
      if (connectivityService.currentStatus == ConnectivityStatus.online) {
        final remoteProduct = await remoteDataSource.getProduct(id);
        await localDataSource.cacheProduct(remoteProduct);
        return Right(remoteProduct.toEntity());
      }

      return Left(CacheFailure());
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  Future<void> _refreshProductInBackground(String id) async {
    try {
      final remoteProduct = await remoteDataSource.getProduct(id);
      await localDataSource.cacheProduct(remoteProduct);
    } catch (e) {
      // Silenciosamente fallar
    }
  }

  @override
  Future<Either<Failure, Product>> createProduct(Product product) async {
    try {
      final productModel = ProductModel.fromEntity(product);

      // 1. Guardar localmente primero
      await localDataSource.cacheProduct(productModel);

      // 2. Si hay conexión, sincronizar inmediatamente
      if (connectivityService.currentStatus == ConnectivityStatus.online) {
        try {
          final remoteProduct = await remoteDataSource.createProduct(productModel);
          await localDataSource.cacheProduct(remoteProduct);
          return Right(remoteProduct.toEntity());
        } catch (e) {
          // Si falla, agregar a queue de sincronización
          await _addToSyncQueue(product, SyncAction.create);
          return Right(product);
        }
      } else {
        // 3. Sin conexión, agregar a queue
        await _addToSyncQueue(product, SyncAction.create);
        return Right(product);
      }
    } catch (e) {
      return Left(CacheFailure());
    }
  }

  @override
  Future<Either<Failure, Product>> updateProduct(Product product) async {
    try {
      final productModel = ProductModel.fromEntity(product);

      // Actualizar localmente
      await localDataSource.cacheProduct(productModel);

      // Sincronizar si hay conexión o agregar a queue
      if (connectivityService.currentStatus == ConnectivityStatus.online) {
        try {
          final remoteProduct = await remoteDataSource.updateProduct(productModel);
          await localDataSource.cacheProduct(remoteProduct);
          return Right(remoteProduct.toEntity());
        } catch (e) {
          await _addToSyncQueue(product, SyncAction.update);
          return Right(product);
        }
      } else {
        await _addToSyncQueue(product, SyncAction.update);
        return Right(product);
      }
    } catch (e) {
      return Left(CacheFailure());
    }
  }

  @override
  Future<Either<Failure, void>> deleteProduct(String id) async {
    try {
      // Eliminar localmente
      await localDataSource.deleteProduct(id);

      // Sincronizar o agregar a queue
      if (connectivityService.currentStatus == ConnectivityStatus.online) {
        try {
          await remoteDataSource.deleteProduct(id);
        } catch (e) {
          await _addDeleteToSyncQueue(id);
        }
      } else {
        await _addDeleteToSyncQueue(id);
      }

      return const Right(null);
    } catch (e) {
      return Left(CacheFailure());
    }
  }

  Future<void> _addToSyncQueue(Product product, SyncAction action) async {
    final syncItem = SyncItem(
      entityId: product.id,
      entityType: 'products',
      action: action,
      data: ProductModel.fromEntity(product).toJson(),
    );

    await syncService.addToQueue(syncItem);
  }

  Future<void> _addDeleteToSyncQueue(String id) async {
    final syncItem = SyncItem(
      entityId: id,
      entityType: 'products',
      action: SyncAction.delete,
      data: {},
    );

    await syncService.addToQueue(syncItem);
  }
}
```

### 5. Connectivity Indicator Widget

```dart
// lib/core/widgets/connectivity_indicator.dart
import 'package:flutter/material.dart';
import '../network/connectivity_service.dart';

class ConnectivityIndicator extends StatelessWidget {
  final ConnectivityService connectivityService;

  const ConnectivityIndicator({
    super.key,
    required this.connectivityService,
  });

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<ConnectivityStatus>(
      stream: connectivityService.statusStream,
      initialData: connectivityService.currentStatus,
      builder: (context, snapshot) {
        final status = snapshot.data ?? ConnectivityStatus.unknown;

        if (status == ConnectivityStatus.online) {
          return const SizedBox.shrink();
        }

        return Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
          color: status == ConnectivityStatus.offline
              ? Colors.red.shade700
              : Colors.orange.shade700,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                status == ConnectivityStatus.offline
                    ? Icons.cloud_off
                    : Icons.cloud_queue,
                color: Colors.white,
                size: 16,
              ),
              const SizedBox(width: 8),
              Text(
                status == ConnectivityStatus.offline
                    ? 'Offline Mode - Changes will sync when online'
                    : 'Checking connection...',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 12,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

// Uso
Scaffold(
  appBar: AppBar(
    title: const Text('Products'),
  ),
  body: Column(
    children: [
      ConnectivityIndicator(connectivityService: getIt<ConnectivityService>()),
      Expanded(
        child: ProductsList(),
      ),
    ],
  ),
)
```

## 🎯 Mejores Prácticas

### 1. Cache-First Strategy

✅ **DO:**
```dart
// Devolver datos del cache inmediatamente
final localData = await localDataSource.getData();
// Actualizar en background
_refreshDataInBackground();
return localData;
```

### 2. Optimistic Updates

✅ **DO:**
```dart
// Actualizar UI inmediatamente
await localDataSource.save(data);
emit(DataSaved(data));

// Sincronizar en background
_syncToServer(data);
```

### 3. Conflict Resolution

✅ **DO:**
```dart
if (localVersion != remoteVersion) {
  // Last-write-wins
  if (local.updatedAt.isAfter(remote.updatedAt)) {
    await remoteDataSource.update(local);
  } else {
    await localDataSource.update(remote);
  }
}
```

## 📚 Recursos Adicionales

- [Offline-First Architecture](https://developer.android.com/topic/architecture/data-layer/offline-first)
- [Hive Database](https://docs.hivedb.dev/)
- [Connectivity Plus](https://pub.dev/packages/connectivity_plus)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md)
- [Testing Strategy](../testing/SKILL.md)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
