from os import listdir, makedirs, unlink
from os.path import exists, isfile, islink, join

from fastapi import HTTPException
from yt_dlp import DownloadError, YoutubeDL

from app.utils.filename_sanitizer import sanitize_filename


async def download_audio(video: str) -> str | None:
    try:
        if not exists("cookies.txt"):
            raise FileNotFoundError("Arquivo cookies.txt não encontrado.")

        downloads_path = "/tmp/downloads"

        if not exists(downloads_path):
            makedirs(downloads_path, exist_ok=True)

        with YoutubeDL() as ydl:
            info = ydl.extract_info(video, download=False)

            if not info:
                return None

            print("info:", info)

            title = str(info.get("title", "Sem título"))
            sanitized_title = sanitize_filename(title)

            ydl_opts = {
                "format": "bestaudio[ext=m4a]",
                "outtmpl": join(downloads_path, f"{sanitized_title}.%(ext)s"),
                "writethumbnail": True,
                "noplaylist": True,
                "postprocessors": [
                    {
                        "key": "FFmpegMetadata",  # Adiciona metadados
                    },
                    {
                        "key": "EmbedThumbnail",  # Embutir a thumbnail como capa
                        "already_have_thumbnail": False,  # Baixa a thumbnail se ainda não existir
                    },
                    {
                        "key": "FFmpegExtractAudio",  # Converte para o formato desejado
                        "preferredcodec": "m4a",
                    },
                ],
                "merge_output_format": "m4a",
                "cookiefile": "cookies.txt",
                "verbose": True,
                "cookiesfrombrowser": ("chrome",),
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video])

            file_path = join(downloads_path, f"{sanitized_title}.m4a")
            print("file_path:", file_path)
            if not exists(file_path):
                return None

            return file_path

    except DownloadError as e:
        print(f"Error downloading {video}: {str(e)}")
        raise HTTPException(500, e.msg)
    except Exception as e:
        print("Erro: ", str(e))
        raise HTTPException(500, str(e))


async def clean_downloads():
    download_folder = "downloads"

    for filename in listdir(download_folder):
        file_path = join(download_folder, filename)

        try:
            if isfile(file_path) or islink(file_path):
                unlink(file_path)
        except Exception as e:
            print(f"Erro ao tentar remover {filename}. Motivo: {str(e)}")
