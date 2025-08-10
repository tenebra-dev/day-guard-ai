import os
import logging

logger = logging.getLogger(__name__)


class GeminiProvider:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not set; GeminiProvider will not function properly.")
        # Placeholder for actual Google Generative AI client
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    async def generate(self, system_prompt: str, user_content: str) -> str:
        # TODO: Implement real Gemini client
        return f"[GEMINI MOCK] {system_prompt} -- {user_content[:100]}"
