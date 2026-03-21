from telethon import TelegramClient, events
import re
import asyncio
import urllib.parse

# 🔑 AFILIADOS
ALIEXPRESS_ID = "quarkszz"
AMAZON_TAG = "quarkszz-20"

# 🔑 TELEGRAM
api_id = 35640192
api_hash = '524c7bb51f9f8f01c22edd275fff4692'

# 📡 CANAIS DE ORIGEM
source_channels = [
    'https://t.me/pcdofafapromo',
    'https://t.me/SetupHumilde',
    'https://t.me/Fraguas84Oficial'
]

# 📤 DESTINO
target_channel = 'https://t.me/quarkszzz'

client = TelegramClient('session', api_id, api_hash)

mensagens_enviadas = set()

# 🔗 GERAR LINK AFILIADO
def gerar_link_afiliado(link):
    try:
        if "aliexpress" in link:
            encoded = urllib.parse.quote(link, safe='')
            return f"https://s.click.aliexpress.com/deep_link.htm?dl_target_url={encoded}&aff_short_key={ALIEXPRESS_ID}"

        if "amazon" in link:
            if "tag=" not in link:
                separador = "&" if "?" in link else "?"
                return f"{link}{separador}tag={AMAZON_TAG}"
            return link

        return link

    except:
        return link

# 🔎 EXTRAIR LINK (FORTE)
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

# 🧹 LIMPAR TEXTO
def limpar_texto(texto):
    texto = re.sub(r'https?://\S+', '', texto)
    texto = re.sub(r'@\w+', '', texto)
    return texto.strip()

# 📩 HANDLER
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
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

    try:
        await client.send_message(
            target_channel,
            msg_final,
            parse_mode='markdown'
        )

        print("💰 Enviado com sucesso!")

    except Exception as e:
        print("❌ Erro:", e)

# 🚀 START
async def main():
    print("🚀 RODANDO 24H...")
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
