import json
import logging
from .llm_client import call_groq
import agent_logger

logger = logging.getLogger(__name__)

class EvaluatorAgent:
    def evaluate(self, answer, mcq_question, correct_option, confidence):
        msg = f"\n" + "="*60 + "\n [AGENT 4/5] EVALUATOR AGENT: Assessing Performance\n" + "="*60 + f"\n > Student Input: '{answer}' (Confidence: {confidence}%)\n > Expectation: '{correct_option}'"
        logger.info(msg)
        agent_logger.log_agent("Evaluator", msg)
        
        # First: ensure exact string match or option letter match overrides LLM hallucination
        is_exact_match = answer.strip().lower() == correct_option.strip().lower()
        if not is_exact_match and answer.strip().lower() in correct_option.strip().lower():
            is_exact_match = True
            
        prompt = (
            f"Question: {mcq_question}. Correct: {correct_option}. Student: {answer}. Confidence: {confidence}%. Exact Match: {is_exact_match}.\n"
            "Evaluate the answer. If wrong and confidence was HIGH, explain the likely misconception.\n"
            "If right and confidence was LOW, provide an encouragement note.\n"
            "Respond JSON: {'correct': true|false, 'feedback': 'narrative feedback'}"
        )
        res = call_groq(prompt, json_mode=True)
        try:
            data = json.loads(res)
            # Override LLM's correct value with the exact match, but keep the feedback
            is_correct = is_exact_match if is_exact_match else data.get("correct", False)
            msg = f" > Verdict: {'CORRECT' if is_correct else 'INCORRECT'} (LLM said: {data.get('correct')}, Exact: {is_exact_match})\n > Feedback: {data.get('feedback', '')}"
            logger.info(msg)
            agent_logger.log_agent("Evaluator", msg)
            return is_correct, data.get('feedback', '')
        except json.JSONDecodeError:
            return answer.strip().lower() == correct_option.strip().lower(), "Manual verification complete."
