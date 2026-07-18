Set WinScriptHost = CreateObject("WScript.Shell")
' El 1 al final permite que los procesos hijos abran ventanas
WinScriptHost.Run Chr(34) & "C:\agenteserver\start_bot.bat" & Chr(34), 1
Set WinScriptHost = Nothing