<div align="center">



# 🤖 Customer Support Chatbot — Decision Engine

### An AI-powered system that handles refunds, exchanges & fraud detection with automated decision-making using LLMs, vision analysis, and knowledge base retrieval.

[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/Atharvasayyyy/Chat_bot-of-CS)
[![Python](https://img.shields.io/badge/Python-3.11.9-blue)](https://python.org)
[![React](https://img.shields.io/badge/React-19.2.5-61dafb)](https://react.dev)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

**[Live Demo](https://customer-support-ui.vercel.app)** · **[API Docs](https://customer-support-api.onrender.com/docs)** · **[Report Bug](https://github.com/Atharvasayyyy/Chat_bot-of-CS/issues)**

</div>

---

## ⚠️ The Problem

Today, many e-commerce support systems still depend heavily on **manual review processes**. As AI-generated content becomes more realistic, **fraudulent refund claims** are becoming harder to detect.

This creates:

| Pain Point                         | Impact                                  |
| ---------------------------------- | --------------------------------------- |
| 🔴 Manual ticket handling          | Slow resolution, inconsistent decisions |
| 🔴 AI-generated fake damage images | Refund fraud & operational losses       |
| 🔴 Scattered support channels      | No unified view for agents              |
| 🔴 Complex refund/exchange rules   | Error-prone manual workflows            |
| 🔴 Overloaded support teams        | Poor customer experience                |

---

## 💡 The Solution

An intelligent AI support agent that combines **LLM reasoning**, **vision-based fraud detection**, and **automated workflows** — so support teams spend time only where it matters.

```
Customer submits query
        ↓
Intent Detection (LLM)           → refund / exchange / general query
        ↓
Purchase & History Verification  → order details, complaint history, pricing
        ↓
Vision AI Pipeline (if image)    → AI-generated? Product match? Damage real?
        ↓
Risk Engine                      → 🟢 Low  🟡 Medium  🔴 High
        ↓
Automated Decision               → auto-refund / request evidence / escalate ticket
        ↓
Notification (SendGrid)          → customer + merchant informed
```

---

## 🚀 Features

### 💬 Customer-Facing

- Multi-turn chat interface with guided wizard flow
- Order lookup via user ID
- Product selection & action type (refund / exchange / return)
- Image upload for product verification
- Real-time request tracking

### 🛠️ Admin Dashboard

- Unified ticket management (pending / approved / rejected)
- Exchange requests with product swap handling
- Refund processing with automated email notifications
- Database viewer for orders, users, and transaction history
- Real-time support analytics

### 🧠 Backend Intelligence

- **ReAct Agent** architecture — reasoning + tools + database interaction
- **LLM-based decision engine** (OpenAI / Groq / Mistral)
- **Vision AI pipeline** — CLIP for product matching, YOLO / Roboflow for damage detection
- **AI-generated image detection** — proactively flags suspicious evidence
- **Dynamic risk scoring** — low / medium / high classification per request
- **Knowledge base retrieval** — vector search over policy docs, FAQs, PDFs
- **Automated email notifications** via SendGrid

---

## 🧠 AI Architecture

<img src="./assets/demo.gif" alt="Customer Support AI Demo" width="70" />

The system uses a **ReAct Agent** architecture with tools, reasoning, and direct database interaction.

```
┌─────────────────────────────────────────────────────────────┐
│                    CUSTOMER SUPPORT CHATBOT                 │
└─────────────────────────────────────────────────────────────┘
         │                                    │
         ▼                                    ▼
    ┌─────────────┐                    ┌──────────────┐
    │   Frontend  │                    │   Backend    │
    │   (Vercel)  │◄──────────────────►│   (Render)   │
    └─────────────┘                    └──────────────┘
         │                                    │
         │ React 19 + Vite                    │ FastAPI + LangChain
         │ TailwindCSS                        │ Python 3.11.9
         │ React Router 7                     │
         │                                    ├─ ReAct Agent
         ├─ Landing Page                      │  ├─ Intent Detection
         ├─ Chat Interface                    │  ├─ Risk Scoring
         ├─ Admin Dashboard                   │  └─ Decision Engine
         └─ Database Viewer                   │
                                              ├─ Vision Pipeline
                                              │  ├─ CLIP (product match)
                                              │  ├─ YOLO / Roboflow (damage)
                                              │  └─ AI-image detection
                                              │
                                              ├─ Knowledge Base
                                              │  ├─ Embeddings (NVIDIA)
                                              │  ├─ Vector DB (Pinecone)
                                              │  └─ Semantic Retrieval
                                              │
                                              ├─ Tools
                                              │  ├─ DB Queries
                                              │  ├─ Refund Processor
                                              │  ├─ Exchange Handler
                                              │  └─ Notification Sender
                                              │
                                              └─ PostgreSQL Database
                                                 ├─ Users / Orders
                                                 ├─ Tickets / Refunds
                                                 └─ Exchanges
```

---

## 🎨 Tech Stack

### Frontend

| Technology       | Version | Purpose                 |
| ---------------- | ------- | ----------------------- |
| React            | 19.2.5  | UI framework            |
| Vite             | 8.0.10  | Build tool & dev server |
| Tailwind CSS     | 4.x     | Styling & design system |
| React Router DOM | 7.14.2  | Client-side routing     |
| Axios            | 1.16.0  | HTTP client             |

### Backend

| Technology | Version | Purpose                   |
| ---------- | ------- | ------------------------- |
| Python     | 3.11.9  | Runtime                   |
| FastAPI    | 0.104.1 | Web framework             |
| LangChain  | 0.1.x   | ReAct agent orchestration |
| OpenAI SDK | 1.10.0+ | LLM integration           |
| Psycopg2   | 2.9.9   | PostgreSQL driver         |
| SendGrid   | 6.12.5  | Email notifications       |
| YOLO v8    | 8.0.206 | Damage detection          |
| CLIP       | —       | Product image matching    |

### Infrastructure & AI

| Service          | Provider             | Purpose                      |
| ---------------- | -------------------- | ---------------------------- |
| Frontend Hosting | Vercel               | SPA deployment               |
| Backend Hosting  | Render               | API deployment               |
| Database         | PostgreSQL (AWS RDS) | Data persistence             |
| Vector DB        | Pinecone             | Semantic search              |
| File Storage     | AWS S3               | Image uploads                |
| Email            | SendGrid             | Notifications                |
| LLM (queries)    | Groq                 | Fast customer query handling |
| LLM (reasoning)  | Mistral AI           | Refund/exchange workflows    |
| Embeddings       | NVIDIA               | Knowledge base search        |
| Vision           | Roboflow + CLIP      | Fraud & damage detection     |

> **Why these models?** This is a prototype/MVP focused on validating the architecture using free-tier and developer-friendly APIs. The system is model-agnostic by design — these can be swapped for OpenAI GPT-4.1, Claude Sonnet, Gemini 2.5, Llama 4, or custom fine-tuned vision models in production.

---

## 📊 Performance Metrics

| Metric                  | Target | Current |
| ----------------------- | ------ | ------- |
| Chat Response Time      | <2s    | ~1.5s   |
| Admin Dashboard Load    | <1s    | ~0.8s   |
| Image Analysis          | <3s    | ~2.2s   |
| Database Query          | <100ms | ~50ms   |
| Manual Review Reduction | —      | 60–80%  |

---

## 🎯 Key Innovation: AI-Generated Image Detection

> As generative AI becomes more accessible, **fake refund claims with AI-generated damage images** will become a major operational challenge for e-commerce.

The vision pipeline proactively checks uploaded evidence:

1. **Is the image AI-generated?** — flags synthetic content before processing
2. **Does it match the purchased product?** — CLIP-based similarity matching
3. **Is the damage real?** — YOLO / Roboflow damage detection

This allows the system to catch fraud before automated refunds are approved.

---

## 📂 Project Structure

```
Customer Support Main
├── 📄 README.md
├── 📄 DEPLOYMENT.md
├── 📄 render.yaml
├── 🖼️ assets/
│   ├── demo.gif              # Hero demo GIF
│   └── architecture.gif      # Architecture demo GIF
│
├── 🎨 Frontend/support-ui/
│   └── src/
│       ├── components/
│       │   ├── admin/        # Tickets, Refunds, Exchanges, Sidebar
│       │   └── chat/         # ChatWindow, InputBox, Message
│       ├── pages/            # AdminPage, ChatPage, DatabasePage, LandingPage
│       └── services/api.js   # API client
│
├── 🐍 Backend/
│   ├── main.py               # FastAPI entry point
│   ├── logic/
│   │   ├── agent.py          # ReAct agent definition
│   │   ├── decision.py       # Decision logic
│   │   ├── risk.py           # Risk scoring
│   │   ├── image_pipeline.py # Vision processing
│   │   ├── kb_retriever.py   # Vector search
│   │   └── chains/           # Refund, exchange, query chains
│   ├── services/
│   │   ├── llm_router.py     # LLM selection
│   │   ├── vision_service.py # YOLO inference
│   │   ├── vector_service.py # Pinecone operations
│   │   └── email_service.py  # SendGrid
│   ├── tools/                # DB tools, refund, exchange, ticket, notification
│   └── DB/                   # Schema, seeds, init scripts
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js 16+
- Python 3.11.9
- PostgreSQL 12+
- API Keys: SendGrid, OpenAI or Groq, NVIDIA Embeddings

### Backend Setup

```bash
cd Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt

cp .env.example .env
# Fill in: DB_HOST, DB_USER, DB_PASSWORD, SENDGRID_API_KEY, OPENAI_API_KEY / GROQ_API_KEY

python DB/init_db.py
python DB/seed_users.py
python DB/seed_orders.py

python -m uvicorn main:app --reload
# API: http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```

### Frontend Setup

```bash
cd Frontend/support-ui
npm install
cp .env.example .env
# Set: VITE_API_BASE_URL=http://127.0.0.1:8000
npm run dev
# UI: http://localhost:5173
```

### Access

| Route           | URL                            |
| --------------- | ------------------------------ |
| Landing Page    | http://localhost:5173          |
| Chat Interface  | http://localhost:5173/chat     |
| Admin Dashboard | http://localhost:5173/admin    |
| Database Viewer | http://localhost:5173/database |
| API Docs        | http://127.0.0.1:8000/docs     |

---

## 📡 API Reference

```http
POST /chat
# multipart/form-data: user_id, message, selected_order_id,
# selected_product, selected_action (refund/exchange/return), image (optional)

GET /dashboard      # All tickets, refunds, exchanges
GET /database       # Full DB snapshot (users, orders, tickets, exchanges, refunds)
GET /orders/{user_id}
```

---

## 🌐 Deployment

```bash
git push origin main
# Vercel auto-deploys frontend
# Render auto-deploys backend via Docker
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for full instructions.

**Live:**

- Frontend: https://customer-support-ui.vercel.app
- Backend: https://customer-support-api.onrender.com

---

## 🔒 Security

- All secrets in `.env` (never committed)
- CORS restricted to frontend domain
- Prompt injection safeguards on LLM inputs
- Decision confidence thresholds — high-risk refunds require manual review
- Audit logs for all transactions, no PII in logs
- Rate limiting built-in

---

## 🗺️ Roadmap

- [ ] Multi-agent orchestration
- [ ] Behavioral fraud analysis
- [ ] Real-time merchant analytics dashboard
- [ ] Voice support
- [ ] Multilingual AI support
- [ ] Fine-tuned damage detection models
- [ ] Autonomous support workflows

---

## 🧪 Testing

```bash
# Backend
cd Backend
python test_tools.py

# Frontend
cd Frontend/support-ui
npm run test
```

---

## 🤝 Contributing

```bash
git checkout -b feature/your-feature
git commit -m "feat: add your feature"
git push origin feature/your-feature
# Open a Pull Request
```

---

## 📝 License

MIT License — see [LICENSE](./LICENSE) for details.

---

<div align="center">

**Built by [Atharva](https://github.com/Atharvasayyyy)**

_Would love feedback from AI engineers, startup founders, customer support teams & e-commerce operators._

</div>
