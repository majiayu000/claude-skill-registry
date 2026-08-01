---
name: disaster-recovery-business-continuity
description: '| ID | sre-disaster-recovery-business-continuity |'
---

# 🆘 Skill: Disaster Recovery & Business Continuity

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-disaster-recovery-business-continuity` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `disaster-recovery`, `business-continuity`, `backup`, `failover`, `rpo`, `rto`, `dr-plan` |
| **Referencia** | [AWS Disaster Recovery](https://aws.amazon.com/disaster-recovery/) |

## 🔑 Keywords para Invocación

- `disaster-recovery`
- `business-continuity`
- `backup-strategy`
- `failover`
- `rpo`
- `rto`
- `dr-plan`
- `@skill:disaster-recovery`

### Ejemplos de Prompts

```
Implementa disaster recovery plan con RPO y RTO
```

```
Configura backup strategy y failover procedures
```

```
Setup business continuity plan para servicios críticos
```

```
@skill:disaster-recovery - Plan completo de DR y BC
```

## 📖 Descripción

Disaster Recovery (DR) y Business Continuity (BC) aseguran que servicios críticos puedan recuperarse rápidamente de desastres. Este skill cubre DR planning, backup strategies, failover procedures, RPO/RTO definitions, y testing procedures.

### ✅ Cuándo Usar Este Skill

- Servicios críticos en producción
- SLAs estrictos
- Compliance requirements
- Data protection requirements
- High availability requirements

### ❌ Cuándo NO Usar Este Skill

- Servicios no críticos
- Desarrollo local
- Prototipos sin datos reales

## 🏗️ DR Strategy Framework

```
RPO (Recovery Point Objective)
    ↓
Backup Frequency
    ↓
RTO (Recovery Time Objective)
    ↓
Failover Procedures
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - [`backup-strategy.sh`](scripts/backup-strategy.sh) - Estrategia automatizada de backups (Bash)
> - [`failover_procedures.py`](scripts/failover_procedures.py) - Gestor de procedimientos de failover (Python CLI)
> - [`dr-test.sh`](scripts/dr-test.sh) - Script completo de testing de DR (Bash)
> - [`requirements.txt`](scripts/requirements.txt) - Dependencias (ninguna, usa stdlib)
>
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso.

### 1. RPO/RTO Definitions

```yaml
# dr/rpo-rto-definitions.yml
services:
  - name: payment-service
    rpo: 5m      # Maximum 5 minutes of data loss
    rto: 15m     # Recovery within 15 minutes
    priority: critical
    backup_strategy: continuous

  - name: user-service
    rpo: 1h      # Maximum 1 hour of data loss
    rto: 30m     # Recovery within 30 minutes
    priority: high
    backup_strategy: hourly

  - name: analytics-service
    rpo: 24h     # Maximum 24 hours of data loss
    rto: 2h      # Recovery within 2 hours
    priority: medium
    backup_strategy: daily
```

### 2. Backup Strategy

**Script ejecutable:** [`scripts/backup-strategy.sh`](scripts/backup-strategy.sh)

Script Bash completo para automatizar estrategia de backups con soporte para backups completos, incrementales, verificación y limpieza.

#### Cuándo ejecutar

- **Backups programados:** Como parte de cron jobs (diarios/horarios)
- **Backups manuales:** Para crear backups bajo demanda
- **Verificación:** Para validar integridad de backups antes de restaurar
- **Limpieza:** Para mantener espacio de almacenamiento bajo control

#### Uso

```bash
# Hacer ejecutable
chmod +x scripts/backup-strategy.sh

# Backup completo (diario)
./scripts/backup-strategy.sh full

# Backup incremental (horario)
./scripts/backup-strategy.sh incremental

# Limpiar backups antiguos
./scripts/backup-strategy.sh cleanup

# Verificar backup
./scripts/backup-strategy.sh verify /backup/full/20240115

# Listar backups disponibles
./scripts/backup-strategy.sh list
```

#### Configuración

Variables de entorno:

```bash
export BACKUP_DIR="/backup"              # Directorio de backups
export RETENTION_DAYS=30                 # Días de retención
export S3_BUCKET="backup-bucket"         # Bucket S3 (opcional)
export DB_HOST="localhost"              # Host de base de datos
export DB_USER="backup_user"             # Usuario de backup
export DB_NAME="mydb"                    # Nombre de base de datos
export APP_DATA_DIR="/var/app/data"      # Directorio de datos de aplicación
```

#### Características

- ✅ Backups completos e incrementales
- ✅ Verificación automática de integridad
- ✅ Upload a S3 (opcional)
- ✅ Limpieza automática con política de retención
- ✅ Logging con colores
- ✅ Manejo de errores robusto

### 3. Failover Procedures

**Script ejecutable:** [`scripts/failover_procedures.py`](scripts/failover_procedures.py)

Gestor completo de procedimientos de failover con registro de servicios, health checks, y ejecución automatizada de failover.

#### Cuándo ejecutar

- **Registro de servicios:** Al configurar nuevos servicios para DR
- **Failover manual:** Cuando se detecta un desastre y se necesita failover
- **Failover automatizado:** Integrado con sistemas de monitoreo
- **Testing:** Para probar procedimientos de failover (dry-run)

#### Uso

```bash
# Registrar servicio
python scripts/failover_procedures.py register \
  --name payment-service \
  --primary us-east-1 \
  --standby us-west-2 \
  --rto 15 \
  --rpo 5

# Ejecutar failover
python scripts/failover_procedures.py failover payment-service

# Dry-run (simular sin cambios)
python scripts/failover_procedures.py failover payment-service --dry-run

# Ver estado de servicio
python scripts/failover_procedures.py status payment-service

# Ver estado de todos los servicios
python scripts/failover_procedures.py status

# Listar servicios registrados
python scripts/failover_procedures.py list
```

#### Características

- ✅ Registro y gestión de servicios
- ✅ Health checks de standby
- ✅ Promoción automática de standby a primary
- ✅ Actualización de routing (DNS/load balancer)
- ✅ Verificación de failover
- ✅ Modo dry-run para testing
- ✅ Persistencia de configuración en JSON
- ✅ Tracking de último failover

### 4. DR Testing

**Script ejecutable:** [`scripts/dr-test.sh`](scripts/dr-test.sh)

Script completo de testing de Disaster Recovery que simula un desastre y verifica todos los procedimientos de recuperación.

#### Cuándo ejecutar

- **Testing regular:** Ejecutar periódicamente (mensual/trimestral) para validar procedimientos
- **Después de cambios:** Después de modificar configuración de DR
- **Entrenamiento:** Para entrenar al equipo en procedimientos de DR
- **Validación:** Antes de aprobar cambios en producción

#### Uso

```bash
# Hacer ejecutable
chmod +x scripts/dr-test.sh

# Test completo
./scripts/dr-test.sh payment-service

# Test sin simular desastre (solo verificar procedimientos)
DR_TEST_SKIP_SIMULATION=true ./scripts/dr-test.sh payment-service

# Test sin failback (más rápido)
DR_TEST_SKIP_FAILBACK=true ./scripts/dr-test.sh payment-service
```

#### Fases del Test

1. **Pre-test checklist** - Verifica backups, standby health, documentación
2. **Simular desastre** - Detiene servicio primary (simulado)
3. **Ejecutar failover** - Ejecuta procedimiento de failover
4. **Verificar disponibilidad** - Confirma que servicio está disponible
5. **Restaurar primary** - Restaura servicio primary
6. **Failback** - Ejecuta procedimiento de failback
7. **Post-test verification** - Verifica salud del servicio y consistencia de datos

#### Características

- ✅ Checklist pre-test completo
- ✅ Simulación de desastre
- ✅ Verificación de cada fase
- ✅ Logging detallado con colores
- ✅ Opciones para saltar fases (testing parcial)
- ✅ Verificación de consistencia de datos

### 5. Multi-Region Setup

```yaml
# k8s/multi-region-deployment.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: dr-config
data:
  primary_region: "us-east-1"
  standby_region: "us-west-2"
  failover_threshold: "5m"
  rpo_minutes: "5"
  rto_minutes: "15"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-primary
  labels:
    app: payment-service
    region: primary
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
      region: primary
  template:
    metadata:
      labels:
        app: payment-service
        region: primary
    spec:
      containers:
      - name: app
        image: payment-service:latest
        env:
        - name: REGION
          value: "primary"
        - name: REPLICATION_MODE
          value: "master"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service-standby
  labels:
    app: payment-service
    region: standby
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payment-service
      region: standby
  template:
    metadata:
      labels:
        app: payment-service
        region: standby
    spec:
      containers:
      - name: app
        image: payment-service:latest
        env:
        - name: REGION
          value: "standby"
        - name: REPLICATION_MODE
          value: "replica"
```

## 🎯 Mejores Prácticas

### 1. RPO/RTO

✅ **DO:**
- Define realistic RPO/RTO
- Align with business requirements
- Test regularly
- Document assumptions

❌ **DON'T:**
- Set unrealistic targets
- Ignore business impact
- Skip testing

### 2. Backups

✅ **DO:**
- Test restore procedures
- Store backups off-site
- Encrypt backups
- Verify backup integrity

❌ **DON'T:**
- Assume backups work
- Skip verification
- Store in same location

### 3. Failover

✅ **DO:**
- Test failover regularly
- Document procedures
- Monitor failover events
- Practice with team

❌ **DON'T:**
- Skip failover testing
- Ignore documentation
- Test only in emergencies

## 🚨 Troubleshooting

### Backup Failures

1. Check disk space
2. Verify permissions
3. Review backup logs
4. Test restore procedures

### Failover Issues

1. Verify standby health
2. Check network connectivity
3. Review failover procedures
4. Test in non-production first

## 📚 Recursos Adicionales

- [AWS Disaster Recovery](https://aws.amazon.com/disaster-recovery/)
- [Google SRE - Disaster Recovery](https://sre.google/workbook/disaster-recovery/)
- [DR Planning Guide](https://www.ready.gov/business/emergency-plans/continuity-planning)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
