# mypy: disable - error - code = "no-untyped-def,misc"
import pathlib
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

# Define the FastAPI app
app = FastAPI()


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
        print(
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
