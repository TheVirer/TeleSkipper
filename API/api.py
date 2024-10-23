import uvicorn
from fastapi import FastAPI
from API.routes import router

app = FastAPI()
app.include_router(router)

def run_api():
    uvicorn.run("API.api:app",port=8000)

