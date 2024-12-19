from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.download import router as download_router
from os.path import exists
from os import makedirs

app = FastAPI()
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["https://you-audio.vercel.app"],
    allow_credentials=True, 
    allow_methods=["GET"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)


downloads_path = 'downloads' 
if not exists(downloads_path): 
    makedirs(downloads_path)

app.include_router(download_router, prefix='/download')

@app.get('/')
def home():
    return {"message": "home"}
