#!/usr/bin/env python3
"""
Simple mock API server to test OpenRouter frontend integration.
This provides the /api/models endpoint without needing the full LangGraph server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from agent.openrouter_config import OpenRouterConfig

app = FastAPI(title="Mock API Server for OpenRouter Testing")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Mock API Server for OpenRouter Testing"}

@app.get("/api/models")
async def get_available_models():
    """Get available models including OpenRouter models."""
    # Get OpenRouter models
    openrouter_config = OpenRouterConfig()
    openrouter_models = []
    
    for model_name, model_info in openrouter_config.FREE_MODELS.items():
        openrouter_models.append({
            "id": model_name,
            "name": model_name,
            "provider": "OpenRouter",
            "provider_icon": "🔗",
            "category": "Free",
            "context_length": model_info["context_length"],
            "description": f"Free {model_info['provider']} model via OpenRouter"
        })
    
    # Get Gemini models
    gemini_models = [
        {
            "id": "gemini-2.0-flash",
            "name": "2.0 Flash",
            "provider": "Google",
            "provider_icon": "⚡",
            "category": "Paid",
            "context_length": 8192,
            "description": "Fast and efficient Gemini model"
        },
        {
            "id": "gemini-2.5-flash-preview-04-17",
            "name": "2.5 Flash",
            "provider": "Google",
            "provider_icon": "⚡",
            "category": "Paid",
            "context_length": 8192,
            "description": "Latest Gemini Flash model"
        },
        {
            "id": "gemini-2.5-pro-preview-05-06",
            "name": "2.5 Pro",
            "provider": "Google",
            "provider_icon": "⚙️",
            "category": "Paid",
            "context_length": 8192,
            "description": "High-quality Gemini Pro model"
        }
    ]
    
    return {
        "models": openrouter_models + gemini_models,
        "default_model": "gpt-oss-20b"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Mock API server is running"}

if __name__ == "__main__":
    print("🚀 Starting Mock API Server for OpenRouter Testing...")
    print("📍 Server will run on http://localhost:2024")
    print("🔗 API endpoint: http://localhost:2024/api/models")
    print("🌐 CORS enabled for frontend testing")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=2024,
        log_level="info"
    )
