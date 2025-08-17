#!/usr/bin/env python3
"""
Configuration examples for OpenRouter integration.
This file shows different ways to configure your LangGraph agent with OpenRouter models.
"""

from agent.configuration import Configuration

def example_all_openrouter():
    """Example: Use OpenRouter models for all tasks."""
    print("🔧 Example: All OpenRouter Models")
    print("-" * 40)
    
    config = Configuration(
        query_generator_model="gpt-oss-20b",
        reflection_model="gpt-oss-20b", 
        answer_model="gpt-oss-20b",
        use_openrouter=True
    )
    
    print(f"Query Generator: {config.query_generator_model}")
    print(f"Reflection: {config.reflection_model}")
    print(f"Answer: {config.answer_model}")
    print(f"Use OpenRouter: {config.use_openrouter}")
    print("✅ All models use OpenRouter (free)")
    print()

def example_mixed_models():
    """Example: Mix OpenRouter and Gemini models."""
    print("🔄 Example: Mixed OpenRouter + Gemini Models")
    print("-" * 40)
    
    config = Configuration(
        query_generator_model="gpt-oss-20b",      # OpenRouter (free)
        reflection_model="llama-3.1-8b-instruct", # OpenRouter (free)
        answer_model="gemini-2.5-pro",            # Gemini (paid)
        use_openrouter=True
    )
    
    print(f"Query Generator: {config.query_generator_model} (OpenRouter)")
    print(f"Reflection: {config.reflection_model} (OpenRouter)")
    print(f"Answer: {config.answer_model} (Gemini)")
    print(f"Use OpenRouter: {config.use_openrouter}")
    print("✅ Mix of free and paid models for cost optimization")
    print()

def example_performance_optimized():
    """Example: Performance-optimized configuration."""
    print("⚡ Example: Performance-Optimized Configuration")
    print("-" * 40)
    
    config = Configuration(
        query_generator_model="gemma-2-9b-it",    # Fast, efficient
        reflection_model="gpt-oss-20b",           # High quality reasoning
        answer_model="gpt-oss-20b",               # High quality output
        use_openrouter=True
    )
    
    print(f"Query Generator: {config.query_generator_model} (Fast)")
    print(f"Reflection: {config.reflection_model} (High Quality)")
    print(f"Answer: {config.answer_model} (High Quality)")
    print(f"Use OpenRouter: {config.use_openrouter}")
    print("✅ Optimized for speed and quality")
    print()

def example_cost_optimized():
    """Example: Cost-optimized configuration."""
    print("💰 Example: Cost-Optimized Configuration")
    print("-" * 40)
    
    config = Configuration(
        query_generator_model="llama-3.1-8b-instruct", # Free, good quality
        reflection_model="llama-3.1-8b-instruct",      # Free, good quality
        answer_model="llama-3.1-8b-instruct",          # Free, good quality
        use_openrouter=True
    )
    
    print(f"Query Generator: {config.query_generator_model} (Free)")
    print(f"Reflection: {config.reflection_model} (Free)")
    print(f"Answer: {config.answer_model} (Free)")
    print(f"Use OpenRouter: {config.use_openrouter}")
    print("✅ All models are free through OpenRouter")
    print()

def example_environment_variables():
    """Example: Using environment variables for configuration."""
    print("🌍 Example: Environment Variable Configuration")
    print("-" * 40)
    
    print("Set these environment variables:")
    print("export QUERY_GENERATOR_MODEL=gpt-oss-20b")
    print("export REFLECTION_MODEL=gpt-oss-20b")
    print("export ANSWER_MODEL=gpt-oss-20b")
    print("export USE_OPENROUTER=true")
    print("export OPENROUTER_API_KEY=your_key_here")
    print()
    print("Then create config:")
    print("config = Configuration()  # Will read from environment")
    print()

def main():
    """Show all configuration examples."""
    print("🚀 OpenRouter Configuration Examples")
    print("=" * 50)
    
    example_all_openrouter()
    example_mixed_models()
    example_performance_optimized()
    example_cost_optimized()
    example_environment_variables()
    
    print("💡 Tips:")
    print("- Use gpt-oss-20b for high-quality reasoning tasks")
    print("- Use llama-3.1-8b-instruct for general tasks")
    print("- Use gemma-2-9b-it for fast, simple tasks")
    print("- Mix models based on your needs and budget")

if __name__ == "__main__":
    main()

