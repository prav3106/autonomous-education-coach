import json
import logging
from .llm_client import call_groq
import agent_logger

logger = logging.getLogger(__name__)

class PlannerAgent:
    def plan(self, level, topic, past_performance, confidence):
        msg = f"\n" + "="*60 + "\n [AGENT 2/5] PLANNER AGENT: Formulating Teaching Strategy\n" + "="*60 + f"\n > Input Level: {level}\n > Student Confidence: {confidence}%"
        logger.info(msg)
        agent_logger.log_agent("Planner", msg)
        
        prompt = (
            f"Student Level: {level}. Topic: {topic}. Past History: {past_performance}. Confidence Level: {confidence}%.\n"
            "Task: Select the most adaptive teaching strategy.\n"
            "Decision Logic:\n"
            "1. If confidence is LOW (<40%) but level is HIGH -> Select 'Confidence Booster'.\n"
            "2. If confidence is HIGH (>80%) but scores are LOW -> Select 'Deep Concept Rebuild'.\n"
            "3. If level is Beginner -> Select 'Step-by-Step Fundamentals'.\n"
            "4. If level is Advanced -> Select 'Socratic Challenge'.\n"
            "Anything else -> Select 'Standard Adaptive'.\n"
            "Return JSON: {'strategy': '...', 'agent_note': 'why this was chosen'}"
        )
        res = call_groq(prompt, json_mode=True)
        try:
            data = json.loads(res)
            strategy = data.get("strategy", "Standard Adaptive")
            msg = f" > AI Logic: {data.get('agent_note', 'Determined based on matrix.')}\n > Selected Strategy: {strategy.upper()}"
            logger.info(msg)
            agent_logger.log_agent("Planner", msg)
            return strategy
        except json.JSONDecodeError:
            msg = " !! Warning: Strategy engine failed. Using Standard."
            logger.info(msg)
            agent_logger.log_agent("Planner", msg)
            return "Standard Adaptive"
