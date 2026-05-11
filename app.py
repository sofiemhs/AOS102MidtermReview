import streamlit as st

st.set_page_config(page_title="Climate Physics Master", layout="wide")

# Progress Tracking Logic
if 'progress' not in st.session_state: st.session_state.progress = 0

def complete_lesson(amount):
    st.session_state.progress = min(st.session_state.progress + amount, 100)

st.sidebar.title("📚 Curriculum")
st.sidebar.progress(st.session_state.progress / 100)
page = st.sidebar.radio("Go to:", ["Course Intro", "1. Model Hierarchy", "2. Radiation Laws", "3. ENSO & Feedbacks", "4. Warming Scenarios"])

if page == "Course Intro":
    st.title("🌍 Climate Science Masterclass")
    st.markdown("### Interactive Study Guide & Progress Tracker")
    st.write("This app is designed to teach you the specific physical mechanisms of climate variability.")
    if st.button("Start Lesson"): complete_lesson(5)

elif page == "1. Model Hierarchy":
    st.header("1. The Model Hierarchy")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Energy Balance Models (EBMs)**")
        st.write("Calculates Earth's temp based on energy in ($S_0$) and out ($T^4$). Good for first-order physics.")
    with col2:
        st.success("**General Circulation Models (GCMs)**")
        st.write("The most complex. Solves 3D equations for wind, ocean, and ice. Uses a grid system.")
    
    st.subheader("Knowledge Check")
    ans = st.selectbox("Which model treats Earth as a single point?", ["GCM", "EBM", "Intermediate"])
    if ans == "EBM": 
        st.balloons()
        complete_lesson(25)

elif page == "2. Radiation Laws":
    st.header("2. Stefan-Boltzmann & Albedo")
    st.latex(r"E = \sigma T^4")
    st.write("Double the temp? You get **16 times** the radiation output. This is why small changes in T are so powerful.")
    st.write("---")
    albedo = st.slider("Adjust Planet Albedo (Reflectivity)", 0.0, 1.0, 0.3)
    st.write(f"At {albedo} albedo, the planet reflects {albedo*100}% of incoming sunlight.")
    if st.button("Mastered this topic"): complete_lesson(20)

elif page == "3. ENSO & Feedbacks":
    st.header("3. The ENSO Mechanism")
    st.markdown("#### The Bjerknes Feedback Loop")
    st.write("1. Trade winds weaken.")
    st.write("2. Warm pool moves East.")
    st.write("3. Temp gradient drops.")
    st.write("4. Trade winds weaken *more*.")
    st.warning("This is a POSITIVE feedback loop!")
    if st.button("Understand the loop"): complete_lesson(25)

elif page == "4. Warming Scenarios":
    st.header("4. Commitment & Sea Level")
    st.write("Even if CO2 stops today, the ocean's **Heat Capacity** means warming continues.")
    st.error("Polar Amplification: The Arctic warms faster because of the Ice-Albedo feedback.")
    if st.button("Finish Course"): complete_lesson(25)

st.sidebar.write(f"Course Progress: {st.session_state.progress}%")

Feel free to take a look and let me know if you'd like to adjust any of the visuals or add more quiz questions!
