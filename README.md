# Sign-in Travel Assistant with RAG Chat — Ho Chi Minh City

## 1. Student & Project Information
- **Course:** Computational Thinking
- **Assignment:** Practice 03 Sign-in Travel Assistant with RAG Chat
- **University:** University of Science
- **Student Name:** `Trần Minh Phi`
- **Student ID:** `25127116`
- **Chosen City:** **Ho Chi Minh City, Vietnam** (12 curated entries in `application/knowledge_base.json`)
- **Demonstration Video:** [Youtube](https://www.youtube.com/watch?v=tFSNeuF2vZc "Computational Thinking Assignment 03 Demo: Authentic RAG Chat")

---

## 2. Project Structure

```text
Project_Auth_RAG_Chat/
├── .venv/                       # Python virtual environment
├── ollama/
│   ├── create_tunnel.py         # Creates a Pinggy public tunnel to local Ollama
│   └── ollama_start.py          # Starts local Ollama server (0.0.0.0:11434) & tunnel
├── application/
│   ├── app.py                   # Main Streamlit web UI (Auth + RAG Chat)
│   ├── authentication.py        # Firebase Authentication REST API (Sign up / Sign in)
│   ├── rag.py                   # Embedding, cosine similarity retrieval, and LLM generation
│   └── knowledge_base.json      # 12 curated travel entries for Ho Chi Minh City
├── tmp/
│   └── ollama.log               # log file for local ollama server
├── .env                         # Environment variables (DO NOT commit to Git)
├── .env.example                 # Template for required environment variables
├── main.py                      # Entry script (if applicable)
├── test.py                      # CLI script to verify Ollama embedding & RAG pipeline
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation & test evaluation
```

---

## 3. Installation & Setup Instructions

### Prerequisites
- Python 3.9 or higher
- [Ollama](https://ollama.com/) installed locally with the required models pulled:
  ```bash
  ollama pull embeddinggemma
  ollama pull qwen3:4b
  ```
- A Firebase project with **Email/Password Authentication** enabled.

### Step 1: Clone the Repository & Install Dependencies
```bash
# Clone the project to your device
git clone https://github.com/MinFee2007/RAG_travel_guide.git
cd RAG_travel_guide

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
```
Inside `.env`:
```env
FIREBASE_API_KEY=your_firebase_web_api_key
OLLAMA_BASE_URL=http://localhost:11434
```
*(Note: When running `ollama_start.py`, `OLLAMA_BASE_URL` in `.env` is automatically updated with the active Pinggy tunnel URL).*

### Step 3: Start Ollama & Pinggy Tunnel
In your first terminal, start the local Ollama server and expose it via Pinggy:
```bash
python ollama/ollama_start.py
```

### Step 4: Run the Streamlit Application
In a second terminal (with `.venv` activated), launch the web application:
```bash
streamlit run application/app.py
```
*(Optional)* You can also verify the RAG backend independently before launching the UI:
```bash
python test.py
```

---

## 4. Test Evaluation Table

The system was tested with **6 queries** (3 directly answerable, 1 paraphrase, and 2 out-of-scope questions not present in `knowledge_base.json`) using `k=2` retrieval with `embeddinggemma` and generation via `qwen3:4b`.

| # | Question Type | Test Question | Expected Entry ID | Retrieved IDs (Scores) | Answer Correct? | Failure Step (if wrong) |
|---|---|---|---|---|---|---|
| **1** | **Answerable** | "I'm currently in district 1, Ho Chi Minh city. Can you recommend me a place for sightseeing the Sai Gon river?" | `G06` | `G06` (0.5165), `G05` (0.5029) | **Yes** | - |
| **2** | **Answerable** | I want to see the whole Ho Chi Minh city from high above. Any suggestion? | `G02` | `G02` (0.4555), `G09` (0.4487) | **Yes** | - |
| **3** | **Answerable** | It's been a long flight for me to get to Ho Chi Minh City. Can you recommend me a place to rest? I'm currently at Ben Nghe Ward and I would prefer somewhere peaceful like a café so I can read my novel while having a cup of tea. | `G10` | `G10` (0.6064), `G05` (0.5067) | **Yes** | - |
| **4** | **Paraphrase** | The tunnels were used by Viet Cong soldiers as hiding spots during combat, as well as serving as communication and supply routes, hospitals, food and weapon caches and living quarters for numerous North Vietnamese fighters. | `G11` | `G11` (0.6561), `G05` (0.3013) | **Yes** | - |
| **5** | **Not in Guide** | I just got to Da Nang city. Can you recommend me a hotel to stay for 3 nights? | None | `G05` (0.3545), `G02` (0.3511) | **Yes** | Generation Step: The question lies outside the program's knowledge base |
| **6** | **Not in Guide** | I just arrived at Ho Chi Minh City and I want to explore this city. Can you recommend me one tourist-attraction? It would be cool if you recommend me a museum since I love history, especially about the Vietnam war. | None | `G05` (0.5485), `G010` (0.5082) | **No** | Retrieval Step: k=2 is too small or the vector similarity for G04 is lower than that of other potential matches for this open-ended query |

---

## 5. Known Limitations & AI Tools Used

### Known Limitations
1. **No Similarity Score Thresholding:** `retrieve_top_k()` always returns the top-$k$ documents regardless of how low their cosine similarity scores are. For completely unrelated questions (e.g., Test #5), the system still sends low-scoring chunks to `qwen3:4b`, relying solely on the system prompt to enforce the `"I don't know"` fallback.
2. **Whole-Document Chunking:** Each entry in `knowledge_base.json` is embedded as a single text block. Very long descriptions (such as `G01` or `G07`) may slightly dilute semantic similarity when users ask hyper-specific questions.
3. **Ephemeral Pinggy Tunnel URL:** Free Pinggy tunnels expire after a limited session duration and generate a new URL upon restart, requiring a manual app refresh if the tunnel disconnects mid-session.
4. **No Metadata Filtering Yet:** Although `category` and `tags` are stored in `knowledge_base.json`, the current retriever only performs dense vector similarity search.
5. **Slow AI model processing speed:** qwen3:4b is a slow model and it takes more than 5 minutes to just answer a question. This happens because the model always undergoes a thorough analysis of the question and validating the answer before providing it.

### Note on AI Tools Used

- **Gemini:**

+ Used for debugging the Ollama `403 Forbidden` CORS/Host header issue over Pinggy (`OLLAMA_HOST=0.0.0.0:11434`), refactoring `@st.cache_resource` in `rag.py`, and structuring documentation in `README.md`.

+ All travel guide entries in `knowledge_base.json` were researched, compiled and verified manually and then got double-checked by AI.