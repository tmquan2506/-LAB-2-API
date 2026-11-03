# Text Summarization API

> **Computational Thinking – Practice 01: Application Programming Interface**

Link video demo: [https://1drv.ms/v/c/e0fb5fdd43e91f48/IQC9uWD4GM3TRZucLnyJt4sRAV9uORwxMrF4S-hy-uYzOYw?e=dDhNKA](https://1drv.ms/v/c/e0fb5fdd43e91f48/IQC9uWD4GM3TRZucLnyJt4sRAV9uORwxMrF4S-hy-uYzOYw?e=dDhNKA)

## Student Information

| Field | Detail |
|-------|--------|
| Name | Thông Minh Quân |
| MSSV | 25127475 |
| Course | Computational Thinking |
| Lab | Practice 01 – API |
| Instructor | Nguyen Ngoc Minh Chau / Le Duc Khoan |

---

## Selected Model

| Field | Detail |
|-------|--------|
| **Model Name** | `facebook/bart-large-cnn` |
| **Hugging Face Page** | https://huggingface.co/facebook/bart-large-cnn |
| **Task** | Text Summarization |
| **Architecture** | BART (Bidirectional and Auto-Regressive Transformers) |

---

## System Description

This Web API wraps the **BART-large-CNN** model – a state-of-the-art abstractive summarization model fine-tuned on the CNN/DailyMail news dataset. Send any long text and receive a concise, human-readable summary in JSON format.

**Endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API introduction & endpoint listing |
| `GET` | `/health` | Operational health check |
| `POST` | `/predict` | Summarize the provided text |

---

## Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd <repo-folder>

# 2. (Optional) Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Application

```bash
uvicorn main:app --reload
```

The server will be available at **http://127.0.0.1:8000**.

> **Note:** The BART model (~1.6 GB) will be downloaded automatically on first startup. Subsequent starts use the cached model.

Interactive API documentation is available at:
- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc      → http://127.0.0.1:8000/redoc

---

## Calling the API

### `GET /`

```bash
curl http://127.0.0.1:8000/
```

**Example response:**
```json
{
  "api": "Text Summarization API",
  "model": "facebook/bart-large-cnn",
  "model_url": "https://huggingface.co/facebook/bart-large-cnn",
  "description": "Submit a long piece of text and receive a concise summary ...",
  "endpoints": {
    "GET  /": "API introduction (this page)",
    "GET  /health": "Health check",
    "POST /predict": "Summarize text"
  }
}
```

---

### `GET /health`

```bash
curl http://127.0.0.1:8000/health
```

**Example response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "model": "facebook/bart-large-cnn"
}
```

---

### `POST /predict`

**Request body:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `text` | string | ✅ | — | Text to summarize (≥ 10 words) |
| `max_length` | integer | ❌ | 130 | Max tokens in summary |
| `min_length` | integer | ❌ | 30 | Min tokens in summary |

**Example request:**
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence has rapidly transformed numerous industries over the past decade. From healthcare to finance, AI-powered tools are streamlining processes, reducing costs, and enabling capabilities that were previously impossible. Machine learning models can now diagnose diseases from medical images with accuracy rivaling human specialists. In the financial sector, algorithmic trading systems process millions of transactions per second, while fraud detection models protect consumers in real time.",
    "max_length": 80,
    "min_length": 20
  }'
```

**Example response:**
```json
{
  "model": "facebook/bart-large-cnn",
  "summary": "Artificial intelligence has rapidly transformed numerous industries over the past decade. Machine learning models can now diagnose diseases from medical images with accuracy rivaling human specialists.",
  "input_word_count": 78,
  "summary_word_count": 31,
  "processing_time_seconds": 4.215
}
```

**Error example (text too short):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "msg": "Value error, 'text' is too short to summarize (need at least 10 words)."
    }
  ]
}
```

---

## Running Tests

```bash
# Make sure the server is running first
uvicorn main:app --reload

# In a separate terminal
python test_api.py
```

---

## Demonstration Video

> 🎬 **[Watch the demo video here](<your-video-link>)**

<!-- Replace the link above with your actual YouTube / Google Drive URL -->

