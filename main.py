import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="THE EMPTY HOUSE",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #050507;
    font-family:
        "Courier New",
        "Noto Sans KR",
        monospace;
}

body {
    user-select: none;
}

#gameWrapper {
    position: relative;
    width: 100vw;
    height: 100vh;
    min-height: 700px;
    overflow: hidden;
    background: #050507;
}

canvas {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    display: block;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
    background: #050507;
}

/* =========================================================
   START SCREEN
   ========================================================= */

#startScreen {
    position: absolute;
    inset: 0;
    z-index: 100;
    display: flex;
    justify-content: center;
    align-items: center;
    background:
        radial-gradient(
            circle at center,
            rgba(30, 30, 35, 0.30) 0%,
            rgba(5, 5, 7, 0.92) 58%,
            rgba(0, 0, 0, 0.98) 100%
        );
    transition:
        opacity 0.8s ease,
        visibility 0.8s ease;
}

#startScreen.hidden {
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}

.startBox {
    width: min(760px, 90vw);
    padding: 58px 60px 52px;
    text-align: center;
    border: 1px solid rgba(180, 180, 190, 0.15);
    background:
        linear-gradient(
            180deg,
            rgba(12, 12, 16, 0.94),
            rgba(5, 5, 8, 0.97)
        );
    box-shadow:
        0 0 80px rgba(0, 0, 0, 0.8),
        inset 0 0 60px rgba(255, 255, 255, 0.015);
}

.logoSmall {
    color: #666670;
    font-size: 12px;
    letter-spacing: 7px;
    margin-bottom: 26px;
}

.gameTitle {
    margin: 0;
    color: #eeeeee;
    font-size: clamp(42px, 7vw, 82px);
    font-weight: 700;
    letter-spacing: 8px;
    line-height: 1;
    text-shadow:
        0 0 12px rgba(255,255,255,0.08),
        0 0 40px rgba(255,255,255,0.03);
}

.gameSubtitle {
    margin-top: 18px;
    color: #8b8b94;
    font-size: clamp(12px, 1.6vw, 16px);
    letter-spacing: 5px;
}

.storyText {
    margin: 48px auto 36px;
    max-width: 590px;
    color: #73737d;
    font-size: 13px;
    line-height: 2.05;
    letter-spacing: 1px;
}

.storyText strong {
    color: #aaaab2;
    font-weight: normal;
}

.startButton {
    position: relative;
    width: 230px;
    height: 58px;
    border: 1px solid #3f3f48;
    outline: none;
    background: #111116;
    color: #d9d9de;
    font-family: inherit;
    font-size: 14px;
    letter-spacing: 5px;
    cursor: pointer;
    transition:
        background 0.2s,
        border-color 0.2s,
        transform 0.2s;
}

.startButton:hover {
    background: #1a1a20;
    border-color: #777780;
    transform: translateY(-2px);
}

.startButton:active {
    transform: translateY(0);
}

.controlsText {
    margin-top: 30px;
    color: #4f4f58;
    font-size: 10px;
    letter-spacing: 2px;
    line-height: 2;
}

/* =========================================================
   HUD
   ========================================================= */

#hud {
    position: absolute;
    z-index: 20;
    left: 22px;
    top: 20px;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.5s;
}

#hud.visible {
    opacity: 1;
}

.hudTitle {
    color: #777780;
    font-size: 10px;
    letter-spacing: 3px;
    margin-bottom: 7px;
}

.barContainer {
    width: 180px;
    height: 7px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 8px;
}

.bar {
    height: 100%;
    width: 100%;
    transition: width 0.15s linear;
}

#healthBar {
    background: #aaaab0;
}

#staminaBar {
    background: #696972;
}

.hudHint {
    margin-top: 15px;
    color: #5a5a63;
    font-size: 9px;
    letter-spacing: 1px;
    line-height: 1.8;
}

#objective {
    position: absolute;
    z-index: 20;
    top: 22px;
    right: 24px;
    color: #777780;
    font-size: 10px;
    letter-spacing: 2px;
    text-align: right;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.5s;
}

#objective.visible {
    opacity: 1;
}

/* =========================================================
   MESSAGE
   ========================================================= */

#messageBox {
    position: absolute;
    z-index: 30;
    left: 50%;
    bottom: 60px;
    transform: translateX(-50%);
    width: min(620px, 80vw);
    text-align: center;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s;
}

#messageBox.visible {
    opacity: 1;
}

#message {
    display: inline-block;
    padding: 12px 20px;
    color: #b6b6bd;
    background: rgba(5,5,8,0.84);
    border: 1px solid rgba(160,160,170,0.12);
    font-size: 11px;
    letter-spacing: 1px;
    line-height: 1.7;
}

/* =========================================================
   INTERACTION
   ========================================================= */

#interaction {
    position: absolute;
    z-index: 25;
    left: 50%;
    bottom: 24px;
    transform: translateX(-50%);
    color: #a5a5ad;
    font-size: 10px;
    letter-spacing: 2px;
    opacity: 0;
    pointer-events: none;
}

#interaction.visible {
    opacity: 1;
}

/* =========================================================
   GAME OVER / END
   ========================================================= */

#endScreen {
    position: absolute;
    inset: 0;
    z-index: 90;
    display: none;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(
            circle at center,
            rgba(20,20,24,0.65),
            rgba(0,0,0,0.97)
        );
}

#endScreen.visible {
    display: flex;
}

.endBox {
    text-align: center;
    width: min(650px, 88vw);
}

.endTitle {
    color: #dddde2;
    font-size: clamp(38px, 6vw, 68px);
    letter-spacing: 9px;
    margin-bottom: 20px;
}

.endText {
    color: #6f6f78;
    font-size: 12px;
    letter-spacing: 2px;
    line-height: 2;
    margin-bottom: 35px;
}

.restartButton {
    width: 190px;
    height: 50px;
    border: 1px solid #3e3e46;
    background: #101015;
    color: #aaaab2;
    font-family: inherit;
    letter-spacing: 3px;
    cursor: pointer;
}

.restartButton:hover {
    background: #18181e;
    border-color: #686870;
}

/* =========================================================
   VIGNETTE
   ========================================================= */

#vignette {
    position: absolute;
    inset: 0;
    z-index: 10;
    pointer-events: none;
    background:
        radial-gradient(
            ellipse at center,
            transparent 38%,
            rgba(0,0,0,0.18) 62%,
            rgba(0,0,0,0.70) 100%
        );
}

/* =========================================================
   NOISE
   ========================================================= */

#noiseOverlay {
    position: absolute;
    inset: 0;
    z-index: 11;
    pointer-events: none;
    opacity: 0.04;
    background-image:
        repeating-linear-gradient(
            0deg,
            rgba(255,255,255,0.15) 0px,
            rgba(255,255,255,0.15) 1px,
            transparent 1px,
            transparent 3px
        );
    mix-blend-mode: screen;
}

</style>
</head>

<body>

<div id="gameWrapper">

    <canvas id="gameCanvas"></canvas>

    <div id="vignette"></div>
    <div id="noiseOverlay"></div>

    <!-- START -->
    <div id="startScreen">

        <div class="startBox">

            <div class="logoSmall">
                A SMALL HORROR GAME
            </div>

            <h1 class="gameTitle">
                THE EMPTY HOUSE
            </h1>

            <div class="gameSubtitle">
                SOMETHING IS STILL INSIDE
            </div>

            <div class="storyText">
                밤이 되자 아무도 살지 않는 집에 불이 켜졌다.<br>
                이상하다고 생각한 <strong>학생</strong>은 집 안으로 들어간다.<br><br>

                처음에는 아무것도 없었다.<br>
                하지만 깊숙한 곳으로 들어갈수록<br>
                <strong>누군가 자신을 따라오고 있다는 느낌</strong>이 들기 시작한다.<br><br>

                열쇠를 찾아 현관으로 돌아가야 한다.
            </div>

            <button class="startButton" id="startButton">
                게임 시작
            </button>

            <div class="controlsText">
                WASD / 방향키 : 이동 &nbsp;&nbsp; SHIFT : 달리기<br>
                F : 손전등 &nbsp;&nbsp; E : 조사
            </div>

        </div>

    </div>

    <!-- HUD -->
    <div id="hud">

        <div class="hudTitle">
            CONDITION
        </div>

        <div class="barContainer">
            <div id="healthBar" class="bar"></div>
        </div>

        <div class="barContainer">
            <div id="staminaBar" class="bar"></div>
        </div>

        <div class="hudHint">
            HP<br>
            STAMINA
        </div>

    </div>

    <!-- OBJECTIVE -->
    <div id="objective">
        OBJECTIVE<br>
        <span id="objectiveText">
            집 안을 조사하라
        </span>
    </div>

    <!-- MESSAGE -->
    <div id="messageBox">
        <div id="message"></div>
    </div>

    <!-- INTERACTION -->
    <div id="interaction">
        [ E ] 조사하기
    </div>

    <!-- END -->
    <div id="endScreen">

        <div class="endBox">

            <div class="endTitle" id="endTitle">
                YOU ESCAPED
            </div>

            <div class="endText" id="endText">
                문이 열렸다.<br>
                그리고 뒤를 돌아보지 않았다.
            </div>

            <button class="restartButton" id="restartButton">
                다시 시작
            </button>

        </div>

    </div>

</div>

<script>

/* =========================================================
   CANVAS
   ========================================================= */

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

ctx.imageSmoothingEnabled = false;

let W = window.innerWidth;
let H = window.innerHeight;

function resizeCanvas() {

    W = window.innerWidth;
    H = window.innerHeight;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    canvas.width = Math.floor(W * dpr);
    canvas.height = Math.floor(H * dpr);

    canvas.style.width = W + "px";
    canvas.style.height = H + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = false;
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();


/* =========================================================
   DOM
   ========================================================= */

const startScreen = document.getElementById("startScreen");
const startButton = document.getElementById("startButton");

const hud = document.getElementById("hud");
const objective = document.getElementById("objective");
const objectiveText = document.getElementById("objectiveText");

const messageBox = document.getElementById("messageBox");
const message = document.getElementById("message");

const interaction = document.getElementById("interaction");

const healthBar = document.getElementById("healthBar");
const staminaBar = document.getElementById("staminaBar");

const endScreen = document.getElementById("endScreen");
const endTitle = document.getElementById("endTitle");
const endText = document.getElementById("endText");
const restartButton = document.getElementById("restartButton");


/* =========================================================
   GAME CONSTANTS
   ========================================================= */

const TILE = 64;

const PLAYER_RADIUS = 14;

const BASE_SPEED = 185;

const SPRINT_SPEED = 300;

const MONSTER_SPEED = 75;

const MONSTER_CHASE_SPEED = 145;

const WORLD_WIDTH = 60 * TILE;

const WORLD_HEIGHT = 60 * TILE;


/* =========================================================
   MAP
   ========================================================= */

const MAP = [

"############################################################",
"#..........................................................#",
"#..........................................................#",
"#....#########.........................#########...........#",
"#....#.......#.........................#.......#...........#",
"#....#.......#.............########....#.......#...........#",
"#....#.......#...................#.....#.......#...........#",
"#....#.......#####...............#.....#.......#####.......#",
"#....#.........................#.......#...................#",
"#....#.........................#.......#...................#",
"#....###########...............#.......###########.........#",
"#..........................................................#",
"#..........................................................#",
"#...............############...............................#",
"#...............#..........#...............................#",
"#...............#..........#....................########...#",
"#...............#..........#....................#......#...#",
"#...............#..........#....................#......#...#",
"#...............#..........##############.......#......#...#",
"#...............#........................#.......#......#...#",
"#...............#........................#.......#......#...#",
"#...............##########################.......########...#",
"#..........................................................#",
"#..........................................................#",
"#.........########.........................................#",
"#.........#......#.........................................#",
"#.........#......#.........................................#",
"#.........#......#...............#########.................#",
"#.........#......#...............#.......#.................#",
"#.........########...............#.......#.................#",
"#...............................#.......#................#",
"#...............................#########..................#",
"#..........................................................#",
"#..........................................................#",
"#.................#########................................#",
"#.................#.......#................................#",
"#.................#.......#................................#",
"#.................#.......#..........############..........#",
"#.................#.......#..........#..........#..........#",
"#.................#########..........#..........#..........#",
"#...................................#..........#..........#",
"#...................................#..........#..........#",
"#...................................############..........#",
"#..........................................................#",
"#..........................................................#",
"#.............................############.................#",
"#.............................#..........#.................#",
"#.............................#..........#.................#",
"#.............................#..........#.................#",
"#.............................############.................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"############################################################"

];


/* =========================================================
   MAP HELPERS
   ========================================================= */

function isWallAt(tx, ty) {

    if (ty < 0 || ty >= MAP.length) {
        return true;
    }

    if (tx < 0 || tx >= MAP[ty].length) {
        return true;
    }

    return MAP[ty][tx] === "#";
}


function worldToTile(x, y) {

    return {
        x: Math.floor(x / TILE),
        y: Math.floor(y / TILE)
    };

}


function circleHitsWall(x, y, radius) {

    const points = [
        [x - radius, y],
        [x + radius, y],
        [x, y - radius],
        [x, y + radius],

        [x - radius * 0.7, y - radius * 0.7],
        [x + radius * 0.7, y - radius * 0.7],
        [x - radius * 0.7, y + radius * 0.7],
        [x + radius * 0.7, y + radius * 0.7]
    ];

    for (const p of points) {

        const tile = worldToTile(p[0], p[1]);

        if (isWallAt(tile.x, tile.y)) {
            return true;
        }

    }

    return false;
}


function tryMove(entity, dx, dy) {

    const nextX = entity.x + dx;

    if (!circleHitsWall(nextX, entity.y, entity.radius)) {
        entity.x = nextX;
    }

    const nextY = entity.y + dy;

    if (!circleHitsWall(entity.x, nextY, entity.radius)) {
        entity.y = nextY;
    }
}


/* =========================================================
   PLAYER
   ========================================================= */

const player = {

    x: 6 * TILE + TILE / 2,
    y: 6 * TILE + TILE / 2,

    radius: PLAYER_RADIUS,

    health: 100,

    stamina: 100,

    flashlight: true,

    moving: false,

    sprinting: false,

    lastDX: 0,

    lastDY: 1,

    animTime: 0,

    bob: 0

};


/* =========================================================
   MONSTER
   ========================================================= */

const monster = {

    x: 43 * TILE + TILE / 2,
    y: 43 * TILE + TILE / 2,

    radius: 18,

    active: false,

    speed: MONSTER_SPEED,

    animTime: 0,

    visibleAmount: 0

};


/* =========================================================
   ITEMS
   ========================================================= */

const keyItem = {

    x: 12 * TILE + TILE / 2,

    y: 46 * TILE + TILE / 2,

    collected: false,

    pulse: 0

};


const exitDoor = {

    x: 56 * TILE + TILE / 2,

    y: 3 * TILE + TILE / 2,

    open: false

};


const note = {

    x: 30 * TILE + TILE / 2,

    y: 20 * TILE + TILE / 2,

    read: false

};


/* =========================================================
   CAMERA
   ========================================================= */

const camera = {

    x: 0,

    y: 0,

    shake: 0

};


function updateCamera() {

    const targetX = player.x - W / 2;

    const targetY = player.y - H / 2;

    camera.x += (targetX - camera.x) * 0.10;

    camera.y += (targetY - camera.y) * 0.10;

    camera.x = Math.max(
        0,
        Math.min(
            WORLD_WIDTH - W,
            camera.x
        )
    );

    camera.y = Math.max(
        0,
        Math.min(
            WORLD_HEIGHT - H,
            camera.y
        )
    );

}


/* =========================================================
   INPUT
   ========================================================= */

const keys = {};

window.addEventListener("keydown", function(e) {

    keys[e.key.toLowerCase()] = true;

    if (
        e.key.toLowerCase() === "w" ||
        e.key.toLowerCase() === "a" ||
        e.key.toLowerCase() === "s" ||
        e.key.toLowerCase() === "d" ||
        e.key === "ArrowUp" ||
        e.key === "ArrowDown" ||
        e.key === "ArrowLeft" ||
        e.key === "ArrowRight" ||
        e.key === " "
    ) {
        e.preventDefault();
    }

});


window.addEventListener("keyup", function(e) {

    keys[e.key.toLowerCase()] = false;

});


/* =========================================================
   GAME STATE
   ========================================================= */

let gameStarted = false;

let gameEnded = false;

let escaped = false;

let gameTime = 0;

let lastTime = 0;

let messageTimer = 0;

let randomEventTimer = 0;

let monsterRevealTimer = 0;

let flashTimer = 0;


/* =========================================================
   MESSAGE
   ========================================================= */

function showMessage(text, duration = 2500) {

    message.textContent = text;

    messageBox.classList.add("visible");

    messageTimer = duration;

}


function updateMessage(dt) {

    if (messageTimer > 0) {

        messageTimer -= dt * 1000;

        if (messageTimer <= 0) {
            messageBox.classList.remove("visible");
        }

    }

}


/* =========================================================
   DISTANCE
   ========================================================= */

function distance(a, b) {

    return Math.hypot(
        a.x - b.x,
        a.y - b.y
    );

}


/* =========================================================
   PLAYER UPDATE
   ========================================================= */

function updatePlayer(dt) {

    let dx = 0;
    let dy = 0;

    if (keys["w"] || keys["arrowup"]) {
        dy -= 1;
    }

    if (keys["s"] || keys["arrowdown"]) {
        dy += 1;
    }

    if (keys["a"] || keys["arrowleft"]) {
        dx -= 1;
    }

    if (keys["d"] || keys["arrowright"]) {
        dx += 1;
    }

    const moving = dx !== 0 || dy !== 0;

    player.moving = moving;

    if (moving) {

        const length = Math.hypot(dx, dy);

        dx /= length;
        dy /= length;

        player.lastDX = dx;
        player.lastDY = dy;

        player.animTime += dt * (
            keys["shift"] && player.stamina > 0
                ? 12
                : 8
        );

    }

    let sprint = false;

    if (
        moving &&
        keys["shift"] &&
        player.stamina > 0
    ) {
        sprint = true;
    }

    player.sprinting = sprint;

    let speed = BASE_SPEED;

    if (sprint) {

        speed = SPRINT_SPEED;

        player.stamina -= 32 * dt;

    } else {

        player.stamina += 20 * dt;

    }

    player.stamina = Math.max(
        0,
        Math.min(100, player.stamina)
    );

    if (moving) {

        tryMove(
            player,
            dx * speed * dt,
            dy * speed * dt
        );

    }

    player.bob = moving
        ? Math.sin(player.animTime * 1.5) * 1.4
        : 0;

}


/* =========================================================
   MONSTER UPDATE
   ========================================================= */

function updateMonster(dt) {

    if (!monster.active) {
        return;
    }

    monster.animTime += dt * 7;

    const dx = player.x - monster.x;

    const dy = player.y - monster.y;

    const dist = Math.hypot(dx, dy);

    if (dist > 1) {

        let speed = monster.speed;

        if (dist < 650) {
            speed = MONSTER_CHASE_SPEED;
        }

        if (dist < 300) {
            speed = MONSTER_CHASE_SPEED + 25;
        }

        const nx = dx / dist;

        const ny = dy / dist;

        tryMove(
            monster,
            nx * speed * dt,
            ny * speed * dt
        );

    }

    if (dist < 95) {

        player.health -= 26 * dt;

        camera.shake = Math.max(
            camera.shake,
            5
        );

        monsterRevealTimer = 250;

    }

    if (dist > 900) {

        monster.visibleAmount -= dt * 0.5;

    } else {

        monster.visibleAmount += dt * 0.8;

    }

    monster.visibleAmount = Math.max(
        0,
        Math.min(1, monster.visibleAmount)
    );

}


/* =========================================================
   ITEMS / INTERACTION
   ========================================================= */

function updateItems() {

    keyItem.pulse += 0.05;

    const keyDistance = distance(
        player,
        keyItem
    );

    const noteDistance = distance(
        player,
        note
    );

    const exitDistance = distance(
        player,
        exitDoor
    );

    interaction.classList.remove("visible");

    if (
        !keyItem.collected &&
        keyDistance < 60
    ) {

        interaction.textContent =
            "[ E ] 열쇠 줍기";

        interaction.classList.add("visible");

        if (keys["e"]) {

            keyItem.collected = true;

            showMessage(
                "낡은 열쇠를 발견했다.",
                2600
            );

            objectiveText.textContent =
                "현관으로 돌아가라";

            keys["e"] = false;

        }

    } else if (
        !note.read &&
        noteDistance < 70
    ) {

        interaction.textContent =
            "[ E ] 메모 조사";

        interaction.classList.add("visible");

        if (keys["e"]) {

            note.read = true;

            showMessage(
                "「여기에는 아무도 없어야 한다.」",
                4000
            );

            keys["e"] = false;

        }

    } else if (
        exitDistance < 75
    ) {

        interaction.textContent =
            keyItem.collected
                ? "[ E ] 문 열기"
                : "열쇠가 필요하다";

        interaction.classList.add("visible");

        if (
            keys["e"] &&
            keyItem.collected
        ) {

            exitDoor.open = true;

            keys["e"] = false;

            finishGame(true);

        }

    }

}


/* =========================================================
   FLASHLIGHT
   ========================================================= */

function updateFlashlight() {

    if (keys["f"]) {

        player.flashlight =
            !player.flashlight;

        keys["f"] = false;

        showMessage(
            player.flashlight
                ? "손전등을 켰다."
                : "손전등을 껐다.",
            1200
        );

    }

}


/* =========================================================
   RANDOM EVENTS
   ========================================================= */

function updateRandomEvents(dt) {

    randomEventTimer += dt;

    if (randomEventTimer > 5) {

        randomEventTimer = 0;

        if (
            gameTime > 8 &&
            Math.random() < 0.30
        ) {

            const events = [

                "어딘가에서 작은 소리가 났다.",

                "바닥이 살짝 삐걱거렸다.",

                "뒤쪽에서 무언가 움직인 것 같다.",

                "집 안이 갑자기 조용해졌다.",

                "멀리서 문이 닫히는 소리가 들렸다."

            ];

            showMessage(
                events[
                    Math.floor(
                        Math.random() * events.length
                    )
                ],
                2200
            );

        }

    }

}


/* =========================================================
   MONSTER ACTIVATION
   ========================================================= */

function checkMonsterActivation() {

    if (
        !monster.active &&
        gameTime > 12
    ) {

        const d = distance(
            player,
            monster
        );

        if (d < 850) {

            monster.active = true;

            showMessage(
                "……방금 뭔가 움직였다.",
                3200
            );

            objectiveText.textContent =
                keyItem.collected
                    ? "현관으로 도망쳐라"
                    : "열쇠를 찾아라";

        }

    }

}


/* =========================================================
   DRAW HELPERS
   ========================================================= */

function px(x, y, size, color) {

    ctx.fillStyle = color;

    ctx.fillRect(
        Math.round(x),
        Math.round(y),
        size,
        size
    );

}


function pixelSprite(
    sprite,
    x,
    y,
    scale,
    palette
) {

    const rows = sprite.length;

    const cols = sprite[0].length;

    const width = cols * scale;

    const height = rows * scale;

    const startX = Math.round(
        x - width / 2
    );

    const startY = Math.round(
        y - height / 2
    );

    for (let row = 0; row < rows; row++) {

        const line = sprite[row];

        for (
            let col = 0;
            col < cols;
            col++
        ) {

            const key = line[col];

            if (
                key === "." ||
                !palette[key]
            ) {
                continue;
            }

            px(
                startX + col * scale,
                startY + row * scale,
                scale,
                palette[key]
            );

        }

    }

}


/* =========================================================
   PLAYER PIXEL SPRITES
   ========================================================= */

const PLAYER_PALETTE = {

    H: "#17171d",
    h: "#292932",

    S: "#e6b99a",
    s: "#d49d7d",

    W: "#e4e4e7",

    U: "#30343e",
    u: "#20232b",

    T: "#8b3940",

    B: "#171a21",

    L: "#252831",

    K: "#0c0d11",

    P: "#4b342b"

};


const PLAYER_FRAMES = [

    [
        "....HHHH....",
        "...HHHHHH...",
        "..HHSSSSHH..",
        "..HSSSSSSH..",
        "..HSSSSSSH..",
        "...HHHHHH...",
        "....WWWW....",
        "...WTTTTW...",
        "...UUUUUU...",
        "..UUUUUUUU..",
        "..UULLLLUU..",
        "..LL....LL..",
        ".LLK....KLL.",
        ".LLK....KLL."
    ],

    [
        "....HHHH....",
        "...HHHHHH...",
        "..HHSSSSHH..",
        "..HSSSSSSH..",
        "..HSSSSSSH..",
        "...HHHHHH...",
        "....WWWW....",
        "...WTTTTW...",
        "...UUUUUU...",
        "..UUUUUUUU..",
        "..UULLLLUU..",
        "...LL..LL...",
        "..LLK..KLL..",
        "..LLK..KLL.."
    ],

    [
        "....HHHH....",
        "...HHHHHH...",
        "..HHSSSSHH..",
        "..HSSSSSSH..",
        "..HSSSSSSH..",
        "...HHHHHH...",
        "....WWWW....",
        "...WTTTTW...",
        "...UUUUUU...",
        "..UUUUUUUU..",
        "..UULLLLUU..",
        ".LL....LL...",
        ".LLK....KLL.",
        ".LLK....KLL."
    ],

    [
        "....HHHH....",
        "...HHHHHH...",
        "..HHSSSSHH..",
        "..HSSSSSSH..",
        "..HSSSSSSH..",
        "...HHHHHH...",
        "....WWWW....",
        "...WTTTTW...",
        "...UUUUUU...",
        "..UUUUUUUU..",
        "..UULLLLUU..",
        "...LL..LL...",
        "..LLK..KLL..",
        "..LLK..KLL.."
    ]

];


/* =========================================================
   MONSTER PIXEL SPRITES
   ========================================================= */

const MONSTER_PALETTE = {

    H: "#09090c",
    h: "#15151b",

    F: "#b7b2aa",

    f: "#817d78",

    E: "#9e3238",

    B: "#111117",

    b: "#1b1b22",

    A: "#292931",

    L: "#09090c",

    G: "#3b3b42"

};


const MONSTER_FRAMES = [

    [
        "......HHHH......",
        "....HHHHHHHH....",
        "...HHHHHHHHHH...",
        "..HHHFFFFFFFFHH..",
        "..HHFFFFFFFFFFHH..",
        ".HHFFFEFFFFEFFFHH.",
        ".HHFFFFFFFFFFFFHH.",
        ".HHFFFFFFFFFFFFHH.",
        "..HHFFFFFFFFFFHH..",
        "..HHHHBBBBHHHHHH..",
        "...HHHBBBBHHHH....",
        "...HHHBBBBHHHH....",
        "..HHHBBBBBBHHH....",
        ".HHHHHBBBBHHHHH...",
        "HHHHHHBBBBHHHHHH..",
        "...HHHBBBBHHH.....",
        "...HHHLLLLHHH.....",
        "..HHHHLLLLHHHH....",
        ".HHHHHLLLLHHHHH...",
        ".HHHHHLLLLHHHHH..."
    ],

    [
        "......HHHH......",
        "....HHHHHHHH....",
        "...HHHHHHHHHH...",
        "..HHHFFFFFFFFHH..",
        "..HHFFFFFFFFFFHH..",
        ".HHFFFEFFFFEFFFHH.",
        ".HHFFFFFFFFFFFFHH.",
        ".HHFFFFFFFFFFFFHH.",
        "..HHFFFFFFFFFFHH..",
        "..HHHHBBBBHHHHHH..",
        "...HHHBBBBHHHH....",
        "..HHHBBBBBBHHH....",
        ".HHHHBBBBBBHHHH...",
        "HHHHHHBBBBHHHHHH..",
        "...HHHBBBBHHH.....",
        "..HHHLLLLLLHHH....",
        ".HHHHHLLLLHHHHH...",
        ".HHHHHLLLLHHHHH...",
        "..HHHHLLLLHHHH....",
        "...HHHLLLLHHH....."
    ],

    [
        "......HHHH......",
        "....HHHHHHHH....",
        "...HHHHHHHHHH...",
        "..HHHFFFFFFFFHH..",
        "..HHFFFFFFFFFFHH..",
        ".HHFFFEFFFFEFFFHH.",
        ".HHFFFFFFFFFFFFHH.",
        ".HHFFFFFFFFFFFFHH.",
        "..HHFFFFFFFFFFHH..",
        "..HHHHBBBBHHHHHH..",
        "...HHHBBBBHHHH....",
        "...HHHBBBBHHHH....",
        "..HHHBBBBBBHHH....",
        ".HHHHHBBBBHHHHH...",
        "HHHHHHBBBBHHHHHH..",
        "..HHHLLLLLLHHH....",
        ".HHHHHLLLLHHHHH...",
        ".HHHHHLLLLHHHHH...",
        "..HHHHLLLLHHHH....",
        "...HHHLLLLHHH....."
    ]

];


/* =========================================================
   DRAW PLAYER
   ========================================================= */

function drawPlayer() {

    const screenX =
        player.x - camera.x;

    const screenY =
        player.y - camera.y + player.bob;

    const moving =
        player.moving;

    let frameIndex = 0;

    if (moving) {

        frameIndex =
            Math.floor(
                player.animTime
            ) % PLAYER_FRAMES.length;

    }

    const sprite =
        PLAYER_FRAMES[frameIndex];

    /*
       아주 작은 픽셀 학생 캐릭터.
       실제 충돌 반경은 14px이지만
       화면에서는 약 36px 정도로 보인다.
    */

    const scale = 3;

    /*
       바닥 그림자도 거대한 원 대신
       작은 픽셀 타원처럼 표현한다.
    */

    ctx.save();

    ctx.fillStyle =
        "rgba(0,0,0,0.35)";

    ctx.fillRect(
        Math.round(screenX - 14),
        Math.round(screenY + 19),
        28,
        4
    );

    pixelSprite(
        sprite,
        screenX,
        screenY,
        scale,
        PLAYER_PALETTE
    );

    /*
       손전등을 들고 있는 느낌의 작은 픽셀
    */

    if (player.flashlight) {

        const handX =
            screenX +
            (player.lastDX >= 0 ? 17 : -20);

        const handY =
            screenY + 5;

        px(
            handX,
            handY,
            3,
            "#b8b8bd"
        );

    }

    ctx.restore();

}


/* =========================================================
   DRAW MONSTER
   ========================================================= */

function drawMonster() {

    if (!monster.active) {
        return;
    }

    const screenX =
        monster.x - camera.x;

    const screenY =
        monster.y - camera.y;

    const frameIndex =
        Math.floor(
            monster.animTime
        ) % MONSTER_FRAMES.length;

    const sprite =
        MONSTER_FRAMES[frameIndex];

    const scale = 3;

    ctx.save();

    /*
       몬스터 그림자
    */

    ctx.fillStyle =
        "rgba(0,0,0,0.55)";

    ctx.fillRect(
        Math.round(screenX - 23),
        Math.round(screenY + 29),
        46,
        5
    );

    /*
       아주 약한 주변 어둠
    */

    const glow =
        ctx.createRadialGradient(
            screenX,
            screenY,
            5,
            screenX,
            screenY,
            75
        );

    glow.addColorStop(
        0,
        "rgba(80,20,25,0.16)"
    );

    glow.addColorStop(
        1,
        "rgba(0,0,0,0)"
    );

    ctx.fillStyle = glow;

    ctx.fillRect(
        screenX - 75,
        screenY - 75,
        150,
        150
    );

    pixelSprite(
        sprite,
        screenX,
        screenY,
        scale,
        MONSTER_PALETTE
    );

    ctx.restore();

}


/* =========================================================
   FLOOR
   ========================================================= */

function drawFloor() {

    const startX =
        Math.floor(camera.x / TILE) - 1;

    const endX =
        Math.ceil(
            (camera.x + W) / TILE
        ) + 1;

    const startY =
        Math.floor(camera.y / TILE) - 1;

    const endY =
        Math.ceil(
            (camera.y + H) / TILE
        ) + 1;

    for (
        let ty = startY;
        ty <= endY;
        ty++
    ) {

        for (
            let tx = startX;
            tx <= endX;
            tx++
        ) {

            if (
                ty < 0 ||
                ty >= MAP.length ||
                tx < 0 ||
                tx >= MAP[ty].length
            ) {
                continue;
            }

            const sx =
                tx * TILE - camera.x;

            const sy =
                ty * TILE - camera.y;

            if (isWallAt(tx, ty)) {

                ctx.fillStyle = "#15151a";

                ctx.fillRect(
                    sx,
                    sy,
                    TILE,
                    TILE
                );

                /*
                   벽 위쪽 픽셀 하이라이트
                */

                ctx.fillStyle =
                    "#202027";

                ctx.fillRect(
                    sx,
                    sy,
                    TILE,
                    2
                );

                /*
                   벽 아래쪽 어두운 픽셀
                */

                ctx.fillStyle =
                    "#0b0b0e";

                ctx.fillRect(
                    sx,
                    sy + TILE - 4,
                    TILE,
                    4
                );

            } else {

                ctx.fillStyle = "#29292d";

                ctx.fillRect(
                    sx,
                    sy,
                    TILE,
                    TILE
                );

                /*
                   바닥 타일의 미세한 픽셀 패턴
                */

                ctx.fillStyle =
                    "rgba(255,255,255,0.018)";

                const pattern =
                    (tx * 17 + ty * 23) % 4;

                if (pattern === 0) {

                    ctx.fillRect(
                        sx + 12,
                        sy + 17,
                        3,
                        3
                    );

                    ctx.fillRect(
                        sx + 43,
                        sy + 46,
                        2,
                        2
                    );

                } else if (pattern === 1) {

                    ctx.fillRect(
                        sx + 28,
                        sy + 12,
                        2,
                        2
                    );

                    ctx.fillRect(
                        sx + 49,
                        sy + 31,
                        3,
                        2
                    );

                }

                ctx.strokeStyle =
                    "rgba(0,0,0,0.08)";

                ctx.strokeRect(
                    sx,
                    sy,
                    TILE,
                    TILE
                );

            }

        }

    }

}


/* =========================================================
   DRAW KEY
   ========================================================= */

function drawKey() {

    if (keyItem.collected) {
        return;
    }

    const sx =
        keyItem.x - camera.x;

    const sy =
        keyItem.y - camera.y;

    const pulse =
        Math.sin(
            keyItem.pulse
        ) * 2;

    ctx.save();

    ctx.fillStyle =
        "rgba(190,190,170,0.07)";

    ctx.fillRect(
        sx - 18 - pulse,
        sy - 18 - pulse,
        36 + pulse * 2,
        36 + pulse * 2
    );

    /*
       픽셀 열쇠
    */

    px(
        sx - 9,
        sy - 3,
        6,
        "#b3b09b"
    );

    px(
        sx - 3,
        sy - 3,
        6,
        "#b3b09b"
    );

    px(
        sx + 3,
        sy - 3,
        6,
        "#b3b09b"
    );

    px(
        sx + 7,
        sy - 9,
        5,
        "#b3b09b"
    );

    px(
        sx + 7,
        sy + 3,
        5,
        "#b3b09b"
    );

    ctx.restore();

}


/* =========================================================
   DRAW NOTE
   ========================================================= */

function drawNote() {

    if (note.read) {
        return;
    }

    const sx =
        note.x - camera.x;

    const sy =
        note.y - camera.y;

    ctx.save();

    /*
       종이
    */

    ctx.fillStyle =
        "#b7b2a4";

    ctx.fillRect(
        sx - 10,
        sy - 13,
        20,
        26
    );

    /*
       종이 픽셀
    */

    ctx.fillStyle =
        "#6c6961";

    ctx.fillRect(
        sx - 6,
        sy - 7,
        12,
        2
    );

    ctx.fillRect(
        sx - 6,
        sy - 2,
        10,
        2
    );

    ctx.fillRect(
        sx - 6,
        sy + 3,
        12,
        2
    );

    ctx.restore();

}


/* =========================================================
   DRAW EXIT
   ========================================================= */

function drawExit() {

    const sx =
        exitDoor.x - camera.x;

    const sy =
        exitDoor.y - camera.y;

    ctx.save();

    /*
       문틀
    */

    ctx.fillStyle =
        "#09090c";

    ctx.fillRect(
        sx - 25,
        sy - 37,
        50,
        74
    );

    /*
       문
    */

    ctx.fillStyle =
        exitDoor.open
            ? "#35353b"
            : "#1c1c21";

    ctx.fillRect(
        sx - 20,
        sy - 32,
        40,
        64
    );

    /*
       문 손잡이
    */

    px(
        sx + 10,
        sy - 1,
        4,
        "#8a8780"
    );

    /*
       출구 표식
    */

    if (!exitDoor.open) {

        ctx.fillStyle =
            "rgba(170,170,180,0.6)";

        ctx.fillRect(
            sx - 7,
            sy - 20,
            14,
            2
        );

        ctx.fillRect(
            sx - 7,
            sy - 16,
            14,
            2
        );

    }

    ctx.restore();

}


/* =========================================================
   DRAW DARKNESS
   ========================================================= */

function drawDarkness() {

    const pxScreen =
        player.x - camera.x;

    const pyScreen =
        player.y - camera.y;

    /*
       전체 어둠
    */

    ctx.save();

    ctx.fillStyle =
        "rgba(0,0,0,0.74)";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    /*
       손전등을 껐으면 조금 더 어둡게
    */

    if (!player.flashlight) {

        ctx.fillStyle =
            "rgba(0,0,0,0.17)";

        ctx.fillRect(
            0,
            0,
            W,
            H
        );

        ctx.restore();

        return;
    }

    /*
       손전등 빛
    */

    const lightRadius =
        player.sprinting
            ? 225
            : 195;

    const gradient =
        ctx.createRadialGradient(
            pxScreen,
            pyScreen,
            15,
            pxScreen,
            pyScreen,
            lightRadius
        );

    gradient.addColorStop(
        0,
        "rgba(0,0,0,0.02)"
    );

    gradient.addColorStop(
        0.25,
        "rgba(0,0,0,0.05)"
    );

    gradient.addColorStop(
        0.55,
        "rgba(0,0,0,0.30)"
    );

    gradient.addColorStop(
        0.80,
        "rgba(0,0,0,0.70)"
    );

    gradient.addColorStop(
        1,
        "rgba(0,0,0,0.96)"
    );

    ctx.globalCompositeOperation =
        "destination-out";

    ctx.fillStyle =
        gradient;

    ctx.beginPath();

    ctx.arc(
        pxScreen,
        pyScreen,
        lightRadius,
        0,
        Math.PI * 2
    );

    ctx.fill();

    /*
       손전등의 중심은 완전히 밝게
    */

    const center =
        ctx.createRadialGradient(
            pxScreen,
            pyScreen,
            1,
            pxScreen,
            pyScreen,
            65
        );

    center.addColorStop(
        0,
        "rgba(0,0,0,0.90)"
    );

    center.addColorStop(
        1,
        "rgba(0,0,0,0)"
    );

    ctx.fillStyle = center;

    ctx.beginPath();

    ctx.arc(
        pxScreen,
        pyScreen,
        65,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();

}


/* =========================================================
   DRAW SCREEN FLASH
   ========================================================= */

function drawFlash() {

    if (flashTimer <= 0) {
        return;
    }

    ctx.save();

    ctx.fillStyle =
        "rgba(255,255,255," +
        Math.min(
            0.18,
            flashTimer / 1000
        ) +
        ")";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    ctx.restore();

}


/* =========================================================
   DRAW PIXEL NOISE
   ========================================================= */

function drawNoise() {

    ctx.save();

    ctx.globalAlpha = 0.035;

    for (let i = 0; i < 120; i++) {

        const x =
            Math.random() * W;

        const y =
            Math.random() * H;

        const size =
            Math.random() < 0.8
                ? 1
                : 2;

        ctx.fillStyle =
            Math.random() < 0.5
                ? "#ffffff"
                : "#000000";

        ctx.fillRect(
            x,
            y,
            size,
            size
        );

    }

    ctx.restore();

}


/* =========================================================
   DRAW WORLD
   ========================================================= */

function drawWorld() {

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    ctx.fillStyle =
        "#07070a";

    ctx.fillRect(
        0,
        0,
        W,
        H
    );

    updateCamera();

    const shakeX =
        camera.shake > 0
            ? (Math.random() - 0.5) *
              camera.shake
            : 0;

    const shakeY =
        camera.shake > 0
            ? (Math.random() - 0.5) *
              camera.shake
            : 0;

    ctx.save();

    ctx.translate(
        shakeX,
        shakeY
    );

    drawFloor();

    drawExit();

    drawKey();

    drawNote();

    drawMonster();

    drawPlayer();

    ctx.restore();

    drawDarkness();

    drawFlash();

    drawNoise();

}


/* =========================================================
   UI UPDATE
   ========================================================= */

function updateUI() {

    healthBar.style.width =
        Math.max(
            0,
            player.health
        ) + "%";

    staminaBar.style.width =
        player.stamina + "%";

    if (keyItem.collected) {

        objectiveText.textContent =
            "현관으로 돌아가라";

    } else {

        objectiveText.textContent =
            "집 안을 조사하라";

    }

}


/* =========================================================
   GAME OVER
   ========================================================= */

function checkGameOver() {

    if (
        player.health <= 0 &&
        !gameEnded
    ) {

        finishGame(false);

    }

}


/* =========================================================
   END GAME
   ========================================================= */

function finishGame(success) {

    gameEnded = true;

    escaped = success;

    if (success) {

        endTitle.textContent =
            "YOU ESCAPED";

        endText.innerHTML =
            "문이 열렸다.<br>" +
            "그리고 뒤를 돌아보지 않았다.";

    } else {

        endTitle.textContent =
            "YOU WERE TOO LATE";

        endText.innerHTML =
            "집 안에는 아무도 없었다.<br>" +
            "적어도 처음에는 그랬다.";

    }

    setTimeout(
        function() {

            endScreen.classList.add(
                "visible"
            );

        },
        800
    );

}


/* =========================================================
   RESET GAME
   ========================================================= */

function resetGame() {

    player.x =
        6 * TILE + TILE / 2;

    player.y =
        6 * TILE + TILE / 2;

    player.health = 100;

    player.stamina = 100;

    player.flashlight = true;

    player.moving = false;

    player.sprinting = false;

    player.lastDX = 0;

    player.lastDY = 1;

    player.animTime = 0;

    player.bob = 0;

    monster.x =
        43 * TILE + TILE / 2;

    monster.y =
        43 * TILE + TILE / 2;

    monster.active = false;

    monster.animTime = 0;

    monster.visibleAmount = 0;

    keyItem.collected = false;

    keyItem.pulse = 0;

    note.read = false;

    exitDoor.open = false;

    camera.x = 0;

    camera.y = 0;

    camera.shake = 0;

    gameTime = 0;

    messageTimer = 0;

    randomEventTimer = 0;

    monsterRevealTimer = 0;

    flashTimer = 0;

    gameEnded = false;

    escaped = false;

    objectiveText.textContent =
        "집 안을 조사하라";

    messageBox.classList.remove(
        "visible"
    );

    endScreen.classList.remove(
        "visible"
    );

}


/* =========================================================
   START
   ========================================================= */

startButton.addEventListener(
    "click",
    function() {

        resetGame();

        gameStarted = true;

        startScreen.classList.add(
            "hidden"
        );

        hud.classList.add(
            "visible"
        );

        objective.classList.add(
            "visible"
        );

        showMessage(
            "집 안을 조사하라.",
            3000
        );

        lastTime =
            performance.now();

    }
);


/* =========================================================
   RESTART
   ========================================================= */

restartButton.addEventListener(
    "click",
    function() {

        resetGame();

        endScreen.classList.remove(
            "visible"
        );

        gameStarted = true;

        hud.classList.add(
            "visible"
        );

        objective.classList.add(
            "visible"
        );

        showMessage(
            "다시 시작했다.",
            2000
        );

        lastTime =
            performance.now();

    }
);


/* =========================================================
   MAIN LOOP
   ========================================================= */

function loop(timestamp) {

    if (!lastTime) {
        lastTime = timestamp;
    }

    let dt =
        (timestamp - lastTime) / 1000;

    lastTime = timestamp;

    dt = Math.min(
        dt,
        0.033
    );

    if (gameStarted && !gameEnded) {

        gameTime += dt;

        updatePlayer(dt);

        updateMonster(dt);

        updateItems();

        updateFlashlight();

        updateRandomEvents(dt);

        checkMonsterActivation();

        updateMessage(dt);

        updateUI();

        checkGameOver();

        if (camera.shake > 0) {

            camera.shake -=
                dt * 15;

            if (camera.shake < 0) {
                camera.shake = 0;
            }

        }

        if (flashTimer > 0) {

            flashTimer -=
                dt * 1000;

        }

    }

    drawWorld();

    requestAnimationFrame(loop);

}

requestAnimationFrame(loop);


/* =========================================================
   INITIAL DRAW
   ========================================================= */

drawWorld();


/* =========================================================
   EXTRA AMBIENCE
   ========================================================= */

let ambientPulse = 0;

function ambienceLoop() {

    ambientPulse += 0.02;

    if (
        gameStarted &&
        !gameEnded &&
        monster.active
    ) {

        const d =
            distance(
                player,
                monster
            );

        if (
            d < 500 &&
            Math.random() < 0.002
        ) {

            flashTimer = 120;

        }

    }

    requestAnimationFrame(
        ambienceLoop
    );

}

ambienceLoop();


/* =========================================================
   PREVENT CONTEXT MENU
   ========================================================= */

window.addEventListener(
    "contextmenu",
    function(e) {
        e.preventDefault();
    }
);


/* =========================================================
   VISIBILITY
   ========================================================= */

document.addEventListener(
    "visibilitychange",
    function() {

        if (
            document.hidden
        ) {

            for (
                const key in keys
            ) {
                keys[key] = false;
            }

        }

    }
);

</script>

</body>
</html>
"""

components.html(
    GAME_HTML,
    height=850,
    scrolling=False
)
