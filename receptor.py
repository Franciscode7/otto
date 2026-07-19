from flask import Flask, request, jsonify
import os
import subprocess
import datetime
import time
from dotenv import load_dotenv
from funciones import *

load_dotenv()  # Cargar variables de entorno desde el archivo .env

app = Flask(__name__)

with open("bot.log", "a") as f:
    f.write(f"Bot iniciado: {datetime.datetime.now()}\n")


# Contraseña simple para seguridad
API_KEY = os.getenv("HEADER_KEY")  # Cámbiala por algo más seguro en producción

@app.route('/orden', methods=['POST'])
def recibir_orden():
    # Validar seguridad
    auth = request.headers.get("X-API-KEY")
    if auth != API_KEY:
        return jsonify({"status": "error", "msg": "No autorizado"}), 401

    data = request.json
    accion = data.get("accion")
    valor = data.get("valor")  # Puede ser URL, ruta, número, etc.

    print(f"Comando recibido del servidor: {accion} -> {valor}")
    
    if accion == "abrir_url":
        if valor: # Verificamos que el usuario envió una URL
            exito = abrir_enlace(valor)
            if exito:
                return jsonify({"status": "ok", "msg": f"Abriendo {valor}"}), 200
            else:
                return jsonify({"status": "error", "msg": "No se pudo abrir el navegador"}), 500
        else:
            return jsonify({"status": "error", "msg": "Falta el valor (URL)"}), 400

    elif accion == "youtube":
        if valor:
            exito, detalle = buscar_youtube(valor)
            if exito:
                return jsonify({"status": "ok", "msg": f"Reproduciendo: {detalle}"}), 200
            else:
                return jsonify({"status": "error", "msg": detalle}), 404
        else:
            return jsonify({"status": "error", "msg": "Falta el nombre del video"}), 400

    
    elif accion == "brillo":
        if valor: 
            exito = ajustar_brillo(valor)
            if exito:
                return jsonify({"status": "ok", "msg": f"Brillo al {valor}%"}), 200
            else:
                return jsonify({"status": "error", "msg": f"No se pudo ajustar el brillo al {valor}%"}), 500
        else:
            return jsonify({"status": "error", "msg": "Valor incorrecto"}), 400

    if accion == "volumen":
        if valor: # Verificamos que el usuario envió una URL
            exito = ajustar_volumen(valor)
            # if exito:
            return jsonify({"status": "ok", "msg": f"Volumen al {valor}%"}), 200
            # else:
            #     return jsonify({"status": "error", "msg": "No se pudo ajustar el volumen"}), 500
        else:
            return jsonify({"status": "error", "msg": "Falta el valor (URL)"}), 400


    elif accion == "nota":
        if valor: # Verificamos que el usuario envió una URL
            exito = escribir_nota(valor)
            if exito:
                time.sleep(1) 
                cerrar_app("Notepad") # Esperamos un segundo antes de responder
                return jsonify({"status": "ok", "msg": f"Nota escrita: {valor}"}), 200
            else:
                return jsonify({"status": "error", "msg": "No se pudo escribir la nota"}), 500
        else:
            return jsonify({"status": "error", "msg": "Falta el valor (URL)"}), 400


    elif accion == "abrir_app":
        if valor: # Verificamos que el usuario envió una URL
            exito = abrir_app(valor)
            if exito:
                return jsonify({"status": "ok", "msg": f"App abierta: {valor}"}), 200
            else:
                return jsonify({"status": "error", "msg": "No se pudo abrir la app"}), 500
        else:
            return jsonify({"status": "error", "msg": "Falta el valor (URL)"}), 400
        
        
    elif accion == "cerrar_app":
        if valor: # Verificamos que el usuario envió una URL
            exito = cerrar_app(valor)
            if exito:
                return jsonify({"status": "ok", "msg": f"App cerrada: {valor}"}), 200
            else:
                return jsonify({"status": "error", "msg": "No se pudo cerrar la app"}), 500
        else:
            return jsonify({"status": "error", "msg": "Falta el valor (URL)"}), 400

if __name__ == '__main__':
    # Ejecuta la terminal como ADMINISTRADOR para que te deje usar el puerto 7777
    app.run(host=os.getenv('HOST'), port=7777)
