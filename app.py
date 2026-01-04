import streamlit as st
import random

# --- 页面配置 ---
st.set_page_config(page_title="宝贝识字大王", page_icon="📖")

# 自定义 CSS：大字体，圆角彩色按钮
st.markdown("""
    <style>
    .word-font { font-size: 100px !important; font-weight: bold; text-align: center; color: #4A90E2; padding: 20px; }
    .stButton>button { 
        width: 100%; height: 90px; font-size: 35px !important; 
        border-radius: 30px; background-color: #E1F5FE; border: 2px solid #81D4FA;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 核心词库（爸爸可以随时在这里增加新词） ---
# 格式：汉字 : 对应的 Emoji 提示
WORDS_DB = {
    "太阳": "☀️", "月亮": "🌙", "大树": "🌳", "花朵": "🌸",
    "苹果": "🍎", "大象": "🐘", "小猫": "🐱", "小狗": "🐶",
    "爸爸": "👨", "妈妈": "👩", "雨伞": "☂️", "汽车": "🚗",
    "星星": "⭐", "西瓜": "🍉", "兔子": "🐰", "书本": "📖"
}

# --- 初始化题目 ---
if 'target_word' not in st.session_state:
    # 随机选一个目标词
    word = random.choice(list(WORDS_DB.keys()))
    st.session_state.target_word = word
    st.session_state.target_emoji = WORDS_DB[word]
    
    # 随机选 3 个干扰项
    others = random.sample([w for w in WORDS_DB.keys() if w != word], 3)
    options = [word] + others
    random.shuffle(options)
    st.session_state.word_options = options
    st.session_state.result = None

# --- 显示界面 ---
st.write("<center><h3>看图识字：这是什么？</h3></center>", unsafe_allow_html=True)

# 显示巨大的 Emoji 提示图
st.markdown(f'<p style="font-size:120px; text-align:center;">{st.session_state.target_emoji}</p>', unsafe_allow_html=True)

# 显示四个汉字按钮
cols = st.columns(2)
for i, opt in enumerate(st.session_state.word_options):
    with cols[i % 2]:
        if st.button(opt, key=f"word_{i}"):
            if opt == st.session_state.target_word:
                st.session_state.result = "win"
            else:
                st.session_state.result = "try"

# --- 反馈逻辑 ---
if st.session_state.result == "win":
    st.markdown(f'<p class="word-font">认对啦！这是「{st.session_state.target_word}」</p>', unsafe_allow_html=True)
    st.balloons()
    if st.button("真厉害！下一题 🚀"):
        for key in ['target_word', 'target_emoji', 'word_options', 'result']:
            del st.session_state[key]
        st.rerun()

elif st.session_state.result == "try":
    st.markdown("<h2 style='text-align: center;'>🐱 🐥 🌈</h2>", unsafe_allow_html=True)
    st.warning("再观察一下图片，试着读出来哦！")
