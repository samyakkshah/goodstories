# GoodStories

GoodStories is an AI-powered platform for automated story creation and publishing. It uses an agentic architecture with
LangGraph/LangChain to plan, draft, critique, and finalize stories, producing high-quality, multi-page narratives with minimal human intervention.

---

## Features

- **Agentic Story Pipeline**: Sketchboard → Draft → Critique → Finalize
- **Zero-shot and Few-shot Prompting** for genre/tone variation
- **FastAPI** backend for ai microservice and modular agents
- **Node.js** backend for database connections and Client respective interactions
- **Next.js** frontend with modern, minimal reading UI
- **PostgreSQL** for storing stories, pages, and metadata
- **Stable Diffusion Integration** for cover art generation
- **Admin Dashboard** for managing stories and pipeline runs

---

## Architecture

LangGraph / LangChain Agents <-> FastAPI Backend <-> PostgreSQL Storage <-> Node.js Backend <->Next.js Frontend

- **LangGraph / LangChain**: Orchestrates multi-agent pipeline steps
- **FastAPI**: Provides APIs for generation, retrieval, and admin controls
- **Node.js**: Provides APIs for database connections and Client respective interactions
- **PostgreSQL**: Stores stories, pages, generation prompts, and images
- **Next.js**: Offers a beautiful reader experience with two-page book-style view

---

##Setup environment variables
Create .env files for FastAPI and Next.js.

1. app

```env
# .env
NEXT_PUBLIC_BASE_URL=<backend_url>
```

2. api

```env
# .env
SUPABASE_URL=<project_url>
SUPABASE_SERVICE_KEY=<service_key_from_supabase>
SUPABASE_ANON_KEY=<anon_key_from_supabase>
PORT=8000 (which port you want to run backend on)

NODE_ENV=dev
```

3. AI Microservice

```env
SUPABASE_URL=<project_url>
SUPABASE_SERVICE_KEY=<service_key_from_supabase>
SUPABASE_ANON_KEY=<anon_key_from_supabase>
APP_PORT=5000 (which port you want to run microservice on)
```

---

## Install dependencies

1. APP:

```sh
cd app
npm install
```

2. API:

```sh
cd api
npm install
```

3. AI Microservice (FastAPI):

```sh
cd ai_generator
py -3.11 -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

---

## Run Services

1. APP

```sh
npm run dev
```

2. API

```sh
npm run dev
```

3. AI Microservice (FastAPI):

```sh
uvicorn main:app --reload
```

or

```sh
python main.py
```

---

## Pipeline

GoodStories uses an agentic, modular generation flow:

1. Sketchboard Agent

   - Creates a plan / outline for the story

2. Draft Agent

   - Writes the first draft from the sketch

3. Critique Agent

   - Provides feedback, edits, improvements

4. Final Agent
   - Produces polished text with selected style/tone

#### All stages are stored and can be inspected or re-run.

---

## Setup Cron Jobs

- Automated daily pipeline runs:
- Generates new stories on schedule
- ~5 stories in <15 minutes (depends on your specs)
- Configurable on cloud/pc

---

## Cover Image Generation

- Integrates with Stable Diffusion 1.5 for AI-generated cover art
- Supports negative prompts for quality control
- Workflow supports API-based generation for pipeline integration

---

## Tech Stack

1. LLM Orchestration: LangGraph/LangChain
2. Backend: FastAPI, Pydantic
3. Frontend: Next.js, TailwindCSS
4. Database: PostgreSQL via Supabase
5. Storage: Supabase
6. Image Generation: Stable Diffusion

---

Project is still in progress, come back for new updates

---

# License

MIT

---

## For questions or collaborations

Email: samyakshah@samyakshah.net
