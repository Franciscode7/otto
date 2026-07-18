from AppOpener import open as app_open, close as app_close

def abrir_app(nombre):
    """
    Busca y abre una aplicación por su nombre.
    Ejemplo: abrir_app("spotify")
    """
    try:
        # match_closest=True ayuda si el nombre no es exacto
        # throw_error=True nos permite capturar el fallo en el except
        app_open(nombre.lower(), match_closest=True, throw_error=True)
        print(f"[APPS] Abriendo: {nombre}")
        return True
    except Exception as e:
        print(f"[ERROR] No se encontró la app '{nombre}': {e}")
        return False
