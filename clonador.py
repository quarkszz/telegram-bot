from telethon import TelegramClient, events, Button
import re
import asyncio
import requests
import hashlib
import time

import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
TRACKING_ID = os.getenv("TRACKING_ID")

# 📡 canais de origem
source_channels = [
    'https://t.me/pcdofafapromo',
    'https://t.me/SetupHumilde',
    'https://t.me/Fraguas84Oficial'
]

# 📤 seu canal
target_channel = 'https://t.me/quarkszzz'

client = TelegramClient('session', api_id, api_hash)

mensagens_enviadas = set()

# 🔎 extrair link
def extrair_link(texto):
    if not texto:
        return None
    links = re.findall(r'https?://\S+', texto)
    for link in links:
        if "aliexpress" in link:
            return link
    return None

# 🔐 assinatura API
def gerar_assinatura(params):
    base = APP_SECRET
    for k in sorted(params.keys()):
        base += k + str(params[k])
    base += APP_SECRET
    return hashlib.md5(base.encode()).hexdigest().upper()

# 💰 gerar link afiliado REAL
def gerar_link_afiliado(link):
    url = "https://api-sg.aliexpress.com/sync"

    params = {
        "app_key": APP_KEY,
        "method": "aliexpress.affiliate.link.generate",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tracking_id": TRACKING_ID,
        "promotion_link_type": "0",
        "source_values": link,
        "sign_method": "md5"
    }

    params["sign"] = gerar_assinatura(params)

    try:
        response = requests.get(url, params=params)
        data = response.json()

        return data["aliexpress_affiliate_link_generate_response"]["resp_result"]["result"]["promotion_links"][0]["promotion_link"]

    except Exception as e:
        print("Erro API:", e)
        return link

# 🎯 filtro
def eh_promocao(texto):
    if not texto:
        return False

    palavras = ["R$", "promo", "desconto", "oferta", "%", "🔥"]
    return any(p.lower() in texto.lower() for p in palavras)

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    mensagem = event.message.text

    if not eh_promocao(mensagem):
        return

    if mensagem in mensagens_enviadas:
        return

    link = extrair_link(mensagem)
    if not link:
        return

    mensagens_enviadas.add(mensagem)

    link_afiliado = gerar_link_afiliado(link)

    texto_limpo = re.sub(r'https?://\S+', '', mensagem).strip()

    msg_final = f"""🔥 *OFERTA ENCONTRADA!*

{texto_limpo}

💰 Aproveite agora:
👇 Clique no botão abaixo"""

    try:
        await asyncio.sleep(4)

        await client.send_message(
            target_channel,
            msg_final,
            file=event.message.media,
            buttons=[[Button.url("🛒 COMPRAR AGORA", link_afiliado)]],
            parse_mode='markdown'
        )

        print("💰 Enviado com afiliado!")

    except Exception as e:
        print("❌ Erro:", e)

print("🚀 SISTEMA COMPLETO RODANDO...")
client.start()
client.run_until_disconnected()
