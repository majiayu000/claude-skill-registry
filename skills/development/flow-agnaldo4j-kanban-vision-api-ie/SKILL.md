---
name: flow
description: >
  Use when working with the Flow library for parallel data processing in Elixir.
  Covers Flow fundamentals, partitioning, windows, joins, departition, and
  performance tuning. Built on top of GenStage for concurrent pipelines.
---

# Flow - Skill Completa para Desenvolvedores Elixir

Guia prático e completo para usar a biblioteca Flow em projetos Elixir.

## O que e Flow?

Flow permite expressar computacoes paralelas sobre colecoes em Elixir, similar ao `Enum` e `Stream`, mas executando operacoes em paralelo usando processos `GenStage`. E ideal para processamento de grandes volumes de dados (bounded ou unbounded).

> **Regra de ouro**: Flow mostra melhorias reais com colecoes grandes. Por padrao trabalha em batches de 500 itens.

---

## 1. Instalacao

```elixir
# mix.exs
def deps do
  [{:flow, "~> 1.0"}]
end
```

```bash
mix deps.get
```

---

## 2. Conceitos Fundamentais

### Enum vs Stream vs Flow

```elixir
# Enum: carrega TUDO em memoria, sequencial
File.stream!("grande.txt")
|> Enum.flat_map(&String.split(&1, " "))
|> Enum.reduce(%{}, fn word, acc -> Map.update(acc, word, 1, &(&1 + 1)) end)

# Stream: lazy, sequencial, um item por vez
File.stream!("grande.txt")
|> Stream.flat_map(&String.split(&1, " "))
|> Enum.reduce(%{}, fn word, acc -> Map.update(acc, word, 1, &(&1 + 1)) end)

# Flow: lazy, PARALELO, em batches
File.stream!("grande.txt")
|> Flow.from_enumerable()
|> Flow.flat_map(&String.split(&1, " "))
|> Flow.partition()
|> Flow.reduce(fn -> %{} end, fn word, acc ->
  Map.update(acc, word, 1, &(&1 + 1))
end)
|> Enum.to_list()
```

### O Pipeline de Execucao

```
[Producers]           # fonte de dados
     |
[Mapper Stages]       # map, filter, flat_map (paralelo, stateless)
     |
[PartitionDispatcher] # roteia dados por hash
     |
[Reducer Stages]      # reduce, group_by (paralelo por particao, stateful)
     |
[Consumer/Output]     # Enum.to_list, start_link, etc.
```

### As 3 Fases de um Stage

1. **Mapping/Filtering** - `map/2`, `filter/2`, `flat_map/2`, `reject/2`
2. **Reducing** - `reduce/3`, `group_by/3`, `emit_and_reduce/3`
3. **Emitting** - `emit/2`, `on_trigger/2`

> **Regra**: mappers NAO podem vir depois de reducers na mesma particao. Reducers so podem aparecer UMA vez por particao.

---

## 3. Criando Flows - Fontes de Dados

### A partir de Enumerables

```elixir
# Uma fonte
[1, 2, 3, 4, 5]
|> Flow.from_enumerable()
|> Flow.map(&(&1 * 2))
|> Enum.to_list()

# Multiplas fontes (RECOMENDADO para evitar gargalos)
streams = for file <- File.ls!("data/") do
  File.stream!(Path.join("data", file), read_ahead: 100_000)
end

streams
|> Flow.from_enumerables()
|> Flow.flat_map(&String.split(&1, " "))
|> Flow.partition()
|> Flow.reduce(fn -> %{} end, fn word, acc ->
  Map.update(acc, word, 1, &(&1 + 1))
end)
|> Enum.to_list()
```

### A partir de GenStage producers

```elixir
# Producers ja rodando
Flow.from_stages([pid1, pid2, pid3])
|> Flow.map(&process/1)
|> Enum.to_list()

# Child specs (producers iniciados junto com o flow)
specs = [{MyProducer, arg1}, {MyProducer, arg2}]
Flow.from_specs(specs)
|> Flow.map(&process/1)
|> Flow.start_link()
```

---

## 4. Operacoes de Mapeamento (Stateless, Paralelas)

```elixir
flow = Flow.from_enumerable(1..1000)

# map - transforma cada elemento
flow |> Flow.map(&(&1 * 2))

# flat_map - transforma e achata
flow |> Flow.flat_map(fn x -> [x, x * 2] end)

# filter - filtra elementos
flow |> Flow.filter(&(rem(&1, 2) == 0))

# reject - rejeita elementos (inverso do filter)
flow |> Flow.reject(&(rem(&1, 2) == 0))

# map_values - mapeia valores de tuplas {key, value}
Flow.from_enumerable([a: 1, b: 2])
|> Flow.map_values(&(&1 * 2))
# => [a: 2, b: 4]

# map_batch - processa o batch inteiro ANTES de map/reduce
# Util para preload de dados
Flow.from_enumerable(user_ids)
|> Flow.map_batch(fn ids ->
  users = Repo.all(from u in User, where: u.id in ^ids)
  users_map = Map.new(users, &{&1.id, &1})
  Enum.map(ids, &Map.fetch!(users_map, &1))
end)
|> Flow.map(&process_user/1)
```

---

## 5. Particionamento - O Coracao do Flow

Particionamento garante que dados relacionados vao para o mesmo stage.

```elixir
# Particionamento padrao (hash do elemento inteiro)
flow |> Flow.partition()

# Por campo de tupla
flow |> Flow.partition(key: {:elem, 0})   # primeiro elem da tupla

# Por chave de mapa
flow |> Flow.partition(key: {:key, :user_id})

# Por funcao customizada
flow |> Flow.partition(key: fn event -> event.category end)

# Hash customizado (controle total do roteamento)
flow |> Flow.partition(hash: fn event ->
  {event, :erlang.phash2(event.user_id, _num_partitions = 4)}
end)

# Numero de stages (padrao: System.schedulers_online())
flow |> Flow.partition(stages: 8)
```

### Quando usar partition?

- **USE** quando precisa agrupar dados (contagem de palavras, aggregacoes por chave)
- **NAO USE** para problemas "embarrassingly parallel" (cada item e independente)
- Particionamento desnecessario aumenta uso de memoria e reduz throughput

### Shuffle vs Partition

```elixir
# shuffle - redistribui sem garantia de agrupamento (DemandDispatcher)
flow |> Flow.shuffle(stages: 4)

# partition - agrupa por hash (PartitionDispatcher)
flow |> Flow.partition(stages: 4)
```

---

## 6. Operacoes de Reducao (Stateful, por Particao)

### reduce

```elixir
# Acumulador e funcao redutora
Flow.from_enumerable(words)
|> Flow.partition()
|> Flow.reduce(fn -> %{} end, fn word, acc ->
  Map.update(acc, word, 1, &(&1 + 1))
end)
|> Enum.to_list()
# => [{"hello", 3}, {"world", 2}, ...]
```

### group_by

```elixir
# Agrupa por chave
Flow.from_enumerable(~w[the quick brown fox], stages: 1)
|> Flow.group_by(&String.length/1)
|> Enum.to_list()
# => [{3, ["fox", "the"]}, {5, ["brown", "quick"]}]

# group_by_key para tuplas {key, value}
Flow.from_enumerable([foo: 1, foo: 2, bar: 3])
|> Flow.group_by_key()
|> Flow.emit(:state)
|> Enum.to_list()
# => [%{foo: [2, 1], bar: [3]}]
```

### emit_and_reduce (emite E reduz ao mesmo tempo)

```elixir
# Sliding window de 3 elementos
Flow.from_enumerable(1..5, stages: 1)
|> Flow.emit_and_reduce(fn -> [] end, fn event, acc ->
  acc = [event | acc] |> Enum.take(3)
  {[Enum.reverse(acc)], acc}
end)
|> Enum.filter(&is_list/1)
# => [[1], [1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
```

### uniq / uniq_by

```elixir
# Elementos unicos (por particao!)
Flow.from_enumerable(1..100)
|> Flow.partition(stages: 1)
|> Flow.uniq_by(&rem(&1, 2))
|> Enum.sort()
# => [1, 2]
```

> **Atencao**: `uniq_by` funciona POR PARTICAO. Para unicidade global, particione pela mesma chave usada no uniq_by.

---

## 7. Controlando a Emissao de Resultados

### emit/2

```elixir
# :events - emite os eventos processados (padrao)
flow |> Flow.reduce(...) |> Flow.emit(:events)

# :state - emite o estado acumulado como um unico evento
flow |> Flow.reduce(...) |> Flow.emit(:state)

# :nothing - nao emite nada (side-effects only)
flow |> Flow.reduce(...) |> Flow.emit(:nothing)
```

### on_trigger/2 (controle total)

```elixir
# Aridade 1: so recebe o estado
flow
|> Flow.reduce(fn -> %{} end, &Map.put(&2, &1, true))
|> Flow.on_trigger(fn map ->
  {[map_size(map)], map}  # {eventos_emitidos, novo_acumulador}
end)

# Aridade 2: recebe estado + info da particao
flow
|> Flow.reduce(fn -> %{} end, reducer_fn)
|> Flow.on_trigger(fn state, {partition_index, total_partitions} ->
  {[state], state}
end)

# Aridade 3: recebe estado + particao + info da window/trigger
flow
|> Flow.reduce(fn -> %{} end, reducer_fn)
|> Flow.on_trigger(fn state, _partition, {window_type, window_id, trigger_name} ->
  IO.puts("Window #{window_type}/#{window_id} triggered by #{inspect(trigger_name)}")
  {[state], %{}}  # emite estado e reseta acumulador
end)
```

---

## 8. Windows - Dividindo Dados no Tempo

### Global Window (padrao)

```elixir
# Todos os eventos em uma unica janela
window = Flow.Window.global()

# Com trigger a cada 10 eventos
window = Flow.Window.global() |> Flow.Window.trigger_every(10)

Flow.from_enumerable(1..100)
|> Flow.partition(window: window, stages: 1)
|> Flow.reduce(fn -> 0 end, &(&1 + &2))
|> Flow.emit(:state)
|> Enum.to_list()
# => [55, 210, 465, 820, 1275, 1830, 2485, 3240, 4095, 5050, 5050]
#     ^cada trigger emite soma parcial          ^ultimo e o :done
```

### Fixed Window (event time)

```elixir
# Janelas de 1 hora baseadas no timestamp do evento
window = Flow.Window.fixed(1, :hour, fn {_word, timestamp} -> timestamp end)

data = [
  {"elixir", 0}, {"elixir", 1_000}, {"erlang", 60_000},
  {"concurrency", 3_200_000}, {"elixir", 4_000_000},
  {"erlang", 5_000_000}, {"erlang", 6_000_000}
]

Flow.from_enumerable(data, max_demand: 5, stages: 1)
|> Flow.partition(window: window, stages: 1)
|> Flow.reduce(fn -> %{} end, fn {word, _}, acc ->
  Map.update(acc, word, 1, &(&1 + 1))
end)
|> Flow.emit(:state)
|> Enum.to_list()
# => [%{"elixir" => 2, "erlang" => 1, "concurrency" => 1},
#     %{"elixir" => 1, "erlang" => 2}]
```

### Fixed Window com Lateness (dados atrasados)

```elixir
window =
  Flow.Window.fixed(1, :hour, fn {_word, timestamp} -> timestamp end)
  |> Flow.Window.allowed_lateness(5, :minute)

# Agora a window emite :watermark quando termina,
# e :done so apos o periodo de latencia
```

### Count Window

```elixir
# Nova janela a cada 10 eventos
window = Flow.Window.count(10)

Flow.from_enumerable(1..100)
|> Flow.partition(window: window, stages: 1)
|> Flow.reduce(fn -> 0 end, &(&1 + &2))
|> Flow.emit(:state)
|> Enum.to_list()
# => [55, 155, 255, 355, 455, 555, 655, 755, 855, 955, 0]
```

### Periodic Window (processing time)

```elixir
# Nova janela a cada 5 segundos
window = Flow.Window.periodic(5, :second)
```

### Triggers

```elixir
# Trigger a cada N elementos
window = Flow.Window.global() |> Flow.Window.trigger_every(100)

# Trigger periodico (processing time, impreciso por natureza)
window = Flow.Window.global() |> Flow.Window.trigger_periodically(1, :second)

# Trigger customizado (punctuation)
window = Flow.Window.global()
|> Flow.Window.trigger(
  fn -> 0 end,  # acumulador inicial do trigger
  fn events, count ->
    length = length(events)
    if count + length >= 1000 do
      {pre, pos} = Enum.split(events, 1000 - count)
      {:trigger, :my_checkpoint, pre, pos, 0}
    else
      {:cont, count + length}
    end
  end
)

# Trigger por mensagem (timers customizados)
# Envie {:trigger, name} para self() dentro do accumulator
flow
|> Flow.reduce(fn ->
  Process.send_after(self(), {:trigger, :my_timer}, 5_000)
  %{}
end, reducer_fn)
```

### Info do Trigger no on_trigger/2

```elixir
# O terceiro argumento do on_trigger revela o que causou o trigger:
# {:global, :global, :done}                    - global window finalizada
# {:global, :global, {:every, 20}}             - trigger_every
# {:global, :global, {:periodically, 1, :second}} - trigger_periodically
# {:fixed, window_timestamp, :done}            - fixed window finalizada
# {:fixed, window_timestamp, :watermark}       - watermark (antes do lateness)
# {:count, window_index, :done}                - count window finalizada
```

---

## 9. Joins - Combinando Dois Flows

### bounded_join (dados finitos)

```elixir
posts = [%{id: 1, title: "hello"}, %{id: 2, title: "world"}]
comments = [{1, "excellent"}, {1, "outstanding"}, {2, "great"}, {3, "unknown"}]

flow = Flow.bounded_join(
  :inner,                                    # :inner | :left_outer | :right_outer | :full_outer
  Flow.from_enumerable(posts),               # flow esquerdo
  Flow.from_enumerable(comments),            # flow direito
  & &1.id,                                   # chave esquerda
  & elem(&1, 0),                             # chave direita
  fn post, {_id, comment} ->                 # funcao de join
    Map.put(post, :comment, comment)
  end
)

Enum.sort(flow)
# => [%{id: 1, title: "hello", comment: "excellent"},
#     %{id: 1, title: "hello", comment: "outstanding"},
#     %{id: 2, title: "world", comment: "great"}]
```

### window_join (com janelas)

```elixir
window = Flow.Window.fixed(1, :hour, fn
  {_, _, timestamp} -> timestamp
  %{timestamp: timestamp} -> timestamp
end)

Flow.window_join(:inner, left_flow, right_flow, window,
  &left_key/1, &right_key/1, &join_fn/2, stages: 4)
```

---

## 10. Departition - Mergindo Resultados de Particoes

```elixir
# Conta palavras e merge todos os resultados em um unico mapa
File.stream!("arquivo.txt")
|> Flow.from_enumerable()
|> Flow.flat_map(&String.split/1)
|> Flow.partition()
|> Flow.reduce(fn -> %{} end, fn word, acc ->
  Map.update(acc, word, 1, &(&1 + 1))
end)
|> Flow.departition(
  fn -> Map.new() end,                                    # acumulador inicial
  fn partition_state, acc -> Map.merge(partition_state, acc) end,  # merge
  fn acc -> acc end                                        # finalizacao
)
|> Enum.to_list()
# => [%{"hello" => 5, "world" => 3, ...}]  # um unico mapa consolidado
```

### take_sort (top N)

```elixir
urls = ~w(www.foo.com www.bar.com www.foo.com www.foo.com www.baz.com)

urls
|> Flow.from_enumerable()
|> Flow.partition()
|> Flow.reduce(fn -> %{} end, fn url, map ->
  Map.update(map, url, 1, &(&1 + 1))
end)
|> Flow.take_sort(3, fn {_url_a, count_a}, {_url_b, count_b} ->
  count_b <= count_a
end)
|> Enum.to_list()
# => [[{"www.foo.com", 3}, {"www.bar.com", 1}, {"www.baz.com", 1}]]
```

---

## 11. Flows Supervisionados (Producao)

### Inline na supervision tree

```elixir
children = [
  {Flow,
   Flow.from_specs([{MyProducer, []}])
   |> Flow.map(&process/1)
   |> Flow.partition()
   |> Flow.reduce(fn -> %{} end, &aggregate/2)}
]

Supervisor.start_link(children, strategy: :one_for_one)
```

### Modulo dedicado

```elixir
defmodule MyApp.WordCounter do
  use Flow

  def start_link(_opts) do
    Flow.from_specs([{MyApp.EventProducer, []}])
    |> Flow.flat_map(&String.split(&1, " "))
    |> Flow.partition()
    |> Flow.reduce(fn -> %{} end, fn word, acc ->
      Map.update(acc, word, 1, &(&1 + 1))
    end)
    |> Flow.start_link()
  end
end

# Na supervision tree:
children = [MyApp.WordCounter]
```

### Com consumers externos (into_stages / into_specs)

```elixir
# Consumers ja rodando
{:ok, pid} = Flow.into_stages(flow, [consumer_pid1, consumer_pid2])

# Consumer specs iniciados junto
consumer_specs = [{MyConsumer, arg, []}]
{:ok, pid} = Flow.into_specs(flow, [{MyConsumer, []}])
```

### Com producer_consumers intermediarios (through_stages / through_specs)

```elixir
# Passar por producer_consumers existentes
flow
|> Flow.through_stages([rate_limiter_pid])
|> Flow.partition()
|> Flow.reduce(...)
|> Flow.start_link()

# Ou com specs
flow
|> Flow.through_specs([{RateLimiter, [], []}])
|> Flow.partition()
|> Flow.reduce(...)
|> Flow.start_link()
```

---

## 12. Patterns e Receitas Praticas

### Contagem de Palavras (completo e otimizado)

```elixir
empty_space = :binary.compile_pattern(" ")
parent = self()

File.stream!("big_file.txt", read_ahead: 100_000)
|> Flow.from_enumerable()
|> Flow.flat_map(&String.split(&1, empty_space))
|> Flow.partition()
|> Flow.reduce(fn -> :ets.new(:words, []) end, fn word, ets ->
  :ets.update_counter(ets, word, {2, 1}, {word, 0})
  ets
end)
|> Flow.on_trigger(fn ets ->
  :ets.give_away(ets, parent, [])
  {[ets], :unused}
end)
|> Enum.to_list()
```

### Processamento de Multiplos Arquivos

```elixir
streams = for file <- File.ls!("data/") do
  File.stream!(Path.join("data", file), read_ahead: 100_000)
end

streams
|> Flow.from_enumerables()
|> Flow.flat_map(&parse_line/1)
|> Flow.partition(key: {:key, :category})
|> Flow.reduce(fn -> %{} end, &aggregate/2)
|> Enum.to_list()
```

### Pipeline ETL

```elixir
Flow.from_enumerable(source_stream)
|> Flow.map(&extract/1)               # Extract
|> Flow.filter(&valid?/1)
|> Flow.partition(key: {:key, :id})
|> Flow.map(&transform/1)             # Transform
|> Flow.reduce(fn -> [] end, fn record, acc ->
  [record | acc]                       # Batch
end)
|> Flow.on_trigger(fn batch ->
  load(batch)                          # Load
  {[], []}                             # Reset batch
end)
|> Flow.run()
```

### Session Windows (gap entre eventos)

```elixir
max_gap = 1_000_000  # 1 segundo em microsegundos

Flow.from_enumerable(events)
|> Flow.partition(key: fn {k, _} -> k end, stages: 1)
|> Flow.emit_and_reduce(fn -> %{} end, fn {word, time}, acc ->
  {count, previous_time} = Map.get(acc, word, {1, time})

  if time - previous_time > max_gap do
    {[{word, {count, previous_time}}], Map.put(acc, word, {1, time})}
  else
    {[], Map.update(acc, word, {1, time}, fn {count, _} -> {count + 1, time} end)}
  end
end)
|> Flow.on_trigger(fn acc -> {Enum.to_list(acc), :unused} end)
|> Enum.to_list()
```

### Streaming com Checkpoints

```elixir
window =
  Flow.Window.global()
  |> Flow.Window.trigger_every(1000)
  |> Flow.Window.trigger_periodically(30, :second)

Flow.from_specs([{EventSource, []}])
|> Flow.partition(window: window)
|> Flow.reduce(fn -> %{} end, &process_event/2)
|> Flow.on_trigger(fn state, _partition, {_, _, trigger} ->
  case trigger do
    {:every, _} -> save_checkpoint(state)
    {:periodically, _, _} -> log_progress(state)
    :done -> save_final(state)
  end
  {[], state}
end)
|> Flow.start_link()
```

---

## 13. Uso em Livebook

```elixir
# Opcao 1: stream nao-linkado (RECOMENDADO)
Flow.from_enumerable([1, 2, 3])
|> Flow.map(&(&1 * 2))
|> Flow.stream(link: false)
|> Enum.to_list()

# Opcao 2: trap exits antes do flow
Process.flag(:trap_exit, true)
```

---

## 14. Performance e Tuning

### Demand (controle de batch)

```elixir
# max_demand: tamanho maximo do batch (padrao: 500)
# min_demand: quando pedir mais dados (padrao: max_demand / 2)
# O batch efetivo e max_demand - min_demand

# Para IO-bound: batches menores
Flow.from_enumerable(stream, max_demand: 20, min_demand: 5)

# Para CPU-bound com dados grandes: batches maiores (padrao ja e bom)
Flow.from_enumerable(stream, max_demand: 1000)

# Para testes/debug: force 1 por vez
Flow.from_enumerable(stream, max_demand: 1)
```

### Numero de Stages

```elixir
# Padrao: System.schedulers_online() (numero de cores)
# CPU-bound: mantenha o padrao
flow |> Flow.partition(stages: System.schedulers_online())

# IO-bound: aumente
flow |> Flow.partition(stages: System.schedulers_online() * 2)
```

### Evite fontes unicas

```elixir
# RUIM: um unico arquivo grande e gargalo
File.stream!("huge_file.txt") |> Flow.from_enumerable()

# BOM: multiplos arquivos menores
streams = Enum.map(files, &File.stream!(&1, read_ahead: 100_000))
Flow.from_enumerables(streams)
```

### Use ETS para contadores

```elixir
# Mapas geram muito garbage em contadores grandes
# ETS e muito mais eficiente para update_counter
Flow.reduce(fn -> :ets.new(:t, []) end, fn item, ets ->
  :ets.update_counter(ets, item, {2, 1}, {item, 0})
  ets
end)
```

### Compile patterns binarios

```elixir
# RUIM: recompila o pattern a cada split
Flow.flat_map(&String.split(&1, " "))

# BOM: compila uma vez
pattern = :binary.compile_pattern(" ")
Flow.flat_map(&String.split(&1, pattern))
```

---

## 15. Referencia Rapida da API

### Fontes de Dados
| Funcao | Descricao |
|--------|-----------|
| `from_enumerable/2` | Uma fonte enumerable |
| `from_enumerables/2` | Lista de enumerables |
| `from_stages/2` | Producers ja rodando |
| `from_specs/2` | Child specs de producers |

### Mappers (stateless, paralelos)
| Funcao | Descricao |
|--------|-----------|
| `map/2` | Transforma cada elemento |
| `flat_map/2` | Transforma e achata |
| `filter/2` | Filtra elementos |
| `reject/2` | Rejeita elementos |
| `map_values/2` | Mapeia valores de tuplas |
| `map_batch/2` | Processa batch inteiro |

### Reducers (stateful, por particao)
| Funcao | Descricao |
|--------|-----------|
| `reduce/3` | Acumula estado |
| `group_by/3` | Agrupa por chave |
| `group_by_key/1` | Agrupa tuplas {k, v} |
| `emit_and_reduce/3` | Emite e reduz simultaneamente |
| `uniq/1` | Elementos unicos |
| `uniq_by/2` | Unicos por funcao |

### Emissao e Controle
| Funcao | Descricao |
|--------|-----------|
| `emit/2` | Controla o que emitir (:events, :state, :nothing) |
| `on_trigger/2` | Callback quando trigger dispara |

### Topologia
| Funcao | Descricao |
|--------|-----------|
| `partition/2` | Nova particao com PartitionDispatcher |
| `shuffle/2` | Nova camada com DemandDispatcher |
| `merge/3` | Merge com dispatcher customizado |
| `departition/5` | Merge resultados de todas as particoes |
| `take_sort/4` | Top N entre todas as particoes |

### Joins
| Funcao | Descricao |
|--------|-----------|
| `bounded_join/7` | Join de flows finitos |
| `window_join/8` | Join com janela temporal |

### Execucao
| Funcao | Descricao |
|--------|-----------|
| `Enum.to_list(flow)` | Coleta resultados (blocking) |
| `run/2` | Executa por side-effects |
| `stream/2` | Converte para Stream |
| `start_link/2` | Inicia como processo supervisionado |
| `into_stages/3` | Inicia com consumers existentes |
| `into_specs/3` | Inicia com consumer specs |
| `through_stages/3` | Passa por producer_consumers existentes |
| `through_specs/3` | Passa por producer_consumer specs |

### Windows
| Funcao | Descricao |
|--------|-----------|
| `Window.global/0` | Janela global (padrao) |
| `Window.fixed/3` | Janela fixa por event time |
| `Window.periodic/2` | Janela por processing time |
| `Window.count/1` | Janela por contagem |
| `Window.allowed_lateness/3` | Tolerancia a dados atrasados (so fixed) |
| `Window.trigger/3` | Trigger customizado |
| `Window.trigger_every/2` | Trigger a cada N eventos |
| `Window.trigger_periodically/3` | Trigger periodico |

---

## 16. Erros Comuns e Como Evitar

```elixir
# ERRO: reduce depois de reduce
flow |> Flow.reduce(...) |> Flow.reduce(...)  # ArgumentError!
# CORRETO: use on_trigger para transformar entre reducoes
flow |> Flow.reduce(...) |> Flow.on_trigger(...)

# ERRO: map depois de reduce
flow |> Flow.reduce(...) |> Flow.map(...)  # ArgumentError!
# CORRETO: use on_trigger ou partition novamente
flow |> Flow.reduce(...) |> Flow.partition() |> Flow.map(...)

# ERRO: emit/on_trigger sem reduce
flow |> Flow.emit(:state)  # ArgumentError!
# CORRETO: sempre apos reduce
flow |> Flow.reduce(...) |> Flow.emit(:state)

# ERRO: bounded_join com dados infinitos (vai estourar memoria)
# CORRETO: use window_join para dados infinitos

# ERRO: uniq_by com dados infinitos sem window (set cresce infinitamente)
# CORRETO: use uniq_by dentro de uma window
```

---

## 17. Quando Usar Flow?

### Use Flow quando:
- Processamento de grandes colecoes (>500 itens)
- Leitura/processamento de multiplos arquivos
- Aggregacoes paralelas (contagem, soma, agrupamento)
- Pipelines ETL
- Processamento de streams em tempo real com GenStage

### NAO use Flow quando:
- Colecoes pequenas (<500 itens) - overhead dos processos nao compensa
- Operacoes estritamente sequenciais - use Stream
- Logica simples sem necessidade de paralelismo - use Enum
- Precisa de ordenacao garantida - Flow nao garante ordem