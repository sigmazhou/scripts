#include "./libxin.ahk"

clickHistory := [[0,0], [0,0], [0,0]]

RButton::{
    saveClickSetupHelper()
}

saveClickSetupHelper(){
    global clickHistory
    MouseGetPos &xpos, &ypos 
    clickHistory.RemoveAt(1,1)
    clickHistory.Push([xpos,ypos])
    A_Clipboard := ArrJoin(clickHistory[1]) . ", {minp: " . ArrJoin(clickHistory[2]) . ", maxp: " . ArrJoin(clickHistory[3]) . "}"
}