from .analyzer_agent import AnalyzerAgent
from .planner_agent import PlannerAgent
from .teaching_agent import TeachingAgent
from .evaluator_agent import EvaluatorAgent
from .memory_agent import MemoryAgent

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
        
        print("\n" + "#"*60)
        print(" TOTAL SYSTEM SYNC COMPLETE: ADAPTIVE LOOP READY")
        print("#"*60 + "\n")
        
        return {
            "level": level,
            "strategy": strategy,
            "lesson": lesson_data.get("lesson", ""),
            "question": lesson_data.get("mcq_question", ""),
            "options": lesson_data.get("options", []),
            "correct_option": lesson_data.get("correct_option", "")
        }
        
    def evaluate_answer(self, db_session, student_id, topic, strategy, user_answer, question, correct_option, confidence):
        # 5. Evaluate
        is_correct, feedback = self.evaluator.evaluate(user_answer, question, correct_option, confidence)
        
        score = 100.0 if is_correct else 0.0
        
        # 6. Save to Memory
        self.memory.save_session(db_session, student_id, topic, score, confidence, strategy)
        
        return {
            "correct": is_correct,
            "score": score,
            "explanation": feedback
        }
