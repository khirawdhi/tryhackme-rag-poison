#!/usr/bin/env python3
import argparse
import json
import os
from typing import List

from rag_core import Chunk, build_vocab_and_idf, tfidf_vector

def read_text_files(folder: str) -> List[str]:
    files = []
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if os.path.isfile(path) and name.lower().endswith(".txt"):
            files.append(path)
    return files

def chunk_text(doc_text: str) -> List[str]:
    parts = [p.strip() for p in doc_text.split("\n\n") if p.strip()]
    return parts if parts else [doc_text.strip()]

def build_chunks(folder: str, source_label: str) -> List[Chunk]:
    chunks: List[Chunk] = []
    for path in read_text_files(folder):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read().strip()
        doc_id = os.path.basename(path)
        for i, piece in enumerate(chunk_text(txt), start=1):
            chunks.append(Chunk(doc_id=f"{doc_id}#chunk{i}", source=source_label, text=piece))
    return chunks

def main():
    ap = argparse.ArgumentParser(description="Build a tiny TF-IDF index for a RAG poisoning demo.")
    ap.add_argument("--kb", required=True, help="Path to trusted KB folder (txt files)")
    ap.add_argument("--inject", default=None, help="Path to injected/untrusted folder (txt files)")
    ap.add_argument("--index", required=True, help="Output index JSON file")
    args = ap.parse_args()

    chunks: List[Chunk] = []
    chunks.extend(build_chunks(args.kb, "official"))
    if args.inject:
        chunks.extend(build_chunks(args.inject, "untrusted"))

    vocab, idf = build_vocab_and_idf(chunks)
    vectors = [tfidf_vector(ch.text, vocab, idf) for ch in chunks]

    payload = {
        "vocab": vocab,
        "idf": idf,
        "chunks": [{"doc_id": c.doc_id, "source": c.source, "text": c.text} for c in chunks],
        "vectors": vectors,
    }

    with open(args.index, "w", encoding="utf-8") as f:
        json.dump(payload, f)

    print(f"[+] Indexed {len(chunks)} chunk(s). Saved: {args.index}")
    if args.inject:
        print("[!] Included UNTRUSTED injected content. Use --trusted-only during query to simulate mitigation.")

if __name__ == "__main__":
    main()
