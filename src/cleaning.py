# src/cleaning.py
import re
from collections import defaultdict

NOISE_PATTERNS = ["no.address@enron.com","enron.announcements","undisclosed","receipt","confirmation","notify","postmaster","mailer-daemon","delivery","administrator","noreply","no-reply"]

def clean_address(addr: str):
    if not addr:
        return None
    addr = addr.strip().lower()
    match = re.search(r"<(.+?)>", addr)
    if match:
        addr = match.group(1).strip()
    if addr.count("@") != 1:
        return None
    if len(addr) > 80:
        return None
    for noise in NOISE_PATTERNS:
        if noise in addr:
            return None
    if not re.match(r"^[\w.\-+]+@[\w.\-]+\.[a-z]{2,}$", addr):
        return None
    return addr

def clean_edges(raw_edges: list, min_interactions: int = 2) -> list:
    print("[cleaning] Cleaning addresses...")
    counter = defaultdict(int)
    for sender, recipient in raw_edges:
        s = clean_address(sender)
        r = clean_address(recipient)
        if s and r and s != r:
            key = tuple(sorted([s, r]))
            counter[key] += 1
    filtered = {k: v for k, v in counter.items() if v >= min_interactions}
    print(f"[cleaning] Pairs after filter: {len(filtered)}")
    return [(u, v, w) for (u, v), w in filtered.items()]
