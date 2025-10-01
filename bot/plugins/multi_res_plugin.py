from pyrogram import Client, filters
from utils.video_utils import generate_multi_resolutions

@Client.on_message(filters.command("multi") & filters.video)
async def multi_resolutions_handler(client, message):
    # Téléchargement de la vidéo envoyée
    input_file = await message.download()
    output_dir = "outputs"

    await message.reply_text("🔄 Génération des différentes résolutions...")

    # Génération des versions multi-résolutions
    results = generate_multi_resolutions(input_file, output_dir)

    # Envoi des vidéos compressées à l'utilisateur
    for res, file_path in results.items():
        if file_path:
            await message.reply_document(file_path, caption=f"🎥 Version {res}")
