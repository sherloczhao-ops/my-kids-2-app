import streamlit as st
import random

# --- 1. 强制视觉风格：适配手机、夜间模式与儿童化 ---
st.markdown("""
<style>
/* 强制背景色，防止夜间模式变黑看不清 */
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #FFF9E3 !important; /* 奶油暖黄色 */
}

/* 标题样式 */
.title-font {
    font-size: 40px !important;
    font-weight: 900;
    color: #FF6B6B;
    text-align: center;
    margin-bottom: 10px;
    text-shadow: 2px 2px #FFFFFF;
}

/* 核心题目卡片 */
.question-box {
    background: #FFFFFF;
    border: 6px solid #FFD93D; /* 明亮的黄色边框 */
    border-radius: 40px;
    padding: 30px 10px;
    text-align: center;
    margin: 10px 0;
    box-shadow: 0 10px 0 #FFD93D; /* 这种阴影更有卡通感 */
}

/* 巨大的题目文字：确保深色，不受系统影响 */
.huge-text {
    font-size: 85px !important;
    font-weight: 900;
    color: #2D3436 !important; /* 强制深灰黑色，保证看清 */
    margin: 20px 0;
}

/* 按钮：果冻感彩色按钮 */
.stButton button {
    background-color: #6C5CE7 !important; /* 漂亮的紫色 */
    color: white !important;
    border-radius: 30px !important;
    height: 100px !important;
    font-size: 35px !important;
    font-weight: 800 !important;
    border: none !important;
    box-shadow: 0 8px 0 #4834D4 !important;
    margin-bottom: 20px !important;
}

.stButton button:active {
    box-shadow: none !important;
    transform: translateY(8px) !important;
}

/* 底部切换按钮专供 */
.nav-button button {
    background-color: #FF8E3C !important;
    height: 60px !important;
    font-size: 20px !important;
}

/* 隐藏侧边栏，因为手机端侧边栏很难找 */
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# --- 2. 词库（保持100个） ---
WORDS_DB = {
    "太阳": "☀️", "月亮": "🌙", "星星": "⭐", "彩虹": "🌈", "大树": "🌳",
    "花朵": "🌸", "小猫": "🐱", "小狗": "🐶", "兔子": "🐰", "大象": "🐘",
    "苹果": "🍎", "香蕉": "🍌", "西瓜": "🍉", "汽车": "🚗", "飞机": "✈️",
    "爸爸": "👨", "妈妈": "👩", "书本": "📖", "铅笔": "✏️", "糖果": "🍬"
    # ... (为了代码简洁，这里展示核心，你可以继续按此格式补全到100个)
}

# --- 3. 逻辑函数 ---
def next_q(mode):
    st.session_state.answered = False
    if mode == "math":
        op = random.choice(['+', '-'])
        if op == '+':
            n1 = random.randint(1, 8); n2 = random.randint(1, 10-n1)
            ans = n1 + n2
        else:
            n1 = random.randint(2, 10); n2 = random.randint(1, n1)
            ans = n1 - n2
        st.session_state.math_q = f"{n1} {op} {n2}"
        st.session_state.math_ans = ans
        opts = {ans}
        while len(opts) < 4: opts.add(random.randint(0, 10))
        st.session_state.math_opts = sorted(list(opts))
    else:
        word = random.choice(list(WORDS_DB.keys()))
        st.session_state.word_target = word
        st.session_state.word_emoji = WORDS_DB[word]
        opts = [word] + random.sample([w for w in WORDS_DB.keys() if w != word], 3)
        random.shuffle(opts)
        st.session_state.word_opts = opts

# --- 4. 主界面渲染 ---
if 'mode' not in st.session_state: 
    st.session_state.mode = "识字"
    next_q("word")

# 顶部模式切换（不用侧边栏，直接放页面顶端）
st.write('<p class="title-font">🌟 宝贝闯关岛 🌟</p>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    if st.button("🔢 玩算术", key="nav_math"): 
        st.session_state.mode = "数学"
        next_q("math")
        st.rerun()
with c2:
    if st.button("📖 识汉字", key="nav_word"): 
        st.session_state.mode = "识字"
        next_q("word")
        st.rerun()

st.markdown("---")

# --- 游戏区域 ---
if st.session_state.mode == "数学":
    if 'math_q' not in st.session_state: next_q("math")
    st.markdown(f'<div class="question-box"><p class="huge-text">{st.session_state.math_q}</p></div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.math_opts):
        with cols[i%2]:
            if st.button(str(opt), key=f"m_{opt}"):
                if opt == st.session_state.math_ans:
                    st.session_state.answered = True
                    st.balloons()
                else:
                    st.toast("🍬 差一点点，再数一数？")

else:
    if 'word_target' not in st.session_state: next_q("word")
    st.markdown(f'<div class="question-box"><p class="huge-text">{st.session_state.word_emoji}</p></div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.word_opts):
        with cols[i%2]:
            if st.button(opt, key=f"w_{opt}"):
                if opt == st.session_state.word_target:
                    st.session_state.answered = True
                    st.balloons()
                else:
                    st.toast("🍦 换个词试试看哦？")

# 下一题按钮
if st.session_state.get('answered'):
    st.write("")
    if st.button("✨ 成功啦！点我下一题 ✨", key="next_total"):
        next_q("math" if st.session_state.mode == "数学" else "word")
        st.rerun()
