import streamlit as st

# --- App Configuration ---
st.set_page_config(page_title="Climate Science Study Guide", page_icon="🌍", layout="centered")

# --- Initialize Session State (Tracking Progress) ---
if 'page' not in st.session_state:
    st.session_state.page = 'Cover'
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {'Lesson 1': 0, 'Lesson 2': 0, 'Lesson 3': 0}

# --- Navigation Functions ---
def go_to_page(page_name, progress_value):
    st.session_state.page = page_name
    st.session_state.progress = progress_value

def check_answer(lesson, correct_ans, user_ans):
    if user_ans == correct_ans:
        st.session_state.scores[lesson] = 1
        st.success("Correct! Great job. 🎉")
    else:
        st.session_state.scores[lesson] = 0
        st.error(f"Not quite! The correct answer was: {correct_ans}")

# --- Sidebar (Progress & Navigation) ---
with st.sidebar:
    st.title("🗺️ Navigation")
    st.progress(st.session_state.progress, text="Course Progress")
    
    st.write("---")
    st.write("### Quick Jump")
    if st.button("Cover Page"): go_to_page('Cover', 0)
    if st.button("Lesson 1: Basics"): go_to_page('Lesson 1', 25)
    if st.button("Lesson 2: Physics & ENSO"): go_to_page('Lesson 2', 50)
    if st.button("Lesson 3: Feedbacks"): go_to_page('Lesson 3', 75)
    if st.button("Finish & Review"): go_to_page('End', 100)

# --- Pages ---

if st.session_state.page == 'Cover':
    st.title("🌍 Master Climate Science")
    st.subheader("Your Interactive Study Guide")
    st.image("https://images.unsplash.com/photo-1611273426858-450d8e3c9cce?q=80&w=800&auto=format&fit=crop", caption="Let's understand our planet.")
    
    st.write("""
    Welcome to your custom climate science course! This app will guide you through:
    * The pillars of climate variability and models.
    * The physical processes governing the Earth.
    * El Niño and climate feedbacks.
    
    Read through the lessons, answer the interactive questions, and track your progress along the way.
    """)
    
    if st.button("🚀 Start Learning", type="primary"):
        go_to_page('Lesson 1', 25)
        st.rerun()

elif st.session_state.page == 'Lesson 1':
    st.title("📖 Lesson 1: Overview & Basics")
    st.write("---")
    
    st.header("The Three Pillars of Variability")
    st.write("""
    * **Internal Variability:** Natural 'wobbles' (e.g., El Niño).
    * **External Forcing (Natural):** Volcanic eruptions, solar output, Milankovitch cycles.
    * **External Forcing (Anthropogenic):** Greenhouse gas emissions and aerosols.
    """)
    
    st.header("Model Hierarchy")
    st.write("""
    * **Energy Balance Models (EBMs):** Treat Earth as a single point.
    * **Intermediate Models:** Focus on specific phenomena with simplified physics.
    * **General Circulation Models (GCMs):** 3D grids simulating wind, oceans, and biology.
    """)
    
    st.header("Basics of Global Climate")
    st.write("""
    * **Stefan-Boltzmann Law:** Energy emitted is proportional to Temperature to the 4th power. Double the temp = 16x the energy!
    * **Albedo:** Fraction of light reflected (~30% for Earth). More ice = more reflection = cooling.
    * **Carbon Reservoirs:** Deep Ocean (holds the most), Fossil Reserves, and Atmosphere (the 'control knob').
    """)
    
    st.write("---")
    st.subheader("🧠 Knowledge Check")
    q1 = st.radio("Which carbon reservoir acts as the 'control knob' for temperature?", 
                  ["Deep Ocean", "Atmosphere", "Fossil Reserves"], key="q1")
    if st.button("Submit Answer 1"):
        check_answer('Lesson 1', "Atmosphere", q1)
        
    if st.button("Next Lesson ➡️"):
        go_to_page('Lesson 2', 50)
        st.rerun()

elif st.session_state.page == 'Lesson 2':
    st.title("🌪️ Lesson 2: Physical Processes & ENSO")
    st.write("---")
    
    st.header("The Rules of the Game")
    st.write("""
    * **Equation of State:** Pressure = Density x Gas Constant x Temperature. In oceans, salinity also changes density.
    * **Geostrophic Balance:** When Pressure Gradient Force (pushing to low pressure) is balanced by the Coriolis Force (pulling to the side). Winds flow *around* pressure systems!
    * **Rossby Waves:** Giant meanders in the jet stream causing 'teleconnections' (e.g., warm Pacific causing cold NY).
    """)
    
    st.header("El Niño (ENSO)")
    st.write("""
    * **Normal State:** Trade winds blow East to West, pushing warm water to Indonesia.
    * **El Niño State:** Trade winds collapse. The 'Warm Pool' sloshes back East toward South America.
    * **Thermocline Feedback:** Weak winds -> Warmer East Pacific -> Reduced temp gradient -> Weaker winds (Self-reinforcing!).
    * **Delayed Oscillator:** Rossby waves hit the coast, reflect as Kelvin waves, and eventually shut off the warming.
    """)
    
    st.write("---")
    st.subheader("🧠 Knowledge Check")
    q2 = st.radio("What happens to trade winds during an El Niño event?", 
                  ["They strengthen and blow faster", "They collapse or reverse", "They blow North to South"], key="q2")
    if st.button("Submit Answer 2"):
        check_answer('Lesson 2', "They collapse or reverse", q2)
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Previous"): go_to_page('Lesson 1', 25); st.rerun()
    with col2:
        if st.button("Next Lesson ➡️"): go_to_page('Lesson 3', 75); st.rerun()

elif st.session_state.page == 'Lesson 3':
    st.title("🔥 Lesson 3: Feedbacks & Global Warming")
    st.write("---")
    
    st.header("The Greenhouse Effect")
    st.write("""
    * **Selective Absorption:** Atmosphere is transparent to Solar (shortwave) but opaque to Infrared (longwave). GHGs trap IR and re-emit it.
    """)
    
    st.header("Detailed Feedbacks")
    st.write("""
    * **Water Vapor (Positive):** Warmer -> More evaporation -> More GHG (water vapor) -> Warmer. (Biggest amplifier!)
    * **Lapse Rate (Negative):** Upper atmosphere warms faster, radiating heat to space efficiently.
    * **Cloud Feedback:** Low clouds cool (reflect sunlight), High clouds warm (trap heat).
    """)
    
    st.header("Global Warming Scenarios")
    st.write("""
    * **Radiative Forcing:** Net change in energy. CO2 is the dominant positive forcing.
    * **Commitment Concept:** Even if emissions stop today, temps will rise for decades as the Deep Ocean catches up.
    * **Polar Amplification:** The Arctic warms much faster due to the Ice-Albedo feedback.
    * **Sea Level Rise:** Caused by Thermal Expansion (warm water takes up more space) and Land Ice Melt (glaciers).
    """)
    
    st.write("---")
    st.subheader("🧠 Knowledge Check")
    q3 = st.radio("Which feedback is considered the single biggest amplifier of global warming?", 
                  ["Cloud Feedback", "Lapse Rate Feedback", "Water Vapor Feedback"], key="q3")
    if st.button("Submit Answer 3"):
        check_answer('Lesson 3', "Water Vapor Feedback", q3)
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Previous"): go_to_page('Lesson 2', 50); st.rerun()
    with col2:
        if st.button("Finish Course 🏆"): go_to_page('End', 100); st.rerun()

elif st.session_state.page == 'End':
    st.balloons()
    st.title("🎓 Course Completed!")
    st.write("---")
    
    st.subheader("Your Final Report")
    total_score = sum(st.session_state.scores.values())
    
    st.metric(label="Total Score", value=f"{total_score} / 3")
    
    if total_score == 3:
        st.success("Perfect Score! You are a climate science master. 🌟")
    elif total_score >= 1:
        st.warning("Great effort! Review the notes and try to get a perfect score next time.")
    else:
        st.error("Keep studying! You'll get it next time.")
        
    st.write("### Score Breakdown:")
    for lesson, score in st.session_state.scores.items():
        st.write(f"**{lesson}:** {'✅ Correct' if score == 1 else '❌ Incorrect'}")
        
    st.write("---")
    if st.button("🔄 Restart Course"):
        st.session_state.scores = {'Lesson 1': 0, 'Lesson 2': 0, 'Lesson 3': 0}
        go_to_page('Cover', 0)
        st.rerun()
