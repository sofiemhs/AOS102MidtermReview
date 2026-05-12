import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Climate Science Terminal v3.0", page_icon="💻", layout="wide")

# --- CUSTOM CLIMATE THEME CSS ---
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

    .stApp { background-color: #006884; }
    
    /* --- SIDEBAR OVERRIDES (WHITE TEXT) --- */
    [data-testid="stSidebar"] {
        background-color: #004d61; /* Darker teal to ensure white text is visible */
    }
    
    [data-testid="stSidebar"], [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #ffffff !important; 
    }
    
    /* Modify sidebar buttons specifically to keep white text readable */
    [data-testid="stSidebar"] .stButton>button {
        background-color: #000000;
        color: #ffffff !important;
        border: 2px solid #ffffff;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #333333;
        color: #ffffff !important;
    }
    /* -------------------------------------- */

    .stButton>button, .stFormSubmitButton>button {
        width: 100%; border-radius: 4px; height: 3em; background-color: #ffffff; 
        color: #000000 !important; font-weight: bold; border: 2px solid #000000;
        transition: 0.3s; box-shadow: 4px 4px 0px #000000;
    }
    
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background-color: #e2e8f0; transform: translate(2px, 2px); box-shadow: 2px 2px 0px #000000;
    }

    .lesson-card {
        background-color: #ffffff; padding: 25px; border-radius: 8px; border: 3px solid #000000;
        box-shadow: 6px 6px 0px rgba(0,0,0,0.8); margin-bottom: 20px; color: #000000 !important; 
    }
    
    .lesson-card h3 { margin-top: 0; border-bottom: 2px dashed #000000; padding-bottom: 10px; }
    div[role="radiogroup"] label, .stRadio p, .stMarkdown p { color: #000000 !important; }
    .stAlert { background-color: #bae6fd; color: #000000 !important; border: 2px solid #000000; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CURRICULUM DATA STRUCTURE
# ==========================================

CURRICULUM = {
    "1. Overview of Climate Variability": {
        "pages": [
            "1.1 Concept: Weather, Climate, & Anomalies", 
            "1.2 Concept: Drivers & Greenhouse Gases", 
            "1.3 Concept: Model Hierarchy & Grid Boxes", 
            "1.4 Concept: IPCC & Emissions Pathways",
            "1.5 Concept: Paleoclimate & Ice Cores",
            "1.6 Model: Smoothing Data",
            "1.7 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "How does the professor define 'climate' compared to 'weather'?", "opts": ["Weather is a boundary value problem, climate is chaotic.", "Weather is a particular event, while climate is the probability of an event occurring.", "There is no difference."], "ans": "Weather is a particular event, while climate is the probability of an event occurring."},
            {"q": "What is an 'anomaly' in climate science?", "opts": ["A malfunctioning weather satellite.", "A departure from normal climatological conditions for a specified time period.", "A sudden spike in CO2 emissions."], "ans": "A departure from normal climatological conditions for a specified time period."},
            {"q": "Which of the following is an example of internal climate variability?", "opts": ["Changes in Earth's orbit.", "El Niño and the North Atlantic Oscillation.", "Volcanic eruptions."], "ans": "El Niño and the North Atlantic Oscillation."},
            {"q": "According to the professor, why is Earth's future annual average surface temperature more predictable than internal variability?", "opts": ["Because it is completely chaotic.", "Because it is controlled by the energy balance of the Earth's climate system.", "Because satellites can perfectly map the grid boxes."], "ans": "Because it is controlled by the energy balance of the Earth's climate system."},
            {"q": "What happens to the concentration of a long-lived greenhouse gas if human emissions remain perfectly constant?", "opts": ["The concentration will stabilize immediately.", "The concentration will undergo an ongoing increase.", "The concentration will drop to zero."], "ans": "The concentration will undergo an ongoing increase."},
            {"q": "What is the purpose of the IPCC?", "opts": ["To conduct new independent climate experiments.", "To review and assess scientific and socio-economic information without conducting its own research.", "To enforce the Paris Agreement globally."], "ans": "To review and assess scientific and socio-economic information without conducting its own research."},
            {"q": "How do General Circulation Models (GCMs) solve physical equations?", "opts": ["By relying completely on historical proxy data.", "By dividing the atmosphere and ocean into millions of discrete grid boxes and computing changes over small time steps.", "By treating the Earth as a single 0-dimensional point."], "ans": "By dividing the atmosphere and ocean into millions of discrete grid boxes and computing changes over small time steps."},
            {"q": "In paleoclimate ice core records, what does the isotope Deuterium (D) primarily help estimate?", "opts": ["Past atmospheric methane concentrations.", "Antarctic air temperature, because heavier isotopes evaporate less easily depending on temperature.", "The speed of the oceanic thermohaline circulation."], "ans": "Antarctic air temperature, because heavier isotopes evaporate less easily depending on temperature."},
            {"q": "During the last glacial maximum, how did global sea levels compare to today?", "opts": ["They were 50 meters higher.", "They were roughly 120 meters below present levels.", "They were exactly the same."], "ans": "They were roughly 120 meters below present levels."},
            {"q": "What was the pre-industrial 'interglacial' concentration of CO2 compared to 'glacial' periods?", "opts": ["Interglacial was ~280 ppm, while glacial was ~180 ppm.", "Interglacial was ~180 ppm, while glacial was ~280 ppm.", "They were both roughly 400 ppm."], "ans": "Interglacial was ~280 ppm, while glacial was ~180 ppm."}
        ]
    },
    "2. Basics of Global Climate": {
        "pages": [
            "2.1 Concept: Components & Parameterization", 
            "2.2 Concept: Energy Balance & Radiation", 
            "2.3 Concept: Atmospheric Circulation", 
            "2.4 Concept: Ocean Circulation & Land Surface",
            "2.5 Concept: The Carbon Cycle",
            "2.6 Model: Carbon Accumulation",
            "2.7 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "What are the three major carbon reservoirs mentioned in the notes?", "opts": ["Ocean, Fossil fuel reserves, and Land", "Atmosphere, Biosphere, and Lithosphere", "Stratosphere, Troposphere, and Cryosphere"], "ans": "Ocean, Fossil fuel reserves, and Land"},
            {"q": "What drives the deep ocean (thermohaline) circulation?", "opts": ["Lunar tides and solar flares.", "Water density (temperature and salinity), wind, and upwelling.", "Only the Coriolis force."], "ans": "Water density (temperature and salinity), wind, and upwelling."},
            {"q": "What is the approximate global average planetary albedo?", "opts": ["0.08", "0.90", "0.31"], "ans": "0.31"},
            {"q": "What is the Hadley cell?", "opts": ["A battery used to power satellites.", "A thermally driven, overturning circulation rising in the tropics and sinking in the subtropics.", "A deep ocean trench near Antarctica."], "ans": "A thermally driven, overturning circulation rising in the tropics and sinking in the subtropics."},
            {"q": "Atmospheric concentrations of CO2 rise by about 1 ppm for each:", "opts": ["2.1 PgC that remains in the atmosphere.", "10.5 PgC emitted by fossil fuels.", "1.0 PgC absorbed by the ocean."], "ans": "2.1 PgC that remains in the atmosphere."},
            {"q": "How is ocean surface circulation characterized in the subtropics and middle latitudes?", "opts": ["As anticyclonic gyres with compensating poleward return flows in narrow western boundary currents.", "As a perfectly straight line from East to West.", "As a completely stagnant mixed layer."], "ans": "As anticyclonic gyres with compensating poleward return flows in narrow western boundary currents."},
            {"q": "How does land use change, such as deforestation, affect the atmosphere?", "opts": ["It cools the planet by increasing albedo.", "It tends to increase CO2 by releasing carbon from soil and biomass.", "It has no measurable effect."], "ans": "It tends to increase CO2 by releasing carbon from soil and biomass."},
            {"q": "What is the Greenhouse Effect primarily driven by?", "opts": ["Ozone absorbing UV radiation in the stratosphere.", "Upward IR trapped by the atmosphere and re-emitted downward, where part is absorbed by the surface.", "Friction from the wind creating heat."], "ans": "Upward IR trapped by the atmosphere and re-emitted downward, where part is absorbed by the surface."},
            {"q": "Approximately how much of the incoming solar radiation is absorbed by the Earth's surface?", "opts": ["Nearly 50%", "About 10%", "Exactly 100%"], "ans": "Nearly 50%"},
            {"q": "Why is the parameterization problem important in climate models?", "opts": ["Because computers are too slow to run at all.", "Because small-scale effects like clouds have important impacts on large-scale climate but are smaller than model grid boxes.", "Because the lithosphere changes too quickly."], "ans": "Because small-scale effects like clouds have important impacts on large-scale climate but are smaller than model grid boxes."}
        ]
    },
    "3. Physical Processes": {
        "pages": [
            "3.1 Concept: Momentum & Forces", 
            "3.2 Concept: State & Hydrostatic Balance", 
            "3.3 Concept: Temp, Continuity, & Chaos", 
            "3.4 Concept: Moisture & Moist Processes",
            "3.5 Concept: Wave Processes",
            "3.6 Model: Adiabatic Lapse Rates",
            "3.7 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "What is the value of the horizontal component of the Coriolis force exactly on the equator?", "opts": ["Maximum", "Zero", "Negative"], "ans": "Zero"},
            {"q": "What happens to the Coriolis force as wind is slowed down by surface friction?", "opts": ["It gets stronger, pulling wind backwards.", "It weakens, allowing the pressure gradient force to pull wind across isobars toward low pressure.", "It remains unaffected by friction."], "ans": "It weakens, allowing the pressure gradient force to pull wind across isobars toward low pressure."},
            {"q": "What is the 'Beta effect'?", "opts": ["The rate of cooling in the stratosphere.", "The change of the Coriolis parameter with latitude, which is proportional to the cosine of latitude and maximum at the equator.", "The ratio of salt to water in ocean upwelling."], "ans": "The change of the Coriolis parameter with latitude, which is proportional to the cosine of latitude and maximum at the equator."},
            {"q": "According to hydrostatic balance, the vertical pressure gradient is dominantly balanced by what?", "opts": ["Gravity", "Friction", "The Coriolis force"], "ans": "Gravity"},
            {"q": "What is the dry adiabatic lapse rate for a rising parcel of air?", "opts": ["2°C per kilometer", "10°C per kilometer", "6°C per kilometer"], "ans": "10°C per kilometer"},
            {"q": "Why is the moist adiabatic lapse rate (roughly 6°C/km) less than the dry adiabatic lapse rate?", "opts": ["Because clouds reflect sunlight.", "Because latent heat is released by the condensation of water vapor, which reduces the cooling.", "Because water vapor is heavier than air."], "ans": "Because latent heat is released by the condensation of water vapor, which reduces the cooling."},
            {"q": "What causes equatorial upwelling in the ocean?", "opts": ["Lunar tides pulling the deep ocean upward.", "The divergence of ocean surface currents away from the equator due to easterly winds and the Coriolis force.", "Volcanic heating at the ocean floor."], "ans": "The divergence of ocean surface currents away from the equator due to easterly winds and the Coriolis force."},
            {"q": "Why does precise weather prediction become essentially impossible after 10 to 14 days?", "opts": ["Because complex, nonlinear feedbacks cause any small initial error to grow rapidly, known as chaos.", "Because satellites run out of power every two weeks.", "Because the Coriolis force resets every 14 days."], "ans": "Because complex, nonlinear feedbacks cause any small initial error to grow rapidly, known as chaos."},
            {"q": "How much latent heat is released during the condensation of water vapor?", "opts": ["3.34 x 10^5 J/kg", "2.50 x 10^6 J/kg", "9.8 m/s^2"], "ans": "2.50 x 10^6 J/kg"},
            {"q": "What are Rossby waves?", "opts": ["Ocean waves that break on the beach.", "Giant meanders in the atmospheric jet stream or ocean that create long-distance teleconnections.", "Sound waves created by thunderstorms."], "ans": "Giant meanders in the atmospheric jet stream or ocean that create long-distance teleconnections."}
        ]
    },
    "4. El Niño (ENSO)": {
        "pages": [
            "4.1 Concept: Normal State & Climatology", 
            "4.2 Concept: El Niño & La Niña Extremes", 
            "4.3 Concept: Feedbacks & Oscillators", 
            "4.4 Concept: ENSO Prediction Limits & Ensembles",
            "4.5 Concept: Teleconnections & Remote Impacts",
            "4.6 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "Under normal Pacific conditions, how does the thermocline depth in the west compare to the east?", "opts": ["It is completely flat.", "It is about 100m shallower in the west.", "It is about 100m deeper in the west."], "ans": "It is about 100m deeper in the west."},
            {"q": "What physical mechanism balances the westward wind stress in the Pacific ocean under normal conditions?", "opts": ["The eastward pressure gradient force in the ocean.", "The gravitational pull of the moon.", "The Coriolis force exactly at the equator."], "ans": "The eastward pressure gradient force in the ocean."},
            {"q": "How did Jakob Bjerknes describe the primary feedback of the Walker circulation?", "opts": ["Winds are completely independent of sea surface temperature.", "An increase in easterly winds increases upwelling and the east-west temperature contrast, which in turn causes the winds.", "Rainfall suppresses the trade winds."], "ans": "An increase in easterly winds increases upwelling and the east-west temperature contrast, which in turn causes the winds."},
            {"q": "During an El Niño warm phase, what happens to the upwelling in the eastern Pacific?", "opts": ["Upwelling stops entirely.", "Upwelling continues, but brings up water that is less cold than normal.", "Upwelling reverses and pushes water down."], "ans": "Upwelling continues, but brings up water that is less cold than normal."},
            {"q": "According to the Delayed Oscillator theory, what ultimately ends an El Niño event?", "opts": ["Subsurface anomalies evolving by slow ocean dynamics return to the eastern Pacific to pull the thermocline back up.", "The sun's solar cycle resets.", "A sudden increase in Atlantic hurricanes pulls heat away from the Pacific."], "ans": "Subsurface anomalies evolving by slow ocean dynamics return to the eastern Pacific to pull the thermocline back up."},
            {"q": "What is the primary fundamental limit to accurately predicting ENSO beyond a few months?", "opts": ["Satellites routinely break down.", "Fundamental weather noise and chaos acting as a random forcing on the slow ocean-atmosphere interaction.", "The lack of any computer models."], "ans": "Fundamental weather noise and chaos acting as a random forcing on the slow ocean-atmosphere interaction."},
            {"q": "Why do climate scientists use ensemble forecasting for ENSO?", "opts": ["To create prettier graphics.", "By starting models from different initial conditions, the ensemble spread provides an estimate of forecast uncertainty.", "To prove that weather noise does not exist."], "ans": "By starting models from different initial conditions, the ensemble spread provides an estimate of forecast uncertainty."},
            {"q": "What is the Pacific-North America (PNA) teleconnection?", "opts": ["An anomalous planetary wave train associated with El Niño that impacts the Northern Hemisphere winter.", "A deep ocean current connecting California to Japan.", "A physical pipeline built to transport water."], "ans": "An anomalous planetary wave train associated with El Niño that impacts the Northern Hemisphere winter."},
            {"q": "How does an El Niño impact winter precipitation in California?", "opts": ["It guarantees severe flooding every time.", "It enhances the probability of a rainier-than-average winter, though it is far from certain due to weather noise.", "It guarantees a severe drought."], "ans": "It enhances the probability of a rainier-than-average winter, though it is far from certain due to weather noise."},
            {"q": "What is the typical impact of El Niño on Atlantic hurricanes between July and October?", "opts": ["It drastically increases the number of named storms.", "It has no statistical effect.", "It tends to reduce the number of named storms and hurricanes."], "ans": "It tends to reduce the number of named storms and hurricanes."}
        ]
    },
    "5. Greenhouse Effect & Feedbacks": {
        "pages": [
            "5.1 Concept: Global Energy Balance & 1-Layer Model", 
            "5.2 Concept: Greenhouse Radiative Forcing", 
            "5.3 Concept: The Climate Feedback Parameter", 
            "5.4 Concept: Water Vapor & Ice Feedbacks",
            "5.5 Concept: Cloud & Lapse Rate Feedbacks",
            "5.6 Concept: Transient vs. Equilibrium Response",
            "5.7 Model: 1-Layer Energy Balance",
            "5.8 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "In the global average energy balance, what is the approximate incoming solar radiation at the top of the atmosphere?", "opts": ["1367 W/m2", "342 W/m2", "168 W/m2"], "ans": "342 W/m2"},
            {"q": "What defines 'Radiative Forcing' ($G$) in the professor's climate model?", "opts": ["The physical force of the wind on the ocean.", "The energy imbalance at the top of the atmosphere before temperature changes to restore balance.", "The amount of solar radiation reflected by clouds."], "ans": "The energy imbalance at the top of the atmosphere before temperature changes to restore balance."},
            {"q": "In the one-layer atmosphere model, what is the 'normal' climatological absorptivity ($\epsilon_a$) of the atmosphere to surface IR?", "opts": ["0.31", "0.50", "0.90"], "ans": "0.90"},
            {"q": "How do positive climate feedbacks mathematically affect the cumulative climate feedback parameter ($\alpha$)?", "opts": ["They increase $\alpha$.", "They have a negative mathematical contribution, decreasing total $\alpha$.", "They multiply $\alpha$ by zero."], "ans": "They have a negative mathematical contribution, decreasing total $\alpha$."},
            {"q": "Roughly how much does water vapor increase per degree Kelvin of warming in the lower troposphere?", "opts": ["1%", "7%", "20%"], "ans": "7%"},
            {"q": "What are the opposing radiative effects of high clouds versus low clouds?", "opts": ["High clouds cool by reflecting IR, low clouds warm by absorbing solar.", "High clouds warm by trapping IR (emitting from colder levels), low clouds cool by reflecting solar.", "Both exclusively cool the planet."], "ans": "High clouds warm by trapping IR (emitting from colder levels), low clouds cool by reflecting solar."},
            {"q": "Why is the Lapse Rate feedback considered negative in the tropics?", "opts": ["Because it causes more snow to fall.", "Because the upper troposphere warms faster than the surface, emitting more IR to space.", "Because it creates low stratus clouds."], "ans": "Because the upper troposphere warms faster than the surface, emitting more IR to space."},
            {"q": "What causes the 'transient' climate response to lag behind the 'equilibrium' climate response?", "opts": ["The time it takes to run the computer models.", "The massive heat capacity of the oceans and ice sheets.", "The slow melting of sea ice."], "ans": "The massive heat capacity of the oceans and ice sheets."},
            {"q": "According to the notes, what tends to cancel out the inter-model variations of the lapse rate feedback?", "opts": ["The snow/ice feedback.", "The cloud top feedback.", "The water vapor feedback."], "ans": "The water vapor feedback."},
            {"q": "If greenhouse gas concentrations are suddenly capped, what happens to the global temperature?", "opts": ["It immediately drops to pre-industrial levels.", "It instantly stabilizes.", "It continues to rise for decades due to the ocean's lag."], "ans": "It continues to rise for decades due to the ocean's lag."}
        ]
    },
    "6. Global Warming Scenarios": {
        "pages": [
            "6.1 Concept: Radiative Forcing & Aerosols", 
            "6.2 Concept: The Commitment Concept", 
            "6.3 Concept: Spatial Patterns", 
            "6.4 Concept: Sea Level Rise",
            "6.5 Model: Sea Level Dynamics",
            "6.6 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "What is Radiative Forcing (Q)?", "opts": ["The net change in Earth's energy balance.", "The force of gravity on the atmosphere.", "The speed of solar wind."], "ans": "The net change in Earth's energy balance."},
            {"q": "What effect do Sulfate Aerosols generally have on climate?", "opts": ["They warm the planet.", "They reflect sunlight, cooling the planet.", "They destroy the ozone layer."], "ans": "They reflect sunlight, cooling the planet."},
            {"q": "Unlike CO2, how long do aerosols stay in the atmosphere?", "opts": ["Centuries", "Decades", "Days/Weeks"], "ans": "Days/Weeks"},
            {"q": "What is the 'Constant Composition Commitment'?", "opts": ["If we stop emissions, temperatures instantly drop.", "Even if emissions stop, warming continues for decades as the ocean reaches equilibrium.", "We are committed to burning coal."], "ans": "Even if emissions stop, warming continues for decades as the ocean reaches equilibrium."},
            {"q": "Why does the Arctic warm faster than the tropics?", "opts": ["Because it is closer to the sun.", "Because of Polar Amplification and the Ice-Albedo feedback.", "Because there is less wind."], "ans": "Because of Polar Amplification and the Ice-Albedo feedback."},
            {"q": "Why does land warm faster than the ocean?", "opts": ["The ocean has a much higher heat capacity.", "Land is darker.", "The ocean reflects more light."], "ans": "The ocean has a much higher heat capacity."},
            {"q": "What are the two main causes of Sea Level Rise?", "opts": ["Thermal Expansion and Land Ice Melt.", "Sea Ice Melt and River Runoff.", "Evaporation and Precipitation."], "ans": "Thermal Expansion and Land Ice Melt."},
            {"q": "Does melting Sea Ice significantly raise sea levels?", "opts": ["Yes, massively.", "No, it is like a melting ice cube in a glass of water.", "Only in the summer."], "ans": "No, it is like a melting ice cube in a glass of water."},
            {"q": "What is Thermal Expansion?", "opts": ["Ice expanding as it freezes.", "Water physically expanding as its temperature increases.", "The atmosphere pushing down on the ocean."], "ans": "Water physically expanding as its temperature increases."},
            {"q": "Which of these adds NEW water to the ocean basin?", "opts": ["Melting sea ice.", "Thermal expansion.", "Melting land ice sheets (Greenland/Antarctica)."], "ans": "Melting land ice sheets (Greenland/Antarctica)."}
        ]
    },
    "Final Exam: Terminal Clearance": {
        "pages": ["Final Knowledge Check"],
        "quiz_pool": []
    }
}

# Auto-populate Final Exam with all available questions
all_questions = []
for chap, data in CURRICULUM.items():
    if chap != "Final Exam: Terminal Clearance":
        all_questions.extend(data["quiz_pool"])
CURRICULUM["Final Exam: Terminal Clearance"]["quiz_pool"] = all_questions

CHAPTER_LIST = list(CURRICULUM.keys())

# ==========================================
# SESSION STATE MANAGEMENT
# ==========================================
if 'unlocked_chapters' not in st.session_state:
    st.session_state.unlocked_chapters = [CHAPTER_LIST[0]]

if 'current_chapter' not in st.session_state:
    st.session_state.current_chapter = CHAPTER_LIST[0]

if 'current_page' not in st.session_state:
    st.session_state.current_page = CURRICULUM[CHAPTER_LIST[0]]["pages"][0]

def change_page(chapter, page):
    st.session_state.current_chapter = chapter
    st.session_state.current_page = page

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("### 💻 SYSTEM NAVIGATOR")
    
    prog_percent = int((len(st.session_state.unlocked_chapters) / len(CHAPTER_LIST)) * 100)
    st.progress(prog_percent / 100)
    st.write(f"**Clearance Level:** {prog_percent}%")
    st.write("---")
    
    for chapter in CHAPTER_LIST:
        is_unlocked = chapter in st.session_state.unlocked_chapters
        
        if is_unlocked:
            with st.expander(f"📂 {chapter}", expanded=(chapter == st.session_state.current_chapter)):
                for page in CURRICULUM[chapter]["pages"]:
                    if st.button(page, key=f"nav_{chapter}_{page}", use_container_width=True, 
                                 type="primary" if st.session_state.current_page == page else "secondary"):
                        change_page(chapter, page)
                        st.rerun()
        else:
            st.markdown(f"🔒 *{chapter} (Locked)*")
            
    st.write("---")
    if st.button("System Reset (Restart Course)"):
        st.session_state.clear()
        st.rerun()

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def render_next_button(current_chapter, current_page):
    pages = CURRICULUM[current_chapter]["pages"]
    current_idx = pages.index(current_page)
    
    if current_idx < len(pages) - 1:
        next_page = pages[current_idx + 1]
        if st.button(f"Proceed to {next_page} ➡️"):
            change_page(current_chapter, next_page)
            st.rerun()

def run_quiz(chapter_name, pool, required_score=5):
    quiz_key = f"quiz_state_{chapter_name}"
    
    if quiz_key not in st.session_state:
        num_questions = min(required_score, len(pool) // 2)
        st.session_state[quiz_key] = random.sample(pool, required_score)
    
    active_questions = st.session_state[quiz_key]
    
    st.markdown(f"### ⚠️ MISSION CLEARANCE: {chapter_name}")
    st.write(f"Pass mark: {required_score}/{required_score}. Questions are randomized from the databanks.")
    
    with st.form(f"form_{chapter_name}"):
        user_answers = []
        for i, qa in enumerate(active_questions):
            st.write(f"**{i+1}. {qa['q']}**")
            ans = st.radio(f"q{i}", qa['opts'], key=f"ans_{chapter_name}_{i}", label_visibility="collapsed")
            user_answers.append(ans)
            st.write("---")
            
        if st.form_submit_button("Submit Analysis"):
            score = sum(1 for i, ans in enumerate(user_answers) if ans == active_questions[i]['ans'])
            
            if score == required_score:
                st.success("ACCESS GRANTED. Security bypassed.")
                st.balloons()
                
                current_chap_idx = CHAPTER_LIST.index(chapter_name)
                if current_chap_idx < len(CHAPTER_LIST) - 1:
                    next_chapter = CHAPTER_LIST[current_chap_idx + 1]
                    if next_chapter not in st.session_state.unlocked_chapters:
                        st.session_state.unlocked_chapters.append(next_chapter)
                    
                    time.sleep(2)
                    change_page(next_chapter, CURRICULUM[next_chapter]["pages"][0])
                    st.rerun()
                else:
                    st.success("🎉 TERMINAL FULLY UNLOCKED. COURSE COMPLETE.")
            else:
                st.error(f"ACCESS DENIED. Score: {score}/{required_score}. Review the logs and try again.")

# ==========================================
# PAGE CONTENT RENDERING
# ==========================================
chapter = st.session_state.current_chapter
page = st.session_state.current_page

st.title(page)

# --- CHAPTER 1 CONTENT ---
if chapter == "1. Overview of Climate Variability":
    if page == "1.1 Concept: Weather, Climate, & Anomalies":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.1: Weather vs. Climate</h3>
        <p>To begin analysis, we must firmly separate weather from climate. According to the foundational texts:</p>
        <ul>
            <li><b>Weather:</b> The state of the atmosphere and ocean at a given moment. It is a <i>particular event</i>.</li>
            <li><b>Climate:</b> The average condition of the atmosphere, ocean, land surfaces, and ecosystems. It represents the <i>probability</i> of an event occurring (e.g., the probability of a >10mm rainfall event in Boulder in September).</li>
        </ul>
        <br><br><br>
        <p><b>Climatology</b> involves taking averages over a sufficiently long interval—such as averaging 15 different Januaries to obtain a baseline January climatology. From this baseline, we calculate <b>Anomalies</b>, which are departures from normal climatological conditions (e.g., subtracting the 1950-1998 average from December 1997 temperatures).</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.2 Concept: Drivers & Greenhouse Gases":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.2: Drivers of Variation</h3>
        <p>Climate varies on many timescales, driven by different physical processes:</p>
        <ul>
            <li><b>Internal Variability:</b> Natural wobbles like El Niño, the North Atlantic Oscillation, and the Pacific Decadal Oscillation.</li>
            <li><b>Natural External Forcing:</b> Variations in Earth's orbital parameters (causing ice ages) or continental drift and geologic CO2 variations.</li>
            <li><b>Anthropogenic Climate Change:</b> Changes due to human activities, such as the ozone hole, acid rain, and global warming.</li>
        </ul>
        <br><br><br>
        <p>The main driver of observed warming since the industrial revolution is anthropogenic greenhouse gas emissions. The atmosphere consists mostly of Nitrogen (78.08%), Oxygen (20.95%), Argon (0.93%), and Water Vapor (0.1 to 2%). However, <b>trace gases</b> control the energy budget by absorbing infrared radiation:</p>
        <ul>
            <li><b>Carbon Dioxide (CO2):</b> ~377 ppm in 2004. Trend driven by fossil fuels; interannual variations driven by biology.</li>
            <li><b>Methane (CH4):</b> 1.75 ppm. Sources include cattle, sheep, rice paddies, wetlands, and termites.</li>
            <li><b>Chlorofluorocarbons (CFCs):</b> Man-made (zero before 1950). Rowland and Molina predicted their ozone destruction in 1974. Phased out by the 1987 Montreal Protocol, though recovery takes ~50 years.</li>
        </ul>
        <p>Earth's future annual average surface temperature is ultimately more predictable than internal weather variations because it is strictly controlled by the <i>energy balance</i>.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.3 Concept: Model Hierarchy & Grid Boxes":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.3: Modeling the System</h3>
        <p>Because the Earth System involves interlocking physical, chemical, and biological aspects, scientists use a hierarchy of mathematical models to simulate it:</p>
        <ul>
            <li><b>Simple Energy Balance Models:</b> Illustrate the fundamental importance of energy balance to the climate state.</li>
            <li><b>Intermediate Complexity Models:</b> Include basic atmosphere/ocean equations but retain only the processes relevant to a target phenomenon (like early ENSO models).</li>
            <li><b>General Circulation Models (GCMs):</b> The most complex. They divide the atmosphere and ocean into a discrete 3D grid (millions of grid boxes).</li>
        </ul>
        <br><br><br>
        <p>In a GCM, equations for the balance of forces and energy are solved numerically. The model calculates the acceleration and rate of change of temperature in each box, depends on neighboring boxes, and then steps forward in time (e.g., 20 minutes for the atmosphere, 1 hour for the ocean). Because simulating centuries is computationally expensive, current efforts are exploring machine-learning emulators.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.4 Concept: IPCC & Emissions Pathways":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.4: Policy and Projections</h3>
        <p>Climate models guide major policy bodies, notably the <b>Intergovernmental Panel on Climate Change (IPCC)</b>. Established in 1988 by UNEP and WMO, the IPCC does not conduct research but reviews it across three Working Groups: WG1 (Physical Science), WG2 (Impacts/Adaptation), and WG3 (Mitigation).</p>
        <br><br><br>
        <p><b>The Paris Agreement (2015, COP21):</b> Aims to hold global temperature rise to "well below 2°C above preindustrial levels" utilizing Nationally Determined Contributions (NDCs). A major gap remains between these NDCs and a 2°C pathway.</p>
        <p>To understand mitigation, we must link emissions to atmospheric concentrations. For a long-lived greenhouse gas like CO2:</p>
        <ul>
            <li><b>Increasing Emissions:</b> Concentration increases at an ever-faster rate.</li>
            <li><b>Constant Emissions:</b> Concentration undergoes an ongoing, continuous increase.</li>
            <li><b>Decreasing Emissions:</b> Concentration still increases, just less quickly.</li>
            <li><b>Very Low Emissions:</b> Only then does stabilization occur. If we overshoot, we must achieve "negative emissions" (actively removing CO2).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.5 Concept: Paleoclimate & Ice Cores":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.5: Deep Time</h3>
        <p>The distant geological past featured climates significantly warmer than present, with higher CO2 levels. Over millions of years, deposition sequestered this carbon as fossil fuels. Humans are returning this CO2 to the atmosphere over a microscopically short period.</p>
        <br><br><br>
        <p>For the past several hundred thousand years, we rely on Antarctic ice cores. Scientists analyze the isotope <b>Deuterium (D)</b>. Water molecules containing heavier isotopes evaporate less easily and condense more easily depending on temperature, allowing scientists to estimate historical temperatures.</p>
        <p>These records show ~100,000-year glacial cycles driven by the <b>Milankovitch theory</b>—variations in Earth's orbital parameters (tilt, eccentricity) with periods of 19, 23, 41, 100, and 400 thousand years. During glacial maximums, CO2 dropped to ~180 ppm, and sea levels plummeted 120 meters below present. During interglacials, CO2 stabilized around ~280 ppm. Modern CO2 levels massively exceed any natural levels seen in the past 650,000 years.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.6 Model: Smoothing Data":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: Moving Averages</h3>
        <p>To see the Anthropogenic trend (the signal), we must smooth out the internal variability (the noise). Watch what happens to the raw data when we apply a 10-year moving average in Python.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code('''
import pandas as pd # Import the pandas library to store and manipulate our data in a table structure
import numpy as np # Import the numpy library to handle complex mathematical arrays and random number generation

# Simulate 50 years of noisy temperature data
years = np.arange(1970, 2020) # Create an array of sequential years starting at 1970 and ending at 2019
noise = np.random.normal(0, 0.5, len(years)) # Generate random temperature variations (mean 0, standard deviation 0.5) for every single year
signal = 0.02 * (years - 1970) # Calculate the true warming trend (the signal), increasing by exactly 0.02 degrees each year
raw_temp = signal + noise # Add the random noise and the true signal together to create realistic chaotic weather data

# Store the simulated data in a structured DataFrame table
df = pd.DataFrame({'Year': years, 'Raw Temp': raw_temp}) 

# Apply a 10-year rolling average to smooth the noise
df['Smoothed Trend'] = df['Raw Temp'].rolling(window=10, center=True).mean() # Take a 10-year sliding window, calculate the average, and center it to reveal the hidden climate signal
        ''', language='python')
        
        if st.button("Run Code", type="primary"):
            st.markdown("### Output Analysis:")
            years = np.arange(1970, 2020)
            np.random.seed(42) 
            noise = np.random.normal(0, 0.4, len(years))
            signal = 0.02 * (years - 1970) 
            raw_temp = signal + noise
            df = pd.DataFrame({'Raw Temp (Noise)': raw_temp}, index=years)
            df['Smoothed Trend (Signal)'] = df['Raw Temp (Noise)'].rolling(window=10, center=True).mean()
            
            st.line_chart(df)
            
            st.info("""
            **Graph Analysis:**
            
            * **Raw Temp (Noise):** Notice how violently this line spikes up and down from year to year. This represents internal climate variability (like El Niño or La Niña). If you only looked at a short 3-to-4 year chunk of this line, you might falsely conclude the planet was rapidly cooling or rapidly warming. This chaotic short-term data represents "weather."
            * **Smoothed Trend (Signal):** By calculating a 10-year rolling average, we strip away the short-term, year-to-year chaos. What remains is a much smoother, steady upward slope. This reveals the underlying anthropogenic forcing (human-caused warming trend) of exactly 0.02 degrees per year that was completely hidden beneath the noise. This long-term statistical average represents "climate."
            """)
            
        render_next_button(chapter, page)

    elif page == "1.7 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 2 CONTENT ---
elif chapter == "2. Basics of Global Climate":
    if page == "2.1 Concept: Components & Parameterization":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.1: The Climate System</h3>
        <p>The climate system consists of distinct components acting across vastly different time scales:</p>
        <ul>
            <li><b>Atmosphere:</b> Responds in days to months.</li>
            <li><b>Ocean:</b> The upper layer responds in months to years, but the deep ocean responds in decades to millennia.</li>
            <li><b>Cryosphere:</b> Includes land ice, ice shelves, glaciers, snow, and sea ice. Responds in months (snow cover) to centuries/millennia (ice caps).</li>
            <li><b>Land Surface & Biosphere:</b> Regulates local moisture and responds in hours to decades.</li>
            <li><b>Lithosphere:</b> The solid earth, operating on extreme geological time scales (10,000s of years for isostatic rebound, 1,000,000s for mountain building).</li>
        </ul>
        <p><b>The Parameterization Problem:</b> When we simulate this system in climate models, we use grid boxes (e.g., 5°x5°). However, models only calculate the <i>average</i> across that box. Small-scale variations inside the box—like squall lines and cumulonimbus clouds—are completely invisible to the grid. Because these small-scale effects deeply impact large-scale heating and radiation, scientists must write equations to mathematically estimate their average effects based on the large-scale moisture and temperature. This estimation technique is called <b>parameterization</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.2 Concept: Energy Balance & Radiation":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.2: The Radiative Imbalance</h3>
        <p>Earth is powered by Solar radiation (Shortwave). The Solar Constant ($S_0$) is roughly 1366 W/m<sup>2</sup>. Because Earth is a sphere and half is in shadow, the average solar flux reaching the top of the atmosphere is about <b>342 W/m<sup>2</sup></b>.</p>
        <p><b>Albedo:</b> Earth's global average planetary albedo is 0.31 (31% of incident solar radiation is reflected back to space). Deep clouds reflect heavily (~0.9), while oceans absorb deeply (albedo ~0.08). The remaining solar radiation—nearly 50%—is absorbed directly by the surface.</p>
        <p><b>Stefan-Boltzmann Law:</b> The Earth must balance this absorbed heat by emitting Infrared (IR) radiation back to space. Emission depends strictly on temperature ($E = \sigma T^4$). Because IR emission scales to the 4th power of temperature, the planet is highly effective at shedding excess heat as it warms.</p>
        <p><b>The Greenhouse Effect:</b> Upward IR emitted from the surface is mostly trapped in the atmosphere by greenhouse gases. The atmosphere warms and re-emits this IR both upward to space and downward to the surface. This downward emission results in significant additional warming of the surface compared to an atmosphere with no IR absorption.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.3 Concept: Atmospheric Circulation":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.3: Atmospheric Heat Transport</h3>
        <p>Because the equator absorbs drastically more solar energy than the poles, there is a massive energy gradient. The atmosphere and ocean exist to transport this heat poleward.</p>
        <ul>
            <li><b>The Hadley Cell:</b> A thermally driven, overturning circulation. Hot air rises deep in the tropics (creating heavy precipitation features like the Intertropical Convergence Zone, or ITCZ) and sinks in the subtropics. This descent causes the subtropics to be warm at upper levels, making it hard to convect, resulting in very little rain (deserts).</li>
            <li><b>Midlatitudes:</b> Atmospheric circulation is dominated by westerlies (winds from the west). Here, energy and moisture transport is dominated by time-varying storms (transient weather disturbances) across storm tracks.</li>
            <li><b>The Walker Circulation:</b> Circulation is not perfectly symmetric. Longitudinally, the Walker circulation dominates the tropics, driven by intense rainfall and convection over the warm waters of the Western Pacific.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.4 Concept: Ocean Circulation & Land Surface":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.4: Currents and Land Use</h3>
        <p><b>Ocean Circulation:</b></p>
        <ul>
            <li><b>Surface Currents:</b> Driven by surface wind and constrained by Earth's rotation. There are easterly currents at the equator and anticyclonic gyres in the subtropics and middle latitudes. Compensating return flows occur in narrow, fast western boundary currents (like the Gulf Stream or Kuroshio).</li>
            <li><b>Thermohaline Circulation:</b> The deep ocean circulation. It is driven by water density, wind, and upwelling. Water density is dictated by both temperature (thermo) and salinity (haline). In small regions off Greenland or Antarctica, extremely cold and salty water sinks, driving exchanges of heat and carbon with the deep ocean on very long timescales.</li>
        </ul>
        <p><b>Land Surface:</b></p>
        <p>The land surface does not transport or store heat significantly compared to the ocean. However, it regulates local temperature, moisture, and carbon. Rapid land use changes, such as deforestation for agriculture or timber, degrade the capability of the terrestrial ecosystem to regulate these cycles, actively releasing carbon from soil and biomass into the atmosphere.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.5 Concept: The Carbon Cycle":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.5: Tracking The Reservoirs</h3>
        <p>Carbon cycles heavily between three major reservoirs:</p>
        <ol>
            <li><b>Ocean:</b> Holds ~85% of carbon, especially in the deep ocean.</li>
            <li><b>Fossil Fuel Reserves:</b> Holds ~8.9% (locked away over millions of years).</li>
            <li><b>Land:</b> Holds ~5.1%.</li>
        </ol>
        <p>The <b>Atmosphere</b> is a substantially smaller carbon reservoir, holding only 1.3%. Because it is so small, relatively tiny net carbon fluxes from human emissions have massive impacts.</p>
        <p><b>Anthropogenic Flux:</b> Fossil fuels emit roughly 8 to 10 PgC/yr (Petagrams of Carbon per year). Land use change adds roughly another 1.6 PgC/yr. Fortunately, only about half of this carbon remains in the atmosphere; the rest is taken up by the ocean and land vegetation sinks. However, atmospheric concentrations of CO2 still rise by about <b>1 ppm for each 2.1 PgC</b> that remains in the atmosphere.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.6 Model: Carbon Accumulation":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: Emissions to Concentrations</h3>
        <p>Using the professor's conversion factor (1 ppm = 2.1 PgC), let's mathematically model how decades of fossil fuel emissions accumulate in the atmosphere, accounting for the ~50% absorption rate by the ocean and land sinks.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code('''
import pandas as pd
import numpy as np

# Simulate years 2000 to 2050
years = np.arange(2000, 2051)

# Assume baseline emissions of 8.0 PgC/yr in 2000, growing steadily
emissions_PgC = 8.0 + 0.15 * (years - 2000)

# Only ~50% of emitted carbon remains in the atmosphere (the rest goes to sinks)
remains_in_atm = emissions_PgC * 0.50

# Conversion rule: Atmospheric concentrations rise 1 ppm for each 2.1 PgC
ppm_increase_per_year = remains_in_atm / 2.1

# Calculate cumulative accumulation starting from ~370 ppm in the year 2000
co2_ppm = np.zeros(len(years))
co2_ppm[0] = 370.0

for i in range(1, len(years)):
    co2_ppm[i] = co2_ppm[i-1] + ppm_increase_per_year[i]

df = pd.DataFrame({'CO2 Concentration (ppm)': co2_ppm}, index=years)
        ''', language='python')
        
        if st.button("Run Code", type="primary"):
            st.markdown("### Output Analysis:")
            years = np.arange(2000, 2051)
            emissions_PgC = 8.0 + 0.15 * (years - 2000)
            remains_in_atm = emissions_PgC * 0.50
            ppm_increase_per_year = remains_in_atm / 2.1
            
            co2_ppm = np.zeros(len(years))
            co2_ppm[0] = 370.0
            for i in range(1, len(years)):
                co2_ppm[i] = co2_ppm[i-1] + ppm_increase_per_year[i]
                
            df = pd.DataFrame({'CO2 Concentration (ppm)': co2_ppm}, index=years)
            
            st.line_chart(df)
            
            st.info("""
            **Graph Analysis:**
            Notice that the CO2 concentration does not just go up—it curves upward at an accelerating rate. Because raw emissions (PgC/yr) are increasing every year, the amount added to the atmosphere after the 50% sink reduction *also* increases every year. At a conversion rate of 2.1 PgC per 1 ppm, we see atmospheric concentrations crossing the critical 400 ppm boundary and accelerating rapidly towards 2050.
            """)
            
        render_next_button(chapter, page)

    elif page == "2.7 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 3 CONTENT ---
elif chapter == "3. Physical Processes":
    if page == "3.1 Concept: Momentum & Forces":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.1: Conservation of Momentum</h3>
        <p>To simulate the climate, models rely on Newton's second law ($ma=F$). For the atmosphere and ocean, this is evaluated as acceleration (rate of change of velocity) equaling the sum of forces per unit mass:</p>
        <p>$$ \text{Velocity Change} = \text{Coriolis} + \text{PGF} + \text{Gravity} + \text{Friction} $$</p>
        <br><br><br>
        <ul>
            <li><b>Coriolis Force:</b> An apparent force that acts on moving masses in a rotating reference frame. It turns a body to the right in the Northern Hemisphere and to the left in the Southern Hemisphere. The horizontal component is exactly zero at the equator.</li>
            <li><b>The Coriolis Parameter ($f$):</b> Equal to $(4\pi / 1 \text{ day}) \sin(\text{latitude})$.</li>
            <li><b>The Beta Effect:</b> The rate of change of the Coriolis parameter with latitude ($\beta = df/dy$). It is proportional to the cosine of latitude and is always positive, maxing out at the equator.</li>
            <li><b>Pressure Gradient Force (PGF):</b> A force per unit mass that naturally accelerates air from higher to lower pressure ($- \frac{1}{\rho} \frac{\partial p}{\partial x}$).</li>
            <li><b>Geostrophic Balance:</b> At large scales, the Coriolis force and the Pressure Gradient Force are the dominant horizontal forces. When they balance perfectly, the wind blows <i>parallel</i> to the isobars rather than straight across them.</li>
            <li><b>Friction ($F_{drag}$):</b> Near the surface, drag slows the wind down. Because the Coriolis force depends on velocity, a slower wind means a weaker Coriolis pull. With the Coriolis force weakened, the Pressure Gradient Force "wins," allowing wind to cross the isobars and spiral inward toward low-pressure centers.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "3.2 Concept: State & Hydrostatic Balance":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.2: Equation of State & Vertical Balance</h3>
        <p>The <b>Equation of State</b> physically relates density to temperature and pressure.</p>
        <ul>
            <li><b>Atmosphere:</b> Governed by the Ideal Gas Law ($p = \rho R T$), where $R = 287 \text{ J kg}^{-1} \text{K}^{-1}$. Density ($\rho$) decreases with warmer temperatures.</li>
            <li><b>Ocean:</b> Density is an empirical function of temperature, pressure, and importantly, <b>salinity</b>. A small increase in ocean temperature expands the water, calculated using the coefficient of thermal expansion ($\epsilon_T = 2.7 \times 10^{-4} \text{ C}^{-1}$). This is the physical mechanism behind sea level rise via thermal expansion.</li>
        </ul>
        <p><b>Hydrostatic Balance:</b> In the vertical direction, the pressure gradient force is overwhelmingly balanced by gravity ($dp/dz = -\rho g$). This means the pressure at any given level in the atmosphere or ocean is exactly proportional to the mass sitting directly above it.</p>
        <p><b>Thermal Circulations:</b> Because warmer air is less dense, a column of warm air stretches taller. This means that at the surface, the warm region will have low pressure, but aloft at higher altitudes, it will actually have <i>high</i> pressure compared to a neighboring cold region. This temperature gradient creates the pressure gradient that drives systems like the Hadley and Walker circulations.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "3.3 Concept: Temp, Continuity, & Chaos":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.3: Advection and Mass Conservation</h3>
        <p><b>The Temperature Equation:</b> Local temperature changes are driven by direct heating, adiabatic expansion/contraction, and <b>advection</b>. Advection terms carry properties from one region to another (e.g., wind blowing from the west carrying cold air, causing local temperatures to drop).</p>
        <br><br><br>
        <p><b>Chaos in Weather:</b> Advection acts as a highly complex, nonlinear feedback. A slight change in initial conditions (like a tiny temperature reading error) yields vastly different outcomes later. This sensitive dependence on initial conditions means that most aspects of precise weather patterns are entirely unpredictable after ~10 to 14 days.</p>
        <p><b>Continuity Equation (Conservation of Mass):</b> Mass cannot be created or destroyed. Horizontal divergence of fluid must be balanced by vertical motion. For example, in the ocean, easterly winds and the Coriolis force push surface currents away from the equator (divergence). To compensate for this missing water, deep, cold, nutrient-rich water must rise from below. This is the physical mechanism behind <b>Equatorial Upwelling</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "3.4 Concept: Moisture & Moist Processes":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.4: Water Vapor and Latent Heat</h3>
        <p><b>Specific Humidity:</b> The mass of water vapor divided by the total mass of air. It is controlled by the balance of sources (evaporation at the surface) and sinks (moist convection resulting in precipitation).</p>
        <p><b>Latent Heat:</b> Massive amounts of energy are stored and released during phase changes. The latent heat of condensation releases $2.50 \times 10^6 \text{ J kg}^{-1}$, which actively heats the surrounding atmosphere. Conversely, the latent heat of freezing (melting ice) requires $3.34 \times 10^5 \text{ J kg}^{-1}$.</p>
        <p><b>Saturation & Lapse Rates:</b></p>
        <ul>
            <li><b>Saturation:</b> Governed by the Clausius-Clapeyron relation. Saturation limits increase sharply with higher temperatures.</li>
            <li><b>Dry Adiabatic Lapse Rate:</b> When a parcel of air rises rapidly, it expands due to dropping pressure. This "work of expansion" cools the parcel without exchanging heat with the environment. The dry adiabatic lapse rate is exactly <b>10°C/km</b>.</li>
            <li><b>Moist Adiabatic Lapse Rate:</b> The parcel cools as it rises until it hits the <b>Lifting Condensation Level</b> (cloud base), where it becomes saturated. As it continues to rise, water vapor condenses, releasing latent heat. This extra heat fights the adiabatic cooling, resulting in a slower temperature drop of roughly <b>6°C/km</b>.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "3.5 Concept: Wave Processes":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.5: Rossby Waves</h3>
        <p>The high-altitude jet stream does not flow in a perfect, straight circle. It wobbles in giant, meandering loops known as <b>Rossby Waves</b>.</p>
        <br><br><br>
        <p>The properties of these waves depend heavily on their wavelength. Adjustment from initial conditions leaves a wave packet propagating slowly westward. While individual highs and lows propagate westward, the actual energy of the wave packet can propagate north, south, as well as eastward.</p>
        <p>Stationary Rossby waves can be excited and maintained by convective heating or flow over massive mountain ranges. Ultimately, Rossby waves are the fundamental mechanism that creates <b>teleconnections</b>—long-distance connections in the climate system that allow distant regions to severely impact each other's weather patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "3.6 Model: Adiabatic Lapse Rates":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: The Physics of Rising Air</h3>
        <p>Let's model the temperature profile of a rising parcel of air, comparing the Dry Adiabatic Lapse Rate (10°C/km) to the Moist Adiabatic Lapse Rate (~6°C/km) to visualize the warming power of latent heat condensation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code('''
import pandas as pd
import numpy as np

# Simulate altitude from 0 to 10 kilometers
altitude_km = np.arange(0, 11, 1)

# Surface temperature in Celsius
surface_temp = 30.0

# Dry Adiabatic Lapse Rate: drops 10 C per km (work of expansion)
dry_temp = surface_temp - (10.0 * altitude_km)

# Moist Adiabatic Lapse Rate: drops approx 6 C per km (latent heat release offsets cooling)
moist_temp = surface_temp - (6.0 * altitude_km)

df = pd.DataFrame({
    'Dry Adiabatic (Unsaturated)': dry_temp,
    'Moist Adiabatic (Saturated)': moist_temp
}, index=altitude_km)

df.index.name = 'Altitude (km)'
        ''', language='python')
        
        if st.button("Run Code", type="primary"):
            st.markdown("### Output Analysis:")
            altitude_km = np.arange(0, 11, 1)
            surface_temp = 30.0
            dry_temp = surface_temp - (10.0 * altitude_km)
            moist_temp = surface_temp - (6.0 * altitude_km)
            
            df = pd.DataFrame({
                'Dry Adiabatic (Unsaturated)': dry_temp,
                'Moist Adiabatic (Saturated)': moist_temp
            }, index=altitude_km)
            
            st.line_chart(df)
            
            st.info("""
            **Graph Analysis:**
            * **Dry Adiabatic:** A rapid cooling of exactly 10°C per kilometer. At 3km high, a 30°C surface parcel has already frozen (0°C).
            * **Moist Adiabatic:** A much slower cooling curve. Because the saturated parcel is constantly condensing water vapor into liquid cloud droplets, it is constantly releasing latent heat ($2.50 \\times 10^6$ J/kg) into itself. This keeps the upper troposphere significantly warmer than it would be otherwise.
            """)
            
        render_next_button(chapter, page)

    elif page == "3.7 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 4 CONTENT ---
elif chapter == "4. El Niño (ENSO)":
    if page == "4.1 Concept: Normal State & Climatology":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.1: The Walker Circulation & Normalcy</h3>
        <p>Before understanding El Niño, we must establish the Pacific's "Normal" conditions in three dimensions.</p>
        <p><b>Atmosphere:</b> Strong Trade Winds blow across the Pacific from East to West. This pushes air to rise in a massive convergence zone over the warm sea surface temperatures (SSTs) in the West.</p>
        <p><b>Ocean:</b> The trade winds act like a snowplow, physically pushing water westward. This causes the thermocline (the boundary between warm upper water and cold deep water) to be roughly <b>100 meters deeper in the west</b>. Consequently, sea level is about 40 cm higher in the west than in the east.</p>
        <br><br><br>
        <p>In the vertical average, the eastward pressure gradient force in the ocean perfectly balances the westward wind stress. Meanwhile, on the equator in the east, the wind stress and Coriolis force cause surface water to diverge, forcing shallow, cold, nutrient-rich water to upwell to the surface.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "4.2 Concept: El Niño & La Niña Extremes":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.2: The Extreme Phases</h3>
        <p><b>El Niño (Warm Phase):</b> The Trade Winds weaken, collapse, or reverse. The unbalanced eastward pressure gradient force in the ocean causes anomalous eastward currents. The deep thermocline from the west sloshes east, deepening the thermocline in the Eastern Pacific. Upwelling still occurs, but it brings up <i>less cold</i> water than normal, causing warmer SSTs and shifting rainfall eastward.</p>
        <br><br><br>
        <p><b>La Niña (Cold Phase):</b> The opposite extreme. Trade Winds strengthen beyond normal. The westward wind stress severely exceeds the eastward ocean pressure gradient, creating anomalous westward currents. The thermocline shallows dramatically in the east, and upwelling brings up water that is <i>colder</i> than normal. Rainfall concentrates heavily in the far western Pacific.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "4.3 Concept: Feedbacks & Oscillators":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.3: The Engines of ENSO</h3>
        <p><b>The Bjerknes Feedback (The Amplifier):</b> First hypothesized by Jakob Bjerknes in 1969, this is a positive, self-reinforcing loop. Weak winds lead to warmer East Pacific SSTs. This reduces the east-west temperature contrast, which is the very cause of the Walker circulation. A reduced temperature gradient causes the winds to weaken <i>even more</i>, driving further warming.</p>
        <p><b>The Delayed Oscillator (The Kill Switch):</b> Why doesn't an ENSO phase last forever? The transition is governed by slow ocean dynamics. Subsurface anomalies in the western Pacific (especially off the equator) evolve slowly and create a delayed effect.</p>
        <br><br><br>
        <p>Deep thermocline anomalies extend eastward as <i>Kelvin waves</i>. Meanwhile, shallow thermocline anomalies extend westward as <i>Rossby waves</i>. When these Rossby waves hit the western boundary of the Pacific, they can no longer travel west. They reflect back eastward, eventually returning across the equator to the Eastern Pacific to violently pull the thermocline back up, ending the El Niño.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "4.4 Concept: ENSO Prediction Limits & Ensembles":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.4: Forecasting the Cycle</h3>
        <p><b>Reliability:</b> 3 to 9-month lead-time predictions of ENSO indices (like Niño-3.4) are generally reliable, though skill inherently decreases with longer lead times. However, the exact spatial pattern of the SST anomaly is less reliable than the general index.</p>
        <p><b>Limits to Predictability:</b> Forecasts lose skill for two main reasons:</p>
        <ol>
            <li><i>Imperfections in the forecast system:</i> Model errors and a scarcity of input data (which can be improved with better technology).</li>
            <li><i>Fundamental limits (Chaos):</i> "Weather noise" acts like a random forcing on the slow ocean-atmosphere interaction. Random transient weather events (like a localized storm) can cause equatorial easterlies to temporarily differ from the expected Bjerknes feedback, causing the cycle to depart from its predicted evolution.</li>
        </ol>
        <br><br><br>
        <p><b>Ensemble Forecasting:</b> To communicate uncertainty, scientists run coupled models starting from slightly different initial ocean conditions. This "ensemble spread" provides an estimate of uncertainty, while the ensemble mean gives the best overall estimate.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "4.5 Concept: Teleconnections & Remote Impacts":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.5: Global Shockwaves</h3>
        <p>ENSO heavily influences global atmospheric and climate anomalies through <b>teleconnections</b>—long-distance linkages. These impact regions shift depending on the seasonal climatology.</p>
        <ul>
            <li><b>Anomalous Planetary Wave Trains:</b> El Niño excites massive atmospheric waves. In the Northern Hemisphere winter (Dec-Feb), this manifests as the <b>Pacific-North America (PNA) teleconnection</b>. In the austral winter (Jun-Aug), it drives the Pacific-South America (PSA) teleconnection.</li>
            <li><b>Jet Stream & Storm Tracks:</b> These planetary waves alter the path of the jet stream, directly shifting global storm tracks.</li>
            <li><b>California Precipitation:</b> During an El Niño, the probability distribution of winter precipitation shifts. The probability of a rainier-than-average winter is substantially enhanced (especially during strong events), but it is <i>far from certain</i> due to the random internal variability of weather noise.</li>
            <li><b>Atlantic Hurricanes:</b> The shifting atmospheric shears from El Niño tend to suppress tropical cyclone development, leading to fewer "named storms" and hurricanes in the Atlantic basin during the July-October season.</li>
            <li><b>Other Phenomena:</b> Other climate patterns include the North Atlantic Oscillation (NAO) / Annular Modes (which shift storm tracks impacting European precipitation) and the Pacific Decadal Oscillation (PDO), which operates on much longer timescales than ENSO.</li>
        </ul>
        <br><br><br>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "4.6 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 5 CONTENT ---
elif chapter == "5. Greenhouse Effect & Feedbacks":
    if page == "5.1 Concept: Global Energy Balance & 1-Layer Model":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.1: The Net Radiation Math</h3>
        <p>To understand feedbacks, we must establish the baseline 1-Layer Energy Balance model in terms of Watts per square meter ($W/m^2$).</p>
        <br><br><br>
        <ul>
            <li><b>Incoming Solar:</b> The average solar radiation reaching the top of the atmosphere is roughly <b>342 $W/m^2$</b>.</li>
            <li><b>Reflection:</b> About 107 $W/m^2$ is immediately reflected back to space by clouds and the surface (albedo).</li>
            <li><b>Absorption:</b> The remaining solar radiation is absorbed: 67 $W/m^2$ by the atmosphere, and <b>168 $W/m^2$</b> absorbed directly by the surface.</li>
        </ul>
        <p>To maintain balance, the Earth must re-emit an equal amount of energy to space. In the 1-layer atmospheric model, we assume "normal" climatology where the atmosphere absorbs roughly <b>90%</b> ($\epsilon_a = 0.90$) of the infrared radiation (IR) emitted by the surface. The atmosphere then radiates IR both up to space and back down to the surface, creating a massive 34°C difference compared to an Earth with no atmosphere.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "5.2 Concept: Greenhouse Radiative Forcing":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.2: Forcing the System</h3>
        <p>When humans add greenhouse gases to the atmosphere, the absorptivity ($\epsilon_a$) of the atmosphere increases. This traps more upgoing IR that would have otherwise escaped to space.</p>
        <p><b>Radiative Forcing ($G$):</b> This is defined as the exact energy imbalance (in $W/m^2$) at the top of the atmosphere <i>before</i> the temperature changes to restore the energy balance. A larger $G$ represents a larger initial deficit in outgoing IR, meaning the surface and atmosphere will have to warm significantly to force enough radiation out to balance the books.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "5.3 Concept: The Climate Feedback Parameter":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.3: The Physics of Alpha</h3>
        <p>As the surface warms to fight the radiative forcing, it emits more IR. The increase in outgoing IR to space per unit increase in surface temperature is known as the <b>Climate Feedback Parameter ($\\alpha$)</b>.</p>
        <p>In a simple model with no extra environmental changes, warming the surface safely balances the forcing ($\\alpha_T \\Delta T_s = G$). However, the climate system reacts: $\\alpha = \\alpha_T + \\alpha_{H_2O} + \\alpha_{ice} + \\alpha_{cloud}$.</p>
        <p><i>Crucial mathematical note:</i> Positive, amplifying feedbacks (like water vapor) actually have a <b>negative mathematical contribution</b> to the total $\\alpha$. Because $\\Delta T_s = G / \\alpha$, a smaller cumulative $\\alpha$ results in a much larger final temperature change.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "5.4 Concept: Water Vapor & Ice Feedbacks":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.4: The Leading Amplifiers</h3>
        <p><b>The Water Vapor Feedback (Positive):</b> As temperature increases, the atmosphere can hold more water vapor. For temperatures typical of the lower troposphere, water vapor increases about <b>7% per °K</b> of warming. Because water vapor is a potent greenhouse gas, it traps more heat, driving more evaporation ($\\alpha_{H_2O} = -2.0$ to $-1.5$ $W/m^2K^{-1}$).</p>
        <p><b>The Snow/Ice Feedback (Positive):</b> Decreases in snow cover and sea ice expose darker ocean and land surfaces. This decreases the global albedo, allowing the Earth to absorb more solar radiation, which amplifies the warming ($\\alpha_{ice} = -0.3$ to $-0.1$ $W/m^2K^{-1}$).</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "5.5 Concept: Cloud & Lapse Rate Feedbacks":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.5: The Complex Modifiers</h3>
        <p><b>Cloud Feedbacks (The Wildcard):</b> Clouds have opposing effects making them highly uncertain.</p>
        <br><br><br>
        <ul>
            <li><i>Low Clouds:</i> Tend to reflect heavy amounts of solar radiation (Net Cooling tendency).</li>
            <li><i>High Clouds:</i> Tend to transmit solar radiation but absorb upwelling IR. Because they are at a higher, colder altitude, they emit very weak IR to space, effectively trapping heat (Net Warming tendency).</li>
            <li><i>Cloud Top Feedback:</i> With warming, cloud tops tend to reach higher, colder altitudes, increasing their warming tendency.</li>
        </ul>
        <p><b>Lapse Rate Feedback:</b></p>
        <ul>
            <li><i>Tropics (Negative Feedback):</i> The upper troposphere warms faster than the surface. This warmer upper level emits more IR to space, acting as a brake on global warming.</li>
            <li><i>High Latitudes (Positive Feedback):</i> The surface warms faster than the upper troposphere.</li>
            <li><i>Note:</i> Inter-model variations of the water vapor feedback tend to cancel out variations in the lapse rate feedback.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "5.6 Concept: Transient vs. Equilibrium Response":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.6: The Delay in the System</h3>
        <p>There are two distinct types of climate projections:</p>
        <ul>
            <li><b>Equilibrium Climate Projections:</b> Represent the final climate change that will be reached eventually once it comes into complete balance with the forcing.</li>
            <li><b>Transient Climate Projections:</b> Project the climate changes in real-time as they go.</li>
        </ul>
        <br><br><br>
        <p>Because the oceans (and ice sheets) possess a massive heat capacity, they absorb a huge portion of the energy imbalance. This causes the transient warming to <b>lag</b> behind the equilibrium response. If greenhouse gas concentrations are suddenly capped (stopped from increasing), the temperature will still continue to rise for decades simply waiting for the ocean's massive thermal inertia to catch up.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "5.7 Model: 1-Layer Energy Balance":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: The Mathematics of Alpha</h3>
        <p>Let's model the impact of positive feedbacks on total equilibrium warming. Using the equation $\\Delta T_s = G / \\alpha$, we apply a theoretical $4.3 W/m^2$ forcing (doubled CO2) and watch how adding positive feedbacks shrinks $\\alpha$ and amplifies the temperature.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code('''
import pandas as pd
import numpy as np

# Simulate different feedback scenarios
# Equation: Delta T = G / alpha
G_doubled_co2 = 4.3  # Radiative forcing (W/m^2)

# Scenarios building up the feedbacks
scenarios = ["1. Basic IR Only", "2. + Water Vapor", "3. + Snow/Ice", "4. + Clouds"]

# Alpha values decrease as positive amplifying feedbacks are mathematically subtracted
alphas = [4.0, 2.0, 1.8, 1.4] 

# Calculate final equilibrium temperature change
delta_T = [G_doubled_co2 / a for a in alphas]

df = pd.DataFrame({'Equilibrium Warming (K)': delta_T}, index=scenarios)
        ''', language='python')
        
        if st.button("Run Code", type="primary"):
            st.markdown("### Output Analysis:")
            G_doubled_co2 = 4.3
            scenarios = ["1. Basic IR Only", "2. + Water Vapor", "3. + Snow/Ice", "4. + Clouds"]
            alphas = [4.0, 2.0, 1.8, 1.4] 
            delta_T = [G_doubled_co2 / a for a in alphas]
            
            df = pd.DataFrame({'Equilibrium Warming (K)': delta_T}, index=scenarios)
            
            st.bar_chart(df)
            
            st.info("""
            **Graph Analysis:**
            Notice how the equilibrium warming ($\\Delta T_s$) skyrockets as we add more positive feedbacks. 
            The basic physics of CO2 trapping heat (Scenario 1) only yields about 1.1K of warming. 
            But when we include the reality that a warmer atmosphere holds more water vapor (Scenario 2), melts reflective ice (Scenario 3), and shifts cloud tops (Scenario 4), the cumulative feedback parameter $\\alpha$ shrinks significantly, amplifying the final temperature change to over 3K.
            """)
            
        render_next_button(chapter, page)

    elif page == "5.8 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 6 CONTENT ---
elif chapter == "6. Global Warming Scenarios":
    if page == "6.1 Concept: Radiative Forcing & Aerosols":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.1: The Net Energy Balance</h3>
        <p><b>Radiative Forcing ($Q$):</b> This is the net change in energy entering versus leaving the Earth system, measured in Watts per square meter. $CO_2$ is the dominant positive (warming) forcing.</p>
        <p><b>Sulfate Aerosols:</b> Burning coal and volcanic eruptions release sulfur particles. These act as a strong negative forcing. They physically reflect sunlight and act as seeds to create highly reflective low clouds. However, unlike $CO_2$ which stays in the atmosphere for centuries, aerosols literally rain out of the sky in a matter of days or weeks.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "6.2 Concept: The Commitment Concept":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.2: Unstoppable Momentum</h3>
        <p>Climate policy often discusses the <b>Constant Composition Commitment</b>.</p>
        <p>If humanity magically stopped emitting all greenhouse gases today, locking the atmosphere's composition exactly where it is right now, the planet's temperature would <i>still continue to rise for decades</i>.</p>
        <p>Why? Because the Deep Ocean is a massive thermal sink. It takes decades for that deep, cold water to fully absorb the heat from the atmosphere. We are "committed" to future warming simply waiting for the ocean to reach equilibrium with the heat we have already trapped.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "6.3 Concept: Spatial Patterns":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.3: Where the Heat Goes</h3>
        <p>Global warming is not uniform across the globe.</p>
        <ul>
            <li><b>Polar Amplification:</b> The Arctic is warming at nearly four times the rate of the tropics. As reflective white ice melts, it reveals dark ocean water. The dark water absorbs massive amounts of heat, melting more ice in a vicious cycle.</li>
            <li><b>Land vs. Ocean:</b> Landmasses warm much faster than oceans. The ocean has an incredibly high heat capacity—meaning it can absorb massive amounts of thermal energy before its temperature actually registers an increase.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "6.4 Concept: Sea Level Rise":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.4: The Expanding Ocean</h3>
        <p>Sea levels are rising due to two distinct physical mechanisms:</p>
        <ol>
            <li><b>Land Ice Melt:</b> Massive glaciers and ice sheets situated on land (Greenland and Antarctica) melt and dump physically new water into the ocean basin. (Note: Melting sea ice, like at the North Pole, does not raise sea levels, just as a melting ice cube doesn't overflow a glass of water).</li>
            <li><b>Thermal Expansion:</b> The fluid mechanics rule from Chapter 3. As the ocean absorbs heat, the water molecules physically vibrate more and spread further apart, expanding the total volume of the ocean.</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "6.5 Model: Sea Level Dynamics":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: Components of Sea Level Rise</h3>
        <p>Let's model the dual impact of Thermal Expansion and Land Ice melt on total sea level rise over the next century.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code('''
import pandas as pd
import numpy as np

# Simulate years 2020 to 2120
years = np.arange(2020, 2121)

# Thermal expansion: steady, linear increase (mm)
thermal = 1.2 * (years - 2020)

# Land Ice melt: accelerates non-linearly due to feedback loops (mm)
ice_melt = 0.5 * ((years - 2020) ** 1.3)

# Total Sea Level Rise
total_slr = thermal + ice_melt

df = pd.DataFrame({
    'Thermal Expansion': thermal,
    'Land Ice Melt': ice_melt,
    'Total Sea Level Rise': total_slr
}, index=years)
        ''', language='python')
        
        if st.button("Run Code", type="primary"):
            st.markdown("### Output Analysis:")
            years = np.arange(2020, 2121)
            thermal = 1.2 * (years - 2020)
            ice_melt = 0.5 * ((years - 2020) ** 1.3)
            total_slr = thermal + ice_melt
            
            df = pd.DataFrame({
                'Thermal Expansion (Steady)': thermal,
                'Land Ice Melt (Accelerating)': ice_melt,
                'Total Sea Level Rise': total_slr
            }, index=years)
            
            st.line_chart(df)
            
            st.info("""
            **Graph Analysis:**
            * **Thermal Expansion:** Shows a steady, linear rise. As the ocean slowly absorbs heat, it steadily expands.
            * **Land Ice Melt:** Notice the curve. Ice melt accelerates as time goes on because of powerful feedback loops (like Polar Amplification). 
            * **Total:** The combination of both factors leads to an aggressively accelerating sea level rise curve toward the end of the century.
            """)
            
        render_next_button(chapter, page)

    elif page == "6.6 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- FINAL EXAM ---
elif chapter == "Final Exam: Terminal Clearance":
    if page == "Final Knowledge Check":
        st.warning("WARNING: This is the final evaluation. Questions are pulled from all previous databanks.")
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=10)
