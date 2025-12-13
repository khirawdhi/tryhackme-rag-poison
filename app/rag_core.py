#!/usr/bin/env python3
import math
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

WORD_RE = re.compile(r"[a-zA-Z0-9_]+")

def tokenize(text: str) -> List[str]:
    return [t.lower() for t in WORD_RE.findall(text)]

def cosine(a: List[float], b: List[float]) -> float:
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))

@dataclass
class Chunk:
    doc_id: str
    source: str     # "official" or "untrusted"
    text: str

def build_vocab_and_idf(chunks: List[Chunk]) -> Tuple[Dict[str, int], List[float]]:
    df: Dict[str, int] = {}
    for ch in chunks:
        seen = set(tokenize(ch.text))
        for term in seen:
            df[term] = df.get(term, 0) + 1

    vocab = {term: i for i, term in enumerate(sorted(df.keys()))}
    n_docs = len(chunks)
    idf = [0.0] * len(vocab)

    for term, i in vocab.items():
        dfi = df[term]
        idf[i] = math.log((n_docs + 1) / (dfi + 1)) + 1.0

    return vocab, idf

def tfidf_vector(text: str, vocab: Dict[str, int], idf: List[float]) -> List[float]:
    tf: Dict[int, int] = {}
    for tok in tokenize(text):
        if tok in vocab:
            idx = vocab[tok]
            tf[idx] = tf.get(idx, 0) + 1

    vec = [0.0] * len(vocab)
    if not tf:
        return vec

    max_tf = max(tf.values())
    for idx, count in tf.items():
        norm_tf = count / max_tf
        vec[idx] = norm_tf * idf[idx]
    return vec

def rank_chunks(query: str, chunks: List[Chunk], vectors: List[List[float]],
                vocab: Dict[str, int], idf: List[float], top_k: int = 3,
                trusted_only: bool = False) -> List[Tuple[float, Chunk]]:
    qvec = tfidf_vector(query, vocab, idf)
    scored: List[Tuple[float, Chunk]] = []
    for ch, v in zip(chunks, vectors):
        if trusted_only and ch.source != "official":
            continue
        s = cosine(qvec, v)
        scored.append((s, ch))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]
