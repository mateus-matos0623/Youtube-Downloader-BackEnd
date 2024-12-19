from os.path import exists, join
from yt_dlp import YoutubeDL, DownloadError
from app.utils.filename_sanitizer import sanitize_filename

async def download_audio(video: str) -> str | None:
    try:
        with YoutubeDL() as ydl:
            info = ydl.extract_info(video, download=False)
            title = str(info.get('title', 'Sem título'))
            sanitized_title = sanitize_filename(title)

            print(f"Título original: {title}") 
            print(f"Título sanitizado: {sanitized_title}")

            ydl_opts = {
                'format': 'bestaudio[ext=m4a]',
                'outtmpl': f'downloads/{sanitized_title}.%(ext)s',
                'writethumbnail': True,
                'noplaylist': True,
                'postprocessors': [
                    {
                        'key': 'FFmpegMetadata',  # Adiciona metadados
                    },
                    {
                        'key': 'EmbedThumbnail',  # Embutir a thumbnail como capa
                        'already_have_thumbnail': False,  # Baixa a thumbnail se ainda não existir
                    },
                    {
                        'key': 'FFmpegExtractAudio',  # Converte para o formato desejado
                        'preferredcodec': 'm4a',
                    },
                ],
                'merge_output_format': 'm4a',
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video])

            file_path = join('downloads', f'{sanitized_title}.m4a')
            print(f'Caminho: ', file_path)

            if not exists(file_path):
                print(f"Arquivo não encontrado: {file_path}")
                return None
            
            return file_path

    except DownloadError as e:
        print(f"Error downloading {video}: {str(e)}")
        return None
    except Exception as e:
        print('Erro: ', str(e))
        return None
