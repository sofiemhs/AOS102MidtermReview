import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Climate Science Terminal v2.0", page_icon="💻", layout="wide")

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
    "1. The Signal and the Noise": {
        "pages": ["1.1 Concept: Weather vs Climate", "1.2 Model: Smoothing Data", "1.3 Knowledge Check"],
        "quiz_pool": [
            {"q": "What type of variability is El Niño considered?", "opts": ["Natural External", "Anthropogenic", "Internal Variability"], "ans": "Internal Variability"},
            {"q": "If a volcano erupts and cools the Earth, what kind of forcing is this?", "opts": ["Internal", "Natural External", "Anthropogenic"], "ans": "Natural External"},
            {"q": "Why do we use paleoclimate proxies like ice cores?", "opts": ["To measure modern CO2", "To establish a baseline of natural climate history", "To predict weather"], "ans": "To establish a baseline of natural climate history"},
            {"q": "What defines 'climate' as opposed to 'weather'?", "opts": ["Weather is a boundary value problem, climate is chaotic.", "Climate is the statistical average of weather over long periods.", "There is no difference."], "ans": "Climate is the statistical average of weather over long periods."},
            {"q": "What is Anthropogenic Forcing?", "opts": ["Human-caused changes like greenhouse gas emissions.", "Volcanic activity.", "Orbital wobbles."], "ans": "Human-caused changes like greenhouse gas emissions."},
            {"q": "Why do we use moving averages on temperature data?", "opts": ["To create noise.", "To smooth out high-frequency internal variability.", "To calculate the Coriolis effect."], "ans": "To smooth out high-frequency internal variability."},
            {"q": "Which of these is an example of a paleoclimate proxy?", "opts": ["Satellites", "Tree rings and ice cores", "Thermometers"], "ans": "Tree rings and ice cores"},
            {"q": "What does a 40-year moving average accomplish?", "opts": ["It reveals the underlying long-term trend by hiding short-term spikes.", "It perfectly predicts the next 40 years.", "It cools the data."], "ans": "It reveals the underlying long-term trend by hiding short-term spikes."},
            {"q": "Is the Earth's orbit considered an internal or external forcing?", "opts": ["Internal", "External", "Neither"], "ans": "External"},
            {"q": "If a dataset has high variance year-to-year, it is considered to have high:", "opts": ["Signal", "Noise", "Equilibrium"], "ans": "Noise"}
        ]
    },
    "2. The Energy Engine": {
        "pages": ["2.1 Concept: Radiative Balance", "2.2 Concept: Ocean Plungers", "2.3 Knowledge Check"],
        "quiz_pool": [
            {"q": "What type of radiation does the Earth emit back into space?", "opts": ["Shortwave solar", "Longwave Blackbody (Infrared)", "Microwave"], "ans": "Longwave Blackbody (Infrared)"},
            {"q": "What drives the ocean's deep Thermohaline Circulation?", "opts": ["Wind", "Lunar tides", "Water density differences (temperature and salinity)"], "ans": "Water density differences (temperature and salinity)"},
            {"q": "Why is there a massive heat transport from the equator to the poles?", "opts": ["To maintain global energy balance", "Because wind only blows North", "Because poles are closer to the sun"], "ans": "To maintain global energy balance"},
            {"q": "What is a Hadley Cell?", "opts": ["A battery", "An atmospheric circulation loop rising at the equator", "A deep ocean trench"], "ans": "An atmospheric circulation loop rising at the equator"},
            {"q": "What makes ocean water denser?", "opts": ["Being warm and fresh", "Being cold and salty", "Being warm and salty"], "ans": "Being cold and salty"},
            {"q": "Where does most deep water formation occur?", "opts": ["The equator", "Near Greenland and Antarctica", "The Mediterranean"], "ans": "Near Greenland and Antarctica"},
            {"q": "Shortwave radiation primarily comes from:", "opts": ["The Earth's core", "The Sun", "Greenhouse gases"], "ans": "The Sun"},
            {"q": "What happens if the Earth absorbs more energy than it emits?", "opts": ["The planet cools", "The planet warms", "Nothing"], "ans": "The planet warms"},
            {"q": "Thermohaline circulation is also known as:", "opts": ["The Jet Stream", "The Global Ocean Conveyor Belt", "The Trade Winds"], "ans": "The Global Ocean Conveyor Belt"},
            {"q": "What limits the Earth from boiling at the equator?", "opts": ["Clouds only", "Heat transport via oceans and atmosphere", "The moon"], "ans": "Heat transport via oceans and atmosphere"}
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
if chapter == "1. The Signal and the Noise":
    if page == "1.1 Concept: Weather vs Climate":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.1: Defining the Parameters</h3>
        <p>Your mentor drops a dataset on your desk. "Separate the noise from the signal," she says.</p>
        <p><b>Weather</b> is highly chaotic—a boundary value problem. You want to know if it will rain exactly at 3 PM on Tuesday. <b>Climate</b>, however, is the statistical average of that weather over long periods (usually 30 years).</p>
        <p>Climate variability comes in three forms:</p>
        <ul>
            <li><b>Internal Variability:</b> Natural wobbles in the system, like El Niño, that move heat around but don't add new energy.</li>
            <li><b>Natural External Forcing:</b> Volcanoes blocking the sun or orbital shifts changing solar input.</li>
            <li><b>Anthropogenic Forcing:</b> Human activity, specifically burning trace greenhouse gases.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)

    elif page == "1.2 Model: Smoothing Data":
        st.markdown("""
        <div class="lesson-card">
        <h3>Modeling Bay: Moving Averages</h3>
        <p>To see the Anthropogenic trend (the signal), we must smooth out the internal variability (the noise). Watch what happens to the raw data when we apply a 10-year moving average in Python.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display the code with heavily commented line-by-line explanations
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
        
        # Only run and display the graph when the user explicitly clicks the button
        if st.button("Run Code", type="primary"):
            st.markdown("### Output Analysis:")
            years = np.arange(1970, 2020)
            np.random.seed(42) # Set a fixed random seed so the graph output looks identical every time it runs
            noise = np.random.normal(0, 0.4, len(years))
            signal = 0.02 * (years - 1970) 
            raw_temp = signal + noise
            df = pd.DataFrame({'Raw Temp (Noise)': raw_temp}, index=years)
            df['Smoothed Trend (Signal)'] = df['Raw Temp (Noise)'].rolling(window=10, center=True).mean()
            
            st.line_chart(df)
            
        render_next_button(chapter, page)

    elif page == "1.3 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- CHAPTER 2 CONTENT ---
elif chapter == "2. The Energy Engine":
    if page == "2.1 Concept: Radiative Balance":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.1: The Gradient</h3>
        <p>The Earth absorbs high-frequency Solar <b>shortwave radiation</b> and glows with invisible, low-frequency <b>longwave radiation (Infrared)</b>.</p>
        <p>Because the Earth is a sphere, sunlight hits the equator directly but grazes the poles. This creates a massive energy imbalance called the <b>Radiative Gradient</b>. If heat didn't move, the equator would literally boil.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "2.2 Concept: Ocean Plungers":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.2: Thermohaline Circulation</h3>
        <p>To fix the Radiative Gradient, the planet uses engines to move heat poleward.</p>
        <p>The Ocean uses <b>Thermohaline Circulation</b>. Water density is driven by temperature (Thermo) and salt (Haline). Near Greenland, water becomes incredibly cold and salty, making it dense. It sinks to the bottom of the ocean, acting like a giant plunger that constantly pulls warm surface water up from the equator to replace it.</p>
        </div>
        """, unsafe_allow_html=True)
        render_next_button(chapter, page)
        
    elif page == "2.3 Knowledge Check":
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=5)

# --- FINAL EXAM ---
elif chapter == "Final Exam: Terminal Clearance":
    if page == "Final Knowledge Check":
        st.warning("WARNING: This is the final evaluation. Questions are pulled from all previous databanks.")
        run_quiz(chapter, CURRICULUM[chapter]["quiz_pool"], required_score=10)
