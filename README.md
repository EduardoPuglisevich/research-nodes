# Research Nodes — Scientific Article Similarity Networks & Interactive Recommender

> An end-to-end system that models 20,000 scientific articles as a similarity network — from raw metadata extraction through NLP-based similarity scoring, community detection, and centrality analysis, all the way to a deployed interactive web app for exploring the resulting graph and getting article recommendations.

Built individually, start to finish — extraction, modeling, and the web app — as part of a Complex Networks course project at UPC. The course required group-based deliverables (each teammate owned a different course in the semester rather than splitting tasks within each course), so the submission carries the team's names academically, but the implementation below is entirely my own work.

**Stack:** Python · scikit-learn · NetworkX · CDlib (Leiden/Louvain/Infomap) · Flask · D3.js

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Dataset](#dataset)
- [Skills Demonstrated](#skills-demonstrated)
- [Tech Stack](#tech-stack)
- [Methodology & Results](#methodology--results)
- [Interactive Web Application](#interactive-web-application)

---

Traditional academic search engines (Scopus, Google Scholar) return large volumes of loosely related results ranked by keyword match, leaving the real work of finding meaningfully related literature to manual filtering. This project reframes literature discovery as a **network problem**: articles become nodes, semantic similarity becomes edge weight, and standard complex-network tooling — community detection, centrality — surfaces thematic clusters and influential papers that keyword search alone can't reveal. The output isn't just an analysis notebook — it's wired into a working web app where a user picks an article and gets back the most similar papers and the most influential ones in its thematic community.

## Problem Statement

- How can similarity-based networks of scientific articles improve the precision and efficiency of literature search?
- Which NLP technique best captures meaningful similarity between article titles at scale — lexical, statistical, or deep semantic?
- Which complex network algorithm best uncovers the true thematic structure of a large, densely-connected similarity graph?

## Dataset

- **Source:** Scopus (Elsevier API)
- **Records:** 20,000 multidisciplinary scientific articles
- **Attributes:** authors, title, source journal, citation count, DOI, abstract, index keywords, search tag

> **Note:** the raw dataset isn't included in this repository. It was extracted via the Scopus/Elsevier API for academic use, and Elsevier's terms of use restrict bulk redistribution of extracted metadata — so it's kept out of the repo by design. The notebook documents the extraction and cleaning steps for anyone with their own Scopus access.

---

## Skills Demonstrated

| Area | Where it shows up |
|---|---|
| NLP similarity modeling, evaluated comparatively | Three approaches benchmarked head-to-head: TF-IDF + cosine similarity, Levenshtein distance, and SBERT sentence embeddings — not just one technique applied blindly |
| Graph construction from unstructured text | 20,000 articles turned into a weighted, undirected similarity graph via pairwise scoring, with a tunable threshold to prune weak edges |
| Community detection, algorithm comparison | Louvain, Infomap, and Leiden benchmarked against each other by modularity across a full threshold sweep — Leiden selected on evidence (modularity 0.537 at threshold 0.12), not by default |
| Centrality analysis | Closeness centrality and PageRank computed per-community to surface both "structurally central" and "most-referenced" articles |
| Full-stack delivery of a research result | Flask backend + D3.js force-directed graph visualization, turning a static analysis into an interactive tool a non-technical user can actually query |
| Recursive graph traversal | Custom weighted subgraph extraction (`create_weighted_subgraph`) walking N-hop neighborhoods above a similarity threshold, used to power the "similar articles" recommendation feature live in the app |

---

## Tech Stack

| Layer | Technology |
|---|---|
| NLP / similarity | scikit-learn (`TfidfVectorizer`), `python-Levenshtein`, `sentence-transformers` (SBERT) |
| Network analysis | NetworkX, CDlib (Louvain, Infomap, Leiden) |
| Data handling & viz | Pandas, NumPy, Matplotlib, Seaborn, WordCloud |
| Web application | Flask (Python backend), Jinja2 templates, Bootstrap |
| Graph visualization | D3.js (force-directed graph, drag interactions, tooltips) |
| Environment | Jupyter Notebook |

---

## Methodology & Results

### Similarity modeling
Three similarity techniques were implemented and compared on article titles, not just theorized about:

1. **TF-IDF + cosine similarity** — selected for the final pipeline for its scalability and computational efficiency at 20,000-article scale.
2. **Levenshtein distance** — evaluated as a lexical baseline; limited in capturing semantic relationships between differently-worded but related titles.
3. **SBERT (Sentence-BERT)** — evaluated for deep semantic similarity; noted as a strong candidate for future extension once abstract-level (not just title-level) similarity is in scope.

### Community detection
Three algorithms — Louvain, Infomap, and Leiden — were each run across a full sweep of similarity thresholds (0 to 1), tracking modularity at every step to find the threshold/algorithm combination that best balances cohesive communities against over-fragmentation.

**Result at the selected threshold (0.12):**

| Metric | Value |
|---|---|
| Algorithm | Leiden |
| Nodes | 984 |
| Edges | 91,545 |
| Communities | 5 |
| Modularity | 0.537 |

Leiden was chosen because it consistently produced higher modularity than Louvain and Infomap across the threshold sweep, not because it's the newest algorithm in the comparison — the notebook shows the actual modularity curves behind that decision.

### Centrality analysis
Within each of the 5 detected communities, **closeness centrality** identifies the article most structurally accessible to the rest of its community, while **PageRank** identifies the article with the strongest connections to other influential articles — together giving two different, complementary answers to "what's the most important paper in this cluster."

---

## Interactive Web Application

The analysis output (the similarity graph and per-article centrality scores) feeds directly into a Flask app rather than staying a static notebook result:

- **Home page**: surfaces the top 5 articles by PageRank across the whole corpus as a starting point.
- **Search & explore**: pick any article, set a similarity threshold via a live slider, and the app extracts an N-hop weighted subgraph around it, rendered as an interactive D3.js force-directed graph (drag nodes, hover for details).
- **Two recommendation modes side by side**: direct neighbors by edge weight ("most similar to this specific article") versus top articles by closeness centrality within the same community ("most central to this article's broader theme") — surfacing the difference between local similarity and thematic importance.

The similarity pipeline currently runs on TF-IDF for scalability; the notebook's SBERT comparison already shows where swapping in semantic embeddings would add the most value, making it a natural next iteration rather than a distant idea.