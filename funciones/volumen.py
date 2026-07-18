import os

def ajustar_volumen(valor):
    # Ajustar volumen con PowerShell (requiere módulo AudioDeviceCmdlets)
    cmd = f"powershell Set-AudioDevice -PlaybackVolume {valor}"
    os.system(cmd)