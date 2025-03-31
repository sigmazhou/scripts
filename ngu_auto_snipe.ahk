#Requires AutoHotkey v2.0
SendMode "Input"
SetDefaultMouseSpeed 0

; 获取间隔参数（单位：毫秒），默认 1000
interval := 820
interval_same_cast := 820
if A_Args.Length >= 1 {
    try interval := Integer(A_Args[1])
    catch {
        MsgBox "参数错误，使用默认间隔 1000ms"
        interval := 1000
    }
}

; 配置需要输入的序列（在此修改内容）
avsp_sequence := "fhgytrewaw edtwewwxay trsewwdetw weagyetr"
avsp_sequence_high_atk := "fhgytreaww edtwewwaxy rstewwdeta wewgyetr"

mega_sequence := "zfhgytrewa wedtwezwxa ytrsewwdet wzeagyetr"

bdw_sequence := "zfhgytrewd wewtaexwzw ytrsadwewt wzewgaytre dwwe"

sequence := bdw_sequence

atk_prio := "zfgytredaxw"
def_prio := "zfgyrdaxtew"
prio_sequence := atk_prio

; target boss color loc and rgb
color_loc_x := 1870
color_loc_y := 1252
color_rgb := 0x8e70c1

last_hit_x := 2270

; manual edit ends here
count := 0
running := false
W := 2880
H := 1800
W_base := 2880
H_base := 1800
win_title := "NGU Idle"

getwinsize


^+`::
`::Reload

End::{
    play_prio(True)
}

Down::{
    checkactive
    global running:=false

    switchdcloadout
    
    global count
    TrayTip "total inputs", count, "mute"
    Reload
}


PgDn::{
    switchadvloadout
}

PgUp::{
    msgbox hasenemy()
}

Up::{
    Loop {
        refresh_till_boss
        key_delay_fixture(2)(play_prio)()
    }
    ;if isboss() and islasthit() {
        ;switchdcloadout
        ;spam_last_hit
    ;}
    ;switchadvloadout
}

Home::{
    getwinsize
    init_wait := 105*60*1000
    loop_wait := 61*60*1000

    Sleep init_wait
    Loop {
        clkslp 1081,773,500 ;loadout2
        clkslp 995,773 ;loadout1
        Sleep loop_wait
    }
}

; main functions
refresh_till_target_boss(){
    Loop {
        Sleep 200
        if hasenemy() and istargetenemy(color_loc_x, color_loc_y, color_rgb) {
            break
        }
        if hasenemy() and !istargetenemy(color_loc_x, color_loc_y, color_rgb) {
            keyslp "{Left}"
            keyslp "{Right}"
            continue
        }
    }
}

refresh_till_boss(){
    Loop {
        Sleep 200
        if hasenemy() and isboss() {
            break
        }
        if hasenemy() and !isboss() {
            keyslp "{Left}"
            keyslp "{Right}"
            keyslp "d"
            continue
        }
    }
}


idle_boss_only(){
    ;idle boss only
    dcdigger := 0
    Loop {
        Sleep 200
        if hasenemy() and !isboss() {
            keyslp "{Left}"
            keyslp "{Right}"
            continue
        }
        if isboss() and islasthit() and !dcdigger {
            switchdcloadout
            advtab
            dcdigger := 1
            continue
        }
        if dcdigger and !isboss() {
            switchadvloadout
            advtab
            dcdigger := 0
            continue
        }
    }
}

play_sequence(){
    global 
    count := 0
    running := true
    lastkey := ""
    
    checkactive
    getwinsize
    
    Loop Parse sequence {
        if !running {
            break
        }
        if (A_LoopField == " ") {
            continue
        }
        ; 发送当前字符（使用文本模式避免特殊符号问题）
        send_key_flavored(A_LoopField)
        count += 1
        tmp_intvl := interval
        if (A_LoopField == lastkey) {
            tmp_intvl := interval_same_cast
        }
        ; last hit check
        if !hasenemy(){
            break
        }
        
        Sleep tmp_intvl
        lastkey := A_LoopField
    }
}

play_prio(inf_loop:=False) {
    global
    count := 0
    running := true
    def_buff_timer_ms := 0
    
    checkactive
    getwinsize
    
    Loop {
        if !running {
            break
        }
        ; 发送当前字符（使用文本模式避免特殊符号问题）
        tc_ms := A_TickCount
        if (tc_ms - def_buff_timer_ms > 18000) {
            send_key_prio("hs")
            def_buff_timer_ms := tc_ms
        } else {
            send_key_prio(prio_sequence)
        }
        count += 1
        ; last hit check
        if !inf_loop and !hasenemy(){
            break
        }

        Sleep interval
    }
}

send_key_prio(prio_seq) {
    ;s_delay := A_KeyDelay
    ;SetKeyDelay 2
    ControlSend prio_seq,,win_title
    ;SetKeyDelay s_delay
    ;Loop Parse prio_seq {
        ;keyslp A_LoopField, 10
    ;}
}

send_key_flavored(key) {
    if (key == "s"){
        keyslp "s", 20
        Send "h"
        return
    }
    if (key == "h") {
        keyslp "h", 20
        Send "s"
        return
    }
    keyslp key, 20
    Send "w"
}

spam_last_hit() {
    while isboss() {
        Send "t"
        Send "e"
        Send "w"
        Sleep 100
    }
}

; fixture
key_delay_fixture(delay, press_duration := -1) {
    ; 返回装饰器函数
    wrapper(func) {
        inner(params*) {
            original_delay := A_KeyDelay
            original_duration := A_KeyDuration

            SetKeyDelay delay, press_duration
            try {
                return func(params*)
            } finally {
                ; 恢复原始设置
                SetKeyDelay original_delay, original_duration
            }
        }
        return inner
    }
    return wrapper
}

; utils
clkslp(x,y,ms:=100,key:="Left",translate_coord_to_rel:=true){
    if translate_coord_to_rel {
        x := x*W/W_base
        y := y*W/W_base
    }
    Click x,y,key
    Sleep ms
}

keyslp(keyseq,ms:=100){
    send keyseq
    Sleep ms
}

dragslp(x1,y1,x2,y2,ms:=100,key:="Left",translate_coord_to_rel:=true){
    if translate_coord_to_rel {
        x1 := x1*W/W_base
        y1 := y1*W/W_base
        x2 := x2*W/W_base
        y2 := y2*W/W_base
    }
    MouseClickDrag key, x1, y1, x2, y2
    Sleep ms
}


getwinsize(){
    global W,H
    if WinExist("NGU Idle")
    {
        WinGetClientPos ,, &W, &H, "NGU Idle"
    }
}

checkactive(){
    if not winActive("NGU Idle")
    {
        TrayTip "win inactive",, "mute"
        reload
        return
    }
}

isboss(){
    c := PixelGetColor(2228*W/W_base,846*W/W_base,"RGB")
    if (c = 0xf7ef29) {
        return True
    }
    return False
}

istargetenemy(x, y, color){
    c := PixelGetColor(x*W/W_base,y*W/W_base,"RGB")
    if (c = color) {
        return True
    }
    return False
}

hasenemy(){
    c1 := PixelGetColor(2193*W/W_base,935*W/W_base,"RGB")   ;000000 ->Power
    if (c1 = 0x000000) {
        return True
    }
    return False
}

islasthit(){
    c := PixelGetColor(last_hit_x*W/W_base,1249*W/W_base,"RGB")
    if (c = 0xb0afb0) {
        return True
    }
    return False
}

isparalyzed(){
    c := PixelGetColor(1428*W/W_base,293*W/W_base,"RGB")
    if (c = 0xf89b9b) {
        return False
    }
    return True
}

switchadvdigger(){
    clkslp 706,1039
    clkslp 1019,711
    clkslp 1971,1283
}

switchdcdigger(){
    clkslp 706,1039
    clkslp 1971,1283
    clkslp 1019,711
}

switchdcloadout() {
    ; digger
    ; switchdcdigger
    ; inventory
    clkslp 720,394
    ;clkslp 1047,991,,"Right"
    ;dragslp 1195,990,1427,340
    clkslp 1081,773 ;loadout2
    ; adventure
    clkslp 720,313
}

switchadvloadout() {
    ;clkslp 2203,631 ;left
    ;digger
    ;switchadvdigger
    ;inventory
    clkslp 720,394
    ;clkslp 1047,991,,"Right"
    ;dragslp 1195,990,1427,340
    clkslp 995,773 ;loadout1
    ;adventure
    clkslp 720,313
}

advtab(){
    clkslp 720,313
}


HideTrayTip() {
    TrayTip  ; Attempt to hide it the normal way.
    if SubStr(A_OSVersion,1,3) = "10." {
        A_IconHidden := true
        Sleep 200  ; It may be necessary to adjust this sleep.
        A_IconHidden := false
    }
}

