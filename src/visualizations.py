# src/visualizations.py
import os, numpy as np, matplotlib.pyplot as plt, networkx as nx
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
TEAL = "#1D9E75"
PURPLE = "#7F77DD"

def plot_graph(G, ec, n_nodes=50):
    top_nodes = [n for n, _ in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:n_nodes]]
    subG = G.subgraph(top_nodes)
    pos = nx.spring_layout(subG, seed=42, k=1.8)
    sizes = [ec.get(n, 0.01)*8000+100 for n in subG.nodes()]
    colors = [ec.get(n, 0.0) for n in subG.nodes()]
    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx_edges(subG, pos, alpha=0.15, edge_color="gray", ax=ax)
    sc = nx.draw_networkx_nodes(subG, pos, node_size=sizes, node_color=colors, cmap=plt.cm.plasma, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(subG, pos, labels={n: n.split("@")[0][:7] for n in subG.nodes()}, font_size=6, ax=ax)
    plt.colorbar(sc, ax=ax, label="Eigenvector Centrality")
    ax.set_title("Enron Email Network", fontweight="bold"); ax.axis("off")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "graph_visualization.png")
    plt.savefig(path, dpi=150, bbox_inches="tight"); print(f"[viz] Saved: {path}"); plt.show()

def plot_top_recommendations(jaccard_scores, ec_scores, top_n=10):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle("Top-10 Friend Recommendations", fontsize=14, fontweight="bold")
    for ax, scores, title, color in [(axes[0], jaccard_scores, "Jaccard Similarity", TEAL),(axes[1], ec_scores, "Eigenvector Centrality", PURPLE)]:
        top = scores[:top_n]
        labels = [f"{u.split(chr(64))[0][:10]}  <->  {v.split(chr(64))[0][:10]}" for u, v, _ in top]
        values = [s for _, _, s in top]
        max_v = max(values) if max(values) > 0 else 1.0
        norm = [v/max_v for v in values]
        bars = ax.barh(range(top_n), norm[::-1], color=color, alpha=0.82)
        ax.set_yticks(range(top_n)); ax.set_yticklabels(labels[::-1], fontsize=8)
        ax.set_xlabel("Normalised Score"); ax.set_title(title, fontweight="bold"); ax.set_xlim(0, 1.18)
        for bar, val in zip(bars, norm[::-1]):
            ax.text(val+0.01, bar.get_y()+bar.get_height()/2, f"{val:.3f}", va="center", fontsize=8)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "top_recommendations.png")
    plt.savefig(path, dpi=150, bbox_inches="tight"); print(f"[viz] Saved: {path}"); plt.show()

def plot_comparison(r1, r2):
    metrics = ["AUC", "P@10", "P@50"]; x = np.arange(len(metrics)); width = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))
    b1 = ax.bar(x-width/2, [r1[m] for m in metrics], width, label="Jaccard", color=TEAL, alpha=0.85)
    b2 = ax.bar(x+width/2, [r2[m] for m in metrics], width, label="Eigenvector Centrality", color=PURPLE, alpha=0.85)
    ax.set_xticks(x); ax.set_xticklabels(metrics, fontsize=12); ax.set_ylim(0, 1.15)
    ax.set_ylabel("Score"); ax.set_title("Jaccard vs Eigenvector Centrality", fontweight="bold"); ax.legend()
    for bar in list(b1)+list(b2):
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h+0.01, f"{h:.3f}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "method_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches="tight"); print(f"[viz] Saved: {path}"); plt.show()

def plot_degree_distribution(G):
    degrees = sorted([d for _, d in G.degree()], reverse=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(range(1, len(degrees)+1), degrees, "o", color=TEAL, alpha=0.5, markersize=3)
    ax.set_xlabel("Rank (log)"); ax.set_ylabel("Degree (log)"); ax.set_title("Degree Distribution", fontweight="bold")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "degree_distribution.png")
    plt.savefig(path, dpi=150, bbox_inches="tight"); print(f"[viz] Saved: {path}"); plt.show()
