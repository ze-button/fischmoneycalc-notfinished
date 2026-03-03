import streamlit as st

st.set_page_config(page_title="Fisch Calc", page_icon="🐟")

st.title("Fisch Moneymaking Calc")
st.write("Calculate how much you can theoretically make in a set amount of time.")

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
    options=["None", "Luminescent", "Ruinous", "Onirifalx"]
)

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
    
        time_to_catch = ((6.8 / ((total_speed / 100) + 1))*((35/80*0.3)+0.7)) + 1.2 + 1 + lure_speed
        catches = time_given / time_to_catch
        total_money = (avg_f_val * val_mult) * catches
        st.divider()
        st.metric("Total Money", f"{total_money:,.0f} C$")
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
        st.divider()
        st.metric("Total Money", f"{total_money:,.0f} C$")
        st.write(f"**Total Catches:** {catches:.1f}")
        st.write(f"**Catch Speed:** {time_to_catch:.2f}s")
