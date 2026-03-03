import json
from .llm_client import call_groq

class TeachingAgent:
    def teach(self, topic, strategy):
        print("\n" + "="*60)
        print(" [AGENT 3/5] TEACHING AGENT: Generating Structured Deep-Dive")
        print("="*60)
        print(f" > Mode: Executing '{strategy}' Strategy")
        
        prompt = (
            f"Role: High-Level Educational Engineer. Topic: '{topic}'. Strategy: '{strategy}'.\n"
            "Requirements for Lesson Content:\n"
            "- Use Structured Markdown (H# headers, bolding, bullet points).\n"
            "- Provide a 'Core Concept' section.\n"
            "- Provide a 'Deep Technical Mechanics' section.\n"
            "- Provide a 'Real-World Application' section.\n"
            "- Must be detailed (400-600 words).\n"
            "- ONE challenging MCQ at the end.\n"
            "Format JSON: {'lesson': 'markdown...', 'mcq_question': '...', 'options': ['...'], 'correct_option': '...'}"
        )
        res = call_groq(prompt, json_mode=True)
        try:
            data = json.loads(res)
            print(f" > Content Delivery: Success. Structured deep-dive generated.")
            return data
        except json.JSONDecodeError:
            print(" !! Warning: Content generation errored. Sending baseline lesson.")
            return {
                "lesson": f"# Understanding {topic}\nLet's deep dive into the core concepts...",
                "mcq_question": f"Which of these is a key mechanic of {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_option": "Option A"
            }
