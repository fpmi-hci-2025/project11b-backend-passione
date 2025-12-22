from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import menu, tables, sessions, carts, orders

app = FastAPI(
    title="Passione API",
    description="REST API для системы управления рестораном Passione",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(menu.router)
app.include_router(tables.router)
app.include_router(sessions.router)
app.include_router(carts.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Passione Restaurant API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}
