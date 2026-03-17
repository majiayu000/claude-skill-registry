---
name: lucene-net
description: >
  USE FOR: Full-text search indexing and querying, faceted search, autocomplete and suggestion
  systems, document search with relevance ranking, and applications requiring embedded search
  without an external server. DO NOT USE FOR: Relational data querying (use EF Core or Dapper),
  real-time analytics on structured data, or scenarios requiring a managed search service
  (use Elasticsearch or Azure AI Search).
license: MIT
metadata:
  displayName: "Lucene.NET"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Apache Lucene.NET Official Website"
    url: "https://lucenenet.apache.org/"
  - title: "Lucene.NET GitHub Repository"
    url: "https://github.com/apache/lucenenet"
  - title: "Lucene.Net NuGet Package"
    url: "https://www.nuget.org/packages/Lucene.Net"
---

# Lucene.NET

## Overview

Lucene.NET is a high-performance, full-featured text search engine library ported from Apache Lucene (Java) to .NET. It provides indexing and searching of text documents with relevance ranking, Boolean queries, phrase queries, wildcard queries, fuzzy matching, and faceting. Unlike Elasticsearch or Solr, Lucene.NET is an embedded library -- it runs in-process with no external server dependency.

Lucene.NET stores its index on the local filesystem (or in memory for testing) and provides near-real-time search capabilities. It is suited for applications that need powerful text search without the operational complexity of a separate search cluster.

The current stable version targets the Lucene 4.8 API. Install via NuGet: `dotnet add package Lucene.Net` plus `Lucene.Net.Analysis.Common` for analyzers and `Lucene.Net.QueryParser` for query parsing.

## Index Creation and Document Indexing

```csharp
using Lucene.Net.Analysis.Standard;
using Lucene.Net.Documents;
using Lucene.Net.Index;
using Lucene.Net.Store;
using Lucene.Net.Util;

public sealed class ArticleIndexer : IDisposable
{
    private const LuceneVersion AppLuceneVersion = LuceneVersion.LUCENE_48;
    private readonly FSDirectory _directory;
    private readonly StandardAnalyzer _analyzer;
    private readonly IndexWriter _writer;

    public ArticleIndexer(string indexPath)
    {
        _directory = FSDirectory.Open(indexPath);
        _analyzer = new StandardAnalyzer(AppLuceneVersion);
        var config = new IndexWriterConfig(AppLuceneVersion, _analyzer)
        {
            OpenMode = OpenMode.CREATE_OR_APPEND
        };
        _writer = new IndexWriter(_directory, config);
    }

    public void IndexArticle(int id, string title, string body, string author, DateTime publishDate)
    {
        var doc = new Document
        {
            new Int32Field("id", id, Field.Store.YES),
            new TextField("title", title, Field.Store.YES),
            new TextField("body", body, Field.Store.YES),
            new StringField("author", author, Field.Store.YES),
            new Int64Field("publishDate", publishDate.Ticks, Field.Store.YES)
        };

        // Update existing or add new
        _writer.UpdateDocument(new Term("id", id.ToString()), doc);
    }

    public void DeleteArticle(int id)
    {
        _writer.DeleteDocuments(new Term("id", id.ToString()));
    }

    public void Commit()
    {
        _writer.Commit();
    }

    public void Dispose()
    {
        _writer.Dispose();
        _analyzer.Dispose();
        _directory.Dispose();
    }
}
```

## Searching the Index

```csharp
using Lucene.Net.Analysis.Standard;
using Lucene.Net.Index;
using Lucene.Net.Search;
using Lucene.Net.Store;
using Lucene.Net.Util;

public sealed class ArticleSearcher : IDisposable
{
    private const LuceneVersion AppLuceneVersion = LuceneVersion.LUCENE_48;
    private readonly FSDirectory _directory;
    private readonly DirectoryReader _reader;
    private readonly IndexSearcher _searcher;

    public ArticleSearcher(string indexPath)
    {
        _directory = FSDirectory.Open(indexPath);
        _reader = DirectoryReader.Open(_directory);
        _searcher = new IndexSearcher(_reader);
    }

    public SearchResults Search(string queryText, int page, int pageSize)
    {
        using var analyzer = new StandardAnalyzer(AppLuceneVersion);
        var parser = new Lucene.Net.QueryParsers.Classic.MultiFieldQueryParser(
            AppLuceneVersion,
            new[] { "title", "body" },
            analyzer);

        Query query = parser.Parse(queryText);

        int topN = page * pageSize;
        TopDocs topDocs = _searcher.Search(query, topN);

        var results = new List<SearchResult>();
        int start = (page - 1) * pageSize;

        for (int i = start; i < Math.Min(start + pageSize, topDocs.ScoreDocs.Length); i++)
        {
            ScoreDoc scoreDoc = topDocs.ScoreDocs[i];
            var doc = _searcher.Doc(scoreDoc.Doc);

            results.Add(new SearchResult
            {
                Id = int.Parse(doc.Get("id")),
                Title = doc.Get("title"),
                Author = doc.Get("author"),
                Score = scoreDoc.Score
            });
        }

        return new SearchResults
        {
            TotalHits = topDocs.TotalHits,
            Results = results
        };
    }

    public void Dispose()
    {
        _reader.Dispose();
        _directory.Dispose();
    }
}

public sealed class SearchResult
{
    public int Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Author { get; set; } = string.Empty;
    public float Score { get; set; }
}

public sealed class SearchResults
{
    public int TotalHits { get; set; }
    public List<SearchResult> Results { get; set; } = new();
}
```

## Advanced Queries

```csharp
using Lucene.Net.Index;
using Lucene.Net.Search;

public sealed class AdvancedQueryBuilder
{
    private readonly IndexSearcher _searcher;

    public AdvancedQueryBuilder(IndexSearcher searcher)
    {
        _searcher = searcher;
    }

    // Boolean query combining multiple conditions
    public TopDocs SearchWithFilters(string keyword, string? author, int maxResults)
    {
        var booleanQuery = new BooleanQuery();

        // Must contain keyword in title or body
        booleanQuery.Add(
            new TermQuery(new Term("title", keyword.ToLowerInvariant())),
            Occur.SHOULD);
        booleanQuery.Add(
            new TermQuery(new Term("body", keyword.ToLowerInvariant())),
            Occur.SHOULD);
        booleanQuery.MinimumNumberShouldMatch = 1;

        // Filter by author if specified
        if (!string.IsNullOrEmpty(author))
        {
            booleanQuery.Add(
                new TermQuery(new Term("author", author)),
                Occur.MUST);
        }

        return _searcher.Search(booleanQuery, maxResults);
    }

    // Fuzzy search for handling typos
    public TopDocs FuzzySearch(string term, int maxResults)
    {
        var fuzzyQuery = new FuzzyQuery(new Term("title", term.ToLowerInvariant()), 2);
        return _searcher.Search(fuzzyQuery, maxResults);
    }

    // Wildcard search
    public TopDocs WildcardSearch(string pattern, int maxResults)
    {
        var wildcardQuery = new WildcardQuery(new Term("title", pattern.ToLowerInvariant()));
        return _searcher.Search(wildcardQuery, maxResults);
    }

    // Phrase search
    public TopDocs PhraseSearch(string field, string[] terms, int maxResults)
    {
        var phraseQuery = new PhraseQuery();
        foreach (string term in terms)
        {
            phraseQuery.Add(new Term(field, term.ToLowerInvariant()));
        }
        phraseQuery.Slop = 1; // Allow one word between terms
        return _searcher.Search(phraseQuery, maxResults);
    }
}
```

## Near-Real-Time Search with SearcherManager

```csharp
using Lucene.Net.Analysis.Standard;
using Lucene.Net.Index;
using Lucene.Net.Search;
using Lucene.Net.Store;
using Lucene.Net.Util;

public sealed class NrtSearchService : IDisposable
{
    private const LuceneVersion AppLuceneVersion = LuceneVersion.LUCENE_48;
    private readonly IndexWriter _writer;
    private readonly SearcherManager _searcherManager;

    public NrtSearchService(string indexPath)
    {
        var directory = FSDirectory.Open(indexPath);
        var analyzer = new StandardAnalyzer(AppLuceneVersion);
        var config = new IndexWriterConfig(AppLuceneVersion, analyzer);

        _writer = new IndexWriter(directory, config);
        _searcherManager = new SearcherManager(_writer, true, null);
    }

    public void Index(Lucene.Net.Documents.Document doc)
    {
        _writer.AddDocument(doc);
        _searcherManager.MaybeRefresh(); // Near-real-time refresh
    }

    public TopDocs Search(Query query, int maxResults)
    {
        IndexSearcher searcher = _searcherManager.Acquire();
        try
        {
            return searcher.Search(query, maxResults);
        }
        finally
        {
            _searcherManager.Release(searcher);
        }
    }

    public void Dispose()
    {
        _searcherManager.Dispose();
        _writer.Dispose();
    }
}
```

## Analyzer Comparison

| Analyzer | Behavior | Use Case |
|---|---|---|
| `StandardAnalyzer` | Tokenizes, lowercases, removes stop words | General-purpose English text |
| `WhitespaceAnalyzer` | Splits on whitespace only | Identifiers, codes |
| `KeywordAnalyzer` | Treats entire value as one token | Exact-match fields (IDs, emails) |
| `SimpleAnalyzer` | Splits on non-letter characters, lowercases | Basic text |
| `CustomAnalyzer` | User-defined token filters | Language-specific, domain-specific |

## Best Practices

1. Use `StandardAnalyzer` for general-purpose text search and switch to a language-specific analyzer (e.g., `EnglishAnalyzer`) when stemming and language-aware stop words improve relevance.
2. Use `StringField` for exact-match fields like IDs and categories and `TextField` for full-text searchable content to ensure correct indexing behavior.
3. Call `IndexWriter.Commit()` after batch indexing operations rather than after every document to amortize the cost of flushing segments to disk.
4. Use `SearcherManager` with `MaybeRefresh()` for near-real-time search instead of reopening `DirectoryReader` manually, which avoids resource leaks and simplifies lifecycle management.
5. Acquire and release `IndexSearcher` through `SearcherManager` in a try-finally block to ensure searchers are returned even when queries throw exceptions.
6. Implement pagination with `TopDocs.ScoreDocs` array slicing rather than using `SearchAfter`, which is only needed for deep pagination beyond 10,000 results.
7. Store only fields you need to display in search results (with `Field.Store.YES`); for fields only used for filtering or sorting, use `Field.Store.NO` to reduce index size.
8. Use `FuzzyQuery` with a maximum edit distance of 1 or 2 for typo tolerance, but avoid it on large indexes with short terms where it may produce too many matches.
9. Run `IndexWriter.ForceMerge(1)` during off-peak maintenance windows to optimize the index into a single segment, improving query performance at the cost of a one-time I/O spike.
10. Dispose all Lucene.NET resources (`IndexWriter`, `DirectoryReader`, `FSDirectory`, analyzers) in the correct order during application shutdown to prevent index corruption.
