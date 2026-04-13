# src/jaccard.py
import networkx as nx

def jaccard_score(G: nx.Graph, u: str, v: str) -> float:
    nu = set(G.neighbors(u))
    nv = set(G.neighbors(v))
    union = nu | nv
    intersection = nu & nv
    if not union:
        return 0.0
    return len(intersection) / len(union)

def compute_jaccard_scores(G: nx.Graph, candidate_pairs: list) -> list:
    print("[jaccard] Computing Jaccard scores...")
    results = []
    for u, v in candidate_pairs:
        score = jaccard_score(G, u, v)
        results.append((u, v, score))
    results.sort(key=lambda x: x[2], reverse=True)
    print(f"[jaccard] Done. Top score: {results[0][2]:.4f}")
    return results
