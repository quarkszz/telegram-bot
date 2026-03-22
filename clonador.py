from telethon import TelegramClient, events
import re
import asyncio
import urllib.parse
import hashlib
import requests
from datetime import datetime

# ==============================
# 🔑 AFILIADOS
# ==============================

APP_KEY = "530014"
APP_SECRET = "2L9VRcfhMQWNkkN2ZY14zOrbPR5PuVs2"

AMAZON_TAG = "quarkszz-20"

# ==============================
# 🔑 TELEGRAM
# ==============================

api_id = 35640192
api_hash = '524c7bb51f9f8f01c22edd275fff4692'

# ==============================
# 📡 CANAIS DE ORIGEM
# ==============================

source_channels = [
    'https://t.me/pcdofafapromo',
    'https://t.me/SetupHumilde',
    'https://t.me/Fraguas84Oficial'
]

# ==============================
# 📤 DESTINO
# ==============================

target_channel = 'https://t.me/quarkszzz'

client = TelegramClient('session', api_id, api_hash)

mensagens_enviadas = set()

# ==============================
# 🔐 GERAR SIGN
# ==============================

def gerar_sign(params, app_secret):
    sorted_params = sorted(params.items())

    base_string = app_secret
    for k, v in sorted_params:
        base_string += f"{k}{v}"
    base_string += app_secret

    return hashlib.md5(base_string.encode('utf-8')).hexdigest().upper()

# ==============================
# 🔍 EXPANDIR LINK (ESSENCIAL)
# ==============================

def expandir_link(link):
    try:
        response = requests.get(link, allow_redirects=True, timeout=5)
        print("🔄 LINK EXPANDIDO:", response.url)
        return response.url
    except:
        return link

# ==============================
# 🌐 ALIEXPRESS API
# ==============================

def gerar_link_aliexpress_api(link_original):
    url = "https://api-sg.aliexpress.com/sync"

    params = {
        "app_key": APP_KEY,
        "method": "aliexpress.affiliate.link.generate",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "format": "json",
        "v": "2.0",
        "sign_method": "md5",
        "promotion_link_type": "0",
        "source_values": link_original
    }

    params["sign"] = gerar_sign(params, APP_SECRET)

    try:
        response = requests.post(url, data=params)
        data = response.json()

        print("🔍 Resposta API:", data)

        return data['aliexpress_affiliate_link_generate_response']['resp_result']['result']['promotion_links'][0]['promotion_link']

    except Exception as e:
        print("❌ Erro API:", e)
        return link_original

# ==============================
# 🔗 GERAR LINK AFILIADO
# ==============================

def gerar_link_afiliado(link):
    try:
        # 🔥 EXPANDE PRIMEIRO (corrige link roubado)
        link = expandir_link(link)

        # AliExpress
        if "aliexpress" in link:
            return gerar_link_aliexpress_api(link)

        # Amazon
        if "amazon" in link:
            if "tag=" not in link:
                separador = "&" if "?" in link else "?"
                return f"{link}{separador}tag={AMAZON_TAG}"
            return link

        return link

    except:
        return link

# ==============================
# 🔎 EXTRAIR LINK
# ==============================

def extrair_link(event):
    if event.message.message:
        links = re.findall(r'(https?://[^\s]+)', event.message.message)
        if links:
            return links[0]

    if event.message.buttons:
        for row in event.message.buttons:
            for btn in row:
                if btn.url:
                    return btn.url

    if event.message.entities:
        for ent in event.message.entities:
            if hasattr(ent, 'url') and ent.url:
                return ent.url

    return None

# ==============================
# 🧹 LIMPAR TEXTO
# ==============================

def limpar_texto(texto):
    texto = re.sub(r'https?://\S+', '', texto)
    texto = re.sub(r'@\w+', '', texto)
    return texto.strip()

# ==============================
# 📩 HANDLER
# ==============================

@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        print("📩 Nova mensagem detectada")

        mensagem = event.message.message

        if not mensagem:
            return

        if mensagem in mensagens_enviadas:
            return

        link = extrair_link(event)

        print("🔎 LINK CAPTURADO:", link)

        if not link:
            print("❌ Sem link")
            return

        mensagens_enviadas.add(mensagem)

        # 🔗 gerar afiliado
        link_afiliado = gerar_link_afiliado(link)

        print("🔗 LINK FINAL:", link_afiliado)

        texto_limpo = limpar_texto(mensagem)

        msg_final = f"""🔥 *SUPER OFERTA!*

🛍️ {texto_limpo}

💰 *Melhor preço encontrado!*
⚡ Aproveite antes que suba!

🔗 {link_afiliado}

🔔 @quarkszzz
"""

        # 🔥 ENVIO COM IMAGEM (SE TIVER)
        if event.message.photo:
            await client.send_file(
                target_channel,
                file=event.message.photo,
                caption=msg_final,
                parse_mode='markdown'
            )
        else:
            await client.send_message(
                target_channel,
                msg_final,
                parse_mode='markdown'
            )

        print("💰 Enviado com sucesso!")

        await asyncio.sleep(1)  # evita spam / limite

    except Exception as e:
        print("💥 ERRO NO HANDLER:", e)

# ==============================
# 🚀 START
# ==============================

async def main():
    print("🚀 BOT RODANDO 24H...")

    try:
        await client.start()
        print("✅ Conectado no Telegram")

        await client.run_until_disconnected()

    except Exception as e:
        print("💥 ERRO CRÍTICO:", e)

asyncio.run(main())
