import pytest

from app.config import Settings
from app.errors import ConfigurationError
from app.services.generation_client import create_generation_client


@pytest.mark.parametrize("provider", ["gemini", "openrouter"])
def test_generation_provider_requires_its_api_key_only_when_requested(provider):
    settings = Settings(
        llm_provider=provider,
        gemini_api_key=None,
        openrouter_api_key=None,
    )
    client = create_generation_client(settings)

    with pytest.raises(ConfigurationError):
        client.generate("test", temperature=0)
