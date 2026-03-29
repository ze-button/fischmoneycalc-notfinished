import streamlit as st
import sympy as sp
import pandas as pd
import io

st.set_page_config(page_title="Fisch Calc", page_icon="🐟")

st.title("A Simple Fisch Moneymaking Calc")
st.write("Calculate how much you can theoretically make in a set amount of time.")
st.caption("by @ze_button on discord")

# inputs
with st.sidebar:
    st.header("Specifications")
    time_given = st.number_input("Time (seconds)", value=750)
    rod_speed = st.number_input("Rod Prog Speed", value=0)
    size_multiplier = st.number_input("Size Multiplier", value=1.0)
    sparkling_chance = st.number_input("Sparkling Chance %", value=1,min_value=1, max_value=100)
    shiny_chance = st.number_input("Shiny Chance %", value=1,min_value=1, max_value=100)
    lure_spd = st.number_input("Lure Speed", value=0)
    fish_count = st.number_input("Fish Count", value=3)
    mutation_count = st.number_input("Mutation Count", value=3)
    passive_specification = st.selectbox(
    "Rod Passive (WIP)",
    options=["None", "Dead Man's Rod", "Ruinous", "Onirifalx","Luminescent","Seraphic","Wind Elemental","Plaguereaver","Dreambreaker","Fabulous"])
    rod_name = st.text_input("Rod Name")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fish Stats")
    st.caption("Make sure the chances add up to 100%")
    st.caption(" ")
    st.caption(" ")
    st.caption(" ")
    fish_data = []
    for i in range(fish_count):
        column = st.columns(3)
        fih_chance = column[0].number_input(f"Fish {i+1} %", value=0.0, step=0.01, format="%.2f", key=f"fch{i}")
        fih_avg_value = column[1].number_input(f"Fish {i+1} C$", value=0.0, key=f"fval{i}")
        fih_progress_speed = column[2].number_input(f"Fish {i+1} PrgSpd", value=0.0, key=f"fspd{i}")
        fish_data.append((fih_chance, fih_avg_value, fih_progress_speed))

with col2:
    st.subheader("Mutations")
    st.caption("Make sure the chances add up to 100%. The chance of not applying a mutation should be included (x% with a 1x multiplier)")
    mutation_data = []
    for i in range(mutation_count):
        column = st.columns(2)
        mut_chance = column[0].number_input(f"Mut {i+1} %", value=0.0, step=0.01, format="%.2f", key=f"mch{i}")
        mut_value = column[1].number_input(f"Mut {i+1} Mult", value=0.0, key=f"mval{i}")
        mutation_data.append((mut_chance, mut_value))


# math
row1_col1, row1_col2, row1_col3 = st.columns([1, 1, 1])
with row1_col2:
    st.write(" ")


row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])

with row2_col2:

    run_calc = st.button("RUN CALCULATOR", type="primary", use_container_width=True)


if run_calc:
        if passive_specification == "None":
            specific_name = rod_name
        else:
            specific_name = passive_specification
        
        sparkling_chance_final = (sparkling_chance * 0.85)/100 + 1
        shiny_chance_final = (shiny_chance * 0.85)/100 + 1
        lure_speed = max(0,1-(lure_spd/100))
    
        average_fish_value = sum(f[0] * f[1] for f in fish_data)/100
        average_fish_prog_speed = sum(f[0] * f[2] for f in fish_data)/100
        average_mutation_multiplier = sum(m[0] * m[1] for m in mutation_data)/100
        total_lure_speed = rod_speed + average_fish_prog_speed

        #sympy stuff
        x = sp.symbols('x', real=True)
    
        r_x = (6.8 / (1 + (total_lure_speed + (5 * x)) / 100)) * ((80-4*2*(0.5+0.8*x))/80)^x
        solutions_ruinous = sp.solve(r_x - x, x)
        positive_solutions_ruinous = [
        float(sol.evalf()) for sol in solutions_ruinous 
        if sol.is_real and sol > 0]
    
        d_x = (6.8 / (1 + ((total_lure_speed / 100)))) * (73.35/80)^x
        solutions_dreambreaker = sp.solve(d_x - x, x)
        positive_solutions_dreambreaker = [
        float(sol.evalf()) for sol in solutions_dreambreaker 
        if sol.is_real and sol > 0]

        f_x = (6.8/(1+(total_lure_speed + 33*x))) *(78.5/80)^x                               
        solutions_fabulous = sp.solve(f_x - x, x)
        positive_solutions_fabulous = [
        float(sol.evalf()) for sol in solutions_fabulous 
        if sol.is_real and sol > 0]
    
        #passivemulti #REDO ALL THIS
        if passive_specification == "Ruinous":
            passives_exponent=((0.15*(20/80))+(0.85))
        elif passive_specification == "Wind Elemental":
            passives_exponent=(50/80)
        elif passive_specification == "Luminescent":
            passives_exponent=((0.15*(60/80)+(0.85)))
        elif passive_specification == "Seraphic":
            passives_exponent=(40/80)
        elif passive_specification=="Onirifalx":
            passives_exponent=((50/80*0.3)+0.7)
        elif passive_specification=="Dead Man's Rod":
            passives_exponent=(40/80)
        elif passive_specification=="None":
            passives_exponent=1
        elif passive_specification=="Plaguereaver":
            passives_exponent=(40/80)
        elif passive_specification=="Dreambreaker":
            passives_exponent=1

        #timetocatchformula
        if passive_specification == "Ruinous":
            time_to_catch_formula= positive_solutions_ruinous[0]
        elif passive_specification == "Dreambreaker":
            time_to_catch_formula= positive_solutions_dreambreaker[0]
        elif passive_specification == "Fabulous":
            time_to_catch_formula= positive_solutions_fabulous[0]
        else:
            time_to_catch_formula= (6.8 / ((total_lure_speed / 100) + 1))

        #finalstuff
        value_multiplier = average_mutation_multiplier * size_multiplier * shiny_chance_final * sparkling_chance_final
        time_to_catch = (time_to_catch_formula*passives_exponent)+ 1.2 + 1 + lure_speed
        catches = time_given / time_to_catch
        total_money_made = (average_fish_value * value_multiplier) * catches
        average_fish_final_value = average_fish_value * value_multiplier
        st.divider()
        st.metric(f"Total Money made with {specific_name}:" , f"{total_money_made:,.0f} C$")
        if passive_specification != "None":
            st.write(f"({rod_name})")
        st.write(f"**Total Catches:** {catches:.1f}")
        st.write(f"**Catch Speed:** {time_to_catch:.2f}s")
        st.write(f"**Average Fish Value:** {average_fish_final_value:.2f}")

                # export
        # results
        if passive_specification == "None":
            export_data = {
                "Column 1": ["Rod","TotalMoney", "TotalCatches", "TimeGiven", "Time-to-catch", "AvgFishVal", "AvgFishValMultip"],
                "Column 2": [specific_name, total_money_made, catches, time_given, time_to_catch, average_fish_final_value, value_multiplier]
            }
        else:
                        export_data = {
                "Column 1": ["Rod","TotalMoney", "TotalCatches", "TimeGiven", "Time-to-catch", "AvgFishVal", "AvgFishValMultip", "Spec"],
                "Column 2": [specific_name, total_money_made, catches, time_given, time_to_catch, average_fish_final_value, value_multiplier, rod_name]
            }
        df = pd.DataFrame(export_data)

        #dataframetoexcelbuffer
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        #downloadbutton
        st.download_button(
            label="Download Excel File",
            data=buffer.getvalue(),
            file_name="fischcalcbyze.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
