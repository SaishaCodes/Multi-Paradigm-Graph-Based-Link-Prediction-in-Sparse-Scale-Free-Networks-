# src/evaluation.py
from sklearn.metrics import roc_auc_score

def precision_at_k(labels, k):
    if k <= 0:
        return 0.0
    return sum(labels[:k]) / k

def evaluate(scored_pairs, test_edges, method_name):
    test_set = set(tuple(sorted(e)) for e in test_edges)
    labels = []
    scores = []
    for u, v, s in scored_pairs:
        labels.append(1 if tuple(sorted([u, v])) in test_set else 0)
        scores.append(s)
    try:
        auc = roc_auc_score(labels, scores) if sum(labels) > 0 else 0.0
    except Exception:
        auc = 0.0
    p10 = precision_at_k(labels, 10)
    p50 = precision_at_k(labels, 50)
    print(f"\n  -- {method_name} --")
    print(f"     AUC-ROC : {auc:.4f}")
    print(f"     P@10    : {p10:.4f}")
    print(f"     P@50    : {p50:.4f}")
    return {"method": method_name, "AUC": auc, "P@10": p10, "P@50": p50}

def compare(jaccard_scores, ec_scores, test_edges):
    print("\n========================================")
    print("  EVALUATION RESULTS")
    print("========================================")
    r1 = evaluate(jaccard_scores, test_edges, "Jaccard Similarity")
    r2 = evaluate(ec_scores,      test_edges, "Eigenvector Centrality")
    return r1, r2
