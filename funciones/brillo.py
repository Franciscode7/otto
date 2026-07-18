import screen_brightness_control as sbc

def ajustar_brillo(nivel):
    try:
        # 1. Limpiamos el valor por si llega con espacios o formato extraño
        nivel_limpio = int(float(str(nivel).strip())) 
        
        # 2. Intentamos cambiar el brillo
        sbc.set_brightness(nivel_limpio)
        return True
    except Exception as e:
        # ¡ESTO ES LO IMPORTANTE! 
        # Escribe el error real en un archivo de texto para que puedas leerlo
        with open(r"C:\agenteserver\error_brillo.txt", "a") as f:
            f.write(f"Error con valor {nivel}: {str(e)}\n")
        return False