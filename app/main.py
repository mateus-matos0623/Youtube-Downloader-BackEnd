from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.download import router as download_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["https://you-audio.vercel.app"],
    allow_credentials=True, 
    allow_methods=["GET"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

app.include_router(download_router)

@app.get('/')
def home():
    return {"message": "home"}
