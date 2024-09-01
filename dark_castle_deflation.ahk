#Requires AutoHotkey v2.0

#Warn  ; Enable warnings to assist with detecting common errors.
SendMode "Input"  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir A_ScriptDir  ; Ensures a consistent starting directory.

; make sure have auto next round on
Home::
{
SetTimer steampaymentprotection, 1000
loop{
    startmap
    placeboatsv2
    placeboatsexp
    startgame
    
    SetTimer detectlvlupscreen, 6000
    slprand 5.6*60*1000
    SetTimer detectlvlupscreen, 0
    slprand random(0,10*1000)
    endround
    detecttotemeventscreen
    slprand random(0,10*1000)
    }
}

PgUp::
{
steampaymentprotection
}

PgDn::
{
MouseGetPos &xpos, &ypos 
MsgBox "The cursor is at X" xpos " Y" ypos " color" PixelGetColor(xpos,ypos)
}

test(){
Msgbox 1
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
        clkslp x,657,200
    loop s2
        clkslp x,864,200
    loop s3
        clkslp x,1040,200
}

startgame(){
    clkslp 2450, 1360
    clkslp 2450, 1360
}


placeboats(){
    ;5.7*60*1000
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
}



placeboatsv2(){
    ;5.6*60*1000, possibly 5.5
    loop 14
        wheeldownslp
    yoff:=Random(-5,0)
    clkslp 2450, 960
    clkslp 1310, 577,,0,yoff    ;village
    
    clkslp 1310, 577
    lvlup 0,0,2     ;vlg

    clkslp 2281, 632
    clkslp 1075, 598,,0,yoff     ;ninja
    clkslp 2281, 456
    clkslp 1171, 597,,0,yoff     ;wizard
    clkslp 2437, 636
    clkslp 1074, 520,,0,yoff     ;alchem

    clkslp 1171, 597
    lvlup 0,3,2     ;wizard
    clkslp 1075, 598
    lvlup 4,0,2     ;ninja
    clkslp 1074, 520
    lvlup 4,0,0     ;alchem
    
    clkslp 1310, 577
    clkslp 450, 1211    ;sell village
}


placeboatsexp(){
    yoff:=Random(0,5)
    clkslp 2281, 992
    clkslp 1337, 901,,0,yoff     ;spike
    loop 14
        wheelupslp
    clkslp 2437, 308
    clkslp 1222, 886,,0,yoff     ;dart
    clkslp 2281, 481
    clkslp 1125, 891,,0,yoff     ;boomerang
    clkslp 2281, 1021
    clkslp 1452, 923,,0,yoff     ;submarine
    
    clkslp 1337, 901    ;spike
    lvlup 2,0,0
    clkslp 1222, 886    ;dart
    lvlup 0,0,4
    clkslp 1125, 891    ;boomerang
    lvlup 0,0,3
    clkslp 1452, 923    ;submarine
    lvlup 2,0,1
}


endround(){
    clkslp 1270, 1200
    clkslp 957, 1140
    slprand 2000
}


detectlvlupscreen(){
    if PixelSearch(&posx,&posy,1240,600,1320,667,0xffffff,1)
    {
        clkslp 1280, 120, 1000
        clkslp 1280, 120, 1000
    }
}


detecttotemeventscreen(){
    if PixelSearch(&posx,&posy,1275,775,1285,785,0x00a1ff,0)
    {
        clkslp 1280, 900, 2000
        clkslp 1085, 720, 1000
        clkslp 1085, 720, 1000
        clkslp 1480, 720, 1000
        clkslp 1480, 720, 1000
        clkslp 1284, 1337, 2000
        send "{Esc}"
        slprand 1000
    }
}

steampaymentprotection(){
    if ImageSearch(&x, &y, 1685,300,1954,400, "./steam_icon_in_game_overlay_2560_1440.png")
    {
        Msgbox "Payment detected"
        Reload
    }
}


^+`::
End::Reload
