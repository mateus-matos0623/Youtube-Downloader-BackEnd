from os import listdir, unlink, makedirs
from yt_dlp import YoutubeDL, DownloadError
from os.path import exists, join, isfile, islink
from app.utils.filename_sanitizer import sanitize_filename


async def download_audio(video: str) -> str:
    try:
        with YoutubeDL() as ydl:
            info = ydl.extract_info(video, download=False)
            title = str(info.get('title', 'Sem título'))
            sanitized_title = sanitize_filename(title)

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

            if not exists(file_path):
                downloads_path = 'downloads' 
                makedirs(downloads_path)
                file_path = join('downloads', f'{sanitized_title}.m4a')
            
            return file_path

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
