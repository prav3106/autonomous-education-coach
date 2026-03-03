import json
from .llm_client import call_groq

class AnalyzerAgent:
    def analyze(self, student_history):
        print("\n" + "="*60)
        print(" [AGENT 1/5] ANALYZER AGENT: Diagnosing Learner State V2")
        print("="*60)
        
        if not student_history:
            print(" > Status: First-time learner detected.")
            print(" > Decision: Assigning 'Beginner' level. Predicted Confidence: 50.0")
            return "Beginner", 50.0
            
        print(f" > Data Source: Retrieved {len(student_history)} past sessions.")
        
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
            print(f" > AI Trend Analysis: {data.get('analysis', 'Evaluated trends.')}")
            print(f" > Resulting Level: {level.upper()}")
            print(f" > Predicted Confidence: {pred_conf}%")
            return level, float(pred_conf)
        except (json.JSONDecodeError, ValueError):
            print(" !! Warning: Analytics engine failed. Using fallbacks.")
            return "Beginner", 50.0
