#!/usr/bin/env python3
import argparse
import json

from rag_core import Chunk, rank_chunks

def naive_answer(query: str, top_chunk: Chunk) -> str:
    lines = []
    lines.append("=== Simulated Assistant Response ===")
    lines.append(f"Question: {query}")
    lines.append("")
    lines.append("Answer based on retrieved context:")
    lines.append(top_chunk.text)
    lines.append("")
    lines.append("(In a real RAG system, this retrieved context would be passed into an LLM.)")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="Query the TF-IDF index (RAG poisoning demo).")
    ap.add_argument("--index", required=True, help="Index JSON file from ingest.py")
    ap.add_argument("--q", required=True, help="User query")
    ap.add_argument("--topk", type=int, default=3, help="Top-k chunks to display")
    ap.add_argument("--trusted-only", action="store_true", help="Only retrieve from trusted (official) sources")
    args = ap.parse_args()

    with open(args.index, "r", encoding="utf-8") as f:
        payload = json.load(f)

    vocab = payload["vocab"]
    idf = payload["idf"]
    chunks = [Chunk(**c) for c in payload["chunks"]]
    vectors = payload["vectors"]

    top = rank_chunks(args.q, chunks, vectors, vocab, idf, top_k=args.topk, trusted_only=args.trusted_only)

    print("=== Retrieval Results (Top-K) ===")
    for i, (score, ch) in enumerate(top, start=1):
        print(f"{i}) score={score:.4f} | source={ch.source} | id={ch.doc_id}")
        preview = ch.text.replace("\n", " ")
        print(f"   {preview[:180]}{'...' if len(preview) > 180 else ''}")
        print()

    if not top:
        print("No results. Try a different query.")
        return

    best = top[0][1]
    print(naive_answer(args.q, best))

if __name__ == "__main__":
    main()
