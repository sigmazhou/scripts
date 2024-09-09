#Requires AutoHotkey v2.0

#Warn  ; Enable warnings to assist with detecting common errors.
SendMode "Input"  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir A_ScriptDir  ; Ensures a consistent starting directory.

W:=2560
H:=1440
default_click_off:=20
default_sleep_off:=20
getwinsize


; make sure have auto next round on
Home::
{
getwinsize
SetTimer steampaymentprotection, 1000
loop{
    startmap
    placeboatsv2 false
    ;placeboatsexp
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
    getwinsize
    detecttotemeventscreen
}

PgDn::
{
getwinsize
MouseGetPos &xpos, &ypos 
MsgBox "The cursor is at X " xpos " Y " ypos "`nrelpos X " Format("{1:0.4f}", xpos/W) " Y " Format("{1:0.4f}", ypos/H) "`ncolor " PixelGetColor(xpos,ypos)
}

test(){
Msgbox 1
}

getwinsize(){
    global W,H,default_click_off
    if WinExist("BloonsTD6")
    {
        WinGetClientPos ,, &W, &H, "BloonsTD6"
        default_click_off:=min(20, W/128)
    }
}

clkrand(x,y,btn:="Left", xoff?, yoff?)
{
    if x>W or y>H or x<0 or y<0
    {
        Msgbox "click pos oob"
        reload
        return
    }
    if not winActive("BloonsTD6")
    {
        Msgbox "win inactive"
        reload
        return
    }
    if x<=1
        x:=x*W
    if y<=1
        y:=y*H
    if !isset(xoff)
        xoff := Random(-default_click_off,default_click_off)
    if !isset(yoff)
        yoff := Random(-default_click_off,default_click_off)
    Click x+xoff, y+yoff, btn
}

slprand(ms){
    off := Random(-default_sleep_off,default_sleep_off)
    Sleep ms+off
}

clkslp(x,y,ms:=500, xoff?, yoff?){
    clkrand(x,y,,xoff?, yoff?)
    slprand ms
}

keyslp(keyseq,ms:=500){
    send keyseq
    slprand ms
}


wheeldownslp(x:=0.92,y:=0.5,ms:=100){
    clkrand x,y,"WD"
    slprand ms
}

wheelupslp(x:=0.92,y:=0.5,ms:=100){
    clkrand x,y,"WU"
    slprand ms
}

startmap(){
    clkslp 0.43, 0.87
    clkslp 0.7, 0.9
    clkslp 0.7, 0.9
    clkslp 0.28, 0.53
    clkslp 0.33, 0.44
    clkslp 0.67, 0.43
    
    ; skip rule intro
    slprand 3500
    clkrand 0.5, 0.7
    slprand 1200
}

lvlup(s1:=0, s2:=0, s3:=0, lr:="L"){
    if lr="L"
        x:=0.17
    else
        x:=0.81
    loop s1
        clkslp x,0.45,200
    loop s2
        clkslp x,0.59,200
    loop s3
        clkslp x,0.73,200
}

startgame(){
    keyslp "{Space}"
    keyslp "{Space}"
}


placeboats(){
    ;unmigrated
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

placeboatsv2(sellvillage:=true){
    ;5.6*60*1000, possibly 5.5
    loop 14
        wheeldownslp
    yoff:=Random(-default_click_off/4,0)
    clkslp 0.95, 0.69
    clkslp 0.512, 0.4,,0,yoff    ;village
    
    clkslp 0.512, 0.4
    lvlup 0,0,2     ;vlg

    clkslp 0.89, 0.44
    clkslp 0.42, 0.415,,0,yoff     ;ninja
    clkslp 0.89, 0.32
    clkslp 0.458, 0.414,,0,yoff     ;wizard
    clkslp 0.95, 0.44
    clkslp 0.42, 0.36,,0,yoff     ;alchem

    clkslp 0.458, 0.414
    lvlup 0,3,2     ;wizard
    clkslp 0.42, 0.415
    lvlup 4,0,2     ;ninja
    clkslp 0.42, 0.36
    lvlup 4,0,0     ;alchem
    
    if sellvillage{
        clkslp 0.512, 0.4
        keyslp "{Backspace}"
    }
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

placeboatsexpv2(){
    yoff:=Random(0,5)
    clkslp 2446, 1166
    clkslp 1332, 900,,0,yoff     ;bm
    clkslp 2278, 1166
    clkslp 1215, 900,,0,yoff     ;eng
    clkslp 2290, 280
    clkslp 1050, 934,,0,yoff     ;mortar
    loop 14
        wheelupslp
    clkslp 2437, 481
    clkslp 1329, 1000,,0,yoff     ;pao
    
    clkslp 1332, 900    ;bm
    lvlup 0,2,3
    clkslp 1215, 900    ;eng
    lvlup 3,0,2
    clkslp 1050, 934    ;mortar
    lvlup 0,0,2
    clkslp 1329, 1000    ;pao
    lvlup 0,0,2
}


endround(){
    clkslp 0.5, 0.84, 1000
    clkslp 0.375, 0.79, 2000
}


detectlvlupscreen(){
    if PixelSearch(&posx,&posy,0.484*W,0.416*H,0.516*W,0.464*H,0xffffff,1)  ; 1240,600,1320,667
    {
        clkslp 0.5, 0.1, 1000
        clkslp 0.5, 0.1, 1000
    }
}


detecttotemeventscreen(){
    if PixelSearch(&posx,&posy,0.498*W,0.538*H,0.502*W,0.546*H,0x00a1ff,1)  ; 1275,775,1285,785     0.498*W,0.538*H,0.502*W,0.544*H,0x00a2ff
    {
        clkslp 0.5, 0.627, 2000

        ; 2 crates
        clkslp 0.425, 0.5, 1000
        clkslp 0.425, 0.5, 1000
        clkslp 0.575, 0.5, 1000
        clkslp 0.575, 0.5, 1000
        ; 3 crates
        clkslp 0.345, 0.5, 1000
        clkslp 0.345, 0.5, 1000
        clkslp 0.5, 0.5, 1000
        clkslp 0.5, 0.5, 1000
        clkslp 0.655, 0.5, 1000
        clkslp 0.655, 0.5, 1000

        clkslp 0.5, 0.927, 1500
        keyslp "{Esc}", 1000
    }
}

steampaymentprotection(){
    if ImageSearch(&x, &y, 0.6*W,0.2*H,0.85*W,0.45*H, "*48 ./steam_icon_in_game_overlay_3840_2160.png") 
        or ImageSearch(&x, &y, 0.6*W,0.2*H,0.85*W,0.45*H, "*48 ./steam_icon_in_game_overlay_2560_1440.png")
    {
        Msgbox "Payment detected"
        Reload
    }
}


^+`::
End::Reload
