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

    /* Main background - Requested Dark Teal */
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
        border-left: 6px solid #0ea5e9; /* Sky blue accent */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
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
        background-color: #e0f2fe; 
        color: #000000 !important; /* All text black */
        border: 1px solid #bae6fd;
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

# --- SESSION STATE (Progress Tracking & Unlocking) ---
# max_unlocked starts at 0 (Welcome page). Passing a test adds 1.
if 'max_unlocked' not in st.session_state:
    st.session_state.max_unlocked = 0

# --- CHAPTER LIST ---
ALL_CHAPTERS = [
    "Welcome", 
    "1. Overview of Climate Variability", 
    "2. Basics of Global Climate", 
    "3. Physical Processes", 
    "4. El Niño & Predictions", 
    "5. Climate Models", 
    "6. Greenhouse Effect & Feedbacks",
    "7. Global Warming Scenarios",
    "FINAL EXAM 🏆"
]

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 🌍 Course Navigator")
    
    # Calculate progress bar (8 total steps to finish the exam)
    prog_percent = int((st.session_state.max_unlocked / 8) * 100)
    st.progress(prog_percent / 100)
    st.write(f"**Course Mastery:** {prog_percent}%")
    st.write("*(Pass the knowledge check to unlock the next chapter)*")
    st.write("---")
    
    # Only show chapters the user has unlocked
    available_chapters = ALL_CHAPTERS[:st.session_state.max_unlocked + 1]
    
    lesson_choice = st.radio("Select Chapter:", available_chapters)
    
    st.write("---")
    if st.button("Reset Course Progress"):
        st.session_state.max_unlocked = 0
        st.rerun()

# --- HELPER FUNCTION TO UNLOCK NEXT CHAPTER ---
def unlock_next(current_chapter_index):
    if st.session_state.max_unlocked == current_chapter_index:
        st.session_state.max_unlocked += 1
        st.success("✅ Correct! You have unlocked the next chapter.")
        st.balloons()
        st.rerun()
    else:
        st.success("✅ Correct! (You already unlocked the next chapter).")

# ==========================================
# PAGE CONTENT
# ==========================================

if lesson_choice == "Welcome":
    st.title("🌱 Comprehensive Climate Science Guide")
    st.markdown("""
    <div class="lesson-card">
    <h3>Welcome to the No-Nonsense Guide to Climate Physics</h3>
    <p>Think of this app as your personal tutor. We are going to take highly complex physics and break them down so simply that a golden retriever could understand them—without losing any of the actual scientific math and logic you need for your exams.</p>
    <p><b>The Catch:</b> You cannot skip ahead. You must prove you understand the concepts by passing a difficult scenario-based question at the end of each chapter before the next one unlocks.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Chapter 1"):
        if st.session_state.max_unlocked == 0:
            st.session_state.max_unlocked = 1
        st.rerun()

# --- CHAPTER 1 ---
elif lesson_choice == "1. Overview of Climate Variability":
    st.title("Chapter 1: Overview of Climate Variability")
    
    tab1, tab2, tab3 = st.tabs(["Dynamics & Systems", "El Niño & Global Warming", "Paleoclimate & History"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Climate Dynamics and Systems</h3>
        <p><b>Weather vs. Climate:</b> Think of weather as your mood today, and climate as your overall personality. Weather is chaotic and impossible to predict perfectly weeks in advance. Climate, however, is a "Boundary Value Problem." If we know exactly how much energy the sun is giving us, and how much greenhouse gas is trapping it, we can calculate the average temperature of the planet.</p>
        <p><b>The System:</b> The Earth isn't just air. It is a massive, connected machine. The atmosphere (air), hydrosphere (oceans), cryosphere (ice), lithosphere (rocks), and biosphere (plants/animals) are constantly trading heat and chemicals (like CO2). If you tweak the chemistry (Trace Gases), you physically alter how much heat the machine traps.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>The Three Pillars of Variability</h3>
        <p>Why does the temperature change from year to year? It comes down to three things:</p>
        <ul>
            <li><b>1. Internal Variability:</b> The machine wobbling on its own. The ocean and atmosphere slosh back and forth. <b>El Niño</b> is the most famous example. Humans didn't cause it; it's just the Earth's natural heartbeat.</li>
            <li><b>2. Natural External Forcing:</b> Someone outside the machine pushing buttons. This includes massive volcanic eruptions (which block the sun and cool the earth) or Milankovitch cycles (the Earth's orbit slowly changing over thousands of years).</li>
            <li><b>3. Anthropogenic External Forcing:</b> Us. Humans digging up carbon that was buried for millions of years and burning it, adding an artificial blanket to the machine.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="lesson-card">
        <h3>Paleoclimate Variability</h3>
        <p>How do we know the Earth is warming unnaturally if we didn't have thermometers 10,000 years ago? We use <b>Proxies</b>. Think of proxies like nature's tape recorders. By drilling deep into ancient ice cores or looking at tree rings and ocean sediment, we can trap ancient air bubbles and measure exactly how much CO2 was in the air during the last Ice Age. This proves our current warming spike is not part of a natural cycle.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Hard Knowledge Check")
    q1 = st.radio("Scenario: A massive volcano erupts in Iceland, spewing ash into the stratosphere and causing global temperatures to drop by 0.5°C for two years. At the same time, the Pacific Ocean shifts into an El Niño phase, causing a slight warming effect in South America. How do we categorize these two events?", 
                  ["Volcano = Anthropogenic Forcing | El Niño = Internal Variability", 
                   "Volcano = Natural External Forcing | El Niño = Internal Variability", 
                   "Volcano = Internal Variability | El Niño = Natural External Forcing",
                   "Both are Internal Variability"], index=None)
    if st.button("Submit Chapter 1"):
        if q1 == "Volcano = Natural External Forcing | El Niño = Internal Variability": unlock_next(1)
        elif q1 is not None: st.error("Incorrect. Remember: Did the volcano come from INSIDE the climate system's normal sloshing, or did it force a change from outside the atmosphere/ocean loop?")

# --- CHAPTER 2 ---
elif lesson_choice == "2. Basics of Global Climate":
    st.title("Chapter 2: Basics of Global Climate")

    tab1, tab2, tab3 = st.tabs(["Radiative Forcing & Energy", "Circulation Systems", "Carbon Cycle"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Radiative Forcing & The Energy Budget</h3>
        <p><b>Blackbody Radiation:</b> Here is the golden rule of physics: <i>Everything that has a temperature glows.</i> The sun is incredibly hot, so it glows in high-energy "Shortwave" radiation (visible light). The Earth is much cooler, so it glows in invisible, low-energy "Longwave" radiation (Infrared heat). </p>
        <p><b>The Gradients:</b> Because the Earth is a sphere, the Equator gets blasted with direct sunlight, while the North and South poles barely get a glancing blow. If nothing moved, the Equator would boil and the poles would freeze solid to the ocean floor. The entire purpose of wind and ocean currents is to act as a delivery service, taking the excess heat from the Equator and dumping it at the poles.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Atmospheric & Ocean Circulation</h3>
        <p><b>The Atmosphere:</b> Hot air rises at the equator, travels towards the poles, cools, and sinks. This creates giant loops called Hadley Cells.</p>
        <p><b>The Ocean's Conveyor Belt:</b> The ocean has two ways to move water. The surface is blown around by the wind. But the deep ocean relies on the <b>Thermohaline Circulation</b> ("Thermo" = Temp, "Haline" = Salt). Think of it like this: Cold water is heavy. Salty water is heavy. Up near Greenland, the water gets freezing cold and super salty (because when sea ice forms, it leaves the salt behind). This incredibly heavy, cold, salty water sinks to the very bottom of the ocean, acting like a giant plunger pulling warm water up from the equator to replace it.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab3:
        st.markdown("""
        <div class="lesson-card">
        <h3>The Carbon Cycle</h3>
        <p>Carbon isn't evil; it's the building block of life. It cycles naturally: you breathe out CO2, a tree eats it, the tree dies and decomposes, releasing it back. The problem is the <b>Fossil Reserves</b>. Millions of years ago, dead plants got buried deep underground before they could decompose, locking their carbon away and cooling the Earth. Humans are now digging up millions of years worth of locked-away carbon and burning it in a single century, completely overwhelming the atmosphere.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Hard Knowledge Check")
    q2 = st.radio("Scenario: Global warming causes massive amounts of the Greenland ice sheet to melt. This dumps billions of gallons of pure, fresh, cold water into the North Atlantic Ocean. Based on the rules of Thermohaline Circulation, what is the most likely result?", 
                  ["The ocean conveyor belt will speed up, pulling more heat to Europe.", 
                   "The fresh water will make the ocean surface lighter and less salty, preventing it from sinking, which could stall the ocean conveyor belt.", 
                   "The fresh water is cold, so it will instantly sink to the bottom, causing a massive deep-ocean tsunami."], index=None)
    if st.button("Submit Chapter 2"):
        if q2 == "The fresh water will make the ocean surface lighter and less salty, preventing it from sinking, which could stall the ocean conveyor belt.": unlock_next(2)
        elif q2 is not None: st.error("Incorrect. Remember the plunger effect. Water MUST be heavy (salty AND cold) to sink. What happens if you add fresh water?")

# --- CHAPTER 3 ---
elif lesson_choice == "3. Physical Processes":
    st.title("Chapter 3: Physical Processes in the Climate System")

    tab1, tab2, tab3 = st.tabs(["Geostrophic Balance", "Equation of State", "Moist Processes"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Conservation of Momentum & Geostrophic Wind</h3>
        <p><b>Pressure Gradient Force (PGF):</b> Mother nature hates a vacuum. If there is a High pressure area (too much air) and a Low pressure area (too little air), the wind will rush straight from High to Low to balance it out. Simple, right?</p>
        <p><b>The Coriolis Effect:</b> Not so fast. The Earth is spinning. If you try to throw a ball straight across a spinning merry-go-round, the ball looks like it curves. On Earth, the Coriolis effect pulls moving air to the <b>Right</b> in the Northern Hemisphere.</p>
        <p><b>Geostrophic Balance:</b> This is the ultimate tug-of-war. The Low Pressure is pulling the air inward. The Coriolis effect is yanking the air to the Right. When these two forces tie, the wind ends up blowing perfectly sideways, doing laps <b>around</b> the low-pressure center instead of going inside it!</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Equation of State & Continuity</h3>
        <p><b>Equation of State:</b> Everything is connected. For the atmosphere, Pressure = Density × Gas Constant × Temperature ($P = \\rho R T$). If you heat a gas, it expands and becomes less dense.</p>
        <p><b>Continuity (Mass Conservation):</b> You can't create or destroy water. Imagine a traffic jam. If the wind blows surface ocean water away from the coast of California (divergence), that water doesn't leave an empty hole in the ocean. Deep, freezing cold, nutrient-rich water from the bottom of the ocean is sucked up to the surface to replace it. This is called <b>Upwelling</b>.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="lesson-card">
        <h3>Moist Processes & Wave Dynamics</h3>
        <p><b>Latent Heat:</b> When water evaporates, it steals heat from the surface (sweating cools you down). When that invisible water vapor rises into the sky and condenses to form a cloud, it releases that stolen heat back into the air like a bomb. This "latent heat" is the fuel for hurricanes.</p>
        <p><b>Rossby Waves:</b> The atmosphere isn't just wind; it has giant invisible waves. Rossby waves are massive wiggles in the jet stream caused by the rotation of the Earth. They are the reason a storm in the Pacific can cause a freeze in New York days later.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Hard Knowledge Check")
    q3 = st.radio("Scenario: You are a meteorologist in the Northern Hemisphere looking at a weather map. You see a massive Low-Pressure system over Chicago. Because of Geostrophic Balance, what direction is the wind blowing around Chicago?", 
                  ["Straight into the center of Chicago to fill the low pressure.", 
                   "Clockwise around Chicago.", 
                   "Counter-Clockwise around Chicago.",
                   "Straight out of Chicago towards High Pressure."], index=None)
    if st.button("Submit Chapter 3"):
        if q3 == "Counter-Clockwise around Chicago.": unlock_next(3)
        elif q3 is not None: st.error("Incorrect. Imagine the air trying to go straight to the center, but an invisible hand (Coriolis) keeps yanking it to the RIGHT. Trace that path in your mind.")

# --- CHAPTER 4 ---
elif lesson_choice == "4. El Niño & Predictions":
    st.title("Chapter 4: El Niño and Year-to-Year Prediction")

    tab1, tab2 = st.tabs(["The Bjerknes Feedback", "The Delayed Oscillator"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Normal Pacific vs. The Bjerknes Feedback</h3>
        <p><b>Normal State:</b> Normally, the Trade Winds blow hard from East to West across the Pacific. This acts like a leaf blower, pushing all the warm surface water over to Indonesia (the "Warm Pool"). Because the warm water was pushed away, cold water gets sucked up from the deep ocean in South America to replace it (Upwelling).</p>
        <p><b>The Bjerknes Feedback Loop:</b> What happens if the leaf blower stutters? If the Trade Winds weaken, the massive pool of warm water in Indonesia starts sloshing back eastward toward South America. Because the East is getting warmer, the temperature difference between East and West drops. This causes the winds to weaken <b>even more</b>, which lets <b>more</b> warm water slosh East. The rich get richer. This runaway positive feedback loop creates El Niño.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Why does El Niño End? (The Delayed Oscillator)</h3>
        <p>If El Niño is a runaway feedback loop, why doesn't it just get hotter forever? The answer is <b>Ocean Waves</b>. When the winds collapse, they don't just move surface water; they send massive, slow-moving underwater waves (Rossby waves) crashing toward Asia.</p>
        <p>Think of bouncing a rubber ball in a small room. The Rossby wave hits the coast of Asia, reflects off the landmass, turns into a different kind of wave (a Kelvin wave), and slowly travels all the way back across the Pacific. Months later, this wave crashes into South America and violently pushes the warm water back down, resetting the ocean and shutting off El Niño. The "cure" for El Niño was generated the moment it started, it just took months to arrive.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Hard Knowledge Check")
    q4 = st.radio("Based on the Delayed Oscillator theory, what is the ultimate 'killer' of an El Niño event?", 
                  ["The Bjerknes feedback loop eventually reversing itself due to high temperatures.", 
                   "Rossby waves reflecting off the Western boundary (Asia), returning as Kelvin waves, and resetting the thermocline depth.", 
                   "A sudden, unexplained strengthening of the Trade Winds from the East."], index=None)
    if st.button("Submit Chapter 4"):
        if q4 == "Rossby waves reflecting off the Western boundary (Asia), returning as Kelvin waves, and resetting the thermocline depth.": unlock_next(4)
        elif q4 is not None: st.error("Incorrect. El Niño doesn't stop itself. Something physical has to travel across the ocean to shut it down.")

# --- CHAPTER 5 ---
elif lesson_choice == "5. Climate Models":
    st.title("Chapter 5: Climate Models")

    tab1, tab2 = st.tabs(["The Grid", "Parameterization"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Building a Virtual Earth</h3>
        <p><b>GCMs (General Circulation Models):</b> We can't put a thermometer on every single inch of the Earth. Instead, climate scientists chop the Earth's atmosphere and ocean into millions of 3D cubes, exactly like a giant <b>Minecraft world</b>. Inside every single cube, supercomputers calculate the physics (Equation of State, Conservation of Momentum) and pass the wind, heat, and moisture to the cube next door.</p>
        <p><b>Resolution Cost:</b> Why don't we just make the cubes 1 inch wide? Because of math. If you cut the size of a grid cube in half, the computer has to do exponentially more calculations. Running a highly detailed global model takes weeks on the world's most powerful supercomputers.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>The Guessing Game: Parameterization</h3>
        <p>Here is the fatal flaw of the Minecraft earth: What if a real-world object is smaller than your Minecraft block? A typical climate model grid box is 50 miles wide. But a thunderstorm might only be 5 miles wide. The computer <b>literally cannot see the thunderstorm</b>.</p>
        <p>Because clouds are crucial for reflecting heat, scientists have to cheat. They use <b>Parameterization</b>. They write a rule: <i>"Hey computer, if the 50-mile box has 80% humidity and rising air, just pretend there are 10 thunderstorms inside it."</i> We are using large-scale physics (which the model can see) to guess the small-scale physics (which it can't). This is the biggest source of error in climate prediction.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Hard Knowledge Check")
    q5 = st.radio("Scenario: A climate model is doing a terrible job predicting global temperatures. Scientists realize the model is failing to simulate 'cumulus clouds' (fluffy low clouds). Why is the model struggling with this, and how must they fix it?", 
                  ["The equations of physics are wrong. They must rewrite the Equation of State.", 
                   "Cumulus clouds are sub-grid scale (too small for the boxes). They must improve their Parameterization math.", 
                   "The model is running too fast. They must increase the grid box size to 500 miles."], index=None)
    if st.button("Submit Chapter 5"):
        if q5 == "Cumulus clouds are sub-grid scale (too small for the boxes). They must improve their Parameterization math.": unlock_next(5)
        elif q5 is not None: st.error("Incorrect. The physics aren't wrong, the computer is just blind to things smaller than its grid boxes.")

# --- CHAPTER 6 ---
elif lesson_choice == "6. Greenhouse Effect & Feedbacks":
    st.title("Chapter 6: The Greenhouse Effect and Feedbacks")

    tab1, tab2 = st.tabs(["The Blanket", "Feedback Loops"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>The Selective Blanket</h3>
        <p><b>Selective Absorption:</b> Greenhouse gases (like CO2 and Water Vapor) are basically a one-way mirror. When the Sun shines down its shortwave light, the CO2 ignores it. It lets the light pass right through to warm the dirt. But when the warm dirt tries to radiate invisible infrared heat back out to space, the CO2 catches it, absorbs it, and shoots it back down to the ground. The heat checks in, but it doesn't check out.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Climate Feedbacks: The Snowball and the Thermostat</h3>
        <p>If we double CO2, the Earth gets 1°C warmer. That's simple physics. The terror of climate change comes from what happens <i>after</i> that 1 degree.</p>
        <ul>
            <li><b>Water Vapor (The Massive Positive Feedback):</b> The Earth gets 1 degree warmer. Warmer air holds more water vapor (evaporation). But water vapor is the strongest greenhouse gas! So the extra vapor traps MORE heat, causing MORE evaporation. This positive feedback loop amplifies the original warming drastically.</li>
            <li><b>Ice-Albedo (Positive Feedback):</b> Earth warms. White, reflective Arctic ice melts. Dark, heat-absorbing ocean water is exposed. Earth absorbs more heat, melting more ice.</li>
            <li><b>Lapse Rate (Negative Feedback):</b> Finally, a thermostat! As the Earth warms, the very top of the atmosphere warms faster. Because it's higher up, it can easily radiate that excess heat off into deep space, acting as a cooling brake on the whole system.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Hard Knowledge Check")
    q6 = st.radio("Which of the following scenarios describes a NEGATIVE climate feedback loop?", 
                  ["Warmer oceans release trapped methane -> The methane traps more heat -> The oceans get warmer.", 
                   "Higher temperatures increase evaporation -> More water vapor enters the air -> The water vapor traps more heat.", 
                   "Higher temperatures increase evaporation -> This forms massive sheets of bright white low clouds -> The clouds reflect the sun's energy back to space, cooling the Earth."], index=None)
    if st.button("Submit Chapter 6"):
        if q6 == "Higher temperatures increase evaporation -> This forms massive sheets of bright white low clouds -> The clouds reflect the sun's energy back to space, cooling the Earth.": unlock_next(6)
        elif q6 is not None: st.error("Incorrect. A negative feedback is a 'thermostat'. It must OPPOSE the initial change (warming leads to a process that causes cooling).")

# --- CHAPTER 7 ---
elif lesson_choice == "7. Global Warming Scenarios":
    st.title("Chapter 7: Scenarios for Global Warming")

    tab1, tab2 = st.tabs(["Baked-In Warming", "Sea Level & Poles"])
    
    with tab1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Transient vs Equilibrium (Baked-In Warming)</h3>
        <p><b>The Ocean Delay:</b> Imagine putting a giant pot of cold water on a roaring stove. Does it boil instantly? No, water has massive "Heat Capacity"—it takes a long time to warm up. The Earth is the same. The atmosphere is the stove, and the deep ocean is the water. <b>Transient response</b> is the warming we feel right now. <b>Equilibrium response</b> is how hot it will eventually get once the deep ocean finally catches up.</p>
        <p><b>The Commitment:</b> This means if humans stopped burning every drop of fossil fuel today, the planet would <i>still continue to warm for decades</i> because the deep ocean is still soaking up the heat we already put into the blanket.</p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Spatial Patterns: Who Gets Hit Hardest?</h3>
        <p><b>Poleward Amplification:</b> Global warming isn't globally equal. The Arctic is warming drastically faster than the equator. Why? Because of the Ice-Albedo feedback loop. When you replace a mirror (ice) with a black t-shirt (ocean), you heat up incredibly fast.</p>
        <p><b>Sea Level Rise:</b> Two things cause the oceans to rise. 1) Melting land-ice (glaciers sliding into the sea). 2) <b>Thermal Expansion</b>. Just like the Equation of State says, when things get hotter, they expand. Just by warming the ocean, the water physically swells, raising sea levels even if zero ice melted.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧠 Hard Knowledge Check")
    q7 = st.radio("Scenario: A politician argues, 'If we cut carbon emissions to absolute zero tomorrow, global temperatures will immediately start dropping back to normal.' Based on climate physics, why is this statement false?", 
                  ["Because the lapse rate feedback will force the atmosphere to heat up.", 
                   "Because of the Equilibrium Response. The deep ocean has massive heat capacity and is still catching up to the current CO2 levels, guaranteeing decades of 'baked-in' warming.", 
                   "Because clouds will trap the heat forever."], index=None)
    if st.button("Submit Chapter 7"):
        if q7 == "Because of the Equilibrium Response. The deep ocean has massive heat capacity and is still catching up to the current CO2 levels, guaranteeing decades of 'baked-in' warming.": unlock_next(7)
        elif q7 is not None: st.error("Incorrect. Remember the pot of water on the stove analogy.")

# --- FINAL EXAM ---
elif lesson_choice == "FINAL EXAM 🏆":
    st.title("🎓 The Final Climate Mastery Exam")
    st.markdown("""
    <div class="lesson-card">
    <h3 style="color:#e11d48 !important;">Final Assessment</h3>
    <p>You have unlocked the final exam. These 5 questions test your ability to synthesize everything you've learned. You must get a 5/5 to pass the course.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("final_exam"):
        st.write("**1. If a climate model has a grid size of 100x100 miles, what mathematical technique MUST scientists use to account for the evaporation happening from a 2-mile wide lake?**")
        e1 = st.radio("Q1", ["Geostrophic Balance", "Parameterization", "The Delayed Oscillator"], key="e1", label_visibility="collapsed")
        
        st.write("---")
        st.write("**2. Which of the following accurately describes the Bjerknes feedback loop during the onset of El Niño?**")
        e2 = st.radio("Q2", [
            "Trade winds strengthen -> Upwelling increases -> Ocean cools.",
            "Trade winds weaken -> Warm pool moves East -> Temp gradient drops -> Winds weaken further.",
            "Rossby waves reflect off Asia -> Kelvin waves cross the ocean -> Thermocline resets."
        ], key="e2", label_visibility="collapsed")
        
        st.write("---")
        st.write("**3. Why is the water vapor feedback considered a POSITIVE feedback loop?**")
        e3 = st.radio("Q3", [
            "Because water vapor forms clouds that cool the earth.",
            "Because warming causes more evaporation, adding water vapor (a GHG) to the air, which traps more heat.",
            "Because water vapor absorbs shortwave radiation directly from the sun."
        ], key="e3", label_visibility="collapsed")
        
        st.write("---")
        st.write("**4. In the Northern Hemisphere, geostrophic winds blow counter-clockwise around a low-pressure system. What two forces are balancing to cause this?**")
        e4 = st.radio("Q4", [
            "Gravity pulling down vs Pressure pushing up.",
            "Pressure Gradient Force pulling inward vs Coriolis Force pulling to the right.",
            "Latent heat rising vs Cold air sinking."
        ], key="e4", label_visibility="collapsed")
        
        st.write("---")
        st.write("**5. What is the primary physical reason that global sea levels will continue to rise for decades even after emissions are stopped (Thermal Expansion)?**")
        e5 = st.radio("Q5", [
            "The Equation of State dictates that as the ocean slowly absorbs the 'baked-in' atmospheric heat, the water becomes less dense and physically expands.",
            "Sea ice melting displaces more water than land ice.",
            "Increased rainfall from the water vapor feedback adds volume to the ocean."
        ], key="e5", label_visibility="collapsed")
        
        submitted = st.form_submit_button("Submit Final Exam")
        
        if submitted:
            score = 0
            if e1 == "Parameterization": score += 1
            if e2 == "Trade winds weaken -> Warm pool moves East -> Temp gradient drops -> Winds weaken further.": score += 1
            if e3 == "Because warming causes more evaporation, adding water vapor (a GHG) to the air, which traps more heat.": score += 1
            if e4 == "Pressure Gradient Force pulling inward vs Coriolis Force pulling to the right.": score += 1
            if e5 == "The Equation of State dictates that as the ocean slowly absorbs the 'baked-in' atmospheric heat, the water becomes less dense and physically expands.": score += 1
            
            if score == 5:
                st.success(f"Score: {score}/5. OUTSTANDING! You have mastered Climate Dynamics! 🌟🌟🌟")
                st.balloons()
            else:
                st.error(f"Score: {score}/5. You need a perfect 5/5 to graduate. Review your notes and try again!")
