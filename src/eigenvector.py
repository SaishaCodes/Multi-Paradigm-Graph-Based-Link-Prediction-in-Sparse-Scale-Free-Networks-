# src/eigenvector.py
import networkx as nx

def compute_ec(G: nx.Graph) -> dict:
    print("[eigenvector] Computing eigenvector centrality...")
    try:
        ec = nx.eigenvector_centrality_numpy(G, weight="weight")
    except Exception:
        try:
            ec = nx.eigenvector_centrality(G, max_iter=1000, weight="weight")
        except nx.PowerIterationFailedConvergence:
            print("[eigenvector] Fallback to degree centrality")
            ec = nx.degree_centrality(G)
    print("[eigenvector] Done.")
    return ec

def ec_recommendation_score(G: nx.Graph, u: str, v: str, ec: dict, alpha: float = 2.0) -> float:
    nu = set(G.neighbors(u))
    nv = set(G.neighbors(v))
    mutual = nu & nv
    return ec.get(u, 0.0) + ec.get(v, 0.0) + alpha * sum(ec.get(m, 0.0) for m in mutual)

def compute_ec_scores(G: nx.Graph, candidate_pairs: list, ec: dict) -> list:
    print("[eigenvector] Computing EC recommendation scores...")
    results = []
    for u, v in candidate_pairs:
        score = ec_recommendation_score(G, u, v, ec)
        results.append((u, v, score))
    results.sort(key=lambda x: x[2], reverse=True)
    print(f"[eigenvector] Done. Top score: {results[0][2]:.6f}")
    return results
