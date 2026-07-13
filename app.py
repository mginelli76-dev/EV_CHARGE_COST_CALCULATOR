import streamlit as st
from PIL import Image

with st.sidebar:
    st.title("Seguimi sui Social")
    st.write("Resta aggiornato sui miei test sulla Hyundai Inster:")
    st.link_button("YouTube", "https://youtube.com/@mginelli76?si=iuRHNZE4UOnIbivr")
    st.link_button("Instagram", "https://instagram.com/ocramgy/")
    st.link_button("TikTok", "https://www.tiktok.com/@ocramgy76?lang=en")
    st.link_button("Facebook", "https://facebook.com/marcoginelli")

try:
    image = Image.open('logo MGY social.jpg')
    st.image(image, width=200)
except:
    pass

st.title("EV CHARGE COST & TIME CALCULATOR powered by MGY")
st.write("Real Efficiency & Time Calculator - Calcolatore ricarica EV con efficienza e tempi reali offerto da MGY")

cap = st.number_input("Capacita Batteria (kWh)", value=49.0, step=1.0, key="cap_unique_input")

# Mappatura esatta dei profili ricarica
profili_data = {
    "Domestica 6A (~1.38 kW) - Eff. 85.5%": {"kw": 1.38, "eff": 0.855, "prezzo": 0.192},
    "Domestica 8A (~1.84 kW) - Eff. 89.1%": {"kw": 1.84, "eff": 0.891, "prezzo": 0.192},
    "Domestica 10A (~2.30 kW) - Eff. 91.3% (Schuko)": {"kw": 2.30, "eff": 0.913, "prezzo": 0.192},
    "Domestica 12A (~2.76 kW) - Eff. 92.7% (Benchmark MGY)": {"kw": 2.76, "eff": 0.927, "prezzo": 0.192},
    "Domestica 16A (~3.70 kW) - Eff. 92.7% (Limite contatore 3 kW)": {"kw": 3.70, "eff": 0.927, "prezzo": 0.192},
    "Domestica/Wallbox 32A (~7.40 kW) - Eff. 92.0% (Contatore 6+ kW)": {"kw": 7.40, "eff": 0.920, "prezzo": 0.192},
    "Pubblica Standard 16A Trifase (~11.00 kW) - Eff. 92.0%": {"kw": 11.00, "eff": 0.920, "prezzo": 0.65},
    "Pubblica Accelerata 32A Trifase (~22.00 kW) - Eff. 92.0%": {"kw": 22.00, "eff": 0.920, "prezzo": 0.69},
    "Fast DC (50 kW) - Eff. 95.0%": {"kw": 50.00, "eff": 0.950, "prezzo": 0.85},
    "Ultra-Fast DC (100 kW) - Eff. 95.0%": {"kw": 100.00, "eff": 0.950, "prezzo": 0.89},
    "Ultra-Fast DC (150+ kW) - Eff. 95.0%": {"kw": 150.00, "eff": 0.950, "prezzo": 0.89}
}

profilo = st.selectbox("Seleziona il tipo di ricarica", list(profili_data.keys()), index=3, key="profilo_unique_select")

kw = profili_data[profilo]["kw"]
eff = profili_data[profilo]["eff"]
prezzo_def = profili_data[profilo]["prezzo"]

if "ultimo_profilo" not in st.session_state or st.session_state.ultimo_profilo != profilo:
    st.session_state.ultimo_profilo = profilo
    st.session_state.prezzo_input_val = prezzo_def

prezzo = st.number_input(
    "Real Price - Inserire Costo reale (EUR/kWh)",
    value=st.session_state.prezzo_input_val,
    format="%.3f",
    key="prezzo_unique_input"
)

col1, col2 = st.columns(2)
with col1:
    inizio = st.number_input("Battery Level Start (%)", value=20, min_value=0, max_value=100, key="inizio_unique_input")
with col2:
    fine = st.number_input("Battery Level End (%)", value=80, min_value=0, max_value=100, key="fine_unique_input")

if st.button("Calculate now - CALCOLA ORA", use_container_width=True, key="btn_unique_calcola"):
    if fine <= inizio:
        st.error("La percentuale finale deve essere maggiore!")
    else:
        # 1. Calcolo Energia e Costi
        kwh_netti = ((fine - inizio) / 100) * cap
        kwh_pagati = kwh_netti / eff
        costo = kwh_pagati * prezzo

        # Limite hardware di bordo (es. Inster a 11 kW)
        kw_ricarica = 11.00 if "22.00 kW" in profilo else kw
        kw_reali = kw_ricarica * eff

        # 2. Calcolo del Tempo lineare pure
        ore_totali = kwh_netti / kw_reali

        # 3. Bilanciamento per la curva di rallentamento finale oltre l'80%
        if fine > 80:
            quota_critica = (fine - max(80, inizio)) / 100
            kwh_finali = quota_critica * cap
            if kw_ricarica <= 22.0:
                ore_totali += (kwh_finali / cap) * 2.1
            else:
                ore_totali += (kwh_finali / kw_reali) * 1.5

        # Conversione finale al minuto
        minuti_totali = int(round(ore_totali * 60))
        ore = minutes_totali = minuti_totali // 60
        minuti = minuti_totali % 60

        st.divider()
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Costo Totale", f"EUR {costo:.2f}")
        with c2:
            st.metric("Tempo Stimato", f"{ore}h {minuti}m")

        st.info(
            "Dettagli Tecnici:\n" +
            "- Modalità: " + profilo + "\n" +
            "- Energia netta erogata: " + str(round(kwh_netti, 2)) + " kWh\n" +
            "- Energia pagata (con perdite): " + str(round(kwh_pagati, 2)) + " kWh\n" +
            "- Potenza reale di picco: " + str(round(kw_reali, 2)) + " kW"
        )
