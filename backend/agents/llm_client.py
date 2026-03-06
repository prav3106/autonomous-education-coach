import os
import json
import logging
import groq
from groq import Groq
from dotenv import load_dotenv
import agent_logger

logger = logging.getLogger(__name__)

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_groq(prompt: str, json_mode: bool = False) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} if json_mode else None
        )
        return response.choices[0].message.content
    except groq.PermissionDeniedError as e:
        msg = "\n" + "="*60 + "\n [ERROR] GROQ ACCESS DENIED (403)\n > Message: Your request was blocked by Groq. This usually happens due to:\n   1. VPN usage (Try disabling it or switching locations)\n   2. Unsupported geographical region\n   3. Network-level security settings\n" + "="*60 + "\n"
        logger.error(msg)
        agent_logger.log_agent("System", msg)
        return json.dumps({"error": "LLM_ACCESS_DENIED", "message": str(e)}) if json_mode else "Error: LLM Access Denied."
    except Exception as e:
        msg = f"\n [ERROR] LLM Call Failed: {type(e).__name__} - {str(e)}"
        logger.error(msg)
        agent_logger.log_agent("System", msg)
        return json.dumps({"error": "LLM_CALL_FAILED", "message": str(e)}) if json_mode else f"Error: {str(e)}"
