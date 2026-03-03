import json
from .llm_client import call_groq

class PlannerAgent:
    def plan(self, level, topic, past_performance, confidence):
        print("\n" + "="*60)
        print(" [AGENT 2/5] PLANNER AGENT: Formulating Teaching Strategy")
        print("="*60)
        print(f" > Input Level: {level}")
        print(f" > Student Confidence: {confidence}%")
        
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
            print(f" > AI Logic: {data.get('agent_note', 'Determined based on matrix.')}")
            print(f" > Selected Strategy: {strategy.upper()}")
            return strategy
        except json.JSONDecodeError:
            print(" !! Warning: Strategy engine failed. Using Standard.")
            return "Standard Adaptive"
