import urllib.request
import urllib.parse
import re
import webbrowser

def buscar_youtube(nombre_video):
    try:
        print(f"[YouTube] Buscando: {nombre_video}")
        
        # Codificamos el texto para la URL (ej: "Rick+Astley...")
        query_string = urllib.parse.urlencode({"search_query": nombre_video})
        url_busqueda = f"https://www.youtube.com/results?{query_string}"
        
        # Hacemos la petición nativa imitando un navegador común
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url_busqueda, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode()
            
        # Buscamos los IDs de los videos en el HTML mediante una expresión regular rápida
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        
        if video_ids:
            # Tomamos el primer resultado que encuentre
            url_final = f"https://www.youtube.com/watch?v={video_ids[0]}"
            
            print(f"[OK] Video encontrado con éxito.")
            webbrowser.open(url_final)
            return True, "Video abierto en el navegador"
        else:
            return False, "No se encontraron resultados en el HTML."
            
    except Exception as e:
        print(f"[DEBUG ERROR] Detalle: {str(e)}")
        return False, str(e)

if __name__ == "__main__":
    buscar_youtube("sometimes de ariana grande")