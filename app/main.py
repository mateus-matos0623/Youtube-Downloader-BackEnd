from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.download import router as download_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

@app.get('/')
def home():
    return {"message": "home"}

app.include_router(download_router, prefix="/download")
