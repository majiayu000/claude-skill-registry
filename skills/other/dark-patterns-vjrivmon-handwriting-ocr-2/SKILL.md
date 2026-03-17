---
name: dark-patterns
description:
  Patrones de diseño manipulativos que engañan usuarios. Use para identificar y
  evitar prácticas poco éticas en diseño de interfaces.
metadata:
  author: ux-ui-skills
  version: "1.0"
  category: anti-patterns
---

# Dark Patterns

## Resumen

Los Dark Patterns son trucos de diseño que manipulan a los usuarios para hacer
cosas que no tenían intención de hacer, generalmente en beneficio del negocio y
en detrimento del usuario.

## Origen

- **Acuñado por**: Harry Brignull
- **Año**: 2010
- **Sitio**: darkpatterns.org (ahora deceptive.design)
- **Propósito**: Documentar y denunciar prácticas manipulativas

## Tipos de Dark Patterns

### Bait and Switch

- Prometes una cosa, entregas otra
- Click en X cierra = aceptar
- "Descargar" que instala otra cosa
- Oferta que cambia en checkout

### Confirmshaming

- Avergonzar al usuario por declinar
- "No, prefiero pagar precio completo"
- "No me interesa ahorrar dinero"
- Lenguaje culposo en opt-outs

### Disguised Ads

- Anuncios que parecen contenido
- Botones de descarga falsos
- Links que parecen navegación
- Sponsored content sin etiquetar

### Forced Continuity

- Free trial → cargo automático
- Sin recordatorio antes de cobro
- Difícil de cancelar
- Cargos ocultos en letra pequeña

### Friend Spam

- Acceso a contactos sin consentimiento claro
- Enviar invitaciones automáticas
- "Importar contactos" que envía spam
- Notifications en nombre del usuario

### Hidden Costs

- Costos revelados al final
- Fees de servicio sorpresa
- Shipping costoso revelado tarde
- Impuestos mostrados al final

### Misdirection

- Atención dirigida lejos de lo importante
- Opción preferida del negocio destacada
- Warnings pequeños vs CTAs grandes
- Visual hierarchy manipulativo

### Price Comparison Prevention

- Dificultar comparar precios
- Unidades diferentes por plan
- Features nombradas diferente
- Bundles que ocultan valor individual

### Privacy Zuckering

- Confundir sobre privacidad
- Defaults que comparten más
- Settings de privacidad ocultos
- Cambios de política enterrados

### Roach Motel

- Fácil entrar, difícil salir
- Sign up en 1 click, cancelar requiere llamada
- Ocultar botón de cancelar
- Múltiples pasos para darse de baja

### Sneak into Basket

- Items agregados sin consentimiento
- Opt-out de extras pre-seleccionados
- "Recommended" items incluidos
- Seguros o servicios añadidos

### Trick Questions

- Doble negación confusa
- Checkboxes que significan opt-out
- Framing engañoso
- Lenguaje deliberadamente confuso

## Legislación y Ética

### Regulaciones

- **GDPR** (EU): Consent debe ser claro
- **CCPA** (California): Derecho a opt-out
- **FTC** (USA): Acciones contra deceptive practices
- **DSA** (EU): Prohibición explícita de dark patterns

### Consecuencias

- Multas millonarias
- Daño reputacional
- Pérdida de confianza
- Class action lawsuits

## Alternativas Éticas

### En lugar de Confirmshaming

```
❌ "No, no quiero ahorrar dinero"
✅ "No, gracias" o "Quizás después"
```

### En lugar de Hidden Costs

```
❌ Precio sin fees hasta checkout
✅ "Total estimado incluyendo envío: $XX"
```

### En lugar de Roach Motel

```
❌ Cancelar requiere llamar a soporte
✅ "Cancelar suscripción" en settings
```

### En lugar de Misdirection

```
❌ "Accept All" grande, "Manage" tiny
✅ Ambas opciones igual de prominentes
```

## Ejemplos Notorios

- **Amazon Prime**: Proceso de cancelación laberíntico
- **LinkedIn**: Importar contactos → spam
- **Facebook**: Privacy settings cambiantes y confusos
- **Booking.com**: "Solo quedan 2 habitaciones" (pressure)
- **Ryanair**: Extras pre-seleccionados

## Cómo Identificarlos

### Preguntas Clave

- ¿El usuario haría esto si entendiera completamente?
- ¿Estamos aprovechando sesgos cognitivos maliciosamente?
- ¿Es igual de fácil hacer lo opuesto?
- ¿Es transparente qué estamos haciendo?

## Métricas Éticas

- **Regret Rate**: Usuarios que revierten acciones
- **Support Tickets**: Quejas por confusión
- **Unsubscribe Rate**: Tras "accidentalmente" subscribirse
- **Trust Score**: Encuestas de confianza

## Principios Relacionados

- [[trust-credibility]] - Construir, no destruir confianza
- [[nielsen-user-control]] - Control real del usuario
- [[least-astonishment]] - Sin sorpresas desagradables

## Referencias

- Brignull, H. (2010). "Dark Patterns"
- https://www.deceptive.design/
- Mathur, A. et al. (2019). "Dark Patterns at Scale"
- Gray, C.M. et al. (2018). "The Dark Side of UX Design"
