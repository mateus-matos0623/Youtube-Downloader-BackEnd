from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException
from app.services.download_service import download_audio
from os.path import join, exists

router = APIRouter()

@router.get('/')
async def download_audio_endpoint(video: str):
    relative_path = await download_audio(video)

    if not relative_path:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    # file_path = join('downloads', relative_path)
    filename = relative_path.split('\\')[-1]
    # print(f"Caminho completo do arquivo: {file_path}")

    # if not exists(file_path): 
    #     raise HTTPException(status_code=404, detail="Arquivo não encontrado no caminho esperado")

    return FileResponse(path=relative_path, 
                        media_type='audio/m4a', 
                        filename=filename, 
                        status_code=200)
