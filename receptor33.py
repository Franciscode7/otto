from flask import Flask, request, jsonify
import os
import subprocess
import datetime

app = Flask(__name__)

with open("bot.log", "a") as f:
    f.write(f"Bot iniciado: {datetime.datetime.now()}\n")


# Contraseña simple para seguridad
API_KEY = "fran123"  # Cámbiala por algo más seguro en producción

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

    if accion == "abrir" or accion == "abrir_url":
        os.system(f"start {valor}")
        return jsonify({"status": "ok", "msg": f"Abriendo {valor}"}), 200

    elif accion == "brillo":
        # Ajustar brillo con PowerShell
        cmd = f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{valor})"
        os.system(cmd)
        return jsonify({"status": "ok", "msg": f"Brillo al {valor}%"})

    elif accion == "volumen":
        # Ajustar volumen con PowerShell (requiere módulo AudioDeviceCmdlets)
        cmd = f"powershell Set-AudioDevice -PlaybackVolume {valor}"
        os.system(cmd)
        return jsonify({"status": "ok", "msg": f"Volumen al {valor}%"})

    elif accion == "ejecutar":
        # Ejecuta cualquier programa (ej: 'notepad', 'calc', 'code')
        subprocess.Popen(valor, shell=True)
        return jsonify({"status": "ok", "msg": f"Lanzando {valor}"})

    return jsonify({"status": "error", "msg": "Acción desconocida"}), 400

if __name__ == '__main__':
    # Ejecuta la terminal como ADMINISTRADOR para que te deje usar el puerto 7777
    app.run(host='0.0.0.0', port=7777)
