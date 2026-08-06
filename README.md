🐾 The Dog Companion | Dynamic AI Persona & Storybook Generator
This is a full-stack AI-driven interactive web application built with Python and Streamlit. I designed it to bring comfort, humor, and emotional solidarity through dynamic storybook art generation and a conversational Snoopy AI companion.

🌟 Overview & Features
Life gets stressful, whether you are pulling an all-nighter for finals or sweating through a heatwave. This application acts as a empathetic companion that mirrors and understands your current situation, offering custom Peanuts-style illustrations alongside witty, yet sympathetic monologues from Snoopy.

Adaptive Persona Engine: Local LLM-driven conversational responses adopting Snoopy's signature personality (relatable, witty, funny, loyal, and slightly sarcastic).

Context-Aware Visual Generation: The customizable prompts dynamically adjust the image and text outputted to match your mood or activity.

Lightweight Multi-Modal Pipeline: Multi-modal image generation is supported using RESTful API routes with dynamic seed generation for unique art images on every interaction.

Custom UI: A streamlined, responsive Streamlit interface optimized for easy maneuverability.

🛠️ Technical Architecture & Stack
```plaintext
[ User Input ]
      │
      ▼
┌───────────────────────────┐
│  1. Retrieval (RAG)       │ ──► Query local search model
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  2. Prompt Augmentation   │ ──► Inject retrieved scene context 
└─────────────┬─────────────┘     (metadata - title + keywords) into Gemma 3
              │
              ▼
┌───────────────────────────┐
│  3. Multi-Modal Gen (LLM) │ ──► Ollama generates Snoopy's dialogue
└─────────────┬─────────────┘     and dynamic image prompts, pretending it is Art Director
              │
              ▼
┌───────────────────────────┐
│  4. Visual Rendering      │ ──► Pollinations.ai API fetches image bytes via
└───────────────────────────┘     Requests + PIL into Streamlit session state
```

Core Stack & Tools Used
- Frontend / UI: Streamlit

- Local LLM Orchestration: Ollama running gemma3:4b

- Image Generation: Pollinations.ai

- Image & Data Processing: Pillow (PIL), Requests, io.BytesIO

- Vector Database & Embeddings (Prototyped): ChromaDB, Pydantic

🧠 Technical Deep-Dive: RAG & Architectural Evolution
1. Retrieval-Augmented Generation (RAG) Pipeline
- This project leverages RAG (Retrieval-Augmented Generation) architecture to ensure Snoopy’s responses and visual scenes remain grounded in specific Peanuts themes while staying true to the user input:
    - Retrieval ($R$): The system processes user inputs through a localized module (search.py) to query a dataset of curated Peanuts scene context
    - Augmentation ($A$): The retrieved scene details, title, and topic context are injected into the system prompt passed to the LLM.
    - Generation ($G$): gemma3:4b processes the augmented context to synthesize accurate dialogues and descriptive 2D animated art.

2. Architectural Pivot: From Static Vector Search to Dynamic Generative Art
Phase 1: Vector Embeddings with ChromaDB (Ingest & Vector Pipeline)
    - In the initial engineering phase, I built a local vector retrieval system using ChromaDB:
        - Data Ingestion (ingest.py): Pre-processed local Peanuts images were packaged into structured objects using Pydantic schemas (schemas.py), extracting AI-generated titles and keyword tags.

        - Semantic Search: User inputs were converted into vector embeddings, querying ChromaDB to display the closest matching pre-existing image using cosine similarity.

Phase 2: Pivot to On-Demand Generative Multi-Modal Art
    - While the vector pipeline succeeded at semantic retrieval, exact image matching felt static and not personal. I evolved the architecture from retrieving static images to generating custom dynamic scenes as the user inputted text:

    - Why the change? If a user says "I'm watching the World Cup," a static database search is limited to pre-stored images on the local machine. By turning the LLM into a Lead Art Director, the system dynamically writes scene descriptions (e.g., "Snoopy is sat excitedly in front of an old-fashioned TV, eating popcorn as he watches 2 teams play soccer on TV") and sends them to Pollinations AI.

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
├── images/                # Local repository for fallback & retrieval index
└── requirements.txt       # Project dependencies
```
