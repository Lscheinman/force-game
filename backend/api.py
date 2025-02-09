from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from builder.map_generator import router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to frontend if needed: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(router)

# Serve API Docs
@app.get("/openapi.json", include_in_schema=False)
def get_open_api_endpoint():
    return JSONResponse(content=app.openapi())

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Game Map API Docs")

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(openapi_url="/openapi.json", title="Game Map API Docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
