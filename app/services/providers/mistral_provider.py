import os
import logging
from mistralai.async_client import MistralAsyncClient

logger = logging.getLogger(__name__)


class MistralProvider:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            logger.warning("MISTRAL_API_KEY not set; MistralProvider will not function properly.")
        self.client = MistralAsyncClient(api_key=api_key)
        self.model = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    async def generate(self, system_prompt: str, user_content: str) -> str:
        resp = await self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content or ""
