import logging
from models import StudentHistory
from sqlalchemy.orm import Session
import agent_logger

logger = logging.getLogger(__name__)

class MemoryAgent:
    def save_session(self, db: Session, student_id, topic, score, confidence, strategy):
        msg = f"\n" + "="*60 + "\n [AGENT 5/5] MEMORY AGENT: Persistence Layer\n" + "="*60 + f"\n > Writing result for {student_id} to MySQL..."
        logger.info(msg)
        agent_logger.log_agent("Memory", msg)
        
        new_record = StudentHistory(
            student_id=student_id,
            topic=topic,
            score=score,
            confidence=confidence,
            strategy=strategy
        )
        db.add(new_record)
        db.commit()
        msg = " > Database status: COMMIT SUCCESS. Record saved."
        logger.info(msg)
        agent_logger.log_agent("Memory", msg)
    
    def get_history(self, db: Session, student_id):
        msg = "\n [Memory Agent] Retrieving historical records from MySQL..."
        logger.info(msg)
        agent_logger.log_agent("Memory", msg)
        records = db.query(StudentHistory).filter(StudentHistory.student_id == student_id).all()
        msg2 = f" > Database status: Found {len(records)} entries for '{student_id}'."
        logger.info(msg2)
        agent_logger.log_agent("Memory", msg2)
        return [{"topic": r.topic, "score": r.score, "strategy": r.strategy, "confidence": r.confidence} for r in records]
