import discord
from discord.ext import commands
from googleapiclient.discovery import build
import asyncio
import json
import os

intents = discord.Intents.default()
intents.members = True  # Subscribe to member events
intents.presences = True  # Subscribe to presence events
intents.message_content = True  # Subscribe to message content

# Token bot Discord
TOKEN = 'token-bot'

# ID channel Discord
CHANNEL_ID_DISCORD = id channel dc

# ID role WOTA
ROLE_ID_WOTA = id role channel dc 

# API key YouTube
YOUTUBE_API_KEY = 'api-key'

# Daftar akun YouTube yang ingin dipantau
YOUTUBE_CHANNEL_IDS = [
    'UCaIbbu5Xg3DpHsn_3Zw2m9w',
    'UCU99s2YAshupQvvVz7XQNcA'
    # tambahkan akun lainnya di sini
]

# File untuk menyimpan ID video terakhir yang dipublikasikan
LAST_VIDEO_ID_FILE = 'last_video_id.json'
if not os.path.exists(LAST_VIDEO_ID_FILE):
    with open(LAST_VIDEO_ID_FILE, 'w') as f:
        json.dump({}, f)

# Membuat bot Discord
bot = commands.Bot(command_prefix='!', intents=intents)

# Membuat klien API YouTube
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

@bot.command(name='tagrole', help='Mengtag role dalam Discord')
async def tagrole(ctx, role: discord.Role):
    await ctx.send(f'Mengtag role {role.mention}!')

# Fungsi untuk memeriksa video baru
async def check_new_video():
    for channel_id in YOUTUBE_CHANNEL_IDS:
        # Membaca ID video terakhir yang dipublikasikan dari file
        try:
            with open(LAST_VIDEO_ID_FILE, 'r') as f:
                try:
                    last_video_ids = json.load(f)
                except json.JSONDecodeError:
                    last_video_ids = {}
                    print(f"File {LAST_VIDEO_ID_FILE} kosong atau tidak berisi data JSON yang valid.")
        except FileNotFoundError:
            last_video_ids = {}

        # Membuat permintaan API YouTube
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            order='date',
            maxResults=1
        )
        response = request.execute()

        # Mendapatkan ID video terbaru yang dipublikasikan
        video_id = response['items'][0]['id']['videoId']

        # Memeriksa apakah video terbaru yang dipublikasikan memiliki ID yang berbeda dari ID video terakhir yang dipublikasikan
        if channel_id not in last_video_ids or video_id != last_video_ids[channel_id]:
            # Mendapatkan judul dan URL video
            title = response['items'][0]['snippet']['title']
            url = f'https://www.youtube.com/watch?v={video_id}'

            # Mengirimkan pesan ke channel Discord
            channel = bot.get_channel(CHANNEL_ID_DISCORD)
            
            await channel.send(f'<@&{ROLE_ID_WOTA}> JOT upload nich !!!\n\n{title}\n{url}')

            # Menyimpan ID video terbaru yang dipublikasikan ke file
            last_video_ids[channel_id] = video_id
            with open(LAST_VIDEO_ID_FILE, 'w') as f:
                json.dump(last_video_ids, f)

# Event untuk memeriksa video baru setiap 10 menit
@bot.event
async def on_ready():
    print(f'{bot.user} telah siap!')
    while True:
        await check_new_video()
        await asyncio.sleep(300)  # 10 menit

# Menjalankan bot Discord
bot.run(TOKEN)
