---
name: "Model Patterns"
description: "Entity and model patterns with JSON serialization, immutability, and equality"
version: "1.0.0"
---

# Model Patterns

## Entity (Domain Layer)

```dart
// lib/domain/entities/user.dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String name;
  final String email;
  final DateTime createdAt;
  final DateTime? updatedAt;
  
  const User({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
    this.updatedAt,
  });
  
  @override
  List<Object?> get props => [id, name, email, createdAt, updatedAt];
  
  User copyWith({
    String? name,
    String? email,
    DateTime? updatedAt,
  }) {
    return User(
      id: id,
      name: name ?? this.name,
      email: email ?? this.email,
      createdAt: createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
```

## Model (Data Layer)

### Basic Model with JSON Serialization

```dart
// lib/data/models/user_model.dart
import '../../domain/entities/user.dart';

class UserModel extends User {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
    required super.createdAt,
    super.updatedAt,
  });
  
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'] as String)
          : null,
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'created_at': createdAt.toIso8601String(),
      if (updatedAt != null) 'updated_at': updatedAt!.toIso8601String(),
    };
  }
  
  User toEntity() {
    return User(
      id: id,
      name: name,
      email: email,
      createdAt: createdAt,
      updatedAt: updatedAt,
    );
  }
  
  factory UserModel.fromEntity(User entity) {
    return UserModel(
      id: entity.id,
      name: entity.name,
      email: entity.email,
      createdAt: entity.createdAt,
      updatedAt: entity.updatedAt,
    );
  }
}
```

### Model with Nested Objects

```dart
class OrderModel extends Order {
  final List<OrderItemModel> itemModels;
  
  const OrderModel({
    required super.id,
    required super.userId,
    required super.total,
    required this.itemModels,
  }) : super(items: itemModels);
  
  factory OrderModel.fromJson(Map<String, dynamic> json) {
    return OrderModel(
      id: json['id'],
      userId: json['user_id'],
      total: json['total'].toDouble(),
      itemModels: (json['items'] as List)
          .map((item) => OrderItemModel.fromJson(item))
          .toList(),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'user_id': userId,
      'total': total,
      'items': itemModels.map((item) => item.toJson()).toList(),
    };
  }
}
```

### Model with Enum

```dart
enum UserRole { admin, user, guest }

extension UserRoleX on UserRole {
  String toJson() => name;
  
  static UserRole fromJson(String json) {
    return UserRole.values.firstWhere(
      (role) => role.name == json,
      orElse: () => UserRole.guest,
    );
  }
}

class UserModel extends User {
  final UserRole roleValue;
  
  const UserModel({
    required super.id,
    required super.name,
    required this.roleValue,
  }) : super(role: roleValue);
  
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      roleValue: UserRoleX.fromJson(json['role']),
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'role': roleValue.toJson(),
    };
  }
}
```

## Immutability Patterns

### Using Freezed (Recommended)

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

@freezed
class UserModel with _$UserModel {
  const factory UserModel({
    required String id,
    required String name,
    required String email,
    DateTime? updatedAt,
  }) = _UserModel;
  
  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
}
```

### Manual Immutability

```dart
class UserModel {
  final String id;
  final String name;
  final String email;
  
  const UserModel({
    required this.id,
    required this.name,
    required this.email,
  });
  
  UserModel copyWith({
    String? name,
    String? email,
  }) {
    return UserModel(
      id: id,
      name: name ?? this.name,
      email: email ?? this.email,
    );
  }
}
```

## Equality Patterns

### Using Equatable

```dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String name;
  
  const User({required this.id, required this.name});
  
  @override
  List<Object?> get props => [id, name];
}
```

### Manual Equality

```dart
class User {
  final String id;
  final String name;
  
  const User({required this.id, required this.name});
  
  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User && other.id == id && other.name == name;
  }
  
  @override
  int get hashCode => id.hashCode ^ name.hashCode;
}
```
