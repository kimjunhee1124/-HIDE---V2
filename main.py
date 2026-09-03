import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HIDE - Pixel School EX", page_icon="👻", layout="wide")

GAME_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box}
body{
  margin:0; background:#07080b; color:#fff; font-family:'Courier New', monospace;
  overflow:hidden; user-select:none;
}
#wrap{display:flex; justify-content:center; align-items:center; min-height:760px}
#viewport{
  position:relative; width:1000px; height:650px;
  background:#0e1015; border:4px solid #2d333f; overflow:hidden;
  box-shadow:0 0 25px rgba(0,0,0,0.9);
}

#map-container{
  position:absolute; top:0; left:0;
  background:#323741;
}

.tile{position:absolute; width:40px; height:40px; box-sizing:border-box; image-rendering:pixelated;}
.floor-tut{
  background: #3a3f4b;
  border-right:1px solid #303540;
  border-bottom:1px solid #303540;
}
.floor-main{
  background: #e2e8f0;
  border-right:1px solid #cbd5e1;
  border-bottom:1px solid #cbd5e1;
}

.wall{
  background:#1a1d24; 
  border:3px solid #0d0e12; 
  box-shadow:inset 2px 2px 0 #2a2f3a, inset -2px -2px 0 #121419;
}

.cab{
  background:#5a626e; 
  border:3px solid #1e2229;
  box-shadow:inset 3px 3px 0 #7c8594, inset -3px -3px 0 #3a4049;
  position:absolute;
}
.cab::before{
  content:""; position:absolute; left:6px; top:6px; right:6px; height:8px;
  background:#3e444d; border-bottom:2px solid #6f7785;
}
.cab::after{
  content:""; position:absolute; right:6px; top:20px; width:4px; height:6px;
  background:#d0d7e1; box-shadow:0 1px 0 #111;
}

.key-item{
  background:transparent;
  display:flex; align-items:center; justify-content:center;
}
.key-icon{
  width:22px; height:22px;
  animation: bounce 0.8s infinite alternate;
}
@keyframes bounce { from { transform:translateY(-2px); } to { transform:translateY(3px); } }

.door{
  background:#27ae60; border:3px solid #1e8449; text-align:center; 
  line-height:34px; font-weight:bold; color:#e8f8f5; font-size:10px;
  box-shadow:inset 2px 2px 0 #52be80;
}

.wood-door{
  background:#8d5524; border:3px solid #5c3a21; text-align:center; 
  line-height:34px; font-weight:bold; color:#f4d03f; font-size:9px;
  box-shadow:inset 2px 2px 0 #a0652d;
}

.sprite{
  position:absolute; width:32px; height:42px; z-index:10;
  transform:translate(-50%, -50%); image-rendering:pixelated;
}
.sprite svg{width:32px; height:42px; shape-rendering:crispEdges;}
.shadow{
  position:absolute; width:26px; height:8px; border-radius:50%;
  background:rgba(0,0,0,0.5); transform:translate(-50%, -50%); z-index:5;
}

.screen{position:absolute; inset:0; display:flex; align-items:center; justify-content:center; z-index:50;}
.hidden{display:none !important;}
#title{flex-direction:column; background:#0b0c10;}
.title{font-size:52px; letter-spacing:4px; text-shadow:4px 4px #8b0000; margin-bottom:10px; color:#f0f0f0;}
.sub{color:#7a8391; margin-bottom:20px; font-size:15px;}
.controls-box{
  background:#161920; border:2px solid #3a4150; padding:15px 25px; border-radius:8px;
  margin-bottom:20px; text-align:center; color:#2ecc71;
}
.selects{display:flex; gap:25px;}
.pick{
  width:180px; height:180px; background:#161920; border:3px solid #3a4150;
  cursor:pointer; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px;
  transition: transform 0.1s;
}
.pick:hover{border-color:#fff; background:#202530; transform:translateY(-3px);}

#hud{
  position:absolute; z-index:40; left:15px; top:15px; right:15px;
  display:flex; justify-content:space-between; pointer-events:none; gap:10px;
}
.panel{background:rgba(10,12,16,0.85); border:2px solid #4a5260; padding:8px 14px; font-size:14px; border-radius:2px;}
#alert{
  position:absolute; z-index:40; left:50%; top:20px; transform:translateX(-50%);
  font-size:20px; background:#c0392b; color:#fff; padding:4px 16px; font-weight:bold;
  display:none; border:2px solid #000; box-shadow:3px 3px 0 #000;
  animation: pulseAlert 0.5s infinite alternate;
}
@keyframes pulseAlert { from { transform: translateX(-50%) scale(1); } to { transform: translateX(-50%) scale(1.05); } }

#tutorialNotice{
  position:absolute; z-index:90; inset:0; background:rgba(0,0,0,0.8);
  display:flex; align-items:center; justify-content:center;
}
.notice-box{
  background:#161920; border:3px solid #3498db; padding:25px 35px; border-radius:8px;
  max-width:550px; text-align:center; box-shadow:0 0 20px rgba(52,152,219,0.4);
}
.notice-box h2{color:#3498db; margin-top:0;}
.notice-box ul{text-align:left; color:#dcdde1; line-height:1.6; margin:15px 0;}

#hideUI{
  position:absolute; z-index:100; inset:0;
  background: radial-gradient(circle, rgba(10, 15, 20, 0.3) 30%, rgba(0, 0, 0, 0.95) 90%);
  backdrop-filter: blur(2px);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
}

#gaugeContainer{
  width:260px; height:16px; background:#1a1a1a; border:2px solid #e74c3c;
  border-radius:8px; margin:10px auto 15px auto; overflow:hidden;
  box-shadow:0 0 10px rgba(231, 76, 60, 0.5);
}
#gaugeBar{
  width:100%; height:100%; background:linear-gradient(90deg, #e74c3c, #ff6b6b);
  transition: width 0.1s linear;
}

#keyDisplay{
  width:85px; height:85px; border:4px solid #e74c3c; background:rgba(22, 25, 32, 0.9);
  display:flex; align-items:center; justify-content:center; font-size:48px; font-weight:bold; margin:10px auto;
  box-shadow:0 0 20px rgba(231, 76, 60, 0.6); color:#fff;
}

#gameover, #winScreen{background:#0a0505; flex-direction:column;}
.bigbtn{
  background:#962d22; color:#fff; border:2px solid #e74c3c; padding:10px 22px; 
  font-size:16px; font-family:inherit; cursor:pointer; margin-top:20px; box-shadow:4px 4px 0 #000;
}
.bigbtn:hover{background:#c0392b;}
</style>
</head>
<body>

<div id="wrap">
<div id="viewport">

  <div id="title" class="screen">
    <div class="title">👻 HIDE : PIXEL SCHOOL</div>
    <div class="sub">괴물을 피해 열쇠를 모아 탈출하세요!</div>
    
    <div class="controls-box">
      <div style="font-size:16px; font-weight:bold; margin-bottom:6px; color:#fff;">🎮 조작 안내</div>
      <div>이동: <b>W, A, S, D</b> 또는 <b>방향키</b></div>
      <div>상호작용 (은신 / 열쇠 획득 / 이동): <b style="color:#f1c40f;">[ E ] Key</b></div>
    </div>

    <div class="selects">
      <div class="pick" onclick="startGame('male')">
        <div id="mPrev"></div><b>남학생</b>
      </div>
      <div class="pick" onclick="startGame('female')">
        <div id="fPrev"></div><b>여학생</b>
      </div>
    </div>
  </div>

  <div id="world" class="screen hidden">
    <div id="map-container">
      <div id="tiles"></div>
      <div id="pShadow" class="shadow"></div>
      <div id="mShadow" class="shadow"></div>
      <div id="player" class="sprite"></div>
      <div id="monster" class="sprite"></div>
    </div>

    <div id="tutorialNotice">
      <div class="notice-box">
        <h2 id="stageTitle">📢 [튜토리얼 스테이지]</h2>
        <p style="color:#f1c40f; font-weight:bold;" id="stageDesc">본 게임에 진입하기 전, 기본 조작과 은신 방법을 익히세요!</p>
        <ul id="stageGoals">
          <li><b>목표:</b> 랜덤 위치의 열쇠(🔑 1개)를 찾으세요.</li>
          <li><b>은신 연습:</b> 괴물이 다가오면 캐비닛에 숨어 QTE 미션을 수행하세요.</li>
          <li><b>입장:</b> 열쇠로 우측 하단의 START 문을 열어 본 게임으로 향하세요.</li>
        </ul>
        <button class="bigbtn" style="background:#2980b9; border-color:#3498db;" onclick="closeTutorial()">이해했습니다 (시작)</button>
      </div>
    </div>

    <div id="hud">
      <div class="panel">🔑 열쇠: <span id="keyCount">0</span>/<span id="targetKeyCount">1</span></div>
      <div class="panel">상태: <span id="mission" style="color:#f1c40f;">[튜토리얼] 열쇠를 찾으세요!</span></div>
      <div class="panel" style="color:#aaa;">조작: WASD(이동) / E(상호작용)</div>
    </div>
    <div id="alert">! 경고: 괴물이 추격 중 !</div>
  </div>

  <div id="hideUI" class="hidden">
    <div id="qteBox" style="text-align:center;">
      <h2 id="hideTitle" style="color:#e74c3c; margin:0 0 6px 0; text-shadow:2px 2px #000;">⚠️ 괴물이 바로 앞에 있습니다! 숨소리를 참으세요!</h2>
      <p id="hideSub" style="color:#bdc3c7; margin:0 0 10px 0; text-shadow:1px 1px #000;">게이지가 다 떨어지기 전에 표시되는 키를 누르세요!</p>
      
      <div style="font-size:18px; color:#e74c3c; font-weight:bold; margin-bottom:8px;">
        ❤️ 숨참기 기회 (실패 실수): <span id="qteHp" style="color:#fff; font-size:22px;">3</span> / 3
      </div>

      <div id="gaugeContainer">
        <div id="gaugeBar"></div>
      </div>

      <div id="keyDisplay">W</div>
      <div style="font-size:16px; color:#ddd; margin-top:5px; text-shadow:1px 1px #000;">남은 성공 횟수: <b id="reqCount" style="color:#f1c40f;">5</b>회</div>
    </div>
    
    <div id="safeBox" class="hidden" style="text-align:center;">
      <h2 style="color:#2ecc71; margin:0 0 10px 0; text-shadow:2px 2px #000;">🤫 안전하게 은신 중입니다...</h2>
      <p style="color:#bdc3c7; margin:0; text-shadow:1px 1px #000;">괴물은 당신을 인식하지 못합니다. 밖으로 나가려면 <b>[E]</b> 키를 누르세요.</p>
    </div>
  </div>

  <div id="gameover" class="screen hidden">
    <h1 style="font-size:48px; color:#c0392b; text-shadow:3px 3px #000;">GAME OVER</h1>
    <p id="overReason" style="color:#a6a6a6;">괴물에게 붙잡혔습니다...</p>
    <button class="bigbtn" onclick="restartGame()">다시 시작</button>
  </div>

  <div id="winScreen" class="screen hidden">
    <h1 id="winTitle" style="font-size:40px; color:#27ae60; text-shadow:3px 3px #000;">🎓 튜토리얼 클리어!</h1>
    <p id="winDesc" style="color:#a6a6a6;">기본 생존 수칙을 모두 익혔습니다. 이제 본 게임으로 입장합니다...</p>
    <button id="winBtn" class="bigbtn" style="background:#27ae60; border-color:#2ecc71;" onclick="startMainGame()">본 게임 시작하기</button>
  </div>

</div>
</div>

<script>
let audioCtx = null;
let chaseBgmInterval = null;
let ambientBgmInterval = null;
let bgmStep = 0;
let ambientStep = 0;

function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
}

function playLockerSound() {
  try {
    initAudio();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(150, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.15);

    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start();
    osc.stop(audioCtx.currentTime + 0.15);
  } catch(e) {}
}

function startAmbientBGM() {
  if (ambientBgmInterval || chaseBgmInterval) return;
  initAudio();

  ambientBgmInterval = setInterval(() => {
    if (!audioCtx || audioCtx.state !== 'running') return;
    
    try {
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      const ambientChords = [130.81, 164.81, 196.00, 220.00];
      osc.type = 'sine';
      osc.frequency.setValueAtTime(ambientChords[ambientStep % ambientChords.length], now);

      gain.gain.setValueAtTime(0.001, now);
      gain.gain.linearRampToValueAtTime(0.06, now + 1.0);
      gain.gain.linearRampToValueAtTime(0.001, now + 3.5);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start(now);
      osc.stop(now + 3.6);

      ambientStep++;
    } catch(e) {}
  }, 4000);
}

function stopAmbientBGM() {
  if (ambientBgmInterval) {
    clearInterval(ambientBgmInterval);
    ambientBgmInterval = null;
  }
}

function startChaseBGM() {
  if (chaseBgmInterval) return;
  stopAmbientBGM();
  initAudio();
  
  bgmStep = 0;
  chaseBgmInterval = setInterval(() => {
    if (!audioCtx || audioCtx.state !== 'running') return;
    
    try {
      const now = audioCtx.currentTime;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      
      const freqs = [82.41, 110.0, 77.78, 116.54];
      osc.type = (bgmStep % 2 === 0) ? 'sawtooth' : 'square';
      osc.frequency.setValueAtTime(freqs[bgmStep % freqs.length], now);
      
      gain.gain.setValueAtTime(0.18, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
      
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      
      osc.start(now);
      osc.stop(now + 0.25);
      
      if (bgmStep % 2 === 1) {
        const osc2 = audioCtx.createOscillator();
        const gain2 = audioCtx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(330, now + 0.1);
        gain2.gain.setValueAtTime(0.1, now + 0.1);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
        osc2.connect(gain2);
        gain2.connect(audioCtx.destination);
        osc2.start(now + 0.1);
        osc2.stop(now + 0.2);
      }
      
      bgmStep++;
    } catch(e) {}
  }, 300);
}

function stopChaseBGM() {
  if (chaseBgmInterval) {
    clearInterval(chaseBgmInterval);
    chaseBgmInterval = null;
  }
}

const TILE_SIZE = 40;
let mapSize = 25;
const maxHideTime = 6.0;

const maleSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="1" width="8" height="2" fill="#2c3e50"/>
  <rect x="3" y="2" width="10" height="4" fill="#2c3e50"/>
  <rect x="4" y="5" width="8" height="5" fill="#f3d2b3"/>
  <rect x="5" y="7" width="2" height="2" fill="#111"/>
  <rect x="9" y="7" width="2" height="2" fill="#111"/>
  <rect x="6" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <rect x="3" y="10" width="10" height="5" fill="#2980b9"/>
  <rect x="7" y="10" width="2" height="3" fill="#fff"/>
  <rect x="7" y="12" width="2" height="2" fill="#c0392b"/>
  <rect x="4" y="15" width="3" height="4" fill="#34495e"/>
  <rect x="9" y="15" width="3" height="4" fill="#34495e"/>
  <rect x="3" y="18" width="4" height="2" fill="#111"/>
  <rect x="9" y="18" width="4" height="2" fill="#111"/>
</svg>`;

const femaleSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="1" width="10" height="3" fill="#5d4037"/>
  <rect x="2" y="3" width="12" height="7" fill="#5d4037"/>
  <rect x="4" y="5" width="8" height="5" fill="#f3d2b3"/>
  <rect x="5" y="7" width="2" height="2" fill="#111"/>
  <rect x="9" y="7" width="2" height="2" fill="#111"/>
  <rect x="6" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <rect x="4" y="8" width="1" height="1" fill="#e84393"/>
  <rect x="11" y="8" width="1" height="1" fill="#e84393"/>
  <rect x="3" y="10" width="10" height="4" fill="#2980b9"/>
  <rect x="7" y="10" width="2" height="2" fill="#fff"/>
  <rect x="3" y="14" width="10" height="3" fill="#c0392b"/>
  <rect x="5" y="17" width="2" height="2" fill="#f3d2b3"/>
  <rect x="9" y="17" width="2" height="2" fill="#f3d2b3"/>
  <rect x="4" y="18" width="3" height="2" fill="#111"/>
  <rect x="9" y="18" width="3" height="2" fill="#111"/>
</svg>`;

const monsterSVG = `
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="2" width="10" height="15" fill="#1e272c"/>
  <rect x="2" y="5" width="12" height="10" fill="#2c3e50"/>
  <rect x="4" y="6" width="3" height="3" fill="#e74c3c"/>
  <rect x="9" y="6" width="3" height="3" fill="#e74c3c"/>
  <rect x="5" y="7" width="1" height="1" fill="#fff"/>
  <rect x="10" y="7" width="1" height="1" fill="#fff"/>
  <rect x="5" y="11" width="6" height="2" fill="#000"/>
  <rect x="6" y="11" width="1" height="1" fill="#fff"/>
  <rect x="9" y="11" width="1" height="1" fill="#fff"/>
  <rect x="3" y="17" width="3" height="3" fill="#111"/>
  <rect x="10" y="17" width="3" height="3" fill="#111"/>
</svg>`;

const keySVG = `
<svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="key-icon">
  <path d="M6 2 C3.8 2 2 3.8 2 6 C2 8.2 3.8 10 6 10 C7 10 7.9 9.6 8.5 9 L11 11.5 L11 13 L13 13 L13 11 L14 11 L14 9 L11.5 6.5 C11.9 5.9 12 5 12 4 C12 2 10 2 6 2 Z M6 4 C7.1 4 8 4.9 8 6 C8 7.1 7.1 8 6 8 C4.9 8 4 7.1 4 6 C4 4.9 4.9 4 6 4 Z" fill="#f1c40f"/>
</svg>`;

let mapData = [];
let selectedGender = 'male';
let isMainGame = false;

let px = 100, py = 100;
let mx = 11 * TILE_SIZE + 20, my = 11 * TILE_SIZE + 20;
let qteHp = 3, keyCount = 0, targetKeys = 1;
let isHidden = false, isChased = false, isQTEActive = false, gameEnded = false;
let isPaused = true;
let keysPressed = {};

let stealthTimer = 0;
let targetKey = 'W';
let hideTimer = 6.0;
let requiredPresses = 5;

let mTargetX = 11 * TILE_SIZE + 20, mTargetY = 11 * TILE_SIZE + 20;

function initPreviews() {
  const mPrev = document.getElementById('mPrev');
  const fPrev = document.getElementById('fPrev');
  if (mPrev) mPrev.innerHTML = `<div class="sprite" style="position:relative">${maleSVG}</div>`;
  if (fPrev) fPrev.innerHTML = `<div class="sprite" style="position:relative">${femaleSVG}</div>`;
}

function generateMap() {
  if (isMainGame) {
    const possibleSizes = [15, 20, 30];
    mapSize = possibleSizes[Math.floor(Math.random() * possibleSizes.length)];
    targetKeys = Math.floor(mapSize / 7) + 2;
  } else {
    mapSize = 25;
    targetKeys = 1;
  }
  
  const mapContainer = document.getElementById('map-container');
  mapContainer.style.width = (mapSize * TILE_SIZE) + 'px';
  mapContainer.style.height = (mapSize * TILE_SIZE) + 'px';

  mapData = [];
  let freeTiles = [];

  for(let r=0; r<mapSize; r++) {
    let row = [];
    for(let c=0; c<mapSize; c++) {
      if(r===0 || r===mapSize-1 || c===0 || c===mapSize-1) {
        row.push(1);
      } else if(r % 4 === 0 && c % 4 === 0 && Math.random() > 0.25) {
        row.push(1);
      } else {
        row.push(0);
        if(r > 2 && c > 2 && !(r === mapSize-2 && c === mapSize-2)) {
          freeTiles.push({r, c});
        }
      }
    }
    mapData.push(row);
  }
  
  if (!isMainGame) {
    mapData[1][1] = 0; mapData[1][2] = 0;
    mapData[2][1] = 0; mapData[2][2] = 0;
  }

  if (isMainGame) {
    const mid = Math.floor(mapSize / 2);
    mapData[0][mid] = 5;
    mapData[mapSize - 1][mid] = 5;
    mapData[mid][0] = 5;
    mapData[mid][mapSize - 1] = 5;
  }

  let cabPositions = isMainGame ? [
    {r:2,c:2}, {r:3,c:mapSize-3}, {r:mapSize-3,c:3}, {r:mapSize-3,c:mapSize-3}, 
    {r:Math.floor(mapSize/2), c:Math.floor(mapSize/2)}
  ] : [
    {r:3,c:3}, {r:8,c:12}, {r:12,c:8}, {r:18,c:18}
  ];

  cabPositions.forEach(p => {
    if(p.r > 0 && p.r < mapSize-1 && p.c > 0 && p.c < mapSize-1) {
      mapData[p.r][p.c] = 2;
    }
  });

  for(let i=0; i<targetKeys; i++) {
    if(freeTiles.length > 0) {
      let randomIndex = Math.floor(Math.random() * freeTiles.length);
      let keyPos = freeTiles.splice(randomIndex, 1)[0];
      mapData[keyPos.r][keyPos.c] = 3;
    }
  }

  mapData[mapSize-2][mapSize-2] = 4;
}

function renderMap() {
  const container = document.getElementById('tiles');
  if(!container) return;
  let html = '';
  const floorStyleClass = isMainGame ? 'floor-main' : 'floor-tut';

  for(let r=0; r<mapSize; r++) {
    for(let c=0; c<mapSize; c++) {
      const type = mapData[r][c];
      let tileClass = floorStyleClass;
      let content = '';

      if(type === 1) tileClass = 'wall';
      else if(type === 2) tileClass = 'cab';
      else if(type === 3) { tileClass = 'key-item'; content = keySVG; }
      else if(type === 4) { tileClass = 'door'; content = isMainGame ? 'EXIT' : 'START'; }
      else if(type === 5) { tileClass = 'wood-door'; content = 'WOOD DOOR'; }

      html += `<div class="tile ${tileClass}" style="left:${c*TILE_SIZE}px; top:${r*TILE_SIZE}px;">${content}</div>`;
    }
  }
  container.innerHTML = html;
}

function resetGameState() {
  if (isMainGame) {
    px = (Math.floor(mapSize / 2)) * TILE_SIZE + 20;
    py = (Math.floor(mapSize / 2)) * TILE_SIZE + 20;
  } else {
    px = 100; py = 100;
  }
  mx = 11 * TILE_SIZE + 20; my = 11 * TILE_SIZE + 20;
  qteHp = 3; keyCount = 0;
  isHidden = false; isChased = false; isQTEActive = false; gameEnded = false;
  stealthTimer = 0;
  keysPressed = {};
  stopChaseBGM();
  stopAmbientBGM();
  
  generateMap();

  document.getElementById('keyCount').textContent = keyCount;
  document.getElementById('targetKeyCount').textContent = targetKeys;
  document.getElementById('qteHp').textContent = qteHp;
  document.getElementById('alert').style.display = 'none';
  document.getElementById('hideUI').classList.add('hidden');
  document.getElementById('gameover').classList.add('hidden');
  document.getElementById('winScreen').classList.add('hidden');
  
  renderMap();
}

function startGame(type) {
  if(type) selectedGender = type;
  playLockerSound();
  
  isMainGame = false;
  document.getElementById('title').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  document.getElementById('player').innerHTML = selectedGender === 'male' ? maleSVG : femaleSVG;
  document.getElementById('monster').innerHTML = monsterSVG;
  
  resetGameState();
  pickMonsterNewTarget();
  
  isPaused = true;
  document.getElementById('tutorialNotice').classList.remove('hidden');
  
  lastTime = performance.now();
  requestAnimationFrame(gameLoop);
}

function startMainGame() {
  isMainGame = true;
  document.getElementById('stageTitle').textContent = "🔥 [본 게임 스테이지]";
  document.getElementById('stageDesc').textContent = "랜덤 크기(15x15, 20x20, 30x30)의 방! 테두리 나무 문과 괴물을 피하세요!";
  document.getElementById('stageGoals').innerHTML = `
    <li><b>랜덤 방 크기:</b> 진입 시 15×15, 20×20, 30×30 중 하나의 방이 생성됩니다.</li>
    <li><b>나무 문:</b> 맵 네 변 테두리의 정중앙에 위치하며, 벽을 뚫고 설치되어 있습니다.</li>
    <li><b>목표:</b> 숨겨진 <b>열쇠(${targetKeys}개)</b>를 모두 수집하세요!</li>
    <li><b>탈출:</b> 열쇠를 모은 뒤 EXIT 문을 통해 최종 탈출하세요.</li>
  `;
  
  document.getElementById('winScreen').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  
  resetGameState();
  pickMonsterNewTarget();
  
  isPaused = true;
  document.getElementById('tutorialNotice').classList.remove('hidden');
  
  lastTime = performance.now();
  requestAnimationFrame(gameLoop);
}

function restartGame() {
  document.getElementById('gameover').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  
  resetGameState();
  pickMonsterNewTarget();
  isPaused = false;
  startAmbientBGM();
  
  lastTime = performance.now();
  requestAnimationFrame(gameLoop);
}

function closeTutorial() {
  playLockerSound();
  document.getElementById('tutorialNotice').classList.add('hidden');
  isPaused = false;
  startAmbientBGM();
}

document.addEventListener('keydown', e => {
  if(isPaused || gameEnded) return;

  const k = e.key.toLowerCase();
  keysPressed[k] = true;

  if(e.key === 'e' || e.key === 'E') {
    handleInteraction();
    return;
  }

  if(isHidden && isQTEActive && ['w','a','s','d'].includes(k)) {
    handleHideInput(k.toUpperCase());
  }
});

document.addEventListener('keyup', e => {
  keysPressed[e.key.toLowerCase()] = false;
});

window.addEventListener('blur', () => {
  keysPressed = {};
});

document.addEventListener('contextmenu', e => {
  e.preventDefault();
});

function isSolid(x, y) {
  const r = 12;
  const points = [
    {x: x - r, y: y - r},
    {x: x + r, y: y - r},
    {x: x - r, y: y + r},
    {x: x + r, y: y + r}
  ];

  for(let p of points) {
    let col = Math.floor(p.x / TILE_SIZE);
    let row = Math.floor(p.y / TILE_SIZE);
    if(row < 0 || row >= mapSize || col < 0 || col >= mapSize) return true;
    if(mapData[row][col] === 1) return true;
  }
  return false;
}

function updatePlayer() {
  let speed = 3.3;
  let dx = 0, dy = 0;
  if(keysPressed['w'] || keysPressed['arrowup']) dy -= 1;
  if(keysPressed['s'] || keysPressed['arrowdown']) dy += 1;
  if(keysPressed['a'] || keysPressed['arrowleft']) dx -= 1;
  if(keysPressed['d'] || keysPressed['arrowright']) dx += 1;

  if(dx !== 0 && dy !== 0) { dx *= 0.7071; dy *= 0.7071; }

  let nx = px + dx * speed;
  let ny = py + dy * speed;

  if(!isSolid(nx, py)) px = nx;
  if(!isSolid(px, ny)) py = ny;

  const pCol = Math.floor(px / TILE_SIZE);
  const pRow = Math.floor(py / TILE_SIZE);
  const tileType = mapData[pRow][pCol];

  const prefix = isMainGame ? '[본 게임]' : '[튜토리얼]';

  if(tileType === 2) {
    document.getElementById('mission').textContent = '[E] 키를 눌러 캐비닛에 숨으세요!';
  } else if(tileType === 3) {
    document.getElementById('mission').textContent = '[E] 키를 눌러 열쇠를 줍으세요!';
  } else if(tileType === 5) {
    document.getElementById('mission').textContent = '[E] 키를 눌러 나무 문을 통과해 다른 방으로 이동하세요!';
  } else if(tileType === 4) {
    if(keyCount >= targetKeys) document.getElementById('mission').textContent = isMainGame ? '[E] 학교 탈출 문 열기!' : '[E] 본 게임 이동!';
    else document.getElementById('mission').textContent = `문이 잠겨 있습니다. (열쇠 ${keyCount}/${targetKeys})`;
  } else if(keyCount < targetKeys) {
    document.getElementById('mission').textContent = `${prefix} 열쇠를 찾으세요! (${keyCount}/${targetKeys})`;
  } else {
    document.getElementById('mission').textContent = `${prefix} 탈출 문으로 이동하세요!`;
  }
}

function handleInteraction() {
  const pCol = Math.floor(px / TILE_SIZE);
  const pRow = Math.floor(py / TILE_SIZE);
  const tileType = mapData[pRow][pCol];

  if(isHidden) {
    if(!isQTEActive) {
      exitCabinetSafe();
    }
    return;
  }

  if(tileType === 2) {
    playLockerSound();
    
    let monsterDist = Math.hypot(px - mx, py - my);
    
    if(isChased || monsterDist < 280) {
      isHidden = true;
      isQTEActive = true;
      startChaseBGM();
      
      mx = px + 15;
      my = py + 20;

      document.getElementById('hideUI').classList.remove('hidden');
      document.getElementById('qteBox').classList.remove('hidden');
      document.getElementById('safeBox').classList.add('hidden');
      
      hideTimer = maxHideTime;
      requiredPresses = 5;
      qteHp = 3;
      document.getElementById('qteHp').textContent = qteHp;
      document.getElementById('reqCount').textContent = requiredPresses;
      document.getElementById('gaugeBar').style.width = '100%';
      nextHideKey();
    } 
    else {
      isHidden = true;
      isQTEActive = false;
      stopChaseBGM();
      stopAmbientBGM();
      document.getElementById('hideUI').classList.remove('hidden');
      document.getElementById('qteBox').classList.add('hidden');
      document.getElementById('safeBox').classList.remove('hidden');
    }
  } 
  else if(tileType === 3) {
    keyCount++;
    mapData[pRow][pCol] = 0;
    renderMap();
    document.getElementById('keyCount').textContent = keyCount;
    if(keyCount >= targetKeys) {
      document.getElementById('mission').textContent = '모든 열쇠 획득! 출구 문으로 이동하세요!';
    } else {
      document.getElementById('mission').textContent = `열쇠 획득! (${keyCount}/${targetKeys})`;
    }
  }
  else if(tileType === 5) {
    playLockerSound();
    resetGameState();
    pickMonsterNewTarget();
    document.getElementById('mission').textContent = '나무 문을 통해 새로운 방으로 이동했습니다!';
  }
  else if(tileType === 4) {
    if(keyCount >= targetKeys) win();
  }
}

function pickMonsterNewTarget() {
  let validTiles = [];
  for(let r = 1; r < mapSize - 1; r++) {
    for(let c = 1; c < mapSize - 1; c++) {
      if(mapData[r][c] === 0) {
        validTiles.push({r, c});
      }
    }
  }

  if(validTiles.length > 0) {
    let pick = validTiles[Math.floor(Math.random() * validTiles.length)];
    mTargetX = pick.c * TILE_SIZE + 20;
    mTargetY = pick.r * TILE_SIZE + 20;
  }
}

function updateMonster() {
  if(isHidden && isQTEActive) {
    document.getElementById('alert').style.display = 'block';
    startChaseBGM();
    return;
  }

  let dist = Math.hypot(px - mx, py - my);
  let detectRange = 260;
  
  if(dist < detectRange && !isHidden && stealthTimer <= 0) {
    isChased = true;
    document.getElementById('alert').style.display = 'block';
    startChaseBGM();
    
    let speed = 2.9; 
    let angle = Math.atan2(py - my, px - mx);
    let vx = Math.cos(angle) * speed;
    let vy = Math.sin(angle) * speed;

    let movedX = false, movedY = false;

    if(!isSolid(mx + vx, my)) {
      mx += vx;
      movedX = true;
    }
    if(!isSolid(mx, my + vy)) {
      my += vy;
      movedY = true;
    }

    if(!movedX && !movedY) {
      if(!isSolid(mx + speed, my)) mx += speed;
      else if(!isSolid(mx - speed, my)) mx -= speed;
      else if(!isSolid(mx, my + speed)) my += speed;
      else if(!isSolid(mx, my - speed)) my -= speed;
    }

    if(dist < 28) lose("괴물에게 붙잡혔습니다!");
  } 
  else {
    isChased = false;
    document.getElementById('alert').style.display = 'none';
    if(!isHidden) {
      stopChaseBGM();
      startAmbientBGM();
    }
    
    let tDist = Math.hypot(mTargetX - mx, mTargetY - my);
    if(tDist < 25) {
      pickMonsterNewTarget();
    } else {
      let speed = 1.8;
      let angle = Math.atan2(mTargetY - my, mTargetX - mx);
      let vx = Math.cos(angle) * speed;
      let vy = Math.sin(angle) * speed;

      let movedX = false, movedY = false;
      if(!isSolid(mx + vx, my)) { mx += vx; movedX = true; }
      if(!isSolid(mx, my + vy)) { my += vy; movedY = true; }

      if(!movedX && !movedY) {
        pickMonsterNewTarget();
      }
    }
  }
}

function updateCamera() {
  const container = document.getElementById('map-container');
  let camX = 500 - px;
  let camY = 325 - py;
  container.style.transform = `translate(${camX}px, ${camY}px)`;
}

function draw() {
  const p = document.getElementById('player');
  const m = document.getElementById('monster');
  p.style.left = px + 'px'; p.style.top = py + 'px';
  m.style.left = mx + 'px'; m.style.top = my + 'px';

  document.getElementById('pShadow').style.left = px + 'px';
  document.getElementById('pShadow').style.top = (py + 16) + 'px';
  document.getElementById('mShadow').style.left = mx + 'px';
  document.getElementById('mShadow').style.top = (my + 16) + 'px';
}

function nextHideKey() {
  const keys = ['W', 'A', 'S', 'D'];
  targetKey = keys[Math.floor(Math.random() * 4)];
  document.getElementById('keyDisplay').textContent = targetKey;
}

function handleHideInput(k) {
  if(k === targetKey) {
    requiredPresses--;
    document.getElementById('reqCount').textContent = requiredPresses;
    if(requiredPresses <= 0) {
      exitCabinetQTESuccess();
      return;
    }
    nextHideKey();
  } else {
    qteHp--;
    document.getElementById('qteHp').textContent = qteHp;
    if(qteHp <= 0) lose("캐비닛 안에서 소음을 내 잡히고 말았습니다!");
  }
}

function updateHideLogic(dt) {
  if(!isQTEActive) return;
  
  hideTimer -= dt;
  let percentage = Math.max(0, (hideTimer / maxHideTime) * 100);
  document.getElementById('gaugeBar').style.width = percentage + '%';
  
  if(hideTimer <= 0) {
    lose("시간 내에 숨소리를 조절하지 못해 괴물에게 캐비닛이 열렸습니다!");
  }
}

function exitCabinetQTESuccess() {
  isQTEActive = false;
  isChased = false;
  stopChaseBGM();
  startAmbientBGM();
  
  pickMonsterNewTarget();
  mx = mTargetX; 
  my = mTargetY;
  stealthTimer = 2.0;

  document.getElementById('qteBox').classList.add('hidden');
  document.getElementById('safeBox').classList.remove('hidden');
  document.getElementById('mission').textContent = '괴물이 당신을 놓치고 떠났습니다! 원하는 때에 [E] 키를 눌러 나가세요.';
}

function exitCabinetSafe() {
  playLockerSound();
  isHidden = false;
  startAmbientBGM();
  document.getElementById('hideUI').classList.add('hidden');
}

function lose(reason) {
  gameEnded = true;
  stopChaseBGM();
  stopAmbientBGM();
  document.getElementById('world').classList.add('hidden');
  document.getElementById('hideUI').classList.add('hidden');
  document.getElementById('gameover').classList.remove('hidden');
  document.getElementById('overReason').textContent = reason;
}

function win() {
  gameEnded = true;
  stopChaseBGM();
  stopAmbientBGM();
  document.getElementById('world').classList.add('hidden');
  document.getElementById('winScreen').classList.remove('hidden');
  
  if (!isMainGame) {
    document.getElementById('winTitle').textContent = "🎓 튜토리얼 클리어!";
    document.getElementById('winDesc').textContent = "기본 생존 수칙을 모두 익혔습니다. 이제 본 게임으로 입장합니다...";
    const btn = document.getElementById('winBtn');
    btn.textContent = "본 게임 시작하기";
    btn.onclick = function() { startMainGame(); };
  } else {
    document.getElementById('winTitle').textContent = "🏆 게임 최종 클리어!";
    document.getElementById('winDesc').textContent = "축하합니다! 방을 탐험하며 열쇠를 모아 무사히 탈출했습니다!";
    const btn = document.getElementById('winBtn');
    btn.textContent = "첫 화면으로 돌아가기";
    btn.onclick = function() { location.reload(); };
  }
}

let lastTime = performance.now();
function gameLoop(now) {
  if(gameEnded) return;
  let dt = (now - lastTime) / 1000;
  lastTime = now;

  if(!isPaused) {
    if(stealthTimer > 0) stealthTimer -= dt;

    if(!isHidden) {
      updatePlayer();
    } else if(isQTEActive) {
      updateHideLogic(dt);
    }

    updateMonster();
    updateCamera();
    draw();
  }

  requestAnimationFrame(gameLoop);
}

window.addEventListener('DOMContentLoaded', () => {
  initPreviews();
});
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=750, scrolling=False)
