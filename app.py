import streamlit as st
from PIL import Image

with st.sidebar:
    st.title("Seguimi sui Social")
    st.write("Resta aggiornato sui miei test sulla Hyundai Inster:")
    st.link_button("YouTube", "https://youtube.com/@mginelli76?si=iuRHNZE4UOnIbivr")
    st.link_button("Instagram", "https://instagram.com/ocramgy/")
    st.link_button("TikTok", "https://www.tiktok.com/@ocramgy76?lang=en")
    st.link_button("Facebook", "https://facebook.com/marcoginelli")

image = Image.open('logo MGY social.jpg')
st.image(image, width=200)

st.title("EV CHARGE COST CALCULATOR powered by MGY")
st.write("Real Efficency Calculator - Calcolatore ricarica EV con efficienza reale offerto da MGY")

cap = st.number_input("Capacita Batteria (kWh)", value=49.0, step=1.0)

profilo = st.selectbox("Type - Tipo di ricarica", ["Home - Casa", "Charging Station - Colonnina (92% eff.)"])

if "Home" in profilo:
    prezzo_default = 0.192

    label_6  = "6A  (~1.38 kW) - Efficienza 85.5%"
    label_8  = "8A  (~1.84 kW) - Efficienza 89.1%"
    label_10 = "10A (~2.30 kW) - Efficienza 91.3%"
    label_12 = "12A (~2.76 kW) - Efficienza 92.7%"

    ampere_labels = [label_6, label_8, label_10, label_12]
    ampere_eff    = [0.855,   0.891,   0.913,    0.927]

    ampere_scelta = st.selectbox("Charging Ampere - Ampere di ricarica", ampere_labels, index=1)
    idx = ampere_labels.index(ampere_scelta)
    eff = ampere_eff[idx]

else:
    prezzo_default = 0.81
    eff = 0.92

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
        kwh_netti  = ((fine - inizio) / 100) * cap
        kwh_pagati = kwh_netti / eff
        costo      = kwh_pagati * prezzo

        st.divider()
        st.metric("Costo Totale", "EUR " + str(round(costo, 2)))

        if "Home" in profilo:
            dettaglio = "Home " + ampere_scelta + " - Efficienza " + str(round(eff * 100, 1)) + "%"
        else:
            dettaglio = "Charging Station - Efficienza 92%"

        st.info(
            "Dettagli Tecnici:\n" +
            "- Profilo: " + dettaglio + "\n" +
            "- Energia netta: " + str(round(kwh_netti, 2)) + " kWh\n" +
            "- Energia pagata (" + str(round(eff * 100, 1)) + "% eff): " + str(round(kwh_pagati, 2)) + " kWh"
        )
