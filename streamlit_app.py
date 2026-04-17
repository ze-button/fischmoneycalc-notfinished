import streamlit as st
import sympy as sp
import pandas as pd
import io
import requests
import re

# --- CONFIG & HELPERS ---

st.set_page_config(page_title="Fisch Calc", page_icon="🐟")

def get_stat(wiki_text, stat_name):
    """Parses wikitext using logic to match the wiki format in the image."""
    # Wiki format is usually |stat_name = value
    search_term = f"|{stat_name.lower()}"
    
    if search_term in wiki_text.lower():
        try:
            # Split by the term and take the part after the first '='
            after_stat = wiki_text.lower().split(search_term)[1]
            # Get the line and split by newline or the next pipe
            line = after_stat.split("\n")[0].split("|")[0]
            # Clean up equals signs and common wiki formatting
            value = line.replace("=", "").replace("[", "").replace("]", "").strip()
            
            # Extract the first numeric sequence found
            numeric_match = re.search(r"[\d\.]+", value)
            return numeric_match.group(0) if numeric_match else "0"
        except:
            return "0"
    return "0"

def fetch_fish_stats(fish_name):
    if not fish_name:
        return 0.0, 0.0
    
    clean_name = fish_name.strip().title()
    url = "https://fischipedia.org/w/api.php"
    headers = {'User-Agent': 'Fischcalc (contact: your@email.com)'}
    params = {
        "action": "parse",
        "page": clean_name,
        "format": "json",
        "prop": "wikitext",
        "redirects": 1 
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'parse' in data:
                content = data['parse']['wikitext']['*']
                
                # Get XP
                xp = get_stat(content, "xp")
                
                # Try 'prog_speed' first, then 'base_resil' as fallback
                prog = get_stat(content, "prog_speed")
                if prog == "0":
                    prog = get_stat(content, "base_resil")
                
                return float(xp), float(prog)
    except:
        return 0.0, 0.0
    return 0.0, 0.0

# --- UI LAYOUT ---
with st.sidebar:
    st.header("Specifications")
    time_given = st.number_input("Time (seconds)", value=750)
    rod_speed = st.number_input("Rod Prog Speed", value=0.0)
    size_multiplier = st.number_input("Size Multiplier", value=1.0)
    sparkling_chance = st.number_input("Sparkling Chance %", value=1, min_value=1, max_value=100)
    shiny_chance = st.number_input("Shiny Chance %", value=1, min_value=1, max_value=100)
    lure_spd = st.number_input("Lure Speed", value=0.0)
    fish_count = st.number_input("Fish Count", value=3, min_value=1)
    mutation_count = st.number_input("Mutation Count", value=3, min_value=1)
    
    glitch_pot = st.selectbox("Glitch Potion?", options=["No", "Yes"])
    passive_specification = st.selectbox(
        "Rod Passive (WIP)",
        options=["None", "Dead Man's Rod", "Ruinous", "Onirifalx", "Luminescent", "Seraphic", "Wind Elemental", "Plaguereaver", "Dreambreaker", "Fabulous"]
    )
    rod_name = st.text_input("Rod Name")
    xp_multi1 = st.number_input("XP Multiplier 1", value=1, min_value=1)
    xp_multi2 = st.number_input("XP Multiplier 2", value=1, min_value=1)
    xp_multi3 = st.number_input("XP Multiplier 3", value=1, min_value=1)
    xp_multi4 = st.number_input("XP Multiplier 4", value=1, min_value=1)

col1, col2 = st.columns(2)

# --- FISH INPUTS ---
with col1:
    st.subheader("Fish Stats")
    fish_data = []
    for i in range(fish_count):
        cols = st.columns(3)
        f_chance = cols[0].number_input(f"Fish {i+1} %", value=0.0, key=f"fch{i}")
        f_name = cols[1].text_input(f"Fish {i+1} name", key=f"fname{i}")
        f_val_input = cols[2].number_input(f"Fish {i+1} C$", value=0.0, key=f"fval{i}")
        
        xp_val, prog_val = 0.0, 0.0
        if f_name:
            xp_val, prog_val = fetch_fish_stats(f_name)
            if xp_val > 0 or prog_val > 0:
                st.caption(f"✅ Found: {xp_val} XP, {prog_val} Speed/Resil")
            else:
                st.caption("⚠️ Wiki data not found or zero. Using 0.")
            
        fish_data.append((f_chance, f_name, xp_val, prog_val, f_val_input))

# --- MUTATION INPUTS ---
with col2:
    st.subheader("Mutations")
    mutation_data = []
    for i in range(mutation_count):
        cols = st.columns(2)
        m_chance = cols[0].number_input(f"Mut {i+1} %", value=0.0, step=0.01, format="%.2f", key=f"mch{i}")
        m_mult = cols[1].number_input(f"Mut {i+1} Mult", value=0.0, key=f"mval{i}")
        mutation_data.append((m_chance, m_mult))

# --- RAW SUMS ---
st.divider()
sum_fish_xp = sum(f[2] for f in fish_data)
sum_fish_speed = sum(f[3] for f in fish_data)

st.columns(2)[0].metric("Sum Fish XP", sum_fish_xp)
st.columns(2)[1].metric("Sum Speed/Resil", sum_fish_speed)

# --- CALCULATOR LOGIC ---
row2_col2 = st.columns([1, 1, 1])[1]

with row2_col2:
    run_calc = st.button("RUN CALCULATOR", type="primary", use_container_width=True, key="main_calc_btn")

if run_calc:
    # weighted averages based on chance
    average_fish_value = sum(f[0] * f[4] for f in fish_data) / 100
    average_fish_prog_speed = sum(f[0] * f[3] for f in fish_data) / 100
    average_fish_xp = sum(f[0] * f[2] for f in fish_data) / 100

    specific_name = passive_specification if passive_specification != "None" else rod_name
    
    sparkling_chance_final = (sparkling_chance * 0.85)/100 + 1
    shiny_chance_final = (shiny_chance * 0.85)/100 + 1
    lure_speed_calc = max(0, 1-(lure_spd/100))

    total_xp_multip = xp_multi1 * xp_multi2 * xp_multi3 * xp_multi4
    no_mut = 100 - (sum(m[0] for m in mutation_data))/100

    average_mutation_multiplier = (sum(m[0] * m[1] for m in mutation_data)/100) + no_mut
    total_lure_speed = rod_speed + average_fish_prog_speed
    total_xp = total_xp_multip * average_fish_xp

    # Sympy solver logic
    x = sp.symbols('x', real=True)
    r_x = (6.8 / (1 + (total_lure_speed + (5 * x)) / 100)) * ((80-4*2*(0.5+0.8*x))/80)**x - x
    d_x = (6.8 / (1 + ((total_lure_speed / 100)))) * (73.35/80)**x - x
    f_x = (6.8 / (1 + (total_lure_speed + 33*x))) * (78.5/80)**x - x

    def solve_safely(equation, symbol, guess=5.0):
        try:
            sol = sp.nsolve(equation, symbol, guess)
            return float(sol)
        except:
            return 6.8 / ((total_lure_speed / 100) + 1) 
    
    if passive_specification == "Ruinous":
        time_to_catch_formula = solve_safely(r_x, x)
    elif passive_specification == "Dreambreaker":
        time_to_catch_formula = solve_safely(d_x, x)
    elif passive_specification == "Fabulous":
        time_to_catch_formula = solve_safely(f_x, x)
    else:
        time_to_catch_formula = (6.8 / ((total_lure_speed / 100) + 1))

    passives_exponent = 1.0
    if passive_specification == "Ruinous": passives_exponent = ((0.15*(20/80))+(0.85))
    elif passive_specification == "Wind Elemental": passives_exponent = (50/80)
    elif passive_specification == "Luminescent": passives_exponent = ((0.15*(60/80)+(0.85)))
    elif passive_specification == "Seraphic": passives_exponent = (40/80)
    elif passive_specification == "Onirifalx": passives_exponent = ((50/80*0.3)+0.7)
    elif passive_specification == "Dead Man's Rod": passives_exponent = (40/80)
    elif passive_specification == "Plaguereaver": passives_exponent = (40/80)
        
    glitch = 2 if glitch_pot == "Yes" else 1

    value_multiplier = average_mutation_multiplier * size_multiplier * shiny_chance_final * sparkling_chance_final
    time_to_catch = (time_to_catch_formula * passives_exponent) + 1.2 + 1 + lure_speed_calc
    catches = time_given / time_to_catch
    total_money_made = (average_fish_value * value_multiplier) * catches * glitch
    average_fish_final_value = average_fish_value * value_multiplier
    xp_final = total_xp * catches

    st.divider()
    st.metric(f"Total Money made with {specific_name}:" , f"{total_money_made:,.0f} C$")
    st.write(f"**Total XP Made:** {xp_final:.2f}")
    st.write(f"**Total Catches:** {catches:.1f}")
    st.write(f"**Catch Speed:** {time_to_catch:.2f}s")
    st.write(f"**Average Fish Value:** {average_fish_final_value:.2f}")
    
    if sum(f[0] for f in fish_data) > 100: st.warning("TOTAL FISH CHANCE EXCEEDS 100%")
    if sum(m[0] for m in mutation_data) > 100: st.warning("TOTAL MUTATION CHANCE EXCEEDS 100%")

    # Excel Export
    export_data = {
        "Stat": ["Rod","TotalMoney", "TotalCatches", "TimeGiven", "CatchSpeed", "AvgFishVal"],
        "Value": [specific_name, total_money_made, catches, time_given, time_to_catch, average_fish_final_value]
    }
    df = pd.DataFrame(export_data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    st.download_button(label="Download Excel File", data=buffer.getvalue(), file_name="fischcalc.xlsx")
