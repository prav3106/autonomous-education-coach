from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, engine, Base
from models import StudentHistory
from agents import HeadAgent
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Autonomous Education Coach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

head_agent = HeadAgent()

class StartRequest(BaseModel):
    student_id: str
    topic: str
    confidence: Optional[float] = 50.0

class AnswerRequest(BaseModel):
    student_id: str
    topic: str
    strategy: str
    user_answer: str
    question: str
    correct_option: str
    confidence: float

@app.get("/motivation")
def get_motivation():
    import random
    quotes = [
        "The limit of your knowledge is the limit of your world. Keep expanding.",
        "Precision in thought leads to excellence in action.",
        "Learning is the only thing the mind never exhausts, never fears, and never regrets.",
        "Autonomous intelligence is the bridge to personalized mastery.",
        "Information is not knowledge. The only source of knowledge is experience and adaptive learning.",
        "Deep dives lead to deep understanding. Never settle for the surface."
    ]
    return {"quote": random.choice(quotes)}

@app.post("/start")
def start_lesson(req: StartRequest, db: Session = Depends(get_db)):
    try:
        data = head_agent.run_adaptive_loop(db, req.student_id, req.topic, req.confidence)
        return {"success": True, "data": data}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer")
def submit_answer(req: AnswerRequest, db: Session = Depends(get_db)):
    try:
        result = head_agent.evaluate_answer(
            db, req.student_id, req.topic, req.strategy,
            req.user_answer, req.question, req.correct_option,
            req.confidence
        )
        return {"success": True, "data": result}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/student/{student_id}")
def get_student(student_id: str, db: Session = Depends(get_db)):
    history = head_agent.memory.get_history(db, student_id)
    return {"success": True, "student_id": student_id, "history": history}

@app.get("/admin/dashboard")
def admin_dashboard(db: Session = Depends(get_db)):
    records = db.query(StudentHistory).all()
    if not records:
        return {"total_students": 0, "average_score": 0, "weakest_topics": [], "topic_wise_stats": {}, "all_records": []}
    
    unique_students = len(set(r.student_id for r in records))
    avg_score = sum(r.score for r in records) / len(records)
    
    topic_stats = {}
    for r in records:
        if r.topic not in topic_stats:
            topic_stats[r.topic] = {"scores": []}
        topic_stats[r.topic]["scores"].append(r.score)
    
    for t in topic_stats:
        topic_stats[t]["average"] = sum(topic_stats[t]["scores"]) / len(topic_stats[t]["scores"])
        topic_stats[t]["count"] = len(topic_stats[t]["scores"])
        del topic_stats[t]["scores"]
    
    sorted_topics = sorted(topic_stats.items(), key=lambda x: x[1]["average"])
    weakest_topics = [t[0] for t in sorted_topics[:3]]
    
    # Granular detail for admin
    all_records = [{
        "student_id": r.student_id,
        "topic": r.topic,
        "score": r.score,
        "confidence": r.confidence,
        "strategy": r.strategy,
        "date": r.created_at.strftime("%Y-%m-%d %H:%M")
    } for r in records]
    
    return {
        "success": True,
        "data": {
            "total_students": unique_students,
            "average_score": avg_score,
            "weakest_topics": weakest_topics,
            "topic_wise_stats": topic_stats,
            "all_records": all_records
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
