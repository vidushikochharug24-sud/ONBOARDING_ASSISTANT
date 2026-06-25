# 🤖 Codebase Onboarding Assistant

An AI-powered developer tool that automatically generates comprehensive onboarding guides for any codebase — eliminating the 2-3 week ramp-up time new engineers face when joining a team.

## 🚀 Live Demo
> https://onboarding-assistant-roan.vercel.app/

## 💡 The Problem
New engineers waste weeks understanding a codebase, constantly interrupting senior developers. Existing tools like GitHub's README or Confluence docs are either too shallow or manually maintained. No tool automatically reads your actual code and generates a structured guide for new joiners.

## ✨ Features

- **3 Input Methods** — Analyze via GitHub URL, ZIP upload, or internal PDF documentation
- **AI-Generated Onboarding Guides** — Structured guides covering architecture, key files, tech stack, and where to start
- **RAG-Powered Codebase Chat** — Ask anything about the codebase ("Where is auth handled?", "How does payment work?") and get answers grounded in actual code using vector semantic search
- **Multi-Tenant Workspaces** — Each company gets an isolated workspace; employees join via domain-based email auth (`@company.com`)
- **Cloud Storage** — All uploaded files stored securely in Supabase Storage
- **Persistent Guides** — Generated guides saved per repo, accessible to all workspace members

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | React + Vite |
| Backend | Flask + Python |
| AI / LLM | Groq (LLaMA 3.3 70B) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | Supabase pgvector |
| Database | Supabase PostgreSQL |
| Storage | Supabase Storage |
| Auth | JWT + domain-based workspace isolation |
| Deploy | Vercel (frontend) + Render (backend) |

## 🧠 How RAG Works

```
Codebase files (GitHub / ZIP)
        ↓
Split into chunks (per function / class)
        ↓
Convert to 384-dim vectors via sentence-transformers
        ↓
Store in Supabase pgvector database
        ↓
User asks: "How does authentication work?"
        ↓
Question → vector → cosine similarity search
        ↓
Top 3 most relevant code chunks retrieved
        ↓
Groq LLaMA answers grounded in actual code
```

## 📁 Project Structure

```
ONBOARDING_ASSISTANT/
├── backend/
│   ├── app.py              # Flask app + blueprint registration
│   ├── auth.py             # JWT auth + domain-based workspace logic
│   ├── analyze.py          # GitHub + ZIP analysis routes
│   ├── storage.py          # Supabase file upload routes
│   ├── rag.py              # RAG pipeline — chunking, embedding, vector search, chat
│   ├── chat.py             # /api/chat route
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Landing.jsx
    │   │   ├── Login.jsx
    │   │   ├── Signup.jsx
    │   │   └── Dashboard.jsx
    │   ├── components/
    │   │   ├── Sidebar.jsx
    │   │   ├── GuideTabs.jsx
    │   │   ├── GuideDisplay.jsx
    │   │   ├── NewAnalysisForm.jsx
    │   │   ├── CodebaseChat.jsx
    │   │   └── LoadingSpinner.jsx
    │   └── utils/
    │       ├── api.js
    │       └── auth.js
    └── package.json
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- [Groq API key](https://console.groq.com) (free)
- [Supabase](https://supabase.com) project (free)


## 🔐 Authentication Flow

1. Company signs up with email + company name
2. Workspace created automatically for their email domain
3. All `@company.com` employees join the same workspace
4. JWT tokens expire after 7 days
5. All guides and files are workspace-isolated




## 👩‍💻 Author

Built by [Vidushi Kochhar](https://github.com/vidushikochharug24-sud) — ECE @ NSUT Delhi
