import subprocess
import requests
# import json
from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
import re
import time

def limpar_nome(nome):
    # Remove qualquer caractere inválido no Windows
    return re.sub(r'[<>:"/\\|?*\uFF1F]', '', nome)

def baixar_playlist(url, pasta_destino, callback_progresso=None, callback_log=None, cancelar_callback=None):
    pasta = Path(pasta_destino)
    pasta.mkdir(exist_ok=True)

    # Primeiro, obtemos a lista de vídeos
    cmd_lista = [
        "yt-dlp",
        "--flat-playlist",
        "--print", "%(id)s", 
        "--skip-download", url
    ]
    
    resultado = subprocess.run(cmd_lista, stdout=subprocess.PIPE, text=True)
    video_ids = resultado.stdout.strip().split('\n')
    total = len(video_ids)

    for i, video_id in enumerate(video_ids, start=1):
        if cancelar_callback and cancelar_callback():
            if callback_log:
                callback_log("⛔ Download cancelado pelo usuário.")
            break

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        if callback_log:
            callback_log(f"🎵 Iniciando download da faixa {i} de {total}")
        
        # mp3_path = baixar_audio(video_url, pasta, callback_log=callback_log)
        mp3_path = baixar_audio(video_url, pasta, cancelar_callback=cancelar_callback)
        
        if mp3_path:
            if callback_log:
                callback_log("🎧 Processando metadados...")
            info = buscar_metadados(mp3_path.stem)
            if info:
                # aplicar_metadados(mp3_path, info)
                mp3_path = aplicar_metadados(mp3_path, info)
        
        if callback_progresso:
            callback_progresso(i, total)
        
        if callback_log:
            callback_log("✅ Download Finalizado.\n")

    for json_file in Path(pasta).glob("*.info.json"):
        json_file.unlink()

# def baixar_audio(url, destino, callback_log=None):
#     temp_output = destino / "%(title)s.%(ext)s"
#     cmd = [
#         "yt-dlp",
#         "-x", "--audio-format", "mp3",
#         "--embed-thumbnail",
#         "--output", str(temp_output),
#         "--write-info-json",
#         url
#     ]
    
#     try:
#         subprocess.run(cmd, check=True)
    
#     except subprocess.CalledProcessError as e:
#         if callback_log:
#             callback_log(f"❌ Erro ao baixar o vídeo: {url}\n{e}")
#         return None

#     arquivos = list(Path(destino).glob("*.mp3"))
#     for mp3 in sorted(arquivos, key=lambda x: x.stat().st_mtime, reverse=True):
#         nome_limpo = limpar_nome(mp3.stem)
#         novo_nome = mp3.with_name(nome_limpo + ".mp3")
#         if mp3 != novo_nome:
#             mp3.rename(novo_nome)
#         return novo_nome
#     return None

def baixar_audio(url, destino, cancelar_callback=None):
    temp_output = destino / "%(title)s.%(ext)s"
    cmd = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "--embed-thumbnail",
        "--output", str(temp_output),
        "--write-info-json",
        url
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while process.poll() is None:
        if cancelar_callback and cancelar_callback():
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            return None
        time.sleep(0.2)

    if process.returncode != 0:
        return None  # evita erro no restante do código

    arquivos = list(Path(destino).glob("*.mp3"))
    for mp3 in sorted(arquivos, key=lambda x: x.stat().st_mtime, reverse=True):
        nome_limpo = limpar_nome(mp3.stem)
        novo_nome = mp3.with_name(nome_limpo + ".mp3")
        if mp3 != novo_nome:
            mp3.rename(novo_nome)
        return novo_nome
    return None


def buscar_metadados(titulo):
    response = requests.get("https://itunes.apple.com/search", params={"term": titulo, "media": "music", "limit": 1})
    data = response.json()
    if data["resultCount"] == 0:
        return None
    return data["results"][0]

def aplicar_metadados(mp3_path, info):
    try:
        audio = EasyID3(mp3_path)
    except Exception:
        audio = MP3(mp3_path, ID3=ID3)
        audio.add_tags()
        audio = EasyID3(mp3_path)

    artista = info.get("artist") or info.get("uploader") or "Desconhecido"
    titulo = info.get("track") or info.get("title") or "Sem Título"

    audio["title"] = titulo
    audio["artist"] = artista
    audio.save()

    # Renomear com base em Artista - Música
    nome_seguro = f"{limpar_nome(artista)} - {limpar_nome(titulo)}.mp3"
    novo_caminho = mp3_path.with_name(nome_seguro)

    try:
        if mp3_path != novo_caminho:
            mp3_path.rename(novo_caminho)
    except FileExistsError:
        pass

    # Remover arquivos .json se existirem
    json_file = mp3_path.with_suffix(".info.json")
    if json_file.exists():
        json_file.unlink()

    return novo_caminho
