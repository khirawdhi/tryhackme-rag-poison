# RAG Data Poisoning: When Knowledge Bases Lie

This repository demonstrates how **Retrieval-Augmented Generation (RAG)** systems can be manipulated through **data poisoning at the knowledge base ingestion layer**, and how simple mitigations can reduce risk.

The project is designed as a **hands-on security lab**.

## Learning Objectives

By completing this lab, you will:

- Understand how RAG systems retrieve and use external data
- Observe how poisoned documents influence AI-generated responses
- Identify indicators of untrusted or malicious retrieved content
- Apply a basic mitigation to reduce RAG data poisoning risk

## Scenario Overview

- An internal AI assistant is used to answer IT and security questions for employees.
- The assistant retrieves documents from a knowledge base before generating answers.
- A contractor uploads a document that appears to be a legitimate policy update.
- After ingestion, the assistant begins suggesting **insecure actions**, such as bypassing MFA.

This lab demonstrates that:
> The **model itself is not hacked** — the **retrieved context is manipulated**.

##  RAG Technical Foundation

Retrieval-Augmented Generation (RAG) works as follows:

1. A user submits a query
2. The system retrieves the most relevant documents
3. Retrieved content is provided as context to the language model
4. The model generates a response based on that context

If malicious data enters the knowledge base, the model may confidently generate unsafe or misleading answers.

## Project Structure

![RAG Data Poisoning Pipeline](/img/rag_poisoning_pipeline.drawio.png)


##  Hands-on Exercise: Poisoning the Retrieval

You will compare the assistant’s behavior in three states:

1. Clean knowledge base (trusted documents only)
2. Poisoned knowledge base (trusted + injected document)
3. Mitigated retrieval (trusted-only filter applied)

## Step 1: Build a Clean Index

cd ~/tryhackme-rag-poison/app

python3 ingest.py --kb ../kb --index ../index_clean.json

python3 query.py --index ../index_clean.json --q "How do I access VPN if MFA is failing?"

Expected behavior:

Top result has source=official
No suggestion to disable MFA. Represents a normal RAG system

## Step 2: Poison the Index

python3 ingest.py --kb ../kb --inject ../injected --index ../index_poisoned.json

python3 query.py --index ../index_poisoned.json --q "How do I access VPN if MFA is failing?"

Expected behavior:

A source=untrusted document may rank highest
The assistant response changes due to altered retrieval context. This demonstrates data poisoning at ingestion time

## Step 3: Apply a Basic Mitigation

python3 query.py --index ../index_poisoned.json --q "How do I access VPN if MFA is failing?" --trusted-only

Expected behavior:

Untrusted documents are excluded. Top result returns to source=official. Response becomes safe again

## Key Security Takeaways

- RAG systems inherit the trustworthiness of their data sources
- The retrieval layer is a critical attack surface
- Source attribution and trust filtering are essential
- Simple mitigations can significantly reduce risk

## Disclaimer
This project is for educational and defensive security purposes only.
Do not use these techniques on systems you do not own or have permission to test.
