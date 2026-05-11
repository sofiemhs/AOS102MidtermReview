import streamlit as st

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Climate Science Terminal", page_icon="💻", layout="wide")

# --- CUSTOM CLIMATE THEME CSS (Strictly #006884 Background & Black Text) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Open+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Open Sans', sans-serif;
        color: #000000 !important; 
    }
    
    h1, h2, h3, h4, h5 {
        font-family: 'Courier Prime', monospace;
        color: #000000 !important; 
        font-weight: bold;
    }

    /* Main background - Requested Dark Teal */
    .stApp {
        background-color: #006884; 
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3em;
        background-color: #ffffff; 
        color: #000000 !important; 
        font-weight: bold;
        border: 2px solid #000000;
        transition: 0.3s;
        box-shadow: 4px 4px 0px #000000;
    }
    
    .stButton>button:hover {
        background-color: #e2e8f0; 
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #000000;
    }

    /* Content Cards / Terminal Windows */
    .lesson-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 8px;
        border: 3px solid #000000;
        box-shadow: 6px 6px 0px rgba(0,0,0,0.8);
        margin-bottom: 20px;
        color: #000000 !important; 
    }
    
    .lesson-card h3 {
        margin-top: 0;
        border-bottom: 2px dashed #000000;
        padding-bottom: 10px;
    }

    .lesson-card li, .lesson-card p {
        color: #000000 !important;
        font-size: 16px;
    }

    /* Form and Radio text */
    div[role="radiogroup"] label, .stRadio p, .stMarkdown p {
        color: #000000 !important;
    }

    /* Info panels */
    .stAlert {
        background-color: #bae6fd; 
        color: #000000 !important; 
        border: 2px solid #000000;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (Progress Tracking & Story Unlocking) ---
if 'max_unlocked' not in st.session_state:
    st.session_state.max_unlocked = 0

# --- CHAPTER LIST ---
ALL_CHAPTERS = [
    "0. Terminal Boot (Welcome)", 
    "1. The Signal and the Noise", 
    "2. The Energy Engine", 
    "3. Fluid Dynamics & Expansion", 
    "4. The Pacific Heartbeat", 
    "5. Building the Matrix (Models)", 
    "6. The Amplifiers (Feedbacks)",
    "7. Choosing the Future"
]

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 💻 SYSTEM NAVIGATOR")
    
    prog_percent = int((st.session_state.max_unlocked / 7) * 100)
    st.progress(prog_percent / 100)
    st.write(f"**Clearance Level:** {prog_percent}%")
    st.write("*(Achieve 5/5 on current mission to unlock next clearance)*")
    st.write("---")
    
    available_chapters = ALL_CHAPTERS[:st.session_state.max_unlocked + 1]
    lesson_choice = st.radio("Access File:", available_chapters)
    
    st.write("---")
    if st.button("System Reset (Restart Course)"):
        st.session_state.max_unlocked = 0
        st.rerun()

# --- HELPER FUNCTION FOR QUIZZES ---
def run_quiz(chapter_index, questions_and_answers):
    with st.form(f"quiz_{chapter_index}"):
        st.markdown("### ⚠️ MISSION CLEARANCE CHECK")
        st.write("You must score 5/5 to bypass security and unlock the next file. Otherwise, review the logs.")
        
        user_answers = []
        for i, qa in enumerate(questions_and_answers):
            st.write(f"**{i+1}. {qa['q']}**")
            ans = st.radio(f"q{i}", qa['opts'], key=f"q_{chapter_index}_{i}", label_visibility="collapsed")
            user_answers.append(ans)
            st.write("---")
            
        if st.form_submit_button("Submit Analysis"):
            score = sum(1 for i, ans in enumerate(user_answers) if ans == questions_and_answers[i]['ans'])
            if score == 5:
                if st.session_state.max_unlocked == chapter_index:
                    st.session_state.max_unlocked += 1
                    st.success("ACCESS GRANTED. New files unlocked in sidebar.")
                    st.balloons()
                    st.rerun()
                else:
                    st.success("Perfect score retained. Clearance already granted.")
            else:
                st.error(f"ACCESS DENIED. Score: {score}/5. You missed some critical data. Reread the log and try again.")

# ==========================================
# PAGE CONTENT (STORY & CODE)
# ==========================================

if lesson_choice == "0. Terminal Boot (Welcome)":
    st.title("💻 Welcome to the AOS102 Terminal")
    st.markdown("""
    <div class="lesson-card">
    <h3>LOG ENTRY: DAY 1</h3>
    <p>You are a junior data analyst at the Global Systems Monitoring division. Your job is to translate raw physical processes into code, analyze climate variability, and project global warming scenarios.</p>
    <p>This terminal contains 7 encrypted case files spanning physical oceanography to atmospheric feedback loops. To decrypt the next file, you must read the mission briefing, study the Python modeling codes, and pass a rigorous 5-question clearance check.</p>
    <p>Failure means you stay stuck on your current assignment. Proceed to Chapter 1 when ready.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Acknowledge & Begin"):
        if st.session_state.max_unlocked == 0:
            st.session_state.max_unlocked = 1
            st.rerun()

elif lesson_choice == "1. The Signal and the Noise":
    st.title("File 1: The Signal and the Noise")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>Mission Briefing</h3>
    <p>Your mentor drops a dataset on your desk showing wild year-to-year temperature swings. "Separate the noise from the signal," she says.</p>
    <p>Climate variability comes in three forms: <b>Internal Variability</b> (natural wobbles like El Niño that we don't cause), <b>Natural External Forcing</b> (volcanoes or orbital shifts), and <b>Anthropogenic Forcing</b> (us burning trace gases). To see human-caused warming, we use <b>Paleoclimate Proxies</b> (ice cores) to prove current trends exceed natural historical bounds.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>Modeling Bay: Moving Averages</h3>
    <p>To see the Anthropogenic trend, we must smooth out the internal variability (the noise). Below is the Python logic based on your <b>PbSet 1B</b> assignment.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.code('''
# AOS102: Smoothing Global Temperature Anomalies (PbSet 1B)
import pandas as pd
import numpy as np

# Apply a 40-year moving average to smooth high-frequency internal variability
movingav_length = 40
df['smoothed_trend'] = df['temp_anomaly'].rolling(window=movingav_length, center=True).mean()

# Identify extreme outliers (greater than 2 standard deviations)
std_dev = df['temp_anomaly'].std()
extreme_years = df[abs(df['temp_anomaly']) > 2 * std_dev]
    ''', language='python')

    run_quiz(1, [
        {"q": "What type of variability is El Niño considered?", "opts": ["Natural External", "Anthropogenic", "Internal Variability"], "ans": "Internal Variability"},
        {"q": "If a volcano erupts and cools the Earth, what kind of forcing is this?", "opts": ["Internal", "Natural External", "Anthropogenic"], "ans": "Natural External"},
        {"q": "Why do we use paleoclimate proxies like ice cores?", "opts": ["To measure modern CO2", "To establish a baseline of natural climate history before human instruments existed", "To predict weather next week"], "ans": "To establish a baseline of natural climate history before human instruments existed"},
        {"q": "In the Python model, why do we use a 40-year moving average on temperature data?", "opts": ["To create noise", "To smooth out high-frequency internal variability and reveal long-term trends", "To calculate the Coriolis effect"], "ans": "To smooth out high-frequency internal variability and reveal long-term trends"},
        {"q": "What defines 'climate' as opposed to 'weather'?", "opts": ["Weather is a boundary value problem, climate is chaotic.", "Climate is the statistical average of weather over long periods, acting as a boundary value problem.", "There is no difference."], "ans": "Climate is the statistical average of weather over long periods, acting as a boundary value problem."}
    ])

elif lesson_choice == "2. The Energy Engine":
    st.title("File 2: The Energy Engine")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>Mission Briefing</h3>
    <p>You pull up satellite thermal imaging. The Earth is absorbing high-frequency Solar shortwave radiation and glowing with invisible, low-frequency <b>Blackbody</b> longwave radiation. Because of the Earth's curve, the equator is cooking while the poles freeze (the Radiative Gradient).</p>
    <p>To prevent boiling, the planet uses engines. The Atmosphere uses <b>Hadley Cells</b>. The Ocean uses <b>Thermohaline Circulation</b>—driven entirely by dense water (cold and salty) sinking near Greenland, acting like a giant plunger pulling warm equatorial water north.</p>
    </div>
    """, unsafe_allow_html=True)

    run_quiz(2, [
        {"q": "What type of radiation does the Earth emit back into space?", "opts": ["Shortwave solar", "Longwave Blackbody (Infrared)", "Microwave"], "ans": "Longwave Blackbody (Infrared)"},
        {"q": "What drives the ocean's deep Thermohaline Circulation?", "opts": ["Wind", "Lunar tides", "Water density differences driven by temperature and salinity"], "ans": "Water density differences driven by temperature and salinity"},
        {"q": "Why is there a massive heat transport from the equator to the poles?", "opts": ["To maintain global energy balance due to the radiative gradient", "Because wind only blows North", "Because the poles are closer to the sun"], "ans": "To maintain global energy balance due to the radiative gradient"},
        {"q": "What is a Hadley Cell?", "opts": ["A battery for satellites", "An atmospheric circulation loop where hot air rises at the equator and sinks in the subtropics", "A deep ocean trench"], "ans": "An atmospheric circulation loop where hot air rises at the equator and sinks in the subtropics"},
        {"q": "Why is digging up fossil reserves fundamentally disrupting the Carbon Cycle?", "opts": ["It removes oxygen from the air", "It reintroduces massive amounts of carbon that was safely locked away in the lithosphere for millions of years", "It causes volcanoes to erupt"], "ans": "It reintroduces massive amounts of carbon that was safely locked away in the lithosphere for millions of years"}
    ])

elif lesson_choice == "3. Fluid Dynamics & Expansion":
    st.title("File 3: Fluid Dynamics & Expansion")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>Mission Briefing</h3>
    <p>The director needs a sea-level rise projection by noon. You must use the <b>Equation of State</b>. As water warms, it becomes less dense and physically expands (Thermal Expansion).</p>
    <p>You also need to map wind currents. The <b>Pressure Gradient Force</b> pulls air inward toward Low pressure, but the Earth is spinning. The <b>Coriolis Force</b> yanks that air to the right (in the North). When these two tie, we get <b>Geostrophic Balance</b>: wind blowing in a circle <i>around</i> the storm.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>Modeling Bay: Thermal Expansion</h3>
    <p>Based on your math in <b>PbSet 2</b>, here is how we script upper-ocean thermal expansion.</p>
    </div>
    """, unsafe_allow_html=True)

    st.code('''
# AOS102: Sea Level Rise via Thermal Expansion (PbSet 2)
# Equation: dh / h0 = epsilon_T * dT

h0_upper_ocean = 300      # Depth of upper ocean in meters
epsilon_T_upper = 2.7e-4  # Thermal expansion coefficient (C^-1)
dT_warming = 4.0          # Projected warming in Celsius

# Calculate sea level rise contribution (dh)
dh_upper = h0_upper_ocean * epsilon_T_upper * dT_warming

print(f"Sea level rise from 4C warming: {dh_upper} meters")
    ''', language='python')

    run_quiz(3, [
        {"q": "What two forces are balancing to create Geostrophic Wind?", "opts": ["Gravity and Buoyancy", "Pressure Gradient Force and Coriolis Force", "Friction and Latent Heat"], "ans": "Pressure Gradient Force and Coriolis Force"},
        {"q": "In the Northern Hemisphere, which way does the Coriolis force pull moving air?", "opts": ["To the Left", "To the Right", "Straight Up"], "ans": "To the Right"},
        {"q": "According to the Equation of State script, what causes thermal expansion?", "opts": ["Warming ocean temperatures causing water to become less dense and expand", "Icebergs sliding into the sea", "More rain falling into the ocean"], "ans": "Warming ocean temperatures causing water to become less dense and expand"},
        {"q": "What happens when surface water diverges away from the coast?", "opts": ["A hole forms in the ocean", "Continuity forces deep, cold water to rise to the surface (Upwelling)", "The water boils"], "ans": "Continuity forces deep, cold water to rise to the surface (Upwelling)"},
        {"q": "What is Latent Heat?", "opts": ["Heat from a volcano", "Heat stored in water vapor during evaporation, released like a bomb when it condenses into clouds", "Friction from the wind"], "ans": "Heat stored in water vapor during evaporation, released like a bomb when it condenses into clouds"}
    ])

elif lesson_choice == "4. The Pacific Heartbeat":
    st.title("File 4: The Pacific Heartbeat (ENSO)")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>Mission Briefing</h3>
    <p>Alarms sound. The Pacific Trade Winds just died. Normally, these winds blow West, pushing a 'Warm Pool' to Indonesia and sucking up cold water in South America. But now, the winds have failed.</p>
    <p>The warm pool sloshes East. This flattens the thermocline, dropping the East-West temperature gradient, which makes the winds fail <i>even more</i>. This runaway train is the <b>Bjerknes Feedback Loop</b> (El Niño). It only ends months later when underwater <b>Rossby waves</b> bounce off Asia, return as Kelvin waves, and reset the ocean (The Delayed Oscillator).</p>
    </div>
    """, unsafe_allow_html=True)

    run_quiz(4, [
        {"q": "What is the normal state of the Equatorial Pacific?", "opts": ["Trade winds blow West; warm pool in Indonesia, cold upwelling in South America", "Trade winds blow East; warm pool in South America", "No wind, uniform temperatures"], "ans": "Trade winds blow West; warm pool in Indonesia, cold upwelling in South America"},
        {"q": "What is the Bjerknes Feedback Loop?", "opts": ["A negative feedback that stops storms", "A positive feedback where weakening winds warm the East, which weakens the winds even further", "A cooling mechanism"], "ans": "A positive feedback where weakening winds warm the East, which weakens the winds even further"},
        {"q": "According to the Delayed Oscillator model, what shuts off an El Niño?", "opts": ["Rossby waves reflecting off Asia and returning as Kelvin waves to reset the thermocline", "Winter snow", "The moon's gravity"], "ans": "Rossby waves reflecting off Asia and returning as Kelvin waves to reset the thermocline"},
        {"q": "What happens to the thermocline during an El Niño?", "opts": ["It tilts steeply", "It completely vanishes", "It flattens out as warm water sloshes East"], "ans": "It flattens out as warm water sloshes East"},
        {"q": "How does an El Niño in the Pacific affect a drought in the Sahel? (What is this called?)", "opts": ["A parameterization", "A Teleconnection", "An error in the data"], "ans": "A Teleconnection"}
    ])

elif lesson_choice == "5. Building the Matrix (Models)":
    st.title("File 5: Building the Matrix")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>Mission Briefing</h3>
    <p>To predict the future, you must build a virtual Earth. <b>General Circulation Models (GCMs)</b> chop the atmosphere into 3D grid boxes. But there is a massive flaw: if your grid box is 50 miles wide, the computer is entirely blind to a 2-mile-wide thunderstorm.</p>
    <p>To fix this, scientists use <b>Parameterization</b>. They write rules saying, "If this large 50-mile box is humid, mathematically assume a thunderstorm is happening inside it."</p>
    </div>
    """, unsafe_allow_html=True)

    run_quiz(5, [
        {"q": "What is a General Circulation Model (GCM)?", "opts": ["A 1D energy equation", "A complex 3D grid simulation calculating fluid dynamics for the atmosphere and ocean", "A statistical guess based solely on past data"], "ans": "A complex 3D grid simulation calculating fluid dynamics for the atmosphere and ocean"},
        {"q": "Why can't we just make grid boxes 1-inch wide?", "opts": ["The computer screen isn't big enough", "The computational cost would be astronomically impossible to process", "It violates the laws of physics"], "ans": "The computational cost would be astronomically impossible to process"},
        {"q": "What must we do for physical processes that are 'sub-grid scale' (like individual clouds)?", "opts": ["Ignore them", "Parameterize them (approximate them based on large-scale variables)", "Manually calculate them on paper"], "ans": "Parameterize them (approximate them based on large-scale variables)"},
        {"q": "What is 'Climate Drift' in early coupled models?", "opts": ["Models drifting off target over time due to minor imbalances requiring flux adjustments", "The physical drifting of continents", "Icebergs floating away"], "ans": "Models drifting off target over time due to minor imbalances requiring flux adjustments"},
        {"q": "Which of the following is the BEST example of a process requiring parameterization?", "opts": ["The rotation of the Earth", "The total solar energy hitting the planet", "Moist convection and cloud formation"], "ans": "Moist convection and cloud formation"}
    ])

elif lesson_choice == "6. The Amplifiers (Feedbacks)":
    st.title("File 6: The Amplifiers")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>Mission Briefing</h3>
    <p>CO2 traps heat via <b>Selective Absorption</b> (letting sunlight in, but blocking infrared heat out). A doubling of CO2 causes about 1°C of raw warming. But the final number is much higher because of <b>Feedbacks</b>.</p>
    <p>The big one: <b>Water Vapor Feedback</b> (+). Warmer air holds more water vapor. Water vapor is a potent GHG. So warming causes more evaporation, which traps more heat, causing more evaporation. The only major brake system is the <b>Lapse Rate Feedback</b> (-): the upper atmosphere warms faster and radiates that extra heat off to deep space.</p>
    </div>
    """, unsafe_allow_html=True)

    run_quiz(6, [
        {"q": "What is Selective Absorption?", "opts": ["Oceans absorbing salt", "GHGs letting shortwave solar in, but blocking longwave infrared from leaving", "Plants breathing CO2"], "ans": "GHGs letting shortwave solar in, but blocking longwave infrared from leaving"},
        {"q": "Why is the Water Vapor feedback loop positive (amplifying)?", "opts": ["Warmer air holds more water vapor, which acts as a GHG, trapping even more heat", "Water cools the Earth", "Vapor turns into ice"], "ans": "Warmer air holds more water vapor, which acts as a GHG, trapping even more heat"},
        {"q": "What is the Ice-Albedo feedback?", "opts": ["Ice reflects heat, so when it melts, dark oceans absorb more heat, melting more ice (+)", "Ice acts as a blanket, keeping the ocean warm (-)", "Ice absorbs CO2"], "ans": "Ice reflects heat, so when it melts, dark oceans absorb more heat, melting more ice (+)"},
        {"q": "How does the Lapse Rate feedback act as a negative (stabilizing) feedback?", "opts": ["It causes more snow", "The upper atmosphere warms faster and efficiently radiates that excess heat out to space", "It slows down the ocean"], "ans": "The upper atmosphere warms faster and efficiently radiates that excess heat out to space"},
        {"q": "As the troposphere (lower atmosphere) warms due to GHGs trapping heat, what happens to the stratosphere above it?", "opts": ["It warms equally", "It catches on fire", "It actually cools down because the heat is trapped below it"], "ans": "It actually cools down because the heat is trapped below it"}
    ])

elif lesson_choice == "7. Choosing the Future":
    st.title("File 7: Choosing the Future")
    
    st.markdown("""
    <div class="lesson-card">
    <h3>Mission Briefing</h3>
    <p>It is the year 2024. Policymakers demand projections for the year 2050. Because the Ocean has massive Heat Capacity, the warming we feel today is only the <b>Transient Response</b>. The <b>Equilibrium Response</b> means we are locked into decades of warming even if emissions hit zero today.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>Modeling Bay: Integrating Scenarios</h3>
    <p>From your <b>PbSet 2</b> assignment, you must code the mathematical integration of CO2 emissions. Only about 47% of human emissions stay in the atmosphere; the rest is eaten by land and oceans.</p>
    </div>
    """, unsafe_allow_html=True)

    st.code('''
# AOS102: CO2 Concentration Integration (PbSet 2)
# d[CO2]/dt = 0.47 * emissions(t)
# Conversion: 1 ppm = 7.8 GtCO2

co2_ppm = 424.6  # Starting value in 2024

# Scenario A: Emissions grow at historical rate of +0.52 Gt/year
for year in range(2024, 2051):
    current_emissions_Gt = 39.6 + 0.52 * (year - 2024)
    added_ppm = (0.47 * current_emissions_Gt) / 7.8
    co2_ppm += added_ppm

print(f"Scenario A CO2 in 2050: {co2_ppm:.1f} ppm")
    ''', language='python')

    run_quiz(7, [
        {"q": "What is the difference between Transient and Equilibrium response?", "opts": ["Transient is immediate warming; Equilibrium is the final warming after the deep ocean catches up", "There is no difference", "Transient is cooling, Equilibrium is warming"], "ans": "Transient is immediate warming; Equilibrium is the final warming after the deep ocean catches up"},
        {"q": "If human emissions instantly drop to absolute zero today, what will happen to global temperatures?", "opts": ["They will instantly drop", "They will continue to slowly rise for decades due to the ocean's massive heat capacity (committed warming)", "They will freeze"], "ans": "They will continue to slowly rise for decades due to the ocean's massive heat capacity (committed warming)"},
        {"q": "In the Python code, why do we multiply emissions by 0.47?", "opts": ["Because 47% of emissions are fake", "Because only ~47% of emitted CO2 remains in the atmosphere (the rest goes into oceans and land)", "Because 0.47 is the gas constant"], "ans": "Because only ~47% of emitted CO2 remains in the atmosphere (the rest goes into oceans and land)"},
        {"q": "What is Poleward Amplification?", "opts": ["The poles warm significantly faster than the tropics, largely due to ice-albedo feedbacks", "The equator warms faster than the poles", "Penguins migrating north"], "ans": "The poles warm significantly faster than the tropics, largely due to ice-albedo feedbacks"},
        {"q": "Aside from melting ice, what is the major driver of Sea Level Rise?", "opts": ["Whale migration", "Thermal Expansion (the water literally expanding as it absorbs heat)", "Increased rainfall"], "ans": "Thermal Expansion (the water literally expanding as it absorbs heat)"}
    ])
