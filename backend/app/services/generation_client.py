from typing import Protocol

import httpx
from google import genai
from google.genai import errors, types

from app.config import Settings
from app.errors import AIProviderError, ConfigurationError


class GenerationClient(Protocol):
    def generate(self, prompt: str, *, temperature: float, json_mode: bool = False) -> str: ...


class GeminiGenerationClient:
    def __init__(self, *, api_key: str | None, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self._client: genai.Client | None = None

    @property
    def client(self) -> genai.Client:
        if not self.api_key:
            raise ConfigurationError("GEMINI_API_KEY is required when LLM_PROVIDER=gemini")
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str, *, temperature: float, json_mode: bool = False) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    response_mime_type="application/json" if json_mode else None,
                ),
            )
        except errors.APIError as exc:
            raise AIProviderError(
                "Gemini could not complete the request. Check GEMINI_API_KEY and GEMINI_MODEL."
            ) from exc
        if not response.text:
            raise AIProviderError("Gemini returned an empty response")
        return response.text.strip()


class OpenRouterGenerationClient:
    def __init__(
        self,
        *,
        api_key: str | None,
        model_name: str,
        base_url: str,
        site_url: str | None,
        app_name: str,
    ):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.site_url = site_url
        self.app_name = app_name

    def generate(self, prompt: str, *, temperature: float, json_mode: bool = False) -> str:
        if not self.api_key:
            raise ConfigurationError("OPENROUTER_API_KEY is required when LLM_PROVIDER=openrouter")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Title": self.app_name,
        }
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url

        payload: dict = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            body = response.json()
            content = body["choices"][0]["message"]["content"]
        except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
            raise AIProviderError(
                "OpenRouter could not complete the request. Check OPENROUTER_API_KEY and "
                "OPENROUTER_MODEL."
            ) from exc

        if not isinstance(content, str) or not content.strip():
            raise AIProviderError("OpenRouter returned an empty response")
        return content.strip()


def create_generation_client(settings: Settings) -> GenerationClient:
    if settings.llm_provider == "openrouter":
        return OpenRouterGenerationClient(
            api_key=settings.openrouter_api_key,
            model_name=settings.openrouter_model,
            base_url=settings.openrouter_base_url,
            site_url=settings.openrouter_site_url,
            app_name=settings.openrouter_app_name,
        )
    return GeminiGenerationClient(
        api_key=settings.gemini_api_key,
        model_name=settings.gemini_model,
    )
