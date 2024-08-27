#Requires AutoHotkey v2.0

#Warn  ; Enable warnings to assist with detecting common errors.
SendMode "Input"  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir A_ScriptDir  ; Ensures a consistent starting directory.

Home::
{
loop{
    startmap
    placeboats

    slprand 5.6*60*1000
    endround
    }
}

PgUp::
{   
    Msgbox 5.6*60*1000
}

PgDn::
{
MouseGetPos &xpos, &ypos 
MsgBox "The cursor is at X" xpos " Y" ypos
}

clkrand(x,y,btn:="Left", xoff?, yoff?)
{
    if !isset(xoff)
        xoff := Random(-20,20)
    if !isset(yoff)
        yoff := Random(-20,20)
    Click x+xoff, y+yoff, btn
}

slprand(ms){
    off := Random(-20,20)
    Sleep ms+off
}

clkslp(x,y,ms:=500, xoff?, yoff?){
    clkrand(x,y,,xoff?, yoff?)
    slprand ms
}


wheeldownslp(x:=2400,y:=800,ms:=100){
    clkrand x,y,"WD"
    slprand ms
}

wheelupslp(x:=2400,y:=800,ms:=100){
    clkrand x,y,"WU"
    slprand ms
}

startmap(){
    clkslp 1100, 1300
    clkslp 1800, 1300
    clkslp 1800, 1300
    clkslp 800, 800
    clkslp 800, 660
    clkslp 1700, 600
    
    ; skip rule intro
    slprand 3000
    clkrand 1240, 1000
    slprand 1200
}

lvlup(s1:=0, s2:=0, s3:=0, lr:="L"){
    if lr="L"
        x:=450
    else
        x:=2070
    loop s1
        clkslp x,657
    loop s2
        clkslp x,864
    loop s3
        clkslp x,1040
}


placeboats(){
    loop 14
        wheeldownslp
    yoff:=Random(-5,0)
    clkslp 2450, 960
    clkslp 1316, 576,,0,yoff    ;village
    
    clkslp 1316, 576
    lvlup 0,2,2     ;vlg

    loop 5
        wheelupslp
    clkslp 2437, 332
    clkslp 1458, 573,,0,yoff     ;boat1
    clkslp 2437, 332
    clkslp 1575, 571,,0,yoff     ;boat2
    clkslp 2437, 332
    clkslp 1455, 471,,0,yoff     ;boat3

    clkslp 1458, 573
    lvlup 4,2,0     ;bt1
    clkslp 1575, 571
    lvlup 3,2,0     ;bt2
    clkslp 1455, 471
    lvlup 1,3,0     ;bt3
    
    clkslp 2450, 1360
    clkslp 2450, 1360
}


endround(){
    clkslp 1270, 1200
    clkslp 957, 1140
    slprand 2000
}

^+`::
End::Reload
