---
name: whatsapp-flows
description: Fluxos conversacionais WhatsApp
---

Desenvolvimento de fluxos interativos para o WhatsApp Business API via Twilio, o canal mais inclusivo do Brasil.

## Contexto

- WhatsApp presente em 99% dos smartphones brasileiros
- 28+ milhões de brasileiros sem acesso à internet convencional usam dados móveis limitados
- Muitos cidadãos só sabem usar WhatsApp
- Já temos integração Twilio em `backend/app/routers/webhook.py`

## Arquitetura Atual
```
Cidadão (WhatsApp) → Twilio → POST /api/v1/webhook/whatsapp/chat → TaNaMaoAgent → Resposta
```

## Templates de Mensagem (Meta-aprovados)

### 1. Boas-vindas
```
Olá! Sou o assistente do Tá na Mão.

Posso te ajudar com:
1️⃣ Ver meus benefícios
2️⃣ Documentos que preciso
3️⃣ Achar CRAS perto de mim
4️⃣ Dinheiro esquecido
5️⃣ Farmácia Popular

Manda o número da opção!
```

### 2. Consulta de Benefício
```
Para consultar seus benefícios, preciso do seu CPF.

Pode mandar aqui que é seguro. Só uso pra consultar, não guardo.

(Manda só os 11 números)
```

### 3. Resultado de Consulta
```
{{nome}}, achei seus dados!

✅ Bolsa Família: R$ {{valor}}/mês
📋 CadÚnico: Atualizado até {{data}}

Quer saber de mais benefícios que você pode ter direito?
Manda SIM ou NÃO.
```

### 4. Checklist de Documentos
```
Para pedir {{beneficio}}, leve ao CRAS:

📄 CPF de todos da família
📄 Certidão de nascimento ou casamento
📄 Comprovante de onde mora
📄 Carteira de trabalho
📄 Comprovante de renda (se tiver)

O CRAS mais perto de você fica em:
📍 {{endereco_cras}}
📞 {{telefone_cras}}
```

### 5. Alerta de Cadastro Vencendo
```
⚠️ {{nome}}, seu CadÚnico precisa ser atualizado!

Se não atualizar até {{data_limite}}, seus benefícios podem ser suspensos.

Leve seus documentos ao CRAS:
📍 {{endereco_cras}}

Horário: {{horario_funcionamento}}
```

## Fluxos Interativos

### Fluxo: Consulta de Benefícios
```python
# backend/app/agent/whatsapp/flows/consulta_beneficio.py

FLOW_CONSULTA = {
    "inicio": {
        "mensagem": "Vou consultar seus benefícios. Manda seu CPF (só números).",
        "espera": "cpf",
        "proximo": "validar_cpf"
    },
    "validar_cpf": {
        "acao": "validar_cpf_tool",
        "sucesso": "consultar",
        "erro": {
            "mensagem": "CPF inválido. Confere e manda de novo (11 números).",
            "voltar": "inicio"
        }
    },
    "consultar": {
        "acao": "consultar_beneficio_tool",
        "sucesso": "mostrar_resultado",
        "erro": {
            "mensagem": "Não consegui consultar agora. Tenta de novo em 5 minutos.",
            "voltar": "fim"
        }
    },
    "mostrar_resultado": {
        "mensagem": "template_resultado",
        "botoes": [
            {"texto": "Ver mais benefícios", "proximo": "elegibilidade"},
            {"texto": "Documentos necessários", "proximo": "checklist"},
            {"texto": "Achar CRAS", "proximo": "buscar_cras"}
        ]
    }
}
```

### Fluxo: Localizar CRAS
```python
FLOW_CRAS = {
    "inicio": {
        "mensagem": "Manda sua localização 📍 ou seu CEP que acho o CRAS mais perto.",
        "espera": "localizacao_ou_cep",
        "proximo": "buscar"
    },
    "buscar": {
        "acao": "buscar_cras_tool",
        "sucesso": "mostrar_cras",
        "erro": {
            "mensagem": "Não achei CRAS perto. Manda outro CEP ou sua cidade.",
            "voltar": "inicio"
        }
    },
    "mostrar_cras": {
        "mensagem": "template_cras_proximo",
        "botoes": [
            {"texto": "Ver no mapa", "acao": "enviar_localizacao"},
            {"texto": "Ligar pro CRAS", "acao": "enviar_telefone"},
            {"texto": "O que levar", "proximo": "checklist_cras"}
        ]
    }
}
```

## Implementação Twilio

### Webhook Handler
```python
# backend/app/routers/webhook.py
@router.post("/whatsapp/chat")
async def whatsapp_webhook(request: Request):
    form = await request.form()
    from_number = form.get("From")  # whatsapp:+5511999999999
    body = form.get("Body", "").strip()
    media_url = form.get("MediaUrl0")  # foto de receita, etc.
    latitude = form.get("Latitude")
    longitude = form.get("Longitude")

    # Recuperar sessão do Redis
    session = await get_whatsapp_session(from_number)

    # Processar pelo fluxo ativo ou agente
    if session.active_flow:
        response = await process_flow(session, body, media_url, latitude, longitude)
    else:
        response = await agent.process(body, session_id=from_number)

    # Enviar resposta via Twilio
    return await send_whatsapp_response(from_number, response)
```

### Envio de Mensagens Interativas
```python
# backend/app/services/whatsapp_service.py
from twilio.rest import Client

async def enviar_menu(to: str, texto: str, botoes: list[dict]):
    """Envia mensagem com botões interativos."""
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(
        from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        to=to,
        body=texto,
        # Botões interativos (máximo 3)
    )
    return message.sid

async def enviar_localizacao(to: str, lat: float, lng: float, nome: str):
    """Envia localização do CRAS/farmácia."""
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(
        from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
        to=to,
        body=f"📍 {nome}",
        persistent_action=[f"geo:{lat},{lng}|{nome}"]
    )
    return message.sid
```

## Gestão de Sessão
```python
# Redis: sessão WhatsApp com TTL de 24h
async def get_whatsapp_session(phone: str) -> WhatsAppSession:
    key = f"wa_session:{phone}"
    data = await redis.get(key)
    if data:
        return WhatsAppSession.parse_raw(data)
    session = WhatsAppSession(phone=phone)
    await redis.setex(key, 86400, session.json())
    return session

async def update_whatsapp_session(session: WhatsAppSession):
    key = f"wa_session:{session.phone}"
    await redis.setex(key, 86400, session.json())
```

## Rate Limiting
```python
# Limite: 1 mensagem por segundo por número, 1000/dia por número
WHATSAPP_RATE_LIMITS = {
    "por_segundo": 1,
    "por_dia": 1000,
    "janela_conversa": 24 * 60 * 60,  # 24h após última mensagem do usuário
}
```

## Arquivos Relacionados
- `backend/app/routers/webhook.py` - Webhook principal
- `backend/app/services/whatsapp_service.py` - Serviço de envio
- `backend/app/agent/whatsapp/flows/` - Fluxos conversacionais
- `backend/app/agent/agent.py` - Agente principal

## Variáveis de Ambiente
```bash
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_WHATSAPP_NUMBER=+14155238886
WHATSAPP_WEBHOOK_URL=https://api.tanamao.com.br/api/v1/webhook/whatsapp/chat
```

## Boas Práticas
- Mensagens curtas (máximo 1024 caracteres por bolha)
- Máximo 3 botões por mensagem interativa
- Sempre oferecer opção "Voltar" ou "Menu principal"
- Confirmar dados sensíveis antes de prosseguir
- Timeout de sessão: 24h (regra do WhatsApp Business)
- Nunca enviar CPF completo de volta na resposta
- Usar emojis com moderação para facilitar leitura

## Troubleshooting
| Problema | Causa | Solução |
|----------|-------|---------|
| Mensagem não chega | Janela de 24h expirou | Usar template aprovado pela Meta |
| Botões não aparecem | Formato incorreto | Verificar payload Twilio |
| Sessão perdida | Redis reiniciou | Tratar como nova conversa |
| Rate limit Twilio | Muitas mensagens | Implementar fila com backoff |
