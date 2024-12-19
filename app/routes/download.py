from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.download_service import download_audio, clean_downloads

router = APIRouter()

@router.get('/download/')
async def download_audio_endpoint(video: str, background_tasks: BackgroundTasks):
    relative_path = await download_audio(video)

    if not relative_path:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    filename = relative_path.split('\\')[-1]
    background_tasks.add_task(clean_downloads)

    return FileResponse(path=relative_path, 
                        media_type='audio/m4a', 
                        filename=filename, 
                        status_code=200)
