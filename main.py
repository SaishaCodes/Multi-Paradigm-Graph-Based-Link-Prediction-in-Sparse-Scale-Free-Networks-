# main.py
import os
import networkx as nx

from src.data_loader   import load_csv, parse_edges
from src.cleaning      import clean_edges
from src.graph_builder import build_graph, train_test_split, get_candidate_pairs
from src.jaccard       import compute_jaccard_scores
from src.eigenvector   import compute_ec, compute_ec_scores
from src.evaluation    import compare
from src.visualizations import (plot_graph, plot_top_recommendations,
                                 plot_comparison, plot_degree_distribution)

CSV_PATH         = os.path.join("data", "emails.csv")
MAX_ROWS         = 50000
MIN_INTERACTIONS = 2
MAX_CANDIDATES   = 5000
TOP_K            = 10

def print_top_k(scores, method_name, k=10):
    print(f"\n{'='*60}")
    print(f"  TOP-{k} RECOMMENDATIONS  -  {method_name}")
    print(f"{'='*60}")
    print(f"  {'#':<4}  {'User A':<28}  {'User B':<28}  Score")
    print(f"  {'-'*56}")
    for i, (u, v, s) in enumerate(scores[:k], 1):
        ua = u.split('@')[0][:25]
        va = v.split('@')[0][:25]
        print(f"  {i:<4}  {ua:<28}  {va:<28}  {s:.6f}")

def main():
    if not os.path.exists(CSV_PATH):
        print("emails.csv not found in data/ folder.")
        print("Running on SYNTHETIC graph...\n")
        G_raw = nx.barabasi_albert_graph(150, 4, seed=42)
        mapping = {i: f"user{i}@enron.com" for i in G_raw.nodes()}
        G_raw = nx.relabel_nodes(G_raw, mapping)
        nx.set_edge_attributes(G_raw, 1, "weight")
        G = G_raw
    else:
        df        = load_csv(CSV_PATH, max_rows=MAX_ROWS)
        raw_edges = parse_edges(df)
        clean     = clean_edges(raw_edges, min_interactions=MIN_INTERACTIONS)
        G         = build_graph(clean)

    G_train, test_edges = train_test_split(G, test_ratio=0.1)
    candidates          = get_candidate_pairs(G_train, max_pairs=MAX_CANDIDATES)
    jaccard_scores      = compute_jaccard_scores(G_train, candidates)
    ec                  = compute_ec(G_train)
    ec_scores           = compute_ec_scores(G_train, candidates, ec)

    print_top_k(jaccard_scores, "JACCARD SIMILARITY",     k=TOP_K)
    print_top_k(ec_scores,      "EIGENVECTOR CENTRALITY", k=TOP_K)

    r1, r2 = compare(jaccard_scores, ec_scores, test_edges)

    print("\n[main] Generating visualisations...")
    plot_degree_distribution(G_train)
    plot_graph(G_train, ec)
    plot_top_recommendations(jaccard_scores, ec_scores, top_n=TOP_K)
    plot_comparison(r1, r2)

    print("\nDone! Check the outputs/ folder for PNG charts.")

if __name__ == "__main__":
    main()
