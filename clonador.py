# 🔑 AFILIADOS
ALIEXPRESS_ID = "quarkszz"
AMAZON_TAG = "quarkszz-20"

from telethon import TelegramClient, events, Button
import re
import asyncio
import urllib.parse

# 🔑 SUAS INFORMAÇÕES (ALTERE AQUI)
api_id = 35640192
api_hash = '524c7bb51f9f8f01c22edd275fff4692'

TRACKING_ID = "quarkszz"

# 📡 CANAIS DE ORIGEM
source_channels = [
    'https://t.me/pcdofafapromo',
    'https://t.me/SetupHumilde',
    'https://t.me/Fraguas84Oficial'
]

# 📤 SEU CANAL
target_channel = 'https://t.me/quarkszzz'

client = TelegramClient('session', api_id, api_hash)

mensagens_enviadas = set()

# 🔗 GERAR LINK AFILIADO (DEEP LINK)
import urllib.parse

def gerar_link_afiliado(link):
    try:
        # 🟠 AliExpress
        if "aliexpress" in link:
            encoded = urllib.parse.quote(link, safe='')
            return f"https://s.click.aliexpress.com/deep_link.htm?dl_target_url={encoded}&aff_short_key={ALIEXPRESS_ID}"

        # 🟡 Amazon
        if "amazon" in link:
            if "tag=" not in link:
                separador = "&" if "?" in link else "?"
                return f"{link}{separador}tag={AMAZON_TAG}"
            return link

        # 🔵 Mercado Livre (sem afiliado direto fácil)
        if "mercadolivre" in link or "meli" in link:
            return link

        # 🌐 outros sites
        return link

    except Exception as e:
        print("Erro afiliado:", e)
        return link

# 🔎 EXTRAIR LINK
def extrair_link(texto):
    if not texto:
        return None

    links = re.findall(r'(https?://[^\s]+)', texto)
    return links[0] if links else None

# 🧹 LIMPAR TEXTO
def limpar_texto(texto):
    texto = re.sub(r'https?://\S+', '', texto)  # remove links
    texto = re.sub(r'@\w+', '', texto)         # remove @canais
    return texto.strip()

# 🎯 FILTRO (opcional)
def eh_promocao(texto):
    if not texto:
        return False

    palavras = ["R$", "promo", "desconto", "oferta", "%", "🔥"]
    return any(p.lower() in texto.lower() for p in palavras)

# 📩 MONITORAR MENSAGENS
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    mensagem = event.message.text

    if not mensagem:
        return

    # (opcional) filtrar promoções
    if not eh_promocao(mensagem):
        return

    if mensagem in mensagens_enviadas:
        return

    link = extrair_link(mensagem)

    if not link:
        print("❌ Sem link, ignorado")
        return

    mensagens_enviadas.add(mensagem)

    link_afiliado = gerar_link_afiliado(link)

    if not link_afiliado:
        link_afiliado = link

    print("🔗 LINK FINAL:", link_afiliado)

    texto_limpo = limpar_texto(mensagem)

    msg_final = f"""🔥 *SUPER OFERTA!*

🛍️ {texto_limpo}

💰 *Melhor preço encontrado!*
⚡ Aproveite antes que suba!

👇 COMPRE AGORA:

🔔 @quarkszzz
"""

   msg_final = f"""🔥 *SUPER OFERTA!*

🛍️ {texto_limpo}

💰 *Melhor preço encontrado!*
⚡ Aproveite antes que suba!

🔗 {link_afiliado}

🔔 @quarkszzz
"""

await client.send_message(
    target_channel,
    msg_final,
    file=event.message.media,
    parse_mode='markdown'
)
        print("💰 Enviado com sucesso!")

    except Exception as e:
        print("❌ Erro ao enviar:", e)

# 🚀 INICIAR BOT
async def main():
    print("🚀 SISTEMA RODANDO 24H...")

    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
