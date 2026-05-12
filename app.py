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
            "1.1 Concept: Correlation vs. Causation",
            "1.2 Concept: Weather, Climate, & Anomalies", 
            "1.3 Concept: Drivers & Greenhouse Gases", 
            "1.4 Concept: Model Hierarchy & Grid Boxes", 
            "1.5 Concept: IPCC & Emissions Pathways",
            "1.6 Concept: Paleoclimate & Ice Cores",
            "1.7 Model: Smoothing Data",
            "1.8 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "According to the notes, what is the danger of assuming causation from correlation?", "opts": ["It is always accurate.", "There could be a third factor involved or it could be by chance (e.g., cheese consumption and engineering degrees).", "Correlation is mathematically equivalent to causation."], "ans": "There could be a third factor involved or it could be by chance (e.g., cheese consumption and engineering degrees)."},
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
            {"q": "During La Niña, what happens to the trade winds and ocean currents?", "opts": ["Trade winds weaken, eastward PGF dominates.", "Trade winds strengthen, westward wind stress exceeds eastward PGF causing anomalous westward currents.", "Trade winds reverse, flowing west to east."], "ans": "Trade winds strengthen, westward wind stress exceeds eastward PGF causing anomalous westward currents."},
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
            {"q": "What are the three main roles for clouds and convection in the climate system?", "opts": ["Creating wind, blocking cosmic rays, and cooling the ocean.", "Heating the atmosphere, reflecting solar radiation (albedo), and trapping infrared radiation (greenhouse effect).", "Absorbing UV, reflecting IR, and producing ozone."], "ans": "Heating the atmosphere, reflecting solar radiation (albedo), and trapping infrared radiation (greenhouse effect)."},
            {"q": "In the detailed radiation budget, how much incoming solar radiation is reflected by clouds, aerosols, and atmospheric gases?", "opts": ["30 W/m2", "107 W/m2", "77 W/m2"], "ans": "77 W/m2"},
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
            "6.1 Concept: Forcings, Aerosols, & Predictability", 
            "6.2 Concept: Emissions Scenarios (SRES, RCPs, SSPs)", 
            "6.3 Concept: Emissions vs. Concentrations & The Gap", 
            "6.4 Concept: Global-Average Response & Ensembles",
            "6.5 Concept: Commitment & Long-Term Sea Level Rise",
            "6.6 Model: Sea Level Dynamics",
            "6.7 Model: Constant Composition Commitment",
            "6.8 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "For a long-lived greenhouse gas, what happens to the concentration if human emissions are kept completely constant?", "opts": ["The concentration increases at a constant rate.", "The concentration increases at an increasing rate.", "The concentration stabilizes."], "ans": "The concentration increases at a constant rate."},
            {"q": "What is the formula for calculating the change in sea level depth (dh) due to thermal expansion?", "opts": ["dh/h = epsilon_T * dT", "dh = mass * volume", "dh/dT = rho * h"], "ans": "dh/h = epsilon_T * dT"},
            {"q": "What is the primary global effect of sulfate aerosols on the climate system?", "opts": ["Net cooling tendency by reflection of sunlight.", "Net warming by trapping infrared radiation.", "Destruction of the ozone layer."], "ans": "Net cooling tendency by reflection of sunlight."},
            {"q": "How does the residence time of aerosols compare to long-lived greenhouse gases?", "opts": ["They have very short residence times compared to long-lived GHGs.", "They stay in the atmosphere for centuries.", "They are permanently trapped in the stratosphere."], "ans": "They have very short residence times compared to long-lived GHGs."},
            {"q": "In CMIP5, what does the '8.5' in the RCP 8.5 scenario represent?", "opts": ["8.5 degrees of warming by 2100.", "8.5 W/m2 radiative forcing in 2100.", "8.5 meters of sea level rise."], "ans": "8.5 W/m2 radiative forcing in 2100."},
            {"q": "In the CMIP6 framework, what does the SSP5-8.5 scenario represent?", "opts": ["A sustainable, green-technology pathway.", "Fossil-fueled development with global population peaking and declining in the 21st century.", "Resurgent nationalism with low economic growth."], "ans": "Fossil-fueled development with global population peaking and declining in the 21st century."},
            {"q": "If human greenhouse gas emissions remain perfectly constant over time, what happens to the atmospheric concentration?", "opts": ["It stabilizes immediately.", "It undergoes an ongoing, continuous increase.", "It slowly decreases."], "ans": "It undergoes an ongoing, continuous increase."},
            {"q": "According to the professor's notes, what is required if emissions are not brought down quickly enough and CO2 overshoots the stabilization target?", "opts": ["Negative emissions (actively removing CO2).", "A massive increase in sulfate aerosols.", "Nothing, the ocean will instantly absorb the excess."], "ans": "Negative emissions (actively removing CO2)."},
            {"q": "What does the 'emissions gap' refer to in the UNEP report?", "opts": ["The difference between North American and European emissions.", "The difference between Nationally Determined Contributions (NDCs) and the reductions needed to stay under 2°C.", "The gap in satellite data tracking carbon dioxide."], "ans": "The difference between Nationally Determined Contributions (NDCs) and the reductions needed to stay under 2°C."},
            {"q": "When dozens of climate models are run with the exact same emissions scenario, why is there an 'envelope' or spread of different temperature projections?", "opts": ["Because of differences in simulated climate feedbacks and internal natural variability.", "Because the supercomputers run at different speeds.", "Because the scenarios are secretly different for each group."], "ans": "Because of differences in simulated climate feedbacks and internal natural variability."},
            {"q": "What is the 'Constant composition commitment'?", "opts": ["The commitment of nations to keep their emissions constant.", "The continued global warming that occurs even if radiative forcing is kept constant at current levels.", "The commitment to maintain constant cloud cover."], "ans": "The continued global warming that occurs even if radiative forcing is kept constant at current levels."},
            {"q": "Why do sea level rise projections show an ongoing increase even long after CO2 concentrations are stabilized?", "opts": ["Because rain falls more frequently in a warmer world.", "Because the deep ocean and ice sheets have very long response times to warming.", "Because landmasses are physically sinking."], "ans": "Because the deep ocean and ice sheets have very long response times to warming."}
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
    if page == "1.1 Concept: Correlation vs. Causation":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.1: Correlation Does Not Imply Causation</h3>
        <p>In climate science, determining the cause of observed trends is critical. Just because two variables track each other perfectly does not mean one causes the other.</p>
        <p>Say variable "a" is correlated to variable "b". The possibilities are:</p>
        <ul>
            <li>"a" could cause "b"</li>
            <li>"b" could cause "a"</li>
            <li>Correlation by chance</li>
            <li>A third factor is involved in their correlation</li>
        </ul>
        <br><br><br>
        <p><b>Example:</b> The per capita consumption of mozzarella cheese correlates almost perfectly with the number of civil engineering doctorates awarded between 2000 and 2009. This is a spurious correlation by chance, not a physical mechanism.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.2 Concept: Weather, Climate, & Anomalies":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.2: Weather vs. Climate</h3>
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

    elif page == "1.3 Concept: Drivers & Greenhouse Gases":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.3: Drivers of Variation</h3>
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

    elif page == "1.4 Concept: Model Hierarchy & Grid Boxes":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.4: Modeling the System</h3>
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

    elif page == "1.5 Concept: IPCC & Emissions Pathways":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.5: Policy and Projections</h3>
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

    elif page == "1.6 Concept: Paleoclimate & Ice Cores":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.6: Deep Time</h3>
        <p>The distant geological past featured climates significantly warmer than present, with higher CO2 levels. Over millions of years, deposition sequestered this carbon as fossil fuels. Humans are returning this CO2 to the atmosphere over a microscopically short period.</p>
        <br><br><br>
        <p>For the past several hundred thousand years, we rely on Antarctic ice cores. Scientists analyze the isotope <b>Deuterium (D)</b>. Water molecules containing heavier isotopes evaporate less easily and condense more easily depending on temperature, allowing scientists to estimate historical temperatures.</p>
        <p>These records show ~100,000-year glacial cycles driven by the <b>Milankovitch theory</b>—variations in Earth's orbital parameters (tilt, eccentricity) with periods of 19, 23, 41, 100, and 400 thousand years. During glacial maximums, CO2 dropped to ~180 ppm, and sea levels plummeted 120 meters below present. During interglacials, CO2 stabilized around ~280 ppm. Modern CO2 levels massively exceed any natural levels seen in the past 650,000 years.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.7 Model: Smoothing Data":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: AOS102 Problem Set 1B - Smoothing Global Temp Anomalies</h3>
        <p>In this interactive module based directly on your PbSet 1B, you will analyze global average surface temperature anomalies from 1850 to 2025. You can adjust the <b>moving average window</b> to separate natural internal variability (noise) from the long-term anthropogenic trend (signal).</p>
        </div>
        """, unsafe_allow_html=True)
        
        window_size = st.slider("Select Moving Average Length (Years):", min_value=5, max_value=80, value=40, step=1)
        
        if st.button("Run Smoothing Analysis", type="primary"):
            st.markdown("### Output Analysis:")
            
            # Simulate historical data resembling NCEI 1850-2025 global temp anomaly
            years = np.arange(1850, 2026)
            np.random.seed(42)
            trend = 0.00008 * (years - 1850)**2 - 0.2  
            noise = np.random.normal(0, 0.15, len(years))
            raw_temp = trend + noise
            # specific 1877/1878 spike from homework
            raw_temp[1877-1850] += 0.4
            raw_temp[1878-1850] += 0.4
            
            df = pd.DataFrame({'Raw Temp Anomaly': raw_temp}, index=years)
            df[f'{window_size}-Year Moving Average'] = df['Raw Temp Anomaly'].rolling(window=window_size, center=True).mean()
            
            st.line_chart(df)
            
            departures = df['Raw Temp Anomaly'] - df[f'{window_size}-Year Moving Average']
            std_dev = departures.std()
            
            st.markdown(f"**Departures from the {window_size}-Year Moving Average:**")
            
            dep_df = pd.DataFrame({'Departures': departures}, index=years)
            dep_df['+1 Std Dev'] = std_dev
            dep_df['-1 Std Dev'] = -std_dev
            dep_df['+2 Std Dev'] = 2 * std_dev
            dep_df['-2 Std Dev'] = -2 * std_dev
            
            st.line_chart(dep_df)
            
            st.info(f"""
            **Homework Analysis (PbSet 1B):**
            * The standard deviation of the departures is **{std_dev:.3f} °C**.
            * If this data followed a perfect normal (Gaussian) distribution, we would expect about 68% of the data to fall within $\pm 1$ standard deviation, and only exceed $\pm 2$ standard deviations about 4.6% of the time.
            * Notice the extreme positive departures in **1877 and 1878**. As noted in the homework, these years experienced an exceptionally strong global El Niño event, driving massive internal variability spikes far beyond the standard deviation!
            """)
            
        render_next_button(chapter, page)

    elif page == "1.8 Knowledge Check":
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
        <p><b>Stefan-Boltzmann Law:</b> The Earth must balance this absorbed heat by emitting Infrared (IR) radiation back to space. The total energy flux integrated across all wavelengths of light for a blackbody emitter depends on absolute temperature T by the Stefan-Boltzmann law: $R = \sigma T^4$, where $\sigma = 5.67 \times 10^{-8} Wm^{-2}K^{-4}$ and T is in Kelvin.</p>
        <p>Actual surfaces or gases do not absorb or emit as a perfect blackbody, so we define an emissivity ($\epsilon$) for each substance. Since absorptivity equals emissivity, the equation becomes $R = \epsilon \sigma T^4$. At the top of the atmosphere, in the global average and for a steady climate, IR emitted balances incoming solar. Global warming involves a slight imbalance where less IR is emitted from the top, leading to a slow warming.</p>
        <p><b>Seasons:</b> It is also important to note that the real reason we have seasons is due to the tilt of the Earth affecting sunlight distribution, not the distance from the sun.</p>
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
        <p><b>Anthropogenic Flux:</b> According to recent carbon budget data (e.g., Friedlingstein et al. 2023), carbon emissions are balanced by sinks. Specifically: Fossil Emissions ($E_{FOS}$) + Net Land-use Change Emissions ($E_{LUC}$) = Atmospheric Growth ($G_{ATM}$) + Land Sink ($S_{LAND}$) + Ocean Sink ($S_{OCEAN}$). These are measured in gigatons of carbon per year ($1 Gt = 1 Pg$). This imbalance implies a rising concentration, and the rate of increase has been increasing over decades.</p>
        <p>Fortunately, only about half of this carbon remains in the atmosphere; the rest is taken up by the ocean and land vegetation sinks. However, atmospheric concentrations of CO2 still rise by about <b>1 ppm for each 2.1 PgC</b> that remains in the atmosphere.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.6 Model: Carbon Accumulation":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: AOS102 Problem Set 2 - Carbon Scenarios</h3>
        <p>This interactive model integrates global CO2 emissions into atmospheric concentrations from 2024 to 2050 using the exact parameters from your homework.</p>
        <ul>
            <li><b>Scenario A:</b> Emissions grow at the historical rate (approx. 0.52 GtCO2/yr per year). Human emissions each year are roughly 17 Gt/yr larger in 2024 than they were in 1990.</li>
            <li><b>Scenario B:</b> Emissions are suddenly capped at 2024 levels (39.6 Gt/yr), staying constant till 2050.</li>
            <li><b>Scenario C:</b> Emissions decrease linearly to zero in 2050.</li>
            <li><b>Scenario D:</b> Emissions decrease linearly to zero in 2030 (highly optimistic) and then remain zero.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        frac_remain = st.slider("Fraction of Emissions Remaining in Atmosphere (Default 0.47):", 0.10, 1.00, 0.47, 0.01)
        
        if st.button("Simulate Scenarios", type="primary"):
            years = np.arange(2024, 2051)
            
            emissions_A = 39.6 + 0.52 * (years - 2024)
            emissions_B = np.full(len(years), 39.6)
            emissions_C = 39.6 - 39.6 * (years - 2024) / (2050 - 2024)
            emissions_D = np.where(years <= 2030, 39.6 - 39.6 * (years - 2024) / (2030 - 2024), 0.0)
            
            def calc_concentration(emissions_array):
                conc = np.zeros(len(years))
                conc[0] = 424.6  # 2024 starting value 
                for i in range(1, len(years)):
                    conc[i] = conc[i-1] + frac_remain * (emissions_array[i] / 7.8)
                return conc
                
            conc_A = calc_concentration(emissions_A)
            conc_B = calc_concentration(emissions_B)
            conc_C = calc_concentration(emissions_C)
            conc_D = calc_concentration(emissions_D)
            
            df_conc = pd.DataFrame({
                'Scenario A (Historical Growth)': conc_A,
                'Scenario B (Constant 2024 Levels)': conc_B,
                'Scenario C (Zero by 2050)': conc_C,
                'Scenario D (Zero by 2030)': conc_D
            }, index=years)
            
            st.line_chart(df_conc)
            
            ppm_diff = conc_A[-1] - conc_D[-1]
            gt_diff = ppm_diff * 7.8
            cost_trillions = gt_diff * 100 / 1000 
            
            st.info(f"""
            **Homework Analysis (PbSet 2):**
            * By 2050, **Scenario A** reaches a staggering **{conc_A[-1]:.1f} ppm**, while the aggressive **Scenario D** stabilizes at **{conc_D[-1]:.1f} ppm**.
            * The conversion factor used here is exactly $1 \\text{ ppm} = 7.8 \\text{ GtCO}_2$. 
            * If you changed the fraction remaining from the historical average of $0.47$ (the average percent for 2013-2022) to a higher value (like $0.55$), it implies the ocean and land carbon sinks are losing their capacity to absorb human emissions. This would drastically amplify the 2100 concentrations for the higher pathways (A and B).
            * **Carbon Capture Economics:** To manually bring Scenario A down to Scenario D's {conc_D[-1]:.1f} ppm in 2050, you would have to extract **{gt_diff:.1f} Gigatons** of CO2. At an optimistic \$100/tonne, this would cost roughly **\${cost_trillions:.1f} Trillion**!
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
        <p><b>El Niño (Warm Phase):</b> Warmer SST in the east; rainfall tends to spread east. The Trade Winds weaken. The unbalanced eastward Pressure Gradient Force (PGF) in the ocean causes anomalous currents in the vertical average through the layer above the thermocline. The thermocline deepens in the east. Upwelling on the equator in the east Pacific brings up water that is less cold than normal.</p>
        <br><br><br>
        <p><b>La Niña (Cold Phase):</b> Cooler SST in the east; rainfall concentrated in the west. Trade Winds strengthen. The westward wind stress exceeds the eastward PGF in the ocean, creating anomalous currents along the Equator. The thermocline shallows in the east. Upwelling on the equator in the east Pacific brings up water colder than normal.</p>
        <br><br><br>
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
            <li><b>Incoming Solar:</b> The average solar radiation reaching the top of the atmosphere is <b>342 $W/m^2$</b>.</li>
            <li><b>Reflection:</b> 107 $W/m^2$ is reflected back to space (77 by clouds, aerosol, and atmospheric gases; 30 by the surface).</li>
            <li><b>Absorption:</b> The remaining solar radiation is absorbed: 67 $W/m^2$ by the atmosphere, and <b>168 $W/m^2$</b> absorbed directly by the surface.</li>
        </ul>
        <p>Surface energy fluxes include Surface Radiation (390 $W/m^2$), Back Radiation from the atmosphere (324 $W/m^2$), Latent Heat via Evapotranspiration (78 $W/m^2$), and Thermals (24 $W/m^2$).</p>
        <p>To maintain balance, the Earth must re-emit an equal amount of energy to space. Outgoing Longwave Radiation totals 235 $W/m^2$, which consists of 165 emitted by the atmosphere, 30 emitted by clouds, and 40 escaping through the atmospheric window.</p>
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
        <p>There are three main roles for clouds and convection:</p>
        <ol>
            <li>Heating of the atmosphere (through a deep layer).</li>
            <li>Reflection of solar radiation (contributing to albedo).</li>
            <li>Trapping of infrared radiation (contributing to the greenhouse effect).</li>
        </ol>
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
    if page == "6.1 Concept: Forcings, Aerosols, & Predictability":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.1: Signal and Noise</h3>
        <p>Climate model predictions for global warming respond to an applied forcing (like greenhouse gases) dictated by specific emissions scenarios. If the forcing occurs, the response <i>will</i> occur within a predictable range of uncertainty (often termed a <b>projection</b>).</p>
        <p>Natural variability, however, remains unpredictable at long lead times. It acts as "noise" over the forced "signal."</p>
        <p><b>Aerosols:</b> Unlike long-lived GHGs, particulate aerosols (like sulfates) have very <b>short residence times</b> (days to weeks). Globally, sulfate aerosols create a strong <b>net cooling tendency</b> by directly reflecting sunlight. This aerosol cooling significantly offsets a portion of current GHG warming, but long-lived greenhouse gases will heavily dominate future scenarios.</p>
        <br><br><br>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "6.2 Concept: Emissions Scenarios (SRES, RCPs, SSPs)":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.2: The Path Forward</h3>
        <p>Because future forcing depends entirely on human societal choices, scientists use coordinated scenarios. These have evolved over IPCC reports:</p>
        <ul>
            <li><b>CMIP3 / SRES (2007):</b> Grouped by economic and population development (e.g., A1FI = Fossil Intensive, A1T = Green Tech, B1 = Sustainable).</li>
            <li><b>CMIP5 / RCPs (2013):</b> Representative Concentration Pathways, named simply by their 2100 radiative forcing. <b>RCP 8.5</b> implies an extreme $8.5 W/m^2$ forcing by 2100. <b>RCP 2.6</b> represents aggressive mitigation.</li>
            <li><b>CMIP6 / SSPs (Current):</b> Shared Socioeconomic Pathways. These merge social choices with forcing. <b>SSP5-8.5</b> represents fossil-fueled development and high population. <b>SSP1-2.6</b> represents a sustainable shift. Note that some sustainable or "overshoot" scenarios (like SSP1-1.9 or SSP5-3.4-OS) actually require <i>net negative emissions</i> to function.</li>
        </ul>
        <br><br><br>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "6.3 Concept: Emissions vs. Concentrations & The Gap":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.3: Filling the Atmosphere</h3>
        <p>It is vital to understand the difference between emitting carbon and the total concentration sitting in the atmosphere. For a long-lived greenhouse gas:</p>
        <ul>
            <li><b>Increasing Emissions:</b> Concentration increases at an ever-faster rate.</li>
            <li><b>Constant Emissions:</b> Ongoing increase of concentration at a constant rate.</li>
            <li><b>Decreasing Emissions:</b> Concentration increases, but at a decreased rate.</li>
            <li><b>Very Low Emissions (Near Zero):</b> Concentration is capped and stabilization occurs.</li>
        </ul>
        <br><br><br>
        <p>If emissions are not brought down quickly enough, CO2 will overshoot the stabilization target. Fixing an overshoot requires <b>negative emissions</b> (actively removing CO2 from the sky).</p>
        <p><b>The Emissions Gap:</b> The UNEP Emissions Gap Report explicitly calculates the massive difference between current Nationally Determined Contributions (NDCs) and the actual deep reductions required to keep global average warming under 2°C.</p>
        <br><br><br>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "6.4 Concept: Global-Average Response & Ensembles":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.4: The Model Envelope</h3>
        <p>Dozens of global research groups (like NCAR, GFDL, GISS, MPI) run their complex climate models using the exact same forcing scenarios.</p>
        <p>Even with identical radiative forcing, global average warming differs slightly from model to model because each group simulates climate feedbacks (like clouds) differently. When plotted together, these models create an "envelope" or shaded spread of projections. The spread highlights the uncertainty caused by both differing model physics and natural interannual weather noise.</p>
        <br><br><br>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "6.5 Concept: Commitment & Long-Term Sea Level Rise":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.5: Unstoppable Momentum</h3>
        <p>What happens if we magically stop emissions right now?</p>
        <p><b>Constant Composition Commitment:</b> Simulations that instantly freeze radiative forcing at year 2000 (or 2100) levels prove that global warming is committed to continue. Temperatures will still slowly rise for decades.</p>
        <p>This commitment is most visible in <b>Sea Level Rise</b>. Sea levels are rising due to two distinct physical mechanisms:</p>
        <ol>
            <li><b>Land Ice Melt:</b> Massive glaciers and ice sheets situated on land (Greenland and Antarctica) melt and dump physically new water into the ocean basin.</li>
            <li><b>Thermal Expansion:</b> The mass of the ocean equals area $\\times \\rho \\times h$. If mass and area are constant, while density decreases by $\\delta \\rho$, depth $h$ must change by $\\delta h$. This gives Equation 3.16: $h \\delta \\rho = -\\rho \\delta h$. Using the coefficient of thermal expansion $\\epsilon_T$ (percent density decrease per °C of temperature increase, with $\\epsilon_T = 2.7 \\times 10^{-4} C^{-1}$ near 22°C), we get $\\delta \\rho = -\\rho \\epsilon_T \\delta T$. This leads to Equation 3.17: $\\frac{\\delta h}{h} = \\epsilon_T \\delta T$. For example, a 300m upper ocean layer warming 3°C yields: $\\delta h = 300 \\times 2.7 \\times 10^{-4} C^{-1} \\times 3C = 0.24m$.</li>
        </ol>
        <p>Because of thermal expansion and land-ice melt, sea levels will experience massive long-term increases, continuing an ongoing rise long after CO2 concentrations are completely stabilized.</p>
        <br><br><br>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "6.6 Model: Sea Level Dynamics":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: AOS102 Problem Set 2 - Sea Level Rise</h3>
        <p>Using the exact equations from your homework, we will calculate the thermal expansion of the ocean and the melting rate of the Greenland Ice Sheet.</p>
        <p><b>Thermal Expansion Formula:</b> $\\delta h / h_0 = \\epsilon_T \\delta T$</p>
        </div>
        """, unsafe_allow_html=True)
        
        delta_T = st.slider("Global Ocean Temperature Increase (ΔT in °C):", 0.0, 10.0, 4.0, 0.1)
        melt_rate_myr = st.slider("Greenland Surface Ice Melt Rate (m/yr):", 0.0, 5.0, 1.0, 0.1)
        
        if st.button("Calculate SLR Impacts", type="primary"):
            h0_upper = 300.0
            eps_upper = 2.7e-4
            dh_upper = h0_upper * eps_upper * delta_T
            
            h0_deep = 4000.0
            eps_deep = 1.5e-4
            dh_deep = h0_deep * eps_deep * delta_T
            
            area_greenland_m2 = 1.69e6 * 1e6
            active_area_m2 = 0.30 * area_greenland_m2
            vol_melt_m3_yr = melt_rate_myr * active_area_m2
            
            area_ocean_m2 = 3.6e8 * 1e6
            slr_m_yr = vol_melt_m3_yr / area_ocean_m2
            slr_cm_decade = (slr_m_yr * 100) * 10
            
            st.success(f"**Thermal Expansion Results for a {delta_T:.1f}°C Warming:**")
            st.write(f"**1. Upper Ocean ($h_0=300m$):** $\\delta h = 300 \\text{ m} \\times 2.7\\times 10^{-4} \\text{ °C}^{-1} \\times {delta_T} \\text{ °C} = $ **{dh_upper:.3f} meters**")
            st.write(f"**2. Deep Ocean ($h_0=4000m$):** $\\delta h = 4000 \\text{ m} \\times 1.5\\times 10^{-4} \\text{ °C}^{-1} \\times {delta_T} \\text{ °C} = $ **{dh_deep:.3f} meters**")
            st.write(f"**Total Thermal Expansion:** **{dh_upper + dh_deep:.3f} meters**")
            
            st.info(f"""
            **Greenland Ice Sheet Melt Physics (PbSet 2 Q3):**
            * Assuming a latent heat of fusion of $L_f = 3.3\\times10^5 \\text{ J/kg}$ and an ice density of roughly $900 \\text{ kg/m}^3$ ($0.9\\times 10^3 \\text{ kg/m}^3$).
            * If the surface melt rate is {melt_rate_myr} m/yr over 30% of Greenland's $1.69\\times10^6 \\text{ km}^2$ area, we add {vol_melt_m3_yr:.2e} $\\text{m}^3$ of water to the ocean each year.
            * Distributed across the World Ocean's $3.6\\times10^8 \\text{ km}^2$, this contributes **{slr_cm_decade:.3f} cm per decade** to global sea level rise!
            """)
            
        render_next_button(chapter, page)

    elif page == "6.7 Model: Constant Composition Commitment":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: The Physics of Lag</h3>
        <p>Let's simulate the "Constant Composition Commitment." We will steadily increase radiative forcing until the year 2050, then instantly freeze it. Watch how temperature and sea level rise respond.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code('''
import pandas as pd
import numpy as np

# Simulate years 2000 to 2200
years = np.arange(2000, 2201)

# Scenario: Radiative forcing steadily increases, then instantly stabilizes in 2050
forcing = np.where(years <= 2050, 2.0 + 0.05 * (years - 2000), 2.0 + 0.05 * 50)

# Temperature lags forcing heavily due to ocean heat capacity (simulated here with an e-folding lag)
temp = np.zeros(len(years))
temp[0] = 0.5
for i in range(1, len(years)):
    equilibrium_T = forcing[i] * 0.75  # 0.75 K per W/m2 sensitivity
    tau = 30.0  # 30-year response time
    temp[i] = temp[i-1] + (equilibrium_T - temp[i-1]) / tau

# Sea level rise from thermal expansion has a much longer, multi-century lag
slr = np.zeros(len(years))
for i in range(1, len(years)):
    slr[i] = slr[i-1] + temp[i] * 1.5

df = pd.DataFrame({
    'Radiative Forcing (W/m2)': forcing,
    'Surface Temp Anomaly (K)': temp,
    'Thermal Expansion SLR (mm)': slr
}, index=years)
        ''', language='python')
        
        if st.button("Run Code", type="primary", key="ccc_button"):
            st.markdown("### Output Analysis:")
            years = np.arange(2000, 2201)
            forcing = np.where(years <= 2050, 2.0 + 0.05 * (years - 2000), 2.0 + 0.05 * 50)
            
            temp = np.zeros(len(years))
            temp[0] = 0.5
            for i in range(1, len(years)):
                equilibrium_T = forcing[i] * 0.75
                tau = 30.0
                temp[i] = temp[i-1] + (equilibrium_T - temp[i-1]) / tau
                
            slr = np.zeros(len(years))
            for i in range(1, len(years)):
                slr[i] = slr[i-1] + temp[i] * 1.5
                
            df_temp = pd.DataFrame({'Radiative Forcing (W/m2)': forcing, 'Surface Temp Anomaly (K)': temp}, index=years)
            df_slr = pd.DataFrame({'Thermal Expansion SLR (mm)': slr}, index=years)
            
            st.line_chart(df_temp)
            st.line_chart(df_slr)
            
            st.info("""
            **Graph Analysis:**
            Notice the forcing (the blue line) flatlines perfectly at the year 2050. We stopped adding GHGs. 
            However, the surface temperature (red line) continues to aggressively climb for decades afterward, taking nearly 100 years to flatten out as the ocean slowly catches up to equilibrium. 
            More terrifying is the second graph: Sea Level Rise (thermal expansion) never stops rising in this 200-year window, driven by the immense thermal inertia of the deep ocean continuing to absorb heat.
            """)
            
        render_next_button(chapter, page)

    elif page == "6.8 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- FINAL EXAM ---
elif chapter == "Final Exam: Terminal Clearance":
    if page == "Final Knowledge Check":
        st.warning("WARNING: This is the final evaluation. Questions are pulled from all previous databanks.")
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=10)
    
