# cfe_simulator.py
import streamlit as st
import json
import os
import time

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Session state
if "q" not in st.session_state:
    st.session_state.q = None
    st.session_state.idx = 0
    st.session_state.answers = {}
    st.session_state.show_calc = False
    st.session_state.start = None

# Load questions
def load(file):
    with open(os.path.join(DATA_DIR, file), "r", encoding="utf-8") as f:
        return json.load(f)

files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
st.set_page_config(page_title="CFE 2025 Exam Simulator", layout="centered")
st.title("CFE 2025 Exam Simulator")
st.caption("400+ real-style questions • Calculator • Numeric answers • English")

with st.sidebar:
    st.header("Load Exam")
    if files:
        choice = st.selectbox("Question bank", files)
        if st.button("Start Exam", type="primary"):
            st.session_state.q = load(choice)
            st.session_state.idx = 0
            st.session_state.answers = {}
            st.session_state.start = time.time()
            st.rerun()
    else:
        st.warning("No JSON file in data/ folder")
        st.info("Run: python generate_cfe_questions.py first")

    if st.button("Calculator"):
        st.session_state.show_calc = True

if not st.session_state.q:
    st.stop()

q = st.session_state.q[st.session_state.idx]
st.write(f"**Question {st.session_state.idx + 1} / {len(st.session_state.q)}** • {q.get('section','')}")

# Timer
if st.session_state.start:
    elapsed = time.time() - st.session_state.start
    mins = int((180*60 - elapsed)//60)
    secs = int(180*60 - elapsed) % 60
    st.sidebar.metric("Time Left", f"{mins:02d}:{secs:02d}")

st.markdown(f"### {q['question']}")

# Numeric question
if q.get("type") == "Numeric":
    ans = st.text_input("Your answer (numbers only)", 
                        value=st.session_state.answers.get(st.session_state.idx, ""),
                        key=f"num{st.session_state.idx}")
    if ans:
        st.session_state.answers[st.session_state.idx] = ans
    if st.button("Check"):
        try:
            if abs(float(ans.replace(",","")) - float(q["correct"])) <= 10:
                st.success("Correct!")
            else:
                st.error(f"Wrong → Correct: {q['correct']:,}")
        except:
            st.error("Enter a number")

    with st.expander("Show work & explanation"):
        st.text_area("Your calculations", height=120, key=f"work{st.session_state.idx}")
        st.write(q["explanation"])

# Multiple choice
else:
    opts = q["options"]
    prev = st.session_state.answers.get(st.session_state.idx)
    choice = st.radio("Choose", 
                      [f"{k}. {v}" for k, v in opts.items()],
                      index=next((i for i,k in enumerate(opts) if k==prev), None),
                      key=f"mc{st.session_state.idx}")
    if choice:
        st.session_state.answers[st.session_state.idx] = choice[0]
        if choice[0] == q["correct"]:
            st.success("Correct!")
        else:
            st.error(f"Wrong → {q['correct']}. {opts[q['correct']]}")
    with st.expander("Explanation"):
        st.write(q.get("explanation",""))

# Calculator
if st.session_state.show_calc:
    st.markdown("### Calculator")
    if "calc" not in st.session_state: st.session_state.calc = ""
    cols = st.columns(4)
    for i, b in enumerate(["7","8","9","/","4","5","6","*","1","2","3","-","C","0",".","+","="]):
        with cols[i%4]:
            if st.button(b):
                if b=="C": st.session_state.calc=""
                elif b=="=":
                    try: st.session_state.calc = str(eval(st.session_state.calc))
                    except: st.session_state.calc="Error"
                else: st.session_state.calc += b
                st.rerun()
    st.text_input("Result", st.session_state.calc or "0", disabled=True)

# Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous") and st.session_state.idx > 0:
        st.session_state.idx -= 1
        st.rerun()
with col2:
    if st.button("Next →" if st.session_state.idx < len(st.session_state.q)-1 else "Finish"):
        if st.session_state.idx == len(st.session_state.q)-1:
            correct = sum(1 for i,a in st.session_state.answers.items()
                          if str(a).strip() == str(st.session_state.q[i]["correct"]).strip())
            st.balloons()
            st.success(f"Exam finished! Score: {correct}/{len(st.session_state.q)}")
        else:
            st.session_state.idx += 1
            st.rerun()
            
# ——————————————————————— BEAUTIFUL FOOTER ———————————————————————
st.markdown("---")

footer = """
<div style="
    background: linear-gradient(90deg, #1e3a8a, #3b82f6);
    color: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    margin-top: 40px;
">
    <h2>CFE 2025 Exam Simulator</h2>
    <p style="font-size: 1.1rem; margin: 10px 0;">
        100% Free • 100% Offline • 1000+ Unique Questions • Real Calculator & Timer
    </p>
    <p style="font-size: 1.3rem; margin: 15px 0;">
        Made with ❤️ by <strong>Moly-malibu</strong>
    </p>
    <p>
        Preparing for the CFE? You're not alone.<br>
        This tool was built to help you pass with confidence — no expensive courses needed.
    </p>
    <p style="margin-top: 20px; font-size: 1rem; opacity: 0.9;">
        Share with friends • Star on GitHub • Let's crush the CFE together!
    </p>
    <div style="margin-top: 15px;">
        <a href="https://github.com/Moly-malibu/CFE_Simulator" style="color:#fff; text-decoration: underline; font-weight: bold;">GitHub Repository</a>
        •
        <a href="mailto:your-email@example.com" style="color:#fff; text-decoration: underline;">Contact Me</a>
        •
        <a href="https://linkedin.com/in/yourprofile" style="color:#fff; text-decoration: underline;">LinkedIn</a>
    </div>
    <p style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
        © 2025 Moly-malibu  • Copyright Protected
    </p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

# Optional: Add a little celebration at the very bottom
st.markdown("<br><br>", unsafe_allow_html=True)
st.balloons()