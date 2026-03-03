import json
from .llm_client import call_groq

class EvaluatorAgent:
    def evaluate(self, answer, mcq_question, correct_option, confidence):
        print("\n" + "="*60)
        print(" [AGENT 4/5] EVALUATOR AGENT: Assessing Performance")
        print("="*60)
        print(f" > Student Input: '{answer}' (Confidence: {confidence}%)")
        print(f" > Expectation: '{correct_option}'")
        
        prompt = (
            f"Question: {mcq_question}. Correct: {correct_option}. Student: {answer}. Confidence: {confidence}%.\n"
            "Evaluate the answer. If wrong and confidence was HIGH, explain the likely misconception.\n"
            "If right and confidence was LOW, provide an encouragement note.\n"
            "Respond JSON: {'correct': true|false, 'feedback': 'narrative feedback'}"
        )
        res = call_groq(prompt, json_mode=True)
        try:
            data = json.loads(res)
            is_correct = data.get("correct", False)
            print(f" > Verdict: {'CORRECT' if is_correct else 'INCORRECT'}")
            print(f" > Feedback: {data.get('feedback', '')}")
            return is_correct, data.get('feedback', '')
        except json.JSONDecodeError:
            return answer.strip().lower() == correct_option.strip().lower(), "Manual verification complete."
