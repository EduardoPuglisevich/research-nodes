# Research Nodes: Scientific Article Similarity Networks using NLP and Complex Networks

## Overview

This project focuses on modeling and analyzing a network of scientific articles connected by content similarity in order to improve the efficiency, precision, and interpretability of academic literature search and exploration. The system leverages Natural Language Processing (NLP) techniques and complex network algorithms to build a similarity-based graph where nodes represent scientific articles and edges represent weighted semantic similarity relationships.

By combining TF-IDF–based text similarity with community detection and centrality metrics, the project demonstrates how network science can support bibliographic analysis, thematic clustering, and identification of influential research works at scale.

This approach addresses the limitations of traditional keyword-based academic search engines (e.g., Scopus, Google Scholar), which often return large volumes of loosely related results and require extensive manual filtering.

---

## Problem Statement

The exponential growth of scientific publications has made systematic literature reviews increasingly complex and time-consuming. Although established methodologies ensure rigor and transparency, the initial search and filtering phase remains a major bottleneck.

This project addresses the following research questions:

- How can similarity-based networks of scientific articles improve the precision and efficiency of literature search?
- How can NLP techniques enhance the identification of meaningful similarities between scientific articles?
- Which complex network algorithms are most suitable for analyzing the structure and dynamics of large-scale article similarity networks?

---

## Dataset

The dataset was extracted from **Scopus**, one of the most comprehensive scientific literature databases available.

- **Source:** Scopus (Elsevier API)
- **Extraction date:** September 20, 2024
- **Records:** 20,000 scientific articles
- **Scope:** Multidisciplinary scientific publications

### Article Attributes

Each article includes the following attributes:

- Authors  
- Author full names  
- Author IDs  
- Title  
- Source title (journal)  
- Number of citations  
- DOI  
- Link to full text  
- Abstract  
- Index keywords  
- Search tag (query label)

---

## Methodology

The project follows a structured workflow combining NLP and complex network analysis:

1. Data ingestion and preprocessing  
2. Text vectorization using TF-IDF  
3. Pairwise similarity computation between article titles  
4. Construction of a weighted, undirected similarity graph  
5. Threshold selection to prune weak similarities  
6. Community detection using multiple algorithms  
7. Centrality analysis to identify key articles  
8. Visualization and thematic validation  

---

## Similarity Modeling

Each node represents a scientific article. An edge exists between two nodes if their similarity score exceeds a predefined threshold.

### NLP Techniques Evaluated

- **TF-IDF + Cosine Similarity**  
  Selected for final implementation due to simplicity, scalability, and computational efficiency.

- **Levenshtein Distance**  
  Evaluated for lexical similarity but limited in capturing semantic relationships.

- **SBERT (Sentence-BERT)**  
  Considered for future extensions due to its ability to capture deep semantic context.

The final implementation uses **TF-IDF** as a robust baseline for large-scale similarity analysis.

---

## Community Detection

To identify thematic groupings within the article network, multiple community detection algorithms were evaluated:

- Leiden  
- Louvain  
- InfoMap  

Threshold selection was guided by statistical analysis and the elbow method to balance modularity and fragmentation.

### Selected Algorithm

**Leiden** was selected due to:

- Higher modularity values  
- Cohesive and interpretable communities  
- Robust behavior across similarity thresholds  

At the selected threshold (similarity = 0.12), the resulting graph contains:

- ~984 nodes  
- ~91,545 edges  
- 5 communities  
- Modularidad ≈ 0.537  

---

## Centrality Metrics

To identify influential articles within each community, the following metrics were applied:

### Closeness Centrality

Identifies articles that are structurally closest to all others in their community, highlighting nodes with high accessibility and influence.

### PageRank

Highlights articles with strong connections to other influential articles, serving as key reference points within thematic clusters.

---

## Results

The analysis shows:

- Clearly differentiated thematic communities  
- High internal cohesion within communities  
- Central articles acting as hubs within their domains  
- Strong alignment between detected communities and semantic tags  

Tag distributions and word clouds further validate the coherence of the detected communities.

---

## System Characteristics

- **Graph type:** Undirected, weighted, non-connected  
- **Similarity metric:** TF-IDF cosine similarity  
- **Community detection:** Leiden  
- **Centrality metrics:** Closeness Centrality, PageRank  
- **Visualization:** Network graphs, tag distributions, word clouds  

---

## Tech Stack

- Python  
- Scikit-learn (TF-IDF)  
- NetworkX / iGraph  
- Leiden, Louvain, InfoMap  
- Matplotlib / Seaborn  
- WordCloud  

---

## Future Work

- Integration of semantic embeddings (Word2Vec, SBERT)  
- Similarity analysis using abstracts or full-text content  
- Temporal analysis of evolving research topics  
- Interactive visualization tools  
- Recommendation systems for academic literature  

---

## Contributors

- **Eduardo Elías Puglisevich Vergara**  
