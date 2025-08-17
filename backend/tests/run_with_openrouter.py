#!/usr/bin/env python3
"""
Startup script for running the LangGraph agent with OpenRouter models.
This script shows how to configure and start your agent with free models.
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if the environment is properly configured."""
    load_dotenv()
    
    required_vars = ["OPENROUTER_API_KEY", "GEMINI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file:")
        print("cp env.template .env")
        print("Then edit .env with your API keys")
        return False
    
    print("✅ Environment is properly configured")
    return True

def show_configuration():
    """Show the current configuration."""
    print("\n🔧 Current Configuration:")
    print("-" * 30)
    
    from agent.configuration import Configuration
    config = Configuration()
    
    print(f"Query Generator: {config.query_generator_model}")
    print(f"Reflection Model: {config.reflection_model}")
    print(f"Answer Model: {config.answer_model}")
    print(f"Use OpenRouter: {config.use_openrouter}")
    print(f"Initial Queries: {config.number_of_initial_queries}")
    print(f"Max Research Loops: {config.max_research_loops}")

def start_agent():
    """Start the LangGraph agent."""
    print("\n🚀 Starting LangGraph Agent with OpenRouter...")
    print("-" * 50)
    
    try:
        # Import the graph
        from agent.graph import graph
        
        print("✅ Agent graph loaded successfully")
        print(f"Graph name: {graph.name}")
        print(f"Graph nodes: {list(graph.nodes.keys())}")
        
        print("\n🎯 Your agent is ready to use!")
        print("You can now:")
        print("1. Use the FastAPI server: langgraph dev")
        print("2. Call the graph directly from Python")
        print("3. Use the CLI interface")
        
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
        print("Please check your configuration and try again")

def main():
    """Main startup function."""
    print("🚀 LangGraph Agent with OpenRouter")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Show configuration
    show_configuration()
    
    # Start agent
    start_agent()
    
    print("\n📚 Next Steps:")
    print("1. Test your agent with: python3 test_openrouter.py")
    print("2. Run examples with: python3 config_examples.py")
    print("3. Start the server with: langgraph dev")
    print("4. Check the documentation: README_OPENROUTER.md")

if __name__ == "__main__":
    main()

