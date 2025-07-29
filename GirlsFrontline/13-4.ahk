#include "../Lib/libxin.ahk"
SendMode "Input"

init(){
    global
    W := GetWinSize("少女前线")[1]
    H := GetWinSize("少女前线")[2]
    ch := Scheduler(W,H,2560,1440)
    ch.sc("restartfight", [803, 1250],{minp:[656, 1217], maxp:[944, 1277], t:900, simpleTimeOffset:300})   ; x4
    ch.sc("restartfightandwait", [803, 1250],{minp:[656, 1217], maxp:[944, 1277], t:4000, simpleTimeOffset:500})   ; x4
    ch.sc("party1", [1539, 427], {minp: [1490, 389], maxp: [1576, 466], t:1200, simpleTimeOffset: 400})
    ch.sc("changepartyformation", [500, 1258], {minp: [325, 1218], maxp: [696, 1294], t:2500, simpleTimeOffset: 400})
    ch.sc("partymember1", [481, 707], {minp: [326, 285], maxp: [634, 1109], t:900, simpleTimeOffset: 300})
    ch.sc("partymember2", [837, 671], {minp: [689, 285], maxp: [993, 991], t:900, simpleTimeOffset: 300})
    ch.sc("filterby", [2347, 541], {minp: [2205, 472], maxp: [2515, 640], t:1200, simpleTimeOffset: 400})
    ch.sc("starred", [1939, 265], {minp: [1775, 239], maxp: [2100, 285], t:1200, simpleTimeOffset: 400})
    ch.sc("stock1", [216, 499], {minp: [78, 260], maxp: [348, 764], t:900, simpleTimeOffset: 300})
    ch.sc("stock2", [564, 504], {minp: [428, 254], maxp: [696, 760], t:900, simpleTimeOffset: 300})
    ch.sc("confirmpartyformation", [2355, 1314], {minp: [2203, 1233], maxp: [2528, 1398], t:2000, simpleTimeOffset: 500})
    ch.sc("back", [189, 105], {minp: [22, 36], maxp: [340, 182], t:6000, simpleTimeOffset: 500})
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

    ch.RegisterWait("fightdone", [[2480,80],[2501,233], [2500,1184], [2500,1292]],[0xffda6e, 0xffbe63, 0xffda6e, 0xffbe63])
    ch.RegisterSleep("gap", 5000,,1000,60000, 1)
    ch.RegisterSleep("gap2", 10000,,1000,120000, 1)
    ch.RegisterCheckPixel("fightdone1", [[2480,80],[2501,233], [2500,1184], [2500,1292]],[0xffda6e, 0xffbe63, 0xffda6e, 0xffbe63])
    ch.RegisterCheckPixel("isfull", [[868, 1053], [1169, 1049]], [0x02ddff, 0xfdb300])
    ch.RegisterCheckPixel("supportdone", [[2509, 84], [2515, 250], [2510, 985], [2510, 1060]], [0x4a4c18, 0x393d10, 0x4a4c18, 0x393d10])
    ch.sc("resendsupport", [2280, 1349], {minp: [2143, 1322], maxp: [2429, 1374], t:1200})
    ch.sc("resendsupportconfirm", [1484, 994], {minp: [1332, 936], maxp: [1652, 1045], t:4000})

    ch.sc("gorecycle", [1280, 1057], {minp: [1100, 1020], maxp: [1457, 1080], t:2000})
    ch.sc("recycleselectchar", [661, 432], {minp: [497, 341], maxp: [822, 524], t:1200})
    ch.sc("autoselectandconfirm", [2357, 1309], {minp: [2206, 1219], maxp: [2525, 1407], t:900}) ;x2
    ch.sc("recycle", [2271, 1210], {minp: [2113, 1155], maxp: [2433, 1269], t:4000})
    ;back
    ch.sc("hometofight", [1864, 850], {minp: [1618, 751], maxp: [2097, 943], t:4000})
    ch.sc("4thfight", [1553, 1322], {minp: [849, 1237], maxp: [2509, 1392], t:3000})
    ch.sc("startfighthome", [1981, 1199], {minp: [1784, 1130], maxp: [2203, 1259], t:5000})
    ;p1
    ch.sc("deploy", [2326, 1278], {minp: [2171, 1218], maxp: [2489, 1331], t:1200})
}

init()

OneRound(){
    global ch
    member := "partymember2"
    plan := ["party1", "changepartyformation", member, 
        "filterby", "starred", "stock1", "stock1", "stock2", "stock1", "confirmpartyformation", "back", "startfight",
        "party2","party2", "fillammo", "planmode", "deselect1","party1", "waypoint1","waypoint2", ["waypoint3v1", "waypoint3v2"], "executeplan", 
        "fightdone", "gap", "restartfight", "restartfight", "restartfight", "restartfightandwait", "isfull"]
    return ch.ExecutePlan(plan)
}

PgUp::{
    planfullp1 := ["gorecycle", "recycleselectchar","autoselectandconfirm", "autoselectandconfirm", "recycle", "back", "gap2", "supportdone"]
    planfullp2 := ["hometofight", "4thfight", "startfighthome", "party1", "deploy", "party2", "deploy"]
    clears := 5
    while clears {
        r := OneRound()
        if r {
            supportdone := ch.ExecutePlan(planfullp1)
            if supportdone {
                ch.ExecutePlan(["resendsupport", "resendsupportconfirm"])
            }
            ch.ExecutePlan(planfullp2)
            clears-=1
        }
    }
}
`::Reload

