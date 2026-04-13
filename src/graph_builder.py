# src/graph_builder.py
import networkx as nx
import numpy as np

def build_graph(edges_weighted: list) -> nx.Graph:
    print("[graph_builder] Building graph...")
    G = nx.Graph()
    for u, v, w in edges_weighted:
        G.add_edge(u, v, weight=w)
    G.remove_edges_from(nx.selfloop_edges(G))
    largest_cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()
    print(f"[graph_builder] Nodes: {G.number_of_nodes()}")
    print(f"[graph_builder] Edges: {G.number_of_edges()}")
    return G

def train_test_split(G: nx.Graph, test_ratio: float = 0.1, seed: int = 42):
    np.random.seed(seed)
    all_edges = list(G.edges())
    n_test = max(1, int(test_ratio * len(all_edges)))
    idx = np.random.choice(len(all_edges), n_test, replace=False)
    test_edges = [all_edges[i] for i in idx]
    G_train = G.copy()
    G_train.remove_edges_from(test_edges)
    print(f"[graph_builder] Test edges held out: {len(test_edges)}")
    print(f"[graph_builder] Train edges: {G_train.number_of_edges()}")
    return G_train, test_edges

def get_candidate_pairs(G: nx.Graph, max_pairs: int = 5000) -> list:
    print("[graph_builder] Generating candidate pairs...")
    candidates = set()
    for node in G.nodes():
        neighbors = set(G.neighbors(node))
        for nbr in neighbors:
            for fof in G.neighbors(nbr):
                if fof != node and not G.has_edge(node, fof):
                    candidates.add(tuple(sorted([node, fof])))
        if len(candidates) >= max_pairs:
            break
    result = list(candidates)[:max_pairs]
    print(f"[graph_builder] Candidate pairs: {len(result)}")
    return result
