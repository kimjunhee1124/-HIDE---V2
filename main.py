import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="THE EMPTY HOUSE",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GAME HTML
# ============================================================

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no"
>

<title>THE EMPTY HOUSE</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html,
body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #050505;
    font-family:
        Arial,
        "Malgun Gothic",
        "Apple SD Gothic Neo",
        sans-serif;
}

body {
    user-select: none;
    -webkit-user-select: none;
}

#gameContainer {
    position: relative;
    width: 100vw;
    height: 100vh;
    min-height: 700px;
    overflow: hidden;
    background: #050505;
}

#gameCanvas {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    display: block;
    background: #080808;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
}

#vignette {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 10;

    /*
        기존보다 훨씬 약하게 조정.
        손전등의 밝기를 다시 어둡게 만들지 않도록
        가장자리만 아주 살짝 어둡게 한다.
    */
    background:
        radial-gradient(
            ellipse at center,
            transparent 55%,
            rgba(0, 0, 0, 0.08) 78%,
            rgba(0, 0, 0, 0.22) 100%
        );
}

#noiseOverlay {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 11;
    opacity: 0.035;
    background-image:
        repeating-linear-gradient(
            0deg,
            rgba(255,255,255,0.08) 0px,
            rgba(255,255,255,0.08) 1px,
            transparent 1px,
            transparent 3px
        );
}

#startScreen,
#gameOverScreen,
#escapeScreen {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    z-index: 100;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            circle at center,
            rgba(30, 30, 30, 0.55),
            rgba(0, 0, 0, 0.97) 75%
        );

    color: white;
}

#gameOverScreen,
#escapeScreen {
    display: none;
}

.screenContent {
    width: min(800px, 90vw);
    text-align: center;
    padding: 40px;
}

.gameTitle {
    font-size: clamp(45px, 8vw, 100px);
    font-weight: 900;
    letter-spacing: 0.08em;
    color: #eeeeee;
    text-shadow:
        0 0 10px rgba(255,255,255,0.08),
        0 0 35px rgba(255,255,255,0.04);
}

.gameSubtitle {
    margin-top: 8px;
    font-size: clamp(13px, 2vw, 20px);
    letter-spacing: 0.42em;
    color: #777;
}

.storyBox {
    margin: 55px auto 35px;
    max-width: 650px;

    color: #aaa;
    font-size: 16px;
    line-height: 2.1;
}

.storyBox p {
    margin-bottom: 14px;
}

.startButton,
.restartButton {
    border: 1px solid #777;
    background: rgba(15,15,15,0.85);
    color: #eee;

    padding: 16px 55px;

    font-size: 17px;
    letter-spacing: 0.12em;

    cursor: pointer;

    transition:
        background 0.2s,
        border-color 0.2s,
        transform 0.2s;
}

.startButton:hover,
.restartButton:hover {
    background: #202020;
    border-color: #ccc;
    transform: translateY(-2px);
}

.warningText {
    margin-top: 20px;
    color: #555;
    font-size: 12px;
    letter-spacing: 0.1em;
}

#hud {
    position: absolute;
    left: 25px;
    top: 25px;
    z-index: 30;

    display: none;

    width: 250px;

    color: white;
    font-size: 13px;

    pointer-events: none;
}

.hudPanel {
    background: rgba(5,5,5,0.62);
    border: 1px solid rgba(255,255,255,0.12);

    padding: 13px 15px;

    backdrop-filter: blur(3px);
}

.hudTitle {
    font-size: 12px;
    color: #777;
    letter-spacing: 0.16em;
    margin-bottom: 8px;
}

.barContainer {
    width: 100%;
    height: 7px;
    background: rgba(255,255,255,0.08);
    margin-top: 5px;
    margin-bottom: 11px;
}

.bar {
    height: 100%;
    width: 100%;
    transition: width 0.1s linear;
}

#healthBar {
    background: #aaa;
}

#staminaBar {
    background: #777;
}

.hudInfo {
    color: #aaa;
    line-height: 1.8;
}

.hudKey {
    color: #eee;
}

#messageBox {
    position: absolute;
    left: 50%;
    bottom: 80px;
    transform: translateX(-50%);

    z-index: 35;

    min-width: 280px;
    max-width: 80vw;

    padding: 14px 22px;

    background: rgba(0,0,0,0.75);
    border: 1px solid rgba(255,255,255,0.13);

    color: #ccc;

    text-align: center;

    font-size: 14px;
    line-height: 1.6;

    opacity: 0;
    transition: opacity 0.3s;

    pointer-events: none;
}

#interactionText {
    position: absolute;
    left: 50%;
    bottom: 30px;
    transform: translateX(-50%);

    z-index: 35;

    color: #ddd;

    font-size: 13px;
    letter-spacing: 0.08em;

    opacity: 0;
    transition: opacity 0.2s;

    pointer-events: none;
}

#objective {
    position: absolute;
    right: 25px;
    top: 25px;

    z-index: 30;

    display: none;

    width: 270px;

    color: #bbb;

    background: rgba(5,5,5,0.62);
    border: 1px solid rgba(255,255,255,0.12);

    padding: 14px 17px;

    font-size: 13px;
    line-height: 1.7;

    pointer-events: none;
}

.objectiveTitle {
    color: #777;
    font-size: 11px;
    letter-spacing: 0.16em;
    margin-bottom: 5px;
}

#flashlightIndicator {
    color: #ccc;
}

#screenFlash {
    position: absolute;
    left: 0;
    top: 0;

    width: 100%;
    height: 100%;

    z-index: 40;

    pointer-events: none;

    background: white;
    opacity: 0;
}

</style>
</head>


<body>

<div id="gameContainer">

    <canvas id="gameCanvas"></canvas>

    <div id="vignette"></div>
    <div id="noiseOverlay"></div>

    <div id="screenFlash"></div>


    <!-- =====================================================
         START SCREEN
         ===================================================== -->

    <div id="startScreen">

        <div class="screenContent">

            <div class="gameTitle">
                THE EMPTY HOUSE
            </div>

            <div class="gameSubtitle">
                SOMETHING IS STILL INSIDE
            </div>

            <div class="storyBox">

                <p>
                    밤이 깊어질 무렵,
                    당신은 오래전부터 비어 있었다는 집 앞에 서 있다.
                </p>

                <p>
                    이상하게도 현관문은 열려 있었다.
                </p>

                <p>
                    집 안쪽에서는 아주 작은 소리가 들려왔다.
                </p>

                <p>
                    이상하다고 생각한 당신은 집 안으로 들어간다.
                </p>

                <p>
                    그리고 문이 닫힌다.
                </p>

                <p>
                    이제 당신은 이곳에서 나가야 한다.
                </p>

                <p>
                    하지만...
                    누군가 당신을 따라오고 있다는 느낌이 든다.
                </p>

            </div>

            <button
                id="startButton"
                class="startButton"
            >
                게임 시작
            </button>

            <div class="warningText">
                WASD / 방향키 : 이동　 SHIFT : 달리기　 F : 손전등　 E : 상호작용
            </div>

        </div>

    </div>


    <!-- =====================================================
         GAME OVER
         ===================================================== -->

    <div id="gameOverScreen">

        <div class="screenContent">

            <div class="gameTitle">
                TOO LATE
            </div>

            <div class="storyBox">

                <p>
                    당신은 더 이상 앞으로 나아갈 수 없었다.
                </p>

                <p>
                    어둠 속에서 무언가가 움직였다.
                </p>

                <p>
                    그리고 모든 것이 조용해졌다.
                </p>

            </div>

            <button
                id="restartButton"
                class="restartButton"
            >
                다시 시작
            </button>

        </div>

    </div>


    <!-- =====================================================
         ESCAPE
         ===================================================== -->

    <div id="escapeScreen">

        <div class="screenContent">

            <div class="gameTitle">
                ESCAPED
            </div>

            <div class="storyBox">

                <p>
                    현관문을 열자 차가운 밤공기가 밀려왔다.
                </p>

                <p>
                    당신은 집 밖으로 빠져나왔다.
                </p>

                <p>
                    하지만 뒤를 돌아본 순간,
                    2층 창문에 누군가 서 있는 것이 보였다.
                </p>

                <p>
                    그리고 창문은 천천히 닫혔다.
                </p>

            </div>

            <button
                id="escapeRestartButton"
                class="restartButton"
            >
                다시 플레이
            </button>

        </div>

    </div>


    <!-- =====================================================
         HUD
         ===================================================== -->

    <div id="hud">

        <div class="hudPanel">

            <div class="hudTitle">
                CONDITION
            </div>

            <div>
                체력
            </div>

            <div class="barContainer">
                <div
                    id="healthBar"
                    class="bar"
                ></div>
            </div>

            <div>
                체력
            </div>

            <div class="barContainer">
                <div
                    id="staminaBar"
                    class="bar"
                ></div>
            </div>

            <div class="hudInfo">

                <div>
                    손전등 :
                    <span id="flashlightIndicator">
                        ON
                    </span>
                </div>

                <div>
                    <span class="hudKey">F</span>
                    손전등
                </div>

                <div>
                    <span class="hudKey">SHIFT</span>
                    달리기
                </div>

                <div>
                    <span class="hudKey">E</span>
                    조사하기
                </div>

            </div>

        </div>

    </div>


    <!-- =====================================================
         OBJECTIVE
         ===================================================== -->

    <div id="objective">

        <div class="objectiveTitle">
            OBJECTIVE
        </div>

        <div id="objectiveText">
            집 안을 조사해 보자.
        </div>

    </div>


    <div id="messageBox"></div>

    <div id="interactionText">
        [E] 조사하기
    </div>

</div>


<script>

/* ==========================================================
   CANVAS
   ========================================================== */

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

ctx.imageSmoothingEnabled = false;


/* ==========================================================
   UI
   ========================================================== */

const startScreen = document.getElementById("startScreen");
const gameOverScreen = document.getElementById("gameOverScreen");
const escapeScreen = document.getElementById("escapeScreen");

const startButton = document.getElementById("startButton");
const restartButton = document.getElementById("restartButton");
const escapeRestartButton = document.getElementById("escapeRestartButton");

const hud = document.getElementById("hud");
const objective = document.getElementById("objective");
const objectiveText = document.getElementById("objectiveText");

const healthBar = document.getElementById("healthBar");
const staminaBar = document.getElementById("staminaBar");

const flashlightIndicator =
    document.getElementById("flashlightIndicator");

const messageBox =
    document.getElementById("messageBox");

const interactionText =
    document.getElementById("interactionText");

const screenFlash =
    document.getElementById("screenFlash");


/* ==========================================================
   CANVAS RESIZE
   ========================================================== */

function resizeCanvas() {

    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    canvas.width =
        Math.floor(window.innerWidth * dpr);

    canvas.height =
        Math.floor(window.innerHeight * dpr);

    canvas.style.width =
        window.innerWidth + "px";

    canvas.style.height =
        window.innerHeight + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

}

window.addEventListener(
    "resize",
    resizeCanvas
);

resizeCanvas();


/* ==========================================================
   CONSTANTS
   ========================================================== */

const TILE = 64;

const MAP_WIDTH = 60;
const MAP_HEIGHT = 60;

const PLAYER_RADIUS = 14;

const MONSTER_RADIUS = 18;

const PLAYER_BASE_SPEED = 185;
const PLAYER_SPRINT_SPEED = 300;

const MONSTER_BASE_SPEED = 72;
const MONSTER_CHASE_SPEED = 145;


/* ==========================================================
   GAME STATE
   ========================================================== */

let gameRunning = false;
let gameEnded = false;
let gameEscaped = false;

let gameTime = 0;

let lastTime = performance.now();

let messageTimer = 0;

let cameraX = 0;
let cameraY = 0;

let objectiveStage = 0;

let hasKey = false;
let hasReadNote = false;

let monsterAwake = false;
let monsterSeen = false;

let doorUnlocked = false;

let randomEventTimer = 0;


/* ==========================================================
   INPUT
   ========================================================== */

const keys = {};

window.addEventListener(
    "keydown",
    function(event) {

        const key = event.key.toLowerCase();

        keys[key] = true;

        if (
            key === " " ||
            key === "arrowup" ||
            key === "arrowdown" ||
            key === "arrowleft" ||
            key === "arrowright"
        ) {
            event.preventDefault();
        }

        if (!gameRunning) {
            return;
        }

        if (key === "f") {

            player.flashlight =
                !player.flashlight;

            updateFlashlightUI();

            showMessage(
                player.flashlight
                    ? "손전등을 켰다."
                    : "손전등을 껐다.",
                1200
            );

        }

        if (key === "e") {
            interact();
        }

    }
);

window.addEventListener(
    "keyup",
    function(event) {

        const key = event.key.toLowerCase();

        keys[key] = false;

    }
);


/* ==========================================================
   MAP
   ========================================================== */

/*
    60 x 60 맵

    # = 벽
    . = 바닥
*/

const map = [];

function buildMap() {

    for (let y = 0; y < MAP_HEIGHT; y++) {

        let row = "";

        for (let x = 0; x < MAP_WIDTH; x++) {

            let wall = false;

            if (
                x === 0 ||
                y === 0 ||
                x === MAP_WIDTH - 1 ||
                y === MAP_HEIGHT - 1
            ) {
                wall = true;
            }

            /*
                외벽
            */

            if (
                x >= 10 &&
                x <= 49 &&
                y === 10
            ) {
                wall = true;
            }

            if (
                x >= 10 &&
                x <= 49 &&
                y === 25
            ) {
                wall = true;
            }

            if (
                x >= 10 &&
                x <= 49 &&
                y === 42
            ) {
                wall = true;
            }

            /*
                세로 벽
            */

            if (
                x === 10 &&
                y >= 10 &&
                y <= 25
            ) {
                wall = true;
            }

            if (
                x === 25 &&
                y >= 25 &&
                y <= 42
            ) {
                wall = true;
            }

            if (
                x === 40 &&
                y >= 10 &&
                y <= 25
            ) {
                wall = true;
            }

            if (
                x === 49 &&
                y >= 42 &&
                y <= 53
            ) {
                wall = true;
            }

            /*
                방 내부 구조
            */

            if (
                x >= 3 &&
                x <= 15 &&
                y === 17
            ) {
                wall = true;
            }

            if (
                x === 15 &&
                y >= 3 &&
                y <= 17
            ) {
                wall = true;
            }

            if (
                x >= 31 &&
                x <= 39 &&
                y === 34
            ) {
                wall = true;
            }

            if (
                x === 31 &&
                y >= 34 &&
                y <= 40
            ) {
                wall = true;
            }

            if (
                x >= 44 &&
                x <= 55 &&
                y === 18
            ) {
                wall = true;
            }

            if (
                x === 44 &&
                y >= 12 &&
                y <= 18
            ) {
                wall = true;
            }

            /*
                통로를 만든다.
            */

            if (
                y === 10 &&
                x >= 18 &&
                x <= 21
            ) {
                wall = false;
            }

            if (
                y === 10 &&
                x >= 36 &&
                x <= 38
            ) {
                wall = false;
            }

            if (
                y === 25 &&
                x >= 15 &&
                x <= 18
            ) {
                wall = false;
            }

            if (
                y === 25 &&
                x >= 27 &&
                x <= 30
            ) {
                wall = false;
            }

            if (
                y === 42 &&
                x >= 22 &&
                x <= 28
            ) {
                wall = false;
            }

            if (
                x === 10 &&
                y >= 19 &&
                y <= 21
            ) {
                wall = false;
            }

            if (
                x === 25 &&
                y >= 29 &&
                y <= 32
            ) {
                wall = false;
            }

            if (
                x === 40 &&
                y >= 20 &&
                y <= 23
            ) {
                wall = false;
            }

            /*
                플레이어 시작 공간
            */

            if (
                x >= 4 &&
                x <= 8 &&
                y >= 4 &&
                y <= 8
            ) {
                wall = false;
            }

            /*
                열쇠 주변
            */

            if (
                x >= 43 &&
                x <= 48 &&
                y >= 45 &&
                y <= 49
            ) {
                wall = false;
            }

            /*
                출구 주변
            */

            if (
                x >= 53 &&
                x <= 57 &&
                y >= 2 &&
                y <= 6
            ) {
                wall = false;
            }

            row += wall ? "#" : ".";

        }

        map.push(row);

    }

}

buildMap();


/* ==========================================================
   MAP HELPERS
   ========================================================== */

function isWallTile(x, y) {

    if (
        x < 0 ||
        y < 0 ||
        x >= MAP_WIDTH ||
        y >= MAP_HEIGHT
    ) {
        return true;
    }

    return map[y][x] === "#";

}


function isWallAtWorld(x, y) {

    const tx = Math.floor(x / TILE);
    const ty = Math.floor(y / TILE);

    return isWallTile(tx, ty);

}


/* ==========================================================
   COLLISION
   ========================================================== */

function circleIntersectsWall(x, y, radius) {

    const minX =
        Math.floor((x - radius) / TILE);

    const maxX =
        Math.floor((x + radius) / TILE);

    const minY =
        Math.floor((y - radius) / TILE);

    const maxY =
        Math.floor((y + radius) / TILE);

    for (
        let ty = minY;
        ty <= maxY;
        ty++
    ) {

        for (
            let tx = minX;
            tx <= maxX;
            tx++
        ) {

            if (!isWallTile(tx, ty)) {
                continue;
            }

            const left = tx * TILE;
            const top = ty * TILE;

            const right =
                left + TILE;

            const bottom =
                top + TILE;

            const closestX =
                Math.max(
                    left,
                    Math.min(x, right)
                );

            const closestY =
                Math.max(
                    top,
                    Math.min(y, bottom)
                );

            const dx =
                x - closestX;

            const dy =
                y - closestY;

            if (
                dx * dx +
                dy * dy <
                radius * radius
            ) {
                return true;
            }

        }

    }

    return false;

}


function moveWithCollision(
    object,
    dx,
    dy,
    radius
) {

    const nextX =
        object.x + dx;

    if (
        !circleIntersectsWall(
            nextX,
            object.y,
            radius
        )
    ) {
        object.x = nextX;
    }

    const nextY =
        object.y + dy;

    if (
        !circleIntersectsWall(
            object.x,
            nextY,
            radius
        )
    ) {
        object.y = nextY;
    }

}


/* ==========================================================
   PLAYER
   ========================================================== */

const player = {

    x: 6 * TILE + TILE / 2,
    y: 6 * TILE + TILE / 2,

    health: 100,
    stamina: 100,

    flashlight: true,

    sprinting: false,

    walkFrame: 0,
    walkTimer: 0,

    lastDX: 0,
    lastDY: 1

};


/* ==========================================================
   MONSTER
   ========================================================== */

const monster = {

    x: 43 * TILE + TILE / 2,
    y: 47 * TILE + TILE / 2,

    active: false,

    speed: MONSTER_BASE_SPEED,

    walkFrame: 0,
    walkTimer: 0,

    targetX: 43 * TILE + TILE / 2,
    targetY: 47 * TILE + TILE / 2,

    wanderTimer: 0

};


/* ==========================================================
   ITEMS
   ========================================================== */

const keyItem = {

    x: 46 * TILE + TILE / 2,
    y: 47 * TILE + TILE / 2,

    collected: false

};


const noteItem = {

    x: 30 * TILE + TILE / 2,
    y: 20 * TILE + TILE / 2,

    collected: false

};


const exitDoor = {

    x: 56 * TILE + TILE / 2,
    y: 3 * TILE + TILE / 2

};


/* ==========================================================
   PIXEL ART
   ========================================================== */

const PLAYER_FRAMES = [

    [
        "   HHHH   ",
        "  HHHHHH  ",
        " HHHSSHHH ",
        " HSSSSSSH ",
        " HSESSSEH ",
        " HSSSSSSH ",
        "  HHHHHH  ",
        "   WWWW   ",
        "  WWWWWW  ",
        " WWTTTTWW ",
        " WWTTTTWW ",
        "  WWWWWW  ",
        "  UUUUUU  ",
        "  UUUUUU  ",
        "  SS  SS  ",
        "  SS  SS  "
    ],

    [
        "   HHHH   ",
        "  HHHHHH  ",
        " HHHSSHHH ",
        " HSSSSSSH ",
        " HSESSSEH ",
        " HSSSSSSH ",
        "  HHHHHH  ",
        "   WWWW   ",
        "  WWWWWW  ",
        " WWTTTTWW ",
        " WWTTTTWW ",
        "  WWWWWW  ",
        "  UUUUUU  ",
        "  UUUUUU  ",
        "   SSSS   ",
        "  SS  SS  "
    ]

];


const MONSTER_FRAMES = [

    [
        "    DDDD    ",
        "  DDDDDDDD  ",
        " DDDPPPPDDD ",
        " DDPPPPPPDD ",
        " DDPERRPEDD ",
        " DDPPPPPPDD ",
        " DDDPPPPDDD ",
        "  DDDDDDDD  ",
        "   DDDDDD   ",
        "  DDDDDDDD  ",
        " DDDDDDDDDD ",
        " DDDDDDDDDD ",
        "  DDDDDDDD  ",
        "  DD    DD  ",
        " DD      DD "
    ],

    [
        "    DDDD    ",
        "  DDDDDDDD  ",
        " DDDPPPPDDD ",
        " DDPPPPPPDD ",
        " DDPERRPEDD ",
        " DDPPPPPPDD ",
        " DDDPPPPDDD ",
        "  DDDDDDDD  ",
        "   DDDDDD   ",
        "  DDDDDDDD  ",
        " DDDDDDDDDD ",
        " DDDDDDDDDD ",
        "  DDDDDDDD  ",
        "   DD  DD   ",
        "  DD    DD  "
    ]

];


const PIXEL_COLORS = {

    H: "#202329",
    S: "#e0b69a",
    E: "#171717",
    W: "#f0f0ed",
    T: "#565c67",
    U: "#30343c",
    D: "#191b20",
    P: "#d7d0c6",
    R: "#8b3d43"

};


/* ==========================================================
   PIXEL SPRITE
   ========================================================== */

function pixelSprite(
    pattern,
    x,
    y,
    scale,
    colors,
    flipX = false
) {

    ctx.save();

    ctx.imageSmoothingEnabled = false;

    const width =
        pattern[0].length * scale;

    const height =
        pattern.length * scale;

    const startX =
        x - width / 2;

    const startY =
        y - height / 2;

    for (
        let row = 0;
        row < pattern.length;
        row++
    ) {

        const line =
            pattern[row];

        for (
            let col = 0;
            col < line.length;
            col++
        ) {

            const symbol =
                line[col];

            if (!colors[symbol]) {
                continue;
            }

            let drawX;

            if (flipX) {

                drawX =
                    startX +
                    (line.length - col - 1) *
                    scale;

            } else {

                drawX =
                    startX +
                    col * scale;

            }

            const drawY =
                startY +
                row * scale;

            ctx.fillStyle =
                colors[symbol];

            ctx.fillRect(
                Math.floor(drawX),
                Math.floor(drawY),
                scale,
                scale
            );

        }

    }

    ctx.restore();

}


/* ==========================================================
   PLAYER DRAW
   ========================================================== */

function drawPlayer() {

    const screenX =
        player.x - cameraX;

    const screenY =
        player.y - cameraY;

    /*
        그림자
    */

    ctx.save();

    ctx.fillStyle =
        "rgba(0,0,0,0.38)";

    ctx.beginPath();

    ctx.ellipse(
        screenX,
        screenY + 24,
        19,
        7,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();


    /*
        걷기 애니메이션
    */

    const frame =
        Math.floor(
            player.walkFrame
        ) %
        PLAYER_FRAMES.length;


    /*
        방향
    */

    const flip =
        player.lastDX < -0.1;


    /*
        캐릭터 본체
    */

    pixelSprite(
        PLAYER_FRAMES[frame],
        screenX,
        screenY,
        3,
        PIXEL_COLORS,
        flip
    );


    /*
        손전등 작은 빛
    */

    if (player.flashlight) {

        ctx.save();

        ctx.fillStyle =
            "rgba(255,245,200,0.25)";

        ctx.beginPath();

        ctx.arc(
            screenX +
            player.lastDX * 18,
            screenY +
            player.lastDY * 18,
            4,
            0,
            Math.PI * 2
        );

        ctx.fill();

        ctx.restore();

    }

}


/* ==========================================================
   MONSTER DRAW
   ========================================================== */

function drawMonster() {

    if (!monster.active) {
        return;
    }

    const screenX =
        monster.x - cameraX;

    const screenY =
        monster.y - cameraY;


    /*
        그림자
    */

    ctx.save();

    ctx.fillStyle =
        "rgba(0,0,0,0.5)";

    ctx.beginPath();

    ctx.ellipse(
        screenX,
        screenY + 26,
        25,
        9,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();


    /*
        약한 주변 그림자
    */

    ctx.save();

    const glow =
        ctx.createRadialGradient(
            screenX,
            screenY,
            5,
            screenX,
            screenY,
            55
        );

    glow.addColorStop(
        0,
        "rgba(0,0,0,0.22)"
    );

    glow.addColorStop(
        1,
        "rgba(0,0,0,0)"
    );

    ctx.fillStyle = glow;

    ctx.beginPath();

    ctx.arc(
        screenX,
        screenY,
        55,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();


    const frame =
        Math.floor(
            monster.walkFrame
        ) %
        MONSTER_FRAMES.length;


    pixelSprite(
        MONSTER_FRAMES[frame],
        screenX,
        screenY,
        3,
        PIXEL_COLORS,
        monster.x > player.x
    );

}


/* ==========================================================
   FLOOR
   ========================================================== */

function drawFloor() {

    const startX =
        Math.max(
            0,
            Math.floor(cameraX / TILE) - 2
        );

    const endX =
        Math.min(
            MAP_WIDTH - 1,
            Math.floor(
                (cameraX + window.innerWidth) /
                TILE
            ) + 2
        );

    const startY =
        Math.max(
            0,
            Math.floor(cameraY / TILE) - 2
        );

    const endY =
        Math.min(
            MAP_HEIGHT - 1,
            Math.floor(
                (cameraY + window.innerHeight) /
                TILE
            ) + 2
        );


    for (
        let y = startY;
        y <= endY;
        y++
    ) {

        for (
            let x = startX;
            x <= endX;
            x++
        ) {

            const sx =
                x * TILE - cameraX;

            const sy =
                y * TILE - cameraY;

            if (map[y][x] === "#") {

                /*
                    벽
                */

                ctx.fillStyle =
                    "#292a2d";

                ctx.fillRect(
                    sx,
                    sy,
                    TILE,
                    TILE
                );


                /*
                    벽 상단
                */

                ctx.fillStyle =
                    "#34363a";

                ctx.fillRect(
                    sx,
                    sy,
                    TILE,
                    4
                );


                /*
                    벽 하단
                */

                ctx.fillStyle =
                    "#1c1d20";

                ctx.fillRect(
                    sx,
                    sy + TILE - 5,
                    TILE,
                    5
                );


                /*
                    벽 내부 픽셀
                */

                ctx.fillStyle =
                    "rgba(255,255,255,0.025)";

                ctx.fillRect(
                    sx + 8,
                    sy + 14,
                    TILE - 16,
                    2
                );

            } else {

                /*
                    바닥
                */

                ctx.fillStyle =
                    "#57575a";

                ctx.fillRect(
                    sx,
                    sy,
                    TILE,
                    TILE
                );


                /*
                    바닥 타일 구분
                */

                ctx.strokeStyle =
                    "rgba(0,0,0,0.10)";

                ctx.lineWidth = 1;

                ctx.strokeRect(
                    sx + 0.5,
                    sy + 0.5,
                    TILE - 1,
                    TILE - 1
                );


                /*
                    아주 약한 바닥 무늬
                */

                if (
                    (x * 13 + y * 7) % 9 === 0
                ) {

                    ctx.fillStyle =
                        "rgba(0,0,0,0.08)";

                    ctx.fillRect(
                        sx + 18,
                        sy + 31,
                        12,
                        3
                    );

                }

            }

        }

    }

}


/* ==========================================================
   KEY DRAW
   ========================================================== */

function drawKey() {

    if (keyItem.collected) {
        return;
    }

    const x =
        keyItem.x - cameraX;

    const y =
        keyItem.y - cameraY;


    ctx.save();

    ctx.translate(x, y);


    /*
        바닥 그림자
    */

    ctx.fillStyle =
        "rgba(0,0,0,0.35)";

    ctx.beginPath();

    ctx.ellipse(
        0,
        12,
        13,
        5,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();


    /*
        열쇠
    */

    ctx.strokeStyle =
        "#d8d0a8";

    ctx.lineWidth = 4;

    ctx.beginPath();

    ctx.arc(
        -7,
        0,
        5,
        0,
        Math.PI * 2
    );

    ctx.stroke();

    ctx.beginPath();

    ctx.moveTo(
        -2,
        0
    );

    ctx.lineTo(
        13,
        0
    );

    ctx.lineTo(
        13,
        5
    );

    ctx.moveTo(
        8,
        0
    );

    ctx.lineTo(
        8,
        4
    );

    ctx.stroke();


    /*
        빛
    */

    const glow =
        ctx.createRadialGradient(
            0,
            0,
            1,
            0,
            0,
            30
        );

    glow.addColorStop(
        0,
        "rgba(240,220,150,0.25)"
    );

    glow.addColorStop(
        1,
        "rgba(240,220,150,0)"
    );

    ctx.fillStyle = glow;

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        30,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();

}


/* ==========================================================
   NOTE DRAW
   ========================================================== */

function drawNote() {

    if (noteItem.collected) {
        return;
    }

    const x =
        noteItem.x - cameraX;

    const y =
        noteItem.y - cameraY;


    ctx.save();

    ctx.translate(
        x,
        y
    );

    ctx.rotate(-0.08);


    ctx.fillStyle =
        "#d9d5c8";

    ctx.fillRect(
        -13,
        -10,
        26,
        20
    );


    ctx.fillStyle =
        "rgba(0,0,0,0.28)";

    ctx.fillRect(
        -8,
        -4,
        16,
        2
    );

    ctx.fillRect(
        -8,
        1,
        12,
        2
    );


    ctx.restore();

}


/* ==========================================================
   EXIT DRAW
   ========================================================== */

function drawExit() {

    const x =
        exitDoor.x - cameraX;

    const y =
        exitDoor.y - cameraY;


    ctx.save();

    ctx.translate(
        x,
        y
    );


    /*
        문
    */

    ctx.fillStyle =
        doorUnlocked
            ? "#64635e"
            : "#3e3d3a";

    ctx.fillRect(
        -22,
        -30,
        44,
        60
    );


    /*
        문 테두리
    */

    ctx.strokeStyle =
        "#191919";

    ctx.lineWidth = 4;

    ctx.strokeRect(
        -22,
        -30,
        44,
        60
    );


    /*
        문 손잡이
    */

    ctx.fillStyle =
        "#b6aa86";

    ctx.beginPath();

    ctx.arc(
        11,
        2,
        3,
        0,
        Math.PI * 2
    );

    ctx.fill();


    /*
        출구 빛
    */

    if (doorUnlocked) {

        const glow =
            ctx.createRadialGradient(
                0,
                0,
                5,
                0,
                0,
                100
            );

        glow.addColorStop(
            0,
            "rgba(220,220,200,0.18)"
        );

        glow.addColorStop(
            1,
            "rgba(220,220,200,0)"
        );

        ctx.fillStyle =
            glow;

        ctx.beginPath();

        ctx.arc(
            0,
            0,
            100,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }


    ctx.restore();

}


/* ==========================================================
   DARKNESS / FLASHLIGHT
   ========================================================== */

/*
    이 부분이 이번에 핵심적으로 수정된 부분.

    이전 방식:
        강한 검은색을 전체에 덮고
        destination-out을 사용하는 과정에서
        손전등이 있어도 전체적으로 너무 어두워지는 문제가 발생.

    현재 방식:
        1. 전체 화면을 중간 정도의 어둠으로 덮는다.
        2. 손전등 영역을 넓게 제거한다.
        3. 중앙에 아주 약한 따뜻한 빛을 추가한다.
        4. 손전등 OFF일 때는 좁은 시야만 제공한다.
*/

function drawDarkness() {

    const screenW =
        window.innerWidth;

    const screenH =
        window.innerHeight;

    const centerX =
        screenW / 2;

    const centerY =
        screenH / 2;


    /*
        ------------------------------------------------------
        손전등 OFF
        ------------------------------------------------------
    */

    if (!player.flashlight) {

        /*
            전체 어둠.
            너무 강하지 않게 조정.
        */

        ctx.save();

        ctx.fillStyle =
            "rgba(0,0,0,0.70)";

        ctx.fillRect(
            0,
            0,
            screenW,
            screenH
        );

        ctx.restore();


        /*
            가까운 곳만 약간 보인다.
        */

        ctx.save();

        ctx.globalCompositeOperation =
            "destination-out";

        const darkVision =
            ctx.createRadialGradient(
                centerX,
                centerY,
                10,
                centerX,
                centerY,
                155
            );

        darkVision.addColorStop(
            0.00,
            "rgba(0,0,0,0.90)"
        );

        darkVision.addColorStop(
            0.35,
            "rgba(0,0,0,0.65)"
        );

        darkVision.addColorStop(
            0.65,
            "rgba(0,0,0,0.30)"
        );

        darkVision.addColorStop(
            0.85,
            "rgba(0,0,0,0.08)"
        );

        darkVision.addColorStop(
            1.00,
            "rgba(0,0,0,0)"
        );

        ctx.fillStyle =
            darkVision;

        ctx.fillRect(
            0,
            0,
            screenW,
            screenH
        );

        ctx.restore();

        return;
    }


    /*
        ------------------------------------------------------
        손전등 ON
        ------------------------------------------------------
    */

    /*
        전체 어둠을 약하게.
        기존 0.78보다 훨씬 밝다.
    */

    ctx.save();

    ctx.fillStyle =
        "rgba(0,0,0,0.48)";

    ctx.fillRect(
        0,
        0,
        screenW,
        screenH
    );

    ctx.restore();


    /*
        손전등 범위.
        달릴 때 조금 넓어진다.
    */

    const lightRadius =
        player.sprinting
            ? 335
            : 300;


    /*
        손전등의 메인 밝은 영역.
    */

    ctx.save();

    ctx.globalCompositeOperation =
        "destination-out";


    const flashlight =
        ctx.createRadialGradient(
            centerX,
            centerY,
            20,
            centerX,
            centerY,
            lightRadius
        );


    /*
        중심은 완전히 밝게.
    */

    flashlight.addColorStop(
        0.00,
        "rgba(0,0,0,1.00)"
    );

    flashlight.addColorStop(
        0.25,
        "rgba(0,0,0,1.00)"
    );

    flashlight.addColorStop(
        0.48,
        "rgba(0,0,0,0.98)"
    );

    flashlight.addColorStop(
        0.65,
        "rgba(0,0,0,0.88)"
    );

    flashlight.addColorStop(
        0.78,
        "rgba(0,0,0,0.62)"
    );

    flashlight.addColorStop(
        0.89,
        "rgba(0,0,0,0.32)"
    );

    flashlight.addColorStop(
        0.96,
        "rgba(0,0,0,0.10)"
    );

    flashlight.addColorStop(
        1.00,
        "rgba(0,0,0,0)"
    );


    ctx.fillStyle =
        flashlight;

    ctx.fillRect(
        0,
        0,
        screenW,
        screenH
    );

    ctx.restore();


    /*
        손전등 중심을 조금 더 밝게 한다.
        이 부분 때문에 캐릭터 주변이 확실하게 보인다.
    */

    ctx.save();

    ctx.globalCompositeOperation =
        "destination-out";

    const centerLight =
        ctx.createRadialGradient(
            centerX,
            centerY,
            5,
            centerX,
            centerY,
            125
        );

    centerLight.addColorStop(
        0,
        "rgba(0,0,0,0.65)"
    );

    centerLight.addColorStop(
        0.5,
        "rgba(0,0,0,0.35)"
    );

    centerLight.addColorStop(
        1,
        "rgba(0,0,0,0)"
    );

    ctx.fillStyle =
        centerLight;

    ctx.fillRect(
        0,
        0,
        screenW,
        screenH
    );

    ctx.restore();


    /*
        손전등 자체의 아주 약한 따뜻한 색감.
    */

    ctx.save();

    const warmGlow =
        ctx.createRadialGradient(
            centerX,
            centerY,
            10,
            centerX,
            centerY,
            210
        );

    warmGlow.addColorStop(
        0,
        "rgba(255,245,205,0.075)"
    );

    warmGlow.addColorStop(
        0.35,
        "rgba(255,240,190,0.035)"
    );

    warmGlow.addColorStop(
        1,
        "rgba(255,240,190,0)"
    );

    ctx.fillStyle =
        warmGlow;

    ctx.fillRect(
        0,
        0,
        screenW,
        screenH
    );

    ctx.restore();

}


/* ==========================================================
   FLASH EFFECT
   ========================================================== */

function flashScreen(
    amount = 0.3,
    duration = 150
) {

    screenFlash.style.opacity =
        amount.toString();

    setTimeout(
        function() {

            screenFlash.style.opacity =
                "0";

        },
        duration
    );

}


/* ==========================================================
   DISTANCE
   ========================================================== */

function distance(
    x1,
    y1,
    x2,
    y2
) {

    const dx =
        x2 - x1;

    const dy =
        y2 - y1;

    return Math.sqrt(
        dx * dx +
        dy * dy
    );

}


/* ==========================================================
   PLAYER UPDATE
   ========================================================== */

function updatePlayer(dt) {

    let dx = 0;
    let dy = 0;


    if (
        keys["w"] ||
        keys["arrowup"]
    ) {
        dy -= 1;
    }

    if (
        keys["s"] ||
        keys["arrowdown"]
    ) {
        dy += 1;
    }

    if (
        keys["a"] ||
        keys["arrowleft"]
    ) {
        dx -= 1;
    }

    if (
        keys["d"] ||
        keys["arrowright"]
    ) {
        dx += 1;
    }


    const moving =
        dx !== 0 ||
        dy !== 0;


    if (moving) {

        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        dx /= length;
        dy /= length;


        player.lastDX = dx;
        player.lastDY = dy;


        /*
            Shift를 누르고 있고
            스태미나가 남아 있을 때 달리기.
        */

        const wantsSprint =
            keys["shift"];


        player.sprinting =
            wantsSprint &&
            player.stamina > 1;


        let speed =
            PLAYER_BASE_SPEED;


        if (player.sprinting) {

            speed =
                PLAYER_SPRINT_SPEED;

            player.stamina -=
                32 * dt;

            if (
                player.stamina < 0
            ) {
                player.stamina = 0;
            }

        } else {

            player.stamina +=
                22 * dt;

            if (
                player.stamina > 100
            ) {
                player.stamina = 100;
            }

        }


        moveWithCollision(
            player,
            dx * speed * dt,
            dy * speed * dt,
            PLAYER_RADIUS
        );


        player.walkTimer +=
            dt;

        if (
            player.walkTimer >= 0.10
        ) {

            player.walkTimer = 0;

            player.walkFrame =
                (
                    player.walkFrame + 1
                ) %
                PLAYER_FRAMES.length;

        }

    } else {

        player.sprinting = false;

        player.stamina +=
            28 * dt;

        if (
            player.stamina > 100
        ) {
            player.stamina = 100;
        }

    }


    /*
        체력이 0이면 게임 오버.
    */

    if (
        player.health <= 0
    ) {

        player.health = 0;

        endGame();

    }

}


/* ==========================================================
   MONSTER AI
   ========================================================== */

function updateMonster(dt) {

    if (!monster.active) {
        return;
    }


    const dist =
        distance(
            monster.x,
            monster.y,
            player.x,
            player.y
        );


    /*
        일정 거리 안으로 들어오면 추적.
    */

    if (dist < 650) {

        monster.targetX =
            player.x;

        monster.targetY =
            player.y;

        monster.speed =
            MONSTER_CHASE_SPEED;

        monsterSeen = true;

    } else {

        monster.speed =
            MONSTER_BASE_SPEED;

        monster.wanderTimer -=
            dt;

        if (
            monster.wanderTimer <= 0
        ) {

            monster.wanderTimer =
                2 +
                Math.random() * 3;

            const angle =
                Math.random() *
                Math.PI * 2;

            const wanderDistance =
                150 +
                Math.random() * 300;

            monster.targetX =
                monster.x +
                Math.cos(angle) *
                wanderDistance;

            monster.targetY =
                monster.y +
                Math.sin(angle) *
                wanderDistance;

        }

    }


    let dx =
        monster.targetX -
        monster.x;

    let dy =
        monster.targetY -
        monster.y;


    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );


    if (
        length > 5
    ) {

        dx /= length;
        dy /= length;


        moveWithCollision(
            monster,
            dx *
                monster.speed *
                dt,
            dy *
                monster.speed *
                dt,
            MONSTER_RADIUS
        );


        monster.walkTimer +=
            dt;

        if (
            monster.walkTimer >= 0.13
        ) {

            monster.walkTimer = 0;

            monster.walkFrame =
                (
                    monster.walkFrame + 1
                ) %
                MONSTER_FRAMES.length;

        }

    }


    /*
        플레이어와 너무 가까워지면
        체력을 조금씩 감소.
    */

    if (
        dist < 42
    ) {

        player.health -=
            20 * dt;

        flashScreen(
            0.04,
            50
        );

    }

}


/* ==========================================================
   CAMERA
   ========================================================== */

function updateCamera() {

    const screenW =
        window.innerWidth;

    const screenH =
        window.innerHeight;


    const targetX =
        player.x -
        screenW / 2;

    const targetY =
        player.y -
        screenH / 2;


    cameraX +=
        (
            targetX -
            cameraX
        ) * 0.12;

    cameraY +=
        (
            targetY -
            cameraY
        ) * 0.12;


    const worldWidth =
        MAP_WIDTH * TILE;

    const worldHeight =
        MAP_HEIGHT * TILE;


    cameraX =
        Math.max(
            0,
            Math.min(
                cameraX,
                Math.max(
                    0,
                    worldWidth -
                    screenW
                )
            )
        );


    cameraY =
        Math.max(
            0,
            Math.min(
                cameraY,
                Math.max(
                    0,
                    worldHeight -
                    screenH
                )
            )
        );

}


/* ==========================================================
   INTERACTION
   ========================================================== */

function interact() {

    /*
        열쇠
    */

    const keyDistance =
        distance(
            player.x,
            player.y,
            keyItem.x,
            keyItem.y
        );


    if (
        !keyItem.collected &&
        keyDistance < 65
    ) {

        keyItem.collected = true;
        hasKey = true;

        objectiveStage = 2;

        objectiveText.textContent =
            "열쇠를 얻었다. 현관으로 돌아가자.";

        showMessage(
            "열쇠를 발견했다.",
            1800
        );

        /*
            몬스터 활성화
        */

        monster.active = true;
        monsterAwake = true;

        showMessage(
            "어딘가에서 문이 닫히는 소리가 들렸다.",
            2500
        );

        return;

    }


    /*
        쪽지
    */

    const noteDistance =
        distance(
            player.x,
            player.y,
            noteItem.x,
            noteItem.y
        );


    if (
        !noteItem.collected &&
        noteDistance < 65
    ) {

        noteItem.collected = true;
        hasReadNote = true;

        objectiveStage = 1;

        objectiveText.textContent =
            "집 안을 더 조사해 보자.";

        showMessage(
            "쪽지에는 짧은 문장이 적혀 있다.\n\n\"문을 열기 전에 반드시 불을 꺼라.\"",
            4000
        );

        return;

    }


    /*
        출구
    */

    const exitDistance =
        distance(
            player.x,
            player.y,
            exitDoor.x,
            exitDoor.y
        );


    if (
        exitDistance < 75
    ) {

        if (!hasKey) {

            showMessage(
                "문이 잠겨 있다.",
                1600
            );

            return;

        }


        if (hasKey) {

            doorUnlocked = true;

            objectiveStage = 3;

            objectiveText.textContent =
                "문을 열어 집 밖으로 나가자.";

            showMessage(
                "열쇠가 맞는다. 문이 열렸다.",
                1800
            );

            setTimeout(
                function() {

                    escapeGame();

                },
                1200
            );

            return;

        }

    }


    /*
        아무것도 없을 때
    */

    showMessage(
        "특별한 것은 보이지 않는다.",
        1200
    );

}


/* ==========================================================
   INTERACTION PROMPT
   ========================================================== */

function updateInteractionPrompt() {

    let visible = false;


    const keyDistance =
        distance(
            player.x,
            player.y,
            keyItem.x,
            keyItem.y
        );


    const noteDistance =
        distance(
            player.x,
            player.y,
            noteItem.x,
            noteItem.y
        );


    const exitDistance =
        distance(
            player.x,
            player.y,
            exitDoor.x,
            exitDoor.y
        );


    if (
        !keyItem.collected &&
        keyDistance < 75
    ) {
        visible = true;
    }


    if (
        !noteItem.collected &&
        noteDistance < 75
    ) {
        visible = true;
    }


    if (
        exitDistance < 85
    ) {
        visible = true;
    }


    interactionText.style.opacity =
        visible ? "1" : "0";

}


/* ==========================================================
   RANDOM EVENTS
   ========================================================== */

function updateRandomEvents(dt) {

    if (!gameRunning) {
        return;
    }

    randomEventTimer -=
        dt;


    if (
        randomEventTimer > 0
    ) {
        return;
    }


    randomEventTimer =
        5 +
        Math.random() * 8;


    const roll =
        Math.random();


    /*
        아주 가벼운 공포 연출.
        그래픽한 장면은 사용하지 않는다.
    */

    if (
        roll < 0.20 &&
        gameTime > 8
    ) {

        showMessage(
            "어딘가에서 작은 소리가 들렸다.",
            1800
        );

    } else if (
        roll < 0.35 &&
        gameTime > 15
    ) {

        showMessage(
            "방금 뒤쪽에서 무언가 움직인 것 같다.",
            1800
        );

    } else if (
        roll < 0.46 &&
        gameTime > 25
    ) {

        showMessage(
            "집 안이 갑자기 조용해졌다.",
            1800
        );

    }


    /*
        일정 시간이 지나면 몬스터가 활성화될 수 있다.
    */

    if (
        gameTime > 18 &&
        hasReadNote &&
        !monster.active
    ) {

        monster.active = true;
        monsterAwake = true;

        showMessage(
            "복도 쪽에서 발소리가 들렸다.",
            2200
        );

    }

}


/* ==========================================================
   OBJECTIVE UPDATE
   ========================================================== */

function updateObjective() {

    if (
        objectiveStage === 0
    ) {

        objectiveText.textContent =
            "집 안을 조사해 보자.";

    } else if (
        objectiveStage === 1
    ) {

        objectiveText.textContent =
            "집 안을 더 조사해 보자.";

    } else if (
        objectiveStage === 2
    ) {

        objectiveText.textContent =
            "열쇠를 얻었다. 현관으로 돌아가자.";

    } else if (
        objectiveStage === 3
    ) {

        objectiveText.textContent =
            "문을 열어 집 밖으로 나가자.";

    }

}


/* ==========================================================
   HUD UPDATE
   ========================================================== */

function updateHUD() {

    healthBar.style.width =
        Math.max(
            0,
            Math.min(
                100,
                player.health
            )
        ) + "%";


    staminaBar.style.width =
        Math.max(
            0,
            Math.min(
                100,
                player.stamina
            )
        ) + "%";


    updateFlashlightUI();

}


function updateFlashlightUI() {

    flashlightIndicator.textContent =
        player.flashlight
            ? "ON"
            : "OFF";

}


/* ==========================================================
   MESSAGE
   ========================================================== */

function showMessage(
    text,
    duration = 1800
) {

    messageBox.textContent =
        text;

    messageBox.style.opacity =
        "1";

    clearTimeout(
        showMessage.timer
    );

    showMessage.timer =
        setTimeout(
            function() {

                messageBox.style.opacity =
                    "0";

            },
            duration
        );

}


/* ==========================================================
   DRAW WORLD
   ========================================================== */

function drawWorld() {

    const screenW =
        window.innerWidth;

    const screenH =
        window.innerHeight;


    /*
        배경
    */

    ctx.fillStyle =
        "#070707";

    ctx.fillRect(
        0,
        0,
        screenW,
        screenH
    );


    /*
        월드
    */

    drawFloor();

    drawKey();

    drawNote();

    drawExit();

    drawMonster();

    drawPlayer();


    /*
        어둠 / 손전등
    */

    drawDarkness();

}


/* ==========================================================
   GAME START
   ========================================================== */

function startGame() {

    gameRunning = true;
    gameEnded = false;
    gameEscaped = false;

    gameTime = 0;

    hasKey = false;
    hasReadNote = false;

    monsterAwake = false;
    monsterSeen = false;

    doorUnlocked = false;

    objectiveStage = 0;

    randomEventTimer =
        4 +
        Math.random() * 3;


    /*
        플레이어 초기화
    */

    player.x =
        6 * TILE +
        TILE / 2;

    player.y =
        6 * TILE +
        TILE / 2;

    player.health = 100;

    player.stamina = 100;

    player.flashlight = true;

    player.sprinting = false;

    player.lastDX = 0;
    player.lastDY = 1;

    player.walkFrame = 0;
    player.walkTimer = 0;


    /*
        몬스터 초기화
    */

    monster.x =
        43 * TILE +
        TILE / 2;

    monster.y =
        47 * TILE +
        TILE / 2;

    monster.active = false;

    monster.speed =
        MONSTER_BASE_SPEED;


    /*
        아이템
    */

    keyItem.collected = false;
    noteItem.collected = false;


    /*
        UI
    */

    startScreen.style.display =
        "none";

    gameOverScreen.style.display =
        "none";

    escapeScreen.style.display =
        "none";

    hud.style.display =
        "block";

    objective.style.display =
        "block";


    updateObjective();
    updateHUD();


    /*
        시작 메시지
    */

    showMessage(
        "집 안을 조사해 보자.",
        2200
    );


    lastTime =
        performance.now();

}


/* ==========================================================
   GAME OVER
   ========================================================== */

function endGame() {

    if (!gameRunning) {
        return;
    }

    gameRunning = false;
    gameEnded = true;

    hud.style.display =
        "none";

    objective.style.display =
        "none";

    gameOverScreen.style.display =
        "flex";

}


/* ==========================================================
   ESCAPE
   ========================================================== */

function escapeGame() {

    if (!gameRunning) {
        return;
    }

    gameRunning = false;
    gameEscaped = true;

    hud.style.display =
        "none";

    objective.style.display =
        "none";

    escapeScreen.style.display =
        "flex";

}


/* ==========================================================
   BUTTON EVENTS
   ========================================================== */

startButton.addEventListener(
    "click",
    function() {

        startGame();

    }
);


restartButton.addEventListener(
    "click",
    function() {

        startGame();

    }
);


escapeRestartButton.addEventListener(
    "click",
    function() {

        startGame();

    }
);


/* ==========================================================
   MAIN UPDATE
   ========================================================== */

function update(dt) {

    if (!gameRunning) {
        return;
    }


    gameTime +=
        dt;


    updatePlayer(dt);

    updateMonster(dt);

    updateCamera();

    updateRandomEvents(dt);

    updateInteractionPrompt();

    updateObjective();

    updateHUD();

}


/* ==========================================================
   MAIN LOOP
   ========================================================== */

function gameLoop(now) {

    let dt =
        (now - lastTime) / 1000;


    /*
        탭 전환 등으로
        dt가 지나치게 커지는 것을 방지.
    */

    dt =
        Math.min(
            dt,
            0.05
        );


    lastTime =
        now;


    update(dt);

    drawWorld();


    requestAnimationFrame(
        gameLoop
    );

}


/* ==========================================================
   START RENDER LOOP
   ========================================================== */

requestAnimationFrame(
    gameLoop
);


/* ==========================================================
   INITIAL UI
   ========================================================== */

updateFlashlightUI();


</script>

</body>
</html>
"""


# ============================================================
# STREAMLIT
# ============================================================

components.html(
    GAME_HTML,
    height=850,
    scrolling=False
)
