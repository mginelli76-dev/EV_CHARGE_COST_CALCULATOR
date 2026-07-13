import streamlit as st
from PIL import Image

with st.sidebar:
    st.title("Seguimi sui Social")
    st.write("Resta aggiornato sui miei test sulla Hyundai Inster:")
    st.link_button("YouTube", "https://youtube.com/@mginelli76?si=iuRHNZE4UOnIbivr")
    st.link_button("Instagram", "https://instagram.com/ocramgy/")
    st.link_button("TikTok", "https://www.tiktok.com/@ocramgy76?lang=en")
    st.link_button("Facebook", "https://facebook.com/marcoginelli")

# Tenta di caricare l'immagine se presente nella stessa cartella
try:
    image = Image.open('logo MGY social.jpg')
    st.image(image, width=200)
except:
    pass

st.title("EV CHARGE COST & TIME CALCULATOR powered by MGY")
st.write("Real Efficiency & Time Calculator - Calcolatore ricarica EV con efficienza e tempi reali offerto da MGY")

cap = st.number_input("Capacita Batteria (kWh)", value=49.0, step=1.0)

profilo = st.selectbox("Type - Tipo di ricarica", ["Home - Casa", "Charging Station - Colonnina (92% eff.)"])

# Inizializzazione variabili potenza teorica
kw_teorici = 0.0

if "Home" in profilo:
    prezzo_default = 0.192

    label_6  = "6A  (~1.38 kW) - Efficienza 85.5%"
    label_8  = "8A  (~1.84 kW) - Efficienza 89.1%"
    label_10 = "10A (~2.30 kW) - Efficienza 91.3%"
    label_12 = "12A (~2.76 kW) - Efficienza 92.7%"

    ampere_labels = [label_6, label_8, label_10, label_12]
    ampere_eff    = [0.855,   0.891,   0.913,    0.927]
    ampere_kw     = [1.38,    1.84,    2.30,     2.76]

    ampere_scelta = st.selectbox("Charging Ampere - Ampere di ricarica", ampere_labels, index=1)
    idx = ampere_labels.index(ampere_scelta)
    eff = ampere_eff[idx]
    kw_teorici = ampere_kw[idx]

else:
    prezzo_default = 0.81
    eff = 0.92
    # Per le colonnine chiediamo la potenza (es. 7, 11, 22 o DC)
    kw_teorici = st.number_input("Potenza Colonnina (kW)", value=11.0, step=1.0)

if "ultimo_profilo" not in st.session_state or st.session_state.ultimo_profilo != profilo:
    st.session_state.ultimo_profilo = profilo
    st.session_state.prezzo_input = prezzo_default

prezzo = st.number_input(
    "Real Price - Inserire Costo reale (EUR/kWh)",
    value=st.session_state.prezzo_input,
    format="%.3f",
    key="prezzo_input"
)

col1, col2 = st.columns(2)
with col1:
    inizio = st.number_input("Battery Level Start (%)", value=20, min_value=0, max_value=100)
with col2:
    fine = st.number_input("Battery Level End (%)", value=80, min_value=0, max_value=100)

if st.button("Calculate now - CALCOLA ORA", use_container_width=True):
    if fine <= inizio:
        st.error("La percentuale finale deve essere maggiore!")
    else:
        # Calcolo energia
        kwh_netti  = ((fine - inizio) / 100) * cap
        kwh_pagati = kwh_netti / eff
        costo      = kwh_pagati * prezzo

        # Calcolo tempo reale lineare
        kw_reali = kw_teorici * eff
        ore_totali = kwh_netti / kw_reali
        
        # Correzione curva di rallentamento sopra l'85% ricalibrata sui 7h 50m (66%->100% @ 12A)
        if fine > 85:
            quota_finale = (fine - max(85, inizio)) / 100
            kwh_rallentati = quota_finale * cap
            # Coefficiente adattato empiricamente per compensare il forte calo di potenza a fine carica
            ore_totali += (kwh_rallentati / kw_reali) * 0.58

        ore = int(ore_totali)
        minuti = int((ore_totali - ore) * 60)

        st.divider()
        
        # Mostra i risultati principali
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Costo Totale", f"EUR {costo:.2f}")
        with c2:
            st.metric("Tempo Stimato", f"{ore}h {minuti}m")

        if "Home" in profilo:
            dettaglio = "Home " + ampere_scelta + " - Efficienza " + str(round(eff * 100, 1)) + "%"
        else:
            dettaglio = f"Charging Station ({kw_teorici} kW) - Efficienza 92%"

        st.info(
            "Dettagli Tecnici:\n" +
            "- Profilo: " + dettaglio + "\n" +
            "- Energia netta in batteria: " + str(round(kwh_netti, 2)) + " kWh\n" +
            "- Energia pagata alla rete: " + str(round(kwh_pagati, 2)) + " kWh\n" +
            "- Potenza reale di carica: " + str(round(kw_reali, 2)) + " kW"
        )
