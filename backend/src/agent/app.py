# mypy: disable - error - code = "no-untyped-def,misc"
import os
import pathlib
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from logging import Logger

logger: Logger = Logger.getLogger(__name__)

# Define the FastAPI app
app = FastAPI()

# Configure allowed origins for CORS
allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
if allowed_origins_env:
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
else:
    allowed_origins = ["*"]  # WARNING: In production, set ALLOWED_ORIGINS to restrict this to your frontend domain(s)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information and frontend access."""
    return {
        "message": "Gemini Fullstack LangGraph API",
        "frontend": "/app/ (use trailing slash)",
        "frontend_files": "/app/index.html, /app/assets/*",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }

@app.get("/api/models")
async def get_available_models():
    """Get available models including OpenRouter models."""
    from agent.openrouter_config import OpenRouterConfig
    from agent.configuration import Configuration
    
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
            "id": "gemini-2.5-flash",
            "name": "2.5 Flash",
            "provider": "Google",
            "provider_icon": "⚡",
            "category": "Paid",
            "context_length": 8192,
            "description": "Latest Gemini Flash model"
        },
        {
            "id": "gemini-2.5-pro",
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





def create_frontend_router(build_dir="frontend/dist"):
    """Creates a router to serve the React frontend.

    Args:
        build_dir: Path to the React build directory relative to the working directory.

    Returns:
        A Starlette application serving the frontend.
    """
    # Use absolute path since we know the container structure
    build_path = pathlib.Path("/deps/frontend/dist")

    if not build_path.is_dir() or not (build_path / "index.html").is_file():
        logger.warning(
            f"WARN: Frontend build directory not found or incomplete at {build_path}. Serving frontend will likely fail."
        )
        # Return a dummy router if build isn't ready
        from starlette.routing import Route

        async def dummy_frontend(request):
            return Response(
                "Frontend not built. Run 'npm run build' in the frontend directory.",
                media_type="text/plain",
                status_code=503,
            )

        return Route("/{path:path}", endpoint=dummy_frontend)

    return StaticFiles(directory=build_path, html=True)


# Mount the frontend under /app to not conflict with the LangGraph API routes
app.mount(
    "/app",
    create_frontend_router(),
    name="frontend",
)
