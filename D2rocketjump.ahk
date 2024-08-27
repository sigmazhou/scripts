#Requires AutoHotkey v2.0


; Only run the script when Destiny 2 is the active window
#Warn
SendMode "Input"  ; Recommended for new scripts due to its superior speed and reliability.
#HotIf WinActive("ahk_exe destiny2.exe")

; Bind the sequence to the middle mouse button
Insert:: {
    ; Press right mouse button down
    Send "{RButton Down}"
    Sleep(1000) ; Wait for 1000 milliseconds

    ; Press left mouse button down
    Send("{LButton Down}")
    Sleep(0) ; Short delay to ensure the right click is registered

    ; Press and release "Q" key
    Send("q")
    Sleep(0) ; Short delay to ensure the "Q" key press is registered

    ; Press "Esc" key twice
    Send("{Esc}")
    Sleep(0) ; Short delay between the two "Esc" key presses
    Send("{Esc}")
    Sleep(0) ; Short delay to ensure the second "Esc" key press is registered

    ; Release left mouse button
    Send("{LButton Up}")
    Sleep(0) ; Short delay to ensure the left mouse button release is registered

    ; Release right mouse button
    Send("{RButton Up}")
}

End::Reload()

#HotIf