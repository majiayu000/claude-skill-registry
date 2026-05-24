---
name: elixir
description: >
  Use when working with Elixir code — writing modules, functions, tests, mix tasks,
  templates, logging, or any Elixir/OTP project. Covers Elixir v1.18.4 / OTP 28,
  including standard library (Kernel), EEx, ExUnit, IEx, Logger, and Mix.
---

# Elixir Development Skill

Reference for Elixir v1.18.4 | OTP 28

---

## 1. Projeto e Estrutura (Mix)

### Criar novo projeto
```bash
mix new my_app               # aplicação simples
mix new my_app --sup         # com Supervisor (OTP)
mix new my_app --umbrella    # projeto umbrella (multi-app)
```

### Estrutura padrão
```
my_app/
├── lib/
│   └── my_app.ex            # módulo principal
├── test/
│   ├── test_helper.exs      # inicializa ExUnit
│   └── my_app_test.exs      # testes
├── config/
│   ├── config.exs           # configuração build-time
│   ├── dev.exs
│   ├── test.exs
│   ├── prod.exs
│   └── runtime.exs          # configuração runtime (releases)
└── mix.exs                  # definição do projeto
```

### mix.exs completo
```elixir
defmodule MyApp.MixProject do
  use Mix.Project

  def project do
    [
      app: :my_app,
      version: "0.1.0",
      elixir: "~> 1.18",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      aliases: aliases(),
      test_coverage: [tool: ExCoveralls]
    ]
  end

  def application do
    [
      extra_applications: [:logger],
      mod: {MyApp.Application, []}
    ]
  end

  defp deps do
    [
      {:jason, "~> 1.4"},
      {:ecto_sql, "~> 3.10"},
      {:ex_doc, "~> 0.31", only: :dev, runtime: false},
      {:excoveralls, "~> 0.18", only: :test}
    ]
  end

  defp aliases do
    [
      setup: ["deps.get", "ecto.setup"],
      "ecto.setup": ["ecto.create", "ecto.migrate", "run priv/repo/seeds.exs"],
      test: ["ecto.create --quiet", "ecto.migrate --quiet", "test"]
    ]
  end
end
```

### Comandos Mix essenciais
```bash
mix deps.get              # instala dependências
mix deps.update --all     # atualiza todas as deps
mix compile               # compila o projeto
mix test                  # roda os testes
mix test --only focus     # roda apenas testes com @tag focus
mix test test/meu_test.exs:42  # roda teste na linha 42
mix format                # formata código
mix format --check-formatted  # verifica formatação (CI)
mix credo                 # análise estática (requer dep credo)
mix docs                  # gera documentação
mix release               # cria release de produção
MIX_ENV=prod mix compile  # compila em modo prod
```

### Ambientes Mix
```bash
MIX_ENV=dev   # padrão
MIX_ENV=test  # usado por `mix test`
MIX_ENV=prod  # produção
```

```elixir
# Verificar ambiente em runtime
Mix.env() #=> :dev | :test | :prod

# Dep apenas para determinado ambiente
{:dep_name, "~> x.y", only: [:dev, :test]}
{:dep_name, "~> x.y", only: :test, runtime: false}
```

---

## 2. Módulos e Funções (Kernel)

### Definindo módulos
```elixir
defmodule MyApp.User do
  @moduledoc """
  Representa um usuário do sistema.
  """

  @type t :: %__MODULE__{
    id: integer(),
    name: String.t(),
    email: String.t(),
    active: boolean()
  }

  defstruct [:id, :name, :email, active: true]

  @doc """
  Cria um novo usuário.

  ## Exemplos

      iex> MyApp.User.new(1, "Alice", "alice@example.com")
      %MyApp.User{id: 1, name: "Alice", email: "alice@example.com", active: true}
  """
  @spec new(integer(), String.t(), String.t()) :: t()
  def new(id, name, email) do
    %__MODULE__{id: id, name: name, email: email}
  end

  # Função privada
  defp validate_email(email), do: String.contains?(email, "@")
end
```

### Pattern matching em funções
```elixir
defmodule MyApp.Shape do
  def area({:circle, r}),        do: :math.pi() * r * r
  def area({:rectangle, w, h}),  do: w * h
  def area({:triangle, b, h}),   do: b * h / 2

  # Cláusula de fallback
  def area(shape), do: {:error, "Unknown shape: #{inspect(shape)}"}
end
```

### Guards
```elixir
defmodule MyApp.Validator do
  # Guards built-in: is_integer, is_float, is_atom, is_binary,
  #                  is_list, is_map, is_tuple, is_nil, is_boolean,
  #                  is_function, is_pid, is_port, is_reference,
  #                  is_number, is_struct, is_exception

  def classify(n) when is_integer(n) and n > 0, do: :positive_integer
  def classify(n) when is_integer(n) and n < 0, do: :negative_integer
  def classify(0),                               do: :zero
  def classify(n) when is_float(n),              do: :float
  def classify(_),                               do: :other

  # Definindo guard customizado com defguard
  defguard is_adult(age) when is_integer(age) and age >= 18

  def can_vote?(age) when is_adult(age), do: true
  def can_vote?(_), do: false
end
```

### Operador pipe `|>`
```elixir
# Sem pipe:
String.trim(String.downcase(String.replace("  Hello World  ", " ", "_")))

# Com pipe (legível, da esquerda para a direita):
"  Hello World  "
|> String.replace(" ", "_")
|> String.downcase()
|> String.trim()
#=> "hello_world"

# Pipeline de processamento real:
users
|> Enum.filter(& &1.active)
|> Enum.map(& &1.email)
|> Enum.sort()
|> Enum.uniq()
```

### Closures e funções anônimas
```elixir
# Função anônima curta
add = fn a, b -> a + b end
add.(1, 2) #=> 3

# Shorthand com &
double = &(&1 * 2)
double.(5) #=> 10

multiply = &(&1 * &2)
multiply.(3, 4) #=> 12

# Capturando função nomeada
to_string_fn = &Integer.to_string/1
to_string_fn.(42) #=> "42"

# Passando como argumento
[1, 2, 3] |> Enum.map(&double.(&1))
# ou mais idiomático:
[1, 2, 3] |> Enum.map(&(&1 * 2))
```

---

## 3. Tipos de Dados e Módulos da Stdlib

### String
```elixir
# Strings são binários UTF-8
"hello" <> " " <> "world"          #=> "hello world"
String.upcase("hello")              #=> "HELLO"
String.downcase("HELLO")            #=> "hello"
String.length("héllo")             #=> 5 (caracteres Unicode)
String.split("a,b,c", ",")         #=> ["a", "b", "c"]
String.trim("  hello  ")           #=> "hello"
String.replace("foo bar", "bar", "baz")  #=> "foo baz"
String.contains?("hello", "ell")   #=> true
String.starts_with?("hello", "he") #=> true
String.ends_with?("hello", "lo")   #=> true
String.to_integer("42")            #=> 42
String.to_float("3.14")            #=> 3.14
String.slice("hello", 1, 3)        #=> "ell"
String.pad_leading("42", 5, "0")   #=> "00042"

# Interpolação
name = "Alice"
"Hello, #{name}!"                  #=> "Hello, Alice!"
"2 + 2 = #{2 + 2}"                #=> "2 + 2 = 4"
```

### Integer e Float
```elixir
Integer.to_string(255, 16)   #=> "FF"        (base 16)
Integer.to_string(8, 2)      #=> "1000"      (base 2)
Integer.parse("42")          #=> {42, ""}
Integer.digits(123)          #=> [1, 2, 3]

Float.round(3.14159, 2)      #=> 3.14
Float.ceil(1.2)              #=> 2.0
Float.floor(1.9)             #=> 1.0
```

### Atom
```elixir
:ok
:error
:hello
true          # atom
false         # atom
nil           # atom

is_atom(:ok)  #=> true
Atom.to_string(:hello)  #=> "hello"
String.to_atom("hello") #=> :hello  (cuidado: não usar com input externo)
String.to_existing_atom("hello")  # mais seguro
```

### List
```elixir
list = [1, 2, 3, 4, 5]

hd(list)          #=> 1
tl(list)          #=> [2, 3, 4, 5]
length(list)      #=> 5
[0 | list]        #=> [0, 1, 2, 3, 4, 5]  (prepend, O(1))
list ++ [6, 7]    #=> [1, 2, 3, 4, 5, 6, 7]
list -- [2, 4]    #=> [1, 3, 5]

List.first(list)  #=> 1
List.last(list)   #=> 5
List.flatten([[1, [2]], [3]])  #=> [1, 2, 3]
List.zip([[1,2], [3,4]])      #=> [{1,3}, {2,4}]
```

### Keyword List
```elixir
# Lista de tuplas de 2 elementos com átomo como chave
opts = [timeout: 5000, retry: 3, verbose: true]

opts[:timeout]            #=> 5000
Keyword.get(opts, :retry) #=> 3
Keyword.put(opts, :debug, false)
Keyword.merge(opts, [timeout: 3000])
Keyword.keys(opts)        #=> [:timeout, :retry, :verbose]

# Usado como opções em funções (convenção Elixir)
def connect(host, port, opts \\ []) do
  timeout = Keyword.get(opts, :timeout, 5000)
  # ...
end
```

### Map
```elixir
map = %{name: "Alice", age: 30, active: true}

# Acesso
map[:name]         #=> "Alice"
map.name           #=> "Alice" (apenas para chaves atom)
Map.get(map, :age) #=> 30
Map.get(map, :email, "n/a")  #=> "n/a" (com default)

# Atualização (imutável – retorna novo map)
%{map | age: 31}          # atualiza chave existente
Map.put(map, :email, "alice@example.com")
Map.delete(map, :active)
Map.merge(map, %{role: :admin})

# Pattern matching em maps
%{name: name, age: age} = map
# name => "Alice", age => 30

# Verificação
Map.has_key?(map, :name)  #=> true
Map.keys(map)             #=> [:active, :age, :name]
Map.values(map)           #=> [true, 30, "Alice"]
Map.to_list(map)          #=> [{:active, true}, {:age, 30}, {:name, "Alice"}]
```

### Tuple
```elixir
tuple = {:ok, "resultado", 42}

elem(tuple, 0)                   #=> :ok
elem(tuple, 1)                   #=> "resultado"
tuple_size(tuple)                #=> 3
put_elem(tuple, 2, 99)          #=> {:ok, "resultado", 99}

# Convenção: usar para retorno com status
{:ok, value}    # sucesso
{:error, reason} # erro

# Pattern matching
case result do
  {:ok, data}    -> process(data)
  {:error, msg}  -> Logger.error(msg)
end
```

### Enum (coleções eager)
```elixir
# Transformação
Enum.map([1,2,3], &(&1 * 2))         #=> [2, 4, 6]
Enum.filter([1,2,3,4], &(rem(&1,2) == 0))  #=> [2, 4]
Enum.reject([1,2,3,4], &(rem(&1,2) == 0))  #=> [1, 3]
Enum.reduce([1,2,3,4], 0, &+/2)      #=> 10
Enum.flat_map([1,2,3], &[&1, &1*2])  #=> [1, 2, 2, 4, 3, 6]

# Busca
Enum.find([1,2,3], &(&1 > 2))        #=> 3
Enum.find_index([1,2,3], &(&1 > 2))  #=> 2
Enum.any?([1,2,3], &(&1 > 2))        #=> true
Enum.all?([1,2,3], &(&1 > 0))        #=> true
Enum.count([1,2,3], &(&1 > 1))       #=> 2

# Ordenação
Enum.sort([3,1,2])                    #=> [1, 2, 3]
Enum.sort([3,1,2], :desc)             #=> [3, 2, 1]
Enum.sort_by(users, & &1.name)
Enum.min([3,1,2])                     #=> 1
Enum.max([3,1,2])                     #=> 3
Enum.min_max([3,1,2])                 #=> {1, 3}

# Agrupamento e partição
Enum.group_by([1,2,3,4], &(rem(&1,2) == 0))
#=> %{false => [1, 3], true => [2, 4]}
Enum.partition([1,2,3,4], &(rem(&1,2) == 0))
#=> {[2, 4], [1, 3]}
Enum.chunk_every([1,2,3,4,5], 2)
#=> [[1, 2], [3, 4], [5]]
Enum.zip([1,2,3], [:a, :b, :c])
#=> [{1, :a}, {2, :b}, {3, :c}]
Enum.with_index(["a","b","c"])
#=> [{"a", 0}, {"b", 1}, {"c", 2}]

# Redução avançada
Enum.sum([1,2,3,4])                   #=> 10
Enum.frequencies(["a","b","a","c"])   #=> %{"a" => 2, "b" => 1, "c" => 1}
Enum.flat_map_reduce([1,2,3], 0, fn x, acc -> {[x, x], acc + x} end)
```

### Stream (coleções lazy)
```elixir
# Use Stream quando: grandes coleções ou pipelines com múltiplos passos
# Avalia apenas quando necessário (com Enum no final)

Stream.map(1..1_000_000, &(&1 * 2))
|> Stream.filter(&(rem(&1, 3) == 0))
|> Stream.take(10)
|> Enum.to_list()

# Leitura de arquivo linha a linha (sem carregar tudo na memória)
File.stream!("big_file.txt")
|> Stream.map(&String.trim/1)
|> Stream.reject(&(&1 == ""))
|> Enum.to_list()

# Stream.cycle – lista infinita
Stream.cycle([1,2,3]) |> Enum.take(7)  #=> [1,2,3,1,2,3,1]

# Stream.iterate
Stream.iterate(0, &(&1 + 1)) |> Enum.take(5)  #=> [0,1,2,3,4]

# Stream.resource – IO externo
Stream.resource(
  fn -> File.open!("file.txt") end,
  fn file ->
    case IO.read(file, :line) do
      :eof -> {:halt, file}
      line -> {[line], file}
    end
  end,
  fn file -> File.close(file) end
)
```

---

## 4. Controle de Fluxo

### if / unless / cond / case
```elixir
# if / unless
if condition do
  "verdadeiro"
else
  "falso"
end

unless is_nil(value) do
  process(value)
end

# Inline
result = if valid?, do: "ok", else: "error"

# cond – múltiplas condições
cond do
  x > 10  -> "grande"
  x > 5   -> "médio"
  x > 0   -> "pequeno"
  true    -> "zero ou negativo"  # cláusula padrão
end

# case – pattern matching
case http_response do
  {:ok, 200, body}    -> process_body(body)
  {:ok, 404, _}       -> {:error, :not_found}
  {:ok, status, _}    -> {:error, {:unexpected_status, status}}
  {:error, reason}    -> {:error, reason}
end
```

### with – encadeamento de pattern matching
```elixir
# Ideal para fluxos "happy path" com possibilidade de erro
with {:ok, user}  <- Users.get(user_id),
     {:ok, order} <- Orders.create(user, params),
     {:ok, email} <- Emails.send_confirmation(order) do
  {:ok, %{user: user, order: order}}
else
  {:error, :not_found}   -> {:error, "Usuário não encontrado"}
  {:error, changeset}    -> {:error, changeset_errors(changeset)}
  error                  -> error
end
```

### for – list comprehension
```elixir
# Básico
for x <- 1..5, do: x * x
#=> [1, 4, 9, 16, 25]

# Com filtro (guard)
for x <- 1..10, rem(x, 2) == 0, do: x
#=> [2, 4, 6, 8, 10]

# Múltiplos geradores (produto cartesiano)
for x <- 1..3, y <- 1..3, x != y, do: {x, y}

# Coletando em map
for {key, val} <- [a: 1, b: 2, c: 3], into: %{}, do: {key, val * 10}
#=> %{a: 10, b: 20, c: 30}

# Coletando em string
for byte <- 'hello', into: "", do: <<byte + 1>>
```

### try / rescue / catch / after
```elixir
try do
  risky_operation()
rescue
  e in RuntimeError -> Logger.error("Runtime error: #{e.message}")
  e in [ArgumentError, FunctionClauseError] -> handle_arg_error(e)
  e -> reraise e, __STACKTRACE__  # re-levanta
catch
  :exit, reason -> handle_exit(reason)
  :throw, value -> handle_throw(value)
after
  cleanup()  # sempre executado
end

# raise e rescue
raise "something went wrong"
raise ArgumentError, message: "invalid argument"
raise MyCustomError, details: %{code: 404}

# throw / catch (fluxo de controle, não erros)
result = catch :throw do
  Enum.each(list, fn item ->
    if condition?(item), do: throw({:found, item})
  end)
  :not_found
end
```

---

## 5. Concorrência e OTP

### Processos
```elixir
# Spawnar processo
pid = spawn(fn -> IO.puts("olá do processo #{inspect(self())}") end)

# Enviar e receber mensagens
send(pid, {:hello, "mundo"})

receive do
  {:hello, msg} -> IO.puts("Recebi: #{msg}")
  other         -> IO.puts("Mensagem inesperada: #{inspect(other)}")
after
  5000 -> IO.puts("Timeout!")
end
```

### GenServer
```elixir
defmodule MyApp.Counter do
  use GenServer

  # --- API pública ---
  def start_link(initial_value \\ 0) do
    GenServer.start_link(__MODULE__, initial_value, name: __MODULE__)
  end

  def increment(amount \\ 1), do: GenServer.cast(__MODULE__, {:increment, amount})
  def get_value,              do: GenServer.call(__MODULE__, :get_value)
  def reset,                  do: GenServer.call(__MODULE__, :reset)

  # --- Callbacks ---
  @impl true
  def init(initial_value), do: {:ok, initial_value}

  @impl true
  def handle_call(:get_value, _from, state), do: {:reply, state, state}
  def handle_call(:reset, _from, _state),    do: {:reply, :ok, 0}

  @impl true
  def handle_cast({:increment, amount}, state), do: {:noreply, state + amount}
end

# Uso
{:ok, _pid} = MyApp.Counter.start_link(10)
MyApp.Counter.increment(5)
MyApp.Counter.get_value()  #=> 15
```

### Supervisor
```elixir
defmodule MyApp.Application do
  use Application

  @impl true
  def start(_type, _args) do
    children = [
      {MyApp.Counter, 0},
      {MyApp.Worker, []},
      {Task.Supervisor, name: MyApp.TaskSupervisor}
    ]

    opts = [strategy: :one_for_one, name: MyApp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end

# Estratégias de reinício:
# :one_for_one   – reinicia só o filho falho
# :one_for_all   – reinicia todos se um falhar
# :rest_for_one  – reinicia o falho e todos iniciados depois dele
```

### Task
```elixir
# Execução assíncrona simples
task = Task.async(fn -> heavy_computation() end)
result = Task.await(task, 10_000)  # timeout em ms

# Múltiplas tasks em paralelo
tasks = Enum.map(urls, &Task.async(fn -> fetch(&1) end))
results = Task.await_many(tasks, 30_000)

# Task supervisionada (não derruba o chamador se falhar)
Task.Supervisor.async_nolink(MyApp.TaskSupervisor, fn ->
  risky_operation()
end)
```

### Agent (estado simples)
```elixir
{:ok, pid} = Agent.start_link(fn -> [] end, name: :my_agent)

Agent.update(:my_agent, fn list -> [new_item | list] end)
Agent.get(:my_agent, & &1)
Agent.get_and_update(:my_agent, fn list -> {list, []} end)
Agent.stop(:my_agent)
```

---

## 6. Testes com ExUnit

### Estrutura básica
```elixir
defmodule MyApp.UserTest do
  use ExUnit.Case, async: true  # async: true para paralelismo

  # Configuração por describe
  setup do
    user = %MyApp.User{id: 1, name: "Alice", email: "alice@test.com"}
    {:ok, user: user}  # contexto disponível nos testes
  end

  describe "new/3" do
    test "cria usuário com valores padrão", %{user: user} do
      assert user.name == "Alice"
      assert user.active == true
    end

    test "email deve conter @" do
      assert_raise ArgumentError, fn ->
        MyApp.User.new(1, "Bob", "invalid-email")
      end
    end
  end

  describe "activate/1" do
    test "retorna usuário ativo" do
      user = %MyApp.User{active: false}
      result = MyApp.User.activate(user)
      assert result.active == true
    end
  end
end
```

### Assertions
```elixir
# Básicas
assert expression                         # verifica se é truthy
refute expression                         # verifica se é falsy
assert value == expected
assert value === expected                 # strict (tipo e valor)

# Comparações
assert length(list) == 3
assert map_size(map) > 0

# Exceções
assert_raise RuntimeError, fn -> raise "oops" end
assert_raise ArgumentError, ~r/invalid/, fn -> bad_call() end

# Mensagens recebidas (processos)
assert_receive {:ok, _value}, 1000        # timeout em ms
refute_receive {:error, _}

# Float
assert_in_delta 3.14, :math.pi(), 0.01

# Pattern matching em assert
assert {:ok, %{id: id}} = create_user()  # bind e verifica estrutura

# Catch para fluxo de throw
assert catch_throw(fn -> throw(:value) end) == :value
assert catch_exit(fn -> exit(:reason) end) == :reason
assert catch_error(fn -> raise "boom" end)
```

### Tags e filtros
```elixir
# Tags em módulo inteiro
@moduletag :integration

# Tag em teste individual
@tag :slow
@tag timeout: 10_000
@tag :skip
test "teste que pula" do ... end

# Rodar com filtros
# mix test --only integration
# mix test --exclude slow
# mix test --include slow
```

### Setup e Callbacks
```elixir
defmodule MyApp.DbTest do
  use ExUnit.Case

  setup_all do
    # Executa uma vez para todos os testes do módulo
    {:ok, db} = MyApp.DB.start_link()
    on_exit(fn -> MyApp.DB.stop(db) end)
    {:ok, db: db}
  end

  setup %{db: db} do
    # Executa antes de cada teste
    MyApp.DB.truncate(db)
    :ok
  end
end
```

### ExUnit.Case doctests
```elixir
defmodule MyApp.Math do
  @doc """
  Soma dois números.

      iex> MyApp.Math.add(1, 2)
      3

      iex> MyApp.Math.add(0, 0)
      0
  """
  def add(a, b), do: a + b
end

defmodule MyApp.MathTest do
  use ExUnit.Case
  doctest MyApp.Math  # executa os exemplos do @doc como testes
end
```

---

## 7. Logger

### Configuração (config/config.exs)
```elixir
import Config

config :logger, level: :debug   # :debug | :info | :warning | :error

config :logger, :default_formatter,
  format: "[$l] $message\n",
  metadata: [:request_id, :user_id]

# Desabilitar logger em testes
config :logger, level: :warning

# Por módulo específico
config :logger, MyApp.NoisyModule, level: :warning
```

### Uso nos módulos
```elixir
defmodule MyApp.Service do
  require Logger

  def process(data) do
    Logger.debug("Processando: #{inspect(data)}")
    Logger.info("Iniciando processamento")

    case do_work(data) do
      {:ok, result} ->
        Logger.info("Sucesso", result_size: byte_size(result))
        {:ok, result}

      {:error, reason} ->
        Logger.warning("Falhou: #{inspect(reason)}")
        {:error, reason}
    end
  rescue
    e ->
      Logger.error("Exceção: #{Exception.message(e)}", error: e)
      reraise e, __STACKTRACE__
  end
end
```

### Níveis de log (ordem de severidade)
```
:debug      # desenvolvimento, diagnóstico
:info       # eventos normais
:notice     # eventos significativos, normais
:warning    # algo inesperado, mas tolerável
:error      # erros que precisam atenção
:critical   # falhas críticas
:alert      # ação imediata necessária
:emergency  # sistema inoperante
```

### Metadata
```elixir
# Global (todos os logs do processo)
Logger.metadata(request_id: "abc123", user_id: 42)

# Por chamada específica
Logger.info("Compra realizada", order_id: order.id, amount: order.total)

# Resetar metadata
Logger.metadata([])
```

---

## 8. EEx (Embedded Elixir / Templates)

### Tags EEx
```
<% código %>          executa código (sem output)
<%= expressão %>      executa e imprime resultado
<%% ... %%>           escapa, não executa (retorna literal)
<%!-- comentário --%> comentário (ignorado)
```

### APIs de uso
```elixir
# 1. Avaliação direta (mais lento, bom para templates dinâmicos)
EEx.eval_string("Olá, <%= name %>!", name: "Alice")
#=> "Olá, Alice!"

EEx.eval_file("templates/email.html.eex", assigns)

# 2. Compilar como função (mais rápido, preferido)
defmodule MyApp.Templates do
  require EEx

  EEx.function_from_string(:def, :render_greeting, "Olá, <%= name %>!", [:name])
  EEx.function_from_file(:def, :render_email, "priv/templates/email.html.eex", [:assigns])
end

# Uso:
MyApp.Templates.render_greeting("Bob")  #=> "Olá, Bob!"
```

### Template com assigns (@var)
```elixir
# Usando SmartEngine (padrão): @var acessa assigns
template = """
<html>
  <body>
    <h1><%= @title %></h1>
    <%= for item <- @items do %>
      <li><%= item %></li>
    <% end %>
  </body>
</html>
"""

EEx.eval_string(template, assigns: [title: "Lista", items: ["a", "b", "c"]])
```

### Compilar para análise (AST)
```elixir
# Para integração avançada ou engine customizada
ast = EEx.compile_string("<%= 1 + 1 %>")
{result, _} = Code.eval_quoted(ast)
```

---

## 9. IEx (Shell Interativo)

### Comandos essenciais
```elixir
h Module              # documentação do módulo
h Module.function/arity  # doc de função específica
i value               # informações sobre um valor
t Module.type         # tipos do módulo

# Exemplos
h String
h String.split/2
h Enum
i "hello"
i [1,2,3]
t GenServer.on_start
```

### Helpers e inspeção
```elixir
IO.inspect(value)                           # imprime com metadados
IO.inspect(value, label: "meu valor")       # com label
IO.inspect(value, limit: :infinity)         # sem truncamento
IO.inspect(value, pretty: true)             # formatado
IO.inspect(value, structs: false)           # mostra como map

# Dentro de pipeline (não altera o fluxo)
[1,2,3]
|> IO.inspect(label: "antes")
|> Enum.map(&(&1 * 2))
|> IO.inspect(label: "depois")
```

### Sessão IEx
```bash
iex                  # shell simples
iex -S mix           # com projeto Mix carregado
iex -S mix phx.server  # com servidor Phoenix
iex --name alice@localhost  # nomeado (cluster)
```

```elixir
# Dentro do IEx:
recompile()           # recompila o projeto sem reiniciar
r ModuleName          # recarrega módulo específico
c "path/to/file.ex"  # compila e carrega arquivo
ls                    # lista diretório
cd "path"             # muda diretório
pwd                   # diretório atual

# Recuperar valor de expressões anteriores
v(1)                  # valor da 1ª expressão
v(-1)                 # valor da última expressão
```

### IEx.pry – debugging
```elixir
defmodule MyApp.Debug do
  def problematic_function(x) do
    require IEx
    IEx.pry()  # para execução aqui (apenas em iex -S mix)
    x * 2
  end
end
```

### IEx.configure
```elixir
# ~/.iex.exs (configuração pessoal)
IEx.configure(
  colors: [enabled: true],
  inspect: [limit: 50, pretty: true],
  history_size: 100
)

import_if_available(Ecto.Query)
alias MyApp.{User, Order, Repo}
```

---

## 10. Padrões e Boas Práticas

### Convenções de nomenclatura
```elixir
# Módulos: PascalCase
defmodule MyApp.UserService do

# Funções e variáveis: snake_case
def create_user(attrs) do

# Funções que retornam bool: terminam em ?
def valid?(changeset)
def empty?(list)

# Funções que levantam exceção: terminam em !
def fetch!(key)   # levanta se não encontrar
def save!(data)   # levanta se falhar

# Funções "bang" vs "safe"
File.read("file.txt")   #=> {:ok, content} | {:error, reason}
File.read!("file.txt")  #=> content | levanta RuntimeError

# Constantes de módulo
@max_retries 3
@default_timeout 5_000
@behaviour MyApp.Behaviour
```

### Estrutura de retorno consistente
```elixir
# Sempre retornar {:ok, value} ou {:error, reason}
def find_user(id) do
  case Repo.get(User, id) do
    nil  -> {:error, :not_found}
    user -> {:ok, user}
  end
end

# Encadeamento com with
def process_order(user_id, params) do
  with {:ok, user}   <- find_user(user_id),
       {:ok, order}  <- create_order(user, params),
       {:ok, _email} <- send_confirmation(order) do
    {:ok, order}
  end
end
```

### @spec – tipagem
```elixir
@spec add(integer(), integer()) :: integer()
def add(a, b), do: a + b

@spec find_user(pos_integer()) :: {:ok, User.t()} | {:error, :not_found}
def find_user(id), do: ...

@spec process([map()], keyword()) :: {:ok, list()} | {:error, String.t()}
def process(items, opts \\ []), do: ...

# Tipos compostos comuns
@type id :: pos_integer()
@type result(t) :: {:ok, t} | {:error, String.t()}
@type option(t) :: t | nil
```

### Macros e metaprogramação
```elixir
defmodule MyApp.DSL do
  defmacro route(method, path, do: block) do
    quote do
      def unquote(:"handle_#{method}")(unquote(path)) do
        unquote(block)
      end
    end
  end
end

# use (injeta comportamento)
defmodule MyApp.Base do
  defmacro __using__(opts) do
    quote do
      import MyApp.Base
      @behaviour MyApp.Behaviour
      Module.register_attribute(__MODULE__, :routes, accumulate: true)
    end
  end
end
```

### Behaviours (interfaces)
```elixir
defmodule MyApp.Notifier do
  @callback send_notification(user :: map(), message :: String.t()) ::
              {:ok, reference()} | {:error, String.t()}

  @callback supported_channels() :: [atom()]

  @optional_callbacks supported_channels: 0
end

defmodule MyApp.EmailNotifier do
  @behaviour MyApp.Notifier

  @impl true
  def send_notification(user, message) do
    # implementação
    {:ok, make_ref()}
  end

  @impl true
  def supported_channels, do: [:email, :html]
end
```

---

## 11. Configuração e Releases

### Config dinâmica em runtime
```elixir
# config/runtime.exs (preferido para produção)
import Config

config :my_app, MyApp.Repo,
  url: System.fetch_env!("DATABASE_URL"),
  pool_size: String.to_integer(System.get_env("POOL_SIZE", "10"))

config :my_app, secret_key_base: System.fetch_env!("SECRET_KEY_BASE")
```

### Application env
```elixir
# Ler configuração em runtime
Application.get_env(:my_app, :timeout, 5000)
Application.fetch_env!(:my_app, :api_key)

# Bom para defaults em módulos
defmodule MyApp.Client do
  @default_timeout Application.compile_env(:my_app, [:client, :timeout], 5000)

  def call(url) do
    timeout = Application.get_env(:my_app, [:client, :timeout], @default_timeout)
    # ...
  end
end
```

---

## 12. Erros Comuns e Soluções

| Erro | Causa | Solução |
|------|-------|---------|
| `FunctionClauseError` | Nenhuma cláusula matchou | Adicionar cláusula fallback ou verificar tipos de entrada |
| `MatchError` | Pattern match falhou com `=` | Usar `case` ou verificar o valor antes |
| `UndefinedFunctionError` | Função não existe ou não foi importada | Verificar `alias`, `import` e `use` |
| `KeyError` | Acesso a chave inexistente em map com `.` | Usar `Map.get/3` com default |
| `ArgumentError` | Argumento inválido para função | Verificar typo, adicionar `when` guards |
| `CaseClauseError` | Nenhuma cláusula do `case` matchou | Adicionar cláusula `_ ->` |
| `WithClauseError` | `with` sem cláusula `else` para o padrão | Adicionar `else` clause |
| `CompileError` | Erro em tempo de compilação | Verificar sintaxe, módulos circulares |
| `Dialyxir warning` | Typespec inconsistente | Corrigir `@spec` |

---

## 13. Referências Rápidas

### Links oficiais (v1.18.4)
- Kernel: https://hexdocs.pm/elixir/1.18.4/Kernel.html
- EEx: https://hexdocs.pm/eex/1.18.4/EEx.html
- ExUnit: https://hexdocs.pm/ex_unit/1.18.4/ExUnit.html
- IEx: https://hexdocs.pm/iex/1.18.4/IEx.html
- Logger: https://hexdocs.pm/logger/1.18.4/Logger.html
- Mix: https://hexdocs.pm/mix/1.18.4/Mix.html
- Guia: https://hexdocs.pm/elixir/introduction.html

### Módulos stdlib mais usados
```
Kernel       - primitivas, guards, operadores
String       - manipulação de strings UTF-8
Integer      - operações com inteiros
Float        - operações com floats
Atom         - operações com atoms
List         - listas encadeadas
Map          - mapas chave-valor
Keyword      - keyword lists
Tuple        - tuplas
Enum         - coleções (eager)
Stream       - coleções (lazy)
IO           - entrada e saída
File         - sistema de arquivos
Path         - caminhos de arquivo
System       - informações do sistema
Process      - processos Elixir
Agent        - estado simples
GenServer    - cliente-servidor genérico
Supervisor   - árvore de supervisão
Task         - computação assíncrona
Registry     - registro chave-processo
Application  - gerenciamento de aplicações
Config       - configuração
Regex        - expressões regulares
DateTime     - data e hora com timezone
Date         - apenas data
Time         - apenas hora
URI          - manipulação de URIs
Jason / Poison - JSON (libs externas)
```