import streamlit as st
import sympy as sp

st.set_page_config(page_title="Fisch Calc", page_icon="🐟")

st.title("Fisch Moneymaking Calc")
st.write("Calculate how much you can theoretically make in a set amount of time.")
st.caption("by @ze_button on discord")

# inputs
with st.sidebar:
    st.header("Specifications")
    time_given = st.number_input("Time (seconds)", value=750)
    rod_speed = st.number_input("Rod Prog Speed", value=0)
    size_mult = st.number_input("Size Multiplier", value=1.0)
    spark_ch = st.number_input("Sparkling Chance %", value=1)
    shin_ch = st.number_input("Shiny Chance %", value=1)
    lure_spd = st.number_input("Lure Speed", value=0)
    passive_spec = st.selectbox(
    "Rod Passive (WIP)",
    options=["None", "Dead Man's Rod", "Ruinous", "Onirifalx"])
    if passive_spec == "None":
        rod_name = st.text_input("Rod Name")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fish Stats")
    f_data = []
    for i in range(5):
        c = st.columns(3)
        ch = c[0].number_input(f"Fish {i+1} %", value=0.0, step=0.01, format="%.2f", key=f"fch{i}")
        val = c[1].number_input(f"Fish {i+1} C$", value=0.0, key=f"fval{i}")
        spd = c[2].number_input(f"Fish {i+1} PrgSpd", value=0.0, key=f"fspd{i}")
        f_data.append((ch, val, spd))

with col2:
    st.subheader("Mutations")
    m_data = []
    for i in range(5):
        c = st.columns(2)
        m_ch = c[0].number_input(f"Mut {i+1} %", value=0.0, step=0.01, format="%.2f", key=f"mch{i}")
        m_val = c[1].number_input(f"Mut {i+1} Mult", value=0.0, key=f"mval{i}")
        m_data.append((m_ch, m_val))

#mathsfordeadmans
if passive_spec == "Dead Man's Rod":
    if st.button("RUN CALCULATOR", type="primary"):
        spark_m = (spark_ch * 0.85)/100 + 1
        shiny_m = (shin_ch * 0.85)/100 + 1
        lure_speed = max(0,1-(lure_spd/100))
    
        avg_f_val = sum(f[0] * f[1] for f in f_data)/100
        avg_f_speed = sum(f[0] * f[2] for f in f_data)
        avg_mut_m = sum(m[0] * m[1] for m in m_data)/100
    
        val_mult = avg_mut_m * size_mult * shiny_m * spark_m
        total_speed = rod_speed + avg_f_speed
    
        time_to_catch = 6.8 / ((total_speed / 100) + 1 ) * (0.5) + 1.2 + 1 + lure_speed
        catches = time_given / time_to_catch
        total_money = (avg_f_val * val_mult) * catches
        st.divider()
        st.metric("Total Money made with Dead Man's Rod", f"{total_money:,.0f} C$")
        st.write(f"**Total Catches:** {catches:.1f}")
        st.write(f"**Catch Speed:** {time_to_catch:.2f}s")

        
#mathforruinous
if passive_spec == "Ruinous":
    if st.button("RUN CALCULATOR", type="primary"):
        spark_m = (spark_ch * 0.85)/100 + 1
        shiny_m = (shin_ch * 0.85)/100 + 1
        lure_speed = max(0,1-(lure_spd/100))
    
        avg_f_val = sum(f[0] * f[1] for f in f_data)/100
        avg_f_speed = sum(f[0] * f[2] for f in f_data)
        avg_mut_m = sum(m[0] * m[1] for m in m_data)/100
    
        val_mult = avg_mut_m * size_mult * shiny_m * spark_m
        total_speed = rod_speed + avg_f_speed
        
        x = sp.symbols('x') #sympy stuff
        f_x = 6.8 / (1 + (total_speed + 5 * x) / 100)
        solutions = sp.solve(f_x - x, x)
        positive_solutions = [float(sol) for sol in solutions if sol > 0]
        
        time_to_catch = positive_solutions[0] + 1.2 + 1 + lure_speed
        catches = time_given / time_to_catch
        total_money = (avg_f_val * val_mult) * catches
        st.divider()
        st.metric("Total Money made with Ruinous Oath", f"{total_money:,.0f} C$")
        st.write(f"**Total Catches:** {catches:.1f}")
        st.write(f"**Catch Speed:** {time_to_catch:.2f}s")


# mathforonirifalx
if passive_spec == "Onirifalx":
    if st.button("RUN CALCULATOR", type="primary"):
        spark_m = (spark_ch * 0.85)/100 + 1
        shiny_m = (shin_ch * 0.85)/100 + 1
        lure_speed = max(0,1-(lure_spd/100))
    
        avg_f_val = sum(f[0] * f[1] for f in f_data)/100
        avg_f_speed = sum(f[0] * f[2] for f in f_data)
        avg_mut_m = sum(m[0] * m[1] for m in m_data)/100
    
        val_mult = avg_mut_m * size_mult * shiny_m * spark_m
        total_speed = rod_speed + avg_f_speed
    
        time_to_catch = ((6.8 / ((total_speed / 100) + 1))*((45/80*0.3)+0.7)) + 1.2 + 1 + lure_speed
        catches = time_given / time_to_catch
        total_money = (avg_f_val * val_mult) * catches
        st.divider()
        st.metric("Total Money made with Onirifalx", f"{total_money:,.0f} C$")
        st.write(f"**Total Catches:** {catches:.1f}")
        st.write(f"**Catch Speed:** {time_to_catch:.2f}s")

# mathfornone
if passive_spec == "None":
    if st.button("RUN CALCULATOR", type="primary"):
        spark_m = (spark_ch * 0.85)/100 + 1
        shiny_m = (shin_ch * 0.85)/100 + 1
        lure_speed = max(0,1-(lure_spd/100))
    
        avg_f_val = sum(f[0] * f[1] for f in f_data)/100
        avg_f_speed = sum(f[0] * f[2] for f in f_data)
        avg_mut_m = sum(m[0] * m[1] for m in m_data)/100
    
        val_mult = avg_mut_m * size_mult * shiny_m * spark_m
        total_speed = rod_speed + avg_f_speed
    
        time_to_catch = (6.8 / ((total_speed / 100) + 1)) + 1.2 + 1 + lure_speed
        catches = time_given / time_to_catch
        total_money = (avg_f_val * val_mult) * catches
        avg_fish_val = avg_f_val*val_mult
        st.divider()
        st.metric(f"Total Money made with {rod_name}:" , f"{total_money:,.0f} C$")
        st.write(f"**Total Catches:** {catches:.1f}")
        st.write(f"**Catch Speed:** {time_to_catch:.2f}s")
        st.write(f"**Average Fish Value:** {avg_fish_val:.2f}s")
