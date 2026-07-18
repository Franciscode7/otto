import psutil
from AppOpener import close as app_close

def cerrar_app(nombre):
    nombre = nombre.lower()
    try:
        # PLAN A: Intentar cierre limpio con AppOpener
        app_close(nombre, match_closest=True, throw_error=True)
        print(f"[APPS] Cerrado limpio: {nombre}")
        return True
    except:
        # PLAN B: Cierre forzado buscando en los procesos del sistema
        print(f"[APPS] AppOpener falló, intentando cierre forzado para: {nombre}")
        encontrado = False
        for proc in psutil.process_iter(['name']):
            try:
                # Comprobamos si el nombre de la app está en el nombre del proceso
                # Ej: si buscas "excel", encontrará "EXCEL.EXE"
                if nombre in proc.info['name'].lower():
                    proc.kill()
                    encontrado = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if encontrado:
            print(f"[APPS] Proceso {nombre} terminado por la fuerza.")
            return True
        else:
            print(f"[ERROR] No se encontró ningún proceso con el nombre: {nombre}")
            return False