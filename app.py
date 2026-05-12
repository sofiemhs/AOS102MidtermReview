import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import copy

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Climate Science Terminal v4.1", page_icon="💻", layout="wide")

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
    
    [data-testid="stSidebar"] {
        background-color: #004d61; 
    }
    
    [data-testid="stSidebar"], [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #ffffff !important; 
    }
    
    [data-testid="stSidebar"] .stButton>button {
        background-color: #000000;
        color: #ffffff !important;
        border: 2px solid #ffffff;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #333333;
        color: #ffffff !important;
    }

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

# --- IMAGE HELPER WITH IDIOT-PROOF EXPLANATIONS ---
def display_image(image_name, caption, idiot_proof_explanation=""):
    try:
        st.image(image_name, caption=caption, use_container_width=True)
        if idiot_proof_explanation:
            st.info(f"💡 **Simple Breakdown:** {idiot_proof_explanation}")
    except:
        st.markdown(f"*(Please upload **{image_name}** to your repository to view the diagram: {caption})*")
        if idiot_proof_explanation:
            st.info(f"💡 **Simple Breakdown:** {idiot_proof_explanation}")

# ==========================================
# CURRICULUM DATA STRUCTURE (RESTORED FULL 6 CHAPTERS + IDIOT PROOFING)
# ==========================================

CURRICULUM = {
    "1. Overview of Climate Variability": {
        "pages": [
            "1.1 Concept: Correlation vs. Causation",
            "1.2 Concept: Weather, Climate, & Anomalies", 
            "1.3 Concept: Trace Gases & Warming", 
            "1.4 Concept: Model Hierarchy & Parameterization", 
            "1.5 Model: Smoothing Data",
            "1.6 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "How does the professor define 'climate quantities'?", "opts": ["As random chaotic boundaries.", "By averages or other statistics over the weather for some sufficiently long interval.", "There is no difference from weather."], "ans": "By averages or other statistics over the weather for some sufficiently long interval."},
            {"q": "What baseline is used for the Global Mean Surface Temperature anomalies in the notes?", "opts": ["1850-1900", "1961-1990 mean", "2000-2020 mean"], "ans": "1961-1990 mean"},
            {"q": "Which of the following is an anthropogenic source of Methane (CH4)?", "opts": ["Air conditioners.", "Cattle, sheep, rice paddies, and fossil fuel by-products.", "Only volcanoes."], "ans": "Cattle, sheep, rice paddies, and fossil fuel by-products."},
            {"q": "What is the parameterization problem?", "opts": ["Models are too fast.", "Representing average effects of scales smaller than the grid scale (e.g., clouds) as a function of the grid scale variables.", "The Earth's orbit is unpredictable."], "ans": "Representing average effects of scales smaller than the grid scale (e.g., clouds) as a function of the grid scale variables."},
            {"q": "When did Chlorofluorocarbons (CFCs) first appear in the atmosphere?", "opts": ["During the last ice age.", "They are man-made and were zero before 1950.", "1850."], "ans": "They are man-made and were zero before 1950."},
            {"q": "What do simple energy balance models illustrate?", "opts": ["The fundamental importance of energy balance to the climate state.", "Exactly when it will rain tomorrow.", "The exact location of El Nino."], "ans": "The fundamental importance of energy balance to the climate state."},
            {"q": "In the notes, what does 'ensemble' mean?", "opts": ["A group of scientists.", "Runs with different natural climate variability (climate model started with slightly different weather).", "A type of trace gas."], "ans": "Runs with different natural climate variability (climate model started with slightly different weather)."}
        ]
    },
    "2. Basics of Global Climate": {
        "pages": [
            "2.1 Concept: The Energy Budget", 
            "2.2 Concept: Blackbody & Radiative Forcing", 
            "2.3 Concept: The Carbon Cycle Breakdown",
            "2.4 Model: The Global Energy Balance",
            "2.5 Model: Carbon Accumulation",
            "2.6 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "In the global average energy budget, what is the exact Incoming Solar Radiation?", "opts": ["235 W/m²", "342 W/m²", "107 W/m²"], "ans": "342 W/m²"},
            {"q": "How much solar radiation is reflected back to space by clouds, aerosols, atmosphere, and surface combined?", "opts": ["168 W/m²", "107 W/m²", "40 W/m²"], "ans": "107 W/m²"},
            {"q": "What defines 'Radiative Forcing'?", "opts": ["Top-of-atmosphere initial imbalance in the energy budget due to change in GHG or aerosols.", "The physical push of wind on the ocean.", "The amount of rain falling in California."], "ans": "Top-of-atmosphere initial imbalance in the energy budget due to change in GHG or aerosols."},
            {"q": "What are the three roles for clouds and convection?", "opts": ["Heating the atmosphere, reflecting solar radiation, and trapping infrared radiation.", "Creating wind, destroying ozone, and melting ice.", "There are no roles."], "ans": "Heating the atmosphere, reflecting solar radiation, and trapping infrared radiation."},
            {"q": "According to the professor, what is the anthropogenic emission breakdown?", "opts": ["8 PgC/yr total (6.4 fossil fuels/cement + 1.6 land use change).", "100 PgC/yr from volcanoes.", "Zero emissions."], "ans": "8 PgC/yr total (6.4 fossil fuels/cement + 1.6 land use change)."},
            {"q": "How much of the anthropogenic carbon remains in the atmosphere?", "opts": ["100%", "Only ~half remains in the atmosphere (time dependent).", "None of it."], "ans": "Only ~half remains in the atmosphere (time dependent)."},
            {"q": "What happens if human greenhouse gas emissions remain perfectly constant over time?", "opts": ["Ongoing increase of concentration.", "Concentration decreases.", "Concentration stays perfectly flat."], "ans": "Ongoing increase of concentration."}
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
            "5.1 Concept: The Greenhouse Mechanism", 
            "5.2 Concept: Main Climate Feedbacks", 
            "5.3 Concept: Transient vs. Equilibrium Response", 
            "5.4 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "How does the greenhouse effect work?", "opts": ["It physically stops the wind.", "Upward IR from the surface is mostly trapped in the atmosphere, warming it, and emitting both upward and downward.", "It blocks incoming solar radiation."], "ans": "Upward IR from the surface is mostly trapped in the atmosphere, warming it, and emitting both upward and downward."},
            {"q": "What is the exact rate of the water vapor feedback?", "opts": ["Water vapor increases ~ 7% per 1°C warming, enhancing warming.", "It decreases by 5%.", "It has no effect."], "ans": "Water vapor increases ~ 7% per 1°C warming, enhancing warming."},
            {"q": "What happens in the snow/ice feedback?", "opts": ["Decreases in snow and ice decrease global albedo, enhancing warming.", "Ice reflects less sunlight.", "Snow cools the core of the Earth."], "ans": "Decreases in snow and ice decrease global albedo, enhancing warming."},
            {"q": "If cloud fraction decreases (for a given cloud type) relative to normal climate, what happens?", "opts": ["It gives the exact same tendency.", "It gives the opposite tendency.", "Clouds disappear forever."], "ans": "It gives the opposite tendency."},
            {"q": "Why does a 'Transient response experiment' show temperature lagging?", "opts": ["Because computers are slow.", "Ocean heat capacity slows this process. Temperature is less than equilibrium due to lag.", "Because the sun dims."], "ans": "Ocean heat capacity slows this process. Temperature is less than equilibrium due to lag."},
            {"q": "What is required if emissions are not brought down quickly enough and CO2 overshoots the target?", "opts": ["Negative emissions are required, i.e. methods for actively removing CO2.", "More aerosols.", "Nothing."], "ans": "Negative emissions are required, i.e. methods for actively removing CO2."}
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
        "pages": ["Midterm Protocol", "Final Knowledge Check"],
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
    
    # Cap required score to avoid crashing if pool is smaller than required
    req_score = min(required_score, len(pool))
    
    if quiz_key not in st.session_state:
        # Deepcopy to prevent random.shuffle from mutating the original database
        sampled_qs = copy.deepcopy(random.sample(pool, req_score))
        for q in sampled_qs:
            random.shuffle(q['opts'])  # Shuffle the options in place for this session
        st.session_state[quiz_key] = sampled_qs
    
    active_questions = st.session_state[quiz_key]
    
    st.markdown(f"### ⚠️ MISSION CLEARANCE: {chapter_name}")
    st.write(f"Pass mark: {req_score}/{req_score}. Questions and options are fully randomized.")
    
    with st.form(f"form_{chapter_name}"):
        user_answers = []
        for i, qa in enumerate(active_questions):
            st.write(f"**{i+1}. {qa['q']}**")
            ans = st.radio(f"q{i}", qa['opts'], key=f"ans_{chapter_name}_{i}", index=None, label_visibility="collapsed")
            user_answers.append(ans)
            st.write("---")
            
        if st.form_submit_button("Submit Analysis"):
            if None in user_answers:
                st.warning("⚠️ Error: Please select an answer for every question before submitting.")
            else:
                score = sum(1 for i, ans in enumerate(user_answers) if ans == active_questions[i]['ans'])
                
                if score == req_score:
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
                    st.error(f"ACCESS DENIED. Score: {score}/{req_score}. Review the logs and try again.")

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
        <p><b>Example:</b> The per capita consumption of mozzarella cheese correlates almost perfectly with the number of civil engineering doctorates awarded. This is a spurious correlation by chance, not a physical mechanism.</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** Just because two lines on a graph go up at the exact same time doesn't mean they are related. Sometimes it's just a total coincidence!")
        render_next_button(chapter, page)

    elif page == "1.2 Concept: Weather, Climate, & Anomalies":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.2: Weather vs. Climate</h3>
        <p>To begin analysis, we must firmly separate weather from climate. According to the midterm review:</p>
        <ul>
            <li><b>Climate Quantities:</b> Defined by averages or other statistics over the weather for some sufficiently long interval.</li>
            <li><b>Example:</b> A histogram of California precipitation (a given amount above or below a long-term average) taken over November-April of many different years to obtain climatological probabilities.</li>
            <li><b>Anomalies:</b> Departures relative to a specific baseline. In the global dataset provided, anomalies are relative to the <b>1961-1990 mean</b>.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        display_image("midterm_california_precip.png", "Histogram of California winter precipitation (1895-2014) - Seager et al., 2014", "Imagine a bar chart where the tallest bars are in the middle. This means 'normal' or 'average' rainfall happens most often. The short bars on the far left and right mean extreme droughts or extreme floods happen very rarely. This shows how climate is about the *probability* of certain weather happening.")
        render_next_button(chapter, page)

    elif page == "1.3 Concept: Trace Gases & Warming":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.3: Drivers of Variation & Trace Gases</h3>
        <p>Trace gases absorb infrared radiation at wavelengths where O2 and N2 are ineffective, altering the Earth's energy budget. The main drivers evaluated in the review include:</p>
        <ul>
            <li><b>Carbon Dioxide (CO2):</b> The main greenhouse gas responsible for observed warming since the industrial revolution.</li>
            <li><b>Methane (CH4):</b> Sourced from cattle, sheep, rice paddies, fossil fuel by-products, wetlands, and termites (measured in parts per billion).</li>
            <li><b>Nitrous Oxide (N2O):</b> Driven by biomass burning and fertilizers (ppb).</li>
            <li><b>Chlorofluorocarbons (CFCs):</b> Man-made chemicals that were exactly zero before 1950 (measured in parts per trillion).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        display_image("midterm_keeling_curve.png", "Carbon dioxide concentrations since 1958 at Mauna Loa", "This graph shows a red line zig-zagging upwards over time. The zig-zags are the Earth 'breathing' every year (plants growing in spring, dying in winter). But the steep upward ramp? That's human pollution adding more and more CO2 into the atmosphere non-stop.")
        display_image("midterm_trace_gases.png", "Concentration of various trace gases estimated since 1850", "You'll see lines that stay totally flat for a long time and then suddenly shoot straight up like a rocket around the year 1850. That rocket launch is the Industrial Revolution, proving these gases spiked exactly when humans started burning lots of fossil fuels.")
        render_next_button(chapter, page)

    elif page == "1.4 Concept: Model Hierarchy & Parameterization":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.4: The Parameterization Problem</h3>
        <p>Climate models use a hierarchy, from Simple Energy Balance Models to General Circulation Models. However, all grid-based models suffer from <b>The parameterization problem</b>.</p>
        <p>For each grid box in a climate model, only the average across the grid box of wind, temperature, etc., is represented. The average of smaller scale effects has important impacts on large-scale climate.</p>
        <p>For example, clouds primarily occur at small scales, yet the average amount of sunlight reflected by clouds affects the average solar heating of a whole grid box.</p>
        <p><b>Parameterization</b> is representing average effects of scales smaller than the grid scale (e.g., clouds) as a function of the grid scale variables (e.g. temperature and moisture) in a climate model.</p>
        </div>
        """, unsafe_allow_html=True)
        display_image("midterm_temp_anomaly.png", "Global mean surface temperatures estimated since preindustrial times", "This graph shows a line hovering around zero for a long time, and then climbing way up into the positive numbers on the right side. Zero is the 'normal' temperature. The line going up proves the Earth is getting undeniably hotter than it used to be.")
        render_next_button(chapter, page)

    elif page == "1.5 Model: Smoothing Data":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: AOS102 Problem Set 1B - Smoothing Global Temp Anomalies</h3>
        <p>Analyze global average surface temperature anomalies. Adjust the <b>moving average window</b> to separate natural internal variability (noise) from the long-term anthropogenic trend (signal).</p>
        </div>
        """, unsafe_allow_html=True)
        
        window_size = st.slider("Select Moving Average Length (Years):", min_value=5, max_value=80, value=40, step=1)
        
        if st.button("Run Smoothing Analysis", type="primary"):
            st.markdown("### Output Analysis:")
            years = np.arange(1850, 2026)
            np.random.seed(42)
            trend = 0.00008 * (years - 1850)**2 - 0.2  
            noise = np.random.normal(0, 0.15, len(years))
            raw_temp = trend + noise
            raw_temp[1877-1850] += 0.4
            raw_temp[1878-1850] += 0.4
            
            df = pd.DataFrame({'Raw Temp Anomaly': raw_temp}, index=years)
            df[f'{window_size}-Year Moving Average'] = df['Raw Temp Anomaly'].rolling(window=window_size, center=True).mean()
            
            st.line_chart(df)
            st.info("💡 **Simple Breakdown:** The chaotic, spiky line is exactly what weather feels like year-to-year: unpredictable. But when we mathematically smooth it out (the flat line), it reveals a hidden, steady ramp upward. That smooth ramp is the true global warming signal hiding beneath the noisy weather.")
            
            departures = df['Raw Temp Anomaly'] - df[f'{window_size}-Year Moving Average']
            std_dev = departures.std()
            
            st.markdown(f"**Departures from the {window_size}-Year Moving Average:**")
            
            dep_df = pd.DataFrame({'Departures': departures}, index=years)
            dep_df['+1 Std Dev'] = std_dev
            dep_df['-1 Std Dev'] = -std_dev
            dep_df['+2 Std Dev'] = 2 * std_dev
            dep_df['-2 Std Dev'] = -2 * std_dev
            
            st.line_chart(dep_df)
            
        render_next_button(chapter, page)

    elif page == "1.6 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 2 CONTENT ---
elif chapter == "2. Basics of Global Climate":
    if page == "2.1 Concept: The Energy Budget":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.1: Pathways of Energy Transfer</h3>
        <p>The Midterm review strictly defines the globally averaged energy budget. Memorize these pathways:</p>
        <ul>
            <li><b>Incoming Solar Radiation:</b> 342 W/m²</li>
            <li><b>Reflected Solar Radiation:</b> 107 W/m² total. (77 W/m² reflected by Clouds, Aerosols, and Atmosphere; 30 W/m² reflected by the Surface).</li>
            <li><b>Absorbed by Surface:</b> 168 W/m²</li>
            <li><b>Outgoing Longwave Radiation:</b> 235 W/m² (195 emitted by atm, 40 atmospheric window)</li>
            <li><b>Back Radiation (Absorbed by Surface):</b> 324 W/m²</li>
            <li><b>Surface Radiation Emitted:</b> 390 W/m²</li>
            <li><b>Latent Heat:</b> 78 W/m²</li>
            <li><b>Thermals:</b> 24 W/m²</li>
        </ul>
        <p>The upward IR from the surface is mostly trapped in the atmosphere, rather than escaping directly to space, so it tends to heat the atmosphere. The atmosphere emits both upward and downward, returning energy back down to the surface, resulting in additional warming (The Greenhouse Effect).</p>
        </div>
        """, unsafe_allow_html=True)
        display_image("midterm_energy_budget.png", "Pathways of energy transfer in a global average", "Think of this like a bank account for the Earth. The sun deposits 342 units of energy. The Earth immediately bounces 107 units away (like a mirror). The remaining energy is absorbed and moves around. To stop from melting, the Earth eventually has to 'pay back' the rest to space as invisible heat (infrared). The fat arrows show how much heat gets trapped by our atmosphere before it finally escapes.")
        render_next_button(chapter, page)

    elif page == "2.2 Concept: Blackbody & Radiative Forcing":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.2: Radiative Forcing Imbalance</h3>
        <p><b>Blackbody Radiation:</b> Total energy flux integrated across all wavelengths of light heavily dictates the Earth's temperature.</p>
        <p><b>Radiative Forcing:</b> The midterm review defines this as the "Top-of-atmosphere initial imbalance in the energy budget due to: change in GHG (trapping infrared radiation) &/or aerosols (reflecting solar radiation)".</p>
        <p>Anthropogenic aerosols reflect more sunlight, generating a forcing that tends to reduce the incoming 107 W/m² baseline. GHGs trap IR, dropping the outgoing radiation below 235 W/m² <i>before</i> the temperature increases. To reach equilibrium, temperature increases until top of atmosphere IR again balances net solar.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.3 Concept: The Carbon Cycle Breakdown":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.3: The Carbon Cycle (PgC)</h3>
        <p>Based on the midterm review data (based on 1990s averages), the anthropogenic carbon flux is strictly broken down as follows:</p>
        <ul>
            <li><b>Anthropogenic emissions:</b> ~8 PgC/yr total.</li>
            <li>This is divided into <b>6.4 PgC/yr</b> from fossil fuels + cement, and <b>1.6 PgC/yr</b> from land use change.</li>
            <li>Fortunately, only ~ half remains in the atmosphere (time dependent).</li>
            <li>Increased atmospheric concentrations yield <b>2.2 PgC/yr</b> increased flux into the ocean.</li>
            <li>An additional <b>2.5 PgC/yr</b> is taken up by land vegetation (e.g., forest regrowth).</li>
        </ul>
        <p>For a long-lived greenhouse gas: Increasing emissions $\\Rightarrow$ concentration increases at ever faster rate; Constant emissions $\\Rightarrow$ ongoing increase of concentration.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.4 Model: The Global Energy Balance":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: Visualizing the W/m² Data</h3>
        <p>Press run to mathematically verify the Top-Of-Atmosphere and Surface balance using the midterm's exact numbers.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Calculate Balance", type="primary"):
            st.write("**Top of Atmosphere Balance:**")
            st.write("Incoming Solar (342) = Reflected Solar (107) + Outgoing Longwave (235)")
            st.success(f"{342} = {107 + 235}")
            
            st.write("**Surface Balance:**")
            st.write("Absorbed Solar (168) + Back Radiation (324) = Sfc Radiation (390) + Thermals (24) + Latent Heat (78)")
            st.success(f"{168 + 324} = {390 + 24 + 78}")
        render_next_button(chapter, page)

    elif page == "2.5 Model: Carbon Accumulation":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: AOS102 Problem Set 2 - Carbon Scenarios</h3>
        <p>This interactive model integrates global CO2 emissions into atmospheric concentrations from 2024 to 2050.</p>
        </div>
        """, unsafe_allow_html=True)
        
        frac_remain = st.slider("Fraction of Emissions Remaining in Atmosphere (Default 0.50):", 0.10, 1.00, 0.50, 0.01)
        
        if st.button("Simulate Scenarios", type="primary"):
            years = np.arange(2024, 2051)
            emissions_A = 39.6 + 0.52 * (years - 2024)
            emissions_D = np.where(years <= 2030, 39.6 - 39.6 * (years - 2024) / (2030 - 2024), 0.0)
            
            def calc_concentration(emissions_array):
                conc = np.zeros(len(years))
                conc[0] = 424.6  
                for i in range(1, len(years)):
                    conc[i] = conc[i-1] + frac_remain * (emissions_array[i] / 7.8)
                return conc
                
            conc_A = calc_concentration(emissions_A)
            conc_D = calc_concentration(emissions_D)
            
            df_conc = pd.DataFrame({
                'Scenario A (Historical Growth)': conc_A,
                'Scenario D (Zero by 2030)': conc_D
            }, index=years)
            
            st.line_chart(df_conc)
            st.info("💡 **Simple Breakdown:** Even if we cap our pollution so it stops growing (Scenario D), the amount of CO2 sitting in the sky STILL goes up for a while before flattening out. Scenario A shows what happens if we keep polluting more every year: the CO2 piles up faster and faster, curving straight into the danger zone.")
            
        render_next_button(chapter, page)

    elif page == "2.6 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 3 CONTENT ---
elif chapter == "3. Physical Processes":
    if page == "3.1 Concept: Momentum & Forces":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.1: Conservation of Momentum</h3>
        <p>To simulate the climate, models rely on Newton's second law ($ma=F$). For the atmosphere and ocean, this is evaluated as acceleration (rate of change of velocity) equaling the sum of forces per unit mass:</p>
        <p>$$ \text{Velocity Change} = \text{Coriolis} + \text{PGF} + \text{Gravity} + \text{Friction} $$</p>
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
            💡 **Simple Breakdown:** This compares two invisible bubbles of air rising into the sky. The 'Dry' bubble gets freezing cold very fast. But the 'Moist' bubble (full of water vapor) cools down much slower. Why? Because as the water turns into cloud droplets, it acts like a tiny heater, keeping the air around it warm!
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
        <p>In the vertical average, the eastward pressure gradient force in the ocean perfectly balances the westward wind stress. Meanwhile, on the equator in the east, the wind stress and Coriolis force cause surface water to diverge, forcing shallow, cold, nutrient-rich water to upwell to the surface.</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** Normally, the wind acts like a giant leaf-blower, pushing all the warm surface water over to Asia. This leaves South America with freezing cold water pulling up from the deep.")
        render_next_button(chapter, page)

    elif page == "4.2 Concept: El Niño & La Niña Extremes":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.2: The Extreme Phases</h3>
        <p><b>El Niño (Warm Phase):</b> Warmer SST in the east; rainfall tends to spread east. The Trade Winds weaken. The unbalanced eastward Pressure Gradient Force (PGF) in the ocean causes anomalous currents in the vertical average through the layer above the thermocline. The thermocline deepens in the east. Upwelling on the equator in the east Pacific brings up water that is less cold than normal.</p>
        <p><b>La Niña (Cold Phase):</b> Cooler SST in the east; rainfall concentrated in the west. Trade Winds strengthen. The westward wind stress exceeds the eastward PGF in the ocean, creating anomalous currents along the Equator. The thermocline shallows in the east. Upwelling on the equator in the east Pacific brings up water colder than normal.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "4.3 Concept: Feedbacks & Oscillators":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.3: The Engines of ENSO</h3>
        <p><b>The Bjerknes Feedback (The Amplifier):</b> First hypothesized by Jakob Bjerknes in 1969, this is a positive, self-reinforcing loop. Weak winds lead to warmer East Pacific SSTs. This reduces the east-west temperature contrast, which is the very cause of the Walker circulation. A reduced temperature gradient causes the winds to weaken <i>even more</i>, driving further warming.</p>
        <p><b>The Delayed Oscillator (The Kill Switch):</b> Why doesn't an ENSO phase last forever? The transition is governed by slow ocean dynamics. Subsurface anomalies in the western Pacific (especially off the equator) evolve slowly and create a delayed effect.</p>
        <p>Deep thermocline anomalies extend eastward as <i>Kelvin waves</i>. Meanwhile, shallow thermocline anomalies extend westward as <i>Rossby waves</i>. When these Rossby waves hit the western boundary of the Pacific, they can no longer travel west. They reflect back eastward, eventually returning across the equator to the Eastern Pacific to violently pull the thermocline back up, ending the El Niño.</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** Think of sloshing water in a bathtub. When the wind stops, the warm water sloshes back across the ocean. But it hits the wall, bounces, and eventually sloshes back the other way, resetting everything. It can't stay warm forever.")
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
        <p><b>Ensemble Forecasting:</b> To communicate uncertainty, scientists run coupled models starting from slightly different initial ocean conditions. This "ensemble spread" provides an estimate of uncertainty, while the ensemble mean gives the best overall estimate.</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** Since weather is basically random, scientists run the same simulation 50 times with slightly different starting weather. It creates a 'spaghetti' of lines. If most lines go up, we can be confident an El Niño is coming, even if we don't know the exact temperature.")
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
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** When the Pacific Ocean gets super warm during El Niño, it acts like a giant boulder dropped in a fast-flowing river. It forces the atmospheric jet stream to bend and wobble around it, entirely changing where rain and snow fall in North America.")
        render_next_button(chapter, page)

    elif page == "4.6 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 5 CONTENT ---
elif chapter == "5. Greenhouse Effect & Feedbacks":
    if page == "5.1 Concept: The Greenhouse Mechanism":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.1: The Three Roles of Clouds</h3>
        <p>According to the midterm review, there are three roles for clouds and convection:</p>
        <ol>
            <li>Heating of the atmosphere (through a deep layer)</li>
            <li>Reflection of solar radiation (contributing to albedo)</li>
            <li>Trapping of infrared radiation (contributing to the greenhouse effect)</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** Low, thick clouds act like a white t-shirt on a hot day, reflecting sunlight and cooling the Earth. High, thin clouds act like a blanket trapping your body heat at night, keeping the Earth warm.")
        render_next_button(chapter, page)

    elif page == "5.2 Concept: Main Climate Feedbacks":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.2: The Amplifiers</h3>
        <p>Climate feedbacks modify changes due to basic greenhouse effect, amplifying warming and adding to the range of warming estimated for a given amount of GHG.</p>
        <p><b>Main Feedbacks:</b></p>
        <ul>
            <li><b>Water Vapor Feedback:</b> Water vapor increases ~ 7% per 1°C warming, and water vapor is a GHG so enhances warming.</li>
            <li><b>Snow/Ice Feedback:</b> Decreases in snow and ice $\\Rightarrow$ global albedo decreases (less solar radiation reflected) $\\Rightarrow$ enhances warming.</li>
            <li><b>Cloud Feedbacks:</b> Due to changes in cloud cover, which affect both cloud contribution to the greenhouse effect and to albedo. If cloud fraction decreases (for given cloud type) relative to normal climate, it gives the opposite tendency.</li>
        </ul>
        <p>Ensemble runs with different natural climate variability (climate model started, e.g., with slightly different weather) show the spread of these feedback uncertainties.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "5.3 Concept: Transient vs. Equilibrium Response":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.3: Ocean Heat Lag</h3>
        <p>In a transient response experiment where greenhouse gas concentrations are capped, the forcing stabilizes.</p>
        <p>However, temperature was less than equilibrium due to lag, so it continues to rise for ~decades (upper ocean), plus an additional increase on deep ocean timescales. This is known as the constant composition commitment.</p>
        <p>If emissions are not brought down quickly enough, CO2 overshoots stabilization target $\\Rightarrow$ negative emissions are required, i.e. methods for actively removing CO2.</p>
        </div>
        """, unsafe_allow_html=True)
        display_image("midterm_transient_lag.png", "Annual average surface air temp response, Manabe et al 1991", "If you slam on the brakes of a speeding train, it still slides forward before stopping. This graph shows the same thing for climate. Even if we completely cap greenhouse gases, the temperature line keeps rising for decades. Why? Because the oceans are gigantic and take a very long time to finish heating up.")
        render_next_button(chapter, page)

    elif page == "5.4 Knowledge Check":
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
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** Pollution isn't just invisible gas. Smog and ash (aerosols) act like millions of tiny mirrors in the sky, bouncing sunlight away and actually *cooling* the planet temporarily, masking how bad global warming really is.")
        render_next_button(chapter, page)

    elif page == "6.2 Concept: Emissions Scenarios (SRES, RCPs, SSPs)":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.2: The Path Forward</h3>
        <p>Because future forcing depends entirely on human societal choices, scientists use coordinated scenarios. These have evolved over IPCC reports:</p>
        <ul>
            <li><b>CMIP3 / SRES (2007):</b> Grouped by economic and population development (e.g., A1FI = Fossil Intensive, A1T = Green Tech, B1 = Sustainable).</li>
            <li><b>CMIP5 / RCPs (2013):</b> Representative Concentration Pathways, named simply by their 2100 radiative forcing. <b>RCP 8.5</b> implies an extreme 8.5 W/m² forcing by 2100. <b>RCP 2.6</b> represents aggressive mitigation.</li>
            <li><b>CMIP6 / SSPs (Current):</b> Shared Socioeconomic Pathways. These merge social choices with forcing. <b>SSP5-8.5</b> represents fossil-fueled development and high population. <b>SSP1-2.6</b> represents a sustainable shift. Note that some sustainable or "overshoot" scenarios (like SSP1-1.9 or SSP5-3.4-OS) actually require <i>net negative emissions</i> to function.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** We don't have a crystal ball for human behavior. So scientists make 'choose your own adventure' paths. SSP5 is the 'burn all the coal' path. SSP1 is the 'switch to solar panels' path.")
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
        <p>If emissions are not brought down quickly enough, CO2 will overshoot the stabilization target. Fixing an overshoot requires <b>negative emissions</b> (actively removing CO2 from the sky).</p>
        <p><b>The Emissions Gap:</b> The UNEP Emissions Gap Report explicitly calculates the massive difference between current Nationally Determined Contributions (NDCs) and the actual deep reductions required to keep global average warming under 2°C.</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 **Simple Breakdown:** Think of the atmosphere as a bathtub and emissions as the faucet. Even if you stop turning the faucet *up* and just leave it running steadily, the bathtub still keeps filling up. To stop the water from rising, you have to turn the faucet almost completely off.")
        render_next_button(chapter, page)

    elif page == "6.4 Concept: Global-Average Response & Ensembles":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 6.4: The Model Envelope</h3>
        <p>Dozens of global research groups (like NCAR, GFDL, GISS, MPI) run their complex climate models using the exact same forcing scenarios.</p>
        <p>Even with identical radiative forcing, global average warming differs slightly from model to model because each group simulates climate feedbacks (like clouds) differently. When plotted together, these models create an "envelope" or shaded spread of projections. The spread highlights the uncertainty caused by both differing model physics and natural interannual weather noise.</p>
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
            <li><b>Thermal Expansion:</b> The mass of the ocean equals area $\\times \\rho \\times h$. If mass and area are constant, while density decreases by $\\delta \\rho$, depth $h$ must change by $\\delta h$. This gives Equation 3.16: $h \\delta \\rho = -\\rho \\delta h$. Using the coefficient of thermal expansion $\\epsilon_T$ (percent density decrease per °C of temperature increase, with $\\epsilon_T = 2.7 \\times 10^{-4} C^{-1}$ near 22°C), we get $\\delta \\rho = -\\rho \\epsilon_T \\delta T$. This leads to Equation 3.17: $\\frac{\\delta h}{h} = \\epsilon_T \\delta T$.</li>
        </ol>
        <p>Because of thermal expansion and land-ice melt, sea levels will experience massive long-term increases, continuing an ongoing rise long after CO2 concentrations are completely stabilized.</p>
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
            st.write(f"**1. Upper Ocean ($h_0=300m$):** $\\delta h = 300 \\text{{ m}} \\times 2.7\\times 10^{{-4}} \\text{{ °C}}^{{-1}} \\times {delta_T} \\text{{ °C}} = $ **{dh_upper:.3f} meters**")
            st.write(f"**2. Deep Ocean ($h_0=4000m$):** $\\delta h = 4000 \\text{{ m}} \\times 1.5\\times 10^{{-4}} \\text{{ °C}}^{{-1}} \\times {delta_T} \\text{{ °C}} = $ **{dh_deep:.3f} meters**")
            st.write(f"**Total Thermal Expansion:** **{dh_upper + dh_deep:.3f} meters**")
            
            st.info(f"""
            💡 **Simple Breakdown (Greenland Ice Sheet Melt Physics):**
            * If the surface melt rate is {melt_rate_myr} m/yr over 30% of Greenland's $1.69\\times10^6 \\text{{ km}}^2$ area, we add {vol_melt_m3_yr:.2e} $\\text{{m}}^3$ of water to the ocean each year.
            * Distributed across the World Ocean's $3.6\\times10^8 \\text{{ km}}^2$, this contributes **{slr_cm_decade:.3f} cm per decade** to global sea level rise! Water swells when it warms, and melting land ice adds literal new water to the tub.
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
            💡 **Simple Breakdown:** Notice the forcing (the blue line) flatlines perfectly at the year 2050. We stopped adding GHGs. 
            However, the surface temperature (red line) continues to aggressively climb for decades afterward, taking nearly 100 years to flatten out as the ocean slowly catches up to equilibrium. 
            More terrifying is the second graph: Sea Level Rise (thermal expansion) never stops rising in this 200-year window, driven by the immense thermal inertia of the deep ocean continuing to absorb heat.
            """)
            
        render_next_button(chapter, page)

    elif page == "6.8 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- FINAL EXAM ---
elif chapter == "Final Exam: Terminal Clearance":
    if page == "Midterm Protocol":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry: Midterm Protocol (Aids Permitted)</h3>
        <p><b>WARNING:</b> Security override protocol logged by the Professor.</p>
        <p>Aids permitted for your exam:</p>
        <ul>
            <li>One 8.5"x11" sheet of paper, double-sided (=2 pgs of notes) of your notes.</li>
            <li>Your name must be on each side, to be handed in with the midterm.</li>
            <li>The notes pages can include figures and clips from lecture slides but should be organized by each student individually.</li>
            <li>Part of each page (at least 10%) should be in your handwriting.</li>
        </ul>
        <p>Good luck.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "Final Knowledge Check":
        st.warning("WARNING: This is the final evaluation. Questions are pulled from all previous databanks.")
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=10)
