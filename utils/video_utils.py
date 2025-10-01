import os
import subprocess
from pathlib import Path

def run_ffmpeg(input_file, output_file, ffmpeg_cmd):
    """
    Lance une commande FFmpeg.
    """
    try:
        print(f"▶️ Exécution FFmpeg : {ffmpeg_cmd}")
        subprocess.run(ffmpeg_cmd, shell=True, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur FFmpeg : {e}")
        return None


def compress_to_resolution(input_file: str, output_dir: str, resolution: str = "720p") -> str:
    """
    Compresse une vidéo en une résolution donnée (720p, 480p, 360p).
    Retourne le chemin du fichier généré.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    res_map = {
        "720p": "1280:720",
        "480p": "854:480",
        "360p": "640:360"
    }

    if resolution not in res_map:
        raise ValueError("Résolution non supportée. Choisis parmi : 720p, 480p, 360p")

    output_file = os.path.join(output_dir, f"video_{resolution}.mp4")
    scale_filter = f"scale={res_map[resolution]}:force_original_aspect_ratio=decrease"

    ffmpeg_cmd = (
        f'ffmpeg -i "{input_file}" -vf "{scale_filter}" '
        f'-c:v libx264 -crf 28 -preset veryfast -c:a aac -b:a 128k "{output_file}" -y'
    )

    return run_ffmpeg(input_file, output_file, ffmpeg_cmd)


def generate_multi_resolutions(input_file: str, output_dir: str) -> dict:
    """
    Génère plusieurs résolutions (720p, 480p, 360p).
    Retourne un dict avec les chemins des fichiers générés.
    """
    results = {}
    for res in ["720p", "480p", "360p"]:
        results[res] = compress_to_resolution(input_file, output_dir, res)
    return results


def resize_custom(input_file: str, output_dir: str, width: int, height: int) -> str:
    """
    Redimensionne une vidéo selon des dimensions personnalisées.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_file = os.path.join(output_dir, f"video_{width}x{height}.mp4")
    scale_filter = f"scale={width}:{height}"

    ffmpeg_cmd = (
        f'ffmpeg -i "{input_file}" -vf "{scale_filter}" '
        f'-c:v libx264 -crf 28 -preset veryfast -c:a aac -b:a 128k "{output_file}" -y'
    )

    return run_ffmpeg(input_file, output_file, ffmpeg_cmd)
