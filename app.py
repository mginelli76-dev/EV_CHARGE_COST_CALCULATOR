import streamlit as st

# Configurazione pagina
st.set_page_config(page_title="Inster Smart Calc", page_icon="⚡")

st.title("⚡ EV CHARGE COST CALCULATOR - Calcola Costo Ricarica")
st.write("Calcolatore ricarica EV con efficienza reale")

# 1. Input Capacità Batteria
cap = st.number_input("Capacità Batteria (kWh)", value=49.0, step=1.0)

# 2. Selezione Profilo
profilo = st.selectbox("Type - Tipo di ricarica", 
                      ["Charging Station - Colonnina (92% eff.)", "Home - Casa (85% eff.)"])

# Imposta valori in base al profilo
if "Charging Station - Colonnina" in profilo:
    prezzo_default = 0.81
    eff = 0.92
else:
    prezzo_default = 0.25
    eff = 0.85

# 3. Altri Input
prezzo = st.number_input("Real Price - Prezzo reale (€/kWh)", value=prezzo_default, format="%.2f")

col1, col2 = st.columns(2)
with col1:
    inizio = st.number_input("Battery Level Start - Batteria Inizio (%)", value=44, min_value=0, max_value=100)
with col2:
    fine = st.number_input("Battery Level End - Batteria Fine (%)", value=80, min_value=0, max_value=100)

# 4. Calcoli
if st.button("Calculate now - CALCOLA ORA", use_container_width=True):
    if fine <= inizio:
        st.error("La percentuale finale deve essere maggiore!")
    else:
        kwh_netti = ((fine - inizio) / 100) * cap
        kwh_pagati = kwh_netti / eff
        costo = kwh_pagati * prezzo
        
        # Risultati grafici
        st.divider()
        st.metric("Costo Totale", f"€ {costo:.2f}")
        
        st.info(f"""
        **Dettagli Tecnici:**
        - Energia in batteria: {kwh_netti:.2f} kWh
        - Energia pagata ({int(eff*100)}% eff): {kwh_pagati:.2f} kWh

        """)

