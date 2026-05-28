---
name: field-consistency-check
description: 检查前后端字段名一致性。自动比较后端 Entity 与前端 Interface 的所有字段，发现缺失或不一致的字段。使用此 Skill 确保数据模型统一。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# 字段一致性检查 Skill

## Entity/Interface 映射表

| 后端 Entity | 前端文件 | Interface 名 |
|-------------|---------|-------------|
| Customer | customerApiClient.ts | Customer |
| Supplier | supplierApiClient.ts | Supplier |
| User | userApiClient.ts | UserDTO |
| Factory | platformApiClient.ts | FactoryDTO |
| FactoryEquipment | equipmentApiClient.ts | Equipment |
| MaterialBatch | materialBatchApiClient.ts | MaterialBatch |
| RawMaterialType | materialTypeApiClient.ts | MaterialType |
| ProductType | productTypeApiClient.ts | ProductType |
| QualityInspection | qualityInspectionApiClient.ts | QualityInspection |
| ShipmentRecord | shipmentApiClient.ts | ShipmentRecord |
| DisposalRecord | disposalRecordApiClient.ts | DisposalRecord |

## 快速检查命令

```bash
cd /Users/jietaoxie/my-prototype-logistics

# 提取后端字段
grep -E "private (String|Long|Boolean|Integer|BigDecimal|LocalDateTime)" \
  backend-java/src/main/java/com/cretas/aims/entity/Customer.java | \
  grep -v "//" | awk '{print $3}' | sed 's/;//' | sort

# 提取前端字段
awk '/export interface Customer \{/,/^\}/' \
  frontend/CretasFoodTrace/src/services/api/customerApiClient.ts | \
  grep -E "^\s+\w+[\?:]" | awk '{print $1}' | sed 's/[?:]//' | sort

# 对比差异
comm -23 /tmp/be.txt /tmp/fe.txt  # 只在后端
comm -13 /tmp/be.txt /tmp/fe.txt  # 只在前端
```

## 字段命名差异表

| Entity | 电话字段 | 地址字段 |
|--------|---------|---------|
| Factory | contactPhone | address |
| Supplier | contactPhone + phone | address |
| Customer | contactPhone + phone | shippingAddress + billingAddress |
| User | phone | - |

## 修复流程

1. 查看后端字段: `grep -E "private" entity/XXX.java`
2. 更新前端 Interface 与后端一致
3. 编译检查: `npx tsc --noEmit --skipLibCheck`

## 相关路径

- 后端 Entity: `backend-java/src/main/java/com/cretas/aims/entity/`
- 前端 API: `frontend/CretasFoodTrace/src/services/api/`
