from datetime import datetime, date
from pywinauto import Application, Desktop
import pyautogui
import time

def escribir_nota(texto):
    
    # Fecha y hora actual
    fecha = datetime.now()
    
    # Formato: Día/Mes/Año Hora:Minuto
    formato = fecha.strftime("%d/%m/%Y %H:%M")
    print("Fecha formateada:", formato)
        
    print(f"{formato} - {texto}")
     
    try:
        # 1. Abrimos el Bloc de notas
        ruta_nota = r"C:\Users\franc\OneDrive\Escritorio\notas.txt"

        # Pasamos la cadena completa de ejecución
        app = Application(backend="win32").start(cmd_line=f'notepad.exe "{ruta_nota}"')
        
        # app = Application(backend="win32").start("notepad.exe")
        
        # 2. Buscamos la ventana (en Windows 11 a veces el título cambia, usamos class_name)
        # Esperamos a que la ventana esté lista
        
        ventana = Desktop(backend="uia").window(class_name="Notepad", found_index=0)
        
        # 3. Enfocamos la ventana para que reciba las teclas
        time.sleep(1)
        
        ventana.set_focus()
        
        # 4. Escribimos el texto
        # with_spaces=True permite que los espacios se envíen correctamente
        # Añade un salto de línea al final del string 
        time.sleep(1)
        
        ventana.type_keys(formato + " - " + texto + "{ENTER}", with_spaces=True, pause=0.05)
        
        time.sleep(0.5)
         
        ventana.type_keys('^g')    

        time.sleep(1)
        # Escribimos el nombre y enviamos el ENTER
        pyautogui.press('enter')
        
        print(f"[NOTEPAD] Texto escrito: {formato} - {texto}")
        return True
    except Exception as e:
        print(f"[ERROR NOTEPAD] {e}")
        return False