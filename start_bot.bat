@echo off
cd /d "C:\agenteserver"
:: Activamos el entorno virtual
call venv\Scripts\activate
:: Lanzamos el receptor y guardamos todo en el log
python receptor.py >> receptor_errors.log 2>&1