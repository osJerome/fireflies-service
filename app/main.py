from fastapi import FastAPI
from app.routers import fireflies
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Firefly Interview ATS Mapping",
    openapi_tags=[
        {"name": "Firefly"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

route = "/api/v1"

app.include_router(fireflies.router, prefix=f"{route}/fireflies", tags=["Firefly"])
