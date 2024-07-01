#Requires AutoHotkey v2.0

#Warn  ; Enable warnings to assist with detecting common errors.
SendMode "Input"  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir A_ScriptDir  ; Ensures a consistent starting directory.

Home::
{
    Loop
    {
        slp := floor(Random(0.2, 0.5) * 1000)
        ControlSend "{Space down}",, "FINAL FANTASY XIV"
        Sleep slp
        ControlSend "{Space up}",, "FINAL FANTASY XIV"
        slp := floor(Random(60*10, 60*12) * 1000)
        Sleep slp
    }
    return
}


End::Reload


