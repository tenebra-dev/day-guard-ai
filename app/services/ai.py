import logging
from typing import Optional

from .providers.openai_provider import OpenAIProvider
from .providers.mistral_provider import MistralProvider
from .providers.gemini_provider import GeminiProvider

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self, provider: str = "openai"):
        self.provider_name = provider
        self.client = self._get_client(provider)

    def _get_client(self, provider: str):
        if provider == "openai":
            return OpenAIProvider()
        if provider == "mistral":
            return MistralProvider()
        if provider == "gemini":
            return GeminiProvider()
        raise ValueError(f"Unsupported provider: {provider}")

    async def summarize(self, content: str, system_prompt: Optional[str] = None) -> str:
        prompt = system_prompt or "Faça um resumo breve e objetivo do dia do usuário."
        logger.info("Summarizing content with %s", self.provider_name)
        return await self.client.generate(prompt, content)

    async def suggest(self, context: str) -> str:
        prompt = "Dê 3 sugestões de próximas ações, considerando localização e horário."
        logger.info("Generating suggestions with %s", self.provider_name)
        return await self.client.generate(prompt, context)
