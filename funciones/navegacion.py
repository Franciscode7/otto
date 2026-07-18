import webbrowser

def abrir_enlace(url):
    """
    Intenta abrir una URL en el navegador predeterminado del sistema.
    """
    try:
        # Verificamos si la URL empieza con http, si no, se lo agregamos
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        # webbrowser.open devuelve True si se lanzó con éxito
        exito = webbrowser.open(url)
        
        if exito:
            print(f"[OK] Navegador abierto en: {url}")
            return True
        else:
            print(f"[ERROR] No se pudo abrir el navegador.")
            return False
            
    except Exception as e:
        print(f"[EXCEPCIÓN] Error en navegador.py: {e}")
        return False