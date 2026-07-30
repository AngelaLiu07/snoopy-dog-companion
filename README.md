🐾 The Dog Companion | Dynamic AI Persona & Storybook Generator
This is a full-stack AI-driven interactive web application built with Python and Streamlit. I designed it to bring comfort, humor, and emotional solidarity through dynamic storybook art generation and a conversational Snoopy AI companion.

🌟 Overview & Features
Life gets stressful, whether you are pulling an all-nighter for finals or sweating through a heatwave. The Dog Companion acts as a empathetic companion that mirrors and understands your current situation, offering custom Peanuts-style illustrations alongside witty, relatable monologues from Snoopy.

Adaptive Persona Engine: Local LLM-driven conversational responses adopting Snoopy's signature personality (relatable, witty, funny, loyal, and slightly sarcastic).

Context-Aware Visual Generation: The customizable prompts dynamically adjust props, lighting, and environments to match your mood or activity.

Lightweight Multi-Modal Pipeline: Fast multi-modal image generation using RESTful API routes with dynamic seed generation for unique art on every interaction.

Cozy Custom UI: A streamlined, responsive Streamlit interface optimized for scannability.

🛠️ Technical Architecture & Stack
```plaintext
[ User Input ]
      │
      ▼
┌───────────────────────────┐
│  1. Retrieval (RAG)       │ ──► Query local asset index / search module
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  2. Prompt Augmentation   │ ──► Inject retrieved scene context into Gemma 3
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  3. Multi-Modal Gen (LLM) │ ──► Ollama generates Snoopy's dialogue
└─────────────┬─────────────┘     and dynamic image prompts, as if it is an Art Director
              │
              ▼
┌───────────────────────────┐
│  4. Visual Rendering      │ ──► Pollinations.ai API fetches image bytes via
└───────────────────────────┘     Requests + PIL into Streamlit session state
```

Core Stack & Tools Used
- Frontend / UI: Streamlit

- Local LLM Orchestration: Ollama running gemma3:4b

- Image Generation: Pollinations.ai (RESTful URL API with custom seed parameterization)

- Image & Data Processing: Pillow (PIL), Requests, io.BytesIO

- Vector Database & Embeddings (Prototyped): ChromaDB, Pydantic

🧠 Technical Deep-Dive: RAG & Architectural Evolution
1. Retrieval-Augmented Generation (RAG) Pipeline
- This project leverages RAG (Retrieval-Augmented Generation) architecture to ensure Snoopy’s responses and visual scenes remain grounded in specific Peanuts themes:
    - Retrieval ($R$): The system processes user inputs through a localized module (search.py) to query a dataset of curated Peanuts scene context
    - Augmentation ($A$): The retrieved scene details, title, and topic context are injected into the system prompt passed to the LLM.
    - Generation ($G$): gemma3:4b processes the augmented context to synthesize both a character-accurate in-person dialogue and a highly descriptive 2D animated art direction prompt.

2. Architectural Pivot: From Static Vector Search to Dynamic Generative Art
Phase 1: Vector Embeddings with ChromaDB (Ingest & Vector Pipeline)
    - In the initial engineering phase, I built a local vector retrieval system using ChromaDB:
        -Data Ingestion (ingest.py): Pre-processed local Peanuts images were into structured objects using Pydantic schemas (schemas.py), extracting AI-generated titles and keyword tags.

        -Semantic Search: User inputs were converted into high-dimensional vector embeddings, querying ChromaDB to display the closest matching pre-existing image using Cosine Similarity.

Phase 2: Pivot to On-Demand Generative Multi-Modal Art
    - While the vector pipeline succeeded at semantic retrieval, exact image matching felt static and not personal. I evolved the architecture from retrieving static images to generating custom dynamic scenes on the fly:

    - Why the change? If a user says "I'm sweating in the desert," a static database search is limited to pre-stored images. By turning the LLM into a Lead Art Director, the system dynamically writes scene descriptions (e.g., "Snoopy slumped over his doghouse wearing sunglasses under a blaring sun") and sends them to Pollinations AI.

    - Preserving the Foundation: The ChromaDB ingestion files (ingest.py, schemas.py) and vector search functions remain preserved in the codebase as an experimental retrieval module.

🚀 Quickstart & Installation
Prerequisites
- Python 3.10+

Ollama installed and running locally with the Gemma model pulled:
```bash
ollama pull gemma3:4b
```

Step-by-Step Setup
1. Clone the repository:
```bash
git clone https://github.com/AngelaLiu07/snoopy-dog-companion.git
cd snoopy-dog-companion
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Launch the Streamlit App:
```bash
streamlit run app.py
```

📂 Project Structure
```Plaintext
├── app.py                 # Main Streamlit interface & UI layout logic
├── image_generation.py    # Pollinations API handler with dynamic seed generation
├── search.py              # Retrieval module for scene titles & keywords
├── ingest.py              # Ingestion pipeline for generating ChromaDB vector embeddings
├── schemas.py             # Pydantic data schemas for image metadata
├── images/                # Local asset repository for fallback & retrieval index
└── requirements.txt       # Project dependencies
```