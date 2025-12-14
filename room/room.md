# `room.md` (TryHackMe room)

```markdown
# RAG Data Poisoning: When Knowledge Bases Lie

---

## Task 1: Learning Objectives

In this room, you will learn how:

- RAG systems retrieve and use external data
- Poisoned documents can influence AI-generated responses
- Untrusted retrieved content can be identified
- Simple mitigations can reduce RAG data poisoning risk

---

## Task 2: Scenario

An internal AI assistant answers IT and security questions for employees.

The assistant retrieves documents from a knowledge base before generating responses.

A contractor uploads a document claiming to be a policy update.  
After ingestion, the assistant begins suggesting insecure actions.

---

## Task 3: Technical Foundation

Retrieval-Augmented Generation (RAG) systems combine:

- **Retrieval** – selecting the most relevant documents
- **Generation** – producing an answer using retrieved content

The language model treats retrieved documents as trusted context.

If malicious data enters the knowledge base, answers can be manipulated without modifying the model.

---

## Task 4: RAG Pipeline Overview

The RAG pipeline follows this flow:

User Query
↓
Document Retrieval (Top-K)
↓
Retrieved Context
↓
LLM Response


Data poisoning occurs at the **ingestion and retrieval layer**, before generation.

---

## Task 5: Hands-on Exercise – Poisoning the Retrieval

You will compare the assistant’s behavior in three states:

1. Clean index (trusted documents only)
2. Poisoned index (trusted + injected document)
3. Mitigated retrieval (trusted-only filter)

> Focus on which document ranks #1 and the `source=` field.

---

### Step 1: Build a Clean Index

```bash
cd ~/tryhackme-rag-poison/app
python3 ingest.py --kb ../kb --index ../index_clean.json
python3 query.py --index ../index_clean.json --q "How do I access VPN if MFA is failing?"
What to notice:

Top result has source=official

Guidance does not suggest disabling MFA

Step 2: Poison the Index
bash
Copy code
python3 ingest.py --kb ../kb --inject ../injected --index ../index_poisoned.json
python3 query.py --index ../index_poisoned.json --q "How do I access VPN if MFA is failing?"
What to notice:

A source=untrusted document may rank highest

The assistant response changes due to altered context

This is data poisoning at the ingestion layer

Step 3: Apply a Mitigation
bash
Copy code
python3 query.py --index ../index_poisoned.json --q "How do I access VPN if MFA is failing?" --trusted-only
What to notice:

Untrusted content is filtered out

Top result returns to source=official

The response becomes safe again

Task 6: Optional Exploration
Try querying:

bash
Copy code
python3 query.py --index ../index_poisoned.json --q "Can we disable MFA temporarily for VPN?"
Then repeat with:

bash
Copy code
python3 query.py --index ../index_poisoned.json --q "Can we disable MFA temporarily for VPN?" --trusted-only
Task 7: Check Your Understanding
Where did the attacker intervene to influence the assistant’s answers?

Why did the injected document rank higher for some queries?

What is one indicator that retrieved context is untrusted?

Name two mitigations that reduce RAG poisoning risk.

What does the --trusted-only flag simulate?

Room Summary
This room demonstrated how RAG systems can be compromised through data poisoning and how basic trust-based controls can significantly reduce risk.
