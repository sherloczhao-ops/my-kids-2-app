import streamlit as st
import random

# --- 1. Apple 教育美学：极致空间优化与夜间模式锁定 ---
st.markdown("""
<style>
/* 锁定背景，适配所有模式 */
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #F2F2F7 !important; 
}

/* 顶部紧凑导航 */
.nav-container {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 5px;
}

/* 题目卡片：高度压缩 */
.question-card {
    background: white;
    border-radius: 25px;
    padding: 20px 10px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin: 5px 0;
}

.huge-emoji { font-size: 80px !important; margin: 0; }
.huge-math { font-size: 60px !important; font-weight: 800; color: #1D1D1F; margin: 0; }

/* 按钮网格：居中且间距合理 */
div[data-testid="stHorizontalBlock"] {
    gap: 10px !important;
}

.stButton button {
    width: 100% !important;
    height: 70px !important; /* 压缩高度以适应屏幕 */
    font-size: 26px !important;
    font-weight: 600;
    border-radius: 18px;
    border: none;
    background-color: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    color: #007AFF !important; /* Apple Blue */
}

/* 搞怪表情动画 */
@keyframes wobble {
    0% { transform: rotate(0deg); }
    25% { transform: rotate(-10deg); }
    75% { transform: rotate(10deg); }
    100% { transform: rotate(0deg); }
}
.funny-error {
    font-size: 100px;
    text-align: center;
    animation: wobble 0.3s ease-in-out;
}

/* 隐藏不必要的 Streamlit 元素 */
#MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. 核心逻辑与 100 词库 ---
WORDS_DB = {
    "太阳": "☀️", "月亮": "🌙", "大树": "🌳", "苹果": "🍎", "小狗": "🐶",
    "汽车": "🚗", "飞机": "✈️", "兔子": "🐰", "大象": "🐘", "花朵": "🌸",
    "糖果": "🍬", "雨伞": "☂️", "香蕉": "🍌", "西瓜": "🍉", "书本": "📖"
    # ... 保持之前的100词库
}

def refresh_q(mode):
    st.session_state.answered = False
    st.session_state.wrong_trigger = False
    if mode == "math":
        op = random.choice(['+', '-'])
        if op == '+':
            n1 = random.randint(1, 8); n2 = random.randint(1, 10-n1)
            ans = n1 + n2
        else:
            n1 = random.randint(2, 10); n2 = random.randint(1, n1)
            ans = n1 - n2
        st.session_state.m_q = f"{n1} {op} {n2}"
        st.session_state.m_ans = ans
        opts = {ans}
        while len(opts) < 4: opts.add(random.randint(0, 10))
        st.session_state.m_opts = sorted(list(opts))
    else:
        w = random.choice(list(WORDS_DB.keys()))
        st.session_state.w_target = w
        st.session_state.w_emoji = WORDS_DB[w]
        opts = random.sample([x for x in WORDS_DB.keys() if x != w], 3) + [w]
        random.shuffle(opts)
        st.session_state.w_opts = opts

# --- 3. 游戏渲染 ---
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "识字"
    refresh_q("word")

# 顶部紧凑导航
c1, c2 = st.columns(2)
with c1:
    if st.button("🔢 算术", type="primary" if st.session_state.game_mode=="数学" else "secondary"):
        st.session_state.game_mode = "数学"
        refresh_q("math")
        st.rerun()
with c2:
    if st.button("📖 识字", type="primary" if st.session_state.game_mode=="识字" else "secondary"):
        st.session_state.game_mode = "识字"
        refresh_q("word")
        st.rerun()

# 搞怪表情处理逻辑
if st.session_state.get('wrong_trigger'):
    st.markdown(f'<p class="funny-error">{random.choice(["🤪", "👻", "🙊", "🙉", "👽"])}</p>', unsafe_allow_html=True)
    st.toast("不对哦，再猜猜！")

# 主展示区
st.markdown('<div class="question-card">', unsafe_allow_html=True)
if st.session_state.game_mode == "数学":
    st.markdown(f'<p class="huge-math">{st.session_state.m_q} = ?</p>', unsafe_allow_html=True)
else:
    st.markdown(f'<p class="huge-emoji">{st.session_state.word_emoji}</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 答案按钮：2x2 排列
col_a, col_b = st.columns(2)
current_opts = st.session_state.m_opts if st.session_state.game_mode == "数学" else st.session_state.w_opts

for i, opt in enumerate(current_opts):
    target_col = col_a if i < 2 else col_b
    if target_col.button(str(opt), key=f"btn_{opt}_{i}"):
        correct = (st.session_state.game_mode == "数学" and opt == st.session_state.m_ans) or \
                  (st.session_state.game_mode == "识字" and opt == st.session_state.w_target)
        if correct:
            st.session_state.answered = True
            st.session_state.wrong_trigger = False
            st.balloons()
        else:
            st.session_state.wrong_trigger = True
            st.rerun()

# 成功后的下一步
if st.session_state.get('answered'):
    if st.button("✅ 做对啦！点我下一题", use_container_width=True):
        refresh_q("math" if st.session_state.game_mode=="数学" else "word")
        st.rerun()
