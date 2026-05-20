Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "E:\AIBuilder\Manager"
WshShell.Run "pythonw.exe main.py", 0, False