import os
import base64
from typing import Optional
import logging


class LLMClient:
    """Simple LLM client interface for LinoLog agents."""

    def __init__(self, provider="openai", api_key=None):
        self.provider = provider
        self.logger = logging.getLogger(__name__)

        # Set API key based on provider
        if provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        elif provider == "anthropic":
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        else:
            self.logger.warning(f"Unknown LLM provider: {provider}")
            self.api_key = None

        # Initialize provider-specific client
        if provider == "openai":
            self._init_openai()
        elif provider == "anthropic":
            self._init_anthropic()
        else:
            self.client = None

    def _init_openai(self):
        """Initialize OpenAI client."""
        try:
            import openai

            self.client = openai.OpenAI(api_key=self.api_key)
            self.logger.info("OpenAI client initialized")
        except ImportError:
            self.logger.error("OpenAI package not installed. Run: pip install openai")
            self.client = None
        except Exception as e:
            self.logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None

    def _init_anthropic(self):
        """Initialize Anthropic client."""
        try:
            import anthropic

            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.logger.info("Anthropic client initialized")
        except ImportError:
            self.logger.error(
                "Anthropic package not installed. Run: pip install anthropic"
            )
            self.client = None
        except Exception as e:
            self.logger.error(f"Failed to initialize Anthropic client: {e}")
            self.client = None

    def analyze_image(self, prompt: str, image_base64: str) -> Optional[str]:
        """Analyze image using LLM vision capabilities."""
        if not self.client:
            return None

        try:
            if self.provider == "openai":
                return self._analyze_image_openai(prompt, image_base64)
            elif self.provider == "anthropic":
                return self._analyze_image_anthropic(prompt, image_base64)
        except Exception as e:
            self.logger.error(f"Image analysis failed: {e}")

        return None

    def analyze_text(self, prompt: str) -> Optional[str]:
        """Analyze text using LLM."""
        if not self.client:
            return None

        try:
            if self.provider == "openai":
                return self._analyze_text_openai(prompt)
            elif self.provider == "anthropic":
                return self._analyze_text_anthropic(prompt)
        except Exception as e:
            self.logger.error(f"Text analysis failed: {e}")

        return None

    def _analyze_image_openai(self, prompt: str, image_base64: str) -> Optional[str]:
        """Analyze image using OpenAI GPT-4 Vision."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Use vision-capable model
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=150,
                temperature=0.3,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            self.logger.error(f"OpenAI image analysis failed: {e}")
            return None

    def _analyze_text_openai(self, prompt: str) -> Optional[str]:
        """Analyze text using OpenAI GPT-4."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            self.logger.error(f"OpenAI text analysis failed: {e}")
            return None

    def _analyze_image_anthropic(self, prompt: str, image_base64: str) -> Optional[str]:
        """Analyze image using Anthropic Claude 3.5 Sonnet."""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64,
                                },
                            },
                        ],
                    }
                ],
            )

            return response.content[0].text.strip()

        except Exception as e:
            self.logger.error(f"Anthropic image analysis failed: {e}")
            return None

    def _analyze_text_anthropic(self, prompt: str) -> Optional[str]:
        """Analyze text using Anthropic Claude 3.5 Sonnet."""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text.strip()

        except Exception as e:
            self.logger.error(f"Anthropic text analysis failed: {e}")
            return None

    def is_available(self) -> bool:
        """Check if LLM client is available and configured."""
        return self.client is not None and self.api_key is not None
