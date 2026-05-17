#!/usr/bin/env bash
# Verificar si todas las fases en task_plan.md están completas
# Siempre salir con código 0 — usar stdout para informar el estado
# Llamado por el hook Stop para informar el estado de finalización de la tarea

PLAN_FILE="${1:-task_plan.md}"

if [ ! -f "$PLAN_FILE" ]; then
    echo "[planning-with-files-es] No se encontró task_plan.md — no hay sesión de planificación activa."
    exit 0
fi

# Contar el total de fases
TOTAL=$(grep -c "### Phase" "$PLAN_FILE" || true)

# Primero verificar formato **Estado:**
COMPLETE=$(grep -cF "**Estado:** complete" "$PLAN_FILE" || true)
IN_PROGRESS=$(grep -cF "**Estado:** in_progress" "$PLAN_FILE" || true)
PENDING=$(grep -cF "**Estado:** pending" "$PLAN_FILE" || true)

# Alternativa: si no se encontró **Estado:** verificar formato en línea [complete]
if [ "$COMPLETE" -eq 0 ] && [ "$IN_PROGRESS" -eq 0 ] && [ "$PENDING" -eq 0 ]; then
    COMPLETE=$(grep -c "\[complete\]" "$PLAN_FILE" || true)
    IN_PROGRESS=$(grep -c "\[in_progress\]" "$PLAN_FILE" || true)
    PENDING=$(grep -c "\[pending\]" "$PLAN_FILE" || true)
fi

# Valor por defecto 0 (si está vacío)
: "${TOTAL:=0}"
: "${COMPLETE:=0}"
: "${IN_PROGRESS:=0}"
: "${PENDING:=0}"

# Informar estado (siempre salir con código 0 — tareas incompletas son estado normal)
if [ "$COMPLETE" -eq "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
    echo "[planning-with-files-es] Todas las fases completadas ($COMPLETE/$TOTAL). Si el usuario tiene trabajo adicional, añadir fases en task_plan.md antes de comenzar."
else
    echo "[planning-with-files-es] Tarea en progreso ($COMPLETE/$TOTAL fases completadas). Actualizar progress.md antes de detenerse."
    if [ "$IN_PROGRESS" -gt 0 ]; then
        echo "[planning-with-files-es] $IN_PROGRESS fases aún en progreso."
    fi
    if [ "$PENDING" -gt 0 ]; then
        echo "[planning-with-files-es] $PENDING fases pendientes."
    fi
fi
exit 0
