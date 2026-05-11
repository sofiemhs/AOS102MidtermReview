import streamlit as st
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="ClimateScience PRO", page_icon="🌍", layout="wide")

# --- CUSTOM "PRETYYYYY" CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #0f172a;
    }

    .main {
        background-color: #f8fafc;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #38bdf8;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #0ea5e9;
        transform: translateY(-2px);
    }

    .lesson-card {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }

    .progress-sidebar {
        background-color: #0f172a;
        color: white;
        padding: 20px;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'completed_lessons' not in st.session_state:
    st.session_state.completed_lessons = set()

# --- SIDEBAR PROGRESS TRACKER ---
with st.sidebar:
    st.markdown("### 🗺️ Study Progress")
    st.progress(st.session_state.progress / 100)
    st.write(f"**Total Completion:** {st.session_state.progress}%")
    st.write("---")
    
    lesson_choice = st.radio(
        "Select Lesson:",
        ["Welcome Page", "1. Variability & Pillars", "2. Models & Radiation", "3. Dynamic Physics", "4. El Niño (ENSO)", "5. Global Warming & Feedbacks"]
    )
    
    if st.button("Clear Progress"):
        st.session_state.progress = 0
        st.session_state.completed_lessons = set()
        st.rerun()

# --- LESSONS ---

if lesson_choice == "Welcome Page":
    st.title("🌍 Climate Science Master Navigator")
    st.markdown("""
    ### Welcome to your Interactive Study Guide!
    This app is designed to teach you everything from **Atmospheric Physics** to **Global Warming Scenarios**.
    
    **How to use:**
    1. Select a lesson from the sidebar.
    2. Read through the deep-dive content.
    3. Pass the **Interactive Knowledge Check** to gain progress points.
    4. Complete all lessons to reach 100%!
    """)
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1000&auto=format&fit=crop")

elif lesson_choice == "1. Variability & Pillars":
    st.title("🌀 Lesson 1: Climate Variability")
    
    with st.container():
        st.markdown("""
        <div class="lesson-card">
        <h3>The Pillars of Variability</h3>
        <p>Climate isn't just one thing—it's a mix of three distinct sources:</p>
        <ul>
            <li><b>Internal Variability:</b> Natural wobbles (ENSO, NAO).</li>
            <li><b>Natural External Forcing:</b> Solar changes, Milankovitch cycles (Earth's orbit), Volcanic dust.</li>
            <li><b>Anthropogenic Forcing:</b> CO2, Methane, and Sulfates.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Knowledge Check")
    q1 = st.radio("Which of these is a 'Natural External' forcing?", ["CO2 Emissions", "Milankovitch Cycles", "El Niño"])
    if st.button("Submit Answer"):
        if q1 == "Milankovitch Cycles":
            st.success("Correct! 🚀")
            if "L1" not in st.session_state.completed_lessons:
                st.session_state.progress += 20
                st.session_state.completed_lessons.add("L1")
        else:
            st.error("Try again! Remember: External forcing comes from outside the climate system.")

elif lesson_choice == "2. Models & Radiation":
    st.title("☀️ Lesson 2: Models & Radiation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Radiation Laws</h3>
        <p>The energy emitted by Earth follows the <b>Stefan-Boltzmann Law</b>:</p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"E = \sigma T^4")
        st.write("This means a small change in temperature (T) leads to a massive change in energy output!")

    with col2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Model Hierarchy</h3>
        <p>Climate is a <b>Boundary Value Problem</b>. We use a hierarchy to simulate it:</p>
        <ul>
            <li><b>EBMs:</b> Simple energy math.</li>
            <li><b>GCMs:</b> 3D math on a global grid.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Albedo Calculator")
    albedo = st.slider("Adjust Earth Albedo (0.3 is average)", 0.0, 1.0, 0.3)
    st.write(f"At {albedo} albedo, the Earth reflects {albedo*100}% of sunlight.")
    
    if st.button("Complete Lesson 2"):
        if "L2" not in st.session_state.completed_lessons:
            st.session_state.progress += 20
            st.session_state.completed_lessons.add("L2")
            st.rerun()

elif lesson_choice == "3. Dynamic Physics":
    st.title("🌪️ Lesson 3: Geophysical Dynamics")
    st.write("Understand the forces moving air and water.")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>The Balance of Forces</h3>
    <p><b>Geostrophic Balance:</b> The state where the <b>Pressure Gradient Force</b> (PGF) is exactly countered by the <b>Coriolis Force</b>.</p>
    <ul>
        <li>In the Northern Hemisphere, Coriolis turns wind to the <b>Right</b>.</li>
        <li><b>Rossby Waves:</b> These are the giant 'meanders' in the Jet Stream that cause weather patterns.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r"P = \rho R T")
    st.caption("The Equation of State for Atmosphere.")
    
    if st.button("Complete Lesson 3"):
        if "L3" not in st.session_state.completed_lessons:
            st.session_state.progress += 20
            st.session_state.completed_lessons.add("L3")
            st.rerun()

elif lesson_choice == "4. El Niño (ENSO)":
    st.title("🌊 Lesson 4: ENSO & Walker Circulation")
    
    tab1, tab2 = st.tabs(["Normal State", "El Niño"])
    
    with tab1:
        st.write("Trade winds blow East to West, cold water upwells in South America.")
    with tab2:
        st.write("Trade winds collapse, warm pool sloshes East. Thermocline flattens.")
    
    st.warning("**Bjerknes Feedback:** A self-reinforcing loop where weak winds lead to warmer waters, which lead to even weaker winds!")
    
    if st.button("Complete Lesson 4"):
        if "L4" not in st.session_state.completed_lessons:
            st.session_state.progress += 20
            st.session_state.completed_lessons.add("L4")
            st.rerun()

elif lesson_choice == "5. Global Warming & Feedbacks":
    st.title("🔥 Lesson 5: Global Warming & Scenarios")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>Feedback Loops</h3>
    <ul>
        <li><b>Water Vapor (+):</b> Biggest amplifier.</li>
        <li><b>Ice-Albedo (+):</b> Causes Polar Amplification.</li>
        <li><b>Lapse Rate (-):</b> Stabilizing feedback in tropics.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("**The Commitment:** Even if emissions stop, temps rise for decades because the Deep Ocean takes forever to warm up.")
    
    if st.button("Finish Course!"):
        if "L5" not in st.session_state.completed_lessons:
            st.session_state.progress = 100
            st.session_state.completed_lessons.add("L5")
            st.balloons()
            st.rerun()

if st.session_state.progress == 100:
    st.title("🏆 100% COMPLETE!")
    st.success("You have mastered Climate Dynamics! You're ready for GitHub.")

Your slide deck and GitHub-ready Python code are both complete! This structure provides the deep detail from your notes with a highly professional and "pretty" design. Feel free to explore the interactive components!
