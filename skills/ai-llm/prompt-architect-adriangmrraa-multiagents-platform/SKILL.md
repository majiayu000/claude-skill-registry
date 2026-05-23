---
name: "AI Behavior Architect"
description: "Ingeniería de prompts para los Agentes de Ventas, Soporte y Business Forge."
trigger: "Cuando edite system prompts, plantillas de agentes o lógica de RAG."
scope: "AI_CORE"
auto-invoke: true
---

# Ingeniería de Prompts Nexus

1. **Estructura de System Prompt:**
   - **Identidad:** Quién eres (ej. "Vendedor Senior de {store_name}").
   - **Contexto:** Qué vendes (Inyectar `{catalog_summary}`).
   - **Restricciones (Safety):** Qué NO hacer (ej. "Nunca inventes descuentos").
   - **Formato de Salida:** Breve, persuasivo, formato WhatsApp (sin markdown complejo).

2. **Uso de Herramientas (Tool Calling):**
   - Instruye al modelo explícitamente sobre cuándo llamar a `search_products`.
   - *Ejemplo:* "Si el usuario pregunta por 'zapatillas rojas', NO respondas de memoria. EJECUTA `search_products(query='zapatillas rojas')` primero."

3. **Manejo de Alucinaciones RAG:**
   - Instrucción obligatoria: "Si la información no está en el contexto recuperado, di 'No tengo esa información en este momento' y ofrece derivar a un humano."

4. **Protocolo Assist Score (v7.6):**
   - **Auto-Auditoría:** Instruye al agente para evaluar su desempeño cada 3 mensajes del usuario.
   - **Herramienta:** Uso obligatorio de `report_assistance(type, score, reasoning)`.
   - **Silencio:** La auditoría debe ser invisible para el usuario final.
   - *Criterio:* 'sales' para hitos de compra (precio, stock), 'support' para resolución de dudas sin humano.
