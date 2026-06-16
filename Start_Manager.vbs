Option Explicit

Dim shell, fso, repoRoot, mainPath, venvPythonw
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

repoRoot = fso.GetParentFolderName(WScript.ScriptFullName)
mainPath = fso.BuildPath(repoRoot, "main.py")

If Not fso.FileExists(mainPath) Then
    MsgBox "Nie znaleziono main.py w: " & repoRoot, vbCritical, "Manager"
    WScript.Quit 1
End If

venvPythonw = fso.BuildPath(repoRoot, ".venv\Scripts\pythonw.exe")
If fso.FileExists(venvPythonw) Then
    shell.Run Quote(venvPythonw) & " " & Quote(mainPath), 0, False
    WScript.Quit 0
End If

If CommandExists("pythonw.exe") Then
    shell.Run "pythonw.exe " & Quote(mainPath), 0, False
    WScript.Quit 0
End If

If CommandExists("pyw.exe") Then
    shell.Run "pyw.exe -3 " & Quote(mainPath), 0, False
    WScript.Quit 0
End If

If CommandExists("python.exe") Then
    shell.Run "python.exe " & Quote(mainPath), 0, False
    WScript.Quit 0
End If

MsgBox "Nie znaleziono Python / pythonw / pyw." & vbCrLf & _
       "Zainstaluj Python albo uruchom aplikację komendą: python main.py", vbCritical, "Manager"
WScript.Quit 1

Function Quote(value)
    Quote = Chr(34) & value & Chr(34)
End Function

Function CommandExists(commandName)
    On Error Resume Next
    Dim exec
    Set exec = shell.Exec("cmd /c where " & commandName)
    If Err.Number <> 0 Then
        Err.Clear
        CommandExists = False
        Exit Function
    End If
    Do While exec.Status = 0
        WScript.Sleep 25
    Loop
    CommandExists = (exec.ExitCode = 0)
End Function
