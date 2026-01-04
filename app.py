import streamlit as st
import random
import time

# --- 1. 像素级还原图片设计风格 ---
st.markdown("""
<style>
/* 背景色：奶黄色 */
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #FFFBE6 !important;
}

/* 顶部胶囊切换按钮 */
.stButton > button[key^="nav_"] {
    border-radius: 50px !important;
    height: 45px !important;
    font-size: 16px !important;
    border: 2px solid #E0E0E0 !important;
    background-color: white !important;
    color: #666 !important;
}
.stButton > button[key*="active"] {
    background-color: #A3D9A5 !important; /* 绿色激活态 */
    color: white !important;
    border: none !important;
}

/* 主题目卡片：加厚橙/蓝边框 */
.question-container {
    background: white;
    border: 8px solid #FFB800; /* 标志性的黄色加厚边框 */
    border-radius: 40px;
    padding: 30px 15px;
    text-align: center;
    margin: 15px auto;
    max-width: 350px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}

.mode-label { color: #888; font-size: 14px; margin-bottom: 5px; text-align: left; padding-left: 10px; }
.huge-text { font-size: 80px !important; font-weight: 900; color: #333; margin: 10px 0; }

/* 答案按钮：还原图片中的 #FF6F61 红色 */
div[data-testid="stHorizontalBlock"] {
    max-width: 350px;
    margin: 0 auto;
}
.stButton > button[key^="btn_"] {
    background-color: #FF85A1 !important; /* 图片中的主红色 */
    color: white !important;
    border-radius: 12px !important;
    height: 65px !important;
    font-size: 24px !important;
    font-weight: bold !important;
    border: none !important;
    box-shadow: 0 4px 0 #FF477E !important; /* 底部深色投影 */
    margin-bottom: 10px !important;
}

/* 搞怪表情动画 */
@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    30% { transform: translate(3px, 2px) rotate(0deg); }
    50% { transform: translate(-1px, 2px) rotate(-1deg); }
    100% { transform: translate(1px, -2px) rotate(-1deg); }
}
.funny-error { font-size: 80px; text-align: center; animation: shake 0.5s infinite; }

/* 隐藏 Streamlit 默认页脚 */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 2. 核心词库与逻辑 ---
WORDS_DB = {
    "太阳": "☀️", "月亮": "🌙", "星星": "⭐", "彩虹": "🌈", "白云": "☁️",
    "下雨": "🌧️", "下雪": "❄️", "闪电": "⚡", "大风": "🌬️", "火焰": "🔥",
    "大树": "🌳", "森林": "🌲", "鲜花": "🌸", "草地": "🌱", "种子": "🌱",
    "泥土": "🟫", "高山": "⛰️", "大海": "🌊", "瀑布": "💦", "地球": "🌍",
    "小狗": "🐶", "小猫": "🐱", "兔子": "🐰", "熊猫": "🐼", "老虎": "🐯",
    "狮子": "🦁", "大象": "🐘", "长颈鹿": "🦒", "斑马": "🦓", "猴子": "🐵",
    "袋鼠": "🦘", "企鹅": "🐧", "松鼠": "🐿️", "小鸡": "🐥", "鸭子": "🦆",
    "孔雀": "🦚", "青蛙": "🐸", "乌龟": "🐢", "螃蟹": "🦀", "章鱼": "🐙",
    "蝴蝶": "🦋", "蜜蜂": "🐝", "蚂蚁": "🐜", "恐龙": "🦖", "金鱼": "🐠",
    "苹果": "🍎", "香蕉": "🍌", "西瓜": "🍉", "草莓": "🍓", "葡萄": "🍇",
    "菠萝": "🍍", "樱桃": "🍒", "桃子": "🍑", "梨子": "🍐", "柠檬": "🍋",
    "蔬菜": "🥗", "玉米": "🌽", "辣椒": "🌶️", "西红柿": "🍅", "胡萝卜": "🥕",
    "蘑菇": "🍄", "米饭": "🍚", "面包": "🍞", "鸡蛋": "🥚", "牛奶": "🥛",
    "汽车": "🚗", "公交车": "🚌", "火车": "🚂", "飞机": "✈️", "火箭": "🚀",
    "轮船": "🚢", "自行车": "🚲", "救护车": "🚑", "消防车": "🚒", "警车": "🚓",
    "房子": "🏠", "学校": "🏫", "医院": "🏥", "公园": "🌳", "城堡": "🏰",
    "书本": "📖", "铅笔": "✏️", "书包": "🎒", "剪刀": "✂️", "尺子": "📏",
    "衣服": "👕", "裙子": "👗", "鞋子": "👟", "帽子": "🎩", "雨伞": "☂️",
    "钥匙": "🔑", "时钟": "⏰", "手机": "📱", "电视": "📺", "牙刷": "🪥",
    "足球": "⚽", "篮球": "🏀", "游泳": "🏊", "跑步": "🏃", "跳舞": "💃",
    "唱歌": "🎤", "画画": "🎨", "睡觉": "😴", "开心": "😄", "礼物": "🎁"
}

def refresh_q(mode):
    st.session_state.answered = False
    st.session_state.show_error = False
    if mode == "math":
        op = random.choice(['+', '-'])
        if op == '+':
            n1 = random.randint(1, 8); n2 = random.randint(1, 10-n1)
            ans = n1 + n2
        else:
            n1 = random.randint(2, 10); n2 = random.randint(1, n1)
            ans = n1 - n2
        st.session_state.q_text = f"{n1} {op} {n2} = "
        st.session_state.q_ans = ans
        opts = {ans}
        while len(opts) < 4: opts.add(random.randint(0, 10))
        st.session_state.q_opts = sorted(list(opts))
    else:
        w = random.choice(list(WORDS_DB.keys()))
        st.session_state.w_target = w
        st.session_state.w_emoji = WORDS_DB[w]
        opts = random.sample([x for x in WORDS_DB.keys() if x != w], 3) + [w]
        random.shuffle(opts)
        st.session_state.q_opts = opts

# --- 3. 界面渲染 ---
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = "识字"
    refresh_q("word")

# 顶部切换区
st.write('<p style="text-align:center; font-weight:bold; font-size:24px; color:#444;">宝贝练习场</p>', unsafe_allow_html=True)
nav_c1, nav_c2 = st.columns(2)
with nav_c1:
    m_active = "_active" if st.session_state.game_mode == "数学" else ""
    if st.button("🔢 算术模式", key=f"nav_math{m_active}", use_container_width=True):
        st.session_state.game_mode = "数学"
        refresh_q("math")
        st.rerun()
with nav_c2:
    w_active = "_active" if st.session_state.game_mode == "识字" else ""
    if st.button("📖 识字模式", key=f"nav_word{w_active}", use_container_width=True):
        st.session_state.game_mode = "识字"
        refresh_q("word")
        st.rerun()

# 搞怪反馈
if st.session_state.get('show_error'):
    st.markdown(f'<p class="funny-error">{random.choice(["🤪", "👻", "🙊", "👽"])}</p>', unsafe_allow_html=True)

# 题目展示区
st.markdown(f'''
<div class="question-container">
    <div class="mode-label">Q) {st.session_state.game_mode} Q</div>
    <div class="huge-text">{(st.session_state.q_text if st.session_state.game_mode=="数学" else st.session_state.w_emoji)}</div>
    <div style="color:#888; font-size:12px;">stsesssion state 💡</div>
</div>
''', unsafe_allow_html=True)

# 选项按钮：2x2 排列
col_left, col_right = st.columns(2)
for i, opt in enumerate(st.session_state.q_opts):
    target_col = col_left if i < 2 else col_right
    if target_col.button(str(opt), key=f"btn_{opt}_{i}", use_container_width=True):
        is_correct = (st.session_state.game_mode == "数学" and opt == st.session_state.q_ans) or \
                     (st.session_state.game_mode == "识字" and opt == st.session_state.w_target)
        if is_correct:
            st.balloons()
            time.sleep(0.5) 
            refresh_q("math" if st.session_state.game_mode == "数学" else "word")
            st.rerun()
        else:
            st.session_state.show_error = True
            st.rerun()

# 下一题
if st.session_state.get('answered'):
    if st.button("🌟 下一题 🌟", key="next_step", use_container_width=True):
        refresh_q("math" if st.session_state.game_mode=="数学" else "word")
        st.rerun()
