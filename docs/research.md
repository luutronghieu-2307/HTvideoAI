# Research Pipeline Component

## Purpose

The **Research Pipeline** component allows MoneyPrinterTurbo to discover web sources and retrieve evidence excerpts before LLM script generation. It uses a self-hosted SearXNG JSON API endpoint or local evidence ingestion.

## Key Features

- **Source Discovery (`discover(query)`)**: Finds web sources, titles, and URLs for a given topic.
- **Evidence Retrieval (`retrieve(question)`)**: Extracts text excerpts and generates SHA-256 checksums for claim-to-source traceability.
- **Factuality Support**: Passes retrieved research notes directly into the LLM system prompt to prevent hallucinations.

## Usage

```python
from app.services.research import SearxngResearchBackend

backend = SearxngResearchBackend(base_url="http://127.0.0.1:8080")
candidates = backend.discover("Why do humans dream?")
evidence = backend.retrieve("Why do humans dream?")
```

## Testing

Covered in `test/services/test_research.py`.
