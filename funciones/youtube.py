from youtubesearchpython import Search
import webbrowser

def buscar_youtube(nombre_video):
    try:
        print(f"[YouTube] Buscando: {nombre_video}")
        
        # Usamos la clase Search genérica que es más robusta
        busqueda = Search(nombre_video, limit = 1)
        resultado = busqueda.result()

        if resultado and 'result' in resultado and len(resultado['result']) > 0:
            video_data = resultado['result'][0]
            url_final = video_data['link']
            titulo = video_data['title']
            
            print(f"[OK] Encontrado: {titulo}")
            webbrowser.open(url_final)
            return True, titulo
        else:
            return False, "No se encontraron resultados."
            
    except Exception as e:
        # Imprime el error completo para saber si es otra cosa
        print(f"[DEBUG ERROR] Detalle: {str(e)}")
        return False, str(e)