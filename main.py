from fastapi import FastAPI

app = FastAPI(title="Passione API", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Hello World from Passione Backend"}


@app.get("/health")
async def health():
    return {"status": "ok"}

