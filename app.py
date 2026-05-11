import streamlit as st

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Climate Science Master Guide", page_icon="🌍", layout="wide")

# --- CUSTOM CLIMATE THEME CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&family=Open+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Open Sans', sans-serif;
        color: #000000 !important; /* All text black */
    }
    
    h1, h2, h3, h4, h5 {
        font-family: 'Merriweather', serif;
        color: #000000 !important; /* All text black */
    }

    /* Main background - BLue */
    .stApp {
        background-color: #006884; 
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #059669; /* Earthy Emerald */
        color: #000000 !important; /* All text black */
        font-weight: bold;
        border: none;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        background-color: #047857; /* Darker Emerald */
        transform: translateY(-2px);
    }

    /* Content Cards */
    .lesson-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #005c5c; /* Deep aquamarine accent */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        color: #000000 !important; /* All text black */
    }
    
    .lesson-card h3 {
        margin-top: 0;
        color: #000000 !important; /* All text black */
    }

    .lesson-card li {
        margin-bottom: 8px;
        color: #000000 !important;
    }
    
    .lesson-card p {
        color: #000000 !important;
    }

    /* Info panels */
    .stAlert {
        background-color: #7cebeb; /* Lighter aquamarine for readability */
        color: #000000 !important; /* All text black */
        border: 1px solid #40B5AD;
    }
    
    /* Force sidebar text to be black */
    .st-emotion-cache-16txtl3 p {
        color: #000000 !important;
    }
    
    /* Force general markdown text to be black */
    .stMarkdown p, .stMarkdown li {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (Tracking Progress) ---
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'completed_lessons' not in st.session_state:
    st.session_state.completed_lessons = set()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 🌍 Course Navigator")
    
    # Calculate progress based on 7 chapters (approx 14.2% each)
    prog_percent = int((len(st.session_state.completed_lessons) / 7) * 100)
    st.progress(prog_percent / 100)
    st.write(f"**Mastery:** {prog_percent}%")
    st.write("---")
    
    lesson_choice = st.radio(
        "Select Chapter:",
        [
            "Welcome", 
            "1. Overview of Climate Variability", 
            "2. Basics of Global Climate", 
            "3. Physical Processes", 
            "4. El Niño & Predictions", 
            "5. Climate Models", 
            "6. Greenhouse Effect & Feedbacks",
            "7. Global Warming Scenarios"
        ]
    )
    
    st.write("---")
    if st.button("Reset Course"):
        st.session_state.progress = 0
        st.session_state.completed_lessons = set()
        st.rerun()

# --- HELPER FUNCTION FOR COMPLETION ---
def mark_completed(lesson_id):
    if lesson_id not in st.session_state.completed_lessons:
        st.session_state.completed_lessons.add(lesson_id)
        st.success(f"Chapter completed! You're making great progress.")
        st.balloons()
        st.rerun()

# ==========================================
# PAGE CONTENT
# ==========================================

if lesson_choice == "Welcome":
    st.title("🌱 Comprehensive Climate Science Guide")
    st.markdown("""
    <div class="lesson-card">
    <h3>Welcome to your fully elaborated study platform!</h3>
    <p>This application covers the entire 7-chapter syllabus of Earth's climate system, physical mechanisms, feedback loops, and global climate modeling.</p>
    <p><b>Instructions:</b></p>
    <ul>
        <li>Navigate through the chapters using the sidebar.</li>
        <li>Read the detailed breakdowns in the tabbed sections.</li>
        <li>Pass the Knowledge Check at the bottom of each chapter to track your progress.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --- CHAPTER 1 ---
elif lesson_choice == "1. Overview of Climate Variability":
    st.title("Chapter 1: Overview of Climate Variability")
    
    tab1, tab2, tab3 = st.tabs(["Dynamics & Systems", "El Niño & Global Warming", "Paleoclimate & History"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Climate Dynamics and Systems</h3>
        <p><b>Climate vs. Weather:</b> Weather is the exact state of the atmosphere at a given time (chaotic), while climate is the boundary value problem defining the statistics of weather over time.</p>
        <p><b>Chemical & Physical Aspects:</b> The climate is a coupled system involving the atmosphere, hydrosphere (oceans), cryosphere (ice), lithosphere (land), and biosphere. Trace gas concentrations (like CO2 and Methane) drastically alter the chemical makeup, leading to physical changes (temperature shifts).</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>El Niño & Global Change</h3>
        <p><b>El Niño:</b> The premier example of natural, internal climate variability. Studies of events like the massive 1997-98 El Niño paved the way for the first coupled ocean-atmosphere models used for forecasting.</p>
        <p><b>Recent History:</b> Global temperatures have risen alongside trace gas concentrations. We also monitor phenomena like the Ozone Hole, which has its own history of study and successful global mitigation (Montreal Protocol).</p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="lesson-card">
        <h3>Paleoclimate Variability</h3>
        <p>By studying ice cores, tree rings, and ocean sediments, we understand how climate behaved before human instrumentation. This gives us a baseline of natural variability (e.g., Milankovitch cycles causing ice ages) to compare against modern anthropogenic warming.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Knowledge Check")
    q1 = st.radio("Which of the following is considered 'natural, internal climate variability'?", ["Ozone Depletion", "El Niño", "Milankovitch Cycles"])
    if st.button("Submit Chapter 1"):
        if q1 == "El Niño": mark_completed("Ch1")
        else: st.error("Incorrect. Remember, El Niño is an internal wobble of the ocean-atmosphere system.")

# --- CHAPTER 2 ---
elif lesson_choice == "2. Basics of Global Climate":
    st.title("Chapter 2: Basics of Global Climate")

    tab1, tab2, tab3 = st.tabs(["Radiative Forcing & Energy", "Circulation Systems", "Carbon Cycle & Land"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Radiative Forcing & Energy Budget</h3>
        <p><b>Blackbody Radiation:</b> The Earth receives Solar (shortwave) energy and emits Blackbody (longwave infrared) energy.</p>
        <p><b>Gradients:</b> The equator receives more solar radiation than the poles. This gradient of radiative forcing requires the atmosphere and ocean to transport heat poleward to maintain a global energy balance.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Atmospheric & Ocean Circulation</h3>
        <p><b>Atmosphere:</b> Features distinct vertical structures (Troposphere, Stratosphere) and latitudinal cells (Hadley, Ferrel, Polar cells) that dictate global wind patterns.</p>
        <p><b>Ocean:</b> Divided into surface wind-driven circulation (gyres) and deep <b>Thermohaline Circulation</b> driven by density differences (temperature and salinity). The ocean's vertical structure includes a mixed layer, thermocline, and deep ocean.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab3:
        st.markdown("""
        <div class="lesson-card">
        <h3>Land Processes & Carbon Cycle</h3>
        <p>Land surfaces impact climate via Albedo (reflectivity) and moisture fluxes. The Carbon Cycle moves carbon between the atmosphere, terrestrial biosphere, oceans, and lithosphere. Human activity disrupts this by rapidly moving lithospheric carbon (fossil fuels) into the atmosphere.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Knowledge Check")
    q2 = st.radio("What drives the ocean's deep Thermohaline Circulation?", ["Surface Winds", "Temperature and Salinity differences", "The Coriolis Force alone"])
    if st.button("Submit Chapter 2"):
        if q2 == "Temperature and Salinity differences": mark_completed("Ch2")
        else: st.error("Incorrect. 'Thermo' means temperature, 'haline' means salinity.")

# --- CHAPTER 3 ---
elif lesson_choice == "3. Physical Processes":
    st.title("Chapter 3: Physical Processes in the Climate System")

    tab1, tab2, tab3 = st.tabs(["Momentum & State", "Temperature & Continuity", "Moist Processes & Waves"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Conservation of Momentum & Equation of State</h3>
        <p><b>Forces:</b> Air and water move due to the Pressure Gradient Force. On a rotating Earth, the Coriolis Force deflects this movement, leading to Geostrophic Wind balances.</p>
        <p><b>Hydrostatic Balance:</b> Relates pressure to height (gravity pulling down vs. pressure pushing up).</p>
        <p><b>Equation of State:</b> For the atmosphere, it's the Ideal Gas Law. For the ocean, density relies on temperature, salinity, and pressure. This explains thermal expansions causing sea-level rise.</p>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r"P = \rho R T")

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Temperature & Continuity Equations</h3>
        <p><b>Temperature:</b> Changes due to advection (moving air/water), radiation, and latent heat. The dry adiabatic lapse rate dictates how dry air cools as it rises.</p>
        <p><b>Continuity (Mass Conservation):</b> Water and air cannot be destroyed. Diverging surface waters must be replaced by deeper water (Coastal & Equatorial Upwelling).</p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="lesson-card">
        <h3>Moist Processes & Wave Dynamics</h3>
        <p><b>Moisture:</b> When air rises, it hits the Lifting Condensation Level, achieving saturation. Condensation releases latent heat, changing the cooling rate to the 'moist adiabat'.</p>
        <p><b>Waves:</b> Gravity waves, Kelvin waves (equatorial trapped waves), and Rossby waves (planetary waves) transfer energy and momentum across vast distances in both the ocean and atmosphere.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Knowledge Check")
    q3 = st.radio("What happens to an air parcel when it reaches the Lifting Condensation Level?", ["It begins to sink", "It reaches saturation and condensation begins", "It loses all its latent heat instantly"])
    if st.button("Submit Chapter 3"):
        if q3 == "It reaches saturation and condensation begins": mark_completed("Ch3")
        else: st.error("Incorrect. This is the exact altitude where clouds form due to saturation.")

# --- CHAPTER 4 ---
elif lesson_choice == "4. El Niño & Predictions":
    st.title("Chapter 4: El Niño and Year-to-Year Prediction")

    tab1, tab2, tab3 = st.tabs(["ENSO Mechanisms", "Wave Dynamics", "Teleconnections & Forecasting"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>The Bjerknes Hypothesis & Extremes</h3>
        <p><b>Climatology:</b> Normal Pacific has a 'Warm Pool' in the West and cold upwelling in the East. </p>
        <p><b>The Loop:</b> Bjerknes proposed that weakened trade winds allow the warm pool to slosh East, which flattens the thermocline, reduces the East-West temperature gradient, and weakens the winds further (Positive Feedback).</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Transition Dynamics (The 1997-98 Event)</h3>
        <p><b>Subsurface Anomalies:</b> El Niño isn't just surface phenomena. Equatorial jets and <b>Kelvin waves</b> transport massive amounts of warm water across the Pacific.</p>
        <p><b>Delayed/Recharge Oscillator:</b> These models explain why El Niño ends. Rossby waves reflect off landmasses and return as Kelvin waves to reset the thermocline, shifting the system toward La Niña.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab3:
        st.markdown("""
        <div class="lesson-card">
        <h3>Prediction & Teleconnections</h3>
        <p><b>Teleconnections:</b> How a warm Pacific alters global weather (e.g., Sahel droughts, altering Hurricane seasons, shifting the North Atlantic Oscillation).</p>
        <p><b>Limits to Skill:</b> Forecasts are limited by the chaotic nature of the atmosphere and spring predictability barriers, but seasonal predictions are highly valuable.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Knowledge Check")
    q4 = st.radio("Which wave is primarily responsible for shifting the thermocline to eventually 'shut off' an El Niño?", ["Gravity Waves", "Rossby to Kelvin wave reflections (Delayed Oscillator)", "Sound Waves"])
    if st.button("Submit Chapter 4"):
        if q4 == "Rossby to Kelvin wave reflections (Delayed Oscillator)": mark_completed("Ch4")
        else: st.error("Incorrect. Review the Delayed Oscillator model.")

# --- CHAPTER 5 ---
elif lesson_choice == "5. Climate Models":
    st.title("Chapter 5: Climate Models")

    tab1, tab2 = st.tabs(["Constructing the Model", "Grids & Parameterization"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Constructing a Climate Model</h3>
        <p><b>Components:</b> A full GCM (General Circulation Model) couples an Atmospheric model, an Ocean model, Land surface (vegetation), and Cryosphere (snow/ice).</p>
        <p><b>The Hierarchy:</b> Models range from simple 1D Energy Balance Models to complex 3D fully coupled spectral models.</p>
        <p><b>Climate Drift:</b> Early coupled models would 'drift' from reality due to minor imbalances, requiring flux adjustments. Modern models evaluate present-day climatology against observations to prevent this.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Resolution & Parameterization</h3>
        <p><b>Grids:</b> Models use numerical representations (Finite-difference grids or spectral equations) processed on parallel computer architectures.</p>
        <p><b>Parameterization:</b> Many physical processes (like individual clouds, mixing, dry/moist convection) are smaller than the model's grid boxes (sub-grid scale). These must be 'parameterized'—approximated based on larger-scale variables.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Knowledge Check")
    q5 = st.radio("What must be done to processes like cloud formation that are too small for a model's grid?", ["They are ignored", "They are Parameterized", "They are calculated perfectly using quantum computing"])
    if st.button("Submit Chapter 5"):
        if q5 == "They are Parameterized": mark_completed("Ch5")
        else: st.error("Incorrect. They must be parameterized (approximated).")

# --- CHAPTER 6 ---
elif lesson_choice == "6. Greenhouse Effect & Feedbacks":
    st.title("Chapter 6: The Greenhouse Effect and Feedbacks")

    tab1, tab2 = st.tabs(["Greenhouse Mechanics", "Climate Feedbacks"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Energy Balance & The Greenhouse Effect</h3>
        <p><b>One-Layer Model:</b> The atmosphere is transparent to solar radiation but absorbs infrared emissions from the surface, re-radiating heat back down. This basic greenhouse effect raises global average temperatures significantly above what they would be otherwise.</p>
        <p><b>Transient vs Equilibrium:</b> Equilibrium response is the final temperature after CO2 doubling. Transient response is the immediate, time-dependent change, which is slower due to the ocean's massive heat capacity.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Climate Feedbacks & Sensitivity</h3>
        <p><b>Climate Sensitivity:</b> The total temperature change resulting from a forcing, amplified or dampened by feedbacks.</p>
        <ul>
            <li><b>Water Vapor (+):</b> Warmer air holds more moisture (a GHG), amplifying warming.</li>
            <li><b>Snow/Ice Albedo (+):</b> Melting ice reveals dark water/land, absorbing more heat.</li>
            <li><b>Lapse Rate (-):</b> A warmer upper atmosphere radiates heat to space faster, dampening surface warming.</li>
            <li><b>Clouds (?):</b> The largest source of uncertainty. Low clouds cool, high clouds warm.</li>
            <li><b>Stratospheric Cooling:</b> As GHGs trap heat low, the stratosphere actually cools down.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Knowledge Check")
    q6 = st.radio("Why does the Stratosphere cool during global warming?", ["Because the ozone layer is thickening", "Because GHGs trap heat in the troposphere below it", "Because clouds reflect heat away from it"])
    if st.button("Submit Chapter 6"):
        if q6 == "Because GHGs trap heat in the troposphere below it": mark_completed("Ch6")
        else: st.error("Incorrect. The troposphere hogs the heat!")

# --- CHAPTER 7 ---
elif lesson_choice == "7. Global Warming Scenarios":
    st.title("Chapter 7: Scenarios for Global Warming")

    tab1, tab2, tab3 = st.tabs(["Forcings & Scenarios", "Spatial Patterns & Impacts", "Observations & The Future"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Greenhouse Gases, Aerosols & Scenarios</h3>
        <p><b>Forcings:</b> GHGs provide positive forcing. Sulfate aerosols (from industry and volcanoes) provide negative forcing (cooling) and act as cloud condensation nuclei.</p>
        <p><b>Scenarios:</b> We use standardized emissions pathways to project multi-model ensemble averages of future climates.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Spatial Patterns, Ice & Sea Level</h3>
        <p><b>Poleward Amplification:</b> Warming is not uniform. The poles (especially the Arctic) warm much faster due to ice-albedo feedbacks.</p>
        <p><b>Sea Level Rise:</b> Driven by oceanic thermal expansion and the melting of land ice (glaciers, ice sheets), drastically increasing extreme coastal events.</p>
        <p><b>Oceans:</b> The ocean acts as a buffer, slowing down the warming process (Transient vs Equilibrium response).</p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="lesson-card">
        <h3>Observed Change & The Road Ahead</h3>
        <p><b>Observations to Date:</b> Current temperature trends are highly inconsistent with natural variability; anthropogenic forcing is the clear driver based on scale dependence and statistical models.</p>
        <p><b>The Road Ahead:</b> Future impacts depend entirely on which emissions paths society chooses to take. The 'best-estimate prognosis' models multiple futures to help policymakers navigate risk.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Knowledge Check")
    q7 = st.radio("Why do the poles warm faster than the equator in global warming scenarios?", ["The ozone hole funnels heat there", "Poleward Amplification driven heavily by the Ice-Albedo feedback", "The oceans are shallower at the poles"])
    if st.button("Submit Chapter 7"):
        if q7 == "Poleward Amplification driven heavily by the Ice-Albedo feedback": mark_completed("Ch7")
        else: st.error("Incorrect. Reflective ice melting exposes dark, heat-absorbing water.")
