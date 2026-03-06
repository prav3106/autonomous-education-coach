import logging
from .analyzer_agent import AnalyzerAgent
from .planner_agent import PlannerAgent
from .teaching_agent import TeachingAgent
from .evaluator_agent import EvaluatorAgent
from .memory_agent import MemoryAgent
import agent_logger

logger = logging.getLogger(__name__)

class HeadAgent:
    def __init__(self):
        self.analyzer = AnalyzerAgent()
        self.planner = PlannerAgent()
        self.teacher = TeachingAgent()
        self.evaluator = EvaluatorAgent()
        self.memory = MemoryAgent()

    def run_adaptive_loop(self, db_session, student_id, topic, initial_confidence=50.0):
        # 1. Retrieve history
        history = self.memory.get_history(db_session, student_id)
        
        # 2. Analyze level and PREDICT confidence
        level, predicted_confidence = self.analyzer.analyze(history)
        
        # Use max of user-reported vs AI-predicted for strategy mapping
        final_confidence = max(initial_confidence, predicted_confidence)
        
        # 3. Plan strategy using Composite Confidence + Level
        strategy = self.planner.plan(level, topic, str(history), final_confidence)
        
        # 4. Generate content
        lesson_data = self.teacher.teach(topic, strategy)
        
        msg = "\n" + "#"*60 + "\n TOTAL SYSTEM SYNC COMPLETE: ADAPTIVE LOOP READY\n" + "#"*60 + "\n"
        logger.info(msg)
        agent_logger.log_agent("System", msg)
        
        return {
            "level": level,
            "strategy": strategy,
            "lesson": lesson_data.get("lesson", ""),
            "mcqs": lesson_data.get("mcqs", [])
        }
        
    def evaluate_answer(self, user_answer, question, correct_option, confidence):
        # 5. Evaluate
        is_correct, feedback = self.evaluator.evaluate(user_answer, question, correct_option, confidence)
        
        score = 100.0 if is_correct else 0.0
        
        return {
            "correct": is_correct,
            "score": score,
            "explanation": feedback
        }
