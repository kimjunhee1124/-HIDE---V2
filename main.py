from pathlib import Path
import re

src = Path("/mnt/data/붙여넣은 텍스트 (1)(1).txt")
text = src.read_text(encoding="utf-8")

new_js = r"""
let audioCtx = null;
let chaseBgmInterval = null;
let ambientBgmInterval = null;
let heartbeatInterval = null;
let bgmStep = 0;
let ambientStep = 0;

function initAudio(){
  try{
    if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if(audioCtx.state === 'suspended') audioCtx.resume();
  }catch(e){}
}

function beep(freq=440, duration=.08, type='square', volume=.05){
  try{
    initAudio();
    if(!audioCtx) return;
    const now=audioCtx.currentTime;
    const o=audioCtx.createOscillator(), g=audioCtx.createGain();
    o.type=type; o.frequency.setValueAtTime(freq,now);
    g.gain.setValueAtTime(volume,now);
    g.gain.exponentialRampToValueAtTime(.001,now+duration);
    o.connect(g); g.connect(audioCtx.destination);
    o.start(now); o.stop(now+duration);
  }catch(e){}
}

function playLockerSound(){ beep(95,.18,'square',.09); setTimeout(()=>beep(55,.12,'sawtooth',.05),70); }
function playDoorSound(){ beep(170,.10,'square',.07); setTimeout(()=>beep(240,.16,'square',.05),90); }
function playKeySound(){ beep(880,.07,'sine',.07); setTimeout(()=>beep(1175,.12,'sine',.05),70); }

function startAmbientBGM(){
  if(ambientBgmInterval || chaseBgmInterval) return;
  initAudio();
  ambientStep=0;
  ambientBgmInterval=setInterval(()=>{
    if(!audioCtx || audioCtx.state!=='running') return;
    const notes=[130.81,164.81,196,146.83,110];
    beep(notes[ambientStep++%notes.length],1.0,'sine',.018);
  },2800);
}
function stopAmbientBGM(){
  if(ambientBgmInterval){clearInterval(ambientBgmInterval);ambientBgmInterval=null;}
}

function startHeartbeat(){
  if(heartbeatInterval) return;
  heartbeatInterval=setInterval(()=>{
    if(!isChased || gameEnded) return;
    beep(58,.07,'sine',.09);
    setTimeout(()=>beep(58,.07,'sine',.07),115);
  },650);
}
function stopHeartbeat(){
  if(heartbeatInterval){clearInterval(heartbeatInterval);heartbeatInterval=null;}
}

function startChaseBGM(){
  if(chaseBgmInterval) return;
  stopAmbientBGM();
  initAudio();
  bgmStep=0;
  startHeartbeat();
  chaseBgmInterval=setInterval(()=>{
    if(!audioCtx || audioCtx.state!=='running') return;
    const freqs=[82.41,82.41,98,73.42,110,82.41];
    beep(freqs[bgmStep++%freqs.length],.18,bgmStep%3===0?'sawtooth':'square',.055);
  },220);
}
function stopChaseBGM(){
  if(chaseBgmInterval){clearInterval(chaseBgmInterval);chaseBgmInterval=null;}
  stopHeartbeat();
}

const TILE_SIZE=40;
const MAIN_ROWS=40, MAIN_COLS=40;
const maxHideTime=6.0;

const maleSVG=`
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
<rect x="4" y="1" width="8" height="2" fill="#2c3e50"/><rect x="3" y="2" width="10" height="4" fill="#2c3e50"/>
<rect x="4" y="5" width="8" height="5" fill="#f3d2b3"/><rect x="5" y="7" width="2" height="2" fill="#111"/><rect x="9" y="7" width="2" height="2" fill="#111"/>
<rect x="3" y="10" width="10" height="5" fill="#2980b9"/><rect x="4" y="15" width="3" height="4" fill="#34495e"/><rect x="9" y="15" width="3" height="4" fill="#34495e"/>
<rect x="3" y="18" width="4" height="2" fill="#111"/><rect x="9" y="18" width="4" height="2" fill="#111"/>
</svg>`;

const femaleSVG=`
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
<rect x="3" y="1" width="10" height="3" fill="#5d4037"/><rect x="2" y="3" width="12" height="7" fill="#5d4037"/>
<rect x="4" y="5" width="8" height="5" fill="#f3d2b3"/><rect x="5" y="7" width="2" height="2" fill="#111"/><rect x="9" y="7" width="2" height="2" fill="#111"/>
<rect x="3" y="10" width="10" height="4" fill="#2980b9"/><rect x="3" y="14" width="10" height="3" fill="#c0392b"/>
<rect x="4" y="18" width="3" height="2" fill="#111"/><rect x="9" y="18" width="3" height="2" fill="#111"/>
</svg>`;

const monsterSVG=`
<svg viewBox="0 0 16 20" xmlns="http://www.w3.org/2000/svg">
<rect x="3" y="2" width="10" height="15" fill="#15181d"/><rect x="2" y="5" width="12" height="10" fill="#252b33"/>
<rect x="4" y="6" width="3" height="3" fill="#e74c3c"/><rect x="9" y="6" width="3" height="3" fill="#e74c3c"/>
<rect x="5" y="11" width="6" height="2" fill="#000"/><rect x="3" y="17" width="3" height="3" fill="#111"/><rect x="10" y="17" width="3" height="3" fill="#111"/>
</svg>`;

const keySVG=`
<svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" class="key-icon">
<path d="M6 2C3.8 2 2 3.8 2 6s1.8 4 4 4c1 0 1.9-.4 2.5-1L11 11.5V13h2v-2h1V9l-2.5-2.5C12 5.9 12 5 12 4c0-2-2-2-6-2ZM6 4c1.1 0 2 .9 2 2S7.1 8 6 8 4 7.1 4 6s.9-2 2-2Z" fill="#f1c40f"/>
</svg>`;

let mapData=[];
let selectedGender='male';
let isMainGame=false;
let currentArea='tutorial'; // tutorial | main | room
let currentRoomSide=null;
let mapRows=25,mapCols=25;

let px=100,py=100,mx=460,my=460;
let qteHp=3,keyCount=0,targetKeys=1;
let isHidden=false,isChased=false,isQTEActive=false,gameEnded=false,isPaused=true;
let stealthTimer=0,targetKey='W',hideTimer=6,requiredPresses=5;
let keysPressed={};
let mTargetX=460,mTargetY=460;
let monsterMemoryTimer=0;
let monsterAwareness=0;
let roomLayouts={};

function initPreviews(){
  const m=document.getElementById('mPrev'), f=document.getElementById('fPrev');
  if(m)m.innerHTML=`<div class="sprite" style="position:relative">${maleSVG}</div>`;
  if(f)f.innerHTML=`<div class="sprite" style="position:relative">${femaleSVG}</div>`;
}

function setMapSize(rows,cols){
  mapRows=rows; mapCols=cols;
  const mc=document.getElementById('map-container');
  mc.style.width=(cols*TILE_SIZE)+'px';
  mc.style.height=(rows*TILE_SIZE)+'px';
}

function addMainDoor(r,c){ mapData[r][c]=5; }
function isInside(r,c){ return r>0 && r<mapRows-1 && c>0 && c<mapCols-1; }

function generateTutorialMap(){
  currentArea='tutorial'; currentRoomSide=null; targetKeys=1;
  setMapSize(25,25); mapData=[]; const free=[];
  for(let r=0;r<25;r++){
    const row=[];
    for(let c=0;c<25;c++){
      if(r===0||r===24||c===0||c===24) row.push(1);
      else if(r%4===0&&c%4===0&&Math.random()>.25) row.push(1);
      else {row.push(0);if(r>4&&c>4&&!(r===23&&c===23))free.push({r,c});}
    }
    mapData.push(row);
  }
  mapData[1][1]=0;mapData[1][2]=0;mapData[2][1]=0;mapData[2][2]=0;
  [{r:3,c:3},{r:8,c:12},{r:12,c:8},{r:18,c:18}].forEach(p=>mapData[p.r][p.c]=2);
  const k=free[Math.floor(Math.random()*free.length)]; if(k)mapData[k.r][k.c]=3;
  mapData[23][23]=4;
}

function carveMainCorridors(){
  // 보장된 순환형 복도. 완전 랜덤 미로가 아니라 추격전이 가능한 구조.
  for(let r=2;r<MAIN_ROWS-2;r++){
    mapData[r][2]=0; mapData[r][3]=0;
    mapData[r][MAIN_COLS-3]=0; mapData[r][MAIN_COLS-4]=0;
  }
  for(let c=2;c<MAIN_COLS-2;c++){
    mapData[2][c]=0; mapData[3][c]=0;
    mapData[MAIN_ROWS-3][c]=0; mapData[MAIN_ROWS-4][c]=0;
  }
  for(let c=5;c<MAIN_COLS-5;c++) if(c%6!==0){mapData[20][c]=0;mapData[21][c]=0;}
  for(let r=5;r<MAIN_ROWS-5;r++) if(r%6!==0){mapData[r][20]=0;mapData[r][21]=0;}
}

function generateMainMap(){
  currentArea='main'; currentRoomSide=null; targetKeys=3;
  setMapSize(MAIN_ROWS,MAIN_COLS); mapData=[]; const free=[];
  for(let r=0;r<MAIN_ROWS;r++){
    const row=[];
    for(let c=0;c<MAIN_COLS;c++){
      if(r===0||r===MAIN_ROWS-1||c===0||c===MAIN_COLS-1) row.push(1);
      else if(Math.random()<.18) row.push(1);
      else {row.push(0);if(r>4&&c>4)free.push({r,c});}
    }
    mapData.push(row);
  }
  carveMainCorridors();

  const cabs=[
    [5,6],[5,15],[5,28],[9,10],[10,31],[15,7],[15,27],
    [22,8],[22,31],[28,12],[29,25],[34,7],[34,27]
  ];
  cabs.forEach(([r,c])=>{if(isInside(r,c)&&mapData[r][c]===0)mapData[r][c]=2;});

  const reserved=new Set(cabs.map(p=>p.join(',')));
  const keySpots=[
    {r:8,c:34},{r:31,c:4},{r:27,c:33}
  ];
  keySpots.forEach(p=>{
    if(mapData[p.r][p.c]===1)mapData[p.r][p.c]=0;
    mapData[p.r][p.c]=3;
  });

  // 네 변 중앙의 문.
  addMainDoor(0,Math.floor(MAIN_COLS/2));
  addMainDoor(MAIN_ROWS-1,Math.floor(MAIN_COLS/2));
  addMainDoor(Math.floor(MAIN_ROWS/2),0);
  addMainDoor(Math.floor(MAIN_ROWS/2),MAIN_COLS-1);

  // 최종 탈출문.
  mapData[MAIN_ROWS-2][MAIN_COLS-2]=4;
}

function generateRoom(side){
  currentArea='room'; currentRoomSide=side;
  const layouts={
    top:{rows:15,cols:23,style:'library'},
    bottom:{rows:18,cols:18,style:'classroom'},
    left:{rows:17,cols:13,style:'storage'},
    right:{rows:14,cols:21,style:'office'}
  };
  const s=layouts[side];
  setMapSize(s.rows,s.cols); mapData=[];
  for(let r=0;r<mapRows;r++){
    const row=[];
    for(let c=0;c<mapCols;c++) row.push((r===0||r===mapRows-1||c===0||c===mapCols-1)?1:0);
    mapData.push(row);
  }

  // 방마다 형태가 확실히 다르게 보이도록 가구/벽 배치.
  if(side==='top'){
    for(let c=3;c<9;c++)mapData[4][c]=1;
    for(let c=13;c<20;c++)mapData[4][c]=1;
    for(let r=7;r<12;r++)mapData[r][5]=1;
    for(let r=7;r<12;r++)mapData[r][17]=1;
    for(let c=8;c<16;c++)mapData[10][c]=1;
  }else if(side==='bottom'){
    for(let c=2;c<7;c++)mapData[3][c]=1;
    for(let c=11;c<16;c++)mapData[3][c]=1;
    for(let c=4;c<14;c++)mapData[8][c]=1;
    for(let r=10;r<15;r++)mapData[r][4]=1;
    for(let r=10;r<15;r++)mapData[r][13]=1;
  }else if(side==='left'){
    for(let r=3;r<9;r++)mapData[r][3]=1;
    for(let r=11;r<15;r++)mapData[r][7]=1;
    for(let c=5;c<11;c++)mapData[6][c]=1;
    for(let c=2;c<8;c++)mapData[12][c]=1;
  }else{
    for(let c=3;c<10;c++)mapData[3][c]=1;
    for(let r=5;r<11;r++)mapData[r][5]=1;
    for(let r=5;r<11;r++)mapData[r][15]=1;
    for(let c=8;c<19;c++)mapData[10][c]=1;
  }

  const cab={
    top:{r:2,c:2},bottom:{r:2,c:mapCols-3},
    left:{r:mapRows-3,c:2},right:{r:mapRows-3,c:mapCols-3}
  }[side];
  if(cab&&mapData[cab.r][cab.c]===0)mapData[cab.r][cab.c]=2;

  if(side==='top'){
    mapData[mapRows-1][Math.floor(mapCols/2)]=5;
  }else if(side==='bottom'){
    mapData[0][Math.floor(mapCols/2)]=5;
  }else if(side==='left'){
    mapData[Math.floor(mapRows/2)][mapCols-1]=5;
  }else{
    mapData[Math.floor(mapRows/2)][0]=5;
  }
}

function setWorldPosition(x,y){px=x;py=y;}

function enterRoom(side){
  if(!isMainGame||currentArea!=='main'||isHidden)return;
  const chasedBefore=isChased;
  const oldPx=px,oldPy=py;
  playDoorSound();
  generateRoom(side);

  if(side==='top'){
    setWorldPosition(Math.floor(mapCols/2)*TILE_SIZE+20,(mapRows-2)*TILE_SIZE+20);
    mx=chasedBefore?Math.floor(mapCols/2)*TILE_SIZE+20:(mapCols-2)*TILE_SIZE+20;
    my=chasedBefore?Math.max(60,py-180):60;
  }else if(side==='bottom'){
    setWorldPosition(Math.floor(mapCols/2)*TILE_SIZE+20,60);
    mx=chasedBefore?Math.floor(mapCols/2)*TILE_SIZE+20:(mapCols-2)*TILE_SIZE+20;
    my=chasedBefore?py+180:(mapRows-2)*TILE_SIZE+20;
  }else if(side==='left'){
    setWorldPosition((mapCols-2)*TILE_SIZE+20,Math.floor(mapRows/2)*TILE_SIZE+20);
    mx=chasedBefore?px+180:60; my=chasedBefore?py:(mapRows-2)*TILE_SIZE+20;
  }else{
    setWorldPosition(60,Math.floor(mapRows/2)*TILE_SIZE+20);
    mx=chasedBefore?px-180:(mapCols-2)*TILE_SIZE+20; my=chasedBefore?py:60;
  }

  isChased=chasedBefore;
  monsterMemoryTimer=chasedBefore?4:0;
  renderMap();updateCamera();
  document.getElementById('mission').textContent=chasedBefore?'문을 닫을 틈도 없습니다. 괴물이 따라 들어왔습니다!':'문 안쪽은 다른 공간으로 이어져 있습니다...';
}

function leaveRoom(){
  if(currentArea!=='room'||isHidden)return;
  const side=currentRoomSide;
  const chasedBefore=isChased;
  playDoorSound();
  generateMainMap();

  if(side==='top'){px=20*Math.floor(0+MAIN_COLS/2)+20;py=80;}
  else if(side==='bottom'){px=Math.floor(MAIN_COLS/2)*TILE_SIZE+20;py=(MAIN_ROWS-3)*TILE_SIZE+20;}
  else if(side==='left'){px=80;py=Math.floor(MAIN_ROWS/2)*TILE_SIZE+20;}
  else{px=(MAIN_COLS-3)*TILE_SIZE+20;py=Math.floor(MAIN_ROWS/2)*TILE_SIZE+20;}

  // 방을 나가도 괴물의 추격 상태를 유지한다.
  isChased=chasedBefore;
  if(chasedBefore){
    if(side==='top'){mx=px;my=py+180;}
    else if(side==='bottom'){mx=px;my=py-180;}
    else if(side==='left'){mx=px+180;my=py;}
    else{mx=px-180;my=py;}
  }else{mx=20*TILE_SIZE+20;my=20*TILE_SIZE+20;}
  currentArea='main';currentRoomSide=null;monsterMemoryTimer=chasedBefore?4:0;
  renderMap();updateCamera();
  document.getElementById('mission').textContent='다시 학교 복도로 나왔습니다. 괴물이 아직 근처에 있을지도 모릅니다.';
}

function generateMap(){
  if(isMainGame)generateMainMap(); else generateTutorialMap();
}

function renderMap(){
  const container=document.getElementById('tiles');
  if(!container)return;
  let html='';
  const floor=isMainGame?'floor-main':'floor-tut';
  for(let r=0;r<mapRows;r++)for(let c=0;c<mapCols;c++){
    const type=mapData[r][c]; let cls=floor,content='';
    if(type===1)cls='wall';
    else if(type===2)cls='cab';
    else if(type===3){cls='key-item';content=keySVG;}
    else if(type===4){cls='door';content='EXIT';}
    else if(type===5){cls='door-wood';content='DOOR';}
    html+=`<div class="tile ${cls}" style="left:${c*TILE_SIZE}px;top:${r*TILE_SIZE}px;">${content}</div>`;
  }
  container.innerHTML=html;
}

function resetState(){
  px=100;py=100;mx=11*TILE_SIZE+20;my=11*TILE_SIZE+20;
  qteHp=3;keyCount=0;isHidden=false;isChased=false;isQTEActive=false;gameEnded=false;
  stealthTimer=0;keysPressed={};currentRoomSide=null;monsterMemoryTimer=0;monsterAwareness=0;
  stopChaseBGM();stopAmbientBGM();
  generateMap();renderMap();
  document.getElementById('keyCount').textContent=keyCount;
  document.getElementById('targetKeyCount').textContent=targetKeys;
  document.getElementById('qteHp').textContent=qteHp;
  document.getElementById('alert').style.display='none';
  document.getElementById('hideUI').classList.add('hidden');
  document.getElementById('gameover').classList.add('hidden');
  document.getElementById('winScreen').classList.add('hidden');
  document.getElementById('mission').textContent=isMainGame?'[본 게임] 열쇠 3개를 찾고 EXIT로 탈출하세요.':'[튜토리얼] 열쇠를 찾으세요!';
}

function startGame(gender){
  initAudio();selectedGender=gender;isMainGame=false;isPaused=false;
  document.getElementById('title').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  document.getElementById('tutorialNotice').classList.remove('hidden');
  document.getElementById('winScreen').classList.add('hidden');
  resetState();startAmbientBGM();
  document.getElementById('player').innerHTML=selectedGender==='female'?femaleSVG:maleSVG;
  document.getElementById('monster').innerHTML=monsterSVG;
  updateCamera();draw();
}

function closeTutorial(){
  document.getElementById('tutorialNotice').classList.add('hidden');
  isPaused=false;
  startAmbientBGM();
}

function startMainGame(){
  initAudio();isMainGame=true;isPaused=false;gameEnded=false;
  document.getElementById('winScreen').classList.add('hidden');
  document.getElementById('world').classList.remove('hidden');
  document.getElementById('tutorialNotice').classList.add('hidden');
  resetState();
  // 시작 직후에는 괴물이 플레이어를 즉시 공격하지 않도록 거리를 둔다.
  px=2*TILE_SIZE+20;py=2*TILE_SIZE+20;
  mx=(MAIN_COLS-3)*TILE_SIZE+20;my=(MAIN_ROWS-3)*TILE_SIZE+20;
  renderMap();updateCamera();draw();startAmbientBGM();
}

function restartGame(){
  document.getElementById('gameover').classList.add('hidden');
  isMainGame=false;isPaused=false;gameEnded=false;
  document.getElementById('title').classList.remove('hidden');
  document.getElementById('world').classList.add('hidden');
  document.getElementById('winScreen').classList.add('hidden');
  stopChaseBGM();stopAmbientBGM();
}

function getCurrentTile(){
  return {r:Math.floor(py/TILE_SIZE),c:Math.floor(px/TILE_SIZE)};
}

function isSolid(x,y){
  const radius=11;
  const pts=[[x-radius,y-radius],[x+radius,y-radius],[x-radius,y+radius],[x+radius,y+radius]];
  return pts.some(([xx,yy])=>{
    const c=Math.floor(xx/TILE_SIZE),r=Math.floor(yy/TILE_SIZE);
    if(r<0||r>=mapRows||c<0||c>=mapCols)return true;
    return mapData[r][c]===1;
  });
}

function tryMove(entity,x,y){
  if(!isSolid(x,y)){entity.x=x;entity.y=y;return true;}
  return false;
}

function updatePlayer(){
  if(isPaused||gameEnded||isHidden)return;
  let dx=0,dy=0;
  if(keysPressed['w']||keysPressed['arrowup'])dy-=1;
  if(keysPressed['s']||keysPressed['arrowdown'])dy+=1;
  if(keysPressed['a']||keysPressed['arrowleft'])dx-=1;
  if(keysPressed['d']||keysPressed['arrowright'])dx+=1;
  if(!dx&&!dy)return;
  const len=Math.hypot(dx,dy);dx/=len;dy/=len;
  const speed=isChased?3.45:3.0;
  const nx=px+dx*speed,ny=py+dy*speed;
  const e={x:px,y:py};
  if(tryMove(e,nx,py))px=e.x;
  e.x=px;e.y=py;if(tryMove(e,px,ny))py=e.y;
}

function doorSideAtPlayer(){
  if(currentArea==='main'){
    const r=Math.floor(py/TILE_SIZE),c=Math.floor(px/TILE_SIZE);
    if(r===0&&c===Math.floor(MAIN_COLS/2))return'top';
    if(r===MAIN_ROWS-1&&c===Math.floor(MAIN_COLS/2))return'bottom';
    if(c===0&&r===Math.floor(MAIN_ROWS/2))return'left';
    if(c===MAIN_COLS-1&&r===Math.floor(MAIN_ROWS/2))return'right';
  }else if(currentArea==='room')return currentRoomSide;
  return null;
}

function handleInteraction(){
  if(gameEnded)return;
  const {r,c}=getCurrentTile();
  if(r<0||r>=mapRows||c<0||c>=mapCols)return;

  if(isHidden){
    if(!isQTEActive)exitCabinetSafe();
    return;
  }

  const type=mapData[r][c];

  if(type===5){
    if(currentArea==='main'){
      const side=doorSideAtPlayer();
      if(side)enterRoom(side);
    }else leaveRoom();
    return;
  }

  if(type===2){
    playLockerSound();
    const dist=Math.hypot(px-mx,py-my);
    if(isChased||dist<300){
      isHidden=true;isQTEActive=true;hideTimer=maxHideTime;requiredPresses=5;qteHp=3;
      document.getElementById('hideUI').classList.remove('hidden');
      document.getElementById('qteBox').classList.remove('hidden');
      document.getElementById('safeBox').classList.add('hidden');
      document.getElementById('qteHp').textContent=qteHp;
      document.getElementById('reqCount').textContent=requiredPresses;
      document.getElementById('gaugeBar').style.width='100%';
      nextHideKey();startChaseBGM();
    }else{
      isHidden=true;isQTEActive=false;
      document.getElementById('hideUI').classList.remove('hidden');
      document.getElementById('qteBox').classList.add('hidden');
      document.getElementById('safeBox').classList.remove('hidden');
      document.getElementById('mission').textContent='캐비닛 안에 숨었습니다. 밖으로 나가려면 [E]';
    }
  }else if(type===3){
    playKeySound();keyCount++;mapData[r][c]=0;
    document.getElementById('keyCount').textContent=keyCount;
    document.getElementById('mission').textContent=keyCount>=targetKeys?'열쇠를 모두 찾았습니다. EXIT로 가세요!':`열쇠 획득 (${keyCount}/${targetKeys})`;
    renderMap();
  }else if(type===4){
    if(keyCount>=targetKeys)win();
    else document.getElementById('mission').textContent=`아직 열쇠가 ${targetKeys-keyCount}개 남았습니다.`;
  }
}

function pickMonsterTarget(){
  const candidates=[];
  for(let r=1;r<mapRows-1;r++)for(let c=1;c<mapCols-1;c++){
    if(mapData[r][c]===0)candidates.push({x:c*TILE_SIZE+20,y:r*TILE_SIZE+20});
  }
  if(candidates.length){
    const p=candidates[Math.floor(Math.random()*candidates.length)];
    mTargetX=p.x;mTargetY=p.y;
  }
}

function canSeePlayer(){
  const dx=px-mx,dy=py-my,dist=Math.hypot(dx,dy);
  if(dist>430)return false;
  const steps=Math.ceil(dist/16);
  for(let i=1;i<steps;i++){
    const x=mx+dx*i/steps,y=my+dy*i/steps;
    const c=Math.floor(x/TILE_SIZE),r=Math.floor(y/TILE_SIZE);
    if(r<0||c<0||r>=mapRows||c>=mapCols)return false;
    if(mapData[r][c]===1)return false;
  }
  return true;
}

function moveMonsterToward(tx,ty,speed){
  const dx=tx-mx,dy=ty-my,dist=Math.hypot(dx,dy);
  if(dist<1)return;
  const nx=mx+dx/dist*speed,ny=my+dy/dist*speed;
  const ex={x:mx,y:my};
  if(tryMove(ex,nx,my))mx=ex.x;
  ex.x=mx;ex.y=my;if(tryMove(ex,mx,ny))my=ex.y;

  // 벽 모서리에 걸리면 축을 바꿔 탈출한다.
  if(Math.abs(mx-ex.x)<.01 && Math.abs(my-ex.y)<.01){
    const alt=[[-speed,0],[speed,0],[0,-speed],[0,speed]];
    for(const [ax,ay] of alt){if(!isSolid(mx+ax,my+ay)){mx+=ax;my+=ay;break;}}
  }
}

function updateMonster(){
  if(gameEnded)return;
  if(isHidden&&isQTEActive){
    document.getElementById('alert').style.display='block';
    startChaseBGM();
    return;
  }

  const dist=Math.hypot(px-mx,py-my);
  const visible=canSeePlayer();

  // 한 번 발견되면 일정 시간 기억해서 문을 넘어가도 추격을 유지한다.
  if(!isHidden && (visible&&dist<430 || isChased || monsterMemoryTimer>0)){
    isChased=true;monsterMemoryTimer=3.2;
    document.getElementById('alert').style.display='block';
    startChaseBGM();
    moveMonsterToward(px,py,currentArea==='room'?3.15:3.0);

    if(dist<25)lose('괴물에게 붙잡혔습니다!');
    return;
  }

  if(monsterMemoryTimer>0)monsterMemoryTimer-=1/60;
  isChased=false;
  document.getElementById('alert').style.display='none';
  stopChaseBGM();startAmbientBGM();

  if(!isHidden){
    const td=Math.hypot(mTargetX-mx,mTargetY-my);
    if(td<28)pickMonsterTarget();
    else moveMonsterToward(mTargetX,mTargetY,1.25);
  }
}

function nextHideKey(){
  const arr=['W','A','S','D'];
  targetKey=arr[Math.floor(Math.random()*arr.length)];
  document.getElementById('keyDisplay').textContent=targetKey;
}

function handleHideInput(k){
  if(!isQTEActive)return;
  if(k===targetKey){
    beep(520,.05,'square',.04);
    requiredPresses--;
    document.getElementById('reqCount').textContent=requiredPresses;
    if(requiredPresses<=0){exitCabinetQTESuccess();return;}
    nextHideKey();
  }else{
    beep(75,.12,'sawtooth',.05);
    qteHp--;document.getElementById('qteHp').textContent=qteHp;
    if(qteHp<=0)lose('캐비닛 안에서 소리를 내고 말았습니다!');
  }
}

function updateHideLogic(dt){
  if(!isQTEActive)return;
  hideTimer-=dt;
  document.getElementById('gaugeBar').style.width=Math.max(0,hideTimer/maxHideTime*100)+'%';
  if(hideTimer<=0)lose('숨을 참는 데 실패해 괴물이 캐비닛을 열었습니다!');
}

function exitCabinetQTESuccess(){
  isQTEActive=false;isChased=false;stealthTimer=2.4;monsterMemoryTimer=0;
  stopChaseBGM();startAmbientBGM();
  pickMonsterTarget();mx=mTargetX;my=mTargetY;
  document.getElementById('qteBox').classList.add('hidden');
  document.getElementById('safeBox').classList.remove('hidden');
  document.getElementById('mission').textContent='괴물이 당신을 놓쳤습니다. [E]로 캐비닛에서 나오세요.';
}

function exitCabinetSafe(){
  playLockerSound();isHidden=false;
  document.getElementById('hideUI').classList.add('hidden');
  startAmbientBGM();
}

function lose(reason){
  if(gameEnded)return;
  gameEnded=true;isPaused=true;
  stopChaseBGM();stopAmbientBGM();
  document.getElementById('world').classList.add('hidden');
  document.getElementById('hideUI').classList.add('hidden');
  document.getElementById('gameover').classList.remove('hidden');
  document.getElementById('overReason').textContent=reason;
}

function win(){
  gameEnded=true;isPaused=true;
  stopChaseBGM();stopAmbientBGM();
  document.getElementById('world').classList.add('hidden');
  document.getElementById('winScreen').classList.remove('hidden');
  if(!isMainGame){
    document.getElementById('winTitle').textContent='🎓 튜토리얼 클리어!';
    document.getElementById('winDesc').textContent='기본 생존 수칙을 익혔습니다. 이제 본 게임으로 입장합니다.';
    document.getElementById('winBtn').textContent='본 게임 시작하기';
    document.getElementById('winBtn').onclick=startMainGame;
  }else{
    document.getElementById('winTitle').textContent='🏆 탈출 성공';
    document.getElementById('winDesc').textContent='세 개의 열쇠를 모두 찾아 학교를 빠져나왔습니다.';
    document.getElementById('winBtn').textContent='첫 화면으로';
    document.getElementById('winBtn').onclick=restartGame;
  }
}

function updateCamera(){
  const c=document.getElementById('map-container');
  c.style.transform=`translate(${500-px}px,${325-py}px)`;
}

function draw(){
  const p=document.getElementById('player'),m=document.getElementById('monster');
  p.style.left=px+'px';p.style.top=py+'px';
  m.style.left=mx+'px';m.style.top=my+'px';
  document.getElementById('pShadow').style.left=px+'px';document.getElementById('pShadow').style.top=(py+16)+'px';
  document.getElementById('mShadow').style.left=mx+'px';document.getElementById('mShadow').style.top=(my+16)+'px';
}

window.addEventListener('keydown',e=>{
  const k=e.key.toLowerCase();
  if(['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','e'].includes(k))e.preventDefault();
  if(isQTEActive){
    if(['w','a','s','d'].includes(k)){handleHideInput(k.toUpperCase());return;}
    return;
  }
  if(k==='e'){handleInteraction();return;}
  keysPressed[k]=true;
});
window.addEventListener('keyup',e=>{keysPressed[e.key.toLowerCase()]=false;});
window.addEventListener('blur',()=>{keysPressed={};});

let lastTime=performance.now();
function gameLoop(now){
  const dt=Math.min(.05,(now-lastTime)/1000);lastTime=now;
  if(!gameEnded&&!isPaused){
    if(stealthTimer>0)stealthTimer-=dt;
    if(!isHidden)updatePlayer(); else updateHideLogic(dt);
    updateMonster();updateCamera();draw();
  }
  requestAnimationFrame(gameLoop);
}

window.addEventListener('DOMContentLoaded',()=>{
  initPreviews();
  document.getElementById('player').innerHTML=maleSVG;
  document.getElementById('monster').innerHTML=monsterSVG;
  requestAnimationFrame(gameLoop);
});
"""

# Replace the entire script body while keeping the existing Streamlit/HTML/CSS shell.
text = re.sub(r'<script>.*?</script>', '<script>' + new_js + '\n</script>', text, flags=re.S)

# Fix the accidental duplicated .selects opening tag in the original shell.
text = text.replace(
    '<div class="selects">\n    <div class="selects">\n      <div class="pick"',
    '<div class="selects">\n      <div class="pick"'
)

# Make the main-stage title/notice explicitly mention doors and rooms.
text = text.replace(
    '괴물을 피해 열쇠를 모아 탈출하세요!',
    '괴물을 피해 열쇠를 모아 학교를 탈출하세요!'
)
text = text.replace(
    '<div id="alert">! 경고: 괴물이 추격 중 !</div>',
    '<div id="alert">! 경고: 괴물이 추격 중 !</div>'
)

out = Path("/mnt/data/HIDE_Pixel_School_개편본.py")
out.write_text(text, encoding="utf-8")
print(out)
print(f"{len(text.splitlines())} lines")
