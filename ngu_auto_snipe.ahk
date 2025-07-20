#Requires AutoHotkey v2.0
SendMode "Input"
#Warn All, Off
SetDefaultMouseSpeed 0

; 获取间隔参数（单位：毫秒），默认 1000
interval := 850
interval_same_cast := 850
if A_Args.Length >= 1 {
    try interval := Integer(A_Args[1])
    catch {
        MsgBox "参数错误，使用默认间隔 1000ms"
        interval := 1000
    }
}

respawn := 1240 ; 1410 ;1240

; 配置需要输入的序列（在此修改内容）
avsp_sequence := "fhgytrewaw edtwewwxay trsewwdetw weagyetr"
avsp_sequence_high_atk := "fhgytreaww edtwewwaxy rstewwdeta wewgyetr"

mega_sequence := "zfhgytrewa wedtwezwxa ytrsewwdet wzeagyetr"

bdw_sequence := "zfhgytrewd wewtaexwzw ytrsadwewt wzewgaytre dwwe"

;e 4
;r 14
;t 8
;y 14
;a 9
;sfh 41
;d 14
;g 27 
;z 14
;x 32
t6v1_sequence := "wfhyztewwre awtdegyzew tsreaxwetd wyzewwatew r"
t8v1_sequence := "fhytaewzret w.2egaydxezt .2eaw.2ecsyrda twz.4we.2www.3fh teacrdzgyt"
t8v1_sequence_v2 := "fhytaewzret w.2egaydxezt .2eaw.2ecsyrdt wae.4wz.2w.2fhte acrdzgyt"

sequence := t8v1_sequence_v2

atk_prio_farm := "zfgyterdw"
atk_prio := "zfgytredaxw"
balanced_prio := "zfgytrdaexw"
def_prio := "zfgyrdaxtew"
prio_sequence := atk_prio_farm

def_buff_gap_ms := 19000

; target boss color loc and rgb
color_loc_x := 1870
color_loc_y := 1252
color_rgb := 0x8e70c1

last_hit_percentile := 0.25

; manual edit ends here
count := 0
running := false
W := 2880
H := 1800
W_base := 2880
H_base := 1800
win_title := "NGU Idle"
def_buff_timer_ms := 0

hp_bar_left := 2203
hp_bar_right := 2800
last_hit_x := 2203 * (1-last_hit_percentile) + 2800 * last_hit_percentile

getwinsize


^+`::
`::Reload

End::{
    Send "{Right}"
    Sleep 300
    play_sequence
}

Down::{
    checkactive
    global running:=false
    
    ;switchdcdigger
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
    auto_regular
}

Insert::{
    dc_last_hit := False
    patched_play_prio := key_delay_fixture(2)(play_prio)
    Loop {
        ;wait_till_spawn
        refresh_till_boss
        if dc_last_hit {
            patched_play_prio(,True)
            switchdcloadout
            spam_last_hit
            switchadvloadout
        } else {
            patched_play_prio(,False)
        }
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
            keyslp "{Left}", 50
            keyslp "{Right}", 50
            send_key_prio("rdx")
            continue
        }
    }
}


wait_till_spawn(){
    Loop {
        Sleep 200
        if hasenemy(){
            break
        }
        send_key_prio("rdx")
    }
}


idle_boss_only(switch_dc:=False){
    ;idle boss only
    dcdigger := 0
    Loop {
        Sleep 200
        if hasenemy() and !isboss() {
            keyslp "{Left}", 50
            keyslp "{Right}", 50
            keyslp "q", 20
            keyslp "d", 20
            keyslp "q", 20
            continue
        }
        if switch_dc and isboss() and islasthit() and !dcdigger {
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
    
    is_latency_input := false
    
    checkactive
    getwinsize
    
    Loop Parse sequence {
        if !running {
            break
        }
        if (A_LoopField == " ") {
            continue
        }
        if (A_LoopField == ".") {
            is_latency_input := true
            continue
        }
        if (is_latency_input) {
            is_latency_input := false
            Sleep A_LoopField*100
            continue
        }
        ; 发送当前字符（使用文本模式避免特殊符号问题）
        Send A_LoopField
        count += 1
        tmp_intvl := interval
        if (A_LoopField == lastkey) {
            tmp_intvl := interval_same_cast
        }
        ; last hit check
        ;if !hasenemy(){
        ;    return
        ;}
        
        Sleep tmp_intvl
        lastkey := A_LoopField
    }
}

play_prio(inf_loop:=False, save_last_hit:=False) {
    global
    count := 0
    running := true
    
    checkactive
    getwinsize
    
    Loop {
        if !running {
            break
        }
        ; 发送当前字符（使用文本模式避免特殊符号问题）
        tc_ms := A_TickCount
        if (tc_ms - def_buff_timer_ms > def_buff_gap_ms) {
            send_key_prio("hhs")
            def_buff_timer_ms := tc_ms
        } else {
            send_key_prio(prio_sequence)
        }
        count += 1
        
        Sleep 50
        interval_remaining := interval-50
        ; last hit check
        if !inf_loop and ((!save_last_hit and !hasenemy()) or (save_last_hit and islasthit())){
            return
        }

        Sleep interval_remaining
    }
}

auto_regular() {
    global
    running := true

    checkactive
    getwinsize
    
    Loop {
        if !running {
            break
        }
        keyslp "w", respawn
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
    while hasenemy() {
        send_key_prio("tew")
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
    c1 := PixelGetColor(2193*W/W_base,1075*W/W_base,"RGB")   ;000000 ->Max HP/HP Regen
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

