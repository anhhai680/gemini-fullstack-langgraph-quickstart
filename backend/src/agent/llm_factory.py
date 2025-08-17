import logging
import os
from typing import Optional, Union
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.configuration import Configuration
from agent.openrouter_config import OpenRouterConfig
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class LLMFactory:
    """Factory for creating different LLM instances."""
    
    def __init__(self, config: Configuration):
        # Ensure environment variables are loaded
        load_dotenv()
        
        # Debug: Check what environment variables are available
        logger.debug(f"Debug: Environment check in LLMFactory:")
        logger.debug(f"  - OPENROUTER_API_KEY exists: {'OPENROUTER_API_KEY' in os.environ}")
        logger.debug(f"  - GEMINI_API_KEY exists: {'GEMINI_API_KEY' in os.environ}")
        logger.debug(f"  - Current working directory: {os.getcwd()}")
        logger.debug(f"  - Configuration use_openrouter: {config.use_openrouter}")
        logger.debug(f"  - Configuration query_generator_model: {config.query_generator_model}")
        
        self.config = config
        self.openrouter_config = OpenRouterConfig()
    
    def create_llm(
        self, 
        model_type: str, 
        temperature: float = 0.7,
        max_retries: int = 2
    ) -> BaseChatModel:
        """
        Create an LLM instance based on the model type.
        
        Args:
            model_type: Type of model to create (query_generator, reflection, answer)
            temperature: Temperature for generation
            max_retries: Number of retries
            
        Returns:
            Configured LLM instance
        """
        if model_type == "query_generator":
            model_name = self.config.query_generator_model
        elif model_type == "reflection":
            model_name = self.config.reflection_model
        elif model_type == "answer":
            model_name = self.config.answer_model
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Debug: Show which model is being used
        logger.debug(f"DEBUG: Creating {model_type} LLM with model: {model_name}")
        logger.debug(f"DEBUG: Configuration reasoning_model: {getattr(self.config, 'reasoning_model', 'Not set')}")
        
        try:
            logger.debug(f"DEBUG: model_name: {model_name} with type {model_type}")
            logger.debug(f"DEBUG: self.config.use_openrouter: {self.config.use_openrouter}")
            logger.debug(f"DEBUG: self._is_openrouter_model({model_name}): {self._is_openrouter_model(model_name)}")

            # Check if it's an OpenRouter model and if OpenRouter is enabled
            if self._is_openrouter_model(model_name) and self.config.use_openrouter:
                # Check if OpenRouter API key is available before trying to use it
                if not os.getenv('OPENROUTER_API_KEY'):
                    logger.debug(f"Warning: OPENROUTER_API_KEY not set, falling back to Gemini for {model_name}")
                    return self._create_gemini_llm("gemini-2.0-flash", temperature, max_retries)
                
                # Check if we should skip OpenRouter due to previous credit issues
                if hasattr(self, '_skip_openrouter_due_to_credits'):
                    logger.debug(f"Warning: Skipping OpenRouter for {model_name} due to previous credit issues, using Gemini")
                    return self._create_gemini_llm("gemini-2.0-flash", temperature, max_retries)
                
                logger.debug(f"Creating OpenRouter LLM with model: {model_name}")
                return self._create_openrouter_llm(model_name, temperature, max_retries)
            else:
                # Fall back to Google Gemini
                logger.debug(f"Creating Gemini LLM with model: {model_name}")
                return self._create_gemini_llm(model_name, temperature, max_retries)
        except Exception as e:
            # Check if it's a credit limit error and provide specific guidance
            error_message = str(e).lower()
            if "insufficient credits" in error_message or "402" in error_message:
                logger.error(f"Warning: OpenRouter credit limit reached for {model_name}, falling back to Gemini")
                logger.error("💡 To use OpenRouter models, add credits at: https://openrouter.ai/settings/credits")
                # Set flag to skip OpenRouter for future requests to avoid repeated credit errors
                self._skip_openrouter_due_to_credits = True
                return self._create_gemini_llm("gemini-2.0-flash", temperature, max_retries)
            elif "authentication" in error_message or "401" in error_message:
                logger.error(f"Warning: OpenRouter authentication failed for {model_name}, falling back to Gemini")
                logger.error("💡 Check your OPENROUTER_API_KEY environment variable")
                return self._create_gemini_llm("gemini-2.0-flash", temperature, max_retries)
            else:
                # Fallback to Gemini for other errors
                logger.error(f"Warning: Failed to create {model_type} LLM with {model_name}, falling back to Gemini: {e}")
                logger.error(f"Error type: {type(e).__name__}")
                return self._create_gemini_llm("gemini-2.0-flash", temperature, max_retries)
    
    def _is_openrouter_model(self, model_name: str) -> bool:
        """Check if the model name corresponds to an OpenRouter model."""
        result = model_name in self.openrouter_config.FREE_MODELS
        logger.debug(f"DEBUG: result of {model_name} in {self.openrouter_config.FREE_MODELS} : {result}")
        return result
    
    def _create_openrouter_llm(
        self, 
        model_name: str, 
        temperature: float, 
        max_retries: int
    ) -> ChatOpenAI:
        """Create an OpenRouter LLM instance."""
        # Validate API key and get fresh value from environment
        api_key = self.openrouter_config.validate_api_key()
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required and cannot be empty")
        
        model_config = self.openrouter_config.get_free_model_config(model_name)
        
        logger.debug(f"Debug: Creating OpenRouter LLM with:")
        logger.debug(f"  - Model: {model_config['model']}")
        logger.debug(f"  - Base URL: {self.openrouter_config.base_url}")
        logger.debug(f"  - Temperature: {temperature}")
        
        # Create the LLM with minimal configuration to avoid compatibility issues
        # OpenRouter models work best with basic configuration
        return ChatOpenAI(
            model=model_config["model"],
            openai_api_key=api_key,
            openai_api_base=self.openrouter_config.base_url,
            temperature=temperature,
            max_retries=max_retries,
            # Disable streaming to avoid compatibility issues
            streaming=False,
            # Use minimal configuration to avoid version conflicts
            request_timeout=60
        )
    
    def _create_gemini_llm(
        self, 
        model_name: str, 
        temperature: float, 
        max_retries: int
    ) -> ChatGoogleGenerativeAI:
        """Create a Google Gemini LLM instance."""
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            max_retries=max_retries,
            api_key=self.config.gemini_api_key
        )
    
    def reset_openrouter_credits_flag(self):
        """Reset the flag that skips OpenRouter due to credit issues."""
        if hasattr(self, '_skip_openrouter_due_to_credits'):
            delattr(self, '_skip_openrouter_due_to_credits')
            logger.debug("✅ OpenRouter credits flag reset - will try OpenRouter models again")
        else:
            logger.debug("ℹ️ No OpenRouter credits flag to reset")

