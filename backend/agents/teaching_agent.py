import json
import logging
from .llm_client import call_groq
import agent_logger

logger = logging.getLogger(__name__)

class TeachingAgent:
    def teach(self, topic, strategy):
        msg = f"\n" + "="*60 + "\n [AGENT 3/5] TEACHING AGENT: Generating Structured Deep-Dive\n" + "="*60 + str(f"\n > Mode: Executing '{strategy}' Strategy")
        logger.info(msg)
        agent_logger.log_agent("Teacher", msg)
        
        prompt = (
            f"Role: High-Level Educational Engineer. Topic: '{topic}'. Strategy: '{strategy}'.\n"
            "Requirements for Lesson Content:\n"
            "- Use Structured Markdown (H# headers, bolding, bullet points).\n"
            "- Provide a 'Core Concept' section.\n"
            "- Provide a 'Deep Technical Mechanics' section.\n"
            "- Provide a 'Real-World Application' section.\n"
            "- Must be detailed (400-600 words).\n"
            "- Generate a batch of EXACTLY 5 challenging MCQs at the end.\n"
            "Format JSON: {'lesson': 'markdown...', 'mcqs': [{'question': '...', 'options': ['...'], 'correct_option': '...'}]}"
        )
        res = call_groq(prompt, json_mode=True)
        try:
            data = json.loads(res)
            msg = f" > Content Delivery: Success. Structured deep-dive generated."
            logger.info(msg)
            agent_logger.log_agent("Teacher", msg)
            return data
        except json.JSONDecodeError:
            msg = " !! Warning: Content generation errored. Sending baseline lesson."
            logger.info(msg)
            agent_logger.log_agent("Teacher", msg)
            return {
                "lesson": f"# Understanding {topic}\nLet's deep dive into the core concepts...",
                "mcqs": [
                    {
                        "question": f"Which of these is a key mechanic of {topic}?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_option": "Option A"
                    }
                ]
            }
