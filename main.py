import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="THE EMPTY HOUSE",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# THE EMPTY HOUSE
# Real-time WASD Horror Game
# Single-file Streamlit Application
# ============================================================

GAME_HTML = r"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

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
    background: #000;
    font-family: Arial, "Malgun Gothic", sans-serif;
    user-select: none;
}

body {
    color: #ddd;
}

#gameWrapper {
    position: fixed;
    inset: 0;
    background: #000;
    overflow: hidden;
}

#gameCanvas {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: #090909;
    cursor: crosshair;
}

#hud {
    position: absolute;
    inset: 0;
    pointer-events: none;
}

#topLeft {
    position: absolute;
    left: 22px;
    top: 20px;
    color: #aaa;
    font-size: 14px;
    text-shadow: 0 2px 4px #000;
}

#healthOuter {
    width: 180px;
    height: 9px;
    margin-top: 7px;
    border: 1px solid #555;
    background: #111;
}

#healthInner {
    width: 100%;
    height: 100%;
    background: #777;
    transition: width .15s;
}

#objective {
    position: absolute;
    right: 22px;
    top: 20px;
    text-align: right;
    color: #aaa;
    font-size: 14px;
    text-shadow: 0 2px 4px #000;
}

#interaction {
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 18px;
    background: rgba(0,0,0,.75);
    border: 1px solid #555;
    color: #ddd;
    font-size: 14px;
    opacity: 0;
    transition: opacity .15s;
}

#message {
    position: absolute;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%);
    min-width: 300px;
    max-width: 700px;
    text-align: center;
    color: #bbb;
    font-size: 15px;
    text-shadow: 0 2px 5px #000;
    opacity: 0;
    transition: opacity .25s;
}

#centerText {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    pointer-events: none;
}

#centerText .big {
    font-size: 54px;
    letter-spacing: 12px;
    font-weight: bold;
}

#centerText .small {
    margin-top: 15px;
    color: #999;
    font-size: 15px;
    letter-spacing: 3px;
}

#startScreen,
#gameOverScreen,
#escapeScreen {
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background:
        radial-gradient(
            circle at center,
            rgba(35,35,35,.55),
            rgba(0,0,0,.98)
        );
    z-index: 20;
}

.screenBox {
    width: min(700px, 90%);
    text-align: center;
}

.title {
    font-size: clamp(42px, 7vw, 82px);
    font-weight: 900;
    letter-spacing: 14px;
    color: #ddd;
    text-shadow:
        0 0 5px #fff2,
        0 0 30px #000;
}

.subtitle {
    margin-top: 12px;
    color: #666;
    letter-spacing: 5px;
    font-size: 13px;
}

.story {
    margin: 45px auto 30px;
    max-width: 570px;
    line-height: 2;
    color: #aaa;
    font-size: 15px;
}

button {
    border: 1px solid #555;
    background: #111;
    color: #ccc;
    padding: 13px 35px;
    font-size: 15px;
    cursor: pointer;
}

button:hover {
    background: #222;
    color: white;
}

.controls {
    margin-top: 25px;
    color: #555;
    font-size: 12px;
    line-height: 2;
}

#gameOverScreen,
#escapeScreen {
    display: none;
}

#gameOverScreen .title {
    color: #722020;
}

#escapeScreen .title {
    color: #9aa99d;
}

#vignette {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
        radial-gradient(
            circle,
            transparent 25%,
            rgba(0,0,0,.15) 50%,
            rgba(0,0,0,.75) 100%
        );
    z-index: 5;
}

#redOverlay {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: rgba(90,0,0,0);
    z-index: 6;
}

#noise {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 7;
    opacity: 0;
    background-image:
        repeating-linear-gradient(
            0deg,
            rgba(255,255,255,.025) 0px,
            rgba(255,255,255,.025) 1px,
            transparent 1px,
            transparent 4px
        );
}

#pauseScreen {
    position: absolute;
    inset: 0;
    display: none;
    justify-content: center;
    align-items: center;
    background: rgba(0,0,0,.75);
    z-index: 15;
}

.pauseText {
    color: #aaa;
    font-size: 25px;
    letter-spacing: 8px;
}

</style>

</head>

<body>

<div id="gameWrapper">

<canvas id="gameCanvas"></canvas>

<div id="hud">

    <div id="topLeft">
        체력
        <div id="healthOuter">
            <div id="healthInner"></div>
        </div>
    </div>

    <div id="objective">
        <div id="objectiveText">
            집 밖으로 나가야 한다.
        </div>
    </div>

    <div id="interaction">
        E
    </div>

    <div id="message"></div>

</div>

<div id="vignette"></div>
<div id="redOverlay"></div>
<div id="noise"></div>

<div id="startScreen">

    <div class="screenBox">

        <div class="title">
            THE EMPTY HOUSE
        </div>

        <div class="subtitle">
            SOMETHING IS STILL INSIDE
        </div>

        <div class="story">

            새벽 2시 17분.<br>
            정신을 차리자 낯선 집 안에 있었다.<br>
            휴대폰은 작동하지 않는다.<br>
            현관문은 잠겨 있다.<br><br>

            그리고 어딘가에서<br>
            발소리가 들린다.

        </div>

        <button id="startButton">
            게임 시작
        </button>

        <div class="controls">
            WASD — 이동<br>
            E — 상호작용<br>
            SHIFT — 달리기<br>
            F — 손전등
        </div>

    </div>

</div>

<div id="gameOverScreen">

    <div class="screenBox">

        <div class="title">
            CAUGHT
        </div>

        <div class="story">
            뒤에서 들리던 발소리가 멈췄다.<br><br>
            너무 조용하다.
        </div>

        <button id="restartButton">
            다시 시작
        </button>

    </div>

</div>

<div id="escapeScreen">

    <div class="screenBox">

        <div class="title">
            ESCAPED
        </div>

        <div class="story">
            문이 열렸다.<br><br>
            차가운 공기가 들어온다.<br><br>
            당신은 집 밖으로 나왔다.<br><br>
            하지만 2층 창문을 바라본 순간,
            누군가 서 있는 것이 보였다.
        </div>

        <button id="escapeRestartButton">
            다시 시작
        </button>

    </div>

</div>

<div id="pauseScreen">
    <div class="pauseText">
        PAUSED
    </div>
</div>

<script>

// ============================================================
// CANVAS
// ============================================================

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let W = window.innerWidth;
let H = window.innerHeight;

function resizeCanvas() {

    W = window.innerWidth;
    H = window.innerHeight;

    canvas.width = W;
    canvas.height = H;
}

window.addEventListener("resize", resizeCanvas);

resizeCanvas();


// ============================================================
// GAME CONSTANTS
// ============================================================

const TILE = 64;

const MAP = [

"############################################################",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..............###########.................................#",
"#..............#.........#.................................#",
"#..............#.........#.................................#",
"#..............#.........#.................................#",
"#..............#.........#.................................#",
"#..............#.........#.................................#",
"#..............#.........#.................................#",
"#..............#.........#.................................#",
"#..............###########.................................#",
"#..........................................................#",
"#..........................................................#",
"#........#######################...........................#",
"#........#.....................#...........................#",
"#........#.....................#...........................#",
"#........#.....................#...........................#",
"#........#.....................#...........................#",
"#........#.....................#...........................#",
"#........#.....................#...........................#",
"#........#######################...........................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#....................###########...........................#",
"#....................#.........#...........................#",
"#....................#.........#...........................#",
"#....................#.........#...........................#",
"#....................#.........#...........................#",
"#....................#.........#...........................#",
"#....................#.........#...........................#",
"#....................###########...........................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"#..........................................................#",
"############################################################"

];

const MAP_H = MAP.length;
const MAP_W = MAP[0].length;

const WORLD_W = MAP_W * TILE;
const WORLD_H = MAP_H * TILE;


// ============================================================
// GAME STATE
// ============================================================

let gameStarted = false;
let gameOver = false;
let escaped = false;
let paused = false;

let keys = {};

let player = {
    x: 6 * TILE,
    y: 6 * TILE,
    radius: 15,
    speed: 180,
    health: 100,
    flashlight: true,
    stamina: 100
};

let monster = {
    x: 43 * TILE,
    y: 43 * TILE,
    radius: 22,
    speed: 78,
    chaseSpeed: 145,
    active: false,
    anger: 0
};

let keyItem = {
    x: 12 * TILE,
    y: 46 * TILE,
    collected: false
};

let exitDoor = {
    x: 56 * TILE,
    y: 3 * TILE,
    radius: 30,
    open: false
};

let note = {
    x: 30 * TILE,
    y: 20 * TILE,
    found: false
};

let camera = {
    x: 0,
    y: 0,
    shake: 0
};

let timePlayed = 0;
let lastTime = performance.now();

let messageTimer = 0;
let randomEventTimer = 8;

let footstepTimer = 0;
let heartbeatTimer = 0;

let flicker = 0;


// ============================================================
// AUDIO
// ============================================================

let audioContext = null;

function initAudio() {

    if (!audioContext) {

        try {
            audioContext =
                new (window.AudioContext ||
                window.webkitAudioContext)();
        }

        catch (e) {
            audioContext = null;
        }
    }
}

function beep(
    frequency,
    duration,
    volume,
    type = "sine"
) {

    if (!audioContext) return;

    try {

        const oscillator =
            audioContext.createOscillator();

        const gain =
            audioContext.createGain();

        oscillator.type = type;

        oscillator.frequency.value =
            frequency;

        gain.gain.setValueAtTime(
            volume,
            audioContext.currentTime
        );

        gain.gain.exponentialRampToValueAtTime(
            0.001,
            audioContext.currentTime + duration
        );

        oscillator.connect(gain);
        gain.connect(audioContext.destination);

        oscillator.start();

        oscillator.stop(
            audioContext.currentTime + duration
        );
    }

    catch (e) {}

}


// ============================================================
// UI
// ============================================================

const startScreen =
    document.getElementById("startScreen");

const gameOverScreen =
    document.getElementById("gameOverScreen");

const escapeScreen =
    document.getElementById("escapeScreen");

const pauseScreen =
    document.getElementById("pauseScreen");

const messageElement =
    document.getElementById("message");

const interactionElement =
    document.getElementById("interaction");

const objectiveElement =
    document.getElementById("objectiveText");

const healthElement =
    document.getElementById("healthInner");

const redOverlay =
    document.getElementById("redOverlay");

const noiseElement =
    document.getElementById("noise");


// ============================================================
// MESSAGES
// ============================================================

function showMessage(text, duration = 3) {

    messageElement.innerHTML = text;

    messageElement.style.opacity = "1";

    messageTimer = duration;
}

function updateMessage(dt) {

    if (messageTimer > 0) {

        messageTimer -= dt;

        if (messageTimer <= 0) {
            messageElement.style.opacity = "0";
        }
    }
}


// ============================================================
// MAP COLLISION
// ============================================================

function isWall(tx, ty) {

    if (
        tx < 0 ||
        ty < 0 ||
        tx >= MAP_W ||
        ty >= MAP_H
    ) {
        return true;
    }

    return MAP[ty][tx] === "#";
}

function circleHitsWall(x, y, radius) {

    const left =
        Math.floor((x - radius) / TILE);

    const right =
        Math.floor((x + radius) / TILE);

    const top =
        Math.floor((y - radius) / TILE);

    const bottom =
        Math.floor((y + radius) / TILE);

    for (
        let ty = top;
        ty <= bottom;
        ty++
    ) {

        for (
            let tx = left;
            tx <= right;
            tx++
        ) {

            if (isWall(tx, ty)) {

                const rx = tx * TILE;
                const ry = ty * TILE;

                const closestX =
                    Math.max(
                        rx,
                        Math.min(x, rx + TILE)
                    );

                const closestY =
                    Math.max(
                        ry,
                        Math.min(y, ry + TILE)
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
    }

    return false;
}


function moveWithCollision(
    object,
    dx,
    dy
) {

    const nx = object.x + dx;

    if (
        !circleHitsWall(
            nx,
            object.y,
            object.radius
        )
    ) {
        object.x = nx;
    }

    const ny = object.y + dy;

    if (
        !circleHitsWall(
            object.x,
            ny,
            object.radius
        )
    ) {
        object.y = ny;
    }
}


// ============================================================
// DISTANCE
// ============================================================

function distance(
    x1,
    y1,
    x2,
    y2
) {

    const dx = x2 - x1;
    const dy = y2 - y1;

    return Math.sqrt(
        dx * dx + dy * dy
    );
}


// ============================================================
// LINE OF SIGHT
// ============================================================

function hasLineOfSight(
    x1,
    y1,
    x2,
    y2
) {

    const d =
        distance(
            x1,
            y1,
            x2,
            y2
        );

    const steps =
        Math.ceil(d / 18);

    for (
        let i = 0;
        i <= steps;
        i++
    ) {

        const t = i / steps;

        const x =
            x1 + (x2 - x1) * t;

        const y =
            y1 + (y2 - y1) * t;

        if (
            isWall(
                Math.floor(x / TILE),
                Math.floor(y / TILE)
            )
        ) {
            return false;
        }
    }

    return true;
}


// ============================================================
// PLAYER
// ============================================================

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

    const moving =
        dx !== 0 || dy !== 0;

    if (moving) {

        const length =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        dx /= length;
        dy /= length;

        let currentSpeed =
            player.speed;

        if (
            keys["shift"] &&
            player.stamina > 0
        ) {

            currentSpeed = 285;

            player.stamina -=
                35 * dt;

        }

        else {

            player.stamina +=
                20 * dt;
        }

        player.stamina =
            Math.max(
                0,
                Math.min(
                    100,
                    player.stamina
                )
            );

        moveWithCollision(
            player,
            dx * currentSpeed * dt,
            dy * currentSpeed * dt
        );

        footstepTimer -= dt;

        if (
            footstepTimer <= 0
        ) {

            beep(
                90 + Math.random() * 20,
                .05,
                .025,
                "square"
            );

            footstepTimer =
                keys["shift"]
                    ? .22
                    : .34;
        }
    }

    else {

        player.stamina +=
            30 * dt;

        player.stamina =
            Math.min(
                100,
                player.stamina
            );

        footstepTimer = 0;
    }
}


// ============================================================
// MONSTER
// ============================================================

function updateMonster(dt) {

    const d =
        distance(
            monster.x,
            monster.y,
            player.x,
            player.y
        );

    if (!monster.active) {

        if (
            d < 550 ||
            timePlayed > 18
        ) {

            monster.active = true;

            showMessage(
                "어딘가에서 발소리가 들린다.",
                3
            );

            beep(
                55,
                .8,
                .05,
                "sawtooth"
            );
        }

        return;
    }

    let targetSpeed =
        monster.speed;

    if (d < 650) {

        targetSpeed =
            monster.chaseSpeed;

        monster.anger +=
            dt;
    }

    else {

        targetSpeed =
            monster.speed;
    }

    let dx =
        player.x - monster.x;

    let dy =
        player.y - monster.y;

    const len =
        Math.sqrt(
            dx * dx +
            dy * dy
        );

    if (len > 0) {

        dx /= len;
        dy /= len;

        moveWithCollision(
            monster,
            dx * targetSpeed * dt,
            dy * targetSpeed * dt
        );
    }

    if (d < 420) {

        heartbeatTimer -= dt;

        if (
            heartbeatTimer <= 0
        ) {

            beep(
                65,
                .12,
                .045,
                "sine"
            );

            heartbeatTimer =
                Math.max(
                    .25,
                    d / 1000
                );
        }
    }

    if (d < 80) {

        player.health -=
            32 * dt;

        camera.shake =
            Math.max(
                camera.shake,
                8
            );

        redOverlay.style.background =
            "rgba(90,0,0,.18)";

        if (
            player.health <= 0
        ) {

            player.health = 0;

            endGame();
        }
    }

    else if (d < 180) {

        redOverlay.style.background =
            "rgba(90,0,0,.08)";
    }

    else {

        redOverlay.style.background =
            "rgba(90,0,0,0)";
    }
}


// ============================================================
// ITEMS
// ============================================================

function updateItems() {

    if (
        !keyItem.collected
    ) {

        const d =
            distance(
                player.x,
                player.y,
                keyItem.x,
                keyItem.y
            );

        if (d < 45) {

            keyItem.collected = true;

            beep(
                700,
                .12,
                .05,
                "sine"
            );

            showMessage(
                "낡은 열쇠를 주웠다.",
                3
            );

            objectiveElement.innerText =
                "열쇠를 사용해 현관문을 열어야 한다.";
        }
    }

    if (
        !note.found
    ) {

        const d =
            distance(
                player.x,
                player.y,
                note.x,
                note.y
            );

        if (d < 55) {

            interactionElement.style.opacity =
                "1";

            interactionElement.innerText =
                "E  조사하기";

        }

        else {

            interactionElement.style.opacity =
                "0";
        }
    }

    const doorDistance =
        distance(
            player.x,
            player.y,
            exitDoor.x,
            exitDoor.y
        );

    if (
        doorDistance < 65
    ) {

        interactionElement.style.opacity =
            "1";

        if (
            keyItem.collected
        ) {

            interactionElement.innerText =
                "E  문 열기";
        }

        else {

            interactionElement.innerText =
                "E  잠겨 있음";
        }
    }

    else if (
        distance(
            player.x,
            player.y,
            note.x,
            note.y
        ) >= 55
    ) {

        interactionElement.style.opacity =
            "0";
    }
}


// ============================================================
// INTERACTION
// ============================================================

function interact() {

    if (!gameStarted) {
        return;
    }

    if (gameOver || escaped) {
        return;
    }

    const noteDistance =
        distance(
            player.x,
            player.y,
            note.x,
            note.y
        );

    if (
        noteDistance < 55 &&
        !note.found
    ) {

        note.found = true;

        showMessage(
            "『문을 열지 마. 네가 들은 소리는 사람이 아니야.』",
            6
        );

        beep(
            130,
            .4,
            .04,
            "triangle"
        );

        return;
    }

    const doorDistance =
        distance(
            player.x,
            player.y,
            exitDoor.x,
            exitDoor.y
        );

    if (
        doorDistance < 65
    ) {

        if (
            !keyItem.collected
        ) {

            showMessage(
                "문은 잠겨 있다.",
                2
            );

            beep(
                80,
                .12,
                .04,
                "square"
            );

            return;
        }

        exitDoor.open = true;

        escaped = true;

        escapeScreen.style.display =
            "flex";

        beep(
            400,
            .4,
            .06,
            "sine"
        );
    }
}


// ============================================================
// RANDOM EVENTS
// ============================================================

function randomEvent() {

    const events = [

        function() {

            showMessage(
                "위층에서 무언가 떨어지는 소리가 났다.",
                3
            );

            beep(
                70,
                .3,
                .05,
                "square"
            );
        },

        function() {

            showMessage(
                "누군가 방금 문을 닫은 것 같다.",
                3
            );

            beep(
                90,
                .2,
                .05,
                "triangle"
            );
        },

        function() {

            showMessage(
                "복도 끝에서 무언가 움직였다.",
                3
            );

            monster.active = true;
        },

        function() {

            showMessage(
                "잠깐... 아무 소리도 들리지 않는다.",
                3
            );
        },

        function() {

            showMessage(
                "벽 너머에서 희미한 긁는 소리가 들린다.",
                4
            );

            beep(
                45,
                .5,
                .03,
                "sawtooth"
            );
        }

    ];

    const event =
        events[
            Math.floor(
                Math.random() *
                events.length
            )
        ];

    event();

    randomEventTimer =
        8 +
        Math.random() * 12;
}


// ============================================================
// CAMERA
// ============================================================

function updateCamera(dt) {

    const targetX =
        player.x - W / 2;

    const targetY =
        player.y - H / 2;

    camera.x +=
        (targetX - camera.x) *
        Math.min(
            1,
            dt * 7
        );

    camera.y +=
        (targetY - camera.y) *
        Math.min(
            1,
            dt * 7
        );

    camera.x =
        Math.max(
            0,
            Math.min(
                WORLD_W - W,
                camera.x
            )
        );

    camera.y =
        Math.max(
            0,
            Math.min(
                WORLD_H - H,
                camera.y
            )
        );

    if (
        camera.shake > 0
    ) {

        camera.shake *=
            Math.pow(
                .05,
                dt
            );

        if (
            camera.shake < .1
        ) {
            camera.shake = 0;
        }
    }
}


// ============================================================
// DRAW WORLD
// ============================================================

function drawWorld() {

    ctx.clearRect(
        0,
        0,
        W,
        H
    );

    let shakeX = 0;
    let shakeY = 0;

    if (
        camera.shake > 0
    ) {

        shakeX =
            (Math.random() - .5) *
            camera.shake;

        shakeY =
            (Math.random() - .5) *
            camera.shake;
    }

    ctx.save();

    ctx.translate(
        -camera.x + shakeX,
        -camera.y + shakeY
    );

    drawFloor();

    drawObjects();

    drawPlayer();

    drawMonster();

    ctx.restore();

    drawDarkness();

    drawNoise();
}


// ============================================================
// FLOOR
// ============================================================

function drawFloor() {

    const startX =
        Math.floor(
            camera.x / TILE
        ) - 1;

    const endX =
        Math.ceil(
            (camera.x + W) / TILE
        ) + 1;

    const startY =
        Math.floor(
            camera.y / TILE
        ) - 1;

    const endY =
        Math.ceil(
            (camera.y + H) / TILE
        ) + 1;

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

            if (
                x < 0 ||
                y < 0 ||
                x >= MAP_W ||
                y >= MAP_H
            ) {
                continue;
            }

            const px =
                x * TILE;

            const py =
                y * TILE;

            if (
                MAP[y][x] === "#"
            ) {

                ctx.fillStyle =
                    "#151515";

                ctx.fillRect(
                    px,
                    py,
                    TILE,
                    TILE
                );

                ctx.strokeStyle =
                    "#202020";

                ctx.strokeRect(
                    px + .5,
                    py + .5,
                    TILE - 1,
                    TILE - 1
                );

            }

            else {

                ctx.fillStyle =
                    "#303030";

                ctx.fillRect(
                    px,
                    py,
                    TILE,
                    TILE
                );

                ctx.strokeStyle =
                    "#353535";

                ctx.strokeRect(
                    px + .5,
                    py + .5,
                    TILE - 1,
                    TILE - 1
                );

                // floor details

                if (
                    (x * 17 + y * 31) % 9 === 0
                ) {

                    ctx.fillStyle =
                        "#282828";

                    ctx.fillRect(
                        px + 12,
                        py + 21,
                        2,
                        2
                    );
                }
            }
        }
    }
}


// ============================================================
// OBJECTS
// ============================================================

function drawObjects() {

    // key

    if (
        !keyItem.collected
    ) {

        ctx.save();

        ctx.translate(
            keyItem.x,
            keyItem.y
        );

        ctx.rotate(
            Math.sin(
                timePlayed * 3
            ) * .1
        );

        ctx.strokeStyle =
            "#b7a65a";

        ctx.lineWidth = 4;

        ctx.beginPath();

        ctx.arc(
            -8,
            -3,
            8,
            0,
            Math.PI * 2
        );

        ctx.stroke();

        ctx.beginPath();

        ctx.moveTo(
            0,
            -3
        );

        ctx.lineTo(
            22,
            -3
        );

        ctx.lineTo(
            22,
            4
        );

        ctx.lineTo(
            15,
            4
        );

        ctx.stroke();

        ctx.restore();
    }


    // note

    if (
        !note.found
    ) {

        ctx.save();

        ctx.translate(
            note.x,
            note.y
        );

        ctx.fillStyle =
            "#b7b2a3";

        ctx.fillRect(
            -16,
            -20,
            32,
            40
        );

        ctx.strokeStyle =
            "#666";

        ctx.strokeRect(
            -16,
            -20,
            32,
            40
        );

        ctx.strokeStyle =
            "#777";

        ctx.lineWidth = 2;

        for (
            let i = -8;
            i <= 10;
            i += 8
        ) {

            ctx.beginPath();

            ctx.moveTo(
                -10,
                i
            );

            ctx.lineTo(
                10,
                i
            );

            ctx.stroke();
        }

        ctx.restore();
    }


    // exit door

    ctx.save();

    ctx.translate(
        exitDoor.x,
        exitDoor.y
    );

    if (
        exitDoor.open
    ) {

        ctx.fillStyle =
            "#18251b";

    }

    else {

        ctx.fillStyle =
            "#253027";
    }

    ctx.fillRect(
        -25,
        -38,
        50,
        76
    );

    ctx.strokeStyle =
        "#617265";

    ctx.lineWidth = 3;

    ctx.strokeRect(
        -25,
        -38,
        50,
        76
    );

    ctx.fillStyle =
        "#888";

    ctx.beginPath();

    ctx.arc(
        15,
        0,
        4,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();
}


// ============================================================
// PLAYER
// ============================================================

function drawPlayer() {

    ctx.save();

    ctx.translate(
        player.x,
        player.y
    );

    ctx.shadowBlur = 15;
    ctx.shadowColor =
        "rgba(255,255,255,.15)";

    ctx.fillStyle =
        "#bdbdbd";

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        player.radius,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.shadowBlur = 0;

    ctx.fillStyle =
        "#202020";

    ctx.beginPath();

    ctx.arc(
        0,
        -3,
        6,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.restore();
}


// ============================================================
// MONSTER DRAW
// ============================================================

function drawMonster() {

    const d =
        distance(
            monster.x,
            monster.y,
            player.x,
            player.y
        );

    if (
        d > 850
    ) {
        return;
    }

    ctx.save();

    ctx.translate(
        monster.x,
        monster.y
    );

    const pulse =
        Math.sin(
            timePlayed * 5
        ) * 2;

    ctx.fillStyle =
        "#171717";

    ctx.beginPath();

    ctx.arc(
        0,
        0,
        monster.radius + pulse,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.strokeStyle =
        "#441b1b";

    ctx.lineWidth = 3;

    ctx.stroke();

    // eyes

    if (
        d < 600
    ) {

        ctx.fillStyle =
            "#b14b4b";

        ctx.beginPath();

        ctx.arc(
            -7,
            -4,
            3,
            0,
            Math.PI * 2
        );

        ctx.arc(
            7,
            -4,
            3,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }

    ctx.restore();
}


// ============================================================
// DARKNESS
// ============================================================

function drawDarkness() {

    const px =
        player.x -
        camera.x;

    const py =
        player.y -
        camera.y;

    let radius =
        player.flashlight
            ? 270
            : 120;

    if (
        flicker > 0
    ) {

        radius *=
            .65 +
            Math.random() * .35;
    }

    const gradient =
        ctx.createRadialGradient(
            px,
            py,
            radius * .15,
            px,
            py,
            radius
        );

    gradient.addColorStop(
        0,
        "rgba(0,0,0,0)"
    );

    gradient.addColorStop(
        .45,
        "rgba(0,0,0,.08)"
    );

    gradient.addColorStop(
        .72,
        "rgba(0,0,0,.55)"
    );

    gradient.addColorStop(
        1,
        "rgba(0,0,0,.96)"
    );

    ctx.fillStyle =
        gradient;

    ctx.fillRect(
        0,
        0,
        W,
        H
    );


    // flashlight cone

    if (
        player.flashlight
    ) {

        const cone =
            ctx.createRadialGradient(
                px,
                py,
                20,
                px,
                py,
                430
            );

        cone.addColorStop(
            0,
            "rgba(255,255,255,.08)"
        );

        cone.addColorStop(
            .6,
            "rgba(255,255,255,.015)"
        );

        cone.addColorStop(
            1,
            "rgba(255,255,255,0)"
        );

        ctx.fillStyle =
            cone;

        ctx.fillRect(
            0,
            0,
            W,
            H
        );
    }
}


// ============================================================
// NOISE
// ============================================================

function drawNoise() {

    noiseElement.style.opacity =
        String(
            .025 +
            Math.random() * .025
        );
}


// ============================================================
// GAME END
// ============================================================

function endGame() {

    if (gameOver) {
        return;
    }

    gameOver = true;

    gameOverScreen.style.display =
        "flex";

    beep(
        45,
        1,
        .08,
        "sawtooth"
    );
}


// ============================================================
// RESET
// ============================================================

function resetGame() {

    gameStarted = true;
    gameOver = false;
    escaped = false;
    paused = false;

    player.x = 6 * TILE;
    player.y = 6 * TILE;
    player.health = 100;
    player.stamina = 100;
    player.flashlight = true;

    monster.x = 43 * TILE;
    monster.y = 43 * TILE;
    monster.active = false;
    monster.anger = 0;

    keyItem.collected = false;
    note.found = false;

    exitDoor.open = false;

    camera.x = 0;
    camera.y = 0;
    camera.shake = 0;

    timePlayed = 0;
    randomEventTimer = 8;

    gameOverScreen.style.display =
        "none";

    escapeScreen.style.display =
        "none";

    pauseScreen.style.display =
        "none";

    interactionElement.style.opacity =
        "0";

    objectiveElement.innerText =
        "집 밖으로 나가야 한다.";

    showMessage(
        "방 안이다. 밖으로 나갈 방법을 찾아야 한다.",
        4
    );
}


// ============================================================
// KEYBOARD
// ============================================================

window.addEventListener(
    "keydown",
    function(e) {

        const key =
            e.key.toLowerCase();

        if (
            [
                "w",
                "a",
                "s",
                "d",
                "shift",
                "f",
                "e",
                "arrowup",
                "arrowdown",
                "arrowleft",
                "arrowright",
                " "
            ].includes(key)
        ) {

            e.preventDefault();
        }

        keys[key] = true;

        if (
            key === "e"
        ) {

            interact();
        }

        if (
            key === "f"
        ) {

            if (gameStarted) {

                player.flashlight =
                    !player.flashlight;

                beep(
                    player.flashlight
                        ? 500
                        : 200,
                    .08,
                    .025,
                    "square"
                );
            }
        }

        if (
            key === " "
        ) {

            paused =
                !paused;

            pauseScreen.style.display =
                paused
                    ? "flex"
                    : "none";
        }
    }
);

window.addEventListener(
    "keyup",
    function(e) {

        keys[
            e.key.toLowerCase()
        ] = false;
    }
);


// ============================================================
// BUTTONS
// ============================================================

document
    .getElementById("startButton")
    .addEventListener(
        "click",
        function() {

            initAudio();

            startScreen.style.display =
                "none";

            resetGame();

            canvas.focus();
        }
    );

document
    .getElementById("restartButton")
    .addEventListener(
        "click",
        function() {

            initAudio();

            resetGame();
        }
    );

document
    .getElementById("escapeRestartButton")
    .addEventListener(
        "click",
        function() {

            initAudio();

            resetGame();
        }
    );


// ============================================================
// GAME LOOP
// ============================================================

function update(dt) {

    if (
        !gameStarted ||
        gameOver ||
        escaped ||
        paused
    ) {
        return;
    }

    timePlayed += dt;

    updatePlayer(dt);

    updateMonster(dt);

    updateItems();

    updateCamera(dt);

    updateMessage(dt);

    randomEventTimer -= dt;

    if (
        randomEventTimer <= 0
    ) {

        randomEvent();

        randomEventTimer =
            10 +
            Math.random() * 15;
    }

    flicker -= dt;

    if (
        Math.random() < .002
    ) {

        flicker = .15;
    }

    healthElement.style.width =
        player.health + "%";

    if (
        player.health < 35
    ) {

        healthElement.style.background =
            "#712525";

    }

    else {

        healthElement.style.background =
            "#777";
    }
}


// ============================================================
// MAIN LOOP
// ============================================================

function loop(now) {

    const dt =
        Math.min(
            .05,
            (now - lastTime) / 1000
        );

    lastTime = now;

    update(dt);

    drawWorld();

    requestAnimationFrame(loop);
}

requestAnimationFrame(loop);

</script>

</body>
</html>
"""

components.html(
    GAME_HTML,
    height=850,
    scrolling=False
)
