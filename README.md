# autonomous-education-coach

# Autonomous Education Coach

A modular multi-agent system powered by Groq API and Local MySQL.

## Features
- **Student Portal**: Adaptive learning powered by AI models.
- **Admin Dashboard**: Analytics on performance and topic weakness.
- **Multi-Agent Architecture**: Uses Analyzer, Planner, Teaching, Evaluator, and Memory agents recursively.

## Prerequisites

Before running the application:
1. **Groq API Key**: Go to [Groq Console](https://console.groq.com/keys).
2. **Local MySQL**: Install MySQL and create a database named `education_coach`.

## Backend Deployment (FastAPI)

### Running Locally
1. `cd backend`
2. Open the `.env` file and configure `GROQ_API_KEY` and `DATABASE_URL`.
   - `DATABASE_URL=mysql+pymysql://user:password@localhost:3306/education_coach`
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python main.py`

### Deployment to Render
1. Create a **Web Service** on Render connected to this repository.
2. Set Root Directory to `backend`.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: ``
5. In Render dashboard, add the Environment Variables:
   - `GROQ_API_KEY`
   - `MONGO_URI`

## Frontend Deployment (React/Vite)

### Running Locally
1. `cd frontend`uvicorn main:app --host 0.0.0.0 --port 10000
2. Create `.env` and set `VITE_BACKEND_URL=http://localhost:8000`
3. Install dependencies: `npm install`
4. Start dev server: `npm run dev`

### Deployment to Netlify
1. Connect this repository to Netlify.
2. Base directory: `frontend`
3. Build command: `npm run build`
4. Publish directory: `frontend/dist`
5. In Netlify Site Settings > Environment Variables, set:
   - `VITE_BACKEND_URL` (Set this to your Render backend URL, e.g., `https://your-backend.onrender.com`)
