#include "../Lib/libxin.ahk"
SendMode "Input"

init(){
    global
    W := GetWinSize("少女前线")[1]
    H := GetWinSize("少女前线")[2]
    ch := InputScheduler(W,H,2560,1440)
    ch.sc("restartfight", [803, 1250],{minp:[656, 1217], maxp:[944, 1277], t:1200, simpleTimeOffset:400})   ; x4
    ch.sc("restartfightandwait", [803, 1250],{minp:[656, 1217], maxp:[944, 1277], t:4000, simpleTimeOffset:500})   ; x4
    ch.sc("party1", [1539, 427], {minp: [1490, 389], maxp: [1576, 466], t:1200, simpleTimeOffset: 400})
    ch.sc("changepartyformation", [500, 1258], {minp: [325, 1218], maxp: [696, 1294], t:2500, simpleTimeOffset: 400})
    ch.sc("partymember1", [481, 707], {minp: [326, 285], maxp: [634, 1109], t:1200, simpleTimeOffset: 400})
    ch.sc("filterby", [2347, 541], {minp: [2205, 472], maxp: [2515, 640], t:1200, simpleTimeOffset: 400})
    ch.sc("starred", [1939, 265], {minp: [1775, 239], maxp: [2100, 285], t:1200, simpleTimeOffset: 400})
    ch.sc("stock1", [216, 499], {minp: [78, 260], maxp: [348, 764], t:900, simpleTimeOffset: 300})
    ch.sc("stock2", [564, 504], {minp: [428, 254], maxp: [696, 760], t:900, simpleTimeOffset: 300})
    ch.sc("confirmpartyformation", [2355, 1314], {minp: [2203, 1233], maxp: [2528, 1398], t:2000, simpleTimeOffset: 500})
    ch.sc("backtofight", [189, 105], {minp: [22, 36], maxp: [340, 182], t:4000, simpleTimeOffset: 500})
    ch.sc("startfight", [2255, 1324], {minp: [1999, 1219], maxp: [2531, 1414], t:4000, simpleTimeOffset: 500})
    ch.sc("party2", [309, 608], {minp: [266, 574], maxp: [350, 651], t:1200, simpleTimeOffset: 400}) ;x2
    ch.sc("fillammo", [2349, 1126], {minp: [2171, 1068], maxp: [2546, 1176], t:1200, simpleTimeOffset: 400})
    ch.sc("planmode", [162, 1262], {minp: [6, 1229], maxp: [308, 1293], t:1200, simpleTimeOffset: 400})
    ch.sc("deselect1", [542, 1273], {minp: [482, 1244], maxp: [651, 1346], t:1200, simpleTimeOffset: 400})
    ch.sc("waypoint1", [1357, 615], {minp: [1314, 569], maxp: [1395, 655], t:900, simpleTimeOffset: 300})
    ch.sc("waypoint2", [1539, 973], {minp: [1495, 935], maxp: [1579, 1012], t:900, simpleTimeOffset: 300})
    ch.sc("waypoint3v1", [1536, 1154], {minp: [1494, 1113], maxp: [1579, 1195], t:900, simpleTimeOffset: 300})
    ch.sc("waypoint3v2", [1539, 788], {minp: [1493, 754], maxp: [1579, 834], t:900, simpleTimeOffset: 300})
    ch.sc("executeplan", [2356, 1331], {minp: [2202, 1249], maxp: [2523, 1408]})
}

init()

OneRound(){
    global ch
    plan := ["restartfight", "restartfight", "restartfight", "restartfightandwait", "party1", "changepartyformation", "partymember1", 
        "filterby", "starred", "stock1", "stock1", "stock2", "stock1", "confirmpartyformation", "backtofight", "startfight",
        "party2","party2", "fillammo", "planmode", "deselect1","party1", "waypoint1","waypoint2", ["waypoint3v1", "waypoint3v2"], "executeplan"]
    ch.ExecutePlan(plan)
}

PgUp::{
    OneRound()
    ;Click 224,480, "LButton"
    ;SendInput "{Click 224 480}"
}
`::Reload

