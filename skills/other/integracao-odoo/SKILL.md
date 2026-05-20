---
name: integracao-odoo
description: "Cria e modifica integracoes com Odoo seguindo processo de 16 etapas. Cobre lancamento de CTes, despesas extras e documentos fiscais. Usar para IMPLEMENTAR novos fluxos de lancamento ou MODIFICAR existentes. Para CONSULTAS usar rastreando-odoo."
---

## QUANDO NAO USAR ESTA SKILL
- OPERAR integracoes ja existentes (esta skill e para CRIAR/MODIFICAR, nao para executar fluxos)
- Rastrear documentos no Odoo (esta skill nao faz consultas de rastreamento)
- Explorar modelo Odoo desconhecido (esta skill assume modelos ja mapeados)

# Integracao Odoo - Sistema de Fretes

> **ATENCAO**: Esta skill eh para DESENVOLVIMENTO (criar/modificar integracoes).
> Para CONSULTAS e rastreamento de fluxos, existe skill especializada em rastreamento.

Skill de desenvolvimento que documenta o processo completo de integracao com o Odoo ERP para lancamento de documentos fiscais (CTe) no sistema de fretes.

## Quando Usar Este Skill

- Implementar novo fluxo de lançamento de documento fiscal no Odoo
- Criar integração para novo tipo de despesa/frete
- Modificar processo existente de lançamento
- Debugar problemas em lançamentos Odoo
- Entender o fluxo de 16 etapas

## Arquitetura da Integração

### Modelos Odoo Envolvidos

| Modelo | Descrição | Uso |
|--------|-----------|-----|
| `l10n_br_ciel_it_account.dfe` | Documento Fiscal Eletrônico | Busca e configuração inicial |
| `l10n_br_ciel_it_account.dfe.line` | Linhas do DFe | Produto e conta analítica |
| `l10n_br_ciel_it_account.dfe.pagamento` | Pagamentos do DFe | Vencimento |
| `purchase.order` | Pedido de Compra | PO gerado do DFe |
| `account.move` | Fatura/Invoice | Documento final |

### IDs Fixos do Odoo (Ambiente Produção)

```python
PRODUTO_SERVICO_FRETE_ID = 29993          # Produto "SERVICO DE FRETE"
CONTA_ANALITICA_LOGISTICA_ID = 1186       # Centro de custo Logística
TEAM_LANCAMENTO_FRETE_ID = 119            # Equipe de lançamento
PAYMENT_PROVIDER_TRANSFERENCIA_ID = 30    # Forma pagamento
COMPANY_NACOM_GOYA_CD_ID = 4              # Empresa
PICKING_TYPE_CD_RECEBIMENTO_ID = 13       # Tipo recebimento CD
```

## As 16 Etapas do Lançamento

### Fase 1: Configuração do DFe (Etapas 1-5)

```
Etapa 1: Buscar DFe pela chave de acesso (44 dígitos)
         Modelo: l10n_br_ciel_it_account.dfe
         Ação: search_read
         Validação: status deve ser '04' (PO)

Etapa 2: Atualizar data de entrada e payment_reference
         Campos: l10n_br_date_in, payment_reference

Etapa 3: Definir tipo_pedido = 'servico'

Etapa 4: Atualizar linha com produto SERVICO DE FRETE
         Modelo: l10n_br_ciel_it_account.dfe.line
         Campos: product_id, analytic_distribution

Etapa 5: Atualizar vencimento
         Modelo: l10n_br_ciel_it_account.dfe.pagamento
         Campo: date_due
```

### Fase 2: Purchase Order (Etapas 6-10)

```
Etapa 6: Gerar Purchase Order
         Método: action_gerar_po_dfe

Etapa 7: Configurar PO
         Campos: team_id, payment_provider_id, picking_type_id

Etapa 8: (Pulada) Impostos calculados automaticamente

Etapa 9: Confirmar PO
         Método: button_confirm

Etapa 10: Aprovar PO (se necessário)
          Método: button_approve
          Condição: state == 'to approve'
```

### Fase 3: Invoice (Etapas 11-16)

```
Etapa 11: Criar Invoice
          Método: action_create_invoice

Etapa 12: Atualizar impostos
          Método: _compute_tax_totals

Etapa 13: Configurar Invoice
          Campos: invoice_date, payment_reference

Etapa 14: Recalcular impostos

Etapa 15: Confirmar Invoice
          Método: action_post

Etapa 16: Atualizar registro local
          Campos: odoo_dfe_id, odoo_purchase_order_id,
                  odoo_invoice_id, lancado_odoo_em,
                  lancado_odoo_por, status
```

## Estrutura do Service de Lançamento

### Campos Necessários no Modelo Local

Para qualquer entidade que será lançada no Odoo, adicionar:

```python
# Integração Odoo
odoo_dfe_id = db.Column(db.Integer, nullable=True, index=True)
odoo_purchase_order_id = db.Column(db.Integer, nullable=True)
odoo_invoice_id = db.Column(db.Integer, nullable=True)
lancado_odoo_em = db.Column(db.DateTime, nullable=True)
lancado_odoo_por = db.Column(db.String(100), nullable=True)

# Status deve incluir 'LANCADO_ODOO'
status = db.Column(db.String(20), default='PENDENTE', nullable=False, index=True)
```

### Estrutura do Service

```python
class LancamentoXxxOdooService(LancamentoOdooService):
    """
    Service para lançar [entidade] no Odoo.
    Herda de LancamentoOdooService e adapta para [entidade].
    """

    def lancar_xxx_odoo(self, xxx_id: int, data_vencimento: date = None) -> Dict[str, Any]:
        """
        Executa lançamento completo no Odoo

        Returns:
            Dict com: sucesso, mensagem, dfe_id, purchase_order_id,
                      invoice_id, etapas_concluidas, auditoria, erro
        """
        # 1. Validações iniciais
        # 2. Buscar CTe vinculado
        # 3. Conectar no Odoo
        # 4. Executar 16 etapas
        # 5. Atualizar registro local
        # 6. Retornar resultado
```

## Auditoria

Cada etapa deve ser registrada na tabela `lancamento_frete_odoo_auditoria`:

```python
LancamentoFreteOdooAuditoria(
    frete_id=None,  # ou ID do frete
    despesa_extra_id=None,  # ou ID da despesa
    cte_id=cte_id,
    chave_cte=chave_cte,
    etapa=numero_etapa,
    etapa_descricao="Descrição da etapa",
    modelo_odoo='modelo.odoo',
    metodo_odoo='nome_metodo',  # se aplicável
    acao='search_read|write|execute_method|skip',
    status='SUCESSO|ERRO',
    mensagem="Mensagem descritiva",
    tempo_execucao_ms=tempo_ms,
    dfe_id=dfe_id,
    purchase_order_id=po_id,
    invoice_id=invoice_id
)
```

## Pré-requisitos para Lançamento

1. **CTe deve existir no Odoo** com status '04' (PO)
2. **CTe deve estar vinculado** ao registro local
3. **Data de vencimento** deve estar definida
4. **Usuário autenticado** no sistema

## Tratamento de Erros e Rollback

```python
def _rollback_xxx_odoo(self, xxx_id: int, etapas_concluidas: int) -> bool:
    """
    Limpa campos Odoo em caso de erro (se não completou 16 etapas)
    """
    if status != 'LANCADO_ODOO' or etapas_concluidas < 16:
        xxx.odoo_dfe_id = None
        xxx.odoo_purchase_order_id = None
        xxx.odoo_invoice_id = None
        xxx.lancado_odoo_em = None
        xxx.lancado_odoo_por = None
        xxx.status = 'status_anterior'
```

## Exemplos Reais de Implementacao

### Exemplo 1: Lancamento de Frete (Referencia Principal)

**Arquivos**:
- Service: `app/fretes/services/lancamento_odoo_service.py`
- Route: `app/fretes/routes.py` - `lancar_frete_odoo()`
- Model: `app/fretes/models.py` - classe `Frete`

**Fluxo resumido**:
```python
# Route recebe requisicao
@fretes_bp.route('/api/fretes/<int:frete_id>/lancar-odoo', methods=['POST'])
def lancar_frete_odoo(frete_id):
    service = LancamentoFreteOdooService()
    resultado = service.lancar_frete_odoo(
        frete_id=frete_id,
        data_vencimento=data_venc,
        usuario=current_user.nome
    )
    return jsonify(resultado)

# Service executa 16 etapas
class LancamentoFreteOdooService(LancamentoOdooService):
    def lancar_frete_odoo(self, frete_id, data_vencimento, usuario):
        # 1. Busca frete no banco local
        frete = Frete.query.get(frete_id)

        # 2. Valida pre-requisitos
        if not frete.chave_cte:
            raise ValueError("Frete sem CTe vinculado")

        # 3. Executa 16 etapas no Odoo
        resultado = self._executar_16_etapas(frete.chave_cte, data_vencimento)

        # 4. Atualiza registro local
        frete.odoo_invoice_id = resultado['invoice_id']
        frete.status = 'LANCADO_ODOO'
        db.session.commit()
```

---

### Exemplo 2: Lancamento de Despesa Extra

**Arquivos**:
- Service: `app/fretes/services/lancamento_despesa_odoo_service.py`
- Route: `app/fretes/routes.py` - `lancar_despesa_odoo()`
- Model: `app/fretes/models.py` - classe `DespesaExtra`

**Diferenca em relacao ao Frete**:
```python
# DespesaExtra pode ter transportadora diferente do Frete pai
# Por isso tem campo transportadora_id proprio

class LancamentoDespesaOdooService(LancamentoOdooService):
    def lancar_despesa_odoo(self, despesa_id, data_vencimento, usuario):
        despesa = DespesaExtra.query.get(despesa_id)

        # Usa CTe da despesa (pode ser diferente do frete)
        chave_cte = despesa.chave_cte

        # Usa transportadora da despesa (se definida) ou do frete
        transportadora = despesa.transportadora or despesa.frete.transportadora

        # Resto do fluxo igual ao Frete
```

**Campos adicionados no modelo DespesaExtra**:
```python
# Em app/fretes/models.py

class DespesaExtra(db.Model):
    # ... campos existentes ...

    # Campos de integracao Odoo (adicionados para lancamento)
    odoo_dfe_id = db.Column(db.Integer, nullable=True, index=True)
    odoo_purchase_order_id = db.Column(db.Integer, nullable=True)
    odoo_invoice_id = db.Column(db.Integer, nullable=True)
    lancado_odoo_em = db.Column(db.DateTime, nullable=True)
    lancado_odoo_por = db.Column(db.String(100), nullable=True)

    # Transportadora alternativa (se diferente do Frete pai)
    transportadora_id = db.Column(db.Integer, db.ForeignKey('transportadoras.id'), nullable=True)
```

---

### Padrao de Frontend para Lancamento

**Modal de progresso** (usado em ambos):
```html
<!-- Modal mostra progresso das 16 etapas -->
<div class="modal" id="modalProgresso">
    <div class="progress-bar">
        <div class="progress" style="width: 0%"></div>
    </div>
    <div id="etapaAtual">Iniciando...</div>
</div>
```

**JavaScript AJAX**:
```javascript
function lancarOdoo(id, tipo) {
    const url = tipo === 'frete'
        ? `/api/fretes/${id}/lancar-odoo`
        : `/api/despesas/${id}/lancar-odoo`;

    fetch(url, { method: 'POST', body: JSON.stringify(dados) })
        .then(response => response.json())
        .then(resultado => {
            if (resultado.sucesso) {
                atualizarUI(resultado);
            } else {
                mostrarErro(resultado.erro, resultado.etapas_concluidas);
            }
        });
}
```

## Checklist para Nova Integração

- [ ] Adicionar campos Odoo no modelo (`odoo_dfe_id`, `odoo_purchase_order_id`, etc.)
- [ ] Adicionar status `LANCADO_ODOO` no modelo
- [ ] Criar script de migração para novos campos
- [ ] Criar Service herdando de `LancamentoOdooService`
- [ ] Implementar método `lancar_xxx_odoo()` com 16 etapas
- [ ] Implementar método `_rollback_xxx_odoo()`
- [ ] Criar route POST para lançamento
- [ ] Criar route GET para auditoria
- [ ] Atualizar template com botão de lançamento e modal
- [ ] Adicionar JavaScript para chamada AJAX com progresso
- [ ] Testar em ambiente de desenvolvimento
- [ ] Documentar no CLAUDE.md

## Conexão com Odoo

```python
from app.odoo.utils.connection import get_odoo_connection

odoo = get_odoo_connection()
if not odoo.authenticate():
    raise Exception("Falha na autenticação com Odoo")

# Operações disponíveis:
odoo.search_read(modelo, filtros, fields, limit)
odoo.read(modelo, ids, fields)
odoo.write(modelo, ids, valores)
odoo.execute_method(modelo, metodo, args)
```

## Guidelines

1. **SEMPRE** registrar auditoria de cada etapa
2. **NUNCA** pular etapas sem registrar na auditoria (usar status 'skip')
3. **SEMPRE** implementar rollback para limpeza em caso de erro
4. **SEMPRE** validar status do DFe antes de iniciar (deve ser '04')
5. **NUNCA** lançar documento que já foi lançado (verificar `odoo_invoice_id`)
6. **SEMPRE** usar transação para atualizar registro local no final
7. **SEMPRE** capturar tempo de execução de cada etapa para diagnóstico

## Relacionado

| Skill | Uso |
|-------|-----|
| rastreando-odoo | Para CONSULTAS e rastreamento de fluxos (NF, PO, SO, titulos, conciliacoes) |
| descobrindo-odoo-estrutura | Para descobrir campos/modelos nao mapeados |
| gerindo-expedicao | Para consultas de carteira, separacoes e estoque |

## Templates Disponiveis

Os templates em `resources/` auxiliam na criacao de novas integracoes:

| Template | Descricao |
|----------|-----------|
| `template_modelo_campos.py` | Campos SQLAlchemy para integracao Odoo |
| `template_service.py` | Estrutura base do Service de lancamento |
| `template_migracao.py` | Script de migracao para novos campos |
| `template_route.py` | Routes Flask para lancamento e auditoria |
