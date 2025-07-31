import json
import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("GROUP_ID")
DATA_FILE = 'database.json'

bot = Bot(token=TOKEN)

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

async def main_loop():
    while True:
        data = read_data()
        if data.get('bot_ativo'):
            try:
                await bot.send_message(chat_id=CHAT_ID, text=f"{data['mensagem']}\n\nEstratégia: {data['estrategia']}")
            except TelegramError as e:
                print(f"Erro ao enviar: {e}")
            await asyncio.sleep(data['tempo_envio'] * 60)
        else:
            await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main_loop())
