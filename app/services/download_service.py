from os import listdir, unlink, makedirs
from yt_dlp import YoutubeDL, DownloadError
from os.path import exists, join, isfile, islink
from app.utils.filename_sanitizer import sanitize_filename


async def download_audio(video: str) -> str:
    try:
        downloads_path = '/tmp/downloads'

        if not exists(downloads_path):
            makedirs(downloads_path)

        with YoutubeDL() as ydl:
            info = ydl.extract_info(video, download=False)
            title = str(info.get('title', 'Sem título'))
            sanitized_title = sanitize_filename(title)

            ydl_opts = {
                'format': 'bestaudio[ext=m4a]',
                'outtmpl': join(downloads_path, f'{sanitized_title}.%(ext)s'),
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
                'cookiefile': 'cookies.txt',
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video])

            file_path = join(downloads_path, f'{sanitized_title}.m4a')

            return file_path if exists(file_path) else None

    except DownloadError as e:
        print(f"Error downloading {video}: {str(e)}")
        return None
    except Exception as e:
        print('Erro: ', str(e))
        return None


async def clean_downloads():
     download_folder = 'downloads'

     for filename in listdir(download_folder):
        file_path = join(download_folder, filename)

        try: 

            if isfile(file_path) or islink(file_path):
                unlink(file_path)

        except Exception as e: 
            print(f'Erro ao tentar remover {filename}. Motivo: {str(e)}')
