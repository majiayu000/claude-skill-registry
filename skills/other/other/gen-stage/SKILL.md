---
name: gen-stage
description: >
  Use when working with GenStage for building concurrent data pipelines with
  back-pressure in Elixir. Covers producers, consumers, dispatchers (Demand,
  Broadcast, Partition), rate limiting, ConsumerSupervisor, and supervision patterns.
---

# Skill GenStage - Guia Completo para Desenvolvedores Elixir

## O que e GenStage?

GenStage e uma especificacao Elixir para troca de eventos entre **producers** (produtores) e **consumers** (consumidores) com **back-pressure** (contrapressao) automatica. Ele resolve o problema fundamental de: "Como processar dados de forma concorrente sem sobrecarregar o sistema?"

A ideia central: **o consumidor pede dados ao produtor** (modelo pull), nao o produtor empurrando dados para o consumidor (modelo push). Isso garante que nenhum componente do pipeline fique sobrecarregado.

---

## Instalacao

```elixir
# mix.exs
defp deps do
  [
    {:gen_stage, "~> 1.0"}
  ]
end
```

Requisito: Elixir >= 1.11

---

## Conceitos Fundamentais

### Os 3 Tipos de Stage

```
+------------+       +---------------------+       +------------+
|  PRODUCER  | ----> | PRODUCER_CONSUMER   | ----> |  CONSUMER  |
| (Source)   |       | (Transformador)     |       | (Sink)     |
+------------+       +---------------------+       +------------+
     ^                        ^                          |
     |                        |                          |
  Gera eventos         Recebe E emite            Consome eventos
  sob demanda          eventos                   e pede mais
```

1. **`:producer`** (source) - Apenas gera eventos. Implementa `handle_demand/2`.
2. **`:consumer`** (sink) - Apenas consome eventos. Implementa `handle_events/3`.
3. **`:producer_consumer`** - Recebe eventos, transforma e emite novos. Implementa `handle_events/3`.

### Como funciona o Back-Pressure

```
Consumer: "Quero 1000 eventos" (max_demand: 1000)
    |
    v
Producer: Envia ate 1000 eventos
    |
    v
Consumer: Processa eventos...
    Quando demanda cai para 750 (min_demand), pede mais 250
    |
    v
Producer: Envia mais 250
    ... ciclo continua ...
```

- `max_demand` - Maximo de eventos solicitados por vez (padrao: 1000)
- `min_demand` - Limiar para pedir mais eventos (padrao: max_demand * 3/4, ou seja, 750)
- O consumidor NUNCA recebe mais do que pediu
- Quando o producer produz em lotes de 100 e max_demand=1000/min_demand=750: apos 3 lotes a demanda cai para 700 (abaixo de 750), entao o consumer pede 300 para voltar a 1000

---

## Padrao 1: Pipeline Basico (Producer -> Consumer)

O caso mais simples: um produtor gera numeros e um consumidor os processa.

```elixir
defmodule NumberProducer do
  use GenStage

  def start_link(initial) do
    GenStage.start_link(__MODULE__, initial, name: __MODULE__)
  end

  @impl true
  def init(counter) do
    {:producer, counter}
  end

  @impl true
  def handle_demand(demand, counter) when demand > 0 do
    # Se counter=3 e demand=2, emite [3, 4] e estado vira 5
    events = Enum.to_list(counter..(counter + demand - 1))
    {:noreply, events, counter + demand}
  end
end

defmodule NumberConsumer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok)
  end

  @impl true
  def init(:ok) do
    # subscribe_to conecta automaticamente ao producer
    {:consumer, :ok, subscribe_to: [{NumberProducer, max_demand: 10}]}
  end

  @impl true
  def handle_events(events, _from, state) do
    Enum.each(events, fn event ->
      IO.puts("Processando: #{event}")
    end)

    # Consumer SEMPRE retorna lista vazia de eventos
    {:noreply, [], state}
  end
end
```

### Supervision Tree

```elixir
children = [
  {NumberProducer, 0},
  Supervisor.child_spec({NumberConsumer, []}, id: :c1),
  Supervisor.child_spec({NumberConsumer, []}, id: :c2),
  Supervisor.child_spec({NumberConsumer, []}, id: :c3),
  Supervisor.child_spec({NumberConsumer, []}, id: :c4)
]

# rest_for_one: se o producer reiniciar, consumers tambem reiniciam
Supervisor.start_link(children, strategy: :rest_for_one)
```

> **IMPORTANTE**: Use `strategy: :rest_for_one` para que se o producer reiniciar, os consumers tambem reiniciem (eles precisam se reinscrever). Com `:one_for_one`, se o producer A morre, os consumers morrem tambem (perdem a inscricao) e o supervisor pode interpretar como muitas falhas simultaneas.

---

## Padrao 2: Pipeline com Transformacao (Producer -> ProducerConsumer -> Consumer)

Quando voce precisa transformar dados entre a fonte e o destino.

```elixir
defmodule DataSource do
  use GenStage

  def start_link(opts) do
    GenStage.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @impl true
  def init(_opts) do
    {:producer, :no_state}
  end

  @impl true
  def handle_demand(demand, state) do
    events = fetch_from_database(demand)
    {:noreply, events, state}
  end

  defp fetch_from_database(count) do
    Enum.map(1..count, fn i -> %{id: i, raw_data: "data_#{i}"} end)
  end
end

defmodule DataTransformer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  @impl true
  def init(:ok) do
    # producer_consumer tem buffer_size: :infinity por padrao!
    {:producer_consumer, :ok, subscribe_to: [{DataSource, max_demand: 100}]}
  end

  @impl true
  def handle_events(events, _from, state) do
    transformed =
      events
      |> Enum.map(&transform/1)
      |> Enum.filter(&valid?/1)

    # producer_consumer PODE filtrar: emitir menos eventos do que recebeu
    {:noreply, transformed, state}
  end

  defp transform(%{raw_data: data} = event) do
    Map.put(event, :processed_data, String.upcase(data))
  end

  defp valid?(%{processed_data: data}), do: String.length(data) > 0
end

defmodule DataSink do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok)
  end

  @impl true
  def init(:ok) do
    {:consumer, :ok, subscribe_to: [{DataTransformer, max_demand: 50}]}
  end

  @impl true
  def handle_events(events, _from, state) do
    Enum.each(events, &persist/1)
    {:noreply, [], state}
  end

  defp persist(event) do
    IO.inspect(event, label: "Persistindo")
  end
end
```

> **Anti-pattern**: NAO crie um stage por passo logico do seu dominio. Stages servem para modelar propriedades de runtime (concorrencia, transferencia de dados), NAO organizacao de codigo. Se voce tem 3 passos logicos, considere combina-los em um unico consumer e escalar com multiplas instancias:

```
                 [Consumer: Step1 + Step2 + Step3]
                /
[Producer] ---->[Consumer: Step1 + Step2 + Step3]
                \
                 [Consumer: Step1 + Step2 + Step3]
```

---

## Padrao 3: BroadcastDispatcher (1 Producer -> N Consumers, todos recebem tudo)

Quando TODOS os consumers precisam receber TODOS os eventos (fan-out).

```elixir
defmodule EventBroadcaster do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  @doc "Envia evento e so retorna apos o despacho"
  def sync_notify(event, timeout \\ 5000) do
    GenStage.call(__MODULE__, {:notify, event}, timeout)
  end

  @impl true
  def init(:ok) do
    # BroadcastDispatcher envia para TODOS os consumers
    # Acumula demanda ate TODOS terem pedido
    {:producer, {:queue.new(), 0}, dispatcher: GenStage.BroadcastDispatcher}
  end

  @impl true
  def handle_call({:notify, event}, from, {queue, pending_demand}) do
    queue = :queue.in({from, event}, queue)
    dispatch_events(queue, pending_demand, [])
  end

  @impl true
  def handle_demand(incoming_demand, {queue, pending_demand}) do
    dispatch_events(queue, incoming_demand + pending_demand, [])
  end

  defp dispatch_events(queue, 0, events) do
    {:noreply, Enum.reverse(events), {queue, 0}}
  end

  defp dispatch_events(queue, demand, events) do
    case :queue.out(queue) do
      {{:value, {from, event}}, queue} ->
        GenStage.reply(from, :ok)
        dispatch_events(queue, demand - 1, [event | events])

      {:empty, queue} ->
        {:noreply, Enum.reverse(events), {queue, demand}}
    end
  end
end
```

### Consumer com filtro (selector)

```elixir
# Consumer que recebe APENAS eventos do tipo :email
defmodule EmailNotifier do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok)
  end

  @impl true
  def init(:ok) do
    selector = fn event -> event.type == :email end

    {:consumer, :ok,
     subscribe_to: [
       {EventBroadcaster, selector: selector}
     ]}
  end

  @impl true
  def handle_events(events, _from, state) do
    Enum.each(events, fn event ->
      IO.puts("Enviando email: #{inspect(event)}")
    end)
    {:noreply, [], state}
  end
end

# Consumer que recebe TODOS os eventos (auditoria)
defmodule AuditLogger do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok)
  end

  @impl true
  def init(:ok) do
    {:consumer, :ok, subscribe_to: [EventBroadcaster]}
  end

  @impl true
  def handle_events(events, _from, state) do
    Enum.each(events, fn event ->
      IO.puts("[AUDIT] #{inspect(event)}")
    end)
    {:noreply, [], state}
  end
end
```

> **Cuidado com o BroadcastDispatcher durante setup**: O primeiro lote de eventos pode ser entregue antes de todos os consumers se inscreverem. Use `demand: :accumulate` no init do producer e chame `GenStage.demand(producer, :forward)` depois que todos os consumers estiverem conectados.

```elixir
def init(:ok) do
  {:producer, state, dispatcher: GenStage.BroadcastDispatcher, demand: :accumulate}
end

# Depois de todos os consumers se inscreverem:
GenStage.demand(EventBroadcaster, :forward)
```

---

## Padrao 4: PartitionDispatcher (Roteamento por Chave)

Quando voce precisa rotear eventos para consumers especificos baseado em uma chave. Apenas UM consumer por particao.

```elixir
defmodule OrderProducer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  @impl true
  def init(:ok) do
    {:producer, {:queue.new(), 0},
     dispatcher: {
       GenStage.PartitionDispatcher,
       partitions: [:standard, :express, :international],
       hash: fn event ->
         # Retorna {evento, nome_da_particao}
         {event, event.shipping_type}
       end
     }}
  end

  # API publica
  def new_order(order) do
    GenStage.cast(__MODULE__, {:order, order})
  end

  @impl true
  def handle_cast({:order, order}, {queue, demand}) do
    queue = :queue.in(order, queue)
    dispatch(queue, demand, [])
  end

  @impl true
  def handle_demand(incoming, {queue, demand}) do
    dispatch(queue, incoming + demand, [])
  end

  defp dispatch(queue, 0, events),
    do: {:noreply, Enum.reverse(events), {queue, 0}}

  defp dispatch(queue, demand, events) do
    case :queue.out(queue) do
      {{:value, order}, queue} ->
        dispatch(queue, demand - 1, [order | events])
      {:empty, queue} ->
        {:noreply, Enum.reverse(events), {queue, demand}}
    end
  end
end

# Um consumer POR particao (obrigatorio)
defmodule OrderProcessor do
  use GenStage

  def start_link(partition) do
    GenStage.start_link(__MODULE__, partition)
  end

  @impl true
  def init(partition) do
    {:consumer, partition,
     subscribe_to: [
       {OrderProducer, partition: partition, max_demand: 20}
     ]}
  end

  @impl true
  def handle_events(orders, _from, partition) do
    Enum.each(orders, fn order ->
      IO.puts("[#{partition}] Processando pedido ##{order.id}")
    end)
    {:noreply, [], partition}
  end
end
```

Supervision:

```elixir
children = [
  {OrderProducer, []},
  Supervisor.child_spec({OrderProcessor, :standard}, id: :proc_standard),
  Supervisor.child_spec({OrderProcessor, :express}, id: :proc_express),
  Supervisor.child_spec({OrderProcessor, :international}, id: :proc_international)
]

Supervisor.start_link(children, strategy: :rest_for_one)
```

### Particoes com inteiros e hash automatico

```elixir
# Particoes 0, 1, 2, 3 com hash automatico via :erlang.phash2
{:producer, state,
 dispatcher: {GenStage.PartitionDispatcher, partitions: 0..3}}

# Inscricao:
{:consumer, state, subscribe_to: [{MyProducer, partition: 0}]}
```

> **Atencao**: O PartitionDispatcher assume distribuicao uniforme entre particoes. Se os dados sao muito desiguais por longos periodos, particoes ocupadas vao acumular no buffer enquanto particoes ociosas ficam paradas. Isso e aceitavel para picos temporarios, mas problematico para desbalanceamento constante.

### A funcao hash pode descartar eventos

```elixir
hash: fn event ->
  case event.priority do
    :low -> :none  # Evento descartado, nao vai para nenhuma particao
    _ -> {event, event.region}
  end
end
```

---

## Padrao 5: Rate Limiter (Controle Manual de Demanda)

Quando voce precisa controlar a taxa de processamento (ex: API com rate limit).

A chave e retornar `{:manual, state}` de `handle_subscribe/4` e usar `GenStage.ask/3` para controlar quando pedir mais eventos.

```elixir
defmodule RateLimitedConsumer do
  use GenStage

  def start_link(opts) do
    GenStage.start_link(__MODULE__, opts)
  end

  @impl true
  def init(_opts) do
    # Estado: mapa de producers com seus pending/interval
    {:consumer, %{}}
  end

  @impl true
  def handle_subscribe(:producer, opts, from, producers) do
    # Configura quantos eventos por intervalo
    pending = opts[:max_demand] || 1000
    interval = opts[:interval] || 5000

    producers = Map.put(producers, from, {pending, interval})
    producers = ask_and_schedule(producers, from)

    # :manual = EU controlo quando pedir mais eventos
    {:manual, producers}
  end

  @impl true
  def handle_cancel(_, from, producers) do
    {:noreply, [], Map.delete(producers, from)}
  end

  @impl true
  def handle_events(events, from, producers) do
    # Acumula pending para proxima janela de tempo
    producers =
      Map.update!(producers, from, fn {pending, interval} ->
        {pending + length(events), interval}
      end)

    # Processa os eventos
    Enum.each(events, &IO.inspect/1)

    {:noreply, [], producers}
  end

  @impl true
  def handle_info({:ask, from}, producers) do
    {:noreply, [], ask_and_schedule(producers, from)}
  end

  defp ask_and_schedule(producers, from) do
    case producers do
      %{^from => {pending, interval}} ->
        GenStage.ask(from, pending)
        Process.send_after(self(), {:ask, from}, interval)
        Map.put(producers, from, {0, interval})

      _ ->
        producers
    end
  end
end
```

### Uso

```elixir
{:ok, producer} = GenStage.start_link(MyProducer, 0)
{:ok, consumer} = GenStage.start_link(RateLimitedConsumer, :ok)

# 10 eventos a cada 2 segundos
GenStage.sync_subscribe(consumer, to: producer, max_demand: 10, interval: 2000)
```

---

## Padrao 6: ConsumerSupervisor (1 Processo por Evento)

Quando cada evento precisa ser processado por um processo filho separado. O `max_demand` age como limite de concorrencia (como um pool).

```elixir
defmodule JobProducer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def enqueue(job) do
    GenStage.cast(__MODULE__, {:enqueue, job})
  end

  @impl true
  def init(:ok) do
    {:producer, {:queue.new(), 0}}
  end

  @impl true
  def handle_cast({:enqueue, job}, {queue, demand}) do
    queue = :queue.in(job, queue)
    dispatch_jobs(queue, demand, [])
  end

  @impl true
  def handle_demand(incoming_demand, {queue, demand}) do
    dispatch_jobs(queue, incoming_demand + demand, [])
  end

  defp dispatch_jobs(queue, 0, events) do
    {:noreply, Enum.reverse(events), {queue, 0}}
  end

  defp dispatch_jobs(queue, demand, events) do
    case :queue.out(queue) do
      {{:value, job}, queue} ->
        dispatch_jobs(queue, demand - 1, [job | events])
      {:empty, queue} ->
        {:noreply, Enum.reverse(events), {queue, demand}}
    end
  end
end

defmodule JobWorkerSupervisor do
  use ConsumerSupervisor

  def start_link(_opts) do
    ConsumerSupervisor.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  @impl true
  def init(:ok) do
    # Filhos DEVEM ter restart: :temporary ou :transient
    children = [
      %{
        id: JobWorker,
        start: {JobWorker, :start_link, []},
        restart: :temporary
      }
    ]

    opts = [
      strategy: :one_for_one,
      subscribe_to: [{JobProducer, max_demand: 50}]
    ]

    ConsumerSupervisor.init(children, opts)
  end
end

defmodule JobWorker do
  def start_link(job) do
    Task.start_link(fn ->
      IO.puts("Processando job: #{inspect(job)}")
      Process.sleep(Enum.random(100..1000))
      IO.puts("Job concluido: #{inspect(job)}")
    end)
  end
end
```

> **Nota**: O `max_demand` no ConsumerSupervisor funciona como limite de concorrencia. Com `max_demand: 50`, no maximo 50 workers rodam simultaneamente. A media de filhos simultaneos e `(max_demand + min_demand) / 2`.

---

## Padrao 7: Producer com Buffer Automatico (Eventos Asincronos)

Quando eventos chegam de forma assincrona (webhooks, filas externas, etc.) e nao sob demanda.

```elixir
defmodule AsyncProducer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  # API publica - eventos chegam a qualquer momento
  def push(events) when is_list(events) do
    GenStage.cast(__MODULE__, {:push, events})
  end

  @impl true
  def init(:ok) do
    # buffer_size: quantos eventos armazenar quando nao ha demanda
    # buffer_keep: :last descarta os mais antigos quando excede, :first descarta os novos
    {:producer, :ok, buffer_size: 50_000, buffer_keep: :last}
  end

  @impl true
  def handle_demand(_demand, state) do
    # Nao temos eventos sob demanda - eles chegam via push/1
    {:noreply, [], state}
  end

  @impl true
  def handle_cast({:push, events}, state) do
    # Eventos sao automaticamente bufferizados se nao houver demanda
    # Se o buffer exceder buffer_size, um log de erro e emitido
    {:noreply, events, state}
  end
end
```

### Sobre o Buffer Automatico

- **`:producer`**: `buffer_size` padrao = `10_000`
- **`:producer_consumer`**: `buffer_size` padrao = `:infinity` (cuidado com memoria!)
- Quando o buffer excede o tamanho, eventos sao descartados e um log e emitido
- Customize o log implementando `format_discarded/2`:

```elixir
@impl true
def format_discarded(discarded_count, current_buffer_size) do
  "Descartados #{discarded_count} eventos. Buffer atual: #{current_buffer_size}"
end
```

---

## Padrao 8: Inscricao Dinamica (subscribe em runtime)

Quando voce nao sabe em tempo de compilacao quais producers existem.

```elixir
defmodule DynamicConsumer do
  use GenStage

  def start_link(opts) do
    GenStage.start_link(__MODULE__, opts)
  end

  def subscribe_to_producer(consumer, producer, opts \\ []) do
    # Retorna {:ok, subscription_tag} ou {:error, reason}
    GenStage.sync_subscribe(consumer, [{:to, producer} | opts])
  end

  def unsubscribe(consumer, subscription_tag, reason \\ :normal) do
    GenStage.cancel({subscription_tag, consumer}, reason)
  end

  @impl true
  def init(_opts) do
    # Inicia SEM inscricoes
    {:consumer, %{}}
  end

  @impl true
  def handle_subscribe(:producer, _opts, from, state) do
    IO.puts("Inscrito em: #{inspect(from)}")
    {:automatic, state}
  end

  @impl true
  def handle_cancel({:cancel, _}, from, state) do
    IO.puts("Desinscrito de: #{inspect(from)}")
    {:noreply, [], state}
  end

  @impl true
  def handle_events(events, {producer_pid, _ref}, state) do
    IO.puts("#{length(events)} eventos de #{inspect(producer_pid)}")
    {:noreply, [], state}
  end
end
```

### sync_subscribe vs async_subscribe

```elixir
# sync_subscribe: bloqueia ate o producer confirmar a inscricao
# Retorna {:ok, tag} ou {:error, reason}
{:ok, tag} = GenStage.sync_subscribe(consumer, to: producer, max_demand: 100)

# async_subscribe: nao bloqueia, inscricao acontece eventualmente
# Retorna {:ok, tag} imediatamente
{:ok, tag} = GenStage.async_subscribe(consumer, to: producer)
```

### Tipos de Cancelamento

```elixir
GenStage.sync_subscribe(consumer,
  to: producer,
  cancel: :permanent   # (padrao) consumer para se producer morrer
  # cancel: :transient # consumer para so se producer morrer com erro
  # cancel: :temporary # consumer NUNCA para por causa do producer
)
```

---

## Padrao 9: Usando GenStage com Streams do Elixir

Para integrar GenStage com o ecossistema de Streams (util para testes e scripts).

```elixir
# Criar um producer a partir de um Enumerable
{:ok, producer} = GenStage.from_enumerable(1..1_000_000)

# Criar um stream a partir de producers (consome como consumer)
GenStage.stream([{producer, max_demand: 100}])
|> Stream.map(&(&1 * 2))
|> Stream.take(10)
|> Enum.to_list()
# => [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
```

### Util para testes

```elixir
test "valida transformacao do pipeline" do
  {:ok, producer} = GenStage.from_enumerable([
    %{id: 1, total: 100},
    %{id: 2, total: -10},    # invalido
    %{id: 3, total: 200}
  ])

  {:ok, transformer} = GenStage.start_link(MyTransformer, :ok)
  GenStage.sync_subscribe(transformer, to: producer, max_demand: 10)

  results =
    GenStage.stream([{transformer, max_demand: 10}])
    |> Enum.to_list()

  assert length(results) == 2
end
```

---

## Padrao 10: Controle de Demanda (accumulate/forward)

Quando voce precisa acumular demanda antes de comecar a processar (ex: esperar que todos os consumers se inscrevam, ou esperar conexao com banco).

```elixir
defmodule DatabaseProducer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  # Chamado quando a conexao com o banco estiver pronta
  def start_producing do
    GenStage.demand(__MODULE__, :forward)
  end

  # Consultar o modo atual
  def demand_mode do
    GenStage.demand(__MODULE__)
  end

  @impl true
  def init(:ok) do
    # :accumulate = acumula demanda sem emitir eventos
    {:producer, :not_connected, demand: :accumulate}
  end

  @impl true
  def handle_demand(demand, state) do
    # So e chamado quando o modo e :forward
    events = fetch_from_db(demand)
    {:noreply, events, state}
  end

  defp fetch_from_db(count) do
    Enum.to_list(1..count)
  end
end
```

---

## Referencia Completa de Callbacks

### Obrigatorios

| Callback | Tipo | Assinatura | Descricao |
|----------|------|------------|-----------|
| `init/1` | Todos | `init(args)` | Retorna `{:producer, state, opts}`, `{:consumer, state, opts}` ou `{:producer_consumer, state, opts}`. Tambem aceita `:ignore` ou `{:stop, reason}` |
| `handle_demand/2` | Producer | `handle_demand(demand, state)` | Recebe demanda (sempre > 0). Retorna `{:noreply, events, new_state}` |
| `handle_events/3` | Consumer/PC | `handle_events(events, from, state)` | Recebe lista de eventos. `from` e `{producer_pid, subscription_tag}` |

### Opcionais

| Callback | Assinatura | Descricao |
|----------|------------|-----------|
| `handle_subscribe/4` | `handle_subscribe(:producer\|:consumer, opts, from, state)` | Controla modo da inscricao. Retorna `{:automatic, state}` ou `{:manual, state}` |
| `handle_cancel/3` | `handle_cancel(reason, from, state)` | Reage a cancelamento. `reason` e `{:cancel, _}`, `{:down, _}`, etc. |
| `handle_call/3` | `handle_call(request, from, state)` | Chamadas sincronas. Pode retornar `{:reply, reply, events, state}` |
| `handle_cast/2` | `handle_cast(request, state)` | Mensagens assincronas |
| `handle_info/2` | `handle_info(msg, state)` | Mensagens genericas |
| `terminate/2` | `terminate(reason, state)` | Limpeza ao parar |
| `format_status/2` | `format_status(reason, [pdict, state])` | Formata status do processo para debug |
| `format_discarded/2` | `format_discarded(discarded, buffered)` | Customiza mensagem de log quando buffer excede |

### Retornos Possiveis

```elixir
# De handle_demand, handle_events, handle_cast, handle_info:
{:noreply, events, new_state}
{:noreply, events, new_state, :hibernate}
{:stop, reason, new_state}

# De handle_call (adiciona opcao de reply):
{:reply, reply, events, new_state}
{:reply, reply, events, new_state, :hibernate}
{:noreply, events, new_state}
{:stop, reason, reply, new_state}
{:stop, reason, new_state}

# De handle_subscribe:
{:automatic, new_state}   # demanda automatica (padrao)
{:manual, new_state}      # voce controla via GenStage.ask/3

# De handle_cancel:
{:noreply, events, new_state}
```

> **Nota**: Em TODOS os callbacks, o campo `events` DEVE ser `[]` para consumers. Producers e producer_consumers podem emitir eventos.

---

## Referencia Completa de Dispatchers

### DemandDispatcher (padrao)

Envia eventos para o consumer com maior demanda pendente. Ordenacao FIFO.

```elixir
{:producer, state}  # usa DemandDispatcher por padrao

# Ou explicitamente com opcoes:
{:producer, state,
 dispatcher: {GenStage.DemandDispatcher,
   shuffle_demands_on_first_dispatch: true,  # evita sobrecarregar o 1o consumer
   max_demand: 1000                           # emite warning se consumer pedir mais
 }}
```

> **Regra**: Todos os consumers de um mesmo producer com DemandDispatcher devem ter o MESMO `max_demand`. Caso contrario, consumers "gulosos" (com max_demand maior) recebem mais eventos.

### BroadcastDispatcher

Envia TODOS os eventos para TODOS os consumers. Aguarda a demanda minima de todos antes de enviar.

```elixir
{:producer, state, dispatcher: GenStage.BroadcastDispatcher}

# Consumer com filtro:
{:consumer, state, subscribe_to: [
  {producer, selector: fn event -> event.important? end}
]}
```

> **Regra**: Um mesmo processo NAO pode se inscrever duas vezes. O BroadcastDispatcher rejeita com `:already_subscribed`.

### PartitionDispatcher

Roteia eventos para particoes fixas. Exatamente 1 consumer por particao.

```elixir
{:producer, state,
 dispatcher: {GenStage.PartitionDispatcher,
   partitions: [:odd, :even],  # ou inteiro: partitions: 4  (gera 0..3)
   hash: fn event ->
     case rem(event, 2) do
       0 -> {event, :even}
       1 -> {event, :odd}
     end
   end
 }}

# Consumer DEVE especificar particao:
{:consumer, state, subscribe_to: [{producer, partition: :even}]}
```

> **Regras**:
> - Se `:partitions` usa nomes nao-inteiros, voce DEVE fornecer `:hash`
> - A funcao hash pode retornar `:none` para descartar o evento
> - Apenas 1 consumer por particao (erro se tentar 2)

---

## Funcoes da API Publica

### Ciclo de Vida

```elixir
GenStage.start_link(module, args, opts)     # Inicia com link ao processo pai
GenStage.start(module, args, opts)          # Inicia sem link
GenStage.stop(stage, reason \\ :normal, timeout \\ :infinity)
```

### Inscricao

```elixir
GenStage.sync_subscribe(stage, opts)                        # Bloqueante
GenStage.async_subscribe(stage, opts)                       # Nao-bloqueante
GenStage.sync_resubscribe(stage, tag, reason, to, opts)     # Cancela e reinscreve
GenStage.async_resubscribe(stage, tag, reason, opts)        # Idem, async
GenStage.cancel({tag, stage}, reason)                       # Cancela inscricao
```

### Controle de Demanda

```elixir
GenStage.ask(from, demand)                  # Pede eventos (so modo :manual)
GenStage.demand(stage)                      # Consulta modo (:forward ou :accumulate)
GenStage.demand(stage, :forward)            # Ativa envio de eventos
GenStage.demand(stage, :accumulate)         # Pausa envio, acumula demanda
```

### Comunicacao (compativel com GenServer)

```elixir
GenStage.call(stage, request, timeout \\ 5000)
GenStage.cast(stage, request)
GenStage.reply(from, reply)
GenStage.sync_info(stage, msg, timeout \\ 5000)  # Enfileira info (respeita ordem com eventos)
GenStage.async_info(stage, msg)                   # Idem, async
```

### Utilitarios

```elixir
GenStage.from_enumerable(enumerable, opts \\ [])  # Cria producer de enumerable
GenStage.stream(subscriptions, opts \\ [])          # Cria stream de producers
GenStage.estimate_buffered_count(stage, timeout \\ 5000)  # Tamanho estimado do buffer
```

---

## Boas Praticas e Armadilhas

### FACA

1. **Use GenStage para concorrencia e transferencia de dados**, nao para organizar codigo ou modelar dominios
2. **Combine passos logicos no mesmo stage** quando possivel - cada stage adiciona overhead de processo e mensagens
3. **Escale com multiplos consumers** em vez de mais stages intermediarios
4. **Use `Task.async_stream/2`** para paralelismo simples antes de recorrer ao GenStage
5. **Configure `max_demand` igual em todos os consumers** de um mesmo producer com DemandDispatcher
6. **Use `strategy: :rest_for_one`** no Supervisor
7. **Use `:subscribe_to` no init** ao inves de subscribe manual - garante re-inscricao apos crashes
8. **Trate `handle_cancel/3`** para limpar estado quando um producer cai

### NAO FACA

1. **Nao crie pipelines longos** com um stage por passo logico
2. **Nao use `max_demand: 1`** exceto para debug - mata performance (sem batching)
3. **Nao misture consumers com `max_demand` diferentes** no DemandDispatcher
4. **Nao esqueça que `producer_consumer` tem `buffer_size: :infinity`** por padrao
5. **Nao ignore o buffer** - monitore com `GenStage.estimate_buffered_count/2`
6. **Nao faca trabalho assincrono em `handle_events/3`** com modo `:automatic` - a demanda e enviada logo apos o retorno; se precisa de async, use modo `:manual`

### Quando usar GenStage vs Alternativas

| Cenario | Solucao |
|---------|---------|
| Paralelismo simples sobre dados em memoria | `Task.async_stream/2` |
| Pipeline com back-pressure customizado | **GenStage** |
| Pipeline com janelas/reducoes/particionamento | **Flow** (construido sobre GenStage) |
| Ingestao de dados (Kafka, SQS, RabbitMQ) | **Broadway** (construido sobre GenStage) |
| Pub/sub simples | `Phoenix.PubSub` ou `Registry` |

---

## Protocolo de Mensagens (Avancado)

GenStage usa um protocolo de mensagens interno para comunicacao entre stages. Util se voce precisa implementar stages customizados ou debugar:

### Consumer -> Producer

```elixir
# Inscricao
{:"$gen_producer", {consumer_pid, subscription_tag}, {:subscribe, current, options}}

# Cancelamento
{:"$gen_producer", {consumer_pid, subscription_tag}, {:cancel, reason}}

# Pedido de demanda
{:"$gen_producer", {consumer_pid, subscription_tag}, {:ask, demand}}
```

### Producer -> Consumer

```elixir
# Cancelamento (confirmacao ou iniciado pelo producer)
{:"$gen_consumer", {producer_pid, subscription_tag}, {:cancel, reason}}

# Envio de eventos (lista nao-vazia)
{:"$gen_consumer", {producer_pid, subscription_tag}, events}
```

> Ao receber inscricao, o producer DEVE monitorar o consumer. O consumer DEVE monitorar o producer ANTES de enviar a inscricao.

---

## Exemplo Completo: Sistema de Processamento de Pedidos

Exemplo realista com producer assincrono, validacao e persistencia em batch:

```elixir
# lib/my_app/pipeline/order_producer.ex
defmodule MyApp.Pipeline.OrderProducer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  def new_order(order) do
    GenStage.cast(__MODULE__, {:new_order, order})
  end

  @impl true
  def init(:ok) do
    {:producer, {:queue.new(), 0}, buffer_size: 10_000}
  end

  @impl true
  def handle_cast({:new_order, order}, {queue, demand}) do
    queue = :queue.in(order, queue)
    dispatch(queue, demand, [])
  end

  @impl true
  def handle_demand(incoming, {queue, demand}) do
    dispatch(queue, incoming + demand, [])
  end

  defp dispatch(queue, 0, events),
    do: {:noreply, Enum.reverse(events), {queue, 0}}

  defp dispatch(queue, demand, events) do
    case :queue.out(queue) do
      {{:value, order}, queue} ->
        dispatch(queue, demand - 1, [order | events])
      {:empty, queue} ->
        {:noreply, Enum.reverse(events), {queue, demand}}
    end
  end
end

# lib/my_app/pipeline/order_consumer.ex
defmodule MyApp.Pipeline.OrderConsumer do
  use GenStage

  def start_link(_opts) do
    GenStage.start_link(__MODULE__, :ok)
  end

  @impl true
  def init(:ok) do
    {:consumer, :ok,
     subscribe_to: [{MyApp.Pipeline.OrderProducer, max_demand: 50}]}
  end

  @impl true
  def handle_events(orders, _from, state) do
    orders
    |> Enum.map(&validate/1)
    |> Enum.filter(&match?({:ok, _}, &1))
    |> Enum.map(fn {:ok, order} -> order end)
    |> persist_batch()

    {:noreply, [], state}
  end

  defp validate(order) do
    cond do
      is_nil(order.customer_id) -> {:error, :missing_customer}
      order.total <= 0 -> {:error, :invalid_total}
      true -> {:ok, Map.put(order, :validated_at, DateTime.utc_now())}
    end
  end

  defp persist_batch([]), do: :ok
  defp persist_batch(orders) do
    entries = Enum.map(orders, fn order ->
      %{
        customer_id: order.customer_id,
        total: order.total,
        validated_at: order.validated_at,
        inserted_at: DateTime.utc_now()
      }
    end)

    MyApp.Repo.insert_all("orders", entries)
  end
end

# lib/my_app/pipeline/supervisor.ex
defmodule MyApp.Pipeline.Supervisor do
  use Supervisor

  def start_link(opts) do
    Supervisor.start_link(__MODULE__, opts, name: __MODULE__)
  end

  @impl true
  def init(_opts) do
    children = [
      MyApp.Pipeline.OrderProducer,
      # 4 consumers processando em paralelo
      Supervisor.child_spec({MyApp.Pipeline.OrderConsumer, []}, id: :consumer_1),
      Supervisor.child_spec({MyApp.Pipeline.OrderConsumer, []}, id: :consumer_2),
      Supervisor.child_spec({MyApp.Pipeline.OrderConsumer, []}, id: :consumer_3),
      Supervisor.child_spec({MyApp.Pipeline.OrderConsumer, []}, id: :consumer_4)
    ]

    Supervisor.init(children, strategy: :rest_for_one)
  end
end
```

### Uso

```elixir
# Em qualquer parte da aplicacao:
MyApp.Pipeline.OrderProducer.new_order(%{
  customer_id: 42,
  total: 99.90,
  items: ["item_a", "item_b"]
})
```

---

## Diagrama de Decisao: Qual Dispatcher Usar?

```
Todos os consumers precisam de todos os eventos?
  |
  |-- SIM --> BroadcastDispatcher
  |            |
  |            +-- Cada consumer quer apenas um subconjunto?
  |                  |-- SIM --> Use :selector na inscricao
  |                  |-- NAO --> Inscricao simples
  |
  |-- NAO --> Eventos devem ir para consumers especificos por chave?
               |
               |-- SIM --> PartitionDispatcher
               |            (defina :hash e :partitions)
               |
               |-- NAO --> DemandDispatcher (padrao)
                            (distribuicao por demanda, tipo round-robin)
```

---

## Checklist para Implementacao

Ao criar um pipeline GenStage, verifique:

- [ ] Cada stage tem `use GenStage` ou `use ConsumerSupervisor`
- [ ] Producers implementam `handle_demand/2`
- [ ] Consumers/ProducerConsumers implementam `handle_events/3`
- [ ] Consumers retornam `[]` como lista de eventos
- [ ] `max_demand` esta configurado adequadamente (nao muito alto, nao muito baixo)
- [ ] Consumers do mesmo producer com DemandDispatcher tem o mesmo `max_demand`
- [ ] `buffer_size` esta configurado para producers que recebem eventos de forma assincrona
- [ ] `buffer_size` de `producer_consumer` esta explicitamente definido (padrao e `:infinity`)
- [ ] Supervision tree usa `strategy: :rest_for_one`
- [ ] Stages estao na ordem correta na supervision tree (producer primeiro)
- [ ] `subscribe_to` esta no `init/1` (nao fazendo subscribe manual) para auto-reinscricao
- [ ] Se usando BroadcastDispatcher, considerou `demand: :accumulate` durante setup
- [ ] Se fazendo trabalho async, usando modo `:manual` com `GenStage.ask/3`
- [ ] Voce considerou se `Task.async_stream/2` seria suficiente para seu caso
