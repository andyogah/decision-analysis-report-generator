"""LLM client supporting OpenAI and Azure OpenAI via environment configuration."""

import os
import openai

class LLMClient:
    """Lightweight wrapper for Chat Completions on OpenAI/Azure OpenAI."""

    def __init__(self, api_key=None, model="gpt-4o"):
        """Configure provider, credentials, and endpoints from environment."""
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()  # "openai" or "azure"
        self.model = model
        if self.provider == "azure":
            self.openai = openai
            self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
            self.api_base = os.getenv("AZURE_OPENAI_API_BASE")
            self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
            self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", model)
            self.openai.api_type = "azure"
            self.openai.api_key = self.api_key
            self.openai.api_base = self.api_base
            self.openai.api_version = self.api_version
        else:
            self.openai = openai
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.openai.api_key = self.api_key

    def generate(self, prompt, max_tokens=2048):
        """Generate text for the given prompt using the configured provider/model."""
        if self.provider == "azure":
            response = self.openai.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.2,
            )
        else:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.2,
            )
        return response.choices[0].message.content.strip()
