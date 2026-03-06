import json
import logging
from .llm_client import call_groq
import agent_logger

logger = logging.getLogger(__name__)

class AnalyzerAgent:
    def analyze(self, student_history):
        msg = "\n" + "="*60 + "\n [AGENT 1/5] ANALYZER AGENT: Diagnosing Learner State V2\n" + "="*60
        logger.info(msg)
        agent_logger.log_agent("Analyzer", msg)
        
        if not student_history:
            msg = " > Status: First-time learner detected.\n > Decision: Assigning 'Beginner' level. Predicted Confidence: 50.0"
            logger.info(msg)
            agent_logger.log_agent("Analyzer", msg)
            return "Beginner", 50.0
            
        msg = f" > Data Source: Retrieved {len(student_history)} past sessions."
        logger.info(msg)
        agent_logger.log_agent("Analyzer", msg)
        
        # New: Deep Analysis including Confidence Prediction
        prompt = (
            f"Given the following student performance history: {student_history}.\n"
            "1. Determine Level: 'Beginner' (avg < 50), 'Intermediate' (50-85), 'Advanced' (> 85).\n"
            "2. Predict Confidence: Based on score consistency and growth, predict an AI-calculated confidence score (0-100).\n"
            "Return JSON: {'level': '...', 'predicted_confidence': 0.0, 'analysis': '...'}"
        )
        res = call_groq(prompt, json_mode=True)
        try:
            data = json.loads(res)
            level = data.get("level", "Beginner")
            pred_conf = data.get("predicted_confidence", 50.0)
            msg = f" > AI Trend Analysis: {data.get('analysis', 'Evaluated trends.')}\n > Resulting Level: {level.upper()}\n > Predicted Confidence: {pred_conf}%"
            logger.info(msg)
            agent_logger.log_agent("Analyzer", msg)
            return level, float(pred_conf)
        except (json.JSONDecodeError, ValueError):
            msg = " !! Warning: Analytics engine failed. Using fallbacks."
            logger.info(msg)
            agent_logger.log_agent("Analyzer", msg)
            return "Beginner", 50.0
