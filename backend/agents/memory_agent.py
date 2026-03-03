from models import StudentHistory
from sqlalchemy.orm import Session

class MemoryAgent:
    def save_session(self, db: Session, student_id, topic, score, confidence, strategy):
        print("\n" + "="*60)
        print(" [AGENT 5/5] MEMORY AGENT: Persistence Layer")
        print("="*60)
        print(f" > Writing result for {student_id} to MySQL...")
        
        new_record = StudentHistory(
            student_id=student_id,
            topic=topic,
            score=score,
            confidence=confidence,
            strategy=strategy
        )
        db.add(new_record)
        db.commit()
        print(" > Database status: COMMIT SUCCESS. Record saved.")
    
    def get_history(self, db: Session, student_id):
        print("\n [Memory Agent] Retrieving historical records from MySQL...")
        records = db.query(StudentHistory).filter(StudentHistory.student_id == student_id).all()
        print(f" > Database status: Found {len(records)} entries for '{student_id}'.")
        return [{"topic": r.topic, "score": r.score, "strategy": r.strategy, "confidence": r.confidence} for r in records]
