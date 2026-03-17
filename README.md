# SalesArena AI

## 🚀 Live Deployment

| | URL |
|---|---|
| **Frontend** | https://salesarena-frontend-4053352533.us-central1.run.app |
| **Backend API** | https://salesarena-backend-prod-4053352533.us-central1.run.app |
| **API Docs** | https://salesarena-backend-prod-4053352533.us-central1.run.app/docs |

---

A real-time AI sales coaching platform that role-plays as a tough buyer, interrupts like a real prospect, analyzes your responses, and trains you to handle objections confidently.

## What It Does

SalesArena AI puts you in a live sales conversation against AI-powered buyer personas — a skeptical CTO, a budget-focused CFO, or an aggressive procurement officer. The AI interrupts, pushes back, and challenges you just like a real buyer would. At the end of each session you get a detailed scorecard with coaching feedback.

**Features:**
- Live bidirectional audio conversation powered by Gemini 2.0 Flash Live
- Camera-on video capture so the AI can read your body language
- Real-time objection detection with instant feedback overlays
- 3 distinct buyer personas with unique objection styles
- End-of-session scorecard across 5 sales metrics
- AI-generated coaching feedback after every session

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| Animation | Framer Motion |
| Backend | FastAPI, Python 3.11, Uvicorn |
| AI | Google Gemini 2.0 Flash Live (google-genai) |
| Transport | WebSocket (binary PCM audio + JPEG video frames) |
| Infra | Google Cloud Run, Terraform, Docker |
| Secrets | Google Secret Manager |

---

## Project Structure

```
SalesArenaAI/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app + WebSocket endpoint
│   │   ├── agent.py         # Gemini Live API integration
│   │   ├── personas.py      # Buyer persona definitions
│   │   └── tools.py         # detect_objection + score_sales_skill tools
│   ├── tests/               # pytest test suite
│   ├── Dockerfile           # Cloud Run ready container
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx     # Main UI (persona selector + arena)
│   │   │   └── layout.tsx
│   │   └── hooks/
│   │       └── useLiveAudio.tsx  # WebSocket + audio/video streaming
│   └── package.json
└── infra/
    ├── terraform/           # Cloud Run, Secret Manager, IAM
    └── scripts/             # deploy.sh, production_deploy.sh/.ps1
```

---

## Buyer Personas

| Persona | ID | Style |
|---------|-----|-------|
| The Skeptic CTO | `skeptic` | Interrupts constantly, demands proof, hates buzzwords |
| The Budget Guardian (CFO) | `budget_guardian` | ROI-obsessed, always has a "free tool that's good enough" |
| The Procurement Officer | `procurement` | Impatient, 3-minute limit, fixates on pricing |

---

## Scoring Metrics

Each session is scored 1–10 on:

- **Confidence** — Self-assurance and vocal presence
- **Objection Handling** — How well you addressed pushback
- **Clarity** — How clearly you communicated your value prop
- **Value Framing** — ROI and benefit articulation
- **Closing** — Moving the conversation toward a deal

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Gemini API key → [Get one free at Google AI Studio](https://aistudio.google.com/apikey)

### Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt

# Set your Gemini API key
export GEMINI_API_KEY="your_api_key_here"   # macOS/Linux
$env:GEMINI_API_KEY="your_api_key_here"     # Windows PowerShell

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Backend runs at: `http://localhost:8001`
API docs at: `http://localhost:8001/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Environment Variables

**Backend** (required):
```
GEMINI_API_KEY=your_gemini_api_key
PORT=8001                          # optional, defaults to 8000
```

**Frontend** (optional, create `frontend/.env.local`):
```
NEXT_PUBLIC_WS_URL=ws://localhost:8001
```

---

## API Reference

| Endpoint | Type | Description |
|----------|------|-------------|
| `GET /` | HTTP | Health check |
| `WS /ws/arena/{persona_id}` | WebSocket | Live sales session |

**WebSocket message format:**
- Frontend → Backend: Binary PCM audio (16kHz) + JSON video frames (JPEG, 1fps)
- Backend → Frontend: Binary audio (Gemini voice response) + JSON events (`scorecard`, `tool_call`)

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## Deployment (Google Cloud Run)

### Quick Deploy

```bash
export GEMINI_API_KEY="your_production_key"
bash infra/scripts/deploy.sh
```

### Production Deploy (Terraform)

```bash
export GEMINI_API_KEY="your_production_key"
bash infra/scripts/production_deploy.sh
```

This will:
1. Build and push the Docker image to Google Container Registry
2. Provision Cloud Run, Secret Manager, and IAM via Terraform
3. Output the live `wss://` WebSocket URL

Set the output URL as `NEXT_PUBLIC_WS_URL` in your frontend deployment environment.

---

## License

Apache 2.0 — see [LICENSE](LICENSE)
