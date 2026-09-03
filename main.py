import streamlit as st
import random
import time

# ============================================================
# 공포 게임 - main.py
# Streamlit Single File Version
# ============================================================

st.set_page_config(
    page_title="THE EMPTY HOUSE",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: "Malgun Gothic", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at center,
            #202020 0%,
            #101010 45%,
            #050505 100%
        );
    color: #dddddd;
}

.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.game-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    letter-spacing: 8px;
    color: #d8d8d8;
    text-shadow:
        0 0 4px #ffffff33,
        0 0 18px #000000;
    margin-bottom: 5px;
}

.game-subtitle {
    text-align: center;
    color: #777777;
    font-size: 13px;
    letter-spacing: 4px;
    margin-bottom: 30px;
}

.story-box {
    background: rgba(10,10,10,0.88);
    border: 1px solid #333333;
    padding: 25px;
    border-radius: 4px;
    line-height: 1.9;
    color: #bdbdbd;
    box-shadow: 0 0 30px #000000;
}

.warning {
    color: #b33a3a;
    font-weight: bold;
}

.item-box {
    background: #111111;
    border: 1px solid #333333;
    padding: 14px;
    margin: 5px 0;
    border-radius: 3px;
}

.map-container {
    background: #080808;
    border: 2px solid #303030;
    padding: 12px;
    border-radius: 5px;
    box-shadow:
        inset 0 0 30px #000000,
        0 0 20px #000000;
}

.map-row {
    display: flex;
    justify-content: center;
}

.map-cell {
    width: 46px;
    height: 46px;
    margin: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    border-radius: 2px;
}

.wall {
    background: #151515;
    border: 1px solid #222222;
}

.floor {
    background: #353535;
    border: 1px solid #454545;
}

.player {
    background: #484848;
    border: 1px solid #777777;
    box-shadow: 0 0 12px #ffffff22;
}

.monster {
    background: #3a1111;
    border: 1px solid #762222;
    box-shadow: 0 0 15px #8b000044;
}

.key {
    background: #423a16;
    border: 1px solid #806f22;
}

.door {
    background: #152b19;
    border: 1px solid #305d38;
}

.exit {
    background: #162c35;
    border: 1px solid #315b68;
}

.status {
    background: #0d0d0d;
    border: 1px solid #292929;
    padding: 14px;
    text-align: center;
    margin-bottom: 15px;
    color: #aaa;
}

.death-screen {
    text-align: center;
    padding: 80px 20px;
    background: #050505;
    border: 1px solid #330000;
    box-shadow: 0 0 80px #300000;
}

.death-title {
    font-size: 54px;
    color: #8b1515;
    letter-spacing: 8px;
    font-weight: 900;
}

.escape-screen {
    text-align: center;
    padding: 70px 20px;
    background: #080d0a;
    border: 1px solid #315d3a;
}

.escape-title {
    font-size: 48px;
    color: #9bbba0;
    letter-spacing: 8px;
}

.message {
    background: #101010;
    border-left: 3px solid #555555;
    padding: 14px 18px;
    margin: 12px 0;
    color: #bdbdbd;
}

.secret-message {
    background: #120d0d;
    border-left: 3px solid #642020;
    padding: 16px;
    color: #c58d8d;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# GAME DATA
# ============================================================

MAP = [
    "###############",
    "#.....#.......#",
    "#.###.#.#####.#",
    "#.#...#.....#.#",
    "#.#.#######.#.#",
    "#.#...........#",
    "#.#####.#######",
    "#.......#.....#",
    "#######.#.###.#",
    "#.......#...#.#",
    "#.#########.#.#",
    "#...........#.#",
    "#.###########.#",
    "#.............#",
    "###############",
]

MAP_HEIGHT = len(MAP)
MAP_WIDTH = len(MAP[0])


# ============================================================
# SESSION STATE
# ============================================================

def init_game():
    st.session_state.started = False
    st.session_state.game_over = False
    st.session_state.escaped = False

    st.session_state.player = [1, 1]
    st.session_state.monster = [13, 13]

    st.session_state.key = [11, 1]
    st.session_state.exit = [13, 13]

    st.session_state.has_key = False
    st.session_state.door_open = False

    st.session_state.turn = 0

    st.session_state.message = (
        "어두운 집 안에서 정신을 차렸다."
    )

    st.session_state.messages = []

    st.session_state.found_note = False
    st.session_state.secret = False

    st.session_state.noise = 0

    st.session_state.monster_alert = 0

    st.session_state.last_move = time.time()


if "started" not in st.session_state:
    init_game()


# ============================================================
# UTILITY
# ============================================================

def is_wall(x, y):
    if y < 0 or y >= MAP_HEIGHT:
        return True

    if x < 0 or x >= MAP_WIDTH:
        return True

    return MAP[y][x] == "#"


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def add_message(text):
    st.session_state.messages.append(text)

    if len(st.session_state.messages) > 6:
        st.session_state.messages.pop(0)


def valid_position(x, y):
    return not is_wall(x, y)


# ============================================================
# MONSTER AI
# ============================================================

def monster_moves_toward_player():
    monster = st.session_state.monster
    player = st.session_state.player

    mx, my = monster
    px, py = player

    candidates = []

    dx = px - mx
    dy = py - my

    if abs(dx) > abs(dy):
        if dx > 0:
            candidates.append((mx + 1, my))
        elif dx < 0:
            candidates.append((mx - 1, my))

        if dy > 0:
            candidates.append((mx, my + 1))
        elif dy < 0:
            candidates.append((mx, my - 1))

    else:
        if dy > 0:
            candidates.append((mx, my + 1))
        elif dy < 0:
            candidates.append((mx, my - 1))

        if dx > 0:
            candidates.append((mx + 1, my))
        elif dx < 0:
            candidates.append((mx - 1, my))

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    random.shuffle(directions)

    for dx2, dy2 in directions:
        candidates.append((mx + dx2, my + dy2))

    for nx, ny in candidates:
        if valid_position(nx, ny):
            st.session_state.monster = [nx, ny]
            break


def monster_turn():
    if st.session_state.game_over:
        return

    if st.session_state.escaped:
        return

    distance_to_player = distance(
        st.session_state.player,
        st.session_state.monster
    )

    # 플레이어가 가까우면 더 적극적으로 움직임
    if distance_to_player <= 7:
        monster_moves_toward_player()
        st.session_state.monster_alert += 1

    else:
        # 멀리 있으면 가끔 랜덤 이동
        if random.random() < 0.45:
            monster_moves_toward_player()

    # 충돌
    if st.session_state.player == st.session_state.monster:
        st.session_state.game_over = True
        st.session_state.message = "무언가가 바로 뒤에 있었다."


# ============================================================
# EVENTS
# ============================================================

def check_events():

    px, py = st.session_state.player

    # 열쇠
    if [px, py] == st.session_state.key:

        if not st.session_state.has_key:
            st.session_state.has_key = True

            add_message(
                "바닥에서 오래된 열쇠 하나를 발견했다."
            )

            add_message(
                "열쇠에는 작은 숫자 '03'이 새겨져 있다."
            )

    # 특정 위치에서 메모 발견
    if [px, py] == [9, 11]:

        if not st.session_state.found_note:

            st.session_state.found_note = True

            add_message(
                "벽에 누군가 급하게 남긴 글씨가 있다."
            )

            add_message(
                "『문을 열지 마. 네가 들은 소리는 사람이 아니야.』"
            )

    # 비밀 이벤트
    if [px, py] == [1, 13]:

        if not st.session_state.secret:

            st.session_state.secret = True

            add_message(
                "벽 안쪽에서 이상한 긁는 소리가 들린다."
            )

    # 출구
    if [px, py] == st.session_state.exit:

        if st.session_state.has_key:

            st.session_state.door_open = True
            st.session_state.escaped = True
            st.session_state.message = (
                "열쇠가 맞았다. 문이 천천히 열렸다."
            )

        else:

            add_message(
                "문은 잠겨 있다. 열쇠가 필요하다."
            )


# ============================================================
# PLAYER MOVEMENT
# ============================================================

def move_player(dx, dy):

    if not st.session_state.started:
        return

    if st.session_state.game_over:
        return

    if st.session_state.escaped:
        return

    px, py = st.session_state.player

    nx = px + dx
    ny = py + dy

    if is_wall(nx, ny):

        add_message(
            "벽에 막혀 있다."
        )

        # 소음 증가
        st.session_state.noise += 1

        if st.session_state.noise >= 2:
            monster_turn()
            st.session_state.noise = 0

        return

    st.session_state.player = [nx, ny]

    st.session_state.turn += 1

    st.session_state.noise = 0

    check_events()

    monster_turn()

    # 가까워졌을 때 경고
    d = distance(
        st.session_state.player,
        st.session_state.monster
    )

    if d <= 3 and not st.session_state.game_over:

        add_message(
            "어딘가에서 발소리가 들린다."
        )

    elif d <= 5 and not st.session_state.game_over:

        add_message(
            "무언가가 가까이 있는 것 같다."
        )


# ============================================================
# MAP RENDER
# ============================================================

def render_map():

    player_x, player_y = st.session_state.player
    monster_x, monster_y = st.session_state.monster
    key_x, key_y = st.session_state.key
    exit_x, exit_y = st.session_state.exit

    html = '<div class="map-container">'

    for y in range(MAP_HEIGHT):

        html += '<div class="map-row">'

        for x in range(MAP_WIDTH):

            cell = MAP[y][x]

            cell_class = "floor"
            symbol = ""

            if cell == "#":

                cell_class = "wall"
                symbol = ""

            else:

                # 플레이어
                if [x, y] == [player_x, player_y]:

                    cell_class = "player"
                    symbol = "●"

                # 괴물
                elif [x, y] == [monster_x, monster_y]:

                    # 일정 거리 안에서만 표시
                    d = distance(
                        [player_x, player_y],
                        [monster_x, monster_y]
                    )

                    if d <= 6:

                        cell_class = "monster"
                        symbol = "?"

                    else:

                        cell_class = "floor"
                        symbol = ""

                # 열쇠
                elif [x, y] == [key_x, key_y]:

                    if not st.session_state.has_key:

                        cell_class = "key"
                        symbol = "◆"

                # 출구
                elif [x, y] == [exit_x, exit_y]:

                    cell_class = "exit"

                    if st.session_state.door_open:
                        symbol = "↗"
                    else:
                        symbol = "▣"

            html += (
                f'<div class="map-cell {cell_class}">'
                f'{symbol}'
                f'</div>'
            )

        html += '</div>'

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="game-title">THE EMPTY HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">SOMETHING IS STILL INSIDE</div>',
    unsafe_allow_html=True
)


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.started:

    st.markdown(
        """
        <div class="story-box">

        <b>새벽 2시 17분.</b>

        <br><br>

        눈을 뜨자 낯선 방이었다.

        <br><br>

        창문은 잠겨 있고,
        현관문은 굳게 닫혀 있다.

        <br>

        휴대폰은 켜지지 않는다.

        <br><br>

        그리고 집 안 어딘가에서,

        <br><br>

        <span class="warning">
        누군가 걷는 소리가 들린다.
        </span>

        <br><br>

        이곳에서 나가야 한다.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "게임 시작",
        use_container_width=True,
        type="primary"
    ):

        st.session_state.started = True

        st.session_state.message = (
            "어두운 방이다. 주변을 살펴보자."
        )

        add_message(
            "방 밖으로 나갈 방법을 찾아야 한다."
        )

        st.rerun()

    st.stop()


# ============================================================
# GAME OVER
# ============================================================

if st.session_state.game_over:

    st.markdown(
        """
        <div class="death-screen">

        <div class="death-title">
        CAUGHT
        </div>

        <br>

        뒤에서 들리던 발소리가 멈췄다.

        <br><br>

        그리고 모든 것이 조용해졌다.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "다시 시작",
        use_container_width=True
    ):

        init_game()
        st.rerun()

    st.stop()


# ============================================================
# ESCAPE
# ============================================================

if st.session_state.escaped:

    st.markdown(
        """
        <div class="escape-screen">

        <div class="escape-title">
        ESCAPED
        </div>

        <br>

        문 밖으로 나왔다.

        <br><br>

        차가운 새벽 공기가 느껴진다.

        <br><br>

        하지만 이상하다.

        <br><br>

        집 안쪽을 돌아보자,

        <br>

        2층 창문에 누군가 서 있었다.

        <br><br>

        <b>그리고 그 사람은 웃고 있었다.</b>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button(
        "처음부터 다시",
        use_container_width=True
    ):

        init_game()
        st.rerun()

    st.stop()


# ============================================================
# STATUS
# ============================================================

d = distance(
    st.session_state.player,
    st.session_state.monster
)

if d <= 2:

    status_text = "⚠️ 위험하다. 무언가가 바로 근처에 있다."

elif d <= 4:

    status_text = "발소리가 가까워지고 있다."

elif d <= 6:

    status_text = "멀리서 이상한 소리가 들린다."

else:

    status_text = "주변은 조용하다."

st.markdown(
    f"""
    <div class="status">
    {status_text}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MAIN GAME
# ============================================================

render_map()


# ============================================================
# CONTROLS
# ============================================================

st.write("")

st.markdown(
    "<div style='text-align:center;color:#777;'>MOVE</div>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col2:

    if st.button(
        "▲",
        use_container_width=True
    ):
        move_player(0, -1)
        st.rerun()


col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "◀",
        use_container_width=True
    ):
        move_player(-1, 0)
        st.rerun()

with col2:

    if st.button(
        "▼",
        use_container_width=True
    ):
        move_player(0, 1)
        st.rerun()

with col3:

    if st.button(
        "▶",
        use_container_width=True
    ):
        move_player(1, 0)
        st.rerun()


# ============================================================
# INVENTORY
# ============================================================

st.write("")

st.markdown(
    "<h4>소지품</h4>",
    unsafe_allow_html=True
)

if st.session_state.has_key:

    st.markdown(
        """
        <div class="item-box">
        🔑 오래된 열쇠
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="item-box">
        소지품 없음
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MESSAGE LOG
# ============================================================

st.write("")

st.markdown(
    "<h4>상황</h4>",
    unsafe_allow_html=True
)

for msg in reversed(st.session_state.messages):

    st.markdown(
        f"""
        <div class="message">
        {msg}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SECRET
# ============================================================

if st.session_state.secret:

    st.markdown(
        """
        <div class="secret-message">

        벽을 자세히 살펴보자.

        <br><br>

        긁힌 자국 사이에 작은 글자가 있다.

        <br><br>

        <b>03 · 17 · 02</b>

        <br><br>

        누군가 이 집에서 무언가를 반복하고 있었다.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DEBUG / GAME INFO
# ============================================================

with st.expander("게임 정보"):

    st.write(
        f"현재 위치: {st.session_state.player}"
    )

    st.write(
        f"괴물 위치: {st.session_state.monster}"
    )

    st.write(
        f"괴물까지 거리: {d}"
    )

    st.write(
        f"이동 횟수: {st.session_state.turn}"
    )

    st.write(
        f"열쇠 획득: {st.session_state.has_key}"
    )


# ============================================================
# RESTART
# ============================================================

st.write("")

if st.button(
    "게임 초기화",
    use_container_width=True
):

    init_game()
    st.rerun()
