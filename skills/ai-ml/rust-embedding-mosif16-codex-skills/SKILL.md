------------------------------------------------------------------------

title: GraphEmbed CLI Tool Specification\
version: 1.0.0\
description: \"A Rust-based CLI tool for generating text embeddings and
managing knowledge graphs\"

------------------------------------------------------------------------

# GraphEmbed CLI Tool

GraphEmbed CLI is a command-line application written in Rust that
integrates text embedding generation with knowledge graph management. It
allows users to create or import knowledge graphs, generate or ingest
vector embeddings for text data, and manipulate the graph's entities and
relationships. The tool supports standard graph data formats (JSON-LD,
RDF/Turtle, CSV) and offers querying and basic visualization
capabilities. This document provides an overview of the tool's features,
usage instructions, workflow, examples, and references to relevant
resources.

## Instructions

**Installation & Setup:** To install GraphEmbed, ensure you have Rust
installed (for source builds) or use a prebuilt binary if provided. You
can compile from source via Cargo:

    $ cargo install graphembed-cli

This will download and build the CLI. After installation, the command
`graphembed` should be available. For help on any command, run
`graphembed help` or `graphembed <command> --help`.

**Command Structure:** GraphEmbed uses subcommands for different
functionalities. General usage follows:

    graphembed <command> [OPTIONS] [ARGS...]

Key commands include:

- `embed` -- Generate embeddings from input text using a chosen model.
- `import` -- Load a knowledge graph from a file (JSON-LD, Turtle, RDF,
  or CSV).
- `export` -- Save the current knowledge graph to a file in a specified
  format.
- `add-entity` -- Create a new entity (node) in the graph.
- `add-rel` -- Create a relationship (edge) between two entities.
- `update` -- Modify an existing entity or relationship.
- `delete` -- Remove an entity or relationship from the graph.
- `query` -- Query the graph for specific patterns or run a SPARQL query
  (if supported).
- `visualize` -- Generate a simple visual representation of the graph.

**Embedding Generation:** The `embed` command produces a numerical
vector (embedding) from a given text input. By default, GraphEmbed
leverages Rust-compatible NLP models (Transformer-based) for embeddings.
You may specify an embedding model with `-m/--model`. For example,
`all-MiniLM-L6-v2` (a popular SentenceTransformer model) can be used if
available. Under the hood, the tool uses **Hugging Face Transformers**
via Rust libraries to compute embeddings. This means you can use
pre-trained models like BERT, MiniLM, etc., without needing Python. The
first time you request a particular model, the tool will download the
model weights if not already present. Ensure you have an internet
connection for model downloads or pre-download the model files. If no
model is specified, a default small embedding model is used.

- *Model backends:* GraphEmbed supports multiple backend frameworks for
  embeddings. It can use **Rust-BERT** (which wraps PyTorch models with
  the `tch` crate) for many Hugging Face models, or an **ONNX Runtime**
  backend for sentence transformers if compiled with the `onnx` feature
  (using the `ort` crate). You can choose the backend via features or
  CLI flags (e.g., `--backend torch` vs `--backend onnx`). The tool
  ensures that generating an embedding requires only the text input --
  the output is a vector of floats printed to stdout or saved to a file
  if specified.

**Ingesting Precomputed Vectors:** In addition to generating embeddings,
you can ingest precomputed embedding vectors into the system. The
`import` command will automatically detect if a given file is an
embedding file based on format (for example, a CSV of vectors or a JSON
array). Alternatively, a dedicated subcommand `ingest-vec` may be
provided (check `graphembed help` for the exact name if available).
Typically, you would prepare a CSV where each line contains an entity
identifier and a list of numerical components of the embedding.
GraphEmbed will read this and attach each vector to the corresponding
entity in the knowledge graph (creating the entity if it doesn't exist).
For example, a CSV with header `entity_id,dim1,dim2,...` can be
ingested. Ensure that the entity identifiers match those used in the
graph (case-sensitive). After ingestion, the embedding becomes a
property of the entity in the graph (accessible for querying or
similarity operations in future versions).

**Knowledge Graph Import/Export:** The `import` and `export` commands
handle reading from or writing to various knowledge graph formats: -
**JSON-LD (.jsonld)** -- A JSON-based linked data format. The tool can
parse JSON-LD files to create the internal graph. It will interpret
`@context`, `@id`, and other JSON-LD keywords properly, so imported data
retains semantic meaning. When exporting to JSON-LD, GraphEmbed will
produce a context and list of triples in JSON-LD structure. -
**RDF/Turtle (.ttl or .rdf)** -- The Turtle syntax (and generic RDF/XML
if `.rdf` is provided) is supported. Import will parse triples and build
the graph accordingly. Export will write out triples with prefixes and
IRIs as needed in Turtle format. - **CSV (.csv)** -- For simplicity,
GraphEmbed expects CSV files to represent triples or edges. Each row
should contain at least three columns: subject, predicate, object
(optionally a fourth for a literal type or language tag if needed). A
header row can be present with names like `subject,predicate,object`. If
no header is present, the tool assumes each line is a triple in order.
CSV import is useful for quickly loading edge lists or simple knowledge
graphs from spreadsheets. Exporting to CSV will produce a triple list in
a similar fashion (one triple per line). - The import command tries to
auto-detect format from file extension. You can override by specifying
`--format jsonld|turtle|csv|rdf` if needed. The tool uses robust parsers
under the hood (e.g., an RDF library for Turtle/JSON-LD) and will report
any parse errors with line numbers for easier debugging of file format
issues.

**Entities and Relationships (CRUD):** GraphEmbed maintains an internal
graph data structure where **entities** are nodes identified by unique
IDs or IRIs, and **relationships** are edges (typically labeled with a
predicate/property name). Using CLI commands, you can **create, update,
and delete** these: - **Creating Entities:** Use `add-entity` with a
unique identifier or label. For RDF-based graphs, this might create a
new URI (you can specify a CURIE or a full URI with `--id`, or let the
tool generate a blank node or namespaced URI). You can also attach
initial data like a type or properties via options. For example,
`graphembed add-entity "Alice" --type Person` might create an entity
with label "Alice" of type Person. - **Creating Relationships:** Use
`add-rel` (or `add-relationship`) specifying a subject, predicate, and
object. For instance, `graphembed add-rel "Alice" "knows" "Bob"` would
add a relationship stating Alice knows Bob. Under the hood, if "Alice"
and "Bob" are label identifiers for entities, the tool will map them to
their internal IDs (or create them if they didn't exist). Predicates can
be given as simple labels or as full URIs; the tool may map common
relation names to a default vocabulary or allow a `--uri` option to
specify an exact property URI. - **Updating:** The `update` command
allows changing an entity's attributes or a relationship's
predicate/target. For example, you might update an entity's name, or
attach a new attribute (like adding an `age` property to a Person). In
an RDF graph context, updating might just mean adding or replacing
certain triples. The CLI might provide flags like
`--set-property name="Alice A."` or similar to modify data.
Relationships could be updated by referencing them (e.g., by an ID or by
the subject-predicate-object triple pattern). - **Deleting:** Use
`delete` with an identifier. You can delete an entity (which will also
remove any relationships involving it) or delete a specific relationship
by providing its triple components. For example,
`graphembed delete entity "Alice"` removes the entity Alice, while
`graphembed delete rel "Alice" "knows" "Bob"` removes only that edge.
The tool will prompt for confirmation if multiple triples are affected
(or you can use `--force` for non-interactive deletion).

**Querying the Graph:** The `query` command lets you retrieve
information from the knowledge graph. By default, GraphEmbed supports
simple pattern queries and, if compiled with the SPARQL feature, full
SPARQL queries: - *Pattern queries:* You can query by providing partial
triple patterns. For example, `graphembed query "Alice -> ?p -> ?o"`
could list all predicates and objects that Alice is connected to. Using
`?` indicates a wildcard (variable) for any matching node or value.
Similarly, `?s -> knows -> Bob` would find all subjects that have a
\"knows\" relationship to Bob. - *SPARQL queries:* If the tool is built
with SPARQL support (using an embedded engine), you can supply a SPARQL
query string:
`graphembed query "SELECT ?friend WHERE { <Alice> <knows> ?friend }"`.
The query should be enclosed in quotes. Results will be printed in a
simple table format or as JSON, depending on flags (e.g.,
`--format csv|json` for result output). Keep in mind that full SPARQL
support may require an additional dependency and can be toggled via a
feature flag at compile time. If SPARQL is not available, the tool will
inform you or fall back to basic queries. - *Performance:* For larger
graphs, consider using indexing or persistent storage. GraphEmbed
primarily holds the graph in memory. If you need to run complex queries
on very large datasets, integration with a dedicated graph database
(like an external SPARQL endpoint or property graph DB) might be
preferable. However, for moderate-sized knowledge graphs, the built-in
query should suffice.

**Visualization:** The `visualize` command produces a human-readable
graph representation. This can help you quickly understand the structure
of the knowledge graph: - By default, `visualize` will output a Graphviz
DOT format text to stdout or to a file (if `-o graph.dot` is specified).
You can then use Graphviz tools (e.g.,
`dot -Tpng graph.dot -o graph.png`) to generate an image. If Graphviz is
installed, you might also use a convenience flag like `--png` to
directly produce an image file. - The visualization simplifies node and
edge labels for clarity. Each entity will appear as a node (often
labeled by its name or ID), and each relationship appears as an arrow
with the predicate label. Literal values attached to entities (like a
name or other data) might appear as separate nodes or annotations. - For
a very large graph, you can limit the visualization to a subgraph (e.g.,
`--focus Alice` to show Alice and directly connected nodes only). This
prevents an overly cluttered diagram. Alternatively, use query commands
to filter what you visualize. - **Example:** if you run
`graphembed visualize -o family.dot`, and your graph contains people and
family relationships, the resulting DOT file can be rendered to show a
network of those individuals connected by edges like \"parentOf\",
\"siblingOf\", etc. This gives a quick insight without manually reading
triples or JSON.

**General Guidelines:** When using GraphEmbed: - **Naming Conventions:**
Entities can be referenced by labels or IDs. If your data is RDF-based,
consider using consistent prefixes (you can set a default base URI via a
config or environment variable). For example, if you have a base
`http://example.com/ns#`, an entity with label `Alice` might be expanded
to `<http://example.com/ns#Alice>`. The CLI tries to manage this
transparently. Avoid using spaces in identifiers unless you quote them
properly in the shell. - **File Handling:** Always specify the correct
file paths for import/export. The tool will not overwrite an existing
file on export unless `--overwrite` is provided. On import, the graph in
memory is appended to by default; use `--clear` before import if you
want to replace the current graph. - **Memory and Performance:**
GraphEmbed loads entire files into memory. Very large knowledge graphs
(e.g., millions of triples) might cause high memory usage. In such
cases, consider splitting data or using an external database. For
embeddings, generating vectors is computationally intensive; model
loading happens once per session for reuse, but each `embed` call will
use CPU (or GPU if supported by the backend) to compute the vector.
Batch embedding is supported via an input file or pipe to avoid
reloading the model repeatedly. - **Extensibility:** The CLI is designed
to be extensible. You can configure it to use different embedding models
or graph stores by editing a config file (usually
`~/.graphembed/config.toml`) or using environment variables. For
example, `GRAPHEMBED_MODEL_DIR` can point to a directory of local models
to avoid downloads. Future plugins might allow custom relationship types
or integration with external vector databases for similarity search.

## Workflow

Using GraphEmbed involves a series of steps from setup to results. Below
is a typical workflow for setting up the tool and utilizing its
features:

1.  **Setup and Installation:** Install the GraphEmbed CLI tool using
    Cargo or download the binary. Ensure that all dependencies (Rust
    standard libraries, any needed system libraries for ML like Intel
    MKL if using CPU acceleration for embeddings) are in place. For
    example, on Linux you might need `libtorch` if using the Torch
    backend, but the Rust crate typically includes it or downloads it
    automatically.
2.  **Initialize a Knowledge Graph:** Start a new knowledge graph or
    import an existing one. For a new graph, you can skip directly to
    adding entities. To import, run `graphembed import data.jsonld`
    (replace with your file). Verify that the CLI reports the number of
    triples or nodes loaded. If you have multiple files, import them one
    by one (the graph will accumulate data).
3.  **Generate or Ingest Embeddings:** If you have text data that needs
    embeddings, use the `embed` command. For a single piece of text:
    `graphembed embed "Your text here..." > vec.json`. This will output
    the embedding vector (e.g., as a JSON array or a space-separated
    list). For batch processing, you could pass a file:
    `graphembed embed --input texts.txt --output vectors.csv`. This
    reads multiple lines of text from `texts.txt` and writes
    corresponding vectors (one per line) to a CSV. If you already have
    embeddings (from Python or another source), prepare them in a CSV or
    JSON format and use `graphembed import vectors.csv` to ingest. After
    this step, your graph may have entities with associated embedding
    vectors.
4.  **Add Entities and Relationships:** Use `add-entity` and `add-rel`
    commands to build or extend your knowledge graph. For instance,
    after importing base data, you might want to add a new entity that
    wasn't in the original file:
    `graphembed add-entity "Carol" --type Person`. Then link Carol to
    existing entities: `graphembed add-rel "Carol" "knows" "Alice"`.
    Continue to use add commands for any new knowledge you want to
    capture. Each operation will update the in-memory graph and confirm
    the addition.
5.  **Update and Delete Operations:** If you discover mistakes or need
    to change the graph, use `update` or `delete`. For example, if
    Carol's name was misspelled,
    `graphembed update entity "Coral" --rename "Carol"` (or similar)
    could fix it. To remove a relationship,
    `graphembed delete rel "Carol" "knows" "Alice"` will delete that
    edge. Always double-check with a query or visualize after
    modifications to ensure the graph is in the desired state.
6.  **Query the Graph:** Now that your graph is populated and possibly
    enriched with embeddings, retrieve information using queries. For
    example, to find all friends of Alice:
    `graphembed query "Alice -> knows -> ?friend"`. The tool will output
    matches, e.g., "friend = Bob, Carol". If SPARQL is enabled and you
    prefer that, use a full SPARQL query for more complex patterns or
    filtering. At this stage, you could also perform semantic similarity
    by combining embeddings and structure: while GraphEmbed doesn't
    directly do vector similarity queries in this version, you can
    manually take two entity embeddings (via `embed` or from stored
    data) and compute cosine similarity using an external tool or a
    small script.
7.  **Visualize (Optional):** For a quick visual check of part of the
    graph, run `graphembed visualize --focus Alice -o subgraph.dot`.
    This generates a DOT file for Alice and her neighbors. Run Graphviz
    or an online DOT viewer to see the graph image. This step helps in
    presentations or just sanity-checking the relationships.
8.  **Export the Graph:** Once you are satisfied with the graph's
    content, save it. Use `graphembed export -f turtle -o output.ttl` to
    get a Turtle file or `-f jsonld` for JSON-LD. The exported file can
    be shared, loaded into other tools, or kept as a persistent store of
    the knowledge graph. If your workflow is iterative, you might export
    after each session as a backup.
9.  **Re-running and Automation:** The above steps can be repeated or
    scripted. Because GraphEmbed is a CLI, you can include it in shell
    scripts or integrate with other processes. For example, you could
    have a nightly job that regenerates embeddings for new text and
    updates a knowledge graph, using a series of `graphembed` commands
    in sequence. The tool's output is designed to be parseable (CSV,
    JSON, or plain text options for commands) so it can fit into larger
    data pipelines.

By following this workflow, you can build a rich knowledge graph that
combines symbolic relationships with vector-based semantic information,
all from the command line. Adjust the steps as needed for your specific
use case (for instance, skip embedding generation if you only need the
graph structure, or vice versa).

## Examples

Below are several usage examples demonstrating GraphEmbed's CLI commands
and their outputs. These examples assume you have a graph about people
and their relationships, as well as some textual data to embed.

- **Generating a Text Embedding:** Use the `embed` command with a model
  to convert text into an embedding vector.

<!-- -->

- $ graphembed embed -m all-MiniLM-L6-v2 "Rust is a systems programming language."
      [0.102, 0.340, -0.215, ..., 0.877]

  *Output:* A JSON-like array of floating-point numbers is printed to
  stdout (here truncated for brevity). Each number represents a
  dimension in the embedding space (e.g., 384 dimensions for MiniLM).
  You can redirect this output to a file or parse it in a script. If the
  model isn't specified, the default model's embedding is returned. The
  first run may take a moment to load the model; subsequent calls will
  be faster.

<!-- -->

- **Importing a Knowledge Graph from JSON-LD:** Suppose you have a file
  `people.jsonld` that contains persons and relationships in JSON-LD
  format.

<!-- -->

- $ graphembed import people.jsonld
      Loaded graph with 50 entities, 120 relationships.

  *Output:* The tool confirms the number of entities and relationships
  loaded. Internally, each `@id` in JSON-LD becomes an entity node, and
  each relationship (triple) is stored. If the JSON-LD had context
  definitions for terms like "name" or "knows", those are preserved.
  After import, the graph is ready for queries or edits.

<!-- -->

- **Exporting the Graph to Turtle:** To save the current graph as an RDF
  Turtle file:

<!-- -->

- $ graphembed export -f turtle -o people.ttl
      Exported graph to people.ttl (120 triples).

  *Output:* The graph is written to `people.ttl`. The CLI reports the
  count of triples. In the Turtle file, you'll find prefix declarations
  (if any) followed by triples such as:

      @prefix foaf: <http://xmlns.com/foaf/0.1/> .
      @prefix ex: <http://example.com/ns#> .

      ex:Alice foaf:knows ex:Bob, ex:Carol ;
              foaf:name "Alice" .

  This indicates Alice knows Bob and Carol, and has a name "Alice". The
  export format is interoperable with other RDF tools.

<!-- -->

- **Adding Entities and Relationships via CLI:** If you want to extend
  the graph with new data:

<!-- -->

- $ graphembed add-entity "Dave" --type Person --id ex:Dave
      Created entity 'Dave' (ex:Dave) of type Person.

      $ graphembed add-rel "Dave" "knows" "Alice"
      Added relationship: Dave --knows--> Alice

  *Output:* The first command adds a new entity named "Dave". We
  explicitly provided an ID `ex:Dave` in the example (using a prefix
  `ex` defined perhaps from the imported data). The tool confirms
  creation. The second command adds a relationship indicating Dave knows
  Alice. The CLI confirms the edge addition in a readable format. If
  "Alice" was not already in the graph, it would either create a new
  node or warn; in this case Alice exists from prior data.

<!-- -->

- **Updating an Entity's Property:** You can add or change properties on
  an entity. For example:

<!-- -->

- $ graphembed update entity "Dave" --set "age=30"
      Updated entity 'Dave': set age = "30"^^<http://www.w3.org/2001/XMLSchema#integer>.

  *Output:* This sets Dave's age to 30 (the CLI infers it as an integer
  literal in RDF terms). The confirmation shows the RDF literal with
  datatype. If the property didn't exist, it's added; if it existed,
  it's updated to the new value. You could similarly update a
  relationship (e.g., change its predicate or qualifiers) with the
  appropriate syntax.

<!-- -->

- **Deleting a Relationship:** Remove an edge from the graph:

<!-- -->

- $ graphembed delete rel "Dave" "knows" "Alice"
      Relationship 'Dave knows Alice' deleted.

  *Output:* The specified triple is removed. If there were multiple
  triples with Dave as subject and Alice as object under different
  predicates, only the one with predicate "knows" is removed. Deleting
  an entity (with `delete entity`) would remove all triples involving
  that entity.

<!-- -->

- **Querying for Connections:** Retrieve information with a simple
  query.

<!-- -->

- $ graphembed query "Alice -> knows -> ?who"
      Alice knows Bob  
      Alice knows Carol  
      Alice knows Dave

  *Output:* The query finds all `?who` such that Alice *knows* them. The
  results list each matching triple (subject Alice, predicate knows,
  object being each result). In this case, Alice knows Bob, Carol, and
  Dave. The output format is a straightforward listing; you can add
  `--format csv` to get:

      Alice,knows,Bob
      Alice,knows,Carol
      Alice,knows,Dave

  which might be easier for scripts to parse. For more complex querying,
  you could enable SPARQL and do something like:

      $ graphembed query "SELECT ?p ?o WHERE { ex:Alice ?p ?o }"

  resulting in a table of all predicates and objects for Alice.

<!-- -->

- **Visualizing a Subgraph:** To generate a quick visualization, focus
  on a subset of the graph.

<!-- -->

- $ graphembed visualize --focus Alice -o alice.dot && dot -Tpng alice.dot -o alice.png

  *Output:* The first part outputs a DOT file centered on Alice. Suppose
  Alice is connected to Bob, Carol, and Dave as in our graph. The DOT
  file will contain nodes for each person and arrows labeled \"knows\"
  pointing out of Alice to the others. After running Graphviz (`dot`),
  the resulting `alice.png` might show something like: Alice → Bob,
  Alice → Carol, Alice → Dave (with arrows). Each node might be labeled
  with the person's name, and additional properties (like age) could
  appear as annotations or separate nodes depending on the visualization
  mode. This provides a quick visual check that our data is correct
  (e.g., we see Dave connected to Alice as expected from the earlier
  commands).

These examples illustrate typical interactions with GraphEmbed. By
combining these commands, you can script complex operations -- for
instance, automatically embedding new text data and inserting it into
the graph, or exporting subsets of the graph for different audiences.
The CLI's consistent format and use of standard data representations
make it a flexible tool in a larger pipeline.

## References

- **Rust-BERT (HF Transformers in Rust):** [rust-bert
  crate](https://crates.io/crates/rust-bert) -- A Rust library that
  provides ready-to-use NLP transformer models (BERT, DistilBERT, etc.)
  and pipelines for tasks like embeddings, using the `tch` (PyTorch)
  backend. Enables generating sentence embeddings with pre-trained
  Hugging Face models in Rust.
- **Sentence Transformers in Rust:** [sbert
  crate](https://crates.io/crates/sbert) -- A community port of
  SentenceTransformers to Rust, built on rust-bert and tch. Supports
  popular sentence embedding models for semantic search. This can be
  used as an alternative embedding generation backend in GraphEmbed.
- **ONNX Runtime for Rust:** [ort crate](https://crates.io/crates/ort)
  -- Rust bindings for ONNX Runtime, allowing high-performance inference
  of ONNX models. Useful for running SentenceTransformer models exported
  to ONNX, often yielding faster or lighter-weight embedding generation.
  GraphEmbed can leverage this for embedding if configured with the onnx
  feature.
- **Hugging Face Candle:** [candle
  library](https://github.com/huggingface/candle) -- A minimalist Rust
  deep learning framework by Hugging Face. Candle enables running
  transformer models fully in Rust (no Python). It's an alternative
  backend that GraphEmbed could use for embedding generation, especially
  in offline or WASM scenarios.
- **Knowledge Graph RDF Toolkit (Sophia):** [Sophia
  crate](https://crates.io/crates/sophia) -- A comprehensive toolkit for
  RDF and Linked Data in Rust. Supports parsing and writing of multiple
  RDF serialization formats (Turtle, N-Triples, JSON-LD via an
  extension) and provides in-memory graph management. GraphEmbed uses
  libraries like Sophia to handle JSON-LD and Turtle import/export and
  may use its graph interfaces for manipulating triples.
- **RDF Graph Library:** [rdf (RDF.rs)](https://crates.io/crates/rdf) --
  A Rust framework for RDF graphs. It provides data structures for
  triples, graph storage, Turtle parsing, and basic SPARQL querying.
  This or similar libraries serve as the foundation for GraphEmbed's
  knowledge graph representation and querying capabilities.
- **Oxigraph (SPARQL Database):** [Oxigraph
  project](https://crates.io/crates/oxigraph) -- An efficient Rust graph
  database with full SPARQL 1.1 support and persistent storage based on
  RocksDB. While GraphEmbed is in-memory, Oxigraph demonstrates how
  SPARQL queries and persistence can be achieved in Rust. GraphEmbed's
  optional SPARQL querying is inspired by Oxigraph, and advanced users
  might use Oxigraph directly for heavy-duty query needs.
- **Graph Visualization:** [Graphviz DOT
  crate](https://crates.io/crates/graphviz) -- A Rust library for
  generating Graphviz DOT graph descriptions. GraphEmbed uses this or a
  similar output method (potentially via `petgraph`'s dot exporters) to
  produce visualizable graph representations. The DOT format can be
  rendered by Graphviz tools to images.
- **CLI Argument Parser:** [Clap crate](https://crates.io/crates/clap)
  -- A widely used Rust library for parsing command-line arguments.
  GraphEmbed employs Clap to define subcommands (`embed`, `import`,
  etc.), options (like `--model`, `--format`), and help messages,
  ensuring a consistent and user-friendly CLI interface.
- **JSON-LD Processing:** [json-ld
  crate](https://crates.io/crates/json_ld) -- A Rust implementation for
  JSON-LD parsing and serialization. This is used under the hood to
  correctly handle JSON-LD context and linking semantics when importing
  or exporting JSON-LD files in GraphEmbed.

Each of these resources contributes to GraphEmbed's functionality. For
further information, refer to the respective documentation of these
crates. By building on established libraries, GraphEmbed ensures
reliability and leverages community support for tasks like machine
learning inference and semantic data handling.

------------------------------------------------------------------------
