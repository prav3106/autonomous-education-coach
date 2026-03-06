import logging
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)
from database import get_db
from models import StudentHistory
from agents import HeadAgent
import agent_logger
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uuid
import random

app = FastAPI(title="Autonomous Education Coach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

head_agent = HeadAgent()

ACTIVE_SESSIONS = {}

class StartRequest(BaseModel):
    student_id: str
    topic: str
    confidence: Optional[float] = 50.0

class AnswerRequest(BaseModel):
    session_id: str
    user_answer: str
    confidence: float

class EndRequest(BaseModel):
    session_id: str

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

@app.post("/start-session")
def start_lesson(req: StartRequest, db: Session = Depends(get_db)):
    try:
        data = head_agent.run_adaptive_loop(db, req.student_id, req.topic, req.confidence)
        
        session_id = str(uuid.uuid4())
        mcqs = data.get("mcqs", [])
        if not mcqs:
            # Fallback if no mcqs were returned
            mcqs = [{
                "question": "Which of these is a key mechanic of the topic?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_option": "Option A"
            }]
        random.shuffle(mcqs)
        
        ACTIVE_SESSIONS[session_id] = {
            "student_id": req.student_id,
            "topic": req.topic,
            "level": data.get("level"),
            "strategy": data.get("strategy"),
            "mcqs": mcqs,
            "current_index": 0,
            "correct_count": 0,
            "confidences": []
        }
        
        first_q = mcqs[0]
        
        return {
            "success": True, 
            "session_id": session_id,
            "data": {
                "lesson": data.get("lesson"),
                "level": data.get("level"),
                "strategy": data.get("strategy"),
                "question": first_q["question"],
                "options": first_q["options"],
                "correct_option": first_q["correct_option"]
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer-question")
def submit_answer(req: AnswerRequest):
    try:
        session = ACTIVE_SESSIONS.get(req.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or expired")
            
        current_idx = session["current_index"]
        current_q = session["mcqs"][current_idx]
        
        # Evaluate
        result = head_agent.evaluate_answer(
            req.user_answer, current_q["question"], current_q["correct_option"], req.confidence
        )
        
        if result["correct"]:
            session["correct_count"] += 1
        session["confidences"].append(req.confidence)
        session["current_index"] += 1
        
        has_next = session["current_index"] < len(session["mcqs"])
        next_q = session["mcqs"][session["current_index"]] if has_next else None
        
        return {
            "success": True, 
            "data": {
                "correct": result["correct"],
                "explanation": result["explanation"],
                "has_next": has_next,
                "next_question": next_q["question"] if has_next else None,
                "next_options": next_q["options"] if has_next else [],
                "next_correct_option": next_q["correct_option"] if has_next else None
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/end-session")
def end_session(req: EndRequest, db: Session = Depends(get_db)):
    try:
        session = ACTIVE_SESSIONS.get(req.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
            
        total_q = len(session["mcqs"])
        score = (session["correct_count"] / total_q) * 100 if total_q > 0 else 0
        avg_confidence = sum(session["confidences"]) / len(session["confidences"]) if session["confidences"] else 50.0
        
        # Save ONE record to the database for this session
        head_agent.memory.save_session(
            db, session["student_id"], session["topic"], score, avg_confidence, session["strategy"]
        )
        
        # Clear session
        del ACTIVE_SESSIONS[req.session_id]
        
        return {
            "success": True,
            "data": {
                "final_score": score,
                "correct_count": session["correct_count"],
                "total_questions": total_q
            }
        }
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
        return {"total_students": 0, "average_score": 0, "all_records": []}
    
    unique_students = len(set(r.student_id for r in records))
    avg_score = sum(r.score for r in records) / len(records)
    
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
            "all_records": all_records
        }
    }

@app.get("/agent-logs")
def agent_logs(since: float = Query(0.0)):
    return {
        "success": True,
        "data": agent_logger.get_logs(since)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
