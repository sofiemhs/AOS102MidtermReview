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
            "1.1 Concept: Pillars of Variability", 
            "1.2 Concept: Trusting Projections", 
            "1.3 Concept: Model Hierarchy", 
            "1.4 Model: Smoothing Data",
            "1.5 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "What type of variability is El Niño considered?", "opts": ["Natural External", "Anthropogenic", "Internal Variability"], "ans": "Internal Variability"},
            {"q": "If a volcano erupts and cools the Earth, what kind of forcing is this?", "opts": ["Internal", "Natural External", "Anthropogenic"], "ans": "Natural External"},
            {"q": "What defines 'climate' as opposed to 'weather'?", "opts": ["Weather is a boundary value problem, climate is chaotic.", "Climate is the statistical average of weather over long periods.", "There is no difference."], "ans": "Climate is the statistical average of weather over long periods."},
            {"q": "What is Anthropogenic Forcing?", "opts": ["Human-caused changes like greenhouse gas emissions.", "Volcanic activity.", "Orbital wobbles."], "ans": "Human-caused changes like greenhouse gas emissions."},
            {"q": "Why is weather prediction limited to a few weeks?", "opts": ["Because it is a boundary value problem.", "Because of chaos and small errors in initial data growing rapidly.", "Because satellites cannot see through clouds."], "ans": "Because of chaos and small errors in initial data growing rapidly."},
            {"q": "Which model treats the Earth as a single point?", "opts": ["GCMs", "Energy Balance Models (EBMs)", "Intermediate Models"], "ans": "Energy Balance Models (EBMs)"},
            {"q": "What do General Circulation Models (GCMs) do?", "opts": ["Divide the world into a 3D grid to simulate complex interactions.", "Only predict ENSO.", "Ignore the oceans entirely."], "ans": "Divide the world into a 3D grid to simulate complex interactions."},
            {"q": "Is the Earth's orbit (Milankovitch cycles) considered an internal or external forcing?", "opts": ["Internal", "External", "Neither"], "ans": "External"},
            {"q": "If you add more energy (CO2) to the system, why can we predict it will warm?", "opts": ["Because it is chaotic.", "Because climate is a boundary value problem striving for energy balance.", "Because weather models say so."], "ans": "Because climate is a boundary value problem striving for energy balance."},
            {"q": "What does a 10-year moving average accomplish?", "opts": ["It predicts the weather next week.", "It smooths out high-frequency noise to reveal long-term signals.", "It cools the dataset down."], "ans": "It smooths out high-frequency noise to reveal long-term signals."}
        ]
    },
    "2. Basics of Global Climate": {
        "pages": [
            "2.1 Concept: Blackbody Radiation", 
            "2.2 Concept: Solar Constant & Albedo", 
            "2.3 Concept: Atmospheric Structure", 
            "2.4 Concept: Carbon Reservoirs",
            "2.5 Model: Blackbody Energy Output",
            "2.6 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "According to the Stefan-Boltzmann Law, energy emitted is proportional to:", "opts": ["Temperature squared", "Temperature cubed", "Temperature to the fourth power"], "ans": "Temperature to the fourth power"},
            {"q": "If you double the temperature of a blackbody, its energy output increases by:", "opts": ["2 times", "4 times", "16 times"], "ans": "16 times"},
            {"q": "What is Albedo?", "opts": ["The fraction of light absorbed.", "The fraction of light reflected.", "The speed of light in water."], "ans": "The fraction of light reflected."},
            {"q": "What happens if Earth's albedo increases?", "opts": ["The Earth cools.", "The Earth warms.", "Nothing happens."], "ans": "The Earth cools."},
            {"q": "Why does the Stratosphere warm with height?", "opts": ["Because it is closer to the sun.", "Because the ozone layer absorbs UV radiation.", "Because clouds trap heat there."], "ans": "Because the ozone layer absorbs UV radiation."},
            {"q": "In which atmospheric layer does weather primarily occur?", "opts": ["Mesosphere", "Stratosphere", "Troposphere"], "ans": "Troposphere"},
            {"q": "Which carbon reservoir holds the most carbon?", "opts": ["The Atmosphere", "The Deep Ocean", "Fossil Reserves"], "ans": "The Deep Ocean"},
            {"q": "Which carbon reservoir is the smallest but most sensitive 'control knob'?", "opts": ["The Atmosphere", "The Deep Ocean", "The Biosphere"], "ans": "The Atmosphere"},
            {"q": "What is the approximate average incoming energy at the top of the atmosphere?", "opts": ["1367 W/m2", "342 W/m2", "0 W/m2"], "ans": "342 W/m2"},
            {"q": "What constitutes 'Fossil Reserves'?", "opts": ["Carbon in living trees.", "Carbon locked away for millions of years.", "Carbon dissolving in the ocean today."], "ans": "Carbon locked away for millions of years."}
        ]
    },
    "3. Physical Processes": {
        "pages": [
            "3.1 Concept: Equation of State", 
            "3.2 Concept: Geostrophic Balance", 
            "3.3 Concept: Friction's Role", 
            "3.4 Concept: Rossby Waves", 
            "3.5 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "What variables are connected in the Equation of State for the atmosphere?", "opts": ["Pressure, Density, and Temperature", "Wind speed, Humidity, and Albedo", "Gravity, Mass, and Volume"], "ans": "Pressure, Density, and Temperature"},
            {"q": "In the ocean, what additional variable strongly affects density?", "opts": ["Oxygen", "Salinity", "Light penetration"], "ans": "Salinity"},
            {"q": "Geostrophic balance occurs when the Pressure Gradient Force is balanced by:", "opts": ["Friction", "Gravity", "The Coriolis Force"], "ans": "The Coriolis Force"},
            {"q": "Because of Geostrophic Balance, how does wind flow in the upper atmosphere?", "opts": ["Straight into low pressure.", "Around high and low-pressure systems.", "Directly north to south."], "ans": "Around high and low-pressure systems."},
            {"q": "What does friction do to wind near the Earth's surface?", "opts": ["Speeds it up.", "Slows it down and weakens the Coriolis Force.", "Causes it to rise straight up."], "ans": "Slows it down and weakens the Coriolis Force."},
            {"q": "When friction weakens the Coriolis force, what happens to the wind?", "opts": ["It stops entirely.", "It crosses isobars and spirals inward toward low pressure.", "It flows perfectly straight."], "ans": "It crosses isobars and spirals inward toward low pressure."},
            {"q": "What are Rossby Waves?", "opts": ["Giant meanders in the jet stream.", "Ocean waves crashing on the shore.", "Sound waves in the stratosphere."], "ans": "Giant meanders in the jet stream."},
            {"q": "How can a warm patch in the Pacific cause a cold snap in New York?", "opts": ["Through groundwater transfer.", "Through teleconnections driven by Rossby Waves.", "It is pure coincidence."], "ans": "Through teleconnections driven by Rossby Waves."},
            {"q": "If density increases while temperature stays constant, what happens to pressure?", "opts": ["It decreases.", "It increases.", "It remains the same."], "ans": "It increases."},
            {"q": "The Coriolis force pulls air to the side because of:", "opts": ["The moon's gravity.", "Earth's rotation.", "Magnetic fields."], "ans": "Earth's rotation."}
        ]
    },
    "4. El Niño (ENSO)": {
        "pages": [
            "4.1 Concept: Normal State", 
            "4.2 Concept: El Niño Warm Phase", 
            "4.3 Concept: Feedbacks & Oscillators", 
            "4.4 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "During the Normal State (Walker Circulation), which way do trade winds blow?", "opts": ["East to West", "West to East", "North to South"], "ans": "East to West"},
            {"q": "Where does the 'Warm Pool' normally sit?", "opts": ["Off the coast of South America", "In the Western Pacific (Indonesia)", "In the Atlantic"], "ans": "In the Western Pacific (Indonesia)"},
            {"q": "What happens to the trade winds during El Niño?", "opts": ["They get much stronger.", "They collapse or reverse.", "They blow vertically."], "ans": "They collapse or reverse."},
            {"q": "What happens to the thermocline during El Niño?", "opts": ["It becomes extremely steep.", "It flattens out across the Pacific.", "It disappears completely."], "ans": "It flattens out across the Pacific."},
            {"q": "What is the Bjerknes Feedback?", "opts": ["A self-reinforcing loop where weak winds lead to warmer East Pacific waters.", "A negative feedback that stops El Niño.", "The process of ice melting."], "ans": "A self-reinforcing loop where weak winds lead to warmer East Pacific waters."},
            {"q": "How does the 'Delayed Oscillator' end El Niño?", "opts": ["Rossby waves hit the West coast, reflect as Kelvin waves, and bring the thermocline back up.", "The sun cools down temporarily.", "Heavy rains cool the ocean surface directly."], "ans": "Rossby waves hit the West coast, reflect as Kelvin waves, and bring the thermocline back up."},
            {"q": "Where does deep, cold water upwell during normal conditions?", "opts": ["In the West Pacific.", "In the East Pacific (South America).", "In the Indian Ocean."], "ans": "In the East Pacific (South America)."},
            {"q": "El Niño is known as the:", "opts": ["Cold Phase", "Neutral Phase", "Warm Phase"], "ans": "Warm Phase"},
            {"q": "What is the thermocline?", "opts": ["The boundary between warm surface water and cold deep water.", "The boundary between the troposphere and stratosphere.", "A type of ocean current."], "ans": "The boundary between warm surface water and cold deep water."},
            {"q": "During El Niño, the 'Warm Pool' sloshes toward:", "opts": ["The West", "The East", "The North Pole"], "ans": "The East"}
        ]
    },
    "5. Greenhouse Effect & Feedbacks": {
        "pages": [
            "5.1 Concept: Selective Absorption", 
            "5.2 Concept: Detailed Feedbacks", 
            "5.3 Knowledge Check"
        ],
        "quiz_pool": [
            {"q": "What is 'Selective Absorption' in the context of the atmosphere?", "opts": ["The atmosphere blocks all sunlight.", "The atmosphere is transparent to shortwave but opaque to longwave radiation.", "The atmosphere absorbs all radiation equally."], "ans": "The atmosphere is transparent to shortwave but opaque to longwave radiation."},
            {"q": "Which type of radiation is emitted by the Sun?", "opts": ["Shortwave", "Longwave (Infrared)", "Microwave"], "ans": "Shortwave"},
            {"q": "Which type of radiation is trapped by Greenhouse Gases?", "opts": ["Shortwave", "Longwave (Infrared)", "Gamma rays"], "ans": "Longwave (Infrared)"},
            {"q": "The Water Vapor feedback is considered:", "opts": ["A negative feedback.", "A positive feedback.", "A neutral feedback."], "ans": "A positive feedback."},
            {"q": "Why is the Water Vapor feedback positive?", "opts": ["Warming causes more evaporation, leading to more water vapor (a GHG), causing more warming.", "Water vapor cools the Earth.", "It creates clouds that always reflect light."], "ans": "Warming causes more evaporation, leading to more water vapor (a GHG), causing more warming."},
            {"q": "What is the Lapse Rate feedback in the tropics?", "opts": ["Positive", "Negative", "Neutral"], "ans": "Negative"},
            {"q": "Why is the Lapse Rate feedback negative?", "opts": ["The upper atmosphere warms faster, radiating heat away more efficiently to space.", "The surface cools down too fast.", "Ozone blocks the heat."], "ans": "The upper atmosphere warms faster, radiating heat away more efficiently to space."},
            {"q": "Which feedback is considered 'The Wildcard'?", "opts": ["Water vapor", "Cloud feedback", "Ice-albedo"], "ans": "Cloud feedback"},
            {"q": "What is the general effect of Low clouds?", "opts": ["They trap heat (Warming).", "They reflect sunlight (Cooling).", "They do nothing."], "ans": "They reflect sunlight (Cooling)."},
            {"q": "What is the general effect of High clouds?", "opts": ["They reflect sunlight (Cooling).", "They trap heat (Warming).", "They freeze the upper atmosphere."], "ans": "They trap heat (Warming)."}
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
    if page == "1.1 Concept: Pillars of Variability":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.1: The Three Pillars</h3>
        <p>Climate variability is driven by three distinct mechanisms. Understanding which one is acting upon the data is the first step of analysis.</p>
        <ul>
            <li><b>Internal Variability:</b> Natural "wobbles" within the climate system itself. These move heat around (like El Niño or the North Atlantic Oscillation) but do not add new energy to the entire globe.</li>
            <li><b>External Forcing (Natural):</b> Factors outside the immediate atmosphere/ocean system. This includes volcanic eruptions (which block sunlight) or Milankovitch cycles (changes in Earth's orbit modifying solar input).</li>
            <li><b>External Forcing (Anthropogenic):</b> Human-driven changes, primarily the emission of greenhouse gases and aerosols into the atmosphere.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.2 Concept: Trusting Projections":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.2: Weather vs. Climate Prediction</h3>
        <p>A common fallacy is asking: <i>"If we can't predict the weather next week, how can we predict the climate in 50 years?"</i></p>
        <p><b>Weather is Chaos:</b> Weather is an initial value problem. Small errors in our starting data (a missing temperature reading over the ocean) grow exponentially over a few days, destroying our ability to predict exactly where a storm will be. </p>
        <p><b>Climate is a Boundary Value Problem:</b> We aren't predicting individual storms. We are predicting the statistical average. If you add a massive amount of new energy to a closed system (via CO2 trapping heat), the system <i>must</i> warm up to reach a new equilibrium. Energy must balance.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.3 Concept: Model Hierarchy":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.3: The Tools of the Trade</h3>
        <p>Scientists don't just use one giant computer program. They use a hierarchy of models:</p>
        <ul>
            <li><b>Energy Balance Models (EBMs):</b> The simplest math. They treat the entire Earth as a single 0-dimensional point to calculate basic temperature physics (Energy In = Energy Out).</li>
            <li><b>Intermediate Models:</b> Focus on specific regional phenomena, like predicting an El Niño event, using simplified physics to save computing power.</li>
            <li><b>General Circulation Models (GCMs):</b> The heavy lifters. These divide the entire globe into a massive 3D grid, simulating fluid dynamics, wind, ocean currents, and even biological processes. </li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.4 Model: Smoothing Data":
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
            * **Raw Temp (Noise):** Notice how violently this line spikes up and down. This represents internal climate variability. If you only looked at a 3-year chunk, you might falsely conclude the planet was rapidly cooling.
            * **Smoothed Trend (Signal):** By calculating a 10-year rolling average, we strip away the short-term chaos. What remains is a smooth, steady upward slope representing the true anthropogenic forcing.
            """)
            
        render_next_button(chapter, page)

    elif page == "1.5 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 2 CONTENT ---
elif chapter == "2. Basics of Global Climate":
    if page == "2.1 Concept: Blackbody Radiation":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.1: The Stefan-Boltzmann Law</h3>
        <p>Everything with a temperature emits radiation. The hotter an object is, the more energy it blasts into space.</p>
        <p>The core equation here is the Stefan-Boltzmann Law. The total energy emitted ($E$) is proportional to the temperature ($T$) raised to the fourth power:</p>
        <p>$$ E = \sigma T^4 $$</p>
        <p>Because of that exponent, temperature changes are incredibly sensitive. If you somehow doubled the temperature of an object, the energy output wouldn't double—it would increase by <b>16 times</b> ($2^4 = 16$).</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.2 Concept: Solar Constant & Albedo":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.2: Incoming Energy and Reflection</h3>
        <p><b>The Solar Constant ($S_0$):</b> The sun blasts the Earth with roughly $1367 \text{ W/m}^2$ of energy. However, because Earth is a sphere (meaning the poles get glancing blows) and half the planet is in nighttime shadow, the average incoming energy at the top of the atmosphere is divided by 4, resulting in about <b>$342 \text{ W/m}^2$</b>. </p>
        <p><b>Albedo ($\alpha$):</b> Not all of that energy is absorbed. Albedo is the fraction of light reflected back into space. Earth's average is about 0.3 (or 30%). White surfaces like ice have high albedo, while dark oceans have low albedo.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.3 Concept: Atmospheric Structure":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.3: Layers of the Sky</h3>
        <p>The atmosphere is not uniform; it is built in distinct layers defined by their temperature profiles.</p>
        <ul>
            <li><b>Troposphere:</b> The lowest layer, where we live and where all weather happens. Here, temperature <b>decreases</b> with height (it gets colder as you climb a mountain). </li>
            <li><b>Stratosphere:</b> The layer above. Paradoxically, temperature <b>increases</b> with height here. This happens because the ozone layer is situated here, actively absorbing high-energy UV radiation from the sun and warming the surrounding air.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.4 Concept: Carbon Reservoirs":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.4: The Big Three Reservoirs</h3>
        <p>Carbon moves through the Earth system via reservoirs. Understanding their scale is crucial:</p>
        <ul>
            <li><b>Deep Ocean:</b> The absolute massive behemoth. It holds the vast majority of the planet's carbon, but the cycle moves incredibly slowly.</li>
            <li><b>Fossil Reserves:</b> Carbon that was "locked away" from the active cycle for millions of years (coal, oil). Humans are currently mining this and forcing it into the active cycle.</li>
            <li><b>Atmosphere:</b> The smallest reservoir. Because it is so small, relatively tiny additions of carbon cause massive fluctuations. It acts as the "control knob" for global temperature.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "2.5 Model: Blackbody Energy Output":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: $T^4$ Sensitivity</h3>
        <p>Let's use Python to visualize how rapidly energy output scales with temperature due to the Stefan-Boltzmann law.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code('''
import pandas as pd
import numpy as np

# Create an array of temperatures from 200 Kelvin to 400 Kelvin
temperatures = np.arange(200, 401, 10) 

# Stefan-Boltzmann Constant
sigma = 5.67e-8 

# Calculate Energy Emitted (E = sigma * T^4)
energy_emitted = sigma * (temperatures ** 4)

# Store in DataFrame
df = pd.DataFrame({'Temperature (K)': temperatures, 'Energy Emitted (W/m2)': energy_emitted})
df.set_index('Temperature (K)', inplace=True)
        ''', language='python')
        
        if st.button("Run Code", type="primary"):
            st.markdown("### Output Analysis:")
            temperatures = np.arange(200, 401, 10) 
            sigma = 5.67e-8 
            energy_emitted = sigma * (temperatures ** 4)
            df = pd.DataFrame({'Temperature (K)': temperatures, 'Energy Emitted (W/m2)': energy_emitted})
            df.set_index('Temperature (K)', inplace=True)
            
            st.line_chart(df)
            
            st.info("""
            **Graph Analysis:**
            Notice the curve of the line. It is not straight. Because energy scales to the fourth power of temperature ($T^4$), as the temperature goes up, the energy emitted skyrockets exponentially. This is the universe's ultimate negative feedback: as Earth gets hotter, it becomes wildly more efficient at blasting heat away into space.
            """)
            
        render_next_button(chapter, page)

    elif page == "2.6 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 3 CONTENT ---
elif chapter == "3. Physical Processes":
    if page == "3.1 Concept: Equation of State":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.1: The Rules of Density</h3>
        <p>The atmosphere and ocean follow strict fluid dynamics. The most basic rule is the <b>Equation of State</b>:</p>
        <p>$$ P = \rho R T $$</p>
        <p>Where $P$ is pressure, $\rho$ is density, $R$ is a gas constant, and $T$ is temperature. This dictates that warm air expands (becomes less dense) and rises, while cold air compresses and sinks.</p>
        <p>In the ocean, there is a massive added variable: <b>Salinity</b>. Cold, salty water is the densest fluid on the planet, driving deep ocean currents.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "3.2 Concept: Geostrophic Balance":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.2: Why Winds Spiral</h3>
        <p>Intuition says wind should blow directly from High Pressure to Low Pressure (the Pressure Gradient Force). But the Earth is spinning, creating the <b>Coriolis Force</b>, which pulls moving air to the side. [Image illustrating the Coriolis Force deflecting wind patterns on Earth]</p>
        <p>In the upper atmosphere, these two forces perfectly counteract each other. The pressure tries to pull the wind inward, and Coriolis pulls it sideways. The result is <b>Geostrophic Balance</b>: the wind flows perfectly <i>around</i> the pressure systems, parallel to the isobars, rather than straight into them.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "3.3 Concept: Friction's Role":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.3: Surface Drag</h3>
        <p>Geostrophic balance breaks down near the Earth's surface. Why? Because of mountains, trees, and buildings.</p>
        <p><b>Friction</b> slows the wind down. Because the Coriolis force depends entirely on wind speed, slower wind means a weaker Coriolis pull. With Coriolis weakened, the Pressure Gradient Force "wins" the tug-of-war, allowing the wind to angle slightly across the isobars and spiral inwards toward the center of the low-pressure system (creating storms).</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "3.4 Concept: Rossby Waves":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 3.4: Teleconnections</h3>
        <p>The high-altitude jet stream does not flow in a perfect, straight circle. It wobbles in giant, meandering loops known as <b>Rossby Waves</b>. </p>
        <p>These planetary-scale waves are the physical mechanism for "teleconnections"—the reason why a localized patch of hot water in the remote Pacific Ocean can alter the flow of the jet stream so drastically that it causes a brutal cold snap in New York.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "3.5 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 4 CONTENT ---
elif chapter == "4. El Niño (ENSO)":
    if page == "4.1 Concept: Normal State":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.1: The Walker Circulation</h3>
        <p>Before understanding El Niño, you must understand the Pacific's normal state.</p>
        <p>Normally, strong Trade Winds blow from East to West across the equator. These winds act like a snowplow, physically pushing warm surface water and piling it up in the Western Pacific (near Indonesia). This massive pile of energy is called the <b>Warm Pool</b>.</p>
        <p>Because the water is pushed West, cold, nutrient-rich deep water is forced to upwell in the East (off the coast of South America) to replace it. </p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "4.2 Concept: El Niño Warm Phase":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.2: The Slosh</h3>
        <p>During an El Niño event, those East-to-West Trade Winds mysteriously collapse or even reverse. </p>
        <p>Without the wind holding it back, that massive "Warm Pool" piled up in Indonesia sloshes entirely back across the Pacific Ocean toward South America. The thermocline (the boundary separating warm surface water from cold deep water) flattens out, completely shutting down the cold water upwelling in the East.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "4.3 Concept: Feedbacks & Oscillators":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 4.3: The Engines of ENSO</h3>
        <p>El Niño is driven by complex feedback loops:</p>
        <ul>
            <li><b>Bjerknes Feedback (The Amplifier):</b> A positive, self-reinforcing loop. Weak winds cause the East Pacific to warm up. This reduces the temperature difference between the East and West. A lower temperature difference causes the winds to weaken <i>even more</i>, causing more warming.</li>
            <li><b>Delayed Oscillator (The Kill Switch):</b> Why doesn't El Niño last forever? When the warm water sloshes East, it sends deep underwater Rossby waves West. These waves hit the coast of Asia, bounce off, transform into Kelvin waves, and travel back East. Months later, they arrive and violently pull the thermocline back up, bringing cold water to the surface and killing the El Niño.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "4.4 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 5 CONTENT ---
elif chapter == "5. Greenhouse Effect & Feedbacks":
    if page == "5.1 Concept: Selective Absorption":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.1: The Greenhouse Trap</h3>
        <p>The core of the greenhouse effect relies on a physics concept called <b>Selective Absorption</b>. [Image explaining the Greenhouse Effect with shortwave and longwave radiation]</p>
        <p>The gases in our atmosphere are mostly transparent to high-energy, high-frequency Shortwave radiation coming from the sun. The sunlight passes right through to the surface.</p>
        <p>However, when the Earth absorbs this light and warms up, it glows by emitting lower-energy Longwave (Infrared) radiation. Greenhouse gases (like $CO_2$, methane, and water vapor) are chemically opaque to this specific frequency. They absorb the infrared heat and re-radiate it back down to the surface, trapping the energy.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "5.2 Concept: Detailed Feedbacks":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 5.2: The Amplifiers</h3>
        <p>CO2 doesn't do all the warming on its own; it triggers secondary mechanisms called feedbacks.</p>
        <ul>
            <li><b>Water Vapor Feedback (Positive/Amplifying):</b> The strongest feedback. As $CO_2$ warms the air, the hotter air causes more ocean evaporation. Water vapor is a potent greenhouse gas, so more water vapor traps more heat, causing even more evaporation.</li>
            <li><b>Lapse Rate Feedback (Negative/Cooling):</b> In the tropics, physics dictates the high upper atmosphere will warm faster than the surface. Because the upper atmosphere has a clearer "view" of space, it becomes highly efficient at radiating heat away, acting as a brake on global warming.</li>
            <li><b>Cloud Feedback (The Wildcard):</b> Clouds are highly complex. Low, thick clouds act as mirrors, reflecting sunlight and cooling the Earth. High, wispy clouds act like blankets, trapping heat. Whether clouds will net-warm or net-cool the planet long-term remains a major area of study.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "5.3 Knowledge Check":
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
            <li><b>Land vs. Ocean:</b> Landmasses warm much faster than oceans. The ocean has an incredibly high heat capacity—meaning it can absorb massive amounts of thermal energy before its temperature actually registers an increase. </li>
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


```
