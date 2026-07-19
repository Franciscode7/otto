import requests
import json
import re
import aiohttp

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes


iaMain = "llama3.1:8b"
iaSecond = "llama3.2:latest"
iaPhi = "phi3.5:3.8b-mini-instruct-q6_K"

# ------------ CONFIG ------------

TOKEN_TELEGRAM = "8742607552:AAH6ESb97z7fLROC8aZFZzvgaOc0U3xHUZQ"

OLLAMA_URL = "http://localhost:11434/api/generate"

LAPTOP_API = "http://100.96.246.102:7777/orden"

API_HEADERS = {
    "X-API-KEY": "fran123",
    "Content-Type": "application/json"
}


# ------------ BOT ------------
async def generar_respuesta_ollama(prompt_usuario):
    # La URL apunta al puerto por defecto de Ollama en el mismo contenedor
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": iaPhi, # Asegúrate que sea el nombre exacto de 'ollama list'
        "prompt": prompt_usuario,
        "system": "Otto, el mejor asistente y usas el modelo " + iaPhi + ". Responde siempre en español y de manera conscisa",
        "stream": False,
        "options": {
            "num_predict": 80,  # Limita la respuesta a ~75-100 palabras
            "temperature": 0.8,   # Creatividad moderada
            "top_k": 20,          # Menos opciones para procesar más rápido
            "num_thread": 16       # Usa 4 hilos de tu CPU (ajusta según tu LXC)
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("response", "Lo siento, recibí una respuesta vacía.")
                else:
                    return f"Error de Ollama: Código de estado {response.status}"
    except Exception as e:
        return f"No pude conectar con la IA: {str(e)}"


async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_text = update.message.text


    # SYSTEM PROMPT (copiado tal cual)
    prompt1 = (
        f"Eres Otto, un asistente que interpreta órdenes.\n\n"

        f"REGLA PRINCIPAL:\n"
        f"Si detectas una orden de automatización, responde EXCLUSIVAMENTE en JSON válido.\n"
        f"No agregues explicaciones, texto extra, markdown ni comentarios.\n\n"
        
        f"Las palabras clave seran 'abrir', 'cerrar', 'brillo', 'volumen', 'anota', 'reproducir', 'ajustar'. en caso de que no lleve ninguna de estas palabras, responde como asistente conversacional normal.\n\n"

        f"Devuelve UN SOLO objeto JSON."
        f"No expliques."
        f"No corrijas."
        f"No agregues texto despues"
        f"Termina inmediatamente después del JSON."

        f"Formato obligatorio:\n"
        f'{{"accion":"TIPO","valor":"DATO"}}\n\n'

        f"ACCIONES SOPORTADAS:\n"

        f"1. Abrir enlaces o páginas web:\n"
        f"Ejemplo:\n"
        f'{{"accion":"abrir_url","valor":"https://google.com"}}\n\n'

        f"2. Buscar o reproducir en YouTube:\n"
        f"Ejemplo:\n"
        f'{{"accion":"youtube","valor":"musica relajante"}}\n\n'

        f"3. Ajustar brillo:\n"
        f"Ejemplo:\n"
        f'{{"accion":"brillo","valor":"40"}}\n\n'

        f"4. Ajustar volumen:\n"
        f"Ejemplo:\n"
        f'{{"accion":"volumen","valor":"20"}}\n\n'

        f"5. Escribir nota:\n"
        f"Ejemplo:\n"
        f'{{"accion":"nota","valor":"comprar tortillas"}}\n\n'

        f"6. Abrir aplicaciones:\n"
        f"Apps conocidas:\n"
        f"Bloc de notas -> notepad\n"
        f"Calculadora -> calc\n"
        f"Explorador -> explorer\n"
        f"Visual Studio Code -> code\n"
        f"Edge -> msedge\n"
        f"Chrome -> chrome\n"

        f"Ejemplo:\n"
        f'{{"accion":"abrir_app","valor":"chrome"}}\n\n'

        f"7. Cerrar aplicaciones:\n"
        f"Ejemplo:\n"
        f'{{"accion":"cerrar_app","valor":"chrome"}}\n\n'

        f"SI NO es comando:\n"
        f"Responde como asistente conversacional normal.\n\n"

        f"Prioridad:\n"
        f"- Si contiene youtube -> youtube\n"
        f"- Si contiene dominio .com .net .org .mx -> abrir_url\n"
        f"- abrir + app -> abrir_app\n"
        f"- cerrar + app -> cerrar_app\n"
        f"- brillo -> brillo\n"
        f"- volumen -> volumen\n"
        f"- nota -> nota\n\n"

        f"Orden del usuario: {user_text}"
    )


    try:

        # ---------- OLLAMA ----------
        res_ollama = requests.post(
            OLLAMA_URL,
            json={
                "model": iaMain,
                "prompt": prompt1,
                "stream": False
            },
            timeout=160
        )

        data = res_ollama.json()


        if "error" in data:
            await update.message.reply_text(
                f"Error Ollama:\n{data['error']}"
            )
            return


        if "response" not in data:
            await update.message.reply_text(
                f"Respuesta inválida:\n{data}"
            )
            return


        respuesta = data["response"]


        # -------- Extraer primer JSON válido --------

        match = re.search(
            r'\{.*?\}',
            respuesta,
            re.DOTALL
        )

        if not match:
            await update.message.reply_text(
                respuesta
            )
            return


        json_texto = match.group(0)

        datos_ia = json.loads(json_texto)


        accion = datos_ia.get("accion")
        valor  = datos_ia.get("valor")


        # -------- Whitelist --------

        acciones_validas = {
            "abrir_url",
            "youtube",
            "brillo",
            "volumen",
            "nota",
            "abrir_app",
            "cerrar_app"
        }

        if accion not in acciones_validas:

            # await update.message.reply_text(
            #     f"Acción no permitida: {accion}"
            # )
            # return
            
            # 1. Indicamos que estamos procesando (opcional, da mejor experiencia)
            await update.message.chat.send_action(action="typing")
            
            # 2. Llamamos a la lógica de tu IA normal
            # Aquí pasas el texto original del usuario que guardaste antes
            respuesta_ia = await generar_respuesta_ollama(update.message.text)
            
            # 3. Respondemos con lo que dijo la IA
            await update.message.reply_text(respuesta_ia)
            return


        # -------- Sanear brillo/volumen --------

        if accion in ("brillo", "volumen"):

            try:
                valor = int(valor)

                if valor < 0:
                    valor = 0

                if valor > 100:
                    valor = 100

            except:
                await update.message.reply_text(
                    "Valor inválido."
                )
                return


        payload = {
            "accion": accion,
            "valor": valor
        }


        # -------- Enviar a tu Flask --------

        try:

            r = requests.post(
                LAPTOP_API,
                json=payload,
                headers=API_HEADERS,
                timeout=10
            )

            if r.ok:

                try:
                    api_resp = r.json()
                    msg = api_resp.get(
                        "msg",
                        "OK"
                    )

                except:
                    msg = r.text


                await update.message.reply_text(
                    f"✅ {msg}"
                )


            else:

                await update.message.reply_text(
                    f"❌ Error API {r.status_code}"
                )


        except requests.exceptions.Timeout:

            await update.message.reply_text(
                "⏱ Timeout con la laptop"
            )


        except requests.exceptions.ConnectionError:

            await update.message.reply_text(
                "🔌 No conecta con la laptop"
            )


    except Exception as e:

        await update.message.reply_text(
            f"💥 Error:\n{e}"
        )



# ------------ MAIN ------------

if __name__ == "__main__":

    app = (
        Application
        .builder()
        .token(TOKEN_TELEGRAM)
        .build()
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            manejar_mensaje
        )
    )

    print("🚀 Escuchando..." + "usando" + iaMain)
    app.run_polling()
