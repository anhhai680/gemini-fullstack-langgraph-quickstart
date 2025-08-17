#!/usr/bin/env python3
"""
Test script for OpenRouter integration.
This script tests the LLM factory and OpenRouter configuration.
"""

import os
from dotenv import load_dotenv
from agent.configuration import Configuration
from agent.llm_factory import LLMFactory
from agent.openrouter_config import OpenRouterConfig

def test_openrouter_config():
    """Test OpenRouter configuration."""
    print("Testing OpenRouter Configuration...")
    
    config = OpenRouterConfig()
    print(f"API Key set: {'Yes' if config.api_key else 'No'}")
    print(f"Base URL: {config.base_url}")
    print(f"Available free models: {list(config.FREE_MODELS.keys())}")
    
    # Test model config retrieval
    try:
        model_config = config.get_free_model_config("gpt-oss-20b")
        print(f"gpt-oss-20b config: {model_config}")
    except ValueError as e:
        print(f"Error getting model config: {e}")
    
    # Test API key validation
    try:
        config.validate_api_key()
        print("✅ API key validation passed")
    except ValueError as e:
        print(f"❌ API key validation failed: {e}")
    
    print()

def test_configuration():
    """Test the main configuration class."""
    print("Testing Configuration Class...")
    
    config = Configuration()
    print(f"Query Generator Model: {config.query_generator_model}")
    print(f"Reflection Model: {config.reflection_model}")
    print(f"Answer Model: {config.answer_model}")
    print(f"Use OpenRouter: {config.use_openrouter}")
    print(f"Gemini API Key set: {'Yes' if config.gemini_api_key else 'No'}")
    
    print()

def test_llm_factory():
    """Test the LLM factory."""
    print("Testing LLM Factory...")
    
    config = Configuration()
    factory = LLMFactory(config)
    
    # Test model detection
    print(f"Is gpt-oss-20b an OpenRouter model? {factory._is_openrouter_model('gpt-oss-20b')}")
    print(f"Is gemini-2.0-flash an OpenRouter model? {factory._is_openrouter_model('gemini-2.0-flash')}")
    
    # Test LLM creation (without actually calling the API)
    try:
        llm = factory.create_llm("query_generator", temperature=0.7)
        print(f"✅ Successfully created LLM: {type(llm).__name__}")
        print(f"Model name: {llm.model_name if hasattr(llm, 'model_name') else 'N/A'}")
    except Exception as e:
        print(f"❌ Error creating LLM: {e}")
    
    print()

def test_environment_variables():
    """Test environment variable loading."""
    print("Testing Environment Variables...")
    
    load_dotenv()
    
    required_vars = [
        "OPENROUTER_API_KEY",
        "GEMINI_API_KEY"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'Set' if value else 'Not set'}")
        else:
            print(f"❌ {var}: Not set")
    
    print()

def main():
    """Run all tests."""
    print("🚀 OpenRouter Integration Test Suite")
    print("=" * 50)
    
    test_environment_variables()
    test_openrouter_config()
    test_configuration()
    test_llm_factory()
    
    print("✅ Test suite completed!")

if __name__ == "__main__":
    main()

