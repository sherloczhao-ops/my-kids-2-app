import streamlit as st
import random

# --- 侧边栏导航 ---
st.sidebar.title("🌟 宝贝的学习乐园")
choice = st.sidebar.radio("想玩什么呢？", ["10以内加减法", "看图识字大王"])

# --- 1. 数学模块 ---
if choice == "10以内加减法":
    st.title("🔢 数学小天才")
    if 'm_n1' not in st.session_state:
        op = random.choice(['+', '-'])
        if op == '+':
            n1 = random.randint(1, 8); n2 = random.randint(1, 10-n1)
        else:
            n1 = random.randint(2, 10); n2 = random.randint(1, n1)
        st.session_state.update({'m_n1':n1, 'm_n2':n2, 'm_op':op, 'm_ans':(n1+n2 if op=='+' else n1-n2)})
    
    st.markdown(f"<h1 style='text-align:center; font-size:80px;'>{st.session_state.m_n1} {st.session_state.m_op} {st.session_state.m_n2} = ?</h1>", unsafe_allow_html=True)
    ans = st.number_input("在这里输入答案哦", min_value=0, max_value=10, step=1, key="math_input")
    if st.button("检查一下"):
        if ans == st.session_state.m_ans:
            st.balloons(); st.success("太棒了！🍭")
            if st.button("下一题"): 
                for k in ['m_n1','m_n2','m_op','m_ans']: del st.session_state[k]
                st.rerun()
        else: st.error("再数数手指头哦 🌈")

# --- 2. 识字模块 ---
else:
    st.title("📖 识字大王")
    words = {"太阳": "☀️", "月亮": "🌙", "苹果": "🍎", "小猫": "🐱", "大树": "🌳"}
    if 'w_target' not in st.session_state:
        target = random.choice(list(words.keys()))
        opts = random.sample(list(words.keys()), 3)
        if target not in opts: opts[0] = target
        random.shuffle(opts)
        st.session_state.update({'w_target':target, 'w_emoji':words[target], 'w_opts':opts})
    
    st.markdown(f"<p style='font-size:120px; text-align:center;'>{st.session_state.w_emoji}</p>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, opt in enumerate(st.session_state.w_opts):
        with cols[i%2]:
            if st.button(opt, key=f"w_{i}"):
                if opt == st.session_state.w_target:
                    st.balloons(); st.success(f"对啦！这是「{opt}」✨")
                    if st.button("下一题 🚀"):
                        for k in ['w_target','w_emoji','w_opts']: del st.session_state[k]
                        st.rerun()
                else: st.warning("再观察一下图片哦 🐥")