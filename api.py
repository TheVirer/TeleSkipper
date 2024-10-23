import uvicorn
from fastapi import FastAPI

app = FastAPI()

def run_api():
    uvicorn.run("api:app",port=8000)

