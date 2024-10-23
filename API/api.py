import uvicorn
from fastapi import FastAPI

app = FastAPI()

def run_api():
    uvicorn.run("API.api:app",port=8000)

