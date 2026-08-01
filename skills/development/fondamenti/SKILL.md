---
name: fondamenti
description: 1. Non conosce la differenza tra Array e LinkedList
---

# Computer Science Skills

## Legenda skills

1. Level 0
2. Level 1
3. Level 2
4. Level 3

### strutture dati

1. Non conosce la differenza tra Array e LinkedList
2. In grado di spiegare e utilizzare array, elenchi collegati, dizionari ecc. In attività pratiche di programmazione
3. Conosce i compromessi spaziali e temporali delle strutture dati di base, Arrays vs LinkedLists, è in grado di spiegare come possono essere implementati gli hashtable e può gestire le collisioni, code prioritarie e modi per implementarli ecc.
4. Conoscenza di strutture dati avanzate come B-tree, cumuli binomiali e di Fibonacci, alberi AVL / Red Black, Splay Trees, Skip List, tentativi ecc.

### algoritmi

1. Non in grado di trovare la media dei numeri in un array
2. Algoritmi di base di ordinamento, ricerca e attraversamento della struttura dei dati e recupero
3. Tree, Graph, semplici algoritmi greedy e divide and conquer, è in grado di comprendere la rilevanza dei livelli di questa matrice.
4. In grado di riconoscere e codificare soluzioni di programmazione dinamica, buona conoscenza di algoritmi grafici, buona conoscenza di algoritmi di calcolo numerico, in grado di identificare problemi NP ecc.

### programmazione dei sistemi

1. Non sa cosa sia un compilatore, un linker o un interprete
2. Conoscenza di base di compilatori, linker e interpreti. Comprende cos'è il codice assembly e come funzionano le cose a livello hardware. Qualche conoscenza di memoria virtuale e paging.
3. Comprende la modalità kernel e la modalità utente, il multi-threading, le primitive di sincronizzazione e il modo in cui sono implementate, in grado di leggere il codice assembly. Comprende il funzionamento delle reti, la comprensione dei protocolli di rete e la programmazione a livello di socket.
4. Comprende l'intero stack di programmazione, hardware (CPU + memoria + cache + interrupt + microcodice), codice binario, assembly, collegamento statico e dinamico, compilazione, interpretazione, compilazione JIT, garbage collection, heap, stack, indirizzamento della memoria ...

## Ingegneria software

### controllo della versione del codice sorgente

1. Backup delle cartelle per data
2. VSS e utente CVS / SVN iniziale
3. Competente nell'uso delle funzionalità CVS e SVN. Sa come ramificare e unire, utilizzare le proprietà del repository di configurazione delle patch, ecc.
4. Conoscenza dei sistemi VCS distribuiti. Ha provato Bzr / Mercurial / Darcs / Git

### build automation

1. Sa solo come *buildare* da IDE
2. Sa come costruire il sistema dalla riga di comando
3. Può impostare uno script per costruire il sistema di base
4. Può impostare uno script per costruire il sistema e anche documentazione, programmi di installazione, generare note di rilascio e contrassegnare il codice nel controllo del codice sorgente

### test automatizzati

1. Pensa che tutti i test siano compito del tester
2. Ha scritto unit test automatizzati e fornisce buoni casi di unit test per il codice che viene scritto
3. Ha scritto codice in modo TDD
4. Comprende ed è in grado di impostare test funzionali, carico / prestazioni e UI automatizzati

## Programmazione

### scomposizione del problema

1. Solo codice lineare con copia incolla per il riutilizzo
2. In grado di suddividere il problema in più funzioni
3. In grado di elaborare funzioni / oggetti riutilizzabili che risolvono il problema generale
4. Utilizzo di strutture e algoritmi di dati appropriati e produzione di codice generico / orientato agli oggetti che incapsula aspetti del problema soggetti a modifiche.


### systems decomposition

1. Non in grado di pensare al di sopra del livello di un singolo file / classe
2. In grado di suddividere lo spazio problematico e la soluzione di progettazione fintanto che si trova all'interno della stessa piattaforma / tecnologia
3. In grado di progettare sistemi che abbracciano più tecnologie / piattaforme.
4. In grado di visualizzare e progettare sistemi complessi con più linee di prodotti e integrazioni con sistemi esterni. Inoltre dovrebbe essere in grado di progettare sistemi di supporto alle operazioni come monitoraggio, reporting, failover ecc.

### comunicazione

1. Non è in grado di esprimere pensieri / idee ai colleghi. Ortografia e grammatica scadenti.
2. I colleghi possono capire cosa viene detto. Buona ortografia e grammatica.
3. È in grado di comunicare efficacemente con i colleghi
4. In grado di comprendere e comunicare pensieri / progetti / idee / specifiche in modo inequivocabile e adattare la comunicazione al contesto

### organizzazione del codice all'interno di un file

1. nessuna prova di organizzazione all'interno di un file
2. I metodi sono raggruppati logicamente o per accessibilità
3. Il codice è raggruppato in regioni e ben commentato con riferimenti ad altri file di origine
4. Il file ha intestazione della licenza, riepilogo, utilizzo dello spazio vuoto ben commentato e coerente. Il file dovrebbe essere bellissimo.

### organizzazione del codice tra i file

1. Nessun pensiero dato all'organizzazione del codice tra i file
2. I file correlati sono raggruppati in una cartella
3. Ogni file fisico ha uno scopo unico, ad es. una definizione di classe, un'implementazione di una caratteristica ecc.
4. L'organizzazione del codice a livello fisico è strettamente correlata al design e l'analisi dei nomi dei file e della distribuzione delle cartelle fornisce approfondimenti sulla progettazione

### organizzazione dell'albero dei sorgenti

1. Tutto in una cartella
2. Separazione di base del codice in cartelle logiche.
3. Nessuna dipendenza circolare, binari, librerie, documenti, build, codice di terze parti, tutto organizzato in cartelle appropriate
4. Il layout fisico dell'albero di origine corrisponde alla gerarchia logica e all'organizzazione. I nomi delle directory e l'organizzazione forniscono informazioni sulla progettazione del sistema.

### leggibilità del codice

1. Nomi mono-sillabe
2. Buoni nomi per file, classi di variabili, metodi ecc.
3. Nessuna funzione lunga, commenti che spiegano codice insolito, correzioni di bug, presupposti del codice
4. Le ipotesi del codice vengono verificate utilizzando assert, il codice scorre in modo naturale - nessuna nidificazione profonda di condizionali o metodi

### defensive coding

1. Non capisce il concetto
2. Controlla tutti gli argomenti e asserisce i presupposti critici nel codice
3. Si assicura di controllare i valori di ritorno e controllare le eccezioni intorno al codice che può non riuscire.
4. Ha la sua libreria per aiutare con la codifica difensiva, scrive unit test che simulano i guasti

### gestione degli errori

1. Codifica solo *happy case*
2. Gestione degli errori di base intorno al codice che può generare eccezioni / generare errori
3. Assicura che errori / eccezioni lascino il programma in buono stato, le risorse, le connessioni e la memoria siano tutte pulite correttamente
4. Codici per rilevare prima possibili eccezioni, mantenere una strategia di gestione delle eccezioni coerente in tutti i livelli di codice, elaborare linee guida sulla gestione delle eccezioni per l'intero sistema.

### IDE

1. Utilizza principalmente IDE per la modifica del testo
2. Conosce l'interfaccia, è in grado di utilizzare efficacemente l'IDE utilizzando i menu.
3. Conosce le scorciatoie da tastiera per le operazioni più utilizzate.
4. Ha scritto macro personalizzate

### API

1. Ha bisogno di cercare frequentemente la documentazione
2. Ha in memoria le API utilizzate più di frequente
3. Conoscenza ampia e approfondita dell'API
4. Ha scritto librerie che si trovano in cima all'API per semplificare le attività usate di frequente e per colmare le lacune nell'API

### framework

1. Non ha utilizzato alcun framework al di fuori della piattaforma principale
2. Ha sentito parlare ma non ha utilizzato i framework popolari disponibili per la piattaforma.
3. Ha utilizzato più di un framework a titolo professionale ed è esperto con gli idiomi dei framework.
4. Autore del framework

### requirements

1. Accetta i requisiti e i codici forniti secondo le specifiche
2. Pone domande sui casi non considerati nelle specifiche
3. Comprendere il quadro completo e individuare intere aree che devono essere specificate
4. In grado di suggerire alternative e flussi migliori a determinati requisiti sulla base dell'esperienza

### scripting

1. Nessuna conoscenza degli strumenti di scripting
2. File batch / script di shell
3. Perl / Python / Ruby / VBScript / Powershell
4. Ha scritto e pubblicato codice riutilizzabile

### database

1. Pensa che Excel sia un database
2. Conosce i concetti di base del database, la normalizzazione, l'ACID, le transazioni e sa scrivere selezioni semplici
3. In grado di progettare schemi di database validi e normalizzati tenendo presente le query che devono essere eseguite, esperto nell'uso di viste, stored procedure, trigger e tipi definiti dall'utente. Conosce la differenza tra indici cluster e non cluster. Competente nell'uso degli strumenti ORM.
4. Può eseguire l'amministrazione di base del database, l'ottimizzazione delle prestazioni, l'ottimizzazione degli indici, scrivere query di selezione avanzate, è in grado di sostituire l'utilizzo del cursore con sql relazionale, comprende come i dati vengono archiviati internamente, comprende come gli indici vengono archiviati internamente, comprende come i database possono essere specchiati, replicati ecc. Capisce come funziona il commit in due fasi.

## Esperienza

### lingue con esperienza professionale

1. Imperativo o orientato agli oggetti
2. Imperativo, orientato agli oggetti e dichiarativo (SQL), bonus aggiuntivo se comprendono la digitazione statica rispetto a quella dinamica, la digitazione debole o forte e i tipi inferiti statici
3. Funzionale, ulteriore vantaggio se capiscono la valutazione pigra, il curry, le continuazioni
4. Concorrente (Erlang, Oz) e Logic (Prolog)

### piattaforme con esperienza professionale

1. 1
2. 2-3
3. 4-5
4. 6+

### anni di esperienza professionale

1. 1
2. 2-5
3. 6-9
4. 10+

### conoscenza del dominio

1. Nessuna conoscenza del dominio
2. Ha lavorato su almeno un prodotto nel dominio.
3. Ha lavorato su più prodotti nello stesso dominio.
4. Esperto di dominio. Ha progettato e implementato diversi prodotti / soluzioni nel dominio. Esperto con termini standard, protocolli utilizzati nel dominio.


---
## Conoscenza

### conoscenza degli strumenti

1. Limitato all'IDE principale (VS.Net, Eclipse ecc.)
2. Conosce alcune alternative agli strumenti comuni e standard.
3. Buona conoscenza di editor, debugger, IDE, alternative open source ecc. Ha utilizzato strumenti ORM.
4. Ha effettivamente scritto strumenti e script, un ulteriore vantaggio se sono stati pubblicati.

### esperienza dei linguaggi

1. Imperativo o orientato agli oggetti
2. Imperativo, orientato agli oggetti e dichiarativo (SQL), bonus aggiuntivo se comprendono la digitazione statica rispetto a quella dinamica, la digitazione debole o forte e i tipi inferiti statici
3. Funzionale, ulteriore vantaggio se capiscono la valutazione pigra, il curry, le continuazioni
4. Concurrent (Erlang, Oz) e Logic (Prolog)


### codebase knowledge

1. Non ha mai esaminato il codice base
2. Conoscenza di base del layout del codice e di come costruire il sistema
3. Buona conoscenza del codice di base, ha implementato diverse correzioni di bug e forse alcune piccole funzionalità.
4. Ha implementato più grandi funzionalità nella codebase e può facilmente visualizzare le modifiche richieste per la maggior parte delle funzionalità o le correzioni di bug.

### conoscenza delle prossime tecnologie

1. Non ha sentito parlare delle prossime tecnologie
2. Ha sentito parlare delle imminenti tecnologie nel campo
3. Ha scaricato l'anteprima alpha / CTP / beta e ha letto alcuni articoli / manuali
4. Ha giocato con le anteprime e ha effettivamente costruito qualcosa con esso e come bonus lo ha condiviso con tutti gli altri

### platform internals

1. Nessuna conoscenza degli interni della piattaforma
2. Ha una conoscenza di base del funzionamento interno della piattaforma
3. Conoscenza approfondita degli interni della piattaforma e possibilità di visualizzare come la piattaforma prende il programma e lo converte in codice eseguibile.
4. Ha scritto strumenti per migliorare o fornire informazioni sugli interni della piattaforma. Ad esempio disassemblatori, decompilatori, debugger ecc.

### libri di settore

1. Serie Unleashed, serie di 21 giorni, serie di 24 ore, serie di manichini ...
2. Codice completo, non farmi pensare, padronanza delle espressioni regolari
3. Design Patterns, Peopleware, Programming Pearls, Algorithm Design Manual, Pragmatic Programmer, Mythical Man month
4. Struttura e interpretazione di programmi per computer, concetti tecnici, modelli di programmazione per computer, arte della programmazione per computer, sistemi di database, [Thinking Forth] (http://thinking-forth.sourceforge.net/), [Little Schemer] (https : //7chan.org/pr/src/The_Little_Schemer_4th_2.pdf)

### blog di settore

1. Ne ha sentito parlare ma non ne ha mai avuto il tempo.
2. Legge blog di tecnologia / programmazione / ingegneria del software e ascolta regolarmente i podcast.
3. Mantiene un blog di collegamento con una raccolta di articoli e strumenti utili che ha raccolto
4. Mantiene un blog in cui vengono condivise intuizioni personali e pensieri sulla programmazione