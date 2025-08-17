import os
from typing import Dict, Any, ClassVar
from pydantic import BaseModel, Field

class OpenRouterConfig(BaseModel):
    """Configuration for OpenRouter integration."""
    
    api_key: str = Field(
        default_factory=lambda: os.getenv("OPENROUTER_API_KEY"),
        description="OpenRouter API key"
    )
    
    base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenRouter API base URL"
    )
    
    # Free models available through OpenRouter
    FREE_MODELS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "gpt-oss-20b": {
            "provider": "openai",
            "model": "gpt-oss-20b",
            "context_length": 8192,
            "free": True
        },
        "llama-3.1-8b-instruct": {
            "provider": "meta",
            "model": "llama-3.1-8b-instruct",
            "context_length": 8192,
            "free": True
        },
        "gemma-2-9b-it": {
            "provider": "google",
            "model": "gemma-2-9b-it",
            "context_length": 8192,
            "free": True
        }
    }
    
    @classmethod
    def get_free_model_config(cls, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific free model."""
        if model_name not in cls.FREE_MODELS:
            raise ValueError(f"Model {model_name} not found in free models")
        return cls.FREE_MODELS[model_name]
    
    def validate_api_key(self) -> str:
        """Validate that OpenRouter API key is set and return the key."""
        print(f"Debug: OpenRouter API key check - key exists: {bool(self.api_key)}, key length: {len(self.api_key) if self.api_key else 0}")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        if not self.api_key.strip():
            raise ValueError("OPENROUTER_API_KEY environment variable cannot be empty")
        # Return the first few characters for debugging (safely)
        safe_key = self.api_key.strip()
        print(f"Debug: Using OpenRouter API key starting with: {safe_key[:8]}...")
        return safe_key
