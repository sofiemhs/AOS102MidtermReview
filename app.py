import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import os

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Climate Science Terminal v4.0", page_icon="💻", layout="wide")

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

# --- IMAGE HELPER ---
def display_image(image_name, caption):
    try:
        st.image(image_name, caption=caption, use_container_width=True)
    except:
        st.markdown(f"*(Please upload **{image_name}** to your repository to view the diagram: {caption})*")

# ==========================================
# CURRICULUM DATA STRUCTURE
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
            {"q": "In the global average energy budget, what is the exact Incoming Solar Radiation?", "opts": ["235 Wm-2", "342 Wm-2", "107 Wm-2"], "ans": "342 Wm-2"},
            {"q": "How much solar radiation is reflected back to space by clouds, aerosols, atmosphere, and surface combined?", "opts": ["168 Wm-2", "107 Wm-2", "40 Wm-2"], "ans": "107 Wm-2"},
            {"q": "What defines 'Radiative Forcing'?", "opts": ["Top-of-atmosphere initial imbalance in the energy budget due to change in GHG or aerosols.", "The physical push of wind on the ocean.", "The amount of rain falling in California."], "ans": "Top-of-atmosphere initial imbalance in the energy budget due to change in GHG or aerosols."},
            {"q": "What are the three roles for clouds and convection?", "opts": ["Heating the atmosphere, reflecting solar radiation, and trapping infrared radiation.", "Creating wind, destroying ozone, and melting ice.", "There are no roles."], "ans": "Heating the atmosphere, reflecting solar radiation, and trapping infrared radiation."},
            {"q": "According to the professor, what is the anthropogenic emission breakdown?", "opts": ["8 PgC/yr total (6.4 fossil fuels/cement + 1.6 land use change).", "100 PgC/yr from volcanoes.", "Zero emissions."], "ans": "8 PgC/yr total (6.4 fossil fuels/cement + 1.6 land use change)."},
            {"q": "How much of the anthropogenic carbon remains in the atmosphere?", "opts": ["100%", "Only ~half remains in the atmosphere (time dependent).", "None of it."], "ans": "Only ~half remains in the atmosphere (time dependent)."},
            {"q": "What happens if human greenhouse gas emissions remain perfectly constant over time?", "opts": ["Ongoing increase of concentration.", "Concentration decreases.", "Concentration stays perfectly flat."], "ans": "Ongoing increase of concentration."}
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
    
    # Cap required score to avoid crashing if pool is smaller than 5
    req_score = min(required_score, len(pool))
    
    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = random.sample(pool, req_score)
    
    active_questions = st.session_state[quiz_key]
    
    st.markdown(f"### ⚠️ MISSION CLEARANCE: {chapter_name}")
    st.write(f"Pass mark: {req_score}/{req_score}. Questions are randomized from the databanks.")
    
    with st.form(f"form_{chapter_name}"):
        user_answers = []
        for i, qa in enumerate(active_questions):
            st.write(f"**{i+1}. {qa['q']}**")
            ans = st.radio(f"q{i}", qa['opts'], key=f"ans_{chapter_name}_{i}", label_visibility="collapsed")
            user_answers.append(ans)
            st.write("---")
            
        if st.form_submit_button("Submit Analysis"):
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
        display_image("midterm_california_precip.png", "Histogram of California winter precipitation (1895-2014) - Seager et al., 2014")
        render_next_button(chapter, page)

    elif page == "1.3 Concept: Trace Gases & Warming":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 1.3: Drivers of Variation & Trace Gases</h3>
        <p>Trace gases absorb infrared radiation at wavelengths where $O_2$ and $N_2$ are ineffective, altering the Earth's energy budget. The main drivers evaluated in the review include:</p>
        <ul>
            <li><b>Carbon Dioxide ($CO_2$):</b> The main greenhouse gas responsible for observed warming since the industrial revolution.</li>
            <li><b>Methane ($CH_4$):</b> Sourced from cattle, sheep, rice paddies, fossil fuel by-products, wetlands, and termites (measured in parts per billion).</li>
            <li><b>Nitrous Oxide ($N_2O$):</b> Driven by biomass burning and fertilizers (ppb).</li>
            <li><b>Chlorofluorocarbons (CFCs):</b> Man-made chemicals that were exactly zero before 1950 (measured in parts per trillion).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        display_image("midterm_keeling_curve.png", "Carbon dioxide concentrations since 1958 at Mauna Loa")
        display_image("midterm_trace_gases.png", "Concentration of various trace gases estimated since 1850")
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
        display_image("midterm_temp_anomaly.png", "Global mean surface temperatures estimated since preindustrial times")
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
            <li><b>Incoming Solar Radiation:</b> 342 $Wm^{-2}$</li>
            <li><b>Reflected Solar Radiation:</b> 107 $Wm^{-2}$ total. (77 $Wm^{-2}$ reflected by Clouds, Aerosols, and Atmosphere; 30 $Wm^{-2}$ reflected by the Surface).</li>
            <li><b>Absorbed by Surface:</b> 168 $Wm^{-2}$</li>
            <li><b>Outgoing Longwave Radiation:</b> 235 $Wm^{-2}$ (195 emitted by atm, 40 atmospheric window)</li>
            <li><b>Back Radiation (Absorbed by Surface):</b> 324 $Wm^{-2}$</li>
            <li><b>Surface Radiation Emitted:</b> 390 $Wm^{-2}$</li>
            <li><b>Latent Heat:</b> 78 $Wm^{-2}$</li>
            <li><b>Thermals:</b> 24 $Wm^{-2}$</li>
        </ul>
        <p>The upward IR from the surface is mostly trapped in the atmosphere, rather than escaping directly to space, so it tends to heat the atmosphere. The atmosphere emits both upward and downward, returning energy back down to the surface, resulting in additional warming (The Greenhouse Effect).</p>
        </div>
        """, unsafe_allow_html=True)
        display_image("midterm_energy_budget.png", "Pathways of energy transfer in a global average")
        render_next_button(chapter, page)

    elif page == "2.2 Concept: Blackbody & Radiative Forcing":
        st.markdown("""
        <div class="lesson-card">
        <h3>Log Entry 2.2: Radiative Forcing Imbalance</h3>
        <p><b>Blackbody Radiation:</b> Total energy flux integrated across all wavelengths of light is $R = \sigma T^4$. Infrared emissions depend heavily on the Earth's temperature.</p>
        <p><b>Radiative Forcing:</b> The midterm review defines this as the "Top-of-atmosphere initial imbalance in the energy budget due to: change in GHG (trapping infrared radiation) &/or aerosols (reflecting solar radiation)".</p>
        <p>Anthropogenic aerosols reflect more sunlight, generating a forcing that tends to reduce the incoming 107 $Wm^{-2}$ baseline. GHGs trap IR, dropping the outgoing radiation below 235 $Wm^{-2}$ <i>before</i> the temperature increases. To reach equilibrium, temperature increases until top of atmosphere IR again balances net solar.</p>
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
        <h3>Modeling Bay: Visualizing the $Wm^{-2}$ Data</h3>
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
            
        render_next_button(chapter, page)

    elif page == "2.6 Knowledge Check":
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
        <p>In a transient response experiment where greenhouse gas concentrations are capped at time $t_s$, the forcing stabilizes.</p>
        <p>However, temperature was less than equilibrium due to lag, so it continues to rise for ~decades (upper ocean), plus an additional increase on deep ocean timescales. This is known as the constant composition commitment.</p>
        <p>If emissions are not brought down quickly enough, CO2 overshoots stabilization target $\\Rightarrow$ negative emissions are required, i.e. methods for actively removing CO2.</p>
        </div>
        """, unsafe_allow_html=True)
        display_image("midterm_transient_lag.png", "Annual average surface air temp response, Manabe et al 1991")
        render_next_button(chapter, page)

    elif page == "5.4 Knowledge Check":
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
