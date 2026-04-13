# Enron Email Friend Recommendation System

A graph-based recommendation system built on the Enron Email Dataset that predicts potential connections between users and identifies tightly connected communities. The project compares classical graph methods with a Graph Neural Network approach for link prediction.

---

## Overview

Large-scale communication networks make it difficult to identify meaningful relationships. This project models email interactions as a graph and predicts potential new connections using:

- Local similarity methods (Jaccard Similarity)
- Global influence methods (Eigenvector Centrality)
- Graph Neural Networks (LightGCN-based FriendGNN)

It also performs clique analysis to detect tightly connected groups and suggest expansion candidates.

---

## Dataset

- **Source:** Enron Email Dataset (Kaggle)
- **Total emails:** ~517,401
- **Time period:** 1999–2002
- **Raw file:** `emails.csv`

---

## Graph Construction

- **Nodes:** Users (email addresses)
- **Edges:** Email interactions between users
- **Edge Weight:** Number of emails exchanged
- **Graph Type:** Undirected, weighted

### Final Graph (processed version)
- Nodes: 3,939  
- Edges: 7,185  

### Extended Graph (full pipeline)
- ~36,000 users  
- ~104,000 edges  

---

## Features

### Data Preprocessing
- Parsing raw email headers  
- Cleaning and normalizing email addresses  
- Expanding multi-recipient fields into individual edges  

### Graph Modeling
- Bidirectional user-user interaction graph  
- Weighted edges based on communication frequency  

### Train / Validation / Test Split
- 80% training  
- 10% validation  
- 10% testing (random edge split)  

---

## Methods

### 1. Jaccard Similarity (Local)

J(A, B) = |N(A) ∩ N(B)| / |N(A) ∪ N(B)|


- Fast and simple  
- Based on shared neighbors  
- Limitation: Produces many ties and weak ranking  

---

### 2. Eigenvector Centrality (Global)

- Measures node importance based on connections to influential nodes  
- Inspired by PageRank  
- Captures global structure of the network  

---

### 3. FriendGNN (Graph Neural Network)

- Based on LightGCN architecture  
- Learns 64-dimensional user embeddings  
- Uses message passing over the graph structure  

#### Loss Function
- Bayesian Personalized Ranking (BPR) loss  
- Optimized for implicit feedback (interaction-based, no ratings)  

#### Recommendation Strategy
- Dot product similarity between embeddings  
- Existing connections are masked out  

---

### 4. Clique Analysis

- Implemented using NetworkX  
- Detects maximal cliques (fully connected subgraphs)  
- Uses Jaccard scoring to suggest new members for clique expansion  

---

## Evaluation

### Setup
- Randomly remove 10% of edges as ground truth  
- Predict missing links  

### Metrics
- AUC-ROC  
- Precision@K  

---

## Results

| Method                  | AUC  | Precision@50 |
|------------------------|------|--------------|
| Jaccard Similarity     | 0.37 | 0.00         |
| Eigenvector Centrality | 0.54 | 0.04         |

---

## Conclusion

Eigenvector Centrality outperforms Jaccard Similarity by leveraging global network structure. Graph Neural Networks further improve representation learning by capturing both local and global patterns.

---

## Project Structure

enron-friend-recommendation/
├── data/
├── src/
├── outputs/
├── notebooks/
├── main.py
├── EnronEmailRecommendation.ipynb
├── requirements.txt


---

## Setup Instructions


git clone https://github.com/SHARMI-P/enron-friend-recommendation.git
cd enron-friend-recommendation

python -m venv venv

Activate Environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate


Install Dependencies
pip install -r requirements.txt
Run the Project
python main.py
Tech Stack
Python
PyTorch
PyTorch Geometric
NetworkX
Pandas
NumPy
Matplotlib
Scikit-learn

Future Work
Incorporate temporal dynamics of email interactions
Explore advanced GNN architectures (GraphSAGE, GAT)
Add explainability for recommendations
Deploy as an interactive web application
