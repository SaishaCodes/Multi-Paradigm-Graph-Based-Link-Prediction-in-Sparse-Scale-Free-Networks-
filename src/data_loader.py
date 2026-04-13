# src/data_loader.py
import pandas as pd

def load_csv(csv_path: str, max_rows: int = 50000) -> pd.DataFrame:
    print(f"[data_loader] Loading: {csv_path}")
    df = pd.read_csv(csv_path, nrows=max_rows)
    print(f"[data_loader] Rows loaded: {len(df)}")
    return df

def extract_field(raw_message: str, field: str) -> str:
    for line in str(raw_message).splitlines():
        if line.lower().startswith(field.lower() + ":"):
            return line[len(field) + 1:].strip()
    return ""

def parse_edges(df: pd.DataFrame) -> list:
    print("[data_loader] Parsing sender/recipient pairs...")
    edges = []
    for _, row in df.iterrows():
        msg = str(row.get("message", ""))
        sender = extract_field(msg, "From").lower()
        to_raw = extract_field(msg, "To").lower()
        if not sender or not to_raw:
            continue
        recipients = [r.strip() for r in to_raw.split(",") if r.strip()]
        for r in recipients:
            if r != sender:
                edges.append((sender, r))
    print(f"[data_loader] Raw edges extracted: {len(edges)}")
    return edges
